# Claim 3 falsification command ledger

All commands below were run from the repository worktree unless an absolute
candidate path is shown. Secret values were never printed.

## Startup and source audit

```bash
orx skill
orx skill orx-experiment-tree
orx skill orx-evidence
orx skill orx-git
orx skill orx-compute
orx projects --json
orx runs fa98c879-0e5c-4ae2-beef-51ebf9c50f43
orx exp status b1af4599-5a9d-4aa1-8a54-32b1fb80d9cd
orx paper 2605.02103 --full
curl --fail --location --user-agent 'OpenResearch-Reproduction/1.0 (claim audit; contact via github.com/MachineLearning-Nerd/icml26-repro-omkG80XURl-td-average-discounted)' https://arxiv.org/html/2605.02103
hf spaces info sabaridsnfuji/repro-bridging-the-gap-between-average-and-discounted-td-learning --expand sha --format json
hf download sabaridsnfuji/repro-bridging-the-gap-between-average-and-discounted-td-learning --repo-type space
hf download DineshAI/omkG80XURl --repo-type space --revision cb04bc356fb2ea3641f65cc9bbd06a299b5980b2
```

The paper HTML retrieved on 2026-07-29 has SHA-256
`c6d1ec937365657dfb23856b8b705b1aab889b68c1538f840bc459a7930563d9`.
The peer Claim 3 page at revision
`fe98ec5fc3c12b79e80c94fc231ea9a39e9d1d44` has SHA-256
`22936858b20588c9d9965223968adb0373f54f5aeafeb00a9e3633bd0bd39792`.

## Protected baseline verification

For each `N` in `1,2,4,5,6`:

```bash
uv run --frozen python evidence/rigorous-2026-07-23/claim_N/verifier.py evidence/rigorous-2026-07-23/claim_N
uv run --frozen python evidence/rigorous-2026-07-23/claim_N/independent_checker.py evidence/rigorous-2026-07-23/claim_N
```

All ten commands returned zero against the exact protected revision.

## Experiment tree and formal execution

```bash
orx create-experiment fa98c879-0e5c-4ae2-beef-51ebf9c50f43 --title 'Claim 3 falsification audit with controlled dimensions' --parent b1af4599-5a9d-4aa1-8a54-32b1fb80d9cd
git fetch origin
git checkout orx/claim-3-falsification-audit-with-controlled-dime
git merge --ff-only origin/master
uv run --frozen python -m py_compile repro/src/claim3_falsification.py repro/src/verify_td.py
uv run --frozen python repro/src/claim3_falsification.py
git commit -m 'Audit Claim 3 falsification under exact assumptions'
git push -u origin orx/claim-3-falsification-audit-with-controlled-dime
orx exp run d24fcac4-ff4b-4942-92e3-903a72f3304d --flavor cpu-upgrade --timeout 3600
orx logs b97a05bb-7e92-4031-8e65-0f78fb74c92f --bytes 20000
orx exp run d24fcac4-ff4b-4942-92e3-903a72f3304d --flavor cpu-upgrade --image ghcr.io/astral-sh/uv:python3.12-bookworm-slim --timeout 3600
orx exp wait d24fcac4-ff4b-4942-92e3-903a72f3304d --timeout 480
orx logs b8362379-48cd-4a46-82bf-a554fa12d9e4
```

The first HF attempt failed before code execution because `uv` was absent.
The second completed with the fixed inherited command.

## Candidate and presentation validation

```bash
uv run --frozen python repro/src/build_claim3_release.py <protected-snapshot> <protected-manifest> <baseline-verifiers> <candidate>
uv pip install --python .venv/bin/python marimo==0.23.14
.venv/bin/marimo check --strict notebooks/claim3_falsification.py
xmllint --noout reports/claim3-falsification/images/*.svg
qlmanage -t -s 900 -o /tmp/claim3-svg-preview reports/claim3-falsification/images/*.svg
orx exp run 86697acd-2be6-4dfa-91cd-fc49db6204d0 --flavor cpu-upgrade --image ghcr.io/astral-sh/uv:python3.12-bookworm-slim --timeout 3600
orx exp wait 86697acd-2be6-4dfa-91cd-fc49db6204d0 --timeout 480
orx logs 57675fd5-0fc9-40c6-8f9b-4be4cb744ba2
```

The candidate builder verifies the complete protected subset, byte-identical
non-target hashes, fresh candidate verifiers, JSON, SVG, text-only uploads,
and credential patterns.
