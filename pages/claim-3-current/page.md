# Claim 3 — no explicit dimension term in the decaying-step bound

## Literal claim

The generated claim says the Theorem 4.3 decaying-stepsize guarantee has no
free explicit dimension-dependent term. It does not say that numerical error
cannot depend on dimension through eta, mixing, or parameter norms.

## Local result

The audited free-symbol sets for the two main-theorem forms and Appendix D.1
contain no free d. An injected explicit-d dependency is detected, and the
same schedule remains finite at the paper-scale dimensions, including
n=1000,d=100.

## Focused falsification result: BLOCKED

The peer endpoint eta1=0.443 at d=40 violates the normalized-feature upper
bound eta1 <= 3/d = 0.075. The peer page does not provide the raw inputs
needed to instantiate Theorem D.1. The independent admissible family has
eta1=1/d exactly, so its dimension trend cannot isolate a forbidden free
dimension factor.

This is a blocked audit, not a falsification of the paper and not a universal
proof of the theorem.

Evidence:

- [Literal Claim 3 contract](https://github.com/MachineLearning-Nerd/icml26-average-discounted-td-learning/blob/main/.openresearch/artifacts/winning_run/claim_3/summary.json)
- [Focused audit verdict](https://github.com/MachineLearning-Nerd/icml26-average-discounted-td-learning/blob/main/evidence/claim3-falsification-2026-07-29/verdict.json)
- [Focused audit report](https://github.com/MachineLearning-Nerd/icml26-average-discounted-td-learning/blob/main/evidence/claim3-falsification-2026-07-29/report.md)
- [Root claim ledger](https://github.com/MachineLearning-Nerd/icml26-average-discounted-td-learning#claim-ledger)
