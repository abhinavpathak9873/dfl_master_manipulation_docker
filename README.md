# DFL Robotics Toolbox

A small internal toolbox for writing robotics experiments as readable Python
task scripts.

The architectural baseline is [`toolbox_plan.md`](toolbox_plan.md), and the
canonical target script is [`example_api.txt`](example_api.txt).

## Current status

The repository currently contains the dependency-free foundation:

- validated `Pose` and `Joints` values;
- a simple robot adapter mapping and composite `Robot` facade;
- explicit perception/grasping capability facades backed by small mappings;
- local file-first ObjectDB loading;
- local grasp-anchor transforms;
- focused unit tests.

Picker 1, ROS, Gazebo, and model integrations are the next vertical slice. The
factory intentionally reports them as unavailable until their real adapter files
exist; it does not pretend the integration is complete.

## Develop

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
```

Experiments belong in `tasks/` and normally run directly:

```bash
python tasks/small_tray_pick.py
```

## Add a backend

Put the implementation in the matching robotics folder and add it to the nearby
mapping. For a segmenter:

```text
dfl_toolbox/perception/segmentation/my_model.py
dfl_toolbox/perception/segmentation/__init__.py
tests/perception/test_my_model.py
```

The task-facing call remains:

```python
segmenter = dfl.perception.segmentation.create(
    backend="my_model.py",
    model="models/my_model.engine",
)
mask = segmenter.segment(rgb)
```

Backend names work with or without the `.py` suffix. The selected script is
constructed once and can keep its model/GPU state across task loops. There is no
plugin manifest or discovery service.

## Object assets

`dfl.objectdb.load("small_tray")` searches an explicit `root`, then
`DFL_OBJECTS_ROOT`, then `./objects`. See
[`plans/work_packets/02_object_assets.md`](plans/work_packets/02_object_assets.md)
for the initial `object.json` shape.

ObjectDB authoring tools may create these files, but ObjectDB never needs to run
for a task to load them.
