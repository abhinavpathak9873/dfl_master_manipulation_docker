#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 || $# -gt 3 ]]; then
  echo "usage: scripts/render_gazebo_preview.sh <picker1|picker2|h2515> <vgc10_1cup|vgc10_4cup|vgp20|2fg14> [output.png]" >&2
  exit 2
fi

robot=$1
tool=$2
output=${3:-"/workspace/logs/phase_00/gazebo-${robot}-${tool}-preview.png"}
case "$robot" in picker1|picker2) model=m1013;; h2515) model=h2515;; *) echo "invalid robot: $robot" >&2; exit 2;; esac
case "$tool" in vgc10_1cup|vgc10_4cup|vgp20|2fg14) ;; *) echo "invalid tool: $tool" >&2; exit 2;; esac

repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
"$repo_root/scripts/compose.sh" gazebo up -d gazebo
"$repo_root/scripts/compose.sh" gazebo restart gazebo >/dev/null
"$repo_root/scripts/compose.sh" gazebo exec -T gazebo bash -lc "set -euo pipefail
  set +u
  source /opt/ros/jazzy/setup.bash
  source /root/ros2_ws/install/setup.bash
  set -u
  ros2 launch dfl_manipulation_toolbox gazebo.launch.py robot:=$robot model:=$model tool:=$tool world:=/root/ros2_ws/install/dfl_manipulation_toolbox/share/dfl_manipulation_toolbox/scenes/gallery/world.sdf > /tmp/dfl-gallery-launch.log 2>&1 &
  launch_pid=\$!
  cleanup() {
    kill -INT \$launch_pid 2>/dev/null || true
    for _ in {1..50}; do
      kill -0 \$launch_pid 2>/dev/null || return 0
      sleep 0.1
    done
    kill -TERM \$launch_pid 2>/dev/null || true
  }
  trap cleanup EXIT
  timeout 60s ros2 topic echo /$robot/ready std_msgs/msg/Bool --once >/dev/null
  ros2 topic pub --times 3 --rate 5 /$robot/dsr_position_controller/commands std_msgs/msg/Float64MultiArray '{data: [0.0, 0.0, 1.5708, 0.0, 1.5708, 0.0]}' >/dev/null
  sleep 3
  ros2 run ros_gz_bridge parameter_bridge '/gallery/camera/image@sensor_msgs/msg/Image[gz.msgs.Image' > /tmp/dfl-gallery-bridge.log 2>&1 &
  bridge_pid=\$!
  trap 'kill -INT \$bridge_pid 2>/dev/null || true; cleanup' EXIT
  timeout 45s python3 /opt/dfl/scripts/capture_ros_image.py /gallery/camera/image '$output'
"
