# M3T ROS/native adapter

## Goal

Integrate M3T's real native capabilities into the tracking API with the smallest
ROS/process boundary required by its build and runtime.

## Task-script payoff

`Tracker(backend="m3t", object=tray)` behaves like a normal stateful object while
developers can trace it directly into the M3T process, models, ROS transport, and
debug rendering.

## Work

1. Pin the M3T source revision, license, build toolchain, model-generation
   requirements, renderer/GPU/OpenGL needs, and supported object features.
2. Prove headless Ubuntu 24.04/Jazzy/container operation before finalizing the
   adapter route.
3. Build M3T in the smallest owning image/package; do not contaminate core
   dependencies unnecessarily.
4. Map D455 RGB/depth/calibration, object mesh/model, FoundationPose seed,
   timestamps/frames, update/reset, and multi-body behavior.
5. Use standard ROS image/camera/pose data and only the focused custom output
   semantics proven necessary.
6. Preserve M3T-native diagnostics, confidence/health signals, debug render, and
   failure text.
7. Handle bad seed, missing/incompatible model, frame/time mismatch, occlusion,
   loss, process crash, cancel/reset, and restart.
8. Measure sustainable rate, latency, CPU/GPU memory, multi-object scaling, and
   headless stability on the locked dataset.

## Acceptance

- M3T initializes and tracks all approved supported objects from FoundationPose
  seeds.
- The Docker/Jazzy/headless path is reproducible and directly diagnosable.
- Actual rate is reported; approximately 30 Hz remains a target, not a false gate.
- Restart produces explicit lost/uninitialized state and requires a fresh seed.
- No native complexity leaks into unrelated task stages.

## Non-goals

Reimplementing M3T, pretending every tracker shares its model format, or adding
a generic native-backend host.
