# File store, approved revisions, and rebuildable index

## Goal

Store object assets as normal files with simple revision history and optional
fast lookup without making a database or Git transaction part of task runtime.

## Task-script payoff

A task resolves an object ID or explicit revision to a stable directory and can
inspect/copy/version it with ordinary filesystem tools.

## Layout

```text
objects/
  small_tray/
    active.json
    revisions/
      <revision_id>/
        object.json
        mesh.glb
        grasps.json
        models/
        references/
```

A flat single-revision object directory is also valid for experiments. The
loader hides this small storage distinction, not the object contents.

## Work

1. Define stable object/revision IDs, safe relative paths, atomic temp-then-rename
   writes, and an explicit active-revision pointer where revision history is used.
2. Keep approved revision directories immutable; create a new revision for an
   authored change.
3. Add an optional rebuildable index only after corpus size makes directory
   scanning inconvenient. Deleting it must lose no canonical data.
4. Validate asset existence and optional hashes at authoring/qualification; let
   callers choose fast versus full validation for runtime experiments.
5. Define local copy/export/import behavior with collision and schema checks.
6. Allow ObjectDB authoring to make Git/Git LFS commits or remote backups, but
   keep that policy outside `objectdb.load`.
7. Document crash behavior for atomic writes and active-pointer changes.

## Acceptance

- Objects load by ID and explicit revision using only local files.
- Interrupted authoring never exposes a half-written approved revision.
- An optional index can be deleted and rebuilt exactly.
- Git, network, SQLite, ObjectDB UI, and sync processes may all be absent during
  task loading.

## Non-goals

A content-addressed storage service, distributed transaction coordinator,
activation journal, or mandatory database.
