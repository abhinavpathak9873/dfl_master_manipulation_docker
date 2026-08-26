# Phase 04 — perception and tracking

## Goal

Provide replaceable, state-explicit RGB-D perception components with measured
behavior on the D455 and four approved objects.

## Task-script payoff

A task constructs `Segmenter`, `PoseEstimator`, and `Tracker` objects, passes
named robotics inputs, swaps a backend ID, and can debug the concrete Python,
ROS, native, model, and dataset layers.

## Packets

1. [D455 recorded dataset](01_d455_dataset.md)
2. [SAM2 segmentation](02_sam2_segmentation.md)
3. [FoundationPose estimation/reseed](03_foundationpose.md)
4. [Tracking API](04_tracking_contract.md)
5. [M3T ROS/native adapter](05_m3t_ros_adapter.md)
6. [Track health and reseed](06_reseed_and_track_health.md)
7. [Timestamped scene snapshots](07_scene_snapshots.md)
8. [Perception benchmarks](08_perception_benchmarks.md)

## Smallest sufficient design

- Ordinary stateful objects selected by direct backend maps.
- Explicit `rgb`, `depth`, `mask`, `mesh`, `object`, and timestamp/frame inputs.
- Docker/ROS/native isolation only where accelerated or C++ dependencies require.
- Actual accuracy/rate/latency/memory/failure evidence, not generic pipeline
  health machinery.
- ROS source timestamps and TF remain visible.

## Exit evidence

The four-object stack produces measured masks, poses, tracks, health/reseed, and
snapshots on recorded D455 data and declared live profiles. Long-run checks
qualify the named stack without becoming a dependency of every experiment.

## Non-goals

A managed perception graph, universal tensor/input format, backend plugin
platform, or hidden tracker recovery runtime.
