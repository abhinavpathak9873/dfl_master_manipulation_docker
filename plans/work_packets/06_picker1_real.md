# 06 — Picker 1 real adapter

## Outcome

The reference task selects `mode="real"` and reuses the operations honestly
shared with Gazebo. Real-only setup and safety behavior remain explicit inside
the Picker 1 real adapter and visible through ROS/vendor tools.

## Work

- Add `Picker1Real` beside the Gazebo adapter and register
  `("picker1", "real")`.
- Record the actual controller generation, endpoint, mounted gripper, D455
  serial/calibration, frames, limits, and stop mechanisms in one small
  hardware-owned profile.
- Verify identity, fresh joint state, connected TF, active controllers, gripper,
  camera, and configured safety bounds in `bringup()`.
- Implement local stop/watchdog behavior where the vendor or network control
  path requires it.
- Keep unsupported simulator-only or hardware-only behavior explicit.

## Acceptance

- Changing only `mode` is sufficient for the subset genuinely shared by the
  two adapters.
- Real setup never silently falls back to simulation.
- ROS nodes, topics, actions, TF, controller state, and vendor diagnostics
  remain directly inspectable.
- A supervised smoke task proves move, cancel, stop, camera, gripper, and clean
  bringdown before the full grasp task.
- Representative trials record the exact task, object, calibration, and
  hardware combination. Qualification is scoped to that combination.

## Stop condition

Missing identity, calibration, controller support, or safe stop behavior blocks
real motion and reports the missing fact. It does not trigger a new lifecycle,
lease, or deployment framework.
