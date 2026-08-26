# Phase 00 — foundation and simulation proof

## Goal

Create the reproducible Jazzy development base, import the required workspace without losing source provenance, prove the supported Doosan models, and establish what Gazebo and Genesis can honestly support. This phase resolves infrastructure facts before public toolbox contracts freeze.

## Settled decisions

- ROS 2 Jazzy on Ubuntu 24.04 containers.
- Gazebo Harmonic is the primary simulator.
- Genesis parity is required, but its official-emulator bridge must pass an evidence gate.
- Doosan Jazzy is pinned to commit `816ecb5d1c2599303eaf9540216afa03552f80ad`.
- Picker 1 and Picker 2 are M1013 profiles; H2515 is separate.
- VGC10 one cup, VGC10 four cups, VGP20, and 2FG14 are supported tool profiles.
- Core, perception, Genesis, ObjectDB, scan reconstruction, Git synchronization, and gateway workloads use separate Compose services.
- ObjectDB runs without GPU, device, or Docker-socket access. Only it may mount canonical object data read-write.

## Work packets

| Packet | Result |
|---|---|
| [01](01_container_and_compose.md) | Reproducible images, services, mounts, environment, and health checks. |
| [02](02_workspace_imports.md) | Pinned dependency manifest and provenance-preserving workspace import. |
| [03](03_doosan_jazzy_migration.md) | Accepted M1013/H2515 vendor baseline for real and virtual control. |
| [04](04_robot_tool_scene_profiles.md) | Stable profile IDs and physical composition records. |
| [05](05_gazebo_emulator.md) | Multi-robot Gazebo launch through the official emulator. |
| [06](06_genesis_bridge_spike.md) | Evidence for or against the required emulator-backed Genesis contract. |
| [07](07_simulator_contract.md) | One ROS controller/sensor contract shared by task code. |
| [08](08_fixed_task_matrix.md) | Fixed-task smoke results across the 24 simulator combinations. |

## Order and parallel work

Start 01 and 02 together after the pins are checked. Packet 03 follows the workspace import; Packet 04 can inventory profile data in parallel. Packet 05 depends on 01, 03, and 04. Packet 06 depends on the same accepted descriptions and emulator facts. Packet 07 starts after both simulator paths have evidence. Packet 08 runs last. A failed Genesis gate stops 07 and 08 for Genesis only and returns the requirement for review.

## Upstream inputs

- [Global decisions](../decisions/000_global_architecture.md)
- [Source inventory](../research/00_source_inventory.md)
- [Dependency audit](../research/01_dependency_audit.md)

## Exit criteria

- Core and GPU images build from locked inputs and report their manifests.
- ObjectDB, scan-worker, and Git-sync images build and pass mount, device, port, and credential-isolation checks.
- M1013 and H2515 load with valid descriptions, limits, controllers, and MoveIt configurations.
- Picker 1 and Picker 2 run concurrently in Gazebo with separate namespaces, ports, TF, and controller managers.
- All tool meshes and control stubs load without changing the vendor source tree.
- Genesis has an accepted bridge result or a blocking decision record.
- The fixed-task matrix produces indexed run artifacts for every supported simulator case.

## What this phase needs from me

Facts: access to the installed arms, controller versions, desktop GPU settings, NUC/Orin details, and calibration files when their packets reach hardware checks. Decisions: none unless the Genesis or vendor-driver evidence gate fails.
