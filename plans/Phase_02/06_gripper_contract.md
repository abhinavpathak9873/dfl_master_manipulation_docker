# Shared gripper contract

## Goal

Give vacuum and parallel grippers one capability-based task interface without erasing the state and parameters that differ between tools.

## Inputs

- Tool profiles
- Typed values/errors
- Simulator tool-state contract
- Existing suction and 2FG14 behavior

## Outputs

- Gripper plugin base contract
- Capabilities and status model
- Task methods `open`, `close`, `grip`, `release`, `status`, and `stop`
- Command/result and timeout policy
- Shared simulator/hardware contract tests
- Tool-identity preflight

## Work

1. Define capabilities for vacuum channels, target vacuum, width control, force control, speed control, object detection, internal/external grip, and measured state.
2. Make unsupported capability use an explicit error; do not approximate width control with a binary suction command.
3. Bind each driver instance to the active robot/tool profile and verified tool identity. Include tool and driver IDs in every command result.
4. Define command lifecycle: accepted, moving/evacuating, achieved, object detected, released, timeout, fault, stopped, and connection lost.
5. Provide safe stop behavior for each capability. Release is a separate task decision and is never implied by generic stop.
6. Normalize width to metres and force to newtons in the public API while allowing profile files to show human-friendly units with schema conversion.
7. Create shared tests for readiness, open/release, grip/close, state, timeout, cancellation, object detection, disconnect, and repeatability.

## Interfaces and data

- Python `Gripper` facade
- Plugin methods and capabilities
- Typed `GripperStatus` and result
- ROS/service/vendor adapter boundary

## Boundaries

- Does not select grasp anchors
- Does not decide when task recovery should release an object
- Does not hide driver-specific diagnostics

## Failure behavior

- Reject wrong tool identity, unsupported capability, out-of-range command, stale status, connection loss, command timeout, and failed object detection.
- A failed grip never reports success because the actuator reached its requested position or vacuum target without object evidence.

## Acceptance

- One shared test suite runs against all four profiles and both simulators.
- Task code can query capabilities before using optional parameters.
- Results distinguish command achieved from object held.
- Stop and disconnect tests leave a declared state.
- Profiles contain driver, geometry, TCP, limits, and qualification status.

## Parallel work

Tool-specific packets run in parallel after this contract freezes.

## What this module needs from me

Nothing.
