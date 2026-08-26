# Canonical object JSON schema

## Goal

Define the human-readable, versioned record stored beside each mesh revision. Preserve the identity, geometry, perception, grasp, local-reference, collision, provenance, and validation data needed by later phases.

## Inputs

- Legacy ObjectDB schema and approved records
- ObjectRevisionRef and GraspAnchor ROS types
- Gripper capabilities
- FoundationPose/SAM2/M3T metadata requirements

## Outputs

- JSON Schema for object revision records
- Canonical examples for all four legacy objects
- Stable object and revision ID rules
- Frame, unit, symmetry, asset-reference, and validation semantics
- Schema migration policy

## Work

1. Use an immutable stable `object_id` slug independent of display name. Use a revision ID derived from approved content or an immutable generated ID recorded with content hashes.
2. Require `schema_version`, `object_id`, `name`, `revision_id`, lifecycle status, canonical frame, units, mesh record, provenance, and validation state.
3. Define mesh fields for relative path, format, SHA-256, source units, normalized scale, vertex/face facts, canonical transform, and symmetry metadata.
4. Define perception metadata for supported backend assets, FoundationPose readiness, segmentation prompts/references, expected object dimensions, and known limitations.
5. Define grasp anchors in the canonical object frame with stable anchor ID, gripper profile ID, TCP pose, approach and retreat vectors/distances, allowed orientation rules, correction offsets, and validation evidence.
6. Define local-reference assets with relative content-addressed paths, camera/calibration identity, viewpoint, mask/depth descriptors, and quality metadata.
7. Define collision geometry separately from the perception mesh and record whether it is generated, simplified, or manually approved.
8. Use relative paths only. Preserve unknown future extension data under a namespaced extension object; unknown top-level fields fail validation.

## Interfaces and data

- Same-base-name `<mesh>.json` file
- JSON Schema version
- Conversion to Python ObjectRevisionRef/GraspAnchor and ROS messages

## Boundaries

- Does not store mutable runtime track state
- Does not embed binary meshes or images in JSON
- Does not use a database row ID as public identity

## Failure behavior

- Reject missing units/frame, invalid hash, absolute or escaping path, duplicate anchor ID, unknown gripper, invalid quaternion, unsafe approach vector, or approval without evidence.
- Schema migration never mutates an approved revision in place.

## Acceptance

- All four migrated examples validate.
- JSON round-trip preserves values and ordering-independent hashes.
- Every asset reference resolves inside the object revision directory or approved shared asset root.
- Grasp and perception consumers need no undocumented field.
- A breaking schema example produces a clear version error.

## Parallel work

Store and grasp-profile work follow the first accepted schema version.

## What this module needs from me

Nothing.
