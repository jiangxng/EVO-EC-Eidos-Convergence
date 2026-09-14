# CRCP-EC-EVO-002 — Operational Change Proposal

Status: RECONCILED CANDIDATE

Source Project: EC

Target Project: EVO

Contract Owner: EC proposal-generation/rationale/evidence/change-intent semantics; EVO target-definition/governance/publication semantics

## Problem

EC may learn that an SOP, Flow, Metric, Capability, Rule or Application definition should change, but learned intelligence cannot directly modify effective EVO definitions or invent EVO mutation semantics.

## Required Contract Change

Establish a versioned Operational Change Proposal supporting:

`EC proposal -> EVO admission/validation -> authorized governance -> approve/reject -> draft definition version -> validate/test -> publish`

Proposal includes at least:

- `target_definition_type`
- `target_definition_id`
- mandatory `base_version`
- `change_intent`
- `proposed_values` and/or `proposed_operations`
- optional `expected_effective_time`
- `evidence_refs[]`
- `impact_hypothesis`
- `compatibility_assessment`
- `migration_assessment`
- `simulation_refs[]`
- provenance and correlation/causation

Any `proposed_operations` vocabulary/schema is defined by the EVO-owned target-definition public contract. EC cannot send arbitrary ungoverned JSON Patch semantics.

Optimistic-concurrency invariant:

If the target definition has advanced beyond `base_version`, admission fails closed with a stale-base result. There is no implicit automatic rebase.

## Ownership

EC owns rationale, evidence, recommendation and change hypothesis/intent.

EVO owns target schema, allowed mutation language, draft creation, validation, approval state/enforcement, migration requirements, publication, effective dates/versioning and rollback/roll-forward.

## Why

Preserve the invariant: EC may propose change; EVO remains authority for effective operational definitions.

## Compatibility Impact

Additive initially. Published operational semantics remain unchanged until an authorized new definition version becomes effective. Existing candidate contracts remain immutable.

## Migration Impact

May require proposal/approval state and definition-version workflow, but EC never writes definition tables directly.

Externally, publication must terminate in an EVO-owned governed mutation/admission boundary. Convergence does not require EVO to implement that boundary internally as an ordinary business Command; that is EVO-internal architecture.

## Security / Authorization Impact

`PROPOSE != REVIEW != APPROVE != PUBLISH != ROLLBACK`.

Permissions are separable and auditable. High-risk definitions such as Posting Rules, Cost Policies, Authorization Rules and Financial Ledger Definitions may require elevated approval classes/policies.

## Tests Required

- proposal validation
- stale `base_version` => fail closed
- conflicting concurrent proposals
- arbitrary unsupported mutation operation rejection
- unauthorized publish rejection
- proposal valid but migration unavailable
- approval after permission revoked
- approved but publish window expired
- idempotency
- simulation-required policy violation
- published version rollback/roll-forward
- complete audit lineage

## Suggested Version

`ec.operational-change-proposal.v1` with EVO-owned target/governance admission semantics.

## Remaining Open Questions

- first definition families enabled
- target-specific mutation profile registry
- multi-party approval policy ownership
- which change classes require simulation before publication
