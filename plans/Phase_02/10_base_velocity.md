# Bounded mobile-base velocity control

## Goal

Expose the existing Picker mobile bases through a small safe velocity primitive
without importing a navigation framework.

## Task-script payoff

Picker tasks can use `robot.base.move_velocity(...)`, inspect odometry/state, and
stop explicitly while H2515 simply exposes no base.

## Work

1. Characterize the Zinger/base driver topics, frames, limits, watchdog, odometry,
   reconnect, and current bringup for Picker 1 and Picker 2.
2. Define bounded linear/angular velocity and duration plus immediate `stop`.
3. Validate finite commands, per-profile limits, namespace, current state, and
   mode support before motion.
4. Use the driver/gateway watchdog for real hardware and equivalent timeout/stop
   behavior in both simulators.
5. Keep odometry and diagnostics accessible; do not create a second base-state
   protocol.
6. Test timeout, process loss, network loss, zero command, repeated stop,
   namespace isolation, and concurrent arm state.
7. Document that navigation and coordinated base-arm planning are separate future
   needs, not hidden inside velocity control.

## Acceptance

- Both Pickers move/stop within declared limits in Gazebo and Genesis.
- Real watchdog behavior is measured before qualification.
- H2515 gives a clear missing-component error.
- Two bases receive only their namespaced commands.

## Non-goals

Nav2, mapping, path planning, fleet scheduling, or coordinated whole-body
planning.
