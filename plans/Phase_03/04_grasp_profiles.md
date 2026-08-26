# Gripper-specific grasp profiles

## Goal

Keep reusable grasp anchors with the object while representing only genuine
tool-specific geometry, commands, and verification needs.

## Task-script payoff

`grasps = tray.grasp_anchors.transform(object_pose)` returns world/robot-frame
candidates; a task filters or selects one for VGC10, VGP20, or 2FG14 without a
service call.

## Work

1. Define an anchor as an object-frame pose plus stable ID and optional approach,
   retreat, clearance, score/label, and provenance.
2. Permit optional compatible-tool/profile IDs and tool-specific values such as
   active cups, expected width/tolerance, force, vacuum threshold, offsets, and
   verification hints.
3. Keep universal fields small; store experimental algorithm data in an extension
   or backend-specific annotation.
4. Implement local transformation by an estimated object pose with explicit
   frames, units, quaternion order, and immutable source anchors.
5. Validate tool compatibility, TCP reference, mesh relation, bounds, and
   obviously unreachable/malformed transforms before motion.
6. Support multiple anchor sets/revisions and algorithmic grasp generation
   alongside fixed anchors.
7. Provide RViz/viewer preview fixtures for all four tool profiles.

## Acceptance

- Known anchors transform to expected world poses within tolerance.
- Selecting a different object pose never mutates stored anchors.
- Tool-specific checks are available without putting object policy in drivers.
- Missing anchors produce a clear empty/no-anchor result; missing required tool
  data names the field and object.
- Fixed and generated grasp candidates can coexist.

## Non-goals

A grasp service, mandatory scoring ontology, or forcing every tool to use the
same metadata.
