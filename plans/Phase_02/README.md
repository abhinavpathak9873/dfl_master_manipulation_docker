# Phase 02 — manipulation API and control

## Goal

Build the explicit task-facing API on the frozen Phase 01 contracts. Preserve the proven DFF motion and visual-servo behavior where it is safe, remove hidden orchestration, support the four gripper profiles, and make concurrent robot ownership predictable.

## Settled decisions

- Normal motion calls plan and execute; separate plan and execute remain public.
- Each motion selects Pilz PTP/LIN/CIRC or OMPL and may declare an ordered fallback.
- Fallback is permitted only after planning failure and before execution begins.
- Task code owns the manipulation sequence and recovery branches.
- `Robot.bringup()` owns a normal ROS launch session; attach mode is explicit.
- Task lifecycle acquires and heartbeats a runtime lease; ObjectDB outage prevents new task startup but does not invalidate an already resolved immutable run.
- No default real-motion prompt.
- Visual-servo target loss commands zero, holds for a bound, attempts bounded reacquisition, then fails.
- Base support is bounded velocity, odometry, watchdog, and stop; no navigation.

## Work packets

| Packet | Result |
|---|---|
| [01](01_robot_lifecycle.md) | One-command owned bringup, attach, preflight, and cleanup. |
| [02](02_motion_contract.md) | Typed plan/execute and combined motion API. |
| [03](03_pilz_motion.md) | Qualified PTP, LIN, and CIRC behavior. |
| [04](04_ompl_and_fallbacks.md) | Collision-aware OMPL and visible fallback ordering. |
| [05](05_visual_servo.md) | Characterized, bounded, observable position/velocity servoing. |
| [06](06_gripper_contract.md) | Shared tool capabilities, commands, status, and errors. |
| [07](07_vgc10_profiles.md) | VGC10 one-cup and four-cup drivers and geometry. |
| [08](08_vgp20.md) | VGP20 driver, geometry, feedback, and qualification. |
| [09](09_2fg14.md) | 2FG14 width/force driver and object-detection behavior. |
| [10](10_base_velocity.md) | Namespaced bounded `cmd_vel`, odometry, deadman, and stop. |
| [11](11_concurrent_robots.md) | Simultaneous Picker 1 and Picker 2 operation. |
| [12](12_manipulation_acceptance.md) | Phase integration and failure-injection report. |

## Order and parallel work

Implement lifecycle and the motion contract first. Pilz and OMPL can proceed together after the motion request/result types freeze. Visual servo begins with characterization and then uses the motion stop contract. The gripper contract precedes the three tool packets, which may run in parallel. Base velocity is independent after lifecycle and namespace contracts. Concurrent integration waits for lifecycle, motion, and at least one tool. Acceptance runs last.

## Upstream inputs

- Phase 00 simulator and vendor contracts
- All frozen Phase 01 contracts
- Current DFF manipulation characterization sources

## Exit criteria

- One explicit task source runs against Picker 1, Picker 2, or H2515 by changing selectors.
- Plan preview and execution use immutable plan identity and current-state validation.
- Pilz, OMPL, and declared fallback outcomes are observable in results and artifacts.
- Visual servo stops safely on stale or lost targets and never blind-finishes.
- All tool drivers pass shared contract tests in both simulators; installed tools pass supervised smoke tests.
- Picker 1 and Picker 2 operate concurrently without shared process, action, TF, or controller ownership.
- Injected failures return typed codes and leave a complete run record.
- Lease acquisition, heartbeat loss, clean release, and stale fail-closed behavior pass against a contract server fixture.

## What this phase needs from me

Facts: mounted tool and hardware access for driver smoke tests. Decisions: none unless a vendor API cannot provide the required state or stop behavior.
