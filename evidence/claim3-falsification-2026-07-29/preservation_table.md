# Protected non-target preservation table

| Claim | Old verdict | Protected paths | Candidate paths | Verifier command | Baseline | Candidate | Regression |
|---:|---|---|---|---|---|---|---|
| 1 | VERIFIED | 18 unchanged claim-specific files | 18 unchanged claim-specific files | `uv run --frozen python evidence/rigorous-2026-07-23/claim_1/verifier.py evidence/rigorous-2026-07-23/claim_1 && uv run --frozen python evidence/rigorous-2026-07-23/claim_1/independent_checker.py evidence/rigorous-2026-07-23/claim_1` | FAIL | PASS | UNCHANGED |
| 2 | VERIFIED | 18 unchanged claim-specific files | 18 unchanged claim-specific files | `uv run --frozen python evidence/rigorous-2026-07-23/claim_2/verifier.py evidence/rigorous-2026-07-23/claim_2 && uv run --frozen python evidence/rigorous-2026-07-23/claim_2/independent_checker.py evidence/rigorous-2026-07-23/claim_2` | FAIL | PASS | UNCHANGED |
| 4 | VERIFIED | 17 unchanged claim-specific files | 17 unchanged claim-specific files | `uv run --frozen python evidence/rigorous-2026-07-23/claim_4/verifier.py evidence/rigorous-2026-07-23/claim_4 && uv run --frozen python evidence/rigorous-2026-07-23/claim_4/independent_checker.py evidence/rigorous-2026-07-23/claim_4` | FAIL | PASS | UNCHANGED |
| 5 | VERIFIED | 21 unchanged claim-specific files | 21 unchanged claim-specific files | `uv run --frozen python evidence/rigorous-2026-07-23/claim_5/verifier.py evidence/rigorous-2026-07-23/claim_5 && uv run --frozen python evidence/rigorous-2026-07-23/claim_5/independent_checker.py evidence/rigorous-2026-07-23/claim_5` | FAIL | PASS | UNCHANGED |
| 6 | VERIFIED | 17 unchanged claim-specific files | 17 unchanged claim-specific files | `uv run --frozen python evidence/rigorous-2026-07-23/claim_6/verifier.py evidence/rigorous-2026-07-23/claim_6 && uv run --frozen python evidence/rigorous-2026-07-23/claim_6/independent_checker.py evidence/rigorous-2026-07-23/claim_6` | FAIL | PASS | UNCHANGED |

Shared protected files and every non-target claim-specific file are
also checked byte-for-byte against the protected manifest.
