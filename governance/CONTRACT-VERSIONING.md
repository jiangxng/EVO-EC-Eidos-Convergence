# Cross-Repository Contract Versioning Policy v0.1

Status: Proposed for Architecture Convergence v0.2.1

## Rules

1. A published contract version is immutable.
2. Contract evolution is independent from product release versions.
3. Additive compatible changes increment the contract patch/minor version according to the contract family's declared policy.
4. Breaking semantic/schema changes require a new incompatible contract version.
5. No contract may silently change while retaining the same version identifier.
6. Providers and consumers must declare supported versions/capabilities.
7. Unknown/incompatible versions fail closed unless an explicit compatibility adapter is certified.
8. Historical replay/interpretation must pin the applicable contract/definition version where semantics depend on it.
9. Deprecation requires replacement guidance, migration window, tests and rollback/compatibility policy.

## Required Change Metadata

Every cross-repository contract change records:

- contract family and owner
- old/new version
- additive vs breaking classification
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

A version combination is `CERTIFIED` only after required contract/integration tests and reference E2E tests pass. Otherwise it is `CANDIDATE`, `BLOCKED`, or `DEPRECATED` as appropriate.
