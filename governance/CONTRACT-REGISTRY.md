# Cross-Repository Contract Registry v0.2.1

Status: Reconciliation Candidate

This registry records canonical architectural families and current candidate public-contract direction. It does not mutate historical v0.2 schemas.

| Family / Profile | Direction | Owner | Candidate version | v0.2 relationship |
|---|---|---|---|---|
| Enterprise Context | EVO -> authorized consumer | EVO | `evo.enterprise-context.v1` TBD | explicit mapping from `EvoIntelligenceFeedV010` where semantics match; feed-only semantics must not be guessed |
| Enterprise Observation | EVO -> EC | EVO | `evo.enterprise-observation.v1` | supersedes overlapping feed/outcome roles through adapters; historical schemas immutable |
| Command Proposal | EC -> EVO | EC envelope / EVO referenced Command+admission | `ec.command-proposal.v1` | explicit adapter from `EvoCommandProposalV010` candidate naming/shape |
| Operational Change Proposal | EC -> EVO governance | EC intent / EVO target+governance | `ec.operational-change-proposal.v1` | new canonical boundary |
| Enterprise Simulation | EC <-> EVO | EC scenario / EVO deterministic calculation | `evo.enterprise-simulation.v0.1` | new canonical boundary; Replay is not a migration target |
| Experience Proposal | EC -> Eidos | Eidos public validation/admissibility / EC producer intent | `eidos.experience-proposal.v1` | explicit adapter from `EcExperienceProposalV010` where semantics survive |
| ActionRequest | Eidos -> Host | Eidos | `eidos.action-request.v1` | explicit adapter from v0.1 candidate; canonical contract is Host-neutral |
| EVO Action Mapping Profile | Host -> EVO | Host integration / EVO Command owner | TBD | evolves v0.2 direct EVO-oriented ActionRequest assumption into certified mapping profile |
| Shared Envelope Profile | cross-cutting | Convergence semantics / product runtime owners | `convergence.shared-envelope.v0.1` | additive normalization/adapters |

## Registry Rules

1. Historical v0.2 contracts are immutable.
2. `supersedes` means architectural role replacement, not byte/schema compatibility.
3. Every adapter must declare which semantics are preserved, transformed, defaulted or unsupported.
4. Unsupported semantics fail closed or use an explicitly declared deterministic fallback.
5. Contract/version capability support is certified by tests and Compatibility Matrix, not inferred from product version.
