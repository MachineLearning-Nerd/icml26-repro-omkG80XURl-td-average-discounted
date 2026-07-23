"""Exact first/second-moment propagation for a controlled scalar TD family.

The family has two states, stationary distribution (1/2, 1/2), feature
phi=(-scale, scale), and flip probability ``delta``.  Its paper-defined
condition number is exactly ``eta = 2 * delta * scale**2``.  Conditional
reward means are chosen so that the projected-Bellman solution is theta*=1;
bounded symmetric reward noise supplies non-degenerate stochastic error.
"""

from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np


@dataclass(frozen=True)
class ScalarFamily:
    delta: float
    scale: float = 1.0
    reward_noise: float = 0.25
    theta_star: float = 1.0

    @property
    def eta(self) -> float:
        return 2.0 * self.delta * self.scale**2

    @property
    def transition(self) -> np.ndarray:
        return np.array(
            [[1.0 - self.delta, self.delta], [self.delta, 1.0 - self.delta]],
            dtype=float,
        )

    @property
    def feature(self) -> np.ndarray:
        return np.array([-self.scale, self.scale], dtype=float)

    @property
    def mean_reward(self) -> np.ndarray:
        # R=(I-P) Phi theta*, hence the exact projected Bellman root is theta*.
        return (np.eye(2) - self.transition) @ self.feature * self.theta_star

    def mixing_time(self, tolerance: float) -> int:
        """Exact worst-start TV mixing time for the symmetric two-state chain."""
        tolerance = min(max(float(tolerance), 1e-15), 0.499999999999)
        rho = abs(1.0 - 2.0 * self.delta)
        if rho == 0.0:
            return 1
        return max(0, math.ceil(math.log(2.0 * tolerance) / math.log(rho)))


def theorem_stepsize(eta: float, horizon: int) -> float:
    """A legal tilde-Theta(1/(eta*T)) step with vanishing initialization bias."""
    proposed = 4.0 * math.log(horizon + 1.0) / (eta * horizon)
    return min(eta / 36.0, proposed)


def _event_affine(
    family: ScalarFamily,
    alpha: float,
    state: int,
    second_state: int,
    next_state: int,
    reward_sign: int,
) -> tuple[float, float]:
    """Return A,B for theta_{t+1}=A theta_t+B under Eq. (15)."""
    phi = family.feature
    reward = family.mean_reward[state] + reward_sign * family.reward_noise
    coefficient = (
        -phi[state] * phi[second_state]
        + (phi[next_state] - phi[state]) * phi[state]
    )
    offset = reward * (phi[state] - phi[second_state])
    return 1.0 + alpha * coefficient, alpha * offset


def iid_operator(family: ScalarFamily, alpha: float) -> np.ndarray:
    """Operator on [mass, E theta, E theta^2] for i.i.d. stationary states."""
    p = family.transition
    ea = eb = ea2 = eab = eb2 = 0.0
    for state in range(2):
        for second_state in range(2):
            for next_state in range(2):
                for reward_sign in (-1, 1):
                    probability = 0.5 * 0.5 * p[state, next_state] * 0.5
                    a, b = _event_affine(
                        family,
                        alpha,
                        state,
                        second_state,
                        next_state,
                        reward_sign,
                    )
                    ea += probability * a
                    eb += probability * b
                    ea2 += probability * a * a
                    eab += probability * a * b
                    eb2 += probability * b * b
    return np.array(
        [[1.0, 0.0, 0.0], [eb, ea, 0.0], [eb2, 2.0 * eab, ea2]],
        dtype=float,
    )


def markov_operator(family: ScalarFamily, alpha: float) -> np.ndarray:
    """Exact conditional-moment operator for two independent Markov chains."""
    p = family.transition
    # Four joint chain states, each storing [mass, first moment, second moment].
    operator = np.zeros((12, 12), dtype=float)
    for state in range(2):
        for second_state in range(2):
            old_joint = 2 * state + second_state
            old = 3 * old_joint
            for next_state in range(2):
                for next_second_state in range(2):
                    new_joint = 2 * next_state + next_second_state
                    new = 3 * new_joint
                    transition_probability = (
                        p[state, next_state] * p[second_state, next_second_state]
                    )
                    for reward_sign in (-1, 1):
                        probability = 0.5 * transition_probability
                        a, b = _event_affine(
                            family,
                            alpha,
                            state,
                            second_state,
                            next_state,
                            reward_sign,
                        )
                        operator[new, old] += probability
                        operator[new + 1, old] += probability * b
                        operator[new + 1, old + 1] += probability * a
                        operator[new + 2, old] += probability * b * b
                        operator[new + 2, old + 1] += probability * 2.0 * a * b
                        operator[new + 2, old + 2] += probability * a * a
    return operator


def exact_metrics(
    family: ScalarFamily,
    horizon: int,
    sampling: str,
) -> dict[str, float]:
    """Return exact mean, second moment, and MSE at the requested horizon."""
    alpha = theorem_stepsize(family.eta, horizon)
    if sampling == "iid":
        initial = np.array([1.0, 0.0, 0.0])
        final = np.linalg.matrix_power(iid_operator(family, alpha), horizon) @ initial
        mass, mean, second = final
    elif sampling == "markov":
        initial = np.zeros(12, dtype=float)
        for joint in range(4):
            initial[3 * joint] = 0.25
        final = (
            np.linalg.matrix_power(markov_operator(family, alpha), horizon) @ initial
        )
        mass = float(final[0::3].sum())
        mean = float(final[1::3].sum())
        second = float(final[2::3].sum())
    else:
        raise ValueError(f"unknown sampling mode: {sampling}")
    mse = second - 2.0 * family.theta_star * mean + family.theta_star**2 * mass
    return {
        "eta": family.eta,
        "delta": family.delta,
        "scale": family.scale,
        "T": int(horizon),
        "alpha": alpha,
        "mixing_time": family.mixing_time(alpha),
        "mass": float(mass),
        "mean": float(mean),
        "second_moment": float(second),
        "mse": float(max(mse, 0.0)),
    }


def rate_regression(
    rows: list[dict[str, float]],
    markov_adjustment: bool = False,
) -> dict[str, float]:
    """Fit log(MSE / log(T) [/ (3*tau+1)]) against log(T), log(eta)."""
    design = []
    response = []
    for row in rows:
        adjustment = math.log(row["T"] + 1.0)
        if markov_adjustment:
            adjustment *= 3.0 * row["mixing_time"] + 1.0
        design.append([1.0, math.log(row["T"]), math.log(row["eta"])])
        response.append(math.log(max(row["mse"] / adjustment, 1e-300)))
    coefficients, residuals, _, _ = np.linalg.lstsq(
        np.asarray(design), np.asarray(response), rcond=None
    )
    fitted = np.asarray(design) @ coefficients
    total = float(np.square(np.asarray(response) - np.mean(response)).sum())
    unexplained = float(np.square(np.asarray(response) - fitted).sum())
    return {
        "intercept": float(coefficients[0]),
        "T_exponent": float(coefficients[1]),
        "eta_exponent": float(coefficients[2]),
        "r_squared": float(1.0 - unexplained / total) if total > 0 else 1.0,
        "residual_sum_squares": float(residuals[0]) if len(residuals) else unexplained,
    }

