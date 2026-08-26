# Phase 01 — shared contracts

## Goal

Freeze the small set of values, ROS interfaces, configuration rules, plugin metadata, names, time rules, task layout, and run records used by every later package. This phase prevents each integration from inventing its own dictionaries, IDs, namespaces, or failure vocabulary.

## Settled decisions

- Use typed Python values and typed exceptions.
- Prefer standard ROS messages and actions; add custom IDL only for missing semantics.
- Task code selects robot, gripper, scene, mode, and pipeline; validated files hold detailed settings.
- Use plugin discovery with stable IDs and contract versions.
- All robot topics and frames are namespaced.
- Every run writes a manifest and structured events; failure retains a bounded data buffer.
- Object resolution, runtime leases, scanning, and reconstruction use typed cross-container ROS contracts.

## Work packets

| Packet | Result |
|---|---|
| [01](01_python_value_types.md) | Immutable Python values, results, and failure taxonomy. |
| [02](02_ros_interfaces.md) | Minimal standard/custom ROS wire contract. |
| [03](03_config_resolution.md) | Deterministic layered configuration and validation. |
| [04](04_plugin_discovery.md) | Inspectable C++/Python extension registration. |
| [05](05_namespaces_tf_and_time.md) | Namespace, frame, unit, timestamp, and freshness rules. |
| [06](06_task_package_convention.md) | External task package shape and one-command execution. |
| [07](07_run_records.md) | Run manifests, event logs, metrics, and failure buffers. |

## Order and parallel work

Packets 01, 03, and 05 start after the Phase 00 simulator contract. Packet 02 consumes their IDs and failure semantics. Packet 04 consumes 01 and 03. Packet 06 consumes 01, 03, and 05. Packet 07 consumes the value and namespace contracts and may finish alongside 06. Freeze all public artifacts together and run cross-package contract tests before Phase 02.

## Upstream inputs

- Phase 00 accepted simulator contract and profiles
- Global decisions
- Source and dependency research

## Exit criteria

- The Python values and error codes serialize without implementation-specific dictionaries.
- The custom ROS IDL set is minimal and passes generated-language builds.
- Task/scan lease and scan/reconstruction action fixtures reject stale epochs and oversized payloads.
- A resolved configuration is deterministic, validated, printable, and saved in the run manifest.
- A sample C++ plugin and Python plugin pass the same registry checks.
- Picker 1 and Picker 2 have non-colliding topics, frames, actions, and diagnostics.
- A sample task runs through one command and produces a complete success and failure record.

## What this phase needs from me

Nothing. Hardware facts remain owned by Phase 00 and Phase 07.
