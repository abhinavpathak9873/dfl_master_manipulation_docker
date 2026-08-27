#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
src="${root}/.devcontainer/src"
manifest="${root}/dependencies.repos"
mkdir -p "${src}"

if command -v vcs >/dev/null 2>&1; then
  vcs import --recursive "${src}" < "${manifest}"
else
  python3 "${root}/scripts/import_sources.py" --manifest "${manifest}" --destination "${src}"
fi

python3 "${root}/scripts/inspect_sources.py" --root "${root}" --require-clean
