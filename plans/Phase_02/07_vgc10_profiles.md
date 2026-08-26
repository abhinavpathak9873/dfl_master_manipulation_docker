# VGC10 one-cup and four-cup profiles

## Goal

Support both required VGC10 physical configurations as distinct, inspectable
profiles sharing only proven driver behavior.

## Task-script payoff

Selecting `gripper="vgc10_1cup"` or `"vgc10_4cup"` gives the correct mount,
TCP, collision, payload, suction command, feedback, and simulator behavior.

## Work

1. Inventory installed controller/services/IO, vacuum channels, commands,
   feedback, and current DFL behavior.
2. Define separate one-cup and four-cup description overlays, mount transforms,
   TCPs, collision geometry, payload, active cups, and grasp expectations.
3. Reuse the shared suction driver only where both profiles truly match.
4. Map open/release, close/grip, stop, vacuum/power/part-detected feedback, timeout,
   and disconnect into useful results.
5. Implement Gazebo and Genesis suction/contact approximations with explicit
   limitations.
6. Validate that object grasp profiles may name cup layout/requirements without
   putting object policy in the driver.
7. Test seal/no-seal, partial seal, release, stop, wrong geometry, and loss of
   communication.

## Acceptance

- Both profiles generate distinct correct robot descriptions and TCPs.
- Task code differs only in selected profile and object/task parameters.
- Feedback-based success and simulator approximations are documented.
- Safe release/stop works in supported real and simulated paths.

## Non-goals

Treating both cup layouts as aliases or claiming simulated vacuum fidelity as
real qualification.
