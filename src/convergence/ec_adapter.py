from __future__ import annotations
from pathlib import Path
from ec.domain import Provenance, Scope, ScopeKind, new_id, now_utc
from ec.knowledge.model import KnowledgeKind, KnowledgeRecord, KnowledgeStatus
from ec.learning.defaults import external_regulation_strategy, case_outcome_learning_strategy
from ec.learning.registry import LearningStrategyRegistry
from ec.learning.loop import OutcomeLearningLoop, DecisionObservation
from ec.storage.memory import InMemoryKnowledgeRepository
from ec.context import ContextCompiler, ContextRequest
from .util import uid, now

class EcAdapter:
    """Adapter over the real bundled EC v1.0.1 reference runtime."""
    def __init__(self, enterprise_id="APM-DEMO"):
        self.enterprise_id=enterprise_id
        self.repo=InMemoryKnowledgeRepository()
        self.strategies=LearningStrategyRegistry()
        self.strategies.register(external_regulation_strategy());self.strategies.register(case_outcome_learning_strategy())
        self.learning=OutcomeLearningLoop(self.repo)

    def ingest_evo_feed(self, feed:dict):
        scope=Scope(ScopeKind.TENANT,self.enterprise_id,tenant_id=self.enterprise_id)
        prov=Provenance("system","evo-adapter","EvoIntelligenceFeed",feed["eventId"])
        for k,v in feed["facts"].items():
            self.repo.append(KnowledgeRecord(KnowledgeKind.FACT,feed["facts"].get("orderNo",feed["eventId"]),k,v,scope,prov,.99,status=KnowledgeStatus.ACCEPTED,tags=("evo-fact",)))

    def analyze_shortage(self, feed:dict):
        order=feed["facts"]["orderNo"]
        ctx=ContextCompiler(self.repo,self.strategies).compile(ContextRequest("resolve material shortage","procurement-manager",self.enterprise_id,"manufacturing",order,risk_class="high"))
        f=feed["facts"]
        a=f["supplierA"];b=f["supplierB"]
        eligible=bool(b.get("qualified")) and b.get("eta") <= f.get("promiseDate") and f.get("marginAfterSupplierB") == "acceptable"
        recommendation="alternate supplier" if eligible else "escalate for manual planning"
        rationale=[]
        if a.get("eta") > f.get("promiseDate"): rationale.append("supplier A ETA exceeds customer promise")
        if b.get("qualified"): rationale.append("supplier B is qualified")
        if b.get("eta") <= f.get("promiseDate"): rationale.append("supplier B ETA protects customer promise")
        if f.get("marginAfterSupplierB")=="acceptable": rationale.append("margin remains acceptable after supplier B premium")
        rationale.append(f"USD {f['revenueAtRiskUsd']} revenue is exposed")
        evidence=[x.record_id for x in ctx.items]
        proposal={
          "contractVersion":"0.1.0","proposalId":uid("CP"),"enterpriseId":self.enterprise_id,"targetCapability":"procurement","commandCode":"procurement.use-alternate-supplier","actorIntent":"AI_PROPOSAL",
          "idempotencyKey":f"supplier-switch:{order}:SUPPLIER-B","correlationId":feed["correlationId"],"businessObjectKey":order,"expectedStateVersion":feed.get("stateVersion"),
          "input":{"orderNo":order,"materialId":f["materialId"],"fromSupplierId":a["id"],"toSupplierId":b["id"],"reason":"material-shortage"},
          "rationale":rationale,"evidence":evidence,"assumptions":["supplier qualification remains valid at execution time"],"risks":[f"incremental material cost {b['costDeltaPercent']}%"],
          "expectedImpact":{"revenueProtectedUsd":f["revenueAtRiskUsd"],"costDeltaPercent":b["costDeltaPercent"],"promiseProtected":eligible},"requiredAuthorization":"ProcurementManager","expiresAt":None
        }
        experience={
          "contractVersion":"0.1.0","proposalId":uid("XP"),"producedAt":now(),
          "composition":{"contractVersion":"0.1.0","experienceId":f"manufacturing.delivery-risk.{order}","title":"Production Delivery Risk Decision Workspace","regions":[
            {"id":"exceptions","capability":"exception-queue","stability":"shared-stable","attention":{"level":"important","reasonCode":"MATERIAL_SHORTAGE"},"props":{"order":order,"risk":"material shortage"}},
            {"id":"decision","capability":"decision-panel","stability":"invariant","attention":{"level":"requires-review","reasonCode":"HUMAN_AUTHORIZATION_REQUIRED","decisionCritical":True},"props":{"recommendation":recommendation,"options":["wait","alternate supplier","split shipment","replan production"],"commandProposalId":proposal["proposalId"]}},
            {"id":"evidence","capability":"evidence-stack","stability":"shared-stable","attention":{"level":"informative","reasonCode":"EVIDENCE"},"props":{"contextRecordIds":evidence}},
            {"id":"impact","capability":"impact-preview","stability":"adaptive","attention":{"level":"important","reasonCode":"REVENUE_AT_RISK"},"props":{"revenueAtRisk":f["revenueAtRiskUsd"],"currency":"USD","supplierBCostDeltaPercent":b["costDeltaPercent"]}},
            {"id":"timeline","capability":"timeline","stability":"personal-stable","attention":{"level":"informative","reasonCode":"DATE_COMPARISON"},"props":{"promiseDate":f["promiseDate"],"supplierAEta":a["eta"],"supplierBEta":b["eta"]}}
          ],"metadata":{"producer":"EC v1.0.1 via Convergence v0.2","standardFallbackRef":"fallback://manufacturing/delivery-risk/v1"}},
          "context":{"contractVersion":"0.1.0","contextId":ctx.request_id,"mode":"role","role":"procurement-manager","expertise":"expert","task":"resolve material shortage","locale":"en-US","device":{"terminal":"web","viewportClass":"expanded","inputModes":["pointer","keyboard"]},"extensions":{"enterpriseId":self.enterprise_id,"correlationId":feed["correlationId"]}},
          "rationale":[{"code":"SUPPLY_RISK","explanation":x,"evidence":evidence[:2]} for x in rationale]
        }
        return ctx, proposal, experience

    def learn_outcome(self, proposal:dict, outcome:dict):
        observed=self.learning.observe(DecisionObservation(
          situation=f"{proposal['businessObjectKey']} material shortage",
          decision=proposal["commandCode"],
          outcome=f"status={outcome['status']}; measures={outcome['measures']}",
          metric_delta=float(outcome["measures"].get("deliveryRiskDelta",0.0)),
          tenant_id=self.enterprise_id,domain="manufacturing"))
        return [{"recordId":r.record_id,"kind":r.kind.value,"status":r.status.value,"predicate":r.predicate,"value":r.value} for r in observed]
