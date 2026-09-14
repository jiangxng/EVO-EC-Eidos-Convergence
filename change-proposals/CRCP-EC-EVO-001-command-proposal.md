# CRCP-EC-EVO-001 — Command Proposal

Status: RECONCILED CANDIDATE

Source Project: EC

Target Project: EVO

Contract Owner: EC recommendation/proposal envelope; EVO referenced Command semantics/input schema/admission

## Problem

EC can recommend an operational action but must never define EVO Command semantics, turn a recommendation directly into BusinessData, or bypass EVO authorization.

## Required Contract Change

Establish a versioned Command Proposal envelope carrying at least:

- `proposal_id`
- `proposal_created_at`
- optional `proposal_expires_at`
- `proposal_basis_version`
- enterprise scope
- `command_contract_id`
- `command_contract_version`
- `command_code`
- `input_schema_version`
- `proposed_input`
- `evidence_refs[]`
- provenance/rationale
- optional intelligence `confidence`
- optional advisory `required_human_decision`
- actor/service/on-behalf-of context where applicable
- correlation/causation
- effective business time
- `command_idempotency_key`

`proposed_input` MUST validate against the EVO-published schema identified by the proposal. EC does not define that schema.

`proposal_id != command_idempotency_key`.

The same proposal may participate in review/rejection/reconsideration; admitted execution obeys EVO Command idempotency independently.

## Why

Fix the invariant: `EC thinks/proposes; EVO owns Command meaning and authorizes/executes`, without creating a second write path.

## Compatibility Impact

Additive wrapper/admission boundary around the existing EVO Command model. Existing v0.2 proposal schema remains immutable and is migrated through an explicit adapter.

## Migration Impact

No BusinessData rewrite. Introduce an adapter/admission layer and lineage from proposal to admitted/rejected Command.

## Security / Authorization Impact

EC proposal is never authorization. EVO independently authenticates, authorizes and validates current state/permissions.

The proposal MUST NOT contain trusted authorization-result semantics such as `authorized`, `permission_granted`, `approved`, or an EC-authored EVO authorization state. Human-review requirements are advisory/governance intent only.

## Tests Required

- valid proposal but invalid EVO Command payload
- valid proposal but revoked actor/delegation
- proposal expired
- Command contract/input schema version retired
- same proposal admitted twice
- same proposal mapped to a different Command => reject
- proposal vs Command idempotency independence
- evidence unavailable while Command remains independently valid
- policy denial / human approval where required
- proposal -> Command -> BusinessData lineage
- correlation/causation preservation

## Suggested Version

`ec.command-proposal.v1` with EVO-owned Command admission mapping.

## Remaining Open Questions

- durable proposal object vs transport envelope
- proposal retention/audit owner
- generic vs command-specific governance metadata
