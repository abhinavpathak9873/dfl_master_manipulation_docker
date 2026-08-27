#!/usr/bin/env bash
set -euo pipefail

repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
log_dir="${repo_root}/logs/phase_00/gazebo-dual-picker"
mkdir -p "${log_dir}"

compose=("${repo_root}/scripts/compose.sh" gazebo)
cleanup_container() {
  "${compose[@]}" restart gazebo >/dev/null 2>&1 || true
}
trap cleanup_container EXIT

"${compose[@]}" up -d gazebo
"${compose[@]}" restart gazebo >/dev/null

docker compose --project-name dfl_master_manipulation \
  --project-directory "${repo_root}/.devcontainer" \
  -f "${repo_root}/.devcontainer/docker-compose.gazebo.yml" exec -T gazebo \
  bash -lc "set -eo pipefail
    source /opt/ros/jazzy/setup.bash
    source /root/ros2_ws/install/setup.bash
    ros2 launch dfl_manipulation_toolbox dual_picker_gazebo.launch.py \
      > /workspace/logs/phase_00/gazebo-dual-picker/launch.log 2>&1 &
    launch_pid=\$!
    cleanup() {
      kill -INT \$launch_pid 2>/dev/null || true
      sleep 3
      kill -TERM \$launch_pid 2>/dev/null || true
      wait \$launch_pid 2>/dev/null || true
    }
    trap cleanup EXIT
    timeout 60s ros2 topic echo /picker1/ready std_msgs/msg/Bool --once >/dev/null
    timeout 60s ros2 topic echo /picker2/ready std_msgs/msg/Bool --once >/dev/null
    python3 /workspace/tasks/phase0_fixed_task.py --robot picker1 --tool vgc10_1cup --mode gazebo \
      > /workspace/logs/phase_00/gazebo-dual-picker/picker1.json &
    picker1_pid=\$!
    python3 /workspace/tasks/phase0_fixed_task.py --robot picker2 --tool 2fg14 --mode gazebo \
      > /workspace/logs/phase_00/gazebo-dual-picker/picker2.json &
    picker2_pid=\$!
    wait \$picker1_pid
    wait \$picker2_pid
    python3 - <<'PY'
import json
from pathlib import Path

root = Path('/workspace/logs/phase_00/gazebo-dual-picker')
results = [json.loads((root / name).read_text()) for name in ('picker1.json', 'picker2.json')]
if {item['robot'] for item in results} != {'picker1', 'picker2'}:
    raise SystemExit('dual-Picker results do not contain both robot identities')
if any(item['status'] != 'passed' for item in results):
    raise SystemExit('one or more dual-Picker tasks failed')
print(json.dumps({'status': 'passed', 'robots': ['picker1', 'picker2'], 'concurrent': True}, sort_keys=True))
PY"
