# Reproduction audit report

## Executive result

The repository contains a reproducible, CPU-only audit of six claims from
*Bridging the Gap Between Average and Discounted TD Learning*. All six local
contracts pass, with independent checkers and negative controls. The correct
summary is:

- evidence-release gate: PASSED;
- overall repository assessment: VERIFIED_SCOPED;
- strict universal paper-claim gate: NOT_READY;
- external publication: AWAITING_JUDGE;
- Claim 3 focused falsification: BLOCKED.

The scope qualifier matters. The exact rate experiments use controlled
families, paper-scale experiments substitute unavailable learned policies, and
the Claim 5 quartic conclusion is explicitly conditional.

## Claim outcomes

### C1 — i.i.d. double-chain rate

The exact moment operator gives a T exponent of -1.0032308678 with
R-squared 0.9952711. A quadratic eta-envelope calibrated on larger
stepsizes passes a smaller held-out set, while the eta-inverse-one control is
rejected. The paper-scale i.i.d. run includes n=1000,d=100.

Producer: repro/src/exact_moments.py and repro/src/rigorous_campaign.py.

### C2 — Markov double-chain rate

The conditional-state moment operator retains the explicit mixing factor. The
adjusted regression gives a T exponent of -1.2142893596 and an eta exponent
of -2.0050632056, with per-eta T slopes between -1.170 and -1.308. All
horizons exceed the measured mixing time, and the zero-reward control is worse.

Producer: repro/src/exact_moments.py and repro/src/rigorous_campaign.py.

### C3 — no free explicit dimension term

The theorem forms and full Appendix D.1 dependency sets contain no free d.
An injected explicit-d control is detected. The same decaying schedule remains
finite at the paper-scale dimensions, including n=1000,d=100.

This does not mean numerical error is independent of dimension: the paper
allows implicit dependence through eta, parameter norms, and mixing.

The separate falsification audit is BLOCKED. The reported peer value
eta1=0.443 at d=40 violates the normalized-feature consequence
eta1 <= 3/d = 0.075, and the peer page lacks the raw ingredients needed to
instantiate Theorem D.1. The controlled admissible family has eta1=1/d, so
its dimension trend cannot isolate a forbidden free d.

Producer: repro/src/rigorous_campaign.py for the literal contract and
repro/src/claim3_falsification.py for the focused audit.

### C4 — quadratic versus quartic condition dependence

The proposed method’s quadratic envelope is measured on held-out values. The
prior average-reward source is audited as quartic and the discounted-TD source
as quadratic. Their condition quantities are kept distinct, so this is a
comparison of published bound structure rather than a claim that one scalar
was measured across all papers.

Producer: repro/src/rigorous_campaign.py and the source-pinned Claim 4 audit.

### C5 — conditional single-chain quartic dependence

The independent dependency graph produces the general
eta-prime-inverse eta-cubed T-inverse dependence. Substituting
eta-prime = Theta(eta) gives the conditional eta-inverse-fourth T-inverse
form. The actual Eq. 17 route is compatible with the quartic envelope, but a
cubic envelope also passes; therefore the empirical route is non-identifying.

Producer: repro/src/single_chain.py, the Claim 5 verifier, and the independent
dependency graph.

### C6 — eta1 >= eta3/2

The proof steps involving the half-scaled Dirichlet seminorm pass, as do 48
systematic cases through n=1000,d=100. The stronger 1.1 eta3 negative
control fails on a tight tabular case.

Producer: repro/src/claim_verifier.py and repro/src/independent_checker.py.

## Reproduction command

```bash
uv sync --frozen
uv run --frozen python repro/src/verify_td.py
```

The recorded winning scientific run used commit
fcf047187bc0139da0c20ed254458f6b35efa99e and took
189.77527779201046 seconds internally.

## External judge status

The repository does not convert local checks into competition points. The
preserved release history contains both 5/12 and a later 6/12 visibility page
for different snapshots. Because there is no fresh external verdict available
here, the audit records the conservative prior score as 5/12 and claims no
increase.

## Remaining work for a strict gate

1. Reproduce the learned paper-scale policy matrices or obtain author-supplied
   policies.
2. Make the hidden constants and threshold conditions needed for a fully
   instantiated universal bound available.
3. Obtain a fresh external judge verdict for the published evidence revision.
