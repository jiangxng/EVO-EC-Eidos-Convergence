# LLM Cross-Repository Collaboration Protocol v0.1

Status: Proposed for Architecture Convergence v0.2.1

## Purpose

This protocol governs collaboration between the LLMs responsible for EVO, Experience Compiler (EC), and Eidos.

## Canonical System Boundary

> EC thinks, learns and improves. EVO executes. Eidos interacts.

- EC may learn.
- EVO and Eidos runtime must not independently accumulate long-term enterprise intelligence or learning.
- EC may propose change. EVO and Eidos accept only versioned, validated and authorized change within their ownership boundaries.
- No LLM, EC recommendation, Eidos interaction, or client assertion is authorization to mutate EVO operational truth.

## Authority Order

For cross-repository architecture, authority is:

1. Versioned public contracts and schemas.
2. Accepted ADRs.
3. Compatibility matrix and certified fixtures/tests.
4. Current project handoffs.
5. Repository implementation within the owning project.
6. Chat history only as temporary working context.

Chat history is never the durable cross-repository authority.

## Collaboration Rules

1. Repositories remain independently owned; Convergence is not a monorepo and not a fourth product.
2. No project imports another project's internal modules or relies on another project's database schema.
3. Cross-project requirements become a Cross-Repo Change Proposal (CRCP).
4. Every public contract has exactly one canonical owner, even when producers and consumers are in different projects.
5. Breaking contract changes require an explicit version change, migration path, compatibility impact, rollback plan and tests.
6. Compatibility claims require executable contract/integration tests and golden fixtures.
7. A project LLM may design its own implementation but must not unilaterally redesign another project's internals.
8. Unknown contract versions and invalid authorization context fail closed.
9. Correlation, causation, lineage, enterprise scope and contract version must survive cross-system boundaries where applicable.
10. Cross-system learned or inferred information retains provenance and must not silently become operational truth.

## Required Reading for a Fresh Project LLM

Before cross-repository work, read:

- `CONSTITUTION.md`
- `governance/OWNERSHIP-MANIFEST.md`
- `governance/CONTRACT-VERSIONING.md`
- `contracts/`
- `compatibility-matrix.json`
- accepted `decisions/`
- the project's `handoffs/<PROJECT>.md`
- relevant open `change-proposals/`

## CRCP Workflow

`Project discovery -> CRCP -> owner review -> reconciliation -> ADR if architectural -> contract/schema -> golden fixture -> provider/consumer tests -> compatibility certification -> implementation`

A CRCP is a request for cross-system change. It is not an approved architecture decision.

## Human Role

Humans provide business direction, authorization and major architecture/product decisions where required. They should not be a permanent copy/paste message bus between project LLMs.
