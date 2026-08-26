# Hardware commissioning records

## Goal

Create versioned, test-backed records for every installed robot, gripper, base, camera, gateway, and calibration used by real mode.

## Inputs

- Profile schemas
- Doosan/gripper/base/camera drivers
- Network/time configuration
- Installed hardware access
- Vendor manuals

## Outputs

- Commissioning record schema
- Records for Picker 1, Picker 2, H2515 when installed, mounted tools, bases, D455s, NUC, and Orin
- Calibration and identity hashes
- Conservative test profiles
- Stop/cancel/watchdog evidence
- Renewal conditions

## Work

1. Record manufacturer/model/serial, firmware, controller generation, endpoints, host owner, driver/source versions, mechanical mount, payload, limits, and safety configuration.
2. Record robot-base, tool, TCP, camera, optical, and scene transforms with method, date, operator, raw data, result, uncertainty, and hash.
3. Verify device identity before motion. For tools without electronic identity, record the physical verification step and photo/reference evidence.
4. Run conservative joint, Cartesian, stop, cancel, tool, base, camera, TF, clock, and network tests separately before combined tasks.
5. Record emergency/protective stop behavior and the steps required to restore ready state. Software tests never replace certified hardware safety procedures.
6. Mark combinations commissioned, simulation-only, expired, or blocked. Expire on relevant firmware, mount, calibration, driver, or mechanical change.
7. Store records outside ordinary task config and reference them by immutable ID/hash in real runs.

## Interfaces and data

- Commissioning record and profile reference
- Preflight identity/expiry checks
- Run manifest links

## Boundaries

- Does not certify machinery or replace vendor safety assessment
- Does not qualify unmounted combinations
- Does not expose credentials in records

## Failure behavior

- Missing/expired identity, calibration, safety evidence, or driver compatibility blocks real mode.
- A failed stop or state test marks the configuration blocked.

## Acceptance

- Each real-tested configuration resolves to complete current records.
- Preflight detects a deliberately mismatched/expired record.
- Transforms and uncertainty reproduce from raw calibration evidence.
- Stop/cancel/watchdog tests are linked.
- Simulation-only combinations cannot claim real qualification.

## Parallel work

Can proceed per available hardware. Real qualification waits for relevant records.

## What this module needs from me

Hardware access and the person authorized to operate each robot safely.
