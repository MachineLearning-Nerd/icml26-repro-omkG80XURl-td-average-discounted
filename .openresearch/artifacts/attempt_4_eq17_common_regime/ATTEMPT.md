# Actual Eq. (17) route — compatible but non-identifying

- Experiment: `cd031ccb-2fa9-4938-85d0-cf3ae63fb9df`
- Run: `6cb136db-dd63-43a2-b2c8-54af75456b48`
- Git SHA: `51a93874d1f12e978833e272bd72984e6031cd8d`
- Backend: local CPU
- Fixed command: `uv run --frozen python repro/src/verify_td.py`

The actual projected single-chain recursion from Eq. (17) was run with 128
deterministic replicates per condition. The family satisfies
`eta'/eta = 4/3` exactly, the projected root is checked by its mean-field
residual, and a frozen-`w` control is materially worse.

The quartic upper envelope held on smaller held-out `eta`, but a stricter cubic
envelope also held and several per-`eta` finite-window slopes were not near
inverse time. This benign family therefore cannot identify quartic worst-case
dependence. The route remains `BLOCKED` and is preserved without tuning its
pre-registered criteria.
