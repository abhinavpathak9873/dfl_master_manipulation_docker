# Container and Compose foundation

## Goal

Define reproducible development and runtime images for the core ROS stack, Isaac ROS perception, Genesis, ObjectDB, scan reconstruction, Git synchronization, and robot-side gateways. Keep dependencies and credentials isolated while every service follows the same configuration, object, calibration, and run-artifact contracts.

## Inputs

- Global architecture decisions
- Pinned dependency audit
- Container patterns from `dff_labs_docker`
- Current desktop GPU and driver inventory

## Outputs

- Ubuntu 24.04/Jazzy core definition at `scripts/Dockerfile.core` and its lock manifest
- Isaac ROS 4.6 perception definition at `scripts/Dockerfile.perception`
- Genesis 1.3.3 definition at `scripts/Dockerfile.genesis` after its smoke gate
- Lean ObjectDB definition at `scripts/Dockerfile.objectdb`, with Jazzy, FastAPI/Uvicorn, ROS adapters, Git, and Git LFS
- On-demand reconstruction definition at `scripts/Dockerfile.scan-worker`, with no canonical write access
- Minimal Git synchronization definition at `scripts/Dockerfile.objectdb-sync`, with the only GitHub write credential
- Gateway definitions under `scripts/`, split by x86 NUC and Jetson target when their base images or architectures differ
- Canonical desktop Compose file at `.devcontainer/docker-compose-dfl-master-manipulation-ros2-jazzy.yml` with services named `core`, `perception`, `genesis`, `objectdb`, `scan-worker`, and `objectdb-sync`
- Additional Compose files under `.devcontainer/` where deployment boundaries justify them, initially `.devcontainer/docker-compose-gateway-ros2-jazzy.yml` for per-host gateways
- `.devcontainer/devcontainer.json` using the `core` service and `/root/ros2_ws` workspace, matching the reference repository convention
- Mode profiles named `real`, `gazebo`, `genesis`, `scan`, and `gateway`
- Persistent mount map and environment-variable schema
- Health checks and one local build/smoke script

## Work

1. Record base-image digests, APT repositories, ROS packages, Python environments, CUDA/TensorRT dependencies, and toolchain versions. Use exact versions or content digests.
2. Build the core image around ROS 2 Jazzy, MoveIt 2, Pilz, Gazebo Harmonic, colcon, rosdep, RViz, rosbag, test tools, and the Doosan build prerequisites.
3. Keep Isaac ROS, Genesis, and scan reconstruction in separate images. Put Dockerfiles under `scripts/`, keep every Compose file under `.devcontainer/` beside `devcontainer.json`, and mount `.devcontainer/src` at `/root/ros2_ws/src`. Use one canonical desktop Compose file plus separate files or overrides only for materially different deployment targets such as gateway hosts; do not duplicate service definitions without a declared owner. Mount project source read-only where possible and write engines, logs, caches, build outputs, and scan staging to service-specific persistent paths.
4. Build ObjectDB without CUDA, simulator, camera, or vendor-control dependencies. Run its server on the container interface but publish it only as `127.0.0.1:8765` on the desktop.
5. Mount `data/object_db` read-write only in `objectdb`; mount its approved assets read-only in core, perception, and scan-worker. Mount `data/scan_staging` read-write only in ObjectDB and scan-worker. Allow environment variables to relocate these durable roots without changing their repository-relative defaults.
6. Keep GitHub credentials out of ObjectDB. Mount a repository-scoped write credential only in `objectdb-sync`; that service may push existing local commits but may not change canonical working-tree content.
7. Give ObjectDB no GPU, robot/camera device, or Docker socket. Give scan-worker no robot/camera device, Docker socket, or canonical write mount.
8. Use Linux host networking for ROS traffic on the trusted lab LAN. Require an explicit `ROS_DOMAIN_ID`, robot namespace, host role, and GPU selection in the environment file.
9. Define separate health fields for process, storage, ROS, scan-worker, backup freshness, GPU runtime, mounted configuration, writable run/staging paths, and clock. A healthy container does not imply robot readiness.
10. Add deterministic clean-build and incremental-build commands through numbered scripts that preserve the reference workflow: `scripts/0_build_and_push.sh`, `scripts/1_pull_images_and_repos.sh`, `scripts/2_system_level_deploy.sh`, and `scripts/3_compile_pkgs.sh`. Never resolve a floating dependency during a release build.
11. Document which service owns each device, port, writable path, GPU cache, lease, and credential. Reject duplicate ownership before processes start.
12. Add `scripts/env.sh`, `scripts/ros_entrypoint.sh`, `scripts/cyclonedds.xml`, and the `scripts/chrony/` clock configuration in the same locations and with the same responsibilities as the reference repository. Add service-specific scripts and Dockerfiles under `scripts/`, using clear service suffixes where several are needed.

## Interfaces and data

- Compose service names and profiles
- Environment keys for domain ID, host role, GPU device, workspace path, and persistent roots. The ROS Domain ID has to be 63.
- Shared mount contract for package-owned config/scenes plus project-level `calibration`, `data/object_db`, `data/scan_staging`, `models`, and `logs/runs`
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
- `.devcontainer/src` is the live host ROS source root and mounts at `/root/ros2_ws/src`; every Compose file is under `.devcontainer/`, and Dockerfiles plus operational scripts are under `scripts/`.
- Multiple Compose files resolve together or independently as documented, with no conflicting container, port, device, volume, or service ownership.
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
