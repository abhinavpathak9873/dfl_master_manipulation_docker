# SAM2 segmentation adapter

## Goal

Reuse Isaac ROS SAM2 for prompted segmentation of the four known objects while adding revision identity, prompt management, mask validation, health, and memory evidence.

## Inputs

- Pinned Isaac ROS 4.6 image
- D455 dataset
- Object records and prompts
- Plugin and tracking contracts

## Outputs

- SAM2 plugin manifest and launch profile
- Typed prompt adapter
- Mask normalization and object-ID mapping
- Segmentation health/status
- Recorded-data tests and GPU-memory instrumentation
- Known limitation record

## Work

1. Use the upstream node and Triton model path. Record model, ONNX, TensorRT engine, precision, input shape, GPU, and package versions.
2. Map typed point or bounding-box prompts to stable object/track IDs. Reject prompt reuse that would change identity without an explicit remove/reset.
3. Validate output resolution, label IDs, timestamp relationship, camera frame, non-empty area, connected components, depth support, and expected size bounds.
4. Normalize valid output to the shared segmentation result without copying the inference algorithm. Preserve the raw mask topic for inspection.
5. Expose prompt add/remove/reset, startup, memory, inference latency, dropped frame, and mask-invalid health.
6. Run repeated prompt, removal, reset, camera restart, Triton restart, and four-object sequences while measuring allocated and resident GPU memory.
7. Treat the documented live-camera memory growth as a release defect if memory continues monotonic growth beyond the accepted bound.

## Interfaces and data

- Isaac ROS SAM2 `add_objects`/remove behavior and mask topic
- Toolbox segmentation plugin
- Mask result used by FoundationPose, M3T health, and local alignment
- Diagnostics and run metrics

## Boundaries

- No custom SAM2 model implementation
- No open-world class detector
- No more than the four approved objects in v1 qualification

## Failure behavior

- Return invalid-mask, prompt, timeout, model, Triton, camera, memory, and reset errors separately.
- Never reuse the last valid mask with a new timestamp.

## Acceptance

- Mask IoU on the annotated qualification subset is at least 0.85 per object unless a stricter object qualification is recorded.
- Wrong labels, empty masks, and stale frames are rejected.
- Four object prompts survive ordinary camera motion and explicit reset.
- GPU memory after a 15-minute warmup remains within a 5% band during the rest of the two-hour test; no scheduled restart is used.
- All results identify model and object revision.

## Parallel work

FoundationPose work consumes valid mask fixtures and may proceed alongside live-memory testing.

## What this module needs from me

Nothing.
