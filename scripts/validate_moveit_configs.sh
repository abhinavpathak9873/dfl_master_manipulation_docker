#!/usr/bin/env bash
set -euo pipefail

set +u
source "/opt/ros/${ROS_DISTRO:-jazzy}/setup.bash"
if [[ -f /root/ros2_ws/install/setup.bash ]]; then
  source /root/ros2_ws/install/setup.bash
fi
set -u

description=$(ros2 pkg prefix --share dfl_manipulation_toolbox)/urdf/dfl_robot.urdf.xacro
scratch=$(mktemp -d /tmp/dfl-moveit-validation.XXXXXX)
trap 'rm -r -- "$scratch"' EXIT

count=0
for robot_model in picker1:m1013 picker2:m1013 h2515:h2515; do
  robot=${robot_model%%:*}
  model=${robot_model##*:}
  moveit_share=$(ros2 pkg prefix --share "dsr_moveit_config_${model}")
  xacro "$moveit_share/config/dsr.srdf.xacro" > "$scratch/$model.srdf"
  for tool in vgc10_1cup vgc10_4cup vgp20 2fg14; do
    urdf="$scratch/$robot-$tool.urdf"
    xacro "$description" robot:="$robot" arm_model:="$model" tool:="$tool" \
      namespace:="$robot" control_backend:=none > "$urdf"
    python3 - "$urdf" "$scratch/$model.srdf" \
      "$moveit_share/config/kinematics.yaml" \
      "$moveit_share/config/joint_limits.yaml" \
      "$moveit_share/config/moveit_controllers.yaml" <<'PY'
import sys
import xml.etree.ElementTree as ET

import yaml

urdf_path, srdf_path, kinematics_path, limits_path, controllers_path = sys.argv[1:]
urdf = ET.parse(urdf_path).getroot()
srdf = ET.parse(srdf_path).getroot()
expected = [f"joint_{index}" for index in range(1, 7)]

group = next((item for item in srdf.findall("group") if item.get("name") == "manipulator"), None)
chain = group.find("chain") if group is not None else None
if chain is None or chain.get("base_link") != "base_link" or chain.get("tip_link") != "link_6":
    raise SystemExit(f"{srdf_path}: invalid manipulator chain")

kinematics = yaml.safe_load(open(kinematics_path, encoding="utf-8"))
if not kinematics.get("manipulator", {}).get("kinematics_solver"):
    raise SystemExit(f"{kinematics_path}: no manipulator kinematics solver")
limits = yaml.safe_load(open(limits_path, encoding="utf-8"))["joint_limits"]
if sorted(limits) != expected:
    raise SystemExit(f"{limits_path}: joint limit keys do not match {expected}")
controllers = yaml.safe_load(open(controllers_path, encoding="utf-8"))["moveit_simple_controller_manager"]
controller_name = controllers["controller_names"][0]
if controllers[controller_name]["joints"] != expected:
    raise SystemExit(f"{controllers_path}: controller joint order does not match {expected}")

parents = {}
for joint in urdf.findall("joint"):
    parent = joint.find("parent")
    child = joint.find("child")
    if parent is not None and child is not None:
        parents[child.get("link")] = parent.get("link")
current = "tool_tcp"
seen = set()
while current in parents and current not in seen:
    seen.add(current)
    current = parents[current]
if "link_6" not in seen:
    raise SystemExit(f"{urdf_path}: tool_tcp is not attached below link_6")
if urdf.find(".//link[@name='tool_tcp']") is None:
    raise SystemExit(f"{urdf_path}: tool_tcp link is missing")
PY
    count=$((count + 1))
  done
done

echo "validated MoveIt mappings for $count robot/tool selections"
