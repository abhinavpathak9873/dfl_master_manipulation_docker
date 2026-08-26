# Gazebo Harmonic with the Doosan emulator

## Goal

Provide the primary simulator path through the pinned Doosan Jazzy stack and official controller emulator, including multiple namespaced robots and all tool descriptions.

## Inputs

- Core container
- Accepted Doosan migration
- Robot/tool profiles
- Gazebo Harmonic/Jazzy pairing

## Outputs

- Single-robot M1013 and H2515 Gazebo launch profiles
- Concurrent Picker 1 and Picker 2 launch
- One emulator instance and unique port per arm
- Tool simulation adapters for suction and parallel-jaw behavior
- D455-compatible simulated RGB-D topics
- Reset, pause, clock, and artifact capture commands

## Work

1. Start Gazebo through the official Doosan Jazzy launch path. Keep the vendor emulator as controller authority and use `ros_gz`/`gz_ros2_control` as documented upstream.
2. Generate unique namespaces, emulator ports, controller managers, joint-state topics, TF prefixes, and spawn positions for every robot instance.
3. Mount each tool through project-owned xacro overlays. Model joint, collision, visual, TCP, and payload behavior separately from the driver.
4. Implement simulated VGC10/VGP20 attachment and release from contact plus configured vacuum rules. Implement 2FG14 joint/width/force feedback sufficient for shared gripper tests.
5. Expose namespaced RGB, depth, CameraInfo, simulated clock, and camera TF using the generic camera contract.
6. Define deterministic world reset and per-run seed handling. Reset must clear attached objects, controller goals, tool state, and dynamic objects.
7. Measure emulator CPU use and document the concurrent robot limit on the desktop.

## Interfaces and data

- Namespaced `FollowJointTrajectory`, `JointState`, controller-manager services, TF, and `/clock`
- Generic RGB-D topics and CameraInfo
- Shared gripper simulation services/actions defined later by the gripper contract
- Reset service or launch command consumed by local tests

## Boundaries

- Does not guarantee Genesis parity
- Does not model every material or pneumatic detail
- Does not implement Nav2

## Failure behavior

- Abort launch on duplicate namespace or port.
- Publish failed controller or sensor health instead of leaving a partially ready simulation marked healthy.
- Cancel active goals and stop controllers during reset.

## Acceptance

- M1013 and H2515 reach home through MoveIt in headless Gazebo.
- Picker 1 and Picker 2 run concurrently without topic, TF, controller, or port collisions.
- Every tool description loads and returns simulated state.
- A fixed object can be grasped, attached, moved, released, and reset.
- Clock and sensor timestamps are monotonic and consistent.

## Parallel work

Genesis spike may run in parallel after the shared profiles exist. The simulator contract consumes both results.

## What this module needs from me

Nothing.
