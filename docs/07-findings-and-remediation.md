# Findings, root causes and corrective actions

The five findings below are scenario examples. Severity reflects service risk and evidence context, not a universal SOC 2 rating rule. Multiple deviations can share a root cause; evaluate extent across the full population.

## F-01 · IAM-04 · High

**Condition:** One termination retained effective access for 3 hours against the one-hour lab SLA.

**Root-cause hypothesis:** The workflow disabled the IdP but omitted existing role sessions from the access-path join.

**Impact:** A departed worker could still access AWS resources during the gap.

**Owner / target:** Identity operations / 2026-10-15 (scenario).

**Corrective action:** Add role-session handling, enforce short privileged sessions and validate every account assignment/native credential path.

**Independent retest:** Use a synthetic leaver with an active session. Validate denial on each path and final removal within 60 minutes.

**Status:** Open in baseline; proposed fix and retest plan only. Original period deviation remains in the evidence.

## F-02 · DAT-01 · High

**Condition:** customer-export has a NON_COMPLIANT public-read evaluation.

**Root-cause hypothesis:** A migration copied a broad policy and had no post-migration access test.

**Impact:** Customer export data may be externally readable; configuration evidence alone does not establish actual disclosure.

**Owner / target:** Storage owner / 2026-10-08 (scenario).

**Corrective action:** Remove the broad grant, enable required blocks, inspect access history and test read/write paths.

**Independent retest:** Obtain a fresh Config evaluation and an independent negative external-access test with the correct request context.

**Status:** Open. Accepted risk, if granted, would remain a failing result.

## F-03 · CHG-01 · High

**Condition:** deploy-03 used an approval for an earlier commit; deploy-02 was self-approved.

**Root-cause hypothesis:** The release join used PR number instead of immutable deployed SHA, and did not compare actor identities.

**Impact:** Unreviewed changes can reach the production service.

**Owner / target:** Release owner / 2026-10-12 (scenario).

**Corrective action:** Bind approvals to exact SHA, require independent authorized review and close administrator bypass paths.

**Independent retest:** Seed a post-approval commit and a self-approval; both must fail while an authorized exact-SHA approval passes.

**Status:** Open. A later successful deployment cannot erase the prior exception.

## F-04 · RES-02 · High

**Condition:** exercise-02 took 5 hours; exercise-03 recovered data 2 hours behind disruption time.

**Root-cause hypothesis:** The recovery procedure omitted startup dependencies and used an insufficient backup schedule.

**Impact:** The service can miss its four-hour recovery or one-hour data-loss objective.

**Owner / target:** Recovery owner / 2026-10-22 (scenario).

**Corrective action:** Fix the dependency order and backup cadence, then repeat an application-validated exercise.

**Independent retest:** Measure from disruption start to validated service recovery; validate recovered-data timestamp and cleanup.

**Status:** Open pending a complete exercise and independent review.

## F-05 · EVD-02 · Medium

**Condition:** archive bucket evidence is stale; one expected bucket has no Config evaluation.

**Root-cause hypothesis:** The team watched job exit status without reconciling the expected bucket population or evaluation age.

**Impact:** Two scoped items have UNKNOWN assurance even if the job succeeds.

**Owner / target:** Monitoring owner / 2026-10-10 (scenario).

**Corrective action:** Add scope reconciliation and observation-age checks with independently scheduled alerts.

**Independent retest:** Drop an expected record and advance observation age past 24 hours; verify UNKNOWN and escalation.

**Status:** Open; missing coverage is not treated as compliant.

## Worked communication: executive briefing

**Illustrative 2026-10-03 review.** The 36-control catalog is documented, while four narrow assertion types have been evaluated over an end-of-period snapshot. Of 21 expected items, 20 are applicable: 5 pass, 8 fail and 7 lack sufficient reliable evidence. One approved public-document delivery exclusion is separate. Five findings remain open. These figures do not determine examination readiness or an audit opinion.

The main exposures are retained leaver access, potential bucket exposure, unreviewed releases and missed recovery objectives. Assign owners to correct the workflows and obtain independent retests; storage exposure warrants prompt investigation. Restore evidence coverage and the missing-bucket population before relying on dashboard summaries. Management should decide audit timing using the complete control/period evidence, not the last-day snapshot.

## Worked communication: engineering handoff for F-03

Expected: every production deployment has authorized independent approval for the exact deployed SHA before deployment, and successful required checks. Actual: deploy-02 shares deployer/approver identity; deploy-03 references an older approved SHA. Reproduce using the offline fixture and inspect the raw release join in the real source workflow. Replace PR-only joins, verify review authorization and prevent post-approval code changes from reusing stale approval. Retest normal, self-approved, changed-SHA and emergency paths. Preserve original events and inspect other affected deployments.

## Closure procedure

1. Confirm actual root cause with evidence, rather than treating the scenario hypothesis as a fact.
2. Record proposed action, owner, target, dependencies and compensating measures.
3. Implement under change control and assess whether similar resources/events are affected.
4. Obtain new source evidence and an independent retest against the original objective.
5. Record success/failure, reviewer approval and residual risk. Close only on supported correction.
6. Retain the original failure and evaluate its impact on period effectiveness; later fixes do not rewrite history.

For distributed teams, use UTC event timestamps and an explicit owner/backup. Leave handoff notes containing condition, evidence link, current blocker and next decision. A completed ticket is a workflow state; the retest establishes whether the control now works.
