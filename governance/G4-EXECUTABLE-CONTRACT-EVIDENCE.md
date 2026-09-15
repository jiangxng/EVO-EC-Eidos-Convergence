# G4 — Executable Contract Evidence v0.2.1

Status: IMPLEMENTED / EXECUTION PENDING CI

This gate records executable evidence only. It does not add architecture vocabulary.

## Evidence implemented

- `src/convergence/contracts_v021.py`
  - Shared Envelope semantic profile validator
  - Enterprise Observation validator
  - Command Proposal validator
  - Operational Change Proposal validator
  - Enterprise Simulation validator + deterministic digest
  - Experience Proposal validator
  - Host-neutral ActionRequest validator
  - EVO Action Mapping profile validator
- `tests/test_contracts_v021.py`
  - valid canonical examples
  - fake/trusted authorization rejection
  - observation/delivery identity separation
  - cross-tenant observation rejection
  - command expiry and proposal/idempotency separation
  - operational-change base-version requirement
  - arbitrary JSON Patch rejection
  - simulation Actual-write rejection
  - deterministic simulation digest
  - Experience capability negotiation rejection
  - mandatory evidence enforcement
  - Shared Core personalization protection
  - Host-neutral ActionRequest validation
  - EVO mapping must not authorize
  - APM causal correlation continuity
- Existing `tests/test_contracts.py` remains the frozen v0.2 behavior regression suite and APM reference E2E.
- `.github/workflows/convergence-certification.yml` executes all test modules on Python 3.12 and 3.13.

## Evidence not yet certified PASS

The files above are present, but G4 remains execution-pending until a trusted runner executes the complete suite successfully. Presence of source/tests is not equivalent to PASS.

## Security negatives represented

- fake authorization / authorization-result injection
- cross-tenant source injection
- expired Command Proposal
- proposal identity reused as command idempotency identity
- missing Operational Change base version
- unsupported/arbitrary JSON Patch mutation
- hypothetical Simulation attempting Actual write
- unsupported Experience capability version
- mandatory evidence omission
- Shared Core personalization override
- ActionRequest trusted-authorization injection

## Remaining fixture expansion

Before release certification, fixture files should be externalized from the test constants for direct reuse by upstream EVO/Eidos provider/consumer harnesses. Until upstream adoption, the executable Python test constants are Convergence-local golden/invalid evidence, not upstream certification.
