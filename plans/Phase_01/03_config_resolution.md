# Configuration resolution and validation

## Goal

Make component selection and detailed behavior deterministic, readable, and safe for real hardware. Task code names profiles; files hold validated parameters.

## Inputs

- Stable profile IDs from Phase 00
- Python types and error codes
- Plugin metadata requirements
- Scene folder contract

## Outputs

- Configuration directory conventions
- Schema for robot, gripper, camera, pipeline, scene, task, and host profiles
- Deterministic resolver with provenance per value
- Resolved-config CLI and redacted snapshot format
- Override allowlist and real-mode protected fields
- Unit and integration tests

## Work

1. Resolve layers in this order: package defaults, host profile, robot profile, gripper profile, camera profile, scene, pipeline, task configuration, then allowlisted CLI overrides.
2. Treat task-code selectors as required inputs, not a hidden layer. Reject selector/config disagreement.
3. Validate each file against a versioned schema and each plugin section against its installed plugin schema. Unknown keys are errors.
4. Mark calibration, robot identity, controller endpoint, joint limits, tool transform, safety bounds, and watchdog settings as protected in real mode. Task files cannot override them.
5. Normalize units during validation and print the canonical unit beside every resolved numeric field.
6. Produce a stable configuration hash and a provenance map showing the file and key that supplied each final value. Save both to the run manifest.
7. Provide commands to validate one file, resolve a task without launching ROS, diff two resolved configurations, and list unused or shadowed settings.

## Interfaces and data

- `Robot(...)` selector inputs
- YAML/JSON schemas and resolved immutable configuration object
- CLI commands `validate-config`, `resolve-config`, and `diff-config`
- Plugin schema hook

## Boundaries

- Does not discover plugins itself
- Does not mutate calibration files
- Does not accept arbitrary environment variables as configuration

## Failure behavior

- Fail on missing selector, unknown key, incompatible profile, duplicate source authority, unit mismatch, protected override, or plugin version mismatch.
- Never fall back to a default robot, gripper, scene, or real network endpoint.

## Acceptance

- The same inputs produce byte-identical canonical output and hash.
- Provenance identifies every resolved leaf.
- Invalid examples cover typos, wrong units, missing frames, unsupported combinations, and protected overrides.
- A task can switch robot, tool, scene, mode, or pipeline without editing unrelated files.
- Secrets and host-specific endpoints are redacted from shareable artifacts.

## Parallel work

Develops beside Python values and namespaces. Plugin discovery and task convention consume it.

## What this module needs from me

Nothing.
