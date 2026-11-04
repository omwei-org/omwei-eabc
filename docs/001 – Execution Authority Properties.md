# Execution Authority Boundary Contract (EABC)

# 001 – Execution Authority Properties

## Purpose

This document defines the normative obligations of the Execution Authority Boundary Contract (EABC).

EABC retains the original P1–P10 obligations and adopts a distinct five-property boundary semantic set. The five boundary semantic properties refine and make assessable particular boundary-level guarantees; they do not replace P1–P10, create duplicate copies of those obligations, or eliminate the independent authority, evidence, failure-semantics, implementation-neutrality, and profile-extensibility requirements.

The normative subject of each requirement is stated separately. A mapping between requirements does not make one requirement automatically satisfied by another.

## Relationship to the Execution Authority Whitepaper

EABC remains accountable to the architectural principles and operationalization model of the Execution Authority research whitepaper. The original P1–P10 obligations retain their established relationship to the whitepaper and its operationalization layer. The boundary semantic set is an additional normative layer adopted by ADR R1 and clarified by accepted decision A1.

EABC describes observable guarantees, not a mandatory implementation architecture, substrate, protocol, storage mechanism, or cryptographic construction.

The original P1–P10 obligations retain their established relationship to the Execution Authority whitepaper:

| EABC obligation | Origin |
|---|---|
| P1 — Independent Execution Authority | Whitepaper Section 3 — Independence |
| P2 — Complete Mediation | Whitepaper Section 3 — Complete Mediation |
| P3 — Deterministic Commit Semantics | Whitepaper Section 3 — Determinism and Commit Control |
| P4 — Context Binding | Whitepaper Section 3 — State/Context Binding (context component), operationalized through the ACT `context` and `constraints` fields |
| P5 — State Binding | Whitepaper Section 3 — State/Context Binding (state component), operationalized through the ACT `validity` field and EAtt `execution_context` |
| P6 — Evidence Integrity | Operationalization layer — EAtt `integrity` field |
| P7 — Evidence Correlation | Operationalization layer — EAtt causal binding to ACT_hash |
| P8 — Failure Semantics | Operationalization layer — Verification Outcome and EAtt `result` field |
| P9 — Implementation Neutrality | Whitepaper Section 5.4 — Technology Neutrality |
| P10 — Extensible Profiles | EABC-specific; realizes the expectation in Whitepaper Section 12.4 that implementation-level questions be resolved by a downstream specification |

This mapping preserves the original distinction between the whitepaper's theoretical properties and its operationalization layer. The five boundary semantic properties are an additional EABC normative layer adopted by ADR R1 and clarified by A1; they do not replace or renumber P1–P10.

---

# 1. Five boundary semantic properties

The EABC boundary semantic set consists of exactly the following five properties:

1. `NON_BYPASSABILITY(B,E)`
2. `INTEGRITY_DEF(B)`
3. `INTEGRITY_STATE(B,E)`
4. `INTEGRITY_CTX(C,B,E)`
5. `EXCLUSIVITY(A,E,I)`

where B is an execution boundary, E is a Protected Effect, C is execution context, A is a Commit Authority, and I is an Authority Interval.

These five properties are distinct from the original P1–P10 obligations. Their normative meanings are defined below.

## 1.1 NON_BYPASSABILITY(B,E)

`NON_BYPASSABILITY(B,E)` concerns paths: whether any path capable of producing Protected Effect E can produce E without mediation by boundary B.

A bypass path is an in-scope path capable of producing E without mediation by B. A path that transmits or realizes an effect without making or conditioning on a `COMMIT(E)` or `REJECT(E)` determination is a path, not by that fact alone a Commit Authority.

A `NON_BYPASSABILITY(B,E)` assessment MUST identify:

- the Protected Effect Scope;
- the Boundary Scope;
- the Path Scope; and
- the method used to establish path coverage and completeness.

The assessment MUST establish both of the following evidence dimensions:

1. **Deployment-topology completeness:** the declared in-scope path universe has not omitted relevant paths capable of producing E. The assessment MUST provide a basis for concluding that the path inventory is sufficiently complete for the claim.
2. **Boundary mediation:** each identified in-scope path capable of producing E is mediated by B. The assessment MUST provide evidence about B's behavior on the identified paths showing that they cannot produce E without the required mediation by B.

Both dimensions are necessary. Topology-completeness evidence alone does not establish mediation. Boundary-mediation evidence alone does not establish that the path inventory is complete.

These are evidence dimensions for one semantic property. They MUST NOT be treated as separate EABC boundary semantic properties or assigned separate property identifiers.

A bypass path that produces E without mediation by B, but without introducing a Parallel Commit Authority, violates `NON_BYPASSABILITY` only. A bypass path that introduces a Parallel Commit Authority for the same E, scope, and I violates both `NON_BYPASSABILITY` and `EXCLUSIVITY(A,E,I)`. The assessment MUST identify which case applies.

The previous EBP-006 `Exclusivity` path-exclusion meaning is migrated to `NON_BYPASSABILITY(B,E)`. The legacy reference MUST be identified only by the versioned alias `EBP-006:Exclusivity@v1` → `NON_BYPASSABILITY(B,E)`. The legacy path-exclusion meaning MUST NOT be silently redefined as the new authority-based `EXCLUSIVITY(A,E,I)`.

A `NON_BYPASSABILITY` assessment MUST declare the applicable `ENFORCEMENT_INDEPENDENCE` level as a separate EBP assurance qualification. The qualification does not alter the semantic definition and is not evidence of path completeness. A semantic claim with an unspecified qualification may be recorded as such, but MUST NOT be used to assign an assurance tier or make a conformance assertion that depends on that tier until the qualification is declared and assessed.

## 1.2 INTEGRITY_DEF(B)

`INTEGRITY_DEF(B)` establishes the authenticity and integrity of the boundary definition applicable to boundary B.

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

**Accepted guarantee — Option A (Prevention)**

The applicable boundary definition MUST NOT be modified or substituted without authorization. Unauthorized modification or substitution of the applicable definition is a failure of this guarantee even if the alteration is later detected and rejected before it affects a determination.

This guarantee concerns the applicable definition itself. It does not require physical immutability of every copy, representation, or archival instance. An authorized update or replacement MAY occur only under an authorized procedure satisfying the requirements below.

The guarantee MUST be assessed against a declared threat model. The assessment MUST identify the adversary capabilities and trust assumptions under which unauthorized modification or substitution is claimed to be prevented. The threat model MUST be bound to the scope of the applicable definition and to the boundary instance under assessment. A general threat model not tied to that scope and instance does not make the prevention claim assessable.

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

#### 2.1.5 Distinction from other requirements

`INTEGRITY_DEF(B)` does not establish:

- the integrity or authenticity of runtime state used for a particular determination; that is `INTEGRITY_STATE(B,E)`;
- the integrity of the context-to-boundary-to-effect binding; that is `INTEGRITY_CTX(C,B,E)`;
- the integrity of evidence artifacts generally; that remains P6, Evidence Integrity;
- the absence of an execution path that bypasses B; that is `NON_BYPASSABILITY(B,E)`;
- the absence of a Parallel Commit Authority; that is `EXCLUSIVITY(A,E,I)`.

A signature, hash, or authenticated configuration artifact MAY contribute evidence, but none is sufficient by itself to establish `INTEGRITY_DEF(B)`. The assessment must also establish that the authentic definition is the one applicable to the boundary instance making the determination.

## 1.3 INTEGRITY_STATE(B,E)

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

## 1.4 INTEGRITY_CTX(C,B,E)

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

## 1.5 EXCLUSIVITY(A,E,I)

ADR R1 defines:

- **Commit Authority:** an entity whose determination of `COMMIT(E)` or `REJECT(E)` is operative for a Protected Effect E, meaning the effect is admitted or refused according to that determination. A path that transmits or realizes an effect without making or conditioning on such a determination is a path, not a Commit Authority.
- **Authority Interval (I):** the interval, within a stated scope, over which a Commit Authority holds the right to decide on E.
- **Parallel Commit Authority:** a Commit Authority A′, distinct from A, whose determination of `COMMIT(E)` or `REJECT(E)` is operative for the same Protected Effect E, scope, and Authority Interval I, and whose determination is not conditioned on the determination of A.

The existence of a decision function alone is not sufficient to establish a Parallel Commit Authority. The function MUST constitute an operative Commit Authority under the definition above.

Conditioning of A's determination on A′'s determination does not, by itself, establish that A′ is a Parallel Commit Authority. Where A′'s determination is not conditioned on A's determination, A′ satisfies the definition irrespective of whether A's determination is conditioned on A′'s. Where the determinations are mutually conditioned, A′ does not satisfy the definition solely on that basis.

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

## 1.6 Separation among the five properties and P6/P7

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

---

# 2. Original EABC P1–P10 obligations

The five boundary semantic properties do not replace the ten original EABC properties. Each original obligation remains normative and MUST be assessed in its own meaning. The mapping below preserves the full original scope and clarifies how the boundary semantic properties relate to it.

## P1 — Independent Execution Authority

The original P1 obligation contains the following requirements:

> Execution authority MUST originate from a trust domain that is independent of the governed execution domain.

> The governed system MUST NOT be capable of modifying, bypassing, or self-authorizing execution authority after authorization has been established.

The second sentence contains distinct obligations. The bypass element is assessed through `NON_BYPASSABILITY(B,E)`; it is not retained as a duplicate P1 semantic property. The authority-origin, anti-self-authorization, and unauthorized-modification obligations remain P1 obligations.

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

### Original P1 rationale

A system cannot independently authorize actions that it is also free to modify.

Separation of execution authority establishes an independently verifiable trust boundary.

This property operationalizes the whitepaper's Independence axiom: ¬Control(A_D, EB) (Section 3.2.2).

### Original P1 evidence guidance

An implementation SHOULD provide evidence demonstrating:

* authority origin
* trust-domain identity
* authority integrity
* authority authenticity

## P2 — Complete Mediation

Every externally committed action MUST pass through the execution-authority boundary.

No execution path capable of producing externally observable effects may bypass evaluation by the execution-authority system.

P2 remains an original EABC obligation. `NON_BYPASSABILITY(B,E)` refines the boundary-level path-mediation assessment and requires both deployment-topology completeness and boundary mediation. A `NON_BYPASSABILITY` claim does not automatically establish all of P2. The conformance assessment MUST preserve and assess P2's full scope separately.

### Original P2 rationale

Partial mediation creates execution paths that cannot be governed.

The contract therefore assumes that every committed action is mediated.

This property operationalizes the whitepaper's Complete Mediation axiom (Section 3.2.1).

### Original P2 evidence guidance

Implementations SHOULD demonstrate:

* mediation identifier
* decision correlation
* execution correlation
* audit continuity

## P3 — Deterministic Commit Semantics

The transition between authorization and execution MUST be explicitly represented. The outcome of this transition MUST be deterministic.

Consumers MUST be able to distinguish authorization granted, authorization denied, execution attempted, execution committed, and execution failed without ambiguity.

P3 includes check-to-effect atomicity: the absence of a gap between the decision and the effect it authorizes. This remains an EABC semantic obligation. It is not replaced by an EBP assurance constraint.

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

### Original P3 rationale

Consumers must be able to distinguish:

* authorization granted
* authorization denied
* execution attempted
* execution committed
* execution failed

without ambiguity.

This property operationalizes the whitepaper's Determinism and Commit Control properties (Section 3), which govern the atomic validated-to-committed transition referenced in the EAtt `commit_event` field (Section 9.3).

### Original P3 evidence guidance

Implementations SHOULD expose:

* commit decision
* execution outcome
* execution status
* failure reason

## P4 — Context Binding

Execution authority MUST be cryptographically or otherwise integrity-bound to the execution context for which it was issued.

Execution authority MUST NOT be reusable outside its intended scope.

`INTEGRITY_CTX(C,B,E)` refines the boundary semantic treatment of context authenticity and the context-to-boundary-to-effect binding. It does not replace all of P4. P4 MUST be assessed in its full original meaning, and evidence for `INTEGRITY_CTX(C,B,E)` does not automatically establish all of P4.

### Original P4 rationale

Execution authority without context binding can be replayed or misapplied.

This property operationalizes the context component of the whitepaper's State/Context Binding property (Section 3), corresponding to the `constraints` and `context` fields of the Authorization Artifact (Section 8.3).

### Original P4 evidence guidance

Examples include:

* workload identity
* target resource
* execution context
* validity interval
* execution constraints

## P5 — State Binding

The original P5 requirement contains two distinct obligations:

> Execution authority MUST identify the state against which authorization was evaluated.

> Consumers MUST be able to determine whether execution occurred against the intended state.

The first obligation is refined through `INTEGRITY_STATE(B,E)`. The second remains independently applicable and MUST be assessed in its own consumer-facing meaning. Its complete normative clarification is reproduced verbatim as §2.2.6 under §1.3 above.

### Original P5 rationale

Authorization decisions are meaningful only within the state in which they were evaluated.

This property operationalizes the state component of the whitepaper's State/Context Binding property (Section 3), corresponding to the `validity` field of the Authorization Artifact and the `execution_context` field of the Execution Attestation (Sections 8.3, 9.3).

### Original P5 evidence guidance

Typical evidence includes:

* policy version
* configuration version
* delegated authority version
* decision-record hash
* state hash

## P6 — Evidence Integrity

Execution-authority evidence MUST be tamper evident.

Consumers MUST be able to determine whether evidence has been modified.

P6 concerns evidence artifacts. It is not replaced by `INTEGRITY_DEF(B)`, `INTEGRITY_STATE(B,E)`, or `INTEGRITY_CTX(C,B,E)`.

### Original P6 rationale

Execution authority depends on trustworthy evidence rather than trust in implementation.

This property operationalizes the `integrity` field of the whitepaper's Execution Attestation (Section 9.3); it belongs to the whitepaper's operationalization layer rather than to the Section 3 theoretical properties.

### Original P6 evidence guidance

Examples include:

* digital signatures
* integrity hashes
* immutable audit records
* authenticated event chains

## P7 — Evidence Correlation

Evidence generated throughout authorization and execution MUST be correlatable.

Consumers MUST be able to reconstruct the execution-authority chain.

P7 remains a distinct evidence obligation. Intrinsic integrity protection of correlation references is specified in 002 — Evidence Model. `INTEGRITY_CTX(C,B,E)` does not replace P7.

### Original P7 rationale

Independent verification requires continuity across architectural layers.

This property operationalizes the causal binding EAtt ⇒ (ACT + EA + CommitEvent) defined in the whitepaper (Section 9.4), and is a precondition for the Artefact Chain Integrity requirement discussed in the whitepaper's Section 12.1.

### Original P7 evidence guidance

Typical correlation includes:

* lifecycle identifier
* correlation identifier
* execution identifier
* decision identifier

## P8 — Failure Semantics

Failure conditions MUST be explicitly represented.

Missing evidence SHALL NOT be interpreted as successful execution.

Consumers must be able to distinguish denied, failed, cancelled, expired, unavailable, and unknown outcomes as applicable. `FAIL_CLOSED` is a profile-level guarantee refinement, not a universal replacement for P8.

### Original P8 rationale

Consumers must distinguish between:

* denied
* failed
* cancelled
* expired
* unavailable
* unknown

This property operationalizes the `result` field of the Execution Attestation and the possible verification outcomes described in the whitepaper's Verification Model (Sections 9.3, 10.5); the whitepaper leaves the specific outcome vocabulary open, which EABC's companion document **003 – Failure and Execution Semantics** resolves.

### Original P8 evidence guidance

Implementations SHOULD provide explicit terminal states.

## P9 — Implementation Neutrality

The execution-authority contract MUST describe observable properties rather than implementation mechanisms.

Conformance is determined by demonstrated properties, not implementation similarity. No boundary property mandates a particular substrate or architecture.

### Original P9 rationale

Multiple independent architectures should be capable of satisfying the same contract.

Conformance is determined by demonstrated properties, not implementation similarity.

This property operationalizes the whitepaper's Technology Neutrality principle (Section 5.4): required boundary strength is a function of protected consequences, not of implementation technology.

---

## P10 — Extensible Profiles

Concrete implementations SHALL define implementation profiles mapping their internal constructs to the EABC properties.

Implementation profiles MUST NOT redefine normative EABC properties.

P10 preserves the distinction between an EABC Implementation Profile, which maps a concrete implementation to EABC requirements, and an EAP Profile. These are not interchangeable profile types.

---

### Original P10 rationale

The contract remains stable while implementations evolve independently.

This property has no direct whitepaper counterpart; it realizes, at the specification layer, the whitepaper's Section 12.4 expectation that concrete data formats, protocols, and implementation-level questions be resolved by a downstream Specification rather than by the theory itself.

---

# 3. Terminology and separation from EBP assurance

The term "independence" has three distinct meanings and MUST NOT be used without its qualifier in normative text:

| Term | Layer | Meaning |
|---|---|---|
| Authority-Origin Independence (P1) | EABC authority semantics | Execution authority originates from a trust domain independent of the governed execution domain; the governed system cannot self-authorize. |
| `ENFORCEMENT_INDEPENDENCE` | EBP assurance | Assurance qualification concerning the enforcement mechanism's trust domain and failure modes relative to the governed actor. |
| Non-Parallelism within `EXCLUSIVITY(A,E,I)` | EABC boundary semantics | No Parallel Commit Authority exists for the same Protected Effect, scope, and Authority Interval. |

The following remain EBP assurance constraints and are not additional EABC boundary semantic properties:

- `ENFORCEMENT_INDEPENDENCE`;
- `TEMPORAL_CONSISTENCY`;
- `MAX_ENFORCEMENT_LATENCY`.

P3 deterministic commit semantics, including check-to-effect atomicity, remains an EABC semantic obligation. `TEMPORAL_CONSISTENCY` and `MAX_ENFORCEMENT_LATENCY` may qualify assurance of an implementation but MUST NOT replace, redefine, or discharge P3.

An EBP assurance constraint may qualify the assurance of an implementation's satisfaction of an EABC semantic obligation. It does not become that semantic obligation. EABC conformance MUST NOT be inferred from an EBP assurance tier.

---

# Summary

A complete EABC assessment preserves both normative layers:

| Layer | Required assessment subjects |
|---|---|
| Original EABC obligations | P1 through P10, each in its own normative meaning |
| Boundary semantic set | `NON_BYPASSABILITY(B,E)`, `INTEGRITY_DEF(B)`, `INTEGRITY_STATE(B,E)`, `INTEGRITY_CTX(C,B,E)`, and `EXCLUSIVITY(A,E,I)` |
| EBP assurance | Applicable assurance constraints assessed separately from EABC semantic conformance |

Evidence MAY be reused across requirements only where it independently establishes each requirement's normative meaning. A mapping or shared evidence artifact MUST NOT collapse distinct obligations.

A conforming implementation remains free to choose its architecture, provided it demonstrates the required properties and supplies evidence sufficient for independent assessment.
