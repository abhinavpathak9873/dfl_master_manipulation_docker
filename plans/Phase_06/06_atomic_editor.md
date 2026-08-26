# Validated object editor

## Goal

Add metadata, asset-reference, profile, and validation edits to the local web GUI while preserving preview, locking, revision creation, and atomic commit.

## Inputs

- Read-only viewer
- Object service/CLI write operations
- Object/grasp schemas
- Single-operator policy

## Outputs

- Edit session UI
- Schema-aware fields and validation
- Preview diff
- Lock status and stale-base handling
- Commit/activate workflow
- Browser/service integration tests

## Work

1. Start an edit session from an exact base revision and acquire a service lock. Keep unsaved browser state separate from canonical staging.
2. Use schema-aware controls for names, tags, frames, units, symmetry, perception metadata, collision asset selection, validation notes, and local-reference metadata.
3. Validate field-level input immediately and run full server validation before preview. The server remains authoritative.
4. Show a semantic diff, new asset hashes, validation changes, and active-base revision before commit.
5. Revision commit creates a new immutable inactive revision. Activation requires a separate confirmation showing old/new revision IDs and lease state; its success response includes the resulting local Git commit and pending remote-sync status.
6. Allow draft editing and commit while a task runs, but disable activation while any task lease is active or stale-unverified. Show the owning run and do not offer task cancellation.
7. On service restart, lock conflict, or stale base, keep local edits exportable but require rebase/review before a new staging session.
8. Never expose a free-form path that escapes the staged object root.

## Interfaces and data

- Viewer edit routes
- Object service lock/stage/validate/diff/commit/activate
- Task/scan lease state and local/remote Git status
- Schema validation errors

## Boundaries

- No simultaneous editors
- No direct JSON save
- No hidden auto-activation

## Failure behavior

- Stale base, lost lock, server validation, asset hash, commit, and activation failures preserve the old active state and show recovery options.
- Remote push failure does not undo a local activation; it shows stale backup health and retry state.
- Browser validation alone never enables commit.

## Acceptance

- Edit/preview/commit/activate creates one valid new revision.
- Cancel creates no approved files.
- Two-session conflict is rejected.
- Service failure during commit leaves active pointer intact.
- Audit artifacts link the run/edit session and diff.
- Active and stale-unverified leases block activation while leaving draft/edit/read behavior available.

## Parallel work

Consumes viewer and service. Grasp editor can build on its session mechanics.

## What this module needs from me

Nothing.
