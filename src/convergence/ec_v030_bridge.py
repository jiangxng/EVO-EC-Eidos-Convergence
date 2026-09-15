from __future__ import annotations

from datetime import datetime, timedelta, timezone

from .ec_adapter import EcAdapter
from .util import uid, now


class EcV030Bridge:
    """Uses the bundled real EC runtime while publishing frozen v1 contracts."""
    def __init__(self):
        self.ec = EcAdapter(enterprise_id='APM')

    def analyze(self, observation: dict):
        f = observation['facts']
        legacy_feed = {'eventId':observation['observationId'],'correlationId':observation['correlationId'],'stateVersion':observation['observationId'],'facts':f}
        self.ec.ingest_evo_feed(legacy_feed)
        ctx, _legacy_proposal, _legacy_experience = self.ec.analyze_shortage(legacy_feed)
        evidence = [observation['observationId']]
        expires_at = (datetime.now(timezone.utc) + timedelta(hours=24)).isoformat().replace('+00:00','Z')
        proposal = {
            'contractVersion':'1.0.0','proposalId':uid('CP'),'enterpriseId':'APM','createdAt':now(),'expiresAt':expires_at,'basis':evidence,
            'commandContractId':'evo.command','commandContractVersion':'1.0.0','commandCode':'procurement.use-alternate-supplier','inputSchemaVersion':'1',
            'proposedInput':{'supplierId':'SUPPLIER-B'},'evidence':evidence,'rationale':'Protect Sep 18 promise','correlationId':observation['correlationId'],
            'commandIdempotencyKey':f"cmd-idem-alt-supplier-{observation['observationId']}"
        }
        experience = {
            'contractVersion':'1.0.0','proposalId':uid('XP'),'producedAt':now(),
            'experience':{'experienceId':'supplier-risk-decision','regions':[{'id':'decision','capabilityId':'decision-panel','capabilityVersion':'1.0.0','stability':'shared-stable','mandatoryEvidence':True,'evidenceRefs':evidence,'accessibility':{'required':True,'label':'Supplier risk decision'}}]},
            'context':{'enterpriseId':'APM','correlationId':observation['correlationId']},'fallback':{'mode':'standard'},
            'extensions':{'ecContextRequestId':ctx.request_id,'authoritativePresentation':{'stateEtag':observation.get('stateEtag','state-7'),'definitionVersion':observation.get('definitionVersion','3')},'recommendation':{'supplierId':'SUPPLIER-B','revenueProtectedUsd':f['revenueAtRiskUsd'],'costDeltaPercent':f['supplierB']['costDeltaPercent']}}
        }
        return proposal, experience

    def learn(self, proposal: dict, outcome: dict):
        adapted_proposal={'businessObjectKey':'SO-20260918-0182','commandCode':proposal['commandCode']}
        adapted_outcome={'status':outcome['status'],'measures':{'deliveryRiskDelta':-1.0,'businessDataId':outcome.get('businessDataId')}}
        return self.ec.learn_outcome(adapted_proposal, adapted_outcome)
