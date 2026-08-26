# Deferred work

These items are plausible, not active architecture.

| Item | Promote when | First implementation shape |
|---|---|---|
| Genesis | A named experiment needs Genesis rather than Gazebo. | One adapter for that task; compare shared operations after it works. |
| H2515 | A task and hardware/simulator window are named. | Direct H2515 adapter plus one task fixture. |
| Picker 2 and concurrent robots | One task truly controls both. | Two explicit `Robot` objects; add shared-resource logic only where collision occurs. |
| VGC10 four-cup, VGP20, 2FG14 | A mounted or simulated task needs each tool. | One tool file and one mapping entry per profile. |
| OMPL fallback and CIRC | A task cannot be expressed reliably with the first motion path. | Explicit task argument; no global fallback policy. |
| Visual servo framework | Two alignment/control methods share proven behavior. | Extract a helper from the working task loop. |
| Base motion | A manipulation task needs base repositioning. | Bounded velocity and stop in the robot's `base` adapter. |
| Custom ROS IDL | A concrete cross-process payload is unclear with standard messages. | Add the smallest message/action for that exchange. |
| Full run recorder | Repeated failures need more than ordinary logs and saved debug images. | Optional recorder used by the affected task. |
| ObjectDB viewer/editor/scanner | Runtime file format and authoring workflow are proven manually. | Companion local tool that reads/writes the same files. |
| Dataset benchmarks | A backend needs measured comparison or regression protection. | Backend-owned recorded fixture and relevant metrics. |
| Gateway processes | Real hardware placement requires drivers away from the task host. | ROS-visible driver/watchdog process for that device only. |
| Broad simulator/robot/tool matrices | Multiple supported combinations exist. | Test only declared supported combinations. |
| Release/upgrade machinery | The toolbox is being distributed as a versioned internal release. | Pin adopted dependencies and run affected fixtures. |

Absence from the active roadmap is intentional. None of these items may become
a prerequisite for the first Picker 1 tray task.
