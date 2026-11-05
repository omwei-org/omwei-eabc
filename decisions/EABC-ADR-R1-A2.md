# EABC Specification Decision R1-A2

**Decision ID:** EABC-ADR-R1-A2  
**Title:** Scope of the Qualified-Independence Terminology Rule  
**Parent Decision:** EABC-ADR-R1 (supplements R1 §5)  
**Authority:** EABC Specification Authority  
**Status:** ACCEPTED  
**Outcome:** ACCEPTED  
**Proposal date:** 2026-11-04

## 1. Purpose and status

This addendum clarifies the scope of the terminology rule in ADR R1 §5, which states:

> These terms shall not be used interchangeably. The bare word "independent" shall not be used in normative text without one of these qualifiers.

The post-migration consistency audit of baseline `a4694af887ce4360c330bd5af76da9225b7dfa88` (finding F-02) found unqualified uses of "independent" in normative text of EABC 001–005, for example "independent assessor", "independent consumer", "independent verification", and "independent implementations". Read literally, R1 §5 prohibits them. Most of them do not denote any of the three meanings of independence that R1 §5 defines.

A2 is an authority decision record. It is non-normative; normative changes follow separately in `docs/`. A2 does not amend or overwrite R1, which remains the historical record. A2 does not modify any definition of R1 or A1.

## 2. Decision

### 2.1 The three qualified terms are unchanged

The three meanings of independence defined in R1 §5 remain exactly:

1. Authority-Origin Independence (P1);
2. Enforcement Independence (EBP assurance);
3. Non-Parallelism (within `EXCLUSIVITY(A,E,I)`).

Where one of these meanings is intended, normative text MUST use the qualified term. The unqualified word "independent" or "independence" MUST NOT be used in normative text to denote any of these three meanings.

### 2.2 General-language use is outside the rule

The rule in R1 §5 does not apply to the use of "independent" in its ordinary sense to describe a party, artifact, implementation, activity, or process in relation to another identified party, artifact, implementation, or process, provided that the use does not denote any of the three meanings in §2.1.

In such use, the normative text SHALL make the reference party, artifact, implementation, activity, or process determinable from the text or its immediate context. Where a general-language use could reasonably be read as one of the three qualified meanings, the text SHOULD use "third-party" or explicitly identify the reference instead of "independent".

### 2.3 Retained names

Existing property names and section headings in EABC documents (for example the original title of P1 and the section heading "Independent Verification") are retained as names. Where such a name corresponds to one of the three qualified terms, the qualified term governs its meaning. A2 does not rename any property or section.

### 2.4 Matters not decided

A2 does not decide whether the EBP-006 Required Boundary Property labelled "Independence" is to be identified as `ENFORCEMENT_INDEPENDENCE` or relabelled. That remains a matter for the EBP assurance alignment.

### 2.5 Effect on existing text

1. No mandatory rewrite of existing general-language uses is required by A2.
2. A single editorial alignment of EABC 001 §3 is authorized, replacing the sentence "The term "independence" has three distinct meanings and MUST NOT be used without its qualifier in normative text." with:

> The qualified terms Authority-Origin Independence, Enforcement Independence, and Non-Parallelism MUST be used, without abbreviation, wherever one of these three meanings is intended. The unqualified word "independent" MUST NOT be used in normative text to denote any of these meanings. General-language uses (for example "third-party assessor") are not affected, provided the reference is determinable from context.

3. New or revised normative text SHALL follow §2.1–§2.3 from the date of acceptance.
4. Each general-language use that could reasonably be read as one of the three qualified meanings SHOULD be reworded when its section is next revised. This does not apply to retained property names and section headings under §2.3.

### 2.6 Exclusions

A2 does not introduce a new property, definition, or requirement. It does not change EABC conformance, the P1–P10 reconciliation of A1, or any evidence record. It does not authorize editing any document other than the editorial alignment in §2.5(2).

## 3. Decision register

| ID | Decision | Alternatives | Recommendation |
| --- | --- | --- | --- |
| A2-D01 | Scope of the R1 §5 rule | Literal: prohibit all unqualified uses; or limit to the three defined meanings | Limit to the three defined meanings (§2.1–§2.2) |
| A2-D02 | General-language uses | Prohibit; or allow with a determinable reference | Allow, with the reference determinable; prefer "third-party" or explicit identification when ambiguous |
| A2-D03 | Retained names | Rename now; or retain names and headings with the qualified term governing meaning | Retain (§2.3) |
| A2-D04 | EBP-006 "Independence" label | Decide here; or defer to EBP alignment | Defer (§2.4) |
| A2-D05 | Existing text | Mandatory rewrite; or one editorial alignment of 001 §3 plus rewording on next revision | One editorial alignment (§2.5) |

## 4. Annex (non-normative) — classification of the uses found by the audit

The following classification is confirmed against the authorized editorial change.

| Use | Proposed classification |
| --- | --- |
| "independent assessor" (e.g. EABC 004 §3.3.1) | General-language; reference: the implementer being assessed. It describes the sufficiency of evidence for a third party. It does not introduce a requirement for assessor independence (A1 Annex B.2). SHOULD be reworded to "third-party assessor" on the next revision of that section. |
| "independent consumer" | General-language; reference: the producer of the evidence. |
| "independent verification" | General-language (activity); reference: the producer of the evidence. Also a retained section heading (§2.3). |
| "independent implementations" | General-language; reference: the reference implementation. |
| P1 title "Independent Execution Authority" | Retained name; the qualified term Authority-Origin Independence governs. |
| "Independence" in EBP-006 | Not decided (§2.4). |

## 5. Authority response

**Outcome:** ACCEPTED  
**Authority:** EABC Specification Authority  
**Decision date:** 2026-11-05  
**Accepted amendments:** A2-D01 through A2-D05, without amendment.  
**Rationale:** The rule in R1 §5 is limited to the three qualified technical meanings of independence. Ordinary general-language uses remain permissible where their reference is determinable and they do not denote one of those meanings. Retained property names and section headings remain unchanged. The EBP-006 "Independence" label is deferred to EBP assurance alignment. The authorized editorial alignment is limited to EABC 001 §3 as specified in §2.5(2).
