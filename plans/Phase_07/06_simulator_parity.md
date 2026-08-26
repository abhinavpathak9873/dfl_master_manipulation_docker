# Gazebo and Genesis parity

## Goal

Prove that both simulators support the same public task, controller, tool, camera, object, perception, alignment, cancellation, and reset contracts within declared numerical tolerances.

## Inputs

- Phase 00 simulator contract/matrix
- Phase 02 manipulation
- Phase 03 objects/scenes
- Phase 04 perception
- Phase 05 grasping
- Phase 06 scan fixtures where simulated capture is supported

## Outputs

- Twenty-four fixed-task parity results
- Representative four-object perception-to-grasp parity results
- Per-interface comparison table
- Tolerance and known-difference record
- Deterministic reset/replay evidence
- Release gate result

## Work

1. Run the identical fixed-task package for three robot profiles and four tools in both simulators.
2. Run one representative D455 scene through masks, pose, tracking/health, scene synchronization, local alignment, gripper verification, attach/lift/place, and reset in both modes.
3. Compare action lifecycle, error codes, namespaces, frames, timestamps, JointState, camera contract, gripper status, odometry, and run artifacts.
4. Measure joint/Cartesian endpoints, contact/attachment outcomes, simulated sensor characteristics, reset determinism, and real-time factor against simulator-specific tolerances.
5. Inject cancel, target loss, tool failure, base heartbeat loss, process death, and reset during active state.
6. Document differences in physics, contact, rendering, and performance. A difference is acceptable only when task-visible logical behavior and safety outcome remain the same.
7. Block Genesis release status if the official-emulator contract or required task behavior remains unmet.

## Interfaces and data

- Same external task packages and public API
- Simulator-specific launch/config only
- Parity report consumed by release

## Boundaries

- No requirement for identical pixels, latency, contacts, or physics values
- No simulator-specific branch in task source

## Failure behavior

- False success, ignored cancel, stale state, missing failure, or task-source branch blocks parity.
- A waived numerical difference needs documented task impact and approval.

## Acceptance

- All 24 fixed cases pass.
- Representative perception-to-grasp task passes in both modes.
- Failure injections produce equivalent typed outcomes and stops.
- Reset leaves no old attachment, command, track, or scene state.
- Report names every accepted difference.

## Parallel work

Runs with hardware qualification after all feature phases accept.

## What this module needs from me

Nothing unless Genesis fails; then return the evidence for scope review.
