from __future__ import annotations

import json

from .evo_live_adapter import LiveEvoAdapter
from .scenario_v030 import ApmLiveScenario


def main() -> None:
    scenario = ApmLiveScenario(LiveEvoAdapter(base_url='http://127.0.0.1:3000'))
    prepared = scenario.prepare_decision()
    before = prepared['observation']
    assert before['observationId'] == 'obs-apm-so-0182-v7'
    assert before['facts']['shortageRisk'] is True
    assert prepared['admission']['executionStatus'] == 'NOT_EXECUTED'
    assert prepared['experience']['presentedStateEtag'] == before['stateEtag']
    result = scenario.approve_and_execute(prepared)
    action = result['actionRequest']
    execution = result['execution']
    after = execution['observation']
    assert 'authorization' not in action and 'authorized' not in action
    assert action['presentedStateEtag'] == before['stateEtag']
    assert execution['outcome']['status'] == 'EXECUTED'
    assert after['observationId'] != before['observationId']
    assert after['facts']['selectedSupplierId'] == 'SUPPLIER-B'
    assert after['facts']['shortageRisk'] is False
    assert execution['command']['idempotentReplay'] is False
    assert len(result['learning']) > 0
    print(json.dumps({
        'status':'PASS',
        'beforeObservationId':before['observationId'],
        'afterObservationId':after['observationId'],
        'commandExecutionId':execution['outcome']['commandExecutionId'],
        'selectedSupplierId':after['facts']['selectedSupplierId'],
        'ecLearningRecords':len(result['learning']),
        'authorizationBoundary':'EVO_REEVALUATED'
    }, indent=2))


if __name__ == '__main__':
    main()
