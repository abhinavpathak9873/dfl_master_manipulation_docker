#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
target="${1:-all}"

case "${target}" in
  core)
    docker compose --project-name dfl_master_manipulation --project-directory "${root}/.devcontainer" \
      -f "${root}/.devcontainer/docker-compose.yml" build core
    ;;
  genesis)
    docker compose --project-name dfl_master_manipulation --project-directory "${root}/.devcontainer" \
      -f "${root}/.devcontainer/docker-compose.genesis.yml" build genesis
    ;;
  all)
    "$0" core
    "$0" genesis
    ;;
  *)
    echo "usage: scripts/0_build_images.sh {core|genesis|all}" >&2
    exit 64
    ;;
esac
