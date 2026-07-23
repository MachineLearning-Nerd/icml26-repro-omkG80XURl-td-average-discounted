"""Second-path checks that recompute decisions from raw claim artifacts."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path
import sys

import numpy as np


def _read_csv(path: Path) -> list[dict[str, object]]:
    def parse(value: str) -> object:
        try:
            return float(value)
        except ValueError:
            return value

    with path.open(newline="") as handle:
        return [
            {key: parse(value) for key, value in row.items()}
            for row in csv.DictReader(handle)
        ]


def _fit(rows: list[dict[str, object]], markov: bool) -> dict[str, float]:
    x, y = [], []
    for row in rows:
        adjustment = math.log(row["T"] + 1.0)
        if markov:
            adjustment *= 3.0 * row["mixing_time"] + 1.0
        x.append([1.0, math.log(row["T"]), math.log(row["eta"])])
        y.append(math.log(max(row["mse"] / adjustment, 1e-300)))
    coef, _, _, _ = np.linalg.lstsq(np.asarray(x), np.asarray(y), rcond=None)
    return {"T_exponent": float(coef[1]), "eta_exponent": float(coef[2])}


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: independent_checker.py CLAIM_DIRECTORY")
        return 64
    claim_dir = Path(sys.argv[1])
    claim_number = int(claim_dir.name.split("_")[-1])
    result: dict[str, object]
    passed = False
    if claim_number == 1:
        rows = _read_csv(claim_dir / "raw_exact_moments.csv")
        fit = _fit(rows, markov=False)
        calibration = [row for row in rows if float(row["eta"]) >= 0.20]
        validation = [row for row in rows if float(row["eta"]) < 0.20]
        quadratic_calibration = max(
            float(row["mse"])
            * float(row["T"])
            * float(row["eta"]) ** 2
            / math.log(float(row["T"]) + 1.0)
            for row in calibration
        )
        quadratic_validation = max(
            float(row["mse"])
            * float(row["T"])
            * float(row["eta"]) ** 2
            / math.log(float(row["T"]) + 1.0)
            for row in validation
        )
        linear_calibration = max(
            float(row["mse"])
            * float(row["T"])
            * float(row["eta"])
            / math.log(float(row["T"]) + 1.0)
            for row in calibration
        )
        linear_validation = max(
            float(row["mse"])
            * float(row["T"])
            * float(row["eta"])
            / math.log(float(row["T"]) + 1.0)
            for row in validation
        )
        passed = (
            -1.25 <= fit["T_exponent"] <= -0.75
            and quadratic_validation <= 1.25 * quadratic_calibration
            and linear_validation > 1.25 * linear_calibration
        )
        result = {
            "recomputed_regression": fit,
            "quadratic_envelope_calibration": quadratic_calibration,
            "quadratic_envelope_validation": quadratic_validation,
            "linear_negative_control_calibration": linear_calibration,
            "linear_negative_control_validation": linear_validation,
            "passed": passed,
        }
    elif claim_number == 2:
        rows = _read_csv(claim_dir / "raw_exact_moments.csv")
        fit = _fit(rows, markov=True)
        per_eta = {}
        for eta in sorted({row["eta"] for row in rows}):
            subset = [row for row in rows if row["eta"] == eta]
            slope = float(
                np.polyfit(
                    np.log([row["T"] for row in subset]),
                    np.log(
                        [
                            row["mse"]
                            / (
                                math.log(row["T"] + 1.0)
                                * (3.0 * row["mixing_time"] + 1.0)
                            )
                            for row in subset
                        ]
                    ),
                    1,
                )[0]
            )
            per_eta[str(eta)] = slope
        passed = (
            -1.30 <= fit["T_exponent"] <= -0.70
            and all(-1.35 <= slope <= -0.65 for slope in per_eta.values())
        )
        result = {
            "recomputed_regression": fit,
            "per_eta_T_exponents": per_eta,
            "passed": passed,
        }
    elif claim_number == 3:
        formulas = json.loads((claim_dir / "raw_formula_dependencies.json").read_text())
        forbidden = [
            formula["name"]
            for formula in formulas
            if "d" in formula["free_symbols"]
        ]
        passed = not forbidden
        result = {"formulas_with_explicit_d": forbidden, "passed": passed}
    elif claim_number == 6:
        rows = _read_csv(claim_dir / "raw_condition_stress.csv")
        minimum_margin = min(row["eta1_minus_half_eta3"] for row in rows)
        proof = json.loads((claim_dir / "raw_proof_steps.json").read_text())
        passed = minimum_margin >= -1e-10 and all(proof["steps"].values())
        result = {
            "minimum_numeric_margin": minimum_margin,
            "proof_steps": proof["steps"],
            "passed": passed,
        }
    else:
        result = {
            "passed": False,
            "reason": "This first-round route deliberately leaves the claim BLOCKED.",
        }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
