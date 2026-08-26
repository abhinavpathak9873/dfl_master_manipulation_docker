# Gazebo and Genesis parity

## Goal

Compare the shared task operations across both simulators for the complete
declared robot/tool matrix and document honest differences.

## Task-script payoff

Switching `mode` preserves useful task structure, and the developer knows which
sensor/contact/timing behaviors differ before relying on them.

## Work

1. Run all 12 robot/tool selections in Gazebo and Genesis using the same compact
   task operations and scene/object assets.
2. Compare construction/readiness, TF, joint state, planning/controllers, Pilz,
   OMPL, relative motion, gripper state, Picker base behavior, D455-equivalent
   RGB-D, stop/cancel, reset, and clock.
3. Compare kinematics, limits, TCP/collision geometry, final pose/joints,
   trajectory timing, contact/force approximation, suction/width behavior,
   rendering/depth, and failure mapping.
4. Run concurrent Picker 1/Picker 2 in both simulators.
5. Feed representative perception/alignment/grasp tasks where sensor fidelity is
   sufficient and label simulator-truth-only evaluation.
6. Set tolerances per observable robotics need rather than demanding identical
   physics internals.
7. Investigate mismatches at concrete adapters/models; do not patch task code with
   simulator conditionals unless the behavior is genuinely mode-specific.
8. Publish exact limitations and reproduction commands.

## Acceptance

- All 24 combinations are exercised with no silent skips.
- Shared operations preserve task API and declared semantics within justified
  tolerances.
- Differences are explicit, attributable, and accessible through concrete
  backends.
- Unsupported fidelity raises/warns clearly instead of false equivalence.
- Parity needs no simulator framework beyond the two adapters and shared checks.

## Non-goals

Pixel-identical rendering, identical physics engines, or using simulation parity
as real-hardware qualification.
