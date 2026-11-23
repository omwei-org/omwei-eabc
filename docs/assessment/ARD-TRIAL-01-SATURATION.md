# ARD-TRIAL-01-SATURATION.md

**Title:** ARD Trial 1 — Saturation and Counting Rules  
**Status:** OWNER APPROVED — PREREGISTRATION CANDIDATE  
**Version:** 0.1  
**Applies to:** ARD-TRIAL-01  
**Methodological baseline:** ARD-001 v0.3  
**Purpose:** Preregistration of discovery counting, independence, diversity, route identity, and saturation criteria.

---

## 1. Purpose and status

This document defines the operational counting rules and saturation criteria for ARD Trial 1.

It supplements the ARD-001 v0.3 methodology and the Trial 1 target specification. It does not modify the normative or methodological content of ARD-001 v0.3.

The purpose is to ensure that:

- discovery runs are counted consistently;
- paired raw-artifact and declared-model discovery is treated as one methodological unit;
- analytical diversity is demonstrated rather than assumed;
- route and failure-class stability are measured against predefined thresholds;
- route identity decisions are reproducible and auditable;
- saturation is assessed as a property of the discovery process, not as proof of the absence of bypasses.

This document is a proposed preregistration supplement. It does not, by itself, freeze the preregistration or authorize discovery execution.

## 2. Counting units

Three distinct units are used.

### 2.1. Discovery execution

A discovery execution is one separately performed analytical examination of the target system using one specified representation of the system model M.

Each execution produces its own record containing:

- execution ID;
- paired block ID;
- analytical approach;
- M representation (`RAW_ARTIFACT` or `DECLARED_MODEL`);
- pinned target version;
- E, B, A and S input references;
- analyst/model and execution conditions;
- tool and access scope;
- discovered route candidates;
- assumptions and evidence gaps;
- rejected candidates and reasons;
- unexamined areas.

One paired discovery block contains two discovery executions.

### 2.2. Paired discovery block

A paired discovery block consists of:

1. A `RAW_ARTIFACT` arm, in which discovery uses the pinned source artifacts without relying on a predeclared system model.
2. A `DECLARED_MODEL` arm, in which discovery uses the declared representation M.

Both arms must use the same:

- Protected Effect E;
- enforcement boundary B;
- attacker model A;
- evidence scope S;
- pinned target version;
- analytical approach.

The intentionally varied dimension is the representation of M.

Any other differences in context, access, tools, tokens, model configuration, or execution conditions must be recorded. Such differences must not be silently treated as equivalent.

The two arms must not have access to each other's findings before both executions are closed. Results are compared only after the paired block is complete.

A paired block is the unit used for independent-run counting and stability measurement.

### 2.3. Independent run

**One independent run equals one completed paired discovery block.**

The two executions within a paired block are not counted as two independent runs.

Therefore:

- `N_min = 8` means eight independent paired discovery blocks;
- eight paired blocks comprise sixteen discovery executions;
- `K_route` and `K_class` are counted in paired blocks, not individual executions.

This prevents artificial inflation of the sample size and preserves the methodological significance of the paired comparison.

## 3. Minimum sample size and analytical diversity

### 3.1. Minimum number of independent runs

The minimum required number is:

`N_min = 8 independent paired discovery blocks`

This is a minimum threshold, not a fixed maximum. If stability criteria are not satisfied after eight blocks, additional blocks are required.

If a predefined resource or execution limit prevents completion of the required criteria, the result must not be reported as saturated.

### 3.2. Required analytical approaches

Four distinct analytical approaches are mandatory.

| ID | Approach | Primary direction of analysis |
|---|---|---|
| P1 | Effect-backward | Start from E and trace backwards to possible commitment mechanisms. |
| P2 | Component-forward | Start from components and interfaces and trace possible paths towards E. |
| P3 | Trust-boundary | Examine trust boundaries, privilege transitions, MCP exposure, and browser/session control. |
| P4 | Stateful/temporal | Examine retries, concurrency, replay, delayed actions, TOCTOU, and accumulated commitments. |

Each approach must be represented by at least two independent paired discovery blocks.

Consequently:

- P1: minimum 2 paired blocks;
- P2: minimum 2 paired blocks;
- P3: minimum 2 paired blocks;
- P4: minimum 2 paired blocks.

The eight-block minimum is therefore structured as four approaches multiplied by two replications.

The order of approaches should be recorded. Where practical, execution order should avoid systematic ordering effects.

### 3.3. Replication independence

Two paired blocks using the same analytical approach count as separate replications only if they satisfy the independence criteria in Section 4.

Repeating the same prompt with cosmetic wording changes does not establish an independent replication.

## 4. Independence and contamination controls

A paired block qualifies as an independent run only when all of the following conditions are satisfied:

1. Its analytical approach and examination objective are specified before execution.
2. Both arms use the same frozen E, B, A, S and target version.
3. The two arms differ intentionally in the representation of M.
4. Each arm is performed in a separate analytical context.
5. Neither arm has access to the other arm's findings before both are closed.
6. Neither arm is exposed to previous route registers or findings from earlier paired blocks.
7. Each arm records its findings, assumptions, gaps, rejected candidates and unexamined areas independently.
8. The paired block is compared with the canonical route register only after both arms are closed.

Each execution must have a unique execution ID. Each paired block must have a unique paired block ID.

If an execution is exposed to previous findings or otherwise fails the independence criteria, it may still be retained as supplementary evidence, but it must not count towards `N_min`, `K_route` or `K_class`.

The reason for exclusion must be recorded.

## 5. Canonical route identity

### 5.1. Purpose

The identity of a route determines whether a finding represents:

- a new canonical route;
- a variant of an existing route;
- a duplicate observation;
- or an unresolved route identity.

This distinction directly affects the `K_route` stability counter.

Route identity must therefore be determined using predefined criteria rather than subjective similarity or convenience.

### 5.2. Required identity dimensions

Each route must be assessed against three dimensions.

**A. Causal mechanism**

The mechanism through which the route can produce, enable, or contribute to the Protected Effect E.

Examples include:

- direct invocation of a commitment operation;
- an alternative execution path;
- reuse of an already-authorized operation;
- manipulation of state or context used by the enforcement decision;
- a temporal sequence that changes the result of a previously valid decision.

**B. Relevant interfaces and transitions**

The interfaces, components and significant transitions through which the route proceeds.

The assessment should identify, where applicable:

- entry interface;
- intermediate components;
- privilege or authority transitions;
- final commitment interface;
- relevant state transitions.

**C. Trust-boundary relationship**

The relationship between the route and the relevant trust boundaries, including:

- whether it crosses or avoids B;
- whether it operates within an established trust domain;
- whether it crosses a privilege boundary;
- whether it relies on a different authority or execution context.

### 5.3. New route versus variant

A finding is a **new canonical route** when it represents a materially distinct causal mechanism or an independently meaningful path through relevant interfaces or trust boundaries towards E.

A finding is a **variant of an existing route** when the underlying causal mechanism and material route remain the same, even if one or more implementation details differ.

Examples of differences that do not automatically establish a new canonical route:

- different payload values;
- different textual instructions;
- different merchant-page content;
- different concrete input values;
- a different instance of the same interface;
- cosmetic differences in execution sequence that do not change the causal path.

A new route may exist even when it shares some components or interfaces with an existing route. Shared components alone do not establish route identity.

### 5.4. Route identity decision record

Each canonical route must have a stable route ID and an identity record containing:

- route ID;
- concise route description;
- causal mechanism;
- relevant interfaces and transitions;
- trust-boundary relationship;
- relationship to E and B;
- links to the original discovery executions;
- known variants;
- identity decision and rationale.

When a new finding is compared with an existing route, the comparison must explicitly address all three identity dimensions.

### 5.5. Ambiguous identity and adjudication

If it is unclear whether a finding is a new route or a variant:

1. Record the finding separately as an identity-unresolved candidate.
2. Document the competing identity interpretations.
3. Identify the missing evidence or analysis needed to resolve the question.
4. Resolve the classification through documented review.

An unresolved identity decision must not be silently merged into an existing route.

An unresolved identity candidate blocks saturation until its identity is resolved.

Any merge, split, or reassignment of canonical route IDs must include a documented rationale and preserve traceability to the original findings.

## 6. Route discovery stability

The required threshold is:

`K_route = 3`

This means three consecutive independent paired discovery blocks must complete without discovering a new canonical route.

A paired block resets the route stability counter if either arm discovers a new canonical route.

A new route discovered independently by both arms within the same paired block resets the counter only once, because the paired block is the counting unit.

A new variant of an existing route does not reset the counter, provided its identity as a variant is supported by the criteria in Section 5.

The counter is calculated over completed independent paired blocks, not executions.

## 7. Failure-class stability

The required threshold is:

`K_class = 3`

This means three consecutive independent paired discovery blocks must complete without discovering a new failure class.

A paired block resets the failure-class stability counter if either arm identifies a new failure class.

A new example of an already established failure class does not reset the counter.

A taxonomy change that introduces a genuinely new failure class, or splits an existing class into materially distinct classes, resets the counter.

Every failure-class assignment must be recorded with its rationale and linked to the relevant route candidates.

Failure-class identity and canonical route identity are separate decisions. Multiple routes may belong to one failure class, and one route may involve more than one failure class.

## 8. Classification stability

Classification stability is a separate mandatory saturation condition.

It is not interchangeable with failure-class stability.

Before saturation can be declared:

- all discovered route candidates must have a resolved classification;
- all classification changes must be documented;
- all changes requiring validation must have completed that validation;
- no classification decision may remain open;
- no unresolved route identity may remain open.

A classification change resulting from new evidence must be recorded and reviewed. If it changes the canonical route register or failure-class taxonomy, the applicable stability counter must be recalculated according to Sections 6 and 7.

Classification stability does not require that all findings be classified as bypasses or covered routes. It requires that their classifications are resolved and supported by the available evidence.

## 9. Priority-area coverage

Priority-area coverage is a mandatory process-completeness condition.

It is not a requirement to discover a route in every priority area.

The following areas must receive explicit examination:

| Priority area | Required examination focus |
|---|---|
| MCP / A2 | Actual MCP exposure, authentication, caller privileges and possible routes through exposed tools. |
| Browser/session control / A4 | Concrete interfaces and permissions enabling browser or session manipulation, including `sameBrowser` configurations. |
| Adapter-related failure classes / A5 | Adapter faults and related candidate route sources, while respecting the approved attacker-model scope. |
| Bounded A1–A4 | Examination of the approved attacker categories within their explicitly accepted limits. |

Each priority area must receive one of the following statuses:

- `EXAMINED_WITH_FINDINGS` — examination produced one or more documented findings.
- `EXAMINED_NO_ROUTE_FOUND` — examination was performed and no route was identified within the documented examination boundaries.
- `UNRESOLVED_INSUFFICIENT_EVIDENCE` — examination was attempted, but a specific evidence or access limitation prevents a conclusive result.

The following status is not acceptable for saturation:

- `NOT_EXAMINED` — the area has not been meaningfully examined.

A priority area cannot be marked examined merely because it was mentioned in a prompt or briefly considered.

Each status must include:

- examination approach;
- relevant execution and paired block IDs;
- interfaces or mechanisms examined;
- findings, if any;
- limitations and assumptions;
- rationale for the assigned status.

An `UNRESOLVED_INSUFFICIENT_EVIDENCE` result may satisfy the process-coverage requirement if the examination was substantive and the limitation is explicitly documented.

However, this status does not resolve the underlying evidence gap and cannot be used to support a positive conformance conclusion.

## 10. Saturation decision

Saturation may be declared only when all of the following conditions are satisfied:

| Condition | Required result |
|---|---|
| Minimum sample size | At least 8 independent paired discovery blocks. |
| Analytical diversity | P1–P4 each represented by at least 2 independent paired blocks. |
| Route stability | `K_route = 3` consecutive paired blocks without a new canonical route. |
| Failure-class stability | `K_class = 3` consecutive paired blocks without a new failure class. |
| Classification stability | No open classification or route identity decisions; required validation completed. |
| Priority-area coverage | Every predefined priority area has a documented and justified examination status. |
| Independence | All counted blocks satisfy the independence and contamination controls. |
| Process integrity | No unresolved process gaps invalidate the counting or stability assessment. |

The minimum sample size and stability windows are independent requirements.

Meeting `N_min` does not automatically satisfy `K_route` or `K_class`.

If a new route or failure class is discovered in the eighth paired block, the corresponding stability window must still be completed. Additional paired blocks are required.

There is no automatic saturation solely because a predefined number of executions has been completed.

### 10.1. Unresolved evidence limitations

An explicitly documented evidence limitation does not automatically invalidate process saturation.

However, saturation must not be interpreted as evidence that the unresolved area is secure or that no bypass exists.

The final saturation report must distinguish:

- stability of observed findings;
- completeness of the prescribed examination process;
- unresolved assumptions and evidence limitations;
- areas that remain outside the declared evidence scope.

## 11. Held-out calibration

Held-out calibration and challenge cases must remain separate from discovery saturation.

They must not be counted towards:

- `N_min`;
- `K_route`;
- `K_class`;
- analytical approach replication requirements.

Calibration cases should include, where available:

- confirmed bypass examples whose ground truth is withheld from the analytical model;
- known open questions or challenge cases;
- cases designed to test whether the analytical process can distinguish real bypasses from plausible but unsupported candidates.

Calibration results must be reported separately.

A calibration success does not establish saturation. Saturation does not establish calibration quality.

## 12. Reporting requirements

The Trial 1 saturation report must contain:

1. The frozen input and target references.
2. The preregistered saturation criteria.
3. The complete execution register.
4. The paired block register.
5. The analytical approach and replication mapping.
6. The canonical route register.
7. The route identity and merge/split decision records.
8. The failure-class register.
9. The route and failure-class stability counter history.
10. The classification validation record.
11. The priority-area coverage register.
12. The excluded or non-independent execution register, with reasons.
13. The held-out calibration results, reported separately.
14. The final saturation decision and any unresolved limitations.

The report must preserve traceability from every canonical route and failure-class decision to its originating executions.

## 13. Relationship to ARD verdicts

Saturation is a discovery-process criterion.

It is not an ARD conformance verdict and does not establish the absence of bypasses.

The following distinctions remain mandatory:

- A saturated discovery process may identify one or more validated bypasses.
- A saturated discovery process may still have unresolved evidence limitations.
- A saturated discovery process does not automatically justify `CONFORMS`.
- A failure to achieve saturation does not prove that a bypass exists.
- A credible, independently validated bypass may support `DOES_NOT_CONFORM` within the declared assessment scope, regardless of whether saturation has been achieved, subject to the ARD-001 evidence requirements.

The final ARD verdict must be determined under ARD-001 v0.3 and the approved Trial 1 scope, not from the saturation counters alone.

## 14. Change control

The following parameters are preregistered candidates for Trial 1:

- `N_min = 8`;
- `K_route = 3`;
- `K_class = 3`;
- four mandatory analytical approaches P1–P4;
- minimum two paired blocks per approach;
- one independent run equals one paired discovery block.

Changes after preregistration must be documented with:

- the original criterion;
- the proposed change;
- the reason;
- the expected effect on comparability and validity;
- the authority approving the change;
- whether previously collected results remain eligible.

Changes must not be made retrospectively merely to obtain saturation.

Any material change to the counting rules or thresholds must be treated as a preregistration amendment, with its impact on the trial explicitly recorded.

---

**End of proposed document.**
