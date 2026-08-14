# Claim 2 — Markov double-chain rate with mixing retained

## Literal claim and outcome

Theorem 4.2 states that two independent Markov chains and a legal constant
stepsize preserve the double-chain `Õ(ε^-1 η^-2)` sample complexity, with the
explicit mixing-time factor and `T≥τ_mix` retained.

**Local evidence verdict: VERIFIED.** A 12×12 conditional moment operator
propagates both genuine chain states exactly from stationarity. After dividing
only the theorem's logarithm and `(3τ_mix+1)` factor, the fitted `T` exponent is
**−1.2142894**, the η exponent is **−2.0050632**, and `R²=0.99078`. Every
per-η `T` exponent lies in the preregistered band: −1.1694, −1.1770, −1.1720,
−1.2105, −1.2490, and −1.3078.

All horizons exceed the measured mixing time and all stepsizes satisfy the
paper restriction. At `n=1000,d=100`, Markov parameter MSE falls from `66.3408`
to `19.6000` by `T=150000`, and value RMSE falls from `0.74917` to `0.40280`.
The zero-reward condition-relaxing control is materially worse.

## Direct evidence

- [Theorem 4.2 source audit](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_2/source_audit.md)
- [Exact contract](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_2/claim_contract.json)
- [Conditional-moment raw CSV](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_2/raw_exact_moments.csv)
- [Paper-scale Markov CSV](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_2/raw_paper_scale.csv)
- [Zero-reward negative-control CSV](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_2/raw_paper_scale_negative_control.csv)
- [Independent checker source](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_2/independent_checker.py) and [output](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_2/independent_checker_output.txt)
- [Verifier source](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_2/verifier.py) and [injected-failure output](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_2/negative_control_output.txt)
- [Method](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_2/method.md), [limitations](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_2/limitations.md), and [summary](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_2/summary.json)

Rerun all claims with `uv run --frozen python repro/src/verify_td.py` from the
[public repository](https://github.com/MachineLearning-Nerd/icml26-average-discounted-td-learning).
