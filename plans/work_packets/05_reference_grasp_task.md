# 05 — reference small-tray grasp task

## Outcome

The canonical task visibly performs home, perception, grasp selection, approach,
local alignment, contact-aware descend where supported, grip, explicit retry,
lift, transfer, release, and retreat in Gazebo.

## Work

- Turn [`example_api.txt`](../../example_api.txt) into
  `tasks/small_tray_pick.py` using the implemented robot/tool combination.
- Transform `tray.grasp_anchors` by the estimated object pose locally.
- Port the proven reference/mask/depth alignment behavior into
  `perception/alignment/reference_depth.py`.
- Keep `LocalAlignment.compute` pure with respect to robot motion; it returns
  a correction with the evidence the task needs.
- Implement `arm.apply_cartesian_offset`, `ascend`, and `descend` as small
  readable motion helpers over the existing arm methods.
- Return a useful gripper result. Put retry bounds and branches in the task.
- Save backend debug artifacts on request or failure where they materially help
  diagnosis.

## Safety behavior

- Freshness, TF, controller, and force/contact checks stay in their owning
  adapters.
- Any uncertain execution or lost control stops and raises a clear error.
- The task does not automatically return home after uncertain contact.
- A backend that cannot implement `stop_on_force` fails before pretending to
  provide it.

## Acceptance

- A robotics developer can explain the complete task by reading one Python file.
- No `pick()`, behavior tree, workflow manifest, retry engine, or hidden
  perception-to-grasp procedure is required.
- Changing the local alignment backend does not change motion/gripper stages.
- Nominal and injected failure fixtures identify the failing stage and backend.
- The task completes in the supported Gazebo robot/tool/object combination.
