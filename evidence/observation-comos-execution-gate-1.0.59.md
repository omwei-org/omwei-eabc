# External Observation — ComOS Node Execution Gate 1.0.59

**Evidence status:** Reported by the ComOS maintainer; underlying run JSON and script have not yet been independently inspected in this repository  
**Reported test date:** 2026-10-15  
**Reported tester:** Ron Reynolds  
**Reported package:** ComOS Node 1.0.59  
**Reported package SHA-256:** `5cb0c0e6238d5e4d0cf1d06002b10cb2257e75c4bb96ce2b64a27802a74b34b2`  
**Reported test count:** 21 attempts  
**Evidence classification:** External-system observation; non-normative; not an EABC conformance assessment

> **Key finding**
>
> Ron Reynolds reports that ComOS Node 1.0.59 validates brokered-act signatures and payload binding, rejects configured-gate failures before inventory reservation, and handles replayed signed acts idempotently. The same report records that the execution gate is optional, accepts an unsigned HTTP decision when the expected identifiers and digest are echoed, and does not mediate every path to relevant state changes in the tested configuration.
>
> These are maintainer-reported results. The attached run JSON and the shipped test script have not yet been independently reviewed here. This record does not claim independent reproduction or complete execution-path coverage.

## 1. Scope and provenance

This record captures the results Ron Reynolds reported in a message on 2026-10-16 about a test run performed on 2026-10-15 using ComOS Node 1.0.59 on a Raspberry Pi 5.

Ron reported that the package hash is named by the signed release manifest:

- [ComOS node release manifest](https://comos-federation.com/.well-known/comos-node-releases.json)
- Reported run artifact: `gate-matrix-20261015223235-4499.json` (provided by Ron as an attachment; not present in this repository at the time this record was written)
- Reported in-package test script: `bundle/node-gate-matrix.mjs`
- Reported invocation from the extracted node folder: `node --env-file=.env bundle/node-gate-matrix.mjs`

According to Ron, the script runs the node's act loop and sale handler against a stand-in hub with a throwaway signing key, stub gates bound to loopback, and a separate disposable database. It refuses to reuse an existing database and drops the test database at completion. Ron reported that the run did not contact the production hub or touch production tenants.

The exact package, manifest signature, script, JSON output, and raw database snapshots have **not** been independently verified as part of this evidence record. Statements about the run below are attributed to Ron's report, not presented as an independently reproduced result.

### Node's hub-key selection (clarification from Ron)

The node reads the optional `COMOS_HUB_ACT_PUBLIC_KEY` setting as a base64-encoded Ed25519 SPKI public key. When set, it selects that key instead of the release-pinned key; when absent, it uses the release pin. Ron reports that the test script generates a throwaway Ed25519 key pair and sets the variable in its own process before the node code loads. It does not write `.env`; its only output file is the JSON report. This is an operator-supported configuration path, not a test-only code path. Using it requires the same access to node configuration as changing the gate URL or replacing the binary. At startup, the node logs the active key ID (`kid`) and whether it came from the release pin or the setting. A malformed key or a key that is not Ed25519 stops the ACT loop rather than allowing unverified processing.

This clarification does not change the evidence status above: the package, script, report, and runtime behaviour remain maintainer-reported until independently inspected. Nor does it remove the operator from the trust boundary. The node README states that the local database has no password and that the operator is the trust boundary; this should remain visible in the record rather than being omitted for a tidier summary.

## 2. Reported test results

Ron reported 21 attempts across the following cases.

| Case | Reported observation | Evidence boundary |
|---|---|---|
| Brokered sale; gate returns `COMMIT` with exact echo | Pending order created; available stock 10→9 and reserved stock 0→1 | One configured brokered-sale path |
| Gate returns `BLOCK` | Sale refused; no order; stock unchanged | Reported fail-closed behaviour for this handler |
| Gate returns `COMMIT` with a different `action_digest` | Refused as `gate_action_digest_mismatch`; stock unchanged | Exact echo mismatch rejected |
| Different local process answers gate URL with correct echo but no signature | Accepted; order created and one unit reserved | Gate decision is not cryptographically authenticated by the described protocol |
| `COMOS_EXECUTION_GATE_URL` unset | Sale executes; receipt decision is `NONE`, reason `no_gate_configured` | Gate is optional in this configuration |
| Timeout, no listener, HTTP 503, malformed JSON | Each attempt refused with a reason; no reservation | Reported fail-closed behaviour for these configured-gate errors |
| Same signed act delivered twice | Second delivery returns existing order; no second reservation | Reported idempotency for the tested replay |
| Payload altered without updating digest / digest recomputed without valid signature / unsigned act / different hub key / expired act | Reported refusals; stock unchanged | Reported act-binding, signature, and expiry checks |
| Hub-signed stranger request naming `order_create` or `inventory_set` | Refused as `ask_not_public` | Tested network request types only |
| Hub-signed `payment_confirm` | Can move an existing pending order to paid without the execution gate | This is a node-side state update recording a settlement already performed by the hub; the node does not move Coms. The ACT requires the hub's settlement reference and transitions only a pending order. The hub owns the financial-settlement guarantee. |
| Operator-local `inventory_set` tool | Changes stock without the gate | Local operator path is outside the brokered-sale gate |
| Operator-local order paths | Local Coms order refused in the reported store; local card order refused because no money account was configured | Store/configuration-specific observations; not a general absence claim |
| Direct database write using the node's database access | Reportedly succeeds in inserting a paid order and decrementing stock by two units | Demonstrates a path available to a process holding those database credentials in the tested setup |

The table summarizes the maintainer's report. It is not a substitute for the raw JSON output, logs, or before/after database records.

## 3. Interpretation

### 3.1 What the report supports

Subject to independent verification of the artifacts, the reported run supports these scoped observations about ComOS Node 1.0.59:

- The tested node rejects multiple invalid or expired brokered acts before dispatch.
- With the execution gate configured, the tested retail-sale handler refuses a sale on a gate block, an action-digest echo mismatch, and several gate transport/protocol failures.
- The tested handler uses `command_id` to make a repeated delivery return the existing order rather than reserve stock a second time.
- The gate decision described in the report is an ordinary HTTP response whose trust depends on control of the configured endpoint; a correctly echoing local process does not need to provide a signature.
- The gate is optional: with its URL unset, the tested brokered sale can execute without an external authorization decision.
- The protected effect of this node-side gate is **sale reservation and order creation**: creating the order and reserving stock. It does not protect the movement of Coms. The hub settles only after the node receipt matches the bound sale, then queues `payment_confirm` to record that already-completed settlement on the node.
- Other operator-local or direct-database paths can change relevant state outside the tested brokered-sale gate.

### 3.2 Mapping to EABC concepts

| EABC concept | Mapping supported by the reported test | Limitation |
|---|---|---|
| `NON_BYPASSABILITY(B,E)` | The report identifies paths to relevant state changes outside the brokered-sale gate, and execution with the gate unset | This is evidence against global mediation in the tested configuration, not a complete enumeration of every path |
| Integrity of authorization/request data | Reported signature, digest, target-node, and expiry checks on brokered acts | Does not establish that the resulting action is authorized under an EGA/EABC authority contract |
| Binding authorization to the exact action | The handler reportedly computes an `action_digest` and checks the gate response's echoed digest | An echoed digest is not proof of authorization; the response itself is not authenticated in the described protocol |
| Fail-closed behaviour | Reported for several failures while a gate URL is configured | Does not apply when the gate is unset; it is scoped to the tested handler and cases |
| Complete mediation | Not established; reported bypass paths exist | Complete path-set coverage has not been performed |
| EGA/EABC integration | No demonstrated use of the complete OMWEI EGA/EABC implementation is identified in the report | This run must not be described as an EGA/EABC validation or conformance test |

The EABC property `NON_BYPASSABILITY(B,E)` concerns the relevant commit boundary and its defined scope. Whether an operator-controlled database path is in scope depends on the declared adversary model and protected effect. The report nevertheless shows that the brokered-sale gate alone is not a universal control over every way the tested machine can change order or inventory state.

A direct database write by the machine operator is not, by itself, proof of a product vulnerability: Ron describes the database as intentionally passwordless on the operator's own machine. It is a relevant boundary fact if the intended guarantee is meant to hold against processes or actors with that level of local control.

## 4. Claims this record does not make

This record does **not** establish:

- independent reproduction of Ron's reported 21 attempts;
- cryptographic verification of the package hash against the signed manifest;
- authenticity or completeness of the reported JSON, script, logs, or database snapshots;
- complete enumeration of every ComOS execution path;
- that ComOS as a whole is insecure, or that all runtime-governance systems share these properties;
- that the tested gate implements EGA, EABC, an Authorized Execution Envelope, or an EABC-conformant SLC;
- that an action digest alone expresses or proves execution authority;
- that the reported local database access is an exploit against the operator's stated trust model.

## 5. Reproduction and evidence integrity

The following materials should be preserved to make this record independently reviewable:

1. The exact ComOS Node 1.0.59 package used in the run.
2. The release manifest and the means to verify its signature and the package hash.
3. The exact `bundle/node-gate-matrix.mjs` script from that package.
4. The raw `gate-matrix-20261015223235-4499.json` output.
5. Any raw logs and database snapshots emitted by the run, including before/after order and inventory records.
6. A rerun using the exact package hash, with the resulting artifacts and environment details retained.

When these artifacts are obtained, verify the package SHA-256 locally, inspect how the script constructs each case, and compare its recorded results with the raw logs and database snapshots. Until then, cite the result as **reported by Ron Reynolds**, not as independently verified by OMWEI.

## 6. Citation language

Suggested concise citation:

> Ron Reynolds reported a 21-attempt test of ComOS Node 1.0.59 on 15 October 2026 (package SHA-256 `5cb0c0e6238d5e4d0cf1d06002b10cb2257e75c4bb96ce2b64a27802a74b34b2`). The reported results cover signed-act validation, configured-gate failure handling, digest echo checks, and replay idempotency. They also document that the gate is optional, its HTTP decision is unauthenticated in the described protocol, and other local/database paths can change state outside that gate. The results characterize the tested configuration and do not establish complete path-set coverage or EGA/EABC conformance.

## 7. Classification

**Classification:** External observation; maintainer-reported test; not independently reproduced in this repository; no EABC conformance verdict.

**Use:** Comparative evidence motivating explicit execution-authority enforcement and path-set analysis. Do not use it as proof that an EGA/EABC implementation has already closed the identified gaps.
