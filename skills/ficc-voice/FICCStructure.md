# FICCStructure: Judge relations

This file governs relations between nodes, from the whole piece down to complex sentences: rules, boundaries and checks only. The relation agent (ficc-structurer) works on the living outline `<文稿>-提纲.md` after the outline agent (ficc-outliner) grows the tree. It rules each relation's type and whether it holds, writes the ruling into the relation slots (§6), and names a seam by its references/connectives.md row, never by wording. Where a relation does not hold, it returns a placement objection (`安放异议`) to the outline agent through the lead; it neither changes the tree nor decides placement (FICCOutline.md 5). Arrangement verbs (hang, re-hang, split, merge, move) name an objection's content. “The user” is the author; “you” is the agent applying the rule.

## 1 Relation library: what to judge relations with

### 1.1 Twenty-one relation types

- **S01** **Find the relation between nodes among the twenty-one types.** The table serves every scale from chapters to sentences, and sets of stories, points, evidence, scenes, perspectives, steps or concepts.

| Relation type | Concrete forms and functions |
|---|---|
| Classification and division of labor | Split the task by aspect, object, stage, cause, and so on; state the basis of division |
| Complementarity | Use different perspectives, scales, or materials to make up for the limits of a single part |
| Overview and unfolding | Overview–detail, whole–part explanation, abstract concept–concrete manifestation |
| Induction and synthesis | Form a common pattern, an overall judgment, or a new understanding from several cases or several analyses |
| Explanation and clarification | Define concepts, explain meanings, describe mechanisms, remove ambiguity |
| Assertion and support | Support a judgment with reasons, facts, and evidence |
| Grounds and inference | Start from existing information or premises and form a new judgment |
| Cause and mechanism | Explain causes, processes, and results, and any feedback loops that may exist |
| Conditions and limits | Make clear the conditions for holding, the scope of application, exceptions, and reservations |
| Progression and deepening | Advance understanding step by step, from surface to depth, from simple to complex |
| Premise and dependency | First provide the concepts, knowledge, preparation, or methods that later content needs |
| Comparison and contrast | Analyze similarities, differences, relative merits, or changes on a shared dimension |
| Analogy and transfer | Understand an unfamiliar object through a familiar one, or examine whether a method can be used in a new situation |
| Objection and response | Present objections, analyze counterexamples, respond to doubts, test and revise judgments |
| Problem and solution | Move from finding and diagnosing a problem to proposing, testing, and evaluating solutions |
| Goals and means | Connect purposes, ways of achieving them, and evaluation criteria |
| Choice and trade-off | Present different paths, and state the selection criteria and the reasons for the trade-off |
| Time and space | Organize content by sequence, simultaneity, flashback, position, movement, or observation path |
| Setup and payoff | Posed question–answer, foreshadowing–reveal, promise–fulfillment |
| Echo and variation | Create new meaning through the recurrence and variation of themes, images, or situations |
| Pacing and mood regulation | Adjust the reading experience through tension and release, density and openness, scene and summary |

### 1.2 How to use it

- **S02** **When you identify a relation type, state in full which item relates to which, through what content, and what relation it forms.** Relations may overlap and cross levels; choose by actual content, not to cover every type. A label is not a relation: if you cannot state all three, it is not yet identified.
- **S03** **When relations overlap, decide the arrangement by the satellite test (S08).** Seam layer: S29. Sibling relations and re-hanging: §3. Carry-over and transition are positions, not library types (FICCVoice.md C04, C13).

### 1.3 Six distinctions

- **S04** **Before using the relation library, distinguish the six most error-prone points.**
  1. Cause and inference: cause and mechanism explains why something happens; grounds and inference, why a judgment can be drawn (seam markers: S18).
  2. Progression and premise: progression goes one step beyond the earlier block; premise and dependency supplies what later content needs and comes first (2.2, 2.3).
  3. Example and proof: one case may illustrate or support, but does not by itself prove a general judgment.
  4. Synthesis and repetition: synthesis says what the parts jointly show, never restates them; a close applies this (FICCVoice.md C17, C19).
  5. Analogy and transfer: state the dimension of similarity and where application stops; surface likeness transfers no conclusion.
  6. Relations and connectives: turns, progressions and causes must hold in content. If you cannot identify the relation, change the content, never add a word (§3, FICCVoice.md V13).

### 1.4 How the relation library connects to arrangements and seams

- **S05** **First judge how the child nodes unfold the parent node. The unfolding decides the arrangement.** Type one, the blocks together make up the parent: a trunk group (S11). Type two, step by step they reach it: a chain (S13). Type three, the parent holds alone and the children only give evidence, examples, explanation, limits, background, counter-views, contrasts or an evaluation of the material: satellites on the step they serve (S14).
- **S06** **The table below only suggests common arrangements and complex-sentence relations. The satellite test (S08) and the diagnostic questions (S18) decide.** The seam column governs the paragraph level and below; above section level, mark relations by position, carry-over paragraphs and linking-back sentences (FICCVoice.md C04, C14).

| Relation type | Common arrangement | Complex-sentence relation at the seam |
|---|---|---|
| Classification and division of labor | Trunk group, one basis of division per group (3.2) | Parallel; from the second item on, mark the add-on relation |
| Complementarity | Trunk group, unfolded by different aspects (3.3) | Parallel (different aspects); progression when the supplementing block goes one layer further |
| Overview and unfolding | The overview sits in the parent node; details that together make up the overview form a trunk group; a single concrete manifestation given for an abstract concept is a satellite | Explication; between details, parallel or sequence |
| Induction and synthesis | Write it in the parent node's claim or close; do not list it as a separate block (2.2, FICCVoice.md C17) | Cause and effect · inference |
| Explanation and clarification | Satellite, hung on the statement it explains | Explication; cause and effect when it describes a mechanism |
| Assertion and support | Satellite, hung beside the step it supports; for argument between siblings, see 3.5 | By position, following the step it supports; giving reasons is cause and effect, giving evidence is explication; premise first and judgment after is cause and effect · inference (1.3 item 1) |
| Grounds and inference | Chain | Cause and effect · inference |
| Cause and mechanism | Chain; with parallel channels or feedback, choose one route the reader can follow (2.3) | Cause and effect; sequence when the mechanism goes step by step |
| Conditions and limits | Chain when the consequent is the parent claim itself; satellite when it limits only one step, following the judgment it limits | Condition, supposition, turn · concession; a light turn when it is only a mismatch |
| Progression and deepening | Trunk group ordered by degree, or a chain | Progression; when written as parallel, mark the add-on relation (emphasis, deepening) |
| Premise and dependency | Chain, premise first; a single background premise is a satellite, placed before its first use (FICCOutline.md O53) | Sequence; cause and effect · inference |
| Comparison and contrast | Trunk group, arranged as a paired contrast, with the shared measurement basis stated first; another period or market used only as a reference is a satellite or goes to the appendix (FICCOutline.md O53) | Parallel (paired contrast); turn |
| Analogy and transfer | Satellite, hung on the step it explains | Explication; condition for the limits of application |
| Objection and response | Chain (question, answer, concede a step, turn back); a trunk group as a paired contrast when both sides enter the parent claim; a counter-view that limits only one step is a satellite (FICCOutline.md O53) | Turn, turn · concession |
| Problem and solution | Chain | Sequence, cause and effect · purpose; for a posed-question opening, see FICCVoice.md C01 |
| Goals and means | Chain; a trunk group when several means stand side by side | Cause and effect · purpose |
| Choice and trade-off | Trunk group; once the trade-off is made, the core is the chosen item | Alternative |
| Time and space | Trunk group, ordered by time or position (for stages, see 3.3) | Sequence; topic frames for position |
| Setup and payoff | Chain (posed question–answer, promise–fulfillment); a distant foreshadowing–reveal becomes a `关键边表` edge (§5) | Sequence; for preview and payoff, see FICCVoice.md C20 |
| Echo and variation | A `关键边表` edge (§5); the arrangement does not change | Parallel · add-on relation (repetition); for back-reference and parallel syntax, see FICCVoice.md V23, V25 |
| Pacing and mood regulation | No set arrangement | Not marked at seams; for sentence patterns, see FICCVoice.md V11, V25 |

## 2 Vertical: what a node does for its parent

- **S07** **Before hanging a block, state what it does for the parent node.** Name what it concretely expresses and how it helps the parent complete its task.

### 2.1 Three arrangements

- **S08** **Separate satellites from the trunk with the cover test.** Cover the block (`遮住测试`) and reread the parent's claim sentence, not its evidence list. If the claim loses part of its answer, the block is trunk; if it loses only support or qualification, it is a satellite. The test sets arrangement, never deletion. A node with only satellite children states its own conclusion.
- **S09** **Tell a story through layer-by-layer progression as far as possible.** Same-layer items that can form one deepening line (shallow to deep, appearance to cause, general to specific) are arranged as that line; lay them flat as parallel only when none goes a step beyond another (S22).
- **S10** **Between sub-points in the same layer, first judge the actual relation, then decide how to write it.** Same-layer branch lines stand in eight relations: turn, supposition, parallel, progression, alternative, cause and effect, condition and sequence (here the 承接关系, sequence relation, not 承接 as the carry-over position). Stages and aspects: S26. Arrangement and core: the S06 row. Marking: §3.

### 2.2 Trunk group

- **S11** **A trunk group keeps four rules: same kind, ordered, an extra layer when items are many, and one extra sentence in the parent node.**
  - Kinds: parallel and enumeration, sequence and stages, alternative, paired contrast, different aspects, progression by degree.
  - Same kind: one basis of division (S24) and comparable granularity (abstraction, not length). Compare subjects on comparable dimensions; each subject's particular issues go back under it.
  - Ordered by how the group formed: steps to a result by time, parts of a whole by structure, like items by degree. Definitions before use, premises before what depends on them, the shared measurement basis before a comparison (stated once: FICCVoice.md C11; inside a sentence: FICCVoice.md V29). Rest one question before the next. Advance by fund flow, time, participants or questions; state any change of ordering basis, and never mix company, time and bullish-versus-bearish order in one group.
  - More items than the reader can hold: add a layer (S25).
  - With no core of its own, the group needs one parent sentence on what the items show together, never only “有三点” (there are three points).
- **S12** **Make each kind of trunk group show what it needs to show.** Parallel: the shared question. Progression: the added step. Alternative: the grounds for the trade-off. Stages: where each starts and turns. Aspects: that together they answer one question. Repeated openings as item markers: FICCVoice.md V25.

### 2.3 Chain

- **S13** **Mark every link of a chain. The chain's conclusion is the parent node's claim.** A chain is a set of children where each step depends on the previous (deductive, causal, inferential, conditional); link relations may differ. An argument node is a chain by default: question, answer, concede a step, turn back, conclusion, one marker per link. For sections, induce the steps first. Choose one route the reader can follow, never presented as the only causal chain (mechanism and unproved steps: FICCOutline.md O13–O15). Consequences go in cause and effect, conclusions in conditions, members in classifications; when material changes use, say so.

### 2.4 Satellite

- **S14** **Hang a satellite beside the step it serves. Do not set it side by side with the trunk.** It need not match the trunk's kind; state what it does for the trunk and which type-three unfolding (S05) it is. Measurement bases follow comparisons, qualifiers follow judgments, evidence follows its statement. Never change the company basket and the gross or net basis at once while “从……到……” (from… to…) reads as one series.
- **S15** **A satellite may unfold layer by layer, as deep as the content requires.** Paragraph organization: FICCVoice.md C16.

## 3 Horizontal: 接前 and the relation to sibling nodes

- **S17** **For horizontal relations, look first at sibling nodes under the same parent node.** Siblings are one parent's same-level children (“same-level” and “same-layer” below mean them): how they divide work, their logical relation, why this order, whether they echo. Structural siblings may stand in cause and effect, progression, argument or rebuttal, not only parallel. An adjacent pair's ruling goes in the later sibling's `接前` row (S77).

### 3.1 Identify the relation first

- **S18** **Judge the relation before choosing words. The answer to the diagnostic question decides which class of word to use.**
  - Put the two sentences or blocks together and go through the table row by row (library mapping: S06). The class goes into `接前`; which seam to mark: FICCVoice.md V22.
  - A causal or inferential class (因果, 因果·推断, 因果·目的, or a dependency) needs `凭：@<原件锚点>`, a source sentence linking both items. Without one, rule the class the source does carry (often 承接关系), put the causal reading in `下游禁改边界`, and send a contested seam to the `关键边表` as `待据` (S74).
  - A question with no answer means the two are not in one layer, or the thinking is unclear. Mark each item fact, expectation or supposition; a relation type alone does not show a purpose achieved or a condition met (S28).

| Relation | Diagnostic question (if “yes”, assign this class) | Statement order | Fact status |
|---|---|---|---|
| 并列 (parallel) | The two items are of the same kind under the same basis of division; equal weight is not required | Swappable: after a swap they are still the same group and lose only the order; if a swap loses a step, it is 递进 | — |
| 并列·附加关系 (parallel · add-on relation) | The later item follows on (承接, carry-over), returns to the earlier one (反复, repetition), sharpens it (强调, emphasis), or goes one layer deeper (深化, deepening); mark it above the parallel relation; it is not a ninth relation; emphasis and deepening = progression written in parallel form, arranged as in the progression and deepening row of the 1.4 table | The later item rests on the earlier one | — |
| 并列·解说 (parallel · explication) | The later item explains, illustrates, or restates the earlier one; then the later item is most likely a satellite of the earlier one, hung per 1.4; it counts as parallel only when the two items truly sit in the same layer | The explaining item follows what it explains | — |
| 承接关系（先后） (sequence) | The two items have a temporal or logical order that cannot be reversed | Fixed; coming first in time does not by itself make a cause | — |
| 递进 (progression) | The later item goes one layer further than the earlier one in scope, quantity, degree, or time; without the earlier item, the later item's weight changes | Fixed; a swap loses the added step | — |
| 转折 (turn) | The later item turns to an opposite or contrasting meaning; opposed meanings are a strong turn, a mere mismatch is a light turn; mark a light turn as usual, and do not substitute a re-mention of earlier text (FICCVoice.md V22) | The turned-to meaning comes second | — |
| 转折·让步 (turn · concession) | First grant or suppose something, then say the result is unaffected by it; granting a fact is a factual concession, supposing is a hypothetical concession, “怎样都一样” (it is the same either way) is a total concession | The granted or supposed item comes first | Factual concession: the granted item is a fact; hypothetical concession: it is only supposed |
| 因果 (cause and effect) | The earlier item is an objective cause of the later item | Usually cause first; a “因为” (because) clause may follow its result | — |
| 因果·推断 (cause and effect · inference) | The earlier item is a premise the reader already accepts, and the later item is a conclusion the text draws from it | Premise first, then the conclusion | — |
| 因果·目的 (cause and effect · purpose) | The earlier item is done in order to obtain the later item | Either order | — |
| 假设 (supposition) | The earlier item is only supposed, not asserted | Supposition first | The earlier item has not happened, or may never happen; what follows from it is not later cited as fact (S28) |
| 选择 (alternative) | Choose one among several possibilities; an open alternative when not yet decided, a settled alternative when the trade-off is made | Options side by side | — |
| 条件 (condition) | When the earlier item is met, the later item holds: the earlier item is what the result needs in order to hold; further split into sufficient (having it is enough), necessary (without it, it fails), and unconditional (the same either way) | Condition first | — |

- **S19** **First confirm the two sentences are in the same layer. Do not give satellites “第一、第二” (first, second).** Never list a cause, its example and its result as three “原因” (causes). A method and its example are not same-level; “办法” (method) to “策略” (strategy) is.
- **S20** **For turns and concessions, look one step further before deciding between same layer and satellite.** The two sides are a same-layer paired contrast (S11) only when both must enter the claim above; a concession limiting one step is that step's satellite (S14). The core is in the consequent, and the claim states its conclusion.
- **S21** **From the second parallel item on, mark the add-on relation or link with a back-reference.** Add-on relations (carry-over, repetition, emphasis, deepening) are marked above the numbering. Check: name the S18 class of every same-layer seam, and for parallel the add-on relation; named but unmarked means mark it.
- **S22** **Judge in this order, asking about progression first.** One step beyond the earlier item: progression. Else, still the same group after a swap: parallel. Else: turn or concession, or only sequence. When the later item arises from the earlier, tell cause from inference and supposition from condition by the S18 rows.
- **S23** **Treat a short progression as parallel in writing, and mark “而且” (moreover) and “甚至” (even) as usual.** In judging it stays progression; do not flatten the key precondition.

### 3.2 Grouping

- **S24** **Use only one basis of division per group. Let one parent node answer only one question.** Two bases make two layers, not one row; a section answering two questions becomes two blocks. Check: state each group's basis and relation, and look for mixed levels of abstraction or nature in one layer.
- **S25** **Keep nodes at the same level, especially paragraphs and sentences, within ten as far as possible.** Split and regroup a parallel structure of more than twelve (unless it lists names) into two layers by one basis (S24), each within ten. Summarizing the claim afterwards: FICCOutline.md O42. Check: count same-layer nodes per layer.

### 3.3 Stages and different aspects

- **S26** **Stages and different aspects are ways of unfolding. Judge the relations between stages and between aspects per S18.**
  - Their markers, time words and topic frames, are not a two-sentence relation.
  - Between stages, tell mere sequence, the earlier leading to the later, and the later overturning the earlier (their words and stage start points: FICCVoice.md V13).
  - Aspects share one basis (volume and price, assets and liabilities, issuers and investors), never “量” (volume) beside “美国” (the United States); topic frames and symmetry: FICCVoice.md V25. They are parallel by default; if the carry-over previews with “而且” (moreover) and a swap loses a step, it is progression, the earlier aspect paying off the carry-over's first half and the later its second.

### 3.4 Easily confused pairs

- **S27** **Separate easily confused relations pair by pair. Put both sides of a turn on the same dimension.** Use the statement-order and fact-status columns of S18 (between nodes, cause versus inference: S04 item 1). Sides not on one dimension make no reversal: use a light turn or parallel. Check: both sides of “但是” (but) sit on one dimension.
- **S28** **Back-test each marked word with the diagnostic questions to rule out common misuses.**
  - Supposition written as fact: what sits under “如果” (if), “一旦” (once) or “只要” (as long as), or follows from it, is later cited as having happened.
  - Restatement written as cause: a classification, case split, restatement or illustration written as “之所以……是因为” (the reason… is that), “所以” (so) or “因此” (therefore).
  - Check: read the half after “因为” (because) or “所以” (so) alone. If it restates or splits the first half, use a colon (：), “分几种” (falls into several kinds), “也就是说” (that is to say), short sentences or a list (no semicolons: FICCVoice.md V07; words: the 转折 and 并列·解说 rows of references/connectives.md).

### 3.5 Two layers of relation at one seam

- **S29** **When one seam carries two layers of relation, identify both. Mark the layer the reader needs most.** That is the layer, logical or unfolding, the reader would misconnect if it were unmarked.
- **S30** **Judge relations by where a node hangs on the tree, not by which sentence it sits next to.**
- **S31** **When siblings stand in argument or rebuttal, arrange them as siblings first. Re-hang only after the satellite test.** Re-hang only if, with one block covered, the parent still holds and that block only gives evidence or limits for another; it then becomes that block's satellite (S14). Otherwise keep them siblings and mark this layer at the seam.

## 4 Whole set: 分担 completeness (S32)

- **S32** **Verify upward sufficiency and child-set completeness (`分担` row) on every parent node (`N0` included) before descending.**
  - Make the child nodes under one parent node together sufficient to complete the parent node's task. Every child being useful is not enough.
  - Map each element of the parent's `主旨` to the child ID proving it (`主干／链环／卫星`), state what step disappears when each child is covered, and clear `无人担`, `重复担`, and `子项合计仍证不出`. If all children hold yet the parent's claim still needs an unproved bridge, add the missing source node or narrow the parent's `主旨` and modality before any leaf is drafted.
  - One row per parent: `分担：“<要素>”→N1.1·主干｜…｜遮住测试：…｜无人担：…｜重复担：…｜子项合计仍证不出：…〔判于r<k>〕`. A cleared cell reads `无`; `〔判于r<k>〕` names the tree revision ruled. On `N0` the elements are the root claim's links and the children are the parts.
  - No leaf under it is drafted until the row clears or the parent's `主旨` and modality are narrowed to what the children prove.
  - A gap or a duplicate goes to the outline agent as a placement objection: add the node, narrow the parent, or merge, delete or replace (FICCOutline.md 5.2). This rule checks the division of work, not the claim's wording (FICCOutline.md O42). Cross-chapter links: §5.
  - *Self-check: Cover each child in turn and read the parent `主旨` aloud; then read all child `主旨` lines together and check whether the parent claim follows without an extra premise.*

## 5 Cross-branch links: the 关键边表 (S33, S74)

- **S33** **Judge relations with distant nodes by the relation library too. Write them as outline annotations. Do not change this branch's arrangement.**
  - After the checks under one parent, look for relations to other branches and judge per S02. The annotation is one `关键边表` row plus `边：<边ID>` on each end (S74), never a relation row inside one end.
  - Most often crossing branches (1.1): distant foreshadowing–reveal and recurrence, arranged and marked per their S06 rows. Dependencies: S04 item 2. Contrasts: the comparison and contrast row of S06. Paying off a preview: FICCVoice.md C20; foreshadowing on the page: FICCVoice.md C15.
- **S74** **Give each relation one home (`分担`, `接前`, `关键边表`) and unseal an edge only with one linking source sentence.**
  - Parent–child: the parent's `分担` (S32). Adjacent siblings: the later sibling's `接前` (S77). Cross-branch, non-adjacent or contested: the `关键边表` only, with `边：<边ID>` on both ends.
  - Key `关键边表` by the **sorted endpoint pair** only and name the `S18` relation class and direction. Columns: `| 边ID | 端点对（排序键） | 关系类（S18）与作用方向 | 连接句凭据@原件锚点 | 状态（已定／待据／不成立） | 两端禁写边界 | 判于版本 |`. Status is required, and `两端禁写边界` is required once sealed `待据`.
  - A second row on the same pair is never auto-applied: the relation agent reviews the rows side by side to merge, keep distinct relation classes, or adjudicate. Two seats ruling one pair with different status seal it `待据`, both ends bounded, until one linking sentence appears (evidence-preservation lock); no backfill overwrites `待据`.
  - To mark a causal or dependency edge (repayment dependency included) `已定`, quote **one primary-source sentence or clause that links both ends**; separate facts at each end without a linking clause must be sealed as `待据` with explicit two-end forbidden claims (`两端禁写边界`). Time order alone never makes a cause.
  - Seal a tempting link, never skip it: where the sources set a co-timed flow, a parallel move or an adjacent figure beside another node so that a reader could take it for that node's cause, funding or dependency, write the pair's row `待据` with `两端禁写边界` naming the link barred at each end (FICCOutline.md O64). An excluded fact (`范围排除` included) or a ban at one end only does not seal it. A source silent on the link, or saying none is disclosed, gives `待据`; `不成立` needs a source sentence that the link does not hold.
  - Example: `| X02 | N2.3—N3.1 | 拟议依赖（N3.1分部收入→N2.3专项债偿付） | A档@L120与B档@L450各述一端，无连接句 | 待据（转核源） | 两端各述披露事实，禁写成偿债来源 | r1 |`.
  - Rows record relations only (ends, class, grounds, limits); placement still decides where content goes (FICCOutline.md 5). Grammar: FICCOutline.md 4.2.

## 6 Relation slots in the living outline

The standalone relation sheet is retired; its fields live in these slots, and `接前` and `边` replace the legacy `关系：` lines and cross-branch `标注：` annotations (the `标注：删` deletion record of FICCOutline.md O58 stays). The relation agent writes and rules `分担` (every parent, `N0` included), `接前` (every later sibling, and the `接前` cell of each `段k` row), `边` (both ends of an edge) and the tree-head `关键边表`. The outline agent owns the tree and every other slot (`名字表`, `主旨`, `任务`, `顺序`, `展开`, `收尾`, `事实`, `算式`, `消歧`, `段k`); it may enter a provisional `分担` or `接前` row while growing the tree, which the relation agent then rules and stamps `〔判于r<k>〕`. Only the relation agent changes a ruled row.

### 6.1 Slots per node

- **S75** **Write relations only into the living outline's relation slots; FICCOutline.md 4.2 defines their grammar once.** There is no separate relation sheet and, in new writing, no separate placement record; do not ask for one just to go through the procedure.
- **S76** **`分担` (the old upward relation and downward unfolding): state how the children unfold this node and whether together they complete it.** Judge by library type and arrangement (S05, §2) and by S32.
- **S77** **`接前` (the old same-layer relation and order reasons): state which earlier sibling this node follows, by which S18 class, on what grounds.**
  - Grammar: `接前：N<前号>·<S18关系类>·凭：@<原件锚点>｜下游禁改边界：<…>`; a first child writes `接前：承<父号>题`. `凭` is required for a causal or inferential class (S18); `下游禁改边界` names the reading the writer must not give the seam (`只是并列，不写成因果或递进`).
  - Confirm the reason in the outline's `顺序` row: whose premises it uses, who later relies on it. If it fails, raise `安放异议` through the lead; the relation agent does not change the order.
- **S78** **`边` and the `关键边表` (the old cross-branch links): record cross-branch dependencies, echoes, foreshadowing and contrasts.** Judge per S33, record per S74; foreshadowing on the page: FICCVoice.md C15.
- **S79** **Facts and the author's original sentences: cite where they are, do not copy them. The packet attaches readable source excerpts.**
  - Facts live in the outline agent's `事实` row (FICCOutline.md O51). A relation row cites anchors (`E012@<档名>:L85`); its `凭` is a source anchor, never a copied fact. A fact still to verify becomes its own to-do item with an issue number (`I-nn`, as in the ledger) and stays out of the body.
  - A sentence marked 〔作者亲写·逐字〕: cite its node; the packet attaches the text (FICCOutline.md O71).
  - Recompute: for a sentence `inline_guards.py scan` marks `recompute_needed`, the tie-out seat or the relation agent writes `重算：<位置>｜证据锚：<source line of each operand>｜运算：<operands, roles, recompute result closed／unclosed／not_formula>｜授权：<rewrite: explain the denominator with tokens the base holds, no derived number; draft: a signed 算式 row or the author's amendment>`. Without a signed authority the sentence stays as the base states it.
- **S82** **Which name the whole piece uses for the same thing: per the `名字表` in the outline head.** The writer uses it as given (FICCOutline.md O32–O34; wording: FICCVoice.md V23, V33). A missing name, or one thing with two names, goes to the outline agent as a to-do item: `<东西>：<在哪个节点看到的说法>`.
- **S83** **Who controls what at handover: SKILL.md 2.** The relation agent rules relations in the slots and never writes one it knows to be wrong as settled. A specific disagreement goes to the lead, who routes relations to the relation agent and placement or order to the outline agent; finish the conflict-free part first.

### 6.2 To-do items for other nodes

- **S81** **To-do items for other nodes: S84.**
- **S84** **To-do items for other nodes (the old relation-sheet field 4) are governed here; what the writer may change outside its node: references/dispatch-notes.md 2.**
  - When a block is placed here and relations change, list the text elsewhere that must follow: the step the parent's carry-over gives it, the neighbouring siblings' linking-back sentences, and sentences that echo it or set it up. One line each, `待办：<节点号>｜<改什么>｜<为什么>`, routed by the lead with no separate seat round per item.
  - Outline maintenance (nodes, `主旨`, `任务`, unfoldings, headings, `名字表`, `顺序`) goes to the outline agent. Do not re-judge settled decisions when carrying them out; when maintenance substantively changes a settled claim, content or order, re-rule the affected relation rows.

## 7 Structure Gate: relate before writing

- **S85** **Check layer by layer, pair by pair, group by group, and seam by seam. Every piece goes through this.**
  - First the relations on the tree; after drafting, that each relation the slots name holds in the body text as a proposition. The outline itself and whether its decisions are carried out: FICCOutline.md 9.
  - Before drafting new writing or an authorized reorganization, and before submitting, check in order: node focus by layer (S86), representative parallel nodes (S88), grouping and whole sets (S24, S32), then from deep, dense, turn-heavy places down to clauses (S91).
  - 闸2, `分担` (S32): cover each child in turn and read the parent `主旨`: which step goes missing? Add up the child `主旨` lines: which link to the parent is still unproved?
  - 闸3, one home and one ruling (S74): wherever a relation says “因为／因此／导致／依赖偿付”, can you paste one source sentence or clause linking both ends? If not, seal it `待据`. A co-timed fact a reader could take for a node's cause gets its two-end `待据` row too.
  - Script gates, `outline_slice.py check-0to1 <文稿>-提纲.md`. Hard Z-SHARE: a node with children (`N0` included) lacks `分担`, a closing cell is not `无`, an item names a non-child, or a child carries no item. Hard Z-EDGE: an endpoint is not two node ids with blocks, a status is missing, an `已定` row has an empty 凭据 or is causal with no `@`, one sorted key carries rows of different status, or a causal `接前` (node or `段k` row) has no `@`. Z-EDGE? (one key, two rows, same status) is a warning that still needs the side-by-side ruling.
  - No leaf is drafted until both gates pass.

### 7.1 Check by layer

- **S86** **The focus of the check changes with the layer the node is in.**
  - Whole piece: center and coverage are FICCOutline.md 9; here, whether the structure serves that goal and what the reader finally gets.
  - Chapters and main parts: the relatively complete task each carries, how it divides work with the others, why this order, what it prepares. Parallel parts may stand alone; a depended-on part comes first.
  - Paragraph markers and wording (cohesion, reference, consistent concepts): FICCVoice.md C23, V37–V40.
  - Sentences: relations per §3; then judgments get explanation, support or qualification (FICCOutline.md O16), restatements add clarity, turns have grounds in content (3.4), and reasoning has no missing links, leaps or needless repetition.
- **S87** **When keeping suspense, information gaps, and deliberate blanks in literary narrative, state their function.** State its role in the whole, and whether and where later text pays it off.

### 7.2 Representative nodes

- **S88** **For representative parallel nodes such as several stories, points, or pieces of evidence, check the focus for each in the table below.** Complementarity, contrast, progression and counterexample are the 1.1 types complementarity, comparison and contrast, progression and deepening, and objection and response. Repeated verification (several blocks on one step): keep it per the third row and §4.

| Node type | Key checks |
|---|---|
| Several stories or cases | Whether they are complementarity, contrast, progression, counterexample, or repeated verification; what each story adds |
| Several points | Whether they support the conclusion separately or derive it layer by layer; whether there are missing links or mutual contradictions |
| Several pieces of evidence | Whether they are independent, relevant, and sufficient; whether they only repeat information from the same source |
| Several narrative scenes | After a scene ends, what has changed in the situation, the characters, the relations, or the reader's understanding |
| Several character perspectives | Whether they add information, create conflicts of understanding, or reveal the limits of a single perspective |
| Several methods or steps | Whether there are sequential dependencies, conditional branches, parallel relations, and check-and-feedback loops |
| Several concepts or models | Whether they stand in inclusion, overlap, or opposition, or apply to different scales or conditions; whether they are mixed up |

### 7.3 Parent–child, grouping, subtree

- **S89** **Subtree tests and the outline's own checks belong to FICCOutline.md 9. This file checks `分担` (S32), grouping (S24) and edges (S74).**

### 7.4 Seam check

- **S90** **Seam check: the relation agent checks that each seam carries the relation its `接前` row names, as a proposition; the marker and wording check is the writer's (FICCVoice.md V22).**

### 7.5 What to check first, and where to start

- **S91** **Start from places with deeper unfolding, denser material, and more turns. Check layer by layer down to sentences and clauses.**
- **S92** **Check first a relation the outline's rows name that the text does not carry (S21), then whether each statement below has a use.**
- **S93** **Openings check belongs to FICCVoice.md C23, not to this file.**
- **S94** **Mechanical checks do not prove the logic holds. Read the content they connect.** Look for causation strengthened out of nothing, speculation turned into fact, qualifiers dropped for smoothness. Complete headings, equal paragraph counts, unchanged numbers, “所以” (so) in every paragraph or a clean `check-0to1` run are no pass.
- **S95** **When you find problems, point out the few that actually affect the writing, and give adjustments that can be carried out.**
  - An adjustment is an action class with its position and the misreading it prevents (re-hang, split, add the missing node, narrow the parent, seal `待据`, mark the relation), never a model-written rewrite (references/clarity-acceptance.md A01). Do not force fault-finding; for a simple task hand over only what is needed.
  - Cold-read hazards (unclear subjects, unmarked relations, two-way back-references, words the reader must decode) are defects to fix before submitting, not a count to report; when unsure, ask the lead. Reporting and who fixes: FICCVoice.md V40.
- **S96** **The tree is grown only when a traversal goes through and each layer reads as a complete small essay.** Where a layer does not go through, hand its opening back for rewriting per FICCVoice.md C01; do not patch the wording. Misplaced content or mismarked relations go to the outline agent as a placement objection through the lead.

## 8 Appendix: sources and on-demand references

Openings, carry-overs and closes: FICCVoice.md C01, C04, C13–C20. Wording and seams: FICCVoice.md V13, V22. Connective rows, supplementary connectives and the two classical systems' disagreements: references/connectives.md. Rationale, examples and history: references/FICCStructure-rationale.md (numbering mapped in its header). The user's original words, past rulings and rule history: references/dev-notes.md section 35. Classical sources, evidence grades and example sources: references/examples-and-rewrites.md, Appendix: Sources. Write the user's new corrections on relations into the section that governs them; the body carries no date markers.
