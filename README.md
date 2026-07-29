# Focused Claim 3 falsification campaign

[![Open Claim 3 audit in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/MachineLearning-Nerd/icml26-repro-omkG80XURl-td-average-discounted/blob/master/notebooks/claim3_falsification.py)

We independently tested whether Claim 3 of **Bridging the Gap Between Average
and Discounted TD Learning** can be falsified by the reported \(d^2\)
hitting-time effect. The peer number was a \(d\)-exponent of **2.015**
(\(R^2=0.994\)); our assumption-valid reconstruction observed **0.183**
across \(d=\{5,10,20,40\}\), using 64 fixed seeds.

**Falsification status: BLOCKED.** The peer page publishes no executable
artifacts, and its \(\eta_1=0.443\) at \(d=40\) violates the
normalized-feature consequence \(\eta_1\le3/d=0.075\) by 5.91×. In our
admissible family, \(\eta_1=1/d\) exactly, so dimension and allowed
condition-number dependence cannot be identified separately. The current
judged Claim 3 verdict remains `TOY`; no score change is claimed.

The reconstruction substitutes a controlled uniform Markov chain because the
peer transition, reward, features, and seeds were unavailable. The formal run
used Hugging Face `cpu-upgrade` for 3m32s, CPython 3.12.11 and NumPy 2.2.6,
with no GPU.

- [Illustrated Claim 3 falsification report](reports/claim3-falsification/report.md)
- [Self-contained Claim 3 marimo notebook](notebooks/claim3_falsification.py)
- [Machine-readable Claim 3 evidence](.openresearch/artifacts/claim3_falsification_2026_07_29)
- [Earlier six-claim reproduction report](reports/rigorous-reproduction/report.md)

## Focused experiment log

| Branch / experiment | Purpose or change | Exact run command | Assessment / outcome | Compute |
|---|---|---|---|---|
| `master` | Publication surface | Not run as an experiment (publication surface) | README, report, notebook, and release manifests | — |
| [Claim 3 falsification audit](https://github.com/MachineLearning-Nerd/icml26-repro-omkG80XURl-td-average-discounted/tree/orx%2Fclaim-3-falsification-audit-with-controlled-dime) | Exact source audit, normalization proof, 64-seed controlled dimension sweep, negative control | `uv run --frozen python repro/src/verify_td.py` | `BLOCKED`; current `TOY` verdict preserved; all cumulative regressions pass | Hugging Face `cpu-upgrade`, 3m32s, no GPU |
| [Claim 3 release child](https://github.com/MachineLearning-Nerd/icml26-repro-omkG80XURl-td-average-discounted/tree/orx%2Fclaim-3-falsification-blocked-release) | Additive Space candidate, preservation suite, report, and notebook | `uv run --frozen python repro/src/verify_td.py` | All cumulative checks pass; focused falsification remains `BLOCKED` | Hugging Face `cpu-upgrade`, 3m37s, no GPU |

---

# Rigorous reproduction: six TD-learning claims

[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/MachineLearning-Nerd/icml26-repro-omkG80XURl-td-average-discounted/blob/master/notebooks/td_rate_reproduction.py)

This project reproduces the six theoretical claims in
**Bridging the Gap Between Average and Discounted TD Learning**
([arXiv 2605.02103](https://arxiv.org/abs/2605.02103)). The central test is the
double-chain sample-complexity rate: the paper predicts
\(\widetilde O(\epsilon^{-1}\eta^{-2})\); exact moments give a \(T\) exponent
of **−1.003** under i.i.d. sampling and, after retaining the explicit mixing
factor, **−1.214 in \(T\)** and **−2.005 in \(\eta\)** under Markov sampling.

All six local claim contracts currently report `VERIFIED`, with independent
checkers and failing negative controls. That is a reproduction assessment, not
a judge score: the live score remains **5/12** until the external judge
evaluates a new Hugging Face revision.

The additive evidence release is published on the existing
[Hugging Face Space](https://huggingface.co/spaces/DineshAI/omkG80XURl/tree/cb04bc356fb2ea3641f65cc9bbd06a299b5980b2)
at revision `cb04bc356fb2ea3641f65cc9bbd06a299b5980b2` and is awaiting a new
judge verdict.

The exact-rate route uses a controlled two-state family so moments can be
propagated without Monte Carlo noise. External validity is checked separately
at the paper’s \((n,d)=(50,5),(100,20),(1000,100)\) dimensions and 150,000-step
schedule. The learned Random-Walk policy matrices were not published, so these
scale runs substitute a documented ergodic cycle with 0.10 teleportation. All
formal runs used local CPU; no GPU or Hugging Face compute was used.

- [Illustrated technical report](reports/rigorous-reproduction/report.md)
- [Publication approval report](reports/rigorous-reproduction/release_report.md)
- [Formal command ledger](reports/rigorous-reproduction/command_ledger.md)
- [Self-contained tutorial notebook](notebooks/td_rate_reproduction.py)
- [Frozen machine-readable winning evidence](.openresearch/artifacts/winning_run)

## Experiment log

Every formal node inherits the exact command shown below; variants live in
committed code rather than command-line knobs.

| Branch / experiment | Purpose or change | Exact run command | Assessment / outcome | Compute |
|---|---|---|---|---|
| `master` | Publication surface | Not run as an experiment (publication surface) | Published README, report, notebook, and exact release manifest; awaiting judge | — |
| [locked judged baseline](https://github.com/MachineLearning-Nerd/icml26-repro-omkG80XURl-td-average-discounted/tree/orx%2Fbaseline-judged-toy-verifier-in-locked-uv-enviro) | Reproduce the judged toy checks in the locked uv environment | `uv run --frozen python repro/src/verify_td.py` | Reproduced the existing weak checks; retained only as regression evidence | local CPU, 15 s |
| [held-out exact moments](https://github.com/MachineLearning-Nerd/icml26-repro-omkG80XURl-td-average-discounted/tree/orx%2Ffreeze-exact-evidence-and-stress-asymptotic-iid) | Exact i.i.d./Markov moments and held-out \(\eta\) envelope | `uv run --frozen python repro/src/verify_td.py` | Claims 1, 2, 3, and 6 verified on their contracts; 4–5 still blocked | local CPU, 30 s |
| [failed Eq. 17 oracle](https://github.com/MachineLearning-Nerd/icml26-repro-omkG80XURl-td-average-discounted/tree/orx%2Factual-single-chain-and-matched-prior-rate-contr) | First actual single-chain implementation | `uv run --frozen python repro/src/verify_td.py` | Correctly blocked: verifier used 1 instead of the projected root \(1/3\); preserved to explain the repair | local CPU, 1 m 45 s |
| [winning scientific node](https://github.com/MachineLearning-Nerd/icml26-repro-omkG80XURl-td-average-discounted/tree/orx%2Fsymbolic-theorem-4-4-chain-and-paper-scale-check) | Correct Eq. 17 root, theorem dependency graph, primary-source audit, and paper-scale checks | `uv run --frozen python repro/src/verify_td.py` | All six cumulative contracts verified; independent checkers returned zero | local CPU, 3 m 15 s |

---

# Repro — Bridging Average and Discounted TD Learning
OpenReview `omkG80XURl`. arXiv `2605.02103`. 6 claims/12 pts. Owner: loop12pt.
