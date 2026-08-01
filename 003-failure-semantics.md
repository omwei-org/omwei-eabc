# Execution Authority Boundary Contract (EABC)

# 003 – Failure and Execution Semantics

## Purpose

This document defines the normative semantics of execution-authority outcomes.

Its purpose is to ensure that independent consumers interpret authorization and execution evidence consistently, regardless of implementation architecture.

EABC specifies the meaning of execution-authority states rather than implementation-specific workflows.

---

# Fundamental Principle

Authorization and execution are distinct concepts.

An authorization decision expresses whether execution is permitted.

Execution expresses whether an externally observable action was attempted or completed.

An implementation MAY represent these as separate lifecycle stages or MAY bind them atomically.

Both approaches are conformant provided the semantics remain explicit.

---

# Execution Lifecycle

Conceptually, execution authority progresses through four stages.

```text
Authorization Evaluation
        │
        ▼
Authorization Decision
        │
        ▼
Execution Transition
        │
        ▼
Execution Outcome
```

Implementations MAY combine multiple stages into a single transaction.

---

# Authorization Outcomes

Authorization outcomes describe only the authorization decision.

The minimum normative outcomes are:

| Outcome   | Meaning                                    |
| --------- | ------------------------------------------ |
| ALLOW     | Execution is authorized.                   |
| DENY      | Execution is prohibited.                   |
| EXPIRED   | Authorization expired before execution.    |
| CANCELLED | Authorization withdrawn before execution.  |
| UNKNOWN   | Authorization status cannot be determined. |

Authorization outcomes do not imply that execution occurred.

---

# Execution Outcomes

Execution outcomes describe execution behavior.

Minimum execution outcomes are:

| Outcome   | Meaning                                            |
| --------- | -------------------------------------------------- |
| ATTEMPTED | Execution was initiated.                           |
| COMMITTED | External state transition occurred.                |
| FAILED    | Execution terminated unsuccessfully.               |
| ABORTED   | Execution intentionally stopped before completion. |
| UNKNOWN   | Execution status cannot be determined.             |

Execution outcomes do not imply successful authorization.

---

# Atomic Binding

Some architectures perform authorization and execution as one indivisible transaction.

Such implementations MAY expose a single atomic transition.

When atomic binding exists, consumers MUST still be able to determine:

* authorization outcome
* execution outcome

even if both originate from the same event.

Atomic implementations MUST NOT obscure either semantic.

---

# Non-Atomic Implementations

Other architectures expose authorization and execution separately.

For example:

```text
ALLOW
      │
      ▼
ATTEMPTED
      │
      ▼
FAILED
```

or

```text
ALLOW
      │
      ▼
(no execution)
```

These remain fully conformant.

---

# Failure Semantics

Failure MUST be explicitly represented.

Consumers MUST distinguish between:

* authorization failure,
* execution failure,
* evidence failure,
* communication failure.

Implementations SHOULD avoid collapsing these into a generic error.

---

# Missing Evidence

Missing evidence SHALL NOT be interpreted as success.

Consumers SHOULD distinguish:

| Condition                      | Meaning                                 |
| ------------------------------ | --------------------------------------- |
| Missing authorization evidence | Authorization cannot be verified.       |
| Missing execution evidence     | Execution cannot be verified.           |
| Missing commit evidence        | Boundary transition cannot be verified. |
| Missing integrity evidence     | Trustworthiness cannot be established.  |

---

# Unknown State

UNKNOWN is a valid terminal semantic.

UNKNOWN indicates insufficient evidence rather than failure.

Consumers SHOULD treat UNKNOWN conservatively according to their own risk model.

---

# Recovery

Recovery behavior is implementation-specific.

EABC requires only that recovery be observable.

Implementations SHOULD expose sufficient evidence to determine:

* whether recovery occurred,
* whether recovery completed,
* whether previous authorization remained valid.

---

# Consumer Requirements

Consumers SHOULD be capable of independently determining:

* Was execution authorized?
* Was execution attempted?
* Was execution committed?
* Did execution fail?
* Can the outcome be independently verified?

Answers to these questions MUST be derivable from evidence rather than implementation knowledge.

---

# Conformance

An implementation conforms to this specification if it:

* explicitly represents authorization semantics,
* explicitly represents execution semantics,
* distinguishes authorization from execution,
* exposes failure conditions,
* does not interpret missing evidence as successful execution,
* provides sufficient evidence for independent evaluation.
