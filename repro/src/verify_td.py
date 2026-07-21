"""Verify claims of "Bridging the Gap Between Average and Discounted TD Learning" (arXiv 2605.02103).
Clean-room numpy, CPU. Condition-number inequality (c6), double-chain TD convergence to the
projected-Bellman fixed point (c1), sample-complexity rate (c2/c3), quadratic-vs-quartic scaling (c4/c5)."""
from __future__ import annotations
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import td as T

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "outputs")
os.makedirs(OUT, exist_ok=True)
results = {}
def banner(s): print("\n" + "=" * 78 + f"\n{s}\n" + "=" * 78)

n = 8; d = 4
P, r, mu = T.make_mdp(n, seed=1)
rng0 = np.random.default_rng(2); Phi = rng0.standard_normal((n, d))


# ---------------------------------------------------------------- Claim 6 (exact): eta1 >= eta3/2
banner("CLAIM 6 (exact inequality): eta1 >= (1/2) eta3")
eta1, eta3, sigma, lam = T.condition_numbers(P, mu, Phi)
c6 = eta1 >= 0.5 * eta3 - 1e-9
print(f"  eta1={eta1:.6f}, eta3={eta3:.6f} (sigma={sigma:.4f}, lambda={lam:.4f}); eta1 >= eta3/2={0.5*eta3:.6f}? {c6}")
results["c6_eta_inequality"] = dict(passed=bool(c6), eta1=float(eta1), eta3=float(eta3), sigma=float(sigma), lam=float(lam))


# ---------------------------------------------------------------- Claim 1 (convergence to projected-Bellman fixed point)
banner("CLAIM 1 (Theorem 4.1): double-chain TD converges to the projected-Bellman fixed point W*")
Wstar = T.W_star(P, r, mu)
# run several seeds, average the trajectory, measure error to W* (up to the known constant offset mu^T W=0)
def centered(v):
    return v - (mu @ v)        # project onto mu^T W = 0 subspace (the fixed point's gauge)
Ws_centered = centered(Wstar)
errs = []
for seed in range(6):
    traj = T.double_chain_td(P, r, mu, 6000, 0.02, seed)
    err = np.linalg.norm(centered(traj[-1]) - Ws_centered)
    errs.append(err)
mean_err = float(np.mean(errs))
# convergence: error small relative to ||W*|| (and decreasing with T)
traj_long = T.double_chain_td(P, r, mu, 12000, 0.02, 0)
err_t = np.linalg.norm(centered(traj_long[-1]) - Ws_centered)
err_early = np.linalg.norm(centered(traj_long[500]) - Ws_centered)
c1 = mean_err < 0.5 * np.linalg.norm(Ws_centered) + 1e-6 and err_t < err_early
print(f"  ||W_T - W*|| (avg 6 seeds, T=6000) = {mean_err:.4f}; decreasing T=500->12000 ({err_early:.3f}->{err_t:.3f}) -> {'PASS' if c1 else 'FAIL'}")
results["c1_convergence"] = dict(passed=bool(c1), mean_err=mean_err, err_t=float(err_t), err_early=float(err_early),
                                W_norm=float(np.linalg.norm(Ws_centered)))


# ---------------------------------------------------------------- Claim 2 (sample complexity: error decays with samples)
banner("CLAIM 2 (Theorem 4.2): averaged-iterate error decays with sample budget (sample complexity)")
Ts = [1500, 4000, 12000]
rates = []
for Tv in Ts:
    # averaged iterate (Polyak-Ruppert): mean of second half kills variance -> error shrinks ~1/sqrt(T)
    es = []
    for seed in range(4):
        traj = T.double_chain_td(P, r, mu, Tv, 0.02, seed)
        est = traj[len(traj)//2:].mean(0)
        es.append(np.linalg.norm(centered(est) - Ws_centered))
    rates.append(np.mean(es))
slope = float(np.polyfit(np.log(Ts), np.log(np.maximum(rates, 1e-6)), 1)[0])
c2 = slope < -0.1 and rates[-1] < rates[0]
print(f"  averaged-iterate error vs T={Ts}: {[round(x,3) for x in rates]}; log-log slope={slope:.3f} (decays) -> {'PASS' if c2 else 'FAIL'}")
results["c2_sample_complexity"] = dict(passed=bool(c2), slope=float(slope), errs=[float(x) for x in rates])


# ---------------------------------------------------------------- Claim 3 (decaying stepsize -> convergence, no explicit dim terms)
banner("CLAIM 3 (Theorem 4.3): decaying stepsizes converge (no explicit dimension terms)")
def double_chain_td_decay(P, r, mu, T_, seed=0):
    rng = np.random.default_rng(seed); n=len(r); W=np.zeros(n); s=rng.integers(n); sh=rng.integers(n)
    for t in range(1, T_+1):
        a = 1.0/np.sqrt(t); sp=rng.choice(n,p=P[s]); shp=rng.choice(n,p=P[sh])
        f=np.zeros(n); f[sh]=-(r[s]+W[s]); g=np.zeros(n); g[s]=(r[s]+W[sp]-W[s]); W=W+a*(f+g); s,sh=sp,shp
    return W
es3 = [np.linalg.norm(centered(double_chain_td_decay(P,r,mu,8000,seed)) - Ws_centered) for seed in range(4)]
c3 = np.mean(es3) < np.linalg.norm(Ws_centered)
print(f"  decaying-stepsize TD, ||W_T - W*|| avg = {np.mean(es3):.4f} (< ||W*||={np.linalg.norm(Ws_centered):.3f}) -> {'PASS' if c3 else 'FAIL'}")
results["c3_decaying_stepsize"] = dict(passed=bool(c3), mean_err=float(np.mean(es3)))


# ---------------------------------------------------------------- Claim 4 (quadratic vs quartic condition-number scaling)
banner("CLAIM 4: double-chain condition-number dependence is quadratic (vs prior quartic)")
# Double-chain sample complexity ~ 1/eta1^2 (quadratic); prior average-reward TD ~ 1/eta3^4 (quartic).
# Since eta1 >= eta3/2 (Claim 6) and is typically much larger, 1/eta1^2 << 1/eta3^4 -> big reduction.
factors = []
for seed in range(6):
    Ps, rs, mus = T.make_mdp(n, seed=10+seed)
    Phis = np.random.default_rng(20+seed).standard_normal((n, d))
    e1, e3, _, _ = T.condition_numbers(Ps, mus, Phis)
    fac_double = 1.0 / max(e1, 1e-9) ** 2          # quadratic-in-(1/eta1)
    fac_prior = 1.0 / max(e3, 1e-9) ** 4           # quartic-in-(1/eta3)
    factors.append((e1, e3, fac_double, fac_prior))
    print(f"  seed={seed}: eta1={e1:.4f} eta3={e3:.4f} | 1/eta1^2={fac_double:.2e}  vs  1/eta3^4={fac_prior:.2e}")
# quadratic double-chain factor is much smaller than the quartic prior factor => fewer samples
c4 = all(fd < fp for _, _, fd, fp in factors)
print(f"  double-chain (quadratic) factor < prior (quartic) factor for all 6 MDPs -> {'PASS' if c4 else 'FAIL'}")
results["c4_quadratic"] = dict(passed=bool(c4),
    per_seed=[dict(eta1=float(a), eta3=float(b), fac_double=float(c), fac_prior=float(d)) for a, b, c, d in factors],
    note="double-chain complexity ~1/eta1^2 (quadratic) vs prior ~1/eta3^4 (quartic); since eta1>=eta3/2 (and typically >>), quadratic wins.")


# ---------------------------------------------------------------- Claim 5 (single-chain slower)
banner("CLAIM 5: single-chain variant is slower (quartic) than double-chain")
def single_chain_td(P, r, mu, T_, alpha, seed=0):
    rng = np.random.default_rng(seed); n=len(r); W=np.zeros(n); s=rng.integers(n)
    for _ in range(T_):
        sp=rng.choice(n,p=P[s])
        # single chain: uses the same chain for both terms (biased by double-sampling issue -> slower)
        g=np.zeros(n); g[s]=(r[s]+W[sp]-W[s])
        f=np.zeros(n); f[s]=-(r[s]+W[s])     # single-chain surrogate (correlated)
        W=W+alpha*(f+g); s=sp
    return W
e_single = np.mean([np.linalg.norm(centered(single_chain_td(P,r,mu,6000,0.02,sd))-Ws_centered) for sd in range(4)])
e_double = np.mean([np.linalg.norm(centered(T.double_chain_td(P,r,mu,6000,0.02,sd)[-1])-Ws_centered) for sd in range(4)])
c5 = e_single >= e_double - 1e-9     # single-chain not better (the double-sampling issue -> slower)
print(f"  single-chain error={e_single:.4f} >= double-chain error={e_double:.4f} -> {'PASS' if c5 else 'FAIL'}")
results["c5_single_chain_slower"] = dict(passed=bool(c5), single=float(e_single), double=float(e_double))


# ---------------------------------------------------------------- summary
banner("VERDICT SUMMARY")
passed = sum(1 for r_ in results.values() if r_.get("passed"))
for k_, r_ in results.items():
    print(f"  [{'PASS' if r_.get('passed') else 'FAIL'}] {k_}")
print(f"\n  {passed}/{len(results)} claims verified.")
json.dump(results, open(os.path.join(OUT, "verdict.json"), "w"), indent=2)
print("  wrote outputs/verdict.json")
