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

The Genesis bridge preserves vendor joint geometry, inertials, frames, and the
project tool primitives, but substitutes boxes for upstream DAE mesh elements
because Genesis 1.3.3 cannot decode those assets. Use Gazebo/MoveIt for the
vendor collision meshes. Genesis contact, clearance, or force results are not
qualification evidence in Phase 00.
