#!/usr/bin/env python3
"""Validate or execute the declared 24-case Phase 00 simulator matrix."""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path
import subprocess
import sys
import time

import yaml


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--mode", choices=("gazebo", "genesis", "all"), default="all")
    parser.add_argument("--fail-fast", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    with (root / "config/phase0_matrix.yaml").open() as stream:
        matrix = yaml.safe_load(stream)
    modes = matrix["modes"] if args.mode == "all" else [args.mode]
    cases = list(itertools.product(modes, matrix["robots"], matrix["tools"]))
    full_count = len(matrix["modes"]) * len(matrix["robots"]) * len(matrix["tools"])
    if full_count != matrix["expected_case_count"]:
        raise SystemExit(f"matrix defines {full_count} cases, expected {matrix['expected_case_count']}")

    source = root / ".devcontainer/src/dfl_manipulation_toolbox"
    sys.path.insert(0, str(source))
    from dfl_manipulation_toolbox.profiles import Selection, resolve, validate_all
    problems = validate_all(source / "config")
    for mode, robot, tool in cases:
        resolve(Selection(robot, tool, mode), source / "config")
    if problems:
        raise SystemExit("profile errors:\n- " + "\n- ".join(problems))
    if not args.execute:
        print(json.dumps({"status": "valid", "selected_cases": len(cases), "full_matrix_cases": full_count,
                          "case_ids": [f"{mode}-{robot}-{tool}" for mode, robot, tool in cases]}, indent=2))
        return

    results = []
    for mode, robot, tool in cases:
        case_id = f"{mode}-{robot}-{tool}"
        started = time.monotonic()
        completed = subprocess.run([str(root / "scripts/run_phase0_case.sh"), mode, robot, tool])
        result = {"case_id": case_id, "returncode": completed.returncode,
                  "status": "passed" if completed.returncode == 0 else "failed",
                  "wall_seconds": time.monotonic() - started}
        results.append(result)
        print(json.dumps(result), flush=True)
        if completed.returncode and args.fail_fast:
            break
    summary = {"generated_at_unix": time.time(), "results": results,
               "passed": sum(item["status"] == "passed" for item in results),
               "failed": sum(item["status"] == "failed" for item in results)}
    output_dir = root / "logs/phase_00"
    output_dir.mkdir(parents=True, exist_ok=True)
    mode_output = output_dir / f"matrix-{args.mode}-summary.json"
    mode_output.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    if args.mode == "all":
        (output_dir / "matrix-summary.json").write_text(
            json.dumps(summary, indent=2) + "\n", encoding="utf-8"
        )
    if summary["failed"] or len(results) != len(cases):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
