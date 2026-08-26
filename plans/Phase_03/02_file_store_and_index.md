# File store, revisions, and rebuildable index

## Goal

Implement the nested `dfl_object_db` data repository with immutable approved revisions, atomic active pointers, path-limited local Git commits, staging, locking, and a disposable search cache.

## Inputs

- Canonical object schema
- Persistent mount contract
- Run records and error types
- Legacy content-addressed assets

## Outputs

- Object directory layout
- Staging and approval transaction design
- Active-revision pointer format
- Filesystem lock and crash-recovery policy
- Rebuildable SQLite read index under `.cache`
- Git/LFS tracking and approved-bundle inclusion policy
- Local commit transaction and remote-sync outbox/status records
- Export, validation, clone/restore-check, and staging-quota commands

## Work

1. Clone the private `dfl_object_db` repository at the configured external ObjectDB durable root, independent of the parent toolbox source history. Do not add a tracked root-level `data/` directory. Store each object under `objects/<object_id>/revisions/<revision_id>/` with its mesh, same-base JSON, collision assets, compact local references, previews, and revision manifest.
2. Keep `objects/<object_id>/current.json` as a small atomic pointer containing object ID, active revision ID, and record hash. It does not duplicate the object record.
3. Write object edits to a private staging directory, validate every file and hash, fsync files and parent directories, then atomically rename the completed revision and replace the current pointer under one transaction journal.
4. Approved revisions are immutable. Editing creates a new revision. Draft staging may be deleted only through the service/CLI after verifying it is not active.
5. Use a single-writer lock with owner, run/session ID, operation, and epoch. A missing heartbeat marks the lock stale but never clears it; diagnostics plus explicit release are required.
6. Track JSON and manifests in normal Git. Track approved meshes, collision assets, compact references, and previews through Git LFS. Exclude raw scan sessions, intermediate reconstructions, bags, logs, caches, engines, and model weights.
7. Treat local Git commit as part of activation. Stage only the approved object bundle and active pointer. If commit fails, restore the prior pointer before releasing the lock and leave the new revision approved but inactive. Startup recovery resolves an unfinished transaction before serving reads.
8. Write a sync-outbox record for each committed HEAD. Remote push is outside the canonical transaction; push status records success, last attempt, error, and oldest unpushed commit without changing object content.
9. Build SQLite search tables from canonical files for names, statuses, tags, gripper compatibility, and qualification. Cache deletion and rebuild must not change canonical state.
10. Keep raw scan sessions under the configured external scan-staging root, outside Git. Enforce a configured byte/session quota, report the high-water mark, and block new sessions until the operator exports or deletes data through the service.
11. Provide verify, rebuild-index, export, clone/restore-check, staging-usage, and explicit cleanup commands. A GitHub backup is accepted only after a clean clone, Git LFS fetch, and full hash/pointer validation.

## Interfaces and data

- Filesystem store API used by the object service
- `current.json` pointer
- Disposable `.cache/object_index.sqlite3`
- Lock record and staging directories
- Local Git HEAD, LFS rules, activation journal, and sync outbox/status
- Noncanonical scan-staging root and quota report

## Boundaries

- SQLite never owns canonical fields or history
- No networked multi-user transaction system
- No direct GUI writes
- No raw scan data or runtime logs in Git

## Failure behavior

- Reject hash mismatch, malformed pointer, missing active revision, lock conflict, partial staging, path traversal, or cache disagreement.
- On crash, leave staged data identifiable and never expose a partial approved revision.
- Reject activation when the local Git commit cannot complete; do not roll back a valid local activation because remote push is unavailable.
- Block new scans at the staging quota without deleting existing sessions.

## Acceptance

- Create, approve, activate, read, and supersede fixtures pass.
- Approved file modification is detected.
- Removing `.cache` then rebuilding yields identical queries.
- Concurrent writer test allows one writer and clear rejection for the other.
- Local commit contains only the approved bundle and active pointer; excluded raw/cache/log files remain untracked.
- Push failure leaves a valid local revision and stale backup health; a later retry advances the remote to the same commit.
- Clean clone plus LFS fetch reproduces all hashes and active pointers.
- Staging quota blocks new sessions and explicit cleanup never removes approved evidence.

## Parallel work

Grasp profiles can refine schema fields alongside the initial store. Migration waits for stable approval behavior.

## What this module needs from me

Nothing.
