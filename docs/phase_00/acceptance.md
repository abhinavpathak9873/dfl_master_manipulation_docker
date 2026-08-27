# Phase 00 acceptance record

This record separates implemented paths from evidence actually collected on
the current host. Generated result files belong under `logs/phase_00/`.

## Automated gates

- `scripts/validate_phase_00.sh`: repository, source pin, Compose, profile, and
  matrix validation.
- `scripts/3_compile_pkgs.sh`: Jazzy dependency resolution and colcon build.
- `scripts/validate_descriptions.sh`: all 12 robot/tool descriptions for
  Gazebo and Genesis backends.
- `scripts/validate_moveit_configs.sh`: M1013/H2515 SRDF, kinematics, limits,
  controller order, and tool-TCP attachment for all 12 selections.
- `scripts/run_phase0_case.sh`: one simulator case with home/probe joint motion,
  a 20 mm tool-frame-relative TCP move, tool state, camera or base checks where
  applicable, cancellation, and stop. A case fails if its measured TCP position
  remains more than 4 mm from the relative target.
- `scripts/run_phase0_matrix.sh --execute`: 24 sequential cases with individual
  logs and an aggregate summary.
- `scripts/run_dual_picker_smoke.sh`: concurrent Picker 1 and Picker 2 tasks in
  one Gazebo world.
- `scripts/smoke_doosan_emulator.sh`: pinned official emulator startup and TCP
  readiness without claiming that it drives simulator physics.
- `scripts/render_robot_gallery.sh`: direct Genesis and Gazebo captures for all
  12 robot/tool selections, stored under `docs/phase_00/gallery/`.

## Evidence collected on 2026-08-27

| Gate | Result | Scope |
| --- | --- | --- |
| Core image build | passed | Pinned Jazzy desktop base and DRCF generation 2 |
| Jazzy colcon build | passed | Ten project and upstream Doosan/MoveIt packages |
| Description expansion | 24/24 passed | 12 selections across Gazebo and Genesis backends |
| MoveIt mapping validation | 12/12 passed | Groups, limits, kinematics, controllers, and tool TCPs |
| Gazebo fixed-task matrix | 12/12 passed | Corrected mount chains; relative-TCP error 3.65–3.89 mm |
| Dual-Picker Gazebo smoke | passed | Two concurrent, namespaced Picker tasks, including relative TCP motion |
| Official Doosan emulator smoke | passed | Pinned 3.0.1 M1013 service and TCP readiness |
| Genesis image/GPU | passed | Genesis 1.3.3, PyTorch 2.11.0+cu128, RTX PRO 4500 |
| Genesis fixed-task matrix | 12/12 passed | Full arm/Picker visuals and conditional camera anchoring; relative-TCP error 0.66–3.83 mm |
| Full simulator matrix | 24/24 passed | Every declared robot/tool/mode selection, including measured relative TCP motion |
| Genesis visual gallery | 12/12 passed | Every robot/tool selection rendered from the implemented URDF at the shared home pose |
| Gazebo visual gallery | 12/12 passed | Every robot/tool selection rendered through an RGB sensor in Gazebo; full DFL mesh resolution verified after resource-path correction |
| Manual image inspection | 24/24 passed | Full framing, expected base, arm continuity, tool identity, mount chain, missing meshes, and home-pose agreement |
| Genesis timing sample | passed | 128.1 Hz; 8.2 MiB allocated, 22.0 MiB reserved |

## Evidence rules

A case is passed only when its task result reports `status=passed` and
`relative_tcp_checked=true`, with `relative_tcp_error_m <= 0.004`. A clear
unsupported-fidelity result may document a limitation but cannot silently skip
a required ROS path. Static profile or URDF validation is not simulator runtime
evidence.

Generated summaries are kept separately as
`logs/phase_00/matrix-gazebo-summary.json` and
`logs/phase_00/matrix-genesis-summary.json`, so one simulator cannot overwrite
the other's evidence. Those logs remain local runtime artifacts; this tracked
record contains the durable acceptance result.

Real hardware is outside the Phase 00 proof. Picker 1, Picker 2, H2515, every
physical tool, and both D455 serial/mount records remain `not_yet_verified` until
a later commissioning session has fresh motion authorization and mounted-hardware
evidence.

The durable images and inspection notes are in
[`gallery/README.md`](gallery/README.md). The confidence level of each modeled
part, and the work still required for safe task transfer, is recorded in
[`simulation_fidelity.md`](simulation_fidelity.md).
