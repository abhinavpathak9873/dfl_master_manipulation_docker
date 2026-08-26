# Pilz PTP, LIN, and CIRC

## Goal

Qualify deterministic Pilz motion for joint/pose transfer, Cartesian approach and retreat, and circular paths while preserving the proven DFF safeguards.

## Inputs

- Motion contract
- Pinned MoveIt/Pilz packages
- Robot joint/Cartesian limits
- Characterization fixtures from current DFF code

## Outputs

- Planner plugins `pilz_ptp`, `pilz_lin`, and `pilz_circ`
- Per-robot Cartesian limits and scaling profiles
- Nearest-valid-IK handling for PTP pose goals
- LIN relative-motion and endpoint validation
- CIRC center/interim-point request model
- Planner contract and regression tests

## Work

1. Map public planner IDs to the Pilz pipeline and exact planner IDs PTP, LIN, and CIRC. Record both names in every attempt.
2. For PTP pose goals, resolve and freeze a valid joint target during planning. Execute that target rather than solving IK again.
3. For LIN, calculate the target in the declared base or tool frame, set the current measured start state, apply geometric speed backoff when required, retime within limits, and validate the complete Cartesian trajectory.
4. Port the existing safeguards for trajectory finiteness, joint limits, discontinuity, duration, speed, acceleration, start-state agreement, and measured endpoint tolerance.
5. Define CIRC requests with an unambiguous center or interim point, path constraint, orientation behavior, and rejection of degenerate geometry.
6. Keep velocity and acceleration details in named configuration profiles; task calls may select scaling within allowed bounds.
7. Characterize old and new trajectories from identical start/target fixtures and explain meaningful differences.

## Interfaces and data

- Motion planner plugin contract
- Pilz pipeline configuration and Cartesian limit files
- Run events for planner, backoff, retiming, and endpoint checks

## Boundaries

- Does not use Pilz as an implicit fallback for OMPL
- Does not approximate a failed LIN path with PTP
- Does not accept a Cartesian fraction below full completion for execution

## Failure behavior

- Reject infeasible IK, incomplete Cartesian path, invalid CIRC geometry, limit violation, retiming failure, stale start state, or endpoint mismatch.
- Return the exact failed safeguard and measured value.

## Acceptance

- PTP, LIN, and CIRC pass shared motion tests on M1013 and H2515.
- LIN descent and retreat follow the requested frame and sign.
- The nearest-IK regression fixtures preserve intended joint branches.
- Endpoint tests include translation, rotation, and joints.
- Gazebo and Genesis expose the same logical results within their tolerances.

## Parallel work

Runs beside OMPL. Visual servo characterization may use the accepted stop and limit utilities.

## What this module needs from me

Nothing.
