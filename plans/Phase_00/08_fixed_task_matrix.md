# Fixed-task simulator matrix

## Goal

Prove the container, profiles, vendor control path, simulator contract, and tool models with one explicit fixed-pose task before the public toolbox grows.

## Inputs

- Accepted simulator contract
- Twelve robot/tool profile combinations
- One fixed scene and collision geometry
- Run-record format draft

## Outputs

- External ROS 2 task package for fixed pick/place
- Twenty-four simulator run cases
- Per-case manifest, logs, trajectory results, endpoint metrics, and screenshots or state captures
- Failure summary and blocking defect list

## Work

1. Write one task that homes the arm, opens/releases the tool, moves to pre-pick, descends with Pilz LIN, actuates the tool, lifts, transfers, descends, releases, retreats, and returns home.
2. Keep poses and distances in the task configuration while robot, gripper, scene, mode, and pipeline selectors remain in code.
3. Run the three robot identities with four tool profiles in Gazebo and Genesis. Use the same task source for all 24 cases.
4. For picker profiles, add a separate bounded base-velocity smoke command and stop; do not include route planning.
5. Record plan ID, planner, action result, actual endpoint, tool result, reset result, and simulator-specific tolerances.
6. Repeat reset and rerun to expose leaked attachments, stale controllers, or non-deterministic starting state.
7. Block later manipulation implementation on any false success, unsafe continuation, namespace collision, or unsupported profile.

## Interfaces and data

- Task-package convention precursor
- Combined task stages over the simulator contract
- Run artifacts consumed by Phase 01 diagnostics

## Boundaries

- Uses fixed poses; no perception, object database lookup, tracking, or local alignment
- Does not set the final Python API signatures

## Failure behavior

- Abort the case on any stage failure and still execute simulator reset plus artifact flush.
- Never continue after partial trajectory execution without a measured state and explicit recovery step.

## Acceptance

- All 24 cases start from a clean reset and reach their declared outcome.
- Every planned motion has feedback and endpoint evidence.
- Every tool reports a meaningful acquired/released or open/closed result.
- Picker base smoke commands stop on duration and watchdog.
- The run matrix identifies no shared namespace or controller ownership.

## Parallel work

No later task API implementation starts until this matrix establishes viable lower-level behavior.

## What this module needs from me

Nothing.
