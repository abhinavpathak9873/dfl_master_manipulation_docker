# Guided multi-view capture

## Goal

Acquire synchronized RGB-D evidence from enough calibrated viewpoints to reconstruct one stationary rigid object while rejecting blurred, stale, masked, or geometrically weak views.

## Inputs

- Scan contract
- D455 profile
- Robot motion API
- SAM2 segmentation
- Scene and scan poses
- Picker 1 scan profile and global scan lease
- Current scan-view acceptance behavior

## Outputs

- Capture planner and explicit robot/camera task
- Two-pass required capture workflow with optional third coverage pass
- View quality evaluator
- Coverage visualization data
- Accepted/rejected capture artifacts
- Replay tests

## Work

1. Require the ObjectDB-owned scan session and global lease, then run preflight for the commissioned Picker 1 station: controlled work surface, stationary object, installed tool/collision identity, eye-in-hand D455 streams, calibration, TF, robot/controller readiness, scene clearance, and writable staging below quota.
2. Present the frozen profile, scene, planned passes, lease owner, and preflight result in ObjectDB. Execute no viewpoint motion until the operator issues the session's explicit start action.
3. Use two declared view passes from complementary elevation/azimuth sets. Require at least nine accepted views per pass. Add a third pass only when coverage metrics identify a named gap.
4. Send motion through the core task/motion API and receive camera data from the gateway ROS graph. Plan each move with visible planner choice and execute only after collision checks; ObjectDB sends no controller command directly.
5. Request or maintain a SAM2 mask from the perception service. Reject view on stale/missing TF, blur, exposure failure, insufficient depth, mask truncation, weak object area, excessive overlap, or unsafe robot pose.
6. Record rejected views and reasons; do not count them toward coverage. Reacquire only through an explicit bounded attempt.
7. Estimate surface/viewpoint coverage from camera/object geometry and accepted masks. Show missing regions to the operator before ending capture.
8. Keep raw accepted and rejected frames immutable with content hashes in quota-managed scan staging.
9. On cancellation or component loss, stop the current motion/capture path, persist the completed-view manifest, and pause. Resume repeats robot/camera/scene preflight and explicit start before another move.

## Interfaces and data

- Scan action feedback
- Robot motion and camera capture
- SAM2 prompt/mask
- View records and coverage data

## Boundaries

- No continuous robot motion during capture
- No handheld uncalibrated camera in v1
- No automatic acceptance of a view because a file exists
- No direct device access or controller call from ObjectDB or browser JavaScript

## Failure behavior

- Stop capture on robot/control loss, object movement, scene change, camera restart, TF/calibration mismatch, or repeated insufficient evidence.
- Return to review rather than continuing with a known coverage gap.

## Acceptance

- Each required pass contains at least nine accepted views.
- All accepted frames have synchronized depth/CameraInfo/TF and valid masks.
- Repeated viewpoints and poor frames are rejected with reasons.
- Cancellation stops motion and preserves a readable staging session.
- Replay reproduces accept/reject decisions.
- No motion occurs before explicit start or after restart until reauthorized.
- Active task and second-scan fixtures are refused without disturbing their owner.

## Parallel work

Read-only viewer can consume capture fixtures. Reconstruction follows accepted sessions.

## What this module needs from me

Facts: safe scan scene, arm view poses, and object placement fixture are commissioned during implementation.
