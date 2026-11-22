# ARD-TRIAL-01 — Browsa A/S Recorded Owner Decision

**Status:** OWNER DECISION RECORDED — ACCEPTED FOR TRIAL 1 INPUT PREPARATION; NOT A DISCOVERY AUTHORISATION.  
**Decision date:** 2026-11-22  
**Decision authority:** Trial 1 Owner  
**Target:** Browsa Open Shopping Agent `browsa-io/open-shopping-agent`  
**Pinned revision:** `b9ad9d38f01acaed5038b5b59b6981ef7aab65a6` (`0.2.1`)  
**Related specification:** `ARD-TRIAL-01-BROWSA-TARGET.md`  
**Decision provenance:** Explicit owner confirmation in the Trial 1 planning conversation on 2026-11-22; this document records that confirmation.  
**Method baseline:** ARD-001 v0.3, pinned in `ARD-TRIAL-01.md`. This decision does not amend that baseline.

## 1. Accepted attacker-model disposition (A)

A describes adversarial capabilities available to an actor within the declared target/instance scope. Acceptance of a candidate capability does not assert that the capability is unrestricted or that a corresponding route is exploitable in the pinned implementation. Each capability must be bounded by actual interfaces, permissions, principals and trust boundaries.

| Candidate | Owner decision | Accepted scope / condition |
|---|---|---|
| A1 — adversarial or compromised agent/model output | **ACCEPT, bounded** | Model/agent output is treated as adversarially influenceable. The capability is limited to actions reachable through actual tools and permissions; it does not imply unrestricted host or browser access. |
| A2 — malicious or compromised MCP client | **ACCEPT, bounded** | Applies only to MCP interfaces actually exposed in the target instance. The effective exposure, authentication and caller privileges must be established and recorded; do not assume MCP exposure merely from the presence of MCP code. |
| A3 — attacker-controlled merchant-page content | **ACCEPT, bounded** | Merchant-page content is treated as untrusted input that may influence agent/browser decisions. Page content is not assumed to invoke privileged operations directly. |
| A4 — browser/session manipulation | **NARROW** | Include only manipulation through concrete, demonstrable in-scope interfaces or control paths and permissions. `sameBrowser: true` remains a priority investigation area, not proof that an actor has the required capability. |
| A5 — adapter faults | **OUTSIDE A** | Retain as a candidate failure class / route source. If an in-scope actor can induce or exploit an adapter fault, represent the actor capability separately and preserve the causal chain. |

### 1.1 Exclusions

The owner accepts the following exclusions for this Trial 1 scope:

- **Direct compromise of the merchant backend/payment processor independent of Browsa — EXCLUDE.**
- **Unrestricted administrative compromise of the target host/OS or deployment operator — EXCLUDE.**
- **Physical access — EXCLUDE.**

These exclusions define the accepted attacker model; they do not authorise deletion of discovered candidate routes. If discovery identifies such routes, retain them in the route register as **Out of scope**, with the applicable exclusion and rationale recorded. If the selected instance or evidence later shows that an excluded capability is in fact part of the intended scope, the owner model must be revisited before discovery proceeds.

## 2. Accepted evidence scope (S)

**Owner decision: ACCEPT — pinned-source + local-reproduction assessment.**

The scope is limited to the pinned source revision and locally reproducible evidence. It is not expanded to a production/deployment assessment or to merchant-side commitment evidence.

### 2.1 Included evidence

- Static inspection of the pinned source revision.
- Call-graph and interface-path analysis.
- Unit tests, fixtures, test configuration and locally reproducible tests.
- Inspection of source-declared browser-control and AI fallback capabilities.
- Review of CLI, web and MCP entry points.
- Fakes, mocks and saved pages, with exact artifacts and limitations retained.

### 2.2 Explicitly outside the accepted evidence scope

- Production or staging deployment assessment.
- Effective runtime configuration of an owner-identified deployment.
- Authorised real-merchant transaction testing.
- Independent merchant-side records showing that a test order was accepted and committed.
- Independent deployment evidence of effective browser-session permissions/isolation beyond source and local tests.

### 2.3 Consequences and limits

1. Fake/saved-page tests establish behaviour of the fixture and exercised code, not merchant-side commitment.
2. A local confirmation page or order number is not independent evidence of E unless correlated to an authoritative merchant record.
3. Source, simulation and deployment evidence must be labelled separately.
4. Routes requiring evidence unavailable within S remain open if they cannot be validated within this scope.
5. A target-level **CONFORMS** conclusion for merchant-side E is not supportable solely from source inspection and local simulation. Unless implementation/deployment assumptions and E are independently established, the target-level result remains **INSUFFICIENT_EVIDENCE**.
6. This S still permits Trial 1 to evaluate ARD's discovery and classification method; it limits the target-level conclusion.

Any future expansion to deployment or merchant-side evidence requires a separate explicit scope decision before the relevant preregistration is frozen. Both paired discovery conditions must use the same declared S.

## 3. Owner decision record and remaining start gates

The following A/S decisions are accepted and recorded by this document:

- [x] A1 accepted, bounded.
- [x] A2 accepted, bounded; actual MCP exposure, authentication and caller privileges remain facts to establish, not assumptions.
- [x] A3 accepted, bounded.
- [x] A4 narrowed to concrete, demonstrable in-scope browser/session control paths; `sameBrowser: true` is an investigation priority, not an assumed capability.
- [x] A5 excluded from A and retained as a candidate failure class / route source.
- [x] Direct independent merchant-backend/payment-processor compromise excluded.
- [x] Unrestricted host/OS administrative compromise excluded.
- [x] Physical access excluded.
- [x] S accepted as pinned-source + local-reproduction; no production/deployment or merchant-side commitment evidence expansion.

**This decision closes the A/S owner-review items only.** It does not freeze the preregistration, satisfy the paired-input gate, set or satisfy saturation criteria, or authorise any discovery run. All other ARD-TRIAL-01 start gates remain independently applicable.

## 4. Explicit non-claims

This decision does not assert that A1–A4 are exploitable in the pinned implementation, that `sameBrowser: true` is a bypass, that an adapter fault is itself an attacker, or that Browsa is conformant/non-conformant. It does not change ARD-001 v0.3, independently validate a bypass, or resolve any ARD-001 ambiguity beyond the operational interpretation separately recorded in the preregistration.

