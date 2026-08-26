# DFL robotics toolbox: accepted direction

Status: accepted planning baseline

Revised: 2026-08-27

## Product

This repository plans a small, modular, hackable internal robotics toolbox. Its
product is the Python task script a robotics developer reads, edits, runs, and
debugs. It is not a production application platform, workflow engine, deployment
framework, or replacement for ROS.

The primary test for every design decision is:

> Does this make a representative robotics task easier to write, modify,
> understand, or debug?

Reliability should come from simple architecture, predictable behavior, explicit
state, clear interfaces, good errors, focused tests, and visible ROS mechanisms.
Complexity must solve a concrete robotics or dependency problem.

## Planning-only boundary

The current repository milestone is the plan. No toolbox package, task
implementation, placeholder backend, test scaffold, or pretend robot is part of
this planning revision. The phase packets specify future work; they do not claim
that it has already started.

## Required utility is not optional scope

Architectural simplification must not reduce the toolbox's intended utility. The
plan retains all of the following:

- Picker 1 with its Doosan M1013 arm and mobile base;
- Picker 2 with its Doosan M1013 arm and mobile base;
- a separate Doosan H2515 robot profile;
- VGC10 one-cup, VGC10 four-cup, VGP20, and 2FG14 tool profiles;
- `real`, `gazebo`, and `genesis` modes wherever the corresponding hardware or
  simulator can honestly support the operation;
- arm motion, base velocity, gripper control, cameras, force-aware operations,
  concurrent Picker 1 and Picker 2 use, and simulator parity;
- segmentation, pose estimation, tracking, reseeding, scene snapshots,
  benchmarks, local alignment, visual servoing, grasp verification, retry, and
  recovery primitives;
- file-first ObjectDB assets, legacy migration, grasp profiles, planning-scene
  synchronization, scanning, reconstruction, viewing, editing, annotation, and
  scan-to-task acceptance;
- desktop, gateway, DDS/QoS/clock, commissioning, qualification, documentation,
  dependency-upgrade, and release work;
- Dockerized, reproducible development and runtime environments.

Phases establish an implementation order and evidence gates. A later phase is
still committed scope. "Build one vertical slice first" never means "support
only Picker 1" or "remove the other tools."

## Target task-script experience

The canonical design example is [`api_example.md`](api_example.md). It uses
ordinary Python so the robotics sequence remains visible from top to bottom:

```python
import dfl_toolbox as dfl

robot = dfl.Robot(
    model="picker1",
    mode="gazebo",
    gripper="vgc10_1cup",
    scene="empty",
)
robot.bringup()

tray = dfl.objectdb.load("small_tray")
segmenter = dfl.perception.Segmenter(
    backend="tensorrt",
    model=tray.models.segmentation,
)

rgb, depth = robot.camera.get_rgbd()
mask = segmenter.segment(rgb)
```

Running a normal experiment should be approximately:

```bash
python tasks/small_tray_pick.py
```

A ROS-aware wrapper or package is allowed where required. It must not become
mandatory ceremony for every experiment. Ordinary `if`, `while`, `try`, and
function calls remain the default orchestration language.

## Repository shape

The repository should mirror the robotics mental model while retaining the
Docker workspace layout already established for this project:

```text
.devcontainer/
  devcontainer.json
  docker-compose.yml
  docker-compose.gazebo.yml
  docker-compose.genesis.yml
  docker-compose.real.yml
  docker-compose.scan.yml
  src/                         # ROS packages mounted at /root/ros2_ws/src
    dfl_manipulation_toolbox/
      dfl_toolbox/
        robots/
        grippers/
        cameras/
        perception/
          detection/
          segmentation/
          pose/
          tracking/
          alignment/
        grasping/
        motion/
        simulation/
        objectdb/
      config/
      launch/
      scenes/
    dfl_manipulation_interfaces/   # only concrete custom ROS IDL
    dfl_*_integration/             # only when dependency isolation requires it
tasks/                         # ordinary task scripts by default
objects/                       # or configured external ObjectDB asset root
calibration/
models/
data/
logs/
scripts/                       # build, run, setup, validation, and diagnostics
plans/
```

Exact package names can change during implementation, but these ownership rules
must not:

- folders use recognizable robotics concepts;
- ordinary task scripts remain first-class;
- ROS packages live directly in `.devcontainer/src/` when they are ROS
  packages;
- Docker/build/operator helpers live in `scripts/`;
- calibration, models, objects, data, and logs remain inspectable files;
- avoid generic `runtime/`, `providers/`, `executors/`, `orchestrators/`, or
  `services/` layers unless a concrete integration proves one is necessary.

## Docker is required supporting infrastructure

Everything must be runnable through pinned Docker/devcontainer environments.
Dockerization is not architectural bloat here: it solves real ROS, GPU, vendor,
simulator, and Python dependency conflicts and makes experiments reproducible.

Compose may provide separate dependency-focused services for:

- core ROS 2 Jazzy, MoveIt, robot drivers, and Gazebo;
- accelerated perception such as Isaac ROS/FoundationPose;
- M3T when its native build requires isolation;
- Genesis;
- the ObjectDB authoring application;
- an on-demand reconstruction/scan worker;
- robot-side gateways or hardware-specific drivers.

These are process and dependency boundaries, not a task graph. Compose brings up
required processes; the Python task still owns the experiment's sequence. Do
not create a separate service merely because a Python class exists. ObjectDB is
not required to be running for a task to load an already-authored local asset.

Each Compose profile must make mounts, devices, GPUs, network assumptions,
health checks, logs, and ownership explicit. Real-hardware profiles must default
to safe startup. Simulator and real profiles should expose the same useful ROS
contract without hiding genuine differences.

## Architecture and debugging path

The expected path through the code is short:

```text
task script
  -> robotics capability object
  -> named backend implementation file
  -> ROS / MoveIt / model / vendor API
```

The public vocabulary follows robotics:

- `Robot`, `Arm`, `Gripper`, `Camera`, and `Base`;
- `Pose`, `Joints`, and small useful result values;
- `Segmenter`, `PoseEstimator`, `Tracker`, and `LocalAlignment`;
- `GraspGenerator`, `ObjectAsset`, and grasp anchors.

Do not insert runtime sessions, providers, executors, resource graphs,
controllers-of-controllers, generalized capability negotiation, or a hidden
communications layer between those objects and their implementations.

## Backend selection and extension

Backend names map through small source-controlled mappings next to each
capability:

```python
SEGMENTERS = {
    "sam2": SAM2Segmenter,
    "tensorrt": TensorRTSegmenter,
    "yolo": YOLOSegmenter,
}
```

An implementation should live in the corresponding robotics folder, such as
`perception/segmentation/sam2.py`. Adding a normal Python backend should require
that file, one mapping entry, dependencies in the appropriate Docker image, and
focused tests. It should not require package entry points, manifests, lifecycle
hooks, generated catalogues, or a dependency-injection system.

Capability objects are preferred to one-shot generic runners because they keep
models and GPU resources loaded and naturally own algorithm state:

```python
tracker = dfl.perception.Tracker(backend="m3t", object=tray)
tracker.initialize(rgb, depth, object_pose)
object_pose = tracker.update(rgb, depth)
```

For users who think in folder/file terms, a capability folder may expose a
small `create(backend="sam2.py", ...)` alias. The optional `.py` suffix is
normalized to the same explicit mapping; it is not dynamic code execution.

Use meaningful Python parameters such as `rgb=`, `depth=`, `mask=`, `mesh=`,
and `object=` in the shared API. A backend may expose its own specialized method
or accept unusual/raw inputs where necessary. Do not force all algorithms
through an opaque `input=[...]` list merely for superficial uniformity.

ROS nodes and external processes remain valid where the underlying technology
requires them. Their capability object should be a thin, inspectable adapter,
and the developer must still be able to use normal ROS tools to diagnose it.

## Robots and modes

`Robot(model=..., mode=..., gripper=..., scene=...)` is a convenience factory,
not a hidden runtime. It selects a concrete backend and exposes the platform's
real composition:

```python
robot.arm.move_pose(...)
robot.base.navigate_to(...)
robot.gripper.open()
rgb, depth = robot.camera.get_rgbd()
```

Picker 1 and Picker 2 remain separate, namespaced composite profiles even
though both use M1013 arms. H2515 remains a separate robot. Each of the four
tool profiles remains explicit. Lower-level implementations must remain directly
importable for debugging.

Shared behaviors use shared method names across `real`, `gazebo`, and
`genesis`. Backend-specific operations are allowed. Unsupported behavior must
fail clearly with the selected robot, tool, mode, and missing operation; do not
silently simulate success, negotiate through a framework, or apply an unrelated
fallback.

`Robot.bringup()` may own a normal ROS launch process and clean up only what it
started. Explicit attach mode may be supported. It must not depend on an
ObjectDB server, task lease service, run daemon, or Compose control plane.

## Lightweight values and configuration

`Pose` and `Joints` are lightweight values. Runtime geometry uses metres and
radians, poses carry explicit frames, and conveniences such as
`pose.offset(z=0.10)` remove repetitive transform code. ROS conversions live at
ROS-facing seams so importing values does not require a running ROS graph.

Task-specific choices remain visible in the task. Small validated files are
appropriate for shared hardware facts, calibrations, limits, network endpoints,
MoveIt settings, large model settings, and scene geometry. Each adapter owns a
short, deterministic resolution order; there is no project-wide configuration
framework whose main effect is hiding parameters from task code.

Results carry information tasks actually use. Expected failures raise clear,
specific errors that say which assumption failed and how to correct it. Add
shared result fields or error categories only after real consumers repeat them.

## Perception, alignment, and grasping

Perception remains backend-swappable at the capability level. SAM2, TensorRT,
YOLO, FoundationPose, M3T, and experimental methods remain independently
replaceable. Local alignment is another explicit capability. Fixed object
anchors, geometric grasping, learned grasping, and custom methods coexist.

Task scripts keep the robotics stages visible. High-level helpers may be added
for repeated patterns, but they must be built from and allow access to the same
small primitives. No opaque `robot.pick()` should hide perception, planning,
force control, retry, and recovery during research.

## ObjectDB and scanning

Runtime object assets are normal files:

```text
objects/
  small_tray/
    object.json
    mesh.glb
    grasps.json
    models/
    references/
```

`dfl.objectdb.load("small_tray")` reads locally and returns an object asset
containing mesh paths, dimensions, reference frames, model references,
annotations, and object-frame grasp anchors as available. Loading a list is a
small convenience. Grasp anchors transform locally from the object's estimated
pose; the task does not call a runtime ObjectDB service for data already loaded.

ObjectDB remains a substantial companion authoring tool. The scanning,
multi-view capture, reconstruction, quality review, revision registration,
viewer, validated editor, grasp annotation, and grasp-test packets all remain.
They can use Dockerized services where reconstruction or UI dependencies require
them. The authoring application writes the same file-first format consumed by
tasks and may use revision history, indexing, locking, or Git backup within its
own boundary when those solve authoring problems.

ObjectDB does not become a runtime control plane. An already-authored task does
not need an ObjectDB server, lease, Git transaction, sync sidecar, or network
resolution step to start. The MoveIt planning scene is owned by the robot/motion
side and is updated explicitly from loaded assets and current perception.

## Safety, testing, and evidence

Architectural simplicity does not remove safety or evidence. Safety logic stays
at the robot, controller, vendor, gateway, and physical-hardware seams. Unknown
or partial execution stops; no automatic motion resume follows loss of control,
perception, TF, time, or network trust.

Testing is proportional to the layer:

- pure-value, file-loading, and transform unit tests;
- recorded RGB-D fixtures and measurable perception/alignment benchmarks;
- simulator tests across the declared robot/tool/mode matrix;
- supervised commissioning and real-hardware qualification for installed
  combinations;
- run artifacts, bags, images, and metrics where they materially improve
  diagnosis and comparison.

Qualification packet thresholds remain explicit, but they qualify a named
backend, matrix, or release; they are not infrastructure every five-minute
experiment must understand.

## Phase-order rule

The eight phases and their individual work packets remain the source of work:

0. Docker foundation, robot profiles, Gazebo, Genesis, and simulator matrix;
1. small shared values, ROS seams, configuration, direct backend maps, task
   conventions, and useful run evidence;
2. manipulation for all declared robots, tools, base behavior, and concurrency;
3. file-first object assets, migration, grasps, and planning-scene use;
4. perception, pose estimation, tracking, reseeding, and benchmarks;
5. alignment, visual servo, grasp verification, retry, and acceptance;
6. the Dockerized ObjectDB scanning and authoring companion;
7. gateways, desktop Compose, recovery, commissioning, parity, qualification,
   documentation, upgrades, and release.

Within and across phases, implement representative vertical slices early so
interfaces are tested by actual tasks. Then complete the remaining declared
matrix and packets. Do not freeze theoretical universal contracts before a
concrete backend exercises them, and do not delete a required capability merely
because it is scheduled later.

## Complexity rule

Before adding architecture, ask in order:

1. Can ordinary task Python express it?
2. Can an existing ROS or vendor mechanism express it?
3. Can one small helper, adapter, or mapping remove the repetition?
4. Do concrete implementations prove that another seam is necessary?
5. What exact task-script or debugging problem pays for the new concept?

Prefer concrete implementation first, a small abstraction second, and a
framework only when repeated real robotics work forces it.
