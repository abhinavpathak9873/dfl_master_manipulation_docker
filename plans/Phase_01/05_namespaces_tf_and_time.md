# Namespaces, TF, units, and time

## Goal

Eliminate cross-robot collisions and stale transforms by defining one naming and timestamp contract for real, Gazebo, and Genesis modes.

## Inputs

- Robot profiles
- Simulator contract
- Existing picker frames and `/dsr01` conflicts
- ROS REP-103 conventions

## Outputs

- Namespace and topic map
- Frame tree specification for each robot class
- Clock-source and timestamp rules
- QoS defaults by data class
- TF and time preflight checks
- Dual-robot contract tests

## Work

1. Place every robot-owned node, action, service, topic, diagnostic key, and controller manager under `/<robot_id>`.
2. Prefix robot-owned TF frames with the robot ID. Picker roots are `<id>/base_footprint`; arm planning starts at `<id>/manipulator_base_link`. H2515 uses a profile-declared fixed root.
3. Standardize tool frames at `<id>/end_effector_mount_link`, profile-specific TCP, and payload tip. Camera optical frames remain REP-103 compliant under the robot prefix.
4. Use SI metres, seconds, radians, newtons, and pascals in runtime contracts. Human-facing millimetre helpers convert explicitly at API boundaries.
5. Use ROS time for stamped data. Simulators publish `/clock`; real systems use synchronized system clocks. Record clock source in every run.
6. For perception-to-motion decisions, require transforms at the observation timestamp. Latest-transform fallback is prohibited. Configure finite lookup and maximum-age bounds.
7. Define QoS: sensor data uses bounded best-effort where appropriate; commands/actions and state needed for safety use reliable profiles; latched static metadata uses transient local.

## Interfaces and data

- Namespace expansion utility
- TF frame IDs in profiles and typed values
- Time/freshness validator
- QoS profile names used by launch and adapters

## Boundaries

- Does not provide map navigation
- Does not introduce a global unprefixed `base_link` alias for concurrent runs
- Does not set clock-sync software policy beyond required health

## Failure behavior

- Preflight fails on duplicate node/controller names, disconnected TF trees, missing optical transforms, clock going backward, excessive skew, or stale required data.
- Motion requests reject poses without a source frame and observation timestamp.

## Acceptance

- Picker 1 and Picker 2 publish complete independent TF trees.
- No arm action, joint-state topic, diagnostic name, or frame collides.
- Recorded images resolve camera-to-robot transforms at their timestamps.
- Sim reset preserves monotonic run-relative time or begins a new run identity.
- QoS tests cover reconnect and late joiners.

## Parallel work

Config and Python types proceed together. ROS IDL and runtime modules consume the frozen names.

## What this module needs from me

Facts: measured network clock skew and selected clock-sync service are collected in Phase 07.
