---
name: ficc-voice
description: "0→1 relay for Chinese FICC writing, from raw material and a research question to a finished piece: ficc-outliner (question card, living outline tree, placement), ficc-structurer (relations, S32 completeness), ficc-writer or the inline seat (paragraphs and sentences written once per node), ficc-composer (optional paragraph-only arm). For research articles, monthly letters, market commentary, lecture notes, case scripts, turning recordings into written text; not finance Q&A, data lookups or calculations. Keywords: 中文 FICC 文稿, 研究文章, 月报, 市场评论, 讲义, 案例讲稿, 录音稿书面化. Not for: 普通金融问答, 取数, 计算."
---

# ficc-voice

## 1 When to use

The trunk grows a piece from 0 to 1: material and a research question → question card and outline tree → relations → each node written once → cold read, tie-out and bounded patches → delivery. Rewriting a finished draft is the secondary entry (FICCOutline.md §10).

T0 reads only this file and the outline; agents read the packet, then the rules their card mode and node duty name. Before drafting: one living outline per piece, `<文稿>-提纲.md` beside the draft, path in the packet (FICCOutline.md §4.2). It is the piece's only live planning file: question card, name table, placement, 事实／算式／消歧／段 rows and the relation slots 分担／接前／关键边表 all live in it. New writing keeps no separate placement record or relation sheet.

The writing phase may go to `ficc-conductor` (card): optional for a short piece, standing for a ficc-hand report. The lead dispatches a fresh `ficc-conductor` for each wave of the writing phase (relay, check wave, close), each started from its card and `conductor-progress.md`. The `ficc-conductor` card is not included in this release (it is bound to the author's task record and handoff scripts); without it the lead runs this router itself.

## 2 Relay table

| Step | Seat | Reads | Input | Output | Fails → |
|---|---|---|---|---|---|
| ① 问题卡与立活树 (a Hand handoff outline replaces it: ficc-hand/references/handoff.md 3) | ficc-outliner build, then place for new material | FICCOutline.md §1–§8, closing on §9 (§10 only when summarizing a finished draft) | goal, material, research question | living outline: 问题卡, 名字表, tree with 主旨四栏, 事实／算式／消歧／段 rows, 〔标题〕 lines | outliner |
| ② 四向递归定关系与S32完备性 | ficc-structurer relate | FICCStructure.md §1–§6, closing on §7 | outline view and node slices (dispatch-notes 6) | 分担, 接前 and 关键边表 rows written into the living outline; to-do items for other nodes | placement objection (`安放异议`) → outliner |
| ③ 单次成段成句 | ficc-writer draft, or the inline seat (dispatch-notes.md 7); ficc-composer only as the optional paragraph-only arm (瘦身方式甲 comparison) | FICCVoice.md by duty. Leaf: §0, §2, §3.1, §3.2 and §4. Lead (N0, a parent with its own opening, a leaf a 收尾 line assigns): adds §1 and the siblings' conclusions. Patch: §0, §3.1, §3.2 and §4 | node slice with its relation slots, signed 算式 rows, source excerpts, name-table rows, adjacent body text | node body, result sheet (回执) | relation issue → structurer; placement or a missing 算式 row → outliner |
| ④ 独立冷读、原件核对与受限修补 | cold read, then clarity in the same seat (ficc-writer); structure check (ficc-structurer check mode: FICCOutline.md §9, FICCStructure.md §7 and FICCVoice.md §4, full text read once); source-check seat (by review tier: `shared-protocols/source-check.md`, Review tiers); 标题级反驳席 (formerly counter-view; card and model: `shared-protocols/model-tiers.md`, Task seat profiles, top-review); patch seat (writer patch or the inline seat) | references/clarity-acceptance.md | full text; for a patch, the node and its findings | findings; bounded patches | per §3 |
| ⑤ 合稿交付 | T0 | §4 | fixed full text | Google Doc | ④ |

Each step closes on its gate before the next starts: ① the Outline Gate and ② the Structure Gate (human criteria plus `outline_slice.py check-0to1`, dispatch-notes 6); ③ FICCVoice.md §4 and, in an inline-seat draft, the fact guards (dispatch-notes.md 7); ④ references/clarity-acceptance.md A01–A02.

The cold read comes first, on the full text and name table alone. The packet names the `voice_check.py --clarity` output as a path; the same seat opens it only after its cold-read findings are written, then checks clarity (references/clarity-acceptance.md 3). T0 consolidates ④ findings, returns each to its seat with location, conflict and needed decision, sends missing evidence to research in parallel, rechecks only affected ranges (dispatch-notes 2.3), does not rule on content. Outline reads: dispatch-notes.md 6 (view, tie-out, cold read).

Short piece (body ≤600 Chinese characters, O44 count, any node scale): one seat, writer draft (or the inline seat, dispatch-notes.md 7), does ③ in one pass from the FICCVoice.md leaf slice (child nodes, section-level carry-over or whole-piece close: the lead slice, adding §1 with C04–C06 and C17–C19); no separate paragraph draft. Wording-only, for a passage whose facts are tied out and whose sentences carry no argument (no “所以、因为、但是、如果” between them): the patch slice only (writer patch). A smoothing request (“说顺”) on an author's passage that argues is dispatched as a short piece in writer draft mode (the FICCVoice.md leaf slice, at any length) with its material rows (who, what, period, unit, qualifier) attached (references/dispatch-notes.md 1 item 7) and with reorganization inside the node authorized (FICCOutline.md O69): paragraph and sentence order may change, the author's judgments may not; facts from the attached rows may be brought in only to complete an example the author began, each named by its row in the result sheet, and no point the author did not make is added. A qualifier the author's passage omits stays under FICCVoice.md I4 (named and handed back per V04, never added silently); restoring whose, which indicator, when, in what unit, on what basis or from what sample for a fact already in the passage, from its row, is not bringing one in (I7, FICCOutline.md O70). Holding two steps does not widen authorization.

## 3 Acceptance and return table

A finding names its rule file; T0 routes it to that file's owner.

| Defect | Rules | Seat | Check |
|---|---|---|---|
| question card without 门槛, 分母 or window; claim as a topic bucket or a pile of numbers; new material unplaced; length too short for kept information; hollow tree or claims; no placement reason; a derived number with no signed 算式 row | FICCOutline.md §1–§8 | outliner | Outline Gate: FICCOutline.md §9 |
| relation unclear or grounds changed; side-by-side items written as cause and effect; wanted causality unproven (no connecting source line); 分担 incomplete (S32); a cross-branch edge ruled twice | FICCStructure.md §1–§6 | structurer | Structure Gate: FICCStructure.md §7 |
| lead, part or section opening not the claim; carry-over as contents list; close restates | FICCVoice.md §1 | writer | structure check: FICCVoice.md §4 |
| bloated paragraph or number wall, opening not the claim, two tasks in a paragraph, unmarked seam | FICCVoice.md §2 | writer | structure check: FICCVoice.md §4; `重段待处置` per references/clarity-acceptance.md 3 |
| figure without measurement basis, lost attribution or qualifier, an own calculation not on the tree, two names for one thing | FICCVoice.md §3.1, name table | writer | cold read and source check: references/clarity-acceptance.md A01 |
| hard-to-follow sentence, unclear reference, vague condition or scope | FICCVoice.md §3.2 | writer | cold read, then clarity: references/clarity-acceptance.md A01 and 3 |
| fact contradicts source; a numeric or basis difference | source-check.md | source-check seat | tie-out; sign-off per references/clarity-acceptance.md A02 |
| heading-level overstatement | source-check.md | 标题级反驳席 | 标题级反驳席 |
| a patch past its named sentences, or a B-grade patch that grew | references/clarity-acceptance.md A02 | patch seat | apply gates (dispatch-notes.md 7) |
| format and spacing | references/format-and-maintenance.md | writer | references/clarity-acceptance.md 3 |

## 4 Kept rulings and pointers

1. Post the checked outline in chat; wait for approval only when the user asks to see it first.
2. Before drafting, settle on the outline what it can: headings, measurement basis and indicators, data window, name table, changed-section format; each later ruling costs an extra revision round.
3. A T0-set default touching ≥100 sentences: ask the user in one sentence before dispatch, or trial it on one piece.
4. Style-only edit or written-register conversion: summarize the outline from the original; no rebuild.
5. T0 routes consolidated to-dos to their owners; drafting seats do not edit the living outline, its placement and relation slots included, on the side.
6. No seat deletes a fact the placement record keeps, only compresses its wording and detail; a needed deletion goes to the outliner for placement review (FICCOutline.md O58).
7. Never skip the counter-view seat on research articles; only it catches heading-level overstatement.
8. Before submitting, run scripts/voice_check.py --clarity; handle hard errors, review candidates and the “！” rows per references/clarity-acceptance.md.
9. After changing rule-file headings or section numbers, run scripts/xref_check.py.
10. The three rule books and references/clarity-acceptance.md hold only rules. Rewrite examples: references/examples-and-rewrites.md; clarity rewrites: clarity-rewrites.md; connectives: connectives.md; model texts: exemplars.md; format: format-and-maintenance.md; grounds: dev-notes.md.
11. The user's current request comes first. Do not draft by comparing against the author's original text. Write user corrections into the relevant rule file.
12. Deliver a native Google Doc by default, updated in place by Doc ID; Markdown is the working source.
13. Since 2026-10-16 rule files are concise English. A retired rule number goes with its line, leaves no pointer, and is never reused; live files cite current numbers only, old-to-new only in records (references/migration-2026-10-17.md). User ruling 2026-11-04, replacing 2026-10-17. The Chinese originals (former references/zh/) are kept in the author's archive, unread by agents and not included in this release.
14. A smoothing request on an author's passage that argues is a content task before a wording task: its material rows (who, what, period, unit, qualifier) before the wording, the claim before the story, every connective backed by a settled relation (FICCVoice.md 0, I1–I3); whoever holds the pen; T0 in chat dispatches it and never smooths it itself; the dispatch grants reorganization inside the node (FICCOutline.md O69) and the completion of the author's examples from the attached rows (each named by row, no new point), never a change of the author's judgments. User rulings 2026-11-06 and 2026-11-07.
15. A short piece, or an addition the user caps at about 1,000 characters: one drafting seat, reading the FICCVoice.md slices per §2, and no comparison arm; the text is posted in chat as soon as the draft passes scripts/voice_check.py. Its check is the doubts the writer's result sheet names plus the numbers, dates and attributions the piece adds, by T0 or one seat, and what is still being checked is named under the posted text. No tie-out wave or counter-view seat holds the post. User, 2026-10-12 (“做多久了还没写完”) and 2026-11-06 (“简略一点，不要那些反复核对的”); CLAUDE.md, Proportion.

## 5 Single-window chat protocol (any model, no tools)

One model in one chat window, with no scripts, runs the same trunk in five steps. Each step ends only when its gate question is answered yes; a no sends the work back into that step. The gates are the eye-test halves of the script gates (FICCOutline.md §9, FICCStructure.md §7).

1. **① 问题卡＋名字表.** From the pasted material and question, write the question card (each 开工问 with `门槛｜分母｜窗口｜删去后会答错什么`) and the name table (名字表). Gate (闸1, card half): does every 开工问 fill 门槛, 分母 and 窗口 (or say 若材料未决), so that a stranger reading the card alone knows what would count as a wrong answer?
2. **② 分层立树.** Build the tree top-down, each node with its 主旨四栏 (FICCOutline.md §3) and each fact with one 写全 home; run the identifier-swap test (识别号置换: a number whose swap changes the claim is a measured value and stays out of 判断 and 因) and the take-away test (拿走测试) on every node. Gate (闸1, claim half): with the children covered, reading only N0 and the card, can a stranger say for each question what the threshold is, what 分母 it takes and which period it reads, and if any item of the 限 field is removed, what would the reader mistake for what?
3. **③ 另起一问：定关系.** Ask it as a separate question: relations only. Run the cover test (遮住测试) on each parent, the adjacent-swap test (相邻对调测试) on each seam and the connecting-sentence check on each cross-branch link, then fill 分担, 接前 and 关键边表. Gate (闸2): cover each child in turn and read the parent's claim; which step is missing, and with all child claims added up, which link to the parent's claim is still unproven? Gate (闸3): for every 因为／因此／导致／依赖偿付, can you paste one source sentence or clause that joins both ends? If not, the edge is sealed as 待据.
4. **④ 段行与算式, then write each node once.** For each heavy node first list its 段1…段k rows and its 算式 and 消歧 rows, then write each node once from FICCVoice.md by its duty (§2). Gate (闸4): does every number not copied verbatim from the original have a closed 算式 row on the tree with its direction (缺口／盈余), and does every 或／仅／补位 or “agreement X has no clause Y” carry a literal source substring or a recorded zero-hit full-text search? Gate (闸5): does each 段 row hold ≤5 independent 写全 statements, is each switch of universe, 分母 or holder split or tabled, and does each split paragraph re-carry subject, period, basis and governing qualifiers?
5. **⑤ 反向原件自校.** Check the text back against the originals per references/clarity-acceptance.md (A01 findings, A02 patch bounds) and label the result “同模型自校，未经异源独立核对”. Gate (闸6): does each finding give only location, the misreading and an action class or open question number, with no model-written fix, and is every changed number backed by a pasted source line?

## 6 Dispatch details

See references/dispatch-notes.md (inline seat: dispatch-notes.md 7).
