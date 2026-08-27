# Phase 00 simulator ROS behavior

Phase 00 shares a small ROS surface between Gazebo and Genesis. It is an
observable compatibility seam, not a simulator framework.

| Behavior | ROS surface | Gazebo | Genesis | Limitation |
| --- | --- | --- | --- | --- |
| Arm command | `/<robot>/dsr_position_controller/follow_joint_trajectory` | Adapter over the vendor position controller | Direct bridge action server | Six ordered Doosan joints only |
| Relative TCP probe | 20 mm along the current `tool_tcp` Z axis, converted to the shared arm action | Numerical position IK over the expanded vendor chain; measured TCP must finish within 4 mm | Same task and gate | Position-only Phase 00 check; full pose planning belongs to the later motion API |
| Arm state | `/<robot>/joint_states` | ros2_control broadcaster | Physics bridge | Position and velocity; effort is not claimed |
| Readiness | `/<robot>/ready` | Simulator I/O node | Bridge and simulator I/O node | Means ROS paths are live, not hardware commissioned |
| Tool command/state | `/<robot>/tool/command`, `tool/state` using `std_msgs/String` JSON | Command echo | Command echo | No seal, force, or object-retention inference |
| Picker base | `cmd_vel`, `odom` | Bounded planar proxy | Bounded planar proxy | State-path test only; no navigation or whole-body planning |
| Picker RGB-D | `camera/color/image_raw`, `camera/depth/image_rect_raw`, camera info | Deterministic calibration target | Genesis renderer | Both paths prove message/timestamp behavior, not D455 photometric parity |
| Frames | namespaced `tf` and `tf_static` | robot_state_publisher | robot_state_publisher | Frame names repeat inside isolated robot namespaces |
| Time | `/clock` and `use_sim_time` | Gazebo | Bridge | Consumers must reject stale messages |
| Cancel/stop | action cancel plus final hold; zero base velocity; tool `stop` | Explicit | Explicit | Emergency-stop equivalence is not claimed |

## Direct inspection

```bash
ros2 action info /picker1/dsr_position_controller/follow_joint_trajectory
ros2 topic echo /picker1/joint_states --once
ros2 topic echo /picker1/tool/state --once
ros2 topic hz /picker1/camera/color/image_raw
ros2 topic echo /picker1/odom --once
ros2 topic echo /clock --once
ros2 node list
```

Gazebo keeps the upstream `gz_ros2_control` system and
`dsr_position_controller`. `dfl-trajectory-adapter` only translates the shared
trajectory action into that controller's position array and verifies measured
joint convergence. Genesis owns its physics command loop directly. The fixed
task computes its relative target and numerical position IK from the selected
expanded URDF, then recomputes TCP position from measured joint state; action
success alone cannot satisfy the relative-motion gate.

The Genesis bridge preserves the full Doosan and DFL Picker visual meshes,
joint geometry, inertials, frames, and tool primitives. Genesis 1.3.3's legacy
URDF parser is unreliable for named elements in some collision DAE files, so
the bridge converts only DAE collision meshes to content-addressed cached STL;
Genesis then decimates and convexifies those collision assets. Base and tool
collision boundaries remain the declared conservative primitives. Genesis
contact, clearance, or force results are therefore not qualification evidence
in Phase 00.

Gazebo resolves project mesh URIs through the package-share roots declared in
`GZ_SIM_RESOURCE_PATH`. The gallery capture caught and fixed a prior state in
which Gazebo silently omitted the DFL Picker base and hand-camera meshes while
the ROS task still passed. Visual acceptance is therefore a separate gate from
the 24-case behavior matrix.

The hand-camera plate is part of the source mounting chain for Picker VGC10
four-cup and 2FG14 selections. It is absent from Picker VGC10 one-cup and VGP20
selections, and from H2515 selections. The 2FG14 shape is a dimension-derived
visual model with static nominal jaws, not vendor CAD. See
[`simulation_fidelity.md`](simulation_fidelity.md) for the complete transfer
boundary.
