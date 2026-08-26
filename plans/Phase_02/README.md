# Phase 02 — manipulation API and control

## Goal

Expose the complete declared robots, tools, bases, planners, servo primitives,
and concurrency through a small task-readable API.

## Task-script payoff

A developer writes `robot.arm.move_pose(...)`, `robot.gripper.close(...)`,
`robot.base.move_velocity(...)`, and ordinary recovery code while retaining
direct access to MoveIt, controllers, and vendor backends.

## Required scope

- Picker 1/M1013, Picker 2/M1013, and H2515.
- VGC10 one cup, VGC10 four cups, VGP20, and 2FG14.
- Gazebo, Genesis, and commissioned real paths.
- Bringup/attach/cleanup, Pilz, OMPL, relative/force-aware motion, visual servo,
  both Picker bases, and concurrent Picker operation.

## Packets

1. [Robot lifecycle](01_robot_lifecycle.md)
2. [Motion API](02_motion_contract.md)
3. [Pilz PTP/LIN/CIRC](03_pilz_motion.md)
4. [OMPL and explicit fallbacks](04_ompl_and_fallbacks.md)
5. [Visual servo](05_visual_servo.md)
6. [Gripper API](06_gripper_contract.md)
7. [VGC10 profiles](07_vgc10_profiles.md)
8. [VGP20](08_vgp20.md)
9. [2FG14](09_2fg14.md)
10. [Base velocity](10_base_velocity.md)
11. [Concurrent robots](11_concurrent_robots.md)
12. [Manipulation acceptance](12_manipulation_acceptance.md)

## Smallest sufficient design

- One convenient Robot factory plus directly importable concrete robots.
- Components reflect actual hardware structure.
- Shared APIs cover repeated behavior; backend-specific methods remain allowed.
- Task Python owns planner choices, retries, and recovery.
- Safety stays at robot/controller/gateway seams; no ObjectDB lease or lifecycle
  platform is required.

## Exit evidence

Readable task scripts demonstrate the declared manipulation matrix, expected
results/errors, safe stop/cancel, namespaces, and supervised real behavior for
installed combinations.

## Non-goals

Opaque pick/place automation, capability negotiation, resource scheduling, or a
controller-of-controllers.
