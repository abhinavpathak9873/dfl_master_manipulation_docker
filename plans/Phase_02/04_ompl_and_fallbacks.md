# OMPL planning and explicit fallbacks

## Goal

Provide collision-aware OMPL planning and simple task-visible pre-execution
fallback attempts for tasks that need them.

## Task-script payoff

A developer can choose an OMPL planner or write a short ordered list of planning
attempts while retaining control over when execution starts.

## Work

1. Configure only the OMPL planners exercised by declared scenes/tasks for
   M1013 and H2515.
2. Expose planner ID, planning time, attempts, constraints, and scaling as clear
   arguments or small adapter-owned settings.
3. Validate current state, target frame, collision scene, constraints, and limits.
4. Represent fallback as an ordered planning-only loop. Stop on the first valid
   plan; never fall back after execution begins.
5. Record each attempt's planner and reason when run evidence is enabled.
6. Reject stale scene/start state at execution and require replanning.
7. Add obstacle, no-path, timeout, invalid-goal, cancellation, and deterministic
   seed fixtures where practical.

## Acceptance

- Named obstacle tasks plan collision-free paths or return a clear no-plan result.
- Fallback ordering is visible and no second planner runs after execution starts.
- A stale plan cannot execute against a changed scene/start state.
- Backend-specific OMPL configuration remains directly inspectable.

## Non-goals

An adaptive planning policy, automatic recovery, or planner registry.
