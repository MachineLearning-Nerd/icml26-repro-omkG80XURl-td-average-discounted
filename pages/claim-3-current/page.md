# Claim 3 — no explicit dimension term in the decaying-step bound

## Literal claim and outcome

The generated claim says Theorem 4.3's decaying-stepsize convergence guarantee
has no **explicit** dimension-dependent term. It does not say dimension cannot
enter implicitly through `η`, mixing, or parameter norms.

**Local evidence verdict for the literal claim: VERIFIED.** The exact free
symbols in both main-theorem branches and the full Appendix Theorem D.1 are:

| Formula | Audited free symbols |
| --- | --- |
| `ξ=1` | `T, τ_mix, c0, a, η, ||θ0||, ||θ*||, r_max` |
| `0<ξ<1` | the same symbols plus `ξ` |
| Appendix D.1 | the above plus `C, β` |

No formula contains a free `d`. An injected explicit-`d` dependency is
detected and rejected. The same schedule remains finite and convergent at
`d=5,20,100`, including `n=1000,d=100`; this scale sweep is a consistency
check, not the reason the syntactic claim is verified.

## Independent falsification attempt

The later counterexample audit remains **BLOCKED — no assumption-valid
falsification was established**. A peer endpoint `η1=0.443,d=40` violates the
paper's normalized-feature upper bound `η1≤3/d=0.075` by 5.91×. In the
independent admissible 64-seed family, `η1=1/d` exactly, so a dimension trend
cannot be separated from the theorem's allowed condition-number dependence.
This negative result does not prove the universal theorem; it prevents an
invalid counterexample from being mislabeled as a falsification.

## Direct evidence

- [Theorem 4.3 source audit](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_3/source_audit.md)
- [Raw formula dependency sets](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_3/raw_formula_dependencies.json)
- [Injected-d dependency set](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_3/negative_control_formula_dependencies.json)
- [Paper-scale raw CSV](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_3/raw_paper_scale.csv)
- [Independent checker source](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_3/independent_checker.py) and [output](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_3/independent_checker_output.txt)
- [Verifier source](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_3/verifier.py) and [injected-failure output](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/rigorous-2026-07-23/claim_3/negative_control_output.txt)
- [Focused falsification evaluation](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/claim3-falsification-2026-07-29/EVAL.md), [raw feasibility check](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/claim3-falsification-2026-07-29/raw_peer_trace_bound.csv), [controlled sweep](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/claim3-falsification-2026-07-29/raw_controlled_dimension_sweep.csv), and [verdict](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/claim3-falsification-2026-07-29/verdict.json)

Rerun all claims with `uv run --frozen python repro/src/verify_td.py` from the
[public repository](https://github.com/MachineLearning-Nerd/icml26-repro-omkG80XURl-td-average-discounted).
