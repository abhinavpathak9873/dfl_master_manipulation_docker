#!/usr/bin/env bash

export ROS_DISTRO="${ROS_DISTRO:-jazzy}"
export ROS_WS="${ROS_WS:-/root/ros2_ws}"
export ROS_DOMAIN_ID="${ROS_DOMAIN_ID:-63}"
export RMW_IMPLEMENTATION="${RMW_IMPLEMENTATION:-rmw_cyclonedds_cpp}"
export CYCLONEDDS_URI="${CYCLONEDDS_URI:-file:///opt/dfl/scripts/cyclonedds.xml}"

source "/opt/ros/${ROS_DISTRO}/setup.bash"
if [[ -f "${ROS_WS}/install/setup.bash" ]]; then
  source "${ROS_WS}/install/setup.bash"
fi
