# Scan and GUI acceptance

## Goal

Prove one complete, safe, understandable physical-object-to-task workflow and
its important failure paths.

## Task-script payoff

The approved scan output becomes a normal local object asset that a fresh task
loads and uses after all authoring/scan containers are stopped.

## Work

1. Start the ObjectDB authoring and on-demand scan dependencies through the
   documented Docker profile; verify the ordinary task profile does not require
   them.
2. Create a session for one representative rigid opaque object on the
   commissioned Picker 1/D455 station.
3. Run eligibility, preflight, explicit start, multi-view capture, review,
   reconstruction, quality decision, revision registration, viewer/editor,
   grasp annotation, simulation test, and supervised real grasp test.
4. Stop/restart/cancel at capture, reconstruction, review, edit, registration,
   and grasp-test stages; verify completed evidence and no automatic motion.
5. Test unsupported material/motion, active scan ownership, quota, camera/TF
   fault, bad mask/depth, reconstruction failure, invalid edit, and backup
   failure.
6. Load the approved asset in a fresh core task with ObjectDB/scan containers
   stopped and network unavailable.
7. Compare task-side mesh/frame/anchor/model use with authoring preview.
8. Record operator steps, timings, confusing points, failures, and direct
   troubleshooting commands.

## Acceptance

- The object becomes a complete, validated, locally loadable revision.
- Every physical motion requires current preflight and explicit start.
- Faults never create a partial approved asset or auto-resume motion.
- UI, CLI, and runtime loader agree on files and transforms.
- Docker isolation solves dependencies without making Compose the workflow.
- A developer can inspect/recover the session without a distributed state system.

## Outputs

- End-to-end acceptance report, screenshots/fixtures, timing and failure notes.
- Approved object/revision and canonical task example using it.
- Clear limits of the first scan station and supported object class.

## Non-goals

Production UX, multi-user availability, remote deployment, or claiming all robots
as commissioned scanning stations.
