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

# Verification at the Point of Consequence

Where an execution boundary evaluates whether an already-issued authority may still be used for a protected transition, **verification** means establishing whether the conditions required for that transition still hold at the point of consequence.

The verification semantics are realized by the existing commit-time gates:

* `FINAL_AUTHORITY_CHECK` evaluates authority validity and its applicable runtime validity conditions.
* `COMMIT_CONDITIONS` evaluates the conditions declared as necessary for the protected transition.

These remain distinct gates and MUST NOT be merged into a new verification primitive.

Accordingly:

```text
Verification at the point of consequence
        =
FINAL_AUTHORITY_CHECK
        +
COMMIT_CONDITIONS
```

This terminology is semantic: it does not introduce a new EABC primitive named `Verification`.

In particular, EBP's `CONFORMANCE_ELIGIBLE` gate remains separate. Conformance establishes whether the execution-boundary implementation is eligible to serve the contract; it is not folded into `FINAL_AUTHORITY_CHECK`.

---

# Required Conditions and Fail-Closed Semantics

When an authority or protected transition explicitly requires a condition to hold at the point of consequence, inability to establish that condition SHALL NOT be interpreted as satisfaction of the condition.

If a required condition cannot be established, the corresponding authorization or commit gate SHALL NOT establish a valid transition on the basis of that condition.

This is the execution-condition application of EABC's general failure rule:

> missing or insufficient evidence does not establish success.

This requirement does not redefine the general `UNKNOWN` outcome. `UNKNOWN` remains a valid semantic for an outcome whose status cannot be determined. The fail-closed rule applies specifically when an implementation is deciding whether an explicitly required condition has been established for a protected transition.

The same fail-closed pattern applies to conformance: EBP already defines `INDETERMINATE` conformance as unacceptable for `VALID_COMMIT`. Conformance validity and execution-condition verification therefore remain separate gates while sharing the same failure principle.

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

Atomicity of an authorization/commit transition does not by itself establish atomicity between `COMMIT` and the subsequent external `EFFECT`. Any guarantee concerning that boundary requires its own execution-boundary semantics.

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

Where missing or insufficient evidence concerns an explicitly required commit condition, the condition SHALL NOT be treated as satisfied.

---

# Unknown State

UNKNOWN is a valid terminal semantic.

UNKNOWN indicates insufficient evidence rather than failure.

Consumers SHOULD treat UNKNOWN conservatively according to their own risk model.

The general `UNKNOWN` outcome does not by itself define the result of every authorization or execution policy. Where a specific condition has been declared necessary for a protected transition, the fail-closed rule above applies to whether that condition is established.

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
