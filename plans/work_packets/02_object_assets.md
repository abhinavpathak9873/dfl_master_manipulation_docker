# 02 — file-first object assets

## Outcome

`dfl.objectdb.load("small_tray")` reads a local object directory and returns
paths, metadata, models, and object-frame grasp anchors. It performs no network
request and starts no process.

## Initial file format

```text
objects/small_tray/
  object.json
  mesh.glb
  models/
    segmentation.engine
```

`object.json` has a small stable core:

- `id`;
- optional `mesh`;
- optional `models` mapping;
- optional `reference_frames` and `dimensions`;
- optional `grasp_anchors`, each containing an ID and `Pose` fields;
- optional free metadata under `annotations`.

Fields are added only for a consuming task or authoring tool. Relative asset
paths must stay inside the object directory.

## Work

- Resolve an explicit root, then `DFL_OBJECTS_ROOT`, then `./objects`.
- Accept one object ID or a list of IDs for the common multi-object setup case.
- Load JSON with clear missing-object, invalid-record, and missing-asset errors.
- Return path objects rather than opening meshes/models eagerly.
- Support attribute and key access for named model assets.
- Transform all anchors by an estimated object pose locally.
- Add a small validation function usable by future authoring scripts.
- Write a legacy migration only after approved source data is available.

## Acceptance

- A temporary small-tray fixture loads with no optional service.
- Path traversal and missing referenced assets fail.
- Anchor transforms preserve the world frame and expected translation/rotation.
- Unknown optional metadata remains available without controlling the pipeline.

## Non-goals

SQLite, an always-on server, runtime leases, revision activation, Git commits,
Git LFS policy, sync sidecars, planning-scene ownership, and a GUI.
