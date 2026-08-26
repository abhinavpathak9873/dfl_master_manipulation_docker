# Direct backend mapping and extension

## Goal

Let developers swap robotics implementations by readable backend ID while
keeping the route to each implementation file obvious.

## Task-script payoff

Changing `backend="foundation_pose"` to `backend="gigapose"` changes only the
selected implementation; adding an experiment usually means one file, one
mapping entry, and focused dependency/test work.

## Design

Each capability owns a small mapping near its implementations:

```python
SEGMENTERS = {
    "sam2": SAM2Segmenter,
    "tensorrt": TensorRTSegmenter,
    "yolo": YOLOSegmenter,
}
```

The implementation files mirror the robotics folders. The optional user spelling
`backend="sam2.py"` normalizes to `sam2`. It never means arbitrary path import or
execution.

## Work

1. Define direct mappings for concrete categories only: robots/modes, grippers,
   segmentation, pose, tracking, alignment, and grasp generation as they appear.
2. Keep construction lazy enough that listing mapping keys does not initialize
   models, ROS processes, or hardware.
3. Forward meaningful constructor arguments and preserve access to the concrete
   implementation for backend-specific features and debugging.
4. Raise an error listing valid local IDs when a backend is unknown; preserve
   the original import/dependency exception when loading fails.
5. Put GPU/native dependencies in the Docker image that owns the backend.
6. Add a focused backend test next to each implementation and capability-level
   tests only for genuinely shared methods.
7. Document the two-step extension path in the capability folder.

## Acceptance

- One sample backend is added with one implementation file and one mapping edit.
- Switching backend IDs leaves unrelated task stages unchanged.
- Backend-specific optional methods remain reachable.
- No Python entry point, manifest, generated catalogue, discovery service,
  dependency-injection container, or qualification registry is required.

## Non-goals

- Third-party binary plugin distribution or arbitrary runtime imports.
- Artificially identical signatures for algorithms with different inputs.
