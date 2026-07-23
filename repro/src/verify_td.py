"""Fixed OpenResearch entrypoint for the cumulative reproduction campaign."""

from __future__ import annotations

from rigorous_campaign import run


if __name__ == "__main__":
    raise SystemExit(run())
