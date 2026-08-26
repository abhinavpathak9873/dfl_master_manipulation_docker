# Scene folders and MoveIt synchronization

## Goal

Load static scene geometry and overlay tracked known objects into the robot's MoveIt planning scene without creating a second world model.

## Inputs

- Scene profile format
- Object repository and collision geometry
- TrackedObject contract
- Motion plan scene-version rules
- Robot namespace and frames

## Outputs

- Scene loader and typed scene view
- MoveIt PlanningScene monitor adapter
- Stable collision-object IDs and version counter
- Attach/detach lifecycle
- Stale-object policy and diagnostics
- Recorded-data and simulator tests

## Work

1. Load static geometry, allowed collision settings, named frames, and simulator world metadata from `.devcontainer/src/dfl_manipulation_toolbox/scenes/<scene_id>/scene.yaml`. Validate every asset and frame before readiness.
2. Resolve tracked object revisions to approved collision geometry. Transform poses at observation timestamps into the robot planning frame.
3. Use collision IDs derived from object ID plus track instance. Update pose and health without changing identity.
4. Increment a scene version for any change that can invalidate a plan. Motion plans record and recheck this version.
5. When an object becomes stale, retain its last conservative collision volume and mark the scene uncertain. Planning that relies on clearing uncertain space is rejected until perception refreshes or an explicit reviewed scene policy resolves it.
6. On successful grasp verification, attach the exact object revision to the active tool link and remove its world instance atomically. Detach at the measured place pose after release verification.
7. Publish diagnostics for missing geometry, TF failure, stale objects, duplicate tracks, attachment mismatch, and scene update latency.

## Interfaces and data

- MoveIt PlanningScene messages/services
- Scene view and version consumed by motion
- TrackedObjectArray input
- Object repository reads
- Attach/detach calls used by tasks

## Boundaries

- MoveIt remains the runtime collision-world authority
- Does not plan paths or choose grasps
- Does not silently remove stale obstacles

## Failure behavior

- Reject unknown revision, missing collision geometry, stale transform, duplicate active instance, attachment mismatch, or scene update timeout.
- Any uncertain scene change invalidates previewed plans.

## Acceptance

- Static fixtures load with declared frames and units.
- Tracked objects add/update collision geometry and advance scene version.
- Stale obstacles remain conservative and block unsafe clearing assumptions.
- Attach/detach keeps world and robot state consistent.
- Motion stale-scene tests reject outdated plans.

## Parallel work

Can start with schema and tracker fixtures. Final attach/detach tests depend on Phase 02 gripper/motion.

## What this module needs from me

Nothing.
