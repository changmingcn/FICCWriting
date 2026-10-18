# Relation sheet template

The relation agent (ficc-structurer) writes the relation sheet it hands to the composer (ficc-composer) and the writer (ficc-writer) per FICCStructure.md 9; the criteria there govern. This template is the single definition of the relation sheet's fields. The relation sheet records only relations: for each relation, answer at least which two items, what relation, on what grounds it holds, and what limits it has. Record a simple, clear relation briefly in one line; do not fill in a table for every sentence. Write one section for each affected node the outline agent (ficc-outliner) lists in the placement record; when first building the whole tree or when there is no new placement, write directly from the outline and the original material. Relation lines and annotation lines go to the outline agent, who writes them into the outline. A new node not yet built keeps its temporary number from the placement record; the drafting seats read the sheet against the number map made once the changes are carried out. The three fields of the former part 2, writing instructions, paragraph-opening and sentence-start markers, and writing advice, were deleted on 2026-10-17: how paragraphs open, carry over, and close belongs to FICCCompose.md, specific wording to FICCVoice.md, length and full-statement places to the outline.

## 1 头部 (header; one per relation sheet)

- 写作单元： (writing unit) which nodes this unit includes. Length and full-statement places follow each node's “展开：” (unfolding) line in the outline (FICCOutline.md O44, O51); do not copy the cap or the counting method. Where an unfolding line gives no cap or full-statement place, list that here as a to-do for the outline agent; do not fill it in yourself.
- 名字表： (name table) write “照提纲头部的名字表” (per the name table in the outline header); do not list names separately. For each name missing from the table and each thing that has two names, write one line, `<东西>：<在哪个节点看到的说法>`, and list it as a to-do for the outline agent, passed on through T0.

## 2 节点 (node: number and claim line)

For each relation, write the endpoints, the type from the relation library, the grounds, and the limits or open items. A limit states a semantic constraint downstream must not change, for example “只是并列，不写成因果或递进” (only parallel; do not write it as cause and effect or progression).

### 2.1 对上关系与下级展开 (upward relation and downward unfolding)

How it unfolds the parent node: which relation-library type, which arrangement (trunk group, chain, satellite), on what grounds. How its child nodes unfold it, and whether together they complete this node's task. Limits or open items.

### 2.2 同层关系与顺序理由 (same-layer relation and reasons for order)

With which sibling node, through what content, what relation it forms, on what grounds, with what limits. For the seam's complex-sentence relation, write the row name from references/connectives.md section “现行连接词表” (current connective table), such as 因果·推断 or 转折·让步; do not write the wording. Confirm the reason in the outline's order line; if it does not hold, write a placement objection (`安放异议`) and hand it to T0 to pass to the outline agent for a ruling; this sheet does not change the order.

### 2.3 跨枝呼应 (cross-branch links)

Which distant node it has an echo, foreshadowing, contrast, or dependency with, through what content, on what grounds; under which node the annotation goes on the outline. How foreshadowing is written where it is planted and where it is revealed belongs to the composer (FICCCompose.md C15).

### 2.6 事实 (facts)

Cite facts and qualifiers by materials-index number, placement record, or material position; do not copy them. One line each: `<位置>｜事实／解释／推测｜问题号（有争议或待裁时写 I-nn，与账本同号）`. Put each fact to be verified on a line of its own, noting that it does not go into the body text. The packet must attach readable source excerpts and qualifiers (who, what they did, what is counted, period, unit, qualifier); do not give only a path.

### 2.7 作者原句 (author's original sentences)

For each original sentence marked 〔作者亲写·逐字〕 on the outline, write its node number on the outline; do not copy it. If there is none, write “无” (none). The packet must attach the original text of the sentence; do not give only a path.

## 3 写进提纲的两种行 (the two kinds of line written into the outline)

The relation agent provides relation lines and annotation lines; the outline agent writes order lines itself, and they are not in this sheet. Both kinds of line, with the nodes they belong to, go to the outline agent to backfill into the outline; the format here governs. The relation agent does not edit the outline directly; lines for nodes not yet built stay in this sheet for now:

- Relation line: `关系：和<节点编号>，通过<什么内容>，是<关系库里的哪一类>`.
- Annotation line: `标注：<呼应／伏笔／对照／依赖> <节点编号>：<通过什么内容>`. When a story is cited elsewhere, add `标注：回指 <主要位置的节点编号>` at the place that cites it.

## 4 其他节点待办 (to-do items for other nodes)

One line per item: which node, what to change (the step the parent node's carry-over gives it, the sibling nodes' linking-back sentences, echo sentences elsewhere), and why. Hand them to T0 to route; do not require a separate agent round for each item.
