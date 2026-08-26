# Doosan Jazzy migration

## Goal

Establish the official Jazzy driver, descriptions, emulator, controllers, and MoveIt assets as the supported arm baseline for M1013 and H2515. Keep project changes outside the vendor checkout.

## Inputs

- Pinned `doosan-robot2` source
- Core Jazzy image
- Current picker description and MoveIt packages
- Installed controller inventory when available

## Outputs

- Build report for the pinned vendor commit
- M1013 and H2515 description/MoveIt compatibility report
- DFL overlay package or configuration for names, ports, frames, tools, and controllers
- Real and virtual bringup commands with explicit host, port, RT host, model, controller generation, and namespace
- Vendor deviations and upstream issue links
- Cancel, stop, and protective-stop evidence

## Work

1. Build the vendor source for controller generation 2.x and 3.x as required by installed hardware. Record which build is used by each robot profile.
2. Compare official M1013/H2515 xacro, joint limits, kinematics, SRDF, controller names, and MoveIt pipelines with the current picker packages. Preserve DFL base and tool integration through overlays.
3. Remove hard-coded `/dsr01` assumptions from project-owned launch/configuration. Assign unique robot namespace, emulator port, controller manager, joint-state topic, and TF prefix from the profile.
4. Verify virtual RViz, virtual MoveIt, Gazebo, and real bringup separately. Treat planning success, controller activation, joint-state freshness, execution, cancel, and stop as distinct checks.
5. Record controller firmware, authority acquisition, servo-on state, safety state, and RT-control availability for each installed arm.
6. Create an upstream-difference ledger. Any vendor patch must be isolated, reproducible, and covered by a regression test.
7. Publish the accepted vendor interface facts to the simulator and motion contract packets.

## Interfaces and data

- Vendor ROS services/actions/topics and controller-manager namespace
- `FollowJointTrajectory` controllers consumed by MoveIt
- Joint states and robot-state TF
- Profile fields for model, host, port, RT host, controller generation, emulator port, and vendor launch arguments

## Boundaries

- Does not define the task-facing Python API
- Does not add gripper control beyond tool-description mounting
- Does not implement Genesis

## Failure behavior

- A successful compile does not pass the packet if controllers or joint states fail at runtime.
- Abort real execution on stale joint state, inactive controller, lost authority, protective stop, or model mismatch.
- Do not fall back from `real` to emulator mode.

## Acceptance

- Pinned source builds in the core image.
- M1013 and H2515 plan and execute a small virtual trajectory.
- Two M1013 emulator instances run together with unique names and ports.
- Real installed arms report fresh state, accept a bounded test trajectory, cancel it, and stop safely.
- No project file changes the vendor checkout.

## Parallel work

Profile inventory may proceed in parallel. Gazebo and task API work consume the accepted vendor facts.

## What this module needs from me

Facts: controller IPs, firmware generations, and a supervised hardware window. If real Jazzy execution is unsupported, return the evidence for a driver-scope decision.
