# Evidence Reference — GR00T SO100/SO101 Pre-Actuation Path

**Update:** Sections 11 and 12 record later runtime tests at the mocked SDK boundary; physical actuation remains untested.

**Status:** Adapter-side gap reproduced; downstream driver path source-traced; transport-level reproduction remains open  
**Analysis date:** 2026-10-15  
**Scope:** Action validation in the NVIDIA Isaac-GR00T SO100 evaluation path, from policy output to the call site that invokes LeRobot's `send_action()`.

> **Key finding**
>
> The inspected GR00T SO100 adapter does not explicitly reject non-finite action values (NaN or ±Inf) or unusually large finite values before constructing the action dictionary. An isolated test harness also observed these values passing through the adapter-side selection path. This does **not**, by itself, prove that the real LeRobot motor bus receives those values or that a physical actuator moves.

The evidence supports a validation gap at the adapter boundary and, by source tracing, a default normalized driver path that maps non-finite/extreme inputs to endpoint targets rather than rejecting them. The runtime SDK/transport effect remains **unverified**.

## 1. Provenance and evidence boundaries

| Component | Source / anchor | What is established |
|---|---|---|
| GR00T SO100 evaluation path | [NVIDIA/Isaac-GR00T](https://github.com/NVIDIA/Isaac-GR00T), `gr00t/eval/real_robot/SO100/eval_so100.py` | Source inspection of the adapter and action-selection path |
| LeRobot dependency | [huggingface/lerobot](https://github.com/huggingface/lerobot), revision `c75455a6de5c818fa1bb69fb2d92423e86c70475` (as pinned by the GR00T SO100 project metadata) | Dependency/revision anchor; does not substitute for a reproduced end-to-end driver test |
| Isolated adapter harness | Fake policy and test doubles; no physical robot | NaN, ±Inf and a large finite value were observed passing through the tested adapter-side path; structural errors raised exceptions |
| Pinned LeRobot source trace | `SO100Follower.send_action()` → `MotorsBus.sync_write()` → `_unnormalize()` → Feetech serialization / `GroupSyncWrite` | Default normalized path appears to transform non-finite and extreme values into bounded endpoint commands; runtime transport test still required |
| Real motor bus / physical actuation | No recording-transport test or physical robot used | Runtime transport result and physical actuation unverified |

This record distinguishes source inspection, isolated reproduction, and real-driver behaviour. They are separate evidence levels and must not be conflated.

## 2. Protected effect and current scope

The effect of interest is a joint-position command ultimately written to a SO100/SO101 motor bus, commonly through a call such as:

```text
robot.send_action(action_dict)
  → LeRobot follower / motor-bus path
  → bus.sync_write("Goal_Position", ...)
```

The adapter-side tests did not establish runtime behaviour at the driver boundary. A subsequent source trace found that the default normalized SO100 path appears to convert non-finite and extreme inputs to endpoint targets before Feetech serialization; a recording-transport test is still required to verify the runtime payload.

## 3. Source-traced adapter path

The inspected GR00T evaluation flow includes the following stages:

```text
policy / Gr00tPolicy.get_action()
        │ action chunk
        ▼
So100Adapter.get_action()
        ▼
So100Adapter.decode_action_chunk()
        ▼
_select_action_steps()
        ▼
robot.send_action(action_dict)   [downstream call site]
```

The adapter's relevant checks are structural rather than a complete numeric-safety policy:

- Policy-side validation checks the expected keys, array type/dtype, shape and horizon.
- The inspected adapter path converts action values to floating-point values but does not explicitly apply an `isfinite` check or an application-defined magnitude/position bound before returning the action dictionary.
- Missing keys and malformed dimensions can raise structural exceptions. Such rejection is not evidence of numeric validation.

These observations concern the inspected code path and revision. They should not be generalized to every GR00T embodiment, every evaluation path, or every configuration.

## 4. Isolated test evidence

The isolated harness used a fake policy and test doubles; it did not control a physical robot.

| Input case | Observed adapter-side result | Interpretation |
|---|---|---|
| Ordinary finite value | Passed through | Expected structural path |
| NaN in a joint value | Passed through as NaN | No adapter-side non-finite rejection observed |
| +Inf in a joint value | Passed through as +Inf | No adapter-side non-finite rejection observed |
| −Inf in a joint value | Passed through as −Inf | No adapter-side non-finite rejection observed |
| Large finite value (for example, `1e100`) | Passed through in the isolated harness | No adapter-side magnitude rejection observed |
| Missing `gripper` key | `KeyError` | Structural rejection |
| Incorrect `single_arm` dimension | `IndexError` | Structural rejection |

**Test boundary:** These results establish behaviour at the tested adapter-side boundary only. They do not establish what the real LeRobot follower, numeric conversion, motor-bus implementation, or physical actuator does with the values.

Functions exercised in the isolated adapter-side tests:

- `So100Adapter.decode_action_chunk`
- `So100Adapter.get_action`
- `_select_action_steps`

in `gr00t/eval/real_robot/SO100/eval_so100.py`.

## 5. Downstream driver: source-level trace; runtime transport test still open

The pinned LeRobot source has now been traced through the SO100 follower and Feetech motor-bus conversion. This is a **source-level finding**, not yet a reproduced runtime test using a recording transport.

Relevant pinned source anchors:

- [SO100 follower implementation](https://github.com/huggingface/lerobot/blob/c75455a6de5c818fa1bb69fb2d92423e86c70475/src/lerobot/robots/so100_follower/so100_follower.py)
- [SO100 follower configuration](https://github.com/huggingface/lerobot/blob/c75455a6de5c818fa1bb69fb2d92423e86c70475/src/lerobot/robots/so100_follower/config_so100_follower.py)
- [Motor-bus conversion and sync-write path](https://github.com/huggingface/lerobot/blob/c75455a6de5c818fa1bb69fb2d92423e86c70475/src/lerobot/motors/motors_bus.py)
- [Feetech sign encoding and packet setup](https://github.com/huggingface/lerobot/blob/c75455a6de5c818fa1bb69fb2d92423e86c70475/src/lerobot/motors/feetech/feetech.py)

### Default configuration path

The SO100 follower selects `MotorNormMode.RANGE_M100_100` for the five body joints when `use_degrees=False` (the default), and `MotorNormMode.RANGE_0_100` for the gripper. The configuration defaults `max_relative_target` to `None`, so the relative-target clipping branch in `send_action()` is skipped unless a deployment overrides it.

For those default normalized modes, `MotorsBus._unnormalize()` clamps values using `min(maximum, max(minimum, value))` and converts the result to an integer motor position. Applying the exact Python operations used by that source gives:

| Input | Body joint normalized value | Gripper normalized value |
|---|---:|---:|
| `NaN` | `-100` (lower endpoint) | `0` (lower endpoint) |
| `+Inf` | `100` (upper endpoint) | `100` (upper endpoint) |
| `-Inf` | `-100` (lower endpoint) | `0` (lower endpoint) |
| Very large positive finite value | `100` (upper endpoint) | `100` (upper endpoint) |
| Very large negative finite value | `-100` (lower endpoint) | `0` (lower endpoint) |

These are normalized endpoints, which are then mapped using the motor calibration ranges. Thus, in the default normalized path, the source does not show these inputs being rejected by a finite-number check; it shows them being converted to endpoint targets. The endpoint targets are numeric and can proceed through sign encoding and serialization if the bus is connected, calibration is present, and the remaining driver/SDK operations succeed.

The `Goal_Position` register is configured as a two-byte value in the pinned Feetech control table. `_serialize_data()` checks that the value is a non-negative integer that fits the selected byte width; for a two-byte register, the maximum is `65535`. Because the default normalized modes first convert values into the calibrated position range, NaN/±Inf do not remain non-finite by the time serialization is attempted.

### Non-default `use_degrees=True` path

The source has a different branch when `use_degrees=True` selects `MotorNormMode.DEGREES` for the five body joints. That branch computes an integer from the degree value without the normalized-mode clamp:

- `NaN` raises `ValueError` during integer conversion;
- `+Inf` and `-Inf` raise `OverflowError`;
- an extreme finite degree value can produce an integer outside the two-byte serialization range and then be rejected by `_serialize_data()`.

This is a source-level consequence of the conversion and serialization code, not a runtime transport test. The gripper remains configured with `RANGE_0_100` in the shown SO100 implementation.

### What remains unverified

The source path proceeds from `send_action()` to `sync_write("Goal_Position", ...)`, then through unnormalization, sign encoding, byte serialization and the Feetech sync-writer setup / packet-send call. However, this evidence record still does **not** contain a runtime test with the pinned implementation and a recording transport proving the exact values submitted to the SDK or transport.

The following remain open:

- a test exercising the actual pinned conversion path with NaN, ±Inf and extreme finite values;
- a recording-transport assertion proving the exact serialized payload and whether the SDK accepts it;
- runtime confirmation of the source-traced `use_degrees=True` exception path and of non-default `max_relative_target` settings;
- any claim about physical motor movement.

No physical movement was performed or is claimed in this record.

## 6. Mapping to EABC concepts

This is a preliminary observation about an external path, not a conformance verdict for GR00T or LeRobot.

| EABC concept | Evidence-supported statement |
|---|---|
| Complete Mediation | The inspected adapter path has no explicit numeric rejection for the tested invalid values. Complete mediation of the full actuator path has not been established or disproved by this adapter-only reproduction. |
| Independent Execution Authority | No independent execution-authority decision is visible in the inspected adapter path. This observation alone is not a complete audit of every possible control path. |
| Fail-closed semantics | The adapter-side path does not explicitly fail closed on the tested non-finite or extreme numeric values. Downstream behaviour remains unverified. |
| Commit Gate | No explicit EABC Commit Gate was identified in the inspected adapter path before its `send_action()` call. |
| Execution Attestation | This evidence run did not identify a commit-time attestation artifact binding an authorization decision to the physical effect. This is a scoped observation, not a system-wide absence proof. |

This document does not claim that GR00T or LeRobot assert EABC conformance.

## 7. What this evidence does not establish

This record does **not** establish:

- that invalid values reach the real motor-bus write in the pinned LeRobot implementation;
- that physical motor movement occurred with invalid values;
- runtime confirmation that the source-traced default conversion results are the values actually submitted to the SDK/transport;
- runtime behaviour under non-default driver configurations (the `use_degrees=True` branch has been source-traced, but not exercised through the runtime driver/transport);
- behaviour of other GR00T embodiments or evaluation paths;
- that adding an `isfinite` check alone would constitute a complete EABC execution-authority boundary;
- interoperability with any EGA or EABC implementation;
- prepare/commit or time-of-check-to-time-of-use (TOCTOU) properties.

## 8. Relationship to EABC / EGA work

The observation is relevant to the general separation between policy output and authority to commit an externally observable effect:

```text
VLA policy output
        │
        ▼
action adapter
        │
        ▼
send_action() / downstream actuator path
```

The adapter-side evidence identifies a place where explicit validation of non-finite and extreme values is not present in the inspected path. It does not demonstrate that a complete execution-authority boundary exists or is absent throughout the entire robot stack.

A separate experiment could evaluate a gate before `send_action()`, with explicit allow/deny semantics and defined action constraints. Such an experiment would be an engineering demonstration, not by itself proof of EABC conformance and not a change to the normative EABC core.

## 9. Reproduction and completion checklist

### Adapter-side finding

1. Check out the relevant NVIDIA/Isaac-GR00T revision.
2. Load `So100Adapter` and its action-selection path, mocking optional dependencies if needed.
3. Use a fake policy to provide NaN, ±Inf, large finite values, missing keys and malformed dimensions.
4. Call `get_action()` and `_select_action_steps()`; inspect the resulting action dictionary.
5. Record the exact revision, commands, test output and assertions.

### Downstream verification still required

1. Use the already identified pinned LeRobot revision `c75455a6de5c818fa1bb69fb2d92423e86c70475` and preserve that exact source anchor.
2. Add a runtime test using the real `SO100Follower` and `FeetechMotorsBus` conversion code with a recording/mock SDK transport; do not use a physical robot for initial fault injection.
3. Exercise the default `use_degrees=False` path with NaN, ±Inf, and extreme finite inputs, then separately exercise `use_degrees=True` and a configured `max_relative_target`.
4. Assert and record whether each case raises, is clamped, or reaches the SDK/transport, including the exact serialized `Goal_Position` bytes where a write is attempted.
5. Keep the result explicitly scoped to the tested revision and configuration.

Until that downstream test is complete, the conclusion must remain limited to the adapter-side validation gap.

## 10. Classification and next step

**Classification: D — adapter-side validation gap reproduced; pinned default driver source maps non-finite/extreme inputs to endpoint targets; runtime transport effect unverified.**

This is a preliminary external-system observation, not validation of an EABC implementation and not evidence of physical actuation with invalid values.

The next evidence-producing step is a recording-transport test against the pinned LeRobot conversion and motor-bus code. The source trace strengthens the concern from an adapter-only observation to a plausible downstream path, but do not classify the runtime motor-write path as confirmed until that test exists.


## 11. Runtime reproduction — pinned LeRobot driver conversion and mocked SDK boundary

**Run:** [Pinned LeRobot SO100 driver reproduction — run 38775382201](https://github.com/omwei-org/omwei-eabc/actions/runs/38775382201)  
**Result:** PASS (workflow conclusion: `success`)  
**Harness commit:** `099cff7446085c8867cf6a79d9d73784257f042e`  
**Upstream LeRobot SHA:** `c75455a6de5c818fa1bb69fb2d92423e86c70475` (verified in the workflow before the test)  
**Python:** CPython 3.11.17  
**Command:** `python evidence/scripts/test_pinned_lerobot_driver.py`

The first run, [38749028591](https://github.com/omwei-org/omwei-eabc/actions/runs/38749028591), failed before executing cases because the checkout's `lerobot/src` directory was not on `sys.path` (`ModuleNotFoundError: No module named 'lerobot'`). The harness was corrected to import from that checked-out source tree, without replacing the driver implementation. The subsequent run above completed and its job logs were inspected.

The harness imports the pinned `Motor`, `MotorCalibration`, `MotorNormMode`, and `FeetechMotorsBus` implementations. It calls the real `FeetechMotorsBus.sync_write("Goal_Position", ...)` conversion/serialization path. Only unrelated utility imports and the `scservo_sdk` transport classes are stubbed. The recording `GroupSyncWrite.addParam()` captures the exact byte list the real driver passes to the mocked SDK boundary; `txPacket()` returns success without sending anything. The workflow does not install or use a different LeRobot implementation.

### Captured case results

Register address was `42` and register width was `2` bytes for all body-joint cases. Payloads below are the exact byte lists recorded by the mocked SDK's `GroupSyncWrite.addParam()`, in serialization order.

| Case | Mode / input | Runtime outcome | Captured bytes | Interpretation |
|---|---|---|---|---|
| finite_mid | `RANGE_M100_100`, `0.0` | write attempted | `[255, 7]` | converted to calibrated midpoint register value 2047 |
| NaN | `RANGE_M100_100`, `NaN` | write attempted | `[0, 0]` | clamped/converts to lower endpoint 0 |
| +Inf | `RANGE_M100_100`, `+Inf` | write attempted | `[255, 15]` | clamped/converts to upper endpoint 4095 |
| −Inf | `RANGE_M100_100`, `−Inf` | write attempted | `[0, 0]` | clamped/converts to lower endpoint 0 |
| huge positive | `RANGE_M100_100`, `1e100` | write attempted | `[255, 15]` | clamped/converts to upper endpoint 4095 |
| huge negative | `RANGE_M100_100`, `-1e100` | write attempted | `[0, 0]` | clamped/converts to lower endpoint 0 |
| degrees NaN | `DEGREES`, `NaN` | `ValueError: cannot convert float NaN to integer` | none | rejected during integer conversion |
| degrees +Inf | `DEGREES`, `+Inf` | `OverflowError: cannot convert float infinity to integer` | none | rejected during integer conversion |
| degrees −Inf | `DEGREES`, `−Inf` | `OverflowError: cannot convert float infinity to integer` | none | rejected during integer conversion |
| degrees huge positive | `DEGREES`, `1e100` | `ValueError` — sign-encoding magnitude exceeds 32767 | none | rejected by the real sign-encoding range check |
| degrees huge negative | `DEGREES`, `-1e100` | `ValueError` — sign-encoding magnitude exceeds 32767 | none | rejected by the real sign-encoding range check |
| gripper NaN | `RANGE_0_100`, `NaN` | write attempted; raw register 0 | `[0, 0]` | lower endpoint |
| gripper +Inf | `RANGE_0_100`, `+Inf` | write attempted; raw register 4095 | `[255, 15]` | upper endpoint |
| gripper −Inf | `RANGE_0_100`, `−Inf` | write attempted; raw register 0 | `[0, 0]` | lower endpoint |

The workflow log ends with: `PASS: 14 cases exercised against pinned LeRobot conversion/write code; no hardware connected.`

### Scope and cases not covered

This is a **runtime test of pinned LeRobot motor-bus conversion/serialization**, and the captured bytes are evidence of the payload passed to a **mocked SDK boundary**. It is not a full runtime test of `SO100Follower.send_action()` or the complete GR00T-to-robot call path. In particular:

- The harness does not instantiate `SO100Follower` or execute its relative-target clipping logic. The `max_relative_target=None` default and configured clipping branch were therefore **not runtime-tested** in this run.
- The ordinary finite case is the midpoint `0.0`; other finite in-range values were not sampled.
- The test captures bytes passed to the mock. It does not prove that a real serial packet was sent, received, accepted by a motor, or caused motion.
- No physical robot was connected and no physical actuation is claimed.
- These 14 cases do not establish complete path-set coverage for GR00T, LeRobot, or a deployed robot system.

Evidence levels remain distinct: (1) adapter-only reproduction; (2) runtime test of the pinned LeRobot motor-bus driver conversion/serialization; (3) payload captured at a mocked SDK boundary; (4) actual physical actuation — **not tested**.


## 12. Follow-up runtime test — actual pinned SO100Follower.send_action()

**Run:** [Pinned LeRobot SO100 driver reproduction — run 38776033231](https://github.com/omwei-org/omwei-eabc/actions/runs/38776033231)  
**Status:** PASS; full job logs inspected  
**Harness commit:** `ae919423cfd7abdcf64ef5e47ce44fa16f6beddc`  
**LeRobot revision:** `c75455a6de5c818fa1bb69fb2d92423e86c70475`  
**Python:** CPython 3.11.17  
**Command:** `python evidence/scripts/test_pinned_lerobot_driver.py`

The harness now imports and calls the actual pinned `SO100Follower.send_action()` method. Construction-time dependencies (base robot initialization, camera factory/config imports, and an unrelated robot factory import) are stubbed so no camera, calibration setup, physical serial device, or motor is initialized. The follower method, pinned `ensure_safe_goal_position()`, `FeetechMotorsBus.sync_write()`, normalization, sign encoding, serialization, and recording `GroupSyncWrite.addParam()` remain the actual pinned implementations. The mock SDK captures payload bytes and does not transmit a packet.

### `send_action()` results

The cases below use a single mocked joint with calibration range 0–4095. For `max_relative_target=None`, present-position reading is not called by the pinned method.

| Case | Configuration / input | `send_action()` outcome | Exact mock SDK bytes |
|---|---|---|---|
| finite | `RANGE_M100_100`, `0.0`, cap `None` | returns `{'joint.pos': 0.0}` | `[255, 7]` |
| NaN | `RANGE_M100_100`, NaN, cap `None` | returns NaN unchanged in returned action; bus conversion maps to lower endpoint | `[0, 0]` |
| +Inf | `RANGE_M100_100`, +Inf, cap `None` | returns +Inf unchanged in returned action; bus conversion maps to upper endpoint | `[255, 15]` |
| −Inf | `RANGE_M100_100`, −Inf, cap `None` | returns −Inf unchanged in returned action; bus conversion maps to lower endpoint | `[0, 0]` |
| `1e100` | `RANGE_M100_100`, cap `None` | returns input unchanged; bus conversion maps to upper endpoint | `[255, 15]` |
| `-1e100` | `RANGE_M100_100`, cap `None` | returns input unchanged; bus conversion maps to lower endpoint | `[0, 0]` |
| NaN degrees | `DEGREES`, cap `None` | `ValueError: cannot convert float NaN to integer` | none |
| +Inf degrees | `DEGREES`, cap `None` | `OverflowError: cannot convert float infinity to integer` | none |
| −Inf degrees | `DEGREES`, cap `None` | `OverflowError: cannot convert float infinity to integer` | none |
| `1e100` degrees | `DEGREES`, cap `None` | `ValueError` from sign-encoding magnitude limit | none |
| `-1e100` degrees | `DEGREES`, cap `None` | `ValueError` from sign-encoding magnitude limit | none |
| relative clip | `RANGE_M100_100`, input `100.0`, present position `0.0`, cap `2.0` | actual helper clips goal to `2.0`; returned action is `{'joint.pos': 2.0}` | `[40, 8]` |

The relative-clipping payload `[40, 8]` is little-endian register value 2088, corresponding to the calibrated conversion of the clipped normalized target 2.0. The warning in the log records original target 100.0 and safe target 2.0.

### Interpretation and remaining limits

This follow-up now establishes runtime behaviour through the actual pinned `SO100Follower.send_action()` method for the cases above, including the `max_relative_target=None` branch and a configured scalar relative-target cap. The previous section's statement that the full follower method was not tested describes the earlier run (38775382201); this new run supersedes that limitation for the listed cases.

Still not tested:
- `max_relative_target` as a per-motor dictionary, including key mismatch and edge configurations;
- a non-zero present-position value or multiple joints in the clipping branch;
- the actual GR00T-to-`send_action()` call chain in one integrated process;
- serial transport, motor acknowledgement, or physical actuation.

**Boundary remains explicit:** this is a runtime test of pinned driver/follower code plus payload capture at a mocked SDK boundary. It does not prove that any serial packet reached a real motor or that physical movement occurred, and it does not establish complete path-set coverage.

