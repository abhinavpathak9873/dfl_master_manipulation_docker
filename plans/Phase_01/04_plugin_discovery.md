# Plugin discovery and qualification

## Goal

Let programmers switch planners, grippers, pose backends, trackers, alignment methods, and simulators by stable ID without hard-coded conditionals or arbitrary dynamic imports.

## Inputs

- Python value contracts
- Configuration resolver
- ROS interface version
- Accepted package split

## Outputs

- Plugin manifest schema
- Python entry-point groups and C++ pluginlib base interfaces
- Registry API and list-implementations CLI
- Contract major-version checks
- Qualification-state records
- One sample Python and C++ plugin with shared registry tests

## Work

1. Define plugin categories and stable IDs. IDs are lowercase namespaced tokens and do not encode filenames.
2. Use Python entry points for in-process Python implementations. Use pluginlib XML for C++ components. Normalize both into one read-only registry view.
3. Require manifest fields for ID, category, package, implementation version, contract major version, configuration schema, hardware/model requirements, supported modes, and test status.
4. Load only installed, declared plugins. Configuration may select an ID but cannot provide module paths, libraries, or executable text.
5. Expose registry inspection without importing GPU-heavy implementations. Lazy import occurs only after configuration and compatibility checks pass.
6. Record selected plugin versions in the resolved configuration and run manifest.
7. Define qualification states `available`, `smoke-tested`, `qualified-sim`, `qualified-real`, and `blocked`, each backed by an artifact reference.

## Interfaces and data

- Python registry API
- pluginlib base classes for C++ integrations
- Entry-point group names per category
- `list-implementations` CLI output consumed by humans and agents

## Boundaries

- Does not create a general service daemon
- Does not auto-select a fallback plugin
- Does not let third-party plugins bypass typed contracts or safety checks

## Failure behavior

- Reject duplicate IDs, unsupported contract versions, missing schemas, unavailable dependencies, and selection of a plugin unqualified for the requested mode.
- Import errors identify the package and dependency without hiding the original exception.

## Acceptance

- Sample Python and C++ plugins appear in one deterministic listing.
- Switching a selected implementation changes no task source.
- GPU-heavy modules are not imported during listing.
- Contract tests run by category against every installed plugin.
- Blocked plugins cannot run in real mode.

## Parallel work

Consumes config and type contracts. Backend-specific Phase 02/04/05 plans begin after registry acceptance.

## What this module needs from me

Nothing.
