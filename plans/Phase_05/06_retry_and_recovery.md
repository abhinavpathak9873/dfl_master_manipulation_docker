# Explicit retry and recovery rules

## Goal

Document safe retryable stages and readable task patterns without introducing a
state-machine framework.

## Task-script payoff

A developer writes ordinary `try`, `if`, and `while` around named perception,
alignment, approach, or gripper operations and can see exactly what will move.

## Work

1. Classify failures by actual stage and whether robot/object state is known:
   perception no-result, stale track, no alignment, planning failure, pre-contact
   cancel, contact/grip failure, slip, partial/unknown motion, and lost control.
2. Allow bounded retry only when the task can re-establish required observations,
   frames, collision state, and safe robot/object state.
3. Make retry count, offset, reobserve/reseed behavior, retreat, and timeout
   explicit in task code or a tiny task-specific helper.
4. Default to no retry for contact/unknown execution unless a named task proves a
   safe recovery.
5. Stop and require explicit recovery/fresh run after uncertain execution,
   network/controller loss, invalid scene, or unknown object attachment.
6. Provide canonical examples for segmentation retry, alignment recompute,
   pre-grasp replan, failed gripper close with small ascent, and abort after
   bounded attempts.
7. Inject failures at every stage and verify visible branch/stop behavior.

## Acceptance

- Retry loops are finite and readable from the task.
- No task silently auto-resumes or auto-homes after uncertainty.
- Each retry revalidates the state it depends on.
- Reusable helpers remain compositions of public primitives and may be opened or
  bypassed.

## Non-goals

A behavior-tree/state-machine runtime, generic recovery planner, or background
task supervisor.
