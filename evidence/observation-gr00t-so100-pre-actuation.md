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
