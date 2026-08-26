# Requirement ownership and traceability

## Ownership rule

Each requirement has one primary work packet. Other packets may consume its outputs but must not redefine them. Shared contracts are accepted before implementation packets proceed.

| Requirement | Primary owner | Main consumers |
|---|---|---|
| Reproducible Jazzy container and Compose services | Phase 00 / `01_container_and_compose.md` | All phases |
| ObjectDB, scan-worker, and Git-sync image/mount isolation | Phase 00 / `01_container_and_compose.md` | Phases 03, 06, 07 |
| Pinned source workspace and existing package integration | Phase 00 / `02_workspace_imports.md` | Phases 01, 02, 07 |
| `dff_mobile_manipulation_docker`-compatible directory pattern | Phase 00 / `01_container_and_compose.md`, `02_workspace_imports.md` | Phases 01, 07 and release structure gate |
| Doosan Jazzy M1013/H2515 migration | Phase 00 / `03_doosan_jazzy_migration.md` | Phases 02, 07 |
| Independent robot, tool, scene, mode, and pipeline selection | Phase 00 / `04_robot_tool_scene_profiles.md` | Phases 01, 02, 03, 07 |
| Official-emulator Gazebo path | Phase 00 / `05_gazebo_emulator.md` | Phases 02, 07 |
| Genesis control feasibility and bridge contract | Phase 00 / `06_genesis_bridge_spike.md` | Phases 02, 07 |
| Simulator-neutral control contract | Phase 00 / `07_simulator_contract.md` | Phases 01, 02, 07 |
| Fixed-pose smoke matrix | Phase 00 / `08_fixed_task_matrix.md` | Phase 02 |
| Python task value types and typed failures | Phase 01 / `01_python_value_types.md` | Phases 02–06 |
| Custom ROS interfaces | Phase 01 / `02_ros_interfaces.md` | Phases 02–07 |
| Runtime lease and scan/reconstruction wire contracts | Phase 01 / `02_ros_interfaces.md` | Phases 02, 03, 06, 07 |
| Deterministic layered configuration | Phase 01 / `03_config_resolution.md` | Phases 02–07 |
| Discoverable plugins and stable IDs | Phase 01 / `04_plugin_discovery.md` | Phases 02, 04, 05, 07 |
| Namespace, TF, units, and time rules | Phase 01 / `05_namespaces_tf_and_time.md` | All runtime phases |
| External task package layout | Phase 01 / `06_task_package_convention.md` | Phases 02, 05, 07 |
| Run manifests and failure buffers | Phase 01 / `07_run_records.md` | All acceptance packets |
| `Robot.bringup()` ownership and attach mode | Phase 02 / `01_robot_lifecycle.md` | Phase 07 |
| Task lease acquisition, heartbeat, and release | Phase 02 / `01_robot_lifecycle.md` | Phases 03, 06, 07 |
| Plan/execute and combined motion API | Phase 02 / `02_motion_contract.md` | Phases 05, 06 |
| Pilz PTP/LIN/CIRC behavior | Phase 02 / `03_pilz_motion.md` | Phases 05–07 |
| OMPL and explicit pre-execution fallbacks | Phase 02 / `04_ompl_and_fallbacks.md` | Phases 05–07 |
| Visual-servo behavior | Phase 02 / `05_visual_servo.md` | Phase 05 |
| Shared gripper contract | Phase 02 / `06_gripper_contract.md` | Tool packets and Phases 03, 05, 06 |
| VGC10 one/four cup | Phase 02 / `07_vgc10_profiles.md` | Phases 05–07 |
| VGP20 | Phase 02 / `08_vgp20.md` | Phases 05–07 |
| 2FG14 | Phase 02 / `09_2fg14.md` | Phases 03, 05–07 |
| Bounded `cmd_vel` base control | Phase 02 / `10_base_velocity.md` | Phase 07 |
| Concurrent Picker 1/Picker 2 operation | Phase 02 / `11_concurrent_robots.md` | Phase 07 |
| Manipulation integration acceptance | Phase 02 / `12_manipulation_acceptance.md` | Phases 05–07 |
| Canonical object JSON schema | Phase 03 / `01_object_json_schema.md` | Phases 04–06 |
| File revisions and rebuildable index | Phase 03 / `02_file_store_and_index.md` | Phase 06 |
| Nested `dfl_object_db` Git history and approved-bundle policy | Phase 03 / `02_file_store_and_index.md` | Phases 06, 07 |
| Four-object approved migration | Phase 03 / `03_legacy_migration.md` | Phases 04–06 |
| Gripper-bound grasp profiles | Phase 03 / `04_grasp_profiles.md` | Phases 05, 06 |
| Atomic object service and CLI | Phase 03 / `05_object_service_and_cli.md` | Phase 06 |
| Always-on ObjectDB runtime, sole-writer mount, leases, and outage behavior | Phase 03 / `05_object_service_and_cli.md` | Phases 04–07 |
| Scene folders and MoveIt synchronization | Phase 03 / `06_scene_and_moveit_sync.md` | Phases 04, 05, 07 |
| Object schema, store, and service contract suite | Phase 03 / `07_object_contract_tests.md` | Phases 04–07 |
| D455 benchmark dataset | Phase 04 / `01_d455_dataset.md` | Phase 04 and 05 |
| SAM2 segmentation | Phase 04 / `02_sam2_segmentation.md` | Phase 04, 05, 06 |
| FoundationPose initialization/reseed | Phase 04 / `03_foundationpose.md` | Phase 04, 05 |
| Tracker-neutral output contract | Phase 04 / `04_tracking_contract.md` | Phase 04, 05 |
| M3T ROS adapter | Phase 04 / `05_m3t_ros_adapter.md` | Phase 04, 05 |
| Track health and reseed | Phase 04 / `06_reseed_and_track_health.md` | Phase 05 |
| Timestamped scene snapshot | Phase 04 / `07_scene_snapshots.md` | Phases 03, 05 |
| Perception benchmarks and two-hour test | Phase 04 / `08_perception_benchmarks.md` | Phase 07 |
| Local-alignment contract | Phase 05 / `01_alignment_contract.md` | Phase 05 implementations |
| Existing alignment characterization | Phase 05 / `02_legacy_characterization.md` | Phase 05 / `03_reference_depth_alignment.md` |
| Reference/mask/depth alignment | Phase 05 / `03_reference_depth_alignment.md` | Phase 05 / `04_bounded_visual_servo.md` |
| Bounded servo orchestration | Phase 05 / `04_bounded_visual_servo.md` | Phase 05 / `07_grasp_acceptance.md` |
| Grasp verification | Phase 05 / `05_grasp_verification.md` | Phase 05 / `06_retry_and_recovery.md` |
| Retry and explicit recovery | Phase 05 / `06_retry_and_recovery.md` | Phase 07 |
| Closed-loop grasp acceptance | Phase 05 / `07_grasp_acceptance.md` | Phases 06, 07 |
| Scan-session state and eligibility | Phase 06 / `01_scan_contract.md` | Phase 06 packets |
| Exclusive scan lease, Picker 1 station, explicit start, and stage resume | Phase 06 / `01_scan_contract.md` | Phase 06 packets and Phase 07 recovery |
| Guided calibrated view capture | Phase 06 / `02_view_capture.md` | Phase 06 / `03_reconstruction_and_quality.md` |
| Reconstruction and mesh-quality decision | Phase 06 / `03_reconstruction_and_quality.md` | Phase 06 / `04_revision_registration.md` |
| Isolated on-demand scan-worker runtime | Phase 06 / `03_reconstruction_and_quality.md` | Phase 06 acceptance and Phase 07 Compose |
| Draft revision registration and approval | Phase 06 / `04_revision_registration.md` | Phase 06 GUI packets |
| Read-only local object viewer | Phase 06 / `05_object_viewer.md` | Phase 06 / `06_atomic_editor.md` and `07_grasp_annotation_and_test.md` |
| Atomic object editor | Phase 06 / `06_atomic_editor.md` | Phase 06 acceptance |
| Grasp annotation, preview, and test | Phase 06 / `07_grasp_annotation_and_test.md` | Phase 06 acceptance |
| Scan-to-approved-object acceptance | Phase 06 / `08_scan_gui_acceptance.md` | Phase 07 documentation and release |
| Robot-side gateway process contract | Phase 07 / `01_gateway_services.md` | Phase 07 integration |
| DDS, QoS, discovery, and clock qualification | Phase 07 / `02_dds_qos_and_clock.md` | Phase 07 integration and release |
| Desktop Compose orchestration | Phase 07 / `03_desktop_compose.md` | Phase 07 qualification |
| One-command exclusive scan profile | Phase 07 / `03_desktop_compose.md` | Phase 07 qualification and operations |
| Restart and explicit recovery behavior | Phase 07 / `04_session_recovery.md` | Phase 07 qualification |
| Mounted hardware identity and commissioning | Phase 07 / `05_hardware_commissioning.md` | Phase 07 real trials |
| Gazebo/Genesis/real task parity | Phase 07 / `06_simulator_parity.md` | Phase 07 real trials and release |
| Thirty-trial real qualification | Phase 07 / `07_real_qualification.md` | Release |
| Generated module and operator documentation | Phase 07 / `08_module_documentation.md` | Release and implementation agents |
| Dependency upgrade evidence and release index | Phase 07 / `09_dependency_upgrades_and_release.md` | Release |
| Asynchronous private GitHub/Git LFS backup and stale-backup health | Phase 07 / `09_dependency_upgrades_and_release.md` | Release and operations |

## Coverage audit

Before release, compare this table with the revised master plan line by line. Add a row for any uncovered requirement. If two packets claim the same interface or stored field, move that decision into one contract packet and update both consumers.
