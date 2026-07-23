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
