# Canonical object JSON schema

## Goal

Define the smallest readable object record that supports the known asset,
perception, grasping, scanning, and provenance needs.

## Task-script payoff

A loaded object exposes obvious attributes such as `mesh`, `dimensions`,
`reference_frames`, `models.segmentation`, `models.pose`, `grasp_anchors`, and
`annotations` without database/service calls.

## Required data

- Stable object ID, display name, schema version, units, and canonical
  object-frame definition.
- Mesh and optional collision geometry with paths relative to the object record.
- Dimensions/bounds and optional mass/material facts actually used.
- Optional model references and backend metadata for segmentation, pose, and
  tracking.
- Object-frame grasp anchors, optional tool-specific parameters, corrections,
  local references, and annotations.
- Provenance, validation status, and useful test/revision information.

## Work

1. Start from the four approved legacy objects and concrete Phase 04/05/06
   consumers; mark most fields optional.
2. Define relative-path, unit, frame, quaternion, naming, and extension-field
   rules.
3. Keep large assets as files; the JSON stores readable references and optional
   hashes.
4. Decide whether grasps are embedded or in a nearby `grasps.json` based on
   actual size/edit workflow; the loader presents the same object attribute.
5. Provide direct validation errors for missing mesh/model/reference, bad path,
   unknown frame, invalid transform, and unsupported schema version.
6. Permit unknown extension keys so experiments can add metadata without a
   central schema redesign.

## Acceptance

- All four approved objects and one minimal hand-authored object validate.
- A human can understand/edit the record with normal tools.
- Asset paths cannot escape the configured object root unintentionally.
- Missing optional assets do not break unrelated capabilities; a backend that
  needs one raises a specific error.

## Non-goals

A universal digital-twin ontology, database schema, or field for every possible
future algorithm.
