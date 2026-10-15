# Evidence Reference — Observation: GR00T SO100 Pre-Actuation Path

**Status:** External system observation (negative path)  
**Date of observed analysis:** 2026-10-15  
**Scope:** Pre-actuation action path from NVIDIA Isaac-GR00T policy output to LeRobot SO100/SO101 motor write

> **Key observation**
>
> **Invalid model outputs (NaN, ±Inf, unusually large finite values) pass through the GR00T SO100 evaluation adapter and reach the LeRobot `send_action()` / motor-write boundary without rejection.**
>
> There is no execution-authority boundary, Commit Gate, or fail-closed check on this protected-effect path in the reference configuration.

## 1. Provenance and chain-of-custody anchors

### Source systems

| Component | Source | Anchor |
|---|---|---|
| GR00T eval path | [NVIDIA/Isaac-GR00T](https://github.com/NVIDIA/Isaac-GR00T) | Local checkout analysed 2026-10-15; key file `gr00t/eval/real_robot/SO100/eval_so100.py` |
| LeRobot driver | [huggingface/lerobot](https://github.com/huggingface/lerobot) @ `c75455a6de5c818fa1bb69fb2d92423e86c70475` | Pinned by GR00T SO100 `pyproject.toml` |
| Automated tests | Isolated unit tests against `So100Adapter` + `_select_action_steps` | Fake policy, no hardware |

### EABC contract anchor

This record is subordinate to:

- `docs/001` — Execution Authority Properties (Complete Mediation, Independent Execution Authority)
- `docs/002` — Evidence Model
- `docs/003` — Failure and Execution Semantics (fail-closed)
- `docs/004` — Conformance

It does **not** redefine EABC requirements. It records an observed gap in an external real-robot VLA evaluation path.

## 2. Protected effect under observation

The externally committed effect of interest is:

```text
LeRobot SO100/SO101 follower
  → bus.sync_write("Goal_Position", goal_pos)
I.e. a joint-position command written to the motor bus.
3. Observed call path (source-traced)
textPolicyClient / Gr00tPolicy.get_action()
        │  action chunk (may contain NaN / ±Inf / large finite)
        ▼
So100Adapter.get_action()
        │
        ▼
So100Adapter.decode_action_chunk()   ← float() conversion only; no isfinite / bounds check
        │
        ▼
_select_action_steps()               ← length check only
        │
        ▼
robot.send_action(action_dict)       ← LeRobot SO100Follower / SO101Follower
        │
        ▼
[if max_relative_target is not None]
  ensure_safe_goal_position()        ← relative clip only; default is None
        │
        ▼
bus.sync_write("Goal_Position", ...) ← EFFECT (motor write path entered)
Policy-level checks that run on this path

Server-side Gr00tPolicy.check_action: keys, np.ndarray, dtype=float32, shape (B,T,D), horizon match.
No isfinite / NaN / Inf / magnitude checks.

Adapter checks

Structural only (missing key → KeyError; wrong dimension → IndexError).
Non-finite and large finite values are forwarded unchanged.

4. Raw test evidence
Isolated tests (fake policy, no hardware) established the following results at the adapter → pre-send_action boundary:













































InputResult at action_dictClassificationNormal finitePassed throughExpectedNaN in jointPassed through as nanNon-rejection+Inf in jointPassed through as infNon-rejection−Inf in jointPassed through as -infNon-rejectionLarge finite (1e10)Passed through unchangedNon-rejectionMissing "gripper" keyKeyErrorStructural rejectionWrong single_arm dimensionIndexErrorStructural rejection
Exact functions under test:

So100Adapter.decode_action_chunk
So100Adapter.get_action
_select_action_steps

in gr00t/eval/real_robot/SO100/eval_so100.py.
5. Driver behaviour (default configuration)
Inspected at LeRobot commit c75455a6de5c818fa1bb69fb2d92423e86c70475:

























MechanismDefaultEffect on NaN / Inf / large valuesmax_relative_targetNoneRelative safety clip disabledensure_safe_goal_positionOnly if max_relative_target setArithmetic clip; does not reject NaN_unnormalize (RANGE_M100_100 / RANGE_0_100)Always on write pathClamps Inf/large to normalised extremes; NaN may be coerced by min/max then written as extreme finite
Conclusion from source + reproduction: with the default configuration, non-finite and large values reach the motor-write call site. There is no explicit fail-closed rejection of invalid actions before sync_write.
No real-hardware movement was performed or claimed.
6. Mapping to EABC properties





























EABC propertyObserved status on this pathComplete MediationNot satisfied. Invalid actions reach the protected effect without an intervening execution-authority decision.Independent Execution AuthorityNot present. Policy output and actuator path are not separated by an independent authority boundary.Fail-closed semanticsNot present for non-finite / extreme values. Invalid inputs are forwarded or silently coerced, not denied.Commit GateAbsent. No explicit allow/deny transition before Goal_Position write.Execution Attestation (EAtt)Absent. No commit-time evidence artifact binding decision to effect.
This is an observation of a non-conforming external path, not a claim that GR00T or LeRobot claim EABC conformance.
7. What this evidence does not establish
This record does not establish:

that physical motor movement occurred with invalid values;
behaviour of non-default LeRobot configurations (max_relative_target set);
behaviour of other GR00T embodiments or eval paths;
that a minimal isfinite guard would constitute a full EABC boundary;
interoperability with any EGA or EABC implementation;
prepare/commit TOCTOU properties (see Validation Run 002 plan).

8. Relationship to EABC / EGA work
This path is a concrete instance of the problem EABC is designed to address:
textAuthorization / decision domain (VLA policy output)
        │
        │  ← no execution-authority boundary
        ▼
Execution domain (motor Goal_Position write)
It is a candidate negative example for:

Complete Mediation,
fail-closed behaviour on protected effects,
the absence of a Commit Gate before externally observable robotic actuation.

A future EGA-style experiment could insert a minimal Commit Gate before send_action (finite + bounds check, explicit deny, optional attestation log) without requiring changes to the normative EABC core.
9. Reproduction checklist
An independent reviewer can reproduce the adapter-boundary results by:

Checking out NVIDIA/Isaac-GR00T.
Loading So100Adapter (with mocks for optional lerobot / transformers deps if needed).
Supplying a fake policy that returns action chunks containing NaN, ±Inf, large finite, missing keys, and wrong dimensions.
Calling get_action + _select_action_steps and inspecting the resulting action_dict.
Confirming that non-finite / large values appear unchanged in the dict that would be passed to robot.send_action().
Inspecting LeRobot so100_follower.py / so101_follower.py and motors_bus.py at the pinned commit for default max_relative_target=None and lack of explicit isfinite rejection before sync_write.

No hardware and no trust in narrative claims are required for the adapter-boundary results.
10. Next steps (non-normative)

Preserve this record under evidence/ as an external negative-path observation.
Optionally add a corresponding illustrative robotic scenario under examples/ showing how an EABC-conformant boundary would mediate the same path.
Optionally prototype a minimal Commit Gate experiment (EGA-style) in front of send_action as a separate engineering exercise — without treating that prototype as an EABC requirement.


Classification: External observation — non-conforming pre-actuation path.

Not a validation of any EABC implementation.
