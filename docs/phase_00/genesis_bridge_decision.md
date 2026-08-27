# Genesis bridge decision

Decision: use a direct Genesis ROS bridge for Phase 00.

The official Doosan emulator cannot remain authoritative without a hardware
adapter that exchanges every emulator command/state cycle with Genesis. The
upstream Jazzy stack exposes either DRFL-backed ros2_control hardware or a
Gazebo-specific `gz_ros2_control` system; neither provides a physics-neutral
external hardware protocol. Putting the emulator in the loop would therefore
require a new control plugin and would be larger—and harder to inspect—than the
bridge being tested.

The direct bridge retains the task-visible behavior needed by Phase 00:
`FollowJointTrajectory`, measured joint state, cancellation with hold, `/clock`,
namespaced TF through robot_state_publisher, rendered Picker RGB-D, tool command
state, and explicit readiness. It loads the same expanded M1013/H2515 and tool
URDF used for description checks. The implementation is confined to
`dfl_genesis_integration`; task code does not import Genesis.

Genesis 1.3.3's legacy URDF loader cannot decode the upstream Doosan DAE meshes.
Passing them to its convexifier stalled construction for more than two minutes.
The bridge therefore replaces only mesh-backed visual and collision elements in
its temporary URDF with bounded box proxies. Joint origins, limits, inertials,
fixed mounts, tool primitives, TCP, and ROS frames still come from the expanded
vendor/project description. Gazebo and MoveIt retain the original meshes. This
is sufficient for Phase 00 articulation and ROS-path proof, but not for Genesis
collision-fidelity claims.

This decision does not claim vendor-control equivalence. Doosan safety logic,
DRFL services, torque/force sensing, real tool I/O, and emulator-specific state
remain unavailable in Genesis. The fixed matrix checks the shared subset and
records these differences rather than inventing feedback.

The official emulator remains available as the pinned `doosan-emulator`
Compose service for vendor-protocol diagnostics. It is not placed in either
simulator's authoritative joint loop: upstream exposes a controller protocol,
not the bidirectional per-step physics interface needed to keep simulated
contacts and emulator state consistent.

## Measured Phase 00 behavior

- All 12 Genesis robot/tool cases passed. Process-level case times were
  122.8–127.7 seconds on the recorded host; initialization dominates, while the
  ROS task itself completed in less than one second after readiness.
- A 200-step M1013/Picker sample sustained 128.1 updates per second. PyTorch
  reported 8.2 MiB allocated and 22.0 MiB reserved after the sample.
- Each matrix case starts from a fresh simulator process. Process restart is the
  Phase 00 reset boundary; no task-visible generalized reset service is claimed.
- Cancellation holds the measured articulation target. Tool feedback remains
  explicitly commanded rather than measured, and contact/force usefulness is
  not claimed with proxy geometry.
