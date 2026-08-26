# Genesis emulator-backed bridge spike

## Goal

Determine whether Genesis can satisfy the accepted simulator contract while the official Doosan emulator remains in the control path. Produce evidence before any production bridge plan proceeds.

## Inputs

- Genesis 1.3.3 image
- Accepted Doosan descriptions and emulator behavior
- Robot/tool profiles
- Gazebo controller traces for comparison

## Outputs

- Minimal isolated bridge prototype
- Architecture trace showing command and state authority
- M1013 and H2515 URDF/xacro import report
- Trajectory, cancellation, tolerance, JointState, TF, and `/clock` measurements
- Emulator-in-loop feasibility decision
- Blocking decision record if the accepted contract cannot be met

## Work

1. Import M1013 and H2515 with official meshes, joint order, limits, inertials, and collision geometry. Record every xacro or package-URI adaptation.
2. Run one Doosan emulator per simulated arm. Determine whether its command/state interfaces can drive a Genesis entity while Genesis reports contacts and rendered sensors without creating two control authorities.
3. Implement only the bridge needed to test `FollowJointTrajectory`, cancellation, preemption, tolerances, fresh JointState, clock, and deterministic reset.
4. Compare commanded and observed trajectories with Gazebo traces. Record joint error, action result, cancel latency, clock behavior, and real-time factor.
5. Test one tool attachment and release path plus the generic camera topics. The spike need not implement all tool physics.
6. If the emulator cannot remain authoritative, stop. Document the exact incompatibility and the alternative Genesis-owned controller design, but do not implement that alternative without approval.
7. If the gate passes, write the production bridge requirements into the simulator contract packet.

## Interfaces and data

- Candidate `FollowJointTrajectory` action
- Namespaced JointState, TF, `/clock`, controller health, and reset
- Internal emulator-to-Genesis joint-state and command mapping

## Boundaries

- A spike is not supported simulator status
- Does not add a second motion planner
- Does not claim physical fidelity from visual similarity

## Failure behavior

- Fail on dual command authority, non-monotonic clock, incorrect joint ordering, ignored cancellation, false success, or reset that retains attachments/goals.
- A failed gate stops Genesis-dependent planning.

## Acceptance

- Both robot models import with limits matching the Doosan source.
- A planned trajectory returns correct action state and measured joints.
- Cancellation reaches a stopped state within the recorded bound.
- Reset is deterministic and clears goals/tool state.
- The evidence explicitly answers whether the official emulator remains in the loop.

## Parallel work

Runs beside Gazebo implementation. Production simulator-neutral work waits for this gate.

## What this module needs from me

No input unless the gate fails; then the user must choose between changing the emulator requirement, reducing Genesis scope, or dropping Genesis parity.
