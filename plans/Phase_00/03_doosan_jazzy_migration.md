# Doosan Jazzy migration

## Goal

Provide direct, inspectable Jazzy support for the M1013 arms used by Picker 1
and Picker 2 and for the separate H2515 robot.

## Task-script payoff

`Robot(model="picker1"|"picker2"|"h2515", ...)` reaches the correct Doosan
description, controllers, MoveIt groups, emulator, and real driver without
changing the manipulation sequence.

## Retained scope

- Pinned `doosan-robot2` Jazzy source and required local description overlays.
- M1013 and H2515 URDF/xacro, SRDF, joint limits, controllers, MoveIt, emulator,
  real-driver, IO, and state behavior.
- Namespaced Picker 1/Picker 2 use and clear H2515 differences.

## Work

1. Build the pinned upstream packages in the core Jazzy image and record any
   minimal patches.
2. Compare current DFL descriptions, frames, joints, groups, limits, controllers,
   services/actions, IO, and launch arguments with upstream.
3. Move only DFL-specific mounts, base composition, tools, camera, calibration,
   and scenes into small overlays.
4. Verify the official emulator and real driver expose equivalent useful state
   and command paths where expected.
5. Ensure launch accepts robot namespace, TF prefix, mode, tool description, and
   scene without global-name collisions.
6. Characterize motion result, stop, cancel, force/IO availability, disconnect,
   and startup readiness for both models.
7. Keep upstream launch and ROS interfaces reachable for direct debugging.

## Outputs

- Reproducible M1013/H2515 Jazzy build and minimal overlay list.
- Robot description/controller/MoveIt launch paths for simulation and reality.
- Behavior and limitation table consumed by the robot adapter packets.
- Evidence for multi-robot namespacing and safe stop.

## Acceptance

- Both M1013 profiles and H2515 load with correct joints, groups, limits, and TF.
- Emulator motion and cancellation are observable through standard ROS tools.
- Real-mode assumptions are documented and never claimed without hardware
  evidence.
- Picker 1 and Picker 2 can coexist without global Doosan names.

## Non-goals

- Reimplementing Doosan drivers or hiding them behind a second middleware.
- Pretending M1013 and H2515 are identical where hardware behavior differs.
