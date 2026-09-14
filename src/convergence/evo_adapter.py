from __future__ import annotations
import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from .util import uid, now

class ReferenceEvoAdapter:
    """Deterministic stand-in for candidate contracts; never presented as upstream EVO."""
    def __init__(self):
        self.executed={}
        self.state={"supplierByOrder":{},"version":1}
    def feed_for_apm(self, scenario:dict):
        return {"contractVersion":"0.1.0","eventId":uid("EV"),"eventType":"material.shortage.detected","enterpriseId":scenario["enterpriseId"],"occurredAt":now(),"businessTime":now(),"correlationId":f"APM:{scenario['orderNo']}:SHORTAGE","provenance":{"producer":"ReferenceEvoAdapter","truthClass":"reference-fact"},"facts":{"orderNo":scenario["orderNo"],"customer":scenario["customer"],"customerPriority":scenario["customerPriority"],"materialId":"MAT-CRIT-SERVO","promiseDate":scenario["promiseDate"],"supplierA":scenario["supplierA"],"supplierB":scenario["supplierB"],"revenueAtRiskUsd":scenario["revenueAtRiskUsd"],"marginAfterSupplierB":scenario["marginAfterSupplierB"]},"flowContext":{"flow":"O2C","step":"material-availability-check"},"metricContext":{"revenueAtRiskUsd":scenario["revenueAtRiskUsd"]},"sopContext":{"sop":"material-shortage-response","version":"0.1.0"},"stateVersion":str(self.state["version"])}
    def execute_approved(self, proposal:dict, action:dict):
        if action["action"]!="APPROVE": raise ValueError("proposal not approved")
        if action["proposalId"]!=proposal["proposalId"]: raise ValueError("proposal mismatch")
        key=proposal["idempotencyKey"]
        if key in self.executed: return self.executed[key]
        if proposal["commandCode"]!="procurement.use-alternate-supplier": raise ValueError("unsupported reference command")
        order=proposal["input"]["orderNo"]
        self.state["supplierByOrder"][order]=proposal["input"]["toSupplierId"]
        self.state["version"]+=1
        outcome={"contractVersion":"0.1.0","outcomeId":uid("OUT"),"enterpriseId":proposal["enterpriseId"],"proposalId":proposal["proposalId"],"correlationId":proposal["correlationId"],"commandExecutionId":uid("CMD"),"status":"SUCCEEDED","observedAt":now(),"measures":{"selectedSupplier":proposal["input"]["toSupplierId"],"promiseProtected":True,"revenueProtectedUsd":proposal["expectedImpact"]["revenueProtectedUsd"],"incrementalCostPercent":proposal["expectedImpact"]["costDeltaPercent"],"deliveryRiskDelta":-1.0},"provenance":{"executor":"ReferenceEvoAdapter","authorization":action["authorization"]}}
        self.executed[key]=outcome
        return outcome

class LiveEvoAdapter:
    """Uses only current public HTTP reference endpoints. It cannot invent missing procurement commands."""
    def __init__(self, base_url:str): self.base=base_url.rstrip('/')
    def _get(self,path):
        with urlopen(self.base+path,timeout=8) as r: return json.loads(r.read().decode())
    def check(self):
        result={"baseUrl":self.base,"checks":{},"liveGap":None}
        for p in ["/health/live","/api/v1/demo/dashboard","/api/v1/demo/ai/catalog"]:
            try: result["checks"][p]={"ok":True,"value":self._get(p)}
            except Exception as e: result["checks"][p]={"ok":False,"error":str(e)}
        result["liveGap"]="Current upstream EVO 1.0.0-alpha.2 does not publish procurement.use-alternate-supplier through the observed reference HTTP API."
        return result
