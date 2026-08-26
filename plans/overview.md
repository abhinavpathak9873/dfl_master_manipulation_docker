# DFL manipulation planning pack

Status: planning only; implementation has not started

## Purpose

This directory is the complete phased plan for the internal DFL robotics
development toolbox. The full utility remains: Picker 1/M1013, Picker 2/M1013,
H2515, all four declared grippers, real/Gazebo/Genesis modes, manipulation,
perception, grasping, ObjectDB authoring/scanning, Docker, gateways, and
qualification.

The audit changes how that scope is built. The task script is the product;
ordinary Python is the default orchestrator; ROS remains visible; Docker solves
real environment and placement problems; ObjectDB runtime data is file-first;
and abstractions must pay for themselves in experiment speed or debugging
clarity.

Read these documents first:

1. [toolbox principles](principles.md) — the non-negotiable design test and full
   scope;
2. [canonical task API](api_example.md) — executable-shaped pseudocode that
   every major decision must keep readable;
3. [global decisions](decisions/000_global_architecture.md) — concrete ownership,
   repository, Docker, robot, and safety decisions;
4. [audit](audit.md) — how every restored packet was simplified without losing
   utility;
5. [traceability](traceability.md) — where each requirement is owned and checked.

Then read the current phase README and the assigned packet. Consult the
[source inventory](research/00_source_inventory.md) and focused research only
when the packet depends on those facts.

## Planning rules

- Keep all eight phases and their individual work packets.
- Use phases for ordering and evidence, not to construct a framework before the
  first useful task can run.
- Build representative vertical slices early, use the findings to sharpen small
  interfaces, and then complete the declared matrix. Sequencing is not scope
  reduction.
- A packet may investigate an uncertain dependency. If evidence disproves its
  route, record the result and choose the smallest alternative that preserves
  the user requirement; do not silently delete the capability.
- Each packet must state the task-script payoff, smallest sufficient design,
  concrete outputs, checks, and non-goals.
- Do not claim an implementation, test result, benchmark, or hardware fact until
  it exists.

## Required repository and Docker shape

The established project shape remains part of the plan:

- `.devcontainer/` owns the devcontainer, Dockerfiles, Compose files, and the
  ROS workspace mounted at `/root/ros2_ws`;
- ROS packages live directly under `.devcontainer/src/`;
- ordinary experiment scripts live under root `tasks/` unless a task genuinely
  needs to be a ROS package;
- `scripts/` owns build, setup, run, validation, and diagnostic commands;
- scenes, calibration, models, objects, data, and logs remain inspectable files;
- `plans/` owns this roadmap.

Everything is Dockerized. Containers split only at concrete dependency, GPU,
device, vendor, or host-placement boundaries. Compose starts required processes
but never replaces the Python task as the robotics workflow.

## Phase map

| Phase | Purpose | Exit evidence |
|---|---|---|
| [Phase 00](Phase_00/README.md) | Reproducible Jazzy/devcontainer and Compose foundation; dependency pins; all robot/tool/camera/scene profiles; Gazebo; Genesis bridge decision; full simulator task matrix. | Images build, mounts/devices are explicit, M1013/H2515 profiles load, Gazebo fixed tasks run, and Genesis has either an accepted bridge or a recorded preserving alternative/decision. |
| [Phase 01](Phase_01/README.md) | Lightweight values, only-needed ROS interfaces, visible configuration, direct backend maps, namespace/TF/time rules, ordinary task convention, and useful debug records. | Concrete Phase 00 and first-task adapters exercise the seams; focused tests pass; no speculative registry/service is required. |
| [Phase 02](Phase_02/README.md) | Task-facing lifecycle, arm motion, Pilz, OMPL, visual servo, every gripper, both Picker bases, concurrent Pickers, and manipulation acceptance. | Declared simulator combinations and supervised installed hardware checks demonstrate behavior and clear failure handling. |
| [Phase 03](Phase_03/README.md) | File-first object assets and revisions, legacy migration, local grasp data, loader/authoring CLI, MoveIt scene synchronization, and contract fixtures. | Four approved objects load locally, validate, transform grasps, and enter/update the planning scene without a runtime ObjectDB service. |
| [Phase 04](Phase_04/README.md) | D455 dataset, SAM2, FoundationPose, M3T, explicit tracker health/reseed, scene snapshots, and measured performance. | Four-object recorded-data checks report accuracy, latency/rate, memory, failure behavior, and declared endurance for the named stack. |
| [Phase 05](Phase_05/README.md) | Replaceable local alignment, legacy behavior characterization, bounded servoing, grasp verification, visible retry/recovery, and closed-loop acceptance. | Representative tasks pass declared simulator and installed-hardware trials with zero unsafe events. |
| [Phase 06](Phase_06/README.md) | Dockerized ObjectDB companion workflow: scan session, D455 capture, reconstruction, revision registration, viewer/editor, grasp annotation, and test. | A new rigid opaque object travels from physical scan through reviewed files and grasp test; no ObjectDB process is required afterward to load it. |
| [Phase 07](Phase_07/README.md) | Required gateways, DDS/QoS/clock setup, desktop Compose profiles, safe recovery, commissioning, simulator parity, real qualification, docs, upgrades, and internal release. | Named deployments and installed combinations have reproducible commands, evidence, limitations, rollback, and no unresolved safety blocker. |

## Work-packet index

- **Phase 00:** [container and Compose](Phase_00/01_container_and_compose.md), [workspace imports](Phase_00/02_workspace_imports.md), [Doosan Jazzy migration](Phase_00/03_doosan_jazzy_migration.md), [robot/tool/scene profiles](Phase_00/04_robot_tool_scene_profiles.md), [Gazebo emulator](Phase_00/05_gazebo_emulator.md), [Genesis bridge spike](Phase_00/06_genesis_bridge_spike.md), [simulator contract](Phase_00/07_simulator_contract.md), [fixed-task matrix](Phase_00/08_fixed_task_matrix.md).
- **Phase 01:** [Python value types](Phase_01/01_python_value_types.md), [ROS interfaces](Phase_01/02_ros_interfaces.md), [configuration resolution](Phase_01/03_config_resolution.md), [direct backend mapping](Phase_01/04_plugin_discovery.md), [namespaces, TF, and time](Phase_01/05_namespaces_tf_and_time.md), [task-script convention](Phase_01/06_task_package_convention.md), [run records](Phase_01/07_run_records.md).
- **Phase 02:** [robot lifecycle](Phase_02/01_robot_lifecycle.md), [motion API](Phase_02/02_motion_contract.md), [Pilz motion](Phase_02/03_pilz_motion.md), [OMPL and fallbacks](Phase_02/04_ompl_and_fallbacks.md), [visual servo](Phase_02/05_visual_servo.md), [gripper API](Phase_02/06_gripper_contract.md), [VGC10 profiles](Phase_02/07_vgc10_profiles.md), [VGP20](Phase_02/08_vgp20.md), [2FG14](Phase_02/09_2fg14.md), [base velocity](Phase_02/10_base_velocity.md), [concurrent robots](Phase_02/11_concurrent_robots.md), [manipulation acceptance](Phase_02/12_manipulation_acceptance.md).
- **Phase 03:** [object JSON schema](Phase_03/01_object_json_schema.md), [file store and index](Phase_03/02_file_store_and_index.md), [legacy migration](Phase_03/03_legacy_migration.md), [grasp profiles](Phase_03/04_grasp_profiles.md), [local loader and authoring CLI](Phase_03/05_object_service_and_cli.md), [scene and MoveIt synchronization](Phase_03/06_scene_and_moveit_sync.md), [object contract tests](Phase_03/07_object_contract_tests.md).
- **Phase 04:** [D455 dataset](Phase_04/01_d455_dataset.md), [SAM2 segmentation](Phase_04/02_sam2_segmentation.md), [FoundationPose](Phase_04/03_foundationpose.md), [tracking API](Phase_04/04_tracking_contract.md), [M3T ROS adapter](Phase_04/05_m3t_ros_adapter.md), [reseed and track health](Phase_04/06_reseed_and_track_health.md), [scene snapshots](Phase_04/07_scene_snapshots.md), [perception benchmarks](Phase_04/08_perception_benchmarks.md).
- **Phase 05:** [alignment API](Phase_05/01_alignment_contract.md), [legacy characterization](Phase_05/02_legacy_characterization.md), [reference/depth alignment](Phase_05/03_reference_depth_alignment.md), [bounded visual servo](Phase_05/04_bounded_visual_servo.md), [grasp verification](Phase_05/05_grasp_verification.md), [retry and recovery](Phase_05/06_retry_and_recovery.md), [grasp acceptance](Phase_05/07_grasp_acceptance.md).
- **Phase 06:** [scan workflow](Phase_06/01_scan_contract.md), [view capture](Phase_06/02_view_capture.md), [reconstruction and quality](Phase_06/03_reconstruction_and_quality.md), [revision registration](Phase_06/04_revision_registration.md), [object viewer](Phase_06/05_object_viewer.md), [atomic editor](Phase_06/06_atomic_editor.md), [grasp annotation and test](Phase_06/07_grasp_annotation_and_test.md), [scan/GUI acceptance](Phase_06/08_scan_gui_acceptance.md).
- **Phase 07:** [gateway services](Phase_07/01_gateway_services.md), [DDS, QoS, and clock](Phase_07/02_dds_qos_and_clock.md), [desktop Compose](Phase_07/03_desktop_compose.md), [session recovery](Phase_07/04_session_recovery.md), [hardware commissioning](Phase_07/05_hardware_commissioning.md), [simulator parity](Phase_07/06_simulator_parity.md), [real qualification](Phase_07/07_real_qualification.md), [module documentation](Phase_07/08_module_documentation.md), [dependency upgrades and release](Phase_07/09_dependency_upgrades_and_release.md).

## Dependency and parallel-work rule

Phase 00 establishes usable Docker and robot/simulator foundations. After that,
packets may proceed as soon as their concrete inputs exist. Do not hold a useful
vertical task behind a phase-wide "contract freeze." For example, a first
Gazebo tray task can exercise values, robot lifecycle, one gripper, local object
loading, and one perception path while the remaining robot/tool matrix continues
in parallel.

Share a file or ROS interface only when two real consumers need it. One packet
owns each shared artifact. If a change affects active consumers, update the
owner, examples, checks, and traceability together. Parallel packets must not
silently edit the same public API, profile, Compose entry point, or schema.

Phase 05 depends on usable manipulation, grasp assets, and tracked poses. Phase
06 reuses the same robot, camera, perception, and object-file primitives; it is
not a runtime prerequisite for those primitives. Phase 07 can validate gateway,
network, Compose, and commissioning work as the associated hardware path becomes
available rather than waiting to become a final deployment program.

## Evidence gates

An investigation packet ends with evidence and a decision. It never silently
changes user scope. The important early uncertainties include Doosan Jazzy
real/emulated behavior, multi-robot namespacing, the Genesis/emulator bridge,
M3T headless/Jazzy viability, and accelerated perception GPU/memory behavior.

If the preferred route fails, the packet documents the smallest alternative,
its task-script effect, and the remaining limitation. A material scope change
returns for user review.

## Completion rule

A packet is complete only when its concrete outputs exist, its focused checks
pass, its task-script payoff is demonstrated, and its limitations are written
plainly. A phase completes when all retained packets meet their acceptance
checks. `traceability.md` must name an owner and evidence for each requirement.
