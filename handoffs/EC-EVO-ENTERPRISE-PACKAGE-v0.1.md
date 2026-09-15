# EC → EVO Enterprise Package v0.1 Handoff

Status: CONTRACT AVAILABLE / RUNTIME INTEGRATION IN PROGRESS
Owner: EVO
Consumer: EC
Governance: 3EC
Date: 2026-09-15

## Purpose

EC may begin compiling Enterprise Packages against the EVO-owned v0.1 contract now. EC MUST NOT invent a parallel package format or depend on EVO internal tables/modules.

This handoff publishes the contract boundary before EVO's production HTTP/persistence integration is complete. Contract availability and runtime endpoint availability are intentionally distinguished.

## Authoritative EVO contract artifacts

Repository: `jiangxng/EVO`
Branch: `evo/enterprise-package-v0.1`
Pinned commit at handoff: `d18fac50f0fc1bb29d9728fd6c5730463f8aeb71`

- `contracts/enterprise-package-v0.1.schema.json`
- `contracts/enterprise-package-api-v0.1.openapi.yaml`
- `docs/public/ENTERPRISE-PACKAGE-v0.1.md`

EC should pin this contract version/commit in fixtures and compatibility tests rather than copy the schema into a divergent EC-owned model.

## Contract operations

The v0.1 boundary defines these operations/capabilities:

- Schema discovery
- Capability discovery
- Validate Enterprise Package
- Plan/Diff Enterprise Package
- Deploy Enterprise Package
- Export Enterprise Package (`DEFINITION_ONLY`)

`Plan/Diff` is a deterministic EVO computation intended primarily for human review. It is not an LLM reasoning operation and successful planning is not deployment authorization.

## Runtime independence

LLMs and EC do not participate in EVO Instance runtime. EVO remains fully operable when EC/LLMs are unavailable. Validate, Plan/Diff, Deploy, Command, BusinessData, Posting, Ledger, Balance, Cost/Valuation and Replay remain deterministic EVO responsibilities.

## EC implementation rule

EC MAY now:

1. Consume the EVO v0.1 package schema.
2. Compile candidate packages from EC knowledge/reasoning.
3. Validate candidate package structure locally against the pinned contract for development feedback.
4. Produce fixtures and round-trip/certification scenarios.
5. Treat EVO Validate/Plan as the authoritative semantic/runtime checks when those endpoints are available.
6. Consume `DEFINITION_ONLY` export for governed portability/learning workflows.

EC MUST NOT:

- write EVO internal databases/tables;
- import EVO private module types as its integration contract;
- treat local EC validation as EVO authorization;
- treat Plan success as Deploy approval;
- make EC/LLM availability a prerequisite for EVO runtime;
- invent new definition kinds or package semantics without a 3EC change proposal.

## Package scope v0.1

For v0.1, an Enterprise Package represents the complete governed `DEFINITION_ONLY` target snapshot for one enterprise scope. Runtime/business history is excluded. BusinessData, LedgerEntry, balances, CommandExecution, work items, posting inputs/runs, replay runs, CostResult/CostRun and valuation runtime records are not package definitions.

The package definition vocabulary is EVO-owned. Current supported kinds are declared by the EVO schema/capability response and include enterprise/domain/transaction/application/field/command/capability/flow/SOP/metric/dimension/ledger/posting/cost/valuation/authorization definition families as defined by the pinned contract.

## Determinism and versioning

EC must preserve package schema version, package identity/version, definition identity/version and explicit dependencies. It must not select an implicit latest EVO definition/rule version when reproducibility requires a pinned version.

The same package + same compatible EVO base/version context must produce deterministic validation and plan semantics.

## Human review and authorization

Canonical deployment chain:

`EC may compile/propose package outside EVO → EVO Validate → EVO deterministic Plan/Diff → Human Review/Approve → EVO Authorization + Deploy`

Human approval evidence and EVO authorization are separate concerns. EC does not grant either.

## Current availability declaration

**Available to EC now:** schema, OpenAPI contract, public semantic documentation, supported operation/capability model, compile-time integration target.

**Still being completed by EVO:** production HTTP wiring, persistent EnterpriseDefinitionSource/Target, deployment idempotency receipt storage, trusted authorization/approval evidence integration, full runtime/CI certification.

Therefore EC should start contract integration and package compilation now, while treating network Deploy as unavailable until EVO publishes runtime readiness.

## Compatibility discipline

Any cross-project semantic change to this contract goes through 3EC. EVO may continue internal implementation behind the contract without EC changes. Additive compatible changes should preserve v0.1 consumers; breaking semantics require an explicit contract version/migration path.

## Certification target

The joint certification target is:

`EC compile → EVO Validate → EVO Plan/Diff → governed approval → EVO Deploy → EVO Export(DEFINITION_ONLY)`

and, for a clean compatible EVO target:

`Export → Validate → Deploy → Export`

must yield semantically equivalent governed definitions, modulo explicitly documented provenance/deployment metadata.
