# Desktop Compose orchestration

## Goal

Start task and scan workloads from declared configurations while keeping ObjectDB available in every mode and enforcing GPU, device, port, writable-path, lease, and credential ownership.

## Inputs

- Phase 00 images/Compose foundation
- Gateway and network profiles
- All runtime launch contracts
- Resolved configuration and plugin registry
- ObjectDB, scan-worker, Git-sync, and lease contracts

## Outputs

- Desktop Compose profiles for real, Gazebo, and Genesis modes
- Exclusive scan profile and one-command scan launcher
- Always-on ObjectDB plus Git-sync orchestration
- GPU assignment profiles
- Service dependency/readiness graph
- One-command task launch wrapper
- Resource conflict checks
- Startup/shutdown tests

## Work

1. Include `objectdb` in real, Gazebo, and Genesis modes. Compose only the other services required by the selected mode and pipeline: real does not start simulators; Gazebo does not start Genesis; ordinary task modes do not start scan-worker.
2. Assign the RTX PRO 4500 and RTX A4000 through named host profiles after Phase 04 measurements. Record GPU UUID, workload, and memory budget.
3. Start ordinary task services in dependency order: ObjectDB storage/resolve, network/time checks, gateways or simulator, core robot/MoveIt, perception, then task lease and task.
4. Gate each edge on the owning health contract rather than fixed sleep. Keep camera and model warmup visible in events.
5. Add one `dfl scan` command that selects the fixed Picker 1 scan profile and starts ObjectDB, network/time checks, its gateway/core path, perception, and scan-worker. It refuses any task/scan or stale-unverified lease and identifies the owner; it never queues or cancels the owner.
6. Keep ObjectDB in read/edit mode when scan-worker stops. Start `objectdb-sync` with a repository-scoped credential and no device/GPU access; a sync failure affects backup health, not ObjectDB readiness.
7. Resolve namespaces, ports, mounts, models, object roots, staging root/quota, calibration, scene, and log path from the frozen config snapshot.
8. Detect duplicate device, namespace, port, GPU cache, canonical writer, staging writer, lease, and credential ownership before launch.
9. Shutdown task or scan action first, then active control, perception/scan-worker, core, and simulator. Keep ObjectDB and Git sync available; preserve artifacts and gateway stop availability until commands are quiescent.

## Interfaces and data

- Compose profiles and environment files
- Task launch wrapper
- Scan launch wrapper and exclusive lease preflight
- Health/readiness dependencies
- Resource ownership map

## Boundaries

- Does not replace ROS launch inside services
- Does not run all GPU services by default
- Does not kill independent unowned lab processes
- Does not let ObjectDB launch containers or expose the Docker socket

## Failure behavior

- Failed readiness stops dependent startup and cleans owned services.
- Resource conflict fails before device access.
- Shutdown timeout escalates stop but records the remaining process.
- Active/stale lease fails scan startup without changing the owner. Git push failure reports stale backup health and continues retrying.

## Acceptance

- One command runs the representative task in each mode.
- One command starts the complete scan environment and opens or prints the loopback ObjectDB URL.
- Mode selection starts only required services.
- No fixed startup sleep is required for correctness.
- GPU and device ownership conflicts are detected.
- Interrupted startup and shutdown leave no owned stale process.
- ObjectDB stays readable when ROS, perception, scan-worker, or GitHub is unavailable and does not claim those dependencies ready.
- Mount and credential checks prove one canonical writer and one GitHub credential owner.

## Parallel work

Consumes gateway/network facts. Documentation can describe accepted commands as they stabilize.

## What this module needs from me

Nothing.
