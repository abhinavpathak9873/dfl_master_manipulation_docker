# Manipulation phase acceptance

## Goal

Integrate lifecycle, motion, planners, visual servo, tools, base velocity, and concurrent robots into a repeatable local qualification suite.

## Inputs

- All Phase 02 packet outputs
- Phase 00 simulator matrix
- Phase 01 task/run contracts
- Installed hardware windows

## Outputs

- Local manipulation qualification command
- Simulation and hardware test matrix
- Failure-injection suite
- Performance and endpoint report
- Phase exit record with open hardware qualifications

## Work

1. Run unit and shared contract tests for every plugin and public value.
2. Run explicit tasks for joint motion, PTP pose, LIN approach/retreat, CIRC, OMPL collision detour, planner fallback, visual servo, each gripper, and bounded base velocity.
3. Run combined fixed pick/place on all 24 simulator cases and dual Picker concurrency.
4. Inject stale plan, changed scene, cancellation, partial execution, target loss, TF failure, controller loss, tool timeout, base heartbeat loss, ObjectDB outage before and after revision resolution, task-lease heartbeat loss, and process signal.
5. Verify every failure code, stop action, recovery-required state, and run artifact.
6. Run supervised installed-hardware smoke tests at conservative profiles for each mounted arm/tool/base configuration.
7. Publish qualification state to plugin manifests only after artifacts pass validation.

## Interfaces and data

- Local test runner and manifest index
- Plugin qualification state
- Phase acceptance report

## Boundaries

- Does not include object perception or learned grasping
- Does not claim real qualification for unavailable hardware
- Does not loosen safety bounds to make tests pass

## Failure behavior

- Any unsafe continuation, false success, ignored cancel, missing artifact, or namespace collision blocks the phase.
- Performance misses remain measured defects; they do not silently change tolerances.

## Acceptance

- All public methods have success and failure fixtures.
- All simulator cases pass their declared tolerances.
- Concurrent Picker tests pass.
- Installed smoke tests stop safely under interruption.
- New task startup fails while an exclusive scan or stale-unverified lease exists; clean shutdown releases its lease exactly once.
- An already resolved fixture keeps using the same verified object revision through ObjectDB restart.
- The acceptance report links every result to configuration, source, and artifacts.

## Parallel work

Runs after all other Phase 02 packets.

## What this module needs from me

Access to installed configurations. No new product decision is required unless a vendor integration fails its contract.
