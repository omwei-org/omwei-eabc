# 006 — Execution Boundary Profile (EBP)

**Status:** Draft v0.1 (design-notes promoted to normative-style prose; not yet cross-reviewed against `docs/002` and `docs/004`for terminology drift)

## 0. Purpose and Scope

This document defines the **Execution Boundary Profile (EBP)**, an extension layer on top of EABC Core (`docs/000`–`005`) that addresses one question Core deliberately leaves open: *which implementation substrate (software, hardware, or a composite of the two) is permitted to realize a given execution boundary, and how is that permission established and kept current?*

EBP does **not** decide substrate. Deciding SW vs. HW placement at the level of the contract itself would violate Core's Implementation Neutrality principle (`docs/001`, Property 9) and would introduce a runtime decision point structurally analogous to a TLS-downgrade vulnerability — a place where an adversary can push the system toward the weaker-but-still-"conformant" option. EBP instead states only the **properties** an execution boundary must satisfy for a given protected effect. Which concrete implementation — software-only, hardware-only, or composite — satisfies those properties is answered by **conformance assessment**, not by the contract.

> **Core principle:** EABC determines the properties an execution boundary must satisfy for a given protected effect; conformance assessment determines which implementation (software, hardware, or composite) satisfies them. A hardware requirement is therefore always a *consequence* of conformance assessment against stated properties, never a normative choice made by EABC itself.

## 1. Relationship to EABC Core

EBP is additive. It introduces one new contract section within `ExecutionBoundaryContract` and one new semantic plane (the *conformance plane*), and otherwise reuses or extends Core mechanisms rather than duplicating them. Everything Core already defines about per-commit authority and evidence (`docs/001`–`003`) continues to apply unchanged to any implementation that adopts EBP.

The full Core ↔ EBP crosswalk (13 elements) is normative and given in §7.

## 2. Required Boundary Properties

`ExecutionBoundaryContract` extends the existing per-commit contract sections (Authority Conditions, Boundary Conditions, Commit Conditions — see `docs/001`, `docs/003`) with a fourth, structurally different section:

**REQUIRED BOUNDARY PROPERTIES** — a static, instance-scoped set of properties that a candidate implementation must satisfy before it is eligible to serve any commit under this contract. Unlike Authority/Boundary/Commit Conditions, which are evaluated per-commit, Required Boundary Properties are evaluated once per implementation instance via conformance assessment (§3), not on every transaction.

The initial property set:

- **Independence** — the boundary's admit/refuse decision is not controllable by the party whose action is being evaluated.
- **Exclusivity** — no path to the protected effect exists that bypasses this boundary.
- **Non-bypass** — same as Exclusivity, stated as a negative requirement on the deployment topology rather than a positive requirement on the boundary itself; kept as a distinct named property because the two are demonstrated by different evidence (topology audit vs. boundary behavior).
- **Physical non-extractability** — where the boundary's own state or keys are the thing being protected, they cannot be extracted or replayed at the layer being assessed.
- **Isolation** — the boundary's execution is not observable-or-influenceable by co-located, non-boundary processes.
- **Renderer integrity** — where the boundary emits evidence or a claim-set for consumption by another system, the emitting logic itself has not been altered from its assessed form.

**Classification test** (for any future candidate property): if satisfying it depends on instance identity, configuration, measurement, or isolation state, it is a Required Boundary Property. If it is a per-commit dynamic predicate (e.g., exact-action binding, schema validity of the request itself), it stays in Core's Authority/Boundary Conditions and does not belong here.

## 3. Conformance Lifecycle

EBP separates three events that are easy to conflate but must not be merged:

1. **Assessment** — a static determination: does implementation instance *i* satisfy the Required Boundary Properties of contract *c*? Performed once (or on each material change to *i*), not per-commit.
2. **Attestation** — the evidence artifact that carries the claim that Assessment succeeded (see §4).
3. **Validity** — whether that Attestation is *currently* acceptable. This can be a runtime question (revocation, expiry, staleness) even though Assessment itself is not.

### 3.1 Locked formulas

```
CONFORMANCE_ELIGIBLE(i, c, t) :=
    ACCEPTABLE_CONFORMANCE_EVIDENCE(i, c, t)
    ∧ CONFORMANCE_VALIDITY_POLICY_SATISFIED(i, c, t)

VALID_COMMIT(a, i, c, t) :=
    CONFORMANCE_ELIGIBLE(i, c, t)
    ∧ FINAL_AUTHORITY_CHECK(a, c, t)
    ∧ COMMIT_CONDITIONS(a, c, t)

```

These are **three parallel gates** and MUST NOT be merged into one another. In particular, `FINAL_AUTHORITY_CHECK`(Core, `docs/003`) keeps its existing scope — authority validity only. It MUST NOT be extended to also carry conformance-status logic; conformance is evaluated as an independent precondition to `VALID_COMMIT`, not as an additional clause inside `FINAL_AUTHORITY_CHECK`'s own checklist.

### 3.2 Conformance Validity Precondition (locked invariant)

Conformance status is tri-state: `VALID | INVALID | INDETERMINATE`.

For the purposes of `VALID_COMMIT`, **`INDETERMINATE` is treated as `INVALID`** — it is never a third acceptable outcome. Deployment or availability policy MUST NOT redefine `INDETERMINATE` as `VALID`; doing so would reopen a fail-open loophole this invariant exists to close.

Conformance status is the composition of three independent validity dimensions:

- **Temporal validity** (is the attestation within its stated validity window)
- **Status / revocation** (has the attestation been revoked)
- **Instance / state freshness** (does the attestation still describe the instance as it currently is)

Composition rule — **most-restrictive-wins**, not averaging:

```
CONFORMANCE_STATUS :=
    INVALID        if any dimension is INVALID
    INDETERMINATE  else if any dimension is INDETERMINATE
    VALID          otherwise

```

This mirrors the same shape used elsewhere in the architecture for POISON-overrides-VALID composition (see `[[sif-slc-architecture]]`'s Fabric Shadow Domain).

### 3.3 Availability is explicitly out of scope for semantics

A deployment MAY use caching, redundancy, or staged rollout to reduce how often `INDETERMINATE` is observed in practice. It MUST NOT use these mechanisms to change what `INDETERMINATE` *means*. This document does not resolve the pre-existing Exclusivity-vs-Availability ("blast radius") tension tracked in `[[sif-slc-architecture]]`; EBP states the requirement, availability engineering remains a deployment/SIF concern.

## 4. Conformance Attestation

EBP introduces **no new cryptographic or attestation primitive**. Conformance Attestation is defined as an **EAT-based EABC Conformance Attestation Profile**: it reuses IETF EAT (RFC 9711, RATS WG) as the base entity/state claim-set format, and layers EBP-specific claims on top:

- `contract_ref` — identifies the `ExecutionBoundaryContract` this attestation is claiming conformance against
- `required_boundary_properties` — the property set (§2) being claimed
- `status` — the tri-state value from §3.2, as claimed by the attesting party (subject to independent Validity evaluation by the relying party — a claimed `VALID` is not authoritative on its own)

This choice is consistent with the already-locked layer stack for the broader architecture: Hardware root → Attestation (TRACE) → Identity/governance layer → EABC execution-authority boundary. EAT was already flagged as a candidate composable input during prior-art research (see `[[omwei-eabc]]`'s prior-art section); this document is the first place it is adopted normatively.

### 4.1 Freshness, temporal validity, and revocation are independent

These three are independent dimensions and MUST be evidenced independently (same discipline as Core's `authority_epoch` / `STALE_EPOCH` distinction, `docs/005`). In particular:

- `valid_until` alone does not prove that the *currently running* instance is the one that was attested. A binding mechanism between attestation and running instance is required wherever instance identity is structurally load-bearing for a claimed property — but EBP does not mandate *which* binding mechanism (static/deployment-time, challenge-response, or continuously-maintained trusted state); that choice is implementation/profile-dependent.
- **Fresh Attestation ≠ Non-bypass.** A freshly and validly attested instance can still sit behind a bypassable deployment topology. These are separate properties (§2) and require separate evidence; neither substitutes for the other.
- **Implementation Identity ≠ Execution Boundary Exclusivity.** Knowing precisely which software/hardware is running (identity) does not by itself establish that no other path to the effect exists (exclusivity). Kept as separate properties for the same reason.

## 5. Conformance Evidence (a new, instance-scoped evidence class)

Core (`docs/002`) defines eight evidence categories, all **transaction-scoped**: Identity, Decision, Context, State, Commit, Execution, Correlation, Integrity.

**Conformance Evidence is instance-scoped**, not transaction-scoped, and is therefore **not** folded in as a ninth member of that list. It is a separate evidence class, parallel to Core's eight, introduced specifically by EBP.

### 5.1 Boundary Evidence Binding (new invariant, classified EXTEND)

Core's Evidence Correlation category already establishes the "Intrinsically Bound" principle (`docs/002`): *correlation without intrinsic integrity protection describes a relationship, but does not prove it.*

EBP extends this principle directly: any reference from transaction-scoped Execution or Commit Evidence to instance-scoped Conformance Evidence must itself be **intrinsically bound** — a bare pointer or label referencing a conformance record is not sufficient; the binding must carry its own integrity protection, exactly as Core already requires for correlation between transaction-scoped evidence categories.

This is classified as an **extension** of an existing Core mechanism, not a new one.

### 5.2 Missing-evidence handling (mirrors Core exactly)

Core already states that missing evidence must never be interpreted as successful execution. EBP states the direct analogue:

> Missing or indeterminate Conformance Evidence SHALL NOT be interpreted as VALID conformance.

## 6. Two previously-undefined nodes, resolved

- **Execution Boundary Policy** — external, customer- or deployment-supplied input specifying which Required Boundary Properties apply to a given deployment. This is explicitly **not** an EABC/EBP primitive; it is an external input that feeds the Contract from outside the object tree defined by this document.
- **Boundary Binding** — the deployment/configuration-time act of associating a specific implementation instance with a specific `ExecutionBoundaryContract`, establishing that instance's `boundary_id`. Boundary Binding is a distinct event from `FINAL_AUTHORITY_CHECK`'s runtime admission decision and from `COMMIT` itself:

```
BIND  ≠  ADMIT  ≠  COMMIT

```

(`ADMIT` here denotes `FINAL_AUTHORITY_CHECK`'s runtime outcome, per Core.) No new runtime state named `ADMITTED` is introduced by this document.

## 7. Locked Core ↔ EBP Crosswalk (normative, 13 elements)

| #ElementClassification |                                                                 |                                                                   |
| ---------------------- | --------------------------------------------------------------- | ----------------------------------------------------------------- |
| 1                      | Required Boundary Properties                                    | NEW                                                               |
| 2                      | Boundary Binding                                                | NEW                                                               |
| 3                      | Conformance Assessment                                          | NEW                                                               |
| 4                      | Conformance Evidence (as a class)                               | NEW                                                               |
| 5                      | Conformance Status / tri-state gate                             | NEW                                                               |
| 6                      | Boundary Evidence Binding                                       | EXTEND (reuses Core's Evidence Correlation / Intrinsically Bound) |
| 7                      | Authority Conditions                                            | REUSE                                                             |
| 8                      | Boundary Conditions                                             | REUSE                                                             |
| 9                      | Commit Conditions                                               | REUSE                                                             |
| 10                     | `FINAL_AUTHORITY_CHECK` (scope narrowed to exclude conformance) | REUSE                                                             |
| 11                     | `COMMIT`                                                        | REUSE                                                             |
| 12                     | `EFFECT`                                                        | REUSE                                                             |
| 13                     | `ExecutionBoundaryContract`'s per-commit sections generally     | REUSE                                                             |
| —                      | `ExecutionBoundaryPolicy`                                       | EXTERNAL INPUT (deliberately outside the EBP object tree)         |

Note on #7–#9: Boundary Conditions in particular reuse Core exactly as much as Authority and Commit Conditions do — `boundary_id matches` corresponds to Core's Context Binding property plus Context Evidence, and `target state current` corresponds to Core's State Binding property plus State Evidence. This is stated explicitly to remove an earlier, unjustified asymmetry under which Boundary Conditions had been informally treated as "more novel" than the other two per-commit condition sets.

This crosswalk confirms the document's overall thesis numerically: EBP adds one new contract section within `ExecutionBoundaryContract` (§2) plus one new semantic plane (the conformance plane, §3–§5), and reuses or extends Core everywhere else. (Earlier draft language described this as "one new top-level object" — corrected: §2 is a new *section of*the existing `ExecutionBoundaryContract` object, per §1's own framing, not a new top-level object in its own right.)

## 8. Open Items

- **§5 ↔ `docs/002` verification (not yet performed):** confirm that Core's Evidence Correlation category and its "Intrinsically Bound" principle carry exactly the normative force §5.1 attributes to them before treating Boundary Evidence Binding as a settled EXTEND. If `docs/002`'s actual language is narrower than assumed here, §5.1 needs to be re-scoped to match, not the other way around.
- **§7 ↔ `docs/002` + `docs/004` verification (not yet performed):** re-check the NEW/EXTEND/REUSE classification in the 13-element crosswalk against both documents directly, specifically to rule out any hidden duplication between EBP's conformance plane and Core's existing Property/Evidence/Profile conformance levels (`docs/004`). Until this is done, treat the crosswalk as internally consistent but not yet cross-validated against Core's actual text.
- Full clause-by-clause cross-check against `docs/002` (evidence model) and `docs/004` (conformance levels) has not yet been performed for this document specifically — the eight-vs-nine-category distinction in §5 was verified against actual repo content during drafting, but the interaction between EBP's conformance levels and Core's existing Property/Evidence/Profile conformance levels (`docs/004`) is not yet written up.
- No implementation profile yet references EBP (EGA/SIF v1, `profiles/ega-sif-v1.md`, predates this document).
- Binding mechanism for instance identity (§4.1) is deliberately left open; a future profile document may wish to recommend one without making it normative at the EBP level.