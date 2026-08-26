# Canonical task-script API

This is planning pseudocode with valid Python shape. It defines the intended developer experience; no backend implementation has started.

```python
import dfl_toolbox as dfl


robot = dfl.Robot(
    model="picker1",
    mode="gazebo",
    gripper="vgc10_1cup",
    scene="empty",
)

home = dfl.Joints(
    -1.550293,
    0.366800,
    -1.943505,
    2.006920,
    1.588168,
    0.006650,
    unit="rad",
)

place_pose = dfl.Pose(
    0.303571,
    -0.059250,
    0.737991,
    q=[0.015896, 0.003527, 0.000954, 0.999867],
    frame="odom",
)

tray = dfl.objectdb.load("small_tray")

segmenter = dfl.perception.segmentation.create(
    backend="tensorrt.py",
    model=tray.models.segmentation,
)

pose_estimator = dfl.perception.pose.create(
    backend="foundation_pose.py",
    object=tray,
)

tracker = dfl.perception.tracking.create(
    backend="m3t.py",
    object=tray,
)

aligner = dfl.perception.alignment.create(
    backend="reference_depth.py",
)

robot.bringup()

try:
    robot.gripper.open()
    robot.arm.move_joints(home)

    rgb, depth = robot.camera.get_rgbd()
    mask = segmenter.segment(rgb)
    object_pose = pose_estimator.estimate(
        rgb=rgb,
        depth=depth,
        mask=mask,
    )
    tracker.initialize(
        rgb=rgb,
        depth=depth,
        pose=object_pose,
    )

    grasp = tray.grasp_anchors.transform(object_pose)[0]
    robot.arm.move_pose(grasp.offset(z=0.10))

    correction = aligner.compute(
        camera=robot.camera,
        object=tray,
        initial_pose=object_pose,
    )
    robot.arm.apply_cartesian_offset(correction)
    robot.arm.descend(0.10, stop_on_force=15.0)

    close_result = robot.gripper.close(
        force=40,
        expected_width=0.035,
    )
    while not close_result.success:
        robot.arm.ascend(0.02)
        robot.arm.descend(0.02, stop_on_force=15.0)
        close_result = robot.gripper.close(
            force=40,
            expected_width=0.035,
        )

    robot.arm.ascend(0.10)
    robot.arm.move_pose(place_pose)
    robot.gripper.open()
finally:
    robot.bringdown()
```

## Required selector scope

The same constructor shape covers all planned robot/tool choices:

```python
picker1 = dfl.Robot(model="picker1", mode="real", gripper="vgc10_1cup")
picker2 = dfl.Robot(model="picker2", mode="gazebo", gripper="vgc10_4cup")
h2515 = dfl.Robot(model="h2515", mode="genesis", gripper="vgp20")
parallel = dfl.Robot(model="picker1", mode="gazebo", gripper="2fg14")
```

Picker 1 and Picker 2 both contain M1013 arms and mobile bases but remain
separate namespaced composite robots. H2515 remains a separate arm profile.
The complete gripper set is VGC10 one cup, VGC10 four cups, VGP20, and 2FG14.

## Backend-construction spelling

The folder-shaped construction above is retained because it mirrors where a
developer looks for an implementation. The shorter capability spelling is also
valid and resolves through the same small mapping:

```python
segmenter = dfl.perception.Segmenter(
    backend="tensorrt",
    model=tray.models.segmentation,
)
```

`backend="sam2.py"` and `backend="sam2"` select the same mapped backend; the
`.py` suffix never executes an arbitrary file path. The backend object is
constructed once so models and tracker state stay loaded.

Shared examples use named inputs such as `rgb=`, `depth=`, `mask=`, and
`object=` because they remain readable when algorithms need different data. A
specialized backend may still expose its own method or accept a raw/list input
when that is genuinely the clearest interface.

## API design test

Every phase must check its decisions against this file. The task should stay a
readable Python sequence; ROS nodes, Docker services, and ObjectDB authoring
processes exist only underneath a concrete dependency or hardware boundary.
No implementation is created by this document.
