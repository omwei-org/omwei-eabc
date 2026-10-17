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

## Classification legend

**TODO:** Define the one-letter classification values used by observation records; no legend is defined here.

- `D` — [GR00T SO100/SO101 Pre-Actuation Path](./observation-gr00t-so100-pre-actuation.md)
