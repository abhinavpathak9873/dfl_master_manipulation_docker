# Dependency upgrades and internal release

## Goal

Keep adopted sources/images/models reproducible and make deliberate upgrades
with focused evidence and rollback, without building a deployment pipeline.

## Task-script payoff

A developer can reproduce the environment that produced a result, intentionally
try an upgrade, compare affected tasks, and return to the prior working pins.

## Work

1. Inventory pinned Docker bases, ROS packages, vendor drivers, Doosan, MoveIt,
   Gazebo, Genesis, CUDA/TensorRT/Isaac ROS, models, M3T, reconstruction, UI,
   Python packages, calibration, and object schema versions actually used.
2. For an upgrade, name the concrete reason, owner, affected images/backends/
   robot modes/tasks, migration risk, and rollback pin before changing it.
3. Update one dependency family at a time when practical and retain old image/
   source pins until acceptance.
4. Rebuild cleanly and run only the affected unit, recorded-data, simulator
   matrix, commissioning, safety, and real-task checks at risk.
5. Measure API/ROS graph, accuracy, latency/rate, memory, GPU compatibility,
   controller/stop, asset, and data-format changes as relevant.
6. Document migrations and never rewrite canonical object/calibration history
   destructively.
7. Create an internal release record containing source/image/model/schema pins,
   supported/commissioned matrix, key evidence, known limitations, build/run
   commands, and rollback.
8. Optional Git/LFS backup of ObjectDB authoring data has separate health and
   recovery documentation; it is not a runtime release gate.
9. Keep releases manual and local unless an actual team problem justifies more
   automation.

## Acceptance

- A clean checkout plus documented Docker commands reproduces the released
  environment.
- Every changed dependency has focused before/after evidence and rollback.
- No required capability disappears silently after an evidence failure.
- Tasks do not need a release service, version registry, or remote backend.
- The release record makes uncommissioned/unqualified combinations explicit.

## Non-goals

Continuous deployment, automatic dependency updates, release orchestration,
remote rollout, or production support machinery.
