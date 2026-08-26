# Decision 000 — task-script-first toolbox

Status: accepted

Date: 2026-08-27

Supersedes: the deployment-focused decision recorded at this path on 2026-08-26

## Decision

The task script is the product and the controlling architecture test.

The toolbox exposes small robotics modules and chooses concrete adapters with
source-controlled mappings. Experiments are ordinary Python files by default.
ROS, MoveIt, simulators, native models, and vendor drivers remain visible and
are used directly behind the relevant adapter seam.

ObjectDB runtime consumption is file-first and local. ObjectDB authoring is a
companion workflow, not a task dependency.

Work proceeds as vertical slices through a named task. A common interface is
extracted after concrete implementations show a repeated shape, not before.

## Consequences

- `tasks/*.py` replaces mandatory sibling ROS task packages.
- `dfl_toolbox` is importable without ROS; ROS conversions live in adapters.
- `Robot` exposes real subassemblies instead of a universal flattened surface.
- Backend IDs map to implementation files through small dictionaries.
- Task-specific configuration stays in the script. Hardware facts stay with the
  hardware adapter.
- Clear Python exceptions replace a global failure/result envelope initially.
- Instrumentation and qualification are added in proportion to observed risk.
- Containers isolate incompatible dependencies but do not form an orchestration
  product.

## Guardrails

- Motion uncertainty and control loss still stop safely.
- Real adapters validate hardware identity, calibration, controller readiness,
  state freshness, and stop behavior.
- ROS namespaces, TF, time, QoS, and vendor semantics stay explicit at ROS
  seams.
- No backend reports a capability or success it cannot actually verify.

## Revisit triggers

Revisit one part of this decision only when a concrete task demonstrates that:

- ordinary Python control flow is insufficient;
- a local object directory is insufficient;
- two real adapters require a deeper shared seam;
- repeated configuration or diagnostics defects justify shared machinery; or
- physical deployment forces a new process boundary.

The proposal must include the affected task before and after the change.
