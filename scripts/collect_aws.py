#!/usr/bin/env python3
"""Read-only AWS Config collection for a single approved account/region bucket list.
This supports DAT-01's public-read assertion, not the whole SOC 2 control catalog.
"""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from evaluate import canonical, digest_bytes


def iso(value):
    if isinstance(value, datetime):
        if value.tzinfo is None:
            raise ValueError('AWS timestamp lacks timezone')
        return value.astimezone(timezone.utc).isoformat()
    return value


def get_all(client, operation, response_key, **request):
    """Retain every page; reject repeated continuation tokens."""
    rows, pages, seen = [], [], set()
    while True:
        page = getattr(client, operation)(**request)
        pages.append(page); rows.extend(page.get(response_key, []))
        token = page.get('NextToken')
        if not token:
            return rows, pages
        if token in seen:
            raise ValueError('Repeated pagination token; completeness cannot be established')
        seen.add(token); request['NextToken'] = token


def collect(session, scope):
    if scope.get('source_identifier') != 'S3_BUCKET_PUBLIC_READ_PROHIBITED':
        raise ValueError('Only the reviewed public-read rule is supported')
    expected = scope.get('expected', [])
    if not expected or any(x.get('control_id') != 'DAT-01' or x.get('resource_type') != 'AWS::S3::Bucket' for x in expected):
        raise ValueError('Scope must enumerate DAT-01 AWS::S3::Bucket resources')
    if len({x['resource_id'] for x in expected}) != len(expected):
        raise ValueError('Duplicate expected resource IDs')
    caller = session.client('sts').get_caller_identity()
    if caller.get('Account') != scope['account_id']:
        raise ValueError('Caller account does not match approved scope')
    config = session.client('config',region_name=scope['region'])
    raw = {'caller_identity':caller, 'rule':None, 'recorder_status':None, 'evaluations':{}}
    readiness_error = None
    try:
        rules = config.describe_config_rules(ConfigRuleNames=[scope['config_rule_name']])
        raw['rule'] = rules
        defined = rules.get('ConfigRules',[])
        if len(defined) != 1 or defined[0].get('ConfigRuleState') != 'ACTIVE' or defined[0].get('Source',{}).get('Owner') != 'AWS' or defined[0].get('Source',{}).get('SourceIdentifier') != scope['source_identifier']:
            raise ValueError('Rule source/state differs from reviewed definition')
        status = config.describe_configuration_recorder_status()
        raw['recorder_status'] = status
        if not any(x.get('recording') is True and x.get('lastStatus') == 'SUCCESS' for x in status.get('ConfigurationRecordersStatus',[])):
            raise ValueError('No healthy recording Config recorder')
    except Exception as error:
        readiness_error = type(error).__name__ + ': ' + str(error)
    records=[]
    for item in expected:
        row=dict(control_id=item['control_id'],resource_id=item['resource_id'],account_id=scope['account_id'],region=scope['region'])
        if readiness_error:
            row['collector_error']=readiness_error
        else:
            try:
                # Deliberately no ComplianceTypes filter: unknown native states matter.
                evaluations,pages=get_all(config,'get_compliance_details_by_resource','EvaluationResults',ResourceType=item['resource_type'],ResourceId=item['resource_id'])
                raw['evaluations'][item['resource_id']]=pages
                matching=[x for x in evaluations if x.get('EvaluationResultIdentifier',{}).get('EvaluationResultQualifier',{}).get('ConfigRuleName')==scope['config_rule_name']]
                if len(matching)!=1:
                    raise ValueError('Expected exactly one result for the approved rule')
                native=matching[0]
                qualifier=native['EvaluationResultIdentifier']['EvaluationResultQualifier']
                if qualifier.get('ResourceId') != item['resource_id'] or qualifier.get('ResourceType') != item['resource_type'] or qualifier.get('EvaluationMode','DETECTIVE') != 'DETECTIVE':
                    raise ValueError('Evaluation identity/mode differs from expected resource')
                row.update(compliance=native.get('ComplianceType'), observed_at=iso(native['EvaluationResultIdentifier']['OrderingTimestamp']),evaluated_at=iso(native.get('ConfigRuleInvokedTime')),recorded_at=iso(native.get('ResultRecordedTime')),annotation=native.get('Annotation'))
            except Exception as error:
                row['collector_error']=type(error).__name__ + ': ' + str(error)
        records.append(row)
    now=datetime.now(timezone.utc).isoformat()
    return dict(schema_version='2.0.0',mode='live-read-only',collected_at=now,scope_sha256=digest_bytes(canonical(scope)),complete=True,account_id=scope['account_id'],region=scope['region'],records=records),raw


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scope',required=True)
    parser.add_argument('--profile',required=True)
    parser.add_argument('--out',required=True,help='New directory; existing directories are never overwritten')
    args=parser.parse_args()
    try:
        import boto3
        from botocore.config import Config
    except ImportError:
        parser.exit(1,'Install optional live dependencies: python3 -m pip install -r requirements-live.txt\n')
    scope=json.loads(Path(args.scope).read_text())
    if 'REPLACE' in json.dumps(scope):
        parser.exit(1,'Review the example scope and replace all placeholder values\n')
    # Bounded standard retries; failed reads become explicit unknown evidence.
    base=boto3.Session(profile_name=args.profile,region_name=scope['region'])
    class RetryingSession:
        def client(self,name,**kwargs):
            return base.client(name,config=Config(retries={'mode':'standard','max_attempts':5}),**kwargs)
    snapshot,raw=collect(RetryingSession(),scope)
    import botocore
    snapshot['sdk_versions']={'boto3':boto3.__version__,'botocore':botocore.__version__}
    output=Path(args.out);output.mkdir(parents=True,exist_ok=False)
    (output/'snapshot.json').write_text(json.dumps(snapshot,indent=2,default=iso)+'\n')
    (output/'raw.json').write_text(json.dumps(raw,indent=2,default=iso)+'\n')
    (output/'scope.json').write_bytes(Path(args.scope).read_bytes())
    (output/'collector.py').write_bytes(Path(__file__).read_bytes())
    (output/'manifest.json').write_text(json.dumps({p.name:digest_bytes(p.read_bytes()) for p in sorted(output.iterdir()) if p.is_file()},indent=2)+'\n')
    print(f'Collected {len(snapshot["records"])} expected resources. Evaluate snapshot.json; review raw.json in restricted custody.')

if __name__=='__main__':
    main()
