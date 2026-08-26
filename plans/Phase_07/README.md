# Phase 07 — gateways, orchestration, recovery, and release

## Goal

Deploy the accepted desktop and robot-side components across the lab network, qualify reconnect and stop behavior, prove simulator parity and installed hardware reliability, and publish compact documentation plus reproducible release evidence.

## Settled decisions

- Desktop owns manipulation intelligence; NUC and Orin are gateways.
- Use a trusted wired LAN and one configured ROS domain.
- Keep network setup simple but test discovery, QoS, bandwidth, clock, reconnect, and duplicate namespaces.
- No automatic task resume after uncertain state.
- All tests run on local lab machines.
- Real routine-use qualification is at least 29 successes in 30 trials with zero unsafe events.
- Dependency upgrades are manual and pinned.
- ObjectDB runs in every mode; scan-worker is on-demand, and ObjectDB-sync owns the only GitHub credential.
- Physical scanning is an exclusive Picker 1 maintenance profile with explicit start and explicit stage resume.

## Work packets

| Packet | Result |
|---|---|
| [01](01_gateway_services.md) | Minimal NUC/Orin sensor and hardware relay services. |
| [02](02_dds_qos_and_clock.md) | Selected RMW profile, bandwidth, discovery, and time health. |
| [03](03_desktop_compose.md) | One-command task/scan orchestration, ObjectDB services, and GPU assignment. |
| [04](04_session_recovery.md) | Restart/reconnect and lease behavior without stale ownership or auto-resume. |
| [05](05_hardware_commissioning.md) | Versioned identity, calibration, endpoint, and stop records. |
| [06](06_simulator_parity.md) | Full Gazebo/Genesis task-contract evidence. |
| [07](07_real_qualification.md) | Installed task 30-trial release evidence. |
| [08](08_module_documentation.md) | Architecture, API, ROS graph, module index, and agent guidance. |
| [09](09_dependency_upgrades_and_release.md) | Locked release manifest, upgrade procedure, and final checklist. |

## Order and parallel work

Gateway inventory and network tests start early. Desktop Compose consumes accepted images, ObjectDB mounts, leases, and service contracts. Commissioning includes the single Picker 1 scan station and feeds recovery plus real qualification. Simulator parity can run alongside hardware commissioning. Documentation develops from accepted packets and freezes before release. Git-sync and dependency/release work finish last.

## Upstream inputs

- All accepted Phase 00–06 contracts and artifacts
- NUC, Jetson, desktop, robot, tool, base, camera, and network access
- Global decisions and traceability

## Exit criteria

- Desktop and gateways discover each other, remain time-synchronized, and report loss/reconnect clearly.
- One command starts the selected desktop stack without duplicate hardware ownership.
- One command starts exclusive scanning, refuses an active task, and leaves ObjectDB available when scan-worker is stopped.
- Desktop death and gateway restart stop commands and never resume a task.
- Gazebo and Genesis pass the required fixed and perception-to-grasp parity cases.
- Installed tasks meet their declared 30-trial threshold with zero unsafe events.
- Documentation lets a human or agent find one capability, ROS graph, config, fixture, and failure path.
- The release manifest pins every source, image, model, calibration, object revision, and qualification artifact.
- A clean private Git/LFS clone reproduces the approved ObjectDB data, and stale remote-backup health is visible.

## What this phase needs from me

Facts: exact gateway hardware/software, network topology, installed configurations, and test schedule. Decisions: none unless a release gate fails.
