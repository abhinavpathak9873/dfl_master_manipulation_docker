# 04 — tray perception slice

## Outcome

The reference task obtains an RGB-D frame, segments the tray, estimates its
pose, and can initialize/update a tracker through ordinary stateful objects.

## Concrete implementation

- Choose the first segmenter from the actual available tray asset and runtime:
  TensorRT if the approved engine exists; otherwise the smallest working SAM2
  path.
- Implement it in
  `dfl_toolbox/perception/segmentation/<backend>.py` and add one mapping entry.
- Implement FoundationPose in
  `dfl_toolbox/perception/pose/foundation_pose.py`.
- Implement M3T only when the task uses tracking, in
  `dfl_toolbox/perception/tracking/m3t.py`.
- Keep model initialization in the object instance.
- Accept explicit keyword inputs such as `rgb`, `depth`, `mask`, and
  `object` in shared task examples. A backend whose natural call is genuinely
  list-shaped may still accept a list without changing the whole toolbox.
- Preserve access to raw ROS/model outputs and backend-specific debugging
  methods.

Heavy dependencies may run in a separate container or ROS process. That
deployment fact stays behind the relevant backend adapter and does not create a
toolbox-wide service framework.

## Evidence

- Record the smallest synchronized D455/Gazebo fixture that reproduces normal,
  missing depth, empty mask, stale timestamp, wrong mesh, and object-loss cases.
- Measure only the latency, accuracy, memory, and stability needed to judge this
  task.
- Never restamp a stale pose as current.

## Acceptance

- Switching one registered segmentation backend changes only its constructor.
- FoundationPose errors clearly when the object mesh is absent.
- Tracker state lives in the tracker instance and can be reset explicitly.
- The debugging path from each public method reaches one backend file and then
  the ROS/model implementation.
