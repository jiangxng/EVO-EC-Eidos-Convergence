# Start Here

For the first run, do **not** clone or modify EVO/Eidos. Run `START-CONVERGENCE-V0.2-WINDOWS.bat` and confirm the reference boundary is coherent first.

After PASS:

1. Start your real EVO API (`http://localhost:3000`).
2. Build your real Eidos repo with `npm run build`.
3. Run live conformance:

```powershell
$env:PYTHONPATH="$PWD\src;$PWD\vendor\ec-v1.0.1\src"
python -m convergence live-check --evo http://localhost:3000 --eidos-repo D:\Documents\eidos
```

Expected:
- EVO health/dashboard/catalog can be read through public HTTP boundaries.
- EC experience proposal passes the real Eidos built validator.
- A `LIVE GAP` remains for the procurement alternate-supplier Command until EVO publishes that capability.
