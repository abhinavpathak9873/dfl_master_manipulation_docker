# Installed real-hardware qualification

## Goal

Demonstrate routine-ready behavior for each declared installed robot/tool task through repeatable trials, safe failure injection, and complete evidence.

## Inputs

- Current commissioning records
- Accepted task packages
- Network/gateway/desktop orchestration
- Perception and grasp qualifications
- Run-record validator

## Outputs

- Declared test matrix per installed configuration
- Thirty-trial run sets
- Failure-injection results
- Success/failure distribution and stage metrics
- Zero-unsafe-event review
- Real qualification state in plugin/profile manifests

## Work

1. Declare robot, tool, base use, camera, scene, four-object subset, task, grasp anchors, pipeline, planner choices, retry bounds, operating conditions, and success criteria before trials.
2. Run preflight and a conservative smoke task. Preserve the exact resolved config and source/commissioning hashes for the trial set.
3. Run 30 end-to-end trials per declared installed task. Count every task failure, recovery-required result, operator intervention, or invalid run according to the written protocol.
4. Require at least 29 successes and zero unsafe events. Do not discard failed valid trials or rerun them under the same set ID.
5. Inject approved safe failures separately: target loss, camera interruption, network interruption, planner failure, gripper non-acquisition, and operator stop.
6. Review endpoint error, alignment correction, tool evidence, cycle time, perception health, network/time health, and failure distribution.
7. Publish qualified, failed, or blocked with exact evidence. A configuration change creates a new qualification set.

## Interfaces and data

- Local qualification runner
- Run manifests and commissioning references
- Profile/plugin qualification status

## Boundaries

- No statistical claim beyond the declared test conditions
- No real testing on uncommissioned combinations
- No tolerance adjustment after trial start

## Failure behavior

- Any unsafe event blocks qualification regardless of task success count.
- Fewer than 29 successes fails the set.
- Missing/corrupt run evidence invalidates the set and is reported, not silently replaced.

## Acceptance

- Each qualified set has 30 valid indexed trials.
- At least 29 pass and zero unsafe events occur.
- Failure injections stop through the intended contract.
- All source, object, config, calibration, and commissioning references resolve.
- The report lists limitations and next renewal condition.

## Parallel work

Runs per available installed configuration while documentation finishes.

## What this module needs from me

A scheduled supervised test window and declared task/object combinations.
