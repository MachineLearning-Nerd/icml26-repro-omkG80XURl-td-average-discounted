# Research and release command ledger

This ledger records the commands that created, ran, inspected, and validated
the formal evidence. Read-only shell inspections (`rg`, `sed`, `git status`,
`df`, XML/JSON parsing, and protected-tree comparisons) are summarized at the
end because they do not alter the scientific result.

## Startup and source audit

```bash
orx skill
orx skill orx-experiment-tree
orx skill orx-evidence
orx skill orx-git
orx skill orx-compute
orx projects --json
orx runs fa98c879-0e5c-4ae2-beef-51ebf9c50f43
orx project view fa98c879-0e5c-4ae2-beef-51ebf9c50f43
git branch -a
git rev-parse HEAD
git status --short
df -h .
env | cut -d= -f1 | sort
curl -L -A 'OpenResearch-Reproduction/1.0 (paper audit; contact via repository)' https://ar5iv.labs.arxiv.org/html/2605.02103
shasum -a 256 paper.html
orx paper 2605.02103 --full
```

The live verdict dataset was fetched and filtered by the exact
`space_id == "DineshAI/omkG80XURl"`. The judged Space revision
`fd9d1c47147abbf084a3f226faf600c7b5155414` was downloaded through the
Hugging Face API, and a SHA-256 protected manifest was generated before any
candidate copy existed. Tokens, credential values, and generated wrappers were
never printed.

## Fixed environment and baseline

```bash
uv lock
uv sync --frozen
orx create-experiment fa98c879-0e5c-4ae2-beef-51ebf9c50f43 --title "Baseline: judged toy verifier in locked uv environment" --run-command 'uv run --frozen python repro/src/verify_td.py'
orx exp run 0acbbffe-b242-40ea-9167-df7589cab4dd --backend local
orx exp wait 0acbbffe-b242-40ea-9167-df7589cab4dd --timeout 480
orx logs af1a658d-4208-47f1-8ef1-036fd3d76b69
```

## Experiment tree

```bash
orx create-experiment fa98c879-0e5c-4ae2-beef-51ebf9c50f43 --title "Exact moment contracts on controlled chain family" --parent 0acbbffe-b242-40ea-9167-df7589cab4dd
orx exp run 96fb0602-a662-48b7-9672-441e37dfc762 --backend local
orx exp wait 96fb0602-a662-48b7-9672-441e37dfc762 --timeout 480
orx logs d4bf0ab1-6fa3-42b8-a22e-cbe0a516844e
orx exp run 96fb0602-a662-48b7-9672-441e37dfc762 --backend local
orx exp wait 96fb0602-a662-48b7-9672-441e37dfc762 --timeout 480
orx logs 59aeff21-1b2e-481e-ac04-184cb3ff423d

orx create-experiment fa98c879-0e5c-4ae2-beef-51ebf9c50f43 --title "Freeze exact evidence and stress asymptotic iid regime" --parent 96fb0602-a662-48b7-9672-441e37dfc762
orx exp run ceef4ab8-dff2-4fad-a2ca-f88b5433faa7 --backend local
orx exp wait ceef4ab8-dff2-4fad-a2ca-f88b5433faa7 --timeout 480
orx logs 890dc4bb-9b02-445e-ae0a-c24895a9ff18

orx create-experiment fa98c879-0e5c-4ae2-beef-51ebf9c50f43 --title "Actual single-chain and matched prior-rate contracts" --parent ceef4ab8-dff2-4fad-a2ca-f88b5433faa7
orx exp run 277ccfbb-5fbf-4baa-8231-7a7fd09d575a --backend local
orx exp wait 277ccfbb-5fbf-4baa-8231-7a7fd09d575a --timeout 480
orx logs dd9e8d62-d0eb-4642-bd1f-718159fa0638

orx create-experiment fa98c879-0e5c-4ae2-beef-51ebf9c50f43 --title "Correct projected root for Eq17 common-regime sweep" --parent 277ccfbb-5fbf-4baa-8231-7a7fd09d575a
orx exp run cd031ccb-2fa9-4938-85d0-cf3ae63fb9df --backend local
orx exp wait cd031ccb-2fa9-4938-85d0-cf3ae63fb9df --timeout 480
orx logs 6cb136db-dd63-43a2-b2c8-54af75456b48

orx create-experiment fa98c879-0e5c-4ae2-beef-51ebf9c50f43 --title "Symbolic Theorem 4.4 chain and paper-scale checks" --parent cd031ccb-2fa9-4938-85d0-cf3ae63fb9df
orx exp run eadcfe06-245c-403b-990d-cad97eac8e28 --backend local
orx exp wait eadcfe06-245c-403b-990d-cad97eac8e28 --timeout 480
orx logs 9271fe67-6213-4c01-adb6-02fbd84b3e65

orx create-experiment fa98c879-0e5c-4ae2-beef-51ebf9c50f43 --title "Release candidate evidence report and logbook" --parent eadcfe06-245c-403b-990d-cad97eac8e28
```

Every experiment edit followed the same Git sequence:

```bash
git fetch origin
git checkout <experiment-branch>
git add <scoped experiment files>
git commit -m '<experiment-specific message>'
git push origin <experiment-branch>
```

## Release validation

```bash
uv run --frozen python repro/src/build_report.py
uv run --frozen python -m py_compile repro/src/build_report.py repro/src/build_release_candidate.py notebooks/td_rate_reproduction.py
xmllint --noout reports/rigorous-reproduction/images/*.svg
uv run --frozen python repro/src/build_release_candidate.py <protected-snapshot> <fresh-candidate>
uv pip install --python .venv/bin/python 'marimo==0.14.17'
uv pip install --python .venv/bin/python --upgrade marimo
.venv/bin/marimo check --fix notebooks/td_rate_reproduction.py
.venv/bin/marimo check --strict notebooks/td_rate_reproduction.py
```

Additional read-only checks validated every candidate JSON file with `jq`,
rendered every report SVG for visual inspection, counted and hashed the old and
new trees, confirmed the 17-path subset, and scanned the repository and
candidate for common token/private-key patterns without printing values.
