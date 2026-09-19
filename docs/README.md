# Execution Authority Boundary Contract (EABC)

# Documentation

## Overview

This directory contains the normative documentation for the Execution Authority Boundary Contract (EABC).

EABC defines an implementation-independent contract describing the minimum properties, evidence requirements, and execution semantics required for trustworthy execution-authority boundaries.

The specification focuses on the relationship between:

* systems that authorize actions;
* systems that enforce execution authority;
* systems that verify externally committed effects.

EABC defines the boundary contract, not a specific implementation.

---

# Specification Structure

The documentation is organized into the following layers:

```text
Architecture Principles
        │
        ▼
Execution Authority Properties
        │
        ▼
Evidence Requirements
        │
        ▼
Execution Semantics
        │
        ▼
Conformance Requirements
        │
        ▼
Interoperability Contract
```

Each document addresses a different aspect of the contract.

---

# Documents

## 000 — Introduction

**File:**

`000-introduction.md`

Defines:

* purpose of EABC;
* motivation;
* scope;
* architectural position;
* design principles.

This document explains why the contract exists.

---

## 001 — Execution Authority Properties

**File:**

`001-execution-authority-properties.md`

Defines the normative architectural properties required by EABC.

Examples include:

* independent execution authority;
* complete mediation;
* deterministic commit semantics;
* context binding;
* state binding;
* evidence integrity;
* evidence correlation.

This document defines what a conforming system must guarantee.

---

## 002 — Evidence Model

**File:**

`002-evidence-model.md`

Defines the evidence categories required to demonstrate compliance with EABC properties.

This document describes:

* identity evidence;
* decision evidence;
* context evidence;
* state evidence;
* commit evidence;
* execution evidence;
* correlation evidence;
* integrity evidence.

This document defines how compliance can be independently evaluated.

---

## 003 — Failure and Execution Semantics

**File:**

`003-failure-semantics.md`

Defines the meaning of authorization and execution states.

This document establishes the distinction between:

* authorization decision;
* execution attempt;
* execution commit;
* execution outcome;
* failure states;
* unknown states.

This prevents ambiguity between permission and actual execution.

---

## 004 — Conformance

**File:**

`004-conformance.md`

Defines how implementations claim compatibility with EABC.

This document specifies:

* conformance requirements;
* evidence sufficiency;
* implementation profiles;
* conformance statements;
* versioning expectations.

---

## 005 — Interoperability Contract

**File:**

`005-interoperability-contract.md`

Defines the provisional interoperability layer between independent EABC implementations.

This document specifies:

* the boundary between EABC semantics and implementation mappings;
* authority epoch and execution epoch semantics;
* authorization outcome mappings;
* correlation requirements;
* integrity-mechanism neutrality;
* commit-time interoperability semantics;
* known implementation mappings;
* validation and evolution requirements.

**Status:** Draft v0.1 — Provisional.

The current version has been validated against one implementation pair and one real interoperability run. It is intentionally not yet a stable universal wire contract.

---

# Implementation Profiles

Concrete architectures are described separately from the core specification.

Implementation profiles are located in:

```text
../profiles/
```

A profile explains how a specific architecture maps its components and evidence artifacts to the EABC requirements.

The first reference profile is:

```text
../profiles/ega-sif-v1.md
```

---

# Design Philosophy

EABC separates:

* architectural requirements from implementations;
* execution authority from governance decisions;
* evidence from assumptions;
* conformance from implementation similarity;
* normative semantics from interoperability mappings.

This separation allows different architectures to interoperate through a shared execution-authority contract without requiring them to share the same internal implementation.

---

# Contribution

The specification is intended to evolve through open discussion and review.

Feedback should focus on:

* missing architectural properties;
* evidence requirements;
* lifecycle semantics;
* interoperability considerations;
* implementation profile mappings;
* validation against additional independent implementations.

The goal is not to standardize one implementation, but to establish a common contract that multiple implementations can satisfy.
