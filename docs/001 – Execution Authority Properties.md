# Execution Authority Boundary Contract (EABC)

# 001 – Execution Authority Properties

## Purpose

This document defines the normative properties required of any system claiming conformance with the Execution Authority Boundary Contract (EABC).

These properties describe **architectural guarantees**, not implementation details.

Implementations are free to choose their internal architecture provided they can demonstrate the required properties using verifiable evidence.

---

## Relationship to the Execution Authority Whitepaper

EABC is not a freestanding property list. It operationalizes two distinct layers of the *Execution Authority* research whitepaper:

* the **five necessary properties of an Execution Authority** established in the whitepaper's theoretical foundation (Independence, Complete Mediation, Commit Control, Determinism, State/Context Binding) — referenced in the whitepaper's Section 12.1 as the properties "defined in Chapter 1";
* the **operationalization layer** of the whitepaper (Sections 8–11: the Authorization Artifact, the Execution Attestation, the Verification Model, and the Assurance Registry), which introduces evidentiary and lifecycle requirements not present in the theoretical layer itself.

Properties 1–5 below correspond directly to the whitepaper's five necessary properties. Properties 6–9 operationalize requirements that the whitepaper establishes structurally (through the ACT and EAtt artifacts and the verification model) but does not itself enumerate as named axioms. Property 10 is specific to EABC as a specification layer and has no whitepaper counterpart.

| EABC Property                     | Origin |
| ----------------------------------- | -------- |
| 1. Independent Execution Authority | Whitepaper Chapter 1 — Independence |
| 2. Complete Mediation               | Whitepaper Chapter 1 — Complete Mediation |
| 3. Deterministic Commit Semantics   | Whitepaper Chapter 1 — Determinism and Commit Control |
| 4. Context Binding                  | Whitepaper Chapter 1 — State/Context Binding (context component); operationalized via the ACT `context`/`constraints` fields (Section 8.3) |
| 5. State Binding                    | Whitepaper Chapter 1 — State/Context Binding (state component); operationalized via the ACT `validity` field and EAtt `execution_context` (Sections 8.3, 9.3) |
| 6. Evidence Integrity               | Operationalization layer — EAtt `integrity` field (Section 9.3) |
| 7. Evidence Correlation             | Operationalization layer — EAtt causal binding to ACT_hash (Section 9.4) |
| 8. Failure Semantics                | Operationalization layer — Verification Outcome (Section 10.5) and EAtt `result` field (Section 9.3) |
| 9. Implementation Neutrality        | Whitepaper Section 5.4 — Technology Neutrality |
| 10. Extensible Profiles             | EABC-specific; no whitepaper counterpart. Realizes the whitepaper's Section 12.4 expectation that a future Specification "resolve the questions this paper deliberately leaves open at the implementation level." |

This mapping is intended to keep EABC answerable to the whitepaper's invariants, consistent with the asymmetric relationship described in the whitepaper's Section 12.4: EABC is derived from and constrained by the whitepaper, while the whitepaper's validity does not depend on any particular choice made here.

---

# Property 1 — Independent Execution Authority

## Requirement

Execution authority MUST originate from a trust domain that is independent of the governed execution domain.

The governed system MUST NOT be capable of modifying, bypassing, or self-authorizing execution authority after authorization has been established.

## Rationale

A system cannot independently authorize actions that it is also free to modify.

Separation of execution authority establishes an independently verifiable trust boundary.

This property operationalizes the whitepaper's Independence axiom: ¬Control(A_D, EB) (Section 3.2.2).

## Evidence

An implementation SHOULD provide evidence demonstrating:

* authority origin
* trust-domain identity
* authority integrity
* authority authenticity

---

# Property 2 — Complete Mediation

## Requirement

Every externally committed action MUST pass through the execution-authority boundary.

No execution path capable of producing externally observable effects may bypass evaluation by the execution-authority system.

## Rationale

Partial mediation creates execution paths that cannot be governed.

The contract therefore assumes that every committed action is mediated.

This property operationalizes the whitepaper's Complete Mediation axiom (Section 3.2.1).

## Evidence

Implementations SHOULD demonstrate:

* mediation identifier
* decision correlation
* execution correlation
* audit continuity

---

# Property 3 — Deterministic Commit Semantics

## Requirement

The transition between authorization and execution MUST be explicitly represented.

The outcome of this transition MUST be deterministic.

## Rationale

Consumers must be able to distinguish:

* authorization granted
* authorization denied
* execution attempted
* execution committed
* execution failed

without ambiguity.

This property operationalizes the whitepaper's Determinism and Commit Control properties (Chapter 1), which govern the atomic validated-to-committed transition referenced in the EAtt `commit_event` field (Section 9.3).

## Evidence

Implementations SHOULD expose:

* commit decision
* execution outcome
* execution status
* failure reason

---

# Property 4 — Context Binding

## Requirement

Execution authority MUST be cryptographically or otherwise integrity-bound to the execution context for which it was issued.

Execution authority MUST NOT be reusable outside its intended scope.

## Rationale

Execution authority without context binding can be replayed or misapplied.

This property operationalizes the context component of the whitepaper's State/Context Binding property (Chapter 1), corresponding to the `constraints` and `context` fields of the Authorization Artifact (Section 8.3).

## Evidence

Examples include:

* workload identity
* target resource
* execution context
* validity interval
* execution constraints

---

# Property 5 — State Binding

## Requirement

Execution authority MUST identify the state against which authorization was evaluated.

Consumers MUST be able to determine whether execution occurred against the intended state.

## Rationale

Authorization decisions are meaningful only within the state in which they were evaluated.

This property operationalizes the state component of the whitepaper's State/Context Binding property (Chapter 1), corresponding to the `validity` field of the Authorization Artifact and the `execution_context` field of the Execution Attestation (Sections 8.3, 9.3).

## Evidence

Typical evidence includes:

* policy version
* configuration version
* delegated authority version
* decision-record hash
* state hash

---

# Property 6 — Evidence Integrity

## Requirement

Execution-authority evidence MUST be tamper evident.

Consumers MUST be able to determine whether evidence has been modified.

## Rationale

Execution authority depends on trustworthy evidence rather than trust in implementation.

This property operationalizes the `integrity` field of the whitepaper's Execution Attestation (Section 9.3); it belongs to the whitepaper's operationalization layer rather than to the Chapter 1 theoretical properties.

## Evidence

Examples include:

* digital signatures
* integrity hashes
* immutable audit records
* authenticated event chains

---

# Property 7 — Evidence Correlation

## Requirement

Evidence generated throughout authorization and execution MUST be correlatable.

Consumers MUST be able to reconstruct the execution-authority chain.

## Rationale

Independent verification requires continuity across architectural layers.

This property operationalizes the causal binding EAtt ⇒ (ACT + EA + CommitEvent) defined in the whitepaper (Section 9.4), and is a precondition for the Artefact Chain Integrity requirement discussed in the whitepaper's Section 12.1.

## Evidence

Typical correlation includes:

* lifecycle identifier
* correlation identifier
* execution identifier
* decision identifier

---

# Property 8 — Failure Semantics

## Requirement

Failure conditions MUST be explicitly represented.

Missing evidence SHALL NOT be interpreted as successful execution.

## Rationale

Consumers must distinguish between:

* denied
* failed
* cancelled
* expired
* unavailable
* unknown

This property operationalizes the `result` field of the Execution Attestation and the possible verification outcomes described in the whitepaper's Verification Model (Sections 9.3, 10.5); the whitepaper leaves the specific outcome vocabulary open, which EABC's companion document **003 – Failure and Execution Semantics** resolves.

## Evidence

Implementations SHOULD provide explicit terminal states.

---

# Property 9 — Implementation Neutrality

## Requirement

The execution-authority contract MUST describe observable properties rather than implementation mechanisms.

## Rationale

Multiple independent architectures should be capable of satisfying the same contract.

Conformance is determined by demonstrated properties, not implementation similarity.

This property operationalizes the whitepaper's Technology Neutrality principle (Section 5.4): required boundary strength is a function of protected consequences, not of implementation technology.

---

# Property 10 — Extensible Profiles

## Requirement

Concrete implementations SHALL define implementation profiles mapping their internal constructs to the EABC properties.

Implementation profiles MUST NOT redefine normative EABC properties.

## Rationale

The contract remains stable while implementations evolve independently.

This property has no direct whitepaper counterpart; it realizes, at the specification layer, the whitepaper's Section 12.4 expectation that concrete data formats, protocols, and implementation-level questions be resolved by a downstream Specification rather than by the theory itself.

---

# Summary

A conforming implementation demonstrates:

| Property                        | Required | Whitepaper Origin |
| --------------------------------- | ---------- | -------------------- |
| Independent Execution Authority  | MUST       | Chapter 1 — Independence |
| Complete Mediation                | MUST       | Chapter 1 — Complete Mediation |
| Deterministic Commit Semantics    | MUST       | Chapter 1 — Determinism / Commit Control |
| Context Binding                   | MUST       | Chapter 1 — State/Context Binding (context) |
| State Binding                     | MUST       | Chapter 1 — State/Context Binding (state) |
| Evidence Integrity                | MUST       | Operationalization layer — EAtt |
| Evidence Correlation              | MUST       | Operationalization layer — EAtt |
| Failure Semantics                 | MUST       | Operationalization layer — Verification Model |
| Implementation Neutrality         | MUST       | Section 5.4 — Technology Neutrality |
| Extensible Profiles               | MUST       | EABC-specific (Section 12.4 expectation) |

Conformance is determined by satisfying these architectural properties, regardless of implementation architecture. Where a property traces to the whitepaper's Chapter 1, conformance with that property is a conformance claim about the underlying theory, not only about this specification.
