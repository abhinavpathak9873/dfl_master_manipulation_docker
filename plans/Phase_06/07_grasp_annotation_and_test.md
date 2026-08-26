# Grasp annotation, preview, and test

## Goal

Let an operator create gripper-specific anchors in the 3D viewer, validate them against geometry and limits, preview immutable plans, and test them through the Phase 05 path.

## Inputs

- Object viewer/editor
- Grasp profile schema
- Robot/tool descriptions
- MoveIt scene and motion API
- Phase 05 alignment, servo, verification, and recovery

## Outputs

- Grasp-anchor 3D editor
- Tool/TCP/approach/retreat preview
- Profile parameter forms for vacuum and 2FG14
- Plan-only preview with exact plan ID
- Explicit simulation/real test action
- Revision-bound test evidence and qualification state

## Work

1. Require selection of object revision and gripper profile before creating an anchor. Display the matching tool geometry and TCP.
2. Place anchor pose in the object canonical frame. Edit approach/retreat vectors, distances, orientation rules, correction offsets, alignment policy, and tool-specific actuation/verification values.
3. Run schema, tool-limit, collision, reachability, pre-grasp, approach, and retreat validation before enabling plan preview.
4. Create an immutable plan through the public motion API and show robot path, collisions, planner, start state, scene version, and plan expiry.
5. Simulation test uses the same explicit stages as Phase 05. Real test is enabled only for commissioned profiles; launching it acquires a task lease through the Phase 02 path and shows the resolved configuration before execution.
6. Record test result, run ID, plan ID, actual endpoints, alignment evidence, gripper evidence, and recovery state against exact anchor/profile/object revisions.
7. Qualification is explicit; one passing test does not promote unrelated revisions.

## Interfaces and data

- Grasp editor over object service
- Motion plan/execute and Phase 05 task action
- Run artifact links stored in object validation evidence

## Boundaries

- No automatic grasp generation
- No direct hardware command from browser JavaScript
- No anchor reuse across gripper profiles
- No test execution while a physical scan lease or stale-unverified lease exists

## Failure behavior

- Wrong tool, uncommissioned real profile, invalid geometry, unreachable/colliding path, stale plan, alignment loss, grip failure, or uncertain state blocks qualification.
- A failed test never changes the active anchor's qualification silently.

## Acceptance

- Vacuum and 2FG14 anchor fixtures render and validate correctly.
- Plan-only preview causes no controller command.
- Stale plan/scene is rejected before execution.
- Simulation result attaches to exact revisions.
- Supervised real test produces complete evidence and safe failure behavior.
- Lease acquisition/release and conflict behavior match ordinary task execution.

## Parallel work

Annotation UI may start after schema/viewer. Test integration waits for Phase 05 acceptance.

## What this module needs from me

Access to a supervised grasp-test window.
