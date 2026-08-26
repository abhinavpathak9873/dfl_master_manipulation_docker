# Installed real-hardware qualification

## Goal

Demonstrate safe repeatable behavior for the installed and commissioned
robot/tool/task combinations without overstating unavailable hardware evidence.

## Task-script payoff

Developers know which ordinary task, robot/tool setup, backends, and limits have
real evidence, while remaining free to run clearly labelled experiments.

## Work

1. Freeze the qualification task, robot/tool/camera/base profile, object/scene,
   calibration, code/source, Docker image, model/backend, limits, and success
   criteria.
2. Run preflight and conservative supervised dry motion before contact trials.
3. Exercise arm planning/execution/stop, installed tool feedback, base behavior
   where used, D455/perception/tracking, alignment, grasp verification, place,
   and explicit failure/recovery branches.
4. Inject safe planned faults: no object, bad mask/pose, stale track/TF,
   no-plan, alignment failure, no grasp, slip, timeout/cancel, and permitted
   network/process interruptions.
5. For each named routine-use combination, run 30 declared trials, require at
   least 29 successes and zero unsafe events; report smaller development samples
   clearly.
6. Record failure stage/reason and bounded useful artifacts rather than only an
   aggregate success rate.
7. Keep not-mounted/not-commissioned combinations in the required profile plan
   and state that real evidence is pending.
8. Require requalification after relevant calibration, mount, firmware, driver,
   model, safety-limit, or major dependency changes.

## Acceptance

- Every claimed real-supported combination links current commissioning and trial
  evidence.
- Zero unsafe event means no limit violation, uncontrolled motion, false
  success after uncertainty, or automatic resume.
- Results include sample size, exact configuration, confidence/uncertainty, and
  observed limitations.
- Ordinary experiments remain runnable without a qualification runtime.

## Non-goals

Regulatory certification, unattended production operation, or turning untested
combinations into unsupported scope.
