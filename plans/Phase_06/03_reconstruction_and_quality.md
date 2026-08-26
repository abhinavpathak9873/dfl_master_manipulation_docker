# Metric reconstruction and qualification

## Goal

Turn accepted multi-view capture into a metric candidate mesh and explicit
quality report using an on-demand dependency-isolated worker.

## Task-script payoff

A developer can replace the reconstruction implementation through a direct
backend/job selection while the resulting object file format and review flow stay
unchanged.

## Work

1. Characterize current reconstruction/cleanup tools and pin the selected
   dependencies in the scan-worker image.
2. Define one direct request containing the session/view manifest, calibration,
   masks/depth, desired backend/settings, output directory, and resource bounds.
3. Define progress/cancel/result only to the extent needed by the local UI and
   long-running job. Use a focused ROS action or local process/API, not a generic
   job system.
4. Reconstruct a metric point cloud/mesh, propose a canonical frame, clean
   artifacts, derive collision geometry/preview, and retain diagnostic outputs.
5. Measure scale/bounds, coverage, holes, density/noise, normals/manifold or other
   backend-relevant quality, and pose-model readiness.
6. Keep reconstruction success separate from reviewed qualification/approval.
7. Enforce time, disk, CPU/GPU/memory limits; cancellation leaves inspectable
   staging and no approved revision.
8. Make backend name, version, image, parameters, input hashes, timings, and
   quality reproducible.

## Acceptance

- Known fixtures reconstruct at correct scale/frame within declared tolerances.
- Invalid calibration/views/masks/depth fail with useful reasons.
- Worker failure/restart never mutates approved object assets.
- The worker starts only for a reconstruction job and releases resources after.
- Another backend can be added without a plugin/job platform.

## Non-goals

Automatic approval, always-on GPU allocation, cloud processing, or a distributed
reconstruction queue.
