"""Build and validate an additive Claim 3 falsification Space candidate."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import stat
import subprocess
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[2]
ARTIFACT = (
    ROOT / ".openresearch" / "artifacts" / "claim3_falsification_2026_07_29"
)
REPORT = ROOT / "reports" / "claim3-falsification"
NOTEBOOK = ROOT / "notebooks" / "claim3_falsification.py"
EVIDENCE_REL = Path("evidence") / "claim3-falsification-2026-07-29"
TARGET_PAGE = Path("pages") / "rigorous-claim-3" / "page.md"
TEXT_SUFFIXES = {".md", ".json", ".csv", ".txt", ".py", ".svg"}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def files(root: Path) -> list[Path]:
    return sorted(
        path for path in root.rglob("*")
        if path.is_file() and ".cache/huggingface" not in path.as_posix()
    )


def target_page() -> str:
    return """# Claim 3 falsification audit: BLOCKED

## Focused evidence status

**BLOCKED — no assumption-valid falsification was established.**

The current judged Claim 3 verdict remains `TOY`. This focused audit does not
replace that verdict with `VERIFIED`, does not claim points, and does not infer
that the theorem is true.

The proposed peer counterexample reports `eta1=0.443` at `d=40`. Under the
paper's normalized-feature assumption, every admissible instance satisfies
`eta1 <= 3/d = 0.075`; the reported endpoint is 5.91 times too large. The peer
page publishes no code, raw data, seeds, feature matrix, mixing constants,
parameter norms, or instantiated Theorem D.1 bound.

An independent 64-seed reconstruction with two Markov chains and
`d={5,10,20,40}` observed a hitting-time exponent of `0.183`, not the peer's
self-reported `2.015`. In that admissible family `eta1=1/d` exactly, so a
dimension trend cannot be separated from the theorem's condition-number
dependence.

## Focused falsification evidence

- [Evaluation](../../evidence/claim3-falsification-2026-07-29/EVAL.md)
- [Exact claim contract](../../evidence/claim3-falsification-2026-07-29/claim_contract.json)
- [Source audit](../../evidence/claim3-falsification-2026-07-29/source_audit.md)
- [Method and three routes](../../evidence/claim3-falsification-2026-07-29/method.md)
- [Peer hypothesis audit](../../evidence/claim3-falsification-2026-07-29/peer_hypothesis_audit.json)
- [Raw feasibility check](../../evidence/claim3-falsification-2026-07-29/raw_peer_trace_bound.csv)
- [Raw controlled sweep](../../evidence/claim3-falsification-2026-07-29/raw_controlled_dimension_sweep.csv)
- [Falsification verifier output](../../evidence/claim3-falsification-2026-07-29/falsification_verifier_output.txt)
- [Independent checker output](../../evidence/claim3-falsification-2026-07-29/independent_checker_output.txt)
- [Negative-control output](../../evidence/claim3-falsification-2026-07-29/negative_control_output.txt)
- [Illustrated report](../../evidence/claim3-falsification-2026-07-29/report.md)
- [Preservation table](../../evidence/claim3-falsification-2026-07-29/preservation_table.md)

## Earlier evidence preserved

The earlier source-formula audit and scale check remain byte-for-byte reachable
at their original paths:

- [Earlier evaluation](../../evidence/rigorous-2026-07-23/claim_3/EVAL.md)
- [Earlier contract](../../evidence/rigorous-2026-07-23/claim_3/claim_contract.json)
- [Earlier raw formula dependencies](../../evidence/rigorous-2026-07-23/claim_3/raw_formula_dependencies.json)

The real falsification verifier exits nonzero when no counterexample is
present. The injected explicit-`d` control exits zero, confirming that the
detector can recognize a contradiction.
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("protected_snapshot", type=Path)
    parser.add_argument("protected_manifest", type=Path)
    parser.add_argument("baseline_verifiers", type=Path)
    parser.add_argument("candidate", type=Path)
    args = parser.parse_args()
    snapshot = args.protected_snapshot.resolve()
    candidate = args.candidate.resolve()
    if candidate.exists():
        raise FileExistsError(f"candidate already exists: {candidate}")
    protected = json.loads(args.protected_manifest.read_text())
    shutil.copytree(snapshot, candidate, ignore=shutil.ignore_patterns(".cache"))
    for path in [candidate, *candidate.rglob("*")]:
        path.chmod(path.stat().st_mode | stat.S_IWUSR)

    evidence = candidate / EVIDENCE_REL
    shutil.copytree(ARTIFACT, evidence)
    shutil.copy2(REPORT / "report.md", evidence / "report.md")
    shutil.copy2(REPORT / "release_report.md", evidence / "release_report.md")
    shutil.copy2(REPORT / "command_ledger.md", evidence / "command_ledger.md")
    shutil.copy2(REPORT / "marimo_validation.md", evidence / "marimo_validation.md")
    shutil.copytree(REPORT / "images", evidence / "images")
    shutil.copy2(NOTEBOOK, evidence / "claim3_falsification.py")
    (candidate / TARGET_PAGE).write_text(target_page())

    preservation_rows: list[dict[str, object]] = []
    preservation_dir = evidence / "preservation"
    preservation_dir.mkdir()
    for claim in (1, 2, 4, 5, 6):
        claim_dir = candidate / "evidence" / "rigorous-2026-07-23" / f"claim_{claim}"
        baseline_parts: list[str] = []
        candidate_parts: list[str] = []
        returncodes: list[int] = []
        commands: list[str] = []
        for name in ("verifier", "independent_checker"):
            script = claim_dir / f"{name}.py"
            claim_relative = claim_dir.relative_to(candidate)
            command = (
                f"uv run --frozen python {script.relative_to(candidate)} "
                f"{claim_relative}"
            )
            result = subprocess.run(
                [sys.executable, str(script), str(claim_dir)],
                cwd=candidate,
                capture_output=True,
                text=True,
            )
            output = result.stdout + result.stderr + f"returncode={result.returncode}\n"
            (preservation_dir / f"claim_{claim}_{name}.txt").write_text(output)
            baseline_file = args.baseline_verifiers / f"claim_{claim}_{name}.txt"
            baseline_parts.append(baseline_file.read_text())
            candidate_parts.append(output)
            returncodes.append(result.returncode)
            commands.append(command)
        protected_paths = sorted(
            entry["path"]
            for entry in protected["files"]
            if entry.get("claims") == [claim]
        )
        preservation_rows.append(
            {
                "claim": claim,
                "old_verdict": "VERIFIED",
                "protected_paths": protected_paths,
                "candidate_paths": protected_paths,
                "verifier_command": " && ".join(commands),
                "baseline_result": "PASS" if all(
                    "returncode=0" in text for text in baseline_parts
                ) else "FAIL",
                "candidate_result": "PASS" if returncodes == [0, 0] else "FAIL",
                "regression_status": "UNCHANGED" if returncodes == [0, 0] else "REGRESSION",
            }
        )

    table = [
        "# Protected non-target preservation table",
        "",
        "| Claim | Old verdict | Protected paths | Candidate paths | Verifier command | Baseline | Candidate | Regression |",
        "|---:|---|---|---|---|---|---|---|",
    ]
    for row in preservation_rows:
        paths = f"{len(row['protected_paths'])} unchanged claim-specific files"
        table.append(
            f"| {row['claim']} | {row['old_verdict']} | {paths} | {paths} | "
            f"`{row['verifier_command']}` | {row['baseline_result']} | "
            f"{row['candidate_result']} | {row['regression_status']} |"
        )
    table.extend(
        [
            "",
            "Shared protected files and every non-target claim-specific file are",
            "also checked byte-for-byte against the protected manifest.",
        ]
    )
    (evidence / "preservation_table.md").write_text("\n".join(table) + "\n")
    (evidence / "preservation_results.json").write_text(
        json.dumps(preservation_rows, indent=2, sort_keys=True) + "\n"
    )

    protected_paths = {entry["path"] for entry in protected["files"]}
    candidate_paths = {
        str(path.relative_to(candidate)) for path in files(candidate)
    }
    missing = sorted(protected_paths - candidate_paths)
    protected_non_target = [
        entry for entry in protected["files"] if entry["protected_non_target"]
    ]
    hash_mismatches = [
        {
            "path": entry["path"],
            "expected": entry["sha256"],
            "observed": sha256(candidate / entry["path"]),
        }
        for entry in protected_non_target
        if sha256(candidate / entry["path"]) != entry["sha256"]
    ]
    if missing or hash_mismatches:
        raise AssertionError(
            f"protected regression: missing={missing}, mismatches={hash_mismatches}"
        )
    if any(row["candidate_result"] != "PASS" for row in preservation_rows):
        raise AssertionError("a protected non-target verifier failed")

    for path in files(candidate):
        if path.suffix == ".json":
            json.loads(path.read_text())
        if path.suffix == ".svg":
            ET.parse(path)

    secret_pattern = re.compile(
        r"(hf_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|"
        r"sk-[A-Za-z0-9]{20,}|BEGIN [A-Z ]*PRIVATE KEY)"
    )
    secret_matches = []
    for path in files(candidate):
        if path.suffix in TEXT_SUFFIXES:
            match = secret_pattern.search(path.read_text(errors="replace"))
            if match:
                secret_matches.append(str(path.relative_to(candidate)))
    if secret_matches:
        raise AssertionError(f"credential-like strings found: {secret_matches}")

    changed_or_added = []
    protected_hashes = {
        entry["path"]: entry["sha256"] for entry in protected["files"]
    }
    for path in files(candidate):
        relative = str(path.relative_to(candidate))
        if relative not in protected_hashes or sha256(path) != protected_hashes[relative]:
            changed_or_added.append(relative)
    non_text = [
        path for path in changed_or_added
        if Path(path).suffix not in TEXT_SUFFIXES
    ]
    if non_text:
        raise AssertionError(f"non-text upload requested: {non_text}")

    allowlist_path = evidence / "upload_allowlist.txt"
    manifest_path = evidence / "candidate_manifest.json"
    for special in (
        str(allowlist_path.relative_to(candidate)),
        str(manifest_path.relative_to(candidate)),
    ):
        if special not in changed_or_added:
            changed_or_added.append(special)
    changed_or_added.sort()
    allowlist_path.write_text("\n".join(changed_or_added) + "\n")

    candidate_manifest = {
        "space_id": "DineshAI/omkG80XURl",
        "protected_revision": "cb04bc356fb2ea3641f65cc9bbd06a299b5980b2",
        "protected_file_count": len(protected_paths),
        "candidate_file_count": len(files(candidate)) + 1,
        "complete_protected_subset": not missing,
        "protected_non_target_count": len(protected_non_target),
        "protected_non_target_hashes_identical": not hash_mismatches,
        "target_page_changed_only": str(TARGET_PAGE),
        "non_target_verifiers_pass": True,
        "upload_is_text_only": True,
        "secret_scan_pass": True,
        "upload_allowlist_count": len(changed_or_added),
        "upload_allowlist": changed_or_added,
        "files": [
            {
                "path": str(path.relative_to(candidate)),
                "sha256": sha256(path),
                "bytes": path.stat().st_size,
            }
            for path in files(candidate)
            if path != manifest_path
        ],
    }
    manifest_path.write_text(
        json.dumps(candidate_manifest, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps({
        key: candidate_manifest[key]
        for key in (
            "protected_file_count",
            "candidate_file_count",
            "complete_protected_subset",
            "protected_non_target_count",
            "protected_non_target_hashes_identical",
            "non_target_verifiers_pass",
            "upload_is_text_only",
            "secret_scan_pass",
            "upload_allowlist_count",
        )
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
