"""Appendix-G-scale external-validity checks for double-chain TD.

The task dimensions, feature construction, horizon, and decaying stepsize
match the paper's Random Walk entries.  The transition/reward instance is a
documented synthetic ergodic cycle because the paper does not publish the
learned policy matrices used for its numerical table.
"""

from __future__ import annotations

import math
import time

import numpy as np


TASKS = ((50, 5), (100, 20), (1000, 100))
CHECKPOINTS = (15_000, 50_000, 150_000)
REPLICATES = 6


def _transition(
    states: np.ndarray, rng: np.random.Generator, n: int
) -> np.ndarray:
    draws = rng.random(len(states))
    result = np.where(
        draws < 0.45,
        (states - 1) % n,
        np.where(draws < 0.90, (states + 1) % n, rng.integers(0, n, len(states))),
    )
    return result.astype(np.int64)


def _instance(n: int, d: int) -> dict[str, object]:
    rng = np.random.default_rng(810_000 + n + d)
    indices = np.arange(n)
    value = np.sin(2.0 * np.pi * indices / n) + 0.35 * np.cos(
        6.0 * np.pi * indices / n
    )
    value -= value.mean()
    # P = .45 left + .45 right + .10 uniform.  The uniform term vanishes on
    # this centered value vector.
    p_value = (
        0.45 * np.roll(value, 1)
        + 0.45 * np.roll(value, -1)
        + 0.10 * value.mean()
    )
    reward = value - p_value

    random_columns = rng.binomial(1, 0.5, size=(n, d - 2)).astype(float)
    raw_phi = np.column_stack([random_columns, np.ones(n), value])
    normalization = max(1.0, float(np.linalg.norm(raw_phi, axis=1).max()))
    phi = raw_phi / normalization
    target_theta = np.zeros(d)
    target_theta[-1] = normalization

    # D is uniform and the symmetric cycle kernel makes D(I-P) symmetric.
    shifted_left = np.roll(phi, 1, axis=0)
    shifted_right = np.roll(phi, -1, axis=0)
    p_phi = 0.45 * shifted_left + 0.45 * shifted_right + 0.10 * phi.mean(axis=0)
    mean_feature = phi.mean(axis=0)
    eta_matrix = phi.T @ (phi - p_phi) / n + np.outer(
        mean_feature, mean_feature
    )
    eta = float(np.linalg.eigvalsh(eta_matrix).min())
    return {
        "phi": phi,
        "reward": reward,
        "target_theta": target_theta,
        "target_value": value,
        "eta": eta,
        "normalization": normalization,
    }


def _simulate(
    n: int,
    d: int,
    sampling: str,
    *,
    zero_reward_control: bool = False,
) -> tuple[list[dict[str, object]], float]:
    instance = _instance(n, d)
    phi = instance["phi"]
    reward = (
        np.zeros(n, dtype=float)
        if zero_reward_control
        else instance["reward"]
    )
    target_theta = instance["target_theta"]
    target_value = instance["target_value"]
    rng = np.random.default_rng(
        820_000 + n + d + (0 if sampling == "iid" else 10_000)
    )
    states = rng.integers(0, n, size=REPLICATES)
    second_states = rng.integers(0, n, size=REPLICATES)
    theta = np.zeros((REPLICATES, d), dtype=float)
    initial_parameter_mse = float(np.mean(np.sum((theta - target_theta) ** 2, axis=1)))
    initial_value_rmse = float(np.sqrt(np.mean(target_value**2)))
    rows: list[dict[str, object]] = []
    started = time.perf_counter()

    for step in range(1, max(CHECKPOINTS) + 1):
        if sampling == "iid":
            states = rng.integers(0, n, size=REPLICATES)
            second_states = rng.integers(0, n, size=REPLICATES)
        next_states = _transition(states, rng, n)
        next_second_states = _transition(second_states, rng, n)
        phi_state = phi[states]
        phi_next = phi[next_states]
        phi_second = phi[second_states]
        state_reward = reward[states]
        td = state_reward + np.sum((phi_next - phi_state) * theta, axis=1)
        correction_scalar = state_reward + np.sum(phi_state * theta, axis=1)
        alpha = 150.0 / (step + 1000.0)
        theta += alpha * (
            td[:, None] * phi_state
            - correction_scalar[:, None] * phi_second
        )
        if sampling == "markov":
            states = next_states
            second_states = next_second_states

        if step in CHECKPOINTS:
            parameter_errors = np.sum((theta - target_theta) ** 2, axis=1)
            value_errors = (theta - target_theta) @ phi.T
            value_mse_per_seed = np.mean(value_errors**2, axis=1)
            value_rmse_per_seed = np.sqrt(value_mse_per_seed)
            rows.append(
                {
                    "route": (
                        "zero_reward_negative_control"
                        if zero_reward_control
                        else "paper_scale_double_chain"
                    ),
                    "sampling": sampling,
                    "n": n,
                    "d": d,
                    "T": step,
                    "alpha": alpha,
                    "replicates": REPLICATES,
                    "eta1": instance["eta"],
                    "feature_normalization": instance["normalization"],
                    "initial_parameter_mse": initial_parameter_mse,
                    "parameter_mse": float(np.mean(parameter_errors)),
                    "parameter_mse_standard_error": float(
                        np.std(parameter_errors, ddof=1) / math.sqrt(REPLICATES)
                    ),
                    "initial_value_rmse": initial_value_rmse,
                    "value_rmse": float(np.mean(value_rmse_per_seed)),
                    "value_rmse_standard_error": float(
                        np.std(value_rmse_per_seed, ddof=1)
                        / math.sqrt(REPLICATES)
                    ),
                    "finite": bool(
                        np.all(np.isfinite(theta))
                        and np.all(np.isfinite(value_errors))
                    ),
                }
            )
    return rows, time.perf_counter() - started


def paper_scale_rows() -> tuple[
    list[dict[str, object]], list[dict[str, object]], dict[str, float]
]:
    rows: list[dict[str, object]] = []
    runtimes: dict[str, float] = {}
    for n, d in TASKS:
        for sampling in ("iid", "markov"):
            result, elapsed = _simulate(n, d, sampling)
            rows.extend(result)
            runtimes[f"{sampling}_n{n}_d{d}"] = elapsed
    controls, elapsed = _simulate(
        100, 20, "markov", zero_reward_control=True
    )
    runtimes["negative_control_n100_d20"] = elapsed
    return rows, controls, runtimes
