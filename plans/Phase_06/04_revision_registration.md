# Scan revision registration

## Goal

Convert a reviewed, qualified reconstruction into a new validated ObjectDB file
revision atomically.

## Task-script payoff

The newly approved object immediately loads through the same local
`dfl.objectdb.load` path as migrated and hand-authored assets.

## Work

1. Require explicit operator review of mesh, scale, frame, collision geometry,
   preview, provenance, quality, and known limitations.
2. Assemble staging `object.json` and assets according to Phase 03, including
   source session/calibration/backend/input hashes and validation result.
3. Let the operator set/confirm canonical frame, name/ID, dimensions, collision
   choice, and initial model/reference metadata.
4. Run full file/schema/path/geometry validation in staging.
5. Atomically create a new immutable revision and update the active pointer only
   after validation and explicit approval.
6. Reload the revision through the runtime loader and preview it in object and
   MoveIt frames.
7. Optionally commit/backup through authoring policy; Git/network failure must
   not corrupt the local revision or prevent normal later task loading.
8. Preserve the scan session as provenance or exportable evidence according to
   local storage policy.

## Acceptance

- Interrupted/rejected registration leaves the active object unchanged.
- Approved revision files are complete, immutable, reloadable, and traceable to
  scan inputs.
- Active-pointer changes are atomic and reversible by selecting an earlier
  revision.
- No runtime lease, server activation, or remote push is required.

## Non-goals

Silent mesh replacement, automatic activation from quality score, or a
distributed commit transaction.
