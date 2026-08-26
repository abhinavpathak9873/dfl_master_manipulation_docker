# Robot-side gateway processes

## Goal

Run only hardware/device responsibilities that must live on the NUC or Jetson,
with ROS-visible state and bounded command safety.

## Task-script payoff

The desktop task uses the same robot/camera/base API while developers can trace a
failure directly to the namespaced gateway ROS node and vendor/device driver.

## Work

1. Inventory each Picker/robot host, OS, architecture, devices, vendor libraries,
   cameras, base/arm/tool connections, network, and current launch.
2. Place a driver on a gateway only when device locality, vendor support,
   bandwidth, or safety requires it; keep planning/perception/task policy on the
   desktop.
3. Define small namespaced launch sets for required arm state/command relay,
   base, tool, camera, hardware diagnostics, and heartbeat/watchdog.
4. Prefer native ROS/vendor interfaces and normal diagnostics. Do not introduce a
   generic gateway protocol.
5. Make command watchdogs stop velocity/servo paths on heartbeat/network/process
   loss; discrete trajectory behavior follows controller/vendor safety evidence.
6. Pin gateway images/sources per architecture and expose direct logs/ROS CLI.
7. Test boot/start/stop, duplicate namespace, desktop disconnect/reconnect,
   gateway restart, stale commands, and device loss.
8. Document which commands are safe to repeat and which require fresh task state.

## Acceptance

- Gateways expose only their required device/state/command responsibilities.
- Loss of desktop command trust reaches measured safe stop behavior.
- Restart does not resume old motion or claim previous commands succeeded.
- Picker 1 and Picker 2 remain independently attributable.
- No desktop intelligence is duplicated on gateways.

## Non-goals

A general edge platform, custom RPC layer, remote task runner, or fleet manager.
