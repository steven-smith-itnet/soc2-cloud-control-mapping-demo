# Readiness and independent examination support

## Distinct deliverables and responsibilities

Readiness work identifies gaps, validates controls and prepares management. A Type I engagement addresses a specified date; a Type II adds operating effectiveness throughout a specified period. Duration, sequencing, sample sizes, report timing and opinion depend on the engagement. Type I is not an obligatory prerequisite for every Type II engagement.

Management owns the system description, selected commitments, controls and assertion. A qualified independent CPA practitioner determines examination procedures and report conclusions. Engineers and assurance staff supply accurate evidence, answer walkthrough questions and remediate issues. This repository provides management-side examples only; it does not fabricate a CPA opinion.

## System-description review scaffold

Use [the system scope draft](02-system-scope.md) as a starting point. Validate against the AICPA Description Criteria with your practitioner: service type, principal commitments and requirements, system components, relevant controls, boundary, incidents, changes, subservice relationships, CUECs/CSOCs and exclusions. The Trust Services Criteria evaluate controls; Description Criteria evaluate how the system is described. A well-designed control matrix does not complete the description automatically.

## Management assertion preparation scaffold

- Identify legal service organization, system, selected categories and date/period.
- Identify applicable Description Criteria and Trust Services Criteria.
- Support claims about description presentation and suitability of control design.
- For Type II, support claims about operating effectiveness throughout the specified period.
- Explain relevant carved-out providers and expected complementary controls consistently with the description.
- Confirm management responsibility, authority, known exceptions and material changes.

This is a preparation checklist, **not a signed assertion or licensed form**. Use the current practitioner-reviewed wording for an actual engagement. Do not sign a claim because automated configuration checks are green.

## PBC and walkthrough protocol

Give each request an ID, accountable custodian, scope/period, due date and restriction. Provide native exports and the validation workpaper. Walk through the actual process from trigger to completion, then show the failure path. For leavers, begin with HR events; for releases, begin with production deployment events; for backups, begin with the committed asset population. Track open auditor questions and clarify unsupported claims promptly.

Maintain a submitted-evidence log and freeze versions. If new evidence changes a prior response, preserve the old version and communicate the correction. Review access to restricted auditor portals and avoid public repository links for confidential source material.

## Supplier SOC report review workpaper

Record provider, service/region, report type, period, system boundary, opinion, relevant exceptions, carved-out dependencies and complementary controls. Compare covered period to your examination period. A bridge letter can add management context but cannot extend the CPA’s tested period. Map required user controls to named internal owners and actual test evidence. Determine whether gaps require additional work or a changed reliance conclusion with the practitioner.

Do not reproduce AWS's restricted SOC 2 report or claim that reviewing it makes the SaaS attested. Service coverage and report terms need verification for the specific account architecture.

## Report anatomy and follow-through

A SOC 2 report commonly includes the independent service auditor’s report, management assertion, system description and, for Type II, tests of controls and results. Additional organization-provided information may be presented separately with clearly identified assurance limits. Restricted use and distribution terms matter.

Distinguish individual test deviations from a modified opinion. Their effect depends on nature, cause, extent, compensating evidence and professional judgment. Discuss unresolved design/operation failures and subsequent events with management and the CPA rather than predicting the opinion from this project’s counts.

After issuance, retain the report and evidence securely, communicate appropriate scope/period limitations to customers, track complementary user responsibilities and independently verify corrective actions. Continue operating controls; report issuance does not freeze the system or eliminate ongoing obligations.
