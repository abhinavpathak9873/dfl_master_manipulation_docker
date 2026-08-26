# Timestamped scene snapshots

## Goal

Provide a small immutable multi-object view for consumers that need a coherent
scene without creating a world-model service.

## Task-script payoff

A task, grasp selector, or planning-scene helper can ask the tracker collection
for the latest objects and explicitly judge each pose's identity, timestamp,
frame, age, and health.

## Work

1. Define a lightweight snapshot containing creation time/frame plus tracked
   entries with original source time/age and object/revision identity.
2. Build it directly from current tracker objects/results; do not copy object
   meshes or large assets into every snapshot.
3. Preserve per-object ages rather than assigning one misleading current stamp.
4. Provide explicit filtering by target ID, health, maximum age, and frame.
5. Transform poses only with timestamp-valid TF and preserve transformation
   provenance for debugging.
6. Let MoveIt/task consumers choose update rate; do not publish at a fixed rate
   without a consumer.
7. Test empty, partial, mixed-age, lost, duplicate-identity, out-of-order, and TF
   failure cases.

## Acceptance

- Snapshot values are immutable and do not alter tracker state.
- Consumers cannot confuse creation time with observation time.
- Lost/stale objects remain explicit or are filtered by an explicit request.
- A task can inspect/print the snapshot without contacting a service.

## Non-goals

A persistent scene database, global world model, or automatic planning-scene
authority.
