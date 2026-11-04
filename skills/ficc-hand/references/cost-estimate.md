# Cost estimate: unit prices, formula and sources

Unit: M = million weighted tokens. Weighted (main basis): input ×1, cache write ×1.25 (subagents, 5-minute lifetime) or ×2 (T0, 1-hour lifetime), cache read ×0.1, output ×5. Sources: （作者的用量审计报告） section 1 (total spend) and section 8 (appendix table 1). The `subagent_tokens` in a notification is the context of that agent's last turn, not spend, and must not be summed into an account (same report; comparison table （审计数据表）).

## 1 Unit price per seat (per seat, main basis)

Computed seat by seat from （审计数据表） with the weights above, then taken at percentiles (computed 2026-10-15; the raw figures of the four categories match appendix table 1: digester total 21.4M, collator 3.1M, scout 1.6M).

| Seat | Seats in 1012Six | Median | p75 | p90 | Used in this skill for |
|---|---|---|---|---|---|
| scout (T3) | 13 | 0.12 | 0.15 | 0.17 | pulling originals, data agents that run existing scripts |
| digester | 48 | 0.43 | 0.56 | 0.62 | digests, one seat per source |
| collator | 5 | 0.69 | 0.72 | 0.76 | the ledger (`ledger.md`); also the proxy unit price for mapper map mode |
| ficc-outliner | 17 | 0.49 | 0.70 | 0.98 | outline check; p75 is the proxy unit price for the outliner building the tree (FICCHand step 5b), the median for mapper fix mode |
| dissenter (T1) | 9 | 0.49 | 0.53 | 0.59 | counter-view before the thesis, counter-view at acceptance |
| refuter (T1) | 78 | 0.53 | 0.63 | 0.77 | red team, when triggered (dispatched as `refuter-t1e`, T1E, since 2026-10-28; this T1 measurement is its proxy unit price) |
| general-purpose | 221 | 0.66 | 0.94 | 1.18 | the triage seat, data agents that must write scripts (no card; the dispatch must pass model: T1E) |

ficc-mapper is a new card with no measurements; its proxy unit prices are inferences, to be replaced with real figures after the first run. dissenter has 9 seats in agents.csv while appendix table 1 lists 8; the one-seat difference has not been traced.

T0: about 0.14M per notification turn (report section 1, item 3: 1,213 notification turns totalling 170.5M; counted per notification, about 0.13M each), with an average context of 508k at the time; with the context capped at about 300k, about 0.08M by proportion (inference). T0's own turns are counted at the same unit price.

T0 at long context (2026-11-02): when T0 is expected to run past about 300k context, count it separately. Each turn re-reads its context at the cache-read weight: T0 ≈ expected turns × expected mean context × 0.1, plus about a quarter for cache writes and output. A turn is one T0 assistant message (the ledger's `t0_turns.csv`); expect about 3 per seat dispatched, plus T0's own turns. Measured on 1101AIFinance: 568 turns for 173 seats, mean context 564,510, cache read 31.7M of T0's 39.8M.

## 2 Formula

```
estimate ≈ [Σ seats×unit price] + [T0 turns×unit price per turn], then multiply by 1.2 as the redispatch margin
T0 turns ≈ notifications (one Workflow wave counts as one) + T0's own turns (framing, thesis, acceptance, handoff, about 20–40)
```

Example: one topic, 12 sources, updating a previous version: scout 2×0.12 + triage 0.66 + digests 12×0.43 + ledger 0.69 + map 0.69 + pre-thesis counter-view 0.49 + red team 0.53 + outline 0.70 + outline check 0.49 + acceptance counter-view 0.49 + fixes 0.49 ≈ 10.6M; T0 about 40 turns × 0.08–0.14 ≈ 3–6M; total times 1.2, about 17–19M. For comparison: the research stage of 1012Six's five pieces (digester, dissenter, collator, scout) totalled about 30.0M on the main basis and 36.5M on the packet basis, about 6–7M per piece (report appendix table 1); the writing stage (ficc-writer 212.9M on the main basis, 254.2M on the packet basis; T0 195.7M on both bases) is far larger than the research stage.

Update of a previous version (2026-11-02): never price the writing stage as “only the affected nodes”. Measure the change with `shared-protocols/scripts/sentence_diff.py NEW OLD` first: at framing, on the line's last update (its final against the version before); once the first frozen draft exists, on that draft against the previous final, then re-estimate the remaining stages. Changed CJK ≈ the `<0.8` share (rewritten or new) × the expected final CJK (`shared-protocols/scripts/cjk_count.py`). Price the report at 3.0–4.7M per 1,000 changed CJK (seats plus T0 per 1,000 final CJK of six earlier full-flow reports, the 1101 audit's comparison: Oil 4.67, Oil R3 4.10, Euro 4.51, Japan 3.78, 1025 govt 3.77, 1025 overseas 3.02), then multiply by 1.2. Engineering bundled into the task is priced on its own (better: its own task).

Example, 1101AIFinance (2026-11-01): estimated 60–90M (research 31M with T0 at 60 turns × 0.14; writing 30–60M as “only the affected nodes”); actual 283.5M (T0 39.8M, seats 243.8M, of which 66.6M was pilot engineering bundled into the task). Reasons: volume (final 112,110 CJK, 1.4 times the 1025 version it updated; against it any change 77,520, `<0.8` 55,996, `<0.6` 45,648) and the bundled pilot. Under the two rules: 55,996 (the `<0.8` share, 49.9%) to 61,661 (55%) changed CJK × 3.0–4.7M × 1.2 ≈ 202–348M; T0 alone 568 turns × 564,510 × 0.1 × 1.25 ≈ 40M.

## 3 Actual cost

After the run, sum the four usage categories in each agent's transcript with the weights above (method in report section 2, “口径与数据”); report the difference between estimate and actual to the user truthfully.

Ledger (2026-11-02): `python3 first-secretary/scripts/build_ledger.py <session_id> --out <task dir>/results/cost/` (under the skills root; several ids for a task across sessions, or none to read work.json `session_ids`). It weights T0's cache writes ×1.25 like every seat (the audit basis; on 1101 the ×2 basis adds 2.7M). Settle with the cost line: `work.py settle … --cost "估算=…;实际=…;比值=…;原因=…"` (`n/a;原因=…` when there is no estimate or no ledger); 比值 is a number or a range of two (anything else is refused), must lie within 5% of 实际/估算 when both are amounts (M, K, B, MM, bn, 万, 亿 or a plain token count; a number without a unit is tokens), and above 1.3 (the computed value when there is one) is marked 复查.
