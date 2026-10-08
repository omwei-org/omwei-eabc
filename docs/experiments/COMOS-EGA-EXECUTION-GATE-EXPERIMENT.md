# ComOS → EGA Execution Gate Experiment

**Status:** EXPERIMENTAL  
**Date:** 2026-10-06

## Question

Can an externally supplied authorization decision stop a real ComOS brokered `retail_sale` before the first protected effect?

## Existing observation path

```
ComOS actual state
    → Observer
    → EvidenceEnvelope
    → EGA
```

The Observer → EGA evidence seam is validated separately.

This experiment does **not** reproduce, publish, or depend on the Observer implementation artifact.

## Execution experiment

The experiment isolates the execution-side seam:

```
EGA decision
    ↓
experimental execution gate
    ↓
ComOS brokered retail_sale
    ↓
protected effect
```

The experimental decision source was deliberately test-only. It was not represented as a production EGA authority, ECT, or cryptographically bound execution artifact.

The temporary ComOS modification was placed in:

```
src/platforms/retail/order-tool-agent.ts
createBrokeredPendingOrder()
```

The gate was placed after catalog/input processing and before the first protected effect, `reserveInventory()`.

## ALLOW result

With the experimental decision set to `ALLOW`:

```
ALLOW
  ↓
reserveInventory()
  ↓
Orders.create()
  ↓
pending order created
```

Observed result:

- inventory changed from 100 to 99
- `reserveInventory()` was reached
- `Orders.create()` was reached
- a pending order was created
- execution returned successfully

Example result:

```
{
  ok: true,
  order_id: "test_ord_1791443361079",
  total: 2850,
  status: "pending"
}
```

## BLOCK result

With the experimental decision set to `BLOCK`:

```
BLOCK
  ↓
execution stops
  ↓
reserveInventory() not reached
  ↓
Orders.create() not reached
```

Observed result:

- `reserveInventory()` was not called
- `Orders.create()` was not called
- no order was created
- inventory remained unchanged at 100
- execution returned the experimental block reason

Example result:

```
{
  ok: false,
  reason: "experimental_ega_block"
}
```

The protected-effect calls were instrumented during the experiment so that BLOCK could be observed as non-entry into the protected-effect section rather than inferred only from the absence of an order.

## Result

The experiment demonstrates that a decision supplied through an externalized EGA test seam can gate the concrete ComOS brokered `retail_sale` execution path before the selected protected effect.

This is an execution-seam experiment, not a claim that the test decision source itself constitutes EGA.

## What this does not establish

This experiment does **not** establish:

- NON_BYPASSABILITY
- complete mediation across ComOS
- authority authenticity
- cryptographic authority binding
- production security
- EABC conformance
- SLC conformance
- payload integrity
- state-drift detection
- coverage of other ComOS execution paths

In particular, other paths to protected effects exist and were deliberately outside the scope of this experiment.

## Implementation status

The experimental ComOS modifications were temporary.

After the experiment:

- the temporary execution gate was removed
- test instrumentation was removed
- the standalone experimental test was removed
- the ComOS source extract was restored to its original state

No ComOS production source changes remain from this experiment.

## Next experiment

The next step is to replace the test decision source with an actual EGA execution authority / ECT at the same execution seam and repeat the ALLOW/BLOCK experiment.

That next step should still remain separate from claims about NON_BYPASSABILITY or SLC conformance.
