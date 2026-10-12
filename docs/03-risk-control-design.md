# Risk-based control design

A catalog is useful only when its controls support the actual system objectives. Start with commitments, then threats and consequences. Record inherent risk before treatment and residual risk after tested measures. Use a documented qualitative scale; do not imply mathematical accuracy from a High/Medium label.

## R-01: Former engineer retains usable role-session access

Impact: Unauthorized access to tenant data. Inherent: High. Residual: Medium pending verified session controls. Owner: Identity operations.

Treatment: Join all access paths, address active sessions, and retest effective access.

Supporting controls: IAM-01, IAM-04, OPS-02.

## R-02: Customer bucket policy enables public reads

Impact: Customer content disclosure. Inherent: High. Residual: Medium pending policy remediation. Owner: Storage owner.

Treatment: Apply blocks, review grants, reconcile inventory and verify external denial.

Supporting controls: DAT-01, DAT-02, APP-01.

## R-03: Production release uses an approval for a different SHA

Impact: Unreviewed code enters production. Inherent: High. Residual: Medium pending release-gate correction. Owner: Release owner.

Treatment: Invalidate approvals on change and require the exact deployed SHA.

Supporting controls: CHG-01, CHG-02.

## R-04: Backup restores after the service deadline or loses too much data

Impact: Contractual recovery commitment missed. Inherent: High. Residual: Medium pending successful exercise. Owner: Recovery owner.

Treatment: Measure both RTO and RPO including dependent services and application validation.

Supporting controls: RES-01, RES-02, RES-03.

## R-05: Evidence collector loses a region but dashboard remains green

Impact: Unsupported management assertions. Inherent: High. Residual: Medium pending heartbeat and reconciliation. Owner: Monitoring owner.

Treatment: Alert on missing runs, missing identities and stale observations.

Supporting controls: MON-01, EVD-01, EVD-02.

## R-06: AWS or identity provider outage prevents service operation

Impact: Service interruption and customer notification failures. Inherent: High. Residual: Medium with tested dependency plan. Owner: Service owner.

Treatment: Review relevant reports and commitments, test fallback and communication.

Supporting controls: VND-01, VND-02, RES-03.

## A control specification before code

Specify objective, owner, operator, reviewer, population source, required frequency, evidence sources, parameters, failure semantics, remediation and limits. A criterion supports more than one possible control and a control may contribute to several criteria. Record rationale and which parts remain untested. Reuse evidence across requirements only after assessing matching scope, frequency, objectives and population.

Worked chain: customer confidentiality commitment → departed worker misuse risk R-01 → IAM-04 all-path access removal → join HR events to IdP/cloud/native credential/session records → one-hour threshold → late removal finding F-01 → session handling fix → independent effective-access retest. This chain prevents a control from becoming an isolated technology checkbox.

The one-hour SLA is approved scenario configuration. A real organization must set deadlines from its risks and commitments, then maintain sufficient removal evidence. Tests never invent thresholds because a framework is present.

## Design, implementation and operation workpapers

Design: does every identity path have a removal method, source, join and failure escalation? Implementation: have those methods been configured and tested? Operation: did every relevant termination during the period lose effective access within the deadline? An on-time ticket does not prove that a role session stopped working.

For each automated test, assess the logic using seeded known failures and known valid records. Validate extracts and timestamps independently. Review code changes and operator rights. Collectors are privileged information processors: their own access, change control and custody must be assessed.

## Human approval and risk acceptance

Require an authorized acceptor independent of the operator where appropriate. Record the failure, business impact, reason, scope, compensating measure, expiry and review cadence. At expiry, retest or escalate. An approved exception stays visible in failed test results and examination-period analysis. Do not relabel a failed control as NOT_APPLICABLE simply to remove it from the score.
