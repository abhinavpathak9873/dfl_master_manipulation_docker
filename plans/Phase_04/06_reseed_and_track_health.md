# Track health and FoundationPose reseeding

## Goal

Turn raw tracker evidence into honest tracking, degraded, stale, lost, and reseeding states, then recover only through a fresh accepted FoundationPose seed.

## Inputs

- Tracking contract
- M3T evidence
- FoundationPose estimate/reset
- SAM2 masks
- Per-object qualification settings

## Outputs

- Deterministic health evaluator
- Reseed state machine
- Per-object thresholds and hysteresis
- Wrong-identity/jump rejection
- Health diagnostics and recovery tests

## Work

1. Evaluate input age, pose age, image/depth continuity, M3T residuals, mask overlap, depth support, pose innovation, velocity bounds, and configured occlusion allowance.
2. Use hysteresis and minimum consecutive evidence to move between tracking and degraded. Time-based stale state overrides a positive residual.
3. Declare lost on expired stale bound, repeated invalid evidence, numerical failure, identity conflict, or impossible pose jump.
4. On lost, stop publishing current state and request a fresh SAM2/FoundationPose initialization. Keep the old track instance as history.
5. Accept reseed only when revision, mask, TF, pose plausibility, and discontinuity rules pass. Start a new track epoch and record the relationship.
6. Bound reseed attempts and rate. Exhaustion remains lost; it never restamps the old pose.
7. Expose the health reasons, thresholds, evidence samples, and last transition in diagnostics and run events.

## Interfaces and data

- TrackedObject health fields
- FoundationPose reseed client
- SAM2 prompt/mask health
- Per-object tracking policy

## Boundaries

- Does not retry forever
- Does not command visual servo directly
- Does not equate high publication rate with health

## Failure behavior

- Conflicting evidence resolves conservatively to degraded/stale/lost according to the state table.
- Reseed failure preserves lost state and reason.

## Acceptance

- Recorded occlusion, frame drop, wrong mask, jump, camera restart, and re-entry cases produce expected transitions.
- No stale pose is labeled tracking.
- Reseed creates a fresh observation and track epoch.
- Attempt bounds and hysteresis prevent oscillation.
- Every transition has machine and human-readable reasons.

## Parallel work

Consumes all perception adapters. Scene snapshots can implement against its output fixtures.

## What this module needs from me

Nothing.
