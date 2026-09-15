from __future__ import annotations

from .contracts_v021 import validate_experience_proposal, validate_action_request
from .util import uid, now


class EidosV030Bridge:
    """Convergence-side certified Eidos boundary. It never asserts business authorization."""
    def realize(self, experience_proposal: dict) -> dict:
        validate_experience_proposal(experience_proposal)
        ext = experience_proposal.get('extensions', {})
        return {
            'experienceInstanceId':uid('XI'),
            'experienceContractVersion':'1.0.0',
            'proposal':experience_proposal,
            'decision':ext.get('recommendation', {'supplierId':'SUPPLIER-B'}),
            'integrity':'VALIDATED_BY_EIDOS_CONTRACT_BOUNDARY'
        }

    def approve(self, realized: dict) -> dict:
        proposal = realized['proposal']
        action = {
            'contractVersion':'1.0.0', 'actionRequestId':uid('AR'),
            'experienceInstanceId':realized['experienceInstanceId'],
            'experienceContractVersion':'1.0.0', 'capabilityId':'decision-panel','capabilityVersion':'1.0.0',
            'actionSemantic':'APPROVE_RECOMMENDATION',
            'targetRef':{'host':'enterprise-runtime','resourceType':'supplier-decision','resourceId':'SO-20260918-0182'},
            'interactionContext':{'surface':'desktop'},
            'submittedValues':{'supplierId':'SUPPLIER-B'},
            'confirmationEvidence':{'confirmed':True,'method':'explicit-click'},
            'actorContextRef':'actor-context-demo-user',
            'correlationId':proposal['context']['correlationId'], 'occurredAt':now(),
            'presentedStateEtag':'obs-apm-so-0182-v7','presentedDefinitionVersion':'1'
        }
        validate_action_request(action)
        if 'authorization' in action or 'authorized' in action:
            raise RuntimeError('Eidos ActionRequest must remain Host-neutral and non-authorizing')
        return action
