# Reference, mask, and depth local alignment

## Goal

Implement the proven reference/mask/depth XY/RPY correction as a direct
LocalAlignment backend.

## Task-script payoff

The task swaps `backend="reference_depth"` or an experimental alignment file
without changing object loading, tracking, or robot motion calls.

## Work

1. Port the characterized pure image/depth/geometry computation into the
   alignment folder with explicit inputs and dependencies.
2. Load object local references from the ObjectAsset, not a runtime service.
3. Validate camera intrinsics, depth scale, source time/frame, object revision,
   mask/reference shape, initial pose, and TF.
4. Keep crop, correspondence, fit, outlier rejection, correction composition,
   and bounds readable and testable as small functions.
5. Return correction/quality/termination plus optional debug images, matches,
   point clouds, and residuals.
6. Reject missing/invalid depth, insufficient mask/reference support, implausible
   fit, out-of-range correction, and no convergence clearly.
7. Compare every golden fixture and live D455 sample against the characterization.
8. Keep parameters visible in task construction or one backend-owned config.

## Acceptance

- Golden corrections match accepted legacy behavior within declared tolerances.
- Failures never produce a plausible-looking zero/success correction.
- Debug artifacts explain why a fit succeeded or failed.
- No robot, service, state machine, or generic pipeline owns the computation.

## Non-goals

Moving the robot, automatic retry, or forcing unrelated alignment algorithms to
accept the same raw inputs.
