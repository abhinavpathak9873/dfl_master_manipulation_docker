# Bounded local-alignment visual servo

## Goal

Apply successive alignment corrections through the Phase 02 servo/motion
primitive with explicit limits, freshness, convergence, and stop behavior.

## Task-script payoff

The task can keep the loop inline or call a small helper whose logic is still
obvious: measure, validate, apply bounded correction, check convergence, repeat
or stop.

## Work

1. Define the readable reference loop in ordinary Python before extracting any
   helper.
2. Require a current healthy target/object identity and timestamp-valid camera/TF
   for every iteration.
3. Bound total/step translation and rotation, speed/acceleration, workspace,
   duration, iterations, and force/contact as supported.
4. Separate correction computation from robot command and log both when debug
   recording is enabled.
5. Define convergence using measured residual/correction and consecutive stable
   samples.
6. On stale/lost target, bad correction, timeout, limit, force, cancel, or
   exception, command zero/stop and return control to the task.
7. Permit bounded reacquisition/recompute only when explicitly requested by the
   task/helper arguments.
8. Test delayed updates, sign/frame error, oscillation, divergence, occlusion,
   cancel, contact, and process/network loss.

## Acceptance

- Known offsets converge within declared task/tool tolerance.
- No command is issued from stale, wrong-object, or out-of-bounds corrections.
- All exits have a reason and safe final command behavior.
- The helper can be removed and expressed as a short equivalent Python loop.

## Non-goals

A generic behavior tree, autonomous recovery, or hidden manipulation sequence.
