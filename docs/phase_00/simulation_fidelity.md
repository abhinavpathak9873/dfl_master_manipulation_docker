# Simulation fidelity ledger

The project is built for task-code transfer, not for treating a simulator run
as hardware qualification. A script can keep the same robot, tool, and motion
intent across backends only where the ROS contract says it can. Physical claims
need measurements from the installed robot.

| Area | Current source | Phase 00 confidence | What remains before real transfer |
| --- | --- | --- | --- |
| M1013 and H2515 shape | Full visual meshes and kinematic chain from pinned Doosan `doosan-robot2` | High for appearance and nominal link geometry | Confirm installed model, flange, joint zero offsets, limits, controller firmware, and payload settings |
| Picker 1 base | Workspace STL plus a separately modeled pedestal | High for the retained STL; medium for the pedestal | Measure pedestal, base footprint, wheels, mass, inertia, and arm mounting transform on Picker 1 |
| Picker 2 base | Full workspace STL and workspace arm mounting transform | High for appearance; unqualified for dynamics | Measure mass distribution, wheel geometry, suspension, friction, and arm mounting transform |
| VGC10 one cup | Full workspace visual mesh; declared mass, TCP, and conservative collision primitive | High for nominal shape | Verify installed cup, mount, TCP, payload, vacuum threshold, seal behavior, and release timing |
| VGC10 four cup | Full workspace visual mesh through the workspace hand-camera plate | High for nominal shape and source mounting chain | Verify cup layout, plate transform, TCP, individual cup behavior, and vacuum dynamics |
| VGP20 | Full workspace 16-cup visual mesh; conservative collision box | High for nominal shape | Verify installed cup pattern, payload, TCP, airflow, pressure, and seal-loss behavior |
| 2FG14 | Dimension-derived visual model and published full-sweep collision envelope | Medium for overall envelope; low for detailed shape | Obtain redistributable vendor CAD, measure fingers and mount, implement jaw kinematics, grip force, contact, and object constraint |
| Hand camera assembly | Workspace `hand_camera_axis_s.dae` on source-matched Picker tool chains | High for the retained assembly mesh; low for optical calibration | Replace sentinel calibration with a fresh serial-specific hand-eye transform and factory intrinsics |
| Arm motion | Same six ordered joints and FollowJointTrajectory-shaped endpoint in both simulators | Good for API and nominal kinematics | Implement and commission the real adapter, compare traces, tune speed/acceleration/jerk limits, and validate stop behavior |
| Base motion | Bounded planar state proxy | API check only | Implement the real base driver and calibrated odometry; model wheel slip and whole-body collision behavior |
| Vacuum tools | Command acknowledgement only | API check only | Add pressure/airflow/seal simulation and validate thresholds against hardware logs |
| 2FG14 actuation | Command acknowledgement; static nominal jaw opening in the visual model | API check only | Add width-controlled jaw joints, force/contact response, grasp retention, and real feedback mapping |
| RGB-D | Deterministic ROS images in Gazebo and a Genesis-rendered stream; Genesis anchors to the camera plate when present and otherwise to `link_6` | Message-contract check only | Match D455 intrinsics, distortion, depth noise, rolling timing, exposure, occlusion, and calibrated extrinsics; replace the direct-mount fallback with a current measured transform |
| Collision/contact | Full visuals with simplified, conservative collision geometry | Suitable for Phase 00 smoke checks | Validate collision envelopes, friction, compliance, payload/contact parameters, and planner padding against measurements |

## Transfer rule

A simulation task may be reused on hardware only after all of these are true:

1. The task depends on the shared robot/tool contract rather than a simulator
   topic or private engine object.
2. The selected physical robot, tool, TCP, camera, payload, and speed limits have
   current calibration and commissioning records.
3. The same task has passed recorded dry-run, low-speed no-payload, and bounded
   payload stages with an operator and an accessible emergency stop.
4. Perception and grasp thresholds come from real observations, not simulator
   constants.
5. A simulator pass remains evidence for software behavior only; it never
   authorizes real motion.

Phase 00 satisfies the first part for its small motion and state seam. It does
not satisfy the hardware commissioning stages. Those remain in Phase 07.
