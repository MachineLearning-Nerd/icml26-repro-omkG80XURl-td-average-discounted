"""Independent command-line gate for one generated claim evidence directory."""

from __future__ import annotations

import json
from pathlib import Path
import sys


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: claim_verifier.py CLAIM_DIRECTORY")
        return 64
    claim_dir = Path(sys.argv[1])
    summary = json.loads((claim_dir / "summary.json").read_text())
    checks = summary.get("checks", {})
    failed = [name for name, passed in checks.items() if passed is not True]
    verdict = summary.get("verdict")
    print(json.dumps({"verdict": verdict, "checks": checks, "failed": failed}, sort_keys=True))
    if failed:
        return 1
    if verdict != "VERIFIED":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

