# Handoff: FICCHand to ficc-voice

## 1 What is handed over

| File | What it is | Who maintains it |
|---|---|---|
| `<文稿名>-提纲.md` | view tree, FICCOutline format, unfolded to paragraph groups; order lines only; relation lines wait for ficc-voice's relation sheet | ficc-outliner (builds it at Hand step 5b, maintains it per FICCOutline after handoff) |
| `<文稿名>-资料索引.md` | index of main materials and data; its head is this handoff note | after handoff, append only and do not change old rows; mark a changed row “已改，见新行” |

Working files are not copied with the handoff; section 9 of the index gives their paths.

## 2 Handoff note (written in section 0 of the materials index)

This section is the only definition of the handoff note's fields.

1. `决策问题与根主旨` (decision question and root claim): one sentence; time window, data cutoff date.
2. `两份文件的路径` (paths of the two files).
3. `当前生效的用户裁定清单` (list of the user rulings currently in force): section number or node number + original text; overturned rulings are not listed. A ruling that changes the strength of a judgment is written as “全文凡……”, so that the writer searches the whole text, not just a list of line numbers.
4. `生效的登记行` (register rows in force): `SUPERSEDED.md` line number, keys, now.
5. `已在提纲上定好的项` (items already settled on the outline): the choice of measurement bases and indicators, data windows, the name table, the change worksheet; items not yet settled are listed as open questions; node positions follow the tree ficc-outliner built, and the index's “提示节点” are hints only. The format of the change section is fixed as two columns “旧版原话｜新说法”; the section opening states which items changed the conclusion and which changed only the degree.
6. `开放问题与待核实` (open questions and items to be verified): numbers in section 8 of the index.
7. `top spark` (top spark): one line: the best anomaly or opportunity, the cost of probing it, what it would change (research-agent/SKILL.md (Before you send)).
8. `最可能错的一条判断和最便宜的检验` (the judgment most likely to be wrong and the cheapest test of it).
9. `验收记录` (acceptance record): the paths and conclusions of the three results (outline check, tieout, counter-view), one line each.
10. `出口` (exit): whether the task's acceptance goal is the research outline only or a finished draft (per the acceptance items of `work.py define`). Outline only: settle after verifying delivery; finished draft: record “研究阶段已完成” (research stage complete), do not settle, continue along the original task goal into ficc-voice, and settle after the finished draft is delivered.
11. `ficc-voice从哪一步接` (the step at which ficc-voice takes over): per section 3.

## 3 Where ficc-voice takes over

Take over at step 3 of the relay table in ficc-voice/SKILL.md (judge relations, issue the relation sheet). The outline has already been checked by ficc-outliner in check mode (FICCOutline 9); do not rebuild it. The finished draft passes through ④ paragraph organization (ficc-composer) and ⑤ sentences and wording (ficc-writer); for a short draft one ficc-writer seat does ④ and ⑤ in a row.

This skill changes no file of ficc-voice.

## 4 After handoff

When a user correction of a view or new material changes a judgment: change the tree first (FICCOutline 6.2, owned by ficc-outliner) and do not go back to FICCHand to rerun; changing the tree is more than changing the table of contents and the wording; reopen the affected evidence and conclusion checks per shared-protocols/source-check.md (Validity of a check; Reread on a changed binding), and do not build a separate process; only when the decision question itself has changed, go back to FICCHand and start again from framing.
