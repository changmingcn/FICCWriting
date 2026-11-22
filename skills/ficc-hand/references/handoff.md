# Handoff: FICCHand to ficc-voice

## 1 What is handed over

- `<文稿名>-提纲.md`: ficc-outliner maintains it per FICCOutline; its relation lines are the relation slots ficc-structurer rules (FICCStructure.md §6).
- `<文稿名>-资料索引.md`, §0 being the card below: append only; a changed row is marked “已改，见新行”.

Working files are not copied; index §9 gives their paths.

## 2 The handoff card (index §0)

The handoff note is a state card (`shared-protocols/handoff.md` §2) that opens the writing-phase packet; this section alone defines it. A long item goes on as a `path:line` pointer.

1 **Position**
- Decision question (one sentence), time window, data cutoff date.
- Paths of the outline and the index.
- Exit: outline only (settle after verifying delivery) or finished draft (record “研究阶段已完成”, no settle, continue into ficc-voice, settle after the draft is delivered).
- Takeover step (§3).

2 **Lessons**
- The run's do-not-repeat lines.
- The judgment most likely wrong (`最可能错的一条判断`) and the cheapest test of it.
- Top spark: the best anomaly or opportunity, the cost of probing it, what it would change (research-agent `SKILL.md` (Before you send)).

3 **Settled**
- Root claim and `R/立论.md` layer 1 (judgments with their strength).
- Explicit must-answers (`明确必答项`), each with its delivery place (node or appendix) and status, answered or undetermined.
- User rulings in force (`当前生效的用户裁定清单`): section or node number + original text, overturned ones left out; a ruling that changes a judgment's strength is written “全文凡……” so the writer searches the whole text.
- Register rows in force: `SUPERSEDED.md` line, keys, now.
- Settled on the outline: measurement bases and indicators, data windows, the name table, the change worksheet (change section in two columns “旧版原话｜新说法”, its opening naming which items changed the conclusion and which only the degree). Node positions follow ficc-outliner's tree; the index's “提示节点” are hints.

4 **Open / trace**
- Open questions and items to be verified (`开放问题与待核实`): index §8 items by number (unresolved critical dependencies, unresolved must-answers, gaps bearing on a retained judgment, each with the judgment or node it limits), disagreements T0 has not ruled (FICCHand 3.6), outline items not yet settled, any pending scope decision (FICCHand 3.1 ⑥), each with the node it affects. Exploratory leads appear only as one pointer to `R/脉络图.md` §1. These stay with T0 (§4); the writer writes each limited, suspended or undetermined judgment as the outline states it and owes answers only to the decision question and the must-answers.
- Acceptance record: outline check, tieout, counter-view: path and conclusion, one line each; a counter-view not seated (FICCHand 3.7 ③) reads `counter-view: not seated (thesis unchanged since step 4)`.
- Read lists, one per taking-over seat (conductor, structurer, composer, writer, external route): read first, read next, readable only for a stated purpose; history files by name, each “不作现行依据” or “禁读”; do-not-read reasons by category only (史, 旧稿, 已被取代, 他席范围), never figures or field names.

## 3 Where ficc-voice takes over

At step ② of the relay table in ficc-voice/SKILL.md (relations), under `ficc-conductor`, the standing writing-phase parent: a fresh one for each wave (relay, check wave, close), each started from this card and `conductor-progress.md`. The outline has passed ficc-outliner's check mode (FICCOutline 9); do not rebuild it. The draft then passes ③ (ficc-writer draft, paragraphs and sentences in one pass; ficc-composer only as the optional paragraph-only arm) and the ④ checks. This skill changes no file of ficc-voice.

## 4 After handoff

A user correction or new material that changes a judgment changes the tree first (FICCOutline 6.2, ficc-outliner), more than the contents and wording; reopen the affected evidence and conclusion checks per `shared-protocols/source-check.md` (Validity of a check; Reread on a changed binding); no separate process, no rerun of FICCHand. Only a changed decision question (the user's scope decision, FICCHand 3.1 ⑥) restarts FICCHand from framing.
