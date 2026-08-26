# M3T ROS adapter

## Goal

Integrate the pinned standalone M3T C++ library as a headless ROS 2 tracking plugin for the four approved objects.

## Inputs

- Pinned M3T commit
- Core/perception build images
- Tracking contract
- FoundationPose seeds
- D455 dataset and object meshes

## Outputs

- Ament wrapper and reproducible M3T build
- ROS RGB/depth camera adapters
- Multi-body tracker plugin
- Headless rendering configuration
- Pose/evidence publisher
- Build, recorded-data, and resource tests

## Work

1. Build M3T as a pinned external CMake dependency with optional Azure Kinect and RealSense components disabled. Feed ROS images through project camera adapters.
2. Prove EGL, OSMesa, or another accepted headless OpenGL path in the perception container. Record GPU/CPU rendering and OpenCV-contrib dependencies.
3. Create bodies and modalities from approved object meshes, camera intrinsics/extrinsics, and per-object tracking configuration.
4. Initialize each body only from an accepted FoundationPose result. Preserve object revision, track instance, and seed timestamp.
5. Run M3T update cycles from the latest synchronized input. Drop superseded frames rather than accumulating latency.
6. Extract pose plus available residual, modality, occlusion, and iteration evidence. Do not fabricate an M3T confidence value.
7. Publish through the tracking contract and expose reset, body add/remove, diagnostics, cycle time, queue drops, and resource use.

## Interfaces and data

- M3T C++ API
- ROS camera subscriptions
- Tracker plugin implementation
- Per-object M3T configuration files

## Boundaries

- No M3T global detector
- No claim that published upstream benchmark rates apply
- No direct task dependency on M3T classes

## Failure behavior

- Build/headless failure, invalid mesh, seed rejection, numerical error, missing camera, queue overflow, and tracker exception map to typed state.
- Adapter crash marks all owned tracks lost; it does not leave a latched fresh pose.

## Acceptance

- Pinned library builds reproducibly on Noble/Jazzy.
- Four bodies initialize from recorded FoundationPose seeds.
- Recorded sequences produce poses without an unbounded processing queue.
- Headless execution needs no interactive display.
- Cycle time, dropped frames, CPU/GPU use, and raw evidence are recorded.

## Parallel work

Build spike begins while tracking contract settles. Final publisher waits for the accepted fields.

## What this module needs from me

Nothing. If headless or ABI integration fails, publish evidence and stop M3T-dependent work.
