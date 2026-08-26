# Object and scene contract acceptance

## Goal

Verify schema, revision transactions, migration, grasp compatibility, service behavior, and MoveIt synchronization as one recoverable data path.

## Inputs

- All Phase 03 outputs
- Four legacy object sources
- Phase 02 motion/tool fixtures
- Recorded tracked-object fixtures

## Outputs

- Local object acceptance command
- Golden canonical records and hashes
- Migration reconciliation report
- Crash/concurrency test results
- Container/mount, lease, Git/LFS, outage, and backup-health results
- Planning-scene integration report
- Phase exit record

## Work

1. Run schema valid/invalid fixtures for identity, paths, units, frames, meshes, symmetries, anchors, tool parameters, local references, and evidence.
2. Run staged edit, preview, commit, activate, supersede, cache rebuild, Git clone/LFS restore, writer conflict, activation-journal, and crash-point tests.
3. Run legacy migration dry-run and commit, then compare source counts/fields/assets with target records.
4. Run grasp selection across all four grippers and prove incompatible anchors are rejected before planning.
5. Replay tracked-object fixtures into MoveIt, including fresh, stale, duplicate, attached, detached, and missing-geometry cases.
6. Prove ObjectDB is the sole canonical writer through container mount checks and failed direct-write fixtures from core, perception, and scan-worker.
7. Acquire task and scan leases; test heartbeat, owner/epoch mismatch, clean release, active-task activation block, stale fail-closed behavior, explicit verified release, and global scan exclusivity.
8. Resolve and hash-check an object, restart ObjectDB, and prove that the existing fixture can continue while new resolution/lease acquisition fails until readiness returns.
9. Inject local Git commit and remote push failures. Local commit failure must preserve the previous active pointer; remote failure must preserve local activation and report stale backup health until retry succeeds.
10. Delete and rebuild the search cache, restart the object service, and repeat queries plus scene loads.
11. Publish artifact hashes and one clear phase result.

## Interfaces and data

- Local test runner
- Golden data under test fixtures
- Phase acceptance manifest

## Boundaries

- Does not assess learned perception accuracy
- Does not scan a new object
- Does not perform the 30-trial real task

## Failure behavior

- Any data loss, mutable approved revision, unexplained migration field, cache-as-authority behavior, wrong-tool grasp, or silently removed stale obstacle blocks the phase.

## Acceptance

- All four objects resolve by ID and active revision.
- Every approved asset hash matches.
- Cache rebuild and backup restore preserve results.
- Clean Git/LFS clone reproduces approved bundles and active pointers; excluded scan/cache/log paths are absent.
- Service and CLI operations agree.
- MoveIt scene output matches canonical collision data and track state.
- Lease, outage, sole-writer mount, and backup-health fixtures pass.

## Parallel work

Final packet only.

## What this module needs from me

Nothing unless legacy approval data is contradictory.
