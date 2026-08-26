# Focused ROS interfaces

## Goal

Use standard ROS interfaces wherever possible and add custom IDL only for
concrete cross-process behavior that cannot be expressed clearly otherwise.

## Task-script payoff

Task-facing objects can adapt to ROS processes without exposing transport
ceremony or creating a second communication architecture.

## Work

1. Inventory actual cross-process exchanges from Doosan, grippers, D455,
   perception, M3T, alignment, scanning, reconstruction, and gateways.
2. Map each to existing geometry, sensor, trajectory, control, MoveIt,
   diagnostics, lifecycle, and standard service/action types.
3. For every remaining semantic gap, document the producer, consumer, why a
   standard type is inadequate, units/frames/time, cancellation, and failure
   behavior before adding IDL.
4. Keep Python-local `Pose`, `Joints`, object assets, configuration, and backend
   calls out of ROS interfaces.
5. Keep the custom interface package small and dependency-light.
6. Test serialization, cancellation, stale timestamps, invalid frames, and
   cross-container compatibility for every custom type actually added.

## Likely concrete gaps to evaluate

- Long-running native reconstruction or alignment actions with progress/cancel.
- A compact tracked-object array if standard pose messages cannot carry required
  identity/health/age semantics.
- Gateway-specific status only if diagnostics messages are insufficient.

These are questions, not preapproved interfaces.

## Acceptance

- Every custom type names real code on both sides.
- Standard ROS tooling can inspect the graph and payloads.
- No custom IDL exists only to enforce a Python class design.
- Removing an unused integration also removes its unused interface cleanly.

## Non-goals

- Runtime lease, plugin catalogue, configuration, run-event, or workflow IDL.
- A generic command/result protocol for arbitrary algorithms.
