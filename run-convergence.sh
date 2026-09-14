#!/usr/bin/env sh
set -eu
ROOT="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
export PYTHONPATH="$ROOT/src:$ROOT/vendor/ec-v1.0.1/src"
python3 -m convergence doctor
python3 -m convergence validate-contracts
python3 -m unittest discover -s "$ROOT/tests" -v
python3 -m convergence e2e
python3 -m convergence function-pack-smoke
python3 -m convergence knowledge-merge-smoke
echo "ARCHITECTURE CONVERGENCE v0.2: PASS"
