# Genesis emulator-backed bridge spike

## Goal

Determine and implement the smallest viable Genesis route that preserves the
useful task-facing and ROS behavior required by the full simulator matrix.

## Task-script payoff

A task can switch to `mode="genesis"` without rewriting its robotics sequence,
while Genesis-specific limitations remain clear and debuggable.

## Evidence question

Can the official Doosan emulator/controller remain authoritative while Genesis
provides physics and sensors? If not, what smallest direct Genesis adapter can
preserve command/state/TF/tool/camera behavior without inventing a simulation
framework?

## Work

1. Pin Genesis and its Python/GPU dependencies in an isolated image.
2. Load M1013 and H2515 plus all four tool descriptions with verified joint,
   inertial, collision, TCP, and frame mappings.
3. Prototype the emulator-in-loop route for joint command/state, stop/cancel,
   tool IO/state, base behavior, D455-equivalent RGB-D, TF, and `/clock`.
4. Compare command/state traces and fixed-task outcomes with Gazebo.
5. Measure update rate, latency, timestamp behavior, reset behavior, GPU memory,
   contact/force usefulness, and multi-robot namespace behavior.
6. If the emulator route fails, document the concrete failure and smallest
   direct bridge alternative, including task-visible differences.
7. Return for review only if a material capability cannot be preserved; do not
   silently drop Genesis or any robot/tool combination.
8. Preserve full visual meshes while converting only collision assets that the
   Genesis URDF parser cannot load. Render all 12 selections at the shared home
   pose and inspect them against Gazebo.

## Outputs

- Reproducible Genesis image/profile and spike code plan.
- Accepted bridge decision with measured evidence.
- Required adapter/description work for the 24-run matrix.
- Honest limitations and direct debugging path.
- Twelve direct Genesis captures using the implemented URDF, not concept art.

## Acceptance

- One M1013 task and one H2515 task exercise motion, tool state, camera/TF/time,
  stop, and reset.
- The chosen route has bounded, measured timing and clear failure behavior.
- The decision names no speculative generalized simulator interface.
- Remaining work for Picker 1, Picker 2, H2515, and four tools is explicit.
- Visual fidelity and physics fidelity are reported separately.

## Non-goals

- Rewriting the whole Doosan stack during the spike.
- Treating one successful pose command as proof of parity.
