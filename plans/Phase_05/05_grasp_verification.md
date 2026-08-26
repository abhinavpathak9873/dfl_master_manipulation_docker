# Grasp verification

## Goal

Decide whether the selected object is held using tool-specific feedback, measured motion, and optional perception evidence instead of actuator completion alone.

## Inputs

- Shared gripper results/status
- Grasp profile verification settings
- Object track and scene attachment
- Arm endpoint/state
- Simulator contact truth for tests

## Outputs

- Typed grasp-verification request/result
- Vacuum and parallel-jaw verification plugins or policies
- Lift-check procedure
- Scene attach eligibility
- Failure evidence and fixtures

## Work

1. For vacuum tools, evaluate achieved vacuum/channel state, pressure stability where available, command timing, and object-loss status. Declare unavailable sensing explicitly.
2. For 2FG14, evaluate object-detected flag, returned width, expected width/tolerance, force state, and connection health.
3. Allow a short configured lift-check only after initial tool evidence passes. Monitor tool state and, when available, object pose consistency during the lift.
4. Bind the result to object revision, anchor, gripper profile, command result, and measured robot pose.
5. Return verified, not-held, uncertain, or lost-after-lift with component evidence.
6. Attach the object to MoveIt only after verified. An uncertain result does not attach and requires explicit recovery.
7. Record simulator ground truth only as test evidence; runtime policy must use the same observable signals available in the selected mode.

## Interfaces and data

- Grasp verification value/API
- Gripper status and result
- MoveIt attach request eligibility
- Optional tracked-object consistency

## Boundaries

- Does not choose retry or release
- Does not assume a suction command proves a seal
- Does not use simulator-only truth in task runtime

## Failure behavior

- Missing required feedback, stale status, width mismatch, vacuum loss, connection loss, object motion inconsistency, and uncertain lift remain distinct.
- Uncertain never maps to success.

## Acceptance

- Tool-specific success and empty-grip fixtures classify correctly.
- Pressure/width loss during lift becomes lost-after-lift.
- Scene attach occurs only on verified.
- Real and simulator policies consume equivalent observable fields.
- Artifacts show every evidence component.

## Parallel work

Runs alongside alignment implementation after gripper contracts exist.

## What this module needs from me

Nothing.
