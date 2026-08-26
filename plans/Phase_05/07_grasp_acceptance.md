# Closed-loop grasp acceptance

## Goal

Demonstrate the full visible perception-to-place sequence across approved
objects, supported tools, simulators, and commissioned hardware.

## Task-script payoff

The representative task remains ordinary readable Python while backend, object,
tool, robot, and mode changes stay localized to their natural selections.

## Reference flow

Load object; capture RGB-D; segment; estimate pose; optionally track; transform
or generate grasps; approach; compute/apply local correction; descend with
declared contact behavior; close; verify; explicitly retry or abort; lift;
transfer; place; release; retreat.

## Work

1. Keep the acceptance tasks as normal Python and use the canonical API shape.
2. Cover the four approved objects and each relevant VGC10 one/four cup, VGP20,
   and 2FG14 grasp profile; report non-applicable object/tool pairings explicitly.
3. Run Gazebo and Genesis trials with simulator truth used only for evaluation.
4. Run conservative supervised installed-hardware trials with fixed scene,
   calibration, object revision, backend/model, limits, and declared success
   criteria.
5. Inject mask/pose/track loss, poor alignment, no-plan, contact, tool failure,
   wrong width/suction, slip, timeout, cancel, and component loss.
6. Require zero unsafe events. Named routine-use qualification uses 30 trials and
   at least 29 successes; development evidence may use smaller clearly labelled
   samples.
7. Save compact failure evidence sufficient to reproduce/tune the named stage.
8. Publish limitations by object/tool/mode/backend instead of hiding them behind
   an aggregate pass.

## Acceptance

- Task logic is readable top-to-bottom and every motion is attributable.
- Successful trials meet pose/place/task-specific tolerances.
- All injected unsafe/uncertain paths stop and do not auto-resume.
- Backend or tool swaps do not force unrelated task rewrites.
- Results state sample size and never overclaim uncommissioned combinations.

## Non-goals

A one-call opaque pick application, deployment certification, or generalized
autonomous recovery.
