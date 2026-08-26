# Guided multi-view capture

## Goal

Capture calibrated, timestamped RGB-D/mask views through the ordinary Picker 1,
D455, arm-motion, and segmentation primitives.

## Task-script payoff

The scan workflow does not create a second robot/camera API; its capture logic
can be understood and debugged like any other Python robotics task.

## Work

1. Define the first commissioned Picker 1 scan station: eye-in-hand D455, tool
   and collision model, scene, object volume, safe scan poses/paths, speed/force
   limits, and base state.
2. Generate or author a small ordered view plan with coverage intent and
   operator preview.
3. At each view, move using Phase 02 primitives, wait for settled/fresh state,
   capture synchronized RGB/depth/CameraInfo/TF, and run the selected segmenter.
4. Save robot/camera poses, source timestamps, calibration, mask, acceptance,
   rejection reason, quality/coverage hints, and file hashes.
5. Reject blur, stale/misaligned streams, invalid depth, bad mask, wrong TF,
   unexpected robot/tool/scene state, or unsafe workspace.
6. Allow operator accept/retry/skip within declared coverage rules.
7. On cancel/fault, stop motion/capture and save the last completed view.
8. Keep direct ROS camera/TF/arm diagnostics and a capture-only dry-run mode.

## Acceptance

- Accepted views are synchronized, calibrated, correctly framed, and replayable.
- Scan motion stays inside declared collision/workspace/speed limits.
- Interrupted capture never auto-continues.
- Capture results can feed reconstruction without a live robot.
- The implementation is a readable scan task/helper, not a capture service
  framework.

## Non-goals

Picker 2/H2515 automated scan qualification in the first station packet,
continuous freehand scanning, or unsupported material compensation.
