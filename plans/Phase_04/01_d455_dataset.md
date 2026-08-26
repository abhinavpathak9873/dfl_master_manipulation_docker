# D455 recorded benchmark dataset

## Goal

Create a reproducible four-object RGB-D dataset with calibrated timestamps, TF, prompts, poses, occlusions, and failure sequences for segmentation, pose, tracking, and local-alignment tests.

## Inputs

- Four approved object revisions
- Installed D455 profile and calibration
- Scene profiles
- Run-record and time contracts
- Object meshes and canonical frames

## Outputs

- Versioned rosbag dataset manifest
- Synchronized RGB, aligned depth, CameraInfo, TF, and robot state
- Independent object-pose ground truth or measured fixture references
- SAM2 prompt annotations and mask ground truth subset
- Train/tuning/qualification sequence split
- Dataset validation and replay commands

## Work

1. Record camera serial, firmware, stream resolution/rate, exposure settings, depth alignment, intrinsic/extrinsic calibration hashes, robot profile, scene, object revisions, and clock health.
2. Capture each object alone and in the four-object scene across distance, viewpoint, partial occlusion, clutter, lighting, robot/camera motion, temporary loss, re-entry, and static intervals.
3. Use a ground-truth method independent of SAM2, FoundationPose, and M3T. Calibrated fixtures, metrology, or marker-derived object frames may be used only after their own error is measured and recorded.
4. Annotate a representative mask subset and object symmetries. Keep raw frames immutable; corrections create a new dataset annotation revision.
5. Separate tuning sequences from final qualification sequences. Do not tune thresholds on the qualification split.
6. Add explicit fault bags for stale TF, missing depth, camera restart, timestamp skew, dropped frames, and wrong mesh scale.
7. Provide replay at original and controlled rates with deterministic topic names and clock.

## Interfaces and data

- Rosbag topics matching the generic RGB-D and TF contract
- Dataset manifest with source/object/calibration hashes
- Ground-truth poses in canonical object frames
- Annotation revision format

## Boundaries

- Does not train a new model
- Does not include unapproved objects in v1 metrics
- Does not use evaluated model output as ground truth

## Failure behavior

- Dataset validation fails on missing frames, non-monotonic timestamps, calibration mismatch, unresolved TF, wrong object revision, or mutable raw data.
- A sequence without reliable ground truth may remain a stress fixture but cannot count toward accuracy.

## Acceptance

- Every object has visible, occluded, moving-camera, loss, and re-entry cases.
- RGB/depth/CameraInfo and TF resolve at each evaluated timestamp.
- Ground-truth error is measured and smaller than the reported model thresholds.
- Qualification split is locked by content hash.
- Replay reproduces topic counts and timing.

## Parallel work

Tracker contract and adapter build work may use early immutable sequences. Final metrics wait for the locked split.

## What this module needs from me

Facts: choose and measure the available ground-truth apparatus. If no apparatus reaches adequate accuracy, present the error budget and options.
