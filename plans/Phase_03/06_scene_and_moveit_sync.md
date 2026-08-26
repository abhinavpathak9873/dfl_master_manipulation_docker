# Scene folders and MoveIt synchronization

## Goal

Load static scene geometry and explicitly synchronize object collision state from
local assets and current perception into the selected robot's MoveIt scene.

## Task-script payoff

A task can select `scene="empty"`, add a loaded tray, update its tracked pose,
attach it after grasp, and remove/detach it through small motion-side helpers.

## Work

1. Define normal scene folders with static geometry, frames, simulator assets,
   default placements, and optional allowed-collision settings.
2. Add explicit helper operations to load scene, add/update/remove object,
   attach/detach object, and inspect current planning-scene state/version.
3. Build collision geometry from the loaded object's collision mesh or declared
   simple geometry; never fetch it from a live ObjectDB service.
4. Transform source poses using ROS TF with timestamp/freshness checks.
5. Define identity mapping among object asset/revision, perception track, MoveIt
   collision object, and task-selected target.
6. Keep update rate controlled by actual consumers; do not mirror every tracker
   sample blindly.
7. Test plan invalidation or revalidation when the relevant scene/start state
   changes.
8. Keep raw MoveIt planning-scene tools/topics available for inspection.

## Acceptance

- Static scenes load with correct units/frames.
- A loaded object can be added, updated, attached, detached, and removed.
- Stale/lost perception cannot silently move collision geometry as current.
- Motion planning uses the intended object revision/pose.
- ObjectDB is not a scene authority or runtime dependency.

## Non-goals

A scene server, world-model platform, or automatic grasp attachment policy.
