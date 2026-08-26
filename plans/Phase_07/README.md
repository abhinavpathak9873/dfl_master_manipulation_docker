# Phase 07 — gateways, deployment support, qualification, and release

## Goal

Make the Dockerized toolbox reliable on the actual lab topology and document
what is qualified, without turning it into a deployment platform.

## Task-script payoff

A developer can start the needed mode, see exactly which host/process owns a
device, debug ROS/DDS directly, recover safely, and trust stated simulator/real
limitations.

## Packets

1. [Robot-side gateways](01_gateway_services.md)
2. [DDS, QoS, bandwidth, and clock](02_dds_qos_and_clock.md)
3. [Desktop Compose profiles](03_desktop_compose.md)
4. [Restart and explicit recovery](04_session_recovery.md)
5. [Hardware commissioning](05_hardware_commissioning.md)
6. [Gazebo and Genesis parity](06_simulator_parity.md)
7. [Installed real qualification](07_real_qualification.md)
8. [Architecture, API, module, and agent documentation](08_module_documentation.md)
9. [Dependency upgrades and internal release](09_dependency_upgrades_and_release.md)

## Smallest sufficient design

- Desktop owns task logic, planning, perception, tracking, and grasp decisions.
- NUC/Jetson gateways own only device-side work that must run there.
- Use normal ROS 2/DDS on a trusted lab LAN.
- Compose profiles start dependency groups, not task workflows.
- Recovery always stops and revalidates; no automatic motion resume.
- Commissioning and qualification are plain records plus executable checks.
- Releases pin what was actually tested and include rollback.

## Exit evidence

The declared modes and installed combinations have reproducible Docker commands,
network/clock evidence, commissioning records, parity results, supervised task
trials, limitations, diagnostics, documentation, pins, and rollback.

## Non-goals

Cluster orchestration, remote production deployment, service mesh, auto-update,
high availability, or a generalized operations runtime.
