#!/usr/bin/env bash
set -euo pipefail

repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
gallery="$repo_root/docs/phase_00/gallery"
robots=(picker1 picker2 h2515)
tools=(vgc10_1cup vgc10_4cup vgp20 2fg14)

mkdir -p "$gallery/genesis" "$gallery/gazebo"
mkdir -p "$repo_root/logs/phase_00/gallery/genesis" "$repo_root/logs/phase_00/gallery/gazebo"
for robot in "${robots[@]}"; do
  for tool in "${tools[@]}"; do
    if [[ ! -s "$gallery/genesis/$robot-$tool.png" ]]; then
      "$repo_root/scripts/render_genesis_preview.sh" "$robot" "$tool" "/workspace/logs/phase_00/gallery/genesis/$robot-$tool.png"
      cp "$repo_root/logs/phase_00/gallery/genesis/$robot-$tool.png" "$gallery/genesis/$robot-$tool.png"
    fi
    if [[ ! -s "$gallery/gazebo/$robot-$tool.png" ]]; then
      "$repo_root/scripts/render_gazebo_preview.sh" "$robot" "$tool" "/workspace/logs/phase_00/gallery/gazebo/$robot-$tool.png"
      cp "$repo_root/logs/phase_00/gallery/gazebo/$robot-$tool.png" "$gallery/gazebo/$robot-$tool.png"
    fi
  done
done
