# DFL manipulation planning pack

## Purpose

This directory plans the first supported release of `dfl_master_manipulation_docker`. It does not authorize an implementation agent to redesign public contracts, substitute dependencies, or widen scope. A packet may investigate an uncertain fact, but a failed evidence gate stops the dependent path and records the result for review.

The pack is ordered by dependency, not by feature visibility. Phase 01 defines shared types and configuration before Phase 02 builds the task API. Later phases may investigate in parallel, but they may not implement against an unaccepted upstream contract.

## Reading order

An implementation agent receives only:

1. this overview;
2. [the global decisions](decisions/000_global_architecture.md);
3. the current phase README;
4. one assigned module plan;
5. the upstream artifacts listed under that plan's Inputs.

Read the [source inventory](research/00_source_inventory.md) when a packet depends on existing code or hardware facts. Read the [dependency audit](research/01_dependency_audit.md) for version, support, or licensing claims. Use [traceability.md](traceability.md) to find the sole owner of a requirement.

## Phase map

| Phase | Establishes | Exit required before the next dependent phase |
|---|---|---|
| [Phase 00](Phase_00/README.md) | Reproducible Jazzy images and Compose services, including the isolated ObjectDB and scan-worker foundations, plus source pins, robot/tool/scene profiles, Gazebo, and a Genesis bridge decision. | Images and mounts pass isolation checks; both robot models load; fixed tasks run in Gazebo; Genesis either passes its bridge gate or is returned for a scope decision. |
| [Phase 01](Phase_01/README.md) | Shared Python values, ROS interfaces, configuration resolution, plugin discovery, namespacing, time, and run records. | Contract tests pass and the interfaces are frozen for Phase 02 consumers. |
| [Phase 02](Phase_02/README.md) | Task-facing lifecycle, motion, Pilz, OMPL, visual servo, grippers, base velocity, and concurrent robots. | Deterministic fixed-task behavior passes in simulation and failure paths produce typed errors. |
| [Phase 03](Phase_03/README.md) | File-first object records, the always-on ObjectDB service, task/scan leases, approved-revision Git history, migration, grasp profiles, and MoveIt scene synchronization. | Four approved objects validate and resolve through the service; activation, lease, Git, outage, and scene contracts pass. |
| [Phase 04](Phase_04/README.md) | D455 dataset, SAM2, FoundationPose, M3T, track health, scene snapshots, and measured performance. | The four-object pipeline passes recorded-data accuracy, failure, memory, and two-hour tests. |
| [Phase 05](Phase_05/README.md) | Local reference/depth alignment, bounded servoing, grasp verification, and explicit retry behavior. | The representative grasp task meets its simulation and installed-hardware acceptance thresholds. |
| [Phase 06](Phase_06/README.md) | The ObjectDB scan workflow, exclusive Picker 1 capture, isolated reconstruction, revision registration, local web GUI, and grasp testing. | A new rigid opaque object passes the explicit scan, review, local Git commit, annotation, and test path without direct canonical-file mutation or hidden motion resume. |
| [Phase 07](Phase_07/README.md) | Gateway deployment, mode and scan orchestration, ObjectDB Git synchronization, DDS/QoS/time checks, recovery, simulator parity, real qualification, documentation, and release control. | Every required packet is accepted, remote backup health is proven, release evidence is indexed, and no blocking decision remains. |

## Work-packet index

- **Phase 00:** [container and Compose](Phase_00/01_container_and_compose.md), [workspace imports](Phase_00/02_workspace_imports.md), [Doosan Jazzy migration](Phase_00/03_doosan_jazzy_migration.md), [robot/tool/scene profiles](Phase_00/04_robot_tool_scene_profiles.md), [Gazebo emulator](Phase_00/05_gazebo_emulator.md), [Genesis bridge spike](Phase_00/06_genesis_bridge_spike.md), [simulator contract](Phase_00/07_simulator_contract.md), [fixed-task matrix](Phase_00/08_fixed_task_matrix.md).
- **Phase 01:** [Python value types](Phase_01/01_python_value_types.md), [ROS interfaces](Phase_01/02_ros_interfaces.md), [configuration resolution](Phase_01/03_config_resolution.md), [plugin discovery](Phase_01/04_plugin_discovery.md), [namespaces, TF, and time](Phase_01/05_namespaces_tf_and_time.md), [task-package convention](Phase_01/06_task_package_convention.md), [run records](Phase_01/07_run_records.md).
- **Phase 02:** [robot lifecycle](Phase_02/01_robot_lifecycle.md), [motion contract](Phase_02/02_motion_contract.md), [Pilz motion](Phase_02/03_pilz_motion.md), [OMPL and fallbacks](Phase_02/04_ompl_and_fallbacks.md), [visual servo](Phase_02/05_visual_servo.md), [gripper contract](Phase_02/06_gripper_contract.md), [VGC10 profiles](Phase_02/07_vgc10_profiles.md), [VGP20](Phase_02/08_vgp20.md), [2FG14](Phase_02/09_2fg14.md), [base velocity](Phase_02/10_base_velocity.md), [concurrent robots](Phase_02/11_concurrent_robots.md), [manipulation acceptance](Phase_02/12_manipulation_acceptance.md).
- **Phase 03:** [object JSON schema](Phase_03/01_object_json_schema.md), [file store and index](Phase_03/02_file_store_and_index.md), [legacy migration](Phase_03/03_legacy_migration.md), [grasp profiles](Phase_03/04_grasp_profiles.md), [object service and CLI](Phase_03/05_object_service_and_cli.md), [scene and MoveIt synchronization](Phase_03/06_scene_and_moveit_sync.md), [object contract tests](Phase_03/07_object_contract_tests.md).
- **Phase 04:** [D455 dataset](Phase_04/01_d455_dataset.md), [SAM2 segmentation](Phase_04/02_sam2_segmentation.md), [FoundationPose](Phase_04/03_foundationpose.md), [tracking contract](Phase_04/04_tracking_contract.md), [M3T ROS adapter](Phase_04/05_m3t_ros_adapter.md), [reseed and track health](Phase_04/06_reseed_and_track_health.md), [scene snapshots](Phase_04/07_scene_snapshots.md), [perception benchmarks](Phase_04/08_perception_benchmarks.md).
- **Phase 05:** [alignment contract](Phase_05/01_alignment_contract.md), [legacy characterization](Phase_05/02_legacy_characterization.md), [reference/depth alignment](Phase_05/03_reference_depth_alignment.md), [bounded visual servo](Phase_05/04_bounded_visual_servo.md), [grasp verification](Phase_05/05_grasp_verification.md), [retry and recovery](Phase_05/06_retry_and_recovery.md), [grasp acceptance](Phase_05/07_grasp_acceptance.md).
- **Phase 06:** [scan contract](Phase_06/01_scan_contract.md), [view capture](Phase_06/02_view_capture.md), [reconstruction and quality](Phase_06/03_reconstruction_and_quality.md), [revision registration](Phase_06/04_revision_registration.md), [object viewer](Phase_06/05_object_viewer.md), [atomic editor](Phase_06/06_atomic_editor.md), [grasp annotation and test](Phase_06/07_grasp_annotation_and_test.md), [scan/GUI acceptance](Phase_06/08_scan_gui_acceptance.md).
- **Phase 07:** [gateway services](Phase_07/01_gateway_services.md), [DDS, QoS, and clock](Phase_07/02_dds_qos_and_clock.md), [desktop Compose](Phase_07/03_desktop_compose.md), [session recovery](Phase_07/04_session_recovery.md), [hardware commissioning](Phase_07/05_hardware_commissioning.md), [simulator parity](Phase_07/06_simulator_parity.md), [real qualification](Phase_07/07_real_qualification.md), [module documentation](Phase_07/08_module_documentation.md), [dependency upgrades and release](Phase_07/09_dependency_upgrades_and_release.md).

## Dependency and parallel work

Phase 00 precedes all implementation. Phase 01 defines the object, lease, scan, and reconstruction wire contracts before Phase 02 builds the task client and Phase 03 implements ObjectDB. After those contracts freeze, object-schema work in Phase 03 and recorded-data preparation in Phase 04 may proceed together. Phase 05 depends on accepted Phase 02 motion behavior, Phase 03 grasp data, and Phase 04 tracked poses. Phase 06 may develop its read-only viewer after the Phase 03 schema freezes, but physical scanning waits for the Phase 02 motion path, Phase 03 leases and write service, and Phase 04 SAM2 path. Phase 07 integrates the mode and scan profiles, remote Git synchronization, and recovery behavior before final acceptance.

Phase 01 supplies frozen shared contracts to Phases 03–07. Changes to them must follow the shared-contract rule below.

Two packets may run in parallel only when their Inputs name stable shared artifacts and their Outputs do not claim the same file, schema, launch entrypoint, or ROS interface. If a shared contract changes, pause its consumers, revise the owning packet, update traceability, and reaccept the contract before work resumes.

## Evidence gates

An investigation packet ends in one of two states: accepted evidence or a blocking decision record. It never silently changes a requirement. The main early gates are Doosan Jazzy real/virtual behavior, mixed multi-robot namespacing, the official-emulator relationship to Genesis, M3T headless/Jazzy viability, and Isaac ROS memory and recovery behavior.

## Completion rule

A module is complete only when every listed output exists, every acceptance check passes, and the published interfaces match the accepted upstream contracts. A phase completes after all its packets pass and its README exit checks are recorded. `traceability.md` must show one owner for every requirement and no unexplained dependency cycle.
