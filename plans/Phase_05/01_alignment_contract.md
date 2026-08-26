# Local-alignment contract

## Goal

Define a plugin-neutral request and result for refining a selected grasp anchor from close-range RGB-D evidence without commanding motion.

## Inputs

- Healthy selected track
- Object revision and grasp profile
- D455 RGB-D/TF contract
- SAM2 masks and local-reference assets
- Typed failures

## Outputs

- Local-alignment plugin interface
- Alignment request/result values
- Correction frame and covariance/confidence semantics
- Evidence and validity bounds
- Shared recorded-data fixtures

## Work

1. Bind every request to robot, camera calibration, object revision, track epoch, grasp anchor, gripper profile, observation timestamp, and expected pre-grasp pose.
2. Return a correction transform in a declared frame, corrected target pose, evidence metrics, capture-range status, validity interval, implementation ID, and artifact references.
3. Separate translational and rotational confidence/evidence. A scalar score may summarize but cannot replace components.
4. Define health states valid, insufficient evidence, outside capture range, stale, identity mismatch, and failed.
5. Require the caller to choose whether and how to apply the correction. The plugin never publishes robot commands or mutates a target frame as a side effect.
6. Define deterministic handling for object symmetries and grasp-anchor orientation rules.
7. Create fixtures for nominal offset, depth bias, mask loss, partial occlusion, wrong object, stale TF, and out-of-range correction.

## Interfaces and data

- Alignment plugin request/result
- `AlignGrasp` ROS action for cross-process implementations
- Reference to local assets in the object record

## Boundaries

- No arm or gripper command
- No coarse object detection
- No hidden retry

## Failure behavior

- Missing revision/anchor/reference, stale input, TF failure, wrong identity, insufficient depth/mask, and out-of-range correction are distinct.
- A result outside its validity interval cannot be executed.

## Acceptance

- Fixtures produce deterministic state and correction.
- Every result identifies exact input revisions and timestamps.
- Wrong identity and stale cases never return valid.
- A consumer can inspect all evidence needed for the policy decision.

## Parallel work

Legacy characterization runs alongside contract design.

## What this module needs from me

Nothing.
