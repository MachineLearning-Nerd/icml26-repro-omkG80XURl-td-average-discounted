# Branch audit

## Target policy

- Default branch: main
- Public branches: 11
- Legacy refs to remove: master and every orx/* branch
- Branch purpose: encoded in descriptive baseline/*, research/*, audit/*, and
  release/* names
- Reachable commit identity: MachineLearning-Nerd
  <MachineLearning-Nerd@users.noreply.github.com>

## Mapping

| Final branch | Source ref | Purpose |
| --- | --- | --- |
| main | master | Publication surface and final audit documents. |
| baseline/judged-toy | orx/baseline-judged-toy-verifier-in-locked-uv-enviro | Original weak verifier baseline. |
| research/exact-moments | orx/exact-moment-contracts-on-controlled-chain-famil | Exact moment operators. |
| research/held-out-rates | orx/freeze-exact-evidence-and-stress-asymptotic-iid | Held-out rate evidence. |
| audit/single-chain-eq17 | orx/actual-single-chain-and-matched-prior-rate-contr | Failed target-root route, retained for audit. |
| audit/projected-root | orx/correct-projected-root-for-eq17-common-regime-sw | Corrected projected-root route. |
| research/paper-scale | orx/symbolic-theorem-4-4-chain-and-paper-scale-check | Winning theorem and paper-scale route. |
| release/rigorous-candidate | orx/release-candidate-evidence-report-and-logbook | Six-claim release candidate. |
| audit/claim3-feasibility | orx/claim-3-falsification-audit-with-controlled-dime | Claim 3 feasibility audit. |
| release/claim3-blocked | orx/claim-3-falsification-blocked-release | Blocked Claim 3 release. |
| release/claim3-publication | orx/claim-3-final-publication-metadata | Publication metadata and navigation. |

## Cleanup record

The mapping is intentionally explicit so old names remain understandable in
the provenance record after the old remote refs were deleted. On 2026-08-14,
the GitHub remote was verified with default branch main, exactly 11 public
branches, no master or orx/* refs, and MachineLearning-Nerd as the only
reachable commit identity across the final local branches.
