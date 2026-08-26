# Robot, tool, camera, scene, and mode profiles

## Goal

Record the physical composition and stable IDs that task code will select. Separate identity and calibration facts from the Phase 01 configuration resolver.

## Inputs

- Global selector decisions
- Current picker descriptions and gripper configurations
- Doosan M1013/H2515 assets
- D455 and base calibration files

## Outputs

- Robot profiles: `picker1`, `picker2`, `h2515`
- Tool profiles: `onrobot_vgc10_1cup`, `onrobot_vgc10_4cup`, `onrobot_vgp20`, `onrobot_2fg14`
- D455 camera profile
- Initial scene profile layout
- Mode records for `real`, `gazebo`, and `genesis`
- Compatibility matrix with simulated and commissioned states

## Work

1. Define profile identity fields: stable ID, display name, description source, arm model, base type, controller namespace, TF prefix, planning group, mount frame, network endpoint source, and supported modes.
2. Define tool facts: driver ID, description asset, mount transform, TCP frames, collision geometry, payload, command capabilities, sensing capabilities, and commissioning status.
3. Separate VGC10 one-cup and four-cup geometry and grasp behavior. Add VGP20 and 2FG14 without aliasing them to the VGC10 driver.
4. Record D455 serial, stream profiles, optical frames, parent mount, calibration provenance, and which host owns the driver.
5. Define `.devcontainer/src/dfl_manipulation_toolbox/scenes/<scene_id>/scene.yaml` plus assets for static geometry, expected frames, simulator world settings, and default object placements.
6. Keep the provisional `calibration/picker1_d455.yaml` sentinel and future commissioned calibration records under the project-level `calibration/` durable mount. Package defaults may live with the owning package, but hardware-derived calibration must not be baked into a package or image.
7. Mark every combination as `supported_sim`, `commissioned_real`, `unsupported`, or `unverified`. Simulation support is required for all twelve robot/tool selections.
8. Provide a profile-inspection command or generated report that Phase 01 can consume when implementing validation.

## Interfaces and data

- Stable selector IDs used by task code
- Profile data consumed by launch, URDF/xacro overlays, config resolution, and run manifests
- Scene folder contract

## Boundaries

- Does not define merge precedence or schema tooling; Phase 01 owns resolution
- Does not claim real support for an unmounted combination
- Does not place dynamic perceived objects in the static scene

## Failure behavior

- Reject duplicate IDs, missing frames, unknown tool drivers, incompatible mount geometry, or a real profile without commissioning data.
- Do not infer a mounted tool from a task request; verify it where hardware can report identity and otherwise require commissioning confirmation.

## Acceptance

- All required profiles validate against a provisional schema.
- Every profile resolves to existing description and calibration assets.
- All twelve simulated combinations produce a valid robot description.
- Real profiles identify the expected hardware checks.
- Scene assets use SI units and declared frames.

## Parallel work

Can inventory data alongside Doosan migration. Simulator packets wait for accepted description and mount outputs.

## What this module needs from me

Facts: installed D455 serial/mount and current tool mounting at qualification time. These are collected from hardware.
