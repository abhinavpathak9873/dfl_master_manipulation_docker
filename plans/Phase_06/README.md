# Phase 06 — object scanning and local web GUI

## Goal

Provide `scan_object` as a guided ObjectDB workflow for capturing one rigid opaque object on the commissioned Picker 1 station, reconstructing it in an isolated worker, reviewing and committing an immutable revision, annotating grasps, and testing them through the accepted manipulation path.

## Settled decisions

- Support rigid, opaque, stationary objects only.
- Use a local web GUI on the desktop.
- ObjectDB owns the scan session, operator workflow, evidence, approval, and canonical commit; it does not own robot, camera, GPU, or Compose processes.
- Core/gateway owns Picker 1 and its eye-in-hand D455, perception owns SAM2, and the on-demand scan-worker owns reconstruction.
- Physical scanning is globally exclusive maintenance work. Active tasks cause startup refusal and are never queued, cancelled, or stopped by the scan launcher.
- Motion requires a fresh preflight and one explicit operator start. A resumed motion stage repeats both review and preflight.
- Completed stages are durable; no crash triggers automatic resume.
- Raw staging is quota-bound and requires explicit export or cleanup.
- The GUI reads and writes through the object service; it never edits canonical files directly.
- Approved revisions are immutable.
- Hardware grasp testing uses Phase 05 primitives and safety behavior.
- Preserve the useful current workflow: guided views, SAM2 masks, plan preview, approval, and grasp testing.

## Work packets

| Packet | Result |
|---|---|
| [01](01_scan_contract.md) | ObjectDB-owned state, exclusive lease, authorization, pause, and resume contract. |
| [02](02_view_capture.md) | Explicitly started Picker 1 multi-view RGB-D acquisition. |
| [03](03_reconstruction_and_quality.md) | Isolated scan-worker, metric meshes, checkpoints, and qualification. |
| [04](04_revision_registration.md) | Staged object record, lease gate, local Git commit, and activation. |
| [05](05_object_viewer.md) | Read-only local 3D object and evidence viewer. |
| [06](06_atomic_editor.md) | Validated metadata/asset/revision editing. |
| [07](07_grasp_annotation_and_test.md) | Gripper-aware anchor editing, plan preview, and test. |
| [08](08_scan_gui_acceptance.md) | End-to-end container, lease, scan, Git/LFS, GUI, and object evidence. |

## Order and parallel work

Freeze the scan and lease contract first. View capture and the read-only viewer may proceed together. Reconstruction implements the isolated worker action and consumes immutable capture manifests. Revision registration consumes qualified worker output and the Phase 03 service. The editor follows the viewer and service. Grasp annotation uses the viewer plus Phase 03 grasp schema; hardware test waits for Phase 05. Acceptance runs last.

## Upstream inputs

- Phase 03 object schema/store/service
- Phase 04 D455, SAM2, and recorded-data contracts
- Phase 05 grasp execution and verification
- Current Object Studio and scanning behavior

## Exit criteria

- A supported object can be captured through a reproducible guided session.
- The one-command scan profile refuses an active task, acquires one global scan lease, and never gives ObjectDB direct hardware or Docker access.
- Reconstruction emits metric perception and collision assets with a qualification report.
- No object becomes active without schema, asset, quality, lease, local Git, and explicit approval checks.
- Viewer/editor operations use the typed service and recover from failed writes.
- Grasp anchors preview against the selected tool and test through an immutable plan.
- The complete workflow produces an accepted object revision and indexed artifacts.

## What this phase needs from me

Access to one representative new rigid opaque object, Picker 1 with its commissioned eye-in-hand D455 and scan scene, and a supervised grasp-test window. No GUI or runtime-boundary decision remains.
