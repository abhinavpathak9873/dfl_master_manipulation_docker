# Concurrent Picker 1 and Picker 2

## Goal

Prove that one desktop can own and observe both M1013 picker stacks at the same time without shared namespace, process, controller, TF, scene, tool, or run-state collisions.

## Inputs

- Lifecycle, motion, gripper, base, namespace, and simulator contracts
- Picker 1 and Picker 2 profiles
- Dual-emulator Gazebo and Genesis capability

## Outputs

- Dual-robot bringup profile
- Per-robot API handles and launch ownership
- Resource-lock rules
- Concurrent motion/base/tool test tasks
- Isolation and contention report

## Work

1. Start each robot with its own namespace, controller manager, MoveIt context, emulator port, TF tree, tool driver, base driver, diagnostics, and run subrecord.
2. Allow a task process to create two `Robot` instances or a small `RobotGroup` that exposes them by ID without merging their state.
3. Define resource locks for shared cameras, GPUs, scenes, and hardware endpoints. A resource cannot have two writers.
4. Run independent arm trajectories concurrently, then staggered tool and base commands. Record timing and verify that cancel/stop targets only the requested robot.
5. Inject failure in one robot's controller, tool, base, and gateway. The other may continue only if its own inputs and shared resources remain healthy and the task explicitly permits it.
6. Keep planning scenes separate unless a later task supplies a reviewed shared-world coordinator. V1 does not plan robot-robot interaction.
7. Measure desktop and emulator resource use and document supported concurrent profiles.

## Interfaces and data

- Multiple `Robot` instances keyed by profile ID
- Per-robot launch ownership and run events
- Resource-lock registry scoped to the task process

## Boundaries

- Does not coordinate collision avoidance between arms
- Does not support shared manipulation or synchronized trajectory execution
- H2515 concurrency is not a v1 release gate

## Failure behavior

- Duplicate resource ownership or namespace fails before motion.
- A global stop command may stop all robots; ordinary cancel remains robot-scoped.
- Shared clock or network failure marks both affected stacks unhealthy.

## Acceptance

- Picker 1 and Picker 2 plan and execute at the same time in Gazebo.
- Per-robot cancel, tool command, base stop, diagnostics, and artifacts stay isolated.
- Failure injection in one stack does not address the other's controllers.
- No unprefixed DSR topic or TF appears.
- Resource usage is recorded against the desktop capacity.

## Parallel work

Follows core lifecycle/motion and one working gripper. Tool-specific qualification can continue.

## What this module needs from me

Nothing.
