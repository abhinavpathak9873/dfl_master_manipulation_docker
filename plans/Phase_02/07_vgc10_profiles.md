# VGC10 one-cup and four-cup profiles

## Goal

Support the two VGC10 physical configurations as distinct geometry and grasp profiles over one qualified vacuum driver.

## Inputs

- Shared gripper contract
- Current picker VGC10 descriptions and controller services
- Object grasp-profile schema draft
- Simulator suction contract

## Outputs

- `onrobot_vgc10_1cup` and `onrobot_vgc10_4cup` profiles
- URDF/xacro overlays, TCPs, payload, and collision geometry
- Vacuum driver plugin and channel mapping
- Vacuum/object-held status policy
- Gazebo and Genesis tool models
- Hardware commissioning tests

## Work

1. Inventory the actual VGC10 controller/service interface, channel control, pressure/vacuum feedback, release behavior, response bounds, and diagnostic states.
2. Keep one-cup and four-cup mounts separate. Record cup positions, active channels, TCP, collision volume, payload, and compatible grasp-profile IDs.
3. Map `grip` to configured vacuum targets/channels and `release` to the vendor-supported vent/off sequence. Report achieved vacuum and object-held evidence when available.
4. Define degraded behavior when only command acknowledgment is available. Such a driver cannot claim object detection and must require task-level verification.
5. Implement simulator attachment from cup contact, orientation, configured seal rules, and vacuum state. Release clears the attachment.
6. Test interrupted grip, failed seal, pressure loss during lift, reconnect, and repeated release.
7. Record commissioned robot/tool pairings without preventing other combinations in simulation.

## Interfaces and data

- Shared Gripper plugin
- Vendor suction services/topics
- Tool profile IDs and grasp-profile compatibility
- Simulated vacuum state

## Boundaries

- Does not share geometry between one-cup and four-cup variants
- Does not infer held object solely from command success

## Failure behavior

- Return typed seal, timeout, pressure-loss, connection, and unsupported-feedback failures.
- Pressure loss during an active task publishes tool health immediately.

## Acceptance

- Both profiles produce distinct robot descriptions and TCPs.
- Shared gripper tests pass in Gazebo and Genesis.
- A failed simulated seal is observable and does not attach the object.
- Installed VGC10 passes open/grip/status/release/stop smoke tests.
- Grasp selection rejects anchors for the wrong VGC10 geometry.

## Parallel work

Runs with VGP20 and 2FG14 packets.

## What this module needs from me

Facts: actual channel plumbing, mounted cup layout, and feedback available on installed VGC10 units.
