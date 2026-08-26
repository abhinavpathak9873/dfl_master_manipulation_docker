# DDS discovery, QoS, bandwidth, and clock

## Goal

Make ordinary ROS 2 communication predictable on the trusted lab LAN using
measured settings and direct diagnostics.

## Task-script payoff

Robot state, commands, D455 streams, TF, and perception stay current across hosts,
and failures can be diagnosed with ROS/DDS/network tools rather than hidden
middleware.

## Work

1. Inventory desktop, NUC, Jetson, NICs, switches, addresses/hostnames, MTU,
   multicast/firewall behavior, and clock sources.
2. Choose one documented RMW implementation and `ROS_DOMAIN_ID` for the lab; keep
   alternative changes explicit.
3. Set QoS per real topic semantics: sensor streams, state, TF static/dynamic,
   commands, actions/services, and diagnostics.
4. Measure bandwidth and latency for D455 RGB-D, TF, state, commands, perception,
   and simultaneous Picker operation.
5. Configure stable host identity and chrony/PTP/NTP as appropriate; measure
   offset/jitter and define freshness bounds used by tasks.
6. Test discovery after staggered startup, host restart, link interruption,
   packet loss, duplicate namespaces, clock jump, and mixed sim/wall time.
7. Provide exact `ros2`, `ddsperf`/network, clock, route, and topic commands for
   diagnosis.
8. Keep large raw data local to its consumer when network cost justifies a real
   process boundary.

## Acceptance

- Required nodes discover consistently and namespaces remain unique.
- Command/state/control latency and clock offset stay within measured task
  bounds.
- Sensor QoS avoids presenting stale queued images as live.
- Network loss leads to the intended gateway/task stop and explicit recovery.
- No second communications/control plane is added.

## Non-goals

SROS2/VPN/cloud networking in the initial lab scope, or dynamic network
orchestration.
