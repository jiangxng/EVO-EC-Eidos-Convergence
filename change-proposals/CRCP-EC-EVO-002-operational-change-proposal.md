# CRCP-EC-EVO-002 — Operational Change Proposal

Status: PROPOSED

Source Project: EC

Target Project: EVO

Contract Owner: EC proposal semantics / EVO operational governance semantics

## Problem

EC may learn that an SOP, Flow, Metric, Capability, Rule or Application definition should change, but learned intelligence cannot directly modify effective EVO definitions.

## Required Contract Change

Establish a versioned Operational Change Proposal contract supporting:

`EC proposal -> EVO validation -> authorized governance -> approve/reject -> draft definition version -> validate/test -> publish`

Proposal should identify target definition/type/version, proposed change, rationale/evidence/provenance, expected impact, compatibility/migration concerns and correlation/causation.

## Why

Preserve the invariant: EC may propose change; EVO remains authority for effective operational definitions.

## Compatibility Impact

Additive initially. Published operational semantics remain unchanged until an authorized new definition version becomes effective.

## Migration Impact

May require proposal/approval state and definition-version workflow, but EC must never write definition tables directly.

## Security / Authorization Impact

`PROPOSE != APPROVE != PUBLISH`. These permissions must be separable and auditable.

## Tests Required

Proposal validation; unauthorized publish rejection; version conflict; stale proposal; idempotency; approval chain; migration validation; rollback; audit lineage.

## Suggested Version

`ec.operational-change-proposal.v1` with EVO-owned governance/admission semantics.

## Open Questions

- first definition families enabled
- whether publication always terminates in an EVO Command
- multi-party approval policy ownership
- dry-run/simulation requirement before publication
