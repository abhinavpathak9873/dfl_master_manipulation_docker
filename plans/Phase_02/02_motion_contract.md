# Arm motion API

## Goal

Provide a small, clear arm interface for the movements researchers repeatedly
write while preserving direct planning/execution access.

## Task-script payoff

Tasks can call `move_joints`, `move_pose`, `ascend`, `descend`,
`apply_cartesian_offset`, `plan`, `execute`, and `stop` with explicit frames,
limits, planners, and useful results.

## Work

1. Define shared methods from actual Doosan/MoveIt use, not a universal motion
   request object.
2. Accept `Joints` and `Pose` values, explicit speed/acceleration where useful,
   planner selection, timeout, and task-visible optional fallback.
3. Define relative helpers in a named tool/world frame and test sign/frame
   behavior.
4. Support force-aware descend only when the robot/mode exposes credible sensing
   and stop behavior; otherwise raise an actionable unsupported error.
5. Keep combined plan-and-execute for common use and separate plan/execute for
   inspection, visualization, approval, or reuse.
6. Treat planning failure, rejected trajectory, cancellation, timeout, partial
   execution, stale scene, and unknown final state distinctly.
7. Never try another planner after execution begins. Unknown/partial execution
   requires stop and explicit recovery.
8. Expose underlying MoveIt/controller data in results/debug access where useful.

## Acceptance

- Canonical joint, pose, offset, descend/contact, cancel, and stop examples are
  readable and behave consistently in supported modes.
- Units/frames/limits are validated before command.
- Unsupported force behavior fails clearly.
- Task code can inspect plans and concrete backend details without bypassing
  safety checks.

## Non-goals

A motion DSL, autonomous planner policy engine, or universal trajectory system.
