# CRCP-EC-EVO-003 — Enterprise Simulation

Status: PROPOSED

Source Project: EC

Target Project: EVO

Contract Owner: EVO deterministic simulation boundary / EC scenario reasoning semantics

## Problem

EC should design hypotheses/scenarios and interpret alternatives, while deterministic cost, inventory, cash, ledger, capacity and scheduling consequences should reuse governed EVO calculation capabilities rather than be reimplemented by an LLM/EC.

## Required Contract Change

Establish a versioned Enterprise Simulation contract with strict separation between Actual and Hypothetical state. Requests pin relevant model/definition/data versions and return reproducible deterministic results plus lineage.

## Why

Avoid duplicated enterprise calculation logic and prevent hypothetical scenarios from contaminating operational truth.

## Compatibility Impact

New public boundary; no change to Actual runtime semantics.

## Migration Impact

Simulation projections/runtimes can be introduced incrementally. Actual BusinessData must never be used as scratch state for simulation.

## Security / Authorization Impact

Simulation is subject to enterprise scope, source-data authorization and model/capability access policy.

## Tests Required

Actual isolation; no side effects; deterministic reproduction; version pinning; authorization; parallel scenarios; scenario expiration; lineage; unsupported model/version fail-closed.

## Suggested Version

`evo.enterprise-simulation.v0.1` candidate until capability set stabilizes.

## Open Questions

- canonical simulator families in EVO
- optimization solver boundary
- snapshot/reference-data semantics
- compute budgets and asynchronous long-running simulation
