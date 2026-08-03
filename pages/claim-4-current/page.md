# Claim 4 — quadratic condition-number dependence

## Literal claim and outcome

Section 1/Table 1 says the proposed average-reward double-chain bound improves
the prior condition-number dependence from quartic to quadratic and matches
the exponent of discounted TD.

**Local evidence verdict: VERIFIED.** The audit reads the three pinned primary
statements and keeps their different condition numbers separate:

| Bound | Primary anchor | Squared-error dependence |
| --- | --- | --- |
| Proposed average reward | Theorems 4.1–4.2 | `ε^-1 η1^-2` |
| Prior average reward | Zhang et al. 2021, Corollary 1 | `ε^-1 η2^-4` |
| Discounted TD | Bhandari et al. 2018, Theorem 2(c) | `ε^-1 ((1−γ)ω)^-2` |

The prior paper states RMSE tolerance ε with ε^-2; rewriting it for the
generated claim's mean-square tolerance gives ε^-1 without changing the
quartic condition factor. The proposed exact-moment route independently
produces an η exponent of −1.6957 and passes the held-out quadratic upper
envelope (`5.4991` calibration, `3.3960` validation). The verifier rejects any
comparison that collapses `η1`, `η2`, `η3`, and discounted `((1−γ)ω)` into one
numerical scalar.

## Direct evidence

- [Section 1/Table 1 source audit](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_4/source_audit.md)
- [Pinned primary-source metadata, anchors, and SHA-256 hashes](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_4/raw_primary_source_rate_audit.json)
- [Measured proposed-route result](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_4/raw_route_result.json)
- [Exact contract](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_4/claim_contract.json)
- [Independent checker source](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_4/independent_checker.py) and [output](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_4/independent_checker_output.txt)
- [Verifier source](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_4/verifier.py) and [injected-failure output](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_4/negative_control_output.txt)
- [Method](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_4/method.md), [limitations](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_4/limitations.md), and [summary](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_4/summary.json)

Rerun all claims with `uv run --frozen python repro/src/verify_td.py` from the
[public repository](https://github.com/MachineLearning-Nerd/icml26-repro-omkG80XURl-td-average-discounted).
