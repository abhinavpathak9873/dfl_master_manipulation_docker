"""Read and validate the small Phase 00 profile set."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


PROFILE_FILES = ("robots", "tools", "cameras", "modes", "compatibility")


class ProfileError(ValueError):
    """A selected profile is absent or internally inconsistent."""


def profile_dir() -> Path:
    local = Path(__file__).resolve().parents[1] / "config"
    if local.is_dir():
        return local
    from ament_index_python.packages import get_package_share_directory

    return Path(get_package_share_directory("dfl_manipulation_toolbox")) / "config"


def load_profiles(directory: Path | None = None) -> dict[str, Any]:
    directory = directory or profile_dir()
    loaded: dict[str, Any] = {}
    for name in PROFILE_FILES:
        path = directory / f"{name}.yaml"
        if not path.is_file():
            raise ProfileError(f"missing profile file: {path}")
        with path.open(encoding="utf-8") as stream:
            loaded[name] = yaml.safe_load(stream)
    return loaded


@dataclass(frozen=True)
class Selection:
    robot_id: str
    tool_id: str
    mode_id: str
    scene_id: str = "empty"


def resolve(selection: Selection, directory: Path | None = None) -> dict[str, Any]:
    profiles = load_profiles(directory)
    robot = _required(profiles["robots"]["robots"], selection.robot_id, "robot")
    tool = _required(profiles["tools"]["tools"], selection.tool_id, "tool")
    mode = _required(profiles["modes"]["modes"], selection.mode_id, "mode")
    if selection.mode_id not in robot["supported_modes"]:
        raise ProfileError(f"robot {selection.robot_id!r} does not support {selection.mode_id!r}")
    if selection.mode_id not in tool["supported_modes"]:
        raise ProfileError(f"tool {selection.tool_id!r} does not support {selection.mode_id!r}")
    scene = profile_dir().parent / "scenes" / selection.scene_id / "scene.yaml"
    if not scene.is_file():
        raise ProfileError(f"scene {selection.scene_id!r} has no scene.yaml at {scene}")
    return {"selection": selection, "robot": robot, "tool": tool, "mode": mode, "scene": scene}


def validate_all(directory: Path | None = None) -> list[str]:
    profiles = load_profiles(directory)
    problems: list[str] = []
    robot_ids = set(profiles["robots"]["robots"])
    tool_ids = set(profiles["tools"]["tools"])
    mode_ids = set(profiles["modes"]["modes"])
    required = profiles["compatibility"]["required_simulator_matrix"]
    for category, actual, expected in (
        ("robots", robot_ids, set(required["robots"])),
        ("tools", tool_ids, set(required["tools"])),
        ("modes", mode_ids, {"gazebo", "genesis", "real"}),
    ):
        if actual != expected:
            problems.append(f"{category}: expected {sorted(expected)}, found {sorted(actual)}")
    for robot_id in required["robots"]:
        for tool_id in required["tools"]:
            for mode_id in required["modes"]:
                try:
                    resolve(Selection(robot_id, tool_id, mode_id), directory)
                except ProfileError as error:
                    problems.append(str(error))
    return problems


def _required(values: dict[str, Any], identifier: str, kind: str) -> dict[str, Any]:
    if identifier not in values:
        raise ProfileError(f"unknown {kind} {identifier!r}; choose one of: {', '.join(sorted(values))}")
    return values[identifier]
