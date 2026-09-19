# Evidence Reference — Interoperability Validation Run 001

**Status:** Real validation record  
**Date of observed run:** 2026-09-18  
**Scope:** Cross-organization interoperability between independent execution-authority implementations

> **Key observation**
>
> **Authority is not a property of the payload alone. Authority is evaluated in the authority state applicable at commit time.**
>
> In this run, the same payload produced the same SHA-256 digest, while the authority context changed from epoch 4 to epoch 5. The first command was `ALLOW`; the later command was `BLOCK` with reason `REVOKED`.

## 1. Provenance and chain-of-custody anchors

This record documents evidence from a real interoperability run performed by two independent implementation sides.

### Source evidence

The two journal entries reproduced below were provided from the participating implementation's running code.

**Source anchor:** Ron Reynolds — live interoperability run, 2026-09-18.  
**Observed timestamps in source data:** 2026-09-18T08:46:40.112Z and 2026-09-18T08:46:41.007Z.

No source-side Git commit SHA was provided with these entries. The date and the exact source timestamps are therefore the available provenance anchor in this record.

### EABC contract anchor

The interoperability contract document existed as:

- **Document:** `docs/005-interoperability-contract.md`
- **Commit:** `4d099956cc6e85d2e780dea4da2c93f103aa4206`
- **Status at the time of recording:** Draft v0.1 — Provisional

The evidence record is intentionally separate from the normative specification. It records observations against a particular contract version rather than changing that contract retroactively.

## 2. Raw source data — verbatim

The following JSON is reproduced verbatim from the two real journal entries supplied from the running implementation:

```json
[
  {
    "seq": 1,
    "command_id": "2666ebb0-4cb9-4336-8abc-ae8e94b8793b",
    "env_id": "recording-relay",
    "epoch": 4,
    "payload_digest": "22055b0016c31920d3ddb38d01edb288b3c5da8592cd3a4b79d1967822483fc9",
    "decision": "ALLOW",
    "at": "2026-09-18T08:46:40.112Z",
    "prev_hash": "000...000",
    "entry_hash": "36f37b56a641b91fa4921af6fe80aa3fce970ee583d3b8528a567ae59d67c6b8"
  },
  {
    "seq": 2,
    "command_id": "7c1f4a9d-2b8e-4f31-9a05-6d3e8c07b514",
    "env_id": "recording-relay",
    "epoch": 5,
    "payload_digest": "22055b0016c31920d3ddb38d01edb288b3c5da8592cd3a4b79d1967822483fc9",
    "decision": "BLOCK",
    "reason": "REVOKED",
    "at": "2026-09-18T08:46:41.007Z",
    "prev_hash": "36f37b56a641b91fa4921af6fe80aa3fce970ee583d3b8528a567ae59d67c6b8",
    "entry_hash": "715ebceb05f445adcc3280f21ed052ad256de73d5e11afb0d10540728aa9874a"
  }
]
```

**Important source-data note:** the public JSON representation of entry 1 omits `reason`. The value `reason = ""` is nevertheless part of the fixed-order hash input described below. The verbatim public entries above are preserved as supplied; the canonical hash-input reconstruction is documented separately in Section 3.

## 3. Exact independent hash-verification recipe

The participating implementation defines `entry_hash` over the following fixed-order array:

```text
[seq, command_id, env_id, epoch, payload_digest, decision, reason, at, prev_hash]
```

Verification:

1. Read the nine fields in exactly this order.
2. For an `ALLOW` entry whose source representation omits `reason`, use `reason = ""`.
3. Serialize as compact JSON: UTF-8, no spaces, separators `,` and `:`, exact string values.
4. Exclude `entry_hash` from the hash input.
5. Compute SHA-256 over the resulting UTF-8 bytes.
6. Compare the hexadecimal digest with the supplied `entry_hash`.
7. Verify each entry's `prev_hash` equals the preceding entry's `entry_hash`.

Observed convention:

```text
ALLOW → reason = ""
BLOCK → reason = explicit reason, e.g. REVOKED
```

This is an implementation/interoperability observation, not a new EABC core requirement.

## 4. Independently verified integrity results

The supplied hashes were independently recomputed from the fixed-order hash input.

### Entry 1

- `seq = 1`
- `decision = ALLOW`
- canonical `reason = ""`
- `prev_hash = 000...000`
- computed `entry_hash`:

```text
36f37b56a641b91fa4921af6fe80aa3fce970ee583d3b8528a567ae59d67c6b8
```

**Result: match.**

### Entry 2

- `seq = 2`
- `decision = BLOCK`
- `reason = REVOKED`
- `prev_hash` equals entry 1 `entry_hash`
- computed `entry_hash`:

```text
715ebceb05f445adcc3280f21ed052ad256de73d5e11afb0d10540728aa9874a
```

**Result: match.**

## 5. Observed interoperability mappings

| Participating implementation | EABC / interoperability meaning | Status |
|---|---|---|
| `ALLOW` | `ALLOW` | Observed |
| `BLOCK` | `DENY` mapping | Observed |
| `payload_digest` | `action_digest` | Observed |
| `epoch` | authority epoch | Observed |
| `command_id` | command correlation identifier | Observed |
| `reason` | block/failure reason where applicable | Observed |
| `seq / prev_hash / entry_hash` | integrity mechanism | Observed, implementation-specific |

`BLOCK` is an implementation mapping to EABC `DENY`; it does not replace the EABC authorization outcome.

The hash-chain fields demonstrate one integrity mechanism; EABC does not require a hash chain.

## 6. Digest binding

Both entries contain the same:

```text
payload_digest =
22055b0016c31920d3ddb38d01edb288b3c5da8592cd3a4b79d1967822483fc9
```

The participating implementation defines this as SHA-256 over the exact payload bytes.

Thus the same payload is observed across two different authority contexts:

```text
same payload
    │
    ├── authority epoch 4 → ALLOW
    │
    └── authority epoch 5 → BLOCK / REVOKED
```

## 7. Principal finding: authority is state-at-commit, not payload property

> ### **AUTHORITY IS NOT A PROPERTY OF THE PAYLOAD**
>
> **The observed authority depends on the authority state applicable at the commit decision.**
>
> The payload digest remained identical while the authority epoch changed:
>
> ```text
> same payload digest
>        │
>        ├── epoch 4 → ALLOW
>        │
>        └── epoch 5 → BLOCK / REVOKED
> ```
>
> Therefore, possession of an otherwise identical payload does not by itself establish authority to commit it.

This is an observed interoperability result. It does not by itself exhaustively validate every possible authority transition.

## 8. Serialisation discovery

The `reason` field produced an independently reproducible discovery.

The public `ALLOW` entry does not display a `reason` field. Recomputing its `entry_hash` showed that the hash input contains `reason = ""`, rather than a missing field or JSON `null`.

Testing the possible reconstructions showed that only the empty-string representation reproduced the published digest.

This demonstrates why interoperability evidence must preserve exact serialization semantics rather than only semantic field descriptions.

The empty-string convention is recorded here as an observed interoperability detail. It is not added to EABC core merely because one implementation uses it.

## 9. Epoch distinction

The run also establishes the need to distinguish an authority epoch from an execution/runtime epoch.

For interoperability, the observed `epoch` maps to the authority state against which the authorization decision was evaluated.

An implementation may additionally expose an execution or runtime epoch. That value must not silently substitute for the authority epoch when evidence is intended to prove the authority state applicable to the commit decision.

This distinction remains important for prepare/commit and TOCTOU validation.

## 10. What this evidence does not establish

This run does **not** by itself validate:

- `EXPIRED`;
- `CANCELLED`;
- `UNKNOWN`;
- execution `FAILED`;
- execution `ABORTED`;
- execution `UNKNOWN`;
- missing or incomplete evidence handling;
- payload substitution or digest mismatch;
- authority change between prepare and commit beyond the observed revocation case;
- interoperability with a third independent implementation.

It also does not establish that the participating implementation's hash-chain format is required by EABC.

## 11. Relationship to EABC documents

This evidence record is subordinate to the normative specification.

Relevant documents:

- `docs/001 – Execution Authority Properties.md`
- `docs/002-evidence-model.md`
- `docs/003-failure-semantics.md`
- `docs/004-conformance.md`
- `docs/005-interoperability-contract.md`

The purpose of this record is to provide concrete validation evidence against those concepts, not to redefine them.

In particular:

- implementation mappings remain mappings;
- observed serialization details remain implementation/interoperability details;
- failure modes not yet demonstrated remain unvalidated;
- no new EABC authorization outcome is created by this run.

## 12. Reproduction checklist

An independent reviewer should be able to reproduce the core integrity verification by:

1. copying the raw entries from Section 2;
2. reconstructing the nine-field hash array from Section 3;
3. using `reason = ""` for the first `ALLOW` entry;
4. serializing compactly as UTF-8 JSON with no spaces;
5. excluding `entry_hash` from the hash input;
6. computing SHA-256;
7. comparing both resulting hashes with Section 4;
8. verifying entry 2 `prev_hash` equals entry 1 `entry_hash`;
9. comparing the identical `payload_digest` values;
10. comparing the authority epochs and decisions.

No trust in a narrative description is required for those checks.

## 13. Next validation step

The next validation cycle should extend the evidence rather than prematurely extend the EABC core.

Priority cases:

1. authority change between prepare and commit;
2. explicit `DENY` mapping beyond `BLOCK / REVOKED`;
3. `EXPIRED`;
4. `CANCELLED`;
5. `UNKNOWN`;
6. execution failure and abort;
7. missing/incomplete evidence;
8. digest mismatch / payload substitution;
9. an additional independent implementation.

The purpose is to determine which observations are stable interoperability requirements, which are implementation mappings, and whether any genuinely missing EABC semantic is exposed by real evidence.
