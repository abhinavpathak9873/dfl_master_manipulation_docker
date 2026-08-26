# DFL Manipulation Toolbox: accepted implementation baseline

Status: Accepted for work-packet implementation  
Decision date: 2026-08-26  
Detailed planning pack: [`plans/overview.md`](plans/overview.md)

## Objective

Build `dfl_master_manipulation_docker`, a deployment-focused ROS 2 Jazzy workspace for repeatable manipulation with Doosan arms. It must let a developer write a short task script while retaining direct access to ROS nodes, launch files, topics, services, actions, parameters, TF, MoveIt, rosbag, and simulator state.

The first release supports two namespaced M1013 profiles, Picker 1 and Picker 2, plus a separate H2515 profile. Its tool profiles are VGC10 with one cup, VGC10 with four cups, VGP20, and 2FG14. The same explicit task steps must work in real mode, Gazebo, and Genesis when the selected hardware combination is available.

V1 proves the complete workflow on four approved legacy objects. The object format may scale beyond that corpus, but an untested claim about 30 known objects or 20 simultaneous objects is not a release requirement.

## Product boundary

This project adds a small task API and typed contracts around standard ROS 2 components. It does not introduce a new runtime framework. Task packages remain ordinary ROS packages directly under `.devcontainer/src/<task_name>`, matching `dff_mobile_manipulation_docker`; there is no intermediate `tasks/` directory. Object data remains separate from source. Heavy integrations for Isaac ROS, M3T, and Genesis receive their own dependency-focused packages so their GPU, native, and Python environments do not leak into the core package.

V1 excludes:

- Nav2 and coordinated base-arm planning;
- cuMotion;
- open-world object recognition;
- compatibility with the old import paths;
- multi-user object editing;
- automatic task resume after a process, network, TF, or perception failure;
- opaque `pick()` and `place()` orchestration.

The mobile base exposes bounded `cmd_vel` control for positioning and tests. It is not part of whole-body planning.

## Repository shape

The repository follows the directory pattern of `dff_mobile_manipulation_docker` without copying its single-container limitation. Compose definitions and the live ROS source workspace live under `.devcontainer/`; Dockerfiles, environment setup, build, pull, deploy, entrypoint, DDS, and clock scripts live under `scripts/`; VS Code configuration lives under `.vscode/`. The live host path `.devcontainer/src` mounts at `/root/ros2_ws/src` in development containers. This project may add Compose files, Dockerfiles, scripts, and durable runtime directories required by its wider service set, provided those additions stay within these directory roles. Do not introduce competing root-level source, Compose, or Dockerfile layouts.

The planned tracked layout is:

```text
dfl_master_manipulation_docker/
├── .devcontainer/
│   ├── devcontainer.json
│   ├── docker-compose-dfl-master-manipulation-ros2-jazzy.yml
│   ├── docker-compose-gateway-ros2-jazzy.yml
│   └── src/
├── .vscode/
├── scripts/
├── calibration/
├── data/
├── logs/
├── models/
├── plans/
├── .dockerignore
├── .gitignore
├── AGENTS.md
├── Context.md
├── README.md
└── toolbox_plan.md
```

`plans/` and `toolbox_plan.md` are retained planning artifacts specific to this repository. Package-owned configuration, scenes, launch files, tests, and documentation stay inside their owning package beneath `.devcontainer/src/`, as they do in the reference repository. The project-level `calibration/`, `data/`, `logs/`, and `models/` directories are durable mount roots required by the multi-service design; generated or sensitive contents remain ignored as appropriate.

The planned ROS source layout is:

```text
.devcontainer/src/
├── doosan-robot2/
├── moveit2_calibration/
├── picker1_final_moveit_config/
├── picker2_bringup/
├── picker2_description/
├── picker2_final_moveit_config/
├── rlab_zinger_4ws-main/
├── ros2_pick_and_place/
├── dfl_manipulation_interfaces/
├── dfl_manipulation_toolbox/
├── dfl_isaac_ros_integration/
├── dfl_m3t_integration/
├── dfl_genesis_integration/
├── object_db/
├── fixed_pick_place/
└── grasp_test/
```

Additional tasks are sibling ROS packages under `.devcontainer/src/<task_name>/`. They are not nested inside the toolbox or a `tasks/` collection directory.

The exact integration-package names may change before their package manifests are created. Their ownership boundaries may not: custom messages belong to the interface package; reusable task and motion behavior belongs to the toolbox; heavy dependency adapters remain isolated; application behavior belongs to task packages.

## Deployment and container model

The main desktop runs task logic, perception, tracking, planning, grasp selection, and the toolbox. The Intel NUC and Jetson AGX Orin act as robot-side gateways for sensors, hardware state, and command relay.

Compose separates the core Jazzy, MoveIt, and Gazebo service from Isaac ROS perception, Genesis, ObjectDB, scan reconstruction, Git synchronization, and gateway services. `objectdb` runs in every mode; `scan-worker` starts only for scanning. ObjectDB owns the only read-write canonical object mount and receives no GPU, camera, robot device, or Docker socket. Every external source or image is pinned; a floating branch or `latest` tag is not a reproducible input.

Machines use a trusted wired lab network, one configured `ROS_DOMAIN_ID`, stable host identities, DDS discovery, and Chrony. Qualification requires measured inter-host clock offset no greater than 5 ms. Phase 07 compares supported RMW choices on the installed network and selects from evidence; if the results tie, use Cyclone DDS.

## Task API and lifecycle

Task code selects stable IDs for `robot`, `gripper`, `scene`, `mode`, and `pipeline`. Detailed limits, calibration, QoS, backend settings, and speed values live in validated configuration. Configuration resolution is deterministic, and a CLI prints the final value of every field with the source layer that supplied it.

`Robot.bringup()` starts and owns a standard ROS launch session. It records the process tree, handles signals, and stops only the processes it owns. An explicit attach mode connects to a deliberately pre-launched stack. A new run rejects a healthy unowned stack instead of silently reusing or terminating it.

Starting a task in real mode authorizes motion; no confirmation prompt appears by default. The gateway watchdog stops streaming velocity and servo commands when the desktop heartbeat expires.

Task scripts state the physical sequence directly: home, pre-grasp, approach, alignment, grip, lift, transfer, pre-place, place, release, retreat, and recovery where the task needs them. The API provides combined motion calls and separate `plan()` and `execute()` access. It returns typed values and raises typed operational exceptions carrying a stable failure code, implementation ID, task stage, and underlying ROS result.

## Planning and control

MoveIt 2 owns the planning scene, collision checking, constraints, and trajectory planning. V1 supports Pilz PTP, LIN, and CIRC plus OMPL. Each motion selects a primary planner or control path and may declare an ordered fallback list. A fallback can run only after planning fails and before any trajectory starts. An unknown or partially executed trajectory stops the task and requires explicit recovery.

Visual servoing is bounded. Loss of a fresh target commands zero velocity during a fixed hold and reacquisition interval, then aborts. The controller never completes an approach blind. The existing Cartesian and visual-servo behavior is characterized before its code is simplified.

Gripper commands use one shared contract but retain tool-specific configuration, feedback, and verification. VGC10 one-cup and four-cup behavior are separate profiles. VGP20 and 2FG14 each have their own adapter and acceptance tests. Hardware limits and payload values must come from vendor data or commissioned measurements, not inferred defaults.

## Object data and planning-scene ownership

Human-readable files are canonical. SQLite may exist only as a disposable, rebuildable index. Each approved object revision contains one mesh and a same-base-name JSON record in an immutable revision directory. The record preserves stable identity, units, canonical frame, provenance, perception metadata, collision geometry, grasp anchors, tool-specific grasp profiles, correction offsets, close-range references, validation state, and test history.

Migration covers the four approved legacy objects and all approved associated revisions. Rejected and superseded database history is retained read-only. The GUI and scripts write through the same typed service and CLI, which perform validation, locking, preview, atomic commit, and revision creation.

Approved object bundles live in a nested private `dfl_object_db` Git repository inside the project data directory. JSON stays in normal Git; approved meshes, collision assets, previews, and compact references use Git LFS. Raw captures, reconstruction intermediates, bags, logs, caches, and model engines stay outside Git. Activation requires a durable local commit, while a credential-isolated synchronization service pushes asynchronously and reports stale backup health.

Task startup acquires a runtime lease and resolves exact revision IDs and hashes through ObjectDB. Consumers read immutable assets from a shared read-only mount. A running task may continue during an ObjectDB outage after resolution; a new task cannot start. Active or stale-unverified task leases block revision activation.

The object service publishes accepted dynamic objects to MoveIt's planning scene. Static scene geometry belongs to the owning toolbox package at `.devcontainer/src/dfl_manipulation_toolbox/scenes/<scene_id>/`. Neither the perception pipeline nor the GUI owns a second world model.

## Perception and tracking

The runtime sensor contract accepts calibrated RGB-D input and is qualified with the installed Intel RealSense D455. Phase 04 records a versioned four-object dataset with camera calibration, TF, object truth, occlusion cases, and failure cases before backend tuning begins.

V1 uses SAM2 for segmentation and Isaac ROS FoundationPose for coarse pose initialization and reseeding. M3T is the intended multi-body tracker. The project supplies a ROS adapter because M3T is a native C++ library, not a ROS package. Every track reports object ID, pose, timestamp, frame, health or confidence evidence, and fresh, stale, or lost state.

Approximately 30 Hz is a target to measure, not a release threshold. Release reports the sustainable rate, latency distribution, accuracy, recovery time, GPU and host memory behavior, and false-stable drift. The complete perception launch graph must run for two hours without scheduled restarts, unbounded memory growth, or stale data represented as current.

## Local alignment and grasp recovery

The first alignment backend reproduces the existing close-range reference-image, mask, and depth-correction behavior. It consumes a selected object revision, grasp anchor, live calibrated RGB-D data, current tool pose, and track health. It emits bounded Cartesian correction commands and explicit completion or failure evidence.

Grasp verification uses tool-appropriate feedback plus motion and scene evidence. Recovery rules are finite and visible in task configuration. A retry can reacquire perception, choose another approved anchor, or retreat to a declared safe pose only when robot state remains trusted. Network loss, uncertain execution, invalid TF, or loss of control stops the task; it does not trigger automatic return-home motion.

## Scanning and object editor

Scanning supports rigid, opaque, stationary objects. Transparent, mirror-like, deformable, or moving subjects are rejected with a recorded reason. The pipeline captures calibrated views, reconstructs a candidate mesh, reports coverage and quality evidence, and creates a draft revision. It never overwrites an approved revision.

The first GUI is a local, single-user web application served by the always-on ObjectDB container. It lists and renders objects, edits metadata, places grasp anchors with the correct tool model, previews changes, commits through the object service, and invokes the same grasp-test contract used by task packages. Business rules stay in the service and schema layer rather than in browser-only code.

`scan_object` is an ObjectDB workflow, not a monolithic runtime. ObjectDB owns its durable session, operator actions, evidence, review, and commit. Core/gateway services own Picker 1 and its commissioned eye-in-hand D455, perception owns SAM2, and an on-demand worker owns reconstruction. Scanning is exclusive maintenance work: active tasks cause startup refusal, motion begins only after fresh preflight and explicit operator start, and restart requires explicit stage resume. Raw staging is quota-bound and removed only by an explicit export or cleanup action.

## Simulation

Gazebo Harmonic is the primary simulator and keeps the official Doosan emulator in the control path. Genesis 1.3.3 is the secondary simulator. Phase 00 first proves whether Genesis can mirror or drive the same command and state contract while the official emulator remains authoritative. If that relationship cannot be made correct, dependent Genesis work stops and produces evidence for a scope decision. It does not quietly replace the accepted emulator requirement.

All twelve robot/tool selections must load in Gazebo and Genesis. Fixed pose tasks verify lifecycle, trajectory semantics, frames, cancellation, stop behavior, tool state, contacts, deterministic reset, and `/clock`. Representative grasp behavior is qualified later against the same task contract.

## Evidence, testing, and release

Tests run on the local lab machines. Every contract should have a live-hardware-independent path using unit tests, fakes, recorded data, headless simulation, or a vendor emulator. Real qualification follows only after those paths pass.

Every task run writes a manifest with resolved configuration, dependency and code versions, robot and tool identity, timestamps, stages, results, and metrics. A bounded rosbag and image buffer is retained on failure. Logs must distinguish planned failure, execution failure, stale perception, invalid TF, tool failure, watchdog stop, and operator cancellation.

Each installed real robot and tool task runs 30 declared trials, with at least 29 successes and zero unsafe events. A trial protocol fixes objects, start states, acceptance geometry, operator actions, environmental conditions, and rules for excluded trials before testing begins.

Dependency upgrades are manual work packets. Each records old and new pins, upstream changes, build and contract-test results, benchmark deltas, data migrations, and rollback instructions.

## Implementation order

1. Phase 00 establishes containers, source pins, robot and tool profiles, scenes, Gazebo, Genesis feasibility, and fixed tasks.
2. Phase 01 freezes shared value types, ROS interfaces, configuration, extension discovery, namespacing, time rules, and run records.
3. Phase 02 builds lifecycle, motion, planners, visual servo, grippers, base velocity, multi-robot behavior, and manipulation acceptance.
4. Phase 03 migrates and validates object revisions, grasp profiles, typed access, and planning-scene synchronization.
5. Phase 04 qualifies the D455, SAM2, FoundationPose, M3T, track health, snapshots, and perception performance.
6. Phase 05 adds local alignment, bounded closed-loop grasping, verification, retry rules, and grasp acceptance.
7. Phase 06 adds scanning, reconstruction qualification, revision registration, the object viewer/editor, and grasp testing.
8. Phase 07 completes gateway deployment, DDS and time qualification, session recovery, simulator parity, hardware trials, module documentation, and release control.

Phase dependencies and safe parallel paths are maintained in [`plans/overview.md`](plans/overview.md). Requirement ownership is maintained in [`plans/traceability.md`](plans/traceability.md). An implementation agent receives one module packet, its phase README, the accepted global decisions, and only the upstream artifacts named by that packet.

## Stop conditions

An implementation packet stops when an evidence gate disproves its premise, an upstream public contract is missing, hardware state is unsafe or uncertain, or a requested change would cross a declared ownership boundary. The agent records the evidence and asks for the specific decision. It does not settle a product or safety choice in code.
