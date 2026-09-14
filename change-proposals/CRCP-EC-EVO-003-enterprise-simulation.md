# CRCP-EC-EVO-003 — Enterprise Simulation

Status: RECONCILED CANDIDATE

Source Project: EC

Target Project: EVO

Contract Owner: EVO deterministic simulation boundary; EC scenario/hypothesis/reasoning semantics

## Problem

EC should design hypotheses/scenarios and interpret alternatives, while deterministic cost, inventory, cash, ledger, capacity and scheduling consequences should reuse governed EVO calculation capabilities rather than be reimplemented by an LLM/EC.

## Required Contract Change

Establish a versioned Enterprise Simulation contract with strict Actual/Hypothetical separation.

A simulation request/run includes at least:

- `simulation_id`
- `scenario_id`
- `enterprise_id`
- baseline `actual_snapshot_ref`
- baseline `as_of_business_time`
- baseline `data_version`
- `definition_pins`
- `rule_pins`
- `valuation_pins`
- `metric_pins`
- `assumptions[]`
- `requested_calculators[]`
- `namespace = HYPOTHETICAL`

Result includes:

- outputs
- lineage
- warnings
- `deterministic_digest`

Mandatory invariants:

- `Replay != Simulation`
- Simulation output MUST NOT mutate or be addressable as Actual BusinessData, LedgerEntry, LedgerBalance or posting state
- same baseline pins + same assumptions + same calculator versions => reproducible deterministic result/digest

The contract permits asynchronous lifecycle semantics such as `SUBMITTED`, `RUNNING`, `COMPLETED`, `FAILED`, `EXPIRED` and cancellation where supported; it does not force synchronous RPC.

## Why

Avoid duplicated enterprise calculation logic and prevent hypothetical scenarios from contaminating operational truth.

## Compatibility Impact

New public boundary; no change to Actual runtime semantics. Current EVO has an implementation gap for a generic public simulation runtime, not an architecture conflict.

## Migration Impact

Simulation runtimes can be introduced incrementally. Actual BusinessData must never be used as scratch state.

Simulation has no business rollback because it has no Actual side effect. Operational cleanup is cancellation/expiry/cache/projection removal only.

## Security / Authorization Impact

Simulation is subject to enterprise scope, source-data authorization and calculator/model capability access policy.

## Tests Required

- simulation cannot write BusinessData
- simulation cannot advance posting high-water
- simulation cannot alter Actual balances
- deterministic reproduction for identical pins/assumptions
- different baseline => distinct run identity/result
- authorization
- concurrent scenario isolation
- scenario expiration/cancellation
- lineage
- unsupported model/calculator/version fail closed

## Suggested Version

`evo.enterprise-simulation.v0.1` candidate until the public calculator set stabilizes.

## Remaining Open Questions

- canonical calculator/simulator families in EVO
- optimization solver adapter boundary
- snapshot/reference-data representation
- compute budgets / async execution service profile
