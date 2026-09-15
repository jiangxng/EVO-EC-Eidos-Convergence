import unittest
from copy import deepcopy
from datetime import datetime, timezone
from convergence.contracts_v021 import *

NOW=datetime(2026,9,15,tzinfo=timezone.utc)

OBS={"contractVersion":"1.0.0","observationId":"obs-1","deliveryId":"del-1","observationType":"BUSINESS_FACT","enterpriseId":"APM","effectiveAt":"2026-09-14T08:00:00Z","observedAt":"2026-09-15T08:00:00Z","publishedAt":"2026-09-15T08:01:00Z","correlationId":"corr-1","source":{"system":"EVO","objectType":"sales-order","objectId":"SO-20260918-0182","objectVersion":"7","enterpriseId":"APM"},"payload":{"status":"APPROVED"},"provenance":{"producer":"EVO"}}
CMD={"contractVersion":"1.0.0","proposalId":"prop-1","enterpriseId":"APM","createdAt":"2026-09-15T08:02:00Z","expiresAt":"2026-09-16T08:02:00Z","basis":["obs-1"],"commandContractId":"evo.command","commandContractVersion":"1.0.0","commandCode":"procurement.use-alternate-supplier","inputSchemaVersion":"1","proposedInput":{"supplierId":"SUPPLIER-B"},"evidence":["obs-1"],"rationale":"protect promise","correlationId":"corr-1","commandIdempotencyKey":"cmd-idem-1"}
CHANGE={"contractVersion":"1.0.0","proposalId":"chg-1","enterpriseId":"APM","targetDefinitionType":"SOP","targetDefinitionId":"procurement-shortage","baseVersion":"3","changeIntent":"prefer qualified alternate under shortage","operations":[{"op":"SET_FIELD","field":"alternatePolicy","value":"QUALIFIED_FASTEST"}],"evidence":["obs-1"],"compatibility":{"classification":"BACKWARD_COMPATIBLE"}}
SIM={"contractVersion":"0.1.0","simulationId":"sim-1","scenarioId":"fifo-cost","enterpriseId":"APM","actualSnapshotRef":"snapshot-77","definitionPins":{"inventory":"4"},"rulePins":{"posting":"9"},"valuationPins":{"cost":"FIFO-v2"},"metricPins":{"margin":"3"},"assumptions":{"qty":10},"calculators":["inventory","cost"],"namespace":"HYPOTHETICAL"}
EXP={"contractVersion":"1.0.0","proposalId":"xp-1","producedAt":"2026-09-15T08:03:00Z","experience":{"experienceId":"supplier-risk-decision","regions":[{"id":"decision","capabilityId":"decision-panel","capabilityVersion":"1.0.0","stability":"shared-stable","mandatoryEvidence":True,"evidenceRefs":["obs-1"],"accessibility":{"required":True,"label":"Supplier risk decision"}}]},"context":{"enterpriseId":"APM","correlationId":"corr-1"},"fallback":{"mode":"standard"}}
ACTION={"contractVersion":"1.0.0","actionRequestId":"ar-1","experienceInstanceId":"xi-1","experienceContractVersion":"1.0.0","capabilityId":"decision-panel","capabilityVersion":"1.0.0","actionSemantic":"APPROVE_RECOMMENDATION","targetRef":{"host":"enterprise-runtime","resourceType":"supplier-decision","resourceId":"SO-20260918-0182"},"interactionContext":{"surface":"desktop"},"submittedValues":{"supplierId":"SUPPLIER-B"},"confirmationEvidence":{"confirmed":True,"method":"explicit-click"},"actorContextRef":"actor-context-1","correlationId":"corr-1","occurredAt":"2026-09-15T08:04:00Z","presentedStateEtag":"state-7","presentedDefinitionVersion":"3"}
ENV={"profileVersion":"0.1.0","enterpriseId":"APM","identity":{"actorType":"HUMAN","actorId":"buyer-1","delegationRef":"deleg-1"},"trace":{"correlationId":"corr-1","causationId":"obs-1"},"capability":{"contractId":"eidos.action-request","supportedVersions":["1.0.0","0.1.0"]}}

class V021ContractTests(unittest.TestCase):
 def test_shared_envelope_valid(self): self.assertTrue(validate_shared_envelope(ENV).ok)
 def test_shared_envelope_fake_auth_invalid(self):
  x=deepcopy(ENV);x["identity"]["authorized"]=True;self.assertFalse(validate_shared_envelope(x).ok)
 def test_observation_valid_backdated(self): self.assertTrue(validate_enterprise_observation(OBS).ok)
 def test_observation_delivery_identity_distinct(self):
  x=deepcopy(OBS);x["deliveryId"]=x["observationId"];self.assertFalse(validate_enterprise_observation(x).ok)
 def test_observation_cross_tenant_invalid(self):
  x=deepcopy(OBS);x["source"]["enterpriseId"]="OTHER";self.assertFalse(validate_enterprise_observation(x).ok)
 def test_command_valid(self): self.assertTrue(validate_command_proposal(CMD,NOW).ok)
 def test_command_expired_invalid(self):
  x=deepcopy(CMD);x["expiresAt"]="2026-09-14T00:00:00Z";self.assertFalse(validate_command_proposal(x,NOW).ok)
 def test_command_fake_authorization_invalid(self):
  x=deepcopy(CMD);x["authorizationResult"]="ALLOW";self.assertFalse(validate_command_proposal(x,NOW).ok)
 def test_command_identity_separation(self):
  x=deepcopy(CMD);x["commandIdempotencyKey"]=x["proposalId"];self.assertFalse(validate_command_proposal(x,NOW).ok)
 def test_operational_change_valid(self): self.assertTrue(validate_operational_change(CHANGE).ok)
 def test_operational_change_requires_base(self):
  x=deepcopy(CHANGE);x["baseVersion"]="";self.assertFalse(validate_operational_change(x).ok)
 def test_operational_change_rejects_json_patch(self):
  x=deepcopy(CHANGE);x["operations"]=[{"op":"replace","path":"/rules/0","value":1}];self.assertFalse(validate_operational_change(x).ok)
 def test_simulation_valid(self): self.assertTrue(validate_enterprise_simulation(SIM).ok)
 def test_simulation_actual_write_invalid(self):
  x=deepcopy(SIM);x["namespace"]="ACTUAL";x["writeActual"]=True;self.assertFalse(validate_enterprise_simulation(x).ok)
 def test_simulation_deterministic_digest(self): self.assertEqual(simulation_digest(SIM),simulation_digest(deepcopy(SIM)))
 def test_experience_valid(self): self.assertTrue(validate_experience_proposal(EXP,{"decision-panel":{"1.0.0"}}).ok)
 def test_experience_unknown_capability_invalid(self): self.assertFalse(validate_experience_proposal(EXP,{"decision-panel":{"2.0.0"}}).ok)
 def test_experience_missing_evidence_invalid(self):
  x=deepcopy(EXP);x["experience"]["regions"][0]["evidenceRefs"]=[];self.assertFalse(validate_experience_proposal(x,{"decision-panel":{"1.0.0"}}).ok)
 def test_experience_shared_core_override_invalid(self):
  x=deepcopy(EXP);x["experience"]["regions"][0]["personalization"]={"overrideSharedCore":True};self.assertFalse(validate_experience_proposal(x,{"decision-panel":{"1.0.0"}}).ok)
 def test_action_host_neutral_valid(self): self.assertTrue(validate_action_request(ACTION).ok)
 def test_action_fake_authorization_invalid(self):
  x=deepcopy(ACTION);x["confirmationEvidence"]["authorized"]=True;self.assertFalse(validate_action_request(x).ok)
 def test_evo_mapping_reauthorizes(self):
  command={"commandCode":"procurement.use-alternate-supplier","enterpriseId":"APM","actor":{"contextRef":"actor-context-1"},"idempotencyKey":"cmd-1","correlationId":"corr-1","input":{"supplierId":"SUPPLIER-B"}}
  self.assertTrue(validate_evo_action_mapping(ACTION,command).ok)
  command["authorized"]=True;self.assertFalse(validate_evo_action_mapping(ACTION,command).ok)
 def test_causal_chain_keeps_correlation(self):
  self.assertEqual(OBS["correlationId"],CMD["correlationId"]);self.assertEqual(CMD["correlationId"],EXP["context"]["correlationId"]);self.assertEqual(EXP["context"]["correlationId"],ACTION["correlationId"])

if __name__=="__main__": unittest.main()
