# Perception benchmark and two-hour acceptance

## Goal

Measure segmentation, pose, tracking, health, reseeding, resource use, and endurance on the locked four-object dataset and selected desktop hardware.

## Inputs

- All Phase 04 implementations
- Locked qualification split
- Pinned containers/models/engines
- Run-record and metric schemas

## Outputs

- One local benchmark command
- Per-object segmentation, pose, tracking, and recovery metrics
- Latency/rate/resource report
- Two-hour memory/freshness report
- Plugin qualification records
- Phase exit decision

## Work

1. Run each component alone and the full SAM2–FoundationPose–M3T graph. Record cold start, warm start, median/p95 latency, throughput, queue drops, CPU, GPU, VRAM, and power when available.
2. Score SAM2 IoU, FoundationPose ADD/ADD-S, M3T pose error and track retention, false-fresh duration, lost-detection latency, reseed time, and identity continuity.
3. Report sustainable M3T update rate on the D455 stream. Do not fail solely for missing 30 Hz; fail on unbounded latency, false freshness, or task-inadequate accuracy.
4. Run occlusion, motion blur, clutter, similar color, depth holes, camera restart, wrong mesh scale, wrong prompt, process restart, and re-entry sequences.
5. Run the full live or faithful replay graph for two hours. After 15-minute warmup, require no monotonic GPU-memory growth outside a 5% band, no OOM, no scheduled restart, and no stale result marked current.
6. Compare metrics with the object qualification fields and the coarse pre-grasp capture range required by Phase 05.
7. Publish raw metrics, plots/tables, config/source hashes, and a concise pass/fail summary.

## Interfaces and data

- Local benchmark runner
- Metric JSON/CSV and run artifacts
- Plugin qualification state
- Per-object qualification records

## Boundaries

- No claim beyond four objects, D455, recorded scenes, and tested hardware
- No hidden threshold change after seeing qualification results

## Failure behavior

- Invalid ground truth, missing hashes, mixed tuning/qualification data, OOM, stale-current output, or unrecoverable process crash invalidates the run.
- A failed M3T accuracy/integration gate stops for review rather than auto-selecting another tracker.

## Acceptance

- SAM2 and FoundationPose meet their packet thresholds.
- M3T rate and accuracy are reported for every object and condition.
- Health has zero stale-as-current violations in the qualification split.
- The two-hour run passes memory and freshness rules.
- All results reproduce from a pinned manifest.

## Parallel work

Final Phase 04 packet.

## What this module needs from me

Nothing unless the selected stack cannot meet task-level accuracy or stability; then present evidence and alternatives.
