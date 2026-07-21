"""Clean-room of average-reward TD (double-chain) from "Bridging the Gap Between Average and
Discounted TD Learning" (arXiv 2605.02103). numpy, CPU.

Projected Bellman (eq 9/10): W* = Pi T_pi W*,  Pi = I - e mu^T (projection onto {mu^T W = 0}),
 equivalently  D(R + P W* - W*) - mu mu^T (R + W*) = 0.
Double-chain TD (eq 12): W_{t+1} = W_t + alpha_t (f(s_t, s_hat_t, W_t) + g(s_t, s'_t, W_t)),
  f[i] = -1(i = s_hat_t)(r_{s_t} + W_t(s_t)),   g[i] = 1(i = s_t)(r_{s_t} + W_t(s'_t) - W_t(s_t)).
Condition numbers:  eta1 = min_{||x||=1}(||Phi x||^2_Dir + (mu^T Phi x)^2)  (eq 3);
  eta3 = sigma * lambda, sigma = min_{||x||=1} x^T Phi^T D Phi x, lambda = min_{y != e, ||y||_D=1} y^T D(I-P)y (eq 2).
"""
from __future__ import annotations
import numpy as np


def make_mdp(n, seed=0):
    rng = np.random.default_rng(seed)
    # Reversible chain: mixing + cycle random walk (both symmetric & doubly-stochastic) => uniform mu,
    # so D=(1/n)I and D(I-P) is symmetric PSD -> condition numbers eta1,eta3 are positive (well-defined).
    cycle = np.zeros((n, n))
    for i in range(n):
        cycle[i, (i - 1) % n] += 0.45; cycle[i, (i + 1) % n] += 0.45; cycle[i, i] += 0.1
    mixing = np.full((n, n), 1.0 / n)
    P = 0.4 * mixing + 0.6 * cycle            # symmetric doubly-stochastic, uniform stationary
    r = rng.uniform(-1, 1, n)
    mu = np.full(n, 1.0 / n)
    return P, r, mu


def W_star(P, r, mu):
    """Projected Bellman fixed point: solve  D(R + P W - W) - mu mu^T (R + W) = 0  (eq 10)."""
    n = len(r); D = np.diag(mu); e = np.ones(n)
    # (DP - D - mu mu^T) W = mu mu^T R - D R
    A = D @ P - D - np.outer(mu, mu)
    b = np.outer(mu, mu) @ r - D @ r
    W, *_ = np.linalg.lstsq(A, b, rcond=None)
    return W


def dirichlet(v, P, mu):
    """||v||^2_Dir = sum_{s,s'} mu(s) P(s'|s) (v(s)-v(s'))^2."""
    return float(np.sum(mu[:, None] * P * (v[:, None] - v[None, :]) ** 2))


def double_chain_td(P, r, mu, T, alpha=0.05, seed=0):
    """Tabular double-chain TD (eq 12) with two independent chains. Returns trajectory of W."""
    rng = np.random.default_rng(seed)
    n = len(r); W = np.zeros(n)
    traj = [W.copy()]
    s = rng.integers(n); shat = rng.integers(n)
    for _ in range(T):
        sp = rng.choice(n, p=P[s]); shatp = rng.choice(n, p=P[shat])
        f = np.zeros(n); f[shat] = -(r[s] + W[s])
        g = np.zeros(n); g[s] = (r[s] + W[sp] - W[s])
        W = W + alpha * (f + g)
        traj.append(W.copy())
        s, shat = sp, shatp
    return np.array(traj)


def condition_numbers(P, mu, Phi):
    """eta1 (eq 3) and eta3 = sigma*lambda (eq 2)."""
    n = len(mu); d = Phi.shape[1]; D = np.diag(mu)
    # eta1 = min_{||x||=1} ||Phi x||^2_Dir + (mu^T Phi x)^2
    # sample unit vectors (monte carlo over the sphere) and also use eigen-analysis via a matrix
    # ||Phi x||^2_Dir = x^T (Phi^T L Phi) x where L is the Dirichlet Laplacian; (mu^T Phi x)^2 = x^T Phi^T mu mu^T Phi x
    L = np.zeros((n, n))
    for s in range(n):
        for sp in range(n):
            L[s, s] += mu[s] * P[s, sp]
            L[s, sp] -= mu[s] * P[s, sp] * 0  # placeholder
    # build Dirichlet matrix Mdir where x^T Mdir x = ||Phi x||^2_Dir
    Mdir = np.zeros((d, d))
    for s in range(n):
        for sp in range(n):
            Mdir += mu[s] * P[s, sp] * np.outer(Phi[s] - Phi[sp], Phi[s] - Phi[sp])
    M1 = Mdir + np.outer(Phi.T @ mu, Phi.T @ mu)
    eta1 = float(np.linalg.eigvalsh(M1).min())          # min eigenvalue = min over ||x||=1
    # eta3 = sigma * lambda
    sigma = float(np.linalg.eigvalsh(Phi.T @ D @ Phi).min())
    # lambda = min_{y != e, ||y||_D=1} y^T D(I-P) y
    # parameterize y = e + z with constraint; approximate via random feasible y and eigen-analysis
    A = D @ (np.eye(n) - P)
    # min of y^T A y over ||y-e||_D small / over the constraint; use min eigenvalue of (D^-1/2 A D^-1/2) restricted
    Dinv_sqrt = np.diag(1 / np.sqrt(mu))
    B = Dinv_sqrt @ A @ np.diag(np.sqrt(mu))            # symmetric; y^T A y = z^T B z, ||y||_D=1 <=> ||z||=1
    ev = np.sort(np.linalg.eigvalsh(B))
    # lambda = min over y != e (||y||_D=1)  <=>  second-smallest eigenvalue (exclude the 0 eigenvalue at e)
    lam = float(ev[1] if ev[0] < 1e-9 else ev[0])
    eta3 = sigma * lam
    return eta1, eta3, sigma, lam
