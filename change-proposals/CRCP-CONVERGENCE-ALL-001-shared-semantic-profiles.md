# CRCP-CONVERGENCE-ALL-001 — Shared Cross-System Semantic Profiles

Status: RECONCILED CANDIDATE

Source Project: Architecture Convergence

Target Projects: EVO / EC / Eidos / Host integrations

Contract Owner: Convergence governs cross-system profile semantics; product identity/authorization/runtime internals remain product-owned

## Problem

Identity, delegation, correlation, causation, lineage, errors and capability negotiation recur across multiple contracts. Independent definitions will drift and break auditable causal chains and gray upgrades.

## Decision Shape

Create one Shared Envelope architecture profile composed from four reusable semantic profiles. These are cross-cutting semantics, **not a seventh business contract family and not a fourth runtime service**.

### Profile A — Identity / Actor / Service / Delegation

Portable semantics include:

- `enterprise_id`
- `actor_id`
- `actor_type`
- optional `service_id`
- optional `delegated_by`
- optional `delegation_scope`
- `purpose`
- `issued_at`
- optional `expires_at`

The canonical profile must not require a specific JWT, IdP, session implementation or authorization engine.

Identity/delegation context carries claims/evidence/context. EVO or another target execution authority decides permission.

### Profile B — Correlation / Causation / Lineage

Portable semantics include:

- `trace_id`
- `correlation_id`
- `causation_id`
- `root_id`
- `source_system`
- `source_record_ref`
- `business_object_refs[]`
- provenance references where applicable

Invariants:

- `causation != authorization`
- `correlation != business lineage`
- transport retry identity != semantic record identity

### Profile C — Cross-System Error Envelope

Portable semantics include:

- `error_id`
- `code`
- `category`
- `message`
- `retryable`
- `source_system`
- `contract_id`
- `contract_version`
- `correlation_id`
- structured `details`

Initial categories:

`VALIDATION`, `AUTHENTICATION`, `AUTHORIZATION`, `CONFLICT`, `VERSION_UNSUPPORTED`, `STALE_STATE`, `RATE_LIMIT`, `TRANSIENT`, `INTERNAL`.

Product-specific codes remain owner-defined; the shared envelope prevents unstructured cross-system error strings.

### Profile D — Contract Capability Negotiation

Portable semantics include:

- `supported_contracts[]`
- `supported_contract_versions[]`
- `capabilities[]`
- `deprecated_contracts[]`

Product version alone must never be used to infer cross-system capability support.

This profile supports N/N-1 compatibility, adapters, canary/gray rollout and fail-closed unsupported-version behavior.

## Why

`EVO -> EC`, `EC -> Eidos`, and `Eidos -> Host -> EVO` must preserve an auditable causal chain without creating shared runtime coupling.

## Compatibility Impact

Additive initially. Existing v0.1/v0.2 candidate envelopes remain immutable and use adapters/normalizers.

## Migration Impact

Gradual envelope normalization per contract family. Products may keep internal identity/error/tracing representations behind adapters.

## Security / Authorization Impact

Critical: shared identity/delegation fields are not self-authenticating authorization. Consumers validate trust according to their own security boundary. Tenant isolation, spoofing, delegation expiry/revocation and redaction are mandatory concerns.

## Tests Required

- identity spoofing rejection
- delegation expiry/revocation
- cross-tenant injection
- causal-chain preservation across EC -> Eidos -> Host -> EVO
- correlation vs lineage distinction
- duplicate delivery identity handling
- unknown contract/version fail closed
- malformed context
- structured error preservation through adapters
- N/N-1 capability negotiation
- deprecated/unsupported capability behavior
- cross-contract golden fixtures

## Suggested Version

Architecture profile: `convergence.shared-envelope.v0.1`

Subprofiles may be independently versioned while the composition profile pins compatible versions.

## Remaining Open Questions

- opaque vs portable delegation evidence
- trust/signature profile between deployments
- error detail redaction rules
- negotiation transport/discovery mechanism
