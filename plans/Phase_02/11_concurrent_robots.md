# Concurrent Picker 1 and Picker 2

## Goal

Prove that two ordinary namespaced Robot objects can operate together without a
scheduler or generalized resource manager.

## Task-script payoff

A developer can construct `picker1` and `picker2`, run explicit Python
concurrency when needed, and debug each robot through its own ROS namespace.

## Work

1. Launch both M1013 composite profiles with distinct nodes, topics, actions,
   services, parameters, controllers, TF trees, bases, tools, cameras, and logs.
2. Instantiate two Robot objects and exercise independent bringup/attach,
   readiness, arm, gripper, base, camera, stop, and cleanup.
3. Define task-local threading/async examples only where operations truly run
   concurrently; sequential Python remains valid.
4. Keep shared physical lab exclusions as simple explicit checks/procedures near
   the hardware boundary.
5. Test same/different tools, one robot failure, one task cancellation, simulator
   reset, and cleanup ownership.
6. Verify MoveIt/controller/node names do not use hidden globals.
7. Document direct ROS commands for attributing messages and processes.

## Acceptance

- Both Pickers complete independent fixed tasks concurrently in both simulators.
- Commands, feedback, TF, logs, and failures remain attributable.
- Stopping/cleaning one does not stop the other unless an explicit lab-wide
  safety stop is invoked.
- No job scheduler, fleet manager, or distributed resource service is required.

## Non-goals

Automatic collision coordination between robots, task allocation, or fleet
orchestration.
