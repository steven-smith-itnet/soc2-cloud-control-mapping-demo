# Evidence quality, population testing and custody

## The evidence contract

Every result needs control/test version, scope hash, resource identity, state, reason, observation time, collection time and source pointer. Run metadata adds logic/input hashes, expected/observed counts and evaluation time. Keep source evidence and its report filters, not only a rendered green status. Retain original exceptions and later retests as separate records.

Observation time describes the source event or state being tested; collection time is when the export was obtained; evaluation time is when test logic ran. A newly collected old Config result is still old evidence. Config's ordering timestamp describes the event or snapshot that triggered evaluation, its rule-invoked time describes the rule evaluation, and its result-recorded time describes persistence of the result. The adapter retains all three and uses ordering time conservatively for freshness. Document which timestamp each assertion uses and why.

## Validate information produced by the entity

Validate scope filters, date/time bounds, pagination, joins, duplicates, row counts and report logic. Reconcile HR terminations to HR source totals; releases to the production deployment log; assets to Organizations plus service-native inventories; restore schedules to completed exercise evidence. Source exports that omit failures are not a complete population.

Validate account and region identity. A Config aggregator helps query recorded resources but does not discover unsupported/unrecorded assets by itself. Some global resources have recording-location considerations. Reconcile disabled regions, newly enrolled accounts and denied read scopes explicitly. Empty responses, timeouts and unexpected native states must be visible.

## Period coverage and sampling

The checked-in snapshot is **one observation at 2026-09-30**. It cannot prove three-month operating effectiveness. Build a control calendar and expected-run ledger. For daily controls, reconcile expected days/runs with collected records; for event-based controls, reconcile every eligible event; for quarterly controls, inspect the review and follow-through. Retain effective versions of policies, logic and parameters throughout the period.

For a worked manual access review, imagine 12 privileged users at quarter-end: reconcile all 12 to assignments and HR, check all reviewer decisions and validate the revoked grants. For an illustrative release walkthrough, select early-, middle- and late-period deployments plus an emergency deployment from a reconciled release population. **These are teaching selections, not an auditor-approved sample size.** The CPA determines sample strategy based on risk, frequency, control reliance, population and judgment. Automated full-population output still needs validation of source completeness and logic/change controls.

## Evidence storage design

A restricted log/evidence account receives raw exports and manifests; a separate reviewer role reads them. Scope prefix/bucket/key policies, encryption rights and retention. Use S3 versioning and, where appropriate, carefully designed Object Lock retention. Governance and compliance modes have different override/deletion implications. Resolve legal hold, privacy deletion and retention conflicts before selecting settings. Prevent the operator from silently replacing accepted evidence.

CloudTrail integrity validation needs digest delivery **and actual validation**. Enabling the setting does not prove the chain was checked. Preserve validation output and investigate missing logs/digests. Log integrity does not demonstrate events that were never selected for logging.

Public examples contain fictional identifiers. Raw provider reports, credentials, personal information, customer content and live access details stay restricted. Review redaction without severing critical correlations. Keep source-to-redacted transformations reproducible and access-controlled.

## PBC index

[PBC requests](../data/pbc-requests.csv) connect request IDs to control IDs, period, source and review expectations. An auditor request tracker should also hold received date, custodian, restriction, version, reviewer, question status and links to the exact submitted artifacts. Never replace an old submitted artifact without retaining history and notifying the relevant reviewer.

## Readiness versus test conclusion

Show catalog controls, executable assertions, items observed, missing evidence, failed tests, approved exclusions and aging findings separately. A 25% narrow-assertion pass rate does not mean the organization is 25% ready, and a future 100% would not imply a clean opinion. Management assesses readiness using design, period coverage, evidence quality and unresolved risk; the CPA independently evaluates the engagement.
