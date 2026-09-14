# Cross-Repository Contract Versioning Policy v0.2

Status: Proposed for Architecture Convergence v0.2.1

## Rules

1. A published contract version is immutable.
2. Contract evolution is independent from product release versions.
3. No contract may silently change while retaining the same version identifier.
4. Providers and consumers must declare supported versions/capabilities.
5. Unknown/incompatible versions fail closed unless an explicit compatibility adapter is certified.
6. Historical replay/interpretation pins the applicable contract/definition version where semantics depend on it.
7. Deprecation requires replacement guidance, migration window, tests and rollback/compatibility policy.
8. Handoffs are informational reconciliation state and never override an accepted ADR or published contract.

## Compatibility Is Multi-Dimensional

Every change is classified independently as:

- `schema_compatibility`
- `semantic_compatibility`
- `behavior_compatibility`

A syntactically additive schema change may still be semantically or behaviorally breaking. For example, adding a new enum value can break an exhaustive consumer even if the producer's schema evolution is additive.

Breaking schema, semantic or behavioral changes require a new incompatible contract version or an explicit certified compatibility adapter.

## Required Change Metadata

Every cross-repository contract change records:

- contract family and owner
- old/new version
- schema compatibility
- semantic compatibility
- behavior compatibility
- producer impact
- consumer impact
- security/authorization impact
- migration path
- rollback/compatibility path
- golden fixture changes
- provider tests
- consumer tests
- compatibility matrix update

## Certification

A version combination is `CERTIFIED` only after required provider, consumer, contract, integration and reference E2E tests pass. Otherwise it is `CANDIDATE`, `BLOCKED`, or `DEPRECATED` as appropriate.
