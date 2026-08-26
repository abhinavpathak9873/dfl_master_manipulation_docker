# Perception benchmarks and endurance

## Goal

Measure the named D455/SAM2/FoundationPose/M3T stack so backend choices and
failure limits are based on evidence.

## Task-script payoff

Developers can compare another backend against task-relevant accuracy, latency,
rate, stability, and memory instead of inheriting a vague qualification label.

## Work

1. Lock development and qualification splits plus exact object, mesh, model,
   calibration, image/container/source, and hardware revisions.
2. Define mask quality, pose translation/rotation error, track drift/loss,
   reseed success/time, end-to-end latency, sustainable rate, CPU/GPU memory, and
   stale-output rules.
3. Report per-object, per-scene, and failure-case distributions, not only averages.
4. Run the combined named stack continuously for the declared two-hour
   qualification window with no scheduled restart.
5. Inject empty mask, bad depth, occlusion, process/GPU failure, ROS disconnect,
   clock/TF error, and restart.
6. Check memory growth, queued-data age, backpressure/drop behavior, and whether
   old output is ever presented as current.
7. Save minimal scripts, configs, raw summaries, plots, and failure artifacts
   needed to reproduce findings.
8. Keep backend-specific thresholds in this qualification packet, not in every
   task/runtime object.

## Acceptance

- Accuracy/stability and performance are reported honestly for all four objects.
- Long-run output stays current, memory remains bounded, and recovery behavior is
  explicit.
- Approximately 30 Hz is reported as measured outcome/target, never assumed.
- A failing backend remains usable for experiments if clearly labelled by its
  measured limitations; release claims remain scoped.
- The benchmark runs without a telemetry or qualification service.

## Non-goals

A benchmarking platform, global score, automatic model promotion, or hidden
runtime gate.
