# Manipulation phase acceptance

## Goal

Demonstrate the complete Phase 02 utility through readable tasks and focused
failure tests.

## Matrix

- Picker 1/M1013, Picker 2/M1013, H2515.
- VGC10 one cup, VGC10 four cups, VGP20, 2FG14.
- Gazebo and Genesis for all 12 selections.
- Commissioned real combinations as hardware is available.
- Concurrent Picker 1/Picker 2 scenario.

## Work

1. Run joint, pose, relative approach/ascend/descend, stop/cancel, Pilz, OMPL,
   gripper, camera/state, and Picker base checks as applicable.
2. Include collision/no-plan, stale TF, unavailable force, tool failure,
   disconnect, timeout, partial/unknown execution, and cleanup faults.
3. Exercise plan inspection/execution and explicit planning fallback.
4. Verify task-visible results/errors and direct backend/ROS diagnostics.
5. Run conservative supervised checks for every commissioned real combination;
   record unmounted combinations as not commissioned, never as unsupported scope.
6. Verify concurrent Picker isolation and shared lab safety procedure.
7. Save compact reproducible evidence required for failures/qualification.

## Acceptance

- Every simulator matrix combination reaches the correct robot/tool backend and
  completes applicable basic operations.
- Safety-critical failures stop and never produce false success or auto-resume.
- The same task API shape is useful across modes; real differences are explicit.
- All four gripper profiles and both Picker bases retain their distinct behavior.
- A robotics developer can understand each acceptance task without a framework
  diagram.

## Outputs

- Matrix result table, failure report, real commissioning links, and reproduction
  commands.
- Known limitations per robot/tool/mode.
- API changes discovered by concrete use, kept as small as possible.

## Non-goals

A single aggregate release score, automated deployment certification, or hiding
uncommissioned hardware facts.
