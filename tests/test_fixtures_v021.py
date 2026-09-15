import json
import unittest
from datetime import datetime, timezone
from pathlib import Path
from convergence.contracts_v021 import *

ROOT=Path(__file__).resolve().parents[1]
FIX=ROOT/'fixtures/v0.2.1'
NOW=datetime(2026,9,15,tzinfo=timezone.utc)

def load(path): return json.loads((FIX/path).read_text(encoding='utf-8'))

class FixtureEvidenceTests(unittest.TestCase):
 def test_observation_golden(self): self.assertTrue(validate_enterprise_observation(load('enterprise-observation/business-fact.valid.json')).ok)
 def test_observation_cross_tenant_negative(self): self.assertFalse(validate_enterprise_observation(load('enterprise-observation/cross-tenant.invalid.json')).ok)
 def test_duplicate_delivery_semantics(self):
  x=load('enterprise-observation/duplicate-delivery.valid.json');self.assertEqual(x['first']['observationId'],x['retry']['observationId']);self.assertNotEqual(x['first']['deliveryId'],x['retry']['deliveryId'])
 def test_command_golden(self): self.assertTrue(validate_command_proposal(load('command-proposal/use-alternate-supplier.valid.json'),NOW).ok)
 def test_command_fake_auth_negative(self): self.assertFalse(validate_command_proposal(load('command-proposal/fake-authorization.invalid.json'),NOW).ok)
 def test_change_golden(self): self.assertTrue(validate_operational_change(load('operational-change/sop-change.valid.json')).ok)
 def test_change_stale_negative(self): self.assertFalse(validate_operational_change(load('operational-change/stale-base-version.invalid.json')).ok)
 def test_change_json_patch_negative(self): self.assertFalse(validate_operational_change(load('operational-change/json-patch.invalid.json')).ok)
 def test_simulation_golden(self): self.assertTrue(validate_enterprise_simulation(load('simulation/fifo-cost.valid.json')).ok)
 def test_simulation_actual_write_negative(self): self.assertFalse(validate_enterprise_simulation(load('simulation/actual-write.invalid.json')).ok)
 def test_experience_golden(self): self.assertTrue(validate_experience_proposal(load('experience-proposal/decision-experience.valid.json'),{'decision-panel':{'1.0.0'}}).ok)
 def test_experience_shared_core_negative(self): self.assertFalse(validate_experience_proposal(load('experience-proposal/shared-core-override.invalid.json'),{'decision-panel':{'1.0.0'}}).ok)
 def test_experience_unsupported_version_negative(self): self.assertFalse(validate_experience_proposal(load('experience-proposal/unsupported-capability-version.invalid.json'),{'decision-panel':{'1.0.0'}}).ok)
 def test_experience_missing_evidence_negative(self): self.assertFalse(validate_experience_proposal(load('experience-proposal/missing-evidence.invalid.json'),{'decision-panel':{'1.0.0'}}).ok)
 def test_experience_accessibility_negative(self): self.assertFalse(validate_experience_proposal(load('experience-proposal/accessibility.invalid.json'),{'decision-panel':{'1.0.0'}}).ok)
 def test_experience_business_authorization_negative(self): self.assertFalse(validate_experience_proposal(load('experience-proposal/business-authorization.invalid.json'),{'decision-panel':{'1.0.0'}}).ok)
 def test_action_golden(self): self.assertTrue(validate_action_request(load('action-request/approve-action.valid.json')).ok)
 def test_action_tampered_confirmation_negative(self): self.assertFalse(validate_action_request(load('action-request/tampered-confirmation.invalid.json')).ok)
 def test_shared_envelope_golden(self): self.assertTrue(validate_shared_envelope(load('shared-envelope/human-context.valid.json')).ok)
 def test_apm_causal_chain(self):
  x=load('integration/apm-causal-chain.valid.json');self.assertEqual(x['enterpriseId'],'APM');self.assertEqual(len({x['correlationId']}),1);self.assertEqual(x['chain'][4]['authorization'],'EVO_REEVALUATES')

if __name__=='__main__': unittest.main()
