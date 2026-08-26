# Local object and scan viewer

## Goal

Provide a focused local visual tool for inspecting canonical objects and scan
candidates where text/RViz alone is insufficient.

## Task-script payoff

Researchers can see whether mesh scale/frame, collision geometry, references,
and grasps are correct before using the same files in a robot task.

## Work

1. Start read-only with a local web UI in the ObjectDB authoring Compose profile.
2. Load object/session data through the same file library used by the CLI; do not
   require a runtime object service.
3. Display mesh/collision geometry, axes/frames, dimensions, revision/provenance,
   model/reference availability, quality metrics, and validation warnings.
4. Overlay grasp anchors, TCP/cup/finger geometry, approach/retreat, and tool
   compatibility.
5. Display scan views, masks, camera poses, coverage, and reconstruction
   diagnostics where available.
6. Provide object/revision search and direct path/reveal/download helpers useful
   to a single local operator.
7. Handle missing/corrupt assets visibly and never convert view failure into an
   edit.
8. Keep browser bundle/UI dependencies inside the authoring image.

## Acceptance

- Golden fixtures render at correct scale/orientation with distinguishable
  object, collision, and grasp frames.
- Read-only use cannot mutate canonical files.
- Missing data produces a warning tied to the exact asset.
- The same object remains usable through files/CLI when the viewer is stopped.

## Non-goals

A multi-user web product, remote hosting, runtime dashboard, or generic 3D asset
manager.
