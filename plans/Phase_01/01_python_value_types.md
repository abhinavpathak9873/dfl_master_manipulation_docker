# Python values, results, and clear failures

## Goal

Define a small dependency-light set of values that makes task code readable and
prevents common unit/frame mistakes.

## Task-script payoff

Developers can write `Pose` and `Joints` directly, offset and transform poses,
and inspect useful motion/gripper/perception results without decoding ROS
messages in task logic.

## Initial values

- `Joints(values, names=None, unit="rad")` with validated length/name behavior.
- `Pose(position=..., quaternion=..., frame=...)` and the positional
  `Pose(x, y, z, q=..., frame=...)` convenience.
- Small transform/offset helpers backed by numerically tested geometry.
- Result values only where tasks consume fields: motion completion, gripper
  success/final width/force, and backend-specific details.
- Clear exceptions for invalid data, unsupported operation, missing asset,
  stale transform/data, planning failure, and unknown execution state.

## Work

1. Fix metres/radians and quaternion ordering; validate finite values and frames.
2. Keep the values importable without ROS, MoveIt, a running graph, or GPU
   packages.
3. Put ROS message conversions in ROS adapter modules.
4. Make values easy to print, compare with tolerances, serialize for focused
   debug records, and use from NumPy where needed.
5. Add only result/error fields exercised by current task examples and backend
   packets.
6. Include robot/tool/mode/backend and the failed assumption in actionable
   errors without inventing an enterprise error-code catalogue.

## Acceptance

- Canonical joint/pose examples are valid Python and round-trip through ROS
  adapters without unit/frame loss.
- Offset, composition, inversion, and anchor transformation tests cover known
  fixtures and invalid inputs.
- Importing values does not import ROS, models, or hardware drivers.
- Errors clearly distinguish unsupported behavior from failed/uncertain motion.

## Non-goals

- Symbolic geometry, a universal result envelope, or exhaustive future types.
- Mirroring every ROS message as a Python class.
