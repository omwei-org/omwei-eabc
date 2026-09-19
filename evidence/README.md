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

- [Validation Run 001](./validation-run-001.md) — first real cross-organization interoperability validation record.
