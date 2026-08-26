# Scanning contract

## Goal

Define the state, inputs, outputs, identity, and failure behavior of a scan session before capture, reconstruction, registration, or GUI code is written.

## Inputs

- Object schema and service
- Runtime lease contract
- D455/camera contract
- Robot motion and run records
- Current two/three-pass scanning workflow
- Rigid opaque scope

## Outputs

- Scan session value and state machine
- Capture/view record schema
- Reconstruction request/result
- Qualification result and error codes
- `ScanObject` ROS action semantics
- Global scan-lease and exclusive-maintenance semantics
- Durable stage/resume and staging-quota policy
- Recorded fixture set

## Work

1. Create a scan session ID and bind it to the fixed Picker 1 scan profile, camera/calibration, scene, installed tool/collision model, provisional object ID/name, operator, source manifest, run ID, and one global scan lease ID/epoch.
2. Define states created, preflight, awaiting-start, capturing, capture-complete, reconstructing, review, qualified, rejected, committed, paused, cancelled, and failed. Persist a monotonically increasing state revision and the input/output manifest hash for every completed stage.
3. Define a view record with robot/camera pose, RGB/depth/CameraInfo/TF timestamps, mask, accepted/rejected status, rejection reason, coverage metadata, and hashes.
4. Define reconstruction output as candidate metric point cloud/mesh, canonical-frame proposal, scale evidence, collision geometry, preview assets, and quality metrics.
5. Define qualification as a separate result. Reconstruction success alone never implies an approved or FoundationPose-ready object.
6. Define eligibility: no task or scan lease may be active or stale-unverified, staging must be below quota, and all selected services/resources must report their owning health. Startup refuses and identifies the blocking owner; it does not queue or stop a task.
7. Require fresh hardware preflight followed by one explicit operator start before entering capturing. Resuming a motion-bearing stage returns to preflight and awaiting-start; reconstruction-only resume requires operator review but no robot authorization.
8. Define cancel at every pre-commit state. Cancellation stops robot/camera activity, flushes artifacts, marks the session terminal or paused as declared, releases the lease only after stop evidence, and leaves canonical ObjectDB unchanged.
9. Map HTTP/GUI actions and ROS action goals to one ObjectDB-owned state controller. The browser and scan-worker never become state authorities.

## Interfaces and data

- `ScanObject` action
- Scan session and view manifests
- Reconstruction/qualification records
- Object service staging reference
- Runtime lease, state revision, and operator authorization event

## Boundaries

- Does not select a reconstruction algorithm in the contract
- Does not approve a record automatically
- Does not support moving, transparent, mirror-like, or deformable targets
- Does not control Docker or open robot/camera devices from ObjectDB
- Does not support concurrent physical scans or scan acquisition on Picker 2/H2515 in v1

## Failure behavior

- Unsupported material/motion, camera/TF failure, unsafe robot state, insufficient views, reconstruction error, quality failure, cancellation, and commit failure are distinct.
- Any failure before explicit commit leaves no active object revision.
- ObjectDB, core, gateway, perception, or worker restart pauses the session. No component restart resumes motion or clears a lease automatically.
- Quota exhaustion blocks new sessions without deleting staged data.

## Acceptance

- State transitions reject skips and invalid repeats.
- Cancellation works during capture and reconstruction.
- Fixtures preserve exact camera/object/calibration identity.
- A failed qualification can be reviewed without becoming active.
- Action feedback identifies current view/pass and next required operator action.
- Active-task, second-scan, stale-lease, quota, preflight, explicit-start, pause, and stage-resume fixtures pass.

## Parallel work

Viewer design can use the result fixtures after the first schema freezes.

## What this module needs from me

Nothing.
