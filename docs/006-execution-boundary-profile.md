# Execution Authority Boundary Contract (EABC)

# 006 – Execution-Boundary Profile (EBP)

## Status

This document defines the EABC Execution-Boundary Profile (EBP).

EBP extends EABC Core without redefining its existing execution-authority, evidence, freshness, provenance, revocation, failure, or commit semantics.

The execution boundary MAY be implemented in software, hardware, or a combination of mechanisms.

---

## 1. Scope

The EABC Execution-Boundary Profile defines the normative semantics for binding execution authority to an execution boundary and for accepting that authority for COMMIT.

EBP adds a contract-level representation of the execution boundary while preserving the existing EABC Core semantics.

The purpose of EBP is to make the boundary through which a protected effect must pass explicit, assessable, and independently verifiable.

EBP does not prescribe a particular enforcement technology.

---

## 2. Terminology

### Execution Boundary

An execution boundary is the point, mechanism, or composite mechanism at which execution authority is accepted before a protected effect may be committed.

An execution boundary MAY be implemented by software, hardware, or a combination of mechanisms.

### ExecutionBoundaryContract

An ExecutionBoundaryContract defines the applicable authority conditions, boundary conditions, commit conditions, and required properties of the execution boundary for a protected effect.

### Boundary Binding

Boundary Binding is the deployment/configuration-plane association between an ExecutionBoundaryContract and the execution-boundary implementation instance through which the protected effect is required to pass.

Boundary Binding is distinct from per-transaction authority admission and from COMMIT.

### Required Boundary Properties

Required Boundary Properties are implementation-level properties that an execution-boundary implementation MUST demonstrate in order to be eligible for the applicable ExecutionBoundaryContract.

They are assessed at the conformance/implementation plane, not as per-commit authorization predicates.

### Conformance Evidence

Conformance Evidence is instance-scoped evidence demonstrating that an execution-boundary implementation satisfies the Required Boundary Properties of an applicable ExecutionBoundaryContract.

Conformance Evidence is a separate evidence class from the eight transaction-scoped EABC Core evidence categories.

### Conformance Status

Conformance Status is the current validity state of applicable Conformance Evidence:

* VALID
* INVALID
* INDETERMINATE

### Conformance Eligibility

Conformance Eligibility is a derived gate indicating whether the applicable execution-boundary implementation may participate in a valid COMMIT.

CONFORMANCE_ELIGIBLE is true only when the applicable Conformance Status is VALID.

---

## 3. ExecutionBoundaryContract

The ExecutionBoundaryContract groups existing EABC Core transaction semantics with the new execution-boundary and conformance semantics.

Conceptually:

```
ExecutionBoundaryContract
├── AUTHORITY CONDITIONS
├── BOUNDARY CONDITIONS
├── COMMIT CONDITIONS
└── REQUIRED BOUNDARY PROPERTIES
```

### 3.1 Authority Conditions

Authority Conditions are evaluated per transaction.

They reuse existing EABC Core semantics including:

* authority validity;
* provenance;
* revocation/status;
* freshness;
* temporal validity;
* exact action binding.

Exact action binding is an authority condition and is not a Required Boundary Property.

### 3.2 Boundary Conditions

Boundary Conditions are evaluated per transaction at the execution boundary.

They MAY include:

* boundary identity;
* applicable target state;
* boundary-specific predicates;
* schema validity where required by the applicable profile.

Boundary Conditions reuse or extend existing Context Binding and State Binding semantics.

Schema validity, when used, is a per-commit boundary predicate and is not a Required Boundary Property.

### 3.3 Commit Conditions

Commit Conditions govern the commit act itself.

They reuse existing EABC Core deterministic commit and failure semantics and MAY include:

* single-use semantics;
* atomicity;
* fail-closed behavior;
* other applicable commit predicates defined by the contract.

Commit Conditions are distinct from Authority Conditions and Required Boundary Properties.

### 3.4 Required Boundary Properties

Required Boundary Properties describe implementation properties of the execution boundary.

Examples include:

* independence;
* exclusivity;
* non-bypass;
* isolation;
* physical non-extractability where required by the applicable contract.

Required Boundary Properties are not per-commit predicates.

They are established through Conformance Assessment and represented through Conformance Evidence.

EBP does not prescribe which implementation mechanism provides a property.

---

## 4. Boundary Binding

A deployment MUST establish a Boundary Binding between the applicable ExecutionBoundaryContract and the execution-boundary implementation instance.

The binding MUST identify, directly or through an unambiguous reference:

* the ExecutionBoundaryContract;
* the execution-boundary implementation instance;
* the protected effect or effect class;
* the boundary through which the protected effect is required to pass.

Boundary Binding occurs in the deployment/configuration plane.

```
BIND ≠ FINAL_AUTHORITY_CHECK ≠ COMMIT
```

Boundary Binding does not itself authorize an execution or constitute a COMMIT.

---

## 5. Protected Effect

A protected effect is an externally observable state transition that is subject to an ExecutionBoundaryContract.

Conceptually:

```
execution authority
      ↓
action
      ↓
target
      ↓
boundary
      ↓
effect
```

An effect MAY be physical or representational. Examples include physical actuation, database mutation, payment, publication, tool execution, software deployment, or another externally observable state transition.

An implementation claiming that an effect is protected by EBP MUST ensure that no unmodeled execution path can produce the protected effect without satisfying the applicable ExecutionBoundaryContract.

---

## 6. Conformance

### 6.1 Conformance Assessment

Conformance Assessment determines whether an execution-boundary implementation satisfies the Required Boundary Properties of an applicable ExecutionBoundaryContract.

Assessment is distinct from runtime conformance validity.

EBP does not define a specific assessment methodology.

### 6.2 Conformance Evidence

Conformance Assessment MUST produce or reference sufficient Conformance Evidence for an independent consumer to evaluate the claimed properties.

Conformance Evidence is instance-scoped.

It MUST be bound to the implementation instance whenever a Required Boundary Property is defined in terms of the identity, configuration, measurement, isolation, exclusivity, or runtime state of that implementation instance.

The evidence MAY use an EAT-based attestation profile or another implementation-neutral evidence carrier.

EBP does not define a proprietary attestation wire format.

### 6.3 Conformance Status

The applicable Conformance Status is derived from the validity dimensions required by the applicable contract.

At minimum, EBP distinguishes:

* temporal validity;
* status/revocation validity;
* implementation-instance or state freshness where applicable.

The composition rule is:

```
INVALID
    if any required validity dimension is INVALID

INDETERMINATE
    else if any required validity dimension is INDETERMINATE

VALID
    otherwise
```

Thus:

```
INVALID > INDETERMINATE > VALID
```

### 6.4 Conformance Eligibility

Conformance Eligibility is derived from Conformance Status.

```
CONFORMANCE_STATUS = VALID
        ↓
CONFORMANCE_ELIGIBLE = true
```

Both INVALID and INDETERMINATE status prevent a valid COMMIT.

Deployment and availability mechanisms MAY determine how conformance status is established, maintained, refreshed, or recovered.

They MUST NOT redefine INDETERMINATE as VALID for COMMIT purposes.

A live remote status lookup at every commit is not required. Caching, local status materialization, redundancy, or other availability mechanisms MAY be used, provided that inability to establish required validity results in INDETERMINATE rather than VALID.

---

## 7. Runtime Commit Semantics

The valid commit path is:

```
VALID_COMMIT :=
    CONFORMANCE_ELIGIBLE
 ∧  FINAL_AUTHORITY_CHECK = PASS
 ∧  COMMIT_CONDITIONS = PASS
```

The three gates have distinct semantics.

```
Conformance Eligibility
    fail → NO VALID COMMIT
             → Conformance Evidence

FINAL_AUTHORITY_CHECK
    fail → DENY
             → Decision Evidence

COMMIT_CONDITIONS
    fail → COMMIT REFUSED
             → Commit Evidence
```

### 7.1 Conformance Failure

If required Conformance Evidence is INVALID or INDETERMINATE:

> NO VALID COMMIT

This outcome MUST NOT be represented as an authorization DENY.

The underlying execution authority MAY remain valid. The failure is that the required execution boundary is not eligible to accept a valid COMMIT.

### 7.2 Authorization Failure

If FINAL_AUTHORITY_CHECK fails:

> DENY

DENY retains its EABC Core meaning as an authorization outcome.

It belongs to Decision Evidence.

FINAL_AUTHORITY_CHECK MUST NOT be used to represent conformance validity.

### 7.3 Commit Failure

If COMMIT_CONDITIONS fail after conformance eligibility and FINAL_AUTHORITY_CHECK have succeeded:

> COMMIT REFUSED

COMMIT REFUSED is a commit failure outcome, not an authorization DENY and not a conformance failure.

It belongs to Commit Evidence and MUST remain distinguishable from DENY and NO VALID COMMIT.

---

## 8. Evidence Model

EBP does not modify the eight EABC Core evidence categories:

1. Identity Evidence
2. Decision Evidence
3. Context Evidence
4. State Evidence
5. Commit Evidence
6. Execution Evidence
7. Correlation Evidence
8. Integrity Evidence

All eight remain transaction-scoped.

EBP introduces a separate evidence class:

```
EBP Conformance Evidence
    └── implementation-scoped conformance claim/attestation
```

Conformance Evidence MUST NOT be treated as a ninth EABC Core evidence category.

### 8.1 Boundary Evidence Binding

A reference from transaction-scoped execution or commit evidence to Conformance Evidence MUST be intrinsically bound.

The referenced:

* conformance claim;
* implementation instance;
* applicable ExecutionBoundaryContract;

MUST be integrity-protected as part of the evidence relationship.

A naked correlation reference describes a relationship but does not prove it.

This requirement directly applies the existing EABC Evidence Correlation and Intrinsically Bound principles to the new instance-scoped Conformance Evidence class.

### 8.2 Failure Evidence Separation

Consumers MUST be able to distinguish:

| Outcome | Semantic source | Evidence |
| --- | --- | --- |
| NO VALID COMMIT | Conformance Eligibility | Conformance Evidence |
| DENY | FINAL_AUTHORITY_CHECK | Decision Evidence |
| COMMIT REFUSED | COMMIT_CONDITIONS | Commit Evidence |
| COMMIT | Successful commit | Commit Evidence |
| EFFECT | Execution outcome | Execution Evidence |

Missing or indeterminate Conformance Evidence SHALL NOT be interpreted as VALID conformance.

---

## 9. Implementation Neutrality

EBP does not determine the enforcement substrate.

The contract specifies required properties; conformance determines whether a concrete implementation satisfies them.

Conceptually:

```
Protected Effect
      ↓
ExecutionBoundaryContract
      ↓
Required Boundary Properties
      ↓
Conformance
      ↓
Implementation
   ┌───────┼────────┐
   ↓       ↓        ↓
  SW      HW     Composite
```

An implementation MAY use:

* a software execution boundary;
* a hardware execution boundary;
* a composite software/hardware mechanism;
* another mechanism capable of satisfying the required properties.

EABC MUST NOT perform runtime substrate routing such as selecting software or hardware based on transaction context.

Where a required property can only be satisfied by a particular design, that conclusion arises from conformance assessment rather than from an EABC runtime routing decision.

Conformance to the same normative EBP semantics does not imply equivalent implementation assurance. Different implementations MAY differ in isolation, bypass resistance, trust anchors, privilege separation, physical enforcement, or other assurance characteristics.

---

## 10. Non-Goals

EBP does not:

* mandate a specific enforcement technology;
* require an SLC;
* require hardware enforcement;
* replace authorization systems;
* replace identity or attestation systems;
* define physical safety requirements;
* define application-specific policy languages;
* require EABC to execute as a separate runtime component;
* claim equivalent assurance across software and hardware implementations;
* by itself establish resistance to privileged bypass, compromise, or physical tampering.

---

## 11. Relationship to EABC Core

EBP is an extension profile of EABC Core.

The following Core semantics are reused rather than redefined:

* execution authority;
* authority state;
* FINAL_AUTHORITY_CHECK;
* COMMIT;
* revocation;
* freshness;
* provenance;
* temporal validity;
* single-use semantics;
* failure semantics;
* transaction-scoped evidence.

The new normative object is the:

> **ExecutionBoundaryContract**

The new semantic plane is:

> **Conformance**

Boundary Evidence Binding extends the existing Evidence Correlation and Intrinsically Bound principles to instance-scoped Conformance Evidence.

ExecutionBoundaryPolicy is an external input to contract construction and is not an EABC primitive.

---

## 12. Conformance Crosswalk

| EBP Element | EABC Core Basis | Classification |
| --- | --- | --- |
| ExecutionBoundaryContract | No direct Core equivalent; groups existing AO/AEE/ECT pipeline semantics with new boundary sections | NEW |
| Authority Conditions | Revocation, Freshness, Provenance; Decision/State Evidence | REUSE |
| Boundary Conditions | Context Binding, State Binding | REUSE / EXTEND |
| Commit Conditions | Deterministic Commit Semantics, Failure Semantics; Commit Evidence | REUSE |
| Required Boundary Properties | No direct Core equivalent; informed by external placement/assurance assessment | NEW |
| Boundary Binding | No direct equivalent; structurally analogous to authority-side binding but applies to the implementation instance | NEW |
| Conformance Assessment | No direct Core equivalent | NEW |
| Conformance Evidence | No existing Core evidence category; EAT may provide the carrier/profile basis | NEW EVIDENCE CLASS |
| Conformance Status | No formal Core equivalent | NEW SEMANTIC LAYER |
| Conformance Eligibility | Derived from Conformance Status | DERIVED GATE |
| Boundary Evidence Binding | Evidence Correlation + Intrinsically Bound | EXTEND |
| ExecutionBoundaryPolicy | External customer/deployment requirements | EXTERNAL INPUT |
| FINAL_AUTHORITY_CHECK | Existing Core operation | REUSE |
| COMMIT | Existing Core operation | REUSE |
| EFFECT | Existing execution outcome | REUSE |

EBP therefore adds one new normative object and one new semantic plane while reusing the existing EABC Core execution, evidence, and commit semantics.

---

## 13. Implementation Profiles

A concrete implementation MAY publish an EBP implementation mapping in addition to its EABC Core profile.

Examples of possible enforcement implementations include:

* software execution-boundary enforcement;
* hardware execution-boundary enforcement;
* composite enforcement;
* fixed-renderer or other constrained-effect enforcement.

An implementation example does not constitute an EBP conformance claim unless its Required Boundary Properties have been assessed and the applicable Conformance Evidence has been established.

---

## 14. Normative Summary

A conforming EBP deployment:

1. defines an ExecutionBoundaryContract for each protected effect or applicable effect class;
2. establishes Boundary Binding at deployment/configuration time;
3. identifies Required Boundary Properties separately from per-commit conditions;
4. establishes Conformance Evidence for the applicable implementation instance;
5. derives Conformance Status as VALID, INVALID, or INDETERMINATE;
6. permits a valid COMMIT only when Conformance Eligibility is true;
7. performs FINAL_AUTHORITY_CHECK using existing EABC Core semantics;
8. evaluates COMMIT_CONDITIONS using existing EABC Core commit semantics;
9. preserves distinct outcomes for conformance failure, authorization DENY, and commit failure;
10. preserves intrinsic evidence binding between transaction-scoped evidence and referenced Conformance Evidence;
11. does not prescribe a concrete software, hardware, or composite enforcement substrate.

