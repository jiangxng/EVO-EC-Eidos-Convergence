from __future__ import annotations
from dataclasses import dataclass
from typing import Any

MODES={"standard","role","personal","shared"}
TERMINALS={"web","desktop","mobile","tablet","large-screen","embedded","terminal","voice","agent"}
STABILITY={"invariant","shared-stable","personal-stable","adaptive"}
ATTENTION={"passive","informative","important","requires-review","urgent","blocking"}
MOTION={"none","reveal","continuity","attention","confirmation","causality","state-transition"}

@dataclass(frozen=True)
class Validation:
    ok: bool
    diagnostics: tuple[str,...]=()

def _req(v:dict, names:list[str], ds:list[str]):
    for n in names:
        if n not in v: ds.append(f"missing:{n}")

def validate_evo_feed(v:Any)->Validation:
    ds=[]
    if not isinstance(v,dict): return Validation(False,("type",))
    _req(v,["contractVersion","eventId","eventType","enterpriseId","occurredAt","businessTime","correlationId","provenance","facts"],ds)
    if v.get("contractVersion")!="0.1.0": ds.append("version")
    return Validation(not ds,tuple(ds))

def validate_command_proposal(v:Any)->Validation:
    ds=[]
    if not isinstance(v,dict): return Validation(False,("type",))
    _req(v,["contractVersion","proposalId","enterpriseId","targetCapability","commandCode","actorIntent","idempotencyKey","correlationId","businessObjectKey","input","rationale","evidence","requiredAuthorization"],ds)
    if v.get("contractVersion")!="0.1.0": ds.append("version")
    if v.get("actorIntent")!="AI_PROPOSAL": ds.append("actorIntent")
    return Validation(not ds,tuple(ds))

def validate_eidos_proposal(v:Any)->Validation:
    # Mirrors the current upstream Eidos 0.1.0 validation semantics for the fields it validates,
    # plus the outer EcExperienceProposal envelope.
    ds=[]
    if not isinstance(v,dict): return Validation(False,("EIDOS_PROPOSAL_TYPE",))
    _req(v,["contractVersion","proposalId","producedAt","composition","context"],ds)
    if v.get("contractVersion")!="0.1.0": ds.append("EIDOS_PROPOSAL_VERSION")
    c=v.get("context")
    if not isinstance(c,dict): ds.append("EIDOS_CONTEXT_TYPE")
    else:
        if c.get("contractVersion")!="0.1.0": ds.append("EIDOS_CONTEXT_VERSION")
        if not c.get("contextId"): ds.append("EIDOS_CONTEXT_ID")
        if c.get("mode") not in MODES: ds.append("EIDOS_CONTEXT_MODE")
        d=c.get("device")
        if not isinstance(d,dict): ds.append("EIDOS_CONTEXT_DEVICE")
        elif d.get("terminal") not in TERMINALS: ds.append("EIDOS_CONTEXT_TERMINAL")
    comp=v.get("composition")
    if not isinstance(comp,dict): ds.append("EIDOS_EXPERIENCE_TYPE")
    else:
        if comp.get("contractVersion")!="0.1.0": ds.append("EIDOS_EXPERIENCE_VERSION")
        if not comp.get("experienceId"): ds.append("EIDOS_EXPERIENCE_ID")
        rs=comp.get("regions")
        if not isinstance(rs,list): ds.append("EIDOS_EXPERIENCE_REGIONS")
        else:
            ids=set()
            for i,r in enumerate(rs):
                if not isinstance(r,dict): ds.append(f"EIDOS_REGION_TYPE:{i}"); continue
                rid=r.get("id")
                if not rid: ds.append(f"EIDOS_REGION_ID:{i}")
                elif rid in ids: ds.append(f"EIDOS_REGION_DUPLICATE:{rid}")
                else: ids.add(rid)
                if not r.get("capability"): ds.append(f"EIDOS_REGION_CAPABILITY:{i}")
                if r.get("stability") not in STABILITY: ds.append(f"EIDOS_REGION_STABILITY:{i}")
                a=r.get("attention")
                if a is not None and (not isinstance(a,dict) or a.get("level") not in ATTENTION): ds.append(f"EIDOS_ATTENTION_LEVEL:{i}")
                m=r.get("motion")
                if m is not None and (not isinstance(m,dict) or m.get("intent") not in MOTION): ds.append(f"EIDOS_MOTION_INTENT:{i}")
    return Validation(not ds,tuple(ds))

def validate_action_request(v:Any)->Validation:
    ds=[]
    if not isinstance(v,dict): return Validation(False,("type",))
    _req(v,["contractVersion","actionRequestId","proposalId","enterpriseId","action","actor","authorization","correlationId","createdAt"],ds)
    if v.get("contractVersion")!="0.1.0": ds.append("version")
    if v.get("action") not in {"APPROVE","REJECT"}: ds.append("action")
    return Validation(not ds,tuple(ds))

def validate_outcome(v:Any)->Validation:
    ds=[]
    if not isinstance(v,dict): return Validation(False,("type",))
    _req(v,["contractVersion","outcomeId","enterpriseId","proposalId","correlationId","commandExecutionId","status","observedAt","measures","provenance"],ds)
    if v.get("contractVersion")!="0.1.0": ds.append("version")
    if v.get("status") not in {"SUCCEEDED","FAILED","PARTIAL"}: ds.append("status")
    return Validation(not ds,tuple(ds))
