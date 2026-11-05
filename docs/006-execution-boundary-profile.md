# 006 — Execution Boundary Profile (EBP)

**Version:** 0.2.3  
**Status:** Accepted by EABC Specification Authority  
**Document role:** EBP assurance framework  
**Normative dependencies:** EABC 001–004; EABC-ADR-R1; EABC-ADR-R1-A1; EABC-ADR-R1-A2

---

## 1. Purpose and scope

### 1.1 Purpose

The Execution Boundary Profile (EBP) defines an assurance layer for evaluating whether a concrete execution-boundary realization provides the assurance required by an applicable contract or execution policy.

EBP specifies:

- which additional assurance requirements apply to a declared execution-boundary property;
- which adversary model and guarantee those requirements address;
- which assurance constraints must hold;
- what evidence is required to assess the concrete realization; and
- whether the resulting assurance remains valid for the assessed instance and deployment.

EBP does not redefine EABC properties, create execution authority, or prescribe the implementation substrate.

### 1.2 Relationship to EABC

EABC defines the normative execution-authority obligations and the five boundary semantic properties.

EBP qualifies the assurance of a concrete implementation against declared assurance requirements. It does not replace EABC assessment or establish EABC conformance by itself.

The following distinctions are normative:

1. EABC defines what must be satisfied.
2. An applicable EBP profile specifies additional assurance requirements for a declared property.
3. The SLC implementation realizes the required enforcement behavior using a concrete architecture and substrate.
4. Assessment evaluates the concrete realization and its evidence against EABC and applicable EBP requirements.

EBP assurance tiers MUST NOT replace, waive, or silently redefine EABC requirements or conformance levels.

### 1.3 Implementation neutrality

EBP MUST NOT prescribe a particular substrate or rank substrates as universally stronger or weaker.

A substrate is a characteristic of the concrete SLC realization, not a property selected by EBP.

Possible realizations include, without limitation:

- software enforcement;
- a Trusted Execution Environment (TEE);
- an MCU combined with a Secure Element;
- FPGA, ASIC, or a hardware enforcement co-processor;
- ISA- or processor-pipeline-level enforcement; and
- hybrid realizations combining multiple mechanisms.

These examples are implementation possibilities, not EBP profiles, assurance tiers, or presumptive conformance outcomes.

The suitability of a realization MUST be assessed against the applicable EABC requirements, adversary model, guarantee, assurance constraints, and deployment assumptions.

### 1.4 Concrete realization under assessment

The object of an EBP assurance assessment is a concrete realization:

`R = (SLC, substrate, configuration, deployment assumptions)`

The assessment MUST identify the realization sufficiently to establish what was evaluated.

A statement that a substrate is generally secure, isolated, certified, or tamper-resistant does not by itself establish that the concrete realization satisfies an EBP profile.

A change to the SLC, substrate, configuration, or a deployment assumption that is material to a claimed guarantee MUST trigger reassessment of the affected assurance claims. Previously recorded assessment results MUST NOT be presumed valid for a materially changed realization.

---

## 2. EBP assurance profile

### 2.1 Profile structure

An EBP assurance profile is a versioned specification of assurance requirements.

The profile is represented by:

`EBP = {property, adversary_model, guarantee, assurance_constraints}`

Where:

- `property` identifies the EABC boundary semantic property whose assurance is being qualified;
- `adversary_model` identifies the adversary capabilities, trust assumptions, and relevant scope;
- `guarantee` states the assurance claim required against that adversary model; and
- `assurance_constraints` identify the additional constraints that the realization and its deployment must satisfy.

The `property` field MUST identify one of the five EABC boundary semantic properties:

1. `NON_BYPASSABILITY(B,E)`
2. `INTEGRITY_DEF(B)`
3. `INTEGRITY_STATE(B,E)`
4. `INTEGRITY_CTX(C,B,E)`
5. `EXCLUSIVITY(A,E,I)`

An EBP profile MUST NOT introduce a sixth EABC boundary semantic property or redefine the normative meaning of an existing property.

### 2.2 Adversary model

Each profile MUST identify the adversary model against which its guarantee is claimed.

The adversary model MUST be sufficiently specific to identify:

- adversary capabilities;
- relevant trust assumptions;
- protected effect and boundary scope, where applicable;
- components, interfaces, and execution paths within the assessment scope; and
- relevant exclusions or residual risks.

A generic threat-model label without a declared relationship to the assessed realization and property is insufficient.

The adversary model is an assessment parameter. It does not prescribe a substrate or implementation mechanism.

### 2.3 Guarantee

The guarantee MUST state what the assessed realization is required to establish against the declared adversary model.

A guarantee MUST be assessable against evidence. Statements of design intent, product capability, certification status, or vendor assurance alone MUST NOT be treated as proof that the guarantee is satisfied.

The guarantee MUST NOT exceed what the declared adversary model, evidence, and assessment scope support.

### 2.4 Assurance constraints

Assurance constraints specify additional conditions under which the guarantee is claimed.

Assurance constraints MAY address, where relevant:

- enforcement independence;
- temporal consistency;
- maximum enforcement latency;
- freshness and validity;
- instance identity and binding;
- configuration integrity;
- deployment assumptions; and
- other profile-specific assurance conditions.

A constraint MUST identify its scope and the claim it qualifies.

A constraint MUST NOT be presented as a new EABC boundary semantic property unless separately adopted through the EABC specification authority process.

### 2.5 Required qualified terminology

The following three meanings MUST remain distinct:

1. **Authority-Origin Independence** — the P1 authority-origin requirement.
2. **Enforcement Independence** — the EBP assurance meaning concerning whether the boundary's admit/refuse decision is controllable by the party whose action is being evaluated.
3. **Non-Parallelism** — the absence of a Parallel Commit Authority within `EXCLUSIVITY(A,E,I)`.

Where one of these meanings is intended, normative text MUST use its qualified term.

The unqualified words "independent" and "independence" MUST NOT be used in normative text to denote any of these three meanings.

General-language uses are permitted where the reference is determinable and the use does not denote one of the three qualified meanings. Where ambiguity is reasonably possible, wording such as "third-party" or an explicit reference SHOULD be used.

The historical EBP-006 Required Boundary Property label `Independence` is reconciled to the qualified term `ENFORCEMENT_INDEPENDENCE`.

The existing EBP-006 definition of the underlying assurance meaning is retained unless expressly amended by the applicable specification authority. This terminology reconciliation does not introduce a sixth EABC boundary semantic property.

---

## 3. Relationship to EABC semantic requirements

### 3.1 Five boundary semantic properties

EBP profiles qualify assurance for one or more of the five EABC boundary semantic properties. They MUST NOT replace the EABC assessment of those properties.

The normative definitions remain in EABC 001 and the accepted decisions R1 and A1.

In particular:

- `NON_BYPASSABILITY(B,E)` concerns complete mediation of every in-scope path capable of producing the Protected Effect.
- `INTEGRITY_DEF(B)` concerns authenticity and integrity of the applicable boundary definition, including its binding to the deciding boundary instance.
- `INTEGRITY_STATE(B,E)` concerns authenticity and integrity of the runtime state used by the boundary in its determination.
- `INTEGRITY_CTX(C,B,E)` concerns the authenticity, provenance, and binding of execution context to the boundary and Protected Effect.
- `EXCLUSIVITY(A,E,I)` concerns the absence of a Parallel Commit Authority for the same Protected Effect, scope, and Authority Interval.

An EBP assurance result for one property MUST NOT automatically establish another property.

### 3.2 NON_BYPASSABILITY and Enforcement Independence

A `NON_BYPASSABILITY(B,E)` assessment MUST declare the applicable `ENFORCEMENT_INDEPENDENCE` qualification as a separate EBP assurance qualification, as required by ADR R1.

The qualification does not alter the semantic definition of `NON_BYPASSABILITY` and MUST NOT be treated as evidence of path completeness or boundary mediation.

A semantic `NON_BYPASSABILITY` claim with an unspecified `ENFORCEMENT_INDEPENDENCE` qualification MAY be recorded as such. It MUST NOT be used to assign an assurance tier or make a conformance assertion that depends on that qualification until the applicable level has been declared and assessed.

The assessment MUST continue to establish both evidence dimensions required by EABC 001:

1. deployment-topology completeness; and
2. boundary mediation.

Neither dimension substitutes for the other.

### 3.3 P3 and temporal assurance

P3 — Deterministic Commit Semantics — remains an EABC semantic obligation.

It includes the required deterministic interpretation of the authorization and execution transition and check-to-effect atomicity: there MUST NOT be a gap between the decision and the effect it authorizes.

`TEMPORAL_CONSISTENCY` and `MAX_ENFORCEMENT_LATENCY` are EBP assurance constraints. They MAY qualify the assurance of a concrete realization's satisfaction of P3.

They MUST NOT:

- replace P3;
- redefine P3;
- turn P3 into an EBP profile property;
- establish P3 solely by satisfying a timing threshold; or
- be treated as a substitute for the required execution-boundary semantics.

Where COMMIT and a subsequent external EFFECT are distinct stages, the assessment MUST address the check-to-effect atomicity required by P3. Atomicity of an authorization/commit transition alone does not establish atomicity between COMMIT and a subsequent external EFFECT.

For avoidance of doubt, P3 is not an additional value of the EBP `property` field.

An EBP profile MAY reference P3 as an EABC obligation when specifying relevant assurance constraints or evidence requirements. Such a reference does not make P3 an EBP profile property.

The applicable EABC P3 obligation MUST be assessed under its own normative meaning, independently of whether a corresponding EBP profile applies.

### 3.4 Integrity and freshness

`INTEGRITY_STATE(B,E)` establishes authenticity and integrity, not freshness.

An authentic state representation may be stale. Where freshness is required by the applicable threat model or contract, it MUST be specified and assessed as a separate assurance concern.

An EBP profile MAY specify freshness, validity, or state-age constraints. Such constraints MUST NOT be presented as a sixth EABC boundary semantic property or silently inserted into the definition of `INTEGRITY_STATE(B,E)`.

### 3.5 Context provenance and factual correctness

`INTEGRITY_CTX(C,B,E)` concerns context authenticity, provenance, and binding.

Provenance alone does not establish factual truth or correctness. Where factual validation or corroboration is required, the applicable requirement and validation basis MUST be specified separately.

An EBP profile MUST NOT collapse context provenance and factual correctness into one undifferentiated claim.

### 3.6 P5 correspondence

An EBP profile or assurance result concerning `INTEGRITY_STATE(B,E)` MUST NOT be treated as automatically establishing both original P5 obligations.

The original obligations remain distinct:

1. identification of the state against which authorization was evaluated; and
2. the consumer-facing ability to determine whether execution occurred against the intended reference state or condition, with the relationship between the two expressly bound to the authorization decision.

The second obligation MUST be assessed under the applicable EABC authorization and execution semantics. Evidence of state authenticity and determination-binding alone is insufficient.

---

## 4. Profile applicability and selection

### 4.1 Source of profile requirements

An EBP profile applies only where an applicable contract, Execution Boundary Policy, or other authoritative requirement expressly references that profile or otherwise establishes its applicability.

The source establishing profile applicability MUST be identifiable and versioned or otherwise unambiguously identifiable.

Execution Boundary Policy is an external policy input. It is not an EABC property and MUST NOT be used to waive or select away EABC property assessments.

Execution Boundary Policy MAY specify:

- which EBP profiles apply;
- the scope in which each profile applies;
- applicable profile versions;
- profile-specific parameters; and
- the rules governing profile applicability and reassessment.

### 4.2 Absence of a profile obligation

This version does not introduce a `NO_PROFILE_REQUIRED` status or enum.

Where no applicable contract or policy imposes an EBP profile obligation, the absence of a profile reference means only that no additional EBP profile obligation is imposed by that source.

This absence MUST NOT be interpreted as:

- an EABC property being inapplicable;
- an EABC property being satisfied;
- EABC conformance being established;
- a substrate being approved or unrestricted; or
- `CONFORMANCE_ELIGIBLE` being automatically satisfied.

The absence of a profile obligation does not remove the need to assess all applicable EABC requirements.

### 4.3 Missing required profile selection

Where an applicable contract or policy requires an EBP profile, but the required profile or its applicable version cannot be identified, the required assurance condition has not been established.

The EBP assessment MUST be recorded as `INDETERMINATE` for the affected requirement.

A missing required profile MUST NOT be interpreted as an absence of a profile obligation.

### 4.4 Profile selection record

Where EBP profiles apply, the assessment record MUST identify:

1. the authoritative contract or policy source;
2. its version or other unambiguous identity;
3. the applicable profile identifiers and versions;
4. the scope of applicability;
5. any required profile parameters; and
6. any unresolved applicability or selection condition.

This record MUST make it possible to distinguish an actual absence of a profile obligation from a missing or unresolved selection required by the applicable policy.

### 4.5 Multiple applicable profiles

Each applicable EBP profile MUST be assessed independently against its declared property, adversary model, guarantee, assurance constraints, and scope.

Where multiple profiles impose requirements on overlapping assessment scope, their applicable requirements are cumulative by default.

A contract or policy MAY expressly designate profiles as alternatives. Such designation MUST identify the alternative set and the applicable selection rule.

Profiles applying to different properties or non-overlapping scopes MUST NOT be treated as conflicting solely because they apply to the same SLC realization.

Where cumulative requirements within overlapping scope are incompatible or cannot be jointly evaluated, the affected assurance result MUST be `INDETERMINATE` until resolved by the authority responsible for the applicable contract or policy.

No profile may silently override, weaken, or waive an EABC requirement or another applicable profile requirement.

---

## 5. EBP conformance eligibility and validity

### 5.1 Separation of gates

EBP conformance eligibility remains a separate gate.

The existing logical expressions are retained:

```
CONFORMANCE_ELIGIBLE(i, c, t) :=
    ACCEPTABLE_CONFORMANCE_EVIDENCE(i, c, t)
    ∧ CONFORMANCE_VALIDITY_POLICY_SATISFIED(i, c, t)

VALID_COMMIT(a, i, c, t) :=
    CONFORMANCE_ELIGIBLE(i, c, t)
    ∧ FINAL_AUTHORITY_CHECK(a, c, t)
    ∧ COMMIT_CONDITIONS(a, c, t)
```

Where:

- `i` identifies the assessed implementation instance;
- `c` identifies the applicable contract or policy context; and
- `t` identifies the relevant assessment or evaluation time.

The three gates MUST NOT be merged.

In particular, `FINAL_AUTHORITY_CHECK` retains its EABC 003 scope. It MUST NOT be extended to carry EBP conformance-status logic.

Conformance establishes whether the execution-boundary implementation is eligible to serve the contract. It is not itself an authority decision and is not folded into `FINAL_AUTHORITY_CHECK`.

### 5.2 EBP assessment outcomes

EBP conformance status remains tri-state:

- `VALID`
- `INVALID`
- `INDETERMINATE`

For the purposes of `VALID_COMMIT`, `INDETERMINATE` is unacceptable and is treated as `INVALID`.

A missing or unresolved required profile, insufficient evidence, unresolved validity condition, or unresolved material change MUST NOT be treated as `VALID`.

The most restrictive applicable result governs. An assessment MUST NOT report `VALID` where a required dimension remains `INDETERMINATE` or `INVALID`.

### 5.3 Validity dimensions

The EBP validity assessment MUST preserve the distinction between:

1. temporal validity;
2. status and revocation validity; and
3. assessed-instance and relevant-state freshness/binding.

Each applicable dimension MUST be supported by evidence.

A validity period alone does not establish that the currently running instance is the instance assessed. Where instance identity is material to a claimed property, the assessment MUST establish the required binding between the assessment evidence and the running instance.

EBP does not prescribe a universal binding mechanism. The mechanism is implementation- and profile-dependent, provided it establishes the required guarantee.

### 5.4 Absence of profile obligations and the eligibility gate

The absence of an EBP profile obligation MUST NOT, by itself, be treated as a positive eligibility result.

Where the EBP gate is invoked, `ACCEPTABLE_CONFORMANCE_EVIDENCE` and `CONFORMANCE_VALIDITY_POLICY_SATISFIED` MUST each be evaluated under the applicable contract and validity policy.

The policy MUST make clear what evidence and validity conditions are sufficient where no additional EBP profile is imposed.

This document does not redefine either predicate or declare that an empty profile set automatically satisfies the gate.

A profile-applicability determination MUST be based on the complete set of authoritative requirements applicable to the declared contract and assessment scope.

The determination MUST identify the sources examined and the basis for concluding that no additional EBP profile obligation applies.

Absence of a profile reference in an incomplete, unidentified, or non-authoritative policy source MUST NOT establish that no profile obligation applies.

The profile-applicability determination is an assessment record, not a separate EBP conformance status.

It MUST NOT independently establish `CONFORMANCE_ELIGIBLE` or replace either predicate in the existing eligibility expression.

---

## 6. EBP assurance evidence and attestation

### 6.1 EBP Assurance Evidence

EBP Assurance Evidence is scoped to the assessed realization and its deployment.

It is distinct from transaction-scoped EABC evidence.

EBP Assurance Evidence MUST identify, as applicable:

- the assessed SLC implementation;
- the substrate and relevant components;
- configuration and deployment assumptions;
- the applicable EBP profiles and versions;
- the adversary model and guarantee;
- the assessment method and result;
- evidence supporting each applicable assurance constraint;
- validity and revocation information; and
- material changes affecting the assessment.

EBP Assurance Evidence does not become an additional transaction-scoped EABC evidence category.

### 6.2 Boundary Evidence Binding

Where an identifier correlates transaction-scoped EABC evidence with instance-scoped EBP Assurance Evidence, that identifier MUST be covered by the same Integrity Evidence that protects the evidence artifact in which it appears.

Correlation MUST NOT depend on an external mapping, index, or side channel that is not itself integrity-protected as part of the evidence artifact it correlates.

A consumer MUST be able to verify provenance and correlation directly from the protected evidence artifacts, without relying on a separately maintained and separately trusted correlation record.

This requirement applies the existing EABC 002 Intrinsically Bound principle to the relationship between transaction-scoped EABC evidence and instance-scoped EBP Assurance Evidence.

It does not create an additional EABC transaction evidence category.

### 6.3 Evidence reuse

A single evidence item MAY support more than one requirement.

It MUST independently establish each requirement's own normative meaning.

Evidence supporting an EBP assurance constraint MUST NOT automatically be treated as evidence satisfying an EABC property, and evidence satisfying an EABC property MUST NOT automatically establish an EBP assurance constraint.

### 6.4 EBP Assurance Attestation

An EBP Assurance Attestation MAY package claims about the assessed realization and its assurance status.

It is optional unless required by an applicable contract or profile.

An attestation:

- is a structured claim about an assessment;
- does not itself prove the truth of the claims;
- does not replace the underlying evidence;
- does not make a claimed `VALID` status authoritative without validity evaluation; and
- MUST be bound to the assessed realization and applicable assessment record.

EBP introduces no new cryptographic or attestation primitive. An EAT-based representation MAY be used where appropriate, but the format does not establish conformance by itself.

### 6.5 Assessor and acceptance

This document does not impose a universal assessor-independence or countersignature requirement.

Transparent implementer-performed assessment and self-accepted N/A remain subject to the accepted EABC 004 and A1 rules.

Any additional assessor qualification or third-party review requirement MUST be stated by the applicable contract or profile. It MUST NOT be inferred from the unqualified word "independent".

---

## 7. Relationship to Execution Boundary Policy and SLC architecture

### 7.1 Execution Boundary Policy

Execution Boundary Policy is an external input that identifies the applicable EBP assurance requirements for a deployment.

It MUST NOT select or waive the five EABC boundary semantic properties.

All five properties remain assessment subjects under EABC 004, subject only to the accepted N/A rules.

### 7.2 SLC realization

The SLC implementation is the enforcement realization being assessed.

The architecture determines the substrate and the mechanisms used to implement the required enforcement behavior.

EBP does not choose between software, TEE, MCU, Secure Element, FPGA, ASIC, ISA/pipeline, or hybrid architectures.

### 7.3 Assessment

The assessment evaluates whether the concrete realization satisfies:

1. all applicable EABC normative requirements;
2. all five EABC boundary semantic properties, with accepted N/A dispositions only where permitted;
3. every applicable EBP profile and assurance constraint;
4. the declared adversary model and guarantee; and
5. the validity and deployment assumptions on which the assurance claim depends.

An assessment result for one layer MUST NOT be substituted for a result required by another layer.

---

## 8. Relationship to EABC conformance levels

EABC conformance levels remain defined by EABC 004.

The existing hierarchy is preserved:

- Level 1 — Property Conformance;
- Level 2 — Evidence Conformance; and
- Level 3 — Profile Conformance.

EBP assurance tiers are separate from these EABC conformance levels.

In particular:

- EBP assurance tiers MUST NOT determine EABC conformance levels.
- EBP assurance tiers MUST NOT replace an EABC property assessment.
- EBP assurance tiers MUST NOT be treated as proof that an EABC semantic property is satisfied.
- EABC conformance MUST NOT be inferred from an EBP assurance tier.
- A claim of Full Level 1 MUST continue to satisfy EABC 004, including assessment of all five boundary semantic properties and the applicable P1–P10 obligations.

The `ENFORCEMENT_INDEPENDENCE` qualification required for `NON_BYPASSABILITY` remains a separate EBP assurance qualification. It does not make EABC Level 1 dependent on a particular EBP assurance tier.

---

## 9. Compatibility and migration

### 9.1 EABC semantic authority

This document is subordinate to EABC 001–004 and the accepted authority decisions R1, A1, and A2.

Nothing in this document amends those decisions.

Where a conflict is identified, the applicable EABC normative text and accepted authority decisions govern. The conflict MUST be recorded for resolution rather than silently resolved by an EBP profile.

### 9.2 EBP-006 legacy terminology

The historical EBP-006 `Exclusivity` path-exclusion meaning is identified by the versioned alias:

`EBP-006:Exclusivity@v1` → `NON_BYPASSABILITY(B,E)`

The legacy alias MUST NOT be silently redefined as the authority-based `EXCLUSIVITY(A,E,I)`.

The historical EBP-006 `Independence` label is reconciled to the qualified assurance meaning `ENFORCEMENT_INDEPENDENCE`. Its underlying assurance meaning is retained unless expressly amended by the applicable specification authority.

### 9.3 Existing records

Historical EBP assessments and evidence records MUST retain their original profile version, terminology, and assessment meaning.

A migration MUST NOT silently reinterpret a historical `VALID`, `INVALID`, or `INDETERMINATE` result under a later profile version.

Where an old assessment is mapped to this version, the mapping MUST identify:

- the original profile and version;
- the original claim and terminology;
- the new profile and version, if applicable;
- the mapping rationale; and
- any gap requiring reassessment.

### 9.4 Material changes

A material change to the assessed SLC, substrate, configuration, deployment assumptions, adversary model, or applicable profile MUST trigger reassessment of affected claims.

A previously valid assessment MUST NOT automatically remain valid after a material change.

Where materiality or its effect on the guarantee cannot be determined, the affected assurance result MUST be `INDETERMINATE` until resolved.

---

## 10. Core-to-EBP relationship summary

| EABC / EBP subject | EBP treatment |
|---|---|
| P1–P10 | Retained as EABC normative obligations; EBP does not replace them |
| Five boundary semantic properties | All remain EABC assessment subjects; profiles may qualify assurance |
| `NON_BYPASSABILITY` | Requires declared `ENFORCEMENT_INDEPENDENCE` qualification under R1 |
| P3 deterministic commit semantics | Remains EABC; temporal constraints qualify but do not replace it |
| `INTEGRITY_STATE` | Authenticity and integrity remain distinct from freshness |
| P5 intended-state correspondence | Remains independently assessable; not inferred from state integrity |
| EABC transaction evidence | Remains governed by EABC 002 |
| EBP Assurance Evidence | Instance-/assessment-scoped; not a ninth transaction evidence category |
| EABC conformance levels | Remain governed by EABC 004 |
| EBP assurance tiers | Separate from EABC conformance levels |
| Execution Boundary Policy | External input selecting applicable EBP assurance requirements, not EABC properties |
| SLC substrate | Chosen by implementation architecture and assessed as part of the concrete realization |
| EBP Assurance Attestation | Optional packaging of claims; not proof by itself |

---

## 11. Authority decisions and remaining open items

### 11.1 Accepted Authority decisions

The EABC Specification Authority has accepted the following design positions as part of EBP v0.2.3:

1. Multiple applicable EBP profiles are cumulative by default within overlapping assessment scope.
2. Alternative profile selection requires explicit authorization by the applicable contract or policy.
3. Absence of an additional EBP profile obligation does not automatically establish `CONFORMANCE_ELIGIBLE`.
4. EBP does not establish a universal assurance-tier hierarchy across profile families.
5. Boundary Evidence Binding follows the EABC 002 Intrinsically Bound principle.
6. P3 remains an EABC obligation and is not an additional value of the EBP `property` field.
7. The historical EBP-006 `Independence` meaning is retained while its terminology is aligned with `ENFORCEMENT_INDEPENDENCE`.

### 11.2 Remaining open items

The following matters remain open for Authority review:

1. **Attestation format:** whether an EAT-based representation should be standardized as a recommended profile or remain optional.
2. **Material-change criteria:** whether common material-change categories should be standardized beyond the requirement to reassess changes affecting a claimed guarantee.

These open items MUST NOT weaken existing EABC requirements or alter the accepted separation between EABC conformance and EBP assurance.

---

## 12. Normative invariants

The following invariants govern interpretation of this document:

1. EBP MUST NOT define or select the SLC substrate.
2. The concrete SLC realization MUST be assessed with its substrate, configuration, and deployment assumptions.
3. EBP MUST NOT create, waive, or select away EABC properties.
4. All five EABC boundary semantic properties remain assessment subjects under EABC 004.
5. EBP profiles MUST qualify, not redefine, EABC properties.
6. P3 remains an EABC semantic obligation; temporal assurance constraints MUST NOT replace it.
7. P3 MUST NOT be introduced as an additional EBP `property` value.
8. `INTEGRITY_STATE` MUST NOT be treated as proof of freshness.
9. `INTEGRITY_CTX` provenance MUST NOT be treated as proof of factual correctness.
10. `NON_BYPASSABILITY` MUST declare the applicable `ENFORCEMENT_INDEPENDENCE` qualification.
11. EABC conformance levels and EBP assurance tiers MUST remain separate.
12. Missing or unresolved required profile selection MUST NOT be treated as absence of a profile obligation.
13. Absence of a profile obligation MUST NOT automatically establish `CONFORMANCE_ELIGIBLE`.
14. `INDETERMINATE` MUST remain unacceptable for `VALID_COMMIT`.
15. EBP Assurance Evidence MUST remain distinct from transaction-scoped EABC evidence.
16. No EBP assurance result or attestation may substitute for the evidence required to establish the underlying claim.
17. Multiple applicable EBP profiles are cumulative by default within overlapping assessment scope.
18. Alternative profile selection MUST be expressly authorized by the applicable contract or policy.
19. Unresolved conflicts between applicable profile requirements MUST result in `INDETERMINATE`.
20. EBP MUST NOT establish a universal assurance-tier hierarchy across profile families.
21. A profile-applicability determination MUST identify the authoritative sources examined and the declared assessment scope.
22. Correlation between EABC transaction evidence and EBP Assurance Evidence MUST satisfy the EABC 002 Intrinsically Bound principle.
