# Existing local-alignment characterization

## Goal

Capture the observable behavior, data dependencies, thresholds, corrections, operator workflow, and failure modes of the current DFF local-grasp alignment before porting it.

## Inputs

- Current local-alignment nodes/actions/topics/configs/tests
- Approved local references and small-tray profile
- Existing run logs and images
- Alignment contract draft

## Outputs

- Behavior map from input to correction and motion target
- ROS graph and parameter inventory
- Recorded/golden fixture set
- Threshold and frame table
- Known bugs and accidental coupling list
- Port equivalence criteria

## Work

1. Trace object focus, reference selection, camera image/depth, TF lookup, mask/crop, correction calculation, target publication, acknowledgment, and diagnostics.
2. Record all coordinate frames, quaternion conventions, units, sign choices, correction clipping, smoothing, focus/ack state, and timing rules.
3. Run current tests and representative recorded inputs. Capture outputs at each stage, not only the final pose.
4. Separate reusable behavior from Object Studio, database, GUI, or task-specific coupling.
5. Identify unsafe or obsolete behavior, including latest-TF fallback, stale target reuse, hidden motion, permissive loss, or direct database mutation.
6. Define numeric equivalence tolerances for accepted behavior and explicit intended differences required by the global decisions.
7. Package fixtures so the new backend can run without the old runtime.

## Interfaces and data

- Characterization fixtures and expected outputs
- Source-to-new behavior matrix
- Threshold provenance table

## Boundaries

- Does not copy old module structure
- Does not preserve known unsafe behavior
- Does not implement the new backend

## Failure behavior

- A behavior with insufficient evidence remains marked unknown; it is not guessed.
- Conflicting code/test behavior is recorded with both sources and a recommended contract interpretation.

## Acceptance

- Every input/output and side effect has an owner.
- Golden fixtures cover success, weak evidence, stale data, wrong focus, and correction bounds.
- All accepted behavior has a numeric equivalence tolerance.
- Every intended difference cites a global decision or measured defect.

## Parallel work

Runs with alignment contract; each informs the other's final review.

## What this module needs from me

Nothing.
