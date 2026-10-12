-- Investigative templates, not assertions of SOC 2 operating effectiveness.
-- Replace database/table, dates, account filters and partition predicates.
-- Schema: Athena's documented CloudTrail table, including useridentity and
-- requestparameters as JSON strings. Event history is not this S3 log table.
-- Verify event selectors and delivery BEFORE interpreting zero rows.
SELECT eventtime, recipientaccountid, awsregion, eventsource, eventname,
       useridentity.arn, errorcode
FROM cloudtrail_logs
WHERE eventtime >= '2026-07-01T00:00:00Z'
  AND eventtime < '2026-10-01T00:00:00Z'
  AND recipientaccountid IN ('444444444444', '666666666666')
  AND useridentity.type = 'Root'
ORDER BY eventtime;

-- Changes to logging/guardrails: correlate with approvals, then verify state.
SELECT eventtime, recipientaccountid, useridentity.arn, eventname,
       requestparameters, errorcode
FROM cloudtrail_logs
WHERE eventtime >= '2026-07-01T00:00:00Z'
  AND eventtime < '2026-10-01T00:00:00Z'
  AND eventname IN ('StopLogging', 'DeleteTrail', 'PutEventSelectors',
                    'DeleteBucketPolicy', 'PutBucketPolicy',
                    'DeletePublicAccessBlock', 'PutPublicAccessBlock')
ORDER BY eventtime;

-- A canary object access is only visible when the relevant S3 data events
-- were selected and delivered. Use a unique non-sensitive canary key.
SELECT eventtime, recipientaccountid, useridentity.arn, eventname, errorcode
FROM cloudtrail_logs
WHERE eventtime >= '2026-09-30T00:00:00Z'
  AND eventtime < '2026-10-01T00:00:00Z'
  AND eventsource = 's3.amazonaws.com'
  AND json_extract_scalar(requestparameters, '$.key') = 'canary/audit-path-check';
-- No "non-MFA" conclusion based on absent MFA fields in federated events.
