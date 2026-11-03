# EABC Specification Decision R1

**Decision ID:** EABC-ADR-R1  
**Title:** Adoption of the Five-Element EABC Boundary Semantic Set and Migration of Existing Property Semantics  
**Authority:** EABC Specification Authority  
**Status:** AMENDED  
**Outcome:** ACCEPTED  
**Date:** 2026-11-03  
**Amendments:** See Section 8

## 1. Decision

The EABC Specification Authority adopts the following five-element boundary semantic set as the working normative baseline for the EABC boundary semantic layer:

1. `NON_BYPASSABILITY(B,E)`
2. `INTEGRITY_DEF(B)`
3. `INTEGRITY_STATE(B,E)`
4. `INTEGRITY_CTX(C,B,E)`
5. `EXCLUSIVITY(A,E,I)`

where B is a boundary, E a Protected Effect, C a context, A a Commit Authority, and I an Authority Interval.

This adoption does not replace the broader EABC model or eliminate the existing authority, evidence, failure-semantics, implementation-neutrality, and profile-extensibility requirements.

## 2. Definitions

**Commit Authority:** An entity whose determination of `COMMIT(E)` or `REJECT(E)` is operative for a Protected Effect E, meaning the effect is admitted or refused according to that determination. A path that transmits or realizes an effect without making or conditioning on such a determination is a path, not a Commit Authority.

**Authority Interval (I):** The interval, within a stated scope, over which a Commit Authority holds the right to decide on E.

**Parallel Commit Authority:** A Commit Authority A′, distinct from A, whose determination of `COMMIT(E)` or `REJECT(E)` is operative for the same Protected Effect E, scope, and Authority Interval I, and whose determination is not conditioned on the determination of A.

The existence of a decision function alone shall not be sufficient to establish a Parallel Commit Authority. The function must constitute an operative Commit Authority under the definition above.

Conditioning of A's determination on A′'s determination does not, by itself, establish that A′ is a Parallel Commit Authority.

Where A′'s determination is not conditioned on A's determination, A′ satisfies this definition irrespective of whether A's determination is conditioned on A′'s.

Where the determinations are mutually conditioned, A′ does not satisfy this definition.

## 3. Semantic clarifications

1. `NON_BYPASSABILITY` and `EXCLUSIVITY` are distinct properties. Neither is defined in terms of the other, and satisfaction of one shall not be inferred from satisfaction of the other.

2. `NON_BYPASSABILITY` concerns paths: whether any path can create E without mediation by B.

3. `EXCLUSIVITY(A,E,I)` concerns decision authority: whether any Parallel Commit Authority exists for E over I.

4. A bypass path that realizes E without mediation by B, but without introducing a Parallel Commit Authority, violates `NON_BYPASSABILITY` only. A bypass path that introduces a Parallel Commit Authority for the same E, scope, and I violates both `NON_BYPASSABILITY` and `EXCLUSIVITY(A,E,I)`. The existence of a decision function alone shall not be sufficient to establish a Parallel Commit Authority; the function must constitute an operative Commit Authority under the definitions above. Assessments shall identify which case applies.

5. `NON_BYPASSABILITY` assessments shall explicitly identify Protected Effect Scope, Boundary Scope, Path Scope, and the method used to establish path coverage and completeness.

6. A `NON_BYPASSABILITY` assessment shall declare the applicable level of `ENFORCEMENT_INDEPENDENCE` as a separate EBP assurance qualification. This qualification shall not alter the semantic definition of `NON_BYPASSABILITY` or be treated as evidence of path completeness.

   A `NON_BYPASSABILITY` claim without a declared level may be recorded as a semantic claim, with an unspecified enforcement-independence qualification. Such a claim shall not be used as the basis for assigning an assurance tier or making a conformance assertion that depends on that tier until the applicable level has been declared and assessed.

7. `INTEGRITY_STATE` establishes state authenticity and does not, by itself, establish freshness.

8. `ENFORCEMENT_INDEPENDENCE`, `TEMPORAL_CONSISTENCY`, and `MAX_ENFORCEMENT_LATENCY` remain EBP assurance constraints and are not additional EABC boundary semantic properties.

9. The check-to-effect atomicity obligation (absence of a gap between the decision and the effect it authorizes) remains a semantic obligation of EABC deterministic commit semantics (P3, EABC 003). `TEMPORAL_CONSISTENCY` is its assurance-layer counterpart, not its replacement.

## 4. Informative logical expression

The following expression is informative and does not constitute a separate normative definition:

`EXCLUSIVITY(A,E,I) ≡ ¬∃A′ : A′ ≠ A ∧ Parallel(A′,A,E,I)`

Here, `Parallel(A′,A,E,I)` is shorthand for the Parallel Commit Authority relationship defined in Section 2. The normative meaning is governed exclusively by the textual definitions in that section.

## 5. Terminology: three uses of "independence"

| Term | Layer | Meaning |
|---|---|---|
| Authority-Origin Independence (P1) | EABC authority semantics | The authority's mandate does not originate from the entity whose action it governs |
| Enforcement Independence | EBP assurance | The enforcement mechanism is not subject to the trust domain or failure modes of the governed actor |
| Non-Parallelism (inside `EXCLUSIVITY`) | EABC boundary semantics | No Parallel Commit Authority exists for E over I |

These terms shall not be used interchangeably. The bare word "independent" shall not be used in normative text without one of these qualifiers.

## 6. Migration requirements

The migration shall preserve the semantic obligations of EABC P1–P10:

- P1 authority-origin independence shall remain explicit in EABC authority semantics.
- P2 shall be refined through `NON_BYPASSABILITY`.
- P3 shall remain in EABC deterministic commit semantics, including check-to-effect atomicity.
- P4 and P5 shall be refined through context and state integrity, respectively.
- P6 and P7 shall remain in EABC evidence semantics.
- P8 shall remain in EABC failure semantics; `FAIL_CLOSED` is a profile-level guarantee refinement, not a universal replacement.
- P9 shall remain an implementation-neutrality principle.
- P10 shall preserve the distinction between EABC Implementation Profiles and EAP Profiles.

### EBP-006 terminology migration

- The previous EBP-006 `Exclusivity` (absence of bypass paths) is migrated to `NON_BYPASSABILITY`.
- Existing references to the old meaning shall carry a versioned alias (`EBP-006:Exclusivity@v1` → `NON_BYPASSABILITY`). The term `Exclusivity` shall not be silently redefined in place.
- The new `EXCLUSIVITY(A,E,I)` shall be introduced under the new definition only after all references to the old meaning have been updated or aliased.

## 7. Consequences

EABC 001–004 and EBP-006 shall be reviewed and updated for consistency with this decision.

The decision establishes semantic adoption only. It does not establish implementation conformance, deployment conformance, or the validity of any particular SLC substrate.

The semantic claim and assurance qualification of `NON_BYPASSABILITY` shall remain separately identifiable in assessments and evidence.

## 8. Amendments

The following amendments were incorporated relative to the original R1 proposal:

1. `EXCLUSIVITY` was parameterized as `EXCLUSIVITY(A,E,I)`.
2. Commit Authority, Authority Interval, and Parallel Commit Authority were explicitly defined.
3. The decision-function test was clarified: a decision function alone does not establish a Parallel Commit Authority.
4. The distinction between path bypass and parallel commit authority was refined, including the case in which a bypass path violates both properties.
5. The logical expression for `EXCLUSIVITY` was classified as informative, with the normative definition residing exclusively in the textual definitions.
6. Conditioning relationships between A and A′ were clarified, including the case where A′'s determination is not conditioned on A's irrespective of whether A's determination is conditioned on A′'s.
7. The three meanings of independence were explicitly distinguished.
8. The `NON_BYPASSABILITY` enforcement-independence qualification was clarified, including the treatment of claims with an unspecified qualification.
9. P3 check-to-effect atomicity was explicitly retained as an EABC semantic obligation.
10. The original EBP-006 Exclusivity meaning was assigned a versioned migration alias.

## 9. Authority decision

**Outcome:** ACCEPTED  
**Status:** AMENDED  
**Rationale:** The amended proposal resolves the identified semantic ambiguities by explicitly distinguishing path mediation from operative commit authority, defining the parameters and conditions of `EXCLUSIVITY`, separating the three uses of independence, preserving check-to-effect atomicity in P3, and defining the assurance qualification required for `NON_BYPASSABILITY` claims.

**Authority:** EABC Specification Authority  
**Authority Holder:** Founder and owner of the architectural direction of Equinibrium  
**Decision Date:** 2026-11-03
