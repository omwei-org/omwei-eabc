# HALOS Prepare / Commit Control Pair — Runs 002 and 003

**Status:** Implementation evidence  
**Scope:** EABC/GIE governed physical execution path  
**Source repository:** `omwei-org/halos-1.3-atl-analysis`  
**Remote evidence commit:** `70eec6c0ce3633b71b0c74ec77407cf55d0cd64b`  
**CI run:** `35463862721` — SUCCESS

## 1. Purpose

This record preserves a paired implementation experiment from the HALOS analysis repository.

The pair uses the same governed physical execution path and the same payload, while differing in whether authority changes between preparation and commit.

The evidence is non-normative. It does not add an EABC authorization outcome, prescribe the HALOS implementation, or establish a hardware-enforced security boundary.

## 2. Paired scenarios

### Run 002 — authority change

Observed sequence:

```
PREPARE @ authority epoch 1
        ↓
ALLOW
        ↓
authority revoked
epoch 1 → 2
        ↓
COMMIT @ current authority state
        ↓
BLOCK / STALE_EPOCH
        ↓
no physical effect
```

The execution payload remains `RELAY:ON`, but the prepared authorization does not result in a physical effect after the authority state changes.

### Run 003 — unchanged-authority control

Observed sequence:

```
PREPARE @ authority epoch 1
        ↓
ALLOW
        ↓
no authority change
epoch 1 → 1
        ↓
COMMIT
        ↓
ALLOW / authorized
        ↓
RELAY:ON applied
```

Run 003 uses:

- `command_id = run003-control-001`
- initial authority epoch = `1`
- final authority epoch = `1`
- decision = `ALLOW`
- reason = `authorized`
- applied = `true`
- applied payload = `RELAY:ON`
- relay state = `true`

Its execution evidence records PREPARE, FINAL_AUTHORITY_CHECK, and EXECUTION/COMMITTED.

## 3. Paired interpretation

The important observation is the controlled difference between the two runs:

| Property | Run 002 | Run 003 |
|---|---|---|
| Payload | `RELAY:ON` | `RELAY:ON` |
| PREPARE | ALLOW | ALLOW |
| Initial authority epoch | 1 | 1 |
| Authority change | 1 → 2 | none |
| Commit decision | BLOCK | ALLOW |
| Physical effect | not applied | applied |
| Governing path | same | same |

The pair therefore provides implementation evidence for the following bounded observation:

> With the tested governed physical execution path, a prepared command does not produce the physical effect after the governing authority is revoked before commit, while the corresponding unchanged-authority control can proceed through commit and apply the same payload.

This is evidence of observed behavior in the tested implementation. It is not, by itself, an exhaustive validation of all possible authority transitions, verifier failures, or execution failure modes.

## 4. Integrity and provenance

Run 003 was committed to the HALOS repository and published through CI.

**Remote commit:**
`70eec6c0ce3633b71b0c74ec77407cf55d0cd64b`

**CI run:**
`35463862721` — SUCCESS

**Published artifacts:**

- `run-002-evidence`
- `run-003-evidence`

Run 003 evidence integrity manifest:

```
run-003-evidence.sha256
a3b02b7e8e476fae27386094209dbb2b7644560e6f432fd5ed49850c05a3f247
```

The SHA-256 value was independently checked against the generated Run 003 evidence artifact.

Run 002 remains the existing reference baseline and its CI publication was preserved unchanged.

## 5. EABC evidence-model mapping

The pair exercises several existing evidence concepts:

- **Decision Evidence:** PREPARE and final commit authorization decisions.
- **State Evidence:** authority epoch at preparation and commit.
- **Commit Evidence:** the transition from prepared authorization to final commit.
- **Execution Evidence:** whether the physical effect was applied.
- **Correlation Evidence:** the execution command identifier and environment/execution context available in the implementation evidence.
- **Integrity Evidence:** deterministic evidence artifact plus SHA-256 manifest.

These are observations against the existing EABC evidence model. The HALOS implementation's concrete field names and outcome labels remain implementation-specific.

In particular, `STALE_EPOCH` is recorded as an implementation-side reason. It is not introduced as a new EABC authorization outcome.

## 6. What this evidence establishes

Within the tested HALOS/GIE implementation:

1. authorization can be observed at preparation;
2. authority state can change before commit;
3. the tested commit path re-evaluates the authority state;
4. the revoked case does not apply the physical effect;
5. an unchanged-authority control reaches ALLOW at commit;
6. the control's physical effect is separately evidenced as applied;
7. the two cases use the same governed execution path and payload;
8. the evidence artifacts are published independently through CI.

## 7. What this evidence does not establish

This pair does **not** establish:

- hardware-enforced isolation;
- resistance to every possible software bypass;
- behavior when the verifier or authority service is unavailable;
- `EXPIRED`, `CANCELLED`, or `UNKNOWN` semantics;
- execution failure or abort semantics;
- payload substitution/digest mismatch handling;
- interoperability with an additional independent implementation;
- that the HALOS-specific hash or artifact format is required by EABC.

Missing or unobservable cases remain validation gaps rather than successful outcomes.

## 8. Relationship to normative EABC

This record is subordinate to the existing EABC specification and evidence model.

It does not modify:

- EABC authorization outcomes;
- the EABC evidence categories;
- interoperability requirements;
- implementation-profile semantics.

The purpose is to preserve concrete implementation evidence that can be independently inspected and compared with later evidence from other implementations.

## 9. Reproduction anchors

An independent reviewer can begin verification from:

- repository: `omwei-org/halos-1.3-atl-analysis`
- commit: `70eec6c0ce3633b71b0c74ec77407cf55d0cd64b`
- CI run: `35463862721`
- artifacts: `run-002-evidence`, `run-003-evidence`
- Run 003 SHA-256: `a3b02b7e8e476fae27386094209dbb2b7644560e6f432fd5ed49850c05a3f247`

The evidence should be interpreted together with the underlying artifacts rather than as a replacement for them.
