#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 3 ]]; then
  echo "usage: $0 <gazebo|genesis> <picker1|picker2|h2515> <tool>" >&2
  exit 2
fi

mode=$1
robot=$2
tool=$3
case "$mode" in gazebo|genesis) ;; *) echo "invalid mode: $mode" >&2; exit 2;; esac
case "$robot" in picker1|picker2) model=m1013;; h2515) model=h2515;; *) echo "invalid robot: $robot" >&2; exit 2;; esac
case "$tool" in vgc10_1cup|vgc10_4cup|vgp20|2fg14) ;; *) echo "invalid tool: $tool" >&2; exit 2;; esac

repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
service=$mode
compose_file=".devcontainer/docker-compose.${mode}.yml"
log_dir="$repo_root/logs/phase_00/$mode-$robot-$tool"
mkdir -p "$log_dir"

compose=("$repo_root/scripts/compose.sh" "$mode")
cleanup_container() {
  "${compose[@]}" restart "$service" >/dev/null 2>&1 || true
}
trap cleanup_container EXIT

"${compose[@]}" up -d "$service"
"${compose[@]}" restart "$service" >/dev/null

launch_package=dfl_manipulation_toolbox
launch_file=gazebo.launch.py
ready_timeout=45
if [[ "$mode" == genesis ]]; then
  launch_package=dfl_genesis_integration
  launch_file=genesis.launch.py
  ready_timeout=180
fi

docker compose --project-name dfl_master_manipulation \
  --project-directory "$repo_root/.devcontainer" -f "$repo_root/$compose_file" exec -T "$service" \
  bash -lc "set -euo pipefail
    set +u
    source /opt/ros/jazzy/setup.bash
    if [[ -f /opt/dfl/core_install/setup.bash ]]; then
      source /opt/dfl/core_install/setup.bash
    fi
    source /root/ros2_ws/install/setup.bash
    set -u
    ros2 launch $launch_package $launch_file robot:=$robot model:=$model tool:=$tool > /workspace/logs/phase_00/$mode-$robot-$tool/launch.log 2>&1 &
    launch_pid=\$!
    cleanup() {
      kill -INT \$launch_pid 2>/dev/null || true
      for _ in {1..50}; do
        kill -0 \$launch_pid 2>/dev/null || break
        sleep 0.1
      done
      kill -TERM \$launch_pid 2>/dev/null || true
      wait \$launch_pid 2>/dev/null || true
    }
    trap cleanup EXIT
    timeout ${ready_timeout}s ros2 topic echo /$robot/ready std_msgs/msg/Bool --once >/dev/null
    python3 /workspace/tasks/phase0_fixed_task.py --robot $robot --tool $tool --mode $mode | tee /workspace/logs/phase_00/$mode-$robot-$tool/result.jsonl"
