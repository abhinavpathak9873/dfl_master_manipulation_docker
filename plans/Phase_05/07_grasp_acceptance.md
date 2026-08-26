# Closed-loop grasp acceptance

## Goal

Qualify the explicit coarse-pose, pre-grasp, local-alignment, servo, grip, verification, lift, and recovery path in both simulators and on installed hardware.

## Inputs

- All Phase 05 modules
- Four approved objects and grasp profiles
- Phase 04 qualification stack
- Phase 02 manipulation suite
- Run records

## Outputs

- Representative explicit grasp task package
- Gazebo and Genesis grasp matrix
- Recorded-failure suite
- Installed robot/tool 30-trial reports
- Phase acceptance decision

## Work

1. Write the task with visible stages and selected planner/control type at each motion. Keep retry bounds in task configuration and default them to zero.
2. Run each qualified object/gripper pairing in both simulators. Include nominal pose error inside the local capture range and rejected error outside it.
3. Inject stale track, wrong revision, bad reference, low mask/depth, alignment jump, target loss, servo timeout, empty grip, object loss on lift, and scene attachment mismatch.
4. Verify stop, failure code, artifact, scene state, and recovery-required status for every injected case.
5. For each installed robot/tool task selected for routine use, declare the object/scene set and run 30 trials under controlled variation.
6. Require at least 29 end-to-end successes and zero unsafe events. Record recoverable failures separately; they still count as task failures.
7. Publish per-stage success, timing, correction, planner, tool evidence, and failure distribution.

## Interfaces and data

- External task package
- Local qualification runner
- Per-object/gripper qualification records

## Boundaries

- Does not claim all four objects work with every real tool
- Does not include scanning or GUI
- Does not relax thresholds after failed trials

## Failure behavior

- Any unsafe continuation, false verified grasp, blind finish, missing stop, or unrecorded state blocks the phase.
- A failed 29/30 result remains unqualified until a new declared test run.

## Acceptance

- All simulator failure cases produce the expected safe state.
- At least one representative task completes in Gazebo and Genesis through the same API.
- Installed qualified tasks meet 29/30 and zero unsafe events.
- Every result links exact object, grasp, tool, config, source, and perception revisions.

## Parallel work

Final Phase 05 packet.

## What this module needs from me

Access to installed hardware and a declared representative task/object set. Selection can be made when the hardware window is scheduled.
