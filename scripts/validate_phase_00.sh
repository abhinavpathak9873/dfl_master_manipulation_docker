#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
python3 "${root}/scripts/validate_phase_00.py" --root "${root}"
python3 -m unittest discover -s "${root}/tests" -p 'test_*.py' -v
python3 "${root}/scripts/inspect_sources.py" --root "${root}" --require-clean
python3 "${root}/scripts/run_phase0_matrix.py"

for profile in dev gazebo genesis real scan; do
  "${root}/scripts/compose.sh" "${profile}" config --quiet
done

if "${root}/scripts/compose.sh" dev ps --status running --services | grep -qx core; then
  "${root}/scripts/compose.sh" dev exec -T core /opt/dfl/scripts/validate_descriptions.sh
  "${root}/scripts/compose.sh" dev exec -T core /opt/dfl/scripts/validate_moveit_configs.sh
else
  echo "ROS description and MoveIt validation not run: core container is not running" >&2
fi
