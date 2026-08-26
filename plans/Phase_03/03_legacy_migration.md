# Approved legacy ObjectDB migration

## Goal

Convert the four approved legacy objects and associated approved revisions into
the file-first format without importing old architecture.

## Task-script payoff

Existing known objects become ordinary assets consumable by the same local loader
and perception/grasp tasks as newly authored objects.

## Work

1. Freeze the read-only legacy database/artifact source and inventory the four
   approved object IDs, revisions, meshes, frames, units, models, references,
   anchors, tool profiles, validation, and provenance.
2. Write one focused converter with explicit field mappings and warnings for
   unknown/lossy data.
3. Normalize units/frames only with recorded source evidence; never guess.
4. Copy assets into new revision staging, validate paths/content/schema, compare
   mesh bounds/transforms/anchor poses, then atomically publish.
5. Preserve legacy IDs/revision provenance or record a deterministic mapping.
6. Archive rejected/superseded legacy history read-only where useful; it need not
   become loadable active data.
7. Generate a human-readable per-object migration report.

## Acceptance

- All approved source records map exactly or identify reviewed deviations.
- Mesh bounds, units, frames, model references, and grasp transforms match
  golden fixtures.
- Running the converter twice is idempotent and never mutates the legacy source.
- Migrated objects load locally and pass the Phase 03 asset checks.

## Non-goals

A permanent compatibility layer, database synchronization, or migration of
unapproved experimental history.
