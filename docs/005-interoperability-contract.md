# EABC Interoperability Contract

**Status:** Draft v0.1 — Provisional  
**Validation status:** Validated against one implementation pair and one real interoperability run  
**Scope:** Interoperability between independent implementations of an EABC execution-authority boundary

---

## 1. Purpose and status

EABC defines normative execution-authority properties, evidence requirements, execution semantics, and conformance requirements.

This document defines the minimum interoperability contract needed when two independent implementations exchange, produce, or reconcile execution-authority evidence.

This document does **not** redefine the normative EABC properties in [001], replace the evidence model in [002], or replace the authorization and execution semantics in [003].

This first version is intentionally provisional. It has been validated against one real implementation pair and one real interoperability run. Observations from that run are included where useful, but an observed implementation behavior is not thereby made a universal EABC requirement.

The contract is intended to evolve as additional independent implementations and real interoperability runs are exercised.

---

## 2. Normative boundary

The interoperability contract has three layers:

1. **EABC normative semantics** — the meaning that implementations MUST preserve.
2. **Interoperability representation** — the minimum shared fields and mappings needed for independent consumers to correlate and interpret evidence.
3. **Implementation mapping** — implementation-specific names, encodings, journal structures, or other mechanisms used to satisfy the shared semantics.

An implementation MAY use different internal names or mechanisms provided that its published mapping preserves the required EABC semantics and evidence relationships.

The interoperability contract MUST NOT require two implementations to share an internal architecture, policy language, transport, storage format, cryptographic primitive, or journal implementation unless explicitly defined by a future profile or interoperability version.

---

## 3. Authority epoch and execution epoch

### 3.1 Authority epoch

**Authority epoch** identifies the governance/authority state against which an authorization decision was evaluated.

An interoperability record carrying an authorization decision SHOULD expose the authority epoch used for that decision.

Where the implementation supports revocation or other authority-state transitions, the authority epoch is part of the evidence needed to establish which authority state applied at commit time.

### 3.2 Execution epoch

**Execution epoch** identifies an execution-side or runtime state where such a concept exists.

Execution epoch and authority epoch MUST NOT be treated as interchangeable merely because an implementation happens to use the same value for both.

An implementation MAY omit execution epoch where no such execution-side concept exists.

### 3.3 Interoperability mapping

For the currently validated implementation pair, the implementation-side `epoch` field maps to **authority epoch**.

This mapping is an implementation mapping, not a requirement that every implementation name the field `epoch`.

---

## 4. Authorization decision mapping

EABC authorization outcomes are defined in [003]:

- `ALLOW`
- `DENY`
- `EXPIRED`
- `CANCELLED`
- `UNKNOWN`

An interoperating implementation MAY use different local terminology, but the mapping to the EABC semantic outcome MUST be explicit.

### 4.1 Known implementation mapping

The currently validated implementation pair uses:

| EABC semantic outcome | Implementation-side outcome |
|---|---|
| `ALLOW` | `ALLOW` |
| `DENY` | `BLOCK` |
| `EXPIRED` | not yet validated |
| `CANCELLED` | not yet validated |
| `UNKNOWN` | not yet validated |

The mapping `DENY ↔ BLOCK` is therefore recorded as a **known implementation mapping**, not as a replacement of the EABC normative term `DENY`.

A future implementation MAY use another local term, provided its mapping is published and unambiguous.

---

## 5. Reason representation

Where an implementation exposes a `reason` field, the field MUST have deterministic semantics for interoperability.

For the currently validated implementation pair:

- authorization allowed without a denial/block reason: `reason = ""`;
- authorization blocked: `reason` contains the explicit implementation reason, for example `REVOKED`.

The empty-string convention is recorded as an **observed interoperability convention** from the real run. It is not currently imposed as a universal EABC requirement on all implementations.

If a future interoperability version requires a canonical wire representation for `reason`, that requirement MUST be established independently of any one implementation.

A consumer MUST NOT infer a successful authorization solely from omission of a `reason` field.

---

## 6. Execution outcome mapping

EABC execution outcomes are defined in [003]:

- `ATTEMPTED`
- `COMMITTED`
- `FAILED`
- `ABORTED`
- `UNKNOWN`

Authorization outcome and execution outcome are separate dimensions.

An implementation MUST preserve enough information for an independent consumer to determine, where evidence permits:

1. whether execution was authorized;
2. whether execution was attempted;
3. whether an external state transition was committed;
4. whether execution failed or was aborted;
5. whether the outcome is unknown because evidence is insufficient.

An authorization decision of `ALLOW` MUST NOT by itself be interpreted as evidence that an external effect was committed.

Likewise, `DENY` (or an implementation mapping such as `BLOCK`) MUST NOT be represented as a successful execution merely because a command was received or evaluated.

---

## 7. Correlation minimum

Independent implementations MUST expose sufficient stable information to correlate authorization, command, and execution evidence without relying on an untrusted external mapping.

For an interoperable execution record, the minimum correlation set is:

| Element | Purpose |
|---|---|
| `command_id` | identifies the command/decision lifecycle |
| `env_id` | identifies the execution environment or governed target context |
| action/payload digest | binds the decision to the exact command bytes |
| authority epoch | identifies the authority state evaluated |
| authorization decision | identifies the authorization result |
| reason, where applicable | explains a non-allow result |
| execution outcome | identifies the observed execution result |

Where applicable, implementations SHOULD additionally expose execution epoch, commit sequence, target, state, timestamps, and integrity references.

The action/payload digest MUST be computed over the exact bytes whose execution is governed. A consumer MUST be able to establish that the digest used for authorization corresponds to the payload presented for execution.

Correlation identifiers and references that establish these relationships MUST themselves be covered by the applicable integrity protection, consistent with [002].

An external index, database join, filename convention, or side-channel mapping that is not itself integrity-protected MUST NOT be the sole basis for establishing the correlation required by EABC.

---

## 8. Integrity mechanism neutrality

EABC interoperability requires verifiable integrity, but does not prescribe one implementation mechanism.

An implementation MAY use:

- hash chains;
- signed records;
- authenticated envelopes;
- append-only journals;
- hardware-backed evidence;
- or another mechanism satisfying the applicable EABC evidence requirements.

The currently validated implementation pair uses journal fields including:

- `seq`;
- `prev_hash`;
- `entry_hash`.

These fields are an implementation-specific integrity mechanism. They are **not EABC interoperability requirements**.

The important interoperability property is that an independent consumer can verify the relevant evidence and its correlation without trusting an opaque implementation-side mapping.

---

## 9. Commit-time semantics

Interoperability MUST preserve the distinction between authorization evaluation and externally effective commit.

The authority state used for the final authorization decision MUST be identifiable in the evidence.

Where an authority state changes between preparation and submission, the implementation MUST expose an outcome that allows the consumer to distinguish the stale or otherwise invalid authorization from a successful commit.

For the currently validated implementation pair, the observed sequence was:

1. command payload digest: `22055b0016c31920d3ddb38d01edb288b3c5da8592cd3a4b79d1967822483fc9`;
2. authority epoch `4`: `ALLOW`;
3. authority epoch advances to `5`;
4. the same payload is evaluated again;
5. implementation result: `BLOCK`, reason `REVOKED`;
6. the payload digest remains unchanged.

This demonstrates that authorization is a property of the command **in its authority context**, not a property of the payload digest alone.

---

## 10. Known implementation mapping

This section is intentionally extensible.

| Semantic element | Current implementation mapping | Status |
|---|---|---|
| EABC `DENY` | `BLOCK` | validated |
| EABC authority epoch | implementation `epoch` | validated |
| EABC action digest | implementation `payload_digest` | validated |
| EABC command identifier | `command_id` | validated |
| No authorization reason | `reason = ""` | observed |
| Integrity evidence | `seq/prev_hash/entry_hash` journal | observed implementation mechanism |
| EABC execution outcomes | implementation-specific mapping | not yet fully validated |

New mappings SHOULD be added here rather than changing EABC core terminology merely to match one implementation.

---

## 11. Real interoperability evidence

The first validation run produced two journal entries for the same payload digest:

- sequence 1: authority epoch `4`, decision `ALLOW`;
- sequence 2: authority epoch `5`, decision `BLOCK`, reason `REVOKED`;
- sequence 2 references the hash of sequence 1;
- both entries carry the same payload digest.

The two entries were independently recomputed and the recorded entry hashes were verified.

This evidence is included as a validation example only. It does not establish that these exact field names, journal structures, or serialization rules are mandatory for EABC implementations generally.

---

## 12. Conformance and evolution

This document is **Draft v0.1 / provisional**.

Its current validation basis is:

- one implementation pair;
- one real interoperability run;
- authorization states observed in that run;
- independently verified integrity and correlation fields.

Before promotion to a stable interoperability version, the contract SHOULD be exercised against:

- at least one additional independent implementation;
- additional failure modes;
- `EXPIRED`;
- `CANCELLED`;
- `UNKNOWN`;
- execution failure and aborted execution;
- missing or incomplete evidence;
- payload substitution or digest mismatch;
- authority-state change between preparation and commit.

Findings from those runs SHOULD update the interoperability contract through explicit revisions rather than silently changing the meaning of existing EABC properties.

---

## 13. Relationship to EABC core documents

This document depends on and complements:

- [001 — Execution Authority Properties](001%20%E2%80%93%20Execution%20Authority%20Properties.md)
- [002 — Evidence Model](002-evidence-model.md)
- [003 — Failure Semantics](003-failure-semantics.md)
- [004 — Conformance](004-conformance.md)

The division of responsibility is:

**EABC core** defines what must be true.  
**Interoperability Contract** defines what independent implementations must expose or map so that the truth can be independently correlated.  
**Implementation mapping** defines how a particular implementation names and represents those semantics.

No implementation-specific mapping in this document overrides a normative EABC property.

---

## 14. Future work

Future revisions may define:

- a canonical machine-readable interoperability schema;
- version negotiation;
- canonical serialization requirements where interoperability requires them;
- additional implementation mappings;
- profile-specific interoperability requirements;
- conformance test vectors;
- multiple real-run validation cases.

Until then, implementations SHOULD prefer explicit published mappings over implicit assumptions.
