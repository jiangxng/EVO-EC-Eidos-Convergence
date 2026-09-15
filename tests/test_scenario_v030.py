import unittest

from convergence.scenario_v030 import ApmLiveScenario


class FakeLiveEvo:
    def __init__(self): self.executed=False
    def observation(self):
        return {'contractVersion':'1.0.0','observationId':'obs-apm-so-0182-v7','deliveryId':'d1','enterpriseId':'APM','correlationId':'corr-apm-shortage-001','stateEtag':'state-7','definitionVersion':'3','facts':{
            'orderNo':'SO-20260918-0182','materialId':'SERVO-MODULE-CRITICAL','promiseDate':'2026-09-18','revenueAtRiskUsd':280000,
            'supplierA':{'id':'SUPPLIER-A','eta':'2026-09-20'},'supplierB':{'id':'SUPPLIER-B','eta':'2026-09-15','qualified':True,'costDeltaPercent':8.4},'marginAfterSupplierB':'acceptable'}}
    def admit_command_proposal(self, proposal):
        self.proposal=proposal
        return {'admitted':True,'executionStatus':'NOT_EXECUTED','authorization':'EVO_REEVALUATES_AT_EXECUTION'}
    def execute_action(self, action):
        self.executed=True; self.action=action
        return {'command':{'businessDataId':'bd-real-1'},'outcome':{'status':'EXECUTED','businessDataId':'bd-real-1'},'observation':{'observationId':'obs-apm-so-0182-supplier-v1'}}


class ScenarioV030Tests(unittest.TestCase):
    def test_prepare_does_not_execute_and_approve_closes_learning_loop(self):
        evo=FakeLiveEvo(); scenario=ApmLiveScenario(evo)
        prepared=scenario.prepare_decision()
        self.assertFalse(evo.executed)
        self.assertEqual(prepared['commandProposal']['proposedInput'],{'supplierId':'SUPPLIER-B'})
        self.assertEqual(prepared['experience']['presentedStateEtag'],'state-7')
        self.assertEqual(prepared['experience']['presentedDefinitionVersion'],'3')
        result=scenario.approve_and_execute(prepared)
        self.assertTrue(evo.executed)
        self.assertNotIn('authorization',result['actionRequest'])
        self.assertEqual(result['actionRequest']['presentedStateEtag'],'state-7')
        self.assertEqual(result['actionRequest']['presentedDefinitionVersion'],'3')
        self.assertEqual(result['execution']['outcome']['status'],'EXECUTED')
        self.assertGreater(len(result['learning']),0)


if __name__ == '__main__': unittest.main()
