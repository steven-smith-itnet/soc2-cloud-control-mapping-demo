# AWS implementation and operational runbooks

These runbooks describe proposed work in an authorized sandbox/real program. They are not executed by the repository. Record account/region, expected results, observed outcomes, operator and reviewer. Use read-only collection by default; perform negative tests and changes only where authorized. AWS services and data events can incur charges; this project provisions none.

## Identity and termination

1. Map workforce IdP identities to Identity Center assignments and permission sets. Include native IAM users, access keys, emergency identities and third-party access.
2. Validate MFA at the IdP and inspect bypasses. `aws:MultiFactorAuthPresent` is not a universal federated MFA signal; credential reports cover native IAM users rather than the entire workforce.
3. At a termination event, stop new authentication, remove assignments and address existing temporary role sessions and native keys. Existing IAM role sessions can survive the portal session.
4. Test whether each access path is actually denied and record the time effective access ends. Reconcile all terminated people against all paths, including missing joins.
5. Inspect the collector’s own access. Do not let a read-only evidence role silently acquire deployment or key-use privileges.

Effective access combines identity/resource policies, trust, boundaries, session policies and organization controls with request context. SCPs do not grant access and have important scope limits, including the management account and service-linked roles. Keep privileged work out of the management account and validate relevant exceptions.

## Logging canary: demonstrate how data reaches evidence custody

1. Enumerate accounts, regions and required management/data event selectors. Decide which sensitive S3 object operations need capture and record cost/volume tradeoffs.
2. Generate a unique non-sensitive object canary and a representative management event using an authorized test identity. Retain event ID, resource, actor and UTC trigger time.
3. Find the expected event in CloudTrail delivery, not just the console's recent event history. Verify selected fields survive normalization and redaction.
4. Trace delivery to log archive, Athena (if used), evidence collector, test output and protected storage. Record latency, missing fields and correlation IDs.
5. Test a broken route/permission in a sandbox and verify independent health alerts. A zero-row query without verified delivery is inconclusive.
6. Enable log-file digests where appropriate and actually run integrity validation. Preserve the result and investigate gaps.

Read-only diagnostic templates for an **existing scoped trail**:

```bash
aws sts get-caller-identity --profile audit-read
aws cloudtrail get-trail-status --name YOUR_TRAIL_ARN --region us-east-1 --profile audit-read
aws cloudtrail get-event-selectors --trail-name YOUR_TRAIL_ARN --region us-east-1 --profile audit-read
aws configservice describe-configuration-recorder-status --region us-east-1 --profile audit-read
```

The provided Config collector policy does not include these CloudTrail permissions; grant separately reviewed reads if needed. See [Athena query templates](../scripts/cloudtrail_queries.sql) and the documented schema/partition setup. Add partition predicates for your actual table. Querying root use or guardrail changes yields investigation leads, not automatic policy violations.

## Data storage and keys

Validate bucket and account public-access blocks, policies, ACL/Object Ownership settings and access-point paths together. The managed public-read rule is a narrow supporting assertion. Do not infer protection against public write or cross-tenant app requests from its PASS.

S3 encrypts new objects by default. If policy requires a specific KMS key, inspect object metadata/inventory as well as defaults and key policies/grants. A bucket default change does not retroactively rewrite existing objects. If you require explicit encryption request headers, assess integrations that rely on bucket defaults and log-delivery permissions.

KMS rotation strategy depends on key type and origin. Rotation does not revoke data access or solve compromised credentials. Review key administration, grants, scheduled deletion, recovery-key availability and access to encrypted backups separately.

## Release control

Join deployed artifact SHA/digest to source commit, authorized reviewer, exact approved SHA, required checks and release time. An old approval for the same PR is not enough. Test self-approval, late approval, changed commits, administrator bypass and emergency changes. Retain required status checks and environment approvals in addition to the source review. Constrain OIDC trust to approved repository/audience/environment claims and restrict the deployment role.

Policy-as-code gates should reject known-bad plans before deployment; Config-style monitoring detects post-deployment drift. Both need reviewed logic, parameter versioning and failure tests. Retain source, plan, policy results, approved artifact and runtime digest as a traceable chain.

## Vulnerability and incident handling

Reconcile running images/instances/functions to supported scanners. Prioritize by exposure and exploitability as well as severity, document deadlines and exceptions, deploy fixes and preserve rescans. A suppressed finding is not proof of remediation.

For a credential compromise exercise: capture detection and triage, classify impact, restrict affected access, preserve relevant logs, assess customer-data exposure, decide required communications with legal/management, recover with validated access and complete the after-action review. Test routing from GuardDuty/application signal to actual owner response and escalation. Do not stop at service enablement.

## Backup and recovery

Map every committed asset to recovery point cadence, retention, custody, key dependency and restoration procedure. Reconcile failures and missing assets. Multi-AZ failover and backup recovery address different risks.

Restore an isolated copy using approved procedures, bring up dependencies, verify application functions and data integrity, and measure time from disruption start to **validated service recovery**. Measure recovered-data timestamp relative to disruption start. Exercise loss of key access and an unavailable dependency, then record cleanup. AWS Backup restore testing can support job orchestration; application validation and commitment assessment remain necessary.

## Continuous operations calendar

| Cadence | Expected operation | Independent check |
|---|---|---|
| Per event | Termination, deployment, incident, sensitive-data disposal | Full eligible event reconciliation and completion evidence |
| Daily | Config/asset collection, backup and scanner intake | Expected/observed resource counts, freshness and heartbeat |
| Weekly | Alerts, vulnerabilities and failed/unknown results | Aging, assigned owners, actual corrective progress |
| Monthly | Control review, evidence access, capacity and pipeline health | Missing-run ledger, review decisions and escalation |
| Quarterly | Access recertification, recovery exercise, oversight | Population completeness, independent retest, approved action follow-up |
| Annually/material change | Risk, policies, training, vendor reports and boundary | Updated commitments, report coverage and design adequacy |

The calendar supports period evidence; it is not a mandatory SOC 2 schedule. Adopt frequencies justified by the system's risks and commitments.
