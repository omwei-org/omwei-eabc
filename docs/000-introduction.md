# Execution Authority Boundary Contract (EABC)

## Introduction

### Purpose

The Execution Authority Boundary Contract (EABC) defines an implementation-independent contract between systems that authorize actions and systems that execute them.

Its purpose is to establish a common vocabulary and evidence model for communicating execution authority across architectural boundaries, regardless of how authorization decisions are produced or how execution is ultimately enforced.

EABC does **not** prescribe a specific authorization architecture, governance framework, runtime, hardware platform, or implementation technology.

Instead, it defines the minimum properties that an execution-authority system must satisfy in order for another system to independently evaluate and consume its execution-authority assertions.

---

## Position in the Execution Authority Hierarchy

EABC does not stand on its own. It is the middle layer of a three-layer hierarchy:

```text
Execution Authority (research whitepaper)
        │   defines WHAT must be true — the five necessary
        │   properties of an Execution Authority (Chapter 1),
        │   the Authorization Artifact (ACT) and Execution
        │   Attestation (EAtt) artifacts, and the verification
        │   and assurance model (Sections 8–11)
        ▼
Execution Authority Boundary Contract (EABC — this repository)
        │   defines the CONTRACT — normative properties (see
        │   001), an evidence model (see 002), execution and
        │   failure semantics (see 003), and conformance
        │   requirements (see 004), each traceable to the
        │   whitepaper's invariants
        ▼
Implementation Profiles (e.g. EGA/SIF v1)
        │   define HOW a concrete architecture satisfies the
        │   contract — mapping its own components and evidence
        │   artifacts onto EABC's normative requirements
        ▼
Concrete Implementations
```

The relationship between layers is intentionally asymmetric, as established in the whitepaper's Section 12.4: EABC is answerable to the whitepaper's invariants, but the whitepaper's validity does not depend on any particular choice made in EABC or in a given profile. Multiple divergent specifications could in principle satisfy the same theoretical requirements; EABC is offered as one such specification.

Each normative property defined in this specification (see **001 – Execution Authority Properties**) is traceable either to the whitepaper's Chapter 1 (the five necessary properties of an Execution Authority) or to its operationalization layer (the ACT/EAtt artifacts and verification model, Sections 8–11). Where a property has no whitepaper counterpart, it is specific to EABC as a specification layer, per the whitepaper's own expectation that implementation-level questions be resolved downstream of the theory.

---

## Motivation

Modern autonomous systems increasingly separate decision-making from execution.

Application governance platforms evaluate policy, delegated authority, and operational context before authorizing actions.

Execution systems are responsible for transforming those authorizations into externally observable effects.

Although many architectures perform these functions, there is currently no implementation-neutral contract describing the evidence that should exist between authorization and execution.

As a result:

* execution-authority evidence is difficult to exchange across vendors,
* governance systems cannot reliably consume execution results from independent execution domains,
* implementations frequently expose internal mechanisms rather than architectural guarantees.

EABC addresses this gap by defining the boundary itself rather than any particular implementation.

---

## Scope

EABC specifies:

* execution-authority properties,
* required evidence associated with those properties,
* mandatory and optional capabilities,
* failure and missing-evidence semantics,
* interoperability requirements between authorization and execution domains,
* implementation profiles for concrete architectures.

EABC intentionally does not specify:

* policy languages,
* authorization algorithms,
* governance workflows,
* hardware implementations,
* cryptographic mechanisms,
* transport protocols.

These remain implementation-specific.

---

## Architectural Position

EABC exists between authorization and execution.

```text
Authorization Domain
        │
        │
        ▼
Execution Authority Boundary (EABC)
        │
        ▼
Execution Domain
        │
        ▼
External State
```

The contract describes the architectural boundary rather than either side of it.

---

## Design Principles

EABC follows several core principles.

### Implementation Neutrality

The contract specifies observable properties rather than internal architecture.

### Evidence-Based Interoperability

Every required property must be supported by verifiable evidence.

### Independent Consumption

A consuming system should not require implementation-specific knowledge in order to evaluate execution authority.

### Extensible Profiles

Concrete implementations map themselves onto the contract through implementation profiles.

The contract remains stable while implementation profiles may evolve independently.

---

## Relationship to Implementation Profiles

EABC is not itself an execution-authority architecture.

Architectures implement EABC by publishing implementation profiles that describe how their constructs satisfy the contract.

An implementation profile typically maps:

* architectural components,
* evidence structures,
* lifecycle semantics,
* state transitions,
* execution guarantees,

onto the normative EABC requirements.

Multiple independent architectures may conform to the same EABC specification. The reference profile, **EGA/SIF v1**, maps its Authorization Object (AO), Authorization Execution Envelope (AEE), and Execution Control Token (ECT) — which together realize the whitepaper's Authorization Artifact (ACT) — and its Commit Gate's Execution Attestation (EAtt) onto the requirements defined here.

---

## Status

This repository defines the initial draft of the Execution Authority Boundary Contract.

The current work focuses on Version 0 of the specification, intended to establish the core architectural properties before defining detailed evidence schemas and implementation profiles.
