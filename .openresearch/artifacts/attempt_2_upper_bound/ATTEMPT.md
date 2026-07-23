# Attempt 2 — held-out quadratic upper-bound envelope

- Experiment: `ceef4ab8-dff2-4fad-a2ca-f88b5433faa7`
- Run: `890dc4bb-9b02-445e-ae0a-c24895a9ff18`
- Git SHA: `f06f34fdfe461b320c0ba8bc1faa4fcda42ec79b`
- Backend: local CPU
- Fixed command: `uv run --frozen python repro/src/verify_td.py`

This attempt interprets the soft-O sample-complexity statement as an upper
bound, not an equality of fitted exponents. Claim 1 calibrates an
`eta^-2 / T` envelope only on `eta >= 0.20`, validates it at held-out smaller
`eta`, and requires an `eta^-1 / T` negative-control envelope to fail. Claims
2, 3, and 6 rerun their accepted exact/source contracts. Claims 4 and 5 remain
`BLOCKED` in this snapshot because matched prior algorithms and the paper's
actual Eq. 17 single-chain update were not yet implemented.

All root-level files from the completed run are copied verbatim below this
directory. The pre-existing `attempt_1_exact` subtree is intentionally not
nested a second time.
