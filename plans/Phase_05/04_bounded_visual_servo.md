# Bounded local-alignment visual servo

## Goal

Apply successive valid local corrections through the Phase 02 visual-servo controller, with explicit observation, convergence, hold, reacquisition, and abort states.

## Inputs

- Local-alignment result stream
- Phase 02 visual-servo primitive
- Healthy selected track
- Grasp profile servo policy
- Run diagnostics

## Outputs

- Explicit task helper for alignment-observe-servo cycles
- Bounded state machine
- Correction-age/jump filters
- Convergence and contact boundary
- Simulation and recorded-target tests

## Work

1. Start only from a verified pre-grasp pose, fresh track, valid anchor/profile, ready gripper, and scene version.
2. Request local alignment, convert the correction to a live target, and stream only while correction identity, age, capture range, and jump checks pass.
3. Set policy bounds for maximum linear/angular command, acceleration/jerk, correction magnitude, total travel, duration, and iteration count from validated configuration.
4. On missing or invalid correction, command zero immediately and enter the Phase 02 hold/reacquire state. A fresh valid correction may resume within the configured bound.
5. Declare convergence only when correction, measured robot speed, target speed, and settle time all pass.
6. End visual servo before the task crosses the configured contact/final-descent boundary. Contact motion uses an explicit next primitive.
7. Record each correction, rejection, command, hold, transition, and measured endpoint.

## Interfaces and data

- Task-level alignment/servo helper composed from public primitives
- Alignment and visual-servo state events
- Policy configuration in grasp profile

## Boundaries

- Does not close the gripper
- Does not blind-finish from the last correction
- Does not retry outside task-declared bounds

## Failure behavior

- Any identity/revision/track change, stale correction, TF failure, limit guard, control loss, expired hold, or exceeded travel aborts.
- Abort returns recovery-required when the robot state or contact boundary is uncertain.

## Acceptance

- Nominal moving-target fixtures converge.
- Loss injection commands zero before hold status.
- Reacquisition accepts continuous corrections and rejects jumps.
- Travel/time/iteration bounds stop the helper.
- No command occurs after invalid correction or contact-boundary exit.

## Parallel work

Consumes completed alignment and servo contracts. Verification work can proceed.

## What this module needs from me

Nothing.
