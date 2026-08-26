# Robot-side gateway services

## Goal

Keep NUC and Jetson roles narrow: acquire camera and robot/base state, expose health, relay bounded commands, and stop locally when desktop control disappears.

## Inputs

- Robot/camera/base profiles
- Vendor drivers
- Namespace/time contracts
- Compose gateway image
- Lifecycle and watchdog behavior

## Outputs

- Gateway launch profiles per host/robot
- Camera, arm, tool, and base relay inventory
- Local command watchdogs
- Gateway health summary
- Device ownership locks
- Disconnect/restart tests

## Work

1. Inventory which host owns each D455, arm controller connection, tool controller, base driver, and hardware network interface. One device has one writer.
2. Launch vendor drivers under the robot namespace with explicit endpoints, serials, frames, QoS, and controller generation.
3. Relay standard ROS state and accepted command/action interfaces. Avoid a new gateway-specific task API.
4. Implement local heartbeat/deadman for visual-servo velocity and base velocity. Expiry commands stop without waiting for the desktop.
5. Report device connection, controller state, camera rate, clock skew, command heartbeat, last error, and restart count.
6. On gateway restart, expose unavailable then initializing then ready. Reject cached or in-flight goals from the prior session.
7. Record a gateway manifest with host OS, kernel, CPU/GPU, driver, firmware, package, calibration, and source versions.

## Interfaces and data

- Namespaced vendor and standard ROS topics/actions
- Gateway diagnostics and heartbeat
- Device lock/ownership record
- Host profile

## Boundaries

- No perception, planning, grasp selection, task logic, or automatic task resume
- No hidden command buffering across disconnect

## Failure behavior

- Device loss, stale heartbeat, clock failure, duplicate owner, controller fault, and restart trigger local stop and unhealthy state.
- Reconnect returns ready only after fresh state and identity checks.

## Acceptance

- Killing desktop control stops velocity commands locally.
- Restarting a gateway does not resume an old trajectory or task.
- Camera and robot state recover with new timestamps and session identity.
- Duplicate device ownership is rejected.
- Health fields appear in run artifacts.

## Parallel work

Network and clock testing runs alongside gateway implementation.

## What this module needs from me

Facts: exact device-to-host mapping and host access.
