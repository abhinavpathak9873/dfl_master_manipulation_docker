# Position and velocity visual servo

## Goal

Provide bounded, inspectable servo primitives for applying live pose/correction
updates safely.

## Task-script payoff

A task or alignment helper can apply a current target with explicit speed,
freshness, convergence, timeout, and stop bounds, while keeping the control loop
visible.

## Work

1. Characterize existing position and velocity servo paths, rates, filtering,
   frames, thresholds, watchdogs, and stop behavior.
2. Define small stateful servo objects or helpers over the actual MoveIt Servo or
   Doosan command path.
3. Require target frame/time/age and reject stale/lost perception.
4. Bound translation, rotation, velocity, acceleration, duration, workspace, and
   force/contact behavior as supported.
5. Command zero/stop during target loss, bounded hold, cancellation, or
   exception; require explicit fresh convergence to continue.
6. Keep target update, convergence, and recovery in ordinary task/helper control
   flow.
7. Test latency, jitter, sign/frame errors, target loss/reacquisition, limits,
   stop, and unsupported-mode behavior.

## Acceptance

- Known offsets converge within declared position/orientation tolerances.
- Stale/lost targets never continue motion.
- Timeout/cancel/network loss reaches zero/stop within measured bounds.
- Debug output exposes target, correction, frame, age, command, and reason.

## Non-goals

A generalized behavior controller, hidden task recovery, or unbounded servo loop.
