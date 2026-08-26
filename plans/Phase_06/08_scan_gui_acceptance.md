# Scan and GUI acceptance

## Goal

Qualify the full supported workflow from empty staging through capture, reconstruction, review, commit, grasp annotation, simulation test, and optional real test.

## Inputs

- All Phase 06 modules
- One representative new rigid opaque object
- Accepted robot/camera/tool profiles
- Accepted ObjectDB/scan-worker images, mounts, lease contracts, and scan launcher
- Run and object validation artifacts

## Outputs

- End-to-end local acceptance script/checklist
- New approved object revision
- GUI visual test report
- Failure/cancel/crash test report
- Phase exit record

## Work

1. Start the scan environment with one project command. Verify ObjectDB remains the only canonical writer, scan-worker has only staging access, and neither has direct Docker/hardware access.
2. Create a Picker 1 scan session, acquire the global lease, run preflight, perform the explicit start, complete two capture passes, review views, reconstruct in scan-worker, review quality, and stage registration.
3. Inspect mesh scale, axes, collision geometry, held-out overlays, provenance, and limitations in the viewer.
4. Commit and activate the object revision through the service; require the local Git commit, rebuild the cache, and resolve it from a clean process. Let remote sync complete or report a deliberate stale-backup fixture.
5. Create one gripper-specific grasp anchor, run schema/reachability/collision validation, preview a plan, and test in both simulators.
6. If hardware is available and commissioned, run one supervised grasp test and attach evidence without changing acceptance thresholds.
7. Repeat with an active task, second scan, stale lease, missing explicit start, cancellation, rejected material/movement, poor views, worker crash at each stage, service crash, quota exhaustion, lock conflict, stale base, failed local Git commit, failed remote push, and failed grasp.
8. Run browser component/visual tests and object-store contract tests together.

## Interfaces and data

- Local acceptance runner and GUI checklist
- Accepted object revision and test evidence
- Phase report

## Boundaries

- One representative object demonstrates workflow; it does not expand the four-object perception qualification automatically
- No multi-user or remote production deployment

## Failure behavior

- Any direct-file mutation, partial active revision, false quality pass, plan execution without accepted plan, or unsafe failure blocks the phase.
- Any automatic motion resume, automatic task cancellation, silent lease release, or silent staging deletion blocks the phase.

## Acceptance

- A new supported object reaches approved active revision with all hashes and evidence.
- Cache rebuild and service restart preserve it.
- GUI shows the same data returned by CLI/service.
- Simulation grasp test uses the public task path.
- All failure cases leave canonical state valid and robot state declared.
- Active tasks are never disturbed by scan startup, and restart requires explicit stage resume plus fresh preflight before motion.
- Raw/intermediate data stays outside Git; an approved bundle round-trips through a clean Git/LFS clone.

## Parallel work

Final Phase 06 packet.

## What this module needs from me

Provide one representative rigid opaque object and hardware time if real grasp evidence is desired.
