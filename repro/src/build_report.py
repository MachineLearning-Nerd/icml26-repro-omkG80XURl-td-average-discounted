"""Build dependency-free SVG figures from the frozen winning artifacts."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / ".openresearch" / "artifacts" / "winning_run"
OUT = ROOT / "reports" / "rigorous-reproduction" / "images"
INK = "#172033"
MUTED = "#64748b"
GRID = "#dbe3ee"
BLUE = "#2563eb"
TEAL = "#0f9f8f"
AMBER = "#d97706"
RED = "#dc2626"


def _svg(body: str, title: str, subtitle: str = "") -> str:
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="900" height="500" '
        'viewBox="0 0 900 500" role="img">\n'
        f"<title>{escape(title)}</title>\n"
        "<rect width=\"900\" height=\"500\" fill=\"#ffffff\" rx=\"18\"/>\n"
        f'<text x="52" y="52" font-family="Inter,Arial,sans-serif" '
        f'font-size="25" font-weight="700" fill="{INK}">{escape(title)}</text>\n'
        f'<text x="52" y="78" font-family="Inter,Arial,sans-serif" '
        f'font-size="14" fill="{MUTED}">{escape(subtitle)}</text>\n'
        f"{body}\n</svg>\n"
    )


def _text(x: float, y: float, value: str, size: int = 13, color: str = INK, anchor: str = "start", weight: int = 400) -> str:
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" '
        f'font-family="Inter,Arial,sans-serif" font-size="{size}" '
        f'font-weight="{weight}" fill="{color}">{escape(value)}</text>'
    )


def headline() -> str:
    c1 = json.loads((DATA / "claim_1" / "summary.json").read_text())
    c2 = json.loads((DATA / "claim_2" / "summary.json").read_text())
    groups = [
        ("i.i.d. T", -1.0, c1["regression"]["T_exponent"]),
        ("Markov T", -1.0, c2["regression"]["T_exponent"]),
        ("Markov η", -2.0, c2["regression"]["eta_exponent"]),
    ]
    body = []
    x0, y0, width, height = 100, 120, 720, 285
    body.append(f'<line x1="{x0}" y1="{y0+height}" x2="{x0+width}" y2="{y0+height}" stroke="{INK}" stroke-width="1.5"/>')
    for tick in (0, 0.5, 1.0, 1.5, 2.0, 2.5):
        y = y0 + height - tick / 2.5 * height
        body.append(f'<line x1="{x0}" y1="{y:.1f}" x2="{x0+width}" y2="{y:.1f}" stroke="{GRID}" stroke-width="1"/>')
        body.append(_text(x0 - 12, y + 5, f"−{tick:g}" if tick else "0", anchor="end", color=MUTED))
    for i, (label, target, observed) in enumerate(groups):
        center = x0 + 130 + i * 235
        for offset, value, color, name in (
            (-38, abs(target), MUTED, "paper"),
            (38, abs(observed), BLUE if i < 2 else TEAL, "observed"),
        ):
            h = value / 2.5 * height
            body.append(
                f'<rect x="{center+offset-27:.1f}" y="{y0+height-h:.1f}" '
                f'width="54" height="{h:.1f}" rx="7" fill="{color}"/>'
            )
            body.append(_text(center + offset, y0 + height - h - 10, f"−{value:.3f}", anchor="middle", weight=700, color=color))
        body.append(_text(center, y0 + height + 30, label, anchor="middle", weight=600))
    body.append(f'<rect x="545" y="92" width="14" height="14" rx="3" fill="{MUTED}"/>')
    body.append(_text(567, 104, "paper exponent", size=12, color=MUTED))
    body.append(f'<rect x="675" y="92" width="14" height="14" rx="3" fill="{BLUE}"/>')
    body.append(_text(697, 104, "observed", size=12, color=MUTED))
    return _svg(
        "\n".join(body),
        "Rate exponents land on the theorem’s scaling",
        "Exact moments; logarithmic and explicit mixing factors removed as specified",
    )


def paper_scale() -> str:
    with (DATA / "claim_2" / "raw_paper_scale.csv").open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    rows = [row for row in rows if row["sampling"] == "markov"]
    body = []
    x0, y0, width, height = 105, 115, 620, 285
    body.append(f'<line x1="{x0}" y1="{y0+height}" x2="{x0+width}" y2="{y0+height}" stroke="{INK}"/>')
    body.append(f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0+height}" stroke="{INK}"/>')
    for tick in (0.0, 0.15, 0.30, 0.45, 0.60):
        y = y0 + height - tick / 0.60 * height
        body.append(f'<line x1="{x0}" y1="{y:.1f}" x2="{x0+width}" y2="{y:.1f}" stroke="{GRID}"/>')
        body.append(_text(x0 - 12, y + 5, f"{tick:.2f}", anchor="end", color=MUTED))
    checkpoints = [15000, 50000, 150000]
    x_for = {t: x0 + i * width / 2 for i, t in enumerate(checkpoints)}
    for t in checkpoints:
        body.append(_text(x_for[t], y0 + height + 28, f"{t//1000}k", anchor="middle", color=MUTED))
    for (n, d), color in [((50, 5), BLUE), ((100, 20), TEAL), ((1000, 100), AMBER)]:
        subset = [r for r in rows if int(r["n"]) == n and int(r["d"]) == d]
        points = [
            (x_for[int(r["T"])], y0 + height - float(r["value_rmse"]) / 0.60 * height)
            for r in subset
        ]
        body.append(
            f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x,y in points)}" '
            f'fill="none" stroke="{color}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'
        )
        for x, y in points:
            body.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="{color}" stroke="white" stroke-width="2"/>')
        label_offset = {50: 12, 100: -8, 1000: -8}[n]
        body.append(
            _text(
                720,
                points[-1][1] + label_offset,
                f"n={n}, d={d}",
                color=color,
                weight=700,
                anchor="end",
            )
        )
    body.append(_text(72, 108, "value RMSE", color=MUTED))
    body.append(_text(455, 465, "updates", anchor="middle", color=MUTED))
    return _svg(
        "\n".join(body),
        "Paper-scale error falls through n=1000, d=100",
        "Two stationary Markov chains; six deterministic replicates per task",
    )


def condition_comparison() -> str:
    labels = [("new average", 2, BLUE), ("prior average", 4, RED), ("discounted", 2, TEAL)]
    body = []
    x0, y0, height = 135, 120, 280
    for tick in range(5):
        y = y0 + height - tick / 4 * height
        body.append(f'<line x1="{x0}" y1="{y}" x2="805" y2="{y}" stroke="{GRID}"/>')
        body.append(_text(x0 - 14, y + 5, str(tick), anchor="end", color=MUTED))
    for i, (label, power, color) in enumerate(labels):
        x = x0 + 90 + i * 210
        h = power / 4 * height
        body.append(f'<rect x="{x-45}" y="{y0+height-h}" width="90" height="{h}" rx="10" fill="{color}"/>')
        body.append(_text(x, y0 + height - h - 12, f"inverse power {power}", anchor="middle", weight=700, color=color))
        body.append(_text(x, y0 + height + 28, label, anchor="middle", weight=600))
    body.append(_text(450, 458, "Primary sources use distinct condition-number definitions; bars compare powers, not raw values.", anchor="middle", color=MUTED))
    return _svg(
        "\n".join(body),
        "Quadratic average-reward dependence matches discounted TD",
        "New theorem and SHA-pinned primary-source denominator audit",
    )


def single_chain_flow() -> str:
    boxes = [
        (40, "Rθ", "η′⁻¹ᐟ²"),
        (190, "λ²", "η′¹ᐟ² η"),
        (340, "Gconst", "η′⁻¹ η⁻¹"),
        (490, "α / ζ", "η⁻² T⁻¹"),
        (640, "error", "η′⁻¹ η⁻³ T⁻¹"),
    ]
    body = []
    for i, (x, name, value) in enumerate(boxes):
        body.append(f'<rect x="{x}" y="170" width="115" height="105" rx="14" fill="#f8fafc" stroke="{BLUE}" stroke-width="2"/>')
        body.append(_text(x + 57.5, 207, name, anchor="middle", weight=700, color=BLUE))
        body.append(_text(x + 57.5, 243, value, anchor="middle", size=14, weight=700))
        if i < len(boxes) - 1:
            body.append(f'<line x1="{x+115}" y1="222" x2="{boxes[i+1][0]-10}" y2="222" stroke="{MUTED}" stroke-width="2"/>')
            body.append(f'<path d="M {boxes[i+1][0]-10} 222 l -9 -6 l 0 12 z" fill="{MUTED}"/>')
    body.append(f'<rect x="267" y="330" width="366" height="70" rx="14" fill="#ecfdf5" stroke="{TEAL}" stroke-width="2"/>')
    body.append(_text(450, 357, "common regime η′ = Θ(η)", anchor="middle", weight=700, color=TEAL))
    body.append(_text(450, 384, "η⁻⁴ T⁻¹", anchor="middle", size=22, weight=700, color=TEAL))
    return _svg(
        "\n".join(body),
        "Why the single-chain theorem becomes quartic",
        "The η′ factor is essential; omitting it is the failing negative control",
    )


def lemma_stress() -> str:
    with (DATA / "claim_6" / "raw_condition_stress.csv").open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    logs = [
        math.log10(max(float(row["eta1"]) / (0.5 * float(row["eta3"])), 1e-12))
        for row in rows
    ]
    top = max(logs) * 1.05
    body = []
    x0, y0, width, height = 100, 115, 650, 285
    body.append(f'<line x1="{x0}" y1="{y0+height}" x2="{x0+width}" y2="{y0+height}" stroke="{RED}" stroke-width="2"/>')
    body.append(_text(735, y0 + height - 8, "lemma boundary: ratio = 1", anchor="end", color=RED))
    for i, (row, value) in enumerate(zip(rows, logs)):
        x = x0 + i / (len(rows) - 1) * width
        y = y0 + height - value / top * height
        color = TEAL if row["family"] == "paper_scale_cycle_teleport" else BLUE
        if row["family"] == "tight_tabular":
            color = AMBER
        body.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.5" fill="{color}" opacity="0.82"/>')
    body.append(_text(72, 108, "log₁₀[η₁/(η₃/2)]", color=MUTED))
    body.append(_text(460, 458, "48 deterministic stress cases", anchor="middle", color=MUTED))
    body.append(f'<circle cx="585" cy="96" r="5" fill="{TEAL}"/>')
    body.append(_text(598, 101, "paper-scale", size=12, color=MUTED))
    body.append(f'<circle cx="690" cy="96" r="5" fill="{AMBER}"/>')
    body.append(_text(703, 101, "tight control", size=12, color=MUTED))
    return _svg(
        "\n".join(body),
        "Every stress case stays above the η₁ ≥ η₃/2 boundary",
        "Dense nonreversible chains, paper-scale dimensions, and a tight tabular control",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    figures = {
        "headline_rate.svg": headline(),
        "paper_scale.svg": paper_scale(),
        "condition_comparison.svg": condition_comparison(),
        "single_chain_flow.svg": single_chain_flow(),
        "lemma_stress.svg": lemma_stress(),
    }
    for name, content in figures.items():
        (OUT / name).write_text(content)
    print(json.dumps({"figures": sorted(figures), "output": str(OUT)}, indent=2))


if __name__ == "__main__":
    main()
