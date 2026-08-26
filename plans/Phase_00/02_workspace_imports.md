# Workspace imports and source provenance

## Goal

Make every adopted ROS/vendor dependency reproducible and easy to trace while
keeping external source management simple.

## Task-script payoff

A developer gets the same robot and backend behavior after a clean rebuild and
can quickly find the exact upstream source when debugging.

## Retained scope

- Pinned Doosan Jazzy sources and the existing DFL ROS packages actually needed.
- Repositories required by Gazebo, Genesis, MoveIt, grippers, D455, perception,
  tracking, ObjectDB authoring, and scanning.
- License, patch, branch/commit, build-order, and local-overlay documentation.

## Work

1. Inventory each existing package and classify it as reuse, migrate, replace,
   reference-only, or archive.
2. Put reproducible source pins in the normal ROS workspace import mechanism
   used by `.devcontainer/src/`.
3. Record the upstream URL, immutable revision, license, owning Docker image,
   reason for adoption, and any local patch.
4. Keep patches small and source-adjacent; prefer upstream ROS/vendor APIs over a
   duplicate wrapper.
5. Remove unused repositories from builds rather than carrying speculative
   integrations.
6. Add one command that reports resolved revisions and detects dirty or missing
   required sources.
7. Route dependency changes through Phase 07's focused upgrade packet.

## Outputs

- Workspace import files and source-provenance table.
- Reuse/migration disposition for current DFL packages.
- Local patch inventory and clean-build order.
- Dependency inspection command.

## Acceptance

- A clean import resolves immutable revisions.
- Every built external package has an owner, purpose, license note, and Docker
  image.
- No task-facing API depends on an unexplained fork or host-only source.
- Removing an unused dependency does not require editing an orchestration
  registry.

## Non-goals

- A source-management service, package catalogue, or automatic updater.
- Importing future robotics stacks before a packet actually uses them.
