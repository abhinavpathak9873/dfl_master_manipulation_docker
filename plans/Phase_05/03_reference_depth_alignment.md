# Reference, mask, and depth local alignment

## Goal

Implement the v1 local-correction backend from stored close-range references, current SAM2 mask/depth, and calibrated geometry while matching accepted characterization behavior.

## Inputs

- Accepted alignment contract and characterization
- Object local-reference assets
- SAM2 mask and D455 RGB-D
- Healthy track and grasp anchor
- Camera/robot TF

## Outputs

- `reference_depth` alignment plugin
- Reference selection and image/depth preprocessing
- 2D and depth correction calculation
- Evidence metrics and artifacts
- Recorded-data and simulation tests

## Work

1. Select references by exact object revision, anchor, gripper profile, camera/calibration identity, and viewpoint bounds.
2. Synchronize RGB, depth, mask, CameraInfo, and TF at the observation timestamp. Crop only from validated regions and retain the mapping to full image coordinates.
3. Compare current evidence with the stored reference using the characterized visual and geometric method. Calculate lateral, depth, and allowed rotational correction in the declared frame.
4. Reject low mask overlap, insufficient valid depth, inconsistent scale, ambiguous match, excessive correction, or reference/calibration mismatch.
5. Clamp nothing silently. If a correction exceeds the capture envelope, return outside-capture-range with the measured value.
6. Record overlays, masks, depth samples, intermediate transforms, residuals, and final correction for each run.
7. Match golden fixtures within the accepted tolerances and add new tests for the simplified architecture.

## Interfaces and data

- Alignment plugin `reference_depth`
- SAM2 mask and RGB-D topics/readers
- Object local-reference files
- Typed correction result

## Boundaries

- Does not command visual servo
- Does not update canonical object data during a task
- Does not train a model

## Failure behavior

- Return reference, sync, mask, depth, match, scale, ambiguity, and capture-range errors separately.
- No correction is valid when camera calibration or anchor revision differs.

## Acceptance

- Golden fixture corrections match within declared translation/rotation tolerances.
- Wrong reference and calibration are rejected.
- Artifacts allow manual verification of the computed correction.
- Runtime meets the configured pre-grasp update budget on the desktop.
- All four objects either have qualified references or are explicitly marked unsupported for this backend.

## Parallel work

Grasp verification may proceed separately. Servo integration consumes valid-result fixtures.

## What this module needs from me

Facts: which of the four migrated objects have approved local references and the exact calibration they use.
