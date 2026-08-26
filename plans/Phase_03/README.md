# Phase 03 — object records, grasps, and planning scene

## Goal

Replace the legacy SQLite-first ObjectDB with an always-on, file-first service while preserving approved meshes, grasp data, local references, and provenance. Give it the only canonical write mount, independent Git history, runtime leases, and one synchronized MoveIt scene representation.

## Settled decisions

- Files are canonical; indexes are rebuildable caches.
- Each approved mesh has a same-base-name JSON record.
- Migrate the four approved legacy objects and approved revisions.
- Archive other legacy history read-only.
- Grasp anchors are bound to gripper profiles.
- GUI and scripts write through one typed service/CLI.
- ObjectDB is an isolated, always-on, loopback-only container and the sole canonical writer.
- Approved bundles live in the nested private `dfl_object_db` Git repository; local activation commits are required and remote push is asynchronous.
- Tasks resolve exact revisions and acquire leases before startup. Active or stale-unverified task leases block activation.
- MoveIt owns the runtime collision scene.

## Work packets

| Packet | Result |
|---|---|
| [01](01_object_json_schema.md) | Versioned object/revision schema. |
| [02](02_file_store_and_index.md) | Immutable approved revisions, local Git history, and rebuildable cache. |
| [03](03_legacy_migration.md) | Verified export of the four approved objects. |
| [04](04_grasp_profiles.md) | Gripper-bound anchors and selection rules. |
| [05](05_object_service_and_cli.md) | Always-on ObjectDB runtime, leases, and atomic read/write operations. |
| [06](06_scene_and_moveit_sync.md) | Static scene plus tracked-object synchronization. |
| [07](07_object_contract_tests.md) | Schema, store, migration, and scene acceptance. |

## Order and parallel work

Define the schema first. Store/index/Git and grasp-profile work consume it and may proceed together. Migration begins after both are stable. Service/CLI consumes the store and implements the Phase 01 lease contract. Scene synchronization consumes schema plus service reads and may start with fixtures. Contract tests run throughout and publish the phase exit last.

## Upstream inputs

- Phase 01 types, IDL, config, namespace, and run records
- Legacy ObjectDB read-only source
- Phase 02 gripper and motion contracts

## Exit criteria

- All four approved objects validate from files with verified meshes and provenance.
- Approved revisions are immutable and active selection is atomic.
- Activation creates a durable local Git commit and is refused while a task lease is active or stale-unverified.
- Deleting the cache and rebuilding it preserves query results.
- Grasp selection rejects incompatible gripper profiles.
- GUI/CLI operations cannot bypass schema, locking, or revision creation.
- Static and dynamic collision objects synchronize to MoveIt with explicit freshness.
- Consumers resolve exact revisions through ObjectDB and can only read the canonical mount.

## What this phase needs from me

Facts: legacy backup location and read access, plus the approved active revision for each object. No schema preference remains.
