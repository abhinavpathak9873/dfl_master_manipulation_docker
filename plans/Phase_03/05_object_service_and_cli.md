# Typed object service and CLI

## Goal

Provide the always-on ObjectDB service as the only validated read/write path for task code, migration tools, and the local web GUI. Keep storage, leases, activation, and outage behavior explicit.

## Inputs

- File store
- Object schema
- ROS interfaces
- Run records
- Single-operator GUI decision
- ObjectDB image and mount-isolation contract
- Runtime lease IDL

## Outputs

- Object repository library
- Loopback-only FastAPI/HTTP/WebSocket server and companion ROS node in the `objectdb` container
- ROS services for exact resolve/read, revision commit/activation, and runtime lease acquisition/heartbeat/release/inspection
- CLI commands for list, show, validate, stage, diff, approve, activate, archive, rebuild-index, verify, leases, backup-status, staging-usage, export-session, and cleanup-session
- Preview and lock semantics
- Authorization boundary for hardware grasp tests
- Split storage, ROS, scan, and backup health
- Service/CLI contract tests

## Work

1. Keep filesystem validation and transactions in one repository library inside ObjectDB. HTTP routes, ROS services, and CLI clients use the same application service; no other container imports the library to write files directly.
2. Serve HTTP on the container interface while Compose publishes only desktop loopback. Keep browsing and exact object resolution available when ROS, perception, and scan-worker are absent.
3. Make read operations resolve stable object ID plus optional revision and return immutable revision ID, record/asset hashes, Git commit, canonical frame, qualification state, and relative read-only asset references. Default active-revision resolution records the exact result used.
4. Make writes begin in staging with an operation/run ID. Return a preview diff, validation findings, and content hashes before commit.
5. Require explicit approve and activate operations. Revision commit creates a new immutable inactive revision. Activation revalidates, rejects every task lease and every foreign scan lease, verifies that the calling scan session has stopped motion and reached review/qualified state when applicable, replaces `current.json`, and completes the required local Git commit.
6. Implement one task or scan lease per controlling run/session with ID and epoch. Task leases may coexist with draft editing and commit, but any active or stale-unverified task lease blocks activation. One global scan lease excludes every task lease and other physical scan.
7. Heartbeat loss marks a lease stale and blocked. Inspection reports its owner and evidence; only an explicit release after process/hardware diagnostics can clear it.
8. Define outage behavior: a new task requires successful resolve plus lease acquisition; a task that already verified immutable assets may continue if ObjectDB restarts. The client must not switch revisions or use an unverified latest cache.
9. Separate data edits from hardware grasp tests. A test command creates a plan and requires the Phase 05 execution path; its result is appended through a new revision or evidence record.
10. Report Git synchronization as health only. ObjectDB creates local commits and outbox records; `objectdb-sync` holds the GitHub credential and performs remote pushes.
11. Record every committed operation and lease transition in run/event artifacts without recreating a mutable audit database.

## Interfaces and data

- Internal Python repository/application API
- HTTP/WebSocket routes for the local app
- ROS resolve, commit/activate, and lease services from Phase 01
- `dfl-object` CLI
- Preview diff, lock/lease records, and backup/staging health

## Boundaries

- Does not expose direct arbitrary file editing
- Does not implement multi-user authentication
- Does not command hardware outside the Phase 05 contract
- Does not control Compose or mount the Docker socket
- Does not stream large immutable assets when a verified read-only mount is available

## Failure behavior

- Reject invalid schema, missing asset, stale base revision, lock conflict, failed hash, failed fsync/rename, failed local Git commit, active/stale lease, or unauthorized activation.
- Failed commit leaves the active pointer unchanged.
- Remote push failure leaves the local activation valid and reports stale backup health.
- Service restart never clears stale leases or resumes a scan action.

## Acceptance

- CLI and ROS service produce identical results.
- Concurrent edit fixture detects stale-base conflict.
- Crash injection before and after rename preserves a valid active revision.
- GUI fixture cannot bypass preview and validation.
- Every active revision is resolvable by exact ID and hash.
- Core, perception, scan-worker, migration, and GUI fixtures cannot write canonical files except through ObjectDB.
- Active and stale-unverified task leases block activation; clean terminal release permits it.
- Resolved task fixture continues with the same hashes through ObjectDB restart, while a new task fails until resolve/lease health recovers.
- HTTP remains healthy for browsing when ROS is absent, and its health response marks ROS/scan unavailable without claiming full readiness.

## Parallel work

Follows store acceptance. Scene read integration can use a read-only repository stub.

## What this module needs from me

Nothing.
