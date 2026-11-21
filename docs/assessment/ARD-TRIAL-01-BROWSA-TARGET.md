# ARD-TRIAL-01 — Trial 1 Target Instance Specification (Browsa OSA)

**Status:** PRELIMINARY — NOT FROZEN.  
**Assessment status:** NOT STARTED.  
**Trial:** 1 — software commerce-agent node.  
**Document type:** Non-normative companion specification to `ARD-TRIAL-01.md`.

This document specifies a preliminary candidate target instance for Trial 1. It is not an assessment result, implementation validation, or conformance verdict. The attacker model and assessment scope remain subject to trial-owner review. This document does not freeze the preregistration or authorise any discovery run.

**Target:** Browsa Open Shopping Agent  
**Repository:** `browsa-io/open-shopping-agent`  
**Pinned revision:** `b9ad9d38f01acaed5038b5b59b6981ef7aab65a6`  
**Version:** `0.2.1`

## 5. Trial 1 — Target Instance Specification

### 5.1 Protected Effect (E)

A merchant accepts and commits a purchase order submitted through the merchant's checkout system, evidenced by an order confirmation attributable to that transaction.

Cart creation, checkout preparation or review, and a locally generated success message do not independently constitute E.

A browser-displayed order number or confirmation page is the primary *observable indicator* of E. Establishing that this indicator reliably corresponds to merchant-side commitment is part of the assessment burden, not a precondition assumed by this specification.

### 5.2 Candidate Enforcement Boundary (B)

The candidate enforcement boundary comprises:

- Engine-level approval and mandate enforcement, including `approvalProblem()` / `gateProblem()` and the relevant decision paths in `src/core/engine.ts`.
- The approval context passed from the engine to the store adapter.
- Adapter-level re-reading of the current checkout total and comparison against the approved amount and currency before the final order-submission action.
- The central adapter invocation path through `placeWith()`.

This is a candidate architectural boundary, not an established NON_BYPASSABILITY result.

The assessment must examine every route capable of producing E, not merely explicit calls to `adapter.placeOrder()`. In particular, it must determine whether browser-controlled actions or other interfaces can reach merchant-side order submission without satisfying the candidate boundary.

### 5.3 Attacker Model (A)

**Status: OPEN — pending trial-owner review and acceptance.**

The following are candidate attacker capabilities for consideration. Their inclusion here does not assert that each capability is achievable in the pinned implementation or any particular deployment.

- **A1 — Model compromise or manipulation:** The model produces actions contrary to the user's intended purchase constraints.
- **A2 — MCP client manipulation:** Unexpected, repeated, malformed, or adversarial tool requests are submitted through the MCP interface.
- **A3 — Malicious merchant-page content:** Page content attempts to influence browser-controlled AI tasks or alter checkout behaviour.
- **A4 — Browser-session manipulation:** Browser state, page content, checkout totals, or browser control is manipulated between review and submission. This includes cases in which an AI-controlled browser task shares the same browser instance and page state as the checkout under review, as in a `sameBrowser: true` configuration.
- **A5 — Adapter faults:** An adapter misidentifies checkout state, reads an incorrect total, or performs an unintended final action.

The trial owner must determine which candidate capabilities belong in A, which assumptions and trust boundaries apply, and which capabilities are excluded. In particular, the presence of a `sameBrowser: true` path is not itself proof that an attacker can exploit it or that it must be included in the final attacker model.

### 5.4 System Model (M)

The initial system model is the pinned source repository at revision `b9ad9d38f01acaed5038b5b59b6981ef7aab65a6`.

Relevant areas include:

- `src/core/engine.ts`
- `src/core/limits.ts`
- `src/core/browsers.ts`
- `src/core/mandate.ts`
- `src/web/session.ts`
- `src/web/server.ts`
- `src/mcp/server.ts`
- `src/stores/`
- Relevant tests, fixtures, and configuration.

The system model includes the engine, session and interface layers, browser-control capabilities, AI fallback mechanisms, store adapters, and their interactions.

The repository inventory is not assumed to be complete. Discovery must consider omitted, undocumented, or otherwise unrepresented interfaces and paths rather than treating the supplied source inventory as exhaustive.

Source inspection at the pinned revision provides structural evidence about declared paths; it does not by itself establish runtime exclusivity of those paths.

The `sameBrowser: true` AI fallback path is a priority area for discovery. The assessment must examine whether an AI-controlled browser task can reach merchant-side order submission without passing through the engine-level approval boundary.

The up-front mandate mechanism is initially treated as an authorised alternative approval path, not as a bypass. Its authorisation source, scope, amount limits, and enforcement must be examined. Its existence alone does not establish either a bypass or adequate enforcement.

### 5.5 Evidence Scope (S)

The preliminary evidence scope includes:

- Static source inspection at the pinned revision.
- Call-graph and interface-path analysis.
- Review of unit tests and fixtures.
- Inspection of browser-control and AI fallback capabilities.
- Review of CLI, web, and MCP entry points.
- Locally reproducible tests using fakes or saved pages.

The currently identified evidence does not include a demonstrated end-to-end purchase committed by a real merchant.

Accordingly:

- Fake-based or saved-page tests do not establish real merchant-side enforcement.
- A locally displayed confirmation is not independent evidence of merchant-side commitment unless its reliability is established.
- Source-level structural evidence must be distinguished from simulated test evidence and deployment-specific evidence.
- Evidence of an actual merchant-side effect must be distinguished from evidence that the local application reports success.

The absence of a real merchant checkout demonstration limits the strength of any positive conformance conclusion. The available evidence must be evaluated against the final attacker model, deployment assumptions, and Protected Effect.

### 5.6 Priority Open Questions

1. Can the AI fallback path using `sameBrowser: true` reach merchant-side order submission without passing through the engine-level approval boundary?
2. Are browser-control permissions technically constrained, or does the implementation rely on model instructions to prevent final order submission?
3. Do all supported adapters enforce the approved amount and currency immediately before the final submission action?
4. Can concurrent, repeated, or delayed approvals create a route to E outside the candidate boundary?
5. Does the up-front mandate mechanism remain within its declared authorisation limits across all relevant paths?
6. What evidence establishes that E actually occurred at the merchant, rather than merely being reported by the local application?

These are questions for discovery and validation, not pre-classified bypasses or findings.

### 5.7 Conformance Evidence Limitation

A CONFORMS verdict cannot be justified solely by source inspection or simulated tests.

A positive verdict requires evidence appropriate to the declared attacker model, deployment assumptions, Protected Effect, and assessment scope.

If the available evidence cannot establish enforcement at the merchant-side commitment boundary, the result must remain INSUFFICIENT_EVIDENCE.

No discovery run is authorised until the target specification, attacker model, assessment scope, and applicable preregistration gates have been reviewed and accepted by the trial owner.
