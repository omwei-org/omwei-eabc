# Execution Authority Boundary Contract (EABC)

# 004 – Conformance

## Status

This document defines the conformance requirements for implementations claiming compatibility with the Execution Authority Boundary Contract (EABC).

Conformance is evaluated against the original P1–P10 obligations and the five boundary semantic properties defined by this specification.

Conformance does not require a particular architecture, product, protocol, hardware platform, substrate, or implementation technology.

---

# Conformance Model

EABC defines conformance at the level of observable architectural behavior.

An implementation conforms by demonstrating that it satisfies the applicable normative execution-authority requirements and exposes sufficient evidence for an independent consumer to verify those requirements.

Internal implementation details are outside the scope of this specification except where they are relevant to establishing an observable normative guarantee.

---

# Conformance Levels

EABC retains its existing three-level conformance hierarchy.

## Level 1 — Property Conformance

Level 1 evaluates the normative properties and obligations of the EABC implementation. Full Level 1 requires assessment of all applicable P1–P10 obligations and each of the five boundary semantic properties, as specified below.

## Level 2 — Evidence Conformance

The implementation provides sufficient evidence for an independent consumer to verify each required property and obligation.

Evidence MUST satisfy the requirements defined in **002 – Evidence Model**.

## Level 3 — Profile Conformance

The implementation publishes an EABC Implementation Profile mapping its architecture onto the EABC specification.

The EABC Implementation Profile SHALL describe:

- architectural components;
- evidence mapping;
- lifecycle semantics;
- execution semantics;
- supported capabilities;
- unsupported capabilities;
- implementation assumptions;
- the mapping to P1–P10 and the five boundary semantic properties.

An EABC Implementation Profile is distinct from an EAP Profile. The two profile types MUST NOT be conflated.

---

# Level 1 — Full Property Conformance

### 3.2 Mandatory assessment for full Level 1

For full Level 1 — Property Conformance:

1. All mandatory P1–P10 requirements applicable under EABC 001 MUST be assessed.
2. Each of the five EABC boundary semantic properties MUST be separately assessed.
3. Each boundary semantic property MUST receive one of the following applicability dispositions:
   - applicable and demonstrated;
   - applicable and not demonstrated;
   - accepted N/A, where permitted by §3.3.
4. An applicable property MUST be demonstrated for full Level 1 conformance.
5. An applicable property that is not demonstrated prevents a claim of full Level 1 conformance.
6. A property MUST NOT be omitted from the assessment merely because the implementation does not expose a corresponding field, component, or evidence label.

The five boundary semantic properties are mandatory assessment subjects. An accepted N/A disposition is an applicability determination, not a declaration that an applicable property has been satisfied.

### 3.3 N/A applicability rules

N/A is an exceptional applicability determination. It is not an implementation-selected exemption.

#### 3.3.1 General requirements

An N/A determination MUST:

1. follow objectively from the declared Protected Effect Scope, Boundary Scope, or another formally relevant scope definition;
2. identify the precise part of the declared scope that makes the property inapplicable;
3. explain why the property has no applicable semantic subject within that scope;
4. be supported by evidence sufficient for an independent assessor to evaluate the justification; and
5. be explicitly accepted by the party responsible for the conformance assessment.

The implementer MAY propose an N/A determination but MUST NOT unilaterally declare it accepted.

Where the assessment is performed by the implementer, an accepted N/A SHALL be marked `self-accepted` in the conformance claim, so that consumers can see that no independent acceptance occurred.

An N/A determination MUST NOT be based solely on:

- absence of a field or label in an implementation;
- absence of evidence supplied by the implementer;
- a decision not to model a relevant subject;
- implementation complexity or cost;
- lack of a particular implementation mechanism;
- an assertion that the property is outside the implementation's responsibility where the declared Protected Effect Scope still includes the relevant effect.

An N/A determination MUST NOT be used to avoid an inconvenient property.

#### 3.3.2 NON_BYPASSABILITY(B,E) and EXCLUSIVITY(A,E,I)

N/A is not permitted for either property.

A Level 1 assessment necessarily concerns a declared Protected Effect Scope and a claimed execution-authority boundary. The assessment MUST therefore evaluate whether the in-scope paths capable of producing the Protected Effect are mediated by the boundary and whether a Parallel Commit Authority exists for the same effect, scope, and Authority Interval, in accordance with ADR R1 §3 and §2.6 of this record.

#### 3.3.3 INTEGRITY_DEF(B)

N/A is not permitted for a claimed boundary.

A boundary necessarily has an applicable definition, whether that definition is stored separately, embedded in an implementation, fixed by an immutable specification, or represented in another form.

The absence of a separately stored configuration or definition file does not make the property inapplicable. The assessment must still establish which authentic definition governs the boundary instance making the determination.

#### 3.3.4 INTEGRITY_STATE(B,E)

An N/A determination MAY be considered only where the declared boundary semantics establish that no runtime state participates in, constrains, or can affect the determination for any effect within the declared Protected Effect Scope.

The assessment MUST establish that the boundary is genuinely stateless with respect to the determination under the declared scope and threat model.

The following are not sufficient grounds for N/A:

- runtime state is not exposed to the consumer;
- runtime state is not separately named;
- state is not recorded in evidence;
- the implementation claims that its state is internal;
- the implementation uses an immutable definition but still has runtime modes, conditions, values, or state-bearing inputs relevant to the determination.

If any runtime state relevant to the determination exists, `INTEGRITY_STATE(B,E)` is applicable.

#### 3.3.5 INTEGRITY_CTX(C,B,E)

An N/A determination MAY be considered only where the formally declared scope genuinely contains no context dimension and there is no explicit empty-context value or other context representation whose binding is relevant to the determination and effect.

In particular:

- If C = ∅ is explicitly represented as the context value, `INTEGRITY_CTX(C,B,E)` remains applicable. The binding of that context value to B and E MUST be assessed.
- An unnamed context remains context if execution-relevant circumstances affect the determination or effect.
- An implicit context remains context.
- A constant or empty context represented as a value remains a context representation whose binding can be assessed.
- Missing context fields, absent telemetry, omitted labels, or an implementation's decision not to model context MUST NOT establish N/A.
- The implementer MUST NOT create N/A eligibility by omitting context from its implementation or documentation.

An N/A determination is possible only where the formally declared scope genuinely contains no context dimension and no explicit empty-context value or other context representation whose binding is relevant.

If any context dimension qualifies the determination or its associated effect, `INTEGRITY_CTX(C,B,E)` is applicable.

#### 3.3.6 N/A assessment record

Every accepted N/A determination MUST be recorded in the conformance evidence with:

- the property identifier;
- the declared Protected Effect Scope and Boundary Scope;
- the relevant formal scope definition;
- the reason the property is inapplicable;
- supporting evidence;
- the identity of the assessor accepting the determination;
- the assessment date and applicable specification version.

An N/A determination MUST be revisited if a scope, boundary, context, or execution-semantic change makes the property applicable.

### 3.4 Full Level 1 and partial/property-level conformance

The existing EABC 004 conformance hierarchy is retained.

**Full Level 1 — Property Conformance**

Full Level 1 requires:

- demonstration of all mandatory P1–P10 requirements applicable under EABC 001;
- assessment of all five boundary semantic properties;
- demonstration of every applicable boundary semantic property;
- acceptance and recording of any N/A determination permitted by §3.3.

An accepted N/A disposition does not constitute a failed property assessment. It establishes that the property has no applicable subject within the formally declared scope.

**Partial/property-level conformance**

EABC 004 already permits implementations that do not satisfy all mandatory properties to declare supported properties, unsupported properties, and implementation limitations.

Such a declaration MAY identify individual properties that have been demonstrated. It MUST NOT be presented as full Level 1 conformance.

A partial/property-level declaration:

- does not create a new conformance level;
- does not convert an applicable but unproven property into N/A;
- does not establish full architectural compatibility;
- leaves the consumer responsible for determining whether the demonstrated subset is sufficient for its own purpose.

**Accepted N/A**

An accepted N/A is an applicability disposition within the existing conformance assessment. It is not a separate conformance level and is not equivalent to a property being demonstrated.

### 3.5 Avoidance of double-counting

P1–P10 remain the original EABC obligations. The five boundary semantic properties provide the adopted boundary semantic model.

Where a boundary semantic property refines or gives a more precise boundary-level meaning to an existing P1–P10 obligation, the relationship is an explicit semantic mapping. It does not create a second copy of the same requirement.

The assessment MUST identify both:

- the original P1–P10 obligation being addressed; and
- the boundary semantic property that refines or supports that obligation.

A single piece of evidence MAY support more than one requirement. However, it MUST independently establish each requirement in that requirement's own normative meaning.

In particular:

- evidence supporting `NON_BYPASSABILITY(B,E)` does not automatically establish P2 in its entirety;
- evidence supporting `INTEGRITY_CTX(C,B,E)` does not automatically establish all of P4;
- evidence supporting `INTEGRITY_STATE(B,E)` does not automatically establish all of P5;
- evidence supporting a boundary semantic property does not automatically establish P6 or P7;
- evidence supporting a P1–P10 obligation does not automatically establish a boundary semantic property.

The conformance assessment MUST NOT count one demonstrated requirement as satisfying another merely because their evidence overlaps or their semantics are related.

### 3.6 Independence from EBP assurance tiers

ADR R1 §3, item 6, remains unchanged.

EABC conformance levels MUST NOT be derived from, conditioned on, or silently mapped to EBP assurance tiers.

The distinction is:

- EABC conformance evaluates whether the applicable EABC requirements and semantic properties are satisfied.
- EBP assurance constraints qualify the assurance of a concrete implementation against a selected EBP.
- An EBP assurance tier MUST NOT replace an EABC property assessment.
- An EBP assurance tier MUST NOT be treated as proof that an EABC semantic property is satisfied.
- An EABC conformance level MUST NOT be inferred from an EBP assurance tier.

A `NON_BYPASSABILITY` assessment MUST continue to declare the applicable `ENFORCEMENT_INDEPENDENCE` level as a separate EBP assurance qualification, as required by ADR R1.

A semantic `NON_BYPASSABILITY` claim with an unspecified enforcement-independence qualification may be recorded as such. It MUST NOT be used to assign an assurance tier or to make a conformance assertion that depends on that tier until the qualification is declared and assessed.

This qualification rule does not make EABC Level 1 dependent on a particular EBP tier.

The EABC conformance hierarchy remains implementation-neutral. It does not prescribe a substrate, trusted execution environment, processor architecture, hardware enforcement component, or software architecture.

---

# Mandatory Requirements

A claim of full EABC Level 1 conformance MUST be supported by assessment of:

- all mandatory P1–P10 requirements applicable under EABC 001;
- `NON_BYPASSABILITY(B,E)`;
- `INTEGRITY_DEF(B)`;
- `INTEGRITY_STATE(B,E)`;
- `INTEGRITY_CTX(C,B,E)`;
- `EXCLUSIVITY(A,E,I)`.

An applicable requirement or boundary semantic property that is not demonstrated prevents a claim of full Level 1 conformance. An accepted N/A is an applicability disposition only where permitted by 001 and does not mean that an applicable property has been demonstrated.

---

# Optional Capabilities

Implementations MAY provide additional capabilities beyond the minimum EABC requirements.

Examples include:

- hardware attestation;
- trusted execution environments;
- formal verification;
- policy explanation;
- runtime telemetry;
- cryptographic proof systems.

Such capabilities MUST NOT alter the normative semantics defined by EABC or substitute for evidence of the required properties.

---

# Evidence Sufficiency

Conformance is determined by evidence, not by implementation claims.

For every mandatory P1–P10 obligation and every boundary semantic property, an implementation SHALL provide evidence sufficient for an independent consumer to evaluate compliance or, where expressly permitted, the applicability of an N/A disposition.

Consumers MUST NOT be required to trust implementation-specific assertions without supporting evidence.

Evidence MAY be reused across requirements only where it independently establishes each requirement's normative meaning. Shared evidence MUST NOT collapse distinct requirements or allow one property to be counted automatically as another.

---

# Independent Verification

A conforming implementation MUST enable independent verification of execution authority.

An independent consumer SHOULD be capable of determining:

- who or what trust domain originated execution authority;
- whether the governed system could self-authorize or modify established authority;
- what action or Protected Effect was authorized;
- under which authority the authorization was granted;
- which boundary definition governed the deciding instance;
- which runtime state was evaluated and how it was bound to the determination;
- the intended reference state or condition and its relationship to the authorization-evaluated state;
- the context and its authoritative provenance;
- whether all relevant paths capable of producing the Protected Effect were inventoried and mediated;
- whether a Parallel Commit Authority exists for the same effect, scope, and Authority Interval;
- whether the decision remained applicable through the associated effect;
- whether execution occurred and completed successfully;
- whether the evidence remains trustworthy and correlatable.

These determinations SHOULD be possible without implementation-specific knowledge.

---

# Implementation Profiles

EABC Implementation Profiles describe how a concrete architecture satisfies the EABC requirements.

Profiles are informative with respect to architecture but normative with respect to their mapping to EABC.

Each EABC Implementation Profile SHOULD identify:

- supported P1–P10 obligations;
- supported boundary semantic properties;
- evidence artifacts and evidence dimensions;
- execution lifecycle;
- failure semantics;
- capability limitations;
- implementation assumptions;
- accepted N/A dispositions and their supporting records, if any;
- EABC specification version and profile version.

EABC Implementation Profiles MUST NOT redefine the normative requirements of EABC. They are distinct from EAP Profiles.

---

# Versioning

EABC implementations SHALL identify the version of the specification to which they claim conformance.

An EABC Implementation Profile SHOULD declare:

- EABC specification version;
- EABC Implementation Profile version;
- profile publication date;
- compatibility information.

---

# Partial and Property-Level Conformance

Implementations that do not satisfy all mandatory requirements SHALL NOT claim full EABC Level 1 conformance.

They MAY declare:

- demonstrated P1–P10 obligations;
- demonstrated boundary semantic properties;
- applicable requirements not demonstrated;
- accepted N/A dispositions, where permitted;
- implementation limitations.

A partial/property-level declaration:

- does not create a new conformance level;
- MUST NOT be presented as full Level 1 conformance;
- MUST NOT convert an applicable but unproven property into N/A;
- does not establish full architectural compatibility;
- leaves the consumer responsible for determining whether the demonstrated subset is sufficient for its own purpose.

An accepted N/A is an applicability disposition within the existing conformance assessment. It is not a separate conformance level and is not equivalent to a property being demonstrated.

---

# Relationship to EBP Assurance Tiers

EABC conformance levels MUST NOT be derived from, conditioned on, or silently mapped to EBP assurance tiers.

The distinction is:

- EABC conformance evaluates whether the applicable P1–P10 obligations and five boundary semantic properties are satisfied.
- EBP assurance constraints qualify the assurance of a concrete implementation against a selected EBP.
- An EBP assurance tier MUST NOT replace an EABC property assessment.
- An EBP assurance tier MUST NOT be treated as proof that an EABC semantic property is satisfied.
- An EABC conformance level MUST NOT be inferred from an EBP assurance tier.

A `NON_BYPASSABILITY` assessment MUST declare the applicable `ENFORCEMENT_INDEPENDENCE` level as a separate EBP assurance qualification. This does not make EABC Level 1 dependent on a particular EBP tier.

The EABC conformance hierarchy remains implementation-neutral. It does not prescribe a substrate, trusted execution environment, processor architecture, hardware enforcement component, or software architecture.

---

# Conformance Statement

An implementation claiming EABC conformance SHOULD publish a Conformance Statement including:

- implementation name;
- implementation version;
- supported EABC version;
- EABC Implementation Profile identifier, if applicable;
- claimed conformance level;
- demonstrated P1–P10 obligations;
- demonstrated boundary semantic properties;
- accepted N/A dispositions, if any, including whether any are self-accepted;
- supported optional capabilities;
- known limitations.

---

# Summary

Full Level 1 requires assessment and demonstration of all applicable P1–P10 obligations and all applicable boundary semantic properties, with N/A permitted only under the narrow rules defined in 001 and transparently recorded. Partial/property-level declarations remain available but do not create a new conformance level.

EABC standardizes the observable contract between authority and execution, not the mechanisms used to implement that contract.
