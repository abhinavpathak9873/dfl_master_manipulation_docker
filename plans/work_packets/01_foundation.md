# 01 — task-facing foundation

## Outcome

A developer can import `dfl_toolbox`, create lightweight robotics values, and
construct named robot/perception capability objects without importing ROS or a
GPU stack.

## Task-script delta

```python
import dfl_toolbox as dfl

home = dfl.Joints([...], unit="rad")
place = dfl.Pose(position=[...], quaternion=[...], frame="odom")
robot = dfl.Robot(model="picker1", mode="gazebo", gripper="vgc10")
segmenter = dfl.perception.segmentation.create(
    backend="tensorrt.py",
    model="tray.engine",
)
```

## Work

- Implement `Pose` with validated position, normalized quaternion, frame,
  composition, and `offset`.
- Implement `Joints` with finite values, optional names, and degree-to-radian
  normalization.
- Implement a small backend resolver used by robotics capability facades.
- Keep backend dictionaries next to the relevant capability folders.
- Expose folder-local constructors such as
  `dfl.perception.segmentation.create(backend="tensorrt.py", ...)`; accept
  names with or without `.py`.
- Construct the backend once and call it repeatedly. Prefer explicit method
  arguments while leaving `implementation` available for unusual
  backend-specific inputs.
- Implement `Robot` as a convenience facade over a concrete robot adapter,
  exposing only the subassemblies that adapter actually has.
- Raise errors that name the requested backend and show the exact mapping file
  to edit.

## Acceptance

- Values import and run under plain Python with no ROS installation.
- Invalid vectors, units, quaternions, names, and frames fail clearly.
- Tests can supply a small fake backend without a plugin package or manifest.
- Backend-specific public methods remain reachable on the selected
  implementation.
- The public names match [`example_api.txt`](../../example_api.txt).

## Non-goals

ROS conversions, configuration layering, plugin discovery, lifecycle managers,
global result envelopes, and exhaustive failure taxonomies.
