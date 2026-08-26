# Existing local-alignment characterization

## Goal

Capture the useful behavior of the current local fitment implementation before
simplifying or relocating it.

## Task-script payoff

The new direct backend preserves the geometry and tuning researchers already
rely on while shedding accidental node/module architecture.

## Work

1. Inventory current nodes, actions/topics, configs, scripts, models/references,
   algorithms, frames, crop/mask/depth rules, and robot command paths.
2. Record correction conventions, XY/RPY order, reference frames, thresholds,
   filters, iteration bounds, termination, and failure behavior.
3. Collect representative inputs/outputs/debug images/point clouds for the
   approved small tray and other available objects.
4. Separate pure computation from ROS transport, visualization, and robot motion.
5. Build golden numeric and visual fixtures for zero, known offset, noise,
   missing depth, bad mask, occlusion, symmetry, stale input, and no convergence.
6. Measure latency, convergence range, repeatability, and sensitivity rather than
   assuming legacy behavior is correct.
7. Identify safety behavior that must remain at the servo/robot seam.
8. Document intentional improvements separately from preservation tests.

## Acceptance

- A reviewer can explain each transform and correction sign from evidence.
- Golden fixtures reproduce current accepted behavior within tolerances.
- Bugs/ambiguities are recorded rather than silently enshrined.
- The plan says which code/data to reuse and which old layers to discard.

## Non-goals

Copying the old topology, configuration hierarchy, or hidden motion ownership.
