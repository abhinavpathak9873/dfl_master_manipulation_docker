# Local source inventory

These repositories are evidence for the active packets. Their structure is not
an architecture requirement.

| Source | Inspected state on 2026-08-27 | Useful evidence |
|---|---|---|
| `/home/abhinavpathak/Documents/dff_mobile_manipulation_docker` | `main` at `b5a206e454516aeb33e257a9cc5918ce5520d82d`, clean | Existing `Robot`, `Pose`, `Joints`, Pilz/Cartesian checks, launch ownership, visual servo, VGC10/2FG14 behavior, and task fixtures |
| `/home/abhinavpathak/Documents/dff_labs_docker` | directory exists; not a Git root at the recorded path | Jazzy/container and simulator installation evidence |
| `/home/abhinavpathak/Documents/dff_intelligence_docker` | directory exists; not a Git root at the recorded path | Object Studio/ObjectDB, FoundationPose, local alignment, scanning, and GUI behavior |
| `/home/abhinavpathak/Documents/DFL_Manipulation_Workspace/ros2_picker1_and picker2_src` | directory exists; not a Git root at the recorded path | Picker descriptions, MoveIt/controller configuration, tools, camera/base integration |

## Reuse rule

Port the smallest behavior needed by the active task and preserve its safety
fixtures. Do not copy the reference facade, configuration hierarchy, process
registry, database topology, or package layout merely because it already
exists.

Before a packet uses a source, record its current Git state or content hash and
inspect local changes. Never discard changes in a reference checkout.
