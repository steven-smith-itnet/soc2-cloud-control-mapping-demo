# Category decisions and common-control reuse

This scenario selects Security, Availability and Confidentiality. Category selection follows service commitments and the engagement, not a desire to display every category. CC1–CC9 are common groupings, and the additional A1/C1/PI1/P-series criteria address category-specific objectives. Read the authoritative AICPA criteria when preparing a real engagement.

## Availability

Connect customer availability commitments to measured capacity, environmental protection, recovery assets and tested recovery. A1.1 concerns capacity; A1.2 contributes through environmental protections, backups and recovery infrastructure; A1.3 addresses recovery testing. The original catalog splits capacity, backup coverage and restore effectiveness to avoid equating a successful backup job with recovered service.

## Confidentiality

Identify information designated confidential, control access and transfer through its lifecycle, and dispose of it according to objectives. C1.1/C1.2 complement access and data controls. Encryption is one supporting mechanism; classification, authorization, retention and disposal remain necessary. Account for copies, object versions, backups and locked audit evidence.

## Processing Integrity extension

EXT-01 adds process specifications and reconciliations across information/input, processing, output and storage. Define what an accepted input is, what complete/correct/authorized processing means, how duplicate jobs are handled, and how lost outputs are detected. Trace identifiers and counts through queues and retries. Seed dropped, duplicate and unauthorized records. A checksum can confirm bytes while the business transformation remains wrong.

This is an optional design exercise; no pipeline attestation or automated Processing Integrity test is claimed here.

## Privacy extension

EXT-02/03 consider notices and choice, collection conditions, use/retention/disposal, access/correction, disclosures, quality and monitoring. A rights workflow needs appropriate identity verification without collecting excessive new data. A deletion request needs handling across the actual lifecycle and applicable retention requirements.

Confidentiality covers designated information; Privacy covers commitments for personal information. Omitting Privacy from a SOC 2 examination does not waive privacy law, contracts or customer promises. Legal review is needed for actual jurisdictions and rights. This project does not provide jurisdiction-specific compliance conclusions.

## Reuse without false equivalence

An identity removal record might support SOC 2 logical access, an ISO 27001 access-management control and a NIST access-control requirement. That does not make the entire requirements identical. Record mapping rationale, relevant clause/version, scope, coverage and remaining obligations. Test the internal objective once where appropriate, then review each framework's distinct requirements with qualified reviewers.

For example, IAM-04's timestamp check supports prompt access removal, but does not prove the completeness of access paths or the entire SOC 2 CC6.2/CC6.3 criteria. A policy or training criterion cannot be satisfied by reusing a bucket posture result. Avoid "one test certifies every framework" language.
