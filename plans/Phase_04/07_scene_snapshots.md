# Timestamped scene snapshots

## Goal

Publish a convenient multi-object view for task and MoveIt consumers without hiding the true age, health, or source rate of each track.

## Inputs

- TrackedObjectArray contract
- Health/reseed output
- Object repository
- Scene/MoveIt synchronization

## Outputs

- Scene snapshot builder
- Selected-target stream
- Configurable snapshot publisher targeting 30 Hz
- Age/confidence/health preservation
- Duplicate and missing-object policy
- Consumer contract tests

## Work

1. Maintain the latest immutable result per active track instance. Replace it only with a newer observation or explicit health transition.
2. Publish snapshots at the configured convenience rate, targeting 30 Hz. Preserve each object's observation timestamp and calculate age at publish time.
3. Expose the selected target through a dedicated typed stream at the tracker/camera update rate when new evidence exists.
4. Resolve each track to an approved object revision and collision geometry before marking it eligible for planning-scene use.
5. Mark degraded, stale, lost, duplicate, or unresolved tracks explicitly. Never omit an obstacle in a way that implies free space.
6. Provide snapshot sequence/version IDs so MoveIt and motion plans can detect change.
7. Measure snapshot construction latency separately from perception inference.

## Interfaces and data

- TrackedObjectArray/SceneSnapshot
- Selected-target topic or reader
- Planning-scene adapter input
- Snapshot version

## Boundaries

- No interpolation presented as a new observation
- No collision-scene mutation inside the snapshot builder
- No planner choice

## Failure behavior

- Time regression, duplicate identity, unknown revision, or missing geometry produces explicit unhealthy entries.
- Snapshot publisher remains alive through missing updates but reports growing age/stale state.

## Acceptance

- A 30 Hz publisher over a 12 Hz tracker shows correct unchanged observation stamps and increasing age.
- Selected-target messages occur only on new accepted tracker evidence or health transition.
- Lost objects remain represented for conservative scene handling.
- Snapshot version changes on pose/health/identity changes.

## Parallel work

Runs with health tests. MoveIt integration already owns collision mutation.

## What this module needs from me

Nothing.
