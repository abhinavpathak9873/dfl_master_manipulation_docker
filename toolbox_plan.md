# DFL robotics toolbox: accepted direction

Status: accepted design baseline

Revised: 2026-08-27

## Product

This repository builds a small internal robotics toolbox. Its product is the
Python task script a robotics developer reads, edits, and runs.

The primary test for a design decision is:

> Does it make a representative robotics task easier to write, change,
> understand, or debug?

The toolbox is not a deployment platform, orchestration runtime, workflow
engine, generalized plugin system, or mandatory ObjectDB service.

## Target experience

The canonical task is [`example_api.txt`](example_api.txt). It deliberately
uses ordinary Python:

- constructors select a robot or algorithm;
- robotics stages are visible in top-to-bottom order;
- loops and branches express retries and recovery;
- composite robots expose `arm`, `base`, `gripper`, and `camera`;
- a developer can replace one backend without rewriting unrelated stages;
- lower-level backend objects and ROS interfaces remain reachable.

Running a task should normally be:

```bash
python tasks/small_tray_pick.py
```

A ROS package or launch wrapper is allowed when the task genuinely needs to be
a ROS executable. It is not the default shape of every experiment.

## Architecture

The ordinary debugging path is:

```text
task script
  -> robotics capability object
  -> named backend implementation file
  -> ROS / MoveIt / model / vendor API
```

Each capability is a deep module only where it removes real integration work.
The public seam uses robotics vocabulary:

- `Robot`, `Arm`, `Gripper`, `Camera`, and `Base`;
- `Pose` and `Joints`;
- `Segmenter`, `PoseEstimator`, `Tracker`, and
  `LocalAlignment`;
- `ObjectAsset` and grasp anchors.

Do not insert runtime sessions, providers, executors, resource graphs, or
controllers-of-controllers between these objects and their implementations.

## Backend selection

Backend names map through small source-controlled dictionaries near their
capability:

```python
SEGMENTERS = {
    "sam2": SAM2Segmenter,
    "tensorrt": TensorRTSegmenter,
}
```

The implementation lives in the matching robotics folder, such as
`dfl_toolbox/perception/segmentation/sam2.py`. Adding a normal Python backend
means adding that file, adding one mapping entry, and adding focused tests.
There are no entry points, manifests, lifecycle hooks, qualification registries,
or dynamic package discovery in the baseline.

For script-like navigation, each capability folder exposes `create`:

```python
segmenter = dfl.perception.segmentation.create(
    backend="sam2.py",
    model="weights/sam2.pt",
)
mask = segmenter.segment(image=rgb, prompt=prompt)
```

The optional `.py` suffix is accepted and normalized to the mapping key
`"sam2"`. The backend is still constructed once, so models and GPU resources
remain loaded across loop iterations. Inputs use positional or named Python
arguments appropriate to the robotics operation. Shared examples prefer names
such as `rgb=`, `depth=`, and `mask=` over `input=[...]`; a backend may
still expose a raw or unusual call directly through `segmenter.implementation`.

Cross-process implementations may use ROS nodes because the algorithm or vendor
stack requires them. The Python object remains a thin, inspectable adapter to
those ROS interfaces. Standard ROS messages are preferred. A custom interface is
added only when a concrete cross-process exchange cannot be expressed clearly
with an existing type.

## Robot selection

`Robot(model=..., mode=..., gripper=..., scene=...)` is a convenience
constructor. It chooses a concrete robot adapter and exposes the robot's real
structure. The same adapter remains directly importable for debugging.

Shared simulation and real behavior should share method names. A backend may
also expose honest backend-specific operations. Unsupported behavior raises a
clear error naming the robot, mode, and missing capability; the toolbox does not
negotiate or silently fall back.

`Robot.bringup()` may own a ROS launch process when useful. It does not require
ObjectDB, a task lease server, a run daemon, or a Compose control plane. Attach
to an already-running ROS graph may be added to an individual robot adapter if
that is a real workflow.

## Values

`Pose` and `Joints` are lightweight, dependency-free values. Runtime geometry
uses metres and radians. Poses carry an explicit frame. Convenience operations
such as `pose.offset(z=0.10)` are welcome when they remove repeated transform
code. ROS conversions belong in ROS-facing adapter modules so importing the
values does not require ROS.

Results carry only information task code uses. For example a gripper close can
return `success`, `final_width`, `force`, and backend details. Avoid a global
result envelope or exhaustive error-code ontology until repeated consumers need
one.

## Configuration

Task choices and experimental parameters remain visible in the task script.
Small files may hold shared hardware facts, calibration, network endpoints,
MoveIt settings, or large backend configuration. Resolution should be a direct
and documented merge owned by the specific adapter, not a project-wide
nine-layer configuration system.

## ObjectDB

Runtime object assets are ordinary files:

```text
objects/
  small_tray/
    object.json
    mesh.glb
    grasps.json        # optional; may also be embedded in object.json
    models/
```

`dfl.objectdb.load("small_tray")` reads these files locally and returns an
`ObjectAsset` with paths, models, metadata, and object-frame grasp anchors.
Loading an object never requires a server or an active ObjectDB process.
`load(["small_tray", "white_box"])` is the corresponding small convenience
for multi-object experiments.

ObjectDB is a companion authoring tool for scanning, reconstruction, review, and
annotation. It writes the same file format the toolbox reads. A viewer, CLI, or
local app may be added as authoring needs become concrete, but it is not part of
task startup and does not own task leases, robot control, Git synchronization,
or the runtime planning scene.

## Reliability

Reliability comes from small modules, explicit state, clear ownership, safe
stops in hardware adapters, good errors, focused fixtures, and visible task
logic.

Instrumentation is proportional:

- unit tests for pure values and file loading;
- recorded fixtures for perception;
- simulator tests for motion and tool adapters;
- supervised hardware checks for real adapters;
- optional run artifacts when they help diagnose a task.

The baseline does not require every successful experiment to produce a release
manifest, event stream, ring buffer, lease record, Git commit, or two-hour
qualification run.

## Initial vertical slice

Build in task order, not infrastructure layers:

1. lightweight values, backend selection, and file-first object loading;
2. Picker 1 in Gazebo with one actually used gripper and camera;
3. the concrete segmentation and coarse-pose backends needed by the tray task;
4. grasp-anchor transformation, local alignment, approach, descend, grip, lift,
   and place;
5. the corresponding real Picker 1 adapter and safety checks;
6. the next robot, tool, simulator, or perception backend only when a named task
   asks for it.

The detailed packets are in [`plans/overview.md`](plans/overview.md). The
disposition of every superseded packet is in [`plans/audit.md`](plans/audit.md).

## Complexity rule

Before adding architecture, ask in order:

1. Can ordinary task Python express it?
2. Can the existing ROS or vendor mechanism express it?
3. Can one small helper or mapping remove the repetition?
4. Do two real implementations prove that a new seam exists?

Complexity is accepted only with a concrete task, observed problem, and a
smaller alternative that has already proved inadequate.
