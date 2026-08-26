# Explicit retry and recovery rules

## Goal

Define which named failures may be retried before contact and which states require task abort and a separate recovery task.

## Inputs

- Failure taxonomy
- Motion, alignment, servo, gripper, and verification states
- Task package convention
- Object/scene attachment state

## Outputs

- Retry classification table
- Reusable pre-contact retry helper with default zero retries
- Recovery-required state record
- Example task branches
- Failure-injection tests

## Work

1. Classify failures by stage and trust: observation-only, planning-only, pre-contact control, contact/grip, post-lift, network/control loss, and unknown.
2. Allow retries only when the task declares a positive bound and the classifier proves no execution/contact uncertainty. Default is zero.
3. Planning fallback is handled inside the motion request before execution. It does not consume a task retry unless the task says so.
4. A perception retry obtains a new observation and track epoch; it cannot reuse stale pose or the failed plan.
5. After uncertain motion, contact, held-object loss, controller loss, TF trust loss, or network loss, abort and write recovery-required with last measured robot/tool/object state.
6. Provide separate explicit recovery task examples: stop and inspect, release when confirmed safe, retreat from a known pose, or rehome after operator/hardware verification.
7. Never run return-home as generic exception cleanup.

## Interfaces and data

- Retry classifier and helper
- Recovery-required record in run manifest
- Task examples using targeted exceptions

## Boundaries

- No generalized autonomous recovery engine
- No automatic resume from checkpoints
- No hidden retry in plugins

## Failure behavior

- Unknown failure class resolves to abort, not retry.
- A failed stop or uncertain state escalates the recovery record.

## Acceptance

- Fixtures prove default zero retries.
- Declared retry counts are exact and bounded.
- No post-contact/control-loss case retries.
- A retry uses fresh perception and planning artifacts.
- Recovery records contain the facts needed for a separate task/operator decision.

## Parallel work

Follows component failure vocabularies. Acceptance uses it.

## What this module needs from me

Nothing.
