# Useful run and failure records

## Goal

Capture enough opt-in evidence to compare experiments and diagnose failures
without turning every task into an observability client.

## Task-script payoff

A developer can choose to save the selected setup, stage results, timings, and a
bounded failure buffer, then open ordinary files to understand what happened.

## Minimal record

- Start/end time and user-provided task/run label.
- Selected robot/tool/mode/scene and concrete backend/model revisions.
- Object asset/revision paths and relevant calibration/config hashes when useful.
- Explicit task stage, result, metrics, and exception text.
- Optional images, point clouds, bag snippets, plots, or backend debug files.
- Safety/stop facts required by qualification packets.

## Work

1. Implement an optional local recorder/context helper that writes one run
   directory; task code can also write ordinary files directly.
2. Use JSON/JSONL plus normal artifact files. Keep the schema small and
   forward-compatible by tolerating unknown fields.
3. Let task and backend packets decide which metrics/artifacts pay for their
   debugging needs.
4. Bound image/bag buffers by size/time and retain them on configured failure.
5. Never block robot stop or cleanup on record writing.
6. Redact credentials/endpoints that should not enter artifacts.
7. Provide a direct summary command and document manual inspection.

## Acceptance

- A task runs normally with recording disabled and no recorder process.
- With recording enabled, an injected failure identifies setup, stage, backend,
  error, and useful bounded evidence.
- Partial/corrupt artifact writes do not masquerade as a successful run.
- Qualification packets can state their required fields without expanding every
  ordinary experiment.

## Non-goals

- An event bus, telemetry backend, run daemon, cloud dashboard, or mandatory
  release manifest.
- Recording every ROS topic by default.
