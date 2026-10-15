# Evidence Reference — GR00T SO100/SO101 Pre-Actuation Path

**Status:** Preliminary external-system observation; downstream driver behaviour remains unverified  
**Analysis date:** 2026-10-15  
**Scope:** Action validation in the NVIDIA Isaac-GR00T SO100 evaluation path, from policy output to the call site that invokes LeRobot's `send_action()`.

> **Key finding**
>
> The inspected GR00T SO100 adapter does not explicitly reject non-finite action values (NaN or ±Inf) or unusually large finite values before constructing the action dictionary. An isolated test harness also observed these values passing through the adapter-side selection path. This does **not**, by itself, prove that the real LeRobot motor bus receives those values or that a physical actuator moves.

The evidence supports a validation gap at the adapter boundary. The end-to-end effect at the real driver/motor-bus boundary remains **unverified**.

## 1. Provenance and evidence boundaries

| Component | Source / anchor | What is established |
|---|---|---|
| GR00T SO100 evaluation path | [NVIDIA/Isaac-GR00T](https://github.com/NVIDIA/Isaac-GR00T), `gr00t/eval/real_robot/SO100/eval_so100.py` | Source inspection of the adapter and action-selection path |
| LeRobot dependency | [huggingface/lerobot](https://github.com/huggingface/lerobot), revision `c75455a6de5c818fa1bb69fb2d92423e86c70475` (as pinned by the GR00T SO100 project metadata) | Dependency/revision anchor; does not substitute for a reproduced end-to-end driver test |
| Isolated adapter harness | Fake policy and test doubles; no physical robot | NaN, ±Inf and a large finite value were observed passing through the tested adapter-side path; structural errors raised exceptions |
| Real motor bus / physical actuation | Not reproduced in this evidence run | Unverified |

This record distinguishes source inspection, isolated reproduction, and real-driver behaviour. They are separate evidence levels and must not be conflated.

## 2. Protected effect and current scope

The effect of interest is a joint-position command ultimately written to a SO100/SO101 motor bus, commonly through a call such as:

```text
robot.send_action(action_dict)
  → LeRobot follower / motor-bus path
  → bus.sync_write("Goal_Position", ...)
```

The adapter-side tests did not establish that the final `sync_write` call in the real driver was reached with the invalid values. The path above identifies the effect being investigated, not a claim that the entire path has been reproduced.

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

## 5. Downstream driver behaviour: open verification item

The GR00T project metadata pins a LeRobot revision, but this evidence record does not contain a reproducible end-to-end test proving the handling of NaN, ±Inf, or extreme finite values by the real driver and motor bus.

In particular, the following must remain open until verified against the pinned source and a test that reaches the relevant code:

- whether and where action values are unnormalised or clipped;
- how NaN and infinities behave under the exact numeric operations used by the pinned implementation;
- whether conversion to motor units or bus payload types rejects, clamps, transforms, or propagates such values;
- whether the real `sync_write("Goal_Position", ...)` call can be reached with the tested inputs.

Do not infer these outcomes from a fake `sync_write`, from generic Python numeric behaviour, or from the presence/absence of `max_relative_target` alone.

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
- exact downstream handling of NaN, ±Inf or large finite values;
- behaviour under non-default driver configurations;
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

1. Inspect the exact LeRobot revision pinned by the GR00T project metadata.
2. Trace the real follower implementation through unit conversion and the motor-bus write method.
3. Add a test using the real conversion/driver code with a recording or fake transport at the lowest practical boundary; do not use a physical robot for initial fault injection.
4. Assert and record exactly what reaches the transport for each invalid input, including any exceptions, clamping, conversion or rejection.
5. Keep the result explicitly scoped to the tested revision and configuration.

Until that downstream test is complete, the conclusion must remain limited to the adapter-side validation gap.

## 10. Classification and next step

**Classification: D — adapter-side validation gap observed; end-to-end driver effect unverified.**

This is a preliminary external-system observation, not validation of an EABC implementation and not evidence of physical actuation with invalid values.

The next evidence-producing step is to verify the pinned LeRobot conversion and motor-bus path with a reproducible test. Do not upgrade the classification to a confirmed motor-write-path finding until that evidence exists.
