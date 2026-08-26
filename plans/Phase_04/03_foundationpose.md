# FoundationPose estimation and reseed backend

## Goal

Estimate an object's coarse 6D pose from explicit RGB-D, mask, calibration, and
object mesh inputs and reuse the same backend for tracker reseeding.

## Task-script payoff

`PoseEstimator(backend="foundation_pose", object=tray).estimate(...)` returns a
framed pose/quality result or a clear missing-mesh/data error.

## Work

1. Pin the selected FoundationPose/Isaac ROS implementation, models, renderer,
   CUDA/TensorRT requirements, and container placement.
2. Make required inputs explicit: RGB, depth, mask, CameraInfo/intrinsics, object
   mesh/canonical frame, source time, and camera/target frame.
3. Normalize depth units/invalid pixels and mesh units once at the adapter seam.
4. Define returned pose frame/time plus backend quality/debug details actually
   used by tracker/task decisions.
5. Keep initialization loaded and expose useful FoundationPose-specific refine or
   debug methods without forcing other estimators to match them.
6. Use a thin ROS action/service/topic adapter only if the process boundary needs
   it; retain direct ROS diagnostics.
7. Handle empty mask, missing mesh, invalid depth/calibration, symmetry,
   timeout, GPU/process loss, implausible pose, and cancellation.
8. Measure accuracy/stability/latency/memory on the four-object dataset.

## Acceptance

- Known fixtures produce poses in the declared frame within reported error.
- Missing/invalid object assets fail before model work with actionable context.
- Output time/frame matches the consumed observation and transforms correctly.
- The same method can explicitly reseed M3T.
- Switching estimator backends does not alter downstream task structure.

## Non-goals

A universal pose-estimation input envelope or automatic tracker orchestration.
