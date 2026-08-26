# Repository guidance

The task script is the product.

## Context pointers

- **Architecture:** read `toolbox_plan.md` before changing a public interface,
  repository structure, backend-selection mechanism, configuration approach, or
  runtime process boundary.
- **Planning:** read `plans/overview.md` and exactly one relevant active packet
  before implementing roadmap work. Read `plans/backlog.md` when promoting
  deferred scope.
- **Public task shape:** read `example_api.txt` before adding or renaming a
  task-facing method.
- **Object assets:** read `plans/work_packets/02_object_assets.md` before
  changing `object.json` or ObjectDB loading.

## Implementation loop

1. Name the task line that should become possible or simpler.
2. Trace the nearest existing path from public call to concrete backend.
3. Implement the behavior in the robotics folder that owns it.
4. Add one direct mapping entry only when named backend selection is useful.
5. Test through the public interface and add backend-specific fixtures where
   hardware, ROS, or model behavior matters.
6. Read the resulting task top to bottom and apply the task-script,
   five-minute, debugging, deletion, and two-implementation tests from
   `plans/audit.md`.

Work is complete when the named task/fixture runs, failures identify the owning
backend and failed assumption, and the direct implementation remains easy to
open.

## Repository shape

- `dfl_toolbox/`: reusable robotics code grouped by domain.
- `tasks/`: ordinary Python experiments.
- `objects/`: local runtime object assets when checked into this repository.
- `tests/`: interface and backend fixtures.
- `plans/`: current decisions and work packets, not runtime configuration.

ROS packages, launch files, containers, and scripts belong beside the backend
that requires them. Keep pure values and local object loading importable without
ROS.

## Hard guardrails

- Preserve user and reference-repository changes.
- Keep uncertain motion/control loss fail-safe in the owning robot adapter.
- Keep ROS nodes, topics, actions, TF, MoveIt, and vendor diagnostics directly
  inspectable.
- Represent unsupported backend behavior with a clear error.
- Keep ObjectDB optional during task execution.
