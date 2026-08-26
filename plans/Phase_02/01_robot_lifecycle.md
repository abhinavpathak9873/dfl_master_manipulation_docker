# Robot lifecycle and task-owned launch

## Goal

Implement the one-command `Robot.bringup()` workflow as an owner of standard ROS launch descriptions. Prevent stale, duplicate, or ambiguously owned runtime processes.

## Inputs

- Resolved configuration
- Run-record API
- Namespace/readiness contract
- Compose service health
- Runtime lease client contract
- Doosan and simulator launch descriptions

## Outputs

- `Robot` constructor with explicit selectors
- `bringup()`, `attach()`, `bringdown()`, and context-manager support
- Launch session owner and process manifest
- Narrow readiness preflight
- Signal and exception cleanup
- Task lease acquisition, heartbeat, inspection, and release
- Lifecycle contract tests

## Work

1. Construct `Robot` from required `robot`, `gripper`, `scene`, `mode`, and `pipeline` selectors. Resolve and freeze configuration before starting processes.
2. Create the run record and acquire one task lease carrying its run ID, selected robot/mode, and configuration hash before any motion-capable process starts. Refuse startup when the lease service is unavailable or another exclusive scan lease exists.
3. Start one standard ROS launch description through the ROS launch API. Record launch UUID, parent PID, child process identities, namespace, domain ID, config hash, lease ID/epoch, and start time.
4. Heartbeat the task lease while the run owns control. ObjectDB loss records degraded lease health but does not stop a task whose required immutable object revisions were already resolved and hash-checked.
5. Before launch, inspect the namespace for expected nodes, controllers, and an ownership token. Refuse a live unowned stack. Reuse is allowed only through explicit `attach()` after compatibility checks.
6. Keep preflight short: profile identity, required services/actions, resolved object hashes, fresh JointState, connected TF, controller state, tool readiness, required camera health, and scene validity.
7. Install SIGINT/SIGTERM handlers that request motion/tool/base stop, flush run events, and terminate only the owned launch tree.
8. Make `bringdown()` idempotent. It cancels active goals, stops velocity streams, releases tool commands when the task policy says release is safe, shuts down owned processes in dependency order, and releases the task lease only after terminal state is recorded.
9. Expose underlying ROS node, launch handle, namespaces, lease state, and resolved configuration for debugging.

## Interfaces and data

- `Robot(...)`, `bringup()`, `attach()`, `bringdown()`
- Lifecycle states `created`, `starting`, `ready`, `stopping`, `stopped`, `failed`
- Ownership token under the robot namespace plus process manifest in the run directory
- Runtime lease ID/epoch and heartbeat status

## Boundaries

- Does not daemonize a hidden permanent runtime
- Does not kill unowned ROS or vendor processes
- Does not run expensive perception benchmarks during preflight

## Failure behavior

- Reject selector/config mismatch, live unowned namespace, inactive controller, stale state, disconnected TF, wrong tool identity, unavailable required sensor, or unhealthy service.
- Reject a new run when ObjectDB resolution/lease acquisition fails, a scan lease is active, or a prior lease remains stale and unverified.
- On partial startup, stop already-started children and record the failing readiness item.
- Cleanup failure is reported but does not suppress the original task error.

## Acceptance

- One command starts a simulation task from a clean host.
- SIGINT during planning, execution, visual servo, gripper motion, and base velocity produces a stopped state and artifact.
- A second bringup refuses the live unowned stack.
- Explicit attach succeeds only when namespace, config hash, mode, and required interfaces match.
- Repeated bringdown changes no external state after the first completion.
- A running fixture survives ObjectDB restart after object resolution; a new fixture cannot start until resolution and lease acquisition recover.
- Missing heartbeat leaves a stale blocked lease until explicit verified release.

## Parallel work

Motion API can use a lifecycle stub after states freeze. Real process tests depend on accepted launch descriptions.

## What this module needs from me

Nothing.
