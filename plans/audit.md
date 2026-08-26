# Architecture audit of the superseded plan

Date: 2026-08-27

This audit compares every former plan and work packet with the toolbox-first
direction. Git history retains the old text; deleted packets are not hidden
requirements.

## Tests used

- **Task-script test:** what new concept appears in the representative task?
- **Five-minute test:** what must a developer understand before trying an idea?
- **Debugging test:** how many layers sit between a task call and its backend?
- **Deletion test:** if the abstraction disappears, where does necessary
  complexity reappear?
- **Two-implementation test:** are there two real adapters, or only a predicted
  seam?

Safety logic at the ROS, controller, vendor, and physical-hardware seams is not
treated as bloat. Infrastructure is retained only when a concrete dependency or
hardware placement requires it.

## Main findings

1. The old roadmap was horizontal and infrastructure-first. It required eight
   phases and dozens of frozen contracts before a complete developer task.
2. ObjectDB had become a runtime control plane: always-on server, leases, sole
   writer, Git transactions, sync sidecar, health graph, and activation gates.
   Runtime tasks only need local immutable files.
3. Backend interchangeability had become a plugin platform with entry points,
   pluginlib manifests, schemas, qualification states, and generated catalogues.
   Source-controlled Python mappings are enough for the current team.
4. Ordinary experiments were forced into ROS application packages with
   lifecycle, run-manifest, and cleanup ceremony.
5. Configuration and result/error designs tried to standardize future robots and
   algorithms before the first vertical slice proved their common shape.
6. The initial release matrix—three robots, four tools, two simulators, multiple
   services, scanning, GUI, gateways, and release operations—optimized coverage
   rather than iteration speed.

## Pseudocode resolution

The revised interface keeps the supplied sketch's shape:

- `dfl.Robot(...)`, composite `robot.arm/gripper/camera/base`, and ordinary
  task control flow;
- folder-local constructors such as
  `dfl.perception.segmentation.create(backend="tensorrt.py", ...)`;
- one easy-to-open implementation file per backend and one direct mapping
  entry;
- positional `Joints(...)` and `Pose(x, y, z, q=..., frame=...)` as well as
  explicit sequence forms;
- local object loading and locally transformed grasp anchors;
- force-aware motion and useful gripper results where the selected hardware
  truly supports them.

The common examples use named robotics inputs instead of one opaque
`input=[...]` array, because `rgb=`, `depth=`, `mask=`, and `object=`
remain readable when backend needs differ. A backend can still accept a list or
expose a specialized call through its concrete implementation. Backends are
constructed once rather than rerunning model initialization on every function
call.

## Core and research documents

| Former document | Verdict | Revised treatment |
|---|---|---|
| `toolbox_plan.md` | Rewrite | Toolbox-first baseline; task script is the controlling interface. |
| `plans/overview.md` | Rewrite | Six task-ordered packets plus one independent ObjectDB authoring track. |
| `plans/traceability.md` | Rewrite | Trace task-visible promises to a small owner and executable check. |
| `decisions/000_global_architecture.md` | Rewrite | Remove deployment-first and service-first decisions; retain useful ROS visibility and safety facts. |
| `research/00_source_inventory.md` | Condense | Keep local sources as evidence and record current drift without copying their architecture. |
| `research/01_dependency_audit.md` | Replace | Keep dependency facts next to the packet that adopts the dependency; reverify changing facts then. |
| `research/02_isaac_ros_jazzy_reuse.md` | Merge | Relevant SAM2/FoundationPose reuse guidance moves to the perception packet. |
| `research/03_capx_agent_interface_audit.md` | Merge | Small examples, focused fixtures, and direct navigation become repository guidance; generated capability registries are dropped. |
| `example_api.txt` | Rewrite and promote | Correct, executable-shaped canonical task referenced by plans, README, and agent guidance. |

## Former Phase 00 — foundation and simulation

| Former packet | Verdict | Reason / destination |
|---|---|---|
| Phase README | Delete | Phase-wide infrastructure gate delayed all useful task work. |
| 01 container and Compose | Defer and narrow | Add only the container needed by the Picker 1 Gazebo or perception adapter; no predeclared service fleet. |
| 02 workspace imports | Merge | Pin and import a dependency inside the concrete backend packet that uses it. |
| 03 Doosan Jazzy migration | Keep, reorder | Becomes part of [Picker 1 Gazebo](work_packets/03_picker1_gazebo.md) and later real mode. |
| 04 robot/tool/scene profiles | Reduce | Keep small adapter-owned records for actual hardware facts; remove universal schemas and matrices. |
| 05 Gazebo emulator | Keep, narrow | Prove Picker 1 plus one gripper and camera before other combinations. |
| 06 Genesis bridge spike | Defer | No named task currently needs Genesis. |
| 07 simulator contract | Delete as advance design | Extract shared behavior only after Gazebo and a second simulator both exist. |
| 08 fixed task matrix | Replace | One representative task is the initial acceptance test; expand only to supported combinations. |

## Former Phase 01 — shared contracts

| Former packet | Verdict | Reason / destination |
|---|---|---|
| Phase README | Delete | Global contract freeze predicted interfaces before integrations existed. |
| 01 Python value types | Keep, reduce | Initial `Pose`, `Joints`, and useful results only; no global plan/track/run ontology. |
| 02 ROS interfaces | Defer | Standard ROS types and adapter-local conversions first; custom IDL requires a concrete cross-process gap. |
| 03 config resolution | Replace | Constructor arguments plus small adapter-owned hardware/config files; no nine-layer resolver or provenance tree. |
| 04 plugin discovery | Replace | Direct dictionaries beside implementation files; no entry points, manifests, pluginlib catalogue, or qualification registry. |
| 05 namespaces, TF, time | Keep at ROS seam | Picker adapter owns its names, TF, freshness, and QoS checks; pure values remain ROS-free. |
| 06 task package convention | Reverse default | Ordinary `tasks/*.py`; create a ROS package only when the task itself must be a ROS executable. |
| 07 run records | Defer and make optional | Add task/backend debug artifacts when observed failures need them; no mandatory event platform. |

## Former Phase 02 — manipulation

| Former packet | Verdict | Reason / destination |
|---|---|---|
| Phase README | Delete | Replaced by one vertical manipulation slice. |
| 01 robot lifecycle | Keep, simplify | `bringup()` may own launch and cleanup; remove ObjectDB leases, global ownership tokens, and mandatory recorder coupling. |
| 02 motion contract | Keep, simplify | Start with `move_joints`, `move_pose`, relative helpers, and `stop`; add split plan/execute when preview is used. |
| 03 Pilz motion | Keep concrete | First motion implementation in the Picker adapter; retain proven trajectory and stop checks. |
| 04 OMPL and fallbacks | Defer | Add when a named task needs collision-aware planning or a second explicit plan attempt. |
| 05 visual servo | Defer extraction | First express alignment/control in the grasp task; extract shared logic only after repetition. |
| 06 gripper contract | Keep, reduce | Shared `open`, `close`, `stop`, and useful result fields; tool-specific parameters remain allowed. |
| 07 VGC10 profiles | Keep one first | Implement only the mounted/selected VGC10 geometry used by the reference task. |
| 08 VGP20 | Defer | Promote with a concrete mounted or simulated task. |
| 09 2FG14 | Defer | Promote with a concrete task; do not copy object settings into the driver. |
| 10 base velocity | Defer | Composite `robot.base` remains a planned slot; implement when a task moves the base. |
| 11 concurrent robots | Defer | Two ordinary `Robot` objects first; shared-resource machinery only after a real collision. |
| 12 manipulation acceptance | Replace | [Reference grasp task](work_packets/05_reference_grasp_task.md) is the end-to-end acceptance. |

## Former Phase 03 — ObjectDB and scene

| Former packet | Verdict | Reason / destination |
|---|---|---|
| Phase README | Delete | ObjectDB is no longer a mandatory runtime phase. |
| 01 object JSON schema | Keep, reduce | Small extensible `object.json` with optional paths, models, anchors, and metadata. |
| 02 file store and index | Replace | Direct directories and files; no SQLite cache, locks, activation journal, nested Git transaction, or sync outbox in runtime. |
| 03 legacy migration | Keep on demand | One readable migration script after source data and the exercised file format are available. |
| 04 grasp profiles | Reduce | Anchors live with the object and transform locally; tool-specific metadata stays optional and explicit. |
| 05 object service and CLI | Delete runtime service | `objectdb.load` is local. A CLI may later help author/validate files but is not a server prerequisite. |
| 06 scene and MoveIt sync | Defer to motion task | Add only the scene operations required by the working grasp task. |
| 07 object contract tests | Keep, reduce | Loader, path safety, asset resolution, and anchor-transform tests at the local interface. |

## Former Phase 04 — perception

| Former packet | Verdict | Reason / destination |
|---|---|---|
| Phase README | Delete | One end-to-end perception slice replaces a pre-frozen graph. |
| 01 D455 dataset | Defer to backend evidence | Create the smallest recorded fixture needed to develop/regress the selected algorithms. |
| 02 SAM2 segmentation | Keep as optional backend | Direct `sam2.py` adapter only if selected by a task. TensorRT may be first if the tray asset already provides it. |
| 03 FoundationPose | Keep | Concrete pose backend with explicit RGB/depth/mask/object inputs. |
| 04 tracking contract | Keep, small | Explicit state lives in `Tracker`; common `initialize/update/reset` only after M3T exercises it. |
| 05 M3T ROS adapter | Keep | Native/ROS complexity stays inside `tracking/m3t.py` and its integration support. |
| 06 reseed and track health | Merge into tracker/task | Do not create a generalized recovery state machine before the task needs reseeding. |
| 07 scene snapshots | Delete initially | The task and MoveIt adapter can consume current typed poses directly; add snapshots for a demonstrated multi-object consumer. |
| 08 perception benchmarks | Keep proportional | Record task-relevant accuracy, latency, and stability; two-hour endurance is a backend qualification tool, not a toolbox-wide gate. |

## Former Phase 05 — alignment and grasping

| Former packet | Verdict | Reason / destination |
|---|---|---|
| Phase README | Merge | Goals become the [reference grasp task](work_packets/05_reference_grasp_task.md). |
| 01 alignment contract | Keep, reduce | `LocalAlignment.compute(...)` returns a correction and never moves the robot. |
| 02 legacy characterization | Keep | Preserve proven geometry and safety behavior without copying the old module topology. |
| 03 reference/depth alignment | Keep | Direct backend implementation and recorded fixtures. |
| 04 bounded visual servo | Merge into visible task/helper | Start with ordinary loop/control flow; extract a helper only when repeated. |
| 05 grasp verification | Merge into gripper result/task | Use actual tool feedback and optional lift check; no policy plugin system initially. |
| 06 retry and recovery | Delete framework | Ordinary targeted `try`, `if`, and `while` in the task; uncertain state still stops clearly. |
| 07 grasp acceptance | Keep, narrow | One tray task in Gazebo, then supervised real trials for the actual installed combination. |

## Former Phase 06 — scanning and GUI

| Former packet | Verdict | Reason / destination |
|---|---|---|
| Phase README | Move out of runtime roadmap | ObjectDB is a companion authoring track. |
| 01 scan contract | Defer | Define session state only when implementing the authoring workflow. |
| 02 view capture | Defer | Use the toolbox's ordinary robot and camera objects from a scan script. |
| 03 reconstruction and quality | Defer | A tool/function may run in a separate environment if its dependencies require it. |
| 04 revision registration | Replace | Author a new object directory/revision; no runtime activation lease or Git transaction requirement. |
| 05 object viewer | Defer | Optional local companion once file inspection becomes painful. |
| 06 atomic editor | Defer | Files plus validation first; GUI transaction design follows observed editing problems. |
| 07 grasp annotation and test | Keep as companion goal | Write anchors into the object asset and test them through the same task primitives. |
| 08 scan GUI acceptance | Defer | Replace the infrastructure matrix with one object-from-scan-to-task workflow when built. |

## Former Phase 07 — deployment and release

| Former packet | Verdict | Reason / destination |
|---|---|---|
| Phase README | Delete | Deployment/release is supporting work, not the product roadmap. |
| 01 gateway services | Defer to physical placement | Keep ROS-visible drivers and local watchdogs only for devices that require a gateway. |
| 02 DDS, QoS, and clock | Keep as deployment checklist | Configure and test the actual LAN; no framework. |
| 03 desktop Compose | Replace | Containers launch incompatible dependencies; Python task remains the orchestrator and ObjectDB is not always-on. |
| 04 session recovery | Reduce | Backends stop safely and return explicit errors; no generalized session/epoch/lease state machine. |
| 05 hardware commissioning | Keep | Real adapters require identity, calibration, limits, stop, and supervised test evidence. |
| 06 simulator parity | Defer | Compare only implemented shared operations after a second simulator exists. |
| 07 real qualification | Keep proportional | Run declared trials for the actual task; it does not block unrelated experimental toolbox use. |
| 08 module documentation | Keep, simplify | Handwritten README, canonical task, backend file location, and focused tests; no manifest-generated index. |
| 09 dependency upgrades and release | Defer | Pin adopted dependencies and rerun affected tasks when an internal release is actually cut. |

## Resulting cut

The active plan shrinks from 66 work packets across eight phase READMEs and
approximately 5,600 lines of planning material to seven focused packets, one
backlog, one traceability table, and this audit. More importantly, the first
useful task moves from the end of a multi-phase contract program to the center
of each implementation decision.
