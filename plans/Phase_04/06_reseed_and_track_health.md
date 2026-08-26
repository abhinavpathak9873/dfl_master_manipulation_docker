# Track health and FoundationPose reseeding

## Goal

Make loss, staleness, and reseeding explicit and bounded for the concrete
FoundationPose-to-M3T path.

## Task-script payoff

A task can see when the pose is safe to use and choose to reseed, wait, retry, or
abort through ordinary Python rather than a hidden recovery engine.

## Work

1. Characterize which M3T outputs correlate with stable, degraded, and lost
   tracking for each approved object.
2. Combine backend diagnostics with observation age, frame/time validity, pose
   jumps, bounds, and consecutive update behavior.
3. Expose a small health value/reason list; keep raw backend metrics available.
4. Define explicit `tracker.reseed(...)` or reset-plus-initialize behavior using
   a current FoundationPose estimate.
5. Put automatic bounded reseed, if a repeated task truly wants it, in a small
   visible helper with max attempts/time and no robot motion.
6. Reject mismatched object revision, stale mask/RGB-D, invalid TF, or implausible
   seed.
7. Test short/long occlusion, object leaving view, reentry, bad seed, process
   restart, and multi-object identity preservation.
8. Record only health/reseed evidence useful to tuning and failure diagnosis.

## Acceptance

- Healthy/stale/lost decisions match reviewed recorded sequences.
- No stale track is consumed as current.
- Reseed uses current data and preserves object identity/revision.
- Exhausted or failed reseed returns control to the task with a clear reason.
- The tracker object remains the owner of tracker state.

## Non-goals

A general recovery state machine, task motion during reseed, or silent infinite
reinitialization.
