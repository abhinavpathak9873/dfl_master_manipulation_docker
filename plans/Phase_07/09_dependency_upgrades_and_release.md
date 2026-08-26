# Dependency upgrades and release

## Goal

Lock a reproducible release, verify every requirement and artifact, and define how future upstream upgrades are evaluated and rolled back.

## Inputs

- All phase acceptance reports
- Source/image/model/calibration/object manifests
- Traceability and documentation
- Local test commands

## Outputs

- Release manifest and version
- Local release checklist
- Requirement coverage and ownership audit
- Dependency-upgrade packet template
- Rollback instructions
- Known limitations and blocked items
- Final signed/dated evidence index
- ObjectDB Git/LFS clone-restore and asynchronous sync evidence

## Work

1. Verify every traceability row has one accepted owner and every blocking phase gate is closed. Record approved deferrals as out-of-scope, not passing work.
2. Pin source commits, image digests, APT/Python packages, model/engine hashes, robot firmware, calibration, object revisions, scenes, plugin versions, and documentation version.
3. Run local clean build, unit, contract, launch, simulator, perception, two-hour, network, failure, and required real qualification commands.
4. Validate all run manifests and artifact links. Keep large runtime artifacts in the declared persistent release store and hash them from the index.
5. Verify the nested private `dfl_object_db` remote, local/remote HEAD, Git LFS rules, approved-bundle allowlist, excluded raw/cache/log paths, sync outbox, and backup freshness. Restore into a clean directory with clone plus LFS fetch and validate every active pointer and asset hash.
6. Create an upgrade template with old/new versions, upstream changes, compatibility risks, build/test matrix, benchmark comparison, data/schema migrations, and rollback.
7. Run the repository-structure gate against the `dff_mobile_manipulation_docker` pattern: Compose and devcontainer files remain under `.devcontainer/`, ROS packages remain direct children of `.devcontainer/src/`, and build/deployment infrastructure remains under `scripts/`. Permit documented additional Compose files, Dockerfiles, and durable mount directories. Fail release on conflicting layout roots or undocumented ownership.
7. Prohibit floating release branches or latest-at-build dependencies. An update receives a new release candidate and repeats affected qualification.
8. Publish release notes containing supported profiles/modes, qualified real tasks, measured limits, deferred scope, known failures, backup state, and recovery guidance.

## Interfaces and data

- Release manifest
- Local checklist and evidence index
- Upgrade work-packet template
- Versioned docs

## Boundaries

- No hosted CI requirement
- No automatic dependency update bot
- No claim for unavailable hardware or untested conditions

## Failure behavior

- Missing pin, broken evidence, duplicate requirement owner, unresolved gate, failed test, or undocumented limitation blocks release.
- Rollback must be tested before the new release is accepted.
- Remote push outage marks backup degraded but does not invalidate a release whose exact local ObjectDB commit and clone/restore evidence are already recorded. An unpushed commit must be named as an operational warning.

## Acceptance

- Fresh local checkout reproduces source and image manifests.
- All required local checks pass.
- Every link/hash resolves.
- Release states exact simulator and real qualification.
- Upgrade template can evaluate one sample dependency change without ambiguity.
- Clean Git/LFS restore matches the released ObjectDB commit, and a forced push outage/retry produces correct backup health without changing canonical data.

## Parallel work

Final packet after all phase exits.

## What this module needs from me

Nothing unless a release gate fails; then the existing stop-for-decision rule applies.
