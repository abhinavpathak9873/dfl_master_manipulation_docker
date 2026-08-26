# FoundationPose estimation and reseed adapter

## Goal

Reuse Isaac ROS FoundationPose for revision-bound coarse 6D pose estimates and tracker reseeding from synchronized RGB-D, CameraInfo, mask, and mesh inputs.

## Inputs

- Pinned FoundationPose nodes and models
- D455 dataset
- SAM2 mask result
- Approved mesh/object schema
- TF/time contract

## Outputs

- FoundationPose plugin manifest and launch profile
- Object-revision/mesh selector
- Typed estimate and tracking result mapping
- Symmetry and scale handling
- Reset/reseed API
- Recorded-data accuracy and failure tests

## Work

1. Resolve every request to an immutable object revision, mesh hash, scale, canonical frame, symmetry record, and current valid mask.
2. Verify rectified RGB, aligned depth, CameraInfo, mask, and TF timestamps before submitting a request. Reject mixed-time inputs.
3. Map `vision_msgs/Detection3DArray` and relevant upstream pose tensors/scores into a typed result while retaining raw-output references.
4. Configure and record engine versions, watchdog, QoS, auto-reset, point-cloud support, and input/output topic names.
5. Normalize symmetric-object error using the object's declared symmetry; never hide an unresolved frame or mesh-axis mismatch as symmetry.
6. Expose explicit initialize, track, reset, and reseed operations. M3T consumes accepted initialization; health logic may request reseed.
7. Test wrong scale, wrong mesh, depth holes, mask erosion, occlusion, camera restart, timeout, object loss, and re-entry.

## Interfaces and data

- Isaac ROS FoundationPose estimation/tracking topics
- Coarse-pose plugin
- Typed pose estimate with object revision and raw artifact
- Reseed request consumed by health state machine

## Boundaries

- Does not own SAM2 prompts
- Does not declare final grasp alignment
- Does not silently substitute a different object mesh

## Failure behavior

- Return input-sync, mask, mesh, scale, TF, estimation, watchdog, support, and reset failures separately.
- A previous pose is never restamped as a new estimate.

## Acceptance

- Qualification ADD-S is at most 10% of object diameter in at least 90% of valid evaluated frames per object, with symmetry-aware scoring.
- Every estimate resolves to the correct canonical frame and revision.
- Reset/reseed after loss produces a new observation timestamp and evidence.
- Wrong mesh/scale tests fail or produce a detected qualification failure.
- Startup and inference metrics are recorded.

## Parallel work

Runs beside SAM2 and M3T build work. Health integration waits for the tracking contract.

## What this module needs from me

Nothing.
