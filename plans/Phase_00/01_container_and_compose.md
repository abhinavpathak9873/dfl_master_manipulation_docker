# Container and Compose foundation

## Goal

Create reproducible ROS 2 Jazzy development/runtime images and small Compose
profiles that support the toolbox's real dependency and device boundaries.

## Task-script payoff

A developer can enter the devcontainer, start the required mode, and run a task
without manually reconstructing ROS, MoveIt, GPU, simulator, camera, or vendor
dependencies.

## Retained scope

- `.devcontainer/devcontainer.json`, Dockerfiles, Compose files, and the ROS
  workspace under `.devcontainer/src/`.
- Core Jazzy/MoveIt/Gazebo, accelerated perception, M3T if isolated, Genesis,
  ObjectDB authoring, on-demand scan worker, and gateway images as justified.
- NVIDIA GPU access, display, D455/USB, robot network, mounts, logs, health
  checks, and safe real-mode defaults.
- `scripts/` commands for build, start, stop, inspect, validate, and clean
  developer-owned outputs.

## Work

1. Inventory host OS, Docker/NVIDIA runtime, GPU, cameras, robot interfaces,
   display needs, UID/GID, and network requirements.
2. Define a small base image strategy and pin ROS/Jazzy, CUDA/TensorRT, simulator,
   vendor, and Python sources in their owning images.
3. Keep the core image sufficient for ROS, MoveIt, Doosan, task Python, and
   Gazebo; isolate incompatible perception/Genesis/reconstruction dependencies.
4. Define Compose profiles for development, Gazebo, Genesis, real hardware,
   perception, ObjectDB authoring, scanning, and gateways. Profiles may compose
   services rather than duplicate definitions.
5. Make every bind/volume path and read/write owner explicit. Runtime task
   consumers read approved object assets directly.
6. Add useful service health checks based on the real process boundary, plus
   commands to inspect raw Compose logs and ROS state.
7. Verify graceful stop and that real/device profiles do not start accidentally
   from a normal development command.
8. Document rebuild scope and cache ownership so dependency iteration remains
   fast.

## Outputs

- Dockerfiles/devcontainer and Compose profiles with pinned inputs.
- Mount/device/GPU/network table and durable-directory layout.
- Human-readable `scripts/` entry points and raw equivalent commands.
- Clean-build and smoke-check record.

## Acceptance

- A clean checkout builds without hidden host state.
- Core, Gazebo, Genesis, perception, authoring, scan, and gateway profiles expose
  only required devices and writable mounts.
- A task can run in the core/Gazebo profile without ObjectDB authoring or scan
  services.
- Stop removes only project-started containers/processes and preserves declared
  data.
- Logs and underlying ROS/Compose state remain directly inspectable.

## Non-goals

- One container per capability, a service registry, or Compose-encoded task flow.
- Production clustering, autoscaling, high availability, or remote deployment.
