# Tracking contract

## Goal

Define how any tracker is initialized, updated, judged healthy, declared stale or lost, reset, and published without assuming that output frequency equals new evidence.

## Inputs

- TrackedObject ROS/Python values
- D455 timestamps and TF rules
- FoundationPose initialization
- M3T API capabilities
- Scene snapshot consumer

## Outputs

- Tracker plugin interface
- State model `uninitialized`, `initializing`, `tracking`, `degraded`, `stale`, `lost`, `reseeding`, `stopped`
- Initialization/update/reset inputs
- Health evidence model
- Track and batch result semantics
- Shared tracker fixtures

## Work

1. Define initialization from object revision, accepted pose, camera calibration, mesh, and observation timestamp.
2. Define update from synchronized RGB/depth and optional mask. A tracker returns pose plus evidence; the wrapper assigns health from the accepted policy.
3. Keep `observation_stamp`, `published_stamp`, and `age` separate. Republishing a pose advances only the publication stamp.
4. Define health evidence fields for image/depth availability, residuals, silhouette agreement, depth support, pose innovation, motion bounds, occlusion, and last successful reseed.
5. Define reset and stop as explicit operations. A lost tracker cannot return to tracking without a fresh initialization/reseed result.
6. Support multiple bodies with stable track instance IDs. Object identity and revision cannot change within an active track.
7. Define thread, queue, drop, and backpressure behavior so slow processing does not build an unbounded stale queue.

## Interfaces and data

- Tracker plugin methods and typed requests/results
- TrackedObject/TrackedObjectArray output
- Health evidence consumed by reseed and scene snapshots

## Boundaries

- Does not set M3T-specific thresholds
- Does not create new object identity
- Does not command robot motion

## Failure behavior

- Missing input, time regression, invalid initialization, identity mismatch, numerical failure, queue overflow, and lost health produce explicit states/codes.
- No state other than tracking/degraded may be presented as current.

## Acceptance

- Shared fixtures cover initialization, update, degraded evidence, stale time, loss, reseed, reset, multi-body IDs, dropped frames, and backpressure.
- Observation age remains correct when snapshots republish.
- A lost track requires fresh initialization.
- Contract tests do not import M3T.

## Parallel work

Starts early. M3T adapter and health policy consume the frozen contract.

## What this module needs from me

Nothing.
