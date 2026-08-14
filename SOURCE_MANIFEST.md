# Source manifest

This manifest separates the paper source, generated evidence, publication
artifacts, and historical snapshots. It is the navigation point for checking
which file supports which statement.

## Paper identity

| Field | Value |
| --- | --- |
| Title | *Bridging the Gap Between Average and Discounted TD Learning* |
| Authors | Haoxing Tian; Zaiwei Chen; Ioannis Ch. Paschalidis; Alex Olshevsky |
| arXiv | [2605.02103](https://arxiv.org/abs/2605.02103) |
| OpenReview identifier | omkG80XURl |
| Paper HTML used for theorem audits | [ar5iv HTML](https://ar5iv.labs.arxiv.org/html/2605.02103) |
| Retrieved paper HTML SHA-256 | 2d40f7e54ced7ee48f9b336f2928e081e679293122d09d09e9fe681a6601a9d9 |

## Evidence roots

| Root | Authority | Contents |
| --- | --- | --- |
| .openresearch/artifacts/winning_run/ | Current local scientific evidence | Six claim contracts, raw outputs, source audits, independent checkers, and the cumulative summary. |
| evidence/claim3-falsification-2026-07-29/ | Current focused audit | Claim 3 formula audit, normalization feasibility check, controlled sweep, controls, and BLOCKED verdict. |
| reports/rigorous-reproduction/ | Explanatory release report | Rate measurements, theorem dependency explanations, limitations, and command ledger. |
| reports/claim3-falsification/ | Focused report mirror | Narrative and preservation records for the Claim 3 campaign. |
| release/hf-space/ | External publication provenance | Protected Space snapshots, allowlists, and publication manifests. |
| outputs/verdict.json | Historical toy snapshot only | Preserved for lineage; not authoritative for the current six-claim result. |

## Claim-to-artifact map

| Claim | Primary machine evidence | Main producer |
| --- | --- | --- |
| C1 | .openresearch/artifacts/winning_run/claim_1/ | repro/src/exact_moments.py, repro/src/rigorous_campaign.py |
| C2 | .openresearch/artifacts/winning_run/claim_2/ | repro/src/exact_moments.py, repro/src/rigorous_campaign.py |
| C3 | .openresearch/artifacts/winning_run/claim_3/ and evidence/claim3-falsification-2026-07-29/ | repro/src/rigorous_campaign.py, repro/src/claim3_falsification.py |
| C4 | .openresearch/artifacts/winning_run/claim_4/ | repro/src/rigorous_campaign.py and primary-source audit inputs |
| C5 | .openresearch/artifacts/winning_run/claim_5/ | repro/src/single_chain.py, dependency graph, and independent checker |
| C6 | .openresearch/artifacts/winning_run/claim_6/ | repro/src/claim_verifier.py and repro/src/independent_checker.py |

## Publication record

- Space: DineshAI/omkG80XURl
- Published candidate revision: cb04bc356fb2ea3641f65cc9bbd06a299b5980b2
- Previous judged revision: fd9d1c47147abbf084a3f226faf600c7b5155414
- No new external judge score is inferred from the local evidence.

The exact Space manifests are retained because they distinguish protected
historical files from the later additive evidence release.
