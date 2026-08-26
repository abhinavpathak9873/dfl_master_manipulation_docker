# Shared gripper API

## Goal

Provide the small behavior genuinely shared by the four declared tools while
allowing honest tool-specific operations and results.

## Task-script payoff

Tasks call `open`, `close`, `stop`, and inspect `success`, `final_width`,
`force`, suction, or backend details appropriate to the selected tool.

## Work

1. Derive the common minimum from VGC10 one/four cup, VGP20, and 2FG14.
2. Define open/close/stop/status plus optional force, width, timeout, and expected
   closure arguments where they make physical sense.
3. Return a small result with success and actually measured/derived feedback;
   backend-specific fields/methods remain reachable.
4. Keep object-specific expected width, suction thresholds, and verification
   policy in the task or object grasp profile, not the driver.
5. Define clear unsupported-parameter and unavailable-feedback errors.
6. Implement simulator state/contact approximations honestly and mark their
   limitations.
7. Test command timeout, cancellation, disconnect, partial closure, no object,
   wrong expected closure, suction loss, and stop.

## Acceptance

- The canonical retry loop is straightforward ordinary Python.
- All four tools meet the shared minimum where physically meaningful.
- Tool-specific feedback is not discarded to force uniformity.
- A selected unsupported argument fails before unsafe command.
- No capability negotiation or tool service framework is required.

## Non-goals

A universal end-effector ontology or automatic grasp-success policy.
