# CaP-X agent-interface audit

## Purpose

Study [CaP-X](https://github.com/capgym/cap-x) for ways to make manipulation operations discoverable, composable, and testable by coding agents. CaP-X remains a reference. It is not installed as the DFL runtime and does not determine repository structure, simulator choice, or task semantics.

## Patterns to borrow

### Small named skills

Expose a compact catalogue of task primitives with stable names, typed inputs, explicit outputs, failure cases, and one minimal example. The DFL equivalent is the generated module index plus task API documentation. Each entry points to its ROS implementation and contract tests.

### Fixtures before open-ended tasks

Give every public primitive a deterministic fixture or recorded-data case. Fixed pose motion, planner selection, segmentation, pose estimation, tracking, grasp selection, and failure handling each need a small runnable example before end-to-end task evaluation.

### Observable evaluation

Evaluate task outcomes from recorded artifacts rather than prose claims. A run manifest identifies the task, configuration, implementation IDs, object revisions, stages, result codes, timing, and evidence files. Acceptance scripts read that manifest and produce a pass/fail report.

### Limited agent context

Assign one work packet with its accepted upstream inputs. The agent should not load the whole planning pack. If its work changes a shared contract, it stops and returns to the owning contract packet.

### Explicit capability registry

Provide a generated catalogue that lists installed planners, grippers, perception backends, trackers, simulators, and scenes. The catalogue is documentation over the plugin manifests, not a second registry.

## Patterns to reject

- Do not replace ROS 2 nodes, actions, services, TF, MoveIt, launch, or rosbag with a Code-as-Policy runtime.
- Do not adopt CaP-X simulator, environment, dependency, or monorepo layout.
- Do not execute generated Python against real hardware without the normal typed API, preflight, launch ownership, and gateway watchdogs.
- Do not let an evaluator define robot safety. Hardware stop, freshness, and controller limits remain runtime contracts.
- Do not turn every primitive into a high-level autonomous skill. Task scripts retain the explicit manipulation sequence.

## Outputs to feed into later plans

- Phase 01 defines the plugin catalogue, typed examples, task-package convention, and run manifest.
- Phase 02 documents one fixture per motion and gripper primitive.
- Phases 03–06 add object, perception, tracking, alignment, and scanning fixtures.
- Phase 07 generates the module index and release evaluation runner from accepted manifests and documentation.

## Acceptance

- Every adopted pattern maps to a concrete DFL artifact and owning packet.
- Every rejected pattern is absent from runtime dependencies and workspace layout.
- An agent can find one capability, its configuration, ROS graph, fixture, and acceptance command without reading unrelated phase files.
- The audit creates no CaP-X runtime dependency.

## What this audit needs from me

Nothing.
