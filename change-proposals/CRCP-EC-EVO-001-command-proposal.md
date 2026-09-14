# CRCP-EC-EVO-001 — Command Proposal

Status: PROPOSED

Source Project: EC

Target Project: EVO

Contract Owner: EC proposal semantics / EVO admission semantics

## Problem

EC can recommend an operational action but must never turn a recommendation directly into BusinessData or bypass EVO authorization.

## Required Contract Change

Establish a versioned Command Proposal envelope carrying at least:

- proposal identity/version
- enterprise scope
- requested public EVO Command reference/version
- proposed input
- provenance/rationale/evidence references
- actor/service/on-behalf-of context where applicable
- correlation/causation
- effective time
- idempotency/admission metadata
- approval/governance requirements as declarative requirements, not authorization claims

## Why

Fix the invariant: `EC thinks/proposes; EVO authorizes/executes` without creating a second write path.

## Compatibility Impact

Additive wrapper/admission boundary around the existing EVO Command model.

## Migration Impact

No BusinessData rewrite. Introduce an adapter/admission layer and lineage from proposal to admitted/rejected Command.

## Security / Authorization Impact

EC proposal is never authorization. EVO independently authenticates/authorizes/validates. Client-supplied `authorized=true` or equivalent must never be trusted.

## Tests Required

Unauthorized rejection; stale/unsupported command version; duplicate/idempotency; policy denial; human approval when required; successful proposal -> Command -> BusinessData lineage; correlation preservation.

## Suggested Version

`ec.command-proposal.v1` with EVO-owned admission mapping.

## Open Questions

- durable proposal object vs transport envelope
- proposal retention/audit owner
- generic vs command-specific approval metadata
