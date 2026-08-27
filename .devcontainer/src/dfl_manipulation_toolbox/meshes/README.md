# DFL Picker mesh assets

These are the DFL-specific visual assets retained from
`DFL_Manipulation_Workspace/ros2_picker1_and picker2_src/picker2_description`.
That ROS package declares BSD-3-Clause and identifies Rajkumar Muthusamy as its
author and maintainer. The Doosan arm geometry is not duplicated here; it comes
from the separately pinned Apache-2.0 `doosan-robot2` checkout.

| Installed asset | Source within `picker2_description/meshes` | SHA-256 |
| --- | --- | --- |
| `picker1/base.stl` | `picker1_mobile_base/base.STL` | `b0c5c0fb5c3c7a5e28fb66b7a3d1a4bd20356e1d1251e04575eb072349ed1224` |
| `picker2/base.stl` | `picker2_mobile_base/base_link.stl` | `5aedfda5e0a13f9cc0fa8e72f3584c76e5e72a807e10a6618c8c85c115fbb5c1` |
| `tools/vgc10_1cup.dae` | `vacuum_gripper/vgc10/vacuum_gripper_vgc10_1cups.dae` | `17d717e91bfac3c06e7cdbc8ae6fdfde5d730fcc0d0fd271c0e35ed53ad90554` |
| `tools/vgc10_4cup.dae` | `vacuum_gripper/vgc10/vacuum_gripper_vgc10_4cups.dae` | `4c91ab76e4cb772713f4eed9bc0e3db14553211617a7f9fd88ba620ef1eacd85` |
| `tools/vgp20.dae` | `vacuum_gripper/vgp20/vacuum_gripper_vgp20_16cups.dae` | `564547d9526c03477a90193b6cda1a09bd161028c8c6398c7e35806f1d5c7d4e` |
| `camera/hand_camera_mount.dae` | `hand_camera/hand_camera_axis_s.dae` | `bf1c7754ad3d8dcc313a82b3b2c91ab431009d9d63ecde04e0e0cd914704bc00` |

The base and tool meshes are visual geometry. Simple declared primitives remain
the collision boundary for the composite bases and tools. The arm collision
meshes come from `doosan-robot2`; the Genesis adapter converts their DAE files
to cached STL and lets Genesis decimate and convexify them.
