# Placement record template

The outline agent (ficc-outliner) writes the placement record per FICCOutline.md 5; it decides and carries out placement and selection, and the relation agent (ficc-structurer) writes the relation sheet for the affected nodes in part 1. This template is the single definition of the placement record's parts. For simple material, write only the parts that apply.

## 1 安放结论 (placement conclusion)

Whether to place it; at which node (write the node number); as a branch of its own, or embedded in, replacing, or merged with an existing block. If it cannot be placed, write whether it is set aside or discarded, and why. When deleting existing facts, state item by item which ones. The last line lists the affected nodes: number and why each is affected; the relation sheet is written node by node from this line. A new node not yet built uses the same temporary number in both records.

## 2 材料价值 (material value)

What it provides, with facts, interpretation, and speculation written separately. For each fact, state in full who, what they did, what is counted, period, unit, and qualifier; mark a disputed or pending item with its question number (write I-nn, the same number as in the ledger, `ledger.md`). What it adds beyond existing content: information, understanding, evidence, or a change in the narrative. Copy author-written sentences verbatim from the original and mark them 〔作者亲写·逐字〕.

## 3 结构理由 (structural reason)

What task it does for the layer above. When positions are in dispute, list two or three candidate positions with each one's role and cost, write why this one was chosen, and why each rejected one does not work.

## 4 修改后的局部提纲 (revised partial outline)

State what the decision changes things to, as changes still to be carried out; writing the record does not mean the outline file has been changed. List only the affected parent nodes, sibling branches, and necessary lower nodes; for each node, write per FICCOutline.md O31 the claim line and the four lines task, order, relation, and unfolding (the relation line waits for backfill from the relation sheet). List the whole piece only when the overall structure changes. The outline agent carries the changes out itself and then hands back the temporary-to-permanent number map; when existing nodes are renumbered, it also lists the old-to-new number map; T0 passes these with the relation sheet to the drafting seats (composer, writer). When a settled claim, content, or order changes substantively, state the change and send it to T0 for the relation agent to add the affected relations.

## 5 待核实或待补充 (to be verified or to be supplied)

Facts still to be verified, material still to be supplied, and structural problems not yet solved; mark each “待核实” (to be verified) or “待补充” (to be supplied).

## 6 内联席字段 (inline-seat fields)

Written by the outliner when the inline seat drafts or patches (dispatch-notes.md 7): one `### <node number>` section per node, one line per field, markers verbatim with the full-width colon, because the packer reads them as written. A field with nothing to say reads 无.

- 底稿 (base text): `底稿：<draft name> <heading>｜L<start>–L<end>`, by line range, never by heading; a new node: `底稿：无`.
- 来源 (source text): `来源：<source name> <section>｜L<start>–L<end>`, several joined by ；.
- 带入 (carry-in): each new fact with institution and date, as it may appear in the body.
- 更新 (update): base-text statements to bring up to date, with the current wording and its date.
- 保留 (keep): what stays, 〔作者亲写·逐字〕 sentences and analogy limits included.
- 不写 (do-not-write): what this node leaves out, and which node holds it.
- 上限 (cap): `上限：N字`, or `上限：见提纲` and the packer reads the cap from the node's unfolding line in the outline.
- 伏笔 (foreshadow): the thread taken from the previous node and the one left for the next.
- 必改句 (must-change sentences): one line each, `原句 → 现行说法` (base sentence → current wording), for base-text sentences that contradict a current judgment.
