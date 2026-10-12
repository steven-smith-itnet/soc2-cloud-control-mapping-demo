import copy
import json
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from evaluate import evaluate, evaluate_item, canonical, digest_bytes
from collect_aws import collect, get_all
from verify_evidence import verify


class ControlTests(unittest.TestCase):
    def setUp(self):
        self.scope=json.loads((ROOT/'data/demo-scope.json').read_text())
        self.snapshot=json.loads((ROOT/'data/demo-snapshot.json').read_text())
        self.now='2026-09-30T15:00:00Z'
    def run_report(self):
        return evaluate(self.scope,self.snapshot,self.now)
    def row(self,control,resource):
        return next(x for x in self.snapshot['records'] if x['control_id']==control and x['resource_id']==resource)
    def state(self,resource):
        return next(x['state'] for x in self.run_report()['results'] if x['resource_id']==resource)
    def test_reproducible_baseline_and_visible_denominator(self):
        r=self.run_report()
        self.assertEqual(r['counts'],dict(PASS=5,FAIL=8,UNKNOWN=7,NOT_APPLICABLE=1))
        self.assertEqual(r['expected_count'],21);self.assertEqual(r['observed_count'],20);self.assertEqual(r['pass_rate'],25.0)
    def test_missing_expected_resource_never_passes(self):
        self.assertEqual(self.state('customer-new'),'UNKNOWN')
    def test_stale_native_compliance_never_passes(self):
        self.assertEqual(self.state('customer-archive'),'UNKNOWN')
    def test_insufficient_data_and_native_na_do_not_pass(self):
        for state in ('INSUFFICIENT_DATA','NOT_APPLICABLE',None,'NEW_STATE'):
            self.row('DAT-01','customer-primary')['compliance']=state
            self.assertEqual(self.state('customer-primary'),'UNKNOWN')
    def test_exclusion_needs_approved_reason(self):
        self.scope['expected'][-1]['applicable']=False
        self.snapshot['scope_sha256']=digest_bytes(canonical(self.scope))
        self.assertEqual(self.state('exercise-04'),'UNKNOWN')
    def test_self_approval_and_wrong_sha_are_detected(self):
        self.assertEqual(self.state('deploy-02'),'FAIL');self.assertEqual(self.state('deploy-03'),'FAIL')
    def test_failure_preserved_with_other_missing_field(self):
        self.row('CHG-01','deploy-02')['approved_at']=None
        self.assertEqual(self.state('deploy-02'),'FAIL')
    def test_string_and_integer_booleans_never_pass(self):
        for val in ('true',1,None):
            self.row('CHG-01','deploy-01')['checks_passed']=val
            self.assertEqual(self.state('deploy-01'),'UNKNOWN')
    def test_timezone_is_required(self):
        self.row('IAM-04','leaver-01')['terminated_at']='2026-09-29T10:00:00'
        self.assertEqual(self.state('leaver-01'),'UNKNOWN')
    def test_rollback_timestamps_are_unknown(self):
        self.row('IAM-04','leaver-01')['all_paths_removed_at']='2026-09-29T09:00:00Z'
        self.assertEqual(self.state('leaver-01'),'UNKNOWN')
    def test_access_path_reconciliation_required(self):
        self.row('IAM-04','leaver-01')['paths_reconciled']=False
        self.assertEqual(self.state('leaver-01'),'UNKNOWN')
    def test_sla_boundary_and_late_active_access(self):
        self.assertEqual(self.state('leaver-05'),'PASS');self.assertEqual(self.state('leaver-03'),'FAIL')
    def test_rto_and_rpo_independent_failures(self):
        self.assertEqual(self.state('exercise-02'),'FAIL');self.assertEqual(self.state('exercise-03'),'FAIL')
    def test_validation_is_required(self):
        self.assertEqual(self.state('exercise-04'),'UNKNOWN')
    def test_duplicate_and_unexpected_records_reject_reconciliation(self):
        self.snapshot['records'].append(copy.deepcopy(self.snapshot['records'][0]))
        self.assertEqual(self.run_report()['counts']['UNKNOWN'],21)
        self.snapshot['records'][-1]['resource_id']='unapproved-bucket'
        self.assertEqual(self.run_report()['counts']['UNKNOWN'],21)
    def test_scope_hash_change_is_detected(self):
        self.scope['parameters']['rto_hours']=8
        self.assertEqual(self.run_report()['counts']['UNKNOWN'],21)
    def test_stale_collection_and_future_observation(self):
        self.snapshot['collected_at']='2026-09-27T15:00:00Z'
        self.assertEqual(self.run_report()['counts']['UNKNOWN'],21)
        self.snapshot['collected_at']=self.now
        self.row('DAT-01','customer-primary')['observed_at']='2026-10-01T15:00:00Z'
        self.assertEqual(self.state('customer-primary'),'UNKNOWN')
    def test_invalid_threshold_fails_validation(self):
        self.scope['parameters']['rto_hours']='4'
        with self.assertRaises(ValueError):self.run_report()
    def test_source_observation_cannot_follow_collection(self):
        self.snapshot['collected_at']='2026-09-30T13:00:00Z'
        self.assertEqual(self.state('customer-primary'),'UNKNOWN')
    def test_event_cannot_follow_source_observation(self):
        self.row('CHG-01','deploy-01')['observed_at']='2026-09-29T14:00:00Z'
        self.now='2026-09-30T13:00:00Z'
        self.snapshot['collected_at']=self.now
        self.assertEqual(self.state('deploy-01'),'UNKNOWN')
    def test_short_commit_id_is_not_immutable_proof(self):
        self.row('CHG-01','deploy-01')['deployed_sha']='a123'
        self.row('CHG-01','deploy-01')['approved_sha']='a123'
        self.assertEqual(self.state('deploy-01'),'UNKNOWN')
    def test_live_context_checked_on_run_and_records(self):
        self.scope.update(account_id='444444444444',region='us-east-1')
        self.snapshot['scope_sha256']=digest_bytes(canonical(self.scope))
        self.snapshot.update(account_id='999999999999',region='us-east-1')
        self.assertEqual(self.run_report()['counts']['UNKNOWN'],21)
        self.snapshot['account_id']='444444444444'
        self.assertEqual(self.run_report()['counts']['UNKNOWN'],21)
        for row in self.snapshot['records']:row.update(account_id='444444444444',region='us-east-1')
        self.assertEqual(self.run_report()['counts']['PASS'],5)
    def test_manifest_detects_tamper_and_unlisted_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp);(folder/'data.json').write_text('{}')
            (folder/'manifest.json').write_text(json.dumps({'data.json':digest_bytes(b'{}')}))
            self.assertEqual(verify(folder),1)
            (folder/'data.json').write_text('{"changed":true}')
            with self.assertRaises(ValueError):verify(folder)
            (folder/'data.json').write_text('{}');(folder/'extra.txt').write_text('x')
            with self.assertRaises(ValueError):verify(folder)


class FakeConfig:
    def __init__(self,broken=False):self.requests=[];self.broken=broken
    def describe_config_rules(self,**request):return {'ConfigRules':[{'ConfigRuleState':'ACTIVE','Source':{'Owner':'AWS','SourceIdentifier':'S3_BUCKET_PUBLIC_READ_PROHIBITED'}}]}
    def describe_configuration_recorder_status(self):return {'ConfigurationRecordersStatus':[{'recording':True,'lastStatus':'SUCCESS'}]}
    def get_compliance_details_by_resource(self,**request):
        self.requests.append(request)
        if self.broken:raise PermissionError('AccessDenied')
        if 'NextToken' not in request:return {'EvaluationResults':[], 'NextToken':'second-page'}
        return {'EvaluationResults':[{'ComplianceType':'COMPLIANT','EvaluationResultIdentifier':{'OrderingTimestamp':datetime(2026,9,30,14,tzinfo=timezone.utc),'EvaluationResultQualifier':{'ConfigRuleName':'soc2-public-read','ResourceId':'customer-primary','ResourceType':'AWS::S3::Bucket'}}}]}
class FakeSession:
    def __init__(self,client,account='444444444444'):self.config=client;self.account=account
    def client(self,name,**kwargs):return self if name=='sts' else self.config
    def get_caller_identity(self):return {'Account':self.account,'Arn':'arn:aws:iam::444444444444:role/collector'}
class CollectorTests(unittest.TestCase):
    def setUp(self):
        self.scope=json.loads((ROOT/'data/aws-scope.example.json').read_text())
        self.scope['expected'][0]['resource_id']='customer-primary'
    def test_every_page_retained_without_compliance_filter(self):
        client=FakeConfig();snapshot,raw=collect(FakeSession(client),self.scope)
        self.assertEqual(snapshot['records'][0]['compliance'],'COMPLIANT')
        self.assertEqual(len(raw['evaluations']['customer-primary']),2)
        self.assertTrue(all('ComplianceTypes' not in r for r in client.requests))
    def test_denied_api_becomes_explicit_collection_error(self):
        snapshot,_=collect(FakeSession(FakeConfig(True)),self.scope)
        self.assertIn('AccessDenied',snapshot['records'][0]['collector_error'])
    def test_wrong_account_is_rejected(self):
        with self.assertRaises(ValueError):collect(FakeSession(FakeConfig(),'999999999999'),self.scope)
    def test_unhealthy_recorder_invalidates_collection(self):
        client=FakeConfig()
        client.describe_configuration_recorder_status=lambda:{'ConfigurationRecordersStatus':[{'recording':False,'lastStatus':'FAILURE'}]}
        snapshot,_=collect(FakeSession(client),self.scope)
        self.assertIn('No healthy',snapshot['records'][0]['collector_error'])
    def test_mismatched_rule_definition_invalidates_collection(self):
        client=FakeConfig()
        client.describe_config_rules=lambda **kwargs:{'ConfigRules':[{'ConfigRuleState':'ACTIVE','Source':{'Owner':'CUSTOM_LAMBDA','SourceIdentifier':'arn:example'}}]}
        snapshot,_=collect(FakeSession(client),self.scope)
        self.assertIn('differs',snapshot['records'][0]['collector_error'])
    def test_repeated_token_rejected(self):
        class Repeats:
            def read(self,**kwargs):return {'Items':[],'NextToken':'same'}
        with self.assertRaises(ValueError):get_all(Repeats(),'read','Items')

if __name__=='__main__':unittest.main()
