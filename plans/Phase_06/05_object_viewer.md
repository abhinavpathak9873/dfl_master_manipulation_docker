# Local object and scan viewer

## Goal

Provide a responsive read-only browser view of canonical objects, revisions, meshes, collision geometry, grasp anchors, local references, scan views, and qualification evidence.

## Inputs

- Object service read API
- Canonical object examples
- Scan/reconstruction fixtures
- Existing React/Three.js Object Studio behavior

## Outputs

- Local React/TypeScript/Three.js viewer
- Object/revision browser
- Mesh/collision/axes/TCP/grasp overlays
- Scan-view and held-out quality inspection
- Health/error display
- UI tests and visual snapshots

## Work

1. Serve the GUI from the ObjectDB container, binding on its container interface while Compose publishes only `127.0.0.1:8765`. V1 has no remote-LAN or multi-user mode.
2. Read object lists, revisions, active pointer, assets, and validation through the typed service/API. The browser receives resolved URLs or streamed assets, never filesystem authority.
3. Render mesh, collision geometry, canonical axes, dimensions, symmetry, gripper model, TCP, grasp anchors, approach/retreat vectors, and correction offsets with toggles.
4. Show scan camera poses, accepted/rejected views, masks, depth, held-out overlays, quality metrics, provenance, and limitations.
5. Keep object ID, revision ID, mesh hash, gripper profile, and qualification status visible during review.
6. Report loading, schema, missing asset, rendering, storage, ROS, scan-worker, lease, staging quota, and backup-freshness state without showing stale data as the selected revision. Browsing remains available when only ROS/scan readiness is down.
7. Add deterministic component tests and screenshots for the four migrated objects plus scan candidates.

## Interfaces and data

- HTTP/WebSocket or local API over the object service
- Split ObjectDB health and loopback route
- Three.js asset rendering
- Read-only routes and selection state

## Boundaries

- No direct file reads from arbitrary browser paths
- No editing in this packet
- No multi-user auth or conflict model
- No Docker controls or direct robot/camera access

## Failure behavior

- Clear the selected 3D state on revision-resolution failure rather than retaining the previous mesh under a new label.
- Surface unsupported asset formats and excessive mesh size.

## Acceptance

- All four objects render with correct scale and axes.
- Switching revisions updates IDs, hashes, overlays, and evidence together.
- Collision and grasp overlays align with canonical coordinates.
- Broken assets and service restarts produce clear errors.
- ROS/scan outage does not hide canonical objects or imply scan readiness.
- Visual snapshots cover main review states.

## Parallel work

Starts after stable read API and fixture data. Editor extends it later.

## What this module needs from me

Nothing.
