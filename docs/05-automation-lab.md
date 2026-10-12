# Automation lab: four narrow assertions with traceable evidence

The offline lab evaluates normalized exports. It does not claim to query HR, IdP, GitHub or AWS Backup. The optional live adapter reads existing AWS Config observations for customer-listed S3 buckets. It creates no infrastructure and performs no remedial action.

## 1. Establish the approved population

Inspect [demo-scope.json](../data/demo-scope.json). It lists 21 expected control/resource pairs, applicability, approved exclusions and parameters. Inspect [demo-snapshot.json](../data/demo-snapshot.json), which contains 20 observed records. A missing expected bucket is deliberately seeded. Populations are independent of successful results: starting from an API response alone hides records the collector missed.

All lab observations belong to the end of the illustrative July–September period. Freeze evaluation time at `2026-09-30T15:00:00Z` for reproducibility. Current-time evaluation will eventually make the fixture stale, as intended. `complete: true` means source export completion was declared, not that missing expected identities become compliant.

## 2. Execute and inspect

```bash
python3 -m unittest discover -s tests -v
python3 scripts/evaluate.py --as-of 2026-09-30T15:00:00Z --out evidence/local-run
python3 scripts/verify_evidence.py evidence/local-run
```

Results: 5 PASS, 8 FAIL, 7 UNKNOWN, 1 approved exclusion. Denominator: 20 applicable items; 5 / 20 = 25%. Unknowns stay in the denominator. There are **four executable assertion types**, not 36 fully automated controls. Use a new output directory each time. `--strict` returns exit 2 for failures/unknowns after writing artifacts; this is useful in a gate and deliberately fails the baseline fixture.

| Control | Executable assertion | Still requires independent work |
|---|---|---|
| DAT-01 | Current, conclusive Config public-read evaluation for each expected bucket | Full bucket/access-point policy review, public write, tenant access, population discovery |
| IAM-04 | Verified all-path removal within one hour of termination | Source extraction/join validation, active session handling, actual effective-access testing |
| CHG-01 | Exact deployed SHA, authorized independent approval before deployment, checks passed | Deployment-export completeness, branch bypasses, dismissed reviews, emergency process |
| RES-02 | Validated recovery within four hours, recovered data within one-hour lag | Real restore, timing source validation, dependency coverage, cleanup and sign-off |

Timestamps require a timezone offset. Boolean strings such as `"true"` are not accepted as proof. Duplicate identities or unexpected items invalidate extraction reconciliation. Scope hash changes invalidate the associated snapshot. Future/stale observations are UNKNOWN. Missing evidence is UNKNOWN; a demonstrated failure can survive a different missing condition on the same valid record. A missing global extract contract makes the run unreliable.

## 3. Build and validate a source adapter

For HR/IdP, use stable employee IDs and enumerate cloud assignments, native users, keys and active role sessions. For releases, use immutable deployment events and exact commit IDs, not just PR numbers. For restore exercises, capture disruption start, validated service recovery and recovered-data timestamp. Keep raw extracts and join diagnostics in restricted custody. Before production reliance, compare automation with a manual review and investigate every disagreement.

Known-fault tests exercise self-approval, old-SHA approval, late approval, late leavers, orphan access, bad timestamps, string booleans, missed resources, stale observations, unknown native states, independent RTO/RPO failures, denied APIs, repeated pagination tokens and tampered manifests. Tests prove those cases, not the entire service.

## 4. Optional live AWS Config collection

Use an existing authorized sandbox/account. Install only optional collector dependencies in a virtual environment:

```bash
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements-live.txt
cp data/aws-scope.example.json data/aws-scope.local.json
```

Edit `aws-scope.local.json`: replace account ID, approved owner, region, exact Config rule name and expected bucket list. Validate scope independently; this adapter cannot discover your organization. The reviewed rule source is `S3_BUCKET_PUBLIC_READ_PROHIBITED`, configured and active for the intended S3 resources. AWS Config recording and evaluations must already exist. Review the proposed [read-only policy](../data/collector-policy.example.json) against current AWS authorization semantics and your environment. Wildcard resource scope here requires a role restricted to the approved account with no mutation permissions; do not attach broad administrator access.

Authenticate with your existing named profile, then collect:

```bash
python3 scripts/collect_aws.py --profile audit-read --scope data/aws-scope.local.json --out evidence/live-collection-001
python3 scripts/evaluate.py --scope data/aws-scope.local.json --input evidence/live-collection-001/snapshot.json --out evidence/live-evaluation-001
python3 scripts/verify_evidence.py evidence/live-evaluation-001
```

The adapter verifies the caller account, Config rule source/state and recorder health. It follows all continuation tokens, never filters away inconclusive native states and retains raw responses. For conservative freshness it uses the native ordering timestamp, which describes the source event or configuration snapshot that triggered evaluation; it also retains rule-invoked and recorded times. A denied read, missing rule result or unhealthy recorder is explicit collection-error evidence. Account mismatch stops collection; evaluation also verifies account and region on the snapshot and each record.

The evaluation bundle includes normalized input, scope, logic, JSON/CSV results and hashes. The separate collection bundle contains raw responses, normalized snapshot, scope, collector source, SDK versions and its own manifest. Verify both directories and retain both in restricted custody; the evaluation bundle does **not** automatically copy `raw.json`. Git ignores `evidence/live*/` and local scope files; inspect your outgoing files before publishing. The website embeds only checked-in synthetic evidence.

## 5. Seed a failure and prove correction

Copy the demo input and keep the original baseline. Change a correct release to a different approved SHA, evaluate into a new output directory and verify the specific FAIL. Correct the SHA and evaluate again. This proves a narrow logic transition. To close a real finding, an independent reviewer needs new source evidence and a test of the actual deployed control. Neither editing a fixture nor a later PASS erases the original period deviation.

## 6. Validate custody

Inspect `manifest.json`, then change a copy of `results.json` and rerun the verifier. Verification must fail. A digest is useful only relative to a trusted manifest. Store authoritative manifests under restricted access or signed/protected custody; local hash files alone are not source authentication or immutable storage.
