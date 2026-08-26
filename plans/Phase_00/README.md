# Phase 00 — Docker foundation and simulation proof

## Goal

Create the reproducible Docker/ROS base and prove the complete declared robot,
tool, and simulator scope without building a runtime platform.

## Task-script payoff

A developer can select Picker 1, Picker 2, or H2515; select any supported
gripper and scene; choose Gazebo or Genesis; bring the robot up; and run a small
motion script through the same visible API.

## Required scope

- Picker 1/M1013 and Picker 2/M1013 as separate namespaced mobile manipulators.
- H2515 as a separate robot profile.
- VGC10 one cup, VGC10 four cups, VGP20, and 2FG14.
- Gazebo Harmonic as the primary simulator and Genesis as a required second mode.
- ROS 2 Jazzy, MoveIt, robot descriptions/controllers, cameras, scenes, and
  Docker/devcontainer workflows.
- All 12 robot/tool selections exercised in both simulators.

## Packets

1. [Container and Compose foundation](01_container_and_compose.md)
2. [Workspace imports and source provenance](02_workspace_imports.md)
3. [Doosan Jazzy migration](03_doosan_jazzy_migration.md)
4. [Robot, tool, camera, scene, and mode profiles](04_robot_tool_scene_profiles.md)
5. [Gazebo Harmonic with the Doosan emulator](05_gazebo_emulator.md)
6. [Genesis emulator-backed bridge spike](06_genesis_bridge_spike.md)
7. [Simulator-neutral ROS behavior](07_simulator_contract.md)
8. [Fixed-task simulator matrix](08_fixed_task_matrix.md)

## Smallest sufficient design

- Keep the established `.devcontainer/`, `.devcontainer/src/`, `scripts/`,
  calibration/data/models/logs, and Compose-profile layout.
- Split containers only for incompatible dependencies, GPUs/devices, or host
  placement.
- Use Compose to start processes; keep task sequencing in Python.
- Use readable robot/tool/scene records rather than a universal configuration
  framework.
- Keep simulator differences in their adapters and fail clearly when an
  operation is unsupported.

## Exit evidence

- Clean Docker builds and documented one-command profiles.
- Explicit mounts, GPUs, devices, networking, health checks, and persistent
  paths.
- M1013 and H2515 descriptions/controllers load in Jazzy.
- Fixed joint, Cartesian, gripper, camera, and stop tasks run for the declared
  Gazebo matrix.
- Genesis either demonstrates the same useful ROS behavior or produces evidence
  and a preserving alternative for review.
- The 24 simulator matrix runs have compact pass/fail evidence and no false
  claims about unimplemented hardware behavior.

## Non-goals

- A Compose control plane, service mesh, workflow graph, or deployment product.
- A simulator abstraction designed ahead of the two concrete integrations.
