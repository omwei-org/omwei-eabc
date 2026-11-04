# Execution Authority Boundary Contract (EABC)

# 002 – Evidence Model

## Purpose

This document defines the evidence model used by the Execution Authority Boundary Contract (EABC).

EABC does not require any specific data format, serialization, protocol, storage mechanism, or cryptographic construction. It defines the minimum evidence required for an independent consumer to evaluate the original P1–P10 obligations and the five boundary semantic properties defined in **001 – Execution Authority Properties**.

Evidence categories, evidence dimensions, and normative properties are distinct concepts. An evidence dimension supports an assessment; it is not a separate EABC semantic property.

---

# Evidence Principles

Execution-authority evidence MUST satisfy the following principles.

## Verifiable

Evidence MUST allow an independent consumer to verify the claimed execution-authority properties and the specific P1–P10 obligations being assessed.

## Correlatable

Evidence generated at different stages of the authorization and execution lifecycle MUST be linkable through stable identifiers.

## Tamper Evident

Consumers MUST be able to detect whether evidence has been modified after creation.

## Complete

Required evidence MUST be sufficient to reconstruct the execution-authority decision and evaluate the declared property scopes without relying on implementation-specific knowledge.

## Portable

Evidence SHOULD remain meaningful outside the implementation that produced it.

## Intrinsically Bound

Any identifier that correlates one piece of evidence to another — in particular, an identifier linking Execution Evidence back to the Decision or Identity Evidence that authorized it — MUST be covered by the same Integrity Evidence that protects the artifact in which it appears.

Correlation MUST NOT depend on an external mapping, index, or side channel that is not itself integrity-protected as part of the evidence artifact it correlates. An independent consumer MUST be able to verify provenance directly from the evidence artifact, without relying on a separately maintained and separately trusted correlation record.

Correlation without intrinsic integrity protection describes a relationship but does not prove it. This principle supports P7 and MUST NOT be treated as a substitute for any of the five boundary semantic properties.

---

# Evidence Categories

EABC groups evidence into logical categories rather than prescribing concrete fields.

## 1. Identity Evidence

Identifies the entities participating in the execution-authority process.

Examples include:

- execution authority identity;
- execution target identity;
- workload identity;
- delegated authority identity;
- trust-domain identity;
- identity of the entity or process entitled to establish, amend, or revoke execution authority.

## 2. Decision Evidence

Describes the authorization decision itself.

Typical evidence includes:

- authorization outcome;
- policy evaluation result;
- decision identifier;
- decision timestamp;
- authorization scope;
- Protected Effect and intended reference state or condition;
- the relationship or transition conditions expressly bound to the authorization decision where P5 requires them.

## 3. Context Evidence

Describes the context under which authorization was evaluated.

Examples include:

- execution context;
- initiating entity and target identity;
- resource identifiers;
- requested action and effect-specific parameters;
- execution constraints;
- validity interval;
- environmental conditions;
- authoritative source designation and provenance for context elements;
- derivation, transformation, aggregation, or relay history where applicable.

Context evidence MUST permit assessment of the authenticity and provenance of relevant context elements and the binding among context C, boundary B, and Protected Effect E. Source authenticity or provenance alone does not establish factual truth or correctness.

## 4. State Evidence

Captures the runtime state against which boundary B made its determination for E.

Typical examples include:

- operational state of B;
- current condition of the governed system or target where read or relied upon by B;
- policy version;
- configuration version;
- delegated-authority version;
- decision-record hash;
- state hash;
- representation or reference identifying the state evaluated and binding it to the determination.

State Evidence MUST permit an assessor to distinguish the state actually used for the determination from state merely reported after the determination. Authenticity does not, by itself, establish freshness.

## 5. Commit Evidence

Represents the transition from authorization and determination to commit and effect.

Consumers SHOULD be able to determine:

- whether execution was authorized;
- whether the required authority and commit conditions were established;
- whether execution was attempted;
- whether COMMIT occurred;
- whether the associated EFFECT occurred;
- whether the required check-to-effect atomicity was maintained;
- whether a revocation, state change, or other condition invalidated the determination before the effect.

Commit Evidence MUST preserve the distinction between an authorization/commit transition and the subsequent external effect where they are separate stages.

## 6. Execution Evidence

Evidence produced by the execution domain.

Examples include:

- execution identifier;
- execution timestamp;
- execution result;
- execution status;
- effect identifier or effect observation;
- failure reason;
- a correlation reference to the Decision Evidence that authorized the execution.

Execution Evidence MUST carry a correlation reference to its originating Decision Evidence, and that reference MUST fall within the scope of the Integrity Evidence protecting the Execution Evidence artifact. An Execution Evidence artifact whose correlation reference is not itself integrity-protected does not satisfy this category.

Where P5 requires consumer-facing execution-state correspondence, evidence MUST permit the consumer to compare the state or condition applicable when the effect occurred against the intended reference and the relationship or permitted transition expressly bound to the authorization decision. This correspondence evidence is distinct from evidence of the authenticity and determination-binding of the state evaluated by B.

## 7. Correlation Evidence

Allows independent reconstruction of the complete execution-authority chain.

Typical correlation artifacts include:

- lifecycle identifier;
- correlation identifier;
- parent reference;
- sequence identifier;
- transaction identifier;
- references binding the authorization decision, boundary determination, commit, and associated effect.

Correlation Evidence is not a standalone category that may be provided separately from the evidence it correlates. Where a correlation identifier references another piece of evidence — most importantly, where it binds Execution Evidence back to the Decision Evidence that authorized it — that identifier MUST be embedded within, and covered by, the Integrity Evidence of the artifact carrying it. A correlation mapping maintained outside the evidence artifacts themselves and not covered by the same integrity mechanism does not satisfy this requirement.

## 8. Integrity Evidence

Demonstrates that evidence has not been modified.

Possible mechanisms include:

- digital signatures;
- integrity hashes;
- authenticated logs;
- immutable event chains.

EABC does not mandate any specific integrity mechanism. Where Integrity Evidence protects an artifact that also carries a Correlation Evidence reference, that reference MUST be within the scope of what is protected. A signature or hash that omits the correlation reference does not satisfy P7 for that artifact.

---

# Evidence Dimensions for Boundary Semantic Properties

The following dimensions are necessary evidence subjects for assessing the five boundary semantic properties. They do not create additional properties.

## 1. NON_BYPASSABILITY(B,E)

A `NON_BYPASSABILITY(B,E)` claim requires both:

### Deployment-topology completeness

Evidence MUST identify the Protected Effect Scope, Boundary Scope, and Path Scope, and establish the method used to enumerate and assess the in-scope paths capable of producing E. It MUST provide a defensible basis for concluding that relevant paths have not been omitted.

A list of known paths without a completeness method does not establish topology completeness.

### Boundary mediation

Evidence MUST establish, for each identified in-scope path capable of producing E, that the path is mediated by B and cannot produce E without the required mediation.

Evidence that B mediates the known paths does not establish that the path inventory is complete.

Both dimensions are necessary. They support one semantic property and MUST NOT be assigned separate EABC property identifiers. Neither dimension alone supports a complete `NON_BYPASSABILITY` claim.

The applicable `ENFORCEMENT_INDEPENDENCE` qualification is recorded separately as an EBP assurance constraint. It is not evidence of topology completeness or a substitute for boundary mediation.

## 2. INTEGRITY_DEF(B)

Evidence MUST permit an assessor to determine:

- the authoritative origin of the applicable boundary definition;
- the identity, scope, and enforcement-relevant content of that definition;
- its authenticity;
- that it is protected against unauthorized modification or substitution under the accepted prevention guarantee and declared threat model;
- that the boundary instance making the COMMIT(E) or REJECT(E) determination is bound to that applicable definition;
- that the threat model is bound to the definition scope and the assessed boundary instance.

Evidence of an authentic stored artifact alone does not establish that the artifact is the definition applicable to the deciding boundary instance.

## 3. INTEGRITY_STATE(B,E)

Evidence MUST permit an assessor to determine:

- which runtime state was relevant to E;
- that the state used by B was authentic and integrity-protected against unauthorized alteration, substitution, or misrepresentation;
- that the evaluated state was bound to the actual COMMIT(E) or REJECT(E) determination;
- that the state was not merely reported after the determination;
- where multiple state elements were used, that they belong to the state evaluation associated with that determination.

The consumer-facing P5 execution-state correspondence obligation is separately applicable. Evidence MUST identify the intended reference state or condition and the relationship or permitted transition expressly bound to the authorization decision, and permit a consumer to determine whether the state or condition at effect corresponded to that reference under the declared semantics.

Evidence establishing `INTEGRITY_STATE(B,E)` does not, by itself, establish execution-state correspondence. Evidence establishing correspondence does not, by itself, establish state authenticity and determination-binding. Freshness remains separate from state authenticity.

## 4. INTEGRITY_CTX(C,B,E)

Evidence MUST permit an assessor to determine:

- the context C applicable to the determination;
- the authoritative source or sources for each relevant context element;
- provenance and relevant transformations for derived, transformed, aggregated, or relayed context;
- authenticity and integrity of context elements from authoritative source or defined derivation through their use by B;
- authenticity and integrity of the binding among C, B, and E;
- that the binding was established no later than the determination and remained valid through the associated effect, invalidation, or abandonment;
- that unauthorized context changes, substitution, or misattribution invalidate the binding and require a new determination or expressly authorized revalidation and rebinding before the effect relies on the changed context.

Provenance establishes source and integrity of a context assertion; it does not by itself establish factual truth or correctness. `INTEGRITY_CTX(C,B,E)` does not establish P3 check-to-effect atomicity.

## 5. EXCLUSIVITY(A,E,I)

Evidence MUST permit an assessor to determine:

- the Protected Effect Scope and Authority Interval I;
- the reference Commit Authority A and the basis for its designation;
- the entities whose determination is, or could be, operative for E over I;
- the method used to establish that candidate inventory is complete;
- the conditioning relationships among A's determination and each candidate A′;
- whether any candidate satisfies the Parallel Commit Authority definition.

Candidate inventory without a stated completeness method does not support the claim. Inclusion in the inventory does not by itself establish that an entity is a Commit Authority.

---

# Evidence Requirements and P1–P10 Reconciliation

For every normative requirement, implementations MUST provide sufficient evidence to demonstrate compliance. Evidence MAY be reused only where it independently establishes each requirement's normative meaning.

| Requirement | Required evidence subjects |
|---|---|
| P1 — Authority-Origin Independence, anti-self-authorization, and unauthorized modification | Identity + authority provenance + authority-state/change records + Integrity |
| P2 — Complete Mediation | Decision + Commit + Correlation, together with complete path inventory and mediation evidence for the boundary-level NON_BYPASSABILITY assessment |
| P3 — Deterministic Commit Semantics | Decision + Commit + Execution + evidence of check-to-effect atomicity |
| P4 — Context Binding | Context + evidence of applicable authority/context scope |
| P5 — State Binding | State + determination binding + independent consumer-facing intended-state correspondence evidence |
| P6 — Evidence Integrity | Integrity |
| P7 — Evidence Correlation | Correlation intrinsically bound within Integrity Evidence |
| P8 — Failure Semantics | Execution + Decision + explicit failure/missing-evidence disposition |
| P9 — Implementation Neutrality | Observable property and evidence mapping; no mechanism-specific assumption as a substitute for a property |
| P10 — Extensible Profiles | EABC Implementation Profile mapping, with profile type and scope identified |
| `NON_BYPASSABILITY(B,E)` | Deployment-topology completeness + boundary mediation |
| `INTEGRITY_DEF(B)` | Definition origin/authenticity/content + declared threat model + boundary-instance binding |
| `INTEGRITY_STATE(B,E)` | Runtime-state authenticity/integrity + determination binding; P5 correspondence remains separate |
| `INTEGRITY_CTX(C,B,E)` | Context-element provenance/authenticity + context/boundary/effect binding and lifecycle continuity |
| `EXCLUSIVITY(A,E,I)` | Reference authority + complete candidate inventory + conditioning relationships |

The evidence dimensions for `NON_BYPASSABILITY` MUST NOT be treated as two semantic properties. P6 and P7 MUST remain distinct from the five boundary semantic properties. A boundary property does not automatically establish P6 or P7, and P6 or P7 evidence does not automatically establish a boundary semantic property.

---

# Missing Evidence

Missing evidence SHALL NOT be interpreted as successful execution.

Consumers SHOULD distinguish between:

- evidence unavailable;
- evidence incomplete;
- evidence unverifiable;
- evidence inconsistent.

An Execution Evidence artifact that lacks an intrinsically bound correlation reference to its Decision Evidence SHOULD be treated as evidence incomplete, not as an implicit authorization.

Where missing or insufficient evidence concerns an explicitly required condition for a protected transition, that condition SHALL NOT be treated as established. This evidence rule does not redefine the general UNKNOWN outcome in 003 — Failure and Execution Semantics.

The interpretation of missing evidence is implementation-independent.

---

# Optional Evidence

Implementations MAY expose additional evidence beyond the EABC minimum.

Examples include:

- telemetry;
- runtime measurements;
- hardware attestation;
- policy explanations;
- execution metrics;
- formal verification artifacts.

Such evidence MUST NOT alter the meaning of the normative EABC properties or original P1–P10 obligations.

---

# Evidence Consumption

Consumers SHOULD evaluate evidence independently of the implementation that generated it.

A consumer SHOULD be capable of determining:

- what was authorized;
- under which authority;
- against which state authorization was evaluated;
- which intended reference state or condition was bound to the authorization decision;
- within which context;
- which boundary made the determination;
- whether all relevant paths capable of producing the Protected Effect are within the declared and assessed path universe;
- whether each identified path is mediated by the boundary;
- whether a Parallel Commit Authority exists for the same effect, scope, and Authority Interval;
- whether execution and the associated effect occurred;
- whether execution corresponded to the intended state under the applicable authorization and execution semantics;
- whether evidence remains trustworthy;
- whether execution evidence can be verifiably traced back to the authorization that permitted it.

No implementation-specific interpretation should be required to answer these questions. In particular, the correlation question MUST be answerable from the evidence artifacts and their integrity protection, without consulting a separately trusted correlation source.

---

# Relationship to Implementation Profiles

EABC Implementation Profiles define how concrete architectures generate evidence satisfying the EABC evidence model and demonstrate the P1–P10 obligations and five boundary semantic properties.

Different implementations may expose different artifacts while remaining fully conformant, provided they demonstrate the required evidence categories and dimensions, satisfy the normative execution-authority properties, and satisfy the intrinsic-binding requirement for any correlation reference between authorization and execution evidence.

An EABC Implementation Profile MUST NOT redefine the normative requirements. An EAP Profile is a distinct profile type and MUST NOT be treated as interchangeable with an EABC Implementation Profile.
