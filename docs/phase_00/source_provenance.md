# Phase 00 source provenance

Generated inputs are imported through `dependencies.repos`; vendor checkouts are
not committed into the parent repository.

| Source | Revision or content hash | License | Disposition | Owning image |
|---|---|---|---|---|
| Doosan `doosan-robot2` | `816ecb5d1c2599303eaf9540216afa03552f80ad` | Apache-2.0 | Reuse directly on Jazzy; project overlays remain separate | core |
| `moveit2_calibration` | `0263c8c8aa8f1b548bf152969900d74b3fbf9a75` | BSD-3-Clause | Import when calibration work is requested | core |
| `picker1_final_moveit_config` | `08db01efd4b5ec2c75d7295a581a4eb2345419722964ae27ae59ac36fa901132` | unresolved local input | Reference/migrate after license resolution | none |
| `picker2_bringup` | `acd187e138f4bf33f932ee5cbe266a4e47f222b409e4560756cb903a45cf8da1` | unresolved local input | Reference for frames and launch behavior | none |
| `picker2_description` | `81867f72b2b504632b8ec9e75800d82fe1641e6f996f11020128d352d5501d3d` plus per-asset hashes | BSD-3-Clause as declared in `package.xml` | Retain the six DFL-specific Picker base/tool/camera visual assets; arm meshes stay with pinned Doosan source | core |
| `picker2_final_moveit_config` | `45fb366ebc83d3693f0eeed535b058a5c4fd59e5be396694271715b85f06de8f` | unresolved local input | Reference/migrate after license resolution | none |
| `rlab_zinger_4ws-main` | `4fdc8ed3f6d22c8f40d5f06aed2424d35da92ebd4f501db7714c86b971563705` | unresolved local input | Reference for installed base only; not a Phase 00 dependency | gateway |
| `ros2_pick_and_place` | `1f4a408d841cb6fa20e02befe81ccf02930070f7ad95d44a6e7813126a1403fa` | unresolved local input | Characterization input; not copied | none |
| `dff_mobile_manipulation_docker` | `b5a206e454516aeb33e257a9cc5918ce5520d82d` | project source | Behavioral reference only | none |
| `dff_labs_docker` | `b32fca56c0f8b1f5707dd50c64a0e636617df903` | project source | Jazzy/Genesis precedent; code is reworked, not vendored | genesis |
| `dff_intelligence_docker` | `0953f8151434fcfdc3b6a3ef929465dc075aa066` | project source | ObjectDB/perception reference only | later phases |
| OnRobot 2FG14 datasheet v1.2.1 | vendor PDF, accessed 2026-08-27 | reference data only | Published 155.2 x 115 x 70 mm envelope, 1.5 kg mass, and TCP dimensions used for the dimension-derived Phase 00 visual/collision model; no vendor CAD copied | core |

The local Humble `doosan-robot2` checkout was dirty when Phase 00 began and is
not an import source. `scripts/inspect_sources.py` rejects dirty or mismatched
required checkouts.

The retained Picker files, original relative paths, and individual SHA-256
values are recorded beside the assets in
`.devcontainer/src/dfl_manipulation_toolbox/meshes/README.md`. This avoids
depending on the old workspace at runtime or copying its package wholesale.

The OnRobot reference is
<https://onrobot.com/storage/datasheets/datasheet_2fg14_v1.2.1_en.pdf>.
The workspace contains no 2FG14 CAD. The URDF therefore uses labeled,
dimension-derived primitives for appearance and a conservative full-sweep box
for collision checking. It must be replaced if redistributable vendor CAD and
installed finger measurements become available.
