# Phase 03 — file-first object assets, grasps, and planning scene

## Goal

Make ObjectDB output easy to load and manipulate locally while retaining legacy
migration, revisions, grasp profiles, and MoveIt scene use.

## Task-script payoff

`tray = dfl.objectdb.load("small_tray")` returns mesh, models, frames, metadata,
and grasp anchors from ordinary files; the task transforms and uses them without
an ObjectDB process.

## Packets

1. [Canonical object JSON](01_object_json_schema.md)
2. [File store, revisions, and optional index](02_file_store_and_index.md)
3. [Approved legacy migration](03_legacy_migration.md)
4. [Gripper-specific grasp profiles](04_grasp_profiles.md)
5. [Local loader and authoring CLI](05_object_service_and_cli.md)
6. [Scene folders and MoveIt synchronization](06_scene_and_moveit_sync.md)
7. [Object and scene acceptance](07_object_contract_tests.md)

## Smallest sufficient design

- Normal inspectable directories and human-readable records are canonical.
- Keep the schema small and extensible from actual perception/grasp consumers.
- Use immutable approved revisions and a rebuildable index only where they help
  authoring/history.
- Load assets and transform anchors locally.
- Use validation and atomic file writes for authoring; no runtime server, lease,
  or Git transaction is required by tasks.
- Motion explicitly owns planning-scene updates.

## Exit evidence

The four approved legacy objects migrate, validate, load with ObjectDB stopped,
resolve their assets/models/grasps, transform anchors correctly, and add/update
collision geometry through the motion-side scene helper.

## Non-goals

An always-on ObjectDB runtime, sole-writer control plane, distributed lease
system, database-first design, or live scene authority.
