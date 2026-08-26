# Visible configuration and shared physical facts

## Goal

Keep experiment choices close to task code while making shared hardware,
calibration, scene, driver, and model settings reproducible.

## Task-script payoff

A developer sees the robot, mode, tool, scene, backend, model, thresholds, and
experimental parameters where they are used, and can inspect any shared value's
source directly.

## Work

1. Treat constructor arguments and explicit keyword arguments as the primary
   experiment configuration.
2. Keep robot/tool/camera profiles, calibration, limits, controller/MoveIt
   settings, network endpoints, scenes, and large backend settings in small
   files owned by their adapter.
3. Give each adapter a short documented precedence, typically explicit task
   value over selected profile over package default. Add another layer only for
   a demonstrated workflow.
4. Resolve paths relative to the owning task/profile/object asset rather than
   global working-directory magic.
5. Validate only facts needed before unsafe or expensive work: IDs, required
   files, units, frames, limits, devices, endpoints, and backend-required assets.
6. Provide a direct `show`/`describe` method or CLI for the selected robot or
   backend where debugging ambiguity warrants it.
7. Keep secrets outside source-controlled files and inject them only into the
   process that uses them.

## Acceptance

- The canonical task's choices remain visible in Python.
- Picker/tool/scene and backend examples resolve deterministically in a clean
  container.
- Missing calibration/model/mesh/device errors name the exact assumption and
  expected location.
- No global resolver must understand every backend's settings.

## Non-goals

- A nine-layer merge system, configuration service, provenance graph, or
  universal schema language.
- Moving obvious task parameters into YAML merely for consistency.
