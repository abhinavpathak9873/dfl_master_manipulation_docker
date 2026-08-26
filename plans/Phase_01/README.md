# Phase 01 — lightweight shared seams

## Goal

Add only the small values and ROS-facing rules repeatedly needed by concrete
robotics integrations. Do not freeze a generalized framework before tasks use it.

## Task-script payoff

The canonical task can create readable poses/joints, select backends, pass named
robotics inputs, run as ordinary Python, and receive clear results/errors.

## Packets

1. [Python values, results, and errors](01_python_value_types.md)
2. [Only-needed ROS interfaces](02_ros_interfaces.md)
3. [Visible configuration](03_config_resolution.md)
4. [Direct backend mapping](04_plugin_discovery.md)
5. [Namespaces, TF, units, and time](05_namespaces_tf_and_time.md)
6. [Task-script convention](06_task_package_convention.md)
7. [Useful run/debug records](07_run_records.md)

## Smallest sufficient design

- Lightweight Python values with ROS conversions only at ROS seams.
- Standard ROS messages/actions/services before custom IDL.
- Constructor arguments for task choices; small files for shared physical facts.
- Source-controlled dictionaries mapping backend IDs to implementation files.
- Normal `tasks/*.py` control flow; ROS packaging only when genuinely necessary.
- Opt-in debug evidence and qualification records, not an observability platform.

## Exit evidence

- The canonical API example is representable without generic `input=[...]`,
  runtime contexts, registries, providers, or workflow definitions.
- A Python backend can be added through one implementation file and one mapping.
- Picker namespaces/TF/time work in the actual Phase 00 integrations.
- Custom ROS interfaces, if any, each name a concrete cross-process need.
- A task runs without a run-record daemon or ObjectDB service.

## Non-goals

- Universal contracts for future robots/algorithms.
- Plugin ecosystems, configuration services, event platforms, or lifecycle
  infrastructure.
