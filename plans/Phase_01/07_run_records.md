# Run manifests, events, metrics, and failure buffers

## Goal

Produce enough evidence to reproduce and diagnose each task without recording full camera data for every successful run.

## Inputs

- Typed results and failures
- Resolved configuration hash/provenance
- Namespace and time rules
- Existing diagnostics and visualization artifacts

## Outputs

- Versioned run-manifest schema
- Structured event JSONL schema
- Metric and artifact index
- Bounded rosbag/image ring-buffer design
- Run directory lifecycle and retention hooks
- Reader/validation CLI and tests

## Work

1. Create one run ID before bringup. Store start/end time, task package/version, source manifest, resolved config and hash, host/container/GPU versions, robot/tool/scene/mode/pipeline, task lease ID/epoch, and operator-supplied run label.
2. Write append-only events for lifecycle, stage start/end, planner attempts, controller results, perception health, gripper state, base commands, recovery decisions, and final outcome.
3. Store large logs, images, bags, plans, and benchmark outputs as artifacts referenced by relative path and content hash.
4. Maintain a bounded pre-failure ring buffer for configured ROS topics and diagnostic images. Flush it on failure or explicit request; discard it on ordinary success.
5. Make artifact flush resilient to task exceptions and signals. Mark incomplete artifacts rather than blocking the hardware stop path.
6. Provide a validator that detects missing required fields, broken references, timestamp regressions, mismatched config hashes, and unknown error codes.
7. Add a concise summary command for humans and a machine-readable result for local qualification scripts.
8. Record every resolved object revision with its object ID, revision ID, record/asset hashes, ObjectDB Git commit, and resolution time. A scan run also records its scan lease, stage revisions, staging usage, worker manifest hashes, operator start/resume actions, and final canonical revision when one is committed.

## Interfaces and data

- `RunRef` Python value
- Run manifest JSON and event JSONL
- Artifact directory under `logs/runs/<run_id>`
- Diagnostics hooks consumed by toolbox and integration packages

## Boundaries

- Does not upload data or implement hosted telemetry
- Does not record full rosbag by default
- Does not define long-term retention policy

## Failure behavior

- Logging failure never prevents an immediate stop command.
- Mark the run `incomplete` when final flush fails.
- Never report success without a terminal task event and result.

## Acceptance

- Success and injected-failure fixtures both validate.
- A killed task leaves a readable manifest and buffered failure evidence.
- Resolved config and selected plugin versions can reproduce the run setup.
- Artifact hashes detect modification.
- The summary names the failing stage, error code, and relevant evidence paths.

## Parallel work

Runs alongside task convention after types and time rules are stable.

## What this module needs from me

A later operations decision may set retention duration and disk quota. It is non-blocking for v1 implementation.
