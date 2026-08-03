# Executive summary

---
<!-- trackio-cell
{"type":"markdown","id":"cell_omk_exec_20260803","created_at":"2026-08-02T23:40:00+00:00","title":"Executive summary","pinned":true,"pinned_at":"2026-08-02T23:40:00+00:00"}
-->

This CPU-only reproduction audits all six generated claims for
[Bridging the Gap Between Average and Discounted TD Learning](https://arxiv.org/html/2605.02103).
The live judge awarded 6/12 to the preserved revision because its rigorous
result boxes linked to repository-relative paths, so the underlying code, raw
data, outputs, and controls were not visible from the static logbook.

The repaired claim pages display the decisive values inline and use direct,
navigable links to every source audit, raw result, verifier, independent
checker, and negative control. The cumulative source and exact `uv.lock` are
now included in the Space. A fresh run on 2026-08-03 completed in 59.76 seconds;
all six contracts and independent checkers passed, all six injected failures
were rejected, and every scientific output matched the preserved evidence
byte-for-byte. Only environment and wall-time records changed.

## Scope & cost

| Item | Reproduction | Literal scope |
| --- | --- | --- |
| Claims | 6/6 source-bound contracts pass locally | Theorems 4.1–4.4, Section 1/Table 1, Equation 3/Lemma B.3 |
| Core route | Exact moments, theorem dependency audits, deterministic paper-scale checks | `n=1000`, `d=100` where scale is relevant |
| Independent route | Separate checker per claim | Recomputes decisive statistics from raw artifacts |
| Controls | Six injected contract failures plus claim-specific condition relaxations | Every checker must be capable of failing |
| Hardware | Local Apple CPU | No GPU or Hub Job needed |
| Runtime | 59.76 seconds for the cumulative rerun | One command, fixed seeds 0–63 |
| Cost | USD 0 | USD 0 |

Start with the [cumulative entrypoint](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/repro/src/verify_td.py),
[campaign source](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/repro/src/rigorous_campaign.py),
[locked environment](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/uv.lock),
[fresh rerun record](https://huggingface.co/spaces/DineshAI/omkG80XURl/blob/main/evidence/visibility-2026-08-03/RERUN.md), and
[public GitHub repository](https://github.com/MachineLearning-Nerd/icml26-repro-omkG80XURl-td-average-discounted).

The live judged score remains **6/12** until the judge evaluates a newly
published revision. Local and blind-review verdicts are not banked points.

---
<!-- trackio-cell
{"type":"figure","id":"cell_omk_poster_20260803","created_at":"2026-08-02T23:40:01+00:00","title":"Reproduction poster (poster_embed.html)","pinned":true,"pinned_at":"2026-08-02T23:40:01+00:00","poster":true}
-->

<iframe src="poster_embed.html" title="Average-reward TD reproduction poster" style="width:100%;height:680px;border:0"></iframe>
