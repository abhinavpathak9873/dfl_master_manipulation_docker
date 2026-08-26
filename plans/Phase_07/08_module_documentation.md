# Architecture, API, module index, and agent guidance

## Goal

Make the toolbox easy for humans and AI agents to navigate, extend, run, and
debug without generating another metadata architecture.

## Task-script payoff

A developer or agent starts from one canonical task, follows a short path to the
capability/backend/ROS implementation, and knows the relevant Docker command,
tests, limitations, and hardware warnings.

## Work

1. Keep `plans/principles.md` and `plans/api_example.md` as the design and
   readability checks.
2. Document the final repository tree by robotics concept and Docker/ROS package
   ownership.
3. For each public capability, show construction, common methods, result/errors,
   concrete backend file map, backend-specific access, and one small example.
4. For each backend, document dependencies/image, required assets/inputs,
   outputs/state, supported robot/tool/modes, direct diagnostics, focused tests,
   and known limitations next to its source.
5. Document task-script convention, object-file format, scanning/authoring
   workflow, Compose profiles, gateways, DDS/time, commissioning, and recovery.
6. Provide a hand-written module index linking files rather than a generated
   plugin/capability catalogue.
7. Include agent guidance for small scoped changes: inspect canonical task,
   modify the nearest robotics module, avoid infrastructure, run focused tests,
   and update limitations/evidence.
8. Test documentation by asking a new developer/agent to add a sample backend,
   run a task, locate a ROS failure, and load an object.

## Acceptance

- Canonical examples are valid, consistent, and match public names.
- Every documented file/command/link exists at the time of implementation.
- Backend addition requires no secret registration steps.
- Safety-critical real commands and unsupported behavior are prominent.
- Documentation is useful without a portal, manifest generator, or architecture
  framework.

## Non-goals

A documentation platform, generated API universe, or substituting prose for
focused code/tests.
