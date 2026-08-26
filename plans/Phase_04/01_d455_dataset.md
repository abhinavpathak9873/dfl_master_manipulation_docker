# D455 recorded benchmark dataset

## Goal

Create the smallest representative RGB-D dataset needed to develop and compare
the declared perception and alignment backends reproducibly.

## Task-script payoff

Developers can run segmentation, pose, tracking, and alignment against normal
recorded fixtures before occupying a robot or guessing about live failures.

## Scope

- Four approved object revisions across representative scenes, distances,
  orientations, lighting, occlusion, motion, and failure cases.
- Synchronized RGB, depth, CameraInfo/intrinsics, source timestamps, camera/robot
  TF, calibration identity, object identity/revision, and scene.
- Ground truth or reviewed labels appropriate to mask, pose, tracking, and
  stale/lost evaluation.
- Separate development and locked qualification splits.

## Work

1. Freeze the installed D455 stream/resolution/fps/depth-scale and calibration
   profile used for capture.
2. Capture both static pose and temporal sequences, including no-object, multiple
   objects, partial view, occlusion, motion blur, invalid/missing depth, and TF
   faults.
3. Store images/arrays plus one readable manifest; keep raw bags only where
   replay adds value.
4. Reference exact mesh/model/object revisions and annotation provenance.
5. Add dataset validation for dimensions, encodings, depth units, time monotonicity,
   missing frames/files, and split leakage.
6. Keep the corpus small enough for local iteration and store large raw material
   outside normal source history as planned.
7. Document capture/replay/visualization commands.

## Acceptance

- Every approved object has usable mask/pose/tracking sequences and deliberate
  failures.
- Samples replay identically in the relevant Docker environments.
- Frames, units, calibration, time, and object revision are unambiguous.
- Qualification labels are reviewable and not derived from the algorithm under
  test.

## Non-goals

A general dataset platform, cloud labelling system, or open-world corpus.
