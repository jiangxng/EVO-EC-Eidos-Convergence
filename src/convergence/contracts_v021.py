from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
import json
from typing import Any

@dataclass(frozen=True)
class Validation:
    ok: bool
    diagnostics: tuple[str, ...] = ()

def _req(v: dict, names: tuple[str, ...], ds: list[str]):
    for n in names:
        if n not in v:
            ds.append(f"missing:{n}")

def _obj(v: Any, name: str, ds: list[str]) -> dict:
    x = v.get(name) if isinstance(v, dict) else None
    if not isinstance(x, dict):
        ds.append(f"type:{name}")
        return {}
    return x

def _version(v: dict, expected: str, ds: list[str]):
    if v.get("contractVersion") != expected:
        ds.append("version")

def _no_trusted_auth(v: Any, ds: list[str], prefix: str = ""):
    forbidden = {"authorized", "authorizationResult", "isAuthorized", "permissionGranted", "trustedAuthorization"}
    if isinstance(v, dict):
        for k, x in v.items():
            if k in forbidden:
                ds.append(f"trusted-auth:{prefix}{k}")
            _no_trusted_auth(x, ds, prefix + k + ".")
    elif isinstance(v, list):
        for i, x in enumerate(v):
            _no_trusted_auth(x, ds, prefix + str(i) + ".")

def validate_shared_envelope(v: Any) -> Validation:
    ds=[]
    if not isinstance(v, dict): return Validation(False,("type",))
    _req(v,("profileVersion","enterpriseId","identity","trace","capability"),ds)
    if v.get("profileVersion") != "0.1.0": ds.append("version")
    ident=_obj(v,"identity",ds); _req(ident,("actorType","actorId"),ds)
    trace=_obj(v,"trace",ds); _req(trace,("correlationId",),ds)
    if trace.get("causationId") == trace.get("authorizationId") and trace.get("causationId") is not None: ds.append("causation-is-authorization")
    cap=_obj(v,"capability",ds); _req(cap,("contractId","supportedVersions"),ds)
    if not isinstance(cap.get("supportedVersions"),list) or not cap.get("supportedVersions"): ds.append("capability-versions")
    _no_trusted_auth(v,ds)
    return Validation(not ds,tuple(ds))

def validate_enterprise_observation(v: Any) -> Validation:
    ds=[]
    if not isinstance(v,dict): return Validation(False,("type",))
    _req(v,("contractVersion","observationId","deliveryId","observationType","enterpriseId","effectiveAt","observedAt","publishedAt","correlationId","source","payload","provenance"),ds)
    _version(v,"1.0.0",ds)
    if v.get("observationId") == v.get("deliveryId"): ds.append("observation-equals-delivery")
    src=_obj(v,"source",ds); _req(src,("system","objectType","objectId","objectVersion"),ds)
    if v.get("enterpriseId") != src.get("enterpriseId",v.get("enterpriseId")): ds.append("cross-tenant")
    return Validation(not ds,tuple(ds))

def validate_command_proposal(v: Any, now: datetime|None=None) -> Validation:
    ds=[]
    if not isinstance(v,dict): return Validation(False,("type",))
    _req(v,("contractVersion","proposalId","enterpriseId","createdAt","expiresAt","basis","commandContractId","commandContractVersion","commandCode","inputSchemaVersion","proposedInput","evidence","rationale","correlationId","commandIdempotencyKey"),ds)
    _version(v,"1.0.0",ds)
    if v.get("proposalId") == v.get("commandIdempotencyKey"): ds.append("proposal-equals-idempotency")
    _no_trusted_auth(v,ds)
    try:
        exp=datetime.fromisoformat(str(v.get("expiresAt")).replace("Z","+00:00"))
        n=now or datetime.now(timezone.utc)
        if exp <= n: ds.append("expired")
    except Exception: ds.append("expiresAt")
    return Validation(not ds,tuple(ds))

def validate_operational_change(v: Any) -> Validation:
    ds=[]
    if not isinstance(v,dict): return Validation(False,("type",))
    _req(v,("contractVersion","proposalId","enterpriseId","targetDefinitionType","targetDefinitionId","baseVersion","changeIntent","operations","evidence","compatibility"),ds)
    _version(v,"1.0.0",ds)
    if not v.get("baseVersion"): ds.append("base-version")
    ops=v.get("operations")
    if not isinstance(ops,list) or not ops: ds.append("operations")
    else:
        allowed={"SET_FIELD","ADD_ITEM","REMOVE_ITEM","REPLACE_RULE","DEPRECATE_ITEM"}
        for op in ops:
            if not isinstance(op,dict) or op.get("op") not in allowed: ds.append("unsupported-operation")
            if isinstance(op,dict) and ("path" in op or op.get("op") in {"add","remove","replace","move","copy","test"}): ds.append("json-patch-forbidden")
    _no_trusted_auth(v,ds)
    return Validation(not ds,tuple(ds))

def simulation_digest(v: dict) -> str:
    material={k:v.get(k) for k in ("enterpriseId","scenarioId","actualSnapshotRef","definitionPins","rulePins","valuationPins","metricPins","assumptions","calculators","namespace")}
    return sha256(json.dumps(material,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()

def validate_enterprise_simulation(v: Any) -> Validation:
    ds=[]
    if not isinstance(v,dict): return Validation(False,("type",))
    _req(v,("contractVersion","simulationId","scenarioId","enterpriseId","actualSnapshotRef","definitionPins","rulePins","valuationPins","metricPins","assumptions","calculators","namespace"),ds)
    if v.get("contractVersion") != "0.1.0": ds.append("version")
    if v.get("namespace") != "HYPOTHETICAL": ds.append("actual-write")
    if v.get("writeActual") is True: ds.append("actual-write")
    return Validation(not ds,tuple(ds))

def validate_experience_proposal(v: Any, supported: dict[str,set[str]]|None=None) -> Validation:
    ds=[]
    if not isinstance(v,dict): return Validation(False,("type",))
    _req(v,("contractVersion","proposalId","producedAt","experience","context","fallback"),ds)
    _version(v,"1.0.0",ds)
    exp=_obj(v,"experience",ds); _req(exp,("experienceId","regions"),ds)
    regs=exp.get("regions")
    if not isinstance(regs,list) or not regs: ds.append("regions")
    else:
        for i,r in enumerate(regs):
            if not isinstance(r,dict): ds.append(f"region:{i}"); continue
            _req(r,("id","capabilityId","capabilityVersion","stability"),ds)
            if supported is not None and r.get("capabilityVersion") not in supported.get(str(r.get("capabilityId")),set()): ds.append(f"unsupported-capability:{i}")
            if r.get("mandatoryEvidence") is True and not r.get("evidenceRefs"): ds.append(f"missing-evidence:{i}")
            if r.get("stability") in {"invariant","shared-stable"} and r.get("personalization",{}).get("overrideSharedCore") is True: ds.append(f"shared-core-override:{i}")
            if r.get("accessibility",{}).get("required") is True and not r.get("accessibility",{}).get("label"): ds.append(f"accessibility:{i}")
    _no_trusted_auth(v,ds)
    return Validation(not ds,tuple(ds))

def validate_action_request(v: Any) -> Validation:
    ds=[]
    if not isinstance(v,dict): return Validation(False,("type",))
    _req(v,("contractVersion","actionRequestId","experienceInstanceId","experienceContractVersion","capabilityId","capabilityVersion","actionSemantic","targetRef","interactionContext","submittedValues","confirmationEvidence","actorContextRef","correlationId","occurredAt","presentedStateEtag","presentedDefinitionVersion"),ds)
    _version(v,"1.0.0",ds)
    target=_obj(v,"targetRef",ds)
    if "host" not in target or "resourceType" not in target or "resourceId" not in target: ds.append("host-neutral-target")
    _no_trusted_auth(v,ds)
    return Validation(not ds,tuple(ds))

def validate_evo_action_mapping(action: dict, command: dict) -> Validation:
    ds=[]
    ar=validate_action_request(action)
    ds.extend(ar.diagnostics)
    for k in ("commandCode","enterpriseId","actor","idempotencyKey","correlationId","input"):
        if k not in command: ds.append(f"command-missing:{k}")
    if command.get("authorized") is not None or command.get("authorizationResult") is not None: ds.append("adapter-must-not-authorize")
    if command.get("correlationId") != action.get("correlationId"): ds.append("correlation-not-preserved")
    return Validation(not ds,tuple(ds))
