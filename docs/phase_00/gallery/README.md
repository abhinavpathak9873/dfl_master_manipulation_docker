# Phase 00 robot gallery

These are direct 1280 x 960 simulator captures of the implemented URDF at the
shared Phase 00 home joint position. They are not concept art. Regenerate the
complete set with `scripts/render_robot_gallery.sh`.

The images answer a visual question only: did each simulator load the selected
base, arm, mount, and tool in the intended kinematic chain? They do not prove
contact, suction, grip force, camera calibration, or safe behavior on hardware.

## Picker 1 / M1013

| Tool | Genesis | Gazebo |
| --- | --- | --- |
| VGC10 one cup | ![Picker 1 with VGC10 one cup in Genesis](genesis/picker1-vgc10_1cup.png) | ![Picker 1 with VGC10 one cup in Gazebo](gazebo/picker1-vgc10_1cup.png) |
| VGC10 four cup | ![Picker 1 with VGC10 four cup in Genesis](genesis/picker1-vgc10_4cup.png) | ![Picker 1 with VGC10 four cup in Gazebo](gazebo/picker1-vgc10_4cup.png) |
| VGP20 | ![Picker 1 with VGP20 in Genesis](genesis/picker1-vgp20.png) | ![Picker 1 with VGP20 in Gazebo](gazebo/picker1-vgp20.png) |
| 2FG14 | ![Picker 1 with 2FG14 in Genesis](genesis/picker1-2fg14.png) | ![Picker 1 with 2FG14 in Gazebo](gazebo/picker1-2fg14.png) |

## Picker 2 / M1013

| Tool | Genesis | Gazebo |
| --- | --- | --- |
| VGC10 one cup | ![Picker 2 with VGC10 one cup in Genesis](genesis/picker2-vgc10_1cup.png) | ![Picker 2 with VGC10 one cup in Gazebo](gazebo/picker2-vgc10_1cup.png) |
| VGC10 four cup | ![Picker 2 with VGC10 four cup in Genesis](genesis/picker2-vgc10_4cup.png) | ![Picker 2 with VGC10 four cup in Gazebo](gazebo/picker2-vgc10_4cup.png) |
| VGP20 | ![Picker 2 with VGP20 in Genesis](genesis/picker2-vgp20.png) | ![Picker 2 with VGP20 in Gazebo](gazebo/picker2-vgp20.png) |
| 2FG14 | ![Picker 2 with 2FG14 in Genesis](genesis/picker2-2fg14.png) | ![Picker 2 with 2FG14 in Gazebo](gazebo/picker2-2fg14.png) |

## H2515

| Tool | Genesis | Gazebo |
| --- | --- | --- |
| VGC10 one cup | ![H2515 with VGC10 one cup in Genesis](genesis/h2515-vgc10_1cup.png) | ![H2515 with VGC10 one cup in Gazebo](gazebo/h2515-vgc10_1cup.png) |
| VGC10 four cup | ![H2515 with VGC10 four cup in Genesis](genesis/h2515-vgc10_4cup.png) | ![H2515 with VGC10 four cup in Gazebo](gazebo/h2515-vgc10_4cup.png) |
| VGP20 | ![H2515 with VGP20 in Genesis](genesis/h2515-vgp20.png) | ![H2515 with VGP20 in Gazebo](gazebo/h2515-vgp20.png) |
| 2FG14 | ![H2515 with 2FG14 in Genesis](genesis/h2515-2fg14.png) | ![H2515 with 2FG14 in Gazebo](gazebo/h2515-2fg14.png) |

## Visual inspection record

All 24 images were opened and checked on 2026-08-27. The check covered full
robot framing, expected base, arm continuity, selected tool identity, missing
mesh failures, hand-camera plate presence, and agreement on the home joint pose.
The first Gazebo pass exposed a missing resource path for DFL meshes; the final
images were captured only after that defect was fixed. Picker-mounted VGC10
four-cup and 2FG14 configurations include the workspace hand-camera plate.
VGC10 one-cup and VGP20 mount directly, as they do in the source Picker
descriptions. H2515 configurations do not invent a Picker camera plate.
