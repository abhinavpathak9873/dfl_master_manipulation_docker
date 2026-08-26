# Simulator-neutral ROS behavior

## Goal

Document the small behavior actually shared by Gazebo, Genesis, and real robot
adapters after both simulator paths have been exercised.

## Task-script payoff

Shared calls such as arm motion, gripper control, base velocity, camera capture,
stop, and state inspection do not change solely because the mode changes.

## Retained behavior

- Namespaced joint/arm controller state and commands.
- Tool commands and useful feedback.
- Base command/odometry for Picker 1 and Picker 2.
- RGB-D, camera info, frames, source timestamps, and simulation clock.
- TF, readiness, reset, stop/cancel, collision/contact, and unsupported-operation
  reporting.

## Work

1. Compare the actual Gazebo, Genesis, and vendor-facing ROS graphs.
2. Prefer standard ROS/controller/sensor messages and actions.
3. Define only shared names, units, frames, timing, readiness, and stop semantics
   used by task or adapter code.
4. Keep simulator-only reset/contact/debug operations on concrete backends.
5. Define clear errors for unavailable force, contact, base, camera, or tool
   behavior; never fabricate support.
6. Add adapter-level checks that run the same small task operation in each mode.
7. Document how to inspect every path with ROS CLI and simulator tools.

## Outputs

- Compact shared behavior table and mode-difference table.
- ROS-facing checks for arm, tool, base, camera, TF/time, readiness, and stop.
- Clear backend responsibilities and unsupported-operation errors.

## Acceptance

- The table is derived from working integrations, not future predictions.
- No custom interface duplicates a standard ROS type.
- A task switches mode without changing shared calls.
- Legitimate mode-specific behavior remains accessible and documented.
- Failed/stale state cannot be presented as current or successful.

## Non-goals

- A simulator runtime, capability negotiation protocol, or false uniformity.
- Hiding the underlying ROS graph.
