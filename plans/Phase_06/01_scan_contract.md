# Scan workflow and local session state

## Goal

Define a simple durable local scan workflow before capture, reconstruction, or
GUI code, without turning it into a generalized state machine platform.

## Task-script payoff

Scanning reuses the same Robot, Camera, Segmenter, and object-file concepts as
normal experiments; completed assets require no scan runtime afterward.

## Session data and stages

A session folder records ID, provisional object name/ID, station/robot/camera/
calibration/scene/tool identity, operator, timestamps, inputs, completed-stage
outputs, decisions, and failure reasons.

Use only workflow stages the UI/operator needs: setup, preflight, awaiting start,
capturing, capture complete, reconstructing, review, approved/rejected, paused,
cancelled, failed, and registered. Each completed stage writes its output
atomically.

## Work

1. Define rigid/opaque/stationary eligibility and clear rejection reasons.
2. Check configured staging quota and that no other process owns physical scan
   motion using the smallest reliable local/ROS lock.
3. Require fresh robot/camera/TF/calibration/scene/tool preflight and one explicit
   operator start before motion.
4. Define view records and reconstruction/quality references as ordinary files.
5. Define cancellation at each stage: stop owned robot/camera work, flush useful
   artifacts, record status, and leave approved object files unchanged.
6. Resume only after operator review. Any motion-bearing resume repeats ownership
   check, preflight, and explicit start.
7. Make one local library the owner of state-file validation/atomic updates; the
   browser and worker are clients, not independent authorities.
8. Keep HTTP/WebSocket endpoints, if used by the local UI, narrowly tied to these
   authoring actions.

## Acceptance

- Invalid stage jumps, concurrent scan ownership, failed preflight, quota, and
  unsupported objects are rejected clearly.
- Cancellation and process restart preserve completed stages without resuming
  motion.
- Reconstruction can resume without robot authorization; capture cannot.
- No normal robotics task must acquire or contact this scan state.

## Non-goals

A distributed workflow engine, global runtime task lease, queue, scheduler, or
automatic approval.
