# Architecture Convergence v0.2.1 — G5 Compatibility Certification Plan

Status: IN PROGRESS

This document is execution evidence, not a new architecture vocabulary source.

## Preconditions

- Architecture / ownership / contract semantics are frozen for certification.
- Frozen v0.2.0 artifacts remain immutable.
- G5 MUST NOT claim PASS from legacy v0.2 tests alone.
- Candidate v0.2.1 contracts must be certified against executable G4 evidence.

## Certification Gates

### G5.1 Compatibility Matrix

For every candidate contract/profile record:
- owner and direction
- candidate contract version
- predecessor v0.2 role where applicable
- schema compatibility
- semantic compatibility
- behavior compatibility
- adapter status
- provider-test status
- consumer-test status
- integration-test status
- known gaps

### G5.2 Adapter / Migration Certification

Certify explicit mappings for:
- EvoIntelligenceFeedV010 -> Enterprise Context / Enterprise Observation split
- EvoOutcomeV010 -> Enterprise Observation outcome projection
- EvoCommandProposalV010 -> Command Proposal
- EcExperienceProposalV010 -> Experience Proposal
- EidosActionRequestV010 -> Host-neutral ActionRequest + EVO mapping profile

Every adapter must declare semantics as PRESERVED / TRANSFORMED / DEFAULTED / UNSUPPORTED. Unsupported semantics fail closed or use a deterministic documented fallback. No silent guessing.

### G5.3 APM End-to-End Regression

Reference APM must remain deterministic and preserve the system boundary:
EVO fact -> EC observation -> EC proposal -> Eidos experience -> Eidos ActionRequest -> Host/EVO mapping -> EVO command/execution -> EVO observation/outcome -> EC learning.

The existing Reference EVO Adapter may remain for v0.2.1 where upstream EVO has a documented public-command gap; that gap must remain explicit and must not be represented as live upstream certification.

### G5.4 v0.2.0 Immutability

Compare the frozen v0.2.0 baseline against certification changes. No frozen v0.2.0 artifact may be silently rewritten. Candidate contracts, fixtures, adapters and tests must be additive/versioned.

### G5.5 CI / Mergeability

Required before release recommendation:
- all canonical schema tests pass
- all golden fixtures pass
- all invalid/security/stale fixtures fail for the intended reason
- provider/consumer tests pass
- adapter tests pass
- APM E2E passes
- compatibility matrix contains no undeclared blocker
- PR is mergeable
- required CI/checks pass

## Release Decision

Only when G1-G5 are evidenced PASS may Convergence recommend:

`merge PR #1 -> main -> tag v0.2.1 -> release`

Until then PR #1 MUST remain unmerged.
