# EABC Specification Decision R1-A1

**Decision ID:** EABC-ADR-R1-A1
**Title:** Normative Clarifications and P1–P10 Reconciliation
**Parent Decision:** EABC-ADR-R1
**Authority:** EABC Specification Authority
**Status:** PROPOSED
**Outcome:** PENDING AUTHORITY REVIEW
**Date:** 2026-11-03

## 1. Purpose and status

### 1.1 Purpose

This proposed addendum identifies and resolves outstanding normative questions arising from the accepted decision EABC-ADR-R1.

Its purpose is to establish an authority-reviewed basis for the subsequent coordinated migration of EABC documents 001–004.

A1 addresses only:

1. normative definitions of `INTEGRITY_DEF(B)`, `INTEGRITY_STATE(B,E)`, and `INTEGRITY_CTX(C,B,E)`;
2. assessment requirements for `EXCLUSIVITY(A,E,I)`;
3. the relationship between the five boundary semantic properties and Level 1 conformance;
4. the applicability and acceptance of N/A determinations;
5. the decomposition and preservation of the original P1 obligations;
6. reconciliation of the five boundary semantic properties with P1–P10 and the EBP assurance layer;
7. the relationship between P2 Complete Mediation, `NON_BYPASSABILITY(B,E)`, and its required evidence dimensions.

### 1.2 Relationship to ADR R1

A1 supplements and clarifies the accepted ADR R1. It does not silently amend, overwrite, or retrospectively replace the historical ADR R1 record.

A1 supplements the following R1 provisions:

- §1 — adoption of the five-element boundary semantic set;
- §2 — Commit Authority, Authority Interval, and Parallel Commit Authority definitions, only where needed to apply the five-property set;
- §3.1–§3.9 — semantic distinctions and assurance-layer separation;
- §5 — the three distinct meanings of independence;
- §6 — preservation and migration of P1–P10;
- §7 — consequences and the distinction between semantic adoption and implementation/deployment conformance.

A1 does not reopen decisions already settled by R1 unless a concrete contradiction with the current EABC specification is identified. No such contradiction is identified by this proposal.

At the time of recording, PR #13 (EBP-006 terminology migration) was merged at commit 0bfe476ec5b0329325480e6b6835c16ef3405512; current main HEAD was 9d82dc877b93255eb857d8b217240e12cc1a8063.

### 1.3 Decision-record status

The repository's `decisions/README.md` classifies decision records as non-normative records of authority decisions. Normative changes resulting from an accepted decision are made separately through changes to the specification documents.

Accordingly:

- A1 is a proposed authority decision record, not normative EABC specification text.
- If accepted, A1 SHALL provide the authority-approved basis for a subsequent normative migration.
- A1 SHALL NOT itself be treated as proof that EABC 001–004 have been updated.
- No implementation or deployment shall be considered conformant merely because it follows this proposed addendum.

Upon completion of the normative migration, the operative EABC specification requirements resulting from this decision SHALL reside in `docs/`. This decision record SHALL remain the historical authority record and SHALL NOT be treated as a parallel specification text or as an alternative source for implementation-level requirements.

### 1.4 Explicit exclusions

A1:

1. does not introduce a sixth EABC boundary semantic property;
2. does not modify or decide the EAP Binding model (R2), which belongs to the EAP Architecture Authority;
3. does not prescribe an implementation architecture, substrate, cryptographic mechanism, or enforcement placement;
4. does not establish implementation or deployment conformance;
5. does not modify EBP-006;
6. does not authorize implementation of the normative migration of EABC 001–004 by itself.

The five boundary semantic properties remain exactly:

1. `NON_BYPASSABILITY(B,E)`
2. `INTEGRITY_DEF(B)`
3. `INTEGRITY_STATE(B,E)`
4. `INTEGRITY_CTX(C,B,E)`
5. `EXCLUSIVITY(A,E,I)`

## 2. Decision A — Normative definitions and assessment requirements

### 2.1 INTEGRITY_DEF(B) — Boundary Definition Integrity

#### 2.1.1 Normative subject and definition

`INTEGRITY_DEF(B)` establishes the authenticity and integrity of the boundary definition applicable to boundary B.

The applicable boundary definition is the authoritative specification of the boundary's identity, scope, decision semantics, and enforcement-relevant content. It includes the elements necessary to determine:

- which boundary is being assessed;
- which Protected Effects and execution paths fall within its declared scope;
- which conditions and constraints govern its `COMMIT(E)` or `REJECT(E)` determinations;
- which decision and enforcement semantics the boundary is required to implement; and
- which boundary instance is governed by that definition.

A boundary definition MAY be represented by a document, configuration, executable representation, hardware description, immutable specification, composite of artifacts, or another implementation-neutral representation. EABC does not prescribe its representation.

For `INTEGRITY_DEF(B)` to be satisfied:

1. The applicable definition MUST have an identifiable authoritative origin.
2. Its identity, scope, and enforcement-relevant content MUST be determinable.
3. The applicable definition MUST be authentic.
4. The applicable definition MUST be protected against unauthorized modification or substitution in accordance with the guarantee selected under §2.1.2.
5. The boundary instance making a `COMMIT(E)` or `REJECT(E)` determination MUST be demonstrably bound to the authentic definition applicable to that instance.
6. The binding between the boundary instance and its applicable definition MUST be sufficiently unambiguous for an independent assessor to determine which definition governs the instance making the determination.
7. An authentic artifact purporting to describe B MUST NOT, by that fact alone, be treated as proof that it is the definition actually applicable to the boundary instance making the determination.

The property concerns the applicable definition governing the deciding boundary instance, not merely the integrity of a stored artifact purporting to describe that boundary.

#### 2.1.2 Distinct guarantee alternatives

Two materially different guarantees are considered.

**Option A — Prevention**

Unauthorized modification or substitution of the applicable boundary definition cannot occur.

Under this option, the applicable boundary definition MUST NOT be modified or substituted without authorization. The guarantee concerns the applicable definition itself, not merely whether an unauthorized version becomes operative or is detected before use.

An unauthorized modification or substitution of the applicable definition is a failure of this guarantee even if the alteration is later detected and rejected before it affects a determination.

This option does not require physical immutability of every copy, representation, or archival instance of the definition. It requires that the applicable boundary definition be protected against unauthorized modification or substitution. Copies that are not applicable to the deciding boundary instance are not, merely by existing, the applicable definition.

An authorized update or replacement MAY occur under an authorized procedure. Such an update is not an unauthorized modification. The procedure MUST establish the authority for the change and the identity, scope, enforcement-relevant content, and instance binding of the resulting applicable definition.

**Option B — Detection before decision impact**

Unauthorized modification or substitution of the applicable boundary definition may occur, but MUST be detected and rejected before it can affect a `COMMIT(E)` or `REJECT(E)` determination.

Under this option, an unauthorized alteration may exist. The boundary MUST detect and reject it before it can influence an operative determination. Detection after the altered definition has affected a determination does not satisfy this option. A later audit finding is not sufficient.

This option permits an unauthorized modification or substitution to occur and relies on detection and rejection before decision impact. It therefore requires evidence that detection and rejection necessarily precede any effect on the determination, including under the declared threat model and relevant failure conditions.

#### 2.1.3 Evaluation and recommendation

Option A and Option B are not equivalent.

Option A provides a stronger guarantee about the applicable definition itself: unauthorized modification or substitution cannot occur.

Option B provides a weaker guarantee: unauthorized modification or substitution may occur, but the altered definition must be detected and rejected before it affects a determination.

Option B introduces an assurance dependency on detection coverage, detection timing, rejection behavior, and the absence of a decision-impact window. It may be appropriate for a profile that explicitly accepts a detect-and-reject model, but it does not establish prevention of unauthorized modification.

Option A is implementation-neutral. It specifies the required integrity result without prescribing immutable storage, access-control mechanisms, hardware protection, authenticated update procedures, or any particular enforcement architecture.

The guarantee in Option A is assessed against a declared threat model. The assessment MUST identify the adversary capabilities and trust assumptions under which unauthorized modification or substitution of the applicable definition is claimed to be prevented. A prevention claim without a declared threat model is not assessable.

The declared threat model MUST be bound to the scope of the applicable definition and to the boundary instance under assessment. A threat model that is declared generally and not tied to that scope and instance does not make the prevention claim assessable.

The threat model is a parameter of the assessment. It does not prescribe a substrate or mechanism and does not make EABC conformance dependent on an EBP assurance tier (§3.6).

Recommendation: adopt Option A — Prevention.

The recommended normative guarantee is:

> The applicable boundary definition MUST NOT be modified or substituted without authorization.

The assessment MUST additionally establish the authenticity of the definition's identity, scope, and enforcement-relevant content, and the binding of that definition to the actual boundary instance making the `COMMIT(E)` or `REJECT(E)` determination.

If the Authority instead selects Option B, it MUST expressly approve the weaker detect-and-reject guarantee. Option B MUST NOT be represented as equivalent to Option A or described as prevention of unauthorized modification.

After the Authority approves a selected option, the normative migration SHALL retain only the selected option.

#### 2.1.4 Authorized updates and replacement

An authorized update, amendment, or replacement of the applicable boundary definition MAY occur through a procedure authorized by the applicable authority rules.

The procedure MUST:

1. identify the entity or process authorized to approve the change;
2. establish the authority for the update or replacement;
3. identify the resulting definition, including its identity, scope, and enforcement-relevant content;
4. establish which boundary instance is governed by the resulting definition; and
5. make the resulting definition applicable only under the authorized update procedure.

The existence of an update mechanism does not itself establish that an update is authorized.

#### 2.1.5 Distinction from other requirements

`INTEGRITY_DEF(B)` does not establish:

- the integrity or authenticity of runtime state used for a particular determination; that is `INTEGRITY_STATE(B,E)`;
- the integrity of the context-to-boundary-to-effect binding; that is `INTEGRITY_CTX(C,B,E)`;
- the integrity of evidence artifacts generally; that remains P6, Evidence Integrity;
- the absence of an execution path that bypasses B; that is `NON_BYPASSABILITY(B,E)`;
- the absence of a Parallel Commit Authority; that is `EXCLUSIVITY(A,E,I)`.

A signature, hash, or authenticated configuration artifact MAY contribute evidence, but none is sufficient by itself to establish `INTEGRITY_DEF(B)`. The assessment must also establish that the authentic definition is the one applicable to the boundary instance making the determination.

### 2.2 INTEGRITY_STATE(B,E) — Runtime State Integrity

#### 2.2.1 Normative subject and definition

`INTEGRITY_STATE(B,E)` establishes the authenticity and integrity of the runtime state that boundary B evaluates in making a `COMMIT(E)` or `REJECT(E)` determination for Protected Effect E.

Runtime state comprises:

(a) the operational state of B itself, and

(b) the current condition of the governed system, target, or execution domain, where B reads or relies on that condition as an input to the determination.

The identity of the target and the requested action are not runtime state; they belong to context under `INTEGRITY_CTX(C,B,E)`.

Runtime state also includes any policy, configuration, delegated-authority, or other state or version value against which B evaluates or relies on the authorization in making its determination. Where the authorization was evaluated at an earlier stage, the assessment MUST establish that the state so identified is the state B relied on for this determination. A value that forms part of the authoritative boundary definition itself may instead have a role under `INTEGRITY_DEF(B)`. Each applicable role MUST be identified and assessed separately.

Examples of possible runtime state include an active safety-controller mode, an enabled or fault state, an active interlock state, internal state used by B's decision logic, or the current value of a target condition read by B. These examples are illustrative, not exhaustive definitions.

For `INTEGRITY_STATE(B,E)` to be satisfied:

1. The runtime state used for the determination MUST be identifiable as the state relevant to E.
2. The state used by B MUST be authentic and integrity-protected against unauthorized alteration, substitution, or misrepresentation.
3. The state evaluated MUST be demonstrably bound to the actual `COMMIT(E)` or `REJECT(E)` determination.
4. B MUST NOT use a state representation that has been substituted, misattributed, or altered without authorization as though it were the state actually evaluated.
5. Where the determination depends on multiple state elements, the assessment MUST establish that the state elements used belong to the state evaluation associated with that determination, rather than an unauthenticated mixture of unrelated or substituted state values.
6. Evidence MUST permit an assessor to distinguish the state used for the determination from state merely reported after the determination.

A state value's presence in a log or attestation does not by itself prove that B actually used that value.

#### 2.2.2 Binding to the determination

The binding between state and determination MUST identify the state representation, version, reference, or equivalent identity sufficient to establish which state B evaluated.

The binding MUST prevent a different state from being represented as the state used for the determination.

The binding MAY be established by any implementation-neutral mechanism that provides the required guarantee.

#### 2.2.3 Distinction from context

`INTEGRITY_STATE(B,E)` concerns the runtime state that B evaluates in making its determination.

`INTEGRITY_CTX(C,B,E)` concerns the execution context that determines the circumstances, scope, and applicability of that determination to E and its associated effect.

For example:

- an active safety-controller mode may be runtime state;
- target identity → context; the current value or condition of the target read by B → runtime state;
- the requested action or effect-specific execution parameters may be context;
- a boundary limit embedded in the authoritative boundary definition may be part of the definition.

These examples do not impose an exhaustive classification. A datum MAY have more than one normative role where the architecture genuinely uses it in more than one way.

Where a datum has multiple roles:

1. each applicable role MUST be identified separately;
2. the evidence MUST establish each applicable property independently; and
3. satisfaction of one property MUST NOT automatically establish another.

The classification depends on the datum's actual normative role in the architecture, not merely its name, storage location, or representation.

#### 2.2.4 Freshness is separate

`INTEGRITY_STATE(B,E)` establishes authenticity and integrity. It does not, by itself, establish freshness.

An authentic state representation may be stale. A state value may genuinely originate from its source and remain unmodified while no longer reflecting the current state.

EABC MUST NOT treat state authenticity as proof of freshness.

Where freshness is required, it MUST be specified and assessed as a separate assurance concern. Freshness may be addressed through an applicable EBP assurance profile, threat model, validity rule, or other explicitly declared assurance constraint.

No freshness requirement is introduced as a sixth EABC boundary semantic property or silently inserted into `INTEGRITY_STATE(B,E)`.

#### 2.2.5 Distinction from INTEGRITY_DEF(B)

`INTEGRITY_DEF(B)` concerns the authentic definition governing the boundary instance.

`INTEGRITY_STATE(B,E)` concerns the runtime state actually evaluated by that instance for a particular determination.

An authentic definition does not prove that the runtime state used for E is authentic. Authentic runtime state does not prove that the definition governing B is authentic.

Both properties MUST be assessed separately.

#### 2.2.6 Preservation of the consumer-facing P5 obligation

The original P5 requirement contains two distinct obligations:

> Execution authority MUST identify the state against which authorization was evaluated.
>
> Consumers MUST be able to determine whether execution occurred against the intended state.

The first obligation is refined through `INTEGRITY_STATE(B,E)`. `INTEGRITY_STATE(B,E)` concerns the authenticity and determination-binding of the runtime state evaluated or relied upon by B when making its determination.

The second obligation remains independently applicable. It concerns whether execution occurred against the intended state. For this obligation, the intended state is the reference state, condition, or state-dependent execution condition designated by the applicable authorization and execution semantics as the basis against which the authorized effect is to occur. The applicable semantics MUST make that reference identifiable, either directly or through an unambiguous reference to an authoritative state or condition. The applicable authorization and execution semantics MUST also expressly establish the relationship between the state against which authorization was evaluated and this intended reference state. The two MUST be the same state or condition, or, where they are distinct, the applicable semantics MUST designate the intended reference and define the relationship, permitted transition, or other conditions connecting it to the state evaluated during authorization. The relationship between the authorization-evaluated state and the intended reference state, including any permitted transition or state evolution, MUST be established as part of, or expressly bound to, the applicable authorization decision. The authorization decision MUST identify the intended reference and the relationship or transition conditions with sufficient precision to make them identifiable and verifiable by the consumer. A definition made merely before execution, but not established as part of or expressly bound to the authorization decision, is insufficient. Any subsequent change to the intended reference or its relationship to the authorization-evaluated state MUST either fall within a transition or state evolution expressly authorized in advance by that authorization decision, with its applicable conditions defined and verifiable, or be established by a new authorization decision or an expressly authorized revalidation before execution. A change that is neither so authorized in advance nor established through new authorization or expressly authorized revalidation MUST NOT be used as the basis for claiming execution-state correspondence.

The consumer-facing execution-state correspondence claim MUST permit a consumer to determine whether the state or condition applicable when the effect occurred corresponded to that intended reference, taking account of any state evolution or transition expressly permitted by the applicable authorization and execution semantics. Where those semantics require an unchanged state, correspondence requires that condition to hold; where they expressly permit defined state evolution, correspondence is assessed against those permitted conditions. The consumer-facing correspondence assessment MUST evaluate the state or condition at effect against the declared relationship to the state evaluated during authorization, including only transitions or differences expressly permitted by the applicable semantics. The intended reference and its relationship to the authorization-evaluated state MUST NOT be retrospectively redefined merely to match the state observed after execution.

This is a consumer-facing execution-state correspondence claim and MUST NOT be treated as automatically satisfied by establishing the authenticity or determination-binding of the state evaluated by B.

The two claims are related but distinct. Evidence establishing `INTEGRITY_STATE(B,E)` does not, by itself, establish that execution occurred against the intended state. Evidence establishing execution-state correspondence does not, by itself, establish the authenticity and determination-binding required by `INTEGRITY_STATE(B,E)`.

The original P5 consumer-facing obligation MUST remain in force after migration to the five boundary semantic properties. It MUST be assessed in its own normative meaning. This clarification does not prescribe a particular evidence format, mechanism, or implementation architecture.

### 2.3 INTEGRITY_CTX(C,B,E) — Context Authenticity and Context-to-Boundary-to-Effect Binding Integrity

#### 2.3.1 Normative subject and definition

`INTEGRITY_CTX(C,B,E)` establishes the authenticity and integrity of execution context C as applicable to the determination, and of the binding among that context, boundary B, and Protected Effect E.

Context C means the execution-relevant circumstances that determine the scope, conditions, and applicability of B's determination to E and its associated effect. The context's authenticity includes the provenance and integrity of its constituent elements from the source or sources designated as authoritative by the applicable context and authorization semantics, through their acceptance or use by B. Where context is derived, transformed, aggregated, or relayed, the applicable semantics MUST make its source provenance and relevant transformations identifiable and sufficiently protected against unauthorized substitution or misrepresentation. This requirement does not presume that every context element originates outside the governed system; it requires the declared authority and provenance rules for each relevant element to be respected. Authenticity and provenance establish the source and integrity of a context assertion; they do not, by themselves, establish that the assertion is factually true or correct. `INTEGRITY_CTX(C,B,E)` MUST NOT be interpreted as a general guarantee of the truth or correctness of facts asserted by an authoritative source. Where factual validation or corroboration is required, the applicable EABC implementation profile, EAP profile, or other applicable specification MUST state that requirement separately, including its validation basis. Such validation MUST NOT be inferred solely from source authenticity or provenance.

Context concerns the circumstances in which the determination is made and the effect to which it applies. It is distinct from the runtime state that B evaluates in making the determination.

Depending on the declared scope, context MAY include the identity of the initiating entity, target identity, requested action, effect-specific execution parameters, applicable execution constraints, or relevant environmental conditions. These examples are illustrative, not exhaustive.

The context MUST be defined sufficiently to identify which context elements determine the circumstances, scope, or applicability of the determination to E and its associated effect. EABC does not prescribe a universal context schema.

For `INTEGRITY_CTX(C,B,E)` to be satisfied:

1. The context C applicable to the determination MUST be identifiable.
2. The source or sources designated as authoritative for each relevant context element, and the provenance of any derived or transformed context, MUST be identifiable under the declared context semantics.
3. The context elements used by B MUST be authentic and integrity-protected against unauthorized substitution, alteration, or misrepresentation from their authoritative source or defined derivation through their use in the determination.
4. The binding among C, B, and E MUST itself be authentic and integrity-protected.
5. The binding MUST be established no later than the determination on E.
6. The binding MUST identify the boundary B that made the determination and the Protected Effect E to which that determination applies.
7. The binding MUST remain valid from the determination on E through the occurrence of the effect to which that determination applies.
8. The binding MUST NOT be silently substituted, broken, or misattributed during that interval.
9. Any context change that falls outside the context evolution explicitly permitted by the declared semantics MUST invalidate the existing binding for the affected effect. A new determination or an explicitly authorized revalidation and rebinding MUST occur before the effect may rely on the changed context.
10. Evidence MUST allow an assessor to establish that the effect being attributed to the determination is the effect associated with the authentic context and boundary binding.

#### 2.3.2 Lifecycle boundary

For this property, the relevant interval begins when B makes the determination on E.

The interval ends when one of the following occurs:

- the effect to which the determination applies occurs;
- the determination is explicitly invalidated or revoked; or
- the associated execution is abandoned or terminated without producing that effect.

If the determination is carried through queues, intermediate execution stages, delegated execution, retries, or transport between components, the binding MUST remain valid through those stages until the associated effect occurs or the determination is invalidated.

A retry or replacement execution that is not the effect instance covered by the original binding MUST NOT inherit the original binding merely because it carries the same request identifier. Its applicability MUST be established under the declared context and effect semantics.

A context change that is explicitly permitted by the declared context semantics does not automatically break the binding. The permitted change and its conditions MUST be defined in advance and must remain verifiable. An unapproved change, substitution, or misattribution breaks the binding.

#### 2.3.3 Distinction from state

`INTEGRITY_CTX(C,B,E)` concerns the execution context that determines the circumstances, scope, and applicability of the determination to E and its associated effect.

`INTEGRITY_STATE(B,E)` concerns the runtime state that B evaluates in making the determination.

A datum MAY participate in both the runtime state and the execution context. Where it does, each role MUST be identified and assessed separately. Evidence for one role MUST NOT automatically be treated as evidence for the other.

#### 2.3.4 Distinction from P3

`INTEGRITY_CTX(C,B,E)` establishes that the correct context, boundary, and effect remain bound to the determination.

It does not replace or absorb P3 deterministic commit semantics.

P3 continues to require explicit and deterministic commit semantics, including check-to-effect atomicity: the absence of a gap between the decision and the effect it authorizes.

P3 additionally covers any gap between determination and effect that does not involve a change of context (for example a change of state or a revocation). `INTEGRITY_CTX(C,B,E)` addresses only context-binding continuity.

A context binding can remain authentic while a check-to-effect atomicity failure occurs. Conversely, a system may implement an atomic transition while binding the decision to the wrong context or effect.

The two obligations are therefore distinct and MUST be assessed separately.

`INTEGRITY_CTX(C,B,E)` MUST NOT be used as evidence that P3 check-to-effect atomicity has been established.

### 2.4 Cross-property separation

The three integrity properties have distinct normative subjects.

| Property | Normative subject | Core question | Explicitly does not establish |
| --- | --- | --- | --- |
| `INTEGRITY_DEF(B)` | Boundary definition | Is this the authentic definition applicable to the deciding boundary instance? | Runtime state integrity |
| `INTEGRITY_STATE(B,E)` | Runtime state evaluated by B | Is the state used for the determination authentic and correctly bound to it? | Freshness by itself |
| `INTEGRITY_CTX(C,B,E)` | Context authenticity and context/boundary/effect binding | Are the relevant context elements authentic, and is their binding to B and E authentic and maintained through the associated effect? | Factual truth or correctness of source assertions; P3 check-to-effect atomicity |

These properties MUST NOT be treated as interchangeable or inferred from one another.

A datum that has more than one normative role MUST be assessed under each applicable property. No property is automatically satisfied merely because another property is satisfied.

### 2.5 Distinction from P6 Evidence Integrity and P7 Evidence Correlation

The three integrity properties concern the integrity of the boundary's semantic subjects:

- the definition governing B;
- the runtime state evaluated by B for E;
- the context-to-boundary-to-effect binding.

P6 Evidence Integrity concerns the integrity of execution-authority evidence artifacts. It requires evidence to be tamper evident and permits consumers to determine whether evidence has been modified.

P7 Evidence Correlation concerns whether evidence generated across authorization and execution can be correlated to reconstruct the execution-authority chain.

The distinction is substantive:

- An authentic evidence artifact does not prove that the boundary definition it describes was the definition actually governing the deciding instance.
- A correlated state record does not prove that the recorded state was the state actually used for the determination.
- An intrinsically bound correlation identifier does not by itself prove that the context-to-boundary-to-effect relationship was authentic and maintained through the associated effect.
- Authenticity of a boundary definition, state, or context binding does not by itself establish that the evidence artifact reporting it is tamper evident or correlatable.

P6 and P7 MUST remain separate EABC obligations. The five boundary semantic properties do not replace them.

### 2.6 EXCLUSIVITY(A,E,I) — Assessment requirements

An `EXCLUSIVITY(A,E,I)` assessment MUST identify:

1. the Protected Effect Scope and the Authority Interval I, with its scope;
2. the reference Commit Authority A and the basis for its designation, being the entity whose determination is operative for E over I under the applicable authority rules;
3. an inventory of entities whose determination is, or could be, operative for E over I;
4. the method used to establish that the inventory is complete;
5. the conditioning relationships among the determinations of A and each other candidate A′.

Inclusion in the candidate inventory does not, by itself, establish that an entity is a Commit Authority. Each candidate MUST be assessed against the Commit Authority definition in ADR R1 §2.

Where more than one entity is a candidate for A, the assessment MUST evaluate the property with each as reference, or justify the designation.

Where A′'s determination is not conditioned on A's determination, A′ satisfies the Parallel Commit Authority definition and `EXCLUSIVITY(A,E,I)` is violated, even if A's determination is conditioned on A′'s. The assessment SHALL record this, because it indicates that the operative decision may lie with A′ and the designation of A should be reviewed.

Where determinations are mutually conditioned, the assessment SHALL record the mutual conditioning relationship and describe the rule by which the combined determination is formed. It MUST NOT classify either determination as a Parallel Commit Authority solely on the basis of that mutual conditioning. Whether the resulting arrangement constitutes a single operative Commit Authority or another authority structure MUST be assessed under the existing definition in ADR R1 §2. Failure to form a determination (for example, deadlock) is governed by P8 failure semantics and is not, by itself, a violation of this property.

As with `NON_BYPASSABILITY(B,E)`, an inventory without a stated completeness method does not support the claim.

## 3. Decision B — Level 1 Property Conformance

### 3.1 Current Level 1 basis

The current EABC 004, under Conformance Levels → Level 1 — Property Conformance, states:

> The implementation demonstrates all mandatory execution-authority properties defined in 001 – Execution Authority Properties.

This establishes architectural compatibility.

A1 clarifies the property set to be assessed for full Level 1 conformance. It does not replace the existing three-level conformance hierarchy.

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

## 4. Decision C — P1 decomposition and preservation

### 4.1 Original P1 obligation

The current EABC 001 Property 1 requirement states:

> Execution authority MUST originate from a trust domain that is independent of the governed execution domain.
>
> The governed system MUST NOT be capable of modifying, bypassing, or self-authorizing execution authority after authorization has been established.

The second sentence contains three distinct obligations. A1 separates them while preserving their full semantic force.

### 4.2 Authority-Origin Independence

The trust-domain origin requirement remains a P1 obligation.

For P1, Authority-Origin Independence means:

> Execution authority MUST originate from a trust domain that is independent of the governed execution domain.

The governed system MUST NOT be capable of creating, granting, or establishing its own execution authority, whether acting alone or jointly with components within, or controlled by, the governed execution domain. A request submitted to, or authority granted by, an entity that originates from an independent trust domain and is entitled to grant it is not self-authorization.

The trust-domain origin requirement and the anti-self-authorization requirement are related but distinct aspects of P1:

- the trust-domain origin requirement specifies where execution authority MUST originate;
- the anti-self-authorization requirement prohibits the governed system from creating, granting, or establishing its own execution authority.

Both MUST be preserved.

The definition of Authority-Origin Independence in ADR R1 §5 SHALL NOT be read as narrowing the original P1 trust-domain requirement to an identity test of a single entity. The independent trust-domain relationship remains part of the requirement.

Authority-Origin Independence MUST NOT be conflated with:

- `ENFORCEMENT_INDEPENDENCE`, which is an EBP assurance constraint concerning the enforcement mechanism's trust domain and failure modes;
- `EXCLUSIVITY(A,E,I)`, which concerns the existence of a Parallel Commit Authority;
- `NON_BYPASSABILITY(B,E)`, which concerns execution paths capable of producing the Protected Effect.

The qualified terminology rules in ADR R1 §5 remain in force. Normative text MUST NOT use the unqualified word "independent" where one of these distinct meanings is intended.

### 4.3 Bypass

The bypass element of the original P1 clause is mapped to:

`NON_BYPASSABILITY(B,E)`

Bypass MUST NOT remain as a separate P1 semantic property or duplicate P1 requirement.

The meaning of bypass is the existence of an in-scope path capable of producing Protected Effect E without mediation by boundary B.

The original P1 bypass element concerns circumvention of execution authority. Circumvention of established authority is realized only through a path that produces the Protected Effect without mediation by the authority-enforcing boundary. It is therefore assessed as `NON_BYPASSABILITY(B,E)`. Where a circumvention does not involve such a path, it falls under the authority-modification obligation in §4.4.

This treatment is consistent with ADR R1 §6:

`EBP-006:Exclusivity@v1` → `NON_BYPASSABILITY(B,E)`

The former EBP-006 path-exclusion meaning MUST NOT be conflated with the new authority-based `EXCLUSIVITY(A,E,I)`.

#### 4.3.1 Required evidence dimensions

A `NON_BYPASSABILITY(B,E)` claim requires two distinct evidence dimensions:

1. Deployment-topology completeness
2. Boundary mediation

Both dimensions are necessary.

Deployment-topology completeness establishes that the declared in-scope path universe has not omitted relevant paths capable of producing E. The assessment MUST identify the Protected Effect Scope, Boundary Scope, and Path Scope, and MUST provide a basis for concluding that the path inventory is sufficiently complete for the claim.

Boundary mediation establishes that each identified in-scope path capable of producing E is mediated by B. The assessment MUST provide evidence about the behavior of B on the identified paths showing that they cannot produce E without the required mediation by B.

The two dimensions establish different things:

- topology completeness establishes that the relevant path universe has not omitted paths;
- boundary mediation establishes that each identified relevant path is mediated by B.

Topology completeness evidence alone does not establish that the identified paths are mediated by B.

Boundary-mediation evidence alone does not establish that the path inventory is complete.

Both are necessary to support a `NON_BYPASSABILITY(B,E)` claim.

These are evidence dimensions for one semantic property. They MUST NOT be treated as separate EABC boundary semantic properties or assigned separate property identifiers.

The legacy EBP-006 path-exclusion mapping concerns `NON_BYPASSABILITY(B,E)` only. It MUST NOT be extended to or conflated with the authority-based `EXCLUSIVITY(A,E,I)`.

### 4.4 Unauthorized modification of established execution authority

The modification element of the original P1 clause is retained as an explicit P1 sub-obligation.

It is not deleted, silently absorbed into `INTEGRITY_DEF(B)`, relabelled as `ENFORCEMENT_INDEPENDENCE`, or introduced as another boundary semantic property.

#### 4.4.1 Established execution authority

For this obligation, established execution authority means an authority grant or authoritative authority state that has been validly created and made operative under the applicable authority rules.

It includes, as applicable:

- the identity of the authority holder or issuer;
- the authorized subject or delegate;
- the authorized action or Protected Effect scope;
- the target or resource scope;
- the applicable conditions and constraints;
- the validity interval;
- delegation and decision rights;
- the operative rights to permit or refuse the protected action;
- the applicable revocation or withdrawal status.

The obligation applies after the authority has been established as operative.

#### 4.4.2 Unauthorized modification

Unauthorized modification means any alteration, substitution, reassignment, expansion, narrowing, or other change to established execution authority that is not validly authorized under the applicable authority rules.

It includes:

- changing the authority holder or issuer without authorization;
- changing the subject, target, action, or Protected Effect scope without authorization;
- extending or altering authority conditions or validity without authorization;
- changing delegation rights or operative decision rights without authorization;
- altering or suppressing revocation or withdrawal state without authorization;
- substituting a different authority grant or authority state while representing it as the established authority.

The governed system MUST NOT be capable of modifying, expanding, replacing, or otherwise altering its own established execution authority or operative decision rights without valid authorization from the entity or process entitled to grant that authority. This applies whether the governed system acts alone or participates with another component or actor. Participation by another component does not make a change authorized where the governed system lacks the authority to grant or approve it.

#### 4.4.3 Authorized changes and revocation

This obligation does not prohibit legitimate authority lifecycle operations.

An authorized authority holder or properly authorized delegate MAY amend, replace, narrow, suspend, or revoke established execution authority through an authorized procedure.

Such a change MUST be attributable to the entity or process entitled to authorize it and MUST be distinguishable from an unauthorized modification initiated or performed by the governed system.

The governed system MAY provide information, submit a request, or initiate a request for an authority change. It MUST NOT thereby acquire the power to authorize its own change.

A legitimate authority procedure MAY involve the governed system and other components, provided that the authority to approve and effect the change remains with the entity or process entitled to grant that authority. The governed system MUST NOT become an authorized source of its own authority merely because another component participates in the procedure.

A valid revocation MUST NOT be treated as unauthorized modification merely because it changes the previously established authority state.

The governing authority rules MUST identify who or what process is entitled to make such changes and under what conditions.

#### 4.4.4 Protected authority state and decision rights

The governed system MUST NOT be able to alter the established authority state or decision rights so as to:

- grant itself authority not validly granted;
- expand its own authority beyond the established scope;
- remove or weaken an applicable restriction;
- change who is entitled to make the operative authority determination;
- suppress, reverse, or misrepresent an authorized revocation;
- represent an unauthorized authority state as an authorized one.

This obligation concerns the integrity of established execution authority. It does not establish that every execution path is mediated by B; that is assessed under `NON_BYPASSABILITY(B,E)`.

#### 4.4.5 Evidence

Evidence for this P1 sub-obligation SHOULD permit an independent assessor to determine:

- the authority state that was established;
- the origin and identity of the entity or process entitled to establish it;
- the scope and operative decision rights of that authority;
- the authorized procedures for amendment, delegation, and revocation;
- the provenance of subsequent authority-state changes;
- whether any change was unauthorized or originated from the governed system;
- whether participation by the governed system in a change procedure was limited to information provision or requesting a change, rather than granting or approving its own authority.

Evidence MAY include authority records, versioned authority-state transitions, authenticated issuer or delegate identity, change authorization records, revocation records, or equivalent implementation-neutral evidence.

No particular cryptographic or storage mechanism is prescribed.

#### 4.4.6 Why this remains P1

This obligation protects the established authority grant and the authority decision rights that follow from it.

It is not a sixth boundary semantic property because it does not define a new relationship among boundary definition, boundary state, context, effect paths, or Parallel Commit Authorities.

It remains part of the broader P1 requirement that the governed entity cannot modify or self-authorize its own execution authority after authorization has been established.

It is also distinct from `INTEGRITY_DEF(B)`: the latter protects the definition governing the boundary instance, while this P1 sub-obligation protects the established execution authority and its operative rights.

## 5. Decision D — P3 and P1–P10 reconciliation

### 5.1 P3 deterministic commit semantics

P3 remains an EABC semantic obligation.

Its scope includes:

- explicit representation of the transition between authorization and execution;
- deterministic interpretation of the transition outcome;
- preservation of the distinction between authorization, attempted execution, committed effect, and execution failure;
- check-to-effect atomicity, meaning the absence of a gap between the decision and the effect it authorizes.

The current EABC 003 statement that atomicity of an authorization/commit transition does not by itself establish atomicity between COMMIT and a subsequent external EFFECT remains valid.

The subsequent normative migration MUST make clear that where those are distinct stages, the execution-boundary semantics must establish the check-to-effect atomicity required by P3.

### 5.2 Relationship to EBP assurance constraints

The following distinctions are preserved:

| Term | Layer | Meaning |
| --- | --- | --- |
| P3 deterministic commit semantics | EABC semantic obligation | Explicit and deterministic authorization-to-execution/commit semantics, including check-to-effect atomicity |
| `TEMPORAL_CONSISTENCY` | EBP assurance constraint | Assurance qualification concerning temporal consistency of the enforcement implementation |
| `MAX_ENFORCEMENT_LATENCY` | EBP assurance constraint | Assurance constraint on the maximum permitted enforcement latency |
| `ENFORCEMENT_INDEPENDENCE` | EBP assurance constraint | Assurance qualification concerning the enforcement mechanism's independence from the governed actor's trust domain or failure modes |
| Authority-Origin Independence | EABC P1 | Execution authority originates from a trust domain independent of the governed execution domain; the governed system cannot self-authorize |
| Non-Parallelism within `EXCLUSIVITY(A,E,I)` | EABC boundary semantic property | No Parallel Commit Authority exists for the same Protected Effect, scope, and Authority Interval |

`TEMPORAL_CONSISTENCY` MUST NOT replace or redefine P3.

`MAX_ENFORCEMENT_LATENCY` MUST NOT replace or redefine P3.

`ENFORCEMENT_INDEPENDENCE` MUST NOT replace Authority-Origin Independence or `EXCLUSIVITY(A,E,I)`.

An EBP assurance constraint may qualify the assurance of an implementation's satisfaction of an EABC semantic obligation. It does not become that semantic obligation.

### 5.3 P1–P10 reconciliation

The five boundary semantic properties do not replace the ten original EABC properties.

The following reconciliation preserves the treatment adopted by ADR R1 and clarifies the retained P1 modification obligation.

| Original property | Treatment | Reconciliation |
| --- | --- | --- |
| P1 — Independent Execution Authority | Split and clarified | Preserve the independent trust-domain origin requirement and anti-self-authorization. Map bypass to `NON_BYPASSABILITY`. Retain unauthorized modification of established execution authority as an explicit P1 sub-obligation. |
| P2 — Complete Mediation | Refined | Preserve P2 as an original EABC obligation. Refine its boundary-level path-mediation assessment through `NON_BYPASSABILITY(B,E)`, supported by topology-completeness and boundary-mediation evidence. |
| P3 — Deterministic Commit Semantics | Retained and clarified | Preserve explicit deterministic transition semantics and check-to-effect atomicity. `TEMPORAL_CONSISTENCY` and `MAX_ENFORCEMENT_LATENCY` remain separate EBP assurance constraints. |
| P4 — Context Binding | Refined | Preserve the original context-binding obligation and refine the boundary semantic treatment through `INTEGRITY_CTX(C,B,E)`. P4 is not replaced by the new property. |
| P5 — State Binding | Refined; both original obligations preserved | `INTEGRITY_STATE(B,E)` refines the obligation to identify the state against which authorization was evaluated. Independently preserve the consumer-facing obligation that consumers MUST be able to determine whether execution corresponded to the intended reference state or condition, expressly related by the applicable authorization and execution semantics to the state evaluated during authorization. The relationship MUST be identical-state or an explicitly designated relationship/transition with defined conditions, established as part of or expressly bound to the authorization decision. Subsequent changes MUST be covered by a transition expressly authorized in advance or by a new authorization/expressly authorized revalidation before execution. Evidence for `INTEGRITY_STATE(B,E)` does not automatically establish execution-state correspondence. Authenticity does not imply freshness. |
| P6 — Evidence Integrity | Retained | Preserve evidence-artifact integrity as a distinct EABC evidence obligation. It is not replaced by `INTEGRITY_DEF`, `INTEGRITY_STATE`, or `INTEGRITY_CTX`. |
| P7 — Evidence Correlation | Retained | Preserve evidence correlation and the intrinsically bound principle as distinct EABC evidence obligations. They are not replaced by `INTEGRITY_CTX`. |
| P8 — Failure Semantics | Retained and clarified | Preserve explicit failure semantics and the distinction between missing evidence and success. `FAIL_CLOSED` remains a profile-level guarantee refinement, not a universal replacement. |
| P9 — Implementation Neutrality | Retained | Preserve implementation neutrality. No boundary property or assurance constraint mandates a substrate or architecture. |
| P10 — Extensible Profiles | Retained and clarified | Preserve implementation-profile extensibility and the distinction between EABC Implementation Profiles and EAP Profiles. |

`INTEGRITY_DEF(B)` and `EXCLUSIVITY(A,E,I)` do not have direct one-to-one predecessors among P1–P10. They are elements of the adopted five-property boundary semantic set, not replacements for an original P1–P10 obligation.

The P1 modification sub-obligation is retained within P1 and does not create an additional boundary semantic property.

### 5.4 Mapping and evidence are not automatic duplication

The relationship between P1–P10 and the five boundary semantic properties is a semantic mapping, not an instruction to duplicate the same normative requirement.

Where one boundary property refines an existing P1–P10 obligation, the conformance assessment MUST preserve the original obligation's full scope and assess the boundary property according to its own defined scope.

Evidence MAY be reused across requirements only where it independently establishes each requirement's normative meaning.

In particular:

- `NON_BYPASSABILITY(B,E)` does not automatically establish all of P2;
- `INTEGRITY_CTX(C,B,E)` does not automatically establish all of P4;
- `INTEGRITY_STATE(B,E)` does not automatically establish all of P5, in particular the independent consumer-facing obligation to determine whether execution corresponded to the intended reference state or condition and its expressly declared relationship to the state evaluated during authorization under the applicable authorization and execution semantics; that relationship MUST be established as part of or expressly bound to the authorization decision, and subsequent changes MUST be covered by an expressly pre-authorized transition or new authorization/expressly authorized revalidation before execution;
- evidence establishing the authenticity and determination-binding of the state evaluated by B does not, by itself, establish that execution corresponded to the intended reference state or condition and its expressly declared relationship to the authorization-evaluated state under the applicable authorization and execution semantics;
- a boundary property does not automatically establish P6 or P7;
- P6 or P7 evidence does not automatically establish a boundary semantic property.

The assessment MUST identify the requirement supported by each item of evidence and the claim that the evidence establishes. Shared evidence MUST NOT be treated as a reason to collapse distinct requirements.

## 6. Decision E — Relationship to R1 and subsequent migration

### 6.1 R1 decisions that remain unchanged

Unless expressly clarified by A1, the following R1 decisions remain unchanged:

1. The five-element boundary semantic set adopted in R1 §1.
2. The definitions of Commit Authority, Authority Interval, and Parallel Commit Authority in R1 §2.
3. The distinction between `NON_BYPASSABILITY` and `EXCLUSIVITY` in R1 §3.
4. The path-based meaning of `NON_BYPASSABILITY`.
5. The requirement to identify Protected Effect Scope, Boundary Scope, Path Scope, and the method used to establish path coverage and completeness.
6. The separate EBP `ENFORCEMENT_INDEPENDENCE` qualification for `NON_BYPASSABILITY` assessments.
7. The distinction between state authenticity and freshness.
8. The separation of `ENFORCEMENT_INDEPENDENCE`, `TEMPORAL_CONSISTENCY`, and `MAX_ENFORCEMENT_LATENCY` from the EABC boundary semantic set.
9. P3 check-to-effect atomicity as an EABC semantic obligation.
10. The three meanings of independence in R1 §5.
11. The versioned EBP-006 legacy alias and its mapping to `NON_BYPASSABILITY`.
12. The distinction between semantic adoption and implementation/deployment conformance.

### 6.2 Questions resolved by A1, if accepted

A1 resolves the following outstanding questions:

- the normative scope and meaning of all three integrity properties;
- the choice between prevention and detection-before-decision-impact for `INTEGRITY_DEF`, and the threat-model binding of the prevention claim;
- the distinction between runtime state and execution context, and the preservation of both P5 obligations: identification/authenticity of the authorization-evaluated state through `INTEGRITY_STATE(B,E)`, and consumer-facing correspondence to an intended reference state whose relationship to that authorization-evaluated state is established as part of or expressly bound to the authorization decision, with subsequent changes limited to expressly pre-authorized transitions or new authorization/expressly authorized revalidation before execution;
- the allowance for a datum to have multiple normative roles where the architecture genuinely uses it in multiple ways;
- the separation of state authenticity and freshness;
- the authenticity and provenance requirements for context elements, as distinct from the authenticity of the context-to-boundary-to-effect binding, and the express exclusion of factual truth/correctness from what provenance alone establishes;
- the bounded lifecycle of the context-to-boundary-to-effect binding;
- the distinction between `INTEGRITY_CTX` and P3 check-to-effect atomicity;
- the distinction between the three integrity properties and P6/P7;
- the assessment requirements for `EXCLUSIVITY(A,E,I)`;
- the requirement to assess all five boundary semantic properties for full Level 1 conformance;
- the narrow circumstances in which N/A may be accepted, including the treatment of C = ∅ and self-accepted N/A;
- the preservation of partial/property-level conformance without creating a new conformance level;
- the independence of EABC conformance levels from EBP assurance tiers;
- the decomposition of the original P1 clause and preservation of its trust-domain origin, anti-self-authorization, and authority-modification obligations;
- the relationship between P2 and the two evidence dimensions for `NON_BYPASSABILITY`;
- the explicit P1–P10 reconciliation and evidence non-duplication rules.

### 6.3 Matters outside A1

A1 does not decide:

- the EAP Binding model or R2;
- the detailed EAP Profile model;
- EBP assurance-tier definitions or substrate-specific conformance;
- implementation-profile mappings;
- concrete implementation or deployment assessments;
- the evidence schema or serialization format for the new property assessments;
- any modification to EBP-006.

These matters require their own scoped work and, where appropriate, the relevant authority decision.

### 6.4 Required sequence

The subsequent work SHALL follow this sequence:

1. Review and accept A1 as a separate authority decision. Until accepted, its proposals remain proposals.
2. Prepare one coordinated normative migration PR for EABC 001–004, after A1 acceptance. The PR SHALL implement the accepted definitions, conformance rules, and P1–P10 reconciliation together, with only strictly necessary editorial references.
3. Prepare implementation-profile work separately. Profiles may then map concrete architectures to the accepted normative requirements without redefining them.
4. Prepare EBP assurance alignment separately. This work may reconcile assurance constraints and implementation qualifications with the accepted EABC semantics but MUST NOT merge the semantic and assurance layers.
5. Keep EAP Binding/R2 separate. Any EAP Binding decision remains the responsibility of the EAP Architecture Authority.

A1 does not authorize implementation of EABC 001–004 by itself. No normative migration is authorized until A1 has been reviewed and accepted by the EABC Specification Authority.

## 7. Authority decision record

### 7.1 Proposed outcome

**Outcome:** PENDING AUTHORITY REVIEW
**Status:** PROPOSED

### 7.2 Decisions requiring authority approval

The EABC Specification Authority is asked to approve or reject the following proposed decisions. The register IDs refer to Annex A.

1. Adoption of Option A — Prevention — for `INTEGRITY_DEF(B)`, with the threat-model binding, rather than Option B — Detection before decision impact, and the instance binding of the definition (A1-D01, A1-D02).
2. The normative definition of `INTEGRITY_STATE(B,E)`, including the preservation of the first original P5 obligation, the independent consumer-facing obligation to determine correspondence with an intended reference state expressly related to the state evaluated during authorization (identical or through a predefined and verifiable relationship/transition), the explicit separation of runtime state from execution context, and the separation of freshness (A1-D03, A1-D06, A1-D21).
3. The normative definition and bounded lifecycle of `INTEGRITY_CTX(C,B,E)`, including context-source authenticity and provenance, the clarification that provenance does not establish factual truth or correctness, and the rule for data with multiple normative roles (A1-D04, A1-D05).
4. The cross-property separation of the three integrity properties from P6 and P7 (A1-D07).
5. Mandatory assessment of all five boundary semantic properties for full Level 1 conformance (A1-D08).
6. The N/A restrictions and acceptance procedure in §3.3, including the treatment of C = ∅ and self-accepted N/A (A1-D09, A1-D10, A1-D11, A1-D12).
7. The preservation of partial/property-level conformance without a new conformance level (A1-D13).
8. The independence of EABC conformance levels from EBP assurance tiers (A1-D15).
9. The P1 decomposition, preserving the trust-domain origin requirement, anti-self-authorization, and unauthorized modification of established execution authority, and mapping bypass to `NON_BYPASSABILITY` (A1-D16, A1-D17, A1-D18).
10. The P2 mapping to `NON_BYPASSABILITY(B,E)` and the requirement for both topology-completeness and boundary-mediation evidence dimensions (A1-D19).
11. The P3 and P1–P10 reconciliation, including the evidence non-duplication rules (A1-D14, A1-D20, A1-D21).
12. The staged migration sequence in §6.4 (A1-D22).
13. The assessment requirements for `EXCLUSIVITY(A,E,I)` in §2.6 (A1-D23).

### 7.3 Authority response

**Outcome:** PENDING
**Authority:** EABC Specification Authority
**Decision date:** Pending
**Accepted amendments:** Pending
**Rationale:** Pending authority review

## Annex A — Decision register

All decisions below are proposals requiring explicit EABC Specification Authority approval.

| ID | Decision | Alternatives | Recommendation |
| --- | --- | --- | --- |
| A1-D01 | INTEGRITY_DEF guarantee | A: prevent unauthorized modification/substitution. B: permit modification but detect and reject before decision impact. | A — Prevention, assessed against a declared threat model bound to the definition scope and boundary instance. B is weaker and not equivalent. |
| A1-D02 | Definition authenticity and instance binding | Artifact-only integrity; or authentic definition plus demonstrable binding to the deciding boundary instance. | Authentic identity, scope, enforcement-relevant content, and instance binding. |
| A1-D03 | INTEGRITY_STATE subject and first P5 obligation | Narrow state of B only; or all runtime state B evaluates or relies on. | Runtime state evaluated by B, covering operational state of B, relevant condition of the governed system/target, and policy/configuration/delegated-authority state or version values; authentic and bound to the determination. This refines the first P5 obligation only; it does not by itself establish the separate consumer-facing execution-state correspondence obligation. |
| A1-D04 | STATE/CTX overlap and context provenance | Force every datum into one category; or allow multiple genuine normative roles while preserving context provenance. | Allow multiple roles, but identify and assess each role independently; establish the authenticity and provenance of context elements under the declared authoritative-source and derivation rules. Provenance does not, by itself, establish factual truth or correctness; any required factual validation must be specified separately. |
| A1-D05 | INTEGRITY_CTX lifecycle | Unbounded lifecycle; or bounded determination-to-effect interval. | Bounded interval from determination through associated effect, with explicit invalidation conditions. |
| A1-D06 | Freshness | Include freshness in STATE; or treat it separately. | Freshness remains separate from INTEGRITY_STATE. |
| A1-D07 | Integrity properties vs P6/P7 | Merge into evidence integrity/correlation; or preserve separate semantic subjects. | Preserve separate boundary semantic and evidence obligations. |
| A1-D08 | Level 1 property set | P1–P10 alone; or P1–P10 plus assessment of the five boundary properties. | Require assessment of all five for full Level 1. |
| A1-D09 | N/A for NON_BYPASSABILITY and EXCLUSIVITY | Permit scope-based N/A; or prohibit it. | Prohibit N/A. |
| A1-D10 | N/A for INTEGRITY_DEF | Permit N/A for embedded or immutable definitions; or prohibit N/A for a claimed boundary. | Prohibit N/A for a claimed boundary. |
| A1-D11 | N/A for STATE and CTX | Broad implementation-declared N/A; or narrowly scope-derived N/A. | Permit only objective, formally scoped, assessor-accepted N/A. Explicit C = ∅ remains applicable. |
| A1-D12 | N/A acceptance | Implementer declaration; or explicit assessor acceptance. | Implementer may propose; assessor must accept and record; implementer-performed assessments mark accepted N/A as self-accepted. |
| A1-D13 | Partial conformance | Create a new level; or retain current EABC 004 mechanism. | Retain current partial/property-level mechanism; no new level. |
| A1-D14 | Evidence reuse | Treat shared evidence as satisfying all mapped requirements; or require independent claim support. | Evidence may be shared only if it independently establishes each requirement's normative meaning. |
| A1-D15 | EABC/EBP relationship | Couple conformance levels to EBP tiers; or keep assessment layers separate. | Preserve R1 §3.6: EBP tiers do not determine EABC conformance. |
| A1-D16 | P1 Authority-Origin Independence | Reduce to a single-entity origin statement; or preserve trust-domain origin and anti-self-authorization. | Preserve both aspects and their qualified terminology; a request to or grant by an independent-trust-domain authority is not self-authorization. |
| A1-D17 | P1 modification | Prohibit only unilateral changes; or require that the governed system not be capable of altering its authority without valid authorization from the entitled authority/process. | Capability-based prohibition; participation by another component does not grant the governed system authority over its own change. |
| A1-D18 | P1 bypass | Retain a duplicate bypass clause; or map it to NON_BYPASSABILITY. | Map bypass to NON_BYPASSABILITY with the stated justification; do not retain a duplicate P1 property. |
| A1-D19 | P2 evidence | Treat topology completeness and mediation as one undifferentiated item; or preserve two necessary dimensions. | Require both deployment-topology completeness and boundary mediation. |
| A1-D20 | P3 and assurance constraints | Treat temporal assurance constraints as replacements; or preserve P3 semantics. | Preserve P3 check-to-effect atomicity; keep TEMPORAL_CONSISTENCY and MAX_ENFORCEMENT_LATENCY in EBP. |
| A1-D21 | P1–P10 reconciliation and P5 preservation | Replace original properties; or map without loss or duplication. | Preserve P1–P10 and explicitly map the five boundary properties. For P5, retain both original obligations: identification of the state against which authorization was evaluated, refined through `INTEGRITY_STATE(B,E)`, and the independent consumer-facing obligation to determine whether execution corresponded to the intended reference state or condition expressly related to that authorization-evaluated state by the applicable authorization and execution semantics. The relationship MUST be identical-state or a distinct, predefined and verifiable relationship/transition with defined conditions, including any expressly permitted state evolution, and MUST be established as part of or expressly bound to the authorization decision. Subsequent changes MUST be covered by a transition expressly authorized in advance or by new authorization/expressly authorized revalidation before execution. Neither claim automatically establishes the other. |
| A1-D22 | Migration sequence | Migrate immediately; or wait for separate A1 acceptance. | Accept A1 first, then prepare one coordinated 001–004 migration PR. |
| A1-D23 | EXCLUSIVITY assessment requirements | Leave EXCLUSIVITY without assessment rules; or require reference-authority designation, candidate inventory with completeness method, conditioning relationships, and no new authority type for mutual conditioning. | Require the §2.6 assessment requirements; do not introduce a new entity type for mutually conditioned determinations. |

## Annex B — Matters for confirmation during authority review

**B.1 Scope of Option A.** Option A is intentionally strong: unauthorized modification or substitution of the applicable boundary definition cannot occur under the declared threat model. It does not require physical immutability of every copy or archival representation. The Authority should confirm that this is the intended scope of prevention. If the Authority prefers detect-and-reject semantics for a particular class of implementation, it should select Option B explicitly rather than treating it as equivalent to Option A.

**B.2 N/A acceptance authority.** The record requires explicit acceptance by the party responsible for the conformance assessment and requires self-accepted N/A to be marked as such, but it does not define an assessor role or an organizational-independence requirement. If the Authority wants a particular assessor qualification, that should be added as an explicit decision rather than inferred from the term "assessor".

**B.3 P1 authority-change procedure.** The record identifies the distinction between the authority entitled to approve a change, the governed system's ability to request or provide information, and the governed system's inability to authorize its own authority change. It does not prescribe a universal authority-change protocol; that remains implementation- and profile-specific, provided the P1 obligation is satisfied.
