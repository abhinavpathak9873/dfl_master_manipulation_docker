# Task package convention

## Goal

Give humans and agents one predictable place and shape for explicit task programs while keeping tasks outside the reusable toolbox.

## Inputs

- Task-facing value and config contracts
- Robot/tool/scene selectors
- Lifecycle and run-record requirements
- Current DFF task examples

## Outputs

- `.devcontainer/src/<task_name>` layout specification
- Minimal task package template
- One-command `ros2 run` entrypoint convention
- Task configuration and test fixture convention
- Task review checklist
- Example fixed-pose task migrated to the convention

## Work

1. Require each task package to be a direct child of `.devcontainer/src/` and contain package metadata, a Python module or scripts directory, an executable entry point, task-local configuration, tests, and a short README. Match the reference repository's sibling-package convention; never create a `tasks/` parent directory.
2. Construct `Robot` with explicit robot, gripper, scene, mode, and pipeline selectors near the top of the executable. Detailed values load through the config resolver.
3. Keep the manipulation sequence in `main()`. Use named stages and targeted `try/except` blocks only where the task has an explicit recovery decision.
4. Call `Robot.bringup()` once, start run recording, execute stages, and call `bringdown()` plus artifact flush in `finally`.
5. Keep reusable algorithms in toolbox or integration packages. A task may own poses, object choices, stage ordering, retry count, and task-specific acceptance.
6. Provide simulation fixtures and a dry configuration-resolution test that do not start hardware.
7. Document one launch-free execution command and optional `ros2 launch` wrapper when the task needs companion visualization.

## Interfaces and data

- Task package import surface
- Console entry point
- Task config and fixture paths
- Stage names recorded in run events

## Boundaries

- Does not create a central task daemon
- Does not hide task stages in a high-level pick/place function
- Does not allow a task to modify protected real-mode configuration

## Failure behavior

- Task startup reports selector/config errors before bringup.
- Unhandled operational failures still stop motion, close the run record, and clean owned processes.
- A task never catches a control-loss error and continues ordinary motion.

## Acceptance

- A new sample task fits the template without editing toolbox code.
- The sample task is discovered directly under `.devcontainer/src/<task_name>` and no package is nested below `.devcontainer/src/tasks/`.
- One command runs the task in either simulator by changing only the mode selector or an allowlisted launch argument.
- Tests verify stage order, cleanup on exception, and config capture.
- The task README names its robot/tool/scene assumptions and real-hardware qualification state.

## Parallel work

Can finish with run-record work. Phase 02 uses the template for all acceptance tasks.

## What this module needs from me

Nothing.
