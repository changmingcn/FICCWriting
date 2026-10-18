# Dispatch details

T0 reads this when dispatching, as needed. Moved out of SKILL.md on 2026-10-17; the original sentences were only shortened, none deleted. The relay table and the acceptance table are in SKILL.md 2–3. Below, “writer” means the seat that drafts this node's body text: for a new draft, composer then writer; for a short piece, writer draft; for a wording-only edit, writer patch.

## 1 packet

1. The COMMON packet is the shared packet head for all writers in the same round; a unit packet writes only what differs for its unit. Merge general rulings into the COMMON packet.
2. T0's rulings file has one section per unit number. A packet points only to its unit's lines and to the general rulings.
3. A ruling lists all known places where the same judgment lands (body text, headings, figure notes, change tables), and the subject, period, sample, and attribution of inference that must be kept. Within a node, fix the same confirmed defect in one pass.
4. A literal replacement whose old sentence, new sentence, and file are all settled is not dispatched to a writer. Merge the whole round into one patch packet (dynamic-workflow references/artifact-schema.md, Packet file), or send it to the owner who is still online.
5. For check and fix rounds, T0 attaches this round's rule excerpt (section number plus original text) to the COMMON packet; writers do not read the full rules. To organize the paragraphs of a whole node, read FICCCompose.md in full; to polish, read FICCVoice.md in full; otherwise follow each card's mode table.
6. Placement records and relation sheets go in the task directory, file names `安放记录-<编号>.md` and `关系单-<编号>.md`.
7. The packet must attach the material excerpts and qualifiers this node uses (who, what they did, what is counted, period, unit, qualifier) and the original text of the 〔作者亲写·逐字〕 sentences. Relation sheet 2.6 and 2.7 record only positions; T0 extracts the original text by position and attaches it, and must not give only a path.
8. Short-piece merged mode: for a short piece (body text ≤600 Chinese characters, counted per O44, whatever the node's layer), dispatch one writer draft seat to do relay steps ④⑤ together, reading references/compose-excerpt.md first and FICCVoice.md after, with no separate paragraph draft. A piece with child nodes, a section-level carry-over, or the whole piece's close also reads FICCCompose.md C04–C06 and C17–C19. A longer piece reads FICCCompose.md in full first. The result sheet lists truthfully the rule files and sections actually read. For a wording-only edit, dispatch writer patch, step ⑤ only; holding two roles does not widen authorization.

## 2 Writing units and to-do items

1. Outside this node, the writer changes only the table of contents and references (section numbers, headings, and back-reference names elsewhere that point to this node, the few characters in echo sentences that refer to this node, and bibliography entries). Body text elsewhere that must change goes on the to-do list; T0 routes the to-do items to that node's owner, and they may be merged into that node's next round, so each item need not get a round of its own. Each round still writes only that one node.
2. If maintaining the outline substantively changes a settled claim, content, or order, T0 dispatches the structurer to add the affected relations. Work that only carries out settled decisions or only aligns numbering (node numbers) is not judged again.
3. A return note states at least the location, the specific conflict, and the decision needed, and goes into the existing to-do lists (result-sheet to-dos, relation sheet 4, placement record 5); do not set up a separate ledger. Whom to return to: per SKILL.md 3. Recheck by the affected range; when an upstream change affects the whole text, check the whole text. When dispatching composer check, attach the previous check result.

## 3 Sweep-edit mode (optional)

Usable in rule sweep-edit rounds and revision rounds. A script first locates the hit sentences; set the granularity by the hit count: one writer per piece, or per three to five units. The writer holds the list of hit sentences, this round's rule excerpt, and one outline excerpt per unit (name table, this node, the adjacent nodes' conclusions, this node's rows in the relation sheet). Node permissions do not change; record diffs by node. On first use, trial it on one piece only and keep another piece on the old way as a control; record each piece's cost per round, the counter-view seat's fix-level finding rate, and the share marked “本轮引入” (introduced this round).

## 4 Pacing

1. Syncing relation lines and annotation lines (backfilling after rulings) may be batched until the user wants to see the outline, or done once a day. Outline changes the writer needs before drafting (nodes, claims, order) are still made at once with each change.
2. At the end of a campaign, build and upload only once.
3. Run the scripts only once at the writer's node level and once before submission. The seat that checks clear expression reads the script output in the writer's result sheet and does not run the scripts again.
4. For a node with a source list, the source-check seat also checks every “institution + date” in the body text against the list, item by item.

## 5 Supplements on relay and rulings (expanding SKILL.md 4)

1. After relay step ③, outliner maintain backfills relation lines and annotation lines per the relation sheet. A new node uses the same temporary number in both records; the outliner hands back the temporary-to-permanent and old-to-new number maps, and T0 passes them to the writer with the relation sheet.
2. Collect comments from trial pieces and new rules into one batch, install it into the rule files, then do one unified revision round.
3. Owners of to-do items: placement, selection, order, and length belong to the outliner; relations to the structurer; paragraph organization to the composer; sentences and wording to the writer.
4. When a fact the placement record keeps really must be deleted, the outliner reviews the placement again within the selection range the task allows, and then the structurer adds the affected relations.
5. The counter-view seat catches heading-level overstatement: a wrong time window, a model's upper bound written as a finding, our inference written as the source's claim. Neither the cold read nor the tie-out catches these.
6. Run the two pre-submission scripts per references/clarity-acceptance.md. Judge review candidates by meaning; do not spoil an accurate expression to clear a flag. After changing a heading or section number of the four rule files, run scripts/xref_check.py before installing.
7. The author's model texts, references/exemplars.md, are kept for reference; no need to compare against them. Grounds, audits, and history, references/dev-notes.md, are not read for daily writing. FICCVoice's sources and maintenance record: references/FICCVoice-provenance.md. The glossary is references/glossary.md.
8. The writer may have a style of its own.
9. Update an existing draft in place by its stable Doc ID. Make HTML, PDF, or Word only when the user asks. When the user wants only the article, do not attach writing notes, self-assessment, or generic disclaimers.
10. Rule numbers V01–V40, S01–S96, O01–O90 are frozen. Rules moved from FICCStructure.md 6–8 into FICCVoice.md are numbered after V40, with pointers left in place in FICCStructure. On 2026-10-17 the paragraph-organization rules moved into FICCCompose.md with their own C numbers (C01–C23), pointers left in place, old numbers not reused; map: references/migration-2026-10-17.md.
