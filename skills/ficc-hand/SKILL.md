---
name: ficc-hand
description: "Use for a FICC or macro topic with a large corpus needing a research report: screen material, form views, deliver a view outline; prose goes to ficc-voice. Keywords: 专题研究报告, 主线支线, 脉络, 组织材料, 协助决策, 给题目和语料, 更新上一版判断, 宏观题目, 语料, 研报库, 旧稿, 观点提纲. Not for: 月报短文, 问答取数, 改写已成的文章."
---

# ficc-hand

T0's router. A run is a research-agent Investigation plus a FICC delta: T0 loads research-agent `SKILL.md` and `FICCHand.md`, and a gate's reference only when producing its artifact. Seats read their card and the reference their packet names, never FICCHand.md.

Does: deliver `<文稿名>-提纲.md` (view tree, `~/.claude/skills/ficc-voice/FICCOutline.md` format) and `<文稿名>-资料索引.md` (pointers, `references/materials-manifest.md`), with the handoff card at the index head (`references/handoff.md`). Roles: the trunk question governs, explicit must-answers keep their delivery duty, leads owe no answer (FICCHand.md 3.1 ⑥).

Does not: write body text, run body-text acceptance, deliver articles or sweep-edit (ficc-voice); add gates (research-agent), corpus retrieval (ficc-research-kit), task records (first-secretary), dispatch rules (dynamic-workflow).

| Step | Seat | FICCHand.md |
|---|---|---|
| 0 Framing | T0 | 3.1 |
| 1 Corpus inventory | T0, scout, triage seat | 3.2 |
| 2 Digests | digester per source | 3.3 |
| 3 Map | collator, ficc-mapper (map) | 3.4 |
| 4 Thesis and counter-view | T0, dissenter | 3.5 |
| 5a Index / 5b Outline | ficc-mapper (index) / ficc-outliner (build) | 3.6 |
| 6 Acceptance | ficc-outliner (check), `scripts/tieout.py` | 3.7 |
| 7 Handoff | T0, then a fresh `ficc-conductor` per writing-phase wave (relay, check wave, close), each started from the card and `conductor-progress.md` | 3.8 |

Cards: `~/.claude/agents/ficc-mapper.md` (map, index, index fixes), `ficc-outliner.md` (build, check, fix). Script: `scripts/tieout.py` (outline numbers, dates and institutions found in the index or ledger; `--self-test` must PASS). After handoff a changed view changes the tree in ficc-voice; this skill is not rerun. Rollback is git. The user's request and CLAUDE.md outrank this skill; where research-agent or ficc-voice differ, the rule's home wins.
