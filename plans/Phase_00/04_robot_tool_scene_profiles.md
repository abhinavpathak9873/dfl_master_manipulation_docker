# Robot, tool, camera, scene, and mode profiles

## Goal

Record the shared physical facts selected by task code without creating a
project-wide configuration framework.

## Task-script payoff

The four constructor arguments `model`, `mode`, `gripper`, and `scene` resolve
to inspectable hardware/simulator facts while experimental choices stay in the
task.

## Required profiles

- Robots: `picker1` (M1013 + base), `picker2` (M1013 + base), and `h2515`.
- Tools: `vgc10_1cup`, `vgc10_4cup`, `vgp20`, and `2fg14`, with aliases only
  where they are unambiguous and documented.
- Camera: installed D455 profiles and calibration references.
- Modes: `real`, `gazebo`, and `genesis`.
- Scenes: normal folders containing static geometry, frames, simulator assets,
  and optional initial placements.

## Work

1. For each robot, record description source, arm model, composite parts,
   namespace/TF prefix, planning group, controller endpoints, base type,
   supported modes, and commissioning reference.
2. For each tool, record driver/backend, mount, TCP, collision geometry, payload,
   commands, feedback, sensing, and supported modes.
3. Keep VGC10 one-cup and four-cup geometry/behavior separate; do not alias
   VGP20 or 2FG14 to a suction implementation.
4. Record camera serial/stream/frame/mount/calibration/host facts without baking
   hardware calibration into images.
5. Define scene folders under the toolbox ROS package and keep dynamic perceived
   objects out of static scene files.
6. Mark combinations as simulated, commissioned-real, unsupported with reason,
   or not-yet-verified. All 12 robot/tool choices remain required in both
   simulators.
7. Provide a direct profile inspection/validation command; no config daemon or
   generated capability catalogue.
8. Preserve source mounting chains. The Picker hand-camera plate sits between
   `link_6` and VGC10 four-cup or 2FG14; one-cup and VGP20 mount directly. Do
   not add the Picker plate to H2515.
9. Record visual provenance separately from collision and actuation fidelity.
   A dimension-derived 2FG14 model is not interchangeable with vendor CAD.

## Outputs

- Small readable robot, tool, camera, mode, and scene records.
- Compatibility/commissioning table.
- Valid descriptions and collision geometry for the simulator matrix.
- Calibration and scene path conventions.
- A fidelity ledger that states which facts are CAD-backed, dimension-derived,
  conservative, simulated-only, or still awaiting hardware measurement.

## Acceptance

- All stable IDs resolve to existing assets and backend names.
- All 12 robot/tool selections generate valid simulated descriptions.
- Picker 1 and Picker 2 remain independently namespaced M1013 composites.
- Real support is claimed only with mounted-hardware evidence.
- Invalid IDs, missing mounts/frames, and unsupported mode operations fail with
  actionable errors.
- The 12 generated selections have visually distinguishable tools and the
  expected intermediate mounts.

## Non-goals

- A universal profile schema for unknown future robots.
- Automatic hardware discovery or capability negotiation.
