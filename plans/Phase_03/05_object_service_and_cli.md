# Local object loader and authoring CLI

## Goal

Provide the simple runtime loader used by tasks and focused local commands that
help humans/ObjectDB author and validate the same files.

## Task-script payoff

`dfl.objectdb.load("small_tray")` and `load(["small_tray", "white_box"])` work
with local files and no server, network, lease, database, or Git operation.

## Runtime API

- `load(id_or_path, revision=None, validate="fast") -> ObjectAsset`.
- Object attributes for metadata, mesh/collision paths, dimensions, frames,
  models, references, annotations, and grasp anchors.
- Explicit path/root selection for experiments and direct file locations.
- Clear missing-object, ambiguous-ID, invalid-schema, missing-required-asset, and
  unsafe-path errors.

## Authoring commands

Keep commands narrow: `list`, `show`, `validate`, `create`, `new-revision`,
`set-active`, `import`, and `export` as the file workflow proves useful. The
ObjectDB application may call the same library functions.

## Work

1. Implement loading as normal Python file parsing/path resolution with lazy
   heavyweight asset access.
2. Resolve IDs within configured local roots deterministically and show the
   chosen path/revision.
3. Keep list loading as a tiny loop/convenience with per-object error context.
4. Separate fast structural validation from explicit full asset/hash/backend
   validation.
5. Use atomic writes and new revisions for authoring changes; runtime assets are
   ordinary read-only Python values.
6. Make CLI output both human-readable and optionally JSON for scripts/agents.
7. Keep the underlying files usable without the CLI or UI.

## Acceptance

- Runtime loading works in the core container with all ObjectDB/scan services
  stopped and network unavailable.
- Four migrated objects and an explicit experimental path resolve correctly.
- Unknown/missing models fail only when the selected backend needs them.
- Authoring commands never expose a partial approved revision.
- No HTTP/ROS object service or sole-writer daemon is required.

## Non-goals

Runtime leases, object-resolution services, automatic Git push, or planning-scene
ownership.
