# EABC Erratum R1-A2-E1

**Decision ID:** EABC-ADR-R1-A2-E1
**Title:** Interpretation note on A2 §2.1–§2.3 for quotations and defining sentences
**Parent Decision:** EABC-ADR-R1-A2
**Authority:** EABC Specification Authority
**Status:** PROPOSED
**Outcome:** PENDING AUTHORITY REVIEW
**Proposal date:** 2026-11-05

## 1. Purpose and status

The closeout audit of baseline `40ed665b8e9dde462bdfa824ee001e211fc714d9` (finding F-02) found occurrences of the word "independent" in `docs/001` that relate to the trust domain of execution authority. This erratum records how A2 §2.1–§2.3 apply to those occurrences and records which sentences are deferred for rewording under A2 §2.5(4).

This erratum is a non-normative decision record. It does not amend or overwrite A2, which remains the accepted decision of record. It does not change A2-D01 to A2-D05, does not change any normative text, and does not authorize editing any document.

## 2. Interpretation

### 2.1 Verbatim quotations of the original P1 obligation

A verbatim quotation of the original P1 obligation, presented as a quotation or as the preserved original text, is not a use of "independent" to denote one of the three qualified meanings within A2 §2.1. The original P1 obligation is preserved by A1 §4.1 and R1 §6, and A2 §2.3 retains existing names.

### 2.2 Defining sentences

A sentence that defines a qualified term (for example the definition of Authority-Origin Independence) uses "independent" within the definiens, to describe the relationship of one trust domain to another identified trust domain. This is a general-language use with a determinable reference under A2 §2.2. It does not use the unqualified word in place of the qualified term.

### 2.3 Table entries naming the qualified term

An occurrence in a table cell whose row or label cell contains the qualified term (or "P1") is a description of that named term. It is within A2 §2.2.

### 2.4 Sentences in which the word stands for the concept

A sentence in which "independent" or "independent trust-domain" stands in for the concept, instead of naming the qualified term, is within the scope of A2 §2.5(4): it SHOULD be reworded to name Authority-Origin Independence when its section is next revised.

## 3. Classification of the occurrences

The classification below applies the criteria in §2.1–§2.4 to the occurrences in `docs/001` that appear in a sentence or cell also containing "trust domain" or "trust-domain".

Classes: Q = verbatim quotation of the original P1 obligation; D = defining sentence; T = table entry naming the qualified term; C = sentence in which the word stands for the concept.

| # | Section | Class | Verbatim quote |
| --- | --- | --- | --- |
| 1 | §2, P1 — Independent Execution Authority | Q | Execution authority MUST originate from a trust domain that is independent of the governed execution domain. |
| 2 | §4.1 Original P1 obligation | Q | Execution authority MUST originate from a trust domain that is independent of the governed execution domain. |
| 3 | §4.2 Authority-Origin Independence | D | Execution authority MUST originate from a trust domain that is independent of the governed execution domain. |
| 4 | §4.2 Authority-Origin Independence | C | A request submitted to, or authority granted by, an entity that originates from an independent trust domain and is entitled to grant it is not self-authorization. |
| 5 | §4.2 Authority-Origin Independence | C | The independent trust-domain relationship remains part of the requirement. |
| 6 | §5.2 Relationship to EBP assurance constraints | T | Assurance qualification concerning the enforcement mechanism's independence from the governed actor's trust domain or failure modes |
| 7 | §5.3 P1–P10 reconciliation | T | Preserve the independent trust-domain origin requirement and anti-self-authorization. Map bypass to `NON_BYPASSABILITY`. Retain unauthorized modification of established execution authority as an explicit P1 sub-obligation. |
| 8 | §3 Terminology and separation from EBP assurance | T | Execution authority originates from a trust domain independent of the governed execution domain; the governed system cannot self-authorize. |

## 4. Deferred rewording (A2 §2.5(4))

- §4.2 Authority-Origin Independence: "A request submitted to, or authority granted by, an entity that originates from an independent trust domain and is entitled to grant it is not self-authorization."
- §4.2 Authority-Origin Independence: "The independent trust-domain relationship remains part of the requirement."

No change to `docs/001` is made or authorized by this erratum. The listed sentences are to be reworded when their section is next revised under the normal change process.

## 5. Matters not decided

This erratum does not decide the EBP-006 "Independence" label (A2 §2.4), does not change the classification of any occurrence outside the scope described in §3, and does not alter A1 or A2.

## 6. Authority response

**Outcome:** PENDING
**Authority:** EABC Specification Authority
**Decision date:** Pending
