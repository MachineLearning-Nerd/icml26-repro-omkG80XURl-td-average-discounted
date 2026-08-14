# Claim 6 — exact condition-number inequality

## Literal claim and outcome

With the paper's half-scaled Dirichlet seminorm and the definitions in Equation
3, Lemma B.3 states `η1 ≥ η3/2` for every admissible chain and full-column-rank
feature matrix.

**Local evidence verdict: VERIFIED.** The audit separately checks every step
that produces the factor one-half:

1. the Dirichlet seminorm equals `vᵀD(I−P)v`;
2. stationary `P` is a contraction in the `D` norm;
3. the orthogonal spectral quantity satisfies `λ≤2`;
4. the constant/orthogonal decomposition has nonnegative coefficients;
5. Rayleigh minimization preserves the half factor.

All five exact gates pass. The numerical route then evaluates 48 deterministic
systems, including dense positive nonreversible chains and paper-scale
`n=1000,d=100`. That largest case has `η1=0.00237115`, `η3=0.000643407`, and
positive margin `η1−η3/2=0.00204945`. The minimum margin over all 48 cases is
`4.11474e−7`. A tight tabular case has `η1=η3=0.5`, so the stronger false
control `η1≥1.1η3` has margin `−0.05` and fails as required.

The stress suite supports the independent proof-step audit; it is not presented
as a finite substitute for a universal inequality.

## Direct evidence

- [Equation 3/Lemma B.3 source audit](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_6/source_audit.md)
- [Exact proof-step record](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_6/raw_proof_steps.json)
- [All 48 raw stress cases](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_6/raw_condition_stress.csv)
- [Exact claim contract](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_6/claim_contract.json)
- [Independent checker source](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_6/independent_checker.py) and [output](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_6/independent_checker_output.txt)
- [Verifier source](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_6/verifier.py) and [injected-failure output](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_6/negative_control_output.txt)
- [Method](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_6/method.md), [limitations](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_6/limitations.md), and [summary](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_6/summary.json)

Rerun all claims with `uv run --frozen python repro/src/verify_td.py` from the
[public repository](https://github.com/MachineLearning-Nerd/icml26-average-discounted-td-learning).
