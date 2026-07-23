"""Vectorized Monte Carlo checks for the paper's Eq. (17) single-chain TD.

The controlled two-state family keeps the transition gap fixed and varies the
feature scale.  Consequently eta' / eta is constant, which is the explicit
"common regime" required by Theorem 4.4's quartic specialization.
"""

from __future__ import annotations

import math

import numpy as np


ETA_GRID = (0.30, 0.22, 0.16, 0.12, 0.09)
QUARTIC_BUDGETS = (4, 8, 16, 32)
SEEDS = tuple(range(128))
DELTA = 0.25


def family_parameters(eta: float) -> dict[str, float]:
    # phi=(0, scale), mu=(1/2,1/2).  Hence
    # eta = scale^2 * (delta/2 + 1/4) and eta'=scale^2/2.
    coefficient = DELTA / 2.0 + 0.25
    scale = math.sqrt(eta / coefficient)
    eta_prime = 0.5 * scale**2
    return {
        "eta": eta,
        "eta_prime": eta_prime,
        "eta_prime_over_eta": eta_prime / eta,
        "scale": scale,
    }


def _project(values: np.ndarray, radius: float) -> np.ndarray:
    return np.clip(values, -radius, radius)


def simulate_condition(
    eta: float,
    quartic_budget: int,
    *,
    freeze_w: bool = False,
) -> dict[str, float | int | str]:
    family = family_parameters(eta)
    eta_prime = family["eta_prime"]
    scale = family["scale"]
    horizon = math.ceil(quartic_budget / eta**4)
    alpha = min(eta / 32.0, 4.0 * math.log(horizon + 1.0) / (eta * horizon))
    beta = alpha
    theta_radius = 2.0 / math.sqrt(eta_prime)
    w_radius = 1.1
    reward_noise = 0.10
    reward_means = np.array([-DELTA * scale, DELTA * scale])
    dirichlet = DELTA * scale**2 / 2.0
    mean_feature_squared = scale**2 / 4.0
    target_theta = dirichlet / (dirichlet + mean_feature_squared)
    r_max = float(np.max(np.abs(reward_means)) + reward_noise)
    stability_aux_squared = eta / (r_max + 2.0 * theta_radius) ** 2
    zeta = eta - 0.5 * stability_aux_squared * (
        r_max + 2.0 * theta_radius
    ) ** 2

    rng = np.random.default_rng(700_000 + int(round(eta * 10000)) * 100 + quartic_budget)
    states = rng.integers(0, 2, size=len(SEEDS), dtype=np.int8)
    theta = np.zeros(len(SEEDS), dtype=float)
    w = np.zeros(len(SEEDS), dtype=float)
    phi = np.array([0.0, scale])

    for _ in range(horizon):
        flips = rng.random(len(SEEDS)) < DELTA
        next_states = np.where(flips, 1 - states, states).astype(np.int8)
        reward = reward_means[states] + np.where(
            rng.random(len(SEEDS)) < 0.5, -reward_noise, reward_noise
        )
        phi_state = phi[states]
        phi_next = phi[next_states]
        old_w = w
        td_part = reward + (phi_next - phi_state) * theta
        correction = (reward + phi_state * theta) * old_w
        theta = _project(theta + alpha * (td_part * phi_state - correction), theta_radius)
        if not freeze_w:
            w = _project(w + beta * (phi_state - w), w_radius)
        states = next_states

    squared_errors = np.square(theta - target_theta)
    mse = float(np.mean(squared_errors))
    standard_error = float(np.std(squared_errors, ddof=1) / math.sqrt(len(SEEDS)))
    return {
        "route": "w_frozen_negative_control" if freeze_w else "paper_eq17",
        "eta": eta,
        "eta_prime": eta_prime,
        "eta_prime_over_eta": family["eta_prime_over_eta"],
        "scale": scale,
        "delta": DELTA,
        "quartic_budget": quartic_budget,
        "T": horizon,
        "alpha": alpha,
        "beta": beta,
        "rho0": beta / alpha,
        "theta_radius": theta_radius,
        "w_radius": w_radius,
        "r_max": r_max,
        "stability_aux_squared": stability_aux_squared,
        "zeta": zeta,
        "replicates": len(SEEDS),
        "mse": mse,
        "mse_standard_error": standard_error,
        "mse_ci95_low": max(0.0, mse - 1.96 * standard_error),
        "mse_ci95_high": mse + 1.96 * standard_error,
        "mean_theta": float(np.mean(theta)),
        "mean_w": float(np.mean(w)),
        "target_theta": target_theta,
        "target_w": scale / 2.0,
        "dirichlet": dirichlet,
        "mean_feature_squared": mean_feature_squared,
        "projected_root_residual": (
            dirichlet - (dirichlet + mean_feature_squared) * target_theta
        ),
        "quartic_normalized_mse": mse
        * horizon
        * eta**4
        / math.log(horizon + 1.0),
        "cubic_normalized_mse": mse
        * horizon
        * eta**3
        / math.log(horizon + 1.0),
    }


def single_chain_rows() -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    rows = [
        simulate_condition(eta, budget)
        for eta in ETA_GRID
        for budget in QUARTIC_BUDGETS
    ]
    controls = [
        simulate_condition(eta, max(QUARTIC_BUDGETS), freeze_w=True)
        for eta in (max(ETA_GRID), min(ETA_GRID))
    ]
    return rows, controls


def rate_regression(rows: list[dict[str, object]]) -> dict[str, float]:
    design = []
    response = []
    for row in rows:
        design.append(
            [1.0, math.log(float(row["T"])), math.log(float(row["eta"]))]
        )
        response.append(
            math.log(
                max(
                    float(row["mse"]) / math.log(float(row["T"]) + 1.0),
                    1e-300,
                )
            )
        )
    coefficients, _, _, _ = np.linalg.lstsq(
        np.asarray(design), np.asarray(response), rcond=None
    )
    fitted = np.asarray(design) @ coefficients
    total = float(np.square(np.asarray(response) - np.mean(response)).sum())
    unexplained = float(np.square(np.asarray(response) - fitted).sum())
    return {
        "intercept": float(coefficients[0]),
        "T_exponent": float(coefficients[1]),
        "eta_exponent": float(coefficients[2]),
        "r_squared": 1.0 - unexplained / total if total > 0.0 else 1.0,
    }
