# ARD-TRIAL-01 — Trial 1 Preregistration

**Status:** PROPOSED — NOT FROZEN; trial execution is not authorised.  
**Method baseline:** ARD-001 Draft v0.3 (trial baseline candidate), frozen by the merge commit recorded below.  
**Trial:** 1 — software commerce-agent node.  
**Document type:** Non-normative experimental preregistration.

## 1. Purpose

This document preregisters the first experimental application of ARD-001 to a software commerce-agent node. The purpose is to evaluate the repeatability and practical usefulness of the ARD discovery, classification, validation and saturation procedure.

Trial 1 evaluates the assessment method. It does **not** issue an SLC-SW conformance verdict, certify the target system, or establish universal non-bypassability.

No discovery run may begin until this preregistration is completed and explicitly frozen. A missing or unresolved item identified as a start gate below blocks execution; it must not be silently supplied by an assessor or discovery model.

## 2. Frozen methodology baseline

- Repository: `omwei-org/omwei-eabc`
- Method document: [`docs/assessment/ARD-001.md`](https://github.com/omwei-org/omwei-eabc/blob/183406713d7db6172302bdec9c2823832e25205b/docs/assessment/ARD-001.md)
- Baseline commit: `183406713d7db6172302bdec9c2823832e25205b`
- Commit URL: https://github.com/omwei-org/omwei-eabc/commit/183406713d7db6172302bdec9c2823832e25205b
- Baseline identity: merge commit for PR #26, “Add ARD-001 v0.3 trial baseline candidate”.
- Baseline status: Draft v0.3, trial baseline candidate, non-normative. It is not ARD-001 v1.0.

The trial must use this exact methodology baseline. Any methodology change after preregistration requires a separately versioned amendment, an explanation of its effect on comparability, and an explicit decision whether the trial must restart.

## 3. Trial target and boundary

**Target category:** Software commerce-agent node.  
**Target instance:** NOT YET IDENTIFIED.  
**System owner / operator:** NOT YET RECORDED.  
**Target version / commit / deployment identifier:** NOT YET RECORDED.

The phrase “commerce-agent node” identifies the agreed trial category only. It does not identify a concrete implementation or establish its architecture, deployment, trust boundaries, or available evidence.

### 3.1 Required instance specification (ARD parameters)

The following fields must be completed from attributable source material before any discovery run:

| Parameter | Required content | Current state |
|---|---|---|
| E — Protected Effect | Exact state transition or externally observable effect to be protected; identify the authoritative commit point. | MISSING |
| B — Enforcement boundary | Concrete location, observations, controls, enforcement decision point, and declared assumptions. | MISSING |
| A — Attacker model | Attacker capabilities, controlled principals/components, trust boundaries, exclusions and rationale. | MISSING |
| M — System model | Components, data/control/management/update/debug interfaces, privileges, delegation, integrations, and known inventory limitations. | MISSING |
| S — Evidence scope | Concrete deployment/build/configuration and what can be inspected or tested; explicit evidence limitations. | MISSING |

No assessor or model may infer or invent E, B, A, M or S. If any remains missing, the result is INSUFFICIENT_EVIDENCE and the trial must not proceed to discovery.

### 3.2 Input provenance register

Every material input claim must be tagged:

- **ESTABLISHED** — directly supported by an identified artifact or attributable observation.
- **DERIVED** — reasoned from identified established facts; derivation and dependencies are recorded.
- **UNCERTAIN** — plausible but not established.
- **MISSING** — required information not supplied or not found.

For each item record: identifier, statement, provenance class, source/artifact and version, locator (path/line/section where possible), collection date, owner, and notes. An uncertain or missing item must not be silently promoted to established fact.

## 4. Discovery design and bias controls

Two discovery inputs are prepared independently and retained as separate, versioned artifacts.

### 4.1 Raw-artifact discovery input

Collect and inventory available primary artifacts before constructing the declared architecture model. Depending on availability, this includes source code, build manifests, dependency and package metadata, configuration, deployment descriptors, API/interface definitions, permission and identity configuration, integration definitions, runtime topology, operational/recovery/update paths, and relevant logs or traces.

Record unavailable artifact categories explicitly. Do not interpret absence of an artifact as evidence that the corresponding interface or path does not exist.

The raw-artifact inventory is supplied to a discovery run whose task is to identify candidate routes and omitted/undocumented interfaces without relying on a pre-written route register.

### 4.2 Declared-model discovery input

Prepare a separate declared-model package containing E, B, A, M and S, plus the provenance register. Run the same discovery objective against this package.

### 4.3 Comparison

Compare the raw-artifact and declared-model discovery outputs. Record:
- routes found only from raw artifacts;
- routes found only from the declared model;
- interfaces, components, privileges or assumptions omitted from M;
- differences caused by unavailable or ambiguous evidence;
- any framing or input asymmetry that could bias the comparison.

The comparison is a method-quality observation, not independent validation of a route and not a conformance verdict.

## 5. Calibration and held-out challenge set

The calibration material must be assembled, versioned, timestamped and access-controlled before the first discovery run. The discovering model must not receive the held-out ground-truth material.

Maintain two separate sets:

1. **Confirmed-bypass ground truth:** cases independently confirmed to be bypasses for the relevant declared instance and scope. These are withheld from discovery and used after the runs to measure rediscovery.
2. **Known open challenge cases:** unresolved questions used to test whether the method preserves uncertainty and classifies open candidates appropriately. They are not ground truth bypasses and must never be automatically counted as bypasses.

The following previously identified open topics are challenge candidates only, unless and until independent evidence establishes otherwise:
- historical open points S1–S5;
- Policy Engine as a software root of trust;
- asynchronous POISON;
- closure of the Protected Effect boundary.

For each calibration item record its source, instance applicability, evidence status, independent validator, classification rationale, and the date on which its status was frozen. If no confirmed-bypass ground truth is available for this target, record that limitation; do not manufacture positive cases or treat open questions as confirmed bypasses.

## 6. Run protocol

After all start gates in Section 10 are satisfied and this preregistration is frozen:

1. Run blind discovery against the raw-artifact input package.
2. Run blind discovery against the declared-model input package.
3. Use the same declared E, B, A and target version for comparable runs. Record any unavoidable input differences.
4. Use multiple materially different model/framing combinations as specified in the frozen saturation criterion.
5. Preserve every run's exact prompt, model/version, parameters, input artifact hashes, timestamp, output, and operator.
6. Do not provide known routes, calibration ground truth, or held-out challenge answers to the discovering model.
7. Consolidate outputs into a canonical route register using ARD-001's route identity rule. Preserve source-run identifiers and disagreements; do not erase variants merely because their descriptions look similar.
8. Keep rejected candidates separate. Reject a candidate only where no causal or enabling relationship to E has been identified. Retain and classify all other candidates, including routes outside A.
9. Record unexamined areas and assumptions explicitly.
10. Submit route candidates to independent validation. Discovery output alone is not evidence and cannot establish an EABC invariant violation.

No exploit code or operational attack instructions are part of this trial protocol.

## 7. Independent validation

For each route selected for validation, record:
- route identifier and exact claim being tested;
- validation type: deployed-system testing, formal analysis, or independent human red-team assessment;
- concrete implementation and version covered;
- deployment assumptions and interfaces/privileges covered;
- validation scope, method summary and result;
- evidence reference and validator independence;
- limitations and unresolved assumptions.

Analytical confirmation may support a Validated bypass classification only when it covers the concrete implementation and establishes that the route exists under the declared deployment assumptions. If a required interface, privilege, mechanism or deployment assumption remains unverified, the route stays open as Argued bypass or Potential bypass, as appropriate.

A route that cannot be validated within S remains in the register and cannot be silently removed. The trial does not require every candidate to be exploitable in a test environment.

## 8. Saturation criterion — NOT YET SET

ARD-001 requires the stopping rule to be declared before the first run. Its Annex B deliberately leaves default values for N_min, K_route and K_class open pending trial evidence. This preregistration therefore does not invent or imply default thresholds.

Before freeze, the trial owner must explicitly set and justify:
- **N_min:** minimum number of independent runs;
- **K_route:** consecutive independent runs with no new route;
- **K_class:** consecutive independent runs with no new failure class;
- **Diversity requirement:** minimum number of materially different models and framings;
- **Counting rule:** how material independence and documented differences are established for this trial.

The criterion must also state how the saturation curve will be reported. Identical reruns and cosmetic prompt edits do not count as independent runs. The criterion cannot be changed after discovery starts; a necessary change requires a documented amendment and a decision on restarting the trial.

## 9. Evaluation measures

Report at minimum:

- **Calibration rediscovery:** proportion and identity of confirmed ground-truth bypasses rediscovered by the discovery process.
- **Open-challenge handling:** whether open cases remain open and are not promoted to confirmed bypasses without independent evidence.
- **New routes:** unique routes per run and across the combined register.
- **New failure classes:** new classes per run and across the trial.
- **Classification consistency:** agreement and disagreement across independent runs, with reasons.
- **Raw/model divergence:** routes and assumptions surfaced by raw-artifact discovery but absent from declared-model discovery, and vice versa.
- **Unvalidated Covered count:** target is zero; a route without independent evidence must not be classified Covered.
- **Unsupported claims:** claims presented as established without attributable evidence.
- **Input provenance quality:** missing, uncertain and derived inputs, and any provenance promotion or ambiguity.
- **Saturation:** observed route/class discovery curve against the frozen stopping rule.

Do not collapse these measures into a single score unless a scoring method is separately justified and preregistered.

## 10. Start gates

Trial execution is blocked until every gate below is satisfied and recorded:

- [ ] Concrete commerce-agent target, owner/operator, version and deployment identity recorded.
- [ ] E, B, A, M and S completed with source-backed provenance.
- [ ] Raw-artifact inventory collected, versioned, and its gaps recorded.
- [ ] Declared-model package and provenance register completed independently of raw-artifact discovery.
- [ ] Raw/model input comparison plan confirmed.
- [ ] Calibration set frozen and timestamped; confirmed bypasses separated from open challenge cases.
- [ ] Availability or absence of confirmed-bypass ground truth documented.
- [ ] N_min, K_route, K_class, diversity and counting rules explicitly set and justified.
- [ ] Run prompts, model/version selection, framing plan and run record format frozen.
- [ ] Independent validation process and validator independence defined.
- [ ] This preregistration reviewed and changed to **FROZEN — EXECUTION AUTHORISED** by the trial owner.

Until all gates are satisfied, the only permitted work is preparation, evidence collection, and review of this preregistration. No Trial 1 discovery run is authorised.

## 11. Trial outputs

The trial package will contain:
1. frozen preregistration and amendments, if any;
2. target and input specification (E, B, A, M, S);
3. input provenance register;
4. raw-artifact inventory and declared-model package;
5. calibration and held-out challenge-set manifest (with restricted ground truth retained separately);
6. exact prompts, model/version and run records;
7. raw/model comparison report;
8. route register and separate rejected-candidate register;
9. independent validation log and evidence references;
10. saturation curve and evaluation report;
11. method-level findings and proposed ARD-001 revisions.

The final report must distinguish method evaluation from any system-level security or conformance conclusion.

## 12. Explicit non-claims

Trial 1 does not:
- validate ARD-001 as a universal method;
- promote ARD-001 to v1.0 or make it normative;
- issue an SLC-SW conformance verdict;
- establish CONFORMS or DOES_NOT_CONFORM for the target merely from discovery output;
- prove the absence of bypasses;
- replace independent validation or deployment-specific conformance assessment.

A later hardware trial is a separate trial on an architecturally different system and is not part of this preregistration.

## 13. Preregistration change log

| Version | Status | Change |
|---|---|---|
| 0.1 | PROPOSED — NOT FROZEN | Initial Trial 1 preregistration. No discovery runs authorised. |
