#!/usr/bin/env bash
set -euo pipefail

repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
compose=("${repo_root}/scripts/compose.sh" gazebo --profile vendor-emulator)

cleanup() {
  "${compose[@]}" stop doosan-emulator >/dev/null 2>&1 || true
}
trap cleanup EXIT

"${compose[@]}" up -d --force-recreate doosan-emulator
for _ in {1..24}; do
  state=$(docker inspect dfl_master_doosan_emulator \
    --format '{{.State.Status}}/{{if .State.Health}}{{.State.Health.Status}}{{end}}')
  if [[ "${state}" == running/healthy ]]; then
    printf '{"image":"doosanrobot/dsr_emulator:3.0.1","model":"%s","status":"passed"}\n' \
      "${DFL_EMULATOR_MODEL:-M1013}"
    exit 0
  fi
  if [[ "${state}" == exited/* || "${state}" == dead/* ]]; then
    docker logs --tail 100 dfl_master_doosan_emulator >&2 || true
    echo "emulator exited before becoming healthy" >&2
    exit 1
  fi
  sleep 5
done

docker inspect dfl_master_doosan_emulator --format '{{json .State}}' >&2
exit 1
