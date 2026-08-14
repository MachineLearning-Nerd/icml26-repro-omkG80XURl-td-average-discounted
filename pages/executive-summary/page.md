# Executive summary

This CPU-only reproduction audits six claims from
[Bridging the Gap Between Average and Discounted TD Learning](https://arxiv.org/abs/2605.02103)
by Haoxing Tian, Zaiwei Chen, Ioannis Ch. Paschalidis, and Alex Olshevsky.

All six local contracts pass with independent checkers and negative controls.
The correct scope label is **VERIFIED_SCOPED**: controlled moment families,
theorem-dependency audits, and documented paper-scale substitutes support the
contracts, but they do not constitute a universal proof of every theorem
instance. The focused Claim 3 falsification attempt is **BLOCKED**, not
falsified.

| Item | Result |
| --- | --- |
| C1–C2 | Exact i.i.d. and Markov moment-rate contracts pass. |
| C3 | No free explicit d is found; focused falsification is blocked. |
| C4 | Quadratic/provenance audit passes without collapsing condition definitions. |
| C5 | General dependency is verified; quartic behavior is conditional on eta-prime = Theta(eta). |
| C6 | Half-scaled Dirichlet proof path and 48-case stress test pass. |
| External judge | Awaiting a fresh verdict; no score increase is claimed. |

The authoritative evidence is in
[.openresearch/artifacts/winning_run](https://github.com/MachineLearning-Nerd/icml26-average-discounted-td-learning/tree/main/.openresearch/artifacts/winning_run).
Run the complete verifier with:

```bash
uv run --frozen python repro/src/verify_td.py
```

The detailed claim ledger is in the repository
[README](https://github.com/MachineLearning-Nerd/icml26-average-discounted-td-learning#claim-ledger)
and [AUDIT_REPORT.md](https://github.com/MachineLearning-Nerd/icml26-average-discounted-td-learning/blob/main/AUDIT_REPORT.md).
