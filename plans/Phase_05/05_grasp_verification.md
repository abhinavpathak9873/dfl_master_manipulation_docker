# Grasp verification

## Goal

Turn available gripper, robot, and optional perception evidence into a small
honest grasp result for task decisions.

## Task-script payoff

After `robot.gripper.close(...)` the task checks useful suction, width, force,
contact, or lift evidence and decides with a normal `if`/`while`.

## Work

1. Inventory reliable real and simulated evidence for VGC10 one/four cup, VGP20,
   and 2FG14.
2. Keep the gripper command result separate from optional post-close/lift
   verification.
3. Read object-specific expected width/tolerance, cup requirements, thresholds,
   and lift checks from the task or grasp profile.
4. Define simple outcomes such as success/failure/unknown with the actual
   observations and reasons; do not fabricate cross-tool confidence.
5. Use attached-object or simulator contact truth only in simulation tests, not
   as a real-runtime shortcut.
6. Bound optional lift/probe motion explicitly and stop on slip, force, stale
   perception, or uncertain state.
7. Test empty close, correct grasp, off-center/partial suction, wrong width,
   slip/loss, unavailable feedback, timeout, and sensor disagreement.
8. Preserve raw vendor feedback for diagnosis.

## Acceptance

- Each tool has documented evidence and limitations.
- Unknown feedback never becomes success by default.
- Object expectations remain outside the driver.
- Task retry examples are readable and can branch on actual result data.
- Simulation-only truth is clearly separated from real evidence.

## Non-goals

A policy plugin system, learned verifier mandate, or automatic task recovery.
