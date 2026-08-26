# Scan revision registration

## Goal

Turn a qualified scan result into a complete staged object revision, then commit and activate it only through explicit review.

## Inputs

- Qualified reconstruction
- Object schema and atomic service
- Scan session/provenance
- Viewer/editor review result
- Task/scan lease state and local Git transaction contract

## Outputs

- Draft object JSON and asset layout
- New-object and new-revision registration paths
- Validation/preview report
- Explicit approve and activate operations
- Rollback and failed-commit tests
- Local Git commit and sync-outbox record

## Work

1. For a new object, validate the proposed stable object ID and display name. For a rescan, bind to the existing object ID and active base revision.
2. Copy or link candidate assets into a staging revision by content hash. Generate the same-base JSON with mesh, scale, canonical frame, collision, perception, and provenance fields.
3. Carry scan session ID, camera/calibration hashes, view hashes, reconstruction tools, metrics, and limitations into provenance and validation.
4. Open the draft in the viewer for scale, frame, geometry, and held-out overlay review. Edits create a revised staging candidate.
5. Commit only after schema, asset, quality, path, staging provenance, and stale-base validation passes. The commit copies the approved bundle through ObjectDB; scan-worker has no canonical write path.
6. Keep activation separate. Refuse it while any task lease or foreign scan lease is active or stale-unverified. The owning scan session may activate only after motion is quiescent and the session reaches review/qualified state. Revalidate the revision, atomically update the active pointer, complete the path-limited local Git commit, and emit a sync-outbox record.
7. On activation, rebuild/update the cache and verify the exact revision, hashes, and Git commit through the object service. Remote push status is reported separately and does not change local validity.
8. Keep the previous active revision available for rollback by pointer change and a new recorded Git commit; never mutate it.

## Interfaces and data

- Object service/CLI stage, commit, activate, and resolve
- Scan result to object-schema mapping
- Viewer review record

## Boundaries

- Does not create grasp anchors automatically
- Does not delete old revisions
- Does not bypass quality with a GUI-only flag

## Failure behavior

- Stale base, ID collision, failed asset copy/hash, invalid schema, failed quality, lock conflict, and atomic commit failure leave current active state unchanged.
- Active/stale task lease or failed local Git commit blocks activation. Remote push failure leaves the local activation valid and marks backup stale.
- Rollback is explicit and recorded.

## Acceptance

- New-object and rescan fixtures both commit correctly.
- All provenance hashes resolve.
- Crash injection preserves previous active revision.
- Activation resolves exact revision/hash through service and cache.
- Activation commit contains only the approved bundle and active pointer; raw session and intermediates remain outside Git.
- Active task and stale-lease fixtures block activation without changing the pointer.
- Rollback restores prior active pointer without file mutation.

## Parallel work

Follows reconstruction and uses viewer/editor outputs.

## What this module needs from me

Nothing.
