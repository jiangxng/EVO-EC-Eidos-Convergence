# Cross-Repository Ownership Manifest v0.1

Status: Proposed for Architecture Convergence v0.2.1

## Canonical Boundary

> EC thinks, learns and improves. EVO executes. Eidos interacts.

## EVO Ownership

EVO owns deterministic operational truth and execution:

- Business facts / BusinessData
- Command admission, authorization, validation and execution
- Effective operational definitions
- Operational Capability definitions
- Published SOP Runtime definitions
- Flow definitions, instances, traces and lineage
- Metric definitions, deterministic calculation, values, history and lineage
- Ledger, balances, cost, valuation and deterministic runtime state
- Deterministic replay
- Deterministic enterprise consequence/simulation engines
- Governed enterprise queries
- Enterprise observations/outcomes sourced from operational truth

EVO does not own long-term enterprise learning, management intelligence, persistent reasoning, experience planning or personalization intelligence.

## EC Ownership

EC owns persistent enterprise intelligence:

- Knowledge and provenance
- Enterprise and industry memory
- Cases, decisions, outcomes, lessons and patterns
- Learning and learning methods
- Research and evidence acquisition
- Reasoning, diagnosis and recommendation
- Scenario/hypothesis design and interpretation
- Context compilation
- SOP / Metric / Flow / Capability Intelligence
- Management Intelligence
- Enterprise Intelligence Packs
- Enterprise Function Packs
- Knowledge Merge
- Long-term user/enterprise understanding where governed
- Production of Experience Proposals for Eidos
- Production of Command Proposals and Operational Change Proposals for EVO

EC does not own EVO authorization or operational truth and must not write EVO internal state directly.

## Eidos Ownership

Eidos owns deterministic experience realization:

- Experience public contract validation
- Experience capability catalog
- Experience composition/resolution
- Deterministic experience runtime and rendering
- Interaction semantics
- Human confirmation semantics
- ActionRequest production
- Standard fallback behavior

Eidos does not own enterprise truth, business authorization/execution, persistent enterprise learning, EC knowledge, or a competing long-term user-intelligence model.

## Convergence Workspace Ownership

Convergence owns cross-repository governance artifacts, not product runtime behavior:

- Contract registry and mirrored/certified schemas
- Cross-repository ownership manifest
- Compatibility matrix
- CRCP workflow
- Cross-repository ADRs
- Golden fixtures
- Contract and integration tests
- Reference enterprise packs used for convergence testing
- Cross-system deployment/certification guidance

## Contract Ownership

| Contract family | Canonical owner | Principal consumers/producers |
|---|---|---|
| EVO Command | EVO | EC proposals, Eidos/Host actions, automation, humans |
| Enterprise Context | EVO | EC, Eidos/Host as authorized |
| Enterprise Observation | EVO | EC |
| Enterprise Simulation | EVO owns deterministic calculation contract; EC owns scenario reasoning semantics | EC |
| Command Proposal | EC owns proposal semantics; EVO owns admission mapping | EC -> EVO |
| Operational Change Proposal | EC owns intelligence proposal semantics; EVO owns operational governance/admission | EC -> EVO |
| Experience Proposal | Eidos owns validation/public experience contract; EC produces | EC -> Eidos |
| ActionRequest | Eidos owns interaction request contract; Host maps; EVO owns final Command admission | Eidos -> Host -> EVO |
| Enterprise Intelligence Pack | EC | EVO/Eidos publishers consume compiled outputs |
| Enterprise Function Pack | EC | EC lifecycle; publishers may consume compiled outputs |
| Knowledge Merge | EC | EC instances |

When a contract spans ownership concerns, the public schema must explicitly separate fields/semantics by owner rather than creating ambiguous shared ownership.
