# ARD-TRIAL-01 — Browsa A/S Owner Review Proposal

**Status:** PROPOSAL FOR TRIAL-OWNER REVIEW — NOT ACCEPTED, NOT FROZEN.  
**Target:** Browsa Open Shopping Agent `browsa-io/open-shopping-agent`  
**Pinned revision:** `b9ad9d38f01acaed5038b5b59b6981ef7aab65a6` (`0.2.1`)  
**Related specification:** `ARD-TRIAL-01-BROWSA-TARGET.md`  
**Purpose:** Make the remaining attacker-model (A) and evidence-scope (S) decisions explicit. This note does not authorise discovery.

## 1. Recommended disposition of A

A should describe adversarial capabilities available to an actor in the declared target/deployment scope. It should not silently assume that a capability exists merely because a code path or component is present.

| Candidate | Recommendation | Rationale / condition |
|---|---|---|
| A1 — adversarial or compromised agent/model output | INCLUDE, bounded | Treat model/agent output as adversarially influenceable. Do not assume unrestricted host or browser access; record only actions reachable through actual tools and permissions. |
| A2 — malicious or compromised MCP client | INCLUDE if MCP is exposed in the target scope | The actor may issue unexpected, repeated, malformed, reordered, or adversarially timed requests. Record the actual authentication and caller privilege assumptions. |
| A3 — attacker-controlled merchant-page content | INCLUDE, bounded | Treat page content as untrusted input that may influence agent/browser decisions. Do not assume page content itself can invoke privileged operations. |
| A4 — browser/session manipulation | INCLUDE only through demonstrated in-scope control paths | The actor's ability to change page/session state must be tied to a concrete exposed interface or control path. `sameBrowser: true` is a priority investigation point, not proof of attacker capability. |
| A5 — adapter faults | DO NOT model as a standalone attacker capability | Record adapter errors and incorrect state interpretation as candidate failure classes/routes. If an in-scope actor can induce or exploit one, model that actor capability separately and preserve the causal chain. |

**Proposed exclusions for explicit owner decision:**
- Direct compromise of the merchant backend/payment processor independent of Browsa.
- Unrestricted administrative compromise of the target host/OS or deployment operator.
- Physical access, unless relevant to the selected deployment and supported by an in-scope route.

An exclusion must be justified against the selected deployment and interface inventory. It does not mean that routes are deleted: routes outside accepted A remain in the register as Out of scope, with the reason recorded, consistent with the interpretation proposed in Section 2.1 of `ARD-TRIAL-01.md`.

### Required owner decision

The trial owner must record one disposition for each A1–A4 (accept / narrow / reject), confirm or revise each proposed exclusion, and identify the relevant principals, trust boundaries, interfaces, and assumptions. The owner must also confirm whether MCP is part of the target instance and whether the browser/session control paths are available to any actor included in A.

No assessor or discovery model may make these decisions on the owner's behalf.

## 2. Recommended disposition of S

The currently supportable scope is a **pinned-source and local-reproduction assessment**, not a production deployment assessment.

### Included evidence

- Static inspection of the pinned source revision.
- Call-graph and interface-path analysis.
- Unit tests, fixtures, test configuration and locally reproducible tests.
- Inspection of source-declared browser-control and AI fallback capabilities.
- Review of CLI, web and MCP entry points.
- Fakes, mocks and saved pages, with exact artifacts and limitations retained.

### Not currently available / not established

- An owner-identified production or staging deployment with pinned effective runtime configuration.
- An authorised real-merchant test arrangement.
- Independent merchant-side records showing that a test order was accepted and committed.
- Independent deployment evidence of effective browser-session permissions/isolation beyond source and local tests.

### Consequences

1. Fake/saved-page tests establish behaviour of the fixture and exercised code, not merchant-side commitment.
2. A local confirmation page/order number is not independent evidence of E unless correlated to an authoritative merchant record.
3. Source, simulation and deployment evidence must be labelled separately.
4. Routes requiring unavailable deployment or merchant-side evidence remain open if they cannot be validated within S.
5. Under this S, a target-level CONFORMS conclusion for merchant-side E is not supportable solely from source inspection and local simulation. Unless implementation/deployment assumptions and E are independently established, the target-level result remains INSUFFICIENT_EVIDENCE.
6. This does not prevent Trial 1 from evaluating ARD's discovery/classification method; it limits the target-level conclusion.

If the owner wants Trial 1 to assess a real deployment or establish merchant-side E, S must be expanded before freeze to identify the deployment, effective configuration, authorised test environment, transaction-observation method and independent evidence source. The same declared S must be supplied to both paired discovery conditions.

## 3. Required owner decisions before preregistration freeze

- [ ] A1 accepted, narrowed or rejected with rationale.
- [ ] A2 accepted, narrowed or rejected; MCP exposure/authentication assumptions recorded.
- [ ] A3 accepted, narrowed or rejected with rationale.
- [ ] A4 accepted, narrowed or rejected; concrete browser/session control paths identified or explicitly left as questions for discovery without asserting attacker capability.
- [ ] A5 moved out of A and retained as a candidate failure-class/route source, or an alternative rationale recorded.
- [ ] Proposed exclusions accepted or revised with deployment-specific rationale.
- [ ] S accepted as pinned-source/local-reproduction scope, or expanded with concrete deployment and merchant-side evidence arrangements.
- [ ] Owner identity/role, decision date, target version and decision references recorded in the preregistration/input provenance register.

Until these decisions are recorded and all other start gates are met, the preregistration remains PROPOSED — NOT FROZEN and no discovery run is authorised.

## 4. Explicit non-claims

This proposal does not assert that A1–A4 are exploitable in the pinned implementation, that `sameBrowser: true` is a bypass, that an adapter fault is an attacker, or that Browsa is conformant/non-conformant. It does not change ARD-001 v0.3 or resolve its ambiguity beyond the operational interpretation already proposed in the preregistration.
