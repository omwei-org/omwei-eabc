# GR00T SO100 — isolated pinned-driver reproduction plan

## Purpose

Reproduce the downstream LeRobot conversion and motor-write path without a local NVIDIA Isaac-GR00T checkout and without a physical robot. This plan is deliberately evidence-first: it must not report a transport-level finding until the pinned implementation has actually been exercised.

## Pinned dependency

- Repository: https://github.com/huggingface/lerobot
- Revision: `c75455a6de5c818fa1bb69fb2d92423e86c70475`
- Relevant path: `SO100Follower.send_action()` → `MotorsBus.sync_write("Goal_Position", ...)` → `_unnormalize()` → Feetech encoding/serialization → SDK group-sync-write call.

## Environment

Use a disposable Python virtual environment or CI runner. Do not install or open a serial device and do not connect a robot.

1. Check out the exact LeRobot revision above.
2. Install the package and only the dependencies needed to import the SO100 follower and Feetech bus.
3. Confirm the checked-out commit equals the pinned SHA before running tests.
4. Use a recording fake for the SDK/serial boundary. The fake must record the arguments/bytes passed to the write call and must not send packets to a real device.

## Required cases

Run each case separately for the default `use_degrees=False` configuration and, where applicable, `use_degrees=True`:

- finite in-range value;
- NaN;
- positive infinity;
- negative infinity;
- very large positive finite value (e.g. `1e100`);
- very large negative finite value (e.g. `-1e100`).

Also test `max_relative_target=None` and an explicit configured value. Do not let the latter test silently read from a real bus: stub the present-position read and record the values supplied to the safety-clipping function.

## Assertions and captured evidence

For every case, record:

- exact input and configuration;
- whether an exception is raised, including exception type and stage;
- the values passed into `sync_write`;
- whether conversion/serialization is reached;
- the exact register values or serialized bytes passed to the mocked SDK writer, if any;
- test command, Python version, OS/CI image, and pinned LeRobot commit.

A test that mocks `send_action()` or tests only a reimplemented clamp function is insufficient. The test must invoke the real pinned conversion code. Any mocked SDK/transport boundary must be clearly identified.

## Acceptance criteria

The result is transport-path evidence only if the test invokes the real pinned follower/motor-bus conversion and captures the real arguments produced by that code at the mocked SDK boundary. It is not evidence of physical actuation.

Keep these evidence levels separate:

1. adapter-only reproduction;
2. pinned driver/conversion runtime test;
3. exact values passed to the mocked SDK/transport;
4. physical actuation.

No result at a lower level establishes a higher level. Do not claim that a physical motor moved.

## Current status

This file specifies the next experiment; it does not itself constitute a test result. The current evidence document remains accurate in classifying the downstream transport effect as unverified until the test runs and its output is recorded.

Status update: The experiment has since been run: [run 38775382201](https://github.com/omwei-org/omwei-eabc/actions/runs/38775382201) and [run 38776033231](https://github.com/omwei-org/omwei-eabc/actions/runs/38776033231).
