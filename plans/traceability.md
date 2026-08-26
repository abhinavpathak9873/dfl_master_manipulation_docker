# Task-visible traceability

The table traces promises in the canonical task to one active packet and one
observable check. It intentionally does not assign ownership to deferred
infrastructure.

| Promise | Owner | Observable check |
|---|---|---|
| Lightweight `Pose` and `Joints` | Packet 01 | Plain-Python value tests |
| Robot selected by model/mode/tool/scene | Packet 01, exercised by 03 | Fake factory test, then Picker 1 smoke task |
| Composite robot exposes actual structure | Packet 03 | Smoke task and adapter inspection |
| Local object load with no server | Packet 02 | Object loader tests with no process/network |
| Models available as object asset paths | Packet 02 | Small-tray fixture |
| Object-frame anchors transform to world poses | Packet 02 | Quaternion/translation fixture |
| Segmenter selected by backend name | Packet 04 | Swap constructor, unchanged task stages |
| Pose estimator receives explicit RGB/depth/mask/object inputs | Packet 04 | Recorded normal and missing-input fixtures |
| Tracker owns its own state | Packet 04 | Initialize/update/reset fixture |
| Local alignment is replaceable and does not move the robot | Packet 05 | Recorded correction fixture and zero command assertion |
| Arm motion helpers read like manipulation | Packets 03 and 05 | Reference task source and Gazebo endpoint checks |
| Force-aware descend is honest per backend | Packets 05 and 06 | Supported contact test or clear unsupported error |
| Gripper close returns useful evidence | Packets 03 and 05 | Empty/success fixture |
| Retry remains ordinary task control flow | Packet 05 | Injected failed-close task fixture |
| ROS remains directly debuggable | Packets 03, 04, and 06 | Named ROS graph/topics/actions in adapter docs |
| Gazebo-to-real reuse is limited to honest shared behavior | Packet 06 | Same task with mode change plus explicit unsupported cases |
| AI agent can find a task call, backend file, and focused test | Repository guidance | Navigation review against one new backend |

When a new public promise appears in the task, add one row only if its owner or
observable check is not obvious from code.
