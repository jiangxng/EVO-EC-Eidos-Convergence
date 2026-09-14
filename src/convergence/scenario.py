from __future__ import annotations
from pathlib import Path
import json
from .evo_adapter import ReferenceEvoAdapter
from .ec_adapter import EcAdapter
from .eidos_adapter import EidosAdapter
from .contracts import validate_evo_feed,validate_command_proposal,validate_eidos_proposal,validate_action_request,validate_outcome
from .util import dump_json

def run_apm(root:Path, output:Path):
    scenario=json.loads((root/'enterprise-packs/apm/scenarios/material-shortage.json').read_text(encoding='utf-8'))
    evo=ReferenceEvoAdapter(); ec=EcAdapter(scenario['enterpriseId']); eidos=EidosAdapter()
    feed=evo.feed_for_apm(scenario); assert validate_evo_feed(feed).ok
    ec.ingest_evo_feed(feed)
    ctx,cmd,xp=ec.analyze_shortage(feed)
    assert validate_command_proposal(cmd).ok
    ev=eidos.validate(xp); assert ev.ok,ev.diagnostics
    action=eidos.approve(cmd); assert validate_action_request(action).ok
    outcome=evo.execute_approved(cmd,action); assert validate_outcome(outcome).ok
    learned=ec.learn_outcome(cmd,outcome)
    output.mkdir(parents=True,exist_ok=True)
    dump_json(output/'01-evo-intelligence-feed.json',feed)
    dump_json(output/'02-ec-command-proposal.json',cmd)
    dump_json(output/'03-ec-experience-proposal.json',xp)
    dump_json(output/'04-eidos-action-request.json',action)
    dump_json(output/'05-evo-outcome.json',outcome)
    dump_json(output/'06-ec-learning.json',learned)
    summary={"status":"PASS","enterprise":"Apex Precision Manufacturing","scenario":"critical-material-shortage","recommendation":xp['composition']['regions'][1]['props']['recommendation'],"approvedSupplier":outcome['measures']['selectedSupplier'],"promiseProtected":outcome['measures']['promiseProtected'],"revenueProtectedUsd":outcome['measures']['revenueProtectedUsd'],"learnedCandidateKinds":[x['kind'] for x in learned],"boundaries":{"EC":"real bundled EC v1.0.1 reference runtime + convergence adapter","EVO":"reference adapter for candidate procurement command","Eidos":"exact 0.1.0 contract mirror/conformance; optional real repo validator"}}
    dump_json(output/'SUMMARY.json',summary)
    return summary
