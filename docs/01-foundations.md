# Foundations and beginner definitions

Start with the distinction between a promise, a risk and a control. A customer expects content to stay private. Unauthorized access is a risk to that promise. A tenant-aware authorization check is one control. A denied cross-tenant request is test evidence. Encryption and monitoring add separate layers, each with its own limits.

SOC 2 describes assurance over a specific system. A tool score, cloud provider report or evidence bundle cannot issue that assurance. An independent CPA evaluates the description and controls for the agreed engagement.

## SOC 2

An independent CPA examination of a service organization’s described system and controls against selected Trust Services Criteria. A report provides assurance for an identified system, date or period, and scope; it is not a product certification.

## SOC 1 / SOC 3

SOC 1 concerns controls relevant to user entities’ financial reporting. SOC 3 is a general-use trust services report with less detail. SOC 2 reports typically serve informed, specified users under restricted use.

## Type I / Type II

Type I addresses the system description and suitability of control design at a specified date. Type II adds operating effectiveness throughout a specified period and a description of tests and results. Neither replaces risk assessment.

## Trust Services Category

One of Security, Availability, Processing Integrity, Confidentiality or Privacy. CC1–CC9 are Common Criteria groupings, not nine categories. This scenario selects Security, Availability and Confidentiality.

## Criterion / point of focus

A criterion is an evaluation benchmark. Points of focus help interpret criteria; they are not a mandatory checklist of individual technology settings.

## Control

A specific action or mechanism that reduces a risk and supports an objective. State who does what, on which population, how often, what evidence remains, and how failures are handled.

## Control owner / operator / reviewer

The owner is accountable for the control; the operator performs it; the reviewer assesses evidence and follows up. Separate these roles where a conflict would undermine assurance.

## Design / implementation / operation

Design asks whether a control could meet its objective. Implementation asks whether it was put in place. Operation asks whether it actually worked with the required consistency during the examined period.

## Population

The complete set of events, identities or resources eligible for a test. An access-removal test starts with HR terminations, not only successful removal tickets.

## Sampling

Selecting items from a reconciled population for examination. Selection depends on risk, frequency, reliance and judgment; there is no universal SOC 2 sample count.

## Evidence

Source information supporting a test conclusion. It needs relevant content, trustworthy origin, time coverage, complete population context and custody.

## PBC

Prepared by client: documents and exports management supplies for auditor requests. A PBC index links request IDs to control IDs, dates, source and reviewer.

## IPE

Information produced by the entity. Validate report filters, joins, pagination, date ranges, logic and record counts before relying on internally generated reports.

## Exception / deficiency

A deviation observed during testing versus a weakness in a control’s design or operation. Assess cause, extent and effect; neither a single exception nor a ticket count determines the audit opinion by itself.

## Finding / root cause

A finding documents expected condition, actual condition, cause, impact and corrective action. Root cause explains the system failure, such as an omitted access path, rather than repeating the symptom.

## Compensating control

A different measure that reduces a risk when the preferred measure is unavailable. Its actual coverage and operation need testing; an approval alone does not make it effective.

## Risk acceptance

An authorized, time-limited decision to retain a stated risk with rationale and monitoring. It annotates a failure and does not convert the underlying test to PASS.

## Readiness

Management’s evaluation and preparation before an examination. It identifies gaps and builds evidence; it does not issue an independent SOC 2 opinion.

## System description

Management’s explanation of services, boundaries, commitments, infrastructure, software, people, procedures, data, dependencies and relevant controls.

## Management assertion

Management’s signed claims about the description and controls for the specified engagement. Management owns the assertions; the CPA owns the examination opinion.

## Subservice organization / carve-out

A provider performing part of the service, such as AWS. Under carve-out, its controls are excluded from the SaaS auditor’s testing; management still explains reliance and oversight. Inclusive treatment includes relevant provider controls in scope.

## CUEC / CSOC

Complementary user entity controls are controls expected at customers. Complementary subservice organization controls are controls expected at a provider. The SaaS is a user of AWS and a service provider to its own customers.

## Bridge letter

A management statement addressing the interval after a SOC report period. It is useful contextual evidence, not an extension of the independent audit opinion.

## Shared responsibility

AWS secures its infrastructure; the customer secures what it builds and configures. The boundary changes with the service, data and architecture.

## AWS account / region / AZ

An account is an administrative and security boundary. A region is a geographic service area; availability zones are isolated locations within a region. Define which are in scope and how global services are treated.

## IAM / STS / Identity Center

IAM defines AWS identities and permission policies. STS issues temporary credentials. Identity Center connects workforce access to account roles and permission sets.

## SCP / boundary / resource policy

An SCP restricts permitted actions for affected organization principals; a boundary caps an identity’s permissions. A resource policy controls access on the resource. Effective access depends on all relevant policies and request context.

## CloudTrail / Config

CloudTrail records selected API activity. Config records supported resource configuration and evaluates rules. Events and configuration observations answer different questions.

## GuardDuty / Security Hub / Inspector

GuardDuty detects threats. Security Hub CSPM aggregates posture findings and control checks. Inspector identifies supported workload vulnerabilities. Enablement is only the start of a response process.

## KMS / SSE-KMS

KMS manages cryptographic keys and controlled key use. SSE-KMS is server-side encryption using KMS keys. Key policies, grants and data access need review together.

## RTO / RPO

Recovery time objective is the tolerated time to restore service. Recovery point objective is tolerated data loss measured as time. A restore can meet one and miss the other.

## Continuous control monitoring

Repeated tests with defined scope, fresh inputs, versioned logic, traceable evidence, failure routing and heartbeat checks. A daily snapshot provides observations; it is not automatic proof of uninterrupted effectiveness.

## PASS / FAIL / UNKNOWN / NOT_APPLICABLE

PASS meets the executable assertion using valid evidence. FAIL has a demonstrated deviation. UNKNOWN lacks enough reliable evidence. NOT_APPLICABLE needs a documented, approved scope reason.

## OIDC / policy as code

OIDC lets a trusted workload obtain short-lived AWS identity from verified claims. Policy as code turns reviewed requirements into executable gates or detections with versioned rules and tests.

Read [the AICPA resources](12-sources.md) alongside these original teaching summaries. No licensed criteria text is reproduced.
