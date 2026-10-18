# FICCHand: from topic and corpus to view outline and materials index

Only T0 reads this file. Current division of labor: FICCHand screens material and forms views, and delivers the view tree built by ficc-outliner and the materials index made by ficc-mapper (ficc-mapper also makes the map and revises the index). Placement goes to ficc-outliner, relations to ficc-structurer, wording to ficc-writer. This skill stops at handoff: ficc-outliner builds the tree and settles positions at step 5b, and writes only order lines. Relation lines wait for ficc-voice's relation sheet; this skill writes no relation types or annotation lines and does not settle wording. Body text, its acceptance and delivery, and sweep edits are all in ficc-voice. How the division of labor was settled (the user's original words of 2026-10-15 and the two changes of 2026-10-17): see `references/hand-history.md` “附 分工沿革（2026-10-15、2026-10-17）”.

Where a rule has a home, write only a pointer (file + section) and do not restate it; this file covers only what has no home elsewhere: what a research report for decisions must answer, what each of the eight steps delivers, and the map. The cost narrative and the lessons left by 1012Six are in `references/hand-history.md`. Language: SKILL.md, the cards, this file and the references are in English; Chinese stays only for trigger words, literal output tokens, term mappings and quoted Chinese content. The record file `references/hand-history.md` stays in Chinese.

## 1 Purpose and deliverables

### 1.1 A research report that supports decisions

Readers make decisions with it, so answer the question first, then give the grounds and the circumstances in which the answer would be wrong. Where each item the report must answer goes in the outline and in the index: see the mapping table in 4.

### 1.2 Deliverables

Two files, written in the task directory (`T/`) and posted in the conversation; upload to Drive only when the user asks (the outline is working material, FICCOutline 4.2). When ficc-voice starts drafting, it places the outline beside the draft per its own convention (ficc-voice/SKILL.md 1):

1. `<文稿名>-提纲.md`: the view tree, format per FICCOutline 4.2: header, name table, root claim, the four things of each node, 〔标题〕 (heading) lines, the source-list node; the tree unfolds to paragraph groups (FICCOutline 4.1 step 5, 3.4), with order lines only; relation lines wait for ficc-voice's relation sheet, see `references/outline-from-research.md`.
2. `<文稿名>-资料索引.md`: the index of main materials and data, pointers only (path:line, data series id), no copying of the original; fields in `references/materials-manifest.md`; its head is the handoff note, see `references/handoff.md`.

Working files (Frame, inventory, digests, the ledger (`ledger.md`), check table, map, thesis, dissent map, cache) stay in the research-state directory (research-agent/references/framing.md (Research-state scaffolding)); the index points to them and does not copy them.

### 1.3 When not to use it

Monthly short pieces must be quick and short and are posted directly in the conversation; they do not go through this skill (memory `feedback-monthly-short-pieces.md`; genre scaling in FICCOutline 7.1). Q&A and data lookups go to research-agent's Lookup or Brief (research-agent/SKILL.md (Route first)). A finished article that needs only a style-only edit or conversion to written register goes to ficc-voice. This skill follows research-agent's Investigation route.

## 2 Division of labor

T0 only clarifies, decomposes, dispatches and accepts; forming the views (the thesis) is T0's synthesis; everything else is dispatched (shared-protocols/model-tiers.md (Tiers; T0 in-session)).

| Step | Who | Tier | Skill loaded at this step |
|---|---|---|---|
| 0 Framing | T0 | T0 | task record (CLAUDE.md task contract, first-secretary/SKILL.md (The work record)); research-agent GATE 1 |
| 1 Corpus inventory | T0 runs `ficc.py stat/find`; scout pulls originals; one triage seat (general-purpose, pass T1E); data: one agent per source (scout or general-purpose) | T3/T1E | ficc-research-kit (GATE 2) |
| 2 Digests | digester, one seat per source | T1E | research-agent GATE 2 |
| 3 Map | collator builds the ledger; ficc-mapper fills the map | T1E | research-agent GATE 3 |
| 4 Thesis and counter-views | T0 forms the thesis; dissenter; refuter when triggered | T0/T1 | research-agent GATE 3, GATE 4 red team |
| 5a Materials index | ficc-mapper in index mode builds the materials index | T1E | none (the card reads only `references/materials-manifest.md`) |
| 5b Outline | ficc-outliner builds the tree (reads FICCOutline.md in full plus `references/outline-from-research.md`) | T1E | none |
| 6 Acceptance | ficc-outliner check mode; `scripts/tieout.py`; dissenter; outline findings go to ficc-outliner (rule/maintain) to fix, index findings to ficc-mapper fix mode | T1E/script/T1 | none |
| 7 Handoff | T0 | T0 | ficc-voice relay, taking over at relay-table step ③; the finished draft passes through ④⑤ (`references/handoff.md` 3) |

Dispatch, caps and Workflow: dynamic-workflow/SKILL.md (Packets and files; Hard lines).

## 3 Process

Each step states: input, action (who), products (fixed file names; `R/` = research-state directory, which is the line's `research/` when there is a work line, otherwise the task directory's `research/`; `T/` = task directory), done condition. Each step's cost control and the errors made in 1012Six are in `references/hand-history.md` section 3.

### 3.1 Framing

- Input: the user's original words, the topic, the corpus scope; when there is a previous version, the old draft and the rows of the register `SUPERSEDED.md` that bear on this topic. Treat an old draft without a sentence-by-sentence check table as unchecked notes, and give its heading-level judgments a second read against the originals (shared-protocols/source-check.md (Documents written from notes; Register)). Old drafts on adjacent topics (not the previous version) are also used as sources as unchecked notes; they go into the inventory and the S table of the materials index, and their register rows go with the packet.
- Action (who): T0; `work.py define` and reporting per the CLAUDE.md task contract.
- Products: `R/brief.md`, written and frozen before any new original is opened (research-agent/references/framing.md (The Frame block)); `T/成本估算.md`.
- Done when: beyond the Frame, five things are written out. ① Decision question: the decision to serve, in the user's original words; for an update topic, write it as “旧版哪几条判断被推翻就改标题、导语和对应章节” (which judgments of the old version, once overturned, change the title, the lead and the corresponding sections), and set the sub-questions one by one against the old version's judgments. Rewrite a predictive question (“会不会转为走阔”) as a conditional one: what state things are in now, under what conditions that would change, and which of those conditions are already visible; the root claim answers this conditional judgment. ② The subject of the answer: when the question asks about “变化和深远意义”, make the subject the composition, the holders and the channels, not the total. ③ Fund flow first: every judgment must translate into who is forced to buy or sell, where the money goes from and to, whether it gets through, and who the marginal price-setter is; a total-to-total inference first passes the distribution and transmission check (memory `user-flow-first-framework.md`, `segmentation-friction-axiom.md`). ④ Fix the time window and data cutoff date in writing, and whether this pass may add new facts, new numbers, new sources. ⑤ Analysis only, no prediction: looking ahead, write only watch items and conditions that would change the judgment; without a mandate, write no trading advice (memory `macro-analysis-not-prediction.md`; FICCOutline 2.1). Show the user the rough cost estimate (`references/cost-estimate.md`) before dispatching the first seat, run once the user agrees, and report the actual figures truthfully after the run.

### 3.2 Corpus inventory

- Input: `R/brief.md`.
- Action (who): T0 runs `ficc.py stat` and `find` in the session; pulling originals is dispatched to one T3 scout; one triage seat: general-purpose (no card, the packet passes the T1E model) or the collator card, which reads cand.tsv and the brief and produces the inventory; data, one agent per source: dispatch scout (T3) to run an existing script, general-purpose (T1E) when a script must be written; the products are `R/cache/<序列>.csv` and one `T/results/D-Q<编号>.md` (series name, source, measurement basis, unit, vintage, latest point, next release date), for the Q table of the index that the mapper builds (ficc-research-kit/SKILL.md (Load order; Data-source routing (first choice order))).
- Products: `R/inventory.md` (candidates, triage, pivotal 10–15 documents, skim at most 15, discarded ones counted by reason; the date column marked “(filename)”, the body date confirmed by the digest seat); `R/cand.tsv`; `原件/` (with PDF twins, for taking figures); `R/cache/` (rerunnable fetch scripts and caches, research-agent/references/collection.md (Cache every pull; search both directions)).
- Done when: the candidates are the union of title/tag queries and body scans; for a cross-cutting topic, scan the whole library, add a subject constraint when selecting documents, and remove near-duplicates (ficc-research-kit/references/topic-playbook.md (Selection rules)); the search-term list gets an added category “制度与监管变化” (institutional and regulatory changes: rule revisions, exemption letters, accounting standards, filings); where a primary source can be fetched, do not wait for an investment bank's citation of it; the old version's source chain also goes into the inventory; for a missing document, establish the reason first, then write it into the gaps; a guide is an index, not evidence.
- Do not read the research library over SMB; use ficc-research-kit's fast path.

### 3.3 Digests

- Input: one original or its cache; the register rows related to it; the views being formed, and when there is a previous version, the old version's judgments, so that COUNTER-CASE attacks them directly.
- Action (who): digester (T1E), one seat per source.
- Products: `T/results/D-<编号>.md`, per research-agent/references/digest-template.md, plus `references/digest-extra-fields.md` (T0 pastes it, together with ficc-research-kit's `PACKET-STANZA.md`, into every digest packet).
- Done when: every load-bearing figure records the extra fields in full, once; when all are in, T0 counts which of them changed the old version's conclusions.
- Homogeneous fan-out (one seat per source) runs each wave as one dynamic-workflow Workflow, one notification per wave.

### 3.4 Map

- Input: the digest directory, `R/brief.md`, register rows.
- Action (who): collator (T1E), then ficc-mapper (T1E, map mode); T0 only spot-checks the landing figures.
- Products: `R/ledger.md` (built by collator, research-agent/references/analysis.md §1; fact rows and conflict rows kept apart, conflicts go to T0; the tier scale is in research-agent/references/digest-template.md (the `tier:` field of FACTS in the template), and the ledger no longer defines its own scale); `R/checks.md` (T0 opens the original at that line to check the landing figures, decides which originals to open by the load-bearing judgments still unverified, sets no cap on the number of documents, and checks only the figures the root and the trunk will use: 数字｜原件位置｜结果, ficc-research-kit/references/topic-playbook.md (Stage 2: Digest interpretation)); `R/脉络图.md` (filled by ficc-mapper per `references/map-template.md`, elements in 4).
- Done when: each of the map's eleven elements has content or states “缺”; every item is anchored to a digest row; conflicts, mismatched measurement bases, confusables and gaps are all marked.
- When ficc-mapper goes back to the originals, it opens only the lines that a dispute, a doubtful figure or a missing field points to; see the ficc-mapper card.

### 3.5 Thesis and counter-views

- Input: the map, read in full; the ledger, opening only the rows the map's anchors point to; `R/checks.md`.
- Action (who): T0 forms the thesis (research-agent/references/analysis.md §2, §4, §6); dissenter (T1, tier pinned by its card, do not pass model) takes its seat after the first wave of digests is saved and before synthesis (research-agent/references/collection.md (Dissent seat)); when research-agent/references/delivery.md §1 triggers, refuter attacks the top three judgments under the root. Weigh per FICCOutline 6.1, 6.2: give the strongest reason first; if it overturns the trunk, change the trunk.
- Products: `R/立论.md` (written by T0: the main judgments in three layers: judgment, point-by-point evidence (each point with date, source, measurement basis), confidence and the link that limits it; which judgments are adopted throughout and which serve only as contrast; the strength of each judgment set once and used throughout; when rewritten after checking, state which version it replaces); `R/dissent-map.md` (research-agent/references/analysis.md §3); register rows (shared-protocols/source-check.md (Register), `supersede.py`).
- Done when: every main judgment passes six heading-level checks: time window (whether the facts hold over the period the judgment speaks of); when a model gives a range, write the range and name the model, and do not treat the upper bound as a finding; do not write an inference as a source; do not generalize one house's sample to the whole; do not turn what the material does not say into a denial; a conclusion uses only evidence of the same category (sentiment, activity and fund flows kept apart). For a partially adopted objection: report the better-fitting measure alongside the standard measure, and list the opponent's reading as a parallel hypothesis with a discriminating reading. A reversal the counter-view raises from the digests alone counts only as a lead; it enters the register only after the original is opened and confirms it. Close at saturation (research-agent/references/analysis.md §9). When a default that T0 set itself would affect many nodes or sentences, ask the user in one sentence before dispatching, or first try it in one place.

### 3.6 Outline and materials index

- Input: `R/立论.md`, the map, the ledger, register rows, `references/report-skeleton.md`, `references/materials-manifest.md`.
- Action (who): 5a ficc-mapper (T1E, index mode) builds the materials index per `references/materials-manifest.md`; 5b ficc-outliner (T1E) builds the tree, reading FICCOutline.md in full plus `references/outline-from-research.md`, with the thesis, the map, the ledger, register rows, the materials index and `references/report-skeleton.md` as input (user 2026-10-17: only ficc-outliner builds the tree).
- Products: `T/<文稿名>-资料索引.md` (5a), `T/<文稿名>-提纲.md` (5b).
- Done when: the outline header follows FICCOutline 2.1, the name table and nodes follow 4.2, 〔标题〕 follows 8.2; the root claim answers the decision question; the name table comes from the confusables table; each node notes the register rows' now; text the user wrote or settled sentence by sentence is marked 〔作者亲写·逐字〕 (FICCOutline 7.3); the order line writes the ordering reason, in terms of the specific content of the two adjacent blocks, and says so where the two could swap (FICCOutline 3.1); relation lines stay empty until ficc-voice's relation sheet, and relation types and annotation lines belong to FICCStructure; the tree unfolds to paragraph groups (FICCOutline 4.1 step 5, 3.4), each node has the four things, nodes near the leaves are written combined per FICCOutline 4.2, and each leaf writes the index ids it uses; a disagreement T0 has not ruled is written per FICCOutline 3.2 with the state of the disagreement as the claim, and is also listed among the open questions; write no body-text sentences. Settle on the outline everything that can be settled there: the choice of measurement bases and indicators, data windows, the name table, the change worksheet. Mark droppable nodes: the written text runs 30% to 50% longer than the outline, and deleting repetition trims only 10%, so a short piece needs its cuts made on the outline. The index has one row per load-bearing figure and per judgment, with an anchor.

### 3.7 Acceptance

- Input: the outline, the materials index, the ledger, the digest directory.
- Action (who), one parallel wave: ① ficc-outliner in check mode checks the outline per FICCOutline 9, reports only and does not edit (per its card it reads FICCOutline through once); ② `python3 ~/.claude/skills/ficc-hand/scripts/tieout.py --outline <提纲> --against <资料索引> <账本>`: every number, date and English institution name in the outline's claims, 〔标题〕 lines and name table must be found in the index or the ledger; ③ dissenter (T1) attacks the root claim and the trunk claims, targeting the six checks of 3.5 and degree words; T0's thesis is attacked just as the mapper's wording is; its input is only the outline, the index and the digests, not T0's narrative (shared-protocols/context-economy.md (Fork and seats)); each finding is marked “本轮引入” (introduced this round) or “旧稿已有” (pre-existing) (definitions in `~/.claude/agents/refuter.md`, `dissenter.md`). Outline findings (the outline-check results, tieout misses on claims and 〔标题〕 lines, the counter-view's comments on claims) go to ficc-outliner (rule/maintain mode) to fix, index findings to ficc-mapper fix mode (index only); one round each, then rerun tieout.
- Products: `T/results/查提纲.md`, `T/results/tieout.txt`, `T/results/X-lead.md`; the revised outline and index.
- Done when: the outline check finds no fault that affects writing; tieout misses are zero, or each has T0's disposition; each counter-view point is judged adopted, partially adopted or not adopted, with one line of discriminating evidence. Review rounds: first-secretary's GATE-REV-02. A task of this skill counts as complete by the five items below (Codex 2026-10-17 audit, section 8); T0's acceptance checks them one by one:
  1. Selection: which material is adopted and which discarded, with reasons that fit the decision question; important gaps stay in the gap table and in section 8 of the index, and do not disappear because the tables are full.
  2. Traceable: every main judgment has evidence anchors, and its subject, indicator, period, unit, condition and strength match; disagreements between houses are not hidden by merged wording.
  3. Distinguishable: source wording, research synthesis and inferences still to be verified (“我们推断”) can be told apart at a glance in the outline and the index.
  4. Ready for the next stage: the outline and the index can be read directly by the next stage (the outline check has passed); the tieout result states which lines and which name table it checked, and zero coverage does not count as a pass; tieout checks tokens only, and whether the meaning is right is judged by the outline check and the counter-view seat.
  5. Handoff: the handoff note states what is settled and what is not, the open questions and the nodes they affect, and continues or ends per the user's final goal (the exit in 3.8).
- T0 takes only the verdict lines of the three results (suspended, user 2026-10-15: the restriction on T0 is suspended); while it is suspended, T0 reads the three results as needed.

### 3.8 Handoff

- Input: the accepted outline and index.
- Action (who): T0.
- Products: the handoff note at the head of the index (`references/handoff.md`); the outline and the index posted in the conversation (FICCOutline 4.2: post first, by default do not wait for approval); settlement per the exit (see “Exit” below).
- Done when: per `references/handoff.md` section 2. The handoff contains the outline, the materials index, the rulings in force, the open items and the acceptance record.
- Exit: choose one of two per the task's acceptance items (`work.py define`). ① The user wants only the research outline: `work.py settle` after verifying delivery. ② The user wants a finished draft: this skill completes only the research stage; record “研究阶段已完成” in the task record, do not settle, and continue along the original task goal into step 3 of the ficc-voice relay table (the finished draft passes through steps 4 and 5, `references/handoff.md` 3); settle after the finished draft is delivered (first-secretary/references/control-policy.md (WORK-01)).
- After handoff: when new material or a user correction changes a judgment, change the tree first (`references/handoff.md` 4); reopen the affected evidence and conclusion checks per shared-protocols/source-check.md (Validity of a check; Reread on a changed binding); do not change only the table of contents and the wording, do not build a separate process, and do not come back to rerun this skill.

## 4 Map

The map is the picture between the digests and the outline: first lay the material out as a structure, then T0 forms the thesis from the structure. Eleven elements; how to fill them, their columns and each item's checks are in `references/map-template.md`, and ficc-mapper fills them per that file. The table below matches the elements to the items a decision report must answer (readers make decisions with it, so answer the question first, then give the grounds and the circumstances in which the answer would be wrong); each item must have a place to land in the outline or the index. The outline delivers views only; how the body text is written belongs to ficc-voice.

| Element | In one sentence | What the report must answer | Into the outline | Into the index |
|---|---|---|---|---|
| 1 Question tree (问题树) | the spine of sub-questions hangs under the root, with main line, branch lines and layers; revise the spine once evidence comes in | the decision question, answer first; main line, branch lines and layers | the outline header states the decision question; the root claim is the judgment on it, placed at the start of the lead (FICCOutline 8.1); order and layering of the root and the trunk: trunk nodes are the steps of the main line, and a branch line hangs under the step it serves; the ordering reason in the order line | head: decision question, time window, data cutoff date; each row marks the node it supports (a hint) |
| 2 Timeline and turning points (时间线与转折) | cut the window into segments with fixed start and end dates, each with its drivers and evidence | the course of development | segment nodes: each segment written as a node or as a paragraph within a node, start and end dates fixed | evidence rows for each segment |
| 3 Mechanism chain (机制链) | where the money comes from and goes to, through whose balance sheet; each link marked confirmed, refuted or reversed | mechanism | mechanism nodes: each link of the chain becomes a node, each marked confirmed, refuted or reversed | evidence rows for each link |
| 4 Holders and participants (持有人与参与方) | who holds, who is buying, who is exiting, who is taking it up; separate accounts per party | mechanism (holder table) | subjects and node division | evidence rows |
| 5 Impact matrix (影响矩阵) | condition—channel—affected party—signal—time window | potential impact | impact nodes, written as conditions: what triggers, through which channel, falling on whom, which signal to watch, in what time window | data-series rows for the signals |
| 6 Confusables (易混淆对照) | two things with one name, measurement bases, stock and flow, direction, units, vintages, current versus historical | questions easily confused | the name table (FICCOutline 4.2); a distinction node where needed | confusion rows (confusable mark) |
| 7 Disagreement table (分歧表) | who, which day, what they say, grounds, our reading | disagreements between houses | a disagreement node when the disagreement itself is a key point, with the claim stating the state of the disagreement | disagreement rows: who, which day, what they say, grounds (disagreement mark) |
| 8 Evidence strength (证据强度) | number of sources (one origin counts once), tier, speaker, confirmed or inferred | evidence strength and confidence | claim strength graded by evidence (FICCOutline 2.3); under the root, write the confidence and the link that limits it | each row's strength, number of sources, single-source mark (strength column) |
| 9 Gaps and items to be verified (缺口与待核实) | what the material does not say, what has not yet been checked | (no separate item) | “待补充” “待核实” | to-be-verified mark |
| 10 Watch list and discriminating readings (观察清单与判别读数) | dated data and events, thresholds, which judgment they change, whether they can truly test this piece | what would change the answer; watch list | nodes for the conditions that change the judgment; a watch node before the conclusion | the series, thresholds and release dates for the conditions; series rows: source, measurement basis, vintage, latest point, next release date |
| 11 Change worksheet (update topics) (改动底稿) | the old version's original words, new evidence, reinforce/qualify/overturn/add | compared with the previous version | change nodes: which judgments changed | change-worksheet rows: the old version's original words, the new judgment, a change of conclusion or of degree |
| Not part of the map: source table (来源表) | institution, body date to the day, report name, path | source list | the source-list node at the end (FICCOutline 4.2) | source rows: institution, body date to the day, report name, path |

The default outline shape (the tree of a decision report) is in `references/report-skeleton.md`; it is only a starting point, and the tree grows by content (FICCOutline 3.4).

## 5 Cost

Estimate per `references/cost-estimate.md`. 1012Six's bill, per-seat costs and control items (trial and suspended items included): `references/hand-history.md` section 5.

## 6 Lessons index

1012Six's lessons index (pointers to rules that have a home, items this skill manages itself, items that belong to the writing side, overturned old rules): `references/hand-history.md` section 6.
