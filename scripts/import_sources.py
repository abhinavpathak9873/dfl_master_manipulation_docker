#!/usr/bin/env python3
"""Import the small Phase 00 VCS manifest without requiring vcstool on host."""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess

import yaml


def run(*args: str, cwd: Path | None = None) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True, stderr=subprocess.STDOUT).strip()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--destination", type=Path, required=True)
    args = parser.parse_args()

    document = yaml.safe_load(args.manifest.read_text())
    repositories = document.get("repositories", {})
    args.destination.mkdir(parents=True, exist_ok=True)
    for name, spec in sorted(repositories.items()):
        if spec.get("type") != "git":
            raise SystemExit(f"{name}: unsupported repository type {spec.get('type')!r}")
        target = args.destination / name
        url = spec["url"]
        revision = spec["version"]
        if not target.exists():
            subprocess.check_call(["git", "clone", "--filter=blob:none", url, str(target)])
        if not (target / ".git").exists():
            raise SystemExit(f"{target}: exists but is not a Git checkout")
        if run("git", "remote", "get-url", "origin", cwd=target) != url:
            raise SystemExit(f"{target}: origin does not match {url}")
        subprocess.check_call(["git", "fetch", "--depth", "1", "origin", revision], cwd=target)
        subprocess.check_call(["git", "checkout", "--detach", revision], cwd=target)


if __name__ == "__main__":
    main()
