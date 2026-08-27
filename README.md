# DFL Master Manipulation Docker

ROS 2 Jazzy development workspace for the DFL manipulation toolbox. Phase 00
provides pinned containers, source imports, profiles, description validation,
Gazebo entry points, a Genesis bridge spike, and the fixed simulator matrix.

The host workspace follows the established DFF layout:

```text
.devcontainer/       devcontainer, Compose, Dockerfiles, ROS source
.devcontainer/src/   project ROS packages and reproducible vendor checkouts
tasks/               ordinary Python experiment scripts
scripts/             build, import, run, inspect, and validation commands
calibration/         commissioned calibration files
data/                durable runtime and scan data
logs/                generated evidence
models/              model and engine mounts
objects/             file-first object assets
plans/               accepted roadmap
```

## Phase 00 quick start

```bash
cp .env.example .env
scripts/1_import_sources.sh
scripts/0_build_images.sh all
scripts/compose.sh dev up -d core
scripts/compose.sh dev exec -T core /opt/dfl/scripts/3_compile_pkgs.sh
scripts/compose.sh genesis up -d genesis
scripts/compose.sh genesis exec -T genesis /opt/dfl/scripts/3_compile_pkgs.sh --genesis
scripts/validate_phase_00.sh
```

Start an interactive development container:

```bash
scripts/compose.sh dev up -d core
scripts/compose.sh dev exec core bash
```

Run the non-motion matrix validation:

```bash
python3 scripts/run_phase0_matrix.py
```

Simulator execution is opt-in and records evidence under `logs/phase_00/`:

```bash
scripts/run_phase0_matrix.sh --execute --mode gazebo
scripts/run_phase0_matrix.sh --execute --mode genesis
scripts/run_dual_picker_smoke.sh
```

Each matrix case checks joint motion, a 20 mm tool-frame-relative TCP move with
a 4 mm measured-position limit, tool command/state, cancellation and stop. The
Picker cases also check their namespaced RGB-D and base-state paths.

The Picker visuals use their distinct base, camera-mount, and supported vacuum
tool meshes retained from `DFL_Manipulation_Workspace`. The M1013/H2515 meshes
come from the pinned Jazzy Doosan source. Produce an inspectable PNG with:

```bash
scripts/render_genesis_preview.sh picker1 vgc10_1cup
```

The pinned official Doosan controller emulator is available as a separate,
one-robot diagnostic boundary. Gazebo physics does not pretend to be driven by
it; start it explicitly when validating the vendor virtual-controller surface:

```bash
scripts/smoke_doosan_emulator.sh
```

Real hardware is not commissioned by Phase 00. The real Compose profile starts
in diagnostics-only mode. Motion remains refused until the current session has
fresh operator authorization and passes `scripts/real_mode_guard.sh`.
