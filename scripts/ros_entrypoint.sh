#!/usr/bin/env bash
set -e

source "/opt/ros/${ROS_DISTRO:-jazzy}/setup.bash"

if [[ -f /opt/dfl/core_install/setup.bash ]]; then
  source /opt/dfl/core_install/setup.bash
fi

workspace="${ROS_WS:-/root/ros2_ws}"
if [[ -f "${workspace}/install/setup.bash" ]]; then
  source "${workspace}/install/setup.bash"
fi

exec "$@"
