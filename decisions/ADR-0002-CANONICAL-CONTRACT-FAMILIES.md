# ADR-0002 — Canonical Cross-System Contract Families

Status: PROPOSED for v0.2.1 reconciliation

## Context

Earlier work and project reviews used partially overlapping names such as `EvoIntelligenceFeed`, `Enterprise Context`, `EvoOutcome`, `Enterprise Observation`, `Command Proposal`, and `Operational Change Proposal`. Without reconciliation, independent LLMs could evolve semantically duplicate contracts.

## Decision

Use six canonical architectural contract families. Existing v0.2 schemas remain immutable historical/reference artifacts until explicitly migrated or superseded.

### 1. Enterprise Context

Direction: EVO -> authorized consumers (principally EC; Eidos/Host when required).

Purpose: governed query/projection of current or requested-version operational facts, definitions, state and lineage.

This is not an event stream and not direct database access.

### 2. Enterprise Observation

Direction: EVO -> EC.

Purpose: immutable/versioned observation of facts, changes, command results, operational outcomes, metric observations, flow traces and exceptions for intelligence/learning.

Important identity rule:

`observation_id != delivery_id`

An observation is a semantic record. A delivery message is transport. The same observation may be delivered repeatedly through retry/replay.

Time semantics must distinguish, where relevant:

`effective_at != observed_at != published_at`

This family subsumes the architectural role previously described by overlapping `IntelligenceFeed`/`Outcome` concepts; exact migration mapping must be explicit rather than silently replacing schemas.

### 3. Command Proposal

Direction: EC -> EVO.

Purpose: propose execution of an already available operational Command.

EC owns the recommendation/proposal envelope. EVO owns the semantic meaning and input schema of the referenced Command.

`Proposal != authorization != execution`.

### 4. Operational Change Proposal

Direction: EC -> EVO governance.

Purpose: propose changing future effective operational definitions such as SOP, Flow, Metric, Capability, Rule or Application definitions.

- EC owns rationale/evidence/recommendation/change intent.
- EVO owns target schemas, allowed mutation language, validation, governance state, approval enforcement, publication, effective versioning and rollback/roll-forward.

`Command Proposal = what should be executed now.`

`Operational Change Proposal = how the enterprise runtime should operate in a future effective version.`

`PROPOSE != REVIEW != APPROVE != PUBLISH != ROLLBACK`.

### 5. Enterprise Simulation

Direction: EC <-> EVO.

EC owns scenario/hypothesis/reasoning semantics. EVO owns deterministic enterprise consequence calculation exposed through a versioned simulation contract.

`Replay != Simulation`.

Simulation runs in a `HYPOTHETICAL` namespace and must never mutate or become addressable as Actual BusinessData, Ledger, balance or posting state.

A reproducible simulation pins baseline Actual snapshot/reference, business time and applicable definition/rule/valuation/metric versions.

### 6. Experience / Action

This is one architectural family containing two independent contracts with different owners, trust models and lifecycles.

#### 6A. Experience Proposal

Direction: EC -> Eidos.

- EC produces semantic Experience intent.
- Eidos owns public validation/admissibility semantics, capability compatibility, Experience Integrity and deterministic realization.

Experience Proposal is not business authorization and must not bypass Eidos mandatory evidence, accessibility, shared-core, Decision Integrity or other constitutional constraints.

#### 6B. ActionRequest

Direction: Eidos -> Host.

ActionRequest is Host-neutral. It represents a deterministic semantic interaction occurrence/request, not inherently an EVO Command request.

For the EVO integration profile:

`Eidos ActionRequest -> Host Adapter -> EVO public Command`

EVO independently authenticates, authorizes, validates and executes.

Human confirmation is evidence, not business authorization.

## Shared Envelope Semantic Profiles

All applicable families reuse shared semantic profiles for:

- enterprise/tenant scope
- actor/service/delegation context
- contract identity/version
- correlation / causation / trace context
- business lineage / provenance
- effective/event/message times
- request/message identity
- idempotency where applicable
- cross-system error envelope
- capability/version negotiation
- sensitive-field projection/redaction

These profiles are reusable cross-cutting semantics, **not additional business contract families**.

`causation != authorization` and `correlation != business lineage`.

## Consequences

New CRCPs use this vocabulary. Older names are not deleted from historical releases. Migrations are explicit and compatibility-tested.
