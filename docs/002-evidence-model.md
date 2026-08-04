# Execution Authority Boundary Contract (EABC)

# 002 – Evidence Model

## Purpose

This document defines the evidence model used by the Execution Authority Boundary Contract (EABC).

EABC does not require any specific data format, serialization, protocol, or cryptographic mechanism.

Instead, it defines the minimum evidence required for an independent consumer to evaluate whether an execution-authority boundary satisfied the normative properties defined in **001 – Execution Authority Properties**.

---

# Evidence Principles

Execution-authority evidence MUST satisfy the following principles.

## Verifiable

Evidence MUST allow an independent consumer to verify the claimed execution-authority properties.

---

## Correlatable

Evidence generated at different stages of the authorization and execution lifecycle MUST be linkable through stable identifiers.

---

## Tamper Evident

Consumers MUST be able to detect whether evidence has been modified after creation.

---

## Complete

Required evidence MUST be sufficient to reconstruct the execution-authority decision without relying on implementation-specific knowledge.

---

## Portable

Evidence SHOULD remain meaningful outside the implementation that produced it.

---

## Intrinsically Bound

Any identifier that correlates one piece of evidence to another — in particular, an identifier linking Execution Evidence back to the Decision or Identity Evidence that authorized it — MUST be covered by the same Integrity Evidence that protects the artifact in which it appears.

Correlation MUST NOT depend on an external mapping, index, or side channel that is not itself integrity-protected as part of the evidence artifact it correlates. An independent consumer MUST be able to verify provenance directly from the evidence artifact, without relying on a separately maintained and separately trusted correlation record.

This principle exists specifically to close a gap that a correlation identifier alone does not: correlation without intrinsic integrity protection describes a relationship, but does not prove it.

---

# Evidence Categories

EABC groups evidence into logical categories rather than prescribing concrete fields.

---

## 1. Identity Evidence

Identifies the entities participating in the execution-authority process.

Examples include:

* execution authority identity
* execution target identity
* workload identity
* delegated authority identity
* trust-domain identity

---

## 2. Decision Evidence

Describes the authorization decision itself.

Typical evidence includes:

* authorization outcome
* policy evaluation result
* decision identifier
* decision timestamp
* authorization scope

---

## 3. Context Evidence

Describes the context under which authorization was evaluated.

Examples include:

* execution context
* resource identifiers
* execution constraints
* validity interval
* environmental conditions

---

## 4. State Evidence

Captures the state against which authorization occurred.

Typical examples include:

* policy version
* configuration version
* delegated authority version
* decision-record hash
* state hash

---

## 5. Commit Evidence

Represents the transition from authorization to execution.

Consumers should be able to determine:

* whether execution was authorized
* whether execution was attempted
* whether execution was committed
* whether execution completed successfully

---

## 6. Execution Evidence

Evidence produced by the execution domain.

Examples include:

* execution identifier
* execution timestamp
* execution result
* execution status
* failure reason
* a correlation reference to the Decision Evidence that authorized the execution (see Correlation Evidence, below)

Execution Evidence MUST carry a correlation reference to its originating Decision Evidence, and that reference MUST fall within the scope of the Integrity Evidence protecting the Execution Evidence artifact. An Execution Evidence artifact whose correlation reference is not itself integrity-protected does not satisfy this category.

---

## 7. Correlation Evidence

Allows independent reconstruction of the complete execution-authority chain.

Typical correlation artifacts include:

* lifecycle identifier
* correlation identifier
* parent reference
* sequence identifier
* transaction identifier

Correlation Evidence is not a standalone category that may be provided separately from the evidence it correlates. Where a correlation identifier references another piece of evidence — most importantly, where it binds Execution Evidence back to the Decision Evidence that authorized it — that identifier MUST be embedded within, and covered by, the Integrity Evidence of the artifact carrying it (see "Intrinsically Bound," above). A correlation mapping maintained outside the evidence artifacts themselves — for example, in a separate index or log not covered by the same integrity mechanism — does not satisfy this requirement, because an independent consumer would then be trusting the mapping rather than verifying the binding.

---

## 8. Integrity Evidence

Demonstrates that evidence has not been modified.

Possible mechanisms include:

* digital signatures
* integrity hashes
* authenticated logs
* immutable event chains

EABC does not mandate any specific integrity mechanism. Where Integrity Evidence protects an artifact that also carries a Correlation Evidence reference (per category 7), that reference is within the scope of what must be protected — a signature or hash that omits the correlation reference does not satisfy Evidence Correlation for that artifact.

---

# Evidence Requirements

For every normative property defined by EABC, implementations MUST provide sufficient evidence to demonstrate compliance.

| Property                        | Required Evidence                                                 |
| --------------------------------- | ---------------------------------------------------------------- |
| Independent Execution Authority  | Identity + Integrity                                              |
| Complete Mediation                | Decision + Commit + Correlation (intrinsically bound, per above)  |
| Deterministic Commit Semantics    | Decision + Commit + Execution                                     |
| Context Binding                   | Context                                                            |
| State Binding                     | State                                                              |
| Evidence Integrity                | Integrity                                                          |
| Evidence Correlation              | Correlation, intrinsically bound within Integrity Evidence — not satisfied by an external mapping |
| Failure Semantics                 | Execution + Decision                                               |

---

# Missing Evidence

Missing evidence SHALL NOT be interpreted as successful execution.

Consumers SHOULD distinguish between:

* evidence unavailable
* evidence incomplete
* evidence unverifiable
* evidence inconsistent

An Execution Evidence artifact that lacks an intrinsically bound correlation reference to its Decision Evidence SHOULD be treated as evidence incomplete, not as an implicit authorization.

The interpretation of missing evidence is implementation-independent.

---

# Optional Evidence

Implementations MAY expose additional evidence beyond the EABC minimum.

Examples include:

* telemetry
* runtime measurements
* hardware attestation
* policy explanations
* execution metrics

Such evidence MUST NOT alter the meaning of the normative EABC properties.

---

# Evidence Consumption

Consumers SHOULD evaluate evidence independently of the implementation that generated it.

A consumer should be capable of determining:

* what was authorized,
* under which authority,
* against which state,
* within which context,
* whether execution occurred,
* whether evidence remains trustworthy,
* whether the execution evidence can be verifiably traced back to the authorization that permitted it.

No implementation-specific interpretation should be required to answer these questions. In particular, the last question MUST be answerable from the execution evidence artifact alone, without consulting a separately trusted correlation source.

---

# Relationship to Implementation Profiles

Implementation profiles define how concrete architectures generate evidence satisfying the EABC evidence model.

Different implementations may expose different artifacts while remaining fully conformant, provided they demonstrate the required evidence categories, satisfy the normative execution-authority properties, and satisfy the intrinsic-binding requirement for any correlation reference between authorization and execution evidence.
