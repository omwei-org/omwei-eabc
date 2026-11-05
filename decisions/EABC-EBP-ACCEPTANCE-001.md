# EBP v0.2.3 — Authority Acceptance Record

**Decision ID:** EABC-EBP-ACCEPTANCE-001  
**Title:** Acceptance of the Execution Boundary Profile Assurance Framework  
**Authority:** EABC Specification Authority  
**Status:** ACCEPTED  
**Outcome:** ACCEPT  
**Decision date:** 2026-11-05  
**Accepted specification:** EBP v0.2.3  
**Normative document:** [docs/006 — Execution Boundary Profile](../docs/006-execution-boundary-profile.md)

---

## 1. Decision

The EABC Specification Authority ACCEPTS EBP v0.2.3 as the Execution Boundary Profile assurance framework.

The accepted version is the consolidated EBP v0.2.3 text submitted for Authority decision on 2026-11-05, incorporating the corrections identified in the adversarial consistency review ADV-01 through ADV-05.

This record documents the Authority decision. The normative requirements of EBP are published in `docs/006-execution-boundary-profile.md`.

## 2. Scope of acceptance

Acceptance confirms the following design decisions:

1. EBP qualifies assurance of concrete SLC realizations without prescribing or selecting their implementation substrate.
2. The five EABC boundary semantic properties remain unchanged and remain subject to EABC assessment.
3. P3 remains an EABC semantic obligation and is not an additional value of the EBP `property` field.
4. `ENFORCEMENT_INDEPENDENCE` retains its established assurance meaning and remains distinct from Authority-Origin Independence and Non-Parallelism.
5. EBP profile applicability, selection, composition, and missing-profile handling follow the rules in EBP v0.2.3.
6. Absence of an additional EBP profile obligation does not automatically establish `CONFORMANCE_ELIGIBLE`.
7. The existing `CONFORMANCE_ELIGIBLE` and `VALID_COMMIT` expressions are preserved.
8. EBP assurance remains distinct from EABC conformance levels and EABC property assessment.
9. EBP Assurance Evidence remains instance-/assessment-scoped and distinct from transaction-scoped EABC evidence.
10. Boundary Evidence Binding applies the EABC 002 Intrinsically Bound principle to the specified cross-evidence correlation.

## 3. Authority limitations and retained open items

This acceptance does not amend or supersede EABC 001–004, EABC-ADR-R1, EABC-ADR-R1-A1, or EABC-ADR-R1-A2.

The following matters remain open for future Authority decision, as recorded in EBP v0.2.3 §11.2:

- whether an EAT-based attestation representation should be standardized as a recommended profile or remain optional;
- whether common material-change categories should be standardized beyond the requirement to reassess changes affecting a claimed guarantee.

These open items do not suspend acceptance of EBP v0.2.3 and MUST NOT be interpreted as permission to weaken its accepted requirements.

## 4. Repository publication

The Authority decision and the normative EBP text are synchronized to the repository through a dedicated pull request.

Repository publication records the accepted specification; it does not create a second acceptance event.

The accepted normative text is identified by version, not by an assumption that any earlier draft or historical EBP-006 text has been silently rewritten.

---

**Authority outcome: ACCEPTED**  
**Specification status: EBP v0.2.3 — ACCEPTED**
