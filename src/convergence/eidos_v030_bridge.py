from __future__ import annotations

from .contracts_v021 import validate_experience_proposal, validate_action_request
from .util import uid, now


class EidosV030Bridge:
    """Certified Eidos boundary: validates/realizes experience and emits Host-neutral action evidence."""
    def realize(self, experience_proposal: dict) -> dict:
        validate_experience_proposal(experience_proposal)
        ext = experience_proposal.get('extensions', {})
        presentation = ext.get('authoritativePresentation', {})
        return {
            'experienceInstanceId':uid('XI'),
            'experienceContractVersion':'1.0.0',
            'proposal':experience_proposal,
            'decision':ext.get('recommendation', {'supplierId':'SUPPLIER-B'}),
            'presentedStateEtag':presentation.get('stateEtag'),
            'presentedDefinitionVersion':presentation.get('definitionVersion'),
            'integrity':'VALIDATED_BY_EIDOS_CONTRACT_BOUNDARY'
        }

    def approve(self, realized: dict) -> dict:
        proposal = realized['proposal']
        if not realized.get('presentedStateEtag') or not realized.get('presentedDefinitionVersion'):
            raise RuntimeError('Eidos cannot emit an executable decision without authoritative presentation evidence')
        action = {
            'contractVersion':'1.0.0','actionRequestId':uid('AR'),'experienceInstanceId':realized['experienceInstanceId'],
            'experienceContractVersion':'1.0.0','capabilityId':'decision-panel','capabilityVersion':'1.0.0','actionSemantic':'APPROVE_RECOMMENDATION',
            'targetRef':{'host':'enterprise-runtime','resourceType':'supplier-decision','resourceId':'SO-20260918-0182'},
            'interactionContext':{'surface':'desktop'},'submittedValues':{'supplierId':'SUPPLIER-B'},
            'confirmationEvidence':{'confirmed':True,'method':'explicit-click'},'actorContextRef':'actor-context-demo-user',
            'correlationId':proposal['context']['correlationId'],'occurredAt':now(),
            'presentedStateEtag':realized['presentedStateEtag'],'presentedDefinitionVersion':realized['presentedDefinitionVersion']
        }
        validate_action_request(action)
        if 'authorization' in action or 'authorized' in action:
            raise RuntimeError('Eidos ActionRequest must remain Host-neutral and non-authorizing')
        return action
