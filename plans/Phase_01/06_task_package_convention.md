# Task-script convention

## Goal

Make ordinary readable Python files the normal unit of robotics experimentation.

## Task-script payoff

A developer can copy `tasks/suitcase_pick.py`, edit robot/backend/parameters and
control flow, run it, and debug each call without learning a workflow format.

## Convention

```text
tasks/
  small_tray_pick.py
  bin_pick.py
  insertion_test.py
```

A task may have a nearby helper or data file when that improves readability.
Convert it into a ROS package under `.devcontainer/src/` only when installation,
ROS entry points, launch composition, or package resources are genuinely needed.

## Work

1. Keep imports, robot construction, poses/joints, object loading, backend
   construction, and robotics stages visible top-to-bottom.
2. Use ordinary Python functions, loops, branches, exceptions, and context
   managers for sequence and cleanup.
3. Allow direct backend imports and ROS calls for debugging or experiments.
4. Keep task-specific parameters in the script; share only stable physical facts
   or genuinely repeated helpers.
5. Provide one ROS-aware runner command that sets the required Compose profile,
   ROS environment, and Python path without wrapping task semantics.
6. Add a short task checklist: selected hardware/mode, frames/units, safe limits,
   stop/cleanup, required assets/models, and expected evidence.
7. Use the canonical API example as the readability test for public changes.

## Acceptance

- The representative tray task runs by a simple command from the core container.
- Retry remains an obvious `while` or `if`.
- A developer can step into the capability and concrete backend.
- No application package, launch tree, manifest, graph, session, or state-machine
  project is mandatory.

## Non-goals

- A task DSL, workflow YAML, behavior-tree requirement, or task generator.
- Preventing advanced tasks from using ROS packages when they actually benefit.
