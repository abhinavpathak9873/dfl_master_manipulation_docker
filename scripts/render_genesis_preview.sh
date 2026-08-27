#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 2 ]]; then
  echo "usage: scripts/render_genesis_preview.sh <picker1|picker2|h2515> <vgc10_1cup|vgc10_4cup|vgp20|2fg14>" >&2
  exit 64
fi

robot="$1"
tool="$2"
case "${robot}" in picker1|picker2|h2515) ;; *) echo "invalid robot: ${robot}" >&2; exit 64 ;; esac
case "${tool}" in vgc10_1cup|vgc10_4cup|vgp20|2fg14) ;; *) echo "invalid tool: ${tool}" >&2; exit 64 ;; esac

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
"${root}/scripts/compose.sh" genesis up -d genesis
"${root}/scripts/compose.sh" genesis exec -T genesis bash -lc \
  "source /opt/ros/jazzy/setup.bash && source /opt/dfl/core_install/setup.bash && source /root/ros2_ws/install/setup.bash && python /opt/dfl/scripts/render_genesis_preview.py '${robot}' '${tool}'"
