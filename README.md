# ICML 2026 reproduction: Average and discounted TD learning

This repository audits the paper **“Bridging the Gap Between Average and
Discounted TD Learning”** for the ICML 2026 reproduction competition.

The audit is currently **VERIFIED_SCOPED**: all six local claim contracts pass
with independent checkers and negative controls, but the evidence uses
controlled families, theorem-dependency audits, and documented paper-scale
substitutes. It is not a universal proof of every theorem instance. The
focused Claim 3 falsification attempt is **BLOCKED**, not a falsification.

## Paper

- **Title:** Bridging the Gap Between Average and Discounted TD Learning
- **Authors:** Haoxing Tian, Zaiwei Chen, Ioannis Ch. Paschalidis, and Alex Olshevsky
- **arXiv:** [2605.02103](https://arxiv.org/abs/2605.02103)
- **OpenReview identifier:** omkG80XURl
- **Competition:** ICML 2026 reproduction
- **Repository owner:** [MachineLearning-Nerd](https://github.com/MachineLearning-Nerd)

The paper studies average-reward temporal-difference learning, where the
Bellman operator is not an ordinary contraction. Its main construction uses
two independent Markov trajectories to estimate the mean-feature correction.
The paper claims quadratic condition-number dependence for the double-chain
method, compared with the quartic dependence associated with a prior
single-chain route.

## Status at a glance

| Area | Status | Meaning |
| --- | --- | --- |
| Local evidence release gate | PASSED | The six claim artifacts, independent checks, controls, and reports are present. |
| Claims 1–6 | VERIFIED_SCOPED | Each declared finite/moment/theorem-dependency contract passes. |
| Claim 3 focused falsification | BLOCKED | The peer endpoint is outside the normalized-feature domain and no fully instantiated bound violation was established. |
| Strict universal paper-claim gate | NOT_READY | Learned policy matrices and some theorem constants are unavailable; conditional claims remain conditional. |
| External publication | AWAITING_JUDGE | A new judge verdict is not available. No score increase is claimed. |

The historical judged record is inconsistent across preserved logbook pages:
the rigorous release records 5/12, while a later visibility page reports 6/12
for a preserved revision. This repository therefore reports the conservative
prior record as 5/12 and makes no new score claim until the external judge
evaluates a published revision.

## Claim ledger

Each row states what was tested, how the result was produced, and where the
machine-readable evidence lives. VERIFIED_SCOPED means that the stated
contract passed; it does not remove the assumptions listed in the paper or in
the evidence files.

| Claim | Paper statement | How the result is produced | Evidence | Status |
| --- | --- | --- | --- | --- |
| C1 | i.i.d. double-chain last-iterate sample complexity is \(\widetilde O(\epsilon^{-1}\eta^{-2})\). | repro/src/exact_moments.py propagates first and second moments through a controlled two-state family; repro/src/rigorous_campaign.py fits the T rate, holds out smaller eta, and runs the paper-scale check. | [.openresearch/artifacts/winning_run/claim_1/summary.json](.openresearch/artifacts/winning_run/claim_1/summary.json), [claim_1/EVAL.md](.openresearch/artifacts/winning_run/claim_1/EVAL.md) | VERIFIED_SCOPED |
| C2 | Two independent stationary Markov chains retain the rate with the explicit mixing factor. | A conditional-state moment operator evaluates the two-chain Markov process; the checker retains tau_mix, fits per-eta slopes, and checks a paper-scale control. | [.openresearch/artifacts/winning_run/claim_2/summary.json](.openresearch/artifacts/winning_run/claim_2/summary.json), [claim_2/EVAL.md](.openresearch/artifacts/winning_run/claim_2/EVAL.md) | VERIFIED_SCOPED |
| C3 | The decaying-step convergence bound has no free explicit d term. | Theorem 4.3 and Appendix D.1 symbol sets are audited; an injected-d negative control must be detected; a fixed schedule is checked at paper-scale dimensions. A separate falsification campaign checks normalization feasibility and a controlled family. | [.openresearch/artifacts/winning_run/claim_3/summary.json](.openresearch/artifacts/winning_run/claim_3/summary.json), [claim3-falsification-2026-07-29/verdict.json](evidence/claim3-falsification-2026-07-29/verdict.json) | VERIFIED_SCOPED; falsification BLOCKED |
| C4 | The proposed average-reward bound is quadratic in its condition quantity, versus a prior quartic average-reward bound and quadratic discounted-TD bound. | The proposed held-out envelope is measured; independently pinned primary-source audits recover the published powers without collapsing distinct condition-number definitions. | [.openresearch/artifacts/winning_run/claim_4/summary.json](.openresearch/artifacts/winning_run/claim_4/summary.json), [claim_4/source_audit.md](.openresearch/artifacts/winning_run/claim_4/source_audit.md) | VERIFIED_SCOPED |
| C5 | The single-chain bound is \(\widetilde O((\eta'\eta^3T)^{-1})\), becoming quartic only when \(\eta'=\Theta(\eta)\). | repro/src/single_chain.py checks the projected Eq. 17 route; an independent dependency graph derives eta-prime inverse eta-cubed T-inverse and performs the conditional substitution. The empirical sweep is explicitly marked non-identifying. | [.openresearch/artifacts/winning_run/claim_5/summary.json](.openresearch/artifacts/winning_run/claim_5/summary.json), [raw_theorem44_dependency_graph.json](.openresearch/artifacts/winning_run/claim_5/raw_theorem44_dependency_graph.json) | VERIFIED_CONDITIONAL |
| C6 | \(\eta_1\geq\eta_3/2\) under the paper’s half-scaled Dirichlet seminorm. | Proof steps are audited algebraically and stress-tested over 48 deterministic chain/feature cases; the stronger 1.1 eta3 statement is used as a negative control. | [.openresearch/artifacts/winning_run/claim_6/summary.json](.openresearch/artifacts/winning_run/claim_6/summary.json), [raw_proof_steps.json](.openresearch/artifacts/winning_run/claim_6/raw_proof_steps.json) | VERIFIED_SCOPED |

The authoritative cumulative run is
[campaign_summary.json](.openresearch/artifacts/winning_run/campaign_summary.json).
The historical [outputs/verdict.json](outputs/verdict.json) is retained as a
toy baseline snapshot and must not be read as the current scientific verdict.

## Claim 3: why the falsification is blocked

The literal Claim 3 contract is syntactic: the audited theorem forms contain
no free dimension symbol d. The focused audit does not claim that this proves
dimension-uniform numerical error.

The peer endpoint reports eta1 = 0.443 at d = 40, but normalized features
imply eta1 <= 3/d = 0.075. The peer page does not provide the feature matrix,
transitions, rewards, seeds, mixing constants, or a fully instantiated Theorem
D.1 right-hand side. The independent admissible family has eta1 = 1/d
exactly, so its dimension trend cannot identify a free dimension effect
separately from the allowed condition-number dependence. The verifier
therefore returns BLOCKED; it does not label the paper falsified.

See the complete [Claim 3 report](evidence/claim3-falsification-2026-07-29/report.md),
[claim contract](evidence/claim3-falsification-2026-07-29/claim_contract.json),
[raw feasibility audit](evidence/claim3-falsification-2026-07-29/raw_peer_trace_bound.csv),
and [verdict](evidence/claim3-falsification-2026-07-29/verdict.json).

## Branch map

The public branch names describe the purpose of each experiment. The
Historical source column records the original competition/orx name for
provenance; the old refs are removed during the repository cleanup.

| Final branch | Historical source | Purpose |
| --- | --- | --- |
| main | master | Publication surface, reports, claim ledger, and release metadata. |
| baseline/judged-toy | orx/baseline-judged-toy-verifier-in-locked-uv-enviro | Reproduce the original weak toy checks in the locked environment. |
| research/exact-moments | orx/exact-moment-contracts-on-controlled-chain-famil | Establish exact i.i.d. and Markov moment operators. |
| research/held-out-rates | orx/freeze-exact-evidence-and-stress-asymptotic-iid | Freeze raw evidence and test held-out asymptotic rate envelopes. |
| audit/single-chain-eq17 | orx/actual-single-chain-and-matched-prior-rate-contr | First single-chain Eq. 17 route; preserved because its target root was wrong. |
| audit/projected-root | orx/correct-projected-root-for-eq17-common-regime-sw | Correct the projected root and rerun the common-regime sweep. |
| research/paper-scale | orx/symbolic-theorem-4-4-chain-and-paper-scale-check | Theorem dependency graph, primary-source audit, and paper-scale checks. |
| release/rigorous-candidate | orx/release-candidate-evidence-report-and-logbook | Package the six-claim evidence release and report. |
| audit/claim3-feasibility | orx/claim-3-falsification-audit-with-controlled-dime | Audit Claim 3 assumptions, normalization, and controlled dimension behavior. |
| release/claim3-blocked | orx/claim-3-falsification-blocked-release | Preserve the blocked falsification result and its release candidate. |
| release/claim3-publication | orx/claim-3-final-publication-metadata | Record the published Claim 3 metadata and navigation. |

The branch cleanup is recorded in [BRANCH_AUDIT.md](BRANCH_AUDIT.md).

## Reproduce

The formal verifier uses the pinned environment:

```bash
uv sync --frozen
uv run --frozen python repro/src/verify_td.py
```

The cumulative run takes about 190 seconds on the recorded local CPU
environment. It uses exact moment propagation for the controlled rate
experiments, deterministic paper-scale substitutes where the paper’s learned
policy matrices are unavailable, independent checkers, and claim-specific
negative controls.

Start with:

- [Rigorous reproduction report](reports/rigorous-reproduction/report.md)
- [Release report](reports/rigorous-reproduction/release_report.md)
- [Command ledger](reports/rigorous-reproduction/command_ledger.md)
- [Claim 3 falsification report](evidence/claim3-falsification-2026-07-29/report.md)
- [Source manifest](SOURCE_MANIFEST.md)
- [Audit report](AUDIT_REPORT.md)
- [Machine-readable gate](publication_gate.json)

## Repository layout

| Path | Role |
| --- | --- |
| repro/src/ | Reproduction algorithms, exact moments, claim verifiers, and checkers. |
| .openresearch/artifacts/winning_run/ | Authoritative six-claim machine-readable evidence. |
| evidence/claim3-falsification-2026-07-29/ | Focused Claim 3 feasibility/falsification audit. |
| reports/ | Technical and publication-facing reports. |
| notebooks/ | Self-contained tutorial and audit notebooks. |
| outputs/ | Historical output snapshots with provenance notes. |
| pages/ and logbook.json | The preserved publication/logbook surface. |
| publication_gate.json and GATE_READY.md | Release status and scope gate. |

## Limitations

- The exact-rate experiments use controlled two-state families rather than a
  universal worst-case search.
- The paper’s learned Random-Walk policy matrices are not published, so
  paper-scale runs use a documented ergodic cycle with 0.10 teleportation.
- Claim 3’s theorem-symbol result permits implicit dependence through eta,
  norms, and mixing; it is not a claim of dimension-free numerical error.
- Claim 5’s quartic dependence is conditional on eta-prime = Theta(eta), and
  the empirical route alone is non-identifying.
- External judge results are not inferred from local checks.

## Citation

```bibtex
@article{tian2026bridging,
  title   = {Bridging the Gap Between Average and Discounted TD Learning},
  author  = {Tian, Haoxing and Chen, Zaiwei and Paschalidis, Ioannis Ch. and Olshevsky, Alex},
  journal = {arXiv preprint arXiv:2605.02103},
  year    = {2026},
  url     = {https://arxiv.org/abs/2605.02103}
}
```

## Thank you

Thank you to Haoxing Tian, Zaiwei Chen, Ioannis Ch. Paschalidis, and Alex
Olshevsky for making the theoretical construction and its assumptions
available for careful reproduction. Their paper provides a useful target for
turning a small reproduction score into a transparent, claim-by-claim audit.

This repository is maintained and attributed to
[MachineLearning-Nerd](https://github.com/MachineLearning-Nerd).
