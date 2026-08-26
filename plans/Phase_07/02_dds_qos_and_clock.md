# DDS discovery, QoS, bandwidth, and clock

## Goal

Select and configure one reliable ROS middleware path for the trusted wired lab LAN without adding SROS2, VPN, or an unnecessary network framework.

## Inputs

- Current DFF Cyclone DDS evidence
- ROS 2 Jazzy Fast DDS and Cyclone DDS packages
- Camera and robot topic rates
- Host/network inventory
- TF freshness requirements

## Outputs

- Measured Fast DDS vs Cyclone DDS comparison
- Selected RMW and versioned profile
- ROS_DOMAIN_ID and interface binding convention
- QoS table
- Chrony configuration and clock-health check
- Bandwidth/reconnect/failure report

## Work

1. Measure `rmw_cyclonedds_cpp` and `rmw_fastrtps_cpp` on the actual LAN using the same D455, joint state, TF, diagnostics, and command workloads.
2. Select the implementation that passes discovery, throughput, p95 latency, reconnect, CPU, and loss tests. Prefer the already-characterized Cyclone path if results are equivalent.
3. Use one explicit ROS_DOMAIN_ID for the deployment and bind to the intended wired interface. Reject accidental Wi-Fi, VPN, loopback-only, or duplicate-domain configuration.
4. Document QoS per topic class. Keep sensor streams bounded; keep actions, controller state, health, and required metadata reliable.
5. Use Chrony on real hosts with one declared lab time source. Require measured host skew no greater than 5 ms for perception-to-motion readiness; record tighter observed values.
6. Test multicast discovery, late join, host restart, switch disconnect, saturated camera bandwidth, dropped packets, and duplicate robot namespaces.
7. Provide a concise local connectivity command that checks peers, topic rates, QoS compatibility, clock skew, and required TF.

## Interfaces and data

- RMW configuration
- DDS XML/profile
- ROS_DOMAIN_ID
- QoS profile names
- Chrony and clock-health output

## Boundaries

- No SROS2, VPN, cloud relay, or Zenoh in v1
- No assumption that matching domain IDs alone proves connectivity

## Failure behavior

- Block readiness on missing required peer, incompatible QoS, duplicate namespace, excessive clock skew, or unusable camera rate.
- Network loss triggers gateway watchdogs and typed desktop health.

## Acceptance

- Selected RMW passes all workload/reconnect cases.
- D455 stream plus robot state stays within measured LAN capacity.
- Required actions and state survive late join/restart as designed.
- Clock skew remains within 5 ms during qualification.
- The connectivity check identifies each injected fault.

## Parallel work

Runs with gateway services and feeds desktop Compose.

## What this module needs from me

Facts: wired interface names, switch topology, IP assignments, and preferred lab time source.
