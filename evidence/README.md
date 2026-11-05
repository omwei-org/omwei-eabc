# Evidence

## Purpose

This directory contains evidence records from real validation and interoperability runs.

Evidence records are **non-normative**. They do not redefine EABC requirements, create new EABC semantics, or prescribe implementation mechanisms.

The distinction between this directory and `examples/` is intentional:

- `examples/` contains illustrative execution scenarios.
- `evidence/` contains records of observed validation events and the material required for independent reproduction.

## Evidence Record Requirements

A validation evidence record SHOULD provide:

- provenance and time anchor;
- the exact raw evidence produced by the participating implementations;
- an independent verification procedure;
- observed implementation mappings;
- integrity verification results;
- limitations and remaining validation gaps.

The objective is that a reviewer who did not participate in the run can reproduce the verification from the record itself.

## Current Records

- [Validation Run 001](./validation-run-001.md) — validation run; date: 2026-09-18; status: Real validation record.
- [Validation Run 002 — Prepare / Authority Change / Commit](./validation-run-002-plan.md) — plan; date: not stated; status: Planned validation experiment (not executed).
- [HALOS Prepare / Commit Control Pair — Runs 002 and 003](./halos-run-002-003-control-pair.md) — validation run; date: not stated; status: Implementation evidence.
- [AgenTrust cMCP PR #740](./observation-agentrust-cmcp-pr-740.md) — observation; date: 2026-10-13 (maintainer review); status: Merged documentation change; source and review discussion inspected through GitHub.
- [ComOS Node Execution Gate 1.0.59](./observation-comos-execution-gate-1.0.59.md) — observation; date: 2026-10-15 (reported test date); status: Reported by the ComOS maintainer; underlying run JSON and script have not yet been independently inspected in this repository.
- [GR00T SO100/SO101 Pre-Actuation Path](./observation-gr00t-so100-pre-actuation.md) — observation; date: 2026-10-15; status: Adapter-side gap reproduced; downstream driver path source-traced; transport-level reproduction remains open.
- [GR00T SO100 isolated pinned-driver reproduction plan](./gr00t-so100-recording-transport-test-plan.md) — plan; date: not stated; status: Plan; experiment has since been run (see status note in the record).
- [Pinned LeRobot driver test script](./scripts/test_pinned_lerobot_driver.py) — script; date: not stated; status: not stated in the script.

## Evidence-state model

An evidence state records the evidentiary basis of a finding. It is not a conformance verdict and MUST NOT be interpreted as one.

- **DECLARED** — the finding is based on an architectural description, source inspection, implementation declaration, or other documented claim that has not been established through an executed and independently verified observation.
- **REPORTED** — an interested party reports an executed observation, but the artifacts required for independent verification are not available to the reviewer.
- **DEMONSTRATED** — an executed observation is supported by preserved artifacts and has been independently reproduced or otherwise independently verified. The verification method and scope MUST be recorded.

A DEMONSTRATED observation may establish successful boundary mediation, a bypass, or another relevant result. The evidence state describes the strength and provenance of the observation, not whether its result supports or contradicts a conformance claim.

Promotion from REPORTED to DEMONSTRATED requires access to the underlying evidence and independent reproduction or equivalent independent verification. Merely preserving an artifact, linking a CI run, or repeating an interested party's conclusion does not by itself establish independent verification.

Evidence state alone MUST NOT determine an EBP verdict. EBP verdicts remain governed by the applicable EBP requirements and assurance constraints.

For a positive `NON_BYPASSABILITY` conclusion, the evidence MUST establish both:

1. completeness of the declared deployment scope and the set of paths capable of producing the Protected Effect; and
2. mediation of every identified in-scope path by the assessed boundary.

A demonstrated bypass capable of producing the Protected Effect within the assessed scope may establish failure of the corresponding `NON_BYPASSABILITY` claim. A bypass outside the declared scope does not, by itself, settle that claim; its relevance to the deployment-scope declaration must be assessed.

## Evidence record metadata

Evidence records MUST identify:

- `record_type`: `run` | `observation` | `plan` | `script`
- `evidence_state`: `declared` | `reported` | `demonstrated`
- `reproduction_state`: `reproducible-from-record` | `artifacts-missing` | `source-only`
- `realization`: an immutable, versioned reference to the assessed realization description, including its content digest, or the explicit value `not-established`.

The realization description, when available, MUST identify the EBP §1.4 tuple:

`R = (SLC, substrate, configuration, deployment assumptions)`

It MUST identify the relevant versions or immutable identities of the tuple elements and indicate which elements the assurance claim depends on. A material change to an element relevant to the assurance claim triggers reassessment under EBP §1.4.

`not-established` means that no immutable realization description has been linked to the record. It MUST NOT be interpreted as a conformance result or as evidence that the realization is inapplicable.

The evidence state and reproduction state are independent dimensions. In particular, `reported` does not mean that artifacts are absent, and `reproducible-from-record` does not by itself promote a finding to `demonstrated`.

## Record classification snapshot

| Record | `record_type` | `evidence_state` | `reproduction_state` | Scope note |
|---|---|---|---|---|
| HALOS Runs 002/003 | `run` | `reported` | `reproducible-from-record` | Preserved control-pair artifacts report mediation on tested GIE path; independent semantic verification and path-set completeness not established |
| ComOS Node 1.0.59 | `observation` | `reported` | `artifacts-missing` | Maintainer-reported observations; run JSON and script unavailable here |
| AgenTrust cMCP PR #740 | `observation` | `declared` | `source-only` | Source/documentation review and synthetic probes; no real order-effect test |
| GR00T SO100/SO101 | `observation` | `reported` | `reproducible-from-record` | Harness and CI evidence recorded; independent verification not claimed |
| Validation Run 001 | `run` | `reported` | `source-only` | Source journal entries supplied; hash recomputation documented, original live run not independently rerun |
| Validation Run 002 | `plan` | `declared` | `source-only` | Planned experiment; not executed |
| GR00T recording-transport test plan | `plan` | `declared` | `source-only` | Plan only; execution results are recorded in the GR00T observation |
| Pinned LeRobot driver test script | `script` | `declared` | `source-only` | Test harness source; the run outcomes are recorded in the GR00T observation |

The metadata is a conservative snapshot of the records at this revision. It does not replace each record's detailed scope, provenance, or limitations.

## Current evidence status

At baseline commit `2fdfe46d76222e17724636fcf071a632d3f4f45b`, no evidence record in this directory supports a `VALID` outcome under EBP §5.2 for `NON_BYPASSABILITY`.

The current evidence collection is stronger at identifying potential bypass paths than at establishing complete mediation. This is an evidence limitation, not a conclusion that the assessed enforcement mechanisms necessarily fail.

A positive `NON_BYPASSABILITY` conclusion requires path-set completeness and evidence of mediation across that complete set. The absence of a demonstrated bypass is not, by itself, evidence of complete mediation.
