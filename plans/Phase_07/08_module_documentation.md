# Architecture, API, module index, and agent guidance

## Goal

Publish compact documentation that lets a developer or agent find one capability, inspect its ROS implementation, configure it, run its fixture, and diagnose a failure without loading the whole repository.

## Inputs

- Accepted public contracts and plugin manifests
- Launch/config/source layout
- All module limitations and qualification artifacts
- CaP-X interface audit

## Outputs

- Root README and quick start
- `docs/architecture.md`
- `docs/API.md`
- Generated `docs/module_index.md`
- Per-module compact docs
- ROS graph/topic/action/frame tables
- Task-author and implementation-author guides
- Decision and troubleshooting index

## Work

1. Describe the desktop/gateway/process architecture, including ObjectDB, scan-worker, Git-sync, package boundaries, mounts, credentials, leases, data flow, ownership, and phase-tested deployment modes.
2. Document every public Python type/method with signature, inputs, return, typed failures, underlying ROS nodes/interfaces, configuration, and one minimal fixture.
3. Generate the module index from plugin manifests and checked documentation metadata. Do not hand-maintain a second implementation registry.
4. For each module, document purpose, implementations, hardware/model needs, config schema, ROS graph, frames, fixture command, qualification state, and known failures.
5. Document task package construction with explicit stages and examples for planner selection, fallback, visual servo, gripper, base, object lookup, and recovery-required handling.
6. Document extension work separately: implement contract, declare plugin, add schema, pass shared tests, add minimal doc, and qualify modes.
7. Add troubleshooting keyed by stable error code and health state, pointing to run artifacts and owning module.
8. Document the one-command scan flow, Picker 1 station boundary, explicit start/resume rules, staging quota/cleanup, activation block, Git/LFS inclusion policy, backup status, and ObjectDB-outage behavior.
9. Document the inherited repository pattern explicitly: `.devcontainer/src` is the host ROS workspace, it mounts at `/root/ros2_ws/src`, all Compose files live under `.devcontainer`, infrastructure lives under `scripts`, and task packages are direct workspace children. Document project-specific durable directories and every additional Compose file rather than implying that the repository must contain only the reference repository's files.

## Interfaces and data

- Markdown documentation and generated module index
- Pointers from root README and task templates
- Plugin manifest doc metadata

## Boundaries

- Does not duplicate source/config facts that are cheap to inspect
- Does not claim unsupported qualification
- Does not require an agent to read every phase plan

## Failure behavior

- Documentation build fails on broken links, missing plugin docs, stale generated index, unknown error code, or public API without ROS mapping.
- Examples must compile or run in their declared fixture.

## Acceptance

- A clean reader can locate and run one motion, gripper, perception, and object fixture.
- An operator can distinguish ObjectDB storage health from ROS, scan-worker, staging, lease, and remote-backup health and follow the permitted recovery.
- Every public call maps to ROS and config details.
- Every installed plugin has qualification and limitation data.
- All links and examples validate.
- The documented tree matches a generated structure check: ROS source is under `.devcontainer/src`, Compose files are under `.devcontainer`, Dockerfiles and operational scripts are under `scripts`, and additional project directories have documented ownership.
- Agent assignment instructions point only to required context.

## Parallel work

Develops throughout but freezes after interfaces and qualification states.

## What this module needs from me

Nothing.
