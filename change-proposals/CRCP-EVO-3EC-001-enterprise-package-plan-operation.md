# CROSS-REPO-CHANGE-PROPOSAL

**Proposal ID:** `CRCP-EVO-3EC-001`  
**Status:** PROPOSED  
**Source Project:** EVO  
**Target:** 3EC cross-project governance / Enterprise Package consumers  
**Related:** `CRCP-EC-EVO-004`

## Problem

While reconciling the EVO-owned Enterprise Package v0.1 public API, EVO determined that a side-effect-free package `Plan/Diff` boundary is valuable between validation and authorized deployment.

Schema validation alone answers whether a package is structurally/semantically admissible. It does not tell EC, operators, Market tooling or Eidos what governed definition changes would occur in a target enterprise scope, whether the expected base version is stale, or which dependencies/migrations/publications are planned.

## Proposed cross-project semantic requirement

3EC should certify an optional/additive **Enterprise Package Deployment Plan** capability with these invariants:

1. Planning is side-effect-free.
2. Planning does not imply deployment authorization.
3. The target enterprise scope and expected base definition version are explicit.
4. The plan reports stable machine-readable intended changes, dependency/compatibility findings and blocking issues.
5. A plan is advisory evidence for a later deployment request; EVO MUST revalidate authorization, base version and package compatibility at mutation time.
6. EC/Eidos/Market MUST NOT treat a successful plan as authorization or as proof that deployment will still succeed after state changes.
7. The operation does not expose EVO private tables/migrations/internal module APIs.

Conceptual EVO-owned operation:

`PlanEnterprisePackageDeployment(enterprise_scope, package, expected_base_version?)`

Exact endpoint/schema remains EVO-owned. 3EC owns only the cross-project semantic expectations and certification profile.

## Compatibility

Additive to CRCP-EC-EVO-004. Consumers that do not support planning may continue `Schema Discovery -> Validate -> Deploy` where EVO permits it.

## Security

Plan is non-mutating but may reveal target enterprise definition metadata; EVO controls authorization/exposure policy. Plan output must not contain secrets, credentials, commercial BusinessData, LedgerEntry history or other actual-state data beyond the minimum governed definition metadata required to explain the plan.

## Certification requested

- valid package produces deterministic plan for a pinned target/base version;
- stale base is explicit/fail-closed;
- plan performs no definition publication or runtime mutation;
- successful plan does not bypass deployment authorization;
- deployment rechecks state/version/authorization;
- plan output contains no forbidden actual commercial data.

## EVO owner status

EVO is publishing this operation experimentally in its v0.1 API design. This CRCP asks 3EC to decide whether the Plan operation becomes part of the cross-project Enterprise Package certification profile. No EC or Eidos implementation change is assumed until 3EC reconciliation.
