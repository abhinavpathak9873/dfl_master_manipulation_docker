# Restart and explicit recovery

## Goal

Define small component-specific stop/restart rules so faults are safe and
understandable without a generalized session/epoch/lease framework.

## Task-script payoff

After a failure, the developer sees what state is known, what stopped, what must
be revalidated, and whether to continue a non-motion step or start a fresh task.

## Work

1. List concrete failures for task process, robot launch, controllers, gateways,
   DDS/network, camera, perception, tracker, simulator, ObjectDB authoring, scan
   capture, and reconstruction.
2. For each, state ownership, observable symptom, safe stop, preserved local
   data, restart command, and required revalidation.
3. Treat trajectory/servo/contact execution as uncertain unless controller/vendor
   evidence proves a final state; require a fresh task/recovery procedure.
4. After perception/tracker restart, require a new current observation/seed and
   scene update before motion.
5. After network/gateway restart, require current robot/tool/base state and
   command-channel watchdog validation.
6. Let reconstruction-only scan work resume from reviewed files; any scan motion
   repeats ownership check, preflight, and explicit operator start.
7. Never auto-home, auto-release, auto-reattach an object, or auto-resume motion.
8. Add fault-injection scripts and concise operator recovery notes near the
   owning component.

## Acceptance

- Every injected fault reaches the declared stop/error and never false success.
- Restarted components cannot consume stale commands, targets, tracks, or scene
   state.
- Non-motion authoring work can reuse validated completed files.
- Recovery logic is component/task-local and inspectable.
- No central recovery coordinator is required.

## Non-goals

Automatic task resume, distributed session management, self-healing deployment,
or generalized compensation workflows.
