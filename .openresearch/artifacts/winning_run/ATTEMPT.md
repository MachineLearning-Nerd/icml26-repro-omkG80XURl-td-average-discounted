# Winning cumulative scientific run

- Experiment: `eadcfe06-245c-403b-990d-cad97eac8e28`
- Run: `9271fe67-6213-4c01-adb6-02fbd84b3e65`
- Git SHA: `fcf047187bc0139da0c20ed254458f6b35efa99e`
- Backend: local CPU
- Fixed command: `uv run --frozen python repro/src/verify_td.py`
- Internal runtime: `189.77527779201046` seconds

All six cumulative claim contracts report `VERIFIED`; all six independent
checkers returned zero, and every injected-failure verifier returned nonzero.
The verdicts are reproduction findings, not live-judge points. The live judged
score remains `5/12` until the external judge evaluates a published revision.
