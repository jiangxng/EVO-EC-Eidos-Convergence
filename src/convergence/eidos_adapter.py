from __future__ import annotations
import json, subprocess, os
from pathlib import Path
from .contracts import validate_eidos_proposal
from .util import uid, now, dump_json

class EidosAdapter:
    def validate(self,proposal): return validate_eidos_proposal(proposal)
    def approve(self,command_proposal,actor_id="procurement-manager-01"):
        return {"contractVersion":"0.1.0","actionRequestId":uid("AR"),"proposalId":command_proposal["proposalId"],"enterpriseId":command_proposal["enterpriseId"],"action":"APPROVE","actor":{"type":"HUMAN","id":actor_id},"authorization":{"role":"ProcurementManager","scope":"supplier-change"},"correlationId":command_proposal["correlationId"],"createdAt":now()}

def verify_with_real_eidos_repo(proposal_path:str,eidos_repo:str):
    repo=Path(eidos_repo)
    dist=repo/'dist/experience/validate.js'
    if not dist.exists():
        return {"ok":False,"reason":"Eidos dist/experience/validate.js not found. Run npm run build in the Eidos repo first."}
    script=Path(__file__).resolve().parents[2]/'tools/verify-eidos.mjs'
    cp=subprocess.run(['node',str(script),str(repo),str(Path(proposal_path).resolve())],capture_output=True,text=True)
    try: payload=json.loads(cp.stdout.strip() or '{}')
    except Exception: payload={"stdout":cp.stdout,"stderr":cp.stderr}
    payload["processExitCode"]=cp.returncode
    return payload
