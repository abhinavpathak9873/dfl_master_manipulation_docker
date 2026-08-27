#!/usr/bin/env bash
set -euo pipefail

workspace="${ROS_WS:-/root/ros2_ws}"
quick=false
clean=false
genesis=false
for argument in "$@"; do
  case "${argument}" in
    --quick) quick=true ;;
    --clean) clean=true ;;
    --genesis) genesis=true ;;
    *) echo "unknown argument: ${argument}" >&2; exit 64 ;;
  esac
done

set +u
source "/opt/ros/${ROS_DISTRO:-jazzy}/setup.bash"
set -u
if ${genesis}; then
  if [[ ! -f /opt/dfl/core_install/setup.bash ]]; then
    echo "Genesis compilation requires the populated core install volume" >&2
    exit 69
  fi
  set +u
  source /opt/dfl/core_install/setup.bash
  set -u
fi
cd "${workspace}"

if ${clean}; then
  for path in "${workspace}/build" "${workspace}/install" "${workspace}/log"; do
    if [[ "${path}" != "${workspace}/"* ]]; then
      echo "refusing unsafe clean target: ${path}" >&2
      exit 70
    fi
    find "${path}" -mindepth 1 -maxdepth 1 -exec rm -r -- {} + 2>/dev/null || true
  done
fi

if ! ${genesis}; then
  rosdep update --rosdistro jazzy
  rosdep install --from-paths src/doosan-robot2 src/dfl_manipulation_toolbox \
    --ignore-src --rosdistro jazzy -y \
    --dependency-types=build --dependency-types=buildtool \
    --dependency-types=build_export --dependency-types=buildtool_export \
    --dependency-types=exec \
    --skip-keys="ament_python serial"
fi

if ${genesis}; then
  packages=(dfl_genesis_integration)
else
  packages=(dfl_manipulation_toolbox)
fi
if ! ${quick} && ! ${genesis}; then
  packages+=(
    dsr_msgs2 dsr_description2 dsr_hardware2 dsr_controller2 dsr_gazebo2 dsr_bringup2
    dsr_moveit_config_m1013 dsr_moveit_config_h2515
  )
fi

cmake_args=(-DCMAKE_BUILD_TYPE=RelWithDebInfo -DCMAKE_EXPORT_COMPILE_COMMANDS=ON)
if [[ "${DFL_DRCF_VERSION:-2}" == "3" ]]; then
  cmake_args+=(-DDRCF_VER=3)
fi

build_args=()
if ${genesis}; then
  # This overlay is consumed only inside the Genesis container, so editable
  # Python installs are useful and do not cross a container boundary.
  build_args+=(--symlink-install)
  build_args+=(--packages-select "${packages[@]}")
else
  # The core install volume is mounted into other containers.  A copy install
  # keeps it relocatable instead of leaving absolute links into core's build
  # volume.
  build_args+=(--packages-up-to "${packages[@]}")
fi
build_args+=(--cmake-args "${cmake_args[@]}")
colcon build "${build_args[@]}"
