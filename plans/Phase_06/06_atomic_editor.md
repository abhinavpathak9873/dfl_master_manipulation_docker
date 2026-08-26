# Validated object editor

## Goal

Allow a single local operator to edit supported object fields safely and create a
new revision without a multi-user transaction architecture.

## Task-script payoff

Corrections to frames, metadata, collision assets, references, and model links
become normal validated object files that task scripts consume immediately.

## Work

1. Define the exact editable fields from Phase 03 and keep unsupported extension
   fields round-trippable.
2. Use a draft copy with preview; never mutate an approved revision in place.
3. Validate IDs, units, frames/transforms, dimensions, relative paths, assets,
   model/reference metadata, and grasp references before save.
4. Show a concise field/asset diff and validation warnings before explicit
   commit.
5. Atomically write a new revision, reload it through the runtime loader, and
   update active selection only when requested.
6. Detect if the source active revision changed during an edit and require the
   operator to refresh or intentionally branch from the selected revision.
7. Keep optional Git commit/backup outside core edit success.
8. Provide the same core edit/validate operations through a local CLI/library for
   automation and debugging.

## Acceptance

- Invalid edits never mutate approved files.
- Unknown extension data survives an unrelated edit.
- Two browser actions cannot silently overwrite a newer source revision.
- A successful edit produces one complete, locally loadable revision.
- Closing/restarting the UI preserves or clearly discards the local draft.

## Non-goals

Collaborative editing, role permissions, distributed locks, approval workflows,
or database transactions.
