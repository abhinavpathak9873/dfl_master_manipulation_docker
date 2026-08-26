# Gazebo Harmonic with the Doosan emulator

## Goal

Make Gazebo Harmonic the reliable primary simulator for the complete declared
robot/tool matrix using the real ROS/controller paths wherever practical.

## Task-script payoff

Changing `mode="real"` to `mode="gazebo"` preserves useful task calls and keeps
ROS topics, TF, controllers, camera data, and gripper state directly visible.

## Retained scope

- Picker 1, Picker 2, H2515, both mobile bases where present, four tools, D455,
  scenes, MoveIt, contact/force behavior where honestly simulatable.
- Official Doosan emulator integration and Gazebo Harmonic/Jazzy compatibility.
- Namespaced single- and dual-Picker launches.

## Work

1. Build the official emulator/Gazebo path in the core image and document exact
   launch arguments.
2. Spawn each robot/tool description with correct joints, TCP, collision model,
   controllers, frames, and namespace.
3. Bridge simulated joint state, command, tool state, camera RGB-D/info, clock,
   contacts, and base state through standard ROS mechanisms.
4. Implement only simulator glue that maps Gazebo behavior to the real adapter's
   useful ROS surface; keep it in a recognizable simulation folder.
5. Define honest force/contact and suction/width approximations and mark data the
   simulator cannot reproduce.
6. Run fixed home, joint, Cartesian, gripper, camera, base, cancel, stop, and
   collision tasks.
7. Capture direct ROS diagnostic commands for common failures.

## Outputs

- Gazebo launch/profile support for all 12 robot/tool selections.
- Simulator behavior/limitation table.
- Fixed task scripts and compact evidence.
- Namespaced dual-Picker smoke path.

## Acceptance

- All declared models spawn without invalid TF, joints, or collision geometry.
- Arm/tool/base/camera paths use the same task calls expected by real mode.
- Stop/cancel and unsupported force behavior are explicit.
- Picker 1 and Picker 2 can coexist without graph collisions.
- Failures can be traced through task -> adapter -> ROS/MoveIt/Gazebo.

## Non-goals

- Photorealism, perfect hardware equivalence, or a Gazebo-specific task API.
- A general simulator manager.
