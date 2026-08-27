#!/usr/bin/env bash
set -euo pipefail

echo "kernel=$(uname -srmo)"
if [[ -r /etc/os-release ]]; then
  . /etc/os-release
  echo "os=${PRETTY_NAME}"
fi
echo "logical_cpus=$(nproc)"
free -h
df -h "$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
docker version --format 'docker_client={{.Client.Version}} docker_server={{.Server.Version}}'
docker compose version
nvidia-smi --query-gpu=index,name,uuid,memory.total,driver_version --format=csv,noheader
