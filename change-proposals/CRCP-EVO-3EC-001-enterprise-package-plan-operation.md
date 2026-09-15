# CROSS-REPO-CHANGE-PROPOSAL

**Proposal ID:** `CRCP-EVO-3EC-001`  
**Status:** PROPOSED  
**Source Project:** EVO  
**Target:** 3EC cross-project governance / Enterprise Package administration surfaces  
**Related:** `CRCP-EC-EVO-004`

## Clarified runtime boundary

**LLMs do not participate in EVO Instance runtime.** EVO must remain fully operational when EC or any LLM is unavailable. Validate, Plan/Diff, Deploy, Command execution, BusinessData persistence, Posting, Ledger, Balance, Cost/Valuation and Replay are deterministic EVO runtime capabilities.

EC may compile or propose an Enterprise Package outside the EVO Instance runtime. That does not make EC/LLM a participant in package deployment execution.

## Problem

While reconciling the EVO-owned Enterprise Package v0.1 public API, EVO determined that a side-effect-free package `Plan/Diff` boundary is valuable between validation and authorized deployment.

Schema validation answers whether a package is structurally/semantically admissible. Human administrators additionally need a deterministic preview of what governed enterprise-definition changes would occur before approving deployment.

## Intended consumer

The primary consumer of Plan/Diff is **human governance**. The result may be rendered by Eidos or another administration/operations UI, exported for audit, or inspected by deterministic tooling. It is not an LLM reasoning interface and must not require EC or an LLM to interpret or execute it.

A Plan/Diff should be both human-readable and machine-structured so a deterministic UI can present additions, removals, version changes, compatibility findings, replay/recalculation impact, blocking issues and warnings without inventing semantics.

## Proposed cross-project semantic requirement

3EC should certify an optional/additive **Enterprise Package Deployment Plan** capability with these invariants:

1. Planning is deterministic and side-effect-free.
2. Planning does not imply deployment authorization or approval.
3. The target enterprise scope and expected base definition version are explicit.
4. The plan reports stable machine-readable intended changes, dependency/compatibility findings, operational impact, warnings and blocking issues.
5. The plan is primarily human review evidence for a later deployment decision.
6. Eidos or another host may render the plan, but presentation/confirmation evidence is not EVO authorization.
7. EVO MUST revalidate authorization, approval requirements, base version and package compatibility at mutation time.
8. A successful plan is not proof that deployment will still succeed after authoritative state changes.
9. The operation does not expose EVO private tables, migrations or internal module APIs.
10. EC/LLM availability is never a prerequisite for Plan/Diff or Deploy.

Conceptual EVO-owned operation:

`PlanEnterprisePackageDeployment(enterprise_scope, package, expected_base_version?)`

Exact endpoint/schema remains EVO-owned. 3EC owns only the cross-project semantic expectations and certification profile.

## Compatibility

Additive to CRCP-EC-EVO-004. The clarification removes EC/LLM as an intended runtime consumer. Consumers that do not support planning may continue `Schema Discovery -> Validate -> Deploy` where EVO governance permits it.

## Security

Plan is non-mutating but may reveal target enterprise definition metadata; EVO controls authorization/exposure policy. Plan output must not contain secrets, credentials, commercial BusinessData, LedgerEntry history or other actual-state data beyond the minimum governed definition metadata required to explain deployment impact.

## Certification requested

- valid package produces deterministic plan for a pinned target/base version;
- the same inputs and pinned authoritative definition versions produce the same semantic plan;
- stale base is explicit/fail-closed;
- plan performs no definition publication or runtime mutation;
- successful plan does not bypass human approval or EVO deployment authorization;
- deployment rechecks state/version/authorization;
- plan can be rendered to a human without EC/LLM participation;
- plan output contains no forbidden actual commercial data;
- EVO package administration remains functional with EC/LLM unavailable.

## EVO owner status

EVO is publishing this operation experimentally in its v0.1 API design as a deterministic human-governance capability. This CRCP asks 3EC to decide whether the Plan operation becomes part of the cross-project Enterprise Package certification profile. No EC implementation change is requested. Eidos may optionally provide a deterministic administration presentation for the plan through a separately governed integration profile.
