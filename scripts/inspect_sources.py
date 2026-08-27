#!/usr/bin/env python3
"""Report and verify exact Phase 00 source revisions."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess

import yaml


def git(path: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(path), *args], text=True).strip()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--require-clean", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    manifest = yaml.safe_load((root / "dependencies.repos").read_text())["repositories"]
    report = []
    failures = []
    for name, spec in sorted(manifest.items()):
        checkout = root / ".devcontainer" / "src" / name
        if not (checkout / ".git").exists():
            failures.append(f"{name}: missing checkout at {checkout}")
            continue
        revision = git(checkout, "rev-parse", "HEAD")
        dirty = bool(git(checkout, "status", "--porcelain"))
        origin = git(checkout, "remote", "get-url", "origin")
        report.append({"name": name, "revision": revision, "dirty": dirty, "origin": origin})
        if revision != spec["version"]:
            failures.append(f"{name}: expected {spec['version']}, got {revision}")
        if origin != spec["url"]:
            failures.append(f"{name}: expected origin {spec['url']}, got {origin}")
        if args.require_clean and dirty:
            failures.append(f"{name}: checkout is dirty")
    print(json.dumps(report, indent=2, sort_keys=True))
    if failures:
        raise SystemExit("\n".join(failures))


if __name__ == "__main__":
    main()
