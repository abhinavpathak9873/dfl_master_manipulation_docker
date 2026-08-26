# ROS interface package

## Goal

Define the smallest custom IDL set needed across processes while using standard ROS messages for geometry, images, trajectories, detections, odometry, and velocity.

## Inputs

- Accepted Python values and error codes
- Simulator wire contract
- Object, perception, alignment, scanning, and health consumers

## Outputs

- `dfl_manipulation_interfaces` package
- Interface inventory documenting each standard and custom type choice
- Custom messages for `ObjectRevisionRef`, `GraspAnchor`, `TrackedObject`, `TrackedObjectArray`, and `ImplementationHealth`
- Services for object resolution, revision commit/activation, and runtime lease acquisition, heartbeat, release, and inspection
- Actions for local grasp alignment, object scanning, and isolated reconstruction
- Generated Python/C++ tests and compatibility rules

## Work

1. Map arm execution to `control_msgs/action/FollowJointTrajectory`, motion data to standard geometry/trajectory messages, cameras to `sensor_msgs`, scene detections to `vision_msgs`, bases to `geometry_msgs/TwistStamped` and `nav_msgs/Odometry`, and diagnostics to `diagnostic_msgs`.
2. Define `ObjectRevisionRef` with stable object ID, immutable revision ID, mesh content hash, and canonical frame.
3. Define `TrackedObject` with revision reference, pose, covariance when available, observation timestamp, source frame, health enum, age, implementation ID, and source result reference.
4. Define `GraspAnchor` with stable anchor ID, gripper profile ID, pose in the object canonical frame, approach/retreat vectors, allowed orientation metadata, and profile revision.
5. Define a common result detail carrying stable error code, message, implementation ID, stage, and run artifact reference. Reuse it in custom service/action results.
6. Define object resolution as object ID plus optional revision, returning the exact immutable revision, Git commit, content hashes, canonical frame, qualification state, and relative asset references.
7. Define a runtime lease identity with lease ID, epoch, owner kind, run/session ID, robot, mode, configuration hash, heartbeat timestamp, and terminal state. Missing heartbeat never authorizes automatic release.
8. Define `ScanObject` around scan profile, provisional object identity, session/lease IDs, state revision, feedback stage, next operator action, and typed result. Keep images and meshes out of the action payload.
9. Define the internal reconstruction action around scan session ID, immutable input-manifest path/hash, pipeline ID/version, requested starting stage, progress, output-manifest path/hash, qualification state, and typed failure.
10. Keep large masks, images, meshes, and point clouds on standard topics or content-addressed storage; custom messages carry references and identity.
11. Set an interface versioning policy: additive compatible fields require default-safe semantics; breaking changes require a major contract update and consumer migration.

## Interfaces and data

- ROS 2 IDL in `dfl_manipulation_interfaces`
- Standard messages/actions listed in the inventory
- Type-support generation for Python and C++

## Boundaries

- Does not implement servers or clients
- Does not duplicate FoundationPose tensor output unless a consumer requires it
- Does not embed JSON blobs as the primary typed interface
- Does not put raw scan data or reconstruction artifacts on ROS service/action payloads

## Failure behavior

- IDL build fails on undocumented fields, duplicated standard semantics, unbounded large payloads, or error results without stable codes.
- Consumers reject unsupported major contract versions.

## Acceptance

- Package builds alone and in the full workspace.
- Python and C++ round-trip fixtures agree.
- QoS and field semantics are documented for every topic/service/action.
- All Phase 02–06 consumers map to a declared interface.
- Lease epoch, stale-owner, action cancel, worker restart, and manifest-hash fixtures round-trip in Python and C++.
- Removing any custom type would lose a named required semantic.

## Parallel work

Begins after value vocabulary stabilizes. Implementation packets can design internally but cannot publish before this package freezes.

## What this module needs from me

Nothing.
