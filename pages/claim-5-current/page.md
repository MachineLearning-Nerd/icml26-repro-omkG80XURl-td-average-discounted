# Claim 5 — single-chain conditional quartic rate

## Literal claim and outcome

Theorem 4.4's single-chain steady-state error is
`Õ(1/(η′ η^3 T))`; it becomes `Õ(1/(η^4 T))` only in the stated common regime
`η′=Θ(η)`, worse than the double-chain quadratic dependence.

**Local evidence verdict: VERIFIED.** The independent dependency graph carries
powers of `(η′,η,T)` through every source step:

| Quantity | Exponent vector |
| --- | --- |
| `R_θ` | `(−1/2, 0, 0)` |
| `λ²` | `(1/2, 1, 0)` |
| `G_const` | `(−1, −1, 0)` |
| `ζ` | `(0, 1, 0)` |
| `α` | `(0, −1, −1)` |
| `α G_const / ζ` | **`(−1, −3, −1)`** |

Substituting `η′=Θ(η)` gives **`(−4,−1)`** in `(η,T)`. Omitting the η′ factor
produces the deliberately wrong cubic vector `(−3,−1)`, which the checker
rejects. The actual projected Equation 17 experiment uses 128 deterministic
replicates and keeps `η′/η=4/3`; its quartic envelope passes on held-out η and
the algorithm control is worse. That finite family is explicitly
non-identifying because a cubic envelope also holds—verification comes from
the exact source dependency graph, not an overfit empirical exponent.

## Direct evidence

- [Theorem 4.4 source audit](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_5/source_audit.md)
- [Exact theorem dependency graph](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_5/raw_theorem44_dependency_graph.json)
- [η′-omission negative graph](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_5/negative_control_theorem44_dependency_graph.json)
- [Exponent arithmetic](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_5/raw_exponent_arithmetic.json) and [projected-root derivation](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_5/raw_projected_root_derivation.json)
- [Raw Equation 17 sweep](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_5/raw_single_chain.csv) and [algorithm control](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_5/raw_single_chain_algorithm_negative_control.csv)
- [Independent checker source](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_5/independent_checker.py) and [output](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_5/independent_checker_output.txt)
- [Verifier source](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_5/verifier.py) and [injected-failure output](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_5/negative_control_output.txt)
- [Method](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_5/method.md), [limitations](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_5/limitations.md), and [summary](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_5/summary.json)

Rerun all claims with `uv run --frozen python repro/src/verify_td.py` from the
[public repository](https://github.com/MachineLearning-Nerd/icml26-repro-omkG80XURl-td-average-discounted).
