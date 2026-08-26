# Phase 05 — local alignment and closed-loop grasping

## Goal

Turn a healthy coarse track and revision-bound grasp anchor into a verified grasp through the proven close-range reference/depth method and bounded visual servo. Keep retries explicit and stop after uncertain contact or state loss.

## Settled decisions

- Port the proven reference/mask/depth alignment behavior before redesigning it.
- Local alignment returns a typed correction and health; it does not move the robot.
- Task code calls alignment, servo, gripper, verification, and recovery primitives explicitly.
- Default retry count is zero. A task may declare bounded retries for named pre-contact failures.
- Blind finish and automatic resume are prohibited.
- Installed tasks use 30 trials, at least 29 successes, and zero unsafe events.

## Work packets

| Packet | Result |
|---|---|
| [01](01_alignment_contract.md) | Tracker-independent local-correction request/result. |
| [02](02_legacy_characterization.md) | Black-box behavior and fixture record from the current system. |
| [03](03_reference_depth_alignment.md) | Ported close-range correction implementation. |
| [04](04_bounded_visual_servo.md) | Safe correction-to-motion orchestration. |
| [05](05_grasp_verification.md) | Tool-specific held-object evidence. |
| [06](06_retry_and_recovery.md) | Explicit retry classes and recovery-required states. |
| [07](07_grasp_acceptance.md) | End-to-end simulation and hardware qualification. |

## Order and parallel work

Define the alignment contract and characterize the current behavior together. Implement the reference/depth backend after both stabilize. Bounded servo consumes the backend and Phase 02 controller. Grasp verification uses the gripper contract and may proceed in parallel. Retry/recovery follows the failure vocabularies. Acceptance runs last.

## Upstream inputs

- Phase 02 motion, visual-servo, and gripper contracts
- Phase 03 object/grasp records and MoveIt scene
- Phase 04 track health and D455 dataset
- Current local-alignment implementation and approved references

## Exit criteria

- Alignment results are revision-, anchor-, camera-, and timestamp-bound.
- The port matches accepted characterization fixtures or documents justified differences.
- Target loss produces zero command and typed failure.
- Grasp verification distinguishes actuator completion from object held.
- Only declared pre-contact failures may retry.
- Representative installed tasks meet 29/30 with zero unsafe events.

## What this phase needs from me

Access to the representative objects, installed tools, and supervised robot trials. No remaining policy decision.
