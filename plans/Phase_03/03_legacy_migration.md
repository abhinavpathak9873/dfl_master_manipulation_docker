# Approved legacy ObjectDB migration

## Goal

Export the four approved objects and their useful approved revisions from the read-only legacy ObjectDB into the new schema with verifiable provenance.

## Inputs

- Read-only legacy SQLite/WAL database and artifact root
- Accepted JSON schema and file store
- Legacy Object Studio behavior notes
- Approved-revision selection rules

## Outputs

- Idempotent migration tool
- Source-to-target field mapping
- Migrated Stanley cup, white box, small tray, and small cardboard box
- Asset/hash and unit verification report
- Read-only archive manifest for non-migrated history
- Migration tests and rollback procedure

## Work

1. Open SQLite with read-only immutable settings and copy no journal state into the source. Record database and artifact-tree hashes before export.
2. Enumerate objects, mesh revisions, annotations, local references, picking profiles, and validation events. Resolve active/approved status from schema-v7 facts rather than row recency.
3. Map mesh units, canonical transform, object IDs, symmetries, FoundationPose metadata, collision data, anchors, gripper profiles, corrections, close-range references, and test history into the new schema.
4. Export every approved revision selected by policy. Keep rejected, draft, superseded, leases, and audit events in a read-only archive manifest rather than reproducing operational tables.
5. For small tray, preserve both approved grasp anchors, 2FG14 width/force/correction/tolerance data, and all approved local-reference evidence with exact units.
6. Run schema and asset validation, compare source and target counts, and produce a per-field reconciliation report. Unmapped populated source fields block acceptance until classified.
7. Make migration idempotent: rerunning against unchanged source produces no new revision and the same hashes.

## Interfaces and data

- Migration CLI with source DB, artifact root, destination, and dry-run arguments
- Migration report and archive manifest
- Canonical file-store API

## Boundaries

- Does not mutate the legacy database
- Does not migrate unapproved records into active state
- Does not infer missing units or frames

## Failure behavior

- Stop on missing artifact, hash mismatch, ambiguous approval, unmapped populated field, inconsistent units, or ID collision.
- Partial target staging remains inactive and can be removed safely.

## Acceptance

- Four objects and all selected approved revisions validate.
- Source/target field reconciliation has no unexplained populated source field.
- All copied assets match recorded hashes.
- A dry run changes nothing.
- A repeated committed run is a no-op.

## Parallel work

Starts after schema, store, and grasp profile fields freeze.

## What this module needs from me

Fact confirmation only if legacy data contains contradictory approval markers; present the exact rows and recommendation.
