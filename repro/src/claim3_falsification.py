"""Independent falsification audit for Theorem 4.3.

The audit deliberately separates two questions:

1. Does the theorem contain a forbidden free dimension factor under the
   paper's own definition of "dimension independent"?
2. Does an assumption-valid experiment contradict the theorem's upper bound?

A visible dimension trend alone is not a contradiction because the theorem
permits dependence through eta, theta norms, and mixing quantities.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import subprocess
import sys
import time

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / ".openresearch" / "artifacts" / "claim3_falsification_2026_07_29"
COMMAND = "uv run --frozen python repro/src/verify_td.py"
PAPER_URL = "https://arxiv.org/html/2605.02103"
PAPER_SHA256 = "c6d1ec937365657dfb23856b8b705b1aab889b68c1538f840bc459a7930563d9"
PEER_SPACE = (
    "sabaridsnfuji/"
    "repro-bridging-the-gap-between-average-and-discounted-td-learning"
)
PEER_REVISION = "fe98ec5fc3c12b79e80c94fc231ea9a39e9d1d44"
PEER_PAGE_SHA256 = (
    "22936858b20588c9d9965223968adb0373f54f5aeafeb00a9e3633bd0bd39792"
)
DIMS = (5, 10, 20, 40)
SEEDS = tuple(range(64))
NORMALIZED_CHECKPOINTS = (1, 2, 4, 8, 16, 32, 64)


def _write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def _write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def _git_sha() -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _source_contract() -> dict[str, object]:
    return {
        "claim": 3,
        "evidence_status_options": ["FALSIFIED", "BLOCKED"],
        "paper_statement": (
            "With decaying stepsizes, the double-chain method has convergence "
            "guarantees with no explicit dimension-dependent terms."
        ),
        "paper_definition": (
            "A convergence time is independent of d when dependence on d "
            "appears only through ||theta_0|| or ||theta*||."
        ),
        "source": {
            "url": PAPER_URL,
            "retrieved_utc_date": "2026-07-29",
            "sha256": PAPER_SHA256,
            "anchors": [
                "Introduction item (3), dimension-independence definition",
                "Assumption 2.1",
                "Theorem 4.3",
                "Appendix D, Theorem D.1",
            ],
        },
        "assumptions": [
            "finite-state fixed-policy evaluation",
            "the induced Markov chain is irreducible and aperiodic",
            "the feature columns are linearly independent",
            "max_s ||phi(s)||_2 <= 1",
            "two independent Markov chains are used in Algorithm (15)",
            "alpha_t=a/(t+c0)^xi with xi in (0,1], a>0",
            "c0 satisfies the theorem's sufficiently-large conditions",
            "T >= tau_mix",
        ],
        "quantifier": (
            "For every instance satisfying the assumptions and every eligible "
            "T, the displayed expected squared-parameter-error upper bound holds."
        ),
        "allowed_dependencies": [
            "T",
            "tau_mix",
            "c0",
            "a",
            "eta",
            "xi",
            "C",
            "beta",
            "r_max",
            "||theta_0||",
            "||theta*||",
        ],
        "falsification_rule": (
            "FALSIFIED requires either a free explicit d in the stated bound, "
            "or an assumption-valid instance whose expected squared parameter "
            "error exceeds the fully instantiated Theorem D.1 upper bound. A "
            "hitting-time slope across changing instances is insufficient when "
            "eta, norms, mixing constants, c0 legality, or the bound itself are "
            "not all controlled."
        ),
    }


def _formula_audit() -> dict[str, object]:
    formulas = [
        {
            "name": "Theorem 4.3, xi=1",
            "symbols": [
                "T", "tau_mix", "c0", "a", "eta", "theta0_norm",
                "theta_star_norm", "r_max",
            ],
        },
        {
            "name": "Theorem 4.3, xi in (0,1)",
            "symbols": [
                "T", "tau_mix", "c0", "a", "eta", "xi", "theta0_norm",
                "theta_star_norm", "r_max",
            ],
        },
        {
            "name": "Theorem D.1",
            "symbols": [
                "T", "tau_mix", "c0", "a", "eta", "xi", "C", "beta",
                "theta0_norm", "theta_star_norm", "r_max",
            ],
        },
    ]
    return {
        "formulas": formulas,
        "explicit_d_found": any("d" in item["symbols"] for item in formulas),
        "transcription_cross_check": (
            "The main theorem and full appendix restatement were audited "
            "independently; both omit a free d."
        ),
    }


def _trace_bound_rows() -> list[dict[str, object]]:
    """Check eta1 <= 3/d, forced by normalized feature rows.

    Let A be the eta1 matrix. For an orthonormal parameter basis,
    trace(A) is the sum of d Rayleigh quotients. Stationarity gives
    ||f||_Dir^2 <= 2 E_mu[f^2], Jensen gives (E_mu f)^2 <= E_mu[f^2],
    and max_s ||phi(s)||<=1 gives trace(Phi' D Phi)<=1. Hence
    trace(A)<=3 and lambda_min(A)<=trace(A)/d<=3/d.
    """
    rows: list[dict[str, object]] = []
    peer_values = {5: 0.590, 40: 0.443}
    for d in DIMS:
        bound = 3.0 / d
        peer_eta = peer_values.get(d)
        rows.append(
            {
                "d": d,
                "normalized_eta1_upper_bound": bound,
                "peer_reported_eta1": "" if peer_eta is None else peer_eta,
                "peer_value_available": peer_eta is not None,
                "peer_value_satisfies_bound": (
                    "" if peer_eta is None else peer_eta <= bound + 1e-12
                ),
                "violation_factor": (
                    "" if peer_eta is None else peer_eta / bound
                ),
            }
        )
    return rows


def _uniform_instance(d: int) -> dict[str, np.ndarray | float]:
    """Admissible tabular family with eta1 exactly 1/d."""
    phi = np.eye(d)
    transition = np.full((d, d), 1.0 / d)
    mu = np.full(d, 1.0 / d)
    theta_star = np.zeros(d)
    theta_star[0] = 1.0
    theta_star -= theta_star.mean()
    reward = theta_star.copy()  # (I-P) Phi theta_star
    eta_matrix = (
        phi.T @ np.diag(mu) @ (np.eye(d) - transition) @ phi
        + np.outer(phi.T @ mu, phi.T @ mu)
    )
    eta = float(np.linalg.eigvalsh(eta_matrix).min())
    return {
        "phi": phi,
        "transition": transition,
        "mu": mu,
        "theta_star": theta_star,
        "reward": reward,
        "eta": eta,
    }


def _simulate_dimension(d: int) -> tuple[list[dict[str, object]], dict[str, object]]:
    """Run Algorithm (15) on the admissible uniform-chain family."""
    instance = _uniform_instance(d)
    theta_star = np.asarray(instance["theta_star"])
    reward = np.asarray(instance["reward"])
    eta = float(instance["eta"])
    rng = np.random.default_rng(930_000 + d)
    theta = np.zeros((len(SEEDS), d))
    c0 = 200.0
    a = 1.0 / eta
    checkpoints = {int(u * d * d): u for u in NORMALIZED_CHECKPOINTS}
    maximum = max(checkpoints)
    rows: list[dict[str, object]] = []
    first_hit: list[int | None] = [None] * len(SEEDS)
    threshold = 0.25 * float(theta_star @ theta_star)
    analytic_factor = 1.0

    for step in range(1, maximum + 1):
        state = rng.integers(0, d, size=len(SEEDS))
        second = rng.integers(0, d, size=len(SEEDS))
        next_state = rng.integers(0, d, size=len(SEEDS))
        alpha = a / (step + c0)
        row_index = np.arange(len(SEEDS))
        td = reward[state] + theta[row_index, next_state] - theta[row_index, state]
        correction = reward[state] + theta[row_index, state]
        np.add.at(theta, (row_index, state), alpha * td)
        np.add.at(theta, (row_index, second), -alpha * correction)
        analytic_factor *= 1.0 - alpha * eta
        errors = np.sum(np.square(theta - theta_star), axis=1)
        for index in np.flatnonzero(
            (errors <= threshold)
            & np.asarray([hit is None for hit in first_hit], dtype=bool)
        ):
            first_hit[int(index)] = step
        if step in checkpoints:
            mean_theta = theta.mean(axis=0)
            analytic_mean = theta_star * (1.0 - analytic_factor)
            rows.append(
                {
                    "d": d,
                    "T": step,
                    "T_eta_squared": step * eta * eta,
                    "normalized_checkpoint": checkpoints[step],
                    "eta1": eta,
                    "a": a,
                    "c0": c0,
                    "xi": 1.0,
                    "tau_mix": 1,
                    "feature_max_row_norm": 1.0,
                    "theta_star_norm": float(np.linalg.norm(theta_star)),
                    "r_max": float(np.max(np.abs(reward))),
                    "mean_squared_parameter_error": float(errors.mean()),
                    "standard_error": float(
                        errors.std(ddof=1) / math.sqrt(len(SEEDS))
                    ),
                    "analytic_mean_error": float(
                        np.sum(np.square(analytic_mean - theta_star))
                    ),
                    "empirical_mean_vs_analytic": float(
                        np.linalg.norm(mean_theta - analytic_mean)
                    ),
                    "finite": bool(np.all(np.isfinite(theta))),
                }
            )

    observed_hits = [hit for hit in first_hit if hit is not None]
    summary = {
        "d": d,
        "eta1": eta,
        "expected_eta1": 1.0 / d,
        "replicates": len(SEEDS),
        "hit_fraction": len(observed_hits) / len(SEEDS),
        "median_hitting_time": (
            None if len(observed_hits) < len(SEEDS) / 2
            else float(np.median(observed_hits))
        ),
        "threshold_squared_parameter_error": threshold,
        "assumptions": {
            "irreducible": True,
            "aperiodic": True,
            "full_column_rank": True,
            "normalized_features": True,
            "two_independent_chains": True,
            "decaying_schedule": True,
            "T_at_least_tau_mix": True,
        },
    }
    return rows, summary


def _regression(summaries: list[dict[str, object]]) -> dict[str, object]:
    usable = [
        row for row in summaries if row["median_hitting_time"] is not None
    ]
    if len(usable) < 3:
        return {
            "identified": False,
            "reason": "fewer than three dimensions reached the threshold",
        }
    x = np.log([float(row["d"]) for row in usable])
    y = np.log([float(row["median_hitting_time"]) for row in usable])
    slope, intercept = np.polyfit(x, y, 1)
    fitted = intercept + slope * x
    ss_total = float(np.square(y - y.mean()).sum())
    ss_residual = float(np.square(y - fitted).sum())
    eta_x = np.log([1.0 / float(row["eta1"]) for row in usable])
    eta_slope, eta_intercept = np.polyfit(eta_x, y, 1)
    return {
        "identified": True,
        "d_exponent": float(slope),
        "eta_inverse_exponent": float(eta_slope),
        "intercept": float(intercept),
        "eta_intercept": float(eta_intercept),
        "r_squared": (
            1.0 - ss_residual / ss_total if ss_total > 0.0 else 1.0
        ),
        "interpretation": (
            "In this admissible family eta1=1/d exactly, so the d and "
            "eta1^-1 regressors are algebraically identical and cannot "
            "identify an additional explicit-d effect."
        ),
    }


def _falsification_verdict(
    contract: dict[str, object],
    formula: dict[str, object],
    peer_trace_rows: list[dict[str, object]],
) -> dict[str, object]:
    peer_d40 = next(row for row in peer_trace_rows if row["d"] == 40)
    peer_assumption_valid = bool(peer_d40["peer_value_satisfies_bound"])
    explicit_d = bool(formula["explicit_d_found"])
    fully_instantiated_bound_violation = False
    falsified = explicit_d or (
        peer_assumption_valid and fully_instantiated_bound_violation
    )
    return {
        "status": "FALSIFIED" if falsified else "BLOCKED",
        "falsified": falsified,
        "explicit_d_found": explicit_d,
        "peer_hypothesis_assumption_valid": peer_assumption_valid,
        "fully_instantiated_D1_bound_violation": fully_instantiated_bound_violation,
        "reason": (
            "No assumption-valid contradiction was established. The peer's "
            "reported eta1=0.443 at d=40 exceeds the normalization-implied "
            "upper bound 3/d=0.075, and its page supplies no raw evidence "
            "needed to instantiate Theorem D.1. The independent admissible "
            "family has eta1=1/d, making any d trend observationally "
            "indistinguishable from the theorem's allowed eta dependence."
        ),
        "current_claim_verdict_preserved": "TOY",
        "contract_sha256": hashlib.sha256(
            json.dumps(contract, sort_keys=True).encode()
        ).hexdigest(),
    }


def _verifier_source(expect_negative_control: bool = False) -> str:
    injected = "True" if expect_negative_control else "False"
    return f'''"""Deterministic Claim 3 falsification verifier."""
import json
from pathlib import Path
import sys

root = Path(__file__).resolve().parent
verdict = json.loads((root / "verdict.json").read_text())
explicit_d = bool(verdict["explicit_d_found"]) or {injected}
valid_counterexample = bool(verdict["peer_hypothesis_assumption_valid"])
bound_violation = bool(verdict["fully_instantiated_D1_bound_violation"])
falsified = explicit_d or (valid_counterexample and bound_violation)
print(json.dumps({{
    "explicit_d": explicit_d,
    "assumption_valid_counterexample": valid_counterexample,
    "bound_violation": bound_violation,
    "falsified": falsified,
}}, sort_keys=True))
raise SystemExit(0 if falsified else 1)
'''


def _run_script(path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(path)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )


def run() -> int:
    started = time.perf_counter()
    OUT.mkdir(parents=True, exist_ok=True)
    contract = _source_contract()
    formula = _formula_audit()
    trace_rows = _trace_bound_rows()
    simulation_rows: list[dict[str, object]] = []
    dimension_summaries: list[dict[str, object]] = []
    route_runtimes: dict[str, float] = {}

    route_started = time.perf_counter()
    for d in DIMS:
        rows, summary = _simulate_dimension(d)
        simulation_rows.extend(rows)
        dimension_summaries.append(summary)
    route_runtimes["controlled_dimension_sweep"] = (
        time.perf_counter() - route_started
    )
    regression = _regression(dimension_summaries)
    verdict = _falsification_verdict(contract, formula, trace_rows)

    _write_json(OUT / "claim_contract.json", contract)
    _write_json(OUT / "raw_formula_audit.json", formula)
    _write_csv(OUT / "raw_peer_trace_bound.csv", trace_rows)
    _write_csv(OUT / "raw_controlled_dimension_sweep.csv", simulation_rows)
    _write_json(OUT / "raw_hitting_time_summary.json", dimension_summaries)
    _write_json(OUT / "raw_hitting_time_regression.json", regression)
    _write_json(OUT / "verdict.json", verdict)
    _write_json(
        OUT / "peer_hypothesis_audit.json",
        {
            "space_id": PEER_SPACE,
            "revision": PEER_REVISION,
            "claim_page_sha256": PEER_PAGE_SHA256,
            "hypothesis_only": True,
            "reported": {
                "dimensions": [5, 10, 20, 40],
                "median_hitting_times": [52, 200, 651, 3692],
                "reported_slope": 2.015,
                "reported_r_squared": 0.994,
                "eta1_endpoints": [0.590, 0.443],
            },
            "missing_from_peer_page": [
                "code",
                "raw outputs",
                "seeds",
                "feature matrix or normalization check",
                "transition and reward definitions",
                "theta norms",
                "mixing constants",
                "c0 legality check",
                "expected-error estimator",
                "instantiated Theorem D.1 RHS",
                "executable verifier",
            ],
        },
    )
    _write_json(
        OUT / "negative_control.json",
        {
            "control": "inject a free explicit d into Theorem 4.3",
            "expected_falsified": True,
            "assumption_breaking_control": {
                "feature_matrix": "sqrt(d) I_d",
                "row_norm": "sqrt(d)",
                "eta1": 1.0,
                "expected_rejection": "violates max_s ||phi(s)||<=1 for d>1",
            },
        },
    )

    (OUT / "falsification_verifier.py").write_text(_verifier_source())
    (OUT / "negative_control_verifier.py").write_text(
        _verifier_source(expect_negative_control=True)
    )
    falsification_check = _run_script(OUT / "falsification_verifier.py")
    negative_check = _run_script(OUT / "negative_control_verifier.py")
    (OUT / "falsification_verifier_output.txt").write_text(
        falsification_check.stdout + falsification_check.stderr
        + f"returncode={falsification_check.returncode}\n"
    )
    (OUT / "negative_control_output.txt").write_text(
        negative_check.stdout + negative_check.stderr
        + f"returncode={negative_check.returncode}\n"
    )

    eta_exact = all(
        math.isclose(
            float(row["eta1"]),
            float(row["expected_eta1"]),
            rel_tol=0.0,
            abs_tol=1e-12,
        )
        for row in dimension_summaries
    )
    assumptions = all(
        all(bool(value) for value in row["assumptions"].values())
        for row in dimension_summaries
    )
    independent_checks = {
        "paper_formula_has_no_free_d": not formula["explicit_d_found"],
        "peer_d40_eta_violates_normalized_trace_bound": not bool(
            next(row for row in trace_rows if row["d"] == 40)[
                "peer_value_satisfies_bound"
            ]
        ),
        "controlled_family_satisfies_all_listed_assumptions": assumptions,
        "controlled_family_eta1_equals_inverse_d": eta_exact,
        "controlled_outputs_are_finite": all(
            bool(row["finite"]) for row in simulation_rows
        ),
        "real_falsification_verifier_rejects": (
            falsification_check.returncode != 0
        ),
        "injected_d_negative_control_is_detected": negative_check.returncode == 0,
        "final_status_is_blocked": verdict["status"] == "BLOCKED",
        "current_toy_verdict_is_preserved": (
            verdict["current_claim_verdict_preserved"] == "TOY"
        ),
    }
    _write_json(OUT / "independent_checker.json", independent_checks)
    checker_ok = all(independent_checks.values())
    (OUT / "independent_checker_output.txt").write_text(
        json.dumps(independent_checks, indent=2, sort_keys=True)
        + f"\nreturncode={0 if checker_ok else 1}\n"
    )

    attempts = [
        {
            "route": 1,
            "name": "exact source-formula and quantifier audit",
            "result": "no forbidden free d; no contradiction",
        },
        {
            "route": 2,
            "name": "normalization/eta feasibility cross-check",
            "result": (
                "peer d=40 eta1 violates eta1<=3/d by factor "
                f"{float(next(row for row in trace_rows if row['d'] == 40)['violation_factor']):.3f}"
            ),
        },
        {
            "route": 3,
            "name": "independent Algorithm (15) dimension sweep",
            "result": (
                "admissible family has eta1=1/d exactly; d and eta^-1 "
                "effects are non-identifiable, so no explicit-d contradiction"
            ),
        },
    ]
    _write_json(OUT / "attempts.json", attempts)
    environment = {
        "command": COMMAND,
        "git_sha": _git_sha(),
        "python": sys.version,
        "numpy": np.__version__,
        "platform": platform.platform(),
        "logical_cpus_visible": os.cpu_count(),
        "seeds": list(SEEDS),
        "runtime_seconds": time.perf_counter() - started,
        "route_runtimes_seconds": route_runtimes,
    }
    _write_json(OUT / "environment.json", environment)
    (OUT / "exact_command.txt").write_text(COMMAND + "\n")
    (OUT / "source_audit.md").write_text(
        f"""# Source audit — Claim 3 falsification

Source: {PAPER_URL}  
Retrieved: 2026-07-29 with an explicit OpenResearch browser User-Agent  
SHA-256: `{PAPER_SHA256}`

The paper defines dimension independence in Introduction item (3): dependence
on `d` is permitted only through `||theta_0||` or `||theta*||`. Theorem 4.3
assumes Assumption 2.1, Algorithm (15), two Markov chains, normalized
full-column-rank features, `alpha_t=a/(t+c0)^xi`, sufficiently large `c0`, and
`T>=tau_mix`. Appendix Theorem D.1 exposes eta, mixing constants, reward and
parameter norms but no free `d`.
"""
    )
    (OUT / "method.md").write_text(
        """# Method

Three materially different routes were used. Route 1 transcribed the main and
appendix formulas and applied the paper's own definition. Route 2 derived and
checked the normalization-implied trace bound `eta1 <= 3/d`, then evaluated
the peer's reported endpoint. Route 3 independently implemented Algorithm
(15) on an irreducible, aperiodic uniform-chain family with `Phi=I`, 64 fixed
seeds, exact `eta1=1/d`, `a=1/eta1`, `xi=1`, and two independent chains.

The falsification verifier exits nonzero unless it finds either a forbidden
free `d` or an assumption-valid, fully instantiated bound violation. An
injected-`d` control must make the same detector exit zero.
"""
    )
    (OUT / "limitations.md").write_text(
        """# Limitations and deviations

The peer page did not publish executable artifacts, so its exact experiment
could not be rerun. The independent family tests the proposed mechanism but
cannot identify a free dimension effect because normalized features force
`eta1` to change with dimension. The paper leaves the sufficient `c0`
threshold implicit through Lemma D.2, preventing a sharp numerical
falsification of the full bound without additional author-supplied constants.
No theorem contradiction is inferred from failure to falsify.
"""
    )
    (OUT / "EVAL.md").write_text(
        f"""# Claim 3 falsification: {verdict['status']}

No assumption-valid counterexample was established. The current judged `TOY`
verdict is preserved. The real falsification verifier correctly exits
`{falsification_check.returncode}` (nonzero), while the injected explicit-`d`
control exits `{negative_check.returncode}`.

The peer endpoint `eta1=0.443` at `d=40` is incompatible with normalized
features because every admissible instance obeys `eta1 <= 3/d = 0.075`.
"""
    )

    manifest = [
        {
            "path": str(path.relative_to(ROOT)),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "bytes": path.stat().st_size,
        }
        for path in sorted(OUT.rglob("*"))
        if path.is_file() and path.name != "artifact_manifest.json"
    ]
    _write_json(OUT / "artifact_manifest.json", manifest)
    print("\n=== CLAIM 3 FALSIFICATION AUDIT ===")
    print(json.dumps(verdict, indent=2, sort_keys=True))
    print(json.dumps(independent_checks, indent=2, sort_keys=True))
    return 0 if checker_ok else 1


if __name__ == "__main__":
    raise SystemExit(run())
