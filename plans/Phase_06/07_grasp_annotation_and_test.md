# Grasp annotation, preview, and test

## Goal

Create object-frame grasp anchors for the four supported tool profiles, preview
their geometry, and test them through the same manipulation primitives used by
tasks.

## Task-script payoff

An authored anchor appears as `object.grasp_anchors` and can be transformed,
selected, approached, aligned, gripped, verified, and retried in ordinary task
code.

## Work

1. Add, duplicate, transform, label, enable/disable, and delete anchors in the
   object's canonical frame.
2. Select compatible tool profiles and edit approach/retreat, cup selection,
   expected width/force/vacuum, correction offsets, servo/alignment hints, and
   verification values only where relevant.
3. Preview object mesh, collision geometry, tool TCP/cups/fingers, approach path,
   clearances, and transformed world pose.
4. Validate frames, quaternion, tool compatibility, geometry bounds, approach
   direction, collision, and required tool-specific fields.
5. Save annotations only as a new object revision using the Phase 03 format.
6. Provide simulation test first, then an explicit supervised real test with
   selected robot/tool/scene, conservative limits, fresh preflight, and operator
   start.
7. Run the visible Phase 05 primitives; do not call a hidden pick workflow.
8. Record test result/limitations with the anchor and keep raw robot/backend
   diagnostics accessible.

## Acceptance

- Previewed transforms match task-side transforms numerically and visually.
- All four tool profile geometries render correctly.
- Failed/aborted tests do not mark an anchor successful or auto-retry.
- Approved anchors load locally with ObjectDB stopped.
- Real test motion cannot start from a stale/restarted authoring session.

## Non-goals

Automatic grasp generation as a replacement for annotation, remote robot control,
or a grasp-testing state-machine platform.
