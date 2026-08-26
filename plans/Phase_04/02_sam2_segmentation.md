# SAM2 segmentation backend

## Goal

Expose SAM2 as a replaceable segmentation capability while containing its
accelerated dependencies in the appropriate Docker/ROS integration.

## Task-script payoff

`segmenter = Segmenter(backend="sam2", ...)` initializes once and
`segmenter.segment(image=rgb, prompt=...)` returns a documented mask without
changing later pose/tracking code.

## Work

1. Pin the selected SAM2/Isaac ROS image, model, preprocessing, prompt mode, and
   GPU requirements using current dependency evidence.
2. Implement the task-facing adapter through the direct segmentation mapping.
   Use a thin ROS client only if the selected Isaac ROS implementation requires
   a separate process.
3. Define accepted image encoding/shape, prompts, output mask encoding/shape,
   timestamp/frame propagation, and per-call optional backend settings.
4. Keep model initialization and GPU resources in the object/process across
   calls.
5. Preserve access to raw backend output and debug visualization.
6. Handle empty/no-object, multiple components, invalid prompt/image, timeout,
   process loss, GPU/model failure, and restart explicitly.
7. Measure mask quality, latency, throughput, warmup, and GPU memory on the D455
   dataset.
8. Add restart/reconnect behavior without a generalized pipeline manager.

## Acceptance

- Masks align with input pixels and preserve sample identity/time.
- The task API works with recorded and live D455 images.
- SAM2 dependencies remain isolated from the core image where required.
- Switching to another segmenter requires no pose/tracker task changes.
- Failures preserve their underlying ROS/model context.

## Non-goals

A segmentation service framework, universal prompt ontology, or hiding
backend-specific capabilities.
