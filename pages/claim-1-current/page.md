# Claim 1 — i.i.d. double-chain fixed point and quadratic rate

## Literal claim and outcome

Under the assumptions and legal constant stepsize of Theorem 4.1, i.i.d.
double-chain TD converges to its unique sample-independent projected-Bellman
fixed point with sample complexity `Õ(ε^-1 η^-2)`.

**Local evidence verdict: VERIFIED.** Exact moment propagation removes Monte
Carlo noise. The fitted `T` exponent is **−1.0032309** (`R²=0.99527`). A
quadratic envelope calibrated only on `η≥0.20` has maximum normalized value
`5.4991`; on strictly smaller held-out η it improves to `3.3960`, within the
preregistered `1.25×` gate. The deliberately weaker η^-1 envelope rises from
`19.4030` to `72.8576` and is rejected.

The independent checker also confirms mass conservation, convergence to the
unique deterministic root, and the legal stepsize. At Appendix-G scale
`n=1000,d=100`, six-seed parameter MSE falls from `66.3408` initially to
`18.7079` at `T=150000`; value RMSE falls from `0.74917` to `0.39313`.

This is an exact controlled-moment reproduction plus a deterministic
paper-scale external-validity check, not a claim that finite experiments
replace the paper's universal proof.

## Direct evidence

- [Theorem 4.1 source audit](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_1/source_audit.md)
- [Exact contract and pass/fail gates](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_1/claim_contract.json)
- [Exact-moment raw CSV](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_1/raw_exact_moments.csv)
- [Paper-scale raw CSV](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_1/raw_paper_scale.csv)
- [Paper-scale condition-relaxing control](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_1/raw_paper_scale_negative_control.csv)
- [Independent checker source](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_1/independent_checker.py) and [output](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_1/independent_checker_output.txt)
- [Verifier source](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_1/verifier.py) and [injected-failure output](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_1/negative_control_output.txt)
- [Method](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_1/method.md), [limitations](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_1/limitations.md), and [machine-readable summary](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_1/summary.json)

Rerun all claims with `uv run --frozen python repro/src/verify_td.py` from the
[public repository](https://github.com/MachineLearning-Nerd/icml26-average-discounted-td-learning).
