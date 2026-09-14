# Deployment and validation

## Windows
1. Install Python 3.12 or 3.13.
2. Extract the ZIP to its own directory.
3. Double-click `START-CONVERGENCE-V0.2-WINDOWS.bat`.
4. Expect `ARCHITECTURE CONVERGENCE v0.2: PASS`.

No Docker, Node, PostgreSQL or LLM API key is required for the reference E2E.

## Optional real-repository conformance
Start EVO normally at `http://localhost:3000`. Build Eidos with `npm run build`. Then:

```powershell
$env:PYTHONPATH="$PWD\src;$PWD\vendor\ec-v1.0.1\src"
python -m convergence live-check --evo http://localhost:3000 --eidos-repo D:\Documents\eidos
```

This verifies what current upstream contracts actually support and reports the remaining procurement live gap instead of silently emulating it.
