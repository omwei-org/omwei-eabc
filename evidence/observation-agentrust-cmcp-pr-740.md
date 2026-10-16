# External Observation — AgenTrust cMCP PR #740: Execution-Scope Path Sets

**Evidence status:** Merged documentation change; source and review discussion inspected through GitHub  
**Repository:** [agentrust-io/cMCP](https://github.com/agentrust-io/cMCP)  
**Pull request:** [#740 — docs(confinement): add execution-scope path-set model with order_create example](https://github.com/agentrust-io/cMCP/pull/740)  
**Related issue:** [#736 — execution scope for protected effects](https://github.com/agentrust-io/cMCP/issues/736)  
**Maintainer review:** Approved by Imran Siddique on 2026-10-13  
**Evidence classification:** Source/documentation review and synthetic confinement probes; not an effect-specific execution test or EABC conformance assessment

## Summary

PR #740 introduced an explicit execution-scope/path-set model into cMCP confinement documentation, using `order_create` as an illustrative protected effect. Review feedback led to narrower evidence claims: the existing fixtures use synthetic tools and canary probes; they do not call a real order API or observe an orders database. The merged documentation now marks P1–P3 as **NOT ESTABLISHED** for actual `order_create` paths, P4 (external service → orders database) as **DECLARED / NOT ESTABLISHED**, and both path-set completeness and complete mediation for `order_create` as **NOT ESTABLISHED**.

**Main result:** the PR improves the precision of cMCP's confinement evidence and makes the boundary between observed probes and unproven effect-level coverage explicit. It does not demonstrate complete mediation for `order_create`.

## What was reviewed and changed

- Distinguished authorization, correlation, observation, and complete mediation as separate claims.
- Distinguished agent-side paths from deployment-side paths, including a possible external writer to an orders database.
- Made the `order_create` table explicitly illustrative rather than an inventory established for a real order service.
- Named the synthetic probes actually exercised (permitted/denied tool calls, IPv4/IPv6/UDP-DNS network probes, filesystem write probe, and child-process network probe).
- Separated logging/sink checks from effect-producing paths.
- Clarified that mutation tests show the tested controls matter for the exercised probes; they do not prove path-set completeness.
- Linked the `NON_BYPASSABILITY(B,E)` concept to the EABC/cMCP profile discussion.

The final maintainer review states that the corrected wording was approved and landed with no executable test changes in that final correction. Earlier review notes reported 25/25 synchronous tests in `test_adapter.py`; async tests were affected by missing `pytest-asyncio`, and the Docker confinement suite requires a suitable Linux/Docker environment and `CMCP_CONFINEMENT_IMAGE`. The final correction was a documentation/test-docstring change, not a new runtime execution campaign.

## EABC interpretation

The PR aligns the documentation with the EABC distinction between declaring an execution scope and proving `NON_BYPASSABILITY(B,E)`:

- Declaring P1–P4 scopes the claim but does not prove the path set is complete.
- Synthetic confinement observations support only the specific probes that ran.
- A deployment-side path to the orders database requires separate deployment evidence.
- Because the real `order_create` paths and P4 are not established, the overall complete-mediation claim for that effect remains **NOT ESTABLISHED**.

This is a useful methodological result: cMCP's documentation now states the limits of its existing evidence rather than presenting generic confinement probes as proof that all paths to a business effect are mediated.

## What this result does not establish

This PR does **not** establish that cMCP is insecure, that its confinement controls fail on the probes they actually test, or that every RAIG system has the same limitations. It does not test a real order service/database, prove complete path-set coverage, or validate an EGA/EABC implementation. It is primarily a documentation and evidence-scoping result, supported by source inspection and existing synthetic fixtures.

## Suggested citation

> AgenTrust cMCP PR #740, “docs(confinement): add execution-scope path-set model with order_create example,” merged after maintainer review on 13 October 2026. The change distinguishes synthetic confinement probes from effect-specific evidence and explicitly leaves the real `order_create` path set and complete-mediation claim **NOT ESTABLISHED**. It is not a real order-service test or an EABC conformance result.

**Classification:** External source/review observation; merged documentation correction; synthetic probes only for the underlying confinement example; no effect-specific complete-mediation verdict.
