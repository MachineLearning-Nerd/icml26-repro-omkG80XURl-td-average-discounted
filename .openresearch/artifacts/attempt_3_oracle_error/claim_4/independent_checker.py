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
    elif claim_number == 4:
        audit = json.loads(
            (claim_dir / "raw_primary_source_rate_audit.json").read_text()
        )
        route = json.loads((claim_dir / "raw_route_result.json").read_text())
        prior_power = audit["prior_average_reward"][
            "mean_square_denominator_exponents"
        ]["eta2"]
        discounted_power = audit["discounted_td"][
            "squared_parameter_error_denominator_exponents"
        ]["one_minus_gamma_times_omega"]
        proposed_power = audit["proposed_average_reward"][
            "squared_parameter_error_denominator_exponents"
        ]["eta1"]
        proposed_envelope = (
            route["proposed_quadratic_envelope_validation"]
            <= 1.25 * route["proposed_quadratic_envelope_calibration"]
        )
        passed = (
            prior_power == -4
            and discounted_power == -2
            and proposed_power == -2
            and proposed_envelope
            and audit["definition_alignment"][
                "powers_are_not_treated_as_values_of_one_common_scalar"
            ]
        )
        result = {
            "prior_average_reward_power": prior_power,
            "discounted_power": discounted_power,
            "proposed_average_reward_power": proposed_power,
            "proposed_heldout_envelope": proposed_envelope,
            "passed": passed,
        }
    elif claim_number == 5:
        rows = _read_csv(claim_dir / "raw_single_chain.csv")
        controls = _read_csv(
            claim_dir / "raw_single_chain_algorithm_negative_control.csv"
        )
        calibration = [row for row in rows if float(row["eta"]) >= 0.16]
        validation = [row for row in rows if float(row["eta"]) < 0.16]
        quartic_calibration = max(
            float(row["quartic_normalized_mse"]) for row in calibration
        )
        quartic_validation = max(
            float(row["quartic_normalized_mse"]) for row in validation
        )
        cubic_calibration = max(
            float(row["cubic_normalized_mse"]) for row in calibration
        )
        cubic_validation = max(
            float(row["cubic_normalized_mse"]) for row in validation
        )
        per_eta = {}
        for eta in sorted({float(row["eta"]) for row in rows}):
            subset = [row for row in rows if float(row["eta"]) == eta]
            per_eta[str(eta)] = float(
                np.polyfit(
                    np.log([float(row["T"]) for row in subset]),
                    np.log(
                        [
                            float(row["mse"])
                            / math.log(float(row["T"]) + 1.0)
                            for row in subset
                        ]
                    ),
                    1,
                )[0]
            )
        ratios = [float(row["eta_prime_over_eta"]) for row in rows]
        target = [
            row
            for row in rows
            if float(row["eta"]) == min(float(item["eta"]) for item in rows)
            and int(float(row["quartic_budget"])) == 32
        ][0]
        control = [
            row
            for row in controls
            if float(row["eta"]) == min(float(item["eta"]) for item in controls)
        ][0]
        passed = (
            max(ratios) - min(ratios) <= 1e-12
            and all(-1.45 <= slope <= -0.55 for slope in per_eta.values())
            and quartic_validation <= 1.35 * quartic_calibration
            and cubic_validation > 1.35 * cubic_calibration
            and float(control["mse"]) > 1.5 * float(target["mse"])
        )
        result = {
            "eta_prime_over_eta_range": [min(ratios), max(ratios)],
            "per_eta_T_exponents": per_eta,
            "quartic_calibration": quartic_calibration,
            "quartic_validation": quartic_validation,
            "cubic_negative_calibration": cubic_calibration,
            "cubic_negative_validation": cubic_validation,
            "algorithm_control_mse": float(control["mse"]),
            "target_mse": float(target["mse"]),
            "passed": passed,
        }
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
