# EVO × EC × Eidos Architecture Convergence v0.2

**Status:** Runnable reference convergence + live conformance bridges  
**Reference enterprise:** Apex Precision Manufacturing (APM)  
**Convergence version:** 0.2.0

## What v0.2 proves

This package makes the cross-system boundary executable without merging the three repositories:

```text
EVO facts / public state
        ↓
EvoIntelligenceFeed v0.1
        ↓
EC v1.0.1 (bundled reference runtime)
context + governed knowledge + decision policy
        ↓
EcExperienceProposal v0.1  ─────→ Eidos contract validation
        ↓
EvoCommandProposal v0.1
        ↓ human approval
EidosActionRequest v0.1
        ↓
EVO Command boundary
        ↓
EvoOutcome v0.1
        ↓
EC outcome learning
```

Core constitutional rule:

> **EC thinks, learns and improves. EVO executes. Eidos interacts.**

No component in this convergence workspace directly reads/writes another product's internal database or private implementation.

## Windows: one click

Requires **Python 3.12 or 3.13**.

Double-click:

```text
START-CONVERGENCE-V0.2-WINDOWS.bat
```

The script runs:

1. doctor
2. contract validation
3. full tests
4. APM reference E2E
5. Package Management smoke test
6. EC knowledge merge smoke test

Expected final line:

```text
ARCHITECTURE CONVERGENCE v0.2: PASS
```

## Manual commands

Windows PowerShell:

```powershell
$env:PYTHONPATH="$PWD\src;$PWD\vendor\ec-v1.0.1\src"
python -m convergence doctor
python -m unittest discover -s tests -v
python -m convergence e2e
```

macOS/Linux:

```bash
export PYTHONPATH="$PWD/src:$PWD/vendor/ec-v1.0.1/src"
python -m convergence doctor
python -m unittest discover -s tests -v
python -m convergence e2e
```

## Current upstream truth vs convergence-owned contracts

The package intentionally distinguishes **upstream-existing** and **v0.2 candidate** contracts.

- **EVO 1.0.0-alpha.2 upstream:** public writes use the Command boundary; current concrete `/api/v1/demo/*` endpoints are reference endpoints.
- **Eidos 1.3.0-teach-and-grow.1 upstream:** `EcExperienceProposalV010`, `ExperienceCompositionV010`, `ExperienceContextV010`, and validators exist.
- **EC v1.0.1:** bundled in `vendor/ec-v1.0.1` and used by the runnable APM E2E.
- **Convergence candidate contracts:** EVO intelligence feed, EC command proposal envelope, Eidos action request, EVO outcome feed. They are versioned here so they can be adopted into upstream repos without cross-importing internals.

## Important live-integration limitation

The current EVO upstream reference API does **not** expose a `procurement.use-alternate-supplier` Command. Therefore:

- the complete APM shortage → Supplier B → approval → execution → outcome → learning loop runs against the **Reference EVO Adapter** in this ZIP;
- `live-check` can verify the current EVO health/dashboard/AI catalog and Eidos contract conformance;
- the full live APM procurement loop remains a deliberate `LIVE GAP` until EVO publishes that procurement capability through its own Command boundary.

This is not hidden or simulated as if it were already upstream.

## Package Management + Knowledge Merge

v0.2 also includes executable foundations for the two additional EC capabilities requested:

- **Enterprise Function Pack** backup/verify/install/rollback reference manager.
- **Two-EC knowledge merge** reference engine preserving provenance and conflicts instead of blind overwrite.

See `docs/EC-21-PACKAGE-MANAGEMENT.md` and `docs/EC-22-KNOWLEDGE-MERGE.md`.
