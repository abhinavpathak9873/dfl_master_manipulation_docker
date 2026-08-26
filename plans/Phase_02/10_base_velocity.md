# Bounded mobile-base velocity control

## Goal

Provide enough base integration to move Picker 1 or Picker 2 through namespaced velocity commands while retaining immediate stop, odometry visibility, and deadman protection.

## Inputs

- Zinger base driver and current picker bringup
- Namespace/time contract
- Robot lifecycle
- Run-record API

## Outputs

- `Base` task facade with `command_velocity`, `stop`, and odometry/state access
- Namespaced TwistStamped command and Odometry contract
- Velocity/acceleration limits per picker profile
- Desktop and gateway watchdogs
- Gazebo/Genesis base adapters
- Failure and smoke tests

## Work

1. Port the correct installed Zinger driver and record its command topic, odometry, joint states, enable/disable path, and hardware faults.
2. Expose bounded linear-x and angular-z commands with required duration or an explicit streaming context. Clamp only within a declared profile; out-of-range requests fail.
3. Stamp every velocity command and include run/session identity where the gateway can verify it.
4. Stop when duration expires, the publisher heartbeat is stale, lifecycle stops, task raises, network is lost, or the gateway rejects a command.
5. Publish odometry and base health under the robot namespace. Task code may inspect them but v1 provides no pose-goal or route planner.
6. Implement equivalent simulator command, odometry, watchdog, and reset behavior.
7. Record requested and measured velocity plus stop latency in run artifacts.

## Interfaces and data

- `robot.base.command_velocity(...)`, `stop()`, `odometry()`
- Namespaced `geometry_msgs/TwistStamped`, `nav_msgs/Odometry`, diagnostics
- Gateway deadman settings

## Boundaries

- No Nav2, global localization, path planning, obstacle avoidance, or base-arm coordination
- Does not accept an unbounded raw `cmd_vel` publication from task code

## Failure behavior

- Stale command, missing odometry, driver fault, excessive measured velocity, network loss, and stop timeout raise typed base/control errors.
- Unknown motion state blocks subsequent arm tasks that require a stationary base.

## Acceptance

- Bounded forward, reverse, and rotation tests stop on duration.
- Killing the desktop publisher stops the simulated and installed base within the recorded bound.
- Picker 1 and Picker 2 topics do not collide.
- Odometry timestamps and frames follow the Phase 01 contract.
- Arm motion can run after a verified stationary-base check.

## Parallel work

Independent of gripper packets. Concurrent robot integration consumes it.

## What this module needs from me

Facts: installed base driver topics, limits, and hardware access.
