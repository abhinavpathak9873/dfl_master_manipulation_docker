# Session restart and recovery

## Goal

Handle process, host, network, sensor, and controller restarts without stale bringup ownership, false-ready state, old commands, or automatic task continuation.

## Inputs

- Lifecycle ownership
- Gateway health/watchdogs
- DDS/time behavior
- Run records
- Explicit recovery policy
- ObjectDB task/scan leases and durable scan stages

## Outputs

- Session identity and epoch rules
- Reconnect state machines
- Stale ownership inspection/cleanup command
- Failure-to-recovery matrix
- Restart and desktop-death tests
- Operator/agent recovery guide
- ObjectDB outage, lease, scan pause/resume, and backup-sync recovery matrix

## Work

1. Assign a run/session UUID to desktop control and a boot/epoch ID to each gateway/simulator. Commands and ownership records identify both where supported.
2. On communication loss, gateway stops bounded streams and reports unhealthy. Desktop cancels active goals, marks state uncertain as required, and ends the task.
3. On reconnect, require fresh identity, JointState, TF, controller/tool/base state, camera frames, and clock health. Do not accept pre-disconnect samples.
4. A restarted component may become ready for a new task or explicit recovery task. It never resumes the failed task or reissues a prior command.
5. Provide an inspect command that distinguishes live owned, live unowned, dead stale, and incompatible sessions. Cleanup removes only verified dead owned artifacts/processes.
6. Define recovery actions by known state: inspect only, release if confirmed safe, controlled retreat from measured pose, rehome after verification, or hardware/operator intervention.
7. Test task, core service, perception, gateway, emulator, camera, network, and desktop restarts at each active stage.
8. On ObjectDB loss, allow only tasks that already resolved and verified their immutable revisions to continue. Block new task/scan leases, revision changes, and unverified object lookup until storage and service health return.
9. Persist task and scan leases across ObjectDB restart. Missing heartbeat changes the lease to stale-blocked; timeout, container restart, or Compose shutdown never clears it automatically.
10. Pause a scan on ObjectDB, core, gateway, perception, or scan-worker loss. Preserve completed stage manifests. Reconstruction-only resume needs operator review; any motion-bearing resume also needs fresh Picker 1 preflight and explicit start.
11. Treat GitHub or sync-sidecar loss as backup degradation. Keep valid local objects readable and active, retry push, and expose the oldest unpushed commit.

## Interfaces and data

- Session/run IDs and gateway epochs
- Lifecycle/readiness health
- Stale ownership CLI
- Recovery-required record
- Lease inspection/release and scan-stage resume records

## Boundaries

- No checkpoint resume
- No generic automatic home
- No killing unowned processes
- No automatic stale-lease release or scan motion resume

## Failure behavior

- Unknown ownership or robot/tool/object state remains blocked and requires operator/hardware inspection.
- Failed stop or reconnect validation escalates severity.
- Lease owner/epoch uncertainty blocks activation and new motion until explicit verified release.

## Acceptance

- Every restart fixture ends the old task exactly once.
- No old command executes after a new gateway epoch.
- Fresh readiness requires new state and timestamps.
- Stale cleanup targets only verified owned dead sessions.
- Recovery guide maps each typed failure class to allowed next actions.
- ObjectDB restart, stale task/scan lease, scan-worker crash, staging recovery, and Git-sync outage fixtures obey the accepted rules.

## Parallel work

Runs after gateway/lifecycle contracts; hardware commissioning supplies real endpoints.

## What this module needs from me

Nothing.
