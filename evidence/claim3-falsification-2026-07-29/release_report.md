# Claim 3 focused release report

- Previous live judged score: `6/12`
- Conservative projected score after this change: **6/12**
- Best-supported possible score: **6/12 forecast; no increase claimed**

This campaign was limited to falsifying Claim 3. It did not establish an
assumption-valid counterexample, so the focused evidence status is `BLOCKED`
and the current judged `TOY` verdict is preserved. Publication is useful as a
negative research result and as an auditable rejection of the peer hypothesis;
it is not forecast to improve the score.

| Claim | Protected status | Candidate status | Confidence | Regression |
|---|---|---|---|---|
| 1 | existing evidence preserved | unchanged | HIGH | verifier + independent checker pass |
| 2 | existing evidence preserved | unchanged | HIGH | verifier + independent checker pass |
| 3 | judged `TOY` | falsification `BLOCKED`; `TOY` preserved | HIGH for BLOCKED decision | target-only additive update |
| 4 | existing evidence preserved | unchanged | HIGH | verifier + independent checker pass |
| 5 | existing evidence preserved | unchanged | HIGH | verifier + independent checker pass |
| 6 | existing evidence preserved | unchanged | HIGH | verifier + independent checker pass |

## Scientific result

The peer hypothesis reports a \(d^{2.015}\) hitting-time slope and
\(\eta_1=0.443\) at \(d=40\). Three independent routes did not produce a valid
falsification:

1. Theorem 4.3 and full Theorem D.1 contain no free \(d\); an injected-\(d\)
   control is detected.
2. Normalized features imply \(\eta_1\le3/d\), so the peer endpoint exceeds
   the admissible \(d=40\) maximum by 5.91×.
3. An independent 64-seed Equation (15) sweep gives a hitting-time exponent
   of 0.183, with \(\eta_1=1/d\) exactly. Dimension and condition-number
   dependence are therefore non-identifiable in that admissible family.

The route is blocked because the peer Space publishes no code, raw data,
features, rewards, seeds, theorem constants, or executable verifier, and the
paper leaves the sufficient-\(c_0\) threshold implicit through Lemma D.2.

## Compute and revisions

- Scientific branch:
  `orx/claim-3-falsification-audit-with-controlled-dime`
- Scientific Git SHA:
  `3ec797a7b78e54dcce9913d8148a019b3ffd5c98`
- Formal run:
  `b8362379-48cd-4a46-82bf-a554fa12d9e4`
- Backend:
  Hugging Face `cpu-upgrade`, no GPU
- Runtime:
  3m32s
- Exact command:
  `uv run --frozen python repro/src/verify_td.py`
- Cost:
  Hugging Face bills the user account per minute; neither the job result nor
  `orx` exposed an exact charge, so no amount is guessed.
- Failed setup attempt:
  `b97a05bb-7e92-4031-8e65-0f78fb74c92f` exited 127 before code execution
  because the default image lacked `uv`; it is excluded from scientific
  evidence.
- Fresh release-child run:
  `57675fd5-0fc9-40c6-8f9b-4be4cb744ba2` at
  `2461c6b0025ea7f8c6ecb6ae3e45e187ad041bc7`, completed in 3m37s with the
  same cumulative result.

## Protected evidence and candidate

The protected Space revision is
`cb04bc356fb2ea3641f65cc9bbd06a299b5980b2`, containing 139 inventoried files.
The candidate contains every protected path. All 120 protected non-target
files have identical SHA-256 hashes, and every non-target verifier and
independent checker passes from the fresh candidate. The only changed
protected path is the target canonical page
`pages/rigorous-claim-3/page.md`; all other changes are additive text evidence.

The candidate manifest, 45-path text-only upload allowlist, preservation
table, secret scan, JSON checks, SVG checks, and notebook validation are part
of the release evidence. No second Space or repository is created.

## Release decision

The release gate passes for an honest `BLOCKED` result:

- all target routes and limitations are recorded;
- the real falsification verifier exits nonzero;
- the injected explicit-\(d\) control exits zero;
- cumulative non-target checks pass;
- protected non-target hashes are unchanged;
- all new uploads are text;
- the credential-pattern scan is clean;
- every SVG renders and the notebook passes `marimo check --strict`.

Publication does not change the live score. Only a later judge verdict can do
so.
