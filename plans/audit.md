# Toolbox-first audit of the full roadmap

Date: 2026-08-27

Status: applied to the active phase and work-packet files

## Audit boundary

This is a surgical architecture audit, not a scope-reduction exercise. All
eight phases and all 66 individual work packets remain. The robot, tool,
simulator, manipulation, perception, ObjectDB, scanning, Docker, gateway, and
qualification goals remain.

The audit removes machinery that does not help a robotics developer assemble,
modify, understand, or debug a task. It does not remove a capability because it
is difficult, scheduled later, or exercised after the first vertical slice.

## Tests applied to every packet

- **Task-script test:** what becomes easier in the Python experiment?
- **Five-minute test:** what new knowledge is required before trying an idea?
- **Debugging test:** is the path from task call to backend and ROS/vendor API
  obvious?
- **Deletion test:** does deleting an abstraction lose a concrete capability?
- **Reality test:** is a contract based on actual integrations or imagined
  future ones?
- **Docker test:** does a container boundary isolate a real dependency, GPU,
  device, or host-placement problem, or merely imitate microservices?

Safety at physical robot, controller, vendor, network-watchdog, and uncertain
execution boundaries remains. Evidence that helps compare algorithms or qualify
hardware remains. Generic infrastructure added only for theoretical robustness
does not.

## Architecture changes applied across the plan

1. Python task scripts remain the orchestration layer. Phase packets may add
   helpers and adapters but not a workflow runtime or mandatory task graph.
2. Docker/devcontainer and Compose remain required. Services correspond to
   concrete incompatible environments or hardware placement, not Python class
   boundaries.
3. Backend extension uses direct source mappings near recognizable robotics
   folders. Entry-point ecosystems, generated catalogues, universal manifests,
   qualification registries, and dependency injection are removed.
4. Task configuration stays in constructor arguments where useful. Files hold
   shared hardware facts, calibration, driver settings, scenes, and large model
   configuration. A global layered configuration framework is removed.
5. ObjectDB runtime reads local files. Scanning and authoring remain a full
   Dockerized companion workflow, but an ObjectDB server, Git sync process, and
   lease service are not task-startup dependencies.
6. Custom ROS IDL is introduced only for an actual cross-process exchange that
   standard ROS types cannot express. Python-only values do not acquire ROS
   infrastructure.
7. Run records are useful, bounded debug evidence selected by the task or
   qualification packet—not an always-on observability platform.
8. A representative vertical slice informs the next interface, while the full
   Picker 1, Picker 2, H2515, four-gripper, Gazebo, Genesis, and real-mode scope
   remains scheduled.

## Full capability matrix retained

| Area | Required scope |
|---|---|
| Robots | Picker 1/M1013, Picker 2/M1013, H2515 |
| Tools | VGC10 one cup, VGC10 four cups, VGP20, 2FG14 |
| Modes | real, Gazebo, Genesis where support is honest |
| Composite hardware | arm, mobile base on both Pickers, gripper, D455/camera, force feedback where available |
| Manipulation | joint/pose/relative motion, Pilz, OMPL, visual servo, force-aware motion, concurrent Pickers |
| Perception | D455 data, SAM2/TensorRT-style segmentation, FoundationPose, M3T, health/reseed, snapshots, benchmarks |
| Grasping | object anchors, algorithmic grasps, local alignment, verification, bounded retry/recovery |
| ObjectDB | file assets, legacy migration, grasp profiles, scanning, reconstruction, viewer, editor, annotation |
| Operations | Docker, gateways, DDS/QoS/clock, commissioning, parity, real qualification, documentation, release |

## Phase 00 — foundation and simulation proof

| Packet | Capability retained | Bloat removed or constrained |
|---|---|---|
| README | Dockerized base, profiles, Gazebo, Genesis evidence gate, full simulator matrix | Phase is an implementation sequence, not a gate that blocks vertical task experiments. |
| 01 container and Compose | Pinned Jazzy/devcontainer, GPU/device/mount profiles, reproducible commands | No service-per-module design, Compose task graph, or universal health framework. |
| 02 workspace imports | Reproducible source pins and provenance for adopted dependencies | No central source-management platform; record only dependencies actually used. |
| 03 Doosan Jazzy migration | M1013 and H2515 descriptions, drivers, control, MoveIt, emulator behavior | No wrapper hierarchy that obscures Doosan ROS packages. |
| 04 robot/tool/scene profiles | Picker 1, Picker 2, H2515; four tools; cameras; scenes; three modes | Small readable profiles for shared facts, not a universal configuration schema. |
| 05 Gazebo emulator | All declared robot/tool combinations on the primary simulator | One honest ROS/controller adapter; no simulator-specific task API. |
| 06 Genesis bridge spike | Genesis support and explicit emulator evidence gate | Spike chooses the smallest workable bridge; it does not invent a simulation framework. |
| 07 simulator contract | Common ROS behavior actually shared by Gazebo, Genesis, and real adapters | Extract after both simulators are exercised; do not predict a universal simulator ontology. |
| 08 fixed task matrix | All 12 robot/tool selections in Gazebo and Genesis, with observable pass/fail evidence | Compact task-level checks replace release-platform ceremony. |

## Phase 01 — lightweight shared seams

| Packet | Capability retained | Bloat removed or constrained |
|---|---|---|
| README | Small values, explicit ROS seams, direct backend maps, visible tasks, useful run evidence | No contract freeze before concrete integrations. |
| 01 Python value types | `Pose`, `Joints`, and result fields needed by tasks | No global result envelope or speculative failure-code ontology. |
| 02 ROS interfaces | Standard messages first; focused custom messages/actions only for proven cross-process gaps | No IDL for Python-local calls or imagined consumers. |
| 03 configuration | Visible task arguments plus adapter-owned hardware/calibration/model files | No nine-layer resolver, global provenance tree, or config service. |
| 04 backend selection | Stable names mapped directly to implementation files/classes | No entry points, plugin manifests, discovery daemon, generated registry, or qualification state machine. |
| 05 namespaces, TF, units, time | Namespaced robots, REP-103 units, explicit frames, timestamps, freshness checks | Kept at ROS seams; no parallel time/frame abstraction. |
| 06 task convention | Ordinary `tasks/*.py`, with ROS packaging only when actually required | No mandatory application package, launch hierarchy, or workflow manifest. |
| 07 run records | Optional task/qualification metadata, focused metrics, bounded failure artifacts | No mandatory event bus, recorder service, or observability platform. |

## Phase 02 — manipulation API and control

| Packet | Capability retained | Bloat removed or constrained |
|---|---|---|
| README | Full arm/base/tool/concurrent-robot scope and visible task recovery | No runtime lease, global lifecycle coordinator, or hidden manipulation procedure. |
| 01 robot lifecycle | `bringup()`, explicit attach, readiness, signal cleanup, ownership of started processes | No ObjectDB dependency, Compose control plane, session service, or generalized ownership tokens. |
| 02 motion | `move_joints`, `move_pose`, relative helpers, `stop`, and public plan/execute where useful | One small arm API; no universal motion request/result framework. |
| 03 Pilz | PTP, LIN, CIRC and measured stop/execution behavior | Direct MoveIt/Pilz adapter, not a planner plugin platform. |
| 04 OMPL/fallbacks | Collision-aware OMPL and explicit pre-execution fallback attempts | Task-visible choices; no automated planner policy engine. |
| 05 visual servo | Position/velocity servo primitives, target freshness, bounds, zero-on-loss | State belongs to the servo object/task; no generalized behavior runtime. |
| 06 gripper | Shared open/close/stop/status with useful success/width/force data | Common minimum plus backend-specific methods; no exhaustive capability negotiation. |
| 07 VGC10 profiles | One-cup and four-cup TCP, geometry, IO/control, simulation | Both profiles remain; shared code only where the hardware behavior truly repeats. |
| 08 VGP20 | Real and simulated VGP20 behavior and status | Direct tool backend, not another service layer. |
| 09 2FG14 | Width/force control, result interpretation, descriptions, simulation | Object expectations remain in task/object grasp data, not a driver policy engine. |
| 10 base velocity | Bounded Picker base velocity, deadman/stop, namespace and odometry | Small `robot.base` API over the existing driver; no navigation framework. |
| 11 concurrent robots | Namespaced Picker 1 and Picker 2 tasks and resource-safe lab operation | Two ordinary robot objects and ROS namespaces first; no scheduler or resource manager. |
| 12 acceptance | Complete matrix-focused manipulation checks and hardware evidence | Acceptance validates capabilities without forcing a deployment platform into daily experiments. |

## Phase 03 — object assets, grasps, and planning scene

| Packet | Capability retained | Bloat removed or constrained |
|---|---|---|
| README | File-first assets, revisions where useful, legacy migration, grasps, scene use | Runtime ObjectDB server and sole-writer control-plane role removed. |
| 01 object schema | Small extensible object record: ID, units/frame, mesh, models, anchors, metadata | Optional fields grow from real consumers; no universal asset ontology. |
| 02 file store/index | Normal object directories, immutable approved revisions if needed, rebuildable index | No runtime activation journal, nested transaction coordinator, or mandatory database. |
| 03 legacy migration | Four approved legacy objects/revisions and an auditable converter | One focused migration tool; rejected history can stay read-only without a compatibility framework. |
| 04 grasp profiles | Object-frame anchors and explicit optional tool-specific data | Anchors load with the asset and transform locally; no service lookup. |
| 05 loader and authoring CLI | Local `objectdb.load`, validate/inspect/create-revision commands | No mandatory runtime service, leases, HTTP dependency, or network resolution. |
| 06 scene/MoveIt sync | Explicitly add/update/remove loaded assets and tracked poses in the planning scene | Motion side owns scene state; ObjectDB is not a live scene authority. |
| 07 contract tests | Loader, paths, hashes where used, transforms, profiles, scene fixtures | Focused file/robotics tests instead of service-topology tests. |

## Phase 04 — perception and tracking

| Packet | Capability retained | Bloat removed or constrained |
|---|---|---|
| README | D455, SAM2, FoundationPose, M3T, health/reseed, snapshots, benchmarks | Backends remain ordinary objects/adapters, not managed pipeline components. |
| 01 D455 dataset | Recorded RGB-D, calibration, frames, object/scene labels and splits | Small reusable evidence set; no dataset platform. |
| 02 SAM2 | Dockerized accelerated backend with clear model/prompt/mask API | Direct mapping and thin ROS adapter where Isaac ROS requires it; no plugin infrastructure. |
| 03 FoundationPose | Explicit RGB/depth/mask/mesh pose estimation and reseeding | Backend-specific features remain accessible; no artificial generic input envelope. |
| 04 tracking | Explicit `initialize`, `update`, `reset`, pose/age/health state | State stays in `Tracker`; no general state-management framework. |
| 05 M3T | Native/ROS integration, object meshes, seeds, measured rate | Isolation only for actual build/process needs. |
| 06 reseed/health | Clear lost/stale policy and explicit FoundationPose reseed | Tracker/task logic, not a generalized recovery engine. |
| 07 snapshots | Timestamped multi-object view for real scene consumers | Add a small value/helper; do not build a scene service. |
| 08 benchmarks | Accuracy, latency, stability, memory, and long-run checks for named stack | Qualification evidence is backend-scoped, not a mandatory runtime platform. |

## Phase 05 — local alignment and closed-loop grasping

| Packet | Capability retained | Bloat removed or constrained |
|---|---|---|
| README | Existing alignment behavior, replaceable algorithms, explicit task stages, acceptance | Task Python owns sequence and recovery. |
| 01 alignment | `LocalAlignment.compute(...)` returns correction/health and never moves hardware | Small capability interface with backend-specific access. |
| 02 legacy characterization | Preserve measured geometry, conventions, thresholds, and safety behavior | Copy behavior and fixtures, not old topology or accidental abstractions. |
| 03 reference/depth alignment | Reference, mask, depth, XY/RPY correction backend | Direct implementation with inspectable debug artifacts. |
| 04 bounded visual servo | Apply corrections with explicit limits, freshness, convergence, and stop | Ordinary bounded control loop or small helper, not a behavior framework. |
| 05 grasp verification | Suction/width/force/lift evidence and useful result | Tool-specific checks remain explicit; no verification policy plugin system. |
| 06 retry/recovery | Named retryable stages, uncertain-state stop, task examples | `if`/`while`/`try` remain the mechanism; no state-machine runtime. |
| 07 acceptance | Four objects, supported tools, simulator and real evidence as declared | Trials qualify named combinations without hiding task logic. |

## Phase 06 — ObjectDB scanning and authoring companion

| Packet | Capability retained | Bloat removed or constrained |
|---|---|---|
| README | Full scan-to-approved-asset workflow in Docker, separate from task runtime | Companion tool, not an always-on robotics control plane. |
| 01 scan session | Explicit stages, evidence, resume review, rigid/opaque scope | Local authoring state; no distributed workflow engine or runtime task lease service. |
| 02 view capture | Picker 1/D455 scan poses, masks, calibration, operator start and safe stop | Reuse robot/camera primitives; no duplicate motion API. |
| 03 reconstruction | On-demand dependency-isolated worker, metric mesh, quality report | Separate container is justified by dependencies; orchestration stays a direct job call. |
| 04 revision registration | Reviewed output becomes a new validated file revision | Atomic local write; Git commit/backup optional authoring policy, never task startup. |
| 05 viewer | Local mesh/reference/grasp/quality inspection | UI reads normal files through a small authoring API only where needed. |
| 06 editor | Validated edits, preview, atomic save/new revision | Single-user local workflow; no multi-user transaction platform. |
| 07 annotation/test | Create tool-aware anchors, preview transforms, run explicit robot tests | Uses the same toolbox primitives and file format as tasks. |
| 08 acceptance | One full physical-object-to-task workflow plus failure/recovery checks | Validate user workflow rather than container/service topology. |

## Phase 07 — deployment support and release evidence

| Packet | Capability retained | Bloat removed or constrained |
|---|---|---|
| README | Gateways, LAN/DDS, Compose, safe recovery, commissioning, parity, qualification, docs, releases | Operations support robotics work; it does not redefine the toolbox as a platform. |
| 01 gateways | NUC/Jetson device-side ROS drivers, state relay, heartbeat/watchdog where physically required | No generic gateway framework or duplicated desktop intelligence. |
| 02 DDS/QoS/clock | Tested discovery, topic QoS, bandwidth, host identity, and clock sync | Use ROS/DDS mechanisms and documented commands; no network control plane. |
| 03 desktop Compose | Profiles for core, perception, Genesis, ObjectDB authoring, scan worker, and gateways | Compose starts dependency groups; Python remains task orchestration; no mandatory ObjectDB/sync services. |
| 04 recovery | Safe stop, component restart behavior, revalidation, explicit fresh task/run | No automatic motion resume or generalized session/epoch/lease state machine. |
| 05 commissioning | Identity, mounts, TCPs, calibration, limits, network, force/tool behavior | Plain records and executable checks, not a configuration product. |
| 06 parity | Shared operations compared across Gazebo and Genesis for full declared matrix | Report honest differences instead of forcing false uniformity. |
| 07 real qualification | Supervised trials, metrics, failures, unsafe-event criteria for installed combinations | Evidence belongs to named tasks/adapters; it does not block unrelated experiments. |
| 08 documentation | Architecture map, task examples, backend locations, Docker commands, diagnostics, limitations | Handwritten and source-adjacent; no generated portal or manifest registry. |
| 09 upgrades/release | Pinned dependency updates, affected tests, rollback, reproducible images | Manual internal release procedure; no deployment pipeline is created. |

## Result

The active roadmap still contains 8 phases, 8 phase READMEs, and 66 individual
work packets. Each packet remains independently actionable and now states its
task-script payoff and smallest sufficient design. Docker, the original
repository layout, every robot, all four grippers, both simulators, real mode,
and the complete robotics/ObjectDB scope are retained.

The reduction is architectural: fewer mandatory layers, registries, services,
leases, global schemas, and orchestration concepts between a task script and the
robotics code it needs.
