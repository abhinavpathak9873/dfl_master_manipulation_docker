# Robot lifecycle and task-owned bringup

## Goal

Make robot setup, readiness, attach, stop, and cleanup convenient without a
separate robotics runtime.

## Task-script payoff

`robot.bringup()` starts what the selected robot/mode needs; the developer can
still inspect the launch process and ROS graph, or attach explicitly to a stack
they started themselves.

## Work

1. Resolve the concrete robot, mode, tool, camera, scene, namespace, and launch
   adapter from the visible constructor.
2. Let bringup own a normal ROS launch subprocess/process tree and record only
   enough local ownership to stop what it started.
3. Provide explicit attach mode for an intentionally running graph; never kill
   or silently reuse an unrelated healthy stack.
4. Check concrete readiness: description, TF, controllers, arm state, selected
   tool, camera/base where present, MoveIt, simulator clock, and required
   cross-process backends.
5. Keep component objects inspectable and direct lower-level backends importable.
6. On signals/exceptions, issue safe stop where needed, cancel owned work, and
   clean up owned processes. Do not auto-home or auto-resume after uncertainty.
7. Return clear readiness/unsupported errors naming the missing ROS/vendor fact.
8. Keep ObjectDB authoring, scan state, run recording, and Compose control
   outside lifecycle. Compose may already have started dependency containers.

## Acceptance

- Bringup/cleanup works repeatedly in Gazebo and Genesis without orphaning owned
  processes.
- Attach does not take ownership of another stack.
- Readiness rejects wrong robot/tool/namespace, stale state, or missing
  controllers.
- Real-mode interruption results in an explicit safe stop and fresh-run
  requirement.
- No session service, lease authority, or lifecycle coordinator is involved.

## Non-goals

A process supervisor, distributed ownership protocol, or hidden ROS launch
replacement.
