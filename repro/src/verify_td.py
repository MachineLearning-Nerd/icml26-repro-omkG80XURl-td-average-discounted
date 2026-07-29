"""Fixed OpenResearch entrypoint for the cumulative reproduction campaign."""

from __future__ import annotations

from claim3_falsification import run as run_claim3_falsification
from rigorous_campaign import run as run_cumulative


if __name__ == "__main__":
    cumulative_returncode = run_cumulative()
    if cumulative_returncode:
        raise SystemExit(cumulative_returncode)
    raise SystemExit(run_claim3_falsification())
