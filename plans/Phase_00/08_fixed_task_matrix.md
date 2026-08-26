# Fixed-task simulator matrix

## Goal

Exercise all required robot/tool selections through small readable tasks in both
Gazebo and Genesis.

## Task-script payoff

A developer can choose any declared robot, tool, and simulator with confidence
that construction, basic motion, sensing, and tool control reach the correct
backend.

## Matrix

- Robots: Picker 1/M1013, Picker 2/M1013, H2515.
- Tools: VGC10 one cup, VGC10 four cups, VGP20, 2FG14.
- Modes: Gazebo and Genesis.
- Total: 24 robot/tool/mode selections, plus a concurrent Picker 1/Picker 2
  scenario.

## Work

1. Use one compact ordinary Python task shape for construction, bringup,
   readiness, home/joint motion, Cartesian or relative motion, tool operation,
   camera/state inspection where present, stop, and cleanup.
2. Keep combination-specific expected behavior in readable test data rather than
   branching through a framework.
3. Add checks for generated descriptions, frames, planning groups, controllers,
   TCP/collision geometry, namespaces, and scene loading.
4. For Picker profiles, check base state/stop without requiring navigation.
5. Record unsupported sensor/force fidelity honestly while still testing clear
   error behavior.
6. Run a dual-Picker namespace/concurrency smoke task.
7. Save concise per-run result, timing, selected revisions, and failure logs only
   as needed to reproduce issues.

## Outputs

- The 24-run matrix definition and reusable task scripts.
- Compact result table and failure artifacts.
- List of real simulator limitations by operation/combination.
- Reproduction commands.

## Acceptance

- Every declared combination constructs and reaches the correct description,
  controllers, tool, scene, and backend in both simulators.
- Required basic operations pass or produce an explicitly accepted simulator
  limitation—not a silent skip.
- Failed combinations are diagnosable through direct task/adapter/ROS paths.
- The matrix does not require a workflow engine, release service, or ObjectDB
  process.

## Non-goals

- Claiming real-hardware commissioning from simulator success.
- Hiding individual combination failures behind aggregate scores.
