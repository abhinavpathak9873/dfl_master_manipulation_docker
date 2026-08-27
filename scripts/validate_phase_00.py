#!/usr/bin/env python3
"""Static Phase 00 acceptance checks that do not require ROS on the host."""

from __future__ import annotations

import argparse
from pathlib import Path
import stat
import sys

import yaml


REQUIRED_COMPOSE = {"dev", "gazebo", "genesis", "real", "scan"}
REQUIRED_ROBOTS = {"picker1", "picker2", "h2515"}
REQUIRED_TOOLS = {"vgc10_1cup", "vgc10_4cup", "vgp20", "2fg14"}
REQUIRED_MODES = {"real", "gazebo", "genesis"}


def load(path: Path):
    with path.open() as stream:
        return yaml.safe_load(stream)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root.resolve()
    failures: list[str] = []

    expected = [
        root / ".devcontainer" / "devcontainer.json",
        root / ".devcontainer" / "docker-compose.yml",
        root / ".devcontainer" / "Dockerfile.core",
        root / ".devcontainer" / "Dockerfile.genesis",
        root / "dependencies.repos",
        root / ".devcontainer" / "src" / "dfl_manipulation_toolbox" / "package.xml",
        root / ".devcontainer" / "src" / "dfl_genesis_integration" / "package.xml",
    ]
    for path in expected:
        if not path.exists():
            failures.append(f"missing required Phase 00 artifact: {path.relative_to(root)}")

    for profile in REQUIRED_COMPOSE - {"dev"}:
        path = root / ".devcontainer" / f"docker-compose.{profile}.yml"
        if not path.exists():
            failures.append(f"missing Compose profile: {path.relative_to(root)}")

    config = root / ".devcontainer" / "src" / "dfl_manipulation_toolbox" / "config"
    if config.exists():
        robots = set(load(config / "robots.yaml")["robots"])
        tools = set(load(config / "tools.yaml")["tools"])
        modes = set(load(config / "modes.yaml")["modes"])
        if robots != REQUIRED_ROBOTS:
            failures.append(f"robot IDs: expected {sorted(REQUIRED_ROBOTS)}, got {sorted(robots)}")
        if tools != REQUIRED_TOOLS:
            failures.append(f"tool IDs: expected {sorted(REQUIRED_TOOLS)}, got {sorted(tools)}")
        if modes != REQUIRED_MODES:
            failures.append(f"mode IDs: expected {sorted(REQUIRED_MODES)}, got {sorted(modes)}")

    scripts = root / "scripts"
    for path in scripts.iterdir():
        if path.suffix == ".sh" and not (path.stat().st_mode & stat.S_IXUSR):
            failures.append(f"script is not executable: {path.relative_to(root)}")

    if failures:
        print("Phase 00 validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        raise SystemExit(1)
    print("Phase 00 static validation passed")


if __name__ == "__main__":
    main()
