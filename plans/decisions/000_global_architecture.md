# Global architecture decisions

Status: Accepted
Date: 2026-08-26

These decisions came from the global grill. Phase and module plans must not ask them again unless new evidence directly contradicts one.

## Product boundary

- Build a deployment-focused ROS 2 Jazzy toolbox, not a separate robotics framework.
- Keep ordinary ROS nodes, launch files, parameters, TF, topics, services, actions, MoveIt, RViz, rosbag, and vendor drivers visible.
- Follow the tracked repository layout of `dff_mobile_manipulation_docker`: Compose and the ROS workspace live under `.devcontainer/`, ROS packages live directly under `.devcontainer/src/`, and Docker/build/deployment support lives under `scripts/`.
- Keep task packages outside the toolbox as sibling packages under `.devcontainer/src/<task_name>`. Do not add an intermediate `tasks/` directory.
- Keep `object_db` separate from toolbox code.
- Exclude Nav2, coordinated base-arm planning, cuMotion, open-world perception, old-import compatibility, a multi-user GUI, and automatic task resume from v1.

## Package and container boundary

- Use `dfl_manipulation_interfaces` for the small set of custom ROS interfaces.
- Use `dfl_manipulation_toolbox` for the Python task API, common contracts, launch ownership, motion adapters, tools, scenes, and diagnostics.
- Isolate Isaac ROS, M3T, and Genesis in dependency-focused integration packages.
- Use separate Compose services for core Jazzy/MoveIt/Gazebo, Isaac ROS perception, Genesis, ObjectDB, an on-demand scan worker, ObjectDB Git synchronization, and gateways.
- Keep `objectdb` running in real, Gazebo, and Genesis modes. Start `scan-worker` only through the scan profile. `objectdb-sync` owns GitHub credentials and remote push retries.
- Give `objectdb` no GPU, robot or camera device, or Docker socket. It owns the only read-write canonical object mount; consumers mount approved assets read-only.

Reason: this split isolates incompatible GPU and Python dependencies without creating one ROS package per class. The toolbox remains easy to browse while heavy integrations can be built and tested independently.

## Robot, tool, scene, and mode selectors

- Task code selects `robot`, `gripper`, `scene`, `mode`, and `pipeline` by stable ID.
- Picker 1 and Picker 2 are separate namespaced M1013 profiles.
- H2515 is a separate robot profile.
- Supported gripper profiles are VGC10 one cup, VGC10 four cups, VGP20, and 2FG14.
- Supported modes are `real`, `gazebo`, and `genesis`.
- All twelve robot/tool selections must run in both simulators. Real testing covers mounted and commissioned combinations.
- A scene lives under `.devcontainer/src/dfl_manipulation_toolbox/scenes/<scene_id>/` and owns static geometry, expected frames, simulator assets, and default object placement. Runtime perception overlays dynamic objects through the MoveIt planning scene.

## Task and motion API

- Task scripts explicitly spell out home, pre-grasp, approach, alignment, grip, lift, transfer, place, release, retreat, and recovery steps as required by the task.
- Do not add opaque `pick()` or `place()` orchestration.
- Keep combined motion calls and separate `plan()` plus `execute()` access.
- Each motion names a primary planner or control path. A task may provide an ordered fallback list.
- A fallback may run only after planning fails and before any trajectory begins. Unknown or partial execution aborts the task.
- Support Pilz PTP, LIN, and CIRC plus OMPL. CuMotion is deferred.
- Preserve the measured behavior of the existing Cartesian and visual-servo paths through characterization tests before simplifying their implementation.

## Lifecycle and authorization

- `Robot.bringup()` is the default one-command workflow. It owns a standard ROS launch session, records its process tree, handles signals, and cleans up only what it started.
- Explicit attach mode may connect to an intentionally pre-launched stack.
- A new run rejects a healthy unowned stack instead of killing it or reusing it implicitly.
- Running a real-mode task authorizes motion. There is no default confirmation prompt.
- Gateway command watchdogs stop velocity or servo commands when the desktop heartbeat expires.

## Configuration and extensions

- Task code names the robot, tool, scene, mode, and pipeline. Detailed speeds, accelerations, limits, calibration, network values, and backend settings remain in validated files.
- Configuration resolution is deterministic and inspectable. A command prints the merged configuration and its source layers.
- Use pluginlib for C++ integrations and Python entry points for Python integrations.
- Every plugin has a stable ID, contract major version, dependency declaration, configuration schema, and shared contract test.
- A list-implementations command reports installed versions, requirements, and qualification state. Configuration never supplies an import path or source filename.

## Results and failures

- Successful operations return typed values such as poses, plans, motion results, tracked objects, grasp records, gripper status, and run artifacts.
- Expected operational failures raise typed exceptions with a stable code, implementation ID, task stage, and underlying ROS result.
- Visual servoing commands zero velocity during bounded hold and reacquisition. It aborts after the configured bound.
- Blind finish, automatic task resume, and automatic return-home motion after uncertain state are prohibited.
- After loss of control, perception, TF, or network trust, stop and require an explicit recovery task or a fresh run.

## Object data

- Human-readable files are canonical. SQLite may exist only as a rebuildable index or cache.
- Every approved revision stores one mesh and a same-base-name JSON record under an immutable revision directory.
- Preserve stable object IDs, units, coordinate frames, provenance, perception metadata, grasp anchors, gripper-specific profiles, correction offsets, local references, collision geometry, validation status, and test history.
- Migrate the four approved legacy objects and all approved associated revisions. Archive rejected and superseded database history read-only.
- GUI and scripts write through one typed service/CLI with validation, locking, preview, atomic commit, and revision creation.
- Store approved data in a nested private Git repository named `dfl_object_db` inside the project data directory. Keep it independent of the toolbox source history.
- Track approved JSON, meshes, collision assets, compact references, previews, manifests, and hashes. Use Git LFS for binary assets; exclude raw scans, intermediate reconstructions, bags, logs, caches, and model engines.
- Activation requires a durable local Git commit. Remote push runs asynchronously; a failed push marks backup health stale but does not invalidate the local activation.
- ObjectDB is the sole canonical writer. Runtime consumers resolve an exact revision through its API, verify hashes, and use the shared read-only asset mount.
- A running task may continue through an ObjectDB outage after exact revision resolution. A new task cannot start until resolution and lease acquisition succeed.
- Any active task lease blocks active-revision changes. A stale task or scan lease fails closed until diagnostics prove its owner is gone and an operator explicitly releases it.

## ObjectDB and scanning runtime

- ObjectDB is an always-on, loopback-only, single-operator web application with HTTP/WebSocket routes and ROS adapters over one repository library.
- ObjectDB owns scan sessions, operator workflow, evidence, review, approval, and canonical commits. Core/gateway services own robot and camera access, perception owns SAM2, and `scan-worker` owns reconstruction.
- `scan_object` is a first-class ObjectDB workflow. One project command starts its required Compose services; ObjectDB never controls Docker directly.
- Qualify Picker 1 with its commissioned eye-in-hand D455, scene, collision model, and scan poses as the only automated v1 scanning station.
- Physical scanning uses one global lease and exclusive maintenance mode. If a task is active, scan startup refuses and reports the owner; it does not queue, cancel, or stop the task.
- Robot motion requires a fresh scan preflight and one explicit operator start. Component restart never resumes motion automatically.
- Completed scan stages remain durable after failure. Resume requires operator review, and every motion-bearing resume repeats hardware preflight.
- Staging has a configured quota. Reaching it blocks new scans until the operator exports or deletes sessions; no raw session expires silently.

## Perception and alignment

- Qualify the generic RGB-D contract with the installed Intel RealSense D455.
- Use SAM2 for segmentation and FoundationPose for coarse pose initialization and reseeding.
- Use M3T as the intended multi-body tracker for the four-object v1 corpus.
- Report M3T's measured sustainable rate. Approximately 30 Hz is a target, not a release threshold.
- Every track carries identity, pose, timestamp, frame, health/confidence, and stale/lost state.
- Reproduce the existing close-range reference, mask, and depth correction behavior as the v1 local-alignment baseline.
- Scanning supports rigid, opaque, stationary objects. Transparent, mirror-like, deformable, and moving objects are rejected with a reason.

## Simulation and deployment

- Gazebo Harmonic is the primary simulator and uses the official Doosan emulator path.
- Genesis must provide the same task and ROS control contract. Phase 00 first tests whether the official emulator can remain in the loop. If not, implementation stops for a scope decision.
- Desktop services own perception, tracking, planning, grasp selection, task logic, and the main API.
- The NUC and Jetson act as robot-side gateways for sensors, hardware state, and command relay.
- Use a trusted wired lab LAN with one configured `ROS_DOMAIN_ID`, stable host identities, ordinary DDS discovery, and clock synchronization. SROS2 and VPNs are deferred.

## Test and release policy

- Run tests on local lab machines; hosted CI is not required.
- All task runs save a manifest with resolved configuration, versions, stages, result, and metrics. A bounded rosbag/image buffer is retained on failure.
- The perception launch graph must run continuously for two hours without scheduled restart, unbounded memory growth, or stale output presented as current.
- Each installed real robot/tool task runs 30 declared trials, passes at least 29, and has zero unsafe events.
- External dependency upgrades are manual, pinned, test-backed work packets with rollback instructions.
- If an evidence gate disproves a requirement, publish the evidence and stop dependent work for user review.
