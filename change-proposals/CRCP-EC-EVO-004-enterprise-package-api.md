# CROSS-REPO-CHANGE-PROPOSAL

**Proposal ID:** `CRCP-EC-EVO-004`

**Status:** PROPOSED

**Source Project:** EC (Experience Compiler)

**Target Project:** EVO

**Contract Owner:** EVO

## Problem

EC needs a stable, machine-readable way to compile enterprise knowledge into an EVO-deployable Enterprise Package without knowing or depending on EVO internal tables, migrations, seed scripts, or implementation details.

EVO has two distinct product layers relevant to this boundary:

1. **EVO Instance** — one deployed instance represents and runs one concrete enterprise.
2. **EVO Market** — distributes reusable Enterprise Packages that can be validated and deployed into EVO instances.

The Enterprise Package format, object definitions, schemas, compatibility rules, and deploy/export semantics are EVO-owned runtime contracts. EC must consume these contracts rather than inventing a parallel package format.

A second requirement is round-trip portability: an existing EVO enterprise must be exportable/backed up as an Enterprise Package that preserves how the enterprise is defined and operated while excluding commercial/transactional business data by default.

## Required Contract Change

EVO should expose a versioned public Enterprise Package API surface with at least the following contract capabilities. Exact endpoint naming and internal implementation remain EVO-owned.

### 1. Package Schema / Capability Discovery

Provide machine-readable APIs that allow EC, EVO Market, tooling, and other authorized consumers to discover:

- Enterprise Package format/version;
- supported EVO runtime versions and compatibility range;
- supported package object types;
- authoritative schema for each object type;
- required/optional fields;
- reference/dependency semantics;
- validation constraints and invariants;
- extension/versioning rules;
- supported runtime capabilities relevant to package compilation.

Conceptual operations:

- `GetEnterprisePackageSchema(version?)`
- `GetEnterprisePackageCapabilities()`

The schema returned by EVO is authoritative. EC must compile to it; EC does not own or redefine it.

### 2. Package Validation

Provide a side-effect-free validation operation before deployment.

Conceptual operation:

- `ValidateEnterprisePackage(package)`

Validation should cover at minimum schema validity, semantic references, dependencies, runtime compatibility, version compatibility, and governed invariants. Errors should be stable and machine-readable so EC can repair/recompile a rejected package.

### 3. Package Deployment

Provide a governed API for deploying an Enterprise Package into an EVO Instance.

Conceptual operation:

- `DeployEnterprisePackage(enterprise_scope, package, expected_base_version?)`

The public contract should support deterministic validation/planning before mutation, authorization, idempotency, package identity/version, dependency resolution, and a published resulting enterprise-definition version. EVO remains the authority that accepts/rejects/publishes operational definitions.

EC supplying a valid package MUST NOT imply authorization to deploy it.

### 4. Enterprise Package Export / Backup

Provide an API to export an existing EVO Instance's enterprise definition as a portable Enterprise Package.

Conceptual operation:

- `ExportEnterprisePackage(enterprise_scope, mode=DEFINITION_ONLY)`

The default portable/backup package requested by EC must represent **how the enterprise is configured to operate**, not **what commercial events have occurred**.

The exported definition package should include all EVO-owned package-supported definitions necessary for deterministic re-validation/re-deployment, subject to EVO's canonical schema. Candidate categories include enterprise metadata needed for package identity, domains, capabilities, applications, command definitions/schemas, flows, SOP definitions, metrics, dimensions, ledger definitions, posting rules, cost/valuation policies, authorization/role templates where portable, dependencies, versions, and lineage/provenance metadata.

The default `DEFINITION_ONLY` export MUST exclude commercial/transactional runtime data such as customer/supplier transactions, sales/purchase orders, operational BusinessData history, LedgerEntries, CostResults, WorkItems, balances/projections, and other enterprise-sensitive actual-state data unless a future separately governed export mode explicitly defines otherwise.

### 5. Round-trip Semantics

EVO should define the expected semantic round-trip property:

`Export(DEFINITION_ONLY, Enterprise A) -> Validate -> Deploy to clean compatible EVO instance`

should recreate an equivalent governed enterprise operating definition, modulo explicitly documented instance-local identities/secrets/runtime state.

Byte-for-byte equality is not required; semantic equivalence and deterministic compatibility evidence are.

## Why

This contract is required for the core EC ↔ EVO division of responsibility:

- EVO owns executable enterprise semantics, package schema, validation, publication, authorization, and runtime truth.
- EC owns understanding, learning, industry knowledge, reasoning, and compilation of knowledge into proposals/packages that conform to EVO's published contract.
- EVO Market distributes EVO-owned Enterprise Packages rather than EC-private representations.

Without this boundary, each new enterprise/industry risks requiring EVO-internal seed scripts or direct implementation changes, which would prevent Enterprise Packages from becoming portable, market-distributable, versioned enterprise operating models.

This API is also required for EC learning workflows: EC must be able to consume a definition-only export of how a real enterprise is configured without requiring access to its commercial transaction history.

## Compatibility Impact

**Additive** as a new public contract family if introduced without changing existing Command/Observation contracts.

The package schema itself must be explicitly versioned. Breaking schema or semantic changes require a new package contract version plus compatibility/migration rules.

EC should negotiate supported package/schema versions rather than assume `latest`.

## Migration Impact

No migration is required for EC until EVO publishes the first supported package contract.

For EVO, existing bootstrap/seed-defined enterprise metadata may need a canonical projection/export path into the new Enterprise Package representation. This proposal does not prescribe EVO's internal storage or migration implementation.

EVO Market should store/distribute packages that declare their package schema version and EVO compatibility requirements.

## Security / Authorization Impact

- Schema/capability discovery may be broadly readable, but EVO decides exposure policy.
- Validate is side-effect-free and must not grant deploy authority.
- Deploy requires EVO authorization in the target enterprise/instance scope.
- Export requires explicit authorization for the source enterprise.
- `DEFINITION_ONLY` export must fail closed against accidental inclusion of commercial/transactional data, secrets, credentials, tokens, personal data, or instance-local sensitive configuration.
- Portable authorization templates must be distinguished from live identities, credentials, grants, and secrets.
- EC identity/delegation evidence is not EVO authorization.

## Tests Required

1. **Schema discovery test** — a fresh EC consumer can obtain a pinned package schema/version without EVO internal knowledge.
2. **Golden package validation** — a minimal valid package passes; broken references/schema/dependencies fail with stable machine-readable errors.
3. **Deploy test** — valid package deploys to a clean EVO Instance and produces a published enterprise-definition version.
4. **Authorization test** — valid package + unauthorized actor fails closed.
5. **Idempotency test** — retrying the same deploy request does not duplicate enterprise definitions.
6. **Definition-only export test** — exported package contains governed definitions and contains no BusinessData/LedgerEntry/CostResult/WorkItem/commercial actuals or secrets.
7. **Round-trip test** — deploy Package P -> export definition-only P' -> deploy P' into clean compatible instance -> semantic enterprise-definition equivalence.
8. **Version negotiation test** — unsupported package/runtime versions fail explicitly; supported N/N-1 behavior follows declared compatibility policy.
9. **EC consumer contract test** — EC compiles a minimal package using only EVO-discovered schema/capabilities and receives successful validation without reading EVO internal code/schema.
10. **EVO Market portability test** — the same signed/versioned package artifact can be retrieved from Market and validated/deployed through the same public EVO contract.

## Suggested Version

Introduce as **Enterprise Package Contract v0.1** (experimental/additive) and stabilize after the first minimal round-trip implementation.

For agile validation, the first implementation should deliberately be small: Schema Discovery -> EC compiles one minimal package -> Validate -> Deploy into clean instance -> Export DEFINITION_ONLY -> Validate/Deploy round-trip. Do not require the full EVO Market implementation before this contract can be tested.

## Open Questions

1. What is the canonical term: `Enterprise Package`, `Operational Pack`, or another EVO-owned name? EC currently uses `Enterprise Package` for this request.
2. Is an EVO Instance strictly one enterprise, or may one runtime host multiple isolated enterprise scopes while preserving the same package semantics?
3. Which definition categories are mandatory in Package v0.1 versus optional/extensions?
4. How should package dependencies and composition be represented for EVO Market (single monolithic package vs composable packages)?
5. What constitutes semantic equivalence for round-trip certification?
6. Which identifiers are portable/stable across export/import and which must be rebound at deployment?
7. How are secrets/external connector credentials represented: omitted, referenced, or deployment-bound placeholders?
8. Should deploy expose an explicit `Plan/Diff` operation before commit?
9. What signing/provenance requirements should EVO Market impose on packages?
10. How does package upgrade/rollback relate to EVO's existing versioned definitions and replay guarantees?

## Resolution

Pending EVO Owner reconciliation. Expected outcomes: ACCEPTED / REJECTED / SUPERSEDED / DEFERRED, with related ADR, canonical contract, schema version, and implementation/certification evidence.