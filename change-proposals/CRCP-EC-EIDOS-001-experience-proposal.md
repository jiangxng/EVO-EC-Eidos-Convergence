# CRCP-EC-EIDOS-001 — Experience Proposal

Status: RECONCILED CANDIDATE

Source Project: EC

Target Project: Eidos

Contract Owner: Eidos public Experience validation/admissibility contract; EC producer/intelligence intent semantics

## Problem

EC produces Experience intent, while current v0.2 reference schemas do not fully express modern Eidos Capability discovery/versioning, Experience Stability, Experience Integrity, Shared Core / Personal Periphery, Decision Experience, accessibility, attention/motion semantics and deterministic fallback.

Without a canonical boundary, EC could couple to renderer internals or Eidos could absorb EC intelligence.

## Required Contract Change

Establish a versioned Experience Proposal boundary where EC expresses semantic Experience intent through Eidos-public capability references and Eidos deterministically validates, constrains, resolves and realizes it.

The contract supports/references at least:

- proposal identity/version
- Experience Capability IDs/versions
- Experience Stability intent
- shared vs personal/adaptive region intent
- Decision Experience intent
- mandatory evidence requirements/references
- attention semantics
- motion semantics where relevant
- accessibility requirements
- fallback requirements
- capability negotiation context
- deterministic diagnostic expectations
- unsupported-capability behavior
- proposal provenance
- correlation/causation

Strict distinction:

`intelligence recommendation != deterministic Experience admissibility`.

EC proposes Experience intent. Eidos owns whether the proposal is admissible under its Constitution, Experience Integrity rules and available Capability Catalog.

## Compatibility Impact

Existing `ec-experience-proposal-v0.1` remains immutable historical/reference contract. Migration is explicit.

## Migration Impact

Provide v0.1 -> canonical adapters where semantics can be preserved. Unsupported semantics fail closed or use an explicitly declared deterministic fallback; they are never guessed silently.

## Security / Authorization Impact

Experience Proposal is not business authorization and cannot grant EVO execution authority.

EC personalization/adaptation proposals cannot override organization policy, accessibility, mandatory evidence, Shared Experience constraints, Decision Integrity or Experience Integrity.

## Tests Required

- EC provider schema conformance
- Eidos consumer validation
- unknown capability
- unsupported capability version
- renderer-independent realization
- mandatory evidence preservation
- shared-core integrity
- personalization constraint rejection
- accessibility validation
- deterministic fallback
- correlation/causation preservation
- invalid proposal diagnostics
- no business execution during realization
- golden Decision Experience fixtures

## Suggested Version

`eidos.experience-proposal.v1` (owner-approved naming).

## Remaining Open Questions

- Capability Catalog negotiation handshake
- exact Stability representation
- Experience instance identity lifecycle
- adaptive-region representation
- renderer support negotiation
- diagnostic/error profile integration
