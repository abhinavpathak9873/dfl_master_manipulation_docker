# Object and scene acceptance

## Goal

Prove that file-first objects, grasp profiles, legacy migration, and planning
scene use are complete and directly debuggable.

## Task-script payoff

A task can load, inspect, transform, and place approved assets in the planning
scene from local files with predictable errors and no hidden runtime dependency.

## Work

1. Validate minimal, full, extension-field, malformed, missing-asset,
   path-escape, unit/frame, and unsupported-version fixtures.
2. Load all four migrated objects by ID and explicit revision with no ObjectDB
   process or network.
3. Compare migrated meshes, dimensions, frames, models, references, provenance,
   and grasp anchors with approved source fixtures.
4. Transform each tool profile's anchors through known poses and preview them
   relative to TCP/collision geometry.
5. Delete/rebuild the optional index and verify canonical results are unchanged.
6. Inject interrupted authoring and confirm no half-written revision becomes
   active.
7. Add/update/attach/detach/remove collision objects from recorded tracks and
   reject stale/mismatched identity.
8. Verify experimental object paths/models and algorithmic grasps do not require
   ObjectDB schema changes.

## Acceptance

- Local loading and validation have clear, deterministic errors.
- Approved data is complete; rejected legacy history stays separate.
- Grasp transforms and scene updates match golden geometry.
- The task-visible object path is asset -> local value -> perception/grasp/scene,
  with no service, database, lease, or Git hop.
- Failures are reproducible from ordinary files and focused commands.

## Outputs

- Versioned fixtures, focused tests, migration comparison, and Phase 03 report.
- Known schema/asset limitations and direct troubleshooting commands.

## Non-goals

Testing an imagined distributed ObjectDB topology or turning fixtures into a
general asset platform.
