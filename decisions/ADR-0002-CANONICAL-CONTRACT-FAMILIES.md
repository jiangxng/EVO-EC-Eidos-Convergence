# ADR-0002 — Canonical Cross-System Contract Families

Status: PROPOSED for v0.2.1 reconciliation

## Context

Earlier work and project reviews used partially overlapping names such as `EvoIntelligenceFeed`, `Enterprise Context`, `EvoOutcome`, `Enterprise Observation`, `Command Proposal`, and `Operational Change Proposal`. Without reconciliation, independent LLMs could evolve semantically duplicate contracts.

## Decision

Use six canonical contract families as the architectural vocabulary. Existing v0.2 schemas remain historical/reference artifacts until migrated or superseded through versioned decisions.

### 1. Enterprise Context

Direction: EVO -> authorized consumers (principally EC; Eidos/Host when required).

Purpose: governed query/projection of current or requested-version operational facts, definitions, state and lineage.

This is not an event stream and not direct database access.

### 2. Enterprise Observation

Direction: EVO -> EC.

Purpose: immutable/versioned observation of facts, changes, command results, outcomes, metric observations, flow traces and exceptions for intelligence/learning.

This subsumes the architectural role previously described by overlapping `IntelligenceFeed`/`Outcome` concepts; exact migration mapping must be explicit rather than silently replacing schemas.

### 3. Command Proposal

Direction: EC -> EVO.

Purpose: propose execution of an already available operational Command.

`Proposal != authorization`. EVO performs admission, authentication/authorization, validation, idempotency and execution.

### 4. Operational Change Proposal

Direction: EC -> EVO governance.

Purpose: propose changing future effective operational definitions such as SOP, Flow, Metric, Capability, Rule or Application definitions.

This is distinct from Command Proposal:

- Command Proposal = what should be executed now.
- Operational Change Proposal = how the enterprise runtime should operate in a future effective version.

`PROPOSE != APPROVE != PUBLISH`.

### 5. Enterprise Simulation

Direction: EC <-> EVO.

EC owns scenario/hypothesis/reasoning semantics. EVO owns deterministic enterprise consequence calculation exposed through a versioned simulation contract. Simulation must remain isolated from Actual operational truth.

### 6. Experience / Action

Direction: EC -> Eidos -> Host -> EVO.

- EC produces Experience Proposal.
- Eidos owns public experience validation/realization semantics.
- Eidos produces ActionRequest from human interaction.
- Host Adapter maps the request to the applicable EVO public Command contract.
- EVO re-authorizes, validates and executes.

Human confirmation is not equivalent to EVO authorization.

## Shared Envelope Concerns

All applicable families must converge on shared semantics for:

- enterprise/tenant scope
- actor/service/delegation context
- contract version
- correlation_id
- causation_id
- lineage/provenance
- effective/event time
- idempotency where applicable
- error envelope
- capability/version negotiation
- sensitive-field projection/redaction

## Consequences

New CRCPs should use this vocabulary. Older names are not deleted from historical releases. Migrations are explicit and compatibility-tested.
