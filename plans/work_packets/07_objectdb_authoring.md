# 07 — ObjectDB companion authoring

## Outcome

ObjectDB helps a developer create and inspect the same local object directories
that runtime tasks load. It can be absent during every task.

## Order

1. Use ordinary files and a small validation command.
2. Add a migration script for the four approved legacy objects.
3. Add grasp-anchor authoring when manual JSON becomes the observed bottleneck.
4. Add scan/reconstruction scripts using normal toolbox robot, camera, and
   perception objects.
5. Add a local viewer/editor only when it materially improves authoring.

## Rules

- The file format is the interface between ObjectDB and runtime.
- A scan script spells out capture poses, camera reads, segmentation, review,
  reconstruction, and save/approve steps.
- Heavy reconstruction may use its own environment because of dependencies.
- New revisions never overwrite approved evidence in place.
- Human review precedes making a new asset the task default.
- Source control and backup use normal project/repository operations; runtime
  loading does not depend on Git state or a sync process.

## Acceptance for the first authoring milestone

- Validate, inspect, copy, and load one object directory from the CLI.
- Migrate one legacy object with units, mesh, models, and grasp anchors intact.
- The resulting directory works with `dfl.objectdb.load` while ObjectDB is not
  running.
- Invalid paths, frames, units, quaternions, and missing assets fail clearly.

## Deferred until observed need

Server APIs, WebSockets, runtime leases, activation transactions, SQLite search
indexes, Git-sync sidecars, multi-user conflict handling, scan state machines,
and a browser GUI.
