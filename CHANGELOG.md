# Changelog

## 1.2.0 (2026-11-07)

Rebuilt from the author's tree of 2026-11-07 with the same release rules as 1.1.0. It carries the three sets of changes made on main after 1.1.0 (voice-trim, retired-pointers, xref-cards-stale) and the author's changes of 2026-11-05 to 2026-11-07 (from “Contract layer” on). Three scripts are new, none removed. ficc-hand, FICCOutline.md and the agent cards are unchanged in this build.

voice-trim (branch claude/gifted-johnson-r902bf): FICCVoice.md cut from 42,635 to 39,413 characters per `docs/FICCVoice-trim-audit.md` and the user's rulings of 2026-11-04. Rule numbers unchanged; no rule changes meaning, only organization and wording.

- FICCVoice.md: V30 merged into V29 (V30 is now a pointer). V22's nine seam checks become seven (the inference and `因为/所以` items point to FICCStructure.md S28, the relation-sheet item to S90), its connective menu is one line, and lists that duplicate references/connectives.md 1 and 6 are gone. V25's group-size cap points to FICCStructure.md S25. V33's language rule points to FICCOutline.md O33. Per-rule “See …-rationale.md” lines are replaced by one pointer in section 8 (those of V07 and V37 stay), which also now names references/examples-and-rewrites.md. V15's description of the complex sentence moved to references/FICCVoice-rationale.md; two examples moved to references/examples-and-rewrites.md. The duplicates of V13, V04, V52, V08, V32, V39 and of the introduction inside V22, V16, V29 are deleted.
- references/voice-excerpt-{polish,coldread,patch,draft}.md: section 1 mirrors the changed lines; polish no longer carries V30. references/clarity-acceptance.md cites V29 alone.
- references/FICCVoice-rationale.md: new V33 section records the user's 2026-10-11 ruling on English terms and names (home: FICCOutline.md O33).
- scripts/xref_check.py: V30 removed from the polish excerpt's required list. scripts/budget.json: caps of the six changed files lowered to their new sizes.

retired-pointers (2026-11-04, after voice-trim): the author withdrew the 2026-10-17 ruling "rule numbers frozen, retired numbers keep pointers". A retired number is now deleted with its line and never reused; every live file cites only current numbers, and the records (references/migration-2026-10-17.md, FICCVoice-provenance.md, history.md, dev-notes.md) keep the old numbers as history. Reviewed by refuter-t1e and a Codex second read.

- FICCVoice.md: the 15 pointer lines of section 2 (V05, V06, V08, V09, V41–V51), the V55 pointer of section 4 and the V30 pointer are gone; V08 is a live rule again ("Mark the add-on relation between parallel child nodes of the same kind"); 39,413 → 38,883 characters. FICCStructure.md: the S16 and S80 pointers and the empty sections 6–8 are gone, sections 9–12 are now 6–9 (relation sheet 6, layer check 7, conclusion 8, appendix 9); 42,292 → 41,582. FICCOutline.md: the O77 pointer is gone, its sentence "In all three, the heading states a judgment" sits under O76; 52,346 → 52,345 (cap 52,473 → 52,345). FICCCompose.md: 31,377 → 31,194.
- 109 live references and lineage notes ("(formerly V05)" and the like) rewritten to current numbers in the rule files, SKILL.md, references (rationale, examples-and-rewrites, dispatch-notes, exemplars, glossary, writing-checklist, relation-sheet-template), scripts/README.md and voice_check.py. references/FICCStructure-rationale.md keeps its own old section numbers and says so in its header. agents/ficc-structurer.md reads FICCStructure.md 1–6 and checks by section 7.
- references/voice-excerpt-polish.md carries V08's intent line; its cap rises 18,372 → 18,450 by the author's ruling of 2026-11-04. The four rule files' caps are lowered to their new sizes.
- scripts/xref_check.py: the retired-number mechanism (pointer lines, RETIRED-RULE, the "(formerly …)" exemption) is removed; a rule number without a definition line is MISSING-RULE; references/migration-2026-10-17.md is excluded as a record. SKILL.md 4 item 13 states the new rule.

xref-cards-stale (2026-11-04, after retired-pointers): scripts/xref_check.py now also scans the FICC agent cards and checks the rationale quotations. Reviewed by refuter-t1e and a Codex second read.

- Cards: the agents/ficc-*.md cards (five in this repo; found at ../../agents from the skill root, so both this repo layout and a home install; skipped with a message when absent; `--cards DIR` overrides) are checked for file-qualified section references and rule numbers (MISSING, MISSING-RULE). A card's section reference carries the section's heading text the first time it cites that section (`FICCStructure.md 7 “Check relations layer by layer”`); a wrong heading is STALE-TITLE, a first mention without one is NO-TITLE. The four changed cards (outliner, structurer, composer, writer) carry these titles; their caps rise by the author's ruling (outliner 2,722→3,173, structurer 2,442→2,549, composer 2,488→2,503, writer 2,599→2,606).
- Rationale quotations: a `Supports: Xnn “…”` quotation that is not a substring of rule Xnn's current text is STALE-QUOTE (Original/Origin historical quotations are not checked; history markers inside a quotation and extra spaces before it no longer hide it). The 15 stale quotations in FICCStructure-rationale.md and FICCVoice-rationale.md are corrected to the current wording; FICCVoice-rationale.md's V07 section is split into V07 (the semicolon ruling) and C08 (paragraphing), and FICCCompose.md C08 points at C08.
- The summary line carries the card and quotation counts; scripts/README.md documents both checks.

Contract layer (`skills/ficc-voice`, user rulings 2026-11-06 and 2026-11-07):

- FICCVoice.md: new section 0, Contract. Twelve invariants I1–I12 that the writer accepts before writing a sentence: one point per paragraph and one job per sentence (I1), a close opens no new point (I2), a connective only for a settled relation (I3), qualifiers travel with the claim (I4), the subject is what the sentence judges (I5), one name per object (I6), a full basis for every number (I7), point first and source after (I8), one judgment per sentence (I9), nothing left to decode (I10), one persona (I11), check before submitting (I12).
- Each I line names its home rule and, where it has them, its method rules, and says whether its check fails a node or only reports. V04, when to hand back, stands outside them.
- references/voice-excerpt-draft.md, -patch.md and -coldread.md copy I1–I12 into section 1. coldread's section 2 makes them the standard the cold read reports against. voice-excerpt-polish.md leaves them out to stay under 20,480 bytes, and its seat reads FICCVoice.md 0 once.
- SKILL.md 2: wording-only (writer patch, step ⑤) is for a passage whose facts are tied out and whose sentences carry no argument. A smoothing request (`说顺`) on an author's passage that argues goes as a short piece in writer draft mode, with its material rows (dispatch-notes.md 1 item 7) and with reorganization inside the node authorized (FICCOutline.md O69). The author's judgments may not change.
- SKILL.md 2, added 2026-11-07: facts from the attached rows may only complete an example the author began, each named by its row. A qualifier the passage omits stays under I4 (named and handed back per V04). Restoring whose, which indicator, when, unit, basis or sample of a fact already in the passage is not bringing one in (I7, FICCOutline.md O70).
- SKILL.md 4 item 14 (new): such a request is a content task before a wording task, whoever holds the pen. T0 dispatches it and never smooths it itself.
- references/dispatch-notes.md 1 item 8: a passage that argues goes as a short piece per SKILL.md 2, and the packet carries SKILL.md 2's authorization sentences verbatim (from “A smoothing request” through “does not widen authorization”).

Consolidation of FICCVoice.md (user ruling 2026-11-06, installed 2026-11-07):

- V52 is retired. Its line on the reader's question in a lead moves into V22: the next sentence opens with a back-reference or an add-on marker (FICCCompose.md C03).
- FICCCompose.md, FICCStructure.md, connectives.md, writing-checklist.md and FICCStructure-rationale.md cite V22, V53 or V54 where they cited V52. xref_check.py drops V52 from the polish excerpt's required list.
- V54: when one seam carries two layers of relation, mark the layer the relation sheet names (FICCStructure.md S29). When two layers nest across two seams, the outer word goes at the outer seam and the inner word at the inner seam. writing-checklist.md item 13 follows.
- V21: the side-by-side line is gone; I3 covers it.
- V25: the same-level, one-dimension and one-basis test is settled before writing (FICCStructure.md S24, S19, S14), and the line on a cause, its example and its result is gone.
- V32: the name-table description points to FICCOutline.md O32–O33, and the line on other people's views points to V57. V57's outline side points to FICCOutline.md O91.
- V04, V07, V26, V32 and V40: the writer hands back per V04 (where a hand-back goes: SKILL.md 3) instead of sending to T0 or the outline agent. V04's permission lines point to FICCOutline.md 7.3 and O69–O74.
- V22 forbids mechanical repetition of a connective or a filler; repeating the noun to carry a relation (V07, V12) is allowed.
- V32: a sentence with numbers may use the short name V26 allows within the paragraph, never a coined label. V34 drops “Correct per user feedback”.
- V40 separates the cold read of your own node from the cold read of another's draft. Section 8's reasoning pointer lists V15, V22, V29 and V53.
- The four voice excerpts mirror these lines. scripts/budget.json sets the caps of FICCVoice.md (38,883 → 42,268 characters), FICCCompose.md, FICCStructure.md and the four excerpts to the installed sizes.

Inline seat and scripts (2026-11-05):

- references/dispatch-notes.md: new section 7, Inline seat. Since 2026-11-05 a model with no tools, fed only what the packet inlines, drafts and patches node bodies, and the ficc-writer card is the backup or comparison arm.
- Section 7 sets the draft and patch modes, the packet order, a seven-block state card, a three-part output contract, parallel lanes, one patch ruling per node, apply checks, findings mapped with findings_map.py, assembly and cost. SKILL.md 2 rows ④ ⑤ and the short-piece line name the seat as an alternative.
- The inline seat's scripts (`scripts/inline-seat/`) are not included; see README and `skills/ficc-voice/scripts/README.md`.
- references/placement-record-template.md: new section 6, the inline-seat fields per node (`底稿`, `来源`, `带入`, `更新`, `保留`, `不写`, `上限`, `伏笔`, `必改句`).
- New scripts (see scripts/README.md): cjk_ids.py, node, line, block and unit ids inside Chinese text without `\b`, and stripping of line references into other documents; heading_list.py, the heading list of a draft read off its outline; findings_map.py, check findings routed to outline nodes by draft line, exit 2 when draft and outline headings do not align.
- outline_slice.py 1.0.1 reads node headings through cjk_ids.py, so an id glued to Chinese text is cut right. It has no new options and now needs cjk_ids.py.
- references/dev-notes.md, a stub here, gains headings 58–60.

## 1.1.0 (2026-11-04)

Rebuilt from the author's tree of 2026-11-04 with the same release rules as 1.0.0. Nine files are new, none removed. FICCStructure.md is unchanged.

Writing rules (`skills/ficc-voice`):

- FICCVoice.md: new V57, views and inferences are not objects. A view, reading or inference is never the subject or object of a verb that moves it, and `读法`, `解读`, `视角`, `判别读数` are not used as labels for our own interpretive moves. Its check regex is the one voice_check H9 uses.
- FICCVoice.md V37: each of the six AI-tone items now points to its home rule (roadmap sentences C01, C06; hollow claims C02, V38, V36; template tone C09, C11, C19; term pileups V32; end-of-paragraph uplift C17, C19; transition fillers C17, V22).
- FICCCompose.md: new C24, define once, then combine in short form. Two or three indicator outcomes name each indicator in full once and then state the outcomes in short form; more than three go into a table. The section 7 check covers C01–C22 and C24.
- FICCOutline.md: new O91, claim lines speak the article's language. Research vocabulary (`读法`, `判别读数`, `对手假设`, `反例`) is translated before it enters a `主旨`, `任务` or `展开` line or the name table. O64's foreshadowing line now states the outliner's own step and points to FICCCompose C15. The text of section 10 (Conclusion) moved to references/FICCOutline-rationale.md.
- SKILL.md relay table: outliner build reads FICCOutline.md 1–4 and 7–8; the structurer relates on the outline view and node slices; the composer gets the node slice; writer polish reads references/voice-excerpt-polish.md. The counter-view seat is renamed `标题级反驳席`. Item 6 points to O58, and item 8 defers to references/clarity-acceptance.md. A trial line names `ficc-conductor`, a card that is not included (README).
- New references/voice-excerpt-draft.md, -polish.md, -patch.md and -coldread.md: per-mode excerpts of FICCVoice.md. Section 1 copies the rules verbatim and section 2 says how to use them. The writer card reads them instead of FICCVoice.md in full.
- references/dispatch-notes.md: new section 6, outline slices (the default since 2026-11-03). Patch packets name their excerpt. A recheck covers the changed-sentence table, and number_set_diff.py runs before any re-tick. Rulings are batched per stage.
- references/clarity-acceptance.md adds V57, C24 and H6, and the “！” rows cite V36 and V19. compose-excerpt.md adds C24. glossary.md covers C01–C24 and adds `标题级反驳席`. format-and-maintenance.md defers to clarity-acceptance.md.

Hand (`skills/ficc-hand`):

- FICCHand.md 3.1 ⑥, task roles. The trunk question (主干问题) governs evidence, main judgments, outline and acceptance. Explicit must-answers (明确必答项) keep their delivery duty. Hint branch questions are exploratory leads (探索线索) that owe no answer or section of their own. Critical dependencies (关键依赖) are checked against the originals first. Leads and sparks share one ranking, and T0's own `[explore]` questions stay off it. Sections 3.2–3.8 carry the roles through, and the red team is dispatched as `refuter-t1e`.
- references/handoff.md: fields 1, 6 and 12 are extended. A new section 2.1 maps every field of the handoff note to the seven-block stage-handoff state card. A trial line names `ficc-conductor`.
- references/map-template.md: the question tree gains columns for task role, use for the trunk, destination in the text and ordering reason. report-skeleton.md, outline-from-research.md, materials-manifest.md and digest-extra-fields.md carry the roles. cost-estimate.md adds T0 at long context, updates of a previous version, a worked example and the ledger command.

Agent cards:

- ficc-outliner: build reads FICCOutline.md 1–4 and 7–8 (7.3 only when summarizing); check reads the outline view; O91 applies in every mode.
- ficc-writer: polish reads voice-excerpt-polish.md, draft adds voice-excerpt-draft.md, patch reads voice-excerpt-patch.md, cold-read reads voice-excerpt-coldread.md; rechecks read only the changed range.
- ficc-structurer and ficc-composer work from the outline view and node slices. ficc-mapper copies task roles into the question tree and never infers them.

Scripts (`skills/ficc-voice/scripts`, see its README.md):

- voice_check.py 4.3 → 4.5: H9, nominalized views (V57), is a review candidate under `--clarity`, narrowed in 4.5. The `不是……而是` and `段末升华` density rows list each hit's line (`density_hits` in `--json`).
- xref_check.py checks the four voice excerpts against FICCVoice.md, and the C numbers in section 3 of compose-excerpt.md against C23 (`--selftest-excerpt`).
- cjk_space.py skips .tsv, .csv, .json and .jsonl files and keeps TAB gaps in Markdown table rows.
- New: outline_slice.py (node, chain, names and view slices of an outline); budget_check.py with budget.json (character caps for the rule and excerpt files); changed_sentences.py (the changed-sentence table for a recheck); number_set_diff.py (number tokens of the frozen and the current draft before a re-tick). changed_sentences.py and number_set_diff.py import sentence_diff.py from shared-protocols, which is not included.

## 1.0.0 (2026-10-18)

First public release of FICCWriting, a set of five skills for writing Chinese FICC prose with Claude Code. Hand (ficc-hand/FICCHand.md, card ficc-mapper) comes first and forms the views: from a topic and a corpus it delivers a view outline, whose tree ficc-outliner builds, and a materials index. It ships in `skills/ficc-hand` and depends on skills that are not included. The writing relay follows. Outline (FICCOutline.md, card ficc-outliner) builds the outline tree and decides where each story or change sits. Structure (FICCStructure.md, card ficc-structurer) judges the relations between nodes and issues the relation sheet. Compose (FICCCompose.md, card ficc-composer) organizes the paragraphs inside a settled node. Voice (FICCVoice.md, card ficc-writer) settles sentences and wording. These four ship in `skills/ficc-voice`, whose SKILL.md routes the relay.

Licenses: the scripts (everything under `skills/*/scripts/`, plus `install.sh` and `uninstall.sh`) are under the MIT License; everything else (rule files, references, agent cards, README, docs) is under Creative Commons Attribution-NonCommercial 4.0 International. The corpus and the quoted letters, reports and drafts are published with the owner's permission under the same CC license. See `LICENSE`.
