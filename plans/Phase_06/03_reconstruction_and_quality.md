# Metric reconstruction and qualification

## Goal

Convert accepted scan views into a metric perception mesh, collision geometry, preview assets, and an objective report suitable for review and later FoundationPose use.

## Inputs

- Accepted scan session
- Camera calibration and poses
- Masks/depth views
- Object schema
- Current reconstruction and quality thresholds
- Scan-worker image and reconstruction action contract

## Outputs

- Reconstruction pipeline plugin or configured external tools
- Metric point cloud and candidate mesh
- Cleaned perception mesh and simplified collision mesh
- OBJ/PLY working assets and GLB preview where useful
- Canonical frame/scale proposal
- Quality report and FoundationPose-ready decision
- On-demand scan-worker action server, health, and stage checkpoint records

## Work

1. Run reconstruction in the on-demand `scan-worker` container. Give it the immutable scan-input manifest and read-write staging mount; give it no canonical write mount, robot/camera device, Docker socket, or GitHub credential.
2. Reconstruct only from accepted views and their exact calibration. Preserve a mapping from output assets to input view hashes, worker image digest, pipeline/plugin versions, and starting stage.
3. Filter background using masks and depth validity, register views in a common frame, fuse geometry, remove isolated components, and retain a raw diagnostic point cloud.
4. Generate a cleaned metric mesh for perception. Produce a separate conservative collision mesh with bounded simplification error.
5. Propose a canonical frame from the scan fixture and measured geometry. Require review before approval; do not recenter or rescale invisibly.
6. Render held-out views and compare silhouette plus depth against captured evidence. Report coverage, scale/dimensions, mesh integrity, component count, holes, and simplification error.
7. Use the existing initial qualification targets: at least nine accepted views per required pass, held-out silhouette IoU at least 0.90, and median or declared depth error no more than 0.010 m. Record the exact statistic used.
8. Checkpoint only at declared stage boundaries with input/output manifest hashes. A worker restart returns the scan session to paused; an operator may resume from the last verified stage or select an earlier stage.
9. Mark output qualified, review-required, or rejected. A quality miss cannot be overridden without a new explicit object revision carrying the exception and reason.

## Interfaces and data

- Reconstruction plugin/configuration
- Internal reconstruction action with stage/progress feedback and hashed result manifest
- Candidate assets and quality JSON
- Inputs to revision registration and viewer

## Boundaries

- Does not train perception models
- Does not make the object active
- Does not claim transparent/reflective/deformable support
- Does not move the robot, acquire camera frames, write canonical files, or launch containers

## Failure behavior

- Reject inconsistent calibration, scale ambiguity, insufficient coverage, invalid mesh, excessive held-out error, disconnected main geometry, or failed collision simplification.
- Retain diagnostic artifacts for review.
- Worker crash, output-hash mismatch, or lost action pauses the session and never promotes partial output.

## Acceptance

- A known fixture reconstructs at measured scale.
- Held-out metrics reproduce from the session inputs.
- Perception and collision meshes have explicit roles and hashes.
- Canonical transform is visible and reviewable.
- A failed metric produces rejected/review-required, never qualified.
- Killing the worker at every stage boundary preserves ObjectDB reads and permits only explicit hash-verified resume.
- A mount test proves the worker cannot modify canonical objects.

## Parallel work

Editor/viewer work proceeds with candidate fixtures. Registration follows qualified results.

## What this module needs from me

Nothing.
