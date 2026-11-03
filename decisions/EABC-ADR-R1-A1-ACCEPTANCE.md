# EABC-ADR-R1-A1 — Author Approval and Review Closure

**Status:** APPROVED — REVIEW CLOSED  
**Decision date:** 2026-11-03  
**Decision authority:** EABC Specification Authority  
**Authority holder:** Specification author  
**Approved artifact:** `decisions/EABC-ADR-R1-A1.md`  
**Approved artifact commit:** `f44655d5d061f61658a7dc4503f5d3183af77430`

## 1. Decision

The specification author, acting as the authority holder for this decision, approves EABC-ADR-R1-A1 at the exact commit identified above and closes its review phase.

The approval adopts the document's operative treatment of D01–D23 and resolves the three authority questions in Annex B as follows.

## 2. Annex B authority decisions

### B.1 — INTEGRITY_DEF

**Adopted: Option A.**

The required protection is prevention of unauthorized modification or substitution within the declared threat model. Detection alone is not an equivalent substitute for this requirement.

### B.2 — N/A acceptance

**Adopted: transparent implementer self-acceptance is permitted.**

An implementer may accept an N/A disposition when it is explicitly identified, transparently documented, and justified against the applicable requirement and scope. This decision does not impose a universal independent-assessor requirement.

### B.3 — P1 authority-change procedure

**Adopted: protocol details may remain implementation- or profile-specific.**

No universal authority-change protocol is introduced by this decision. The normative P1 obligation remains in force; implementation/profile specificity does not waive or weaken it.

## 3. Effect and boundaries of approval

This approval:

- approves A1 at the exact commit identified above;
- closes the A1 review phase;
- adopts the three Annex B decisions stated in Section 2;
- leaves the A1 normative text unchanged;
- does not itself amend EABC 001–004 or EBP-006;
- does not claim implementation, deployment, SLC-substrate, or EBP-assurance conformance;
- does not authorize or perform the subsequent normative migration.

Any coordinated migration of EABC 001–004, EBP alignment, implementation-profile work, or EAP Binding/R2 work remains a separate, explicitly scoped activity.

## 4. Audit basis

The approval is based on the completed read-only review of A1 at commit `f44655d5d061f61658a7dc4503f5d3183af77430`, whose verdict was **READY WITH EXPLICIT AUTHORITY DECISIONS**. The review identified no CRITICAL or MAJOR defect and no mandatory document edit before authority disposition.

The audit was not itself the authority approval. This record captures the subsequent explicit approval and the author's decisions on Annex B.

## 5. Closure

**EABC-ADR-R1-A1: APPROVED.**  
**A1 review: CLOSED.**

The approved A1 artifact remains immutable at the referenced commit for the purpose of this decision. Any later amendment must be handled as a separately versioned change and reviewed accordingly.
