# EVO Convergence Handoff

Status: v0.2.1 reconciliation input

## Canonical Role

EVO is the deterministic enterprise runtime and system of operational truth.

Preserve current implementation assets. Correct ownership wording and cross-system boundaries rather than replacing the repository.

## Current Alignment

Keep Command -> BusinessData -> Posting -> Ledger/Cost/Runtime State and deterministic Replay semantics.

Narrow/clarify:

- Capability -> Operational Capability.
- Flow -> Definition / Instance / Trace / Lineage; intelligence belongs to EC.
- Metrics -> definitions, deterministic calculation, values/history/lineage; interpretation/learning belongs to EC.
- SOP -> Published SOP Runtime Definition; SOP Intelligence belongs to EC.
- AI module -> external intelligent-actor access adapter, not enterprise intelligence/learning.
- Management Intelligence -> EC; EVO retains Management Runtime semantics.
- Simulation -> deterministic consequence calculation only; EC owns scenario reasoning.

## Cross-Repo Priorities

1. Enterprise Context public boundary.
2. Enterprise Observation public boundary.
3. Command Proposal admission mapping without a second write path.
4. Operational Change Proposal governance/admission.
5. Enterprise Simulation contract with strict Actual/Hypothetical isolation.
6. ActionRequest -> Host -> EVO Command mapping.
7. Shared identity/delegation, correlation/causation/lineage, error and version negotiation conventions.

## Non-Negotiable Constraints

- EC/Eidos do not read/write EVO database directly.
- EC/Eidos do not import EVO internal modules.
- EC proposal is never authorization.
- Eidos confirmation is never authorization.
- All operational mutation ends at the normal EVO Command boundary.
