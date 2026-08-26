# Phase 04 — perception and tracking

## Goal

Qualify the four-object RGB-D perception path on the desktop: SAM2 masks, FoundationPose initialization, M3T multi-body tracking, explicit track health, and timestamped scene snapshots. Publish measured accuracy and throughput without presenting stale poses as current.

## Settled decisions

- Qualify the generic RGB-D contract on the installed D455.
- Use SAM2 and FoundationPose from Isaac ROS 4.6.
- Use M3T as the intended multi-body tracker.
- FoundationPose initializes and reseeds M3T.
- Approximately 30 Hz is a reported target, not a release threshold.
- Selected-target updates are exposed at the tracker/camera rate; scene snapshots may publish at 30 Hz while preserving each object's true age.
- Run the combined perception graph for two continuous hours without scheduled restarts.

## Work packets

| Packet | Result |
|---|---|
| [01](01_d455_dataset.md) | Reproducible four-object RGB-D benchmark and ground truth. |
| [02](02_sam2_segmentation.md) | Qualified mask adapter and memory behavior. |
| [03](03_foundationpose.md) | Revision-bound pose estimation and reseeding. |
| [04](04_tracking_contract.md) | Tracker-neutral states, health, and typed outputs. |
| [05](05_m3t_ros_adapter.md) | Headless C++ M3T integration. |
| [06](06_reseed_and_track_health.md) | Lost/degraded/reseed state machine. |
| [07](07_scene_snapshots.md) | Timestamped multi-object snapshot for MoveIt. |
| [08](08_perception_benchmarks.md) | Accuracy, rate, memory, recovery, and two-hour evidence. |

## Order and parallel work

Dataset work starts first. Tracking-contract design can proceed from recorded fixture requirements. SAM2 and FoundationPose adapters may run in parallel after the pinned image exists. The M3T build spike starts early but its ROS output waits for the tracking contract. Health/reseed consumes FoundationPose and M3T. Scene snapshots consume the health output. Benchmarks run last.

## Upstream inputs

- Isaac ROS reuse audit
- Phase 01 types, ROS interfaces, plugins, TF/time, and run records
- Phase 03 approved objects and scene synchronization
- D455 calibration and camera topics

## Exit criteria

- The dataset and ground truth can be replayed without a live robot.
- SAM2 and FoundationPose outputs bind to exact object revisions and observation times.
- M3T builds headless, tracks the four objects, and exposes health independent of raw publication rate.
- No stale or lost track is labeled current.
- Scene snapshots preserve individual observation age and uncertainty.
- The two-hour run passes its memory, freshness, and recovery gates.

## What this phase needs from me

Facts: representative lighting, work surface, object placements, motion sequences, and independent ground-truth capture. Collect these from the lab. No new algorithm preference remains.
