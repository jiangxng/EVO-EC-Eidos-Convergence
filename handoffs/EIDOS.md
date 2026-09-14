# Eidos Convergence Handoff

Status: v0.2.1 reconciliation input

## Canonical Role

Eidos is the deterministic experience and interaction runtime.

It validates and realizes experience proposals using explicit, versioned, discoverable and composable capabilities. It does not own enterprise operational truth or persistent enterprise learning.

## Eidos Owns

- Experience public contract validation
- Experience Capability Catalog
- Experience composition/resolution
- Deterministic experience runtime/rendering
- Interaction semantics
- Human confirmation semantics
- ActionRequest production
- Standard fallback behavior

## Eidos Does Not Own

- EVO business facts or operational definitions as an alternate source of truth
- EVO authorization or Command execution
- EC knowledge, enterprise memory or long-term learning
- a competing long-term personalization/user-intelligence brain
- arbitrary business mutation outside Host/EVO public boundaries

## Canonical Action Boundary

`Human -> Eidos interaction -> ActionRequest -> Host Adapter -> EVO Command -> EVO authorization/validation/execution`

Human confirmation is evidence of an interaction step; it is not final business authorization.

## EC Boundary

`EC Experience Proposal -> Eidos validation -> deterministic resolution/realization`

Personalization intelligence may be proposed by EC. Eidos must not silently learn a competing persistent profile.

## Cross-Repo Priorities

- Formalize ActionRequest public contract ownership and neutral semantics.
- Define Host Adapter mapping to versioned EVO Command metadata without depending on EVO internals.
- Preserve correlation/causation/interaction context through the action path.
- Keep query/action boundaries separate from Eidos rendering internals.
