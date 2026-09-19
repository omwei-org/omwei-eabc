# Validation Run 002 — Prepare / Authority Change / Commit

**Status:** Planned validation experiment  
**Purpose:** Validate commit-time authority semantics under a real authority-state change between preparation and commit.

> **Core question**
>
> If a command is prepared while authority is valid, and the authority state changes before the externally effective commit, does the final commit decision use the current authority state rather than the authority state observed during preparation?

This document is a test protocol, not a validation result. No outcome should be recorded as established until the experiment is actually executed and the resulting evidence is preserved.

## 1. Hypothesis

A prepared command does not acquire permanent authority merely because authorization was valid at preparation time.

The final externally effective commit MUST be governed by the authority state applicable at the commit decision.

Expected evidence pattern:

```text
prepare
  │
  ├── authority epoch N → authorization available
  │
  │       AUTHORITY CHANGES
  │       epoch N → N+1
  │
  ▼
commit
  │
  └── final decision evaluated against epoch N+1
          │
          └── no external effect if authority is no longer valid
```

The exact implementation-side outcome is intentionally not predetermined by this plan. For example, an implementation may report a stale-epoch or revoked condition. Such terminology must be mapped to EABC semantics only after the observed evidence establishes the mapping.

## 2. Test invariants

The run should preserve these invariants:

1. The prepared payload bytes remain unchanged.
2. The payload digest remains unchanged from prepare through commit.
3. The command identifier remains unchanged.
4. The environment identifier remains unchanged.
5. Authority changes after preparation and before final commit.
6. The final decision records the authority state actually evaluated at commit.
7. No external effect is treated as committed unless execution evidence establishes it.
8. Evidence from both implementation sides can be correlated without an untrusted side channel.

## 3. Required observations

### Prepare

Capture at minimum:

- `command_id`
- `env_id`
- exact payload bytes or a reproducible reference to them
- payload/action digest
- authority epoch observed at preparation
- preparation timestamp
- authorization/preparation result
- evidence integrity reference

### Authority transition

Capture:

- old authority epoch
- new authority epoch
- transition/revocation event
- transition timestamp
- integrity reference

### Commit

Capture:

- same `command_id`
- same `env_id`
- same payload/action digest
- authority epoch used for final decision
- final authorization outcome
- implementation-side reason, where present
- execution outcome
- commit/execution timestamp
- evidence integrity reference

## 4. Primary correlation check

The reviewer must be able to establish:

```text
prepare.command_id == commit.command_id

prepare.payload_digest == commit.payload_digest

prepare.env_id == commit.env_id

prepare.authority_epoch != commit.authority_epoch
```

The final authority epoch must be attributable to the final authorization/commit decision rather than inferred from an unrelated runtime value.

## 5. Expected semantic interpretation

If the authority changes from epoch N to N+1 before commit and the command is not reauthorized under N+1, the run should demonstrate that the previously prepared authorization does not by itself authorize the later external effect.

The result should then be mapped to the existing EABC authorization outcomes:

- `ALLOW`
- `DENY`
- `EXPIRED`
- `CANCELLED`
- `UNKNOWN`

Do **not** add an implementation-specific outcome such as `STALE_EPOCH` to the EABC core merely because the implementation uses that term.

If the implementation returns `STALE_EPOCH`, record it first as the observed implementation outcome and determine its EABC mapping from the actual evidence.

## 6. Negative control

Where feasible, perform a second commit with a freshly authorized command after the authority transition.

The control should use a new command identifier and must not reuse the old authorization artifact.

Expected comparison:

```text
old prepared authorization
        ↓
authority changed
        ↓
commit → blocked/not authorized

fresh authorization under current state
        ↓
commit → outcome determined by current authority
```

## 7. Failure and evidence handling

The run must distinguish:

- authorization failure;
- execution failure;
- communication failure;
- evidence failure;
- unknown outcome.

Missing evidence must not be interpreted as successful execution.

If the implementation cannot determine whether an external effect occurred, record `UNKNOWN` rather than inferring `FAILED` or `COMMITTED`.

## 8. Evidence package

After execution, preserve:

1. raw authority-side records verbatim;
2. raw execution-side records verbatim;
3. exact payload/action digest;
4. authority transition evidence;
5. commit/execution evidence;
6. integrity verification recipe;
7. independently recomputed integrity results;
8. cross-side correlation table;
9. implementation mappings;
10. anomalies and serialization discoveries;
11. source-side commit/version identifiers where available;
12. the EABC interoperability-contract commit against which the run was performed.

The resulting record should become `evidence/validation-run-002.md` only after the run has actually occurred.

## 9. Success criteria

The experiment is successful as an evidence run if an independent reviewer can determine from the preserved artifacts:

1. what was prepared;
2. under which authority state it was prepared;
3. that authority changed before commit;
4. what authority state was evaluated at commit;
5. what authorization decision resulted;
6. whether execution was attempted;
7. whether an external state transition was committed;
8. how the records from both sides correlate;
9. that the relevant integrity evidence can be independently verified.

A successful experiment does not automatically imply a new EABC requirement. Its result must first be classified as:

- existing EABC semantic already demonstrated;
- interoperability mapping;
- implementation-specific behavior;
- or evidence of a potentially missing EABC semantic.

## 10. Constraints

This run should not:

- modify the meaning of EABC authorization outcomes in advance;
- introduce `STALE_EPOCH` as a sixth authorization outcome;
- require Ron's hash-chain implementation as an EABC mechanism;
- rely on a shared internal architecture;
- infer execution success from authorization alone;
- rewrite or normalize the exact payload merely to make correlation easier.

The purpose is to test the boundary, not to design the result into the test.

## 11. Relation to Validation Run 001

Run 001 established an observed pair:

```text
same payload digest
epoch 4 → ALLOW
epoch 5 → BLOCK / REVOKED
```

Run 002 asks the stronger temporal question:

```text
authorized at prepare
        ↓
authority changes
        ↓
same prepared command reaches commit
        ↓
what happens?
```

This distinction is important. Run 001 demonstrates authority-context dependence across observed evaluations. Run 002 is intended to test whether that property is enforced across the prepare-to-commit temporal boundary.

## 12. Current status

**Not executed.**

No conclusion about prepare/commit authority invalidation should be drawn from this document until real execution evidence is attached to a subsequent validation record.
