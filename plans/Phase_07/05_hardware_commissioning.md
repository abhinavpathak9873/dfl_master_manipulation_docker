# Hardware commissioning records

## Goal

Record and verify the concrete physical facts required to operate each installed
robot, tool, base, and camera safely.

## Task-script payoff

Selecting a real profile either reaches verified mounted hardware/calibration and
limits or fails before motion with the exact missing commissioning fact.

## Work

1. Create readable per-installation records for Picker 1/M1013, Picker 2/M1013,
   H2515, bases, D455 cameras, VGC10 one/four cup, VGP20, and 2FG14 as installed.
2. Verify serial/identity, host/network, namespace, firmware/driver, description,
   joint/tool limits, mount/TCP, payload, collision geometry, IO, and stop path.
3. Measure base limits/watchdog, arm motion/stop, gripper open/close/stop/feedback,
   camera streams/depth scale, TF, and time sync.
4. Calibrate robot/base/tool/camera relationships with provenance, date, method,
   uncertainty, and responsible operator.
5. Distinguish simulated support, installed-uncommissioned, commissioned, and not
   physically mounted. Do not erase required profiles because a combination is
   currently unmounted.
6. Use conservative supervised scripts that expose underlying ROS/vendor state.
7. Store records in the established calibration/config/data layout and reference
   them from profiles.
8. Define re-commission triggers after mount, calibration, firmware, network,
   driver, damage, or major dependency changes.

## Acceptance

- Every installed component has an identity-to-profile match and current evidence.
- Wrong/missing tool, calibration, limits, or endpoint blocks real motion clearly.
- Stop/watchdog behavior is measured, not assumed.
- Records are inspectable files, not entries in a configuration service.

## Non-goals

Automatic hardware inventory, asset management platform, or claiming unmounted
combinations as real-tested.
