"""Deterministic Claim 3 falsification verifier."""
import json
from pathlib import Path
import sys

root = Path(__file__).resolve().parent
verdict = json.loads((root / "verdict.json").read_text())
explicit_d = bool(verdict["explicit_d_found"]) or False
valid_counterexample = bool(verdict["peer_hypothesis_assumption_valid"])
bound_violation = bool(verdict["fully_instantiated_D1_bound_violation"])
falsified = explicit_d or (valid_counterexample and bound_violation)
print(json.dumps({
    "explicit_d": explicit_d,
    "assumption_valid_counterexample": valid_counterexample,
    "bound_violation": bound_violation,
    "falsified": falsified,
}, sort_keys=True))
raise SystemExit(0 if falsified else 1)
