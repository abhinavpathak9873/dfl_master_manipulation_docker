# 03 — Picker 1 Gazebo vertical slice

## Outcome

One ordinary Python task constructs Picker 1 in Gazebo, calls `bringup()`,
opens the selected gripper, reads RGB-D, moves to joints and poses, makes a
relative Cartesian move, stops, and cleans up what it started.

## Concrete implementation

- Start from the pinned/verified Doosan Jazzy source and existing DFF motion
  behavior.
- Add `dfl_toolbox/robots/picker1.py` with an explicit
  `Picker1Gazebo` adapter and register `("picker1", "gazebo")`.
- Expose `robot.arm`, `robot.gripper`, `robot.camera`, and only expose
  `robot.base` if the selected simulated description genuinely supports it.
- Use standard ROS/MoveIt/controller interfaces directly.
- Keep ROS conversions, namespaces, TF freshness, QoS, launch ownership, and
  controller errors in this adapter or a small Picker/Doosan support module.
- Implement the one VGC10 profile used by the reference task. Add other tool
  files only with their own task.

## Preserve from existing DFF code

- measured start state;
- finite trajectory and joint-limit checks;
- cancellation and stop behavior;
- Cartesian direction/frame correctness;
- cleanup of launch processes owned by the adapter.

Reuse behavior and tests, not the old facade/config/process-registry topology.

## Acceptance

- `python tasks/picker1_smoke.py` runs from a clean Gazebo start.
- The script has no ROS launch graph, controller name, or vendor service detail.
- `ros2 node list`, topics, actions, TF, MoveIt, and Gazebo remain directly
  inspectable while it runs.
- Interrupting motion calls the adapter stop path and cleans only owned launch
  processes.
- An unsupported force-aware move raises a message naming Picker 1, Gazebo, and
  the missing operation.

## Stop condition

If the official Doosan Jazzy/Gazebo path cannot drive the selected robot,
capture the exact build/runtime evidence. Do not build a second control runtime
inside the toolbox.
