"""Inspect and validate profiles without a configuration service."""

from __future__ import annotations

import argparse
import json

from .profiles import Selection, load_profiles, resolve, validate_all


def main() -> None:
    parser = argparse.ArgumentParser(prog="dfl-profile")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("list")
    subparsers.add_parser("validate")
    show = subparsers.add_parser("show")
    show.add_argument("--robot", required=True)
    show.add_argument("--tool", required=True)
    show.add_argument("--mode", required=True)
    show.add_argument("--scene", default="empty")
    args = parser.parse_args()
    if args.command == "list":
        profiles = load_profiles()
        output = {name: sorted(profiles[name][name]) for name in ("robots", "tools", "cameras", "modes")}
    elif args.command == "validate":
        problems = validate_all()
        if problems:
            raise SystemExit("profile validation failed:\n- " + "\n- ".join(problems))
        output = {"status": "valid", "simulator_selections": 24}
    else:
        resolved = resolve(Selection(args.robot, args.tool, args.mode, args.scene))
        output = {key: (str(value) if key in {"selection", "scene"} else value) for key, value in resolved.items()}
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
