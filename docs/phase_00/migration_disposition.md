# Legacy source disposition

Phase 00 imports two clean, pinned upstream repositories through
`dependencies.repos`: Doosan Robotics Jazzy at
`816ecb5d1c2599303eaf9540216afa03552f80ad` and `moveit2_calibration` at
`0263c8c8aa8f1b548bf152969900d74b3fbf9a75`.

The old Humble workspace packages were inspected but not copied. Their local
license and provenance were not sufficient for wholesale import, and the
Doosan Jazzy repository already owns the arm descriptions, ros2_control
systems, Gazebo launch path, controller configuration, and MoveIt packages.
Phase 00 reuses those upstream packages and keeps project-specific profiles,
tool collision primitives, launch glue, and simulator adapters in two new ROS
packages.

Legacy Picker descriptions remain reference material for later characterization.
No legacy package is presented as Jazzy-compatible merely because its files can
be copied into the workspace.
