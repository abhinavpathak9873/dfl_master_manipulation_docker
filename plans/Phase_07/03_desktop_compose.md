# Desktop Compose profiles

## Goal

Provide simple Docker commands for each dependency/mode combination while
keeping experiment logic in Python.

## Task-script payoff

A developer starts the required environment, runs `python tasks/...`, and can
inspect/stop each underlying ROS/model/simulator process directly.

## Profiles

- Development/core.
- Gazebo.
- Genesis.
- Real hardware with selected gateways.
- Accelerated perception and native M3T as needed.
- ObjectDB authoring.
- Scan: authoring plus on-demand reconstruction and required capture dependencies.
- Diagnostic/qualification variants only where they add concrete flags or
  artifacts.

## Work

1. Compose the Phase 00 service definitions rather than duplicating images,
   mounts, environment, and health checks.
2. Parameterize robot/tool/scene/mode/namespace through explicit environment or
   command arguments consumed by normal launch/adapters.
3. Make GPUs, displays, camera/USB devices, host networking, ROS domain, gateway
   endpoints, object/model/calibration mounts, and writable outputs visible.
4. Start ObjectDB/scan only for authoring; normal real/Gazebo/Genesis tasks mount
   approved object files and do not depend on those services.
5. Make readiness diagnostic, not a workflow scheduler: show which required
   process/ROS fact is absent.
6. Provide one-command start/stop/log/status plus raw Compose commands.
7. Test conflicting profiles, missing device/GPU/network, stale containers,
   partial startup, stop, and rebuild.
8. Keep robot bringup ownership clear: Compose owns dependency containers;
   `Robot.bringup()` or explicit launch owns the selected ROS launch process as
   documented.

## Acceptance

- Each common mode starts reproducibly from a clean checkout.
- Task sequence exists only in the Python task.
- Authoring/scan processes are absent from ordinary task startup.
- Stop affects only the selected project/profile and preserves declared data.
- Direct Docker logs and ROS graph inspection identify partial readiness.

## Non-goals

A Compose control plane, service discovery layer, workflow graph, production
deployment system, or always-on object Git-sync sidecar.
