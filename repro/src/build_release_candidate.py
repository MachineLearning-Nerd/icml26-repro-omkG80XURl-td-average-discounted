"""Build an additive, text-only Trackio logbook release candidate."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import stat


ROOT = Path(__file__).resolve().parents[2]
WINNING = ROOT / ".openresearch" / "artifacts" / "winning_run"
REPORT = ROOT / "reports" / "rigorous-reproduction"
JUDGED_REVISION = "fd9d1c47147abbf084a3f226faf600c7b5155414"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_page(path: Path, title: str, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"# {title}\n\n{body.strip()}\n")


def claim_page(number: int, summary: dict[str, object]) -> str:
    checks = "\n".join(
        f"- [{'x' if passed else ' '}] `{name}`"
        for name, passed in summary["checks"].items()
    )
    evidence = f"../../evidence/rigorous-2026-07-23/claim_{number}"
    special = ""
    if number == 1:
        special = (
            "\n\nExact regression: T exponent **−1.003**. The quadratic "
            "held-out envelope passed and the eta-inverse-one control failed."
        )
    elif number == 2:
        special = (
            "\n\nMixing-adjusted regression: T exponent **−1.214**, eta "
            "exponent **−2.005**; all per-eta T exponents lie between "
            "−1.170 and −1.308."
        )
    elif number == 3:
        special = (
            "\n\nThe result is a source-formula property: dimension may still "
            "enter implicitly through eta, norms, and mixing."
        )
    elif number == 4:
        special = (
            "\n\nThe audit keeps eta1, eta2, eta3, and discounted condition "
            "numbers distinct. It does not compare bare powers of one scalar."
        )
    elif number == 5:
        special = (
            "\n\nThe actual Eq. 17 family is compatible but non-identifying: "
            "a cubic envelope also holds. Verification comes from the exact "
            "Theorem 4.4 dependency graph and conditional substitution."
        )
    elif number == 6:
        special = (
            "\n\nThe 48-case suite includes dense nonreversible chains and "
            "n=1000,d=100. The stronger 1.1*eta3 control fails."
        )
    return f"""
## Verdict

**{summary['verdict']}**

{summary['assessment']}{special}

## Contract checks

{checks}

Independent checker return code: `{summary['independent_checker_returncode']}`.
The injected-failure verifier returned nonzero.

## Durable evidence

- [Evaluation]({evidence}/EVAL.md)
- [Claim contract]({evidence}/claim_contract.json)
- [Source audit]({evidence}/source_audit.md)
- [Method]({evidence}/method.md)
- [Limitations]({evidence}/limitations.md)
- [Summary]({evidence}/summary.json)
- [Independent checker output]({evidence}/independent_checker_output.txt)
- [Negative-control output]({evidence}/negative_control_output.txt)
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot", type=Path)
    parser.add_argument("candidate", type=Path)
    args = parser.parse_args()
    snapshot = args.snapshot.resolve()
    candidate = args.candidate.resolve()
    if candidate.exists():
        raise FileExistsError(
            f"candidate already exists; refusing to overwrite: {candidate}"
        )
    shutil.copytree(snapshot, candidate)
    for path in [candidate, *candidate.rglob("*")]:
        path.chmod(path.stat().st_mode | stat.S_IWUSR)

    evidence = candidate / "evidence" / "rigorous-2026-07-23"
    evidence.mkdir(parents=True)
    for number in range(1, 7):
        shutil.copytree(WINNING / f"claim_{number}", evidence / f"claim_{number}")
    shutil.copy2(WINNING / "campaign_summary.json", evidence)
    shutil.copy2(WINNING / "artifact_manifest.json", evidence)
    shutil.copy2(WINNING / "ATTEMPT.md", evidence)
    shutil.copy2(REPORT / "report.md", evidence / "illustrated_report.md")
    shutil.copy2(REPORT / "release_report.md", evidence)
    shutil.copy2(REPORT / "command_ledger.md", evidence)
    shutil.copy2(REPORT / "marimo_validation.md", evidence)
    shutil.copy2(
        ROOT / "notebooks" / "td_rate_reproduction.py",
        evidence / "td_rate_reproduction.py",
    )
    shutil.copytree(REPORT / "images", evidence / "images")

    exact_logbook = evidence / f"judged-{JUDGED_REVISION}-logbook.json"
    shutil.copy2(snapshot / "logbook.json", exact_logbook)

    overview_body = """
This additive evidence package replaces none of the judged pages. It adds a
rigorous campaign with exact moments, held-out rate envelopes, paper-scale
checks, primary-source audits, independent checkers, and negative controls.

The previous live judged score is **5/12**. All six local contracts report
`VERIFIED`, but this page does not claim judge points; only a later live verdict
can change the score.

| Claim | Local evidence verdict | Key result |
|---|---|---|
| 1 | VERIFIED | i.i.d. T exponent −1.003; held-out quadratic envelope |
| 2 | VERIFIED | Markov T exponent −1.214, eta exponent −2.005 |
| 3 | VERIFIED | no explicit d in all theorem forms; scale check through d=100 |
| 4 | VERIFIED | measured new envelope plus quartic/quadratic primary-source audit |
| 5 | VERIFIED | eta-prime inverse, eta-cubed inverse general dependency; quartic conditionally |
| 6 | VERIFIED | proof steps and 48 stress cases through n=1000,d=100 |

See the six claim pages in the navigation and the
[illustrated report](../../evidence/rigorous-2026-07-23/illustrated_report.md).
"""
    write_page(
        candidate / "pages" / "rigorous-reproduction" / "page.md",
        "Rigorous reproduction — 2026-07-23",
        overview_body,
    )

    new_children = [
        {
            "slug": "rigorous-reproduction",
            "title": "Rigorous reproduction",
            "file": "pages/rigorous-reproduction/page.md",
            "children": [],
        }
    ]
    for number in range(1, 7):
        summary = json.loads(
            (WINNING / f"claim_{number}" / "summary.json").read_text()
        )
        slug = f"rigorous-claim-{number}"
        write_page(
            candidate / "pages" / slug / "page.md",
            f"Rigorous Claim {number}: {summary['verdict']}",
            claim_page(number, summary),
        )
        new_children.append(
            {
                "slug": slug,
                "title": f"Rigorous Claim {number}",
                "file": f"pages/{slug}/page.md",
                "children": [],
            }
        )

    logbook_path = candidate / "logbook.json"
    logbook = json.loads(logbook_path.read_text())
    existing_slugs = {child["slug"] for child in logbook["root"]["children"]}
    if existing_slugs.intersection(child["slug"] for child in new_children):
        raise ValueError("new logbook slug collides with judged navigation")
    logbook["root"]["children"].extend(new_children)
    logbook["updated_at"] = "2026-07-23T21:00:00+00:00"
    logbook["agent_view_tokens"] = max(
        int(logbook.get("agent_view_tokens", 0)), 6000
    )
    logbook_path.write_text(json.dumps(logbook, indent=2) + "\n")

    old_paths = sorted(
        str(path.relative_to(snapshot))
        for path in snapshot.rglob("*")
        if path.is_file()
    )
    new_paths = {
        str(path.relative_to(candidate))
        for path in candidate.rglob("*")
        if path.is_file()
    }
    missing = [path for path in old_paths if path not in new_paths]
    if missing:
        raise AssertionError(f"judged paths missing from candidate: {missing}")

    old_hashes = {
        str(path.relative_to(snapshot)): sha256(path)
        for path in snapshot.rglob("*")
        if path.is_file()
    }
    identical = [
        path
        for path, digest in old_hashes.items()
        if sha256(candidate / path) == digest
    ]
    changed = sorted(set(old_paths) - set(identical))
    additions = sorted(new_paths - set(old_paths))
    non_text = [
        path
        for path in additions + changed
        if (candidate / path).suffix.lower()
        not in {".md", ".json", ".csv", ".txt", ".py", ".svg"}
    ]
    if non_text:
        raise AssertionError(f"non-text upload candidate: {non_text}")

    manifest = {
        "judged_revision": JUDGED_REVISION,
        "old_file_count": len(old_paths),
        "candidate_file_count": len(new_paths),
        "old_paths_are_subset": not missing,
        "byte_identical_old_paths": identical,
        "intentionally_changed_old_paths": changed,
        "exact_judged_logbook_copy": str(exact_logbook.relative_to(candidate)),
        "upload_allowlist": additions + changed,
        "files": [
            {
                "path": path,
                "sha256": sha256(candidate / path),
                "bytes": (candidate / path).stat().st_size,
            }
            for path in additions + changed
        ],
    }
    release_dir = candidate.parent
    (release_dir / "release_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n"
    )
    (release_dir / "upload_allowlist.txt").write_text(
        "\n".join(additions + changed) + "\n"
    )
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
