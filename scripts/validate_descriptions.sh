#!/usr/bin/env bash
set -euo pipefail

set +u
source "/opt/ros/${ROS_DISTRO:-jazzy}/setup.bash"
set -u
if [[ -f /root/ros2_ws/install/setup.bash ]]; then
  set +u
  source /root/ros2_ws/install/setup.bash
  set -u
fi

description=$(ros2 pkg prefix --share dfl_manipulation_toolbox)/urdf/dfl_robot.urdf.xacro
scratch=$(mktemp -d /tmp/dfl-description-validation.XXXXXX)
trap 'rm -r -- "$scratch"' EXIT

count=0
for robot_model in picker1:m1013 picker2:m1013 h2515:h2515; do
  robot=${robot_model%%:*}
  model=${robot_model##*:}
  for tool in vgc10_1cup vgc10_4cup vgp20 2fg14; do
    for backend in gazebo none; do
      output="$scratch/$robot-$tool-$backend.urdf"
      xacro "$description" robot:="$robot" arm_model:="$model" tool:="$tool" \
        namespace:="$robot" control_backend:="$backend" > "$output"
      python3 - "$output" "$backend" <<'PY'
import sys
import xml.etree.ElementTree as ET

path, backend = sys.argv[1:]
root = ET.parse(path).getroot()
links = [element.attrib["name"] for element in root.findall("link")]
joints = [element.attrib["name"] for element in root.findall("joint")]
if len(links) != len(set(links)):
    raise SystemExit(f"{path}: duplicate links")
if len(joints) != len(set(joints)):
    raise SystemExit(f"{path}: duplicate joints")
required = {"world", "base_link", "link_6", "tool_tcp"}
missing = required.difference(links)
if missing:
    raise SystemExit(f"{path}: missing links {sorted(missing)}")
movable = {joint.attrib["name"] for joint in root.findall("joint") if joint.attrib.get("type") != "fixed"}
expected = {f"joint_{index}" for index in range(1, 7)}
if movable != expected:
    raise SystemExit(f"{path}: movable joints {sorted(movable)}, expected {sorted(expected)}")
if backend == "gazebo" and root.find("ros2_control") is None:
    raise SystemExit(f"{path}: Gazebo description has no ros2_control block")
if backend == "none" and root.find("ros2_control") is not None:
    raise SystemExit(f"{path}: Genesis description unexpectedly has ros2_control")
PY
      count=$((count + 1))
    done
  done
done

echo "validated $count description/backend selections"
