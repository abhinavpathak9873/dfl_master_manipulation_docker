# OMPL planning and explicit fallbacks

## Goal

Provide general collision-aware planning and task-declared planning alternatives without making motion behavior unpredictable.

## Inputs

- Motion contract
- MoveIt planning scene
- Robot OMPL configurations
- Run-record attempts

## Outputs

- `ompl` planner plugin
- Validated per-robot OMPL planner profiles
- Ordered fallback executor for planning attempts
- Attempt classification and artifact capture
- Collision and fallback contract tests

## Work

1. Map `ompl` to a profile-selected MoveIt OMPL planner. The profile records algorithm, timeout, attempts, simplification, optimization objective, and scaling; task code sees the stable `ompl` ID.
2. Plan against the captured robot start state, attached objects, static scene, and dynamic scene snapshot. Save the planning-scene version and trajectory validation report.
3. Run the primary planner once according to its configured attempt policy. Move to the next declared fallback only for classified planning failures.
4. Do not fallback after a controller goal is accepted, after any measured motion, on cancellation ambiguity, or when the start/scene state changes.
5. Record each attempt's planner ID, duration, MoveIt code, target, start hash, scene version, and trajectory artifact.
6. Validate OMPL trajectories through the same joint-limit, collision, timing, and endpoint preconditions used by other planners.
7. Test explicit sequences such as PTP then OMPL and OMPL then PTP; no global default may add an unlisted attempt.

## Interfaces and data

- Planner plugin `ompl`
- Motion request `fallback` tuple
- MoveIt planning scene and OMPL pipeline
- Attempt events in run records

## Boundaries

- Does not perform execution recovery
- Does not silently relax collision geometry, tolerances, or goal constraints
- Does not add cuMotion

## Failure behavior

- Classify no-solution, timeout, invalid start, invalid goal, collision, and internal errors.
- State or scene invalidation ends the whole request instead of trying another planner.

## Acceptance

- Collision fixtures demonstrate valid detours and rejected paths.
- Fallback order matches the task request exactly.
- Execution-start injection proves no fallback occurs afterward.
- Every attempt has a plan artifact or explicit reason none exists.
- Changing OMPL algorithm in a profile changes no task source.

## Parallel work

Runs with Pilz after the common motion contract freezes.

## What this module needs from me

Nothing.
