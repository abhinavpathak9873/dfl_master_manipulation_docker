# Isaac ROS Jazzy reuse audit

## Decision

Pin Isaac ROS 4.6 and reuse its supported SAM2 and FoundationPose packages. Do
not wrap NVIDIA nodes merely to rename them. Add only configuration, launch
composition, the thin task-facing adapter needed by a concrete call, and health
logic not supplied upstream. CuMotion is outside the current plan.

## Requirement mapping

| Toolbox requirement | Upstream capability | Integration choice |
|---|---|---|
| Prompted known-object segmentation | Isaac ROS Segment Anything 2 | Direct node reuse with a toolbox launch/config profile and a thin prompt/result adapter |
| Coarse mesh-based 6D pose | Isaac ROS FoundationPose estimation | Direct node reuse; provide mesh/mask selection, object revision binding, symmetry metadata, and typed result mapping |
| Fast pose update after initialization | FoundationPose tracking node | Use for initialization continuity and as the source that seeds or reseeds M3T; keep its result available for comparison |
| Multi-body scene tracking | Not satisfied by the selected FoundationPose graph alone | Direct M3T adapter behind the small `Tracker` API |
| Track health and stale state | Partial upstream reset and support checks | Project health policy that evaluates timestamps, point-cloud support, innovation, drift evidence, and reseed outcomes |
| NITROS transport | Supported within NVIDIA graphs | Preserve NITROS inside the NVIDIA graph; cross into the task adapter only where standard ROS messages are needed |

## Version and image policy

- Base the perception image on the versioned Isaac ROS 4.6 development image or its documented Dockerfile inputs.
- Pin APT packages to the 4.6 repository and source dependencies to `release-4.6` or an exact audited commit.
- Record base-image digest, driver version, CUDA version, TensorRT version, GPU ID, model hashes, engine-build arguments, and package versions in named qualification reports.
- Keep model and TensorRT engine caches on persistent versioned mounts. Reject an engine whose model hash, GPU architecture, TensorRT version, or build options do not match its manifest.

## SAM2 adapter

The adapter owns object prompts, prompt-to-object ID mapping, mask validation,
timeout, and useful memory diagnostics. It does not own the SAM2 model or
inference implementation. The task-facing call uses explicit image and prompt
arguments. Source timestamp/frame remain available where the call crosses ROS.

Test prompt addition, replacement, removal, empty masks, label collisions, resolution mismatch, camera restart, Triton restart, and memory growth. The four-object corpus stays below the documented default object limit, but the adapter must still reject unsupported counts rather than truncate.

## FoundationPose adapter

The adapter obtains mesh, scale, canonical frame, symmetry data, and model
references from the locally loaded object asset. It validates rectified
RGB/depth/CameraInfo timestamps before submitting estimation. The result carries
the pose/frame/time plus upstream quality and debug details actually used by the
task or tracker.

Tracking configuration must expose auto-reset, point-cloud support, watchdog, QoS, and input topics. Test initial estimation, stable tracking, mask loss, depth holes, camera restart, large pose jump, object symmetry, wrong mesh scale, stale CameraInfo, and reset to estimation.

## Desktop and Jetson policy

The accepted deployment runs SAM2, FoundationPose, and M3T on the desktop. The NUC and Jetson publish sensors and hardware state. Do not add a Jetson inference deployment until Phase 07 records the exact Orin model, JetPack version, memory budget, and a task that benefits from moving inference onboard.

## Acceptance

- The pinned perception image builds on the desktop and records its source/image/model pins in the benchmark report.
- The D455 graph produces synchronized color, depth, CameraInfo, mask, coarse pose, and tracking outputs with declared QoS.
- Restarting any perception node produces stale/lost health, never a fresh reused pose.
- Repeated prompt and reset tests show bounded GPU memory over the two-hour run.
- Recorded-data results can be replayed without a robot, and their metrics include latency, update rate, accuracy, memory, and failure counts.
- Toolbox documentation links each public call to the NVIDIA node, topics, parameters, model assets, and limitation it uses.

## What this audit needs from me

Nothing. Exact camera serials, JetPack version, GPU assignment, and benchmark results are Phase 00/04 facts.
