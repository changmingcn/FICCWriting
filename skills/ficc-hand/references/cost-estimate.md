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
| refuter (T1) | 78 | 0.53 | 0.63 | 0.77 | red team, when triggered |
| general-purpose | 221 | 0.66 | 0.94 | 1.18 | the triage seat, data agents that must write scripts (no card; the dispatch must pass model: T1E) |

ficc-mapper is a new card with no measurements; its proxy unit prices are inferences, to be replaced with real figures after the first run. dissenter has 9 seats in agents.csv while appendix table 1 lists 8; the one-seat difference has not been traced.

T0: about 0.14M per notification turn (report section 1, item 3: 1,213 notification turns totalling 170.5M; counted per notification, about 0.13M each), with an average context of 508k at the time; with the context capped at about 300k, about 0.08M by proportion (inference). T0's own turns are counted at the same unit price.

## 2 Formula

```
estimate ≈ [Σ seats×unit price] + [T0 turns×unit price per turn], then multiply by 1.2 as the redispatch margin
T0 turns ≈ notifications (one Workflow wave counts as one) + T0's own turns (framing, thesis, acceptance, handoff, about 20–40)
```

Example: one topic, 12 sources, updating a previous version: scout 2×0.12 + triage 0.66 + digests 12×0.43 + ledger 0.69 + map 0.69 + pre-thesis counter-view 0.49 + red team 0.53 + outline 0.70 + outline check 0.49 + acceptance counter-view 0.49 + fixes 0.49 ≈ 10.6M; T0 about 40 turns × 0.08–0.14 ≈ 3–6M; total times 1.2, about 17–19M. For comparison: the research stage of 1012Six's five pieces (digester, dissenter, collator, scout) totalled about 30.0M on the main basis and 36.5M on the packet basis, about 6–7M per piece (report appendix table 1); the writing stage (ficc-writer 212.9M on the main basis, 254.2M on the packet basis; T0 195.7M on both bases) is far larger than the research stage.

## 3 Actual cost

After the run, sum the four usage categories in each agent's transcript with the weights above (method in report section 2, “口径与数据”); report the difference between estimate and actual to the user truthfully.
