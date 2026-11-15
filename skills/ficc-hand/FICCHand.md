# FICCHand: from topic and corpus to view outline and materials index

Only T0 reads this file, beside research-agent `SKILL.md`. A run is a research-agent Investigation (gates and reviews not restated); per step this file gives the product, seat, gate and FICC-only done-condition. The tree is ficc-outliner's alone; relations and wording are ficc-voice's. Record: `references/hand-history.md` (not a current basis).

## 1 Purpose and deliverables

### 1.1 A research report that supports decisions

Readers make decisions with it, so answer the question first, then give the grounds and the circumstances in which the answer would be wrong. Each retained judgment, explicit must-answer and critical dependency has a place to land in the outline or the index (4).

### 1.2 Deliverables

Two files in `T/` (task directory), posted in the conversation, on Drive only when asked: `<文稿名>-提纲.md` (view tree, `references/outline-from-research.md`) and `<文稿名>-资料索引.md` (pointers only, `references/materials-manifest.md`; its head is the handoff card). Working files stay in `R/` (the line's `research/`, else the task directory's; research-agent `references/framing.md` (Research-state scaffolding)).

### 1.3 When not to use it

Monthly short pieces (memory `feedback-monthly-short-pieces.md`), Q&A and data lookups (research-agent Lookup or Brief), style or register work on a finished article (ficc-voice).

## 2 Steps

| Step | Gate | Seat (tier) | Products |
|---|---|---|---|
| 0 Framing (3.1) | 1 | T0 | `R/brief.md`, `T/成本估算.md` |
| 1 Corpus inventory (3.2) | 2 | T0 `ficc.py stat/find`; scout (T3) pulls; one triage seat (T1E general-purpose or collator); data: scout runs a script, general-purpose (T1E) writes one | `R/inventory.md`, `R/cand.tsv`, `原件/`, `R/cache/`, `T/results/D-Q<编号>.md` |
| 2 Digests (3.3) | 2 | digester (T1E) per source, one Workflow wave | `T/results/D-<编号>.md` |
| 3 Map (3.4) | 3 | collator, then ficc-mapper map mode (T1E) | `R/ledger.md`, `R/checks.md` (T0), `R/脉络图.md` |
| 4 Thesis (3.5) | 3; 4 red team | T0; one dissenter (T1); fresh-eyes wave; top-review on trigger | `R/立论.md`, `R/dissent-map.md`, register rows |
| 5a Index (3.6) | — | ficc-mapper index mode (T1E) | `T/<文稿名>-资料索引.md` |
| 5b Outline (3.6) | — | ficc-outliner build mode (T1E) | `T/<文稿名>-提纲.md` |
| 6 Acceptance (3.7) | 4 | ficc-outliner check mode; `scripts/tieout.py` | `T/results/查提纲.md`, `T/results/tieout.txt` |
| 7 Handoff (3.8) | 4 | T0, then `ficc-conductor` | handoff card at index §0 |

Caps: dynamic-workflow `SKILL.md` (Hard lines); models: `shared-protocols/model-tiers.md` (Task seat profiles); packets, results, fresh fix seats: `shared-protocols/handoff.md`. T0 reads map §1, §3, §8; §7 (disagreements) always; §11 (the change worksheet) on an update topic; other sections and ledger rows by anchor.

## 3 Process

### 3.1 Framing (step 0)

- Input: the user's words, topic, corpus scope; for an update, the old draft and its `SUPERSEDED.md` rows. An old draft without a check table, and any old draft on an adjacent topic, is unchecked notes: heading-level judgments reread against the originals (`shared-protocols/source-check.md` (Documents written from notes)), listed in the inventory and the index S table.
- `R/brief.md` is frozen before any new original opens (research-agent `references/framing.md` (The Frame block)).
- Done when:
  - beyond the Frame, six things are written out.
    - ① Decision question: the decision to serve, in the user's original words;
      - for an update topic, write it as “旧版哪几条判断被推翻就改标题、导语和对应章节” (which judgments of the old version, once overturned, change the title, the lead and the corresponding sections), and set the sub-questions one by one against the old version's judgments.
      - Rewrite a predictive question (“会不会转为走阔”) as a conditional one: what state things are in now, under what conditions that would change, and which of those conditions are already visible;
      - the root claim answers this conditional judgment.
    - ② The subject of the answer: when the question asks about “变化和深远意义”, make the subject the composition, the holders and the channels, not the total.
    - ③ Fund flow first: every judgment must translate into who is forced to buy or sell, where the money goes from and to, whether it gets through, and who the marginal price-setter is;
      - a total-to-total inference first passes the distribution and transmission check (memory `user-flow-first-framework.md`, `segmentation-friction-axiom.md`).
    - ④ Fix the time window and data cutoff date in writing, and whether this pass may add new facts, new numbers, new sources.
    - ⑤ Analysis only, no prediction: looking ahead, write only watch items and conditions that would change the judgment;
      - without a mandate, write no trading advice (memory `macro-analysis-not-prediction.md`; FICCOutline 2.1).
    - ⑥ Task roles: the role list below, in `R/brief.md`.
  - The cost estimate (`references/cost-estimate.md`) is in the opening ask (first-secretary `references/control-policy.md` (`WORK-03`)), pricing the fresh-eyes wave both ways when the question is open-ended; actual figures are reported truthfully after the run.
- ⑥ Task roles (任务角色): the trunk question (主干问题) governs the evidence, the main judgments, the outline and acceptance; explicit must-answers (明确必答项) keep their delivery duty; exploratory leads (探索线索) steer the exploration and owe no answer or section of their own. Doctrine: research-agent `references/framing.md` (Task roles). Here: the role list is kept current in `R/questions.md`; an unresolved critical dependency (关键依赖) goes into map §9 and index §8; the route's completion items are the five of 3.7 and the exit of 3.8; the handoff's open items are the card's open block (`references/handoff.md` 2).

### 3.2 Corpus inventory (step 1)

- Search terms and the first wave serve the trunk's direct answer and its rivals first; a lead gets corpus only for the part of the trunk it tests (⑥).
- `R/inventory.md`: pivotal 10–15, skim at most 15, discards counted by reason; dates marked “(filename)” until the digest confirms the body date. `原件/` keeps PDF twins for figures. `R/cache/` per research-agent `references/collection.md` (Cache every pull; search both directions). `D-Q` files feed the index Q table (ficc-research-kit `SKILL.md` (Data-source routing (first choice order))).
- Done when: the candidates are the union of title/tag queries and body scans; a cross-cutting topic scans the whole library with a subject constraint, near-duplicates removed (ficc-research-kit `references/topic-playbook.md` (Selection rules)); the search terms include “制度与监管变化” (rule revisions, exemption letters, accounting standards, filings); a fetchable primary source is fetched, not waited for in a bank's citation; the old version's source chain is in the inventory; a missing document's reason is established before it enters the gaps; a guide is an index, not evidence.
- Never read the library over SMB; use ficc-research-kit's fast path.

### 3.3 Digests (step 2)

- The wave's COMMON file carries `references/digest-extra-fields.md` and ficc-research-kit `PACKET-STANZA.md`; each packet, the source, its register rows, the views being formed, for an update the old version's judgments (COUNTER-CASE attacks them), the trunk question and the role of the question it serves.
- Done when: every load-bearing figure records the extra fields in full, once; when all are in, T0 counts which digests changed the old version's conclusions.

### 3.4 Map (step 3)

- Ledger per research-agent `references/analysis.md` §1 (fact and conflict rows apart, conflicts to T0; tiers only from the digest template). Map per `references/map-template.md`; the mapper opens original lines only where a dispute, a doubtful figure or a missing field points.
- `R/checks.md` (T0): 数字｜原件位置｜结果 for the landing figures the root and trunk use, opened at the line, chosen by unverified load-bearing judgments, critical dependencies first, no cap (ficc-research-kit `references/topic-playbook.md` (Stage 2: Digest interpretation)).
- Done when: each of the eleven elements has content or states “缺”; every evidence item is anchored to a digest row, an unexplored question-tree row to the user's words or `R/brief.md`; critical dependencies, conflicts, mismatched measurement bases, confusables and gaps are marked; the map is at most 25 KB, its byte count stated in the mapper's result.

### 3.5 Thesis and counter-view (step 4)

- T0 forms the thesis (research-agent `references/analysis.md` §2, §4, §6). One counter seat, the dissenter (research-agent `references/collection.md` (Dissent seat)); the fresh-eyes wave on the first `R/立论.md`, screened before the outline (same file); the top-review seat on the top three judgments only when research-agent `references/delivery.md` §1 triggers.
- Weigh per FICCOutline 6.1, 6.2: strongest reason first; an objection that overturns the trunk changes the trunk claims; the trunk question changes only by the user's scope decision.
- `R/立论.md` (T0, one current file, at most 12 KB): judgments in three layers (judgment; evidence point by point with date, source, measurement basis; confidence and its limiting link); which are adopted and which only contrast; each strength set once; a rewrite names the version it replaces. `R/dissent-map.md`: research-agent `references/analysis.md` §3; register rows: `shared-protocols/source-check.md` (Register).
- Done when:
  - every main judgment passes six heading-level checks:
    - time window (whether the facts hold over the period the judgment speaks of);
    - when a model gives a range, write the range and name the model, and do not treat the upper bound as a finding;
    - do not write an inference as a source;
    - do not generalize one house's sample to the whole;
    - do not turn what the material does not say into a denial;
    - a conclusion uses only evidence of the same category (sentiment, activity and fund flows kept apart).
  - A partially adopted objection: the better-fitting measure beside the standard one, the opponent's reading as a parallel hypothesis with a discriminating reading.
  - A reversal raised from the digests alone is an unverified lead; it enters the register only once its original confirms it.
  - Stop when the decision question and each explicit must-answer have closed at saturation (research-agent `references/analysis.md` §9) and every critical dependency is checked against its original or limits or suspends its judgment; a lead closes or pauses on contribution, and an unsaturated one is an open thread (research-agent `references/delivery.md` D18) with its reason in the question tree.
  - A default T0 set itself that would affect many nodes or sentences: ask the user in one sentence before dispatching, or first try it in one place.

### 3.6 Outline and materials index (step 5)

- 5a per `references/materials-manifest.md`. 5b per the outliner card's build mode and `references/outline-from-research.md` (inputs listed there). User ruling: only ficc-outliner builds the tree.
- Done when: the tree meets `references/outline-from-research.md` (Build; Done when) with FICCOutline 2.1 header, 4.2 name table and nodes, 8.2 〔标题〕, unfolded to paragraph groups (4.1 step 5, 3.4); the index has one anchored row per load-bearing figure and per judgment.

### 3.7 Acceptance (step 6)

- One parallel wave: ① ficc-outliner check mode (FICCOutline 9), reports only; ② `python3 ~/.claude/skills/ficc-hand/scripts/tieout.py --outline <提纲> --against <资料索引> <账本>` (`references/materials-manifest.md` 3); ③ the counter-view: a dissenter on the root and trunk claims, seated when the thesis changed after step 4 or a CLAUDE.md Proportion trigger holds (a contested core conclusion, a key data conflict, thin evidence): the six checks of 3.5, degree words, counter-evidence from a lead paused, closed or left out, unverified critical dependencies. ③ reads only the outline, the index, the digests and map §1, and marks each finding “本轮引入” or “旧稿已有”. Otherwise ③ is not seated and the acceptance record says `counter-view: not seated (thesis unchanged since step 4)`.
- Outline findings go to a fresh ficc-outliner seat (rule/maintain mode), index findings to a fresh ficc-mapper seat (fix mode); one fix round per list, then tieout again (CLAUDE.md Proportion).
- Done when: the outline check finds no fault that affects writing; tieout misses are zero or each has T0's disposition; with ③ seated, each counter-view point is judged adopted, partially adopted or not, with one line of discriminating evidence; with ③ not seated, the acceptance record carries the not-seated line.
- Complete by the five items below, checked against the decision question's answer, each explicit must-answer and each critical dependency, never the leads' answer rate; item 1's important gaps bear on one of those three, item 5's open questions are the card's open block:
  1. Selection: which material is adopted and which discarded, with reasons that fit the decision question; important gaps stay in the gap table and in section 8 of the index, and do not disappear because the tables are full.
  2. Traceable: every main judgment has evidence anchors, and its subject, indicator, period, unit, condition and strength match; disagreements between houses are not hidden by merged wording.
  3. Distinguishable: source wording, research synthesis and inferences still to be verified (“我们推断”) can be told apart at a glance in the outline and the index.
  4. Ready for the next stage: the outline and the index can be read directly by the next stage (the outline check has passed); the tieout result states which lines and which name table it checked, and zero coverage does not count as a pass; tieout checks tokens only, and whether the meaning is right is judged by the outline check and, when seated, the counter-view seat.
  5. Handoff: the handoff note states what is settled and what is not, the open questions and the nodes they affect, and continues or ends per the user's final goal (the exit in 3.8).

### 3.8 Handoff (step 7)

- The card heads the index (`references/handoff.md` 2); outline and index are posted without waiting for approval (FICCOutline 4.2).
- Exit, per the acceptance items: ① outline only: `work.py settle` after verifying delivery. ② Finished draft: record “研究阶段已完成”, do not settle, and from ficc-voice relay step ③ (`references/handoff.md` 3) dispatch a fresh `ficc-conductor` for each wave of the writing phase (relay, check wave, close), each started from the card and `conductor-progress.md`; settle after the draft is delivered (first-secretary `references/control-policy.md` (WORK-01)).
- At settle, rewrite the line's `next.md` as its current-state card, at most 10 KB, replaced text to `next-history.md` (`shared-protocols/handoff.md` §1).
- After handoff: a changed judgment changes the tree first and reopens the affected checks (`references/handoff.md` 4); never only the contents and wording, no separate process, no rerun of this skill.

## 4 Map

The material laid out as a structure, from which T0 forms the thesis (`references/map-template.md`); it lands per `references/report-skeleton.md` and `references/materials-manifest.md`. The map keeps the full record; the outline takes only what serves the answer.
