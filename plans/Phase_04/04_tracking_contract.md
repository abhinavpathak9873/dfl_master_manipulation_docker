# Explicit tracking API

## Goal

Define the small stateful behavior exercised by M3T and task loops without a
general state-management system.

## Task-script payoff

A task constructs one `Tracker`, calls `initialize`, repeatedly calls `update`,
inspects age/health, and explicitly resets or reseeds it.

## API shape

- `initialize(rgb, depth, object_pose, ...)`
- `update(rgb, depth, ...) -> tracked pose/result`
- `reset()`
- Optional concrete-backend methods and diagnostics.

Track output carries object/revision identity, pose, source timestamp/frame,
observation age, and the health/confidence/lost facts real consumers need.

## Work

1. Derive exact shared methods and fields from the M3T integration and Phase 05
   consumers.
2. Keep tracker state, model resources, previous observation, and health inside
   the tracker object.
3. Define monotonic source-time handling, duplicate/out-of-order rejection, TF
   behavior, and reset semantics.
4. Distinguish uninitialized, initializing, healthy, degraded, stale, lost, and
   failed only where task decisions differ.
5. Preserve raw M3T confidence/diagnostics rather than fabricating a universal
   normalized score.
6. Define multi-object usage as multiple owned tracks or a concrete M3T
   multi-body object, whichever the backend naturally supports.
7. Test initialize/update/reset, object mismatch, bad time, occlusion, loss, and
   process restart.

## Acceptance

- State transitions follow explicit method calls and source data.
- A stale/lost track cannot masquerade as a current pose.
- M3T-specific features remain reachable.
- No external tracker-state service or general lifecycle framework is needed.

## Non-goals

Automatic backend switching, hidden reseed policy, or universal confidence
normalization.
