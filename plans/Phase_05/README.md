# Phase 05 — local alignment and closed-loop grasping

## Goal

Preserve proven close-range alignment behavior, make algorithms replaceable, and
express grasp execution, verification, retry, and recovery visibly in task code.

## Task-script payoff

A developer computes an XY/RPY correction, applies it through the arm, descends
with explicit bounds/force behavior, closes the selected gripper, checks the
result, and writes an ordinary Python retry loop.

## Packets

1. [Local-alignment API](01_alignment_contract.md)
2. [Existing behavior characterization](02_legacy_characterization.md)
3. [Reference/mask/depth alignment](03_reference_depth_alignment.md)
4. [Bounded visual servo](04_bounded_visual_servo.md)
5. [Grasp verification](05_grasp_verification.md)
6. [Explicit retry and recovery](06_retry_and_recovery.md)
7. [Closed-loop acceptance](07_grasp_acceptance.md)

## Smallest sufficient design

- `LocalAlignment.compute(...)` returns correction and diagnostics; it never
  moves the robot.
- Backends use direct mappings and explicit named inputs.
- Servoing is a bounded visible loop/helper over Phase 02 primitives.
- Gripper/tool evidence remains honest and tool-specific.
- Retry/recovery stays ordinary Python; uncertainty stops.

## Exit evidence

The approved objects and supported tools demonstrate alignment, approach,
contact, verification, bounded failures, and declared simulator/real trials with
zero unsafe events.

## Non-goals

A manipulation state-machine runtime, recovery policy engine, opaque pick helper,
or verification plugin system.
