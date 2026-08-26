# Global toolbox architecture decisions

Status: accepted planning baseline

Date: 2026-08-27

These decisions apply to every phase. Revisit one only when implementation
evidence shows that it blocks a concrete robotics task or cannot meet a safety
requirement.

## Product boundary

- Build an internal robotics development and research toolbox whose primary
  interface is an ordinary Python task script.
- Do not build a deployment platform, workflow engine, generalized robotics
  framework, managed component runtime, or mandatory ObjectDB service.
- Keep ROS 2 Jazzy, launch, parameters, TF, topics, services, actions, MoveIt,
  RViz, rosbag, controller state, and vendor drivers visible and directly
  debuggable.
- Preserve the complete planned utility; simplify architecture, not robots,
  tools, modes, algorithms, ObjectDB authoring, or test coverage.

## Repository layout

- Follow the established Docker repository shape: devcontainer, Dockerfiles,
  Compose files, and the ROS workspace under `.devcontainer/`; ROS packages
  directly under `.devcontainer/src/`; operator/build helpers under `scripts/`.
- Keep ordinary experiment scripts under root `tasks/` by default. A task may
  live as a sibling ROS package under `.devcontainer/src/` only when it genuinely
  needs ROS packaging, installation, or launch semantics.
- Inside the toolbox, organize by robotics concepts: `robots`, `grippers`,
  `cameras`, `perception`, `grasping`, `motion`, `simulation`, and `objectdb`.
- Keep scenes, calibration, models, objects, data, and logs as inspectable files
  in explicit mounts/directories.
- Do not add generic `runtime`, `provider`, `executor`, `manager`, `resource`, or
  orchestration layers without a demonstrated problem that a smaller module
  cannot solve.

## Docker and process boundaries

- Dockerization is required for reproducible development and operation.
- Use separate images/Compose services only for real dependency or placement
  boundaries: core Jazzy/MoveIt/Gazebo, accelerated perception, native M3T when
  needed, Genesis, ObjectDB authoring, on-demand scan reconstruction, and
  hardware gateways.
- Do not create a service per Python class or capability. Normal Python
  capabilities remain imports and ordinary objects.
- Compose starts dependency groups and exposes clear health/device/mount/log
  information. It does not encode the task sequence; the Python script does.
- ObjectDB authoring and scan services are opt-in. An experiment loading an
  approved local asset must not require ObjectDB, scan worker, or Git-sync
  services to be running.
- Give each container only the GPU, camera, robot device, network mode, and
  writable mounts it genuinely needs. Make persistent ownership explicit.
- Pin adopted images and dependency sources. Keep one command per common
  profile and a direct command for inspecting the underlying Compose/ROS state.

## Robot, tool, scene, and mode selectors

- The convenient task constructor is
  `Robot(model=..., mode=..., gripper=..., scene=...)`.
- Picker 1 and Picker 2 are separate, namespaced composite robots. Both use an
  M1013 arm and expose their mobile base, gripper, camera, and other installed
  hardware through their real structure.
- H2515 is a separate robot profile and must not be flattened into a fictional
  universal mobile manipulator.
- Required tool profiles are VGC10 one cup, VGC10 four cups, VGP20, and 2FG14.
- Required modes are `real`, `gazebo`, and `genesis` wherever an honest adapter
  can provide the operation. Unsupported behavior fails clearly.
- The simulator matrix covers all 12 robot/tool selections in Gazebo and
  Genesis. Real qualification covers installed and commissioned combinations.
- Scene folders own static geometry, expected frames, simulator assets, and
  initial placements. The motion side explicitly updates dynamic collision
  objects from loaded assets and current perception.
- Concrete lower-level robot/tool/simulator backends remain directly importable
  for debugging.

## Task and motion API

- Task scripts explicitly show home, perception, approach, alignment, contact,
  grip, verification, lift, transfer, place, release, retreat, and recovery as
  needed by that experiment.
- Ordinary Python `if`, `while`, `try`, functions, and small objects are the
  default task orchestration.
- Do not hide a research manipulation pipeline behind an opaque `pick()` or
  `place()` implementation. Repeated high-level helpers may be built on the same
  directly accessible primitives.
- Expose `robot.arm`, `robot.base`, `robot.gripper`, and `robot.camera` according
  to the actual platform. Multi-arm platforms may expose named arms rather than
  a flattened interface.
- Start with clear calls such as `move_joints`, `move_pose`, `ascend`, `descend`,
  `apply_cartesian_offset`, and `stop`. Keep separate `plan` and `execute` when a
  task actually previews, inspects, or reuses plans.
- Support Pilz PTP/LIN/CIRC and OMPL through small MoveIt adapters. Planner
  selection and any pre-execution fallback remain visible in task arguments or
  a short helper; never continue after unknown or partial execution.
- Force-aware motion belongs in a robot backend where sensing/control supports
  it. An unsupported mode raises a useful error rather than silently degrading.

## Lifecycle and safety

- `Robot.bringup()` is the convenient workflow and may own a normal ROS launch
  process. It records enough local state to clean up only what it started.
- Explicit attach mode may connect to an intentionally pre-launched stack.
- Starting a real task authorizes the motion written in that task; no generic
  confirmation framework is required. Physical scan motion retains its explicit
  operator-start requirement because it is an authoring workflow around a
  person and object.
- Gateway command watchdogs stop velocity/servo commands when required by the
  physical connection.
- Loss of control, TF/time validity, perception freshness, or network trust
  causes an explicit safe stop. Never auto-resume motion or guess that an
  interrupted command completed.
- Hardware exclusivity may use the smallest local/ROS ownership check needed to
  prevent two writers. Do not introduce an ObjectDB-owned distributed lease
  system for normal task execution.

## Lightweight values, errors, and configuration

- `Pose` and `Joints` are lightweight Python values using metres and radians;
  poses carry an explicit frame. ROS conversions live in ROS adapters.
- Add small result values only when task code consumes the fields—for example,
  gripper success, final width, and force.
- Errors name the failed operation, selected robot/tool/mode/backend, violated
  assumption, and corrective context. Avoid a global enterprise error taxonomy.
- Task choices and experimental parameters remain visible in the script.
- Small validated files hold shared hardware facts, limits, calibration,
  network endpoints, MoveIt/controller configuration, scene geometry, and large
  backend settings. Resolution is short, deterministic, and owned by the
  relevant adapter.
- Provide direct diagnostics showing the selected file/value where ambiguity is
  likely. Do not build a project-wide layered configuration service.

## Backend extensibility

- A capability such as `Segmenter`, `PoseEstimator`, `Tracker`,
  `LocalAlignment`, or `GraspGenerator` is an ordinary Python object.
- Backend IDs map through small source-controlled dictionaries next to their
  implementation files. The optional user spelling `backend="sam2.py"` may be
  normalized to `sam2`.
- A normal Python backend requires its implementation file, one mapping entry,
  dependencies in the relevant Docker image, and focused tests.
- Do not require Python entry points, plugin manifests, generated catalogues,
  discovery services, qualification registries, configuration schemas, or
  dependency injection.
- Native C++ or ROS-process implementations may use the mechanisms their actual
  stack requires, but the task-facing adapter remains thin and inspectable.
- Shared methods cover repeated behavior. Backend-specific methods are allowed;
  do not force different algorithms into an opaque generic `input` array.

## ROS interfaces and namespaces

- Prefer standard ROS messages, services, and actions.
- Add a custom interface package only for concrete cross-process semantics that
  standard types cannot express clearly. Keep Python-local values out of IDL.
- Namespace every robot and tool path. Picker 1 and Picker 2 must coexist
  without topic, node, controller, parameter, action, service, or TF collisions.
- Follow REP-103 units and coordinate conventions. Preserve source timestamps
  and frames, and reject stale or unavailable transforms explicitly.
- Use normal ROS CLI and graph tools as the first debugging path.

## Object data

- Human-readable files are canonical. An object directory contains a small
  record plus mesh and optional grasp/model/reference assets.
- Preserve stable object ID, units, canonical frame, dimensions, mesh/collision
  paths, provenance, optional perception models, object-frame grasp anchors,
  tool-specific data where necessary, local references, validation status, and
  useful test history.
- `dfl.objectdb.load(...)` reads those files locally and returns an asset object.
  Tasks transform its grasp anchors locally and explicitly add assets to the
  planning scene.
- Migrate the four approved legacy objects and their approved revisions. Archive
  rejected/superseded source history read-only where useful.
- Immutable approved revisions and a rebuildable index are allowed where they
  improve authoring/history. SQLite is never the only source of truth.
- Hash validation, Git commits, Git LFS, and remote backup may be used inside the
  ObjectDB authoring workflow. They are not prerequisites for loading an object
  in an experiment.

## ObjectDB and scanning companion

- ObjectDB remains a standalone companion application for capture, scanning,
  reconstruction, cleanup, review, annotation, revision creation, and grasp
  testing.
- It writes the same files the toolbox loads and does not need to run during an
  experiment.
- Qualify Picker 1 with its commissioned eye-in-hand D455, scene, collision
  model, and scan poses as the first physical scanning station; reuse ordinary
  robot/camera/perception primitives.
- Scanning v1 supports rigid, opaque, stationary objects and clearly rejects
  unsupported materials/behavior.
- Reconstruction may run in an on-demand Docker service because its dependencies
  justify isolation. A direct job request/result is enough; do not build a
  general distributed workflow engine.
- Scan stages and evidence may persist locally so an operator can review and
  resume. Motion-bearing resume always repeats preflight and explicit start.
- Physical scanning must exclude concurrent task motion using the smallest
  reliable machine/ROS-level lock and clear ownership diagnostics. ObjectDB does
  not become the lease authority for every normal task.
- The local viewer/editor remains single-operator and file-oriented. Atomic save
  and validation are required; multi-user transactions and service meshes are
  not.

## Perception, alignment, and grasping

- Qualify the generic RGB-D seam on the installed Intel RealSense D455.
- Retain SAM2, TensorRT-style segmentation backends, FoundationPose, M3T, track
  health/reseed, and task-relevant scene snapshots.
- Each track carries identity, pose, source timestamp/frame, age, and clear
  healthy/stale/lost state as needed by consumers.
- Approximately 30 Hz for M3T is a measurement target, not a fabricated success
  claim. Benchmarks publish actual rate, latency, accuracy/stability, memory, and
  failure behavior.
- Preserve existing close-range reference/mask/depth alignment behavior through
  characterization before changing its geometry.
- `LocalAlignment.compute(...)` returns a correction and diagnostics; applying
  robot motion is a separate visible task step.
- Object-defined anchors, geometric generators, learned grasping, and custom
  experimental methods coexist. Grasp verification uses actual tool/robot
  evidence and returns simple useful results.
- Retry and recovery are explicit ordinary task control flow. Reusable helpers
  may emerge only after repeated tasks prove the same pattern.

## Simulation, gateways, and deployment support

- Gazebo Harmonic is the primary simulator and uses the official Doosan emulator
  path where viable.
- Genesis must support the same useful task-facing and ROS behavior. Phase 00
  tests whether the official emulator can remain in the loop; failure records a
  decision and smallest alternative rather than silently removing Genesis.
- Desktop processes own task logic, perception, tracking, planning, and grasp
  selection. NUC/Jetson gateways own only hardware/device-side responsibilities
  that must run there.
- Use a trusted wired lab LAN with configured `ROS_DOMAIN_ID`, stable host names,
  ordinary DDS discovery, tested QoS, and synchronized clocks. Do not layer a
  second communications framework over ROS.

## Testing and release evidence

- Run tests on local lab machines; hosted CI is optional, not required.
- Use focused unit tests for pure/file code, recorded fixtures for perception,
  simulator matrices for robot/tool behavior, and supervised hardware tests for
  installed combinations.
- Run records are opt-in for ordinary experiments and required where a packet's
  benchmark or qualification needs reproducible evidence. Keep the format small
  and retain bounded failure artifacts that actually aid diagnosis.
- Long-duration perception checks and 30-trial/29-success real-task criteria
  remain named qualification goals where specified; they do not force every
  experiment through a release runtime.
- External dependency upgrades are manual, pinned, test-backed work with
  rollback instructions.
- If evidence disproves an assumption, preserve the user capability where
  feasible, publish the evidence, and request a decision before any material
  scope reduction.
