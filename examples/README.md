# Examples

## Purpose

This directory contains example scenarios demonstrating how the Execution Authority Boundary Contract (EABC) can be applied in practice.

Examples are intended to make the architectural concepts easier to understand by showing how authorization, execution authority, evidence, and external state transitions relate to each other.

Examples are **illustrative**.

They do not define additional requirements and do not replace the normative specification contained in:

```text
../docs/
```

---

# Relationship to the Specification

Examples demonstrate the concepts defined by EABC:

```text id="h7k8v3"
EABC Specification
        │
        ├── Properties
        ├── Evidence Model
        ├── Execution Semantics
        └── Conformance
                │
                ▼
            Examples
                │
                ▼
     Practical Execution Scenarios
```

The examples show how a conforming implementation may satisfy the contract.

---

# Example Structure

Each example SHOULD describe:

* the initiating intent;
* the authorization process;
* the execution-authority boundary;
* the evidence generated;
* the execution outcome;
* the final externally committed effect.

Examples SHOULD make clear the distinction between:

* permission to execute;
* attempt to execute;
* successful external state change.

---

# Available Examples

## Minimal Execution Flow

**File:**

```text
minimal-execution-flow.md
```

Demonstrates the basic EABC lifecycle:

```text id="ph1w8q"
Intent
  │
  ▼
Authorization Decision
  │
  ▼
Execution Authority Validation
  │
  ▼
Commit Decision
  │
  ▼
Execution Outcome
  │
  ▼
External State Change
```

This example illustrates the minimum concepts required to understand an execution-authority boundary.

---

# Future Examples

Additional examples may include:

* autonomous agent action approval;
* financial transaction execution;
* industrial control operation;
* robotic action authorization;
* multi-agent delegated authority;
* recovery after execution failure;
* hardware-backed execution authority.

---

# Example Requirements

Examples SHOULD:

* use implementation-neutral terminology;
* identify the relevant EABC properties;
* identify evidence categories;
* distinguish authorization from execution;
* avoid implying that one implementation is required.

---

# Non-Goals

Examples are not intended to:

* define APIs;
* define message formats;
* prescribe deployment architectures;
* replace implementation profiles.

They exist to improve understanding and interoperability.

---

# Contributing Examples

New examples should demonstrate a clear execution-authority scenario and explain:

1. What action is being authorized.
2. Who or what provides authorization.
3. Where the execution-authority boundary exists.
4. What evidence is generated.
5. How the final state transition is verified.

Examples should remain compatible with the implementation-neutral principles of EABC.
