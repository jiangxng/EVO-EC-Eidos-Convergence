# APM Integrated Validation Environment v0.1

Status: INTEGRATION CANDIDATE — bootstrap available, browser stack not yet certified

## Goal

One reproducible environment for validating EVO + EC + Eidos as one enterprise system:

- Eidos: deterministic enterprise website/experience.
- EVO: operational truth, authorization and deterministic execution.
- EC: optional advisory/consulting intelligence.
- 3EC: orchestration, version locking, compatibility and certification only; it is not a fourth product runtime.

## First Windows bootstrap

```bat
git clone -b integration/apm-stack-v0.1 https://github.com/jiangxng/EVO-EC-Eidos-Convergence.git 3EC
cd 3EC
SETUP-WINDOWS.bat
STATUS-WINDOWS.bat
TEST-WINDOWS.bat
```

`SETUP-WINDOWS.bat` clones EVO, EC and Eidos into `workspace/` and detaches each repository at the exact SHA in `stack.lock.json`. This is intentional: branches are development streams; validation stacks use immutable commits.

## Current lock

- 3EC base: `8c2ac2fcce3bbe87a4b34655f598f54a3c6fdec6`
- EVO integration source: `ce7240191455e1691fff84d032483f28ed3df469`
- EVO Enterprise Package v0.1 contract pin: `d18fac50f0fc1bb29d9728fd6c5730463f8aeb71`
- EC: `fc2be5d6f24facbcf0e4090d7920a5eed45fd758`
- Eidos: `52f8923ab2b4ee833ae5b05623bfd180f554570a`

## Network target

```text
Browser
  |
  | HTTP/HTTPS
  v
Gateway / Reverse Proxy
  |-- /      -> Eidos APM Website
  |-- /api/* -> EVO public API
  `-- /advisory/* -> EC API (optional)

Eidos -- ActionRequest --> Host Adapter --> EVO Command/Authorization/Execution
EC <---- governed public observation/context ---- EVO
EC ---- Experience/Recommendation Proposal ----> Eidos
EVO ----> PostgreSQL
```

The normal business path MUST NOT traverse EC. Removing EC must not stop already-published Eidos + EVO enterprise operation.

## Certification ladder

1. Repository bootstrap is reproducible from `stack.lock.json`.
2. Each product's own tests/build pass.
3. Contract compatibility tests pass.
4. EVO can initialize a clean APM enterprise definition set.
5. Browser opens the APM Eidos website and reads real EVO state.
6. One human-confirmed Eidos action reaches a real EVO Command and changes governed state.
7. EC reads a governed EVO Observation and produces visible diagnosis/evidence/recommendation.
8. Stop EC; steps 5 and 6 remain operational.
9. Enterprise Package chain reaches EVO Validate -> Plan/Diff -> human review -> authorization -> Deploy -> Export(DEFINITION_ONLY) as EVO runtime endpoints become available.

## Important current limitation

This branch is deliberately honest: it provides the version lock and bulk setup/update/status/test foundation now. It does **not** yet claim that the final browser-visible Eidos + EVO + EC Docker Compose stack is ready. The Eidos enterprise website, gateway/compose wiring, real EVO browser business path and EC optional-service wiring still require cross-project owner implementation/certification.

Do not treat repository-level PASS as integrated website certification.
