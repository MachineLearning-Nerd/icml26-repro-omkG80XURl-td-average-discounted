import marimo

__generated_with = "0.23.14"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.md(r"""
    # Can a \(d^2\) curve falsify a dimension-free TD bound?

    **Answer from this audit: not here.** The proposed counterexample reports
    \(\eta_1=0.443\) at \(d=40\), but the paper's normalized-feature assumption
    forces \(\eta_1\le3/d=0.075\). The exact falsification status is
    **BLOCKED**, and the existing `TOY` verdict is preserved.

    The evidence below is embedded. Opening the notebook does not rerun the
    formal CPU experiment.
    """)
    return


@app.cell
def _(mo):
    hero = """
    <svg viewBox="0 0 760 300" xmlns="http://www.w3.org/2000/svg"
         role="img" aria-label="Peer eta1 exceeds normalized upper bound">
      <rect width="760" height="300" rx="18" fill="#f8fafc"/>
      <text x="28" y="38" font-family="sans-serif" font-size="21"
            font-weight="700" fill="#172033">Assumption check at d=40</text>
      <text x="28" y="62" font-family="sans-serif" font-size="13"
            fill="#64748b">normalized features imply η₁ ≤ 3/d</text>
      <line x1="80" y1="246" x2="710" y2="246" stroke="#94a3b8"/>
      <rect x="150" y="216" width="170" height="30" rx="7" fill="#0f9f8f"/>
      <text x="235" y="202" text-anchor="middle" font-family="sans-serif"
            font-size="17" font-weight="700" fill="#0f766e">0.075</text>
      <text x="235" y="272" text-anchor="middle" font-family="sans-serif"
            font-size="14" fill="#172033">admissible maximum</text>
      <rect x="440" y="69" width="170" height="177" rx="7" fill="#dc2626"/>
      <text x="525" y="55" text-anchor="middle" font-family="sans-serif"
            font-size="17" font-weight="700" fill="#b91c1c">0.443</text>
      <text x="525" y="272" text-anchor="middle" font-family="sans-serif"
            font-size="14" fill="#172033">peer self-report</text>
      <text x="653" y="145" text-anchor="middle" font-family="sans-serif"
            font-size="16" font-weight="700" fill="#991b1b">5.91×</text>
      <text x="653" y="165" text-anchor="middle" font-family="sans-serif"
            font-size="13" fill="#991b1b">too large</text>
    </svg>
    """
    mo.Html(hero)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## The exact contract

    Theorem 4.3 uses two independent Markov chains and
    \(\alpha_t=a/(t+c_0)^\xi\), with normalized, full-column-rank features.
    A rigorous falsification must find either:

    1. a free explicit \(d\) in Theorem 4.3 or its full Theorem D.1; or
    2. an admissible instance whose expected squared parameter error exceeds
       the fully instantiated upper bound.

    A fitted hitting-time slope is not enough when \(\eta\), norms, mixing,
    or the sufficient-\(c_0\) condition are not controlled.
    """)
    return


@app.cell
def _(mo):
    route_rows = [
        {
            "route": "Source formula",
            "observation": "No free d in Theorem 4.3 or D.1",
            "result": "no contradiction",
        },
        {
            "route": "Feasibility proof",
            "observation": "peer eta₁ exceeds 3/d by 5.91×",
            "result": "out of domain",
        },
        {
            "route": "Independent sweep",
            "observation": "64 seeds; eta₁=1/d exactly",
            "result": "non-identifying",
        },
    ]
    mo.ui.table(route_rows, selection=None, pagination=False)
    return


@app.cell
def _(mo):
    dimension_rows = [
        {"d": 5, "eta1": 0.200, "median hitting time": 206.5},
        {"d": 10, "eta1": 0.100, "median hitting time": 201.5},
        {"d": 20, "eta1": 0.050, "median hitting time": 243.0},
        {"d": 40, "eta1": 0.025, "median hitting time": 296.0},
    ]
    mo.vstack(
        [
            mo.md("## Independent Algorithm (15) reconstruction"),
            mo.ui.table(dimension_rows, selection=None, pagination=False),
            mo.md(
                r"""
                The log-log hitting-time exponent is **0.183**, versus the
                peer page's self-reported **2.015**. This divergence is not a
                proof for the theorem; it shows that the proposed effect is not
                reproduced on a clean admissible family.
                """
            ),
        ]
    )
    return


@app.cell
def _(mo):
    dimension = mo.ui.slider(
        start=5,
        stop=40,
        step=5,
        value=40,
        label="feature dimension d",
        show_value=True,
    )
    dimension
    return (dimension,)


@app.cell
def _(dimension, mo):
    d = dimension.value
    mo.md(
        rf"""
        With normalized features, every admissible \(d={d}\) instance obeys

        \[
        \eta_1 \le 3/d = \mathbf{{{3 / d:.3f}}}.
        \]

        The independent uniform-chain family is tighter:
        \(\eta_1=1/d=\mathbf{{{1 / d:.3f}}}\). Consequently,
        \(\log d=\log\eta_1^{{-1}}\); a single cross-dimensional regression
        cannot identify separate coefficients for the two.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        "\n".join(
            [
                "## Reproduce the formal evidence",
                "",
                "The fixed command ran on Hugging Face `cpu-upgrade` with no GPU:",
                "",
                "```bash",
                "uv run --frozen python repro/src/verify_td.py",
                "```",
                "",
                "Commit: `3ec797a7b78e54dcce9913d8148a019b3ffd5c98`  ",
                "Runtime: 3m32s  ",
                "Seeds: 0–63",
                "",
                "The real falsification verifier exits nonzero because no",
                "counterexample is established. An injected explicit-`d`",
                "control exits zero, so the detector recognizes contradictions.",
            ]
        )
    )
    return


@app.cell
def _(mo):
    mo.callout(
        """
        **Final evidence status: BLOCKED.** The existing Claim 3 `TOY` verdict
        remains unchanged. A future falsification needs a fully specified,
        assumption-valid instance and an executable violation of Theorem D.1.
        """,
        kind="warn",
    )
    return


if __name__ == "__main__":
    app.run()
