# CRCP-EIDOS-EVO-001 — Host-Neutral ActionRequest and EVO Integration Profile

Status: RECONCILED CANDIDATE

Source Project: Eidos

Target Project: Host boundary; EVO is one certified execution profile

Contract Owner: Eidos ActionRequest semantics; Host mapping semantics; EVO owns Command admission for the EVO profile

## Problem

Eidos emits deterministic semantic interaction requests but must not become an EVO-specific frontend, call EVO internal services, or treat client confirmation as business authorization.

## Required Contract Change

Universal boundary:

`Human/System interaction -> Eidos ActionRequest -> Host`

An ActionRequest is Host-neutral. A Host may map it to EVO, another authorized enterprise service, local deterministic host behavior, navigation, collaboration/document operations or a future execution substrate.

For the EVO integration profile:

`Eidos ActionRequest -> Host Adapter -> EVO public Command`

ActionRequest carries at least:

- `action_request_id`
- `contract_version`
- `experience_instance_id`
- `experience_contract_version`
- `capability_id`
- `capability_version`
- `action_semantic`
- `action_contract_id`
- `action_contract_version`
- neutral `action_target_ref`
- `interaction_context`
- `submitted_values`
- optional `confirmation_evidence`
- `actor_context_ref`
- `correlation_id`
- `causation_id`
- `occurred_at`
- optional `idempotency_key`
- optional `host_mapping_hint`
- optional `presented_state_etag`
- optional `presented_definition_version`

Confirmation evidence, where applicable, can include `confirmed_at`, `interaction_instance_id`, `actor_ref`, `confirmation_method`, `presented_contract_version` and `presented_data_version`.

## Trust Boundary

Eidos can attest that an interaction occurred under a particular Experience instance. It cannot attest that the actor is authorized for the resulting business mutation.

ActionRequest MUST NOT carry trusted client-originated assertions such as `authorized=true`, `permission_granted=true`, arbitrary trusted business-role claims, or executable callback/code.

For EVO, Host maps `action_target_ref` against a public/versioned EVO CommandDefinition projection; EVO independently authenticates, authorizes, validates state/schema/idempotency and executes.

## TOCTOU / Staleness

Presented state and definition/version evidence allows Host/EVO to detect that what the human confirmed differs from current executable state. Stale confirmation handling is policy/Command-specific and must fail closed where the target requires optimistic validation.

## Compatibility Impact

Existing `eidos-action-request-v0.1` remains immutable. Introduce an explicit adapter to the canonical Host-neutral contract where semantics can be preserved.

## Migration Impact

No business-data migration. Host adapters are independently versioned/certified profiles.

## Security / Authorization Impact

Human confirmation is evidence, not authorization. Host identity/delegation and target execution authorization are explicit. Submitted values, target mapping and presentation-state evidence are integrity-sensitive.

## Tests Required

- host-neutral ActionRequest schema/fixture
- ActionRequest -> EVO Command profile fixture
- invalid/unknown capability/action contract
- stale presented state
- stale presented definition/Command version
- confirmation actor != execution actor
- revoked delegated actor
- tampered submitted values after confirmation
- host mapping changed between render/action
- replayed/duplicate ActionRequest
- correlation/causation preservation
- client authorization-claim tampering
- unsupported action mapping

## Suggested Version

`eidos.action-request.v1` plus separately certified Host mapping profiles.

## Remaining Open Questions

- deployment/ownership of each Host Adapter
- neutral public target discovery model
- offline client semantics
- integrity/signature profile for confirmation evidence where required
