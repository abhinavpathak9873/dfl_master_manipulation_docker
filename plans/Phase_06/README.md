# Phase 06 — ObjectDB scanning and authoring companion

## Goal

Provide the complete physical-object-to-reusable-file workflow as a Dockerized
companion tool, separate from normal task runtime.

## Task-script payoff

A researcher scans, reconstructs, reviews, annotates, and approves an object;
later `dfl.objectdb.load(...)` consumes the resulting files with ObjectDB stopped.

## Required scope

- Rigid, opaque, stationary objects for the first supported workflow.
- Picker 1 with its commissioned eye-in-hand D455 as the first automated scan
  station; the design reuses toolbox robot/camera primitives and does not forbid
  future stations.
- Guided capture, on-demand reconstruction, quality review, file revision
  registration, viewer, validated editor, grasp annotation/preview/test, and
  end-to-end acceptance.
- Local single-operator web UI where it materially improves visual authoring.
- Docker isolation for UI/reconstruction dependencies.

## Packets

1. [Scan workflow and state](01_scan_contract.md)
2. [Guided multi-view capture](02_view_capture.md)
3. [Metric reconstruction and quality](03_reconstruction_and_quality.md)
4. [Revision registration](04_revision_registration.md)
5. [Local object and scan viewer](05_object_viewer.md)
6. [Validated atomic editor](06_atomic_editor.md)
7. [Grasp annotation, preview, and test](07_grasp_annotation_and_test.md)
8. [Scan and GUI acceptance](08_scan_gui_acceptance.md)

## Smallest sufficient design

- File-backed local session folders and explicit stages.
- Normal robot/camera/perception calls for capture.
- Direct request/result to an on-demand reconstruction worker.
- Reviewed atomic write of the same file-first asset format tasks load.
- Minimal machine/ROS-level exclusion for physical scan motion; no task-wide
  lease platform.
- Motion-bearing resume always repeats review, preflight, and explicit start.

## Exit evidence

One new physical object travels from capture through reconstruction, review,
registration, grasp annotation/test, and later task loading. Faults preserve
useful completed stages and never auto-resume robot motion.

## Non-goals

An always-on ObjectDB control plane, distributed workflow engine, multi-user
application, runtime object service, or Docker controller inside ObjectDB.
