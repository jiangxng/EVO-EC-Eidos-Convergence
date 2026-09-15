# CRCP-EVO-EC-001 — Enterprise Observation

Status: RECONCILED CANDIDATE

Source Project: EVO

Target Project: EC

Contract Owner: EVO

## Problem

EC's long-term learning loop needs authoritative operational facts/outcomes from EVO, but EC must not read EVO's database or depend on EVO internal table/module structure.

## Required Contract Change

Establish a versioned Enterprise Observation public contract. The semantic observation record includes at least:

- `observation_id`
- `observation_type`
- `observation_version`
- `enterprise_id`
- `source_object_type`
- `source_object_id`
- optional `source_object_version`
- `effective_at`
- `observed_at`
- `published_at`
- `correlation_id`
- `causation_id`
- `source_definition_versions`
- `source_contract_versions`
- `payload`
- `provenance`
- `redaction_profile`

Delivery metadata is transport metadata and is not part of observation identity.

Mandatory invariants:

- `observation_id != delivery_id`
- `effective_at`, `observed_at`, and `published_at` are distinct semantics
- retry/replay may deliver the same observation more than once
- EC consumption must therefore be idempotent by observation identity

Observation types may cover business facts, command/decision operational outcomes, metric observations, flow traces/execution and exceptions.

## Why

This enables `EVO fact -> observation -> EC case/outcome/lesson -> learning` while preserving system ownership and replay/backdated/delayed-delivery semantics.

## Compatibility Impact

Additive to EVO runtime. Existing BusinessData/Command semantics do not change. Existing v0.2 candidate feed/outcome schemas remain immutable and require explicit adapters/migration mapping.

## Migration / Rollback

Initial path:

`EVO internal operational truth -> governed projection -> outbox -> observation adapter v1`

Rollback disables publisher/consumer/adapters; it never rewrites BusinessData.

Historical bootstrap is a separate governed endpoint/contract/profile and must never mean EC scans EVO DB directly.

## Security / Authorization Impact

Tenant/enterprise scoped. Service identity, purpose/scope, sensitive dimension/customer/employee/financial projection, redaction policy version and consumer authorization are mandatory. EC has no implicit superuser status.

## Tests Required

- schema/version compatibility
- same observation delivered twice
- deterministic projection of same source fact
- backdated `effective_at`
- delayed/out-of-order delivery
- redacted vs privileged projection
- consumer checkpoint recovery
- unsupported observation version
- cross-tenant injection rejection
- lineage/provenance preservation
- outbox/recovery behavior

## Suggested Version

`evo.enterprise-observation.v1`

## Remaining Open Questions

- event vs derived-state observation subtype model
- raw fact projection requirements
- historical bootstrap/cursor/checkpoint contract
- delivery ordering guarantees by transport profile
