# Position and velocity visual servo

## Goal

Port the tested DFF visual-servo behavior into an explicit control primitive with timestamped targets, bounded commands, observable convergence, and fail-safe target loss.

## Inputs

- Current DFF visual-servo code, configs, logs, and tests
- Motion stop contract
- TF/time rules
- Robot velocity/RT command path
- Live target contract from Phase 04 consumers

## Outputs

- Behavior characterization report
- `visual_servo()` task primitive and request/result types
- Static and live target publisher adapters
- Velocity controller with safety limits, filtering, and convergence rules
- Hold/reacquire state machine with blind finish removed
- Diagnostics topics and recorded-data/simulation tests

## Work

1. Run the existing static and moving-target tests and capture command rates, convergence, filters, joint limits, acceleration/jerk behavior, stale thresholds, hold states, and stop latency.
2. Separate target production from control. The target contains pose, frame, observation timestamp, source health, and optional velocity estimate; the controller never calls a perception implementation directly.
3. Transform each target at its observation timestamp, calculate bounded Cartesian error, map to joint velocity with singularity and position-limit guards, and stream through the accepted vendor/gateway interface.
4. Publish controller state, error, command, target age, target speed, saturation, and convergence evidence at a diagnostic rate.
5. On stale or lost target, immediately command zero and enter bounded hold. Accept reacquisition only when identity, timestamp, jump, and confidence gates pass. Expiry returns a typed target-lost failure.
6. Define convergence from position/orientation tolerance, target-motion bounds, measured robot motion, and settle time. Static success cannot be declared while the target or robot is still moving above bounds.
7. Remove blind finish and permissive lost-target defaults. Port only safeguards whose behavior is supported by characterization evidence.

## Interfaces and data

- `Arm.visual_servo(target, policy=...)`
- Live pose target protocol
- Namespaced velocity/RT command and stop interfaces
- Visual-servo diagnostic status and run events

## Boundaries

- Does not own object detection, pose estimation, or local correction
- Does not auto-switch to planned position motion after target loss
- Does not run on an unqualified network/driver path

## Failure behavior

- Zero command on stale target, TF failure, lost identity, limit proximity, singularity, command rejection, heartbeat loss, or cancellation.
- If stop acknowledgment is missing, raise control-loss and require explicit recovery.

## Acceptance

- Static and moving simulation targets converge within policy tolerances.
- Stale/loss injection produces zero commands before the hold state is reported.
- Reacquisition accepts bounded continuous targets and rejects jumps/wrong identity.
- No test enters blind finish.
- Command, error, and stop latency are present in run artifacts.

## Parallel work

Characterization starts early. Final controller consumes motion stop, namespace, and run-record contracts.

## What this module needs from me

Nothing.
