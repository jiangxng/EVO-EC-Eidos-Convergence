# CRCP-EVO-EC-001 — Enterprise Observation

Status: PROPOSED

Source Project: EVO

Target Project: EC

Contract Owner: EVO

## Problem

EC's long-term learning loop needs authoritative facts and outcomes from EVO, but EC must not read EVO's database or depend on EVO internal table/module structure.

## Required Contract Change

Establish a versioned Enterprise Observation public contract covering, as applicable:

- business fact observations
- command/decision outcomes
- metric observations
- flow execution/trace
- exceptions
- provenance and lineage
- enterprise/tenant scope
- effective/event time
- source definition/contract versions

## Why

This enables `EVO fact -> observation -> EC case/outcome/lesson -> learning` while preserving system ownership.

## Compatibility Impact

Additive. Existing EVO Command/BusinessData semantics must not change.

## Migration Impact

Begin through projection/outbox/integration adapters. Historical bootstrap/backfill is a separate concern and must not couple EC to canonical tables.

## Security / Authorization Impact

Tenant/enterprise scoped. Service identity, purpose/scope, field projection/redaction and consumer authorization are mandatory. EC has no implicit superuser status.

## Tests Required

Schema/version compatibility; authorization; tenant isolation; duplicate delivery/idempotent consumption; ordering semantics where promised; redaction; historical-version fixture; lineage; outbox/recovery.

## Suggested Version

`evo.enterprise-observation.v1` (candidate naming; concrete schema version to be owned by EVO and certified here).

## Open Questions

- event vs derived-state observation separation
- raw fact projection requirements
- historical bootstrap/cursor/checkpoint model
- delivery ordering guarantees
