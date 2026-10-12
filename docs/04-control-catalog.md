# Control catalog and AWS implementation/testing handbook

36 original illustrative controls. The selected scenario excludes EXT-01 through EXT-03; they teach optional category work. Mappings indicate contributions, not a full compliance determination. Each implementation describes a proposed design, not a claim that an AWS deployment exists.

## GOV-01 · Accountability and independent oversight

**Domain:** Governance · **Owner:** Executive sponsor · **Frequency:** Quarterly

**Supporting references:** CC1.1, CC1.2, CC1.3, CC1.5. Supports the listed criteria in this system; partial, judgment-based mapping, not criterion equivalence.

**Risk:** Controls can be bypassed when responsibilities and escalation rights are unclear.

**Population:** Service leadership, control owners, oversight meetings

**Proposed implementation:** Approve an ethics policy, accountability matrix, delegated authority and independent oversight charter. Assign a primary and backup for every control.

**Design test:** Inspect approval authority and conflicts between operator, reviewer and risk acceptor.

**Operating test:** Inspect each quarterly oversight packet and trace overdue issues to decisions and follow-up.

**Evidence:** Approved charter; RACI version history; Meeting minutes; Action register.

**Automation:** Human review.

**Limits:** AWS account ownership does not establish organizational accountability.

**Reference:** [AWS Security Reference Architecture](https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture/welcome.html)

## GOV-02 · Workforce competence and security education

**Domain:** Governance · **Owner:** People operations · **Frequency:** At hire and annually

**Supporting references:** CC1.4, CC2.2. Supports the listed criteria in this system; partial, judgment-based mapping, not criterion equivalence.

**Risk:** Untrained personnel mishandle customer data or escalate incidents too late.

**Population:** Employees and contractors with scoped system access

**Proposed implementation:** Require role-specific onboarding, acceptable-use acknowledgement and security training before production access. Track contractors as well as employees.

**Design test:** Confirm curriculum addresses data handling, reporting, privileged work and access termination.

**Operating test:** Reconcile HR roster to completion records. Inspect overdue training and approved follow-up for every missed deadline.

**Evidence:** HR roster; Training export; Acknowledgements; Follow-up tickets.

**Automation:** Human review.

**Limits:** A completion certificate does not prove a person can perform an operational procedure.

**Reference:** [AWS Security Reference Architecture](https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture/welcome.html)

## GOV-03 · Commitments and customer communication

**Domain:** Governance · **Owner:** Service owner · **Frequency:** Quarterly and material change

**Supporting references:** CC2.1, CC2.2, CC2.3. Supports the listed criteria in this system; partial, judgment-based mapping, not criterion equivalence.

**Risk:** The system fails promises that engineering never received.

**Population:** Contracts, security promises, SLAs, notices and support channels

**Proposed implementation:** Maintain a commitments register linking customer promises to controls, metrics and notification procedures. Approve changes jointly with legal and engineering.

**Design test:** Trace each promise to a measurable system requirement and named owner.

**Operating test:** Inspect contract changes and a notification exercise; verify owners received changes before release.

**Evidence:** Commitments register; Approved notices; Communication records.

**Automation:** Human review.

**Limits:** A marketing availability claim is not evidence of delivered availability.

**Reference:** [AWS Security Reference Architecture](https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture/welcome.html)

## RSK-01 · Risk assessment with change and fraud analysis

**Domain:** Governance · **Owner:** Risk owner · **Frequency:** Annually and material change

**Supporting references:** CC3.1, CC3.2, CC3.3, CC3.4, CC9.1. Supports the listed criteria in this system; partial, judgment-based mapping, not criterion equivalence.

**Risk:** Risk treatment overlooks insider misuse, dependency failures or new data flows.

**Population:** Service assets, threat scenarios, suppliers and planned changes

**Proposed implementation:** Define objectives and risk thresholds. Assess inherent and residual risk, including fraud and tenant isolation. Reassess after expansion, acquisition or incidents.

**Design test:** Inspect scoring rules and scenario coverage; trace high risks to treatment owners.

**Operating test:** Inspect the approved assessment, change-triggered reassessments and treatment follow-through.

**Evidence:** Risk register; Threat model; Treatment approvals; Change assessments.

**Automation:** Human review.

**Limits:** Risk scoring is a prioritization convention, not a calculated probability of loss.

**Reference:** [AWS Security Reference Architecture](https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture/welcome.html)

## MON-01 · Independent controls evaluation and issue escalation

**Domain:** Governance · **Owner:** Assurance lead · **Frequency:** Monthly

**Supporting references:** CC4.1, CC4.2. Supports the listed criteria in this system; partial, judgment-based mapping, not criterion equivalence.

**Risk:** The dashboard appears healthy while control evidence is absent or unreliable.

**Population:** All scoped controls and outstanding findings

**Proposed implementation:** Review control design, test results, unknowns and aging issues independently of operation. Escalate repeated deficiencies to oversight.

**Design test:** Confirm review criteria, escalation triggers and reviewer independence.

**Operating test:** Trace monthly review decisions to evidence, tickets and independently verified closure.

**Evidence:** Review packs; Evaluation workpapers; Escalations; Retest records.

**Automation:** Human review.

**Limits:** A native compliance score excludes human controls and unrecorded resources.

**Reference:** [AWS Config rule evaluation](https://docs.aws.amazon.com/config/latest/developerguide/evaluate-config.html)

## GOV-04 · Policies, procedures and control versioning

**Domain:** Governance · **Owner:** Policy owner · **Frequency:** Annual review and every change

**Supporting references:** CC5.1, CC5.2, CC5.3. Supports the listed criteria in this system; partial, judgment-based mapping, not criterion equivalence.

**Risk:** A documented objective has no executable procedure or deployed enforcement.

**Population:** Policies, operating runbooks and automated test definitions

**Proposed implementation:** Version policy requirements, operating procedures and test parameters together. Approve substantive changes and communicate effective dates.

**Design test:** Walk a requirement from policy to operator instructions and technology enforcement.

**Operating test:** Inspect policy reviews and change records; verify the effective version matches tested operation.

**Evidence:** Policy history; Procedure approvals; Control specification; Release history.

**Automation:** Human review.

**Limits:** Publishing a policy alone cannot demonstrate that it operated.

**Reference:** [AWS Security Reference Architecture](https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture/welcome.html)

## IAM-01 · Federated identity and MFA enforcement

**Domain:** Identity · **Owner:** Identity engineering · **Frequency:** Continuous; quarterly review

**Supporting references:** CC6.1, CC6.2. Supports the listed criteria in this system; partial, judgment-based mapping, not criterion equivalence.

**Risk:** Stolen credentials allow privileged access.

**Population:** Workforce identities, Identity Center assignments and emergency IAM users

**Proposed implementation:** Use an identity provider with MFA and conditional access, IAM Identity Center permission sets and short-lived role sessions. Maintain separately monitored emergency access.

**Design test:** Review IdP enforcement, bypass paths, permission sets and session duration. Test denied and allowed logins in a sandbox.

**Operating test:** Correlate sign-in records, role assumptions and exception approvals across the period.

**Evidence:** IdP policy export; Identity Center assignments; Sign-in logs; Break-glass drills.

**Automation:** API collection + human review.

**Limits:** IAM credential reports omit federated users. A missing aws:MultiFactorAuthPresent value does not establish missing MFA for federation.

**Reference:** [IAM MFA API access](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_mfa_configure-api-require.html)

## IAM-02 · Least privilege and access recertification

**Domain:** Identity · **Owner:** System owner · **Frequency:** Quarterly and role change

**Supporting references:** CC6.1, CC6.3. Supports the listed criteria in this system; partial, judgment-based mapping, not criterion equivalence.

**Risk:** Accumulated privilege enables data theft or unauthorized changes.

**Population:** Human assignments, service roles, trust policies and resource grants

**Proposed implementation:** Grant job-based permission sets and narrow workload roles. Review identity policies together with resource policies, trust, session policies, boundaries and organization restrictions.

**Design test:** Test representative effective-access paths including cross-account assumptions and explicit denies.

**Operating test:** Reconcile assignments to HR and role inventory. Inspect each review decision and evidence that revoked grants were removed.

**Evidence:** Assignment inventory; Reviewer decisions; Policy simulation context; Removal tickets.

**Automation:** API collection + human review.

**Limits:** SCPs and permission boundaries limit grants; neither grants permissions. Policy simulations need context and do not prove every runtime path.

**Reference:** [IAM policy evaluation logic](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html)

## IAM-03 · Privileged and emergency access

**Domain:** Identity · **Owner:** Security operations · **Frequency:** Per use; monthly review

**Supporting references:** CC6.2, CC6.3. Supports the listed criteria in this system; partial, judgment-based mapping, not criterion equivalence.

**Risk:** Unreviewed root use bypasses routine separation of duties.

**Population:** Root principals, privileged sessions and emergency credentials

**Proposed implementation:** Remove root access keys, protect emergency identities with MFA, prohibit routine root work, require approval and alert on privileged use. Evaluate centralized root management where appropriate.

**Design test:** Inspect custody, approval, monitoring and emergency recovery procedures.

**Operating test:** Trace every emergency use to justification, approval, session logs and after-action review.

**Evidence:** Root credential status; Privileged-use logs; Approvals; Drill results.

**Automation:** Human review.

**Limits:** A root MFA screenshot cannot demonstrate that privileged use was reviewed.

**Reference:** [IAM MFA API access](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_mfa_configure-api-require.html)

## IAM-04 · Leaver access removal across every access path

**Domain:** Identity · **Owner:** Identity operations · **Frequency:** Per termination; daily reconciliation

**Supporting references:** CC6.2, CC6.3. Supports the listed criteria in this system; partial, judgment-based mapping, not criterion equivalence.

**Risk:** A departed worker retains usable access.

**Population:** HR terminations joined to IdP, cloud assignments, IAM credentials and active sessions

**Proposed implementation:** Set a one-hour lab SLA for all access paths. Disable IdP login, remove assignments, address active role sessions and native keys, and record final effective-access removal time.

**Design test:** Inspect joins, immutable HR identifiers, time zones, retry handling and orphan-account detection.

**Operating test:** Evaluate all terminations against access-path exports. Investigate missing joins and late removal; independently retest each path.

**Evidence:** HR events; Assignment removal; Session/key invalidation records; Reconciliation report.

**Automation:** Executable offline test.

**Limits:** The executable check evaluates supplied final-removal timestamps. It does not query HR or revoke access. Identity Center logout alone does not end existing IAM role sessions.

**Reference:** [Identity Center authentication sessions](https://docs.aws.amazon.com/singlesignon/latest/userguide/authconcept.html)

## IAM-05 · Workload identity and secret lifecycle

**Domain:** Identity · **Owner:** Platform engineering · **Frequency:** Continuous; quarterly review

**Supporting references:** CC6.1, CC6.3, CC6.6. Supports the listed criteria in this system; partial, judgment-based mapping, not criterion equivalence.

**Risk:** Long-lived build secrets or broad trust let attackers assume production roles.

**Population:** Runtime roles, CI identities, secrets and trust relationships

**Proposed implementation:** Use ECS task roles and OIDC federation for CI. Constrain audience, repository and environment subjects. Store secrets in Secrets Manager and verify rotation consumers.

**Design test:** Review role trust, secrets access, rotation design and prod/nonprod isolation.

**Operating test:** Inspect role use, denied federation tests and successful rotation exercises without exposing secret values.

**Evidence:** Trust policies; OIDC claims; Rotation metadata; Consumer validation.

**Automation:** API collection + human review.

**Limits:** No static access key does not imply a narrowly scoped role.

**Reference:** [IAM OIDC federation](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_oidc.html)

## DAT-01 · S3 public-access prevention

**Domain:** Data protection · **Owner:** Storage owner · **Frequency:** Continuous; daily evaluation

**Supporting references:** CC6.1, CC6.6, C1.1. Supports the listed criteria in this system; partial, judgment-based mapping, not criterion equivalence.

**Risk:** Public access exposes customer content.

**Population:** Customer-data buckets and documented public delivery buckets

**Proposed implementation:** Apply account and bucket public-access blocks, minimize resource policies, disable unnecessary ACLs and review access points and cross-account grants. Keep approved public delivery separate.

**Design test:** Inspect effective policies, account settings and alternate access paths against classification.

**Operating test:** Reconcile bucket inventory to current Config public-read results, investigate every exception and test external access safely.

**Evidence:** Bucket inventory; Config evaluations; Public-access settings; Policy review.

**Automation:** Executable Config evidence test.

**Limits:** The live collector supports public-read prevention only. It does not test public write, tenant authorization or every access point.

**Reference:** [Config S3 public-read managed rule](https://docs.aws.amazon.com/config/latest/developerguide/s3-bucket-public-read-prohibited.html)

## DAT-02 · Encryption and key governance

**Domain:** Data protection · **Owner:** Key custodian · **Frequency:** Continuous; quarterly review

**Supporting references:** CC6.1, CC6.7, C1.1. Supports the listed criteria in this system; partial, judgment-based mapping, not criterion equivalence.

**Risk:** Sensitive data or cryptographic keys become accessible to unauthorized parties.

**Population:** S3 objects, RDS storage, EBS volumes and relevant KMS keys

**Proposed implementation:** Use customer-managed KMS keys where the data policy requires them. Review key policies, grants, deletion controls and rotation eligibility. Check existing objects as well as bucket defaults.

**Design test:** Verify key access separation, service integration and rotation strategy for the specific key type.

**Operating test:** Inspect key changes and denied-use tests; reconcile object inventory to required encryption and key IDs.

**Evidence:** Encryption metadata; KMS policies and grants; Key change logs; Object inventory.

**Automation:** API collection + human review.

**Limits:** S3 encrypts new uploads by default. Bucket default SSE-KMS does not re-encrypt old objects; encryption headers and service delivery paths require deliberate design.

**Reference:** [S3 server-side encryption](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingServerSideEncryption.html)

## DAT-03 · Transport protection and network boundaries

**Domain:** Data protection · **Owner:** Network engineering · **Frequency:** Continuous; monthly review

**Supporting references:** CC6.6, CC6.7. Supports the listed criteria in this system; partial, judgment-based mapping, not criterion equivalence.

**Risk:** Traffic is intercepted or untrusted networks reach sensitive services.

**Population:** Public endpoints, VPC paths, database connections and external transfers

**Proposed implementation:** Require HTTPS at public ingress, private application/database subnets, restrictive security groups and scoped endpoints. Enforce database TLS and controlled egress.

**Design test:** Review path diagrams, endpoint policies, listener settings and TLS clients.

**Operating test:** Test blocked paths and plaintext requests; inspect rule changes and certificate renewal evidence.

**Evidence:** Network diagrams; Listener/SG exports; Connectivity tests; TLS test results.

**Automation:** API collection + human review.

**Limits:** A private subnet does not by itself prevent exfiltration or enforce tenant isolation.

**Reference:** [AWS Security Reference Architecture](https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture/welcome.html)

## DAT-04 · Confidential data retention and disposal

**Domain:** Data protection · **Owner:** Data owner · **Frequency:** Monthly and on deletion request

**Supporting references:** CC6.5, CC6.7, C1.1, C1.2. Supports the listed criteria in this system; partial, judgment-based mapping, not criterion equivalence.

**Risk:** Data persists beyond agreed retention or disposal destroys required evidence.

**Population:** Customer content, replicas, logs, exports, backups and keys

**Proposed implementation:** Maintain classification and retention rules. Track deletion through replicas and backup expiration, apply legal-hold exceptions and document custody for physical disposal inherited from AWS.

**Design test:** Inspect deletion paths, retention conflicts and customer commitments.

**Operating test:** Trace selected deletion events to application records, storage changes and backup expiration; verify legal holds are authorized.

**Evidence:** Classification register; Deletion workflow; Lifecycle configs; Disposal verification.

**Automation:** Human review.

**Limits:** Deleting a live object does not delete older versions, locked evidence or backup copies.

**Reference:** [S3 Object Lock](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html)

## APP-01 · Tenant isolation and data-flow authorization

**Domain:** Application · **Owner:** Application security · **Frequency:** Every release and quarterly

**Supporting references:** CC6.1, CC6.6, CC6.7. Supports the listed criteria in this system; partial, judgment-based mapping, not criterion equivalence.

**Risk:** A valid customer reads or writes another tenant’s content.

**Population:** API routes, worker jobs, signed URLs and customer-data paths

**Proposed implementation:** Derive tenant identity server-side, scope every read/write, separate worker privileges and bind signed URLs to authorized objects. Document trust boundaries and data sinks.

**Design test:** Inspect authorization design across ingress, application, storage, queues and export paths.

**Operating test:** Run cross-tenant positive/negative tests and trace a canary through application logs, CloudTrail data events and the evidence store.

**Evidence:** Data-flow diagram; Authorization tests; Canary trace; Remediation verification.

**Automation:** Human review.

**Limits:** IAM encryption controls cannot prove application-layer tenant isolation.

**Reference:** [CloudTrail data events](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-data-events-with-cloudtrail.html)

## APP-02 · Controlled uploads and data ingress

**Domain:** Application · **Owner:** Application owner · **Frequency:** Per upload and release

**Supporting references:** CC6.8, CC7.1. Supports the listed criteria in this system; partial, judgment-based mapping, not criterion equivalence.

**Risk:** Malicious content or unsafe components execute in the service.

**Population:** Untrusted files, dependencies, containers and import jobs

**Proposed implementation:** Validate types and size, scan untrusted content, quarantine failures and restrict execution permissions. Apply dependency and container scanning before promotion.

**Design test:** Inspect bypass handling and quarantine isolation.

**Operating test:** Test rejected content and inspect scan failures, promotion decisions and dependency exceptions.

**Evidence:** Scan records; Quarantine tests; Build gates; Exception approvals.

**Automation:** Human review.

**Limits:** A scan enabled setting does not establish complete input coverage.

**Reference:** [AWS Security Reference Architecture](https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture/welcome.html)

## OPS-01 · Logging coverage and delivery integrity

**Domain:** Operations · **Owner:** Platform security · **Frequency:** Continuous; daily health review

**Supporting references:** CC2.1, CC7.2. Supports the listed criteria in this system; partial, judgment-based mapping, not criterion equivalence.

**Risk:** Actions cannot be reconstructed because events were never recorded or delivered.

**Population:** Organization accounts, enabled regions, required event types and log destinations

**Proposed implementation:** Centralize an organization trail, management events and selected sensitive data events in a log account. Enable digest files, restrictive access and delivery alarms. Record excluded events.

**Design test:** Review account/region selectors, key/bucket permissions, digest handling and retention.

**Operating test:** Trace generated canary events end to end; check delivery errors, event latency, validation results and health alerts throughout the period.

**Evidence:** Selectors; Trail status; Canary traces; Digest validation; Delivery alarms.

**Automation:** API collection + human review.

**Limits:** CloudTrail event history covers recent management activity. A trail enabled result alone proves neither data-event coverage nor delivery.

**Reference:** [CloudTrail data events](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-data-events-with-cloudtrail.html)

## OPS-02 · Detection and accountable alert response

**Domain:** Operations · **Owner:** Security operations · **Frequency:** Continuous; weekly triage review

**Supporting references:** CC7.2, CC7.3. Supports the listed criteria in this system; partial, judgment-based mapping, not criterion equivalence.

**Risk:** Threat findings are generated but nobody assesses them.

**Population:** GuardDuty, Security Hub CSPM, application alerts and routed findings

**Proposed implementation:** Define severity routing, owner acknowledgment targets and escalation. Feed GuardDuty and application detections to the response queue and monitor the routing pipeline.

**Design test:** Generate safe sample findings and verify every expected destination and escalation rule.

**Operating test:** Trace the alert population to acknowledgments, analysis, dispositions and SLA breaches.

**Evidence:** Detector settings; Alert exports; Triage tickets; Routing tests.

**Automation:** API collection + human review.

**Limits:** GuardDuty threat detection and Security Hub posture checks serve different purposes. Finding suppression is not remediation.

**Reference:** [GuardDuty findings](https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_findings.html)

## OPS-03 · Vulnerability management and verified remediation

**Domain:** Operations · **Owner:** Service engineering · **Frequency:** Daily intake; weekly review

**Supporting references:** CC7.1, CC7.2. Supports the listed criteria in this system; partial, judgment-based mapping, not criterion equivalence.

**Risk:** Known vulnerabilities remain reachable in production.

**Population:** Deployed images, EC2 instances, Lambda packages and dependency inventories

**Proposed implementation:** Use Inspector and build scanning; set risk-based deadlines that consider exposure and exploitability. Track exceptions with expiry and compensating controls.

**Design test:** Reconcile deployed assets to supported scanners and verify deadline rules.

**Operating test:** Trace findings to patched deployment digests and fresh rescans; preserve aged and accepted failures.

**Evidence:** Asset/scanner reconciliation; Findings; Patch tickets; Rescan evidence.

**Automation:** API collection + human review.

**Limits:** A critical-CVE count ignores unscanned assets. A closed ticket without a rescan does not prove correction.

**Reference:** [Inspector findings](https://docs.aws.amazon.com/inspector/latest/user/findings-managing.html)

## OPS-04 · Incident response and lessons learned

**Domain:** Operations · **Owner:** Incident commander · **Frequency:** Per incident; semiannual exercise

**Supporting references:** CC7.3, CC7.4, CC7.5. Supports the listed criteria in this system; partial, judgment-based mapping, not criterion equivalence.

**Risk:** Teams fail to contain, notify or recover during an incident.

**Population:** Security events, incidents, communications and recovery actions

**Proposed implementation:** Define severity, command roles, legal/customer communication, forensic custody, containment and recovery runbooks. Exercise a credential compromise with customer-data impact.

**Design test:** Walk through escalation and decision authority including out-of-hours coverage.

**Operating test:** Inspect the incident population, a tabletop and actual remediation actions with verified completion.

**Evidence:** Incident timeline; Exercise packet; Custody log; After-action register.

**Automation:** Human review.

**Limits:** Tabletop attendance does not establish that technical recovery succeeds.

**Reference:** [AWS Security Reference Architecture](https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture/welcome.html)

## CHG-01 · Independent approval tied to the deployed commit

**Domain:** Change management · **Owner:** Release owner · **Frequency:** Every production deployment

**Supporting references:** CC8.1. Supports the listed criteria in this system; partial, judgment-based mapping, not criterion equivalence.

**Risk:** Self-approved or unreviewed code reaches production.

**Population:** Production deployment events joined to PRs, reviews and immutable commit IDs

**Proposed implementation:** Protect branches and release environments, require an independent authorized reviewer, bind approval to the deployed SHA and control emergency paths. Use OIDC for AWS deployment roles.

**Design test:** Inspect bypass rights, approval freshness after commits and actor authorization.

**Operating test:** Reconcile every deployment to its exact SHA, approval before deployment, independent reviewer and successful required checks.

**Evidence:** Deployment events; Commit approvals; Branch rules; CI check exports.

**Automation:** Executable offline test.

**Limits:** The executable test uses normalized exports. It does not query GitHub, check review dismissal policy or prove all deployments were exported.

**Reference:** [IAM OIDC federation](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_oidc.html)

## CHG-02 · Infrastructure policy gates and drift

**Domain:** Change management · **Owner:** Platform engineering · **Frequency:** Every change; daily drift review

**Supporting references:** CC5.2, CC7.1, CC8.1. Supports the listed criteria in this system; partial, judgment-based mapping, not criterion equivalence.

**Risk:** Approved infrastructure differs from deployed state or violates a baseline.

**Population:** Terraform/CloudFormation plans, deployed infrastructure and break-glass changes

**Proposed implementation:** Review plans and apply policy checks for public exposure, encryption and logging. Pin tool versions, capture applied plan hashes and route out-of-band changes for review.

**Design test:** Inspect rule coverage, bypass authority and false-negative fixtures.

**Operating test:** Trace plans to approvals, deployments and Config drift. Reconcile emergency changes to retrospective review.

**Evidence:** Plan hashes; Policy results; Apply records; Drift tickets.

**Automation:** API collection + human review.

**Limits:** A passing plan does not prove the live resource remained configured correctly.

**Reference:** [AWS Config rule evaluation](https://docs.aws.amazon.com/config/latest/developerguide/evaluate-config.html)

## CHG-03 · Secure development and dependency provenance

**Domain:** Change management · **Owner:** Engineering lead · **Frequency:** Every release

**Supporting references:** CC6.8, CC8.1. Supports the listed criteria in this system; partial, judgment-based mapping, not criterion equivalence.

**Risk:** A compromised dependency or build produces an unsafe release.

**Population:** Repositories, dependencies, images, tests and deployment artifacts

**Proposed implementation:** Threat-model major features, review code, run security tests and dependency scans, and promote immutable signed or verified artifacts. Restrict build role and repository administration.

**Design test:** Review trust boundaries from source to registry to runtime and required security gates.

**Operating test:** Inspect release samples across teams and period; verify artifact digest and gate completion at deployment.

**Evidence:** Threat models; SBOMs; Scan results; Artifact provenance; Release logs.

**Automation:** Human review.

**Limits:** A signature authenticates a producer; it does not prove secure code or correct configuration.

**Reference:** [AWS Security Reference Architecture](https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture/welcome.html)

## RES-01 · Backup coverage and protected recovery points

**Domain:** Resilience · **Owner:** Backup owner · **Frequency:** Daily; monthly inventory review

**Supporting references:** CC7.5, A1.2. Supports the listed criteria in this system; partial, judgment-based mapping, not criterion equivalence.

**Risk:** Ransomware or failure destroys both primary data and recovery copies.

**Population:** RDS, S3 and other committed recovery assets across accounts

**Proposed implementation:** Map asset-specific RPO to backup cadence and retention. Use separate recovery custody, scoped permissions and cross-account/region copies where justified. Validate KMS access and protected vault policy.

**Design test:** Inspect protected assets, failed jobs, deletion rights and recovery dependencies.

**Operating test:** Reconcile source assets to successful recovery points within approved RPO; investigate failed and missing jobs.

**Evidence:** Backup plans; Protected-resource inventory; Job history; Vault/key policies.

**Automation:** API collection + human review.

**Limits:** RDS Multi-AZ supports availability; it does not replace a recovery copy.

**Reference:** [AWS Backup restore testing](https://docs.aws.amazon.com/aws-backup/latest/devguide/restore-testing.html)

## RES-02 · Restore testing against RTO and RPO

**Domain:** Resilience · **Owner:** Recovery owner · **Frequency:** Quarterly and major architecture change

**Supporting references:** CC7.5, A1.3. Supports the listed criteria in this system; partial, judgment-based mapping, not criterion equivalence.

**Risk:** Backups exist but recovery misses customer commitments or restores unusable data.

**Population:** Scheduled restore exercises for each critical service and dependency

**Proposed implementation:** Restore into an isolated environment, validate application/data integrity, measure recovery from disruption start and measure recovered data lag against RTO/RPO. Record cleanup.

**Design test:** Review test realism, start/finish definitions and required dependency validation.

**Operating test:** Compare each exercise to four-hour RTO and one-hour RPO lab thresholds; inspect application sign-off and retest late or incomplete exercises.

**Evidence:** Restore job; Disruption/recovery times; Recovered-data timestamp; Validation sign-off.

**Automation:** Executable offline test.

**Limits:** The executable test evaluates provided measurements and validation status. It does not restore AWS resources.

**Reference:** [AWS Backup restore testing](https://docs.aws.amazon.com/aws-backup/latest/devguide/restore-testing.html)

## RES-03 · Availability capacity and failover readiness

**Domain:** Resilience · **Owner:** Site reliability · **Frequency:** Monthly; semiannual failover

**Supporting references:** A1.1, A1.2, A1.3. Supports the listed criteria in this system; partial, judgment-based mapping, not criterion equivalence.

**Risk:** Capacity exhaustion or dependency failure interrupts the service.

**Population:** Committed service paths, quotas, multi-AZ dependencies and capacity metrics

**Proposed implementation:** Set SLOs tied to commitments, monitor saturation and quotas, distribute critical paths across availability zones and document region-recovery tradeoffs.

**Design test:** Inspect single points of failure, capacity assumptions and alert thresholds.

**Operating test:** Inspect load/failover tests, response to saturation alarms and measured restoration within objectives.

**Evidence:** Capacity forecasts; SLO reports; Load tests; Failover reports.

**Automation:** Human review.

**Limits:** An architectural multi-AZ label cannot demonstrate successful failover.

**Reference:** [RDS Multi-AZ](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.MultiAZ.html)

## VND-01 · Supplier assurance and AWS report review

**Domain:** Third parties · **Owner:** Vendor risk owner · **Frequency:** At onboarding and annually

**Supporting references:** CC9.2. Supports the listed criteria in this system; partial, judgment-based mapping, not criterion equivalence.

**Risk:** Inherited controls or supplier dependencies fail without a customer response.

**Population:** AWS, identity provider, source host and critical monitoring suppliers

**Proposed implementation:** Tier vendors, review current SOC reports and contractual safeguards, identify report exceptions and map relevant complementary user entity controls to internal owners.

**Design test:** Inspect service/region coverage, report period, scope and carve-outs.

**Operating test:** Review annual packets and follow-up; trace AWS user controls to the service’s own evidence.

**Evidence:** Vendor inventory; Restricted report-review memo; CUEC mapping; Follow-up actions.

**Automation:** Human review.

**Limits:** AWS SOC 2 does not attest to this SaaS configuration. A bridge letter is a management statement and does not extend the audited period.

**Reference:** [AWS SOC FAQ](https://aws.amazon.com/compliance/soc-faqs/)

## VND-02 · Business disruption and dependency mitigation

**Domain:** Third parties · **Owner:** Service owner · **Frequency:** Annual exercise and dependency change

**Supporting references:** CC9.1, CC9.2. Supports the listed criteria in this system; partial, judgment-based mapping, not criterion equivalence.

**Risk:** A supplier failure or staff loss interrupts service without an alternative.

**Population:** Critical supplier outages, key staff absence and communications

**Proposed implementation:** Document fallback, dependency recovery, customer notification and alternate operational coverage. Assess insurance and other risk-transfer choices as part of risk treatment.

**Design test:** Inspect dependency scenarios, responsibilities and realistic fallback assumptions.

**Operating test:** Exercise a supplier outage and inspect actions to remove unworkable dependencies.

**Evidence:** Dependency map; Continuity exercise; Treatment decisions.

**Automation:** Human review.

**Limits:** Risk transfer does not remove the need to meet the service’s own commitments.

**Reference:** [AWS Security Reference Architecture](https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture/welcome.html)

## PHY-01 · Physical responsibility boundary

**Domain:** Third parties · **Owner:** Facilities and vendor risk · **Frequency:** Annual; per personnel change

**Supporting references:** CC6.4, CC6.5. Supports the listed criteria in this system; partial, judgment-based mapping, not criterion equivalence.

**Risk:** Physical custody is assumed to be entirely inherited even for employee devices.

**Population:** AWS facilities plus workforce endpoints and any customer-operated locations

**Proposed implementation:** Inherit AWS datacenter physical controls through relevant report review. Maintain endpoint inventory, device access, return and disposal procedures for workforce assets.

**Design test:** Separate provider facilities from customer-controlled devices and premises.

**Operating test:** Inspect report review and selected device return/disposal records.

**Evidence:** AWS report-review memo; Endpoint inventory; Device return records.

**Automation:** Human review.

**Limits:** AWS datacenter assurance does not cover a contractor laptop.

**Reference:** [AWS shared responsibility](https://aws.amazon.com/compliance/shared-responsibility-model/)

## EVD-01 · Evidence custody and data minimization

**Domain:** Assurance engineering · **Owner:** Evidence custodian · **Frequency:** Each collection; monthly access review

**Supporting references:** CC2.1, CC4.1, CC5.2. Supports the listed criteria in this system; partial, judgment-based mapping, not criterion equivalence.

**Risk:** Evidence can be overwritten, detached from its source or expose customer secrets.

**Population:** Raw exports, test outputs, manifests and restricted audit artifacts

**Proposed implementation:** Capture UTC observation/collection times, scope and logic hashes, raw response pointers and approvals. Store protected evidence separately from public synthetic examples; restrict retention and access.

**Design test:** Inspect chain of custody, tamper detection, access restrictions and redaction method.

**Operating test:** Recompute manifests, inspect access history and trace output to raw input and reviewed logic.

**Evidence:** Hash manifest; Run metadata; Custody log; Evidence access review.

**Automation:** Executable evidence packaging.

**Limits:** A hash detects a changed file only if the manifest is trusted. It is not a signature or proof of source authenticity.

**Reference:** [S3 Object Lock](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html)

## EVD-02 · Monitor the monitoring pipeline

**Domain:** Assurance engineering · **Owner:** Monitoring owner · **Frequency:** Every scheduled run

**Supporting references:** CC4.1, CC7.2. Supports the listed criteria in this system; partial, judgment-based mapping, not criterion equivalence.

**Risk:** A stopped collector displays an old passing result indefinitely.

**Population:** Expected collections by account, region, control and cadence

**Proposed implementation:** Compare scheduled runs to an independent heartbeat inventory, alert on missed/failing jobs, monitor evidence age and reconcile expected to observed resources. Assign unknowns to owners.

**Design test:** Seed denied APIs, truncated pages, malformed values and missed schedules; verify alarms and escalation.

**Operating test:** Inspect missed-run population, freshness results and recovery tickets; verify the detector still runs when the collector fails.

**Evidence:** Schedule inventory; Heartbeat records; Seeded-fault results; Alert tickets.

**Automation:** API collection + human review.

**Limits:** A job-success signal does not prove a complete extract.

**Reference:** [AWS Config rule evaluation](https://docs.aws.amazon.com/config/latest/developerguide/evaluate-config.html)

## EXT-01 · Processing completeness and accuracy

**Domain:** Optional extensions · **Owner:** Data processing owner · **Frequency:** Every batch and release

**Supporting references:** PI1.1, PI1.2, PI1.3, PI1.4, PI1.5. Supports the listed criteria in this system; partial, judgment-based mapping, not criterion equivalence.

**Risk:** A job silently drops, duplicates or corrupts customer records.

**Population:** Input manifests, processing jobs, outputs and stored results

**Proposed implementation:** If processing integrity enters scope, define accepted inputs, processing specifications, reconciliation totals, retry/idempotency and output/storage checks. Reject bad input and route discrepancies.

**Design test:** Inspect completeness and correctness requirements at input, processing, output and storage boundaries.

**Operating test:** Trace input identifiers to output counts/hashes; seed duplicates, missing records and unauthorized transformations.

**Evidence:** Input/output manifests; Reconciliation totals; Job error records; Validation approvals.

**Automation:** Human review.

**Limits:** Checksums alone do not prove business-level correctness. This extension is outside the selected examination scenario.

**Reference:** [AWS Security Reference Architecture](https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture/welcome.html)

## EXT-02 · Privacy purpose, notice and choice

**Domain:** Optional extensions · **Owner:** Privacy owner · **Frequency:** At collection and purpose change

**Supporting references:** P1.1, P2.1, P3.1, P3.2. Supports the listed criteria in this system; partial, judgment-based mapping, not criterion equivalence.

**Risk:** Personal information is collected without appropriate notice, authority or choice.

**Population:** Personal-information purposes, notices, consent and collection channels

**Proposed implementation:** If Privacy enters scope, inventory purposes, define notices and lawful/contractual collection conditions, implement choice where applicable, and record valid consent decisions.

**Design test:** Inspect notice/choice design and alignment with actual collection flows.

**Operating test:** Trace a personal-information collection to current notice, relevant choice and approved purpose.

**Evidence:** Purpose inventory; Notice history; Consent/choice records.

**Automation:** Human review.

**Limits:** Confidentiality protects designated information; Privacy includes obligations across the personal-information lifecycle. This scenario excludes Privacy attestation.

**Reference:** [AWS Security Reference Architecture](https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture/welcome.html)

## EXT-03 · Privacy lifecycle and individual rights

**Domain:** Optional extensions · **Owner:** Privacy operations · **Frequency:** Per request; quarterly monitoring

**Supporting references:** P4.1, P4.2, P4.3, P5.1, P5.2, P6.1, P6.2, P6.3, P6.4, P6.5, P6.6, P6.7, P7.1, P8.1. Supports the listed criteria in this system; partial, judgment-based mapping, not criterion equivalence.

**Risk:** Individuals cannot exercise applicable rights and onward disclosures escape monitoring.

**Population:** Personal-information use, retention, rights, disclosures, quality and complaints

**Proposed implementation:** Define purpose-limited use, retention/disposal, identity verification for requests, access/correction, third-party sharing terms, breach communications and complaint handling.

**Design test:** Trace the lifecycle inventory to rights/disclosure procedures and monitoring responsibilities.

**Operating test:** Inspect requests, corrections, deletion/retention decisions, third-party authorizations and complaint resolution against stated deadlines.

**Evidence:** Rights register; Disclosure records; Correction records; Complaint monitoring.

**Automation:** Human review.

**Limits:** This extension needs jurisdiction-specific legal review; a SOC 2 privacy scope does not establish blanket legal compliance.

**Reference:** [AWS Security Reference Architecture](https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture/welcome.html)

## AST-01 · Asset inventory and scoped population reconciliation

**Domain:** Assurance engineering · **Owner:** Asset owner · **Frequency:** Daily and on account onboarding

**Supporting references:** CC2.1, CC6.1, CC6.5. Supports the listed criteria in this system; partial, judgment-based mapping, not criterion equivalence.

**Risk:** Unknown assets escape security controls and audit populations.

**Population:** Accounts, regions, global-service identities, resources and owners

**Proposed implementation:** Reconcile Organizations, approved region lists, workload inventories and service-native exports. Track owner, classification and lifecycle including retired assets. Review gaps before excluding them.

**Design test:** Compare inventory sources and inspect discovery limits, permissions, pagination and global-service handling.

**Operating test:** Inspect daily differences and onboarding records; trace newly discovered and retired assets to required controls and disposal decisions.

**Evidence:** Account inventory; Regional resource exports; Reconciliation records; Asset lifecycle tickets.

**Automation:** API collection + human review.

**Limits:** Config only sees supported recorded resources. An inventory needs independent sources and explicit completeness checks.

**Reference:** [AWS Config rule evaluation](https://docs.aws.amazon.com/config/latest/developerguide/evaluate-config.html)
