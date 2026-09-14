# CRCP-EIDOS-EVO-001 — ActionRequest to EVO Command

Status: PROPOSED

Source Project: Eidos

Target Project: EVO / Host boundary

Contract Owner: Eidos ActionRequest semantics; EVO Command admission; Host mapping is integration responsibility

## Problem

Eidos produces human interaction actions but must not call EVO internal services or treat a client confirmation as business authorization.

## Required Contract Change

Formalize:

`Eidos ActionRequest -> Host Adapter -> EVO public Command`

ActionRequest expresses neutral interaction information such as action target, submitted values, interaction context, human confirmation and correlation. Host maps against published/versioned public Command metadata. EVO performs final authentication, authorization, validation, idempotency and execution.

## Why

Preserve `Eidos interacts; EVO executes` and prevent UI/runtime coupling to EVO internals.

## Compatibility Impact

Additive integration boundary.

## Migration Impact

No business-data migration. Existing Eidos ActionRequest candidate schema should be reconciled/versioned rather than silently rewritten.

## Security / Authorization Impact

Human confirmation is not authorization. Never trust a client assertion equivalent to `authorized=true`. Host identity/delegation and EVO authorization are explicit.

## Tests Required

ActionRequest -> Command golden fixture; invalid schema; expired definition/command version; permission denial; duplicate submit/idempotency; correlation preservation; tampered client authorization claim; unsupported action mapping.

## Suggested Version

`eidos.action-request.v1` mapped to an EVO-owned public Command version.

## Open Questions

- deployment/ownership of Host Adapter
- neutral projection of EVO CommandDefinition metadata
- offline client semantics
- how Eidos discovers compatible action targets/capabilities
