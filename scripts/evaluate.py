#!/usr/bin/env python3
"""Evaluate narrow control assertions over reconciled, normalized exports.
No network calls, credentials, AWS mutations, or implied SOC 2 opinion.
"""
import argparse
import csv
import hashlib
import json
import math
import re
from datetime import datetime, timezone
from pathlib import Path

VERSION = '2.0.0'
SUPPORTED = {'DAT-01', 'IAM-04', 'CHG-01', 'RES-02'}


def digest_bytes(value):
    return hashlib.sha256(value).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()


def timestamp(value):
    if not isinstance(value, str):
        raise ValueError('Timestamp must be an ISO 8601 string with an offset')
    result = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if result.tzinfo is None or result.utcoffset() is None:
        raise ValueError('Timestamp requires a timezone offset')
    return result.astimezone(timezone.utc)


def number(value):
    if isinstance(value, bool) or not isinstance(value, (float, int)) or not math.isfinite(value) or value < 0:
        raise ValueError('Expected a finite nonnegative number, not a string or boolean')
    return value


def result(control, resource, state, reason):
    return dict(control_id=control, resource_id=resource, state=state, reason=reason)


def evaluate_item(expected, record, now, parameters, collected_at=None):
    control, resource = expected['control_id'], expected['resource_id']
    def outcome(state, reason):
        return result(control, resource, state, reason)
    if control not in SUPPORTED:
        return outcome('UNKNOWN', 'No executable assertion is implemented for this control')
    if expected.get('applicable') is False:
        if expected.get('exclusion_reason') and expected.get('approved_by'):
            return outcome('NOT_APPLICABLE', expected['exclusion_reason'])
        return outcome('UNKNOWN', 'Exclusion lacks a reason or approving owner')
    if expected.get('applicable') is not True:
        return outcome('UNKNOWN', 'Applicability is missing or malformed')
    if record is None:
        return outcome('UNKNOWN', 'Expected population item has no source record')
    if record.get('collector_error'):
        return outcome('UNKNOWN', 'Source collection failed: ' + str(record['collector_error']))
    try:
        observed = timestamp(record['observed_at'])
        if collected_at is not None and observed > collected_at:
            return outcome('UNKNOWN', 'Observation is later than collection')
        age = (now - observed).total_seconds()
        if age < 0 or age > number(parameters['freshness_hours']) * 3600:
            return outcome('UNKNOWN', 'Observation is stale or in the future')
        if control == 'DAT-01':
            states = {'COMPLIANT': 'PASS', 'NON_COMPLIANT': 'FAIL'}
            native = record.get('compliance')
            if native not in states:
                return outcome('UNKNOWN', 'No conclusive applicable Config public-read evaluation')
            return outcome(states[native], 'Narrow assertion: Config public-read rule returned ' + native)
        if control == 'IAM-04':
            ended = timestamp(record['terminated_at'])
            removed_value = record.get('all_paths_removed_at')
            limit = number(parameters['leaver_sla_hours']) * 3600
            if ended > now:
                raise ValueError('Termination is future-dated')
            if record.get('access_still_active') is True and (now - ended).total_seconds() > limit:
                return outcome('FAIL', 'Known active access after removal deadline')
            if record.get('access_still_active') is not None and type(record.get('access_still_active')) is not bool:
                raise ValueError('access_still_active must be a boolean')
            if removed_value is None:
                return outcome('UNKNOWN', 'Final effective-access removal has not been established')
            removed = timestamp(removed_value)
            if removed < ended or removed > observed:
                raise ValueError('Removal timestamp is impossible')
            hours = (removed - ended).total_seconds() / 3600
            if hours > limit / 3600:
                return outcome('FAIL', f'All-path removal took {hours:g} hours; limit {limit/3600:g}')
            if record.get('access_still_active') is True:
                return outcome('FAIL', 'Access remains active despite a recorded removal timestamp')
            if record.get('access_still_active') is not False or record.get('paths_reconciled') is not True:
                return outcome('UNKNOWN', 'Access-path completeness or inactive state was not verified')
            return outcome('PASS', f'Final removal verified in {hours:g} hours')
        if control == 'CHG-01':
            deployed = timestamp(record['deployed_at'])
            if deployed > observed:
                raise ValueError('Deployment is later than its observation')
            # Demonstrated violations survive missing inputs in a different condition.
            if record.get('deployer') and record.get('approver') == record.get('deployer'):
                return outcome('FAIL', 'Deployer approved their own change')
            if record.get('deployed_sha') and record.get('approved_sha') and record['deployed_sha'] != record['approved_sha']:
                return outcome('FAIL', 'Approved SHA differs from deployed SHA')
            if record.get('checks_passed') is False or record.get('approver_authorized') is False:
                return outcome('FAIL', 'Required checks or reviewer authorization failed')
            approved_value = record.get('approved_at')
            if approved_value:
                approved = timestamp(approved_value)
                if approved > deployed:
                    return outcome('FAIL', 'Approval happened after deployment')
            else:
                return outcome('UNKNOWN', 'Approval timestamp is missing')
            for field in ('deployer', 'approver', 'deployed_sha', 'approved_sha'):
                if not isinstance(record.get(field), str) or not record[field].strip():
                    raise ValueError('Missing or malformed ' + field)
            if any(not re.fullmatch(r'[0-9a-fA-F]{40}|[0-9a-fA-F]{64}', record[field]) for field in ('deployed_sha', 'approved_sha')):
                raise ValueError('Commit IDs must be full hexadecimal hashes')
            if record.get('checks_passed') is not True or record.get('approver_authorized') is not True:
                return outcome('UNKNOWN', 'Successful checks or reviewer authorization is not verified')
            return outcome('PASS', 'Exact deployed SHA independently approved before deployment; required checks passed')
        if control == 'RES-02':
            start = timestamp(record['disruption_at'])
            recovered = timestamp(record['validated_recovery_at'])
            data = timestamp(record['recovered_data_at'])
            if recovered < start or recovered > observed or data > start:
                raise ValueError('Recovery or data timeline is impossible')
            hours = (recovered - start).total_seconds() / 3600
            lag = (start - data).total_seconds() / 3600
            if hours > number(parameters['rto_hours']) or lag > number(parameters['rpo_hours']):
                return outcome('FAIL', f'RTO {hours:g} hours / RPO {lag:g} hours exceed an approved limit')
            if record.get('application_validated') is False:
                return outcome('FAIL', 'Application/data validation failed after restore')
            if record.get('application_validated') is not True:
                return outcome('UNKNOWN', 'Application/data validation evidence is missing')
            return outcome('PASS', f'Validated recovery: RTO {hours:g} hours / RPO {lag:g} hours')
    except (KeyError, TypeError, ValueError, OverflowError) as error:
        return outcome('UNKNOWN', 'Invalid or incomplete evidence: ' + str(error))


def evaluate(scope, snapshot, as_of):
    now = timestamp(as_of)
    params = scope.get('parameters', {})
    for key in ('freshness_hours', 'leaver_sla_hours', 'rto_hours', 'rpo_hours'):
        number(params[key])
    expected = scope['expected']
    keys = [(item['control_id'], item['resource_id']) for item in expected]
    if len(set(keys)) != len(keys):
        raise ValueError('Duplicate identities in expected population')
    rows = snapshot['records']
    indexed, duplicates = {}, set()
    for row in rows:
        key = (row.get('control_id'), row.get('resource_id'))
        if key in indexed:
            duplicates.add(key)
        indexed[key] = row
    extras = sorted(set(indexed) - set(keys), key=str)
    header_error = None
    try:
        collected = timestamp(snapshot['collected_at'])
        if collected > now or (now-collected).total_seconds() > number(params['freshness_hours'])*3600:
            header_error = 'Collection timestamp is stale or future-dated'
        elif snapshot.get('scope_sha256') != digest_bytes(canonical(scope)):
            header_error = 'Snapshot does not match the approved scope hash'
        elif any(snapshot.get(field) != scope[field] for field in ('account_id', 'region') if field in scope):
            header_error = 'Snapshot account/region does not match approved scope'
        elif any(row.get(field) != scope[field] for row in rows for field in ('account_id', 'region') if field in scope):
            header_error = 'Source record account/region differs from approved scope'
        elif extras or duplicates:
            header_error = 'Extract has unexpected or duplicate population identities'
        elif snapshot.get('complete') is not True:
            header_error = 'Extract completeness was not established'
    except (KeyError, TypeError, ValueError) as error:
        header_error = 'Invalid collection metadata: ' + str(error)
    results = [result(item['control_id'], item['resource_id'], 'UNKNOWN', header_error) if header_error
               else evaluate_item(item, indexed.get(key), now, params, collected) for item, key in zip(expected, keys)]
    counts = {state: sum(r['state'] == state for r in results) for state in ('PASS', 'FAIL', 'UNKNOWN', 'NOT_APPLICABLE')}
    applicable = len(results) - counts['NOT_APPLICABLE']
    return dict(schema_version=VERSION, mode=snapshot.get('mode','unspecified'), as_of=as_of,
                test_version=VERSION, scope_sha256=digest_bytes(canonical(scope)),
                expected_count=len(expected), observed_count=len(rows), unexpected=[list(k) for k in extras],
                duplicate_identities=[list(k) for k in sorted(duplicates,key=str)], counts=counts,
                pass_rate=round(100*counts['PASS']/applicable,1) if applicable else None,
                denominator_note='PASS / (PASS + FAIL + UNKNOWN); approved exclusions shown separately. Narrow assertions only.',
                results=results)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scope', default='data/demo-scope.json')
    parser.add_argument('--input', default='data/demo-snapshot.json')
    parser.add_argument('--as-of', help='Explicit UTC evaluation time; use fixture time for the reproducible demo')
    parser.add_argument('--out', default='evidence/local-run')
    parser.add_argument('--strict', action='store_true', help='Exit 2 when FAIL or UNKNOWN exists (artifact creation still completes)')
    args = parser.parse_args()
    scope_path, input_path = Path(args.scope), Path(args.input)
    scope, snapshot = json.loads(scope_path.read_text()), json.loads(input_path.read_text())
    as_of = args.as_of or datetime.now(timezone.utc).isoformat()
    report = evaluate(scope,snapshot,as_of)
    report['logic_sha256'] = digest_bytes(Path(__file__).read_bytes())
    report['input_sha256'] = digest_bytes(input_path.read_bytes())
    report['scope_file_sha256'] = digest_bytes(scope_path.read_bytes())
    output = Path(args.out)
    output.mkdir(parents=True,exist_ok=False)
    (output/'results.json').write_text(json.dumps(report,indent=2)+'\n')
    (output/'input.json').write_bytes(input_path.read_bytes())
    (output/'scope.json').write_bytes(scope_path.read_bytes())
    (output/'logic.py').write_bytes(Path(__file__).read_bytes())
    with (output/'results.csv').open('w',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=['control_id','resource_id','state','reason'])
        writer.writeheader();writer.writerows(report['results'])
    (output/'manifest.json').write_text(json.dumps({p.name:digest_bytes(p.read_bytes()) for p in sorted(output.iterdir()) if p.is_file()},indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('expected_count','observed_count','counts','pass_rate')},indent=2))
    if args.strict and (report['counts']['FAIL'] or report['counts']['UNKNOWN']):
        raise SystemExit(2)

if __name__ == '__main__':
    main()
