# Motion planning and execution contract

## Goal

Expose readable combined motion methods plus separate immutable planning and execution. Make selected planners, attempts, start state, scene state, cancellation, and endpoint evidence visible.

## Inputs

- Python values and errors
- ROS FollowJointTrajectory contract
- MoveIt planning scene version
- Robot lifecycle
- Existing DFF arm API

## Outputs

- `Arm` API: `move_joint_to`, `move_to_pose`, `move_relative`, `plan_*`, `execute`, `stop`, and state queries
- Immutable motion request, plan, attempt, and result models
- Planner/control selection fields and fallback list
- Start-state and scene-version validation
- Cancellation and measured-endpoint policy
- Shared motion contract tests

## Work

1. Define explicit joint, pose, named-target, and relative-motion requests. Every request names robot, planning group, target, reference frame, velocity/acceleration scaling, timeout, primary planner, and optional fallbacks.
2. Plan against a captured joint-state timestamp and planning-scene version. Store start-state hash, selected IK branch or joint goal, trajectory, planner metadata, and validity deadline in the plan.
3. Implement combined methods as `plan` followed by the same public `execute`; do not maintain a separate hidden execution path.
4. Before execution, verify robot identity, controller readiness, current-state tolerance, plan age, scene version, and tool/attachment state. Reject rather than silently replan.
5. Map MoveIt and controller outcomes into stable planning, execution, cancellation, timeout, and endpoint error codes.
6. After controller success, measure joint and Cartesian endpoint error against configured tolerances. Controller success with a failed endpoint check is an execution failure.
7. Make `stop()` cancel the active goal, request vendor/controller stop, stop servo and base streams, and wait for measured stationary state within a finite bound.

## Interfaces and data

- Task-facing `Arm` methods
- MoveIt planning component or action
- Namespaced FollowJointTrajectory controller
- `MotionPlan` and `MotionResult` values plus run events

## Boundaries

- Does not choose a planner automatically
- Does not retry after execution begins
- Does not own task-level recovery or return-home behavior

## Failure behavior

- Planning errors contain planner ID and MoveIt code.
- Execution rejects stale plans and scene changes.
- Unknown controller state, partial execution, failed cancellation, or endpoint mismatch aborts the task and marks recovery required.

## Acceptance

- Combined and split paths execute the same immutable plan.
- Changing the primary or fallback planner requires no task-logic change beyond the explicit argument.
- A moved start state and changed collision scene both invalidate previewed plans.
- Cancel and stop tests reach measured stationary state.
- All outcomes identify planner attempts and artifacts.

## Parallel work

Pilz and OMPL implementations begin after request/result fields freeze. Visual servo consumes the stop behavior.

## What this module needs from me

Nothing.
