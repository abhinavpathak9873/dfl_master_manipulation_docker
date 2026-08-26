# Requirement ownership and traceability

## Ownership rule

Each requirement has one primary packet. Other packets consume its concrete
output without redefining it. Ownership prevents contradictory files; it does
not require a global contract layer or phase-wide freeze.

| Requirement | Primary owner | Proof or main consumer |
|---|---|---|
| Dockerized Jazzy/devcontainer and dependency-focused Compose profiles | Phase 00 / `01_container_and_compose.md` | Build, device, GPU, mount, health, and smoke checks used by every phase |
| Established `.devcontainer/src`, `scripts`, file-data, and ordinary-task layout | Phase 00 / `01_container_and_compose.md`; Phase 01 / `06_task_package_convention.md` | Repository-shape check and canonical task command |
| Pinned source imports and provenance | Phase 00 / `02_workspace_imports.md` | Rebuild from clean checkout; upgrade packet consumes pins |
| Doosan Jazzy M1013 and H2515 integration | Phase 00 / `03_doosan_jazzy_migration.md` | Robot descriptions/controllers/MoveIt/emulator checks |
| Picker 1, Picker 2, H2515, four tools, cameras, scenes, and modes | Phase 00 / `04_robot_tool_scene_profiles.md` | Profile enumeration and matrix packets |
| Gazebo official-emulator path | Phase 00 / `05_gazebo_emulator.md` | Fixed manipulation smoke tasks |
| Genesis control route and evidence gate | Phase 00 / `06_genesis_bridge_spike.md` | Same task-level observations as Gazebo or documented preserving alternative |
| Shared simulator ROS behavior | Phase 00 / `07_simulator_contract.md` | Gazebo/Genesis parity checks and real-adapter consumers |
| All 12 robot/tool selections in both simulators | Phase 00 / `08_fixed_task_matrix.md` | 24 compact, repeatable task runs |
| Lightweight `Pose`, `Joints`, and useful results/errors | Phase 01 / `01_python_value_types.md` | Task API examples and focused unit tests |
| Only-needed custom cross-process ROS types | Phase 01 / `02_ros_interfaces.md` | Actual adapters/actions that cannot use standard ROS types |
| Visible task parameters and adapter-owned shared configuration | Phase 01 / `03_config_resolution.md` | Printed selected sources and representative constructors |
| Direct backend ID-to-file/class mappings | Phase 01 / `04_plugin_discovery.md` | Add one example backend with one mapping and focused test |
| Robot namespaces, TF, REP-103 units, source time, and freshness | Phase 01 / `05_namespaces_tf_and_time.md` | Concurrent Picker and perception transform checks |
| Ordinary `tasks/*.py` convention and optional ROS-packaged task exception | Phase 01 / `06_task_package_convention.md` | Canonical tray task reads top-to-bottom and runs by one command |
| Small opt-in run/debug evidence | Phase 01 / `07_run_records.md` | Benchmark/qualification packets and failure diagnosis |
| `Robot.bringup()`, attach, readiness, and owned cleanup | Phase 02 / `01_robot_lifecycle.md` | Gazebo and supervised-real start/stop tests |
| Arm move/plan/execute/relative/stop API | Phase 02 / `02_motion_contract.md` | Phase 02 fixed task and Phase 05 grasp task |
| Pilz PTP/LIN/CIRC | Phase 02 / `03_pilz_motion.md` | Simulator trajectory/stop checks and real characterization |
| OMPL and explicit pre-execution fallbacks | Phase 02 / `04_ompl_and_fallbacks.md` | Collision-aware named tasks and attempt evidence |
| Bounded position/velocity visual servo | Phase 02 / `05_visual_servo.md` | Phase 05 local-alignment loop |
| Shared minimal gripper behavior and result fields | Phase 02 / `06_gripper_contract.md` | Four concrete tool packets and task retry logic |
| VGC10 one-cup and four-cup | Phase 02 / `07_vgc10_profiles.md` | Simulator/installed tool checks |
| VGP20 | Phase 02 / `08_vgp20.md` | Simulator/installed tool checks |
| 2FG14 | Phase 02 / `09_2fg14.md` | Width/force/result checks and grasp task |
| Bounded Picker mobile-base velocity and stop | Phase 02 / `10_base_velocity.md` | Namespaced simulator and installed-base checks |
| Concurrent Picker 1 and Picker 2 | Phase 02 / `11_concurrent_robots.md` | Collision-free ROS graph plus explicit concurrent task |
| Manipulation phase acceptance | Phase 02 / `12_manipulation_acceptance.md` | Declared matrix and representative tasks |
| Small extensible object JSON | Phase 03 / `01_object_json_schema.md` | Four-object fixtures and Phase 04/05 consumers |
| Normal file store, approved revisions, and optional rebuildable index | Phase 03 / `02_file_store_and_index.md` | Delete/rebuild index and local load checks |
| Four approved legacy-object migration | Phase 03 / `03_legacy_migration.md` | Source-to-file validation report |
| Object-frame anchors and optional tool-specific grasp data | Phase 03 / `04_grasp_profiles.md` | Local transform and all-tool preview tests |
| Local `objectdb.load` plus authoring validate/inspect/revision CLI | Phase 03 / `05_object_service_and_cli.md` | Task loads with no ObjectDB process; authoring atomic-write checks |
| Scene folders and explicit MoveIt planning-scene synchronization | Phase 03 / `06_scene_and_moveit_sync.md` | Loaded/static/tracked collision-object fixtures |
| Object/file/grasp/scene contract suite | Phase 03 / `07_object_contract_tests.md` | Phase 03 acceptance |
| D455 recorded benchmark dataset | Phase 04 / `01_d455_dataset.md` | Phase 04 and 05 backend tests |
| SAM2 segmentation backend | Phase 04 / `02_sam2_segmentation.md` | Mask quality, latency, failure, Docker restart tests |
| FoundationPose estimate and reseed backend | Phase 04 / `03_foundationpose.md` | Pose accuracy/stability and missing-mesh errors |
| Explicit tracker state/API | Phase 04 / `04_tracking_contract.md` | M3T implementation and task loop |
| M3T native/ROS adapter | Phase 04 / `05_m3t_ros_adapter.md` | Headless/Jazzy/mesh/seed/rate evidence |
| Track health and explicit reseed | Phase 04 / `06_reseed_and_track_health.md` | Occlusion/stale/lost/recovery fixtures |
| Timestamped multi-object scene snapshots | Phase 04 / `07_scene_snapshots.md` | Planning-scene and grasp consumers |
| Perception accuracy/rate/memory/endurance benchmarks | Phase 04 / `08_perception_benchmarks.md` | Named-stack qualification report |
| Replaceable local-alignment API | Phase 05 / `01_alignment_contract.md` | Multiple or reference backend task examples |
| Existing alignment behavior characterization | Phase 05 / `02_legacy_characterization.md` | Golden fixtures consumed by reference backend |
| Reference/mask/depth XY/RPY alignment | Phase 05 / `03_reference_depth_alignment.md` | Recorded and live debug comparisons |
| Bounded visible alignment servo loop | Phase 05 / `04_bounded_visual_servo.md` | Convergence/loss/limit/stop tests |
| Tool-aware grasp verification | Phase 05 / `05_grasp_verification.md` | Suction/width/force/lift evidence |
| Explicit Python retry and uncertain-state recovery | Phase 05 / `06_retry_and_recovery.md` | Readable task examples and injected failures |
| Closed-loop grasp acceptance | Phase 05 / `07_grasp_acceptance.md` | Four-object/supported-tool declared trials |
| File-backed scan stages and eligibility | Phase 06 / `01_scan_contract.md` | Stop/review/resume fixtures; no runtime task lease dependency |
| Guided Picker 1/D455 multi-view capture | Phase 06 / `02_view_capture.md` | Calibrated, timestamped accepted views and safe interruption |
| On-demand reconstruction and mesh-quality decision | Phase 06 / `03_reconstruction_and_quality.md` | Isolated Docker job and metric quality report |
| Reviewed scan output to validated object revision | Phase 06 / `04_revision_registration.md` | Atomic file registration and local reload |
| Read-only local object/scan viewer | Phase 06 / `05_object_viewer.md` | Visual fixture checks |
| Validated single-user atomic editor | Phase 06 / `06_atomic_editor.md` | Invalid-edit rejection and new-revision write |
| Grasp annotation, preview, and explicit robot test | Phase 06 / `07_grasp_annotation_and_test.md` | Same file and task primitives as runtime |
| Physical object to reusable task asset | Phase 06 / `08_scan_gui_acceptance.md` | End-to-end scan/approve/load/grasp report |
| Physically required NUC/Jetson gateway behavior | Phase 07 / `01_gateway_services.md` | Device/state/watchdog/disconnect tests |
| DDS discovery, QoS, bandwidth, identity, and clock | Phase 07 / `02_dds_qos_and_clock.md` | ROS CLI and network measurements |
| Desktop Compose dependency profiles | Phase 07 / `03_desktop_compose.md` | One-command mode/scan profiles with task logic still in Python |
| Safe restart and explicit fresh-run recovery | Phase 07 / `04_session_recovery.md` | Fault-injection and no-auto-motion checks |
| Mounted hardware commissioning | Phase 07 / `05_hardware_commissioning.md` | Identity/calibration/limits/stop/tool records |
| Gazebo/Genesis shared-operation parity | Phase 07 / `06_simulator_parity.md` | Full declared matrix with honest difference report |
| Installed real-hardware qualification | Phase 07 / `07_real_qualification.md` | Declared supervised trials and zero unsafe events |
| Architecture, task API, backend, Docker, diagnostics, and limitation docs | Phase 07 / `08_module_documentation.md` | Human/agent navigation checks |
| Pinned dependency upgrades, rollback, reproducible internal release | Phase 07 / `09_dependency_upgrades_and_release.md` | Affected-test report and image/source pins |

## Coverage audit

Before an internal release, compare this table with the phase packets and the
canonical task example. Add a row for an uncovered user requirement. If two
packets claim the same implementation file or public seam, choose one owner and
make the other an explicit consumer. Never create a registry or service merely
to resolve unclear written ownership.
