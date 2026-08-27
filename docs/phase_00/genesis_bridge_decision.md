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

Genesis 1.3.3's legacy URDF parser reports decoder failures for named elements
inside some Doosan collision DAE files. Disabling convexification also makes
high-polygon collision preprocessing unacceptably slow. Neither issue requires
discarding the visual meshes: the full M1013 model builds in roughly five
seconds when visual geometry is retained and collision processing is bounded.

The bridge now keeps the original Doosan and DFL Picker visual assets. It
converts only DAE collision meshes to content-addressed STL files in the
Genesis cache, then asks Genesis to decimate and convexify those files. Joint
origins, limits, inertials, fixed mounts, TCP, and ROS frames still come from
the expanded description. Picker base/tool collisions remain conservative
primitives, so Phase 00 does not make contact- or clearance-fidelity claims.

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

- All 12 Genesis robot/tool cases passed joint motion and the measured 20 mm
  relative-TCP probe. Relative position errors were 1.31–3.68 mm against the
  4 mm gate.
- The first cold-cache measurements took 122.8–127.7 seconds per process. With
  generated kernels and collision conversions cached, the detailed-mesh matrix
  took 21.1–35.4 seconds per fresh simulator process on the recorded host.
- A 200-step M1013/Picker sample sustained 128.1 updates per second. PyTorch
  reported 8.2 MiB allocated and 22.0 MiB reserved after the sample.
- Each matrix case starts from a fresh simulator process. Process restart is the
  Phase 00 reset boundary; no task-visible generalized reset service is claimed.
- Cancellation holds the measured articulation target. Tool feedback remains
  explicitly commanded rather than measured, and contact/force usefulness is
  not claimed from simplified collision geometry.
- The direct bridge's position gains are set high enough to keep the heavier
  H2515 inside the shared TCP-position gate under simulated gravity. They are
  simulator control parameters, not real-robot tuning values.
