# Source register

Reviewed 2026-10-03. AICPA and official AWS references support the framework and service details. All scenarios, internal controls and explanatory prose are original illustrative applications. This register does not reproduce licensed criteria or restricted provider reports. Source review does not imply live AWS validation. Recheck current service behavior for actual implementations.

## AICPA Trust Services Criteria, 2017 with 2022 points of focus

[AICPA Trust Services Criteria, 2017 with 2022 points of focus](https://www.aicpa-cima.com/resources/download/2017-trust-services-criteria-with-revised-points-of-focus-2022)

Criteria references; original control designs and paraphrased teaching explanations. Download may require a free account.

## AICPA Description Criteria, 2018 with 2022 guidance

[AICPA Description Criteria, 2018 with 2022 guidance](https://www.aicpa-cima.com/resources/download/get-description-criteria-for-your-organizations-soc-2-r-report)

System-description preparation; download may require a free account.

## AICPA SOC suite and illustrative report resources

[AICPA SOC suite and illustrative report resources](https://www.aicpa-cima.com/resources/landing/system-and-organization-controls-soc-suite-of-services)

Report types and practitioner resources.

## AWS shared responsibility

[AWS shared responsibility](https://aws.amazon.com/compliance/shared-responsibility-model/)

Provider/customer boundary.

## AWS SOC FAQ

[AWS SOC FAQ](https://aws.amazon.com/compliance/soc-faqs/)

AWS reports, Artifact and report use.

## AWS Security Reference Architecture

[AWS Security Reference Architecture](https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture/welcome.html)

Multi-account design reference; verify services and implementation for your environment.

## IAM policy evaluation logic

[IAM policy evaluation logic](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html)

Effective-access caveats.

## IAM MFA API access

[IAM MFA API access](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_mfa_configure-api-require.html)

MFA context and enforcement.

## Identity Center authentication sessions

[Identity Center authentication sessions](https://docs.aws.amazon.com/singlesignon/latest/userguide/authconcept.html)

Role sessions can persist independently of the IdP session.

## IAM OIDC federation

[IAM OIDC federation](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_oidc.html)

CI workload identity.

## S3 server-side encryption

[S3 server-side encryption](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingServerSideEncryption.html)

Defaults and existing object caveats.

## Config S3 public-read managed rule

[Config S3 public-read managed rule](https://docs.aws.amazon.com/config/latest/developerguide/s3-bucket-public-read-prohibited.html)

Narrow assertion used by the live collector.

## AWS Config rule evaluation

[AWS Config rule evaluation](https://docs.aws.amazon.com/config/latest/developerguide/evaluate-config.html)

Resource coverage and evaluation semantics.

## Config compliance API

[Config compliance API](https://docs.aws.amazon.com/config/latest/APIReference/API_GetComplianceDetailsByResource.html)

Pagination and timestamps; no INSUFFICIENT_DATA filtering.

## CloudTrail data events

[CloudTrail data events](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-data-events-with-cloudtrail.html)

Explicit selectors and data-plane logging.

## CloudTrail integrity validation

[CloudTrail integrity validation](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-log-file-validation-intro.html)

Digest delivery versus actual validation.

## S3 Object Lock

[S3 Object Lock](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html)

Retention and custody choices.

## GuardDuty findings

[GuardDuty findings](https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_findings.html)

Threat finding lifecycle.

## Inspector findings

[Inspector findings](https://docs.aws.amazon.com/inspector/latest/user/findings-managing.html)

Vulnerability findings and remediation.

## AWS Backup restore testing

[AWS Backup restore testing](https://docs.aws.amazon.com/aws-backup/latest/devguide/restore-testing.html)

Restore exercises and validation.

## RDS Multi-AZ

[RDS Multi-AZ](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.MultiAZ.html)

Availability architecture.

## AWS Audit Manager SOC 2 framework

[AWS Audit Manager SOC 2 framework](https://docs.aws.amazon.com/audit-manager/latest/userguide/SOC2.html)

Automated evidence support; not independent attestation.

## Athena CloudTrail queries

[Athena CloudTrail queries](https://docs.aws.amazon.com/athena/latest/ug/cloudtrail-logs.html)

Schema/partition setup for provided SQL.

## Organizations service control policies

[Organizations service control policies](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html)

Organization guardrails and scope limitations.

## KMS key rotation

[KMS key rotation](https://docs.aws.amazon.com/kms/latest/developerguide/rotate-keys.html)

Rotation eligibility and historical keys.
