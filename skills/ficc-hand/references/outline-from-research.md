# Building the outline from FICCHand research

For ficc-outliner at FICCHand step 5b, when the packet names this file. It adds to FICCOutline.md, which governs where they differ. Moved from the ficc-mapper card's outline mode, 2026-10-17 (user: only ficc-outliner builds the tree).

## Inputs

- `立论.md`: the parent's ruled views (leading view, what is adopted and what only contrasted, the strength of each judgment).
- `brief.md`: the trunk (decision) question, the explicit must-answers (明确必答项) with the delivery place each asks for, and the exploratory leads (探索线索).
- The map (`脉络图`), the ledger (`ledger.md`) and `<文稿名>-资料索引.md`.
- `~/.claude/skills/ficc-hand/references/report-skeleton.md`: the default tree. Start there, then grow by content.

## Build `<文稿名>-提纲.md`

Organize the tree by the argument of `立论.md`, not by the question tree's order or rows: a node carries retained findings, necessary background or contrast, or the content an explicit must-answer requires; a map row whose 成文去向 is 仅工作记录 gets no node; a lead's finding enters only when it serves the answer, where the argument needs it: a trunk step, its own level when it can change the root claim, or a 支线发现 (branch finding) under the step it serves; each explicit must-answer gets the place `brief.md` names (its own node, an appendix before the source list, or a named node). Never infer must-answers or the number of sections from map rows.

Name table per FICCOutline O32–O34; node lines per O31; depth per O24 (to paragraph groups); order per O18. Research adds:

1. Head: the decision question in the user's words, the explicit must-answers and where each is delivered, time window, data cutoff, what this pass may add. The root claim (`主旨`) answers the decision question, with confidence and its limiting link.
2. Name-table (`名字表`) rows come from the confusables section of the map.
3. Each claim states a view the parent ruled, at the strength `立论.md` fixes: time windows matching the data; model results as ranges with the model named; one-house findings attributed; degree words (创新高, 仍, 几乎, 主要) only where the source says them; no causation that neither a parent ruling in `立论.md` nor the evidence supports (a research inference the parent approved stays, marked with whose it is, its grounds and its conditions); “材料没说” never turned into a denial.
4. A disagreement `立论.md` does not rule: state it per O21 and put the node on the open-question list.
5. Order line (`顺序：`): the ordering reason (O18), taken from the question tree's 成文排序依据 column where the node maps to a question-tree row, otherwise written per FICCOutline 3.1; never a bare `Q<id>`. Leave the relation line (`关系：`) empty until ficc-voice's relation sheet fills it; write no relation types or annotation lines.
6. Each node's unfolding line (`展开`) lists the index ids it uses (E, Q, F), adopted apart from contrast-only (“采纳：E12、E15；对照：E20（Citi）”); every leaf has them.
7. Node ids N-prefixed only; line numbers of other files go in backticks.
8. Carry register rows' `now` (line number + now text) under the nodes that use them. Mark the author's own sentences 〔作者亲写·逐字〕 and droppable nodes 〔可舍〕 at the end of the claim line.

## Before handing back

- Headings: check per FICCOutline.md O81 (with `--names <提纲文件>`).
- Run `python3 ~/.claude/skills/ficc-hand/scripts/tieout.py --outline <outline> --against <index> <ledger>`; fix or list every miss. Exit 3 (未检查) means a claim line or the name table is in a form the script does not read, or a token is ambiguous (待核): fix the markup or resolve the token and re-run.
