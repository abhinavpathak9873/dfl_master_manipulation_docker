# Container and Compose foundation

## Goal

Define reproducible development and runtime images for the core ROS stack, Isaac ROS perception, Genesis, ObjectDB, scan reconstruction, Git synchronization, and robot-side gateways. Keep dependencies and credentials isolated while every service follows the same configuration, object, calibration, and run-artifact contracts.

## Inputs

- Global architecture decisions
- Pinned dependency audit
- Container patterns from `dff_labs_docker`
- Current desktop GPU and driver inventory

## Outputs

- Ubuntu 24.04/Jazzy core Dockerfile and lock manifest under `scripts/`
- Isaac ROS 4.6 perception image definition
- Genesis 1.3.3 image definition after its smoke gate
- Lean ObjectDB image with Jazzy, FastAPI/Uvicorn, ROS adapters, Git, and Git LFS
- On-demand scan-worker image with reconstruction dependencies but no canonical write access
- Minimal ObjectDB-sync image with the only GitHub write credential
- Gateway image definition for x86 NUC and Jetson targets
- `.devcontainer/docker-compose-dfl-master-manipulation-ros2-jazzy.yml` with services named `core`, `perception`, `genesis`, `objectdb`, `scan-worker`, `objectdb-sync`, and per-host gateways
- `.devcontainer/devcontainer.json` using the `core` service and `/root/ros2_ws` workspace, matching the reference repository convention
- Mode profiles named `real`, `gazebo`, `genesis`, `scan`, and `gateway`
- Persistent mount map and environment-variable schema
- Health checks and one local build/smoke script

## Work

1. Record base-image digests, APT repositories, ROS packages, Python environments, CUDA/TensorRT dependencies, and toolchain versions. Use exact versions or content digests.
2. Build the core image around ROS 2 Jazzy, MoveIt 2, Pilz, Gazebo Harmonic, colcon, rosdep, RViz, rosbag, test tools, and the Doosan build prerequisites.
3. Keep Isaac ROS, Genesis, and scan reconstruction in separate images. Put every Dockerfile under `scripts/`, keep the Compose file beside `devcontainer.json`, and mount `.devcontainer/src` at `/root/ros2_ws/src`. Mount project source read-only where possible and write engines, logs, caches, build outputs, and scan staging to service-specific persistent paths.
4. Build ObjectDB without CUDA, simulator, camera, or vendor-control dependencies. Run its server on the container interface but publish it only as `127.0.0.1:8765` on the desktop.
5. Resolve ObjectDB and scan-staging host paths from explicit durable-root environment variables rather than tracked root-level `data/` directories. Mount the ObjectDB checkout read-write only in `objectdb`; mount its approved assets read-only in core, perception, and scan-worker. Mount scan staging read-write only in ObjectDB and scan-worker.
6. Keep GitHub credentials out of ObjectDB. Mount a repository-scoped write credential only in `objectdb-sync`; that service may push existing local commits but may not change canonical working-tree content.
7. Give ObjectDB no GPU, robot/camera device, or Docker socket. Give scan-worker no robot/camera device, Docker socket, or canonical write mount.
8. Use Linux host networking for ROS traffic on the trusted lab LAN. Require an explicit `ROS_DOMAIN_ID`, robot namespace, host role, and GPU selection in the environment file.
9. Define separate health fields for process, storage, ROS, scan-worker, backup freshness, GPU runtime, mounted configuration, writable run/staging paths, and clock. A healthy container does not imply robot readiness.
10. Add deterministic clean-build and incremental-build commands through numbered scripts that preserve the reference workflow: `scripts/0_build_and_push.sh`, `scripts/1_pull_images_and_repos.sh`, `scripts/2_system_level_deploy.sh`, and `scripts/3_compile_pkgs.sh`. Never resolve a floating dependency during a release build.
11. Document which service owns each device, port, writable path, GPU cache, lease, and credential. Reject duplicate ownership before processes start.
12. Add `scripts/env.sh`, `scripts/ros_entrypoint.sh`, `scripts/cyclonedds.xml`, and the `scripts/chrony/` clock configuration in the same locations and with the same responsibilities as the reference repository. Add service-specific scripts only under `scripts/`; do not create a root `docker/` directory.

## Interfaces and data

- Compose service names and profiles
- Environment keys for domain ID, host role, GPU device, workspace path, and persistent roots. The ROS Domain ID has to be 63.
- Shared mount contract for package-owned config/scenes/calibration and external durable roots for the ObjectDB checkout, scan staging, models, and run logs
- ObjectDB loopback port, Git-sync outbox/status path, and credential mount contract
- Container health status used by `Robot.bringup()` preflight

## Boundaries

- Does not create ROS package APIs
- Does not select perception algorithms beyond the accepted pins
- Does not provision host NVIDIA drivers or operating systems
- Does not put Docker lifecycle control inside ObjectDB

## Failure behavior

- Fail the build on an unpinned repository, missing checksum, unresolved rosdep, or incompatible CUDA/TensorRT combination.
- Fail startup when required mounts, GPU devices, or domain configuration are absent.
- Report device-ownership conflicts before starting ROS processes.
- Refuse writable canonical mounts outside ObjectDB and refuse a GitHub credential outside ObjectDB-sync.

## Acceptance

- `docker compose config` resolves without implicit values.
- `.devcontainer/src` is the only live host ROS source root and mounts at `/root/ros2_ws/src`; no root-level `src/`, `docker/`, `compose.yaml`, `tasks/`, `config/`, `calibration/`, `scenes/`, `models/`, `logs/`, or `data/` path is introduced.
- Each image builds twice from the lock inputs; the second build changes no dependency manifest.
- Core starts a Jazzy node and a headless Gazebo smoke world.
- Perception reports both GPUs and imports the pinned Isaac ROS packages.
- Genesis imports version 1.3.3 and executes a fixed joint-control smoke test.
- ObjectDB image starts a loopback health fixture and imports its HTTP, ROS, storage, and Git/LFS runtime dependencies with ROS and GPU services absent; Phase 03 owns the real APIs.
- Core, perception, and scan-worker cannot modify a canonical object fixture.
- Scan-worker can write its staging fixture but cannot reach a robot/camera device or Docker socket.
- ObjectDB-sync can push a test Git/LFS commit without exposing its credential to ObjectDB.
- Gateway image starts on the recorded NUC/Orin architecture or records a blocking compatibility result.

## Parallel work

Workspace manifest work may run in parallel. Simulator and API implementation waits for the accepted images and mount contract.

## What this module needs from me

Facts: exact NUC architecture/OS, Jetson model/JetPack, host driver, and desired GPU assignment. The implementer must collect them; no design choice is requested.
