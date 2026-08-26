# Simulator-neutral ROS contract

## Goal

Freeze the ROS actions, topics, frames, clock, reset, controller, tool, and sensor behavior that task code will use in Gazebo and Genesis.

## Inputs

- Accepted Gazebo behavior
- Genesis bridge gate result
- Robot/tool/camera profiles
- Standard ROS control and sensor message types

## Outputs

- Simulator contract specification
- Topic/action/frame map per robot namespace
- Controller and gripper state machines
- Reset and seed semantics
- Contract-test suite runnable against either simulator
- Known simulator-specific tolerance table

## Work

1. Define the required arm action as namespaced `control_msgs/action/FollowJointTrajectory`, with standard goal, feedback, result, cancel, tolerance, and timestamp semantics.
2. Define JointState, robot-state TF, camera RGB/depth/CameraInfo, odometry for picker bases, Twist command, tool state, diagnostics, and simulated clock.
3. Define controller readiness and reset states. A reset transitions through unavailable, initializing, and ready; task execution is rejected before ready.
4. Define gripper simulation outcomes for suction acquired/lost and parallel-jaw open/closed/object-detected. Keep physics implementation private to each simulator.
5. Define deterministic seed and scene-loading behavior. A test names the same robot, tool, scene, and task in either mode.
6. Set simulator-specific numerical tolerances for joint endpoints, Cartesian endpoints, contact, attachment, and timing. Keep logical success and failure codes identical.
7. Implement shared black-box tests without importing either simulator's Python API.

## Interfaces and data

- Standard ROS control, sensor, geometry, nav, TF, clock, and diagnostics interfaces
- Shared tool-state interface later frozen in Phase 02
- Reset/readiness contract consumed by `Robot.bringup()`

## Boundaries

- Does not require identical rendering, contacts, latency, or physics
- Does not expose simulator-native objects to task code

## Failure behavior

- Treat missing feedback, stale state, ignored cancel, or false-ready status as contract failure.
- A simulator-specific limitation must be explicit; it cannot return generic success.

## Acceptance

- The same test binary selects Gazebo or Genesis only through configuration.
- Both backends pass action lifecycle, state, TF, clock, reset, camera, and tool-state tests.
- Tolerance differences are named and justified.
- No task fixture imports `gz`, Genesis, or simulator-native types.

## Parallel work

Phase 01 types may begin from this accepted wire contract. Fixed-task matrix follows.

## What this module needs from me

Nothing if the Genesis gate passes.
