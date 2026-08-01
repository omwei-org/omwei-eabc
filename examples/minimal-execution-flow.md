# Minimal Execution Flow Example

## Purpose

This example demonstrates the minimum lifecycle of an execution-authority boundary.

The scenario shows how an autonomous system action moves from intent creation to an externally committed effect while preserving:

* authorization evidence;
* execution authority;
* execution outcome;
* independent verification.

This example is illustrative and does not define additional EABC requirements.

---

# Scenario

An autonomous software agent determines that an external action is required.

Example:

> An autonomous operations agent detects that a service instance requires scaling and proposes creating an additional compute resource.

The agent may generate the request, but it does not directly possess execution authority.

---

# Actors

The example contains four conceptual actors.

```text id="1l7w4x"
+----------------+
| Autonomous     |
| Agent          |
+----------------+
        |
        |
        ▼
+----------------+
| Authorization  |
| Domain         |
+----------------+
        |
        |
        ▼
+----------------+
| Execution      |
| Authority      |
| Boundary       |
+----------------+
        |
        |
        ▼
+----------------+
| External       |
| System         |
+----------------+
```

---

# Step 1 — Intent Creation

The autonomous agent creates an intent describing the desired action.

Example:

```text id="2xw7k5"
Intent:
    Action:
        Create compute resource

    Target:
        Production environment

    Reason:
        Capacity threshold exceeded
```

At this stage:

* no execution authority exists;
* no external effect has occurred;
* the action remains a proposal.

---

# Step 2 — Authorization Evaluation

The authorization domain evaluates the requested action.

The evaluation may consider:

* policy;
* delegated authority;
* current system state;
* operational constraints;
* risk conditions.

The result is an authorization decision.

Example:

```text id="o0x5h4"
Authorization Decision:

    Result:
        ALLOW

    Scope:
        Create compute resource

    Validity:
        30 minutes

    Decision ID:
        decision-12345
```

Important:

An authorization decision does not prove that execution occurred.

It only establishes permission.

---

# Step 3 — Execution Authority Boundary

The execution-authority boundary receives the authorized action.

The boundary verifies:

* authorization integrity;
* execution context;
* target identity;
* validity conditions;
* required evidence.

The boundary determines whether the action may transition into execution.

Example:

```text id="jv6f5r"
Execution Authority Check:

    Authorization:
        Valid

    Context:
        Matching

    Target:
        Verified

    Decision:
        COMMIT ALLOWED
```

---

# Step 4 — Execution Attempt

The execution domain receives the authorized action.

An execution attempt is created.

Example:

```text id="w5u9p8"
Execution Attempt:

    Execution ID:
        execution-789

    Status:
        ATTEMPTED
```

At this point:

* execution has started;
* the final external state is not yet guaranteed.

---

# Step 5 — Commit Result

The execution domain reports the result of the transition.

Example:

```text id="t2b1xm"
Execution Result:

    Status:
        COMMITTED

    External Effect:
        Compute resource created

    Timestamp:
        2026-08-01T08:00:00Z
```

The committed state transition is now externally observable.

---

# Step 6 — Evidence Correlation

The complete lifecycle can be reconstructed using correlated evidence.

Example:

```text id="39g7l1"
Intent ID
    │
    ▼
Decision ID
    │
    ▼
Execution Authority ID
    │
    ▼
Execution ID
    │
    ▼
Commit Record
```

An independent consumer can determine:

* what action was requested;
* who authorized it;
* under what conditions;
* whether execution occurred;
* whether the external state changed.

---

# Failure Example

Authorization and execution are separate lifecycle concepts.

A valid authorization may still result in failed execution.

Example:

```text id="q8d4vr"
Authorization:

    ALLOW


Execution:

    ATTEMPTED


Result:

    FAILED
```

The system must not interpret this as successful execution.

---

# Atomic Execution Example

Some architectures may bind authorization and execution into one atomic transition.

Example:

```text id="b4z7nt"
Authorization:
    ALLOW

Execution:
    COMMITTED

Transaction:
    ATOMIC
```

This remains compatible with EABC if the implementation preserves both semantic meanings.

---

# EABC Properties Demonstrated

This example demonstrates:

| Property                        | Demonstration                                      |
| ------------------------------- | -------------------------------------------------- |
| Independent Execution Authority | Agent does not directly execute                    |
| Complete Mediation              | Action crosses the authority boundary              |
| Deterministic Commit Semantics  | Commit result is explicit                          |
| Context Binding                 | Target and conditions are verified                 |
| State Binding                   | Decision context is preserved                      |
| Evidence Integrity              | Records can be independently verified              |
| Evidence Correlation            | Lifecycle identifiers connect events               |
| Failure Semantics               | Authorization and execution failures are separated |

---

# Summary

The purpose of an execution-authority boundary is not to decide what an agent should do.

Its purpose is to ensure that when an action becomes an externally committed effect:

* authority is explicit;
* authorization is verifiable;
* execution is observable;
* evidence is preserved.

EABC provides the common contract that allows these guarantees to be expressed across different architectures.
