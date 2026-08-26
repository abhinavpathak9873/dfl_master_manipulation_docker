# Python values, results, and failure taxonomy

## Goal

Define the implementation-neutral Python objects returned to task code and the typed failures used for expected operational problems.

## Inputs

- Simulator contract
- Object/perception/grasp requirements from the master plan
- Existing `Pose`, `Joints`, motion result, and gripper behavior

## Outputs

- Public Python value module
- Immutable `Pose`, `Joints`, `MotionPlan`, `MotionResult`, `TrackedObject`, `SceneSnapshot`, `ObjectRevisionRef`, `GraspAnchor`, `GripperStatus`, and `RunRef` types
- Exception hierarchy and stable error-code enumeration
- ROS conversion helpers and unit tests
- API documentation with minimal examples

## Work

1. Keep geometry in SI units and radians. Every pose carries a non-empty frame and source timestamp when derived from sensors.
2. Represent joints by ordered names plus values; reject ambiguous positional lists when the active robot order is not supplied.
3. Make plans immutable and bind them to robot ID, start-state hash, planner ID, creation time, target, and validity conditions.
4. Make motion results record plan ID, selected attempt, controller result, actual endpoint, timing, and artifact reference.
5. Define failure families for configuration, readiness, planning, execution, cancellation, control loss, stale data, perception, alignment, gripper, object data, and simulator contract errors.
6. Give every operational error a stable machine code, concise human message, stage, implementation ID, robot ID, and nested ROS/vendor detail.
7. Provide strict conversions to and from standard ROS messages without silently selecting frames, units, quaternion order, or current time.

## Interfaces and data

- Python public imports from `dfl_manipulation_toolbox`
- Conversion to `geometry_msgs/PoseStamped`, `sensor_msgs/JointState`, `vision_msgs/Detection3D`, and trajectory/action results
- Error codes reused by custom ROS results and run events

## Boundaries

- Does not start ROS nodes
- Does not contain plugin-specific payloads beyond a namespaced diagnostics map
- Does not decide stored ObjectDB JSON fields

## Failure behavior

- Constructors reject NaN/Inf, zero quaternion, missing frame, duplicate joints, unknown units, and inconsistent timestamps.
- Conversion failure is explicit; no latest TF or default-frame fallback.

## Acceptance

- Round-trip conversions preserve values, frames, timestamps, names, and error codes.
- Hash/equality behavior is deterministic.
- Plans cannot be mutated after preview.
- Every expected failure named in the global decision record maps to one exception and code.
- Public examples contain no implementation dictionary.

## Parallel work

Config and namespace contracts may develop in parallel. ROS IDL follows the stable field vocabulary.

## What this module needs from me

Nothing.
