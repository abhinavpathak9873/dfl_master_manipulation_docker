# Pilz PTP, LIN, and CIRC

## Goal

Integrate the concrete Pilz motion paths needed for predictable industrial arm
movement on M1013 and H2515.

## Task-script payoff

A task selects `planner="pilz_ptp"`, `pilz_lin`, or `pilz_circ` and receives
clear planning/execution results without knowing adapter internals.

## Work

1. Characterize existing DFL and upstream MoveIt/Pilz calls, frames, scaling,
   limits, blending, and result behavior.
2. Implement the smallest direct adapter for PTP, LIN, and CIRC, keeping
   backend-specific circle parameters explicit.
3. Validate joint/cartesian limits, start state, scene version, and required
   frames before planning.
4. Keep plan output inspectable and execute only a plan associated with the
   current robot/scene/start state.
5. Map cancel, timeout, planning rejection, controller rejection, and unknown
   execution honestly.
6. Test M1013 and H2515 kinematics plus namespaced Picker profiles in both
   simulators.
7. Characterize installed real behavior with conservative speeds and stop tests.

## Acceptance

- PTP reaches joint/pose targets within declared tolerance.
- LIN preserves required Cartesian straightness; CIRC follows declared geometry.
- Invalid geometry and limits fail before motion.
- Cancellation/stop leaves an observable state and never reports false success.
- Direct MoveIt/Pilz diagnostics remain available.

## Non-goals

A planner plugin marketplace or automatic planner selection.
