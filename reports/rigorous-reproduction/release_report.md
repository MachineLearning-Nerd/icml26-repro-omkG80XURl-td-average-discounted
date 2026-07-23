# Publication report

- Previous live judged score: `5/12`
- Conservative projected score range after the proposed change: **9–11/12**
- Best-supported possible new score: **12/12 (forecast, not a judge result)**

The current live total remains **5/12**. The previous Hugging Face and Judge
heads were `fd9d1c47147abbf084a3f226faf600c7b5155414`. The approved additive
release is now published at HF revision
`cb04bc356fb2ea3641f65cc9bbd06a299b5980b2`; no new judge verdict has been
observed yet.

| Claim | Current points | Possible points | Confidence | Evidence status | Basis and remaining risk |
|---|---:|---:|---|---|---|
| 1 | 1 | 2 | MEDIUM | VERIFIED | Exact i.i.d. moments give a T exponent of −1.003; a held-out quadratic envelope passes and an eta-inverse-one control fails. The controlled family is not a universal empirical proof. |
| 2 | 1 | 2 | MEDIUM | VERIFIED | Mixing-adjusted Markov regression gives T −1.214 and eta −2.005, with per-eta T slopes from −1.170 to −1.308. Finite-chain coverage remains narrower than the theorem’s universal domain. |
| 3 | 0 | 2 | HIGH | VERIFIED | All three theorem forms omit free d; an injected-d formula fails; the unchanged schedule improves error through d=100. Dimension may still enter implicitly through eta, norms, and mixing, as the source allows. |
| 4 | 1 | 2 | MEDIUM | VERIFIED | The proposed held-out quadratic envelope is paired with SHA-pinned primary-source audits of the prior quartic average-reward and quadratic discounted bounds. Cross-paper condition definitions remain distinct. |
| 5 | 1 | 2 | MEDIUM | VERIFIED | The independently checked Theorem 4.4 dependency graph yields eta-prime inverse, eta-cubed inverse, and T-inverse, becoming quartic only when eta-prime is Theta(eta). The actual Eq. 17 family is compatible but empirically non-identifying. |
| 6 | 1 | 2 | HIGH | VERIFIED | The proof path is checked step by step and the inequality passes 48 deterministic cases through n=1000,d=100; a stronger 1.1 eta3 control fails. Numerical stress supports rather than replaces the analytic argument. |

No claim is `LOW` confidence, so the mandatory three-route retry rule is not
triggered for the approval gate. Claim 5 nevertheless retains three materially
different routes: statement/exponent audit, actual Eq. 17 simulation, and an
independent dependency-graph derivation. No claim is `BLOCKED`.

## What changed

All six claims changed relative to the live verdict:

1. fitted i.i.d. time and held-out condition envelopes replace a tiny
   “error decreased” check;
2. mixing-adjusted time and condition exponents replace a weak negative slope;
3. exact theorem-symbol auditing and an injected-d control replace a norm
   sanity check;
4. measured held-out scaling and SHA-pinned primary sources replace arithmetic
   on unrelated condition numbers;
5. the actual Eq. 17 recursion and exact conditional dependency replace one
   small single-versus-double comparison;
6. a corrected Dirichlet definition, proof-step audit, scale stress, and a
   stronger false control replace one numerical instance.

## Experiment tree and winning revision

The stacked tree is:

`baseline → exact moments → held-out stress → actual Eq. 17 → corrected root → dependency graph + paper scale → release candidate`

The winning scientific branch is
`orx/symbolic-theorem-4-4-chain-and-paper-scale-check` at
`fcf047187bc0139da0c20ed254458f6b35efa99e`. Its cumulative local-CPU run
completed in 3m15s (189.775s measured internally), and all six claim verifiers
plus the independent checker returned success. Formal compute cost was **$0**:
all runs used the user’s local CPU, with no GPU and no Hugging Face upgrade.

The fixed command on every node is:

```bash
uv run --frozen python repro/src/verify_td.py
```

The locked research environment is CPython 3.12.11, NumPy 2.2.6, and uv
0.11.29. Marimo 0.23.14 was installed with `uv pip` only as optional
presentation validation in the same repository `.venv`; it is absent from
`pyproject.toml` and `uv.lock` and is not part of any formal run.

## Release-candidate checks

- Paper HTML SHA-256:
  `2d40f7e54ced7ee48f9b336f2928e081e679293122d09d09e9fe681a6601a9d9`.
- The exact 17-file judged Space snapshot is protected.
- All 17 old paths are present in the candidate.
- Sixteen old files are byte-identical.
- Only `logbook.json` is intentionally changed, solely to add navigation.
- The original judged `logbook.json` is copied into the new evidence tree.
- The exact upload allowlist contains 123 text files.
- All candidate JSON parses, all SVG is valid XML, and the credential-pattern
  scan found no match.
- The notebook passes `marimo check --strict`.

The exact manifest and upload list are in `release/hf-space/`. The illustrated
article, machine evidence, notebook, and formal command ledger are linked from
the repository landing page.

## Publication completed

The 123 allowlisted text paths were published through Hugging Face’s
`create_commit` API to the existing Space `DineshAI/omkG80XURl`. An exact
revision download contained 139 files and matched the approved candidate
byte-for-byte. The reader-facing artifacts were then fast-forwarded to the
repository’s `master` branch without rewriting experiment history. The release
node is marked `PUBLISHED / AWAITING_JUDGE`. No second Space was created, and
the live score remains 5/12 until a new judge verdict exists.
