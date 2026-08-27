#!/usr/bin/env bash
set -euo pipefail

if [[ "${DFL_REAL_MOTION_ENABLED:-0}" != "1" ]]; then
  echo "Real profile is diagnostics-only: DFL_REAL_MOTION_ENABLED is not 1."
  echo "Phase 07 commissioning must provide robot endpoints, firmware, tool identity, calibration, and current authorization."
  exec sleep infinity
fi

required=(DFL_PICKER1_HOST DFL_PICKER1_RT_HOST)
for key in "${required[@]}"; do
  value="${!key:-UNCONFIGURED}"
  if [[ -z "${value}" || "${value}" == "UNCONFIGURED" ]]; then
    echo "refusing real-mode startup: ${key} is unconfigured" >&2
    exit 78
  fi
done

echo "Real motion was explicitly enabled, but Phase 00 does not launch hardware automatically."
echo "Use the commissioned Phase 07 launch command after a fresh safety preflight."
exec sleep infinity
