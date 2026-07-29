# Claim 3 falsification audit: BLOCKED

## Focused evidence status

**BLOCKED — no assumption-valid falsification was established.**

The current judged Claim 3 verdict remains `TOY`. This focused audit does not
replace that verdict with `VERIFIED`, does not claim points, and does not infer
that the theorem is true.

The proposed peer counterexample reports `eta1=0.443` at `d=40`. Under the
paper's normalized-feature assumption, every admissible instance satisfies
`eta1 <= 3/d = 0.075`; the reported endpoint is 5.91 times too large. The peer
page publishes no code, raw data, seeds, feature matrix, mixing constants,
parameter norms, or instantiated Theorem D.1 bound.

An independent 64-seed reconstruction with two Markov chains and
`d={5,10,20,40}` observed a hitting-time exponent of `0.183`, not the peer's
self-reported `2.015`. In that admissible family `eta1=1/d` exactly, so a
dimension trend cannot be separated from the theorem's condition-number
dependence.

## Focused falsification evidence

- [Evaluation](../../evidence/claim3-falsification-2026-07-29/EVAL.md)
- [Exact claim contract](../../evidence/claim3-falsification-2026-07-29/claim_contract.json)
- [Source audit](../../evidence/claim3-falsification-2026-07-29/source_audit.md)
- [Method and three routes](../../evidence/claim3-falsification-2026-07-29/method.md)
- [Peer hypothesis audit](../../evidence/claim3-falsification-2026-07-29/peer_hypothesis_audit.json)
- [Raw feasibility check](../../evidence/claim3-falsification-2026-07-29/raw_peer_trace_bound.csv)
- [Raw controlled sweep](../../evidence/claim3-falsification-2026-07-29/raw_controlled_dimension_sweep.csv)
- [Falsification verifier output](../../evidence/claim3-falsification-2026-07-29/falsification_verifier_output.txt)
- [Independent checker output](../../evidence/claim3-falsification-2026-07-29/independent_checker_output.txt)
- [Negative-control output](../../evidence/claim3-falsification-2026-07-29/negative_control_output.txt)
- [Illustrated report](../../evidence/claim3-falsification-2026-07-29/report.md)
- [Preservation table](../../evidence/claim3-falsification-2026-07-29/preservation_table.md)

## Earlier evidence preserved

The earlier source-formula audit and scale check remain byte-for-byte reachable
at their original paths:

- [Earlier evaluation](../../evidence/rigorous-2026-07-23/claim_3/EVAL.md)
- [Earlier contract](../../evidence/rigorous-2026-07-23/claim_3/claim_contract.json)
- [Earlier raw formula dependencies](../../evidence/rigorous-2026-07-23/claim_3/raw_formula_dependencies.json)

The real falsification verifier exits nonzero when no counterexample is
present. The injected explicit-`d` control exits zero, confirming that the
detector can recognize a contradiction.
