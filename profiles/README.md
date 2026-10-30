# Implementation Profiles

## Purpose

The Execution Authority Boundary Contract (EABC) defines a set of implementation-independent architectural properties, evidence requirements, execution semantics, and conformance criteria.

An **Implementation Profile** describes how a specific architecture satisfies those normative requirements.

Implementation Profiles bridge the gap between a concrete system and the implementation-neutral EABC specification.

---

# Relationship to the Core Specification

The EABC specification defines **what** must be demonstrated.

Implementation Profiles define **how** a particular architecture demonstrates it.

For example:

```text
EABC Specification
        │
        ├── Required Properties
        ├── Evidence Model
        ├── Execution Semantics
        └── Conformance Requirements
                │
                ▼
        Implementation Profile
                │
                ▼
        Concrete Architecture
```

The EABC specification remains stable even as implementation profiles evolve.

---

# Scope of an Implementation Profile

An Implementation Profile documents how a specific execution-authority architecture maps to the EABC contract.

A profile should identify:

* architectural components;
* execution-authority boundary;
* evidence artifacts;
* execution lifecycle;
* state and context binding;
* failure semantics;
* implementation assumptions;
* implementation limitations.

Profiles should avoid introducing new normative requirements.

---

# Required Structure

An Implementation Profile SHOULD include the following sections:

1. Introduction
2. Architectural Overview
3. Execution Authority Boundary
4. Property Mapping
5. Evidence Mapping
6. Execution Semantics
7. Failure Semantics
8. Conformance Statement
9. Known Limitations

Additional sections may be included where appropriate.

---

# Property Mapping

Each profile should explain how the implementation satisfies every mandatory property defined by EABC.

A typical mapping table might include:

| EABC Property                   | Implementation Mechanism | Evidence |
| ------------------------------- | ------------------------ | -------- |
| Independent Execution Authority | ...                      | ...      |
| Complete Mediation              | ...                      | ...      |
| Context Binding                 | ...                      | ...      |
| State Binding                   | ...                      | ...      |

The mapping should describe architectural behavior rather than implementation internals.

---

# Evidence Mapping

Profiles should identify the implementation artifacts that satisfy each evidence category defined by EABC.

Examples include:

* authorization records;
* execution authorization artifacts;
* audit events;
* execution receipts;
* integrity proofs;
* correlation identifiers.

The profile should explain how these artifacts allow an independent consumer to evaluate the EABC properties.

---

# Conformance Declaration

Each profile SHOULD declare:

* implementation name;
* implementation version;
* supported EABC version;
* profile version;
* publication date;
* conformance level.

If the implementation supports only a subset of EABC capabilities, the unsupported capabilities should be explicitly identified.

---

# Versioning

Implementation Profiles evolve independently of the EABC specification.

Changes to a profile do not modify the normative requirements of EABC.

Profiles should clearly indicate:

* supported EABC version;
* profile version;
* compatibility with previous profile versions.

---

# Multiple Profiles

The EABC specification is designed to support multiple independent implementations.

This directory may therefore contain profiles for different execution-authority architectures.

Examples include:

```text
profiles/
├── ega-sif-v1.md
├── vendor-x-runtime.md
├── robotics-reference.md
└── example-reference.md
```

Each profile is evaluated independently for conformance with the EABC specification.

## Profile authoring methodology

A separate, non-normative [Implementation Profile Template](../docs/methodology/EABC-IMPLEMENTATION-PROFILE-TEMPLATE.md) provides a reusable structure for declaring scope, failure modes, status, threat model, artifacts, and falsification conditions. It creates no EABC property, requirement, or conformance level; its starter exit classes are not a mandatory taxonomy.

## Listed Independent Profiles

- [CUSTOS-CORE](CUSTOS-CORE.md) — independent implementation profile, indexed by reference to commit-pinned source documents. Its exit-class register is useful for comparison; a second independently produced profile would test whether the vocabulary holds without either author having to explain their terms. Two classes are declared open and two closed only within stated boundaries. The register does not aggregate these statuses into a conformance level. The repository's tests detect specific pre-registered weakenings under the stated test design; they do not establish non-bypassability.

## Listed Joint Architectural Mappings

- [Bounded Routing V5 — Independent Structural Witness](../docs/EABC_IP_BR_V5_001.md) — frozen joint architectural mapping by Stanislav Levarsky and Stephen Gettel. The underlying Bounded Routing V5 architecture was independently developed; the EABC mapping is joint, not an independently authored mapping. The profile records partial property correspondence and explicitly does not claim full EABC conformance. Its frozen source is anchored at Bounded Routing commit `1a3a5495903ae08d8acc3f93c7a7460a059dad2b`; profile content SHA-256: `b87df53bd45f9d5ea296efb1cb93292b9d41fe115f02c8cde1484f55eb9b90c4`.

---

# Design Principle

Implementation Profiles are **descriptive**, not **prescriptive**.

They describe how an existing architecture satisfies the EABC contract.

They do not redefine, extend, or replace the normative requirements established by the core EABC specification.

This separation allows EABC to remain implementation-neutral while enabling diverse execution-authority architectures to demonstrate interoperability through a common contractual model.
