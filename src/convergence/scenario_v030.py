from __future__ import annotations

from .evo_live_adapter import LiveEvoAdapter
from .ec_v030_bridge import EcV030Bridge
from .eidos_v030_bridge import EidosV030Bridge


class ApmLiveScenario:
    def __init__(self, evo: LiveEvoAdapter | None = None):
        self.evo = evo or LiveEvoAdapter()
        self.ec = EcV030Bridge()
        self.eidos = EidosV030Bridge()

    def prepare_decision(self):
        before = self.evo.observation()
        proposal, experience = self.ec.analyze(before)
        admission = self.evo.admit_command_proposal(proposal)
        if not admission.get('admitted'):
            raise RuntimeError('EVO rejected EC Command Proposal')
        realized = self.eidos.realize(experience)
        return {'observation':before,'commandProposal':proposal,'admission':admission,'experience':realized}

    def approve_and_execute(self, prepared: dict):
        action = self.eidos.approve(prepared['experience'])
        executed = self.evo.execute_action(action)
        after = executed['observation']
        if after['observationId'] == prepared['observation']['observationId']:
            raise RuntimeError('EVO did not produce a new authoritative observation')
        learning = self.ec.learn(prepared['commandProposal'], executed['outcome'])
        return {'actionRequest':action,'execution':executed,'learning':learning}
