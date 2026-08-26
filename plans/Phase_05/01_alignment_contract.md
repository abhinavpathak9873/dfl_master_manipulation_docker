# Local-alignment API

## Goal

Define the small replaceable capability that computes a fine correction from
current sensor/object information without commanding hardware.

## Task-script payoff

`aligner.compute(camera=robot.camera, object=tray,
initial_pose=object_pose)` returns a correction that the task explicitly inspects
and applies.

## API behavior

- Inputs are named robotics concepts required by the backend: current RGB-D or
  camera, object asset/revision, initial pose, mask/track, grasp anchor, local
  references, calibration/TF, and optional backend settings.
- Output contains a framed translation/rotation correction, source time,
  convergence/quality information used by the task, and debug details.
- A backend may expose refine/render/specialized methods.
- Compute never moves the arm, opens/closes the gripper, or loops indefinitely.

## Work

1. Derive shared behavior from the existing reference/depth method and at least
   one intended experimental replacement.
2. Validate object identity/revision, required references, input time/frame, TF,
   calibration, depth/mask quality, and configured bounds.
3. Define correction direction/composition and make it visually/numerically
   testable.
4. Use a direct backend mapping under `perception/alignment/<name>.py`.
5. Preserve raw diagnostics/images/point clouds on request.
6. Return clear no-solution, low-quality, stale-input, missing-asset, and
   unsupported-method errors.
7. Keep backend resources/state in the object where appropriate.

## Acceptance

- Known recorded offsets produce corrections in the documented direction/frame.
- A task may inspect, reject, scale, or apply the result separately.
- Switching alignment backend leaves motion/task structure unchanged.
- Backend-specific inputs do not force an opaque generic input list.

## Non-goals

Robot command ownership, a universal registration ontology, or hidden servoing.
