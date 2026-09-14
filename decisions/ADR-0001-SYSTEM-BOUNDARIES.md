# ADR-0001 — Canonical EVO × EC × Eidos System Boundaries

Status: PROPOSED for v0.2.1 reconciliation

## Context

EVO, EC and Eidos evolved independently and contain terminology that can imply overlapping responsibility. Cross-repository integration requires a durable boundary independent of chat history or a particular LLM.

## Decision

The canonical boundary is:

> EC thinks, learns and improves. EVO executes. Eidos interacts.

More precisely:

- EVO is the deterministic enterprise runtime and system of operational truth.
- EC is the persistent enterprise intelligence system and long-term learning substrate.
- Eidos is the deterministic experience and interaction runtime.
- LLMs are replaceable reasoning engines and development collaborators; they are not durable architecture authority.
- EC may learn at runtime. EVO and Eidos must not independently form competing long-term enterprise learning/intelligence systems.
- EC may propose changes/actions, but proposals never bypass EVO governance, authorization, validation or Command semantics.
- Eidos human confirmation is interaction evidence, not business authorization.
- Cross-system communication uses versioned public contracts. No direct database coupling or internal-module imports are permitted.

## Consequences

Existing implementation assets are preserved where consistent with the boundary. Misleading ownership language is deprecated or narrowed rather than triggering repository replacement.

## Compatibility

This ADR is intended as a convergence clarification. Product implementations remain independently versioned and must declare compatibility through the Convergence matrix.

## Rejected Alternatives

- Merge the three repositories into a monorepo as an architecture solution.
- Give EVO its own persistent enterprise-learning brain.
- Give Eidos long-term personalization learning independent of EC.
- Allow EC direct database writes to EVO for convenience.
- Treat LLM/chat memory as architectural authority.
