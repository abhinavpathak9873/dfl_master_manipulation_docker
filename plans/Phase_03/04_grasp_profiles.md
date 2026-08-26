# Gripper-specific grasp profiles

## Goal

Represent and select grasp anchors whose geometry, TCP, actuation, approach, and verification match the active gripper profile.

## Inputs

- Object schema
- Shared gripper capabilities
- Tool geometry/TCP profiles
- Legacy anchors and picking profiles
- Motion and local-alignment requirements

## Outputs

- Grasp-profile schema fields and Python value
- Selection/filter API
- Compatibility and orientation rules
- Correction and verification settings
- Validation fixtures for vacuum and parallel tools

## Work

1. Bind every grasp anchor to one gripper profile ID and tool-profile revision. Reusing an anchor for another tool requires a new validated profile.
2. Store anchor pose in the object canonical frame and specify the TCP it targets. Record approach/retreat unit vectors, distances, allowed orientation or symmetry rules, and collision clearance.
3. For vacuum tools, store cup/channel geometry requirements, target vacuum, seal/contact constraints, and held-object verification method.
4. For 2FG14, store grip direction, width, force, speed, internal/external mode, expected returned width, tolerance, and require-object behavior.
5. Store coarse correction, local-reference selection, visual-servo policy, and final press/descent bounds separately from the anchor pose.
6. Select by object revision, active gripper profile, task orientation constraints, qualification state, and optional anchor ID. Return all rejection reasons when no candidate remains.
7. Record grasp-test evidence by anchor/profile/revision; never promote a test result to another object or tool revision.

## Interfaces and data

- Typed `GraspAnchor` and grasp profile
- Object JSON fields
- `select_grasps(object_ref, gripper_id, constraints)` API
- Inputs consumed by Phase 05

## Boundaries

- Does not execute motion or gripper commands
- Does not synthesize grasps in v1
- Does not hide fallback anchor choice

## Failure behavior

- Reject tool/TCP mismatch, unqualified profile, invalid direction, out-of-range width/force/vacuum, missing local reference, or stale object revision.
- No-candidate result lists deterministic rejection causes.

## Acceptance

- Small-tray 2FG14 profile preserves known values and references.
- Vacuum fixtures distinguish one-cup, four-cup, and VGP20 anchors.
- Selection is deterministic for identical inputs.
- Wrong-tool and wrong-revision tests fail before planning.
- Test evidence is revision-bound.

## Parallel work

Can develop with store layout after schema fields settle. Migration consumes it.

## What this module needs from me

Nothing.
