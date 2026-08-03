# Clean visibility-repair rerun — 2026-08-03

- Command: `uv run --frozen python repro/src/verify_td.py`
- Starting Git SHA: `835edb8f3f6914f89e4b79dc68b2852fd268c2cb`
- Environment: CPython 3.12.11, NumPy 2.2.6, local Apple CPU
- Runtime: 59.759636207978474 seconds
- Cost: USD 0
- Seeds: integers 0 through 63 where stochastic simulation is used
- Result: Claims 1–6 `VERIFIED` at their preregistered source-bound contracts
- Independent checkers: 6/6 returned 0
- Injected-failure verifiers: 6/6 returned nonzero

The regenerated claim directories were compared file-by-file with the judged
Space evidence. All scientific and contract files were byte-identical:

| Claim | Byte-identical files | Expected differences |
| --- | ---: | --- |
| 1 | 14/17 | environment, paper-scale runtime, runtime |
| 2 | 14/17 | environment, paper-scale runtime, runtime |
| 3 | 15/18 | environment, paper-scale runtime, runtime |
| 4 | 13/15 | environment, runtime |
| 5 | 17/19 | environment, runtime |
| 6 | 13/15 | environment, runtime |

The differing files contain machine paths or wall-clock measurements, not
scientific values. In particular, every `summary.json`,
`independent_checker_output.txt`, `negative_control_output.txt`, raw CSV/JSON,
contract, verifier, and checker matched byte-for-byte.

The cumulative sources and locked environment are published at:

- `repro/src/verify_td.py`
- `repro/src/rigorous_campaign.py`
- `repro/src/exact_moments.py`
- `repro/src/paper_scale.py`
- `repro/src/single_chain.py`
- `repro/src/claim3_falsification.py`
- `pyproject.toml`
- `uv.lock`

Claim 3's separate falsification search also reran. It preserved its honest
`BLOCKED` status because no assumption-valid contradiction was found; this is
consistent with verification of the narrower literal generated claim that the
displayed theorem has no explicit free `d` term.
