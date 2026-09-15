# CRCP-ALL-APM-ENTERPRISE-WEBSITE-001

Status: PROPOSED / INTEGRATION BLOCKER
Source: EC Owner
Targets: EVO Owner, Eidos Owner, EC Owner
Contract Owner: existing public contracts remain owned by their current owners
Governance: 3EC
Date: 2026-09-15

## Problem

The three projects have substantial architecture and contract work, but the user still lacks one reproducible validation environment that opens as a real enterprise website and proves the three-system boundary with real EVO data.

This is now the first-priority integration acceptance milestone. Further isolated infrastructure work must not substitute for this visible validation target.

## Required integrated outcome

Deliver an Apex Precision Manufacturing (APM) enterprise website that a user can start on Windows/Linux with a small Docker-based validation stack and open in a browser.

The target boundary is:

`Browser -> Eidos experience/runtime -> EVO public API/Command runtime`

with EC as an optional advisory sidecar:

`EVO Observation -> EC analysis/recommendation -> Eidos advisory experience -> Human decision -> Eidos ActionRequest -> Host -> EVO authorization/Command`

EC MUST NOT be in the mandatory business execution path.

## Minimum visible website scope

The website should look and behave like an enterprise system rather than a contract test page. Initial navigation may be deliberately small, but the target information architecture includes:

- operating/home dashboard;
- sales orders;
- procurement;
- inventory;
- production;
- shipment;
- receivables;
- work/exceptions;
- EC advisory area.

The first certified increment needs one complete real business slice, not all modules. The existing APM supplier-delay/supplier-switch scenario is the preferred first slice.

## Owner deliverables

### EVO Owner

Provide or certify public runtime endpoints needed by the first APM slice. The existing 3EC v0.3 candidate expects observation, proposal admission and action execution semantics. EVO remains owner of facts, authorization and deterministic execution. No private DB/module coupling is allowed.

### Eidos Owner

Provide the browser-visible APM enterprise shell and first real business slice using Eidos deterministic experience contracts/capabilities. Business actions must produce ActionRequest and must not directly mutate EVO state. The UI must continue to support normal enterprise operation when EC is unavailable.

### EC Owner

Provide optional advisory analysis for the APM slice, evidence/recommendation/impact intent, and Enterprise Package compilation support where the existing EVO v0.1 package contract is applicable. EC does not authorize or execute business mutations.

### 3EC integration

Own only orchestration, pinned version matrix, cross-project certification, startup/stop/reset/log scripts, network topology and acceptance evidence. 3EC does not become a fourth product and does not copy ownership of EVO/Eidos/EC implementation.

## Level-1 deployment target

Keep the first validation topology intentionally small:

- reverse proxy / unified browser entry (when website is available);
- Eidos web;
- EVO API;
- EVO worker;
- PostgreSQL;
- EC advisory API/sidecar.

Docker Compose is preferred. Kubernetes, HA databases, vector/graph stores and production-scale EC infrastructure MUST NOT block this milestone.

## Required acceptance tests

1. User starts the pinned stack using documented Windows commands.
2. Browser opens the APM enterprise website.
3. At least one page reads authoritative business data from EVO.
4. At least one human-confirmed business action crosses Eidos ActionRequest -> Host -> EVO and produces a new authoritative EVO state.
5. EC can consume an EVO observation and produce an advisory recommendation/evidence/impact experience.
6. Stop EC: Eidos + EVO still browse and execute the deterministic business slice; only advisory functionality degrades.
7. Restart the stack: governed EVO business state persists.
8. Reset demo: destructive reset is explicit and recreates a deterministic APM seed.
9. 3EC records exact certified EVO/EC/Eidos commit SHAs.

## Existing evidence / reuse

3EC branch `v0.3.0-apm-demo` already contains a thin live EVO adapter, APM scenario, EC/Eidos bridges and a browser decision page. These are integration evidence and may be reused or replaced by the owning projects, but MUST NOT be mistaken for the final Eidos enterprise website.

EVO Enterprise Package v0.1 is already handed off to EC as a contract target. Contract availability is distinct from runtime endpoint readiness.

## Compatibility

This proposal does not itself change any public contract. It requests integration against existing public boundaries. If an Owner discovers a missing or incompatible public semantic, that change MUST be raised as a separate CRCP rather than silently added here.

## Security / authorization

Human confirmation is not EVO authorization. EVO must revalidate/re-authorize mutation requests. EC recommendations never carry execution authority. No cross-project direct database writes.

## Definition of done

The milestone is not done when diagrams or unit tests pass. It is done when a clean Windows validation machine can pin/sync the three projects, start the stack, open the APM website, observe real EVO facts, execute the first governed business action, observe EC advice, stop EC and prove EVO+Eidos runtime independence.
