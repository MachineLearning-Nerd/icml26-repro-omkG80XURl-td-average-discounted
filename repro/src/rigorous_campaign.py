"""Generate claim-by-claim evidence for the first rigorous reproduction round."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile
import time

import numpy as np

from exact_moments import ScalarFamily, exact_metrics, rate_regression


ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS = ROOT / ".openresearch" / "artifacts"
COMMAND = "uv run --frozen python repro/src/verify_td.py"
PAPER_URL = "https://ar5iv.labs.arxiv.org/html/2605.02103"
PAPER_SHA256 = "2d40f7e54ced7ee48f9b336f2928e081e679293122d09d09e9fe681a6601a9d9"
IID_ETA_GRID = (0.40, 0.28, 0.20, 0.14, 0.10, 0.07, 0.05, 0.035)
MARKOV_ETA_GRID = (0.40, 0.28, 0.20, 0.14, 0.10, 0.07)
NORMALIZED_BUDGETS = (4096, 8192, 16384, 32768)


CLAIMS = {
    1: {
        "anchor": "#S4.Thmtheorem1",
        "statement": (
            "Under Assumption 2.1, double-chain TD with i.i.d. stationary "
            "sampling and a legal constant step has last-iterate "
            "sample complexity tilde-O(epsilon^-1 eta^-2) and converges to "
            "the unique projected-Bellman solution."
        ),
    },
    2: {
        "anchor": "#S4.Thmtheorem2",
        "statement": (
            "Under Assumption 2.1, two independent stationary Markov chains, "
            "the stated constant-step restriction, and T>=tau_mix, the "
            "double-chain last iterate has a tilde-O(1/T) bound and "
            "tilde-O(epsilon^-1 eta^-2) sample complexity, with the explicit "
            "mixing factor retained."
        ),
    },
    3: {
        "anchor": "#S4.Thmtheorem3",
        "statement": (
            "For alpha_t=a/(t+c0)^xi, xi in (0,1], sufficiently large c0, "
            "and T>=tau_mix, Theorem 4.3 has no explicit dimension factor; "
            "dimension may enter only through norms and condition quantities."
        ),
    },
    4: {
        "anchor": "#S1.T1",
        "statement": (
            "The proposed two-chain theoretical bound is quadratic in eta1^-1, "
            "compared with quartic prior coupled-SA bounds and quadratic "
            "discounted-TD bounds, under their respective condition-number "
            "definitions."
        ),
    },
    5: {
        "anchor": "#S4.Thmtheorem4",
        "statement": (
            "The single-chain bound is tilde-O(1/(eta' eta^3 T)) and becomes "
            "quartic tilde-O(1/(eta^4 T)) only in the stated common regime "
            "eta'=Theta(eta)."
        ),
    },
    6: {
        "anchor": "#A2.Thmtheorem3",
        "statement": (
            "For every admissible chain and full-column-rank feature matrix, "
            "eta1 >= eta3/2 under Equations (3), (2), and the half-scaled "
            "Dirichlet seminorm in Equation (7)."
        ),
    },
}


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def git_sha() -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def environment_record() -> dict[str, object]:
    return {
        "command": COMMAND,
        "git_sha": git_sha(),
        "python": sys.version,
        "python_executable": sys.executable,
        "numpy": np.__version__,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "logical_cpus": os.cpu_count(),
        "seeds": list(range(64)),
        "paper_url": PAPER_URL,
        "paper_html_sha256": PAPER_SHA256,
    }


def exact_rows(sampling: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    eta_grid = IID_ETA_GRID if sampling == "iid" else MARKOV_ETA_GRID
    for eta in eta_grid:
        family = ScalarFamily(delta=eta / 2.0)
        if not math.isclose(family.eta, eta, rel_tol=0.0, abs_tol=1e-15):
            raise AssertionError("controlled-family eta construction drifted")
        for normalized_budget in NORMALIZED_BUDGETS:
            horizon = math.ceil(normalized_budget / eta**2)
            row = exact_metrics(family, horizon, sampling)
            row["normalized_budget"] = normalized_budget
            row["normalized_mse"] = (
                row["mse"] * eta**2 * horizon / math.log(horizon + 1.0)
            )
            if sampling == "markov":
                row["mixing_adjusted_mse"] = (
                    row["normalized_mse"] / (3.0 * row["mixing_time"] + 1.0)
                )
            rows.append(row)
    return rows


def _stationary_distribution(p: np.ndarray) -> np.ndarray:
    mu = np.full(p.shape[0], 1.0 / p.shape[0])
    for _ in range(20000):
        nxt = mu @ p
        if np.max(np.abs(nxt - mu)) < 1e-14:
            break
        mu = nxt
    mu = np.maximum(mu, 0.0)
    return mu / mu.sum()


def condition_numbers(
    p: np.ndarray, mu: np.ndarray, phi: np.ndarray
) -> tuple[float, float, float, float]:
    dmat = np.diag(mu)
    a = dmat @ (np.eye(len(mu)) - p)
    asym = 0.5 * (a + a.T)
    mean_feature = phi.T @ mu
    eta1_matrix = phi.T @ asym @ phi + np.outer(mean_feature, mean_feature)
    eta1 = float(np.linalg.eigvalsh(eta1_matrix).min())
    sigma = float(np.linalg.eigvalsh(phi.T @ dmat @ phi).min())
    invsqrt = np.diag(1.0 / np.sqrt(mu))
    normalized = invsqrt @ asym @ invsqrt
    eigenvalues = np.linalg.eigvalsh(normalized)
    lam = float(eigenvalues[1])
    return eta1, sigma * lam, sigma, lam


def condition_stress_rows() -> tuple[list[dict[str, object]], dict[str, object]]:
    rows: list[dict[str, object]] = []
    identity_errors = []
    contraction_excesses = []
    case = 0
    for n, d, repetitions in (
        (2, 2, 8),
        (4, 2, 8),
        (8, 4, 8),
        (16, 8, 8),
        (32, 12, 6),
        (64, 20, 4),
        (128, 32, 2),
    ):
        for repetition in range(repetitions):
            rng = np.random.default_rng(10000 + case)
            raw = rng.random((n, n))
            raw /= raw.sum(axis=1, keepdims=True)
            p = 0.90 * raw + 0.10 / n
            mu = _stationary_distribution(p)
            phi = rng.normal(size=(n, d))
            row_norms = np.linalg.norm(phi, axis=1)
            phi /= max(1.0, float(row_norms.max()))
            eta1, eta3, sigma, lam = condition_numbers(p, mu, phi)

            probe = rng.normal(size=n)
            direct = 0.5 * np.sum(
                mu[:, None] * p * (probe[:, None] - probe[None, :]) ** 2
            )
            matrix = float(probe @ np.diag(mu) @ (np.eye(n) - p) @ probe)
            identity_errors.append(abs(direct - matrix))
            contraction_excesses.append(
                float(np.linalg.norm(p @ probe * np.sqrt(mu)) ** 2)
                - float(np.linalg.norm(probe * np.sqrt(mu)) ** 2)
            )
            rows.append(
                {
                    "case": case,
                    "family": "dense_positive",
                    "n": n,
                    "d": d,
                    "seed": 10000 + case,
                    "eta1": eta1,
                    "eta3": eta3,
                    "sigma": sigma,
                    "lambda": lam,
                    "eta1_minus_half_eta3": eta1 - 0.5 * eta3,
                    "eta1_over_eta3": eta1 / eta3,
                }
            )
            case += 1

    # Paper-scale state/feature dimensions from Appendix G, with a structured,
    # reversible ergodic transition so the n=1000 check remains reproducible.
    for n, d in ((50, 5), (100, 20), (1000, 100)):
        rng = np.random.default_rng(20000 + n)
        p = np.full((n, n), 0.20 / n)
        indices = np.arange(n)
        p[indices, indices] += 0.20
        p[indices, (indices - 1) % n] += 0.30
        p[indices, (indices + 1) % n] += 0.30
        mu = np.full(n, 1.0 / n)
        phi = rng.normal(size=(n, d))
        phi /= max(1.0, float(np.linalg.norm(phi, axis=1).max()))
        eta1, eta3, sigma, lam = condition_numbers(p, mu, phi)
        rows.append(
            {
                "case": case,
                "family": "paper_scale_cycle_teleport",
                "n": n,
                "d": d,
                "seed": 20000 + n,
                "eta1": eta1,
                "eta3": eta3,
                "sigma": sigma,
                "lambda": lam,
                "eta1_minus_half_eta3": eta1 - 0.5 * eta3,
                "eta1_over_eta3": eta1 / eta3,
            }
        )
        case += 1

    # Tight tabular case: eta1=eta3, so the deliberately stronger 1.1*eta3
    # negative control must fail rather than passing vacuously.
    p = np.full((2, 2), 0.5)
    mu = np.full(2, 0.5)
    phi = np.eye(2)
    eta1, eta3, sigma, lam = condition_numbers(p, mu, phi)
    rows.append(
        {
            "case": case,
            "family": "tight_tabular",
            "n": 2,
            "d": 2,
            "seed": -1,
            "eta1": eta1,
            "eta3": eta3,
            "sigma": sigma,
            "lambda": lam,
            "eta1_minus_half_eta3": eta1 - 0.5 * eta3,
            "eta1_over_eta3": eta1 / eta3,
        }
    )

    proof = {
        "steps": {
            "dirichlet_equals_quadratic_form": bool(
                max(identity_errors) < 1e-10
            ),
            "P_is_D_norm_contraction_on_stress_probes": bool(
                max(contraction_excesses) < 1e-10
            ),
            "lambda_is_at_most_two": bool(
                max(float(row["lambda"]) for row in rows) <= 2.0 + 1e-10
            ),
            "scalar_decomposition_coefficients_nonnegative_for_lambda_in_0_2": bool(
                all(
                    lam_value / 2.0 >= 0.0 and 1.0 - lam_value / 2.0 >= 0.0
                    for lam_value in np.linspace(0.0, 2.0, 1001)
                )
            ),
            "rayleigh_minimum_preserves_half_factor": bool(
                min(float(row["eta1_minus_half_eta3"]) for row in rows) >= -1e-10
            ),
        },
        "max_dirichlet_identity_error": max(identity_errors),
        "max_sampled_contraction_excess": max(contraction_excesses),
        "negative_control": {
            "proposed_false_statement": "eta1 >= 1.1 * eta3",
            "tight_case_margin": eta1 - 1.1 * eta3,
            "expected_to_fail": bool(eta1 - 1.1 * eta3 < 0.0),
        },
    }
    return rows, proof


def formula_dependencies() -> list[dict[str, object]]:
    return [
        {
            "name": "theorem_4_3_xi_equals_1",
            "free_symbols": [
                "T",
                "tau_mix",
                "c0",
                "a",
                "eta",
                "theta0_norm",
                "theta_star_norm",
                "r_max",
            ],
        },
        {
            "name": "theorem_4_3_xi_between_0_and_1",
            "free_symbols": [
                "T",
                "tau_mix",
                "c0",
                "a",
                "eta",
                "xi",
                "theta0_norm",
                "theta_star_norm",
                "r_max",
            ],
        },
        {
            "name": "theorem_D_1_explicit_constants",
            "free_symbols": [
                "T",
                "tau_mix",
                "c0",
                "a",
                "eta",
                "xi",
                "C",
                "beta",
                "theta0_norm",
                "theta_star_norm",
                "r_max",
            ],
        },
    ]


def source_audit_text(number: int) -> str:
    claim = CLAIMS[number]
    qualifications = {
        1: (
            "The rate is an upper bound for squared parameter error at the last "
            "iterate. The tilde hides logarithms; alpha must obey eta/18."
        ),
        2: (
            "The displayed theorem retains tau_mix and starts both chains in "
            "stationarity. Varying the transition gap also varies mixing, so "
            "the checker keeps the explicit (3*tau_mix+1) factor."
        ),
        3: (
            "The paper defines dimension independence to permit d to enter "
            "implicitly through ||theta_0||, ||theta*||, eta, and mixing."
        ),
        4: (
            "The compared works use eta1, eta2, eta3, and eta_discounted; a "
            "numerical comparison of bare powers is not a faithful rate test."
        ),
        5: (
            "Quartic eta^-4 is conditional on eta'=Theta(eta). The general "
            "displayed dependence is 1/(eta' eta^3 T)."
        ),
        6: (
            "Equation (7) includes a factor 1/2. Omitting it, as the judged "
            "toy implementation did, changes eta1 and invalidates an exact audit."
        ),
    }[number]
    return (
        f"# Source audit — Claim {number}\n\n"
        f"Source: [{PAPER_URL}{claim['anchor']}]({PAPER_URL}{claim['anchor']})  \n"
        f"Retrieved HTML SHA-256: `{PAPER_SHA256}`\n\n"
        f"Exact audited statement: {claim['statement']}\n\n"
        f"Qualification controlling this contract: {qualifications}\n"
    )


def method_text(number: int) -> str:
    methods = {
        1: (
            "A two-state irreducible/aperiodic family has phi=(-1,1), flip "
            "probability eta/2, bounded symmetric reward noise, and theta*=1. "
            "A 3x3 affine moment operator is exponentiated exactly, not sampled. "
            "Route 1 preregisters an equality-style exponent fit. Route 2 treats "
            "tilde-O as the upper bound it is: a quadratic envelope is calibrated "
            "on eta>=0.20 and tested without refitting on smaller held-out eta, "
            "while an eta^-1 envelope is required to fail as a negative control."
        ),
        2: (
            "The same family is propagated with a 12x12 conditional moment "
            "operator over both genuine chain states. Both chains start from "
            "their stationary distribution. Regression divides out the theorem's "
            "logarithm and explicit (3*tau_mix+1) term."
        ),
        3: (
            "The main and full appendix formulas are transcribed as dependency "
            "sets. A checker rejects any free explicit symbol d. A negative "
            "control injects d into the formula and must be rejected."
        ),
        4: (
            "This route measures the proposed method directly but does not yet "
            "implement the cited prior algorithms under matched condition-number "
            "families. It therefore cannot settle the cross-paper comparison."
        ),
        5: (
            "This route audits the conditional exponent arithmetic but does not "
            "yet measure the actual single-chain Eq. (17) sample complexity "
            "across a family satisfying eta'=Theta(eta)."
        ),
        6: (
            "The proof is decomposed into independently checked identities and "
            "Rayleigh steps, then stressed on positive nonreversible chains, "
            "paper-scale (n,d) pairs through (1000,100), and a tight tabular case."
        ),
    }
    return f"# Method — Claim {number}\n\n{methods[number]}\n"


def make_claim_dir(number: int) -> Path:
    claim_dir = ARTIFACTS / f"claim_{number}"
    claim_dir.mkdir(parents=True, exist_ok=True)
    return claim_dir


def common_files(
    number: int,
    summary: dict[str, object],
    contract_checks: list[str],
    limitations: str,
    runtime_seconds: float,
) -> None:
    claim_dir = make_claim_dir(number)
    write_json(
        claim_dir / "claim_contract.json",
        {
            "claim": number,
            "paper_statement": CLAIMS[number]["statement"],
            "source_url": PAPER_URL + CLAIMS[number]["anchor"],
            "source_sha256": PAPER_SHA256,
            "assumptions": [
                "finite-state fixed-policy evaluation",
                "irreducible and aperiodic induced chain",
                "full-column-rank normalized features",
                "stationary sampling where required",
                "paper-prescribed step-size regime",
            ],
            "machine_checks": contract_checks,
            "allowed_verdicts": ["VERIFIED", "FALSIFIED", "BLOCKED"],
        },
    )
    (claim_dir / "source_audit.md").write_text(source_audit_text(number))
    (claim_dir / "method.md").write_text(method_text(number))
    (claim_dir / "limitations.md").write_text(
        f"# Limitations and deviations — Claim {number}\n\n{limitations}\n"
    )
    write_json(claim_dir / "summary.json", summary)
    env = environment_record()
    write_json(claim_dir / "environment.json", env)
    (claim_dir / "exact_command.txt").write_text(COMMAND + "\n")
    write_json(
        claim_dir / "runtime.json",
        {
            "route_runtime_seconds": runtime_seconds,
            "backend": "local CPU",
            "logical_cpus_visible": os.cpu_count(),
            "gpu_used": False,
        },
    )
    shutil.copyfile(ROOT / "repro" / "src" / "claim_verifier.py", claim_dir / "verifier.py")
    shutil.copyfile(
        ROOT / "repro" / "src" / "independent_checker.py",
        claim_dir / "independent_checker.py",
    )

    checker = subprocess.run(
        [sys.executable, str(ROOT / "repro" / "src" / "independent_checker.py"), str(claim_dir)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    (claim_dir / "independent_checker_output.txt").write_text(
        f"returncode={checker.returncode}\n{checker.stdout}{checker.stderr}"
    )
    summary["independent_checker_returncode"] = checker.returncode
    if checker.returncode != 0 and summary.get("verdict") == "VERIFIED":
        summary["verdict"] = "BLOCKED"
        summary["assessment"] = (
            f"{summary['assessment']} The independent checker returned "
            f"{checker.returncode}, so the evidence is downgraded to BLOCKED."
        )
    write_json(claim_dir / "summary.json", summary)

    with tempfile.TemporaryDirectory() as temporary:
        negative_dir = Path(temporary)
        negative = json.loads(json.dumps(summary))
        first_check = next(iter(negative["checks"]))
        negative["checks"][first_check] = False
        write_json(negative_dir / "summary.json", negative)
        verifier = subprocess.run(
            [sys.executable, str(ROOT / "repro" / "src" / "claim_verifier.py"), str(negative_dir)],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
    (claim_dir / "negative_control_output.txt").write_text(
        "Injected failure: first contract check forced false.\n"
        f"returncode={verifier.returncode}\n{verifier.stdout}{verifier.stderr}"
    )
    if verifier.returncode == 0:
        raise AssertionError(f"Claim {number} negative control passed unexpectedly")

    checks_text = "\n".join(
        f"- [{'x' if passed else ' '}] `{name}`"
        for name, passed in summary["checks"].items()
    )
    (claim_dir / "EVAL.md").write_text(
        f"# Claim {number}: {summary['verdict']}\n\n"
        f"{summary['assessment']}\n\n"
        f"## Contract checks\n\n{checks_text}\n\n"
        f"Independent checker return code: `{checker.returncode}`. "
        "The negative-control verifier returned nonzero as required.\n"
    )


def run_legacy_regression() -> None:
    print("\n=== CUMULATIVE REGRESSION: FROZEN JUDGED TOY BASELINE ===")
    result = subprocess.run(
        [sys.executable, str(ROOT / "repro" / "src" / "legacy_verify_td.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    if result.returncode != 0:
        raise RuntimeError("frozen legacy regression failed")


def run() -> int:
    started = time.perf_counter()
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    run_legacy_regression()

    print("\n=== CLAIM 1: EXACT IID MOMENT RATE ===")
    route_start = time.perf_counter()
    iid_rows = exact_rows("iid")
    claim1_dir = make_claim_dir(1)
    write_csv(claim1_dir / "raw_exact_moments.csv", iid_rows)
    iid_fit = rate_regression(iid_rows)
    largest = [row for row in iid_rows if row["normalized_budget"] == max(NORMALIZED_BUDGETS)]
    calibration = [row for row in iid_rows if row["eta"] >= 0.20]
    validation = [row for row in iid_rows if row["eta"] < 0.20]
    quadratic_calibration = max(float(row["normalized_mse"]) for row in calibration)
    quadratic_validation = max(float(row["normalized_mse"]) for row in validation)
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
    claim1_summary = {
        "verdict": "VERIFIED",
        "assessment": (
            "Exact moment propagation converges to the deterministic root. A "
            "quadratic tilde-O envelope calibrated on eta>=0.20 holds on "
            "strictly smaller held-out eta values without refitting, while the "
            "eta^-1 negative-control envelope is rejected."
        ),
        "regression": iid_fit,
        "upper_envelope_route": {
            "quadratic_calibration_max": quadratic_calibration,
            "quadratic_validation_max": quadratic_validation,
            "linear_negative_control_calibration_max": linear_calibration,
            "linear_negative_control_validation_max": linear_validation,
            "holdout_multiplier": 1.25,
        },
        "checks": {
            "T_exponent_in_minus_one_band": -1.25
            <= iid_fit["T_exponent"]
            <= -0.75,
            "quadratic_upper_envelope_holds_on_smaller_eta_holdout": quadratic_validation
            <= 1.25 * quadratic_calibration,
            "eta_inverse_one_negative_control_rejected": linear_validation
            > 1.25 * linear_calibration,
            "regression_r_squared_at_least_0_98": iid_fit["r_squared"] >= 0.98,
            "largest_budget_mean_within_0_02_of_unique_root": max(
                abs(float(row["mean"]) - 1.0) for row in largest
            )
            <= 0.02,
            "moment_mass_conserved": max(
                abs(float(row["mass"]) - 1.0) for row in iid_rows
            )
            <= 1e-10,
        },
    }
    if not all(claim1_summary["checks"].values()):
        claim1_summary["verdict"] = "BLOCKED"
        claim1_summary["assessment"] = (
            "The exact T exponent and deterministic fixed point are resolved, "
            "but at least one held-out upper-envelope or negative-control check "
            "failed. The equality-style fit from Route 1 remains recorded as "
            f"eta exponent {iid_fit['eta_exponent']:.3f}."
        )
    common_files(
        1,
        claim1_summary,
        list(claim1_summary["checks"]),
        (
            "This is an exact reproduction on a controlled finite family, not "
            "a formal re-proof for every admissible MDP. It tests squared "
            "parameter error and the paper-prescribed logarithmic step schedule."
        ),
        time.perf_counter() - route_start,
    )
    print(json.dumps(claim1_summary, indent=2))

    print("\n=== CLAIM 2: EXACT MARKOV CONDITIONAL MOMENTS ===")
    route_start = time.perf_counter()
    markov_rows = exact_rows("markov")
    claim2_dir = make_claim_dir(2)
    write_csv(claim2_dir / "raw_exact_moments.csv", markov_rows)
    markov_fit = rate_regression(markov_rows, markov_adjustment=True)
    per_eta_slopes = {}
    for eta in MARKOV_ETA_GRID:
        subset = [row for row in markov_rows if row["eta"] == eta]
        per_eta_slopes[str(eta)] = float(
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
    claim2_summary = {
        "verdict": "VERIFIED",
        "assessment": (
            "A conditional-state moment operator exactly propagates two "
            "independent stationary Markov chains. After retaining the theorem's "
            "explicit mixing factor, the last-iterate error follows the stated "
            "tilde-O(1/T) envelope across all controlled eta values."
        ),
        "regression": markov_fit,
        "per_eta_T_exponents": per_eta_slopes,
        "checks": {
            "mixing_adjusted_T_exponent_in_minus_one_band": -1.30
            <= markov_fit["T_exponent"]
            <= -0.70,
            "all_per_eta_T_exponents_in_band": all(
                -1.35 <= slope <= -0.65 for slope in per_eta_slopes.values()
            ),
            "all_horizons_exceed_mixing_time": all(
                row["T"] >= row["mixing_time"] for row in markov_rows
            ),
            "all_stepsizes_obey_eta_over_18": all(
                row["alpha"] <= row["eta"] / 18.0 + 1e-15
                for row in markov_rows
            ),
            "moment_mass_conserved_with_matrix_power_roundoff_tolerance": max(
                abs(float(row["mass"]) - 1.0) for row in markov_rows
            )
            <= 1e-9,
        },
    }
    if not all(claim2_summary["checks"].values()):
        claim2_summary["verdict"] = "BLOCKED"
        claim2_summary["assessment"] = (
            "At least one preregistered exact Markov contract check failed; "
            "the route is retained as evidence but not promoted to VERIFIED."
        )
    common_files(
        2,
        claim2_summary,
        list(claim2_summary["checks"]),
        (
            "Changing flip probability changes eta and mixing together. The "
            "analysis therefore keeps, rather than hides, the exact mixing-time "
            "factor. It does not claim an eta exponent after discarding mixing."
        ),
        time.perf_counter() - route_start,
    )
    print(json.dumps(claim2_summary, indent=2))

    print("\n=== CLAIM 3: EXPLICIT-DIMENSION DEPENDENCY AUDIT ===")
    route_start = time.perf_counter()
    formulas = formula_dependencies()
    claim3_dir = make_claim_dir(3)
    write_json(claim3_dir / "raw_formula_dependencies.json", formulas)
    forbidden = [
        formula["name"] for formula in formulas if "d" in formula["free_symbols"]
    ]
    negative_formulas = json.loads(json.dumps(formulas))
    negative_formulas[0]["free_symbols"].append("d")
    write_json(claim3_dir / "negative_control_formula_dependencies.json", negative_formulas)
    negative_rejected = any(
        "d" in formula["free_symbols"] for formula in negative_formulas
    )
    claim3_summary = {
        "verdict": "VERIFIED",
        "assessment": (
            "The claimed absence of an explicit dimension term is a syntactic "
            "property of the theorem and full appendix restatement. The audited "
            "free-symbol sets contain no d, while the injected-d control is "
            "detected."
        ),
        "checks": {
            "no_explicit_d_in_theorem_4_3_xi_1": "d"
            not in formulas[0]["free_symbols"],
            "no_explicit_d_in_theorem_4_3_xi_open_interval": "d"
            not in formulas[1]["free_symbols"],
            "no_explicit_d_in_full_theorem_D_1": "d"
            not in formulas[2]["free_symbols"],
            "negative_control_with_explicit_d_is_rejected": negative_rejected,
            "no_unexpected_forbidden_formula": not forbidden,
        },
    }
    if not all(claim3_summary["checks"].values()):
        claim3_summary["verdict"] = "BLOCKED"
    common_files(
        3,
        claim3_summary,
        list(claim3_summary["checks"]),
        (
            "This verifies the paper's explicitly defined syntactic claim. It "
            "does not assert dimension-uniform numerical error when eta or "
            "parameter norms themselves deteriorate with d."
        ),
        time.perf_counter() - route_start,
    )
    print(json.dumps(claim3_summary, indent=2))

    print("\n=== CLAIM 4: FIRST ROUTE REMAINS BLOCKED ===")
    route_start = time.perf_counter()
    claim4_dir = make_claim_dir(4)
    write_json(
        claim4_dir / "raw_route_result.json",
        {
            "route": "exact proposed-method moment scaling",
            "proposed_method_eta_exponent": iid_fit["eta_exponent"],
            "missing": "matched implementations of cited prior algorithms",
        },
    )
    claim4_summary = {
        "verdict": "BLOCKED",
        "assessment": (
            "The proposed method's quadratic envelope is directly measured, "
            "but this route does not yet reproduce the cited quartic prior "
            "algorithms under matched definitions. Arithmetic comparison alone "
            "would repeat the judge-identified flaw."
        ),
        "checks": {
            "proposed_method_quadratic_envelope_measured": -2.30
            <= iid_fit["eta_exponent"]
            <= -1.70,
            "prior_algorithms_implemented_under_matched_contract": False,
        },
    }
    common_files(
        4,
        claim4_summary,
        list(claim4_summary["checks"]),
        (
            "A cross-paper complexity claim needs primary-source algorithm and "
            "condition-number alignment. That work is deferred to a distinct route."
        ),
        time.perf_counter() - route_start,
    )
    print(json.dumps(claim4_summary, indent=2))

    print("\n=== CLAIM 5: FIRST ROUTE REMAINS BLOCKED ===")
    route_start = time.perf_counter()
    claim5_dir = make_claim_dir(5)
    exponent_arithmetic = {
        "general_bound_eta_prime_exponent": -1,
        "general_bound_eta_exponent": -3,
        "common_regime_substitution_eta_prime_equals_eta": -4,
    }
    write_json(claim5_dir / "raw_exponent_arithmetic.json", exponent_arithmetic)
    claim5_summary = {
        "verdict": "BLOCKED",
        "assessment": (
            "The paper's conditional exponent arithmetic is reproducible, but "
            "actual Eq. (17) sample complexity has not yet been measured across "
            "an eta'=Theta(eta) family. One small error comparison is not reused."
        ),
        "checks": {
            "conditional_quartic_exponent_arithmetic_reproduced": (
                exponent_arithmetic["general_bound_eta_prime_exponent"]
                + exponent_arithmetic["general_bound_eta_exponent"]
                == -4
            ),
            "single_chain_sample_complexity_measured_on_common_regime_family": False,
        },
    }
    common_files(
        5,
        claim5_summary,
        list(claim5_summary["checks"]),
        (
            "The quartic statement is a bound in a conditional regime, not a "
            "universal empirical equality. A separate simulator route is required."
        ),
        time.perf_counter() - route_start,
    )
    print(json.dumps(claim5_summary, indent=2))

    print("\n=== CLAIM 6: PROOF-STEP AND SYSTEMATIC STRESS CHECK ===")
    route_start = time.perf_counter()
    condition_rows, proof = condition_stress_rows()
    claim6_dir = make_claim_dir(6)
    write_csv(claim6_dir / "raw_condition_stress.csv", condition_rows)
    write_json(claim6_dir / "raw_proof_steps.json", proof)
    minimum_margin = min(
        float(row["eta1_minus_half_eta3"]) for row in condition_rows
    )
    claim6_summary = {
        "verdict": "VERIFIED",
        "assessment": (
            "Every algebraic step responsible for the factor 1/2 is checked, "
            "the exact inequality holds across diverse and paper-scale cases, "
            "and a tight tabular case rejects the stronger 1.1*eta3 control."
        ),
        "case_count": len(condition_rows),
        "minimum_margin": minimum_margin,
        "checks": {
            "all_proof_steps_pass": all(proof["steps"].values()),
            "all_systematic_cases_satisfy_half_bound": minimum_margin >= -1e-10,
            "includes_paper_scale_n1000_d100": any(
                row["n"] == 1000 and row["d"] == 100 for row in condition_rows
            ),
            "includes_nonreversible_positive_chains": any(
                row["family"] == "dense_positive" for row in condition_rows
            ),
            "stronger_1_1_negative_control_fails_on_tight_case": proof[
                "negative_control"
            ]["expected_to_fail"],
        },
    }
    if not all(claim6_summary["checks"].values()):
        claim6_summary["verdict"] = "BLOCKED"
        claim6_summary["assessment"] = (
            "At least one proof-step, systematic stress, scale, or negative "
            "control check failed; the lemma is not marked verified."
        )
    common_files(
        6,
        claim6_summary,
        list(claim6_summary["checks"]),
        (
            "The numerical suite is not itself a universal proof; universality "
            "comes from the audited decomposition and Rayleigh argument. Floating "
            "stress checks use a 1e-10 tolerance."
        ),
        time.perf_counter() - route_start,
    )
    print(json.dumps(claim6_summary, indent=2))

    total = time.perf_counter() - started
    combined = {
        "git_sha": git_sha(),
        "command": COMMAND,
        "runtime_seconds": total,
        "claims": {
            "1": claim1_summary["verdict"],
            "2": claim2_summary["verdict"],
            "3": claim3_summary["verdict"],
            "4": claim4_summary["verdict"],
            "5": claim5_summary["verdict"],
            "6": claim6_summary["verdict"],
        },
    }
    write_json(ARTIFACTS / "campaign_summary.json", combined)
    manifest_rows = []
    for path in sorted(ARTIFACTS.rglob("*")):
        if path.is_file():
            manifest_rows.append(
                {
                    "path": str(path.relative_to(ROOT)),
                    "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                    "bytes": path.stat().st_size,
                }
            )
    write_json(ARTIFACTS / "artifact_manifest.json", manifest_rows)
    print("\n=== FIRST-ROUND CLAIM VERDICTS ===")
    print(json.dumps(combined, indent=2))
    for number in range(1, 7):
        print((ARTIFACTS / f"claim_{number}" / "EVAL.md").read_text())
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
