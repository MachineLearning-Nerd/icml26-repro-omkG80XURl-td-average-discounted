# Attempt 3 — Eq. (17) run with a rejected target oracle

- Experiment: `277ccfbb-5fbf-4baa-8231-7a7fd09d575a`
- Run: `dd9e8d62-d0eb-4642-bd1f-718159fa0638`
- Git SHA: `03fbf600a84be7c073ffbc7e6cf0da0e35b4528a`
- Backend: local CPU
- Fixed command: `uv run --frozen python repro/src/verify_td.py`

This snapshot is preserved as failed evidence. The actual paper Eq. (17)
recursion was run, but the verifier compared the parameter against `theta=1`.
For the non-centered feature family `phi=(0,s)`, direct substitution into the
projected Bellman equation gives

`theta* = Dir(phi) / (Dir(phi) + (mu^T phi)^2) = 1/3`.

The observed mean parameter was approximately `0.332`, exposing the target
oracle error. The independent checker returned nonzero and Claim 5 remained
`BLOCKED`. This run is not counted as affirmative Claim 5 evidence.
