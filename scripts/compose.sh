#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
profile="${1:-dev}"
shift || true

case "${profile}" in
  dev) compose_file="${root}/.devcontainer/docker-compose.yml" ;;
  gazebo|genesis|real|scan)
    compose_file="${root}/.devcontainer/docker-compose.${profile}.yml"
    ;;
  *)
    echo "usage: scripts/compose.sh {dev|gazebo|genesis|real|scan} <compose arguments...>" >&2
    exit 64
    ;;
esac

exec docker compose --project-name dfl_master_manipulation \
  --project-directory "${root}/.devcontainer" -f "${compose_file}" "$@"
