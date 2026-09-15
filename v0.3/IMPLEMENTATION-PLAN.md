# v0.3.0 — Real APM Integration & Clickable Demo

Status: IMPLEMENTATION

## Frozen authority

v0.2.1 Architecture / Ownership / Contract Semantics are frozen inputs. v0.3.0 implements them; it does not reopen them.

Canonical boundary:

> EC thinks, learns and improves. EVO executes. Eidos interacts.

## User-visible acceptance

A browser user can inspect the APM supplier-shortage decision, evidence and projected impact, approve the alternate-supplier recommendation, and observe the decision traverse the real contract chain into EVO. The UI must refresh from new EVO facts/outcomes rather than mutate local demo state.

## Real vertical slice

1. EVO emits canonical Enterprise Observation from operational facts.
2. EC consumes Observation and produces Command Proposal + Experience Proposal.
3. Eidos validates and deterministically realizes the Decision Experience.
4. Human approval produces Host-neutral ActionRequest.
5. Host adapter maps the request to an EVO-owned Command admission request.
6. EVO independently re-authorizes and executes the published Command.
7. EVO appends BusinessData and emits new Observation/Outcome.
8. EC records/evaluates the outcome as learning input.
9. Eidos refreshes from authoritative state.

## Implementation order

### EVO slice
1. Published Command input-schema enforcement.
2. Formal `procurement.use-alternate-supplier` CommandDefinition and input schema.
3. Enterprise Observation provider/projection.
4. Command Proposal admission adapter.
5. Host-neutral ActionRequest → EVO mapping adapter.
6. APM real causal-chain provider/consumer tests.

### EC slice
1. Consume canonical Enterprise Observation.
2. Produce alternate-supplier Command Proposal.
3. Produce Eidos Experience Proposal.
4. Consume EVO Outcome/Observation and persist learning candidate.

### Eidos slice
1. Consume canonical Experience Proposal through certified compatibility mapping.
2. Render decision-panel with mandatory evidence, impact and fallback.
3. Produce Host-neutral ActionRequest preserving confirmation and TOCTOU evidence.
4. Refresh from authoritative post-command state.

### Demo shell
A thin integration host composes the three independently owned runtimes. It owns transport/wiring only. It must not become a fourth business system and must not own enterprise truth, learning or Experience semantics.

## APM scenario

Customer: Northstar Industrial Systems
Sales order: SO-20260918-0182
Product: Precision Drive Assembly / Critical Servo Module
Promise date: 2026-09-18
Revenue at risk: approximately USD 280,000
Supplier A: revised delivery 2026-09-20
Supplier B: qualified, +8.4% purchase cost
Decision: approve alternate supplier to protect customer promise.

## Fail-closed requirements

- EC-supplied authorization is never trusted.
- Eidos confirmation is never EVO authorization.
- EVO re-evaluates authorization at command admission.
- tenant mismatch fails closed.
- expired proposal/delegation fails closed.
- unsupported command/input schema version fails closed.
- stale presented state/definition fails closed where required.
- duplicate delivery preserves semantic identity and command idempotency.
- correlation/causation preserve lineage but never grant authority.

## Out of scope for this first slice

- Operational Change runtime admission.
- Full Enterprise Simulation provider.
- Broad procurement suite beyond the minimum APM alternate-supplier capability.
- UX personalization beyond deterministic Eidos contract behavior.

## Exit gate

v0.3.0 first-demo gate passes only when the browser click reaches a real EVO Command, produces new authoritative facts, returns Outcome/Observation to EC, and the Eidos UI reflects the authoritative post-command state. A local-only UI state change does not count.