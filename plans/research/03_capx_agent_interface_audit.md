# CaP-X agent-interface audit

## Purpose

Study [CaP-X](https://github.com/capgym/cap-x) for ways to make manipulation operations discoverable, composable, and testable by coding agents. CaP-X remains a reference. It is not installed as the DFL runtime and does not determine repository structure, simulator choice, or task semantics.

## Patterns to borrow

### Small named skills

Expose a compact handwritten index of task primitives with stable names,
meaningful inputs, explicit outputs, failure cases, and one minimal example.
Each entry points directly to its implementation file, ROS boundary when one
exists, and focused tests.

### Fixtures before open-ended tasks

Give every public primitive a deterministic fixture or recorded-data case. Fixed pose motion, planner selection, segmentation, pose estimation, tracking, grasp selection, and failure handling each need a small runnable example before end-to-end task evaluation.

### Observable evaluation

Evaluate named benchmarks and qualification tasks from recorded artifacts rather
than prose claims. A small local record identifies the selected setup, object
revision, stages, results, timing, and evidence needed by that check. Ordinary
experiments can run without recording.

### Limited agent context

Assign one work packet with its concrete inputs. The agent should start from the
canonical task and nearest robotics module, then read only relevant sources. If
work changes a shared API or file format, update its owning packet and consumers
together.

### Direct capability map

Provide a small handwritten index and source-controlled mappings that list the
robots, grippers, perception backends, trackers, simulators, and scenes actually
present. Do not generate a catalogue or maintain plugin manifests.

## Patterns to reject

- Do not replace ROS 2 nodes, actions, services, TF, MoveIt, launch, or rosbag with a Code-as-Policy runtime.
- Do not adopt CaP-X simulator, environment, dependency, or monorepo layout.
- Do not execute generated Python against real hardware without the normal API,
  preflight, launch ownership, controller limits, and required gateway watchdogs.
- Do not let an evaluator define robot safety. Hardware stop, freshness, and
  controller limits remain in the concrete robot/control path.
- Do not turn every primitive into a high-level autonomous skill. Task scripts retain the explicit manipulation sequence.

## Outputs to feed into later plans

- Phase 01 defines direct backend maps, typed examples, the ordinary task-script
  convention, and optional useful run evidence.
- Phase 02 documents one fixture per motion and gripper primitive.
- Phases 03–06 add object, perception, tracking, alignment, and scanning fixtures.
- Phase 07 maintains the handwritten module index, Docker/run commands, focused
  evidence, and limitations.

## Acceptance

- Every adopted pattern maps to a concrete DFL artifact and owning packet.
- Every rejected pattern is absent from runtime dependencies and workspace layout.
- An agent can find one capability, its configuration, ROS graph, fixture, and acceptance command without reading unrelated phase files.
- The audit creates no CaP-X runtime dependency.

## What this audit needs from me

Nothing.
