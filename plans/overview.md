# Toolbox roadmap

## Planning rule

Every work packet starts and ends with a representative task script. Interfaces
may evolve while the vertical slice is being learned; later work must not wait
for a speculative global contract to freeze.

An implementation packet receives:

1. [the accepted direction](../toolbox_plan.md);
2. the relevant work packet;
3. only the existing backend, task, object, or hardware evidence named by that
   packet.

## Active order

| Phase | Order | Packet | Task-visible result |
|---|---:|---|---|
| 00 — plain-Python foundation | 1 | [Foundation](work_packets/01_foundation.md) | `Pose`, `Joints`, `Robot`, and named capability objects import without ROS. |
| 00 — plain-Python foundation | 2 | [Object assets](work_packets/02_object_assets.md) | `objectdb.load("small_tray")` returns local models and transformable grasp anchors. |
| 01 — Gazebo tray slice | 3 | [Picker 1 Gazebo](work_packets/03_picker1_gazebo.md) | One ordinary Python task brings up Picker 1, sees RGB-D, moves, and actuates one gripper. |
| 01 — Gazebo tray slice | 4 | [Perception slice](work_packets/04_perception_slice.md) | That task segments and estimates the tray pose through replaceable named backends. |
| 01 — Gazebo tray slice | 5 | [Reference grasp task](work_packets/05_reference_grasp_task.md) | The full visible approach, alignment, descend, grip, retry, lift, and place task works in Gazebo. |
| 02 — real Picker 1 | 6 | [Picker 1 real](work_packets/06_picker1_real.md) | Changing `mode` selects the real adapter for the shared supported operations. |

[ObjectDB authoring](work_packets/07_objectdb_authoring.md) is an independent
Phase 03 companion track. It may proceed after the file format is exercised by
a task, and it never blocks runtime object loading.

## Current state

Packets 01 and the runtime half of 02 have an initial implementation in this
repository. They are intentionally small and dependency-free. Their interfaces
are provisional until Packet 03 exercises them against a real ROS adapter.

## Completion rule

A packet is complete when:

- its named task or fixture runs;
- the task reads like robotics from top to bottom;
- the debugging path reaches the concrete backend directly;
- errors name the failed assumption and relevant backend;
- no new mandatory process, manifest, registry, or configuration layer was
  introduced without a concrete need in that task.

## Scope promotion

Deferred work is listed in [`backlog.md`](backlog.md). Promote an item only
with a named experiment and the smallest supported robot/tool/mode/object
combination that proves it. The promoted packet must say which lines of the task
script become easier.
