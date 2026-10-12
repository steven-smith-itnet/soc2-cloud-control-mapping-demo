# Learner workshop with worked reasoning

## Track 1: beginner, no AWS account

1. Read the foundations and explain SOC 2, Type I/II, criterion, control, population and evidence in your own words.
2. Open System & scope. Trace one upload from customer to authorized storage and logging. Identify application authorization versus AWS access boundaries.
3. Pick IAM-04. Explain its risk, owner, population, frequency, evidence and limits without mentioning a tool first.
4. Run the offline lab. Identify one PASS, one FAIL, one UNKNOWN and the approved exclusion. Explain why the denominator is 20.
5. Read F-01 and propose a retest that checks usable access, not a closed ticket.

Acceptance: you can describe the commitment → risk → control → test → evidence → remediation chain and identify who owns the management assertion and independent opinion.

## Track 2: assurance engineering

1. Copy the fixture; make deploy-01 approved at an earlier SHA. Expected: FAIL for that deployment.
2. Restore the correct SHA but set checks_passed to the string "true". Expected: UNKNOWN.
3. Remove customer-primary from records. Expected: UNKNOWN for that expected bucket, not a reduced population count.
4. Duplicate a record. Expected: the run rejects reconciliation and all results become UNKNOWN.
5. Set an observation beyond the evaluation time. Expected: UNKNOWN.
6. Change an approved threshold without updating the scope hash. Expected: snapshot mismatch, UNKNOWN run.
7. Keep recovery within four hours but move recovered data two hours behind disruption. Expected: RPO FAIL despite acceptable RTO.
8. Run manifest verification, modify a copy of an artifact and rerun. Expected: integrity check failure.

Acceptance: each output explains the exact assertion and limitation. Preserve separate baseline/fault/retest outputs rather than editing accepted evidence.

## Track 3: optional authorized AWS sandbox

Review an explicit account/region/bucket scope and named read-only profile. Use the Config collector against an existing active public-read rule. Inspect every raw page, expected/observed identity and native observation timestamp. Simulate a denied read with a restricted test role if authorized. Expected: collection-error evidence, then UNKNOWN in evaluation. Verify a newly collected stale native evaluation stays UNKNOWN.

Acceptance: a reviewer can trace normalized results to native input and confirm that no API error or missing page is treated as compliance. Live evidence remains restricted and outside the public site.

## Worked answers

- Baseline expected population: 21 items. Observed: 20. One missing expected item remains UNKNOWN. The approved public-docs exclusion removes one item from applicability, leaving 20.
- Narrow assertion pass rate: 5 / (5 + 8 + 7) = 25%. It is neither a criterion-coverage percentage nor a SOC 2 readiness score.
- Two leavers pass at 30 and 60 minutes. A three-hour removal and verified active access after the deadline fail; a missing final-removal conclusion is UNKNOWN.
- Release failures include self-approval, wrong approved SHA and approval after deployment. Missing approval and a string boolean are UNKNOWN.
- Recovery distinguishes late service restoration, excessive data lag and missing application sign-off.
- Closure requires new source evidence and independent testing of the implemented fix. A synthetic mutation proves logic behavior, not a production correction.

Use the interactive Review & practice section for additional explain-back questions. Answer first, then reveal the reasoning.
