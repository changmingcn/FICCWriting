---
name: ficc-voice
description: "Four-seat relay for Chinese FICC writing: ficc-outliner (outline, placement), ficc-structurer (relations), ficc-composer (paragraphs), ficc-writer (sentences, wording). For research articles, monthly letters, market commentary, lecture notes, case scripts, turning recordings into written text; not finance Q&A, data lookups or calculations. Keywords: 中文 FICC 文稿, 研究文章, 月报, 市场评论, 讲义, 案例讲稿, 录音稿书面化. Not for: 普通金融问答, 取数, 计算."
---

# ficc-voice

## 1 When to use

T0 reads only this file and the outline; agents read the packet, then rules per card mode. Before drafting: one outline per piece, `<文稿名>-提纲.md` beside the draft, path in the packet.

Trial (2026-10-25): at the research→writing handoff T0 may hand this router to `ficc-conductor` (card), which runs it from on-disk state; the protocol is kept in the author's task directory and is not included in this release.

## 2 Relay table

| Step | Seat | Reads | Input | Output | Fails → |
|---|---|---|---|---|---|
| ① Build or summarize outline (Hand handoff outline replaces it: ficc-hand/references/handoff.md 3) | outliner build | FICCOutline.md 1–4, 7–8 (7.3 only if summarizing) | goal, material or original draft | outline (name table `名字表`, order, unfolding, 〔标题〕 lines) | outliner |
| ② Place | outliner place | FICCOutline.md 4.2 and 5–6 | outline, new material or change | placement record (references/placement-record-template.md), revised outline | outliner |
| ③ Relate | structurer relate | FICCStructure.md 1–6 | outline view and node slices (dispatch-notes 6), placement record | relation sheet (references/relation-sheet-template.md) | placement objection (`安放异议`) → outliner |
| ④ Paragraphs | composer compose, or the inline seat (dispatch-notes.md 7) | FICCCompose.md | node slice, relation sheet, material excerpts, adjacent body text | paragraph draft | relation issue → structurer |
| ⑤ Sentences, wording | writer polish, or the inline seat (dispatch-notes.md 7) | references/voice-excerpt-polish.md (FICCVoice.md by V number) | node slice, paragraph draft, name table, material excerpts | revised node, result sheet | paragraph issue → composer |
| ⑥ Check | all four seats (writer: expression, cold read), source-check seat (by review tier: `shared-protocols/source-check.md`, Review tiers) and 标题级反驳席 (formerly counter-view) | §3 Check | full text | findings | per §3 |
| ⑦ Deliver | T0 | §4 | fixed full text | Google Doc | ⑥ |

Cold read gets only full text and name table. T0 consolidates ⑥ findings, returns each to its seat with location, conflict and needed decision, sends missing evidence to research in parallel, rechecks only affected ranges (dispatch-notes 2.3), does not rule on content. Outline reads: dispatch-notes.md 6 (view, tie-out, cold read).

Short piece (body ≤600 Chinese characters, O44 count, any node scale): one seat, writer draft (or the inline seat, dispatch-notes.md 7), does ④⑤ per references/compose-excerpt.md (child nodes, section-level carry-over or whole-piece close: plus C04–C06, C17–C19), then references/voice-excerpt-draft.md and voice-excerpt-polish.md; no separate paragraph draft. Wording-only, for a passage whose facts are tied out and whose sentences carry no argument (no “所以、因为、但是、如果” between them): ⑤ only (writer patch, references/voice-excerpt-patch.md). A smoothing request (“说顺”) on an author's passage that argues is dispatched as a short piece in writer draft mode (compose-excerpt, or FICCCompose.md in full above 600 characters, then voice) with its material rows (who, what, period, unit, qualifier) attached (references/dispatch-notes.md 1 item 7) and with reorganization inside the node authorized (FICCOutline.md O69): paragraph and sentence order may change, the author's judgments may not; facts from the attached rows may be brought in only to complete an example the author began, each named by its row in the result sheet, and no point the author did not make is added. A qualifier the author's passage omits stays under FICCVoice.md I4 (named and handed back per V04, never added silently); restoring whose, which indicator, when, in what unit, on what basis or from what sample for a fact already in the passage, from its row, is not bringing one in (I7, FICCOutline.md O70). Holding two steps does not widen authorization.

## 3 Acceptance and return table

| Defect | Rules | Seat | Check |
|---|---|---|---|
| new material unplaced, length too short for kept information, hollow tree or claims, no placement reason | FICCOutline.md 1–6 | outliner | FICCOutline.md 9 |
| relation unclear or grounds changed, side-by-side items written as cause and effect, wanted causality unproven, group missing a link | FICCStructure.md 1–5 | structurer | FICCStructure.md 7 |
| bloated paragraph, opening not the claim, two tasks in a paragraph, carry-over as contents list, close restates | FICCCompose.md 1–6 | composer | FICCCompose.md 7 |
| hard-to-follow sentence, unclear reference, vague condition or scope, unmarked seam | FICCVoice.md 2–4 | writer | FICCVoice.md 7 |
| figure without measurement basis, lost attribution, misplaced note, two names for one thing | FICCVoice.md 5, name table | writer | FICCVoice.md 7 |
| fact contradicts source | source-check.md | source-check seat | tie-out |
| heading-level overstatement | source-check.md | 标题级反驳席 | 标题级反驳席 |
| format and spacing | references/format-and-maintenance.md | writer | references/clarity-acceptance.md 3 |

## 4 Kept rulings and pointers

1. Post the checked outline in chat; wait for approval only when the user asks to see it first.
2. Before drafting, settle on the outline what it can: headings, measurement basis and indicators, data window, name table, changed-section format; each later ruling costs an extra revision round.
3. A T0-set default touching ≥100 sentences: ask the user in one sentence before dispatch, or trial it on one piece.
4. Style-only edit or written-register conversion: summarize the outline from the original; no rebuild.
5. T0 routes consolidated to-dos to their owners; drafting seats do not edit the outline, placement record or relation sheet on the side.
6. No seat deletes a fact the placement record keeps, only compresses its wording and detail; a needed deletion goes to the outliner for placement review (FICCOutline.md O58).
7. Never skip the counter-view seat on research articles; only it catches heading-level overstatement.
8. Before submitting, run scripts/voice_check.py --clarity and scripts/cjk_space.py --check; handle hard errors, review candidates and the “！” rows per references/clarity-acceptance.md.
9. After changing rule-file headings or section numbers, run scripts/xref_check.py.
10. The four rule files hold only rules. Rewrite examples: references/examples-and-rewrites.md; clarity rewrites: clarity-rewrites.md; connectives: connectives.md; model texts: exemplars.md; format: format-and-maintenance.md; grounds: dev-notes.md.
11. The user's current request comes first. Do not draft by comparing against the author's original text. Write user corrections into the relevant rule file.
12. Deliver a native Google Doc by default, updated in place by Doc ID; Markdown is the working source.
13. Since 2026-10-16 rule files are concise English. A retired rule number goes with its line, leaves no pointer, and is never reused; live files cite current numbers only, old-to-new only in records (references/migration-2026-10-17.md). User ruling 2026-11-04, replacing 2026-10-17. references/zh/ is archive only, unread by agents.
14. A smoothing request on an author's passage that argues is a content task before a wording task: its material rows (who, what, period, unit, qualifier) before the wording, the claim before the story, every connective backed by a settled relation (FICCVoice.md 0, I1–I3); whoever holds the pen; T0 in chat dispatches it and never smooths it itself; the dispatch grants reorganization inside the node (FICCOutline.md O69) and the completion of the author's examples from the attached rows (each named by row, no new point), never a change of the author's judgments. User rulings 2026-11-06 and 2026-11-07.

## 5 Dispatch details

See references/dispatch-notes.md.
