# Workspace imports and source provenance

## Goal

Create the normal ROS 2 source workspace required by the master plan while keeping vendor code pinned and project-owned migrations traceable. Avoid stale embedded copies and unexplained local forks.

## Inputs

- Source inventory
- Doosan Jazzy pin
- Existing DFL workspace package list
- Container build contract

## Outputs

- `dependencies.repos` or equivalent exact VCS manifest
- Project-owned `src/` layout with provenance notes
- Import script that refuses dirty or mismatched vendor sources
- Migration ledger for each copied DFL package
- License inventory and third-party notices
- Colcon package graph report
- Nested ObjectDB data-repository bootstrap contract

## Work

1. Classify every source as upstream dependency, project-owned package to migrate, reference-only repository, data migration input, or rejected duplicate.
2. Import `doosan-robot2` from the official Jazzy commit through the VCS manifest. Keep its checkout unmodified; place configuration overlays and adapters in DFL packages.
3. Migrate `moveit2_calibration`, picker descriptions/bringup/configs, the Zinger base driver, and `ros2_pick_and_place` only after recording source path, commit or content hash, license, and reason.
4. Create `dfl_manipulation_interfaces`, `dfl_manipulation_toolbox`, the three integration-package locations, the `object_db` application package, `src/tasks`, and scene directories without implementing later-phase behavior.
5. Reserve `data/object_db/` for the independent private `dfl_object_db` checkout and exclude it from the parent source repository. Store its remote URL and expected access mode without credentials; release and run manifests record the exact data commit.
6. Run rosdep and colcon graph inspection. Record duplicate package names, missing Jazzy releases, hard-coded Humble paths, Python version assumptions, and dependency cycles.
7. Define the vendor-patch policy: prefer overlays; if an upstream patch is unavoidable, store a minimal patch file with issue link, tested commit, and removal condition.
8. Generate a machine-readable source manifest included in every release run record.

## Interfaces and data

- VCS import manifest
- Source provenance schema: name, role, origin, revision, license, local path, dirty state
- Workspace package names consumed by colcon and launch
- ObjectDB data remote plus commit identity consumed by setup and release tools

## Boundaries

- Does not port source behavior to Jazzy
- Does not modify reference repositories
- Does not copy ObjectDB records; Phase 03 owns data migration

## Failure behavior

- Stop on dirty vendor checkouts, missing licenses, duplicate package names, or a source whose authority cannot be established.
- Do not choose between conflicting project-owned copies by path name; compare history and behavior evidence.

## Acceptance

- A fresh directory can reproduce the same `src/` dependency revisions.
- `vcs status` and the source manifest agree.
- Colcon discovers each intended package once.
- Reference-only repositories do not appear in runtime dependencies.
- Every migrated package has provenance and an explicit Phase owner for its port.
- A fresh setup can clone `data/object_db/` independently without nesting its history in the parent repository.

## Parallel work

Container work may proceed from the same pins. Doosan migration starts after this manifest is accepted.

## What this module needs from me

Nothing.
