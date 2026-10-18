# FICCStructure: Judge relations

This file governs the relations between nodes, from the whole piece down to complex sentences, and holds only rules, boundaries, and checks. The relation agent (ficc-structurer) takes the tree, the placement record, and the order reasons from the outline agent (ficc-outliner), judges each relation's type and whether it holds, and writes the result node by node into a relation sheet for Compose and Voice. At seams it gives the row name in references/connectives.md. Where a relation does not hold, it returns a placement objection to the outline agent through T0, and it neither changes the tree nor decides placement (FICCOutline.md 5). Arrangement verbs (hang, re-hang, split, merge, move) name the content of an objection, which the outline agent carries out. In these rules, “the user” means the author, and “you” means the agent applying the rule.

## 1 Relation library: what to judge relations with

### 1.1 Twenty-one relation types

- **S01** **Find the relation between nodes among the twenty-one types.**
  - Judge relations between chapters, parts, paragraphs, and sentences by the table below.
  - Judge relations among several stories, points, pieces of evidence, scenes, perspectives, steps, or concepts by the same table.

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

- **S02** **When you identify a relation type, state in full which item relates to which, through what content, and what relation it forms.**
  - These relations may overlap and may be used across levels: one seam may be both a cause and mechanism relation and an assertion and support relation.
  - Choose by actual content. Do not try to cover every type.
  - Identifying a relation type must not stop at attaching a label: state which node relates to which node, through what content, and what relation it forms.
  - Check: if you cannot state all three, the relation is not yet identified.
  - See references/FICCStructure-rationale.md 1.2.
- **S03** **When relations overlap, decide the arrangement by the satellite test (S08).**
  - Which layer to mark at the seam: per S29.
  - What relation holds between siblings, and whether to re-hang: per 3.
  - Treat carry-over and transition as positions. Do not list them in the relation library. See FICCCompose.md C04, C13.

### 1.3 Six distinctions

- **S04** **Before using the relation library, distinguish the six most error-prone points.**
  1. Cause and inference: cause and mechanism explains why something happens; grounds and inference explains why a judgment can be drawn.
     - Separate the markers at seams per S18.
  2. Progression and premise: progression and deepening stresses that understanding or plot moves forward, with the later block going one step beyond the earlier one; premise and dependency stresses what foundation later content needs, and the premise goes before the content that depends on it (2.2, 2.3).
  3. Example and proof: an example may help understanding and may also provide support, but a single case is not necessarily enough to prove a general judgment.
  4. Synthesis and repetition: induction and synthesis reveal what the parts jointly show; they do not merely restate earlier text.
     - A close applies this item: it gathers what the child nodes show back into the block's claim and does not restate it (FICCCompose.md C17).
  5. Analogy and transfer: analogy and transfer state on which dimension things are similar and where the application stops; do not conclude that a conclusion transfers on surface similarity alone.
  6. Relations and connectives: turns, progressions, and causes must hold in content; they must not be manufactured by connectives.
     - If you cannot identify the relation, change the content. Do not add a word (3, FICCVoice.md 4).
  - See references/FICCStructure-rationale.md 1.3.

### 1.4 How the relation library connects to arrangements and seams

- **S05** **First judge how the child nodes unfold the parent node. The unfolding decides the arrangement.**
  - Unfolding falls into three types, each matching one arrangement.
    - Type one: several blocks together exactly make up the parent node. Arrange them as a trunk group (S11).
    - Type two: step by step, they arrive at the parent node. Arrange them as a chain (S13).
    - Type three: the parent node already holds on its own, and the child nodes only give it evidence, examples, explanations, limits, background, counter-views, contrasts, or an evaluation of the material. Make them satellites, hung on the step they serve (S14).
  - See references/FICCStructure-rationale.md 1.4.
- **S06** **The table below only suggests common arrangements and complex-sentence relations. The satellite test (S08) and the diagnostic questions (S18) decide.**
  - The complex-sentence relation column governs only the paragraph level and below.
  - Mark relations above the section level by position, carry-over paragraphs, and linking-back sentences (FICCCompose.md C04, C14).

| Relation type | Common arrangement | Complex-sentence relation at the seam |
|---|---|---|
| Classification and division of labor | Trunk group, one basis of division per group (3.2) | Parallel; from the second item on, mark the add-on relation |
| Complementarity | Trunk group, unfolded by different aspects (3.3) | Parallel (different aspects); progression when the supplementing block goes one layer further |
| Overview and unfolding | The overview sits in the parent node; details that together make up the overview form a trunk group; a single concrete manifestation given for an abstract concept is a satellite | Explication; between details, parallel or sequence |
| Induction and synthesis | Write it in the parent node's claim or close; do not list it as a separate block (2.2, FICCCompose.md C17) | Cause and effect · inference |
| Explanation and clarification | Satellite, hung on the statement it explains | Explication; cause and effect when it describes a mechanism |
| Assertion and support | Satellite, hung beside the step it supports; for argument between siblings, see 3.5 | By position, following the step it supports; giving reasons is cause and effect, giving evidence is explication; premise first and judgment after is cause and effect · inference (1.3 item 1) |
| Grounds and inference | Chain | Cause and effect · inference |
| Cause and mechanism | Chain; with parallel channels or feedback, choose one route the reader can follow (2.3) | Cause and effect; sequence when the mechanism goes step by step |
| Conditions and limits | Chain when the consequent is the parent claim itself; satellite when it limits only one step, following the judgment it limits | Condition, supposition, turn · concession; a light turn when it is only a mismatch |
| Progression and deepening | Trunk group ordered by degree, or a chain | Progression; when written as parallel, mark the add-on relation (emphasis, deepening) |
| Premise and dependency | Chain, premise first; a single background premise is a satellite, placed before its first use (FICCOutline.md 5.3) | Sequence; cause and effect · inference |
| Comparison and contrast | Trunk group, arranged as a paired contrast, with the shared measurement basis stated first; another period or market used only as a reference is a satellite or goes to the appendix (FICCOutline.md 5.3) | Parallel (paired contrast); turn |
| Analogy and transfer | Satellite, hung on the step it explains | Explication; condition for the limits of application |
| Objection and response | Chain (question, answer, concede a step, turn back); a trunk group as a paired contrast when both sides enter the parent claim; a counter-view that limits only one step is a satellite (FICCOutline.md 5.3) | Turn, turn · concession |
| Problem and solution | Chain | Sequence, cause and effect · purpose; for a posed-question opening, see FICCCompose.md C01 |
| Goals and means | Chain; a trunk group when several means stand side by side | Cause and effect · purpose |
| Choice and trade-off | Trunk group; once the trade-off is made, the core is the chosen item | Alternative |
| Time and space | Trunk group, ordered by time or position (for stages, see 3.3) | Sequence; topic frames for position |
| Setup and payoff | Chain (posed question–answer, promise–fulfillment); a distant foreshadowing–reveal becomes a cross-branch annotation (5) | Sequence; for preview and payoff, see FICCCompose.md C20 |
| Echo and variation | Cross-branch annotation (5); the arrangement does not change | Parallel · add-on relation (repetition); for back-reference and parallel syntax, see FICCVoice.md 4.3 and 4.5 |
| Pacing and mood regulation | No set arrangement | Not marked at seams; for sentence patterns, see FICCVoice.md 3 and 4.5 |

## 2 Vertical: what it does for the parent node

- **S07** **Before hanging a block, state what it does for the parent node.**
  - When you hang a block, first state two things: what it concretely expresses, and by what means it helps the parent node complete its task.

### 2.1 Three arrangements

- **S08** **Separate satellites from the trunk with the cover test.**
  - The parent claim means the parent node's claim sentence, not the evidence list in its claim field.
  - Check: cover this block and reread the parent claim.
    - If the claim now lacks part of its answer, the block is a component of the answer (trunk).
    - If the claim still gives its whole answer and loses only support or qualification, the block is a satellite.
  - The result sets the arrangement only. It does not decide whether a block is deleted.
  - When a node has only satellite child nodes, its claim is its own conclusion.
- **S09** **Tell a story through layer-by-layer progression as far as possible.**
  - When several items in the same layer can form one line that goes deeper, arrange them as that line.
  - The line runs from shallow to deep, from appearance to cause, or from general to specific.
  - Lay items out flat as parallel only when no item goes a step beyond another (S22).
- **S10** **Between sub-points in the same layer, first judge the actual relation, then decide how to write it.**
  - Branch lines in the same layer may stand in eight relations: turn, supposition, parallel, progression, alternative, cause and effect, condition, and sequence. Sequence here is the 承接关系 (sequence relation), not 承接 as a position (carry-over).
  - Unfolding by stage (by time period) and by different aspects: per S26.
  - Which arrangement each relation falls into and where its core lies: per the matching row in S06.
  - Once the relation is identified, mark it with a connective: how to identify it, per 3.

### 2.2 Trunk group

- **S11** **A trunk group keeps four rules: same kind, ordered, an extra layer when items are many, and one extra sentence in the parent node.**
  - Trunk groups include parallel and enumeration, sequence and stages, alternative, paired contrast, different aspects, and progression ordered by degree.
  - First, same kind: only one basis of division (S24), with comparable granularity.
    - Granularity means level of abstraction, not length.
    - When comparing several subjects, discuss them on comparable dimensions. Put each subject's particular issues back under that subject.
  - Second, ordered: the order serves understanding and argument, and is decided by how the group is formed.
    - When finding the several steps to a result, order by time.
    - When splitting a whole, order by structure.
    - When grouping like with like, order by degree.
    - Place necessary definitions before their use, and premises before the inferences that depend on them.
    - Stating a shared definition or background only once: → FICCCompose.md C11.
    - When comparing, state the shared measurement basis first.
    - Where a definition or measurement basis hangs within a sentence, rather than among nodes and steps: see FICCVoice.md 5.1.
    - Bring one question to a point where it can be wrapped up for now, then move to the next.
    - You may advance by fund flow, time, participants, or questions. When you change the basis of ordering, state the turn.
    - Do not switch within one group between ordering by company, by time, and by bullish versus bearish.
  - Third, when the same layer has more items than the reader can remember, add a layer (S25).
  - Fourth, since a trunk group has no core of its own, the parent node first writes one extra sentence on what the items show together.
    - Do not write only “有三点” (there are three points).
- **S12** **Make each kind of trunk group show what it needs to show.**
  - Parallel: the shared question is visible.
  - Progression: the added step is visible.
  - Alternative: write the grounds for the trade-off.
  - Stages: state where each stage starts and where it turns.
  - Different aspects: together they answer one question.
  - For marking items by repeating the same opening in each, see FICCVoice.md 4.5.

### 2.3 Chain

- **S13** **Mark every link of a chain. The chain's conclusion is the parent node's claim.**
  - A chain is a set of child nodes where each step depends on the previous one: deductive, causal, inferential, and conditional chains.
  - The relations between links may differ.
  - By default, arrange an argument node as a chain: question, answer, concede a step, turn back, conclusion, with one marker per link.
  - When sections form a chain, first induce the steps.
  - Choose only one route the reader can follow for the chain. Do not write it as the only causal chain.
  - How a mechanism runs through, and how to leave the step the material cannot prove: see FICCOutline.md 2.2.
  - Put consequences in cause and effect, conclusions in conditions, and members in classifications each in their own place.
  - When the same material changes use, say so rather than shift its level silently.

### 2.4 Satellite

- **S14** **Hang a satellite beside the step it serves. Do not set it side by side with the trunk.**
  - A satellite is not required to be of the same kind as the trunk.
  - State what it does for the current trunk, and which kind of type-three unfolding in S05 it is.
  - Measurement bases follow comparisons, qualifiers follow judgments, and evidence follows the statement it supports.
  - Do not change the company basket and the gross or net basis at the same time while letting “从……到……” (from… to…) look like one series.
  - See references/FICCStructure-rationale.md 2.4.
- **S15** **A satellite may unfold layer by layer, as deep as the content requires.**
  - Paragraph organization: FICCCompose.md C16.
- **S16** → FICCCompose.md C19

## 3 Horizontal: the relation between it and its sibling nodes

- **S17** **For horizontal relations, look first at sibling nodes under the same parent node.**
  - For horizontal relations, prefer sibling nodes under the same parent node (sibling nodes are the same-level nodes under one parent node; same-level and same-layer child nodes below all mean them): how they divide the work, what their logical relation is, why they are ordered this way, and whether they echo each other.
  - Siblings in structure are not necessarily parallel in logic: siblings may also stand in cause and effect, progression, argument, or rebuttal.

### 3.1 Identify the relation first

- **S18** **Judge the relation before choosing words. The answer to the diagnostic question decides which class of word to use.**
  - This section judges the eight complex-sentence relations at the seam between two sentences or two blocks. Their mapping to the relation library: per S06.
  - Put the two sentences together and go through the table below question by question.
  - Once the class is identified, which seam to mark: per FICCVoice.md V22, V52.
  - Check: if a question yields no answer, first check whether the two sentences are in the same layer, or whether the thinking is not yet clear.
  - Mark separately whether each item is a fact, an expectation, or a supposition. A relation type alone does not show that a purpose was achieved or a condition was met (back-test: S28, supposition written as fact).

| Relation | Diagnostic question (if “yes”, assign this class) | Statement order | Fact status |
|---|---|---|---|
| 并列 (parallel) | The two items are of the same kind under the same basis of division; equal weight is not required | Swappable: after a swap they are still the same group and lose only the order; if a swap loses a step, it is 递进 | — |
| 并列·附加关系 (parallel · add-on relation) | The later item follows on (承接, carry-over), returns to the earlier one (反复, repetition), sharpens it (强调, emphasis), or goes one layer deeper (深化, deepening); mark it above the parallel relation; it is not a ninth relation; emphasis and deepening = progression written in parallel form, arranged as in the progression and deepening row of the 1.4 table | The later item rests on the earlier one | — |
| 并列·解说 (parallel · explication) | The later item explains, illustrates, or restates the earlier one; then the later item is most likely a satellite of the earlier one, hung per 1.4; it counts as parallel only when the two items truly sit in the same layer | The explaining item follows what it explains | — |
| 承接关系（先后） (sequence) | The two items have a temporal or logical order that cannot be reversed | Fixed; coming first in time does not by itself make a cause | — |
| 递进 (progression) | The later item goes one layer further than the earlier one in scope, quantity, degree, or time; without the earlier item, the later item's weight changes | Fixed; a swap loses the added step | — |
| 转折 (turn) | The later item turns to an opposite or contrasting meaning; opposed meanings are a strong turn, a mere mismatch is a light turn; mark a light turn as usual, and do not substitute a re-mention of earlier text (FICCVoice.md V52) | The turned-to meaning comes second | — |
| 转折·让步 (turn · concession) | First grant or suppose something, then say the result is unaffected by it; granting a fact is a factual concession, supposing is a hypothetical concession, “怎样都一样” (it is the same either way) is a total concession | The granted or supposed item comes first | Factual concession: the granted item is a fact; hypothetical concession: it is only supposed |
| 因果 (cause and effect) | The earlier item is an objective cause of the later item | Usually cause first; a “因为” (because) clause may follow its result | — |
| 因果·推断 (cause and effect · inference) | The earlier item is a premise the reader already accepts, and the later item is a conclusion the text draws from it | Premise first, then the conclusion | — |
| 因果·目的 (cause and effect · purpose) | The earlier item is done in order to obtain the later item | Either order | — |
| 假设 (supposition) | The earlier item is only supposed, not asserted | Supposition first | The earlier item has not happened, or may never happen; what follows from it is not later cited as fact (S28) |
| 选择 (alternative) | Choose one among several possibilities; an open alternative when not yet decided, a settled alternative when the trade-off is made | Options side by side | — |
| 条件 (condition) | When the earlier item is met, the later item holds: the earlier item is what the result needs in order to hold; further split into sufficient (having it is enough), necessary (without it, it fails), and unconditional (the same either way) | Condition first | — |

- **S19** **First confirm the two sentences are in the same layer. Do not give satellites “第一、第二” (first, second).**
  - When listing “原因” (causes), do not list a cause, an example of that cause, and its result as three items.
  - Jumping from a method to its example is not same-level. You may move from “办法” (method) to “策略” (strategy).
- **S20** **For turns and concessions, look one step further before deciding between same layer and satellite.**
  - Only when both sides must enter the claim of the layer above are they a same-layer pair, arranged as a paired contrast (S11).
  - A concession that limits only one step is a satellite of that step (S14).
  - The core is in the consequent, and the claim states the consequent's conclusion.
- **S21** **From the second parallel item on, mark the add-on relation or link with a back-reference.**
  - Add-on relations are carry-over, repetition, emphasis, and deepening. Mark them above the numbering.
  - Check: for every same-layer seam, name which class in the table above it is; for parallel, also name the add-on relation.
    - If you can name it but it is unmarked, mark it.
- **S22** **Judge in this order, asking about progression first.**
  - First ask whether the later item goes one step beyond the earlier one.
  - If it does, it is progression.
  - If not, and the items remain the same group of like items after swapping, it is parallel.
  - If neither, see whether it turns (turn or concession) or only comes after (sequence).
  - When the later item arises from the earlier one, tell cause and effect from inference by what the earlier item is (S18 rows).
  - When the earlier item is only supposed or required, not asserted, tell supposition from condition by the S18 rows.
- **S23** **Treat a short progression as parallel in writing, and mark “而且” (moreover) and “甚至” (even) as usual.**
  - In judging the relation it is still progression. Do not flatten the key precondition.
  - See references/FICCStructure-rationale.md 3.1.

### 3.2 Grouping

- **S24** **Use only one basis of division per group. Let one parent node answer only one question.**
  - When two bases are needed, split into two layers rather than setting them side by side.
  - Split a section that answers two questions at once into two blocks, each answering one.
  - Check: state the basis of division and the relation for each group.
  - Check: look for things of different levels of abstraction or different nature mixed into the same layer.
- **S25** **Keep nodes at the same level, especially paragraphs and sentences, within ten as far as possible.**
  - If a parallel structure of more than twelve nodes appears, then unless it lists a list of names, you should consider splitting and regrouping it into new substructures.
  - When splitting, divide into two layers by one basis of division (S24), and keep each layer within ten as far as possible as well.
  - How to summarize the claim after layering: see FICCOutline.md 4.3.
  - Check: count the same-layer nodes in each layer.
    - Where there are more than ten, see whether they can be split into two layers by one basis of division.
    - Split and regroup a parallel structure of more than twelve per this rule, unless it lists a list of names.

### 3.3 Stages and different aspects

- **S26** **Stages and different aspects are ways of unfolding. Judge the relations between stages and between aspects per S18.**
  - Their markers are time words and topic frames. These do not count as a relation between two sentences.
  - Between stages, distinguish these three:
    - Mere sequence.
    - The earlier stage leads to the later one.
    - The later stage overturns the earlier one.
  - Which words each of the three uses, and which point in time opens each stage: see FICCVoice.md 4.1.
  - Which topic frames aspects use, and how to keep them symmetric: see FICCVoice.md 4.5.
  - The aspects use one basis of division, such as volume and price, assets and liabilities, or issuers and investors.
  - Do not let one aspect be “量” (volume) and another “美国” (the United States).
  - By default, aspects are parallel.
  - If the carry-over sentence previews with “而且” (moreover) and swapping loses a step, judge it as progression.
  - Then the earlier aspect pays off the first half of the carry-over sentence, and the later one pays off the second half.
  - See references/FICCStructure-rationale.md 3.3.

### 3.4 Easily confused pairs

- **S27** **Separate easily confused relations pair by pair. Put both sides of a turn on the same dimension.**
  - Separate parallel from progression, sequence from cause and effect, cause and effect from inference, turn from concession, and supposition from condition by the S18 table, using its statement-order and fact-status columns. Between nodes, cause and inference: S04 item 1.
  - If the two sides are not on the same dimension, there is no reversal: change the turn to a light turn or parallel.
  - Check: the two sides of “但是” (but) sit on the same dimension.
  - See references/FICCStructure-rationale.md 3.4.
- **S28** **Back-test each marked word with the diagnostic questions to rule out common misuses.**
  - The S18 table does not show these two misuses:
    - Supposition written as fact: a supposition or condition carried by “如果” (if), “一旦” (once), or “只要” (as long as), or a result derived under it, is later cited as a fact that has happened (default rule: S18).
    - Restatement written as cause: classification, case splitting, restatement, or illustration is written as “之所以……是因为” (the reason… is that), “所以” (so), or “因此” (therefore). Here the two halves are in fact the same thing.
  - Word choice for “但是” (but): references/connectives.md 转折 row (for “换句话说” (in other words), the 并列·解说 row).
  - Check: take out the half sentence after “因为” (because) or “所以” (so) on its own.
    - Judge whether it is the cause or result of the first half, or a restatement or case split of the first half.
    - If the latter, use a colon (：), “分几种” (falls into several kinds), or “也就是说” (that is to say) instead, or lay the items out as separate short sentences or as a list (no semicolons in body prose, FICCVoice.md V07).

### 3.5 Two layers of relation at one seam

- **S29** **When one seam carries two layers of relation, identify both. Mark the layer the reader needs most.**
  - When a logical relation and an unfolding relation hold at once, judge both layers.
  - At the seam, mark the layer the reader needs most, that is, the layer the reader would misconnect if it were unmarked.
  - See references/FICCStructure-rationale.md 3.5.
- **S30** **Judge relations by where a node hangs on the tree, not by which sentence it sits next to.**
  - See references/FICCStructure-rationale.md 3.5.
- **S31** **When siblings stand in argument or rebuttal, arrange them as siblings first. Re-hang only after the satellite test.**
  - Re-hang only if, with one block covered, the parent node still holds and that block only gives evidence or limits for another block.
  - After re-hanging, it is a satellite of that block (S14).
  - Otherwise arrange them as siblings, and mark this layer of relation at the seam.
  - See references/FICCStructure-rationale.md 3.5.

## 4 Whole set: are the child nodes enough together

- **S32** **Make the child nodes under one parent node together sufficient to complete the parent node's task.**
  - Every block being useful is not enough. Also check two things:
    - No necessary link is missing: each needed explanation, argument, plot point, or operating step has a block carrying it.
    - Several blocks do not duplicate the same task.
  - Return duplicates to the outline agent as a placement objection. It merges, deletes, or replaces them (FICCOutline.md 5.2).
  - Check: write down the thing the parent node is to accomplish, and list under it the share each child node carries.
    - Find the share no one carries.
    - Find the share two blocks carry.
  - This rule checks the division of work, not the wording of the claim (summarizing it: FICCOutline.md 4.3).
  - For dependencies, contrasts, foreshadowing, and echoes across chapters, see 5.
  - See references/FICCStructure-rationale.md 4.

## 5 Cross-branch links: echoes, foreshadowing, and dependencies with distant nodes

- **S33** **Judge relations with distant nodes by the relation library too. Write them as outline annotations. Do not change this branch's arrangement.**
  - After checking under one parent node, check whether the block relates to other branches.
  - Judge per S02.
  - The two types that most often cross branches (1.1):
    - Distant foreshadowing–reveal within setup and payoff.
    - Recurrence and variation within echo and variation.
  - How these two are arranged and marked at seams: per these two rows of the S06 table.
  - Judge cross-branch dependencies per S04 item 2. Hang cross-branch contrasts per the comparison and contrast row of the S06 table.
  - For a preview in the body text, who pays it off and how it matches: per FICCCompose.md C20.
  - How cross-branch foreshadowing lands on the page: FICCCompose.md C15.
  - See references/FICCStructure-rationale.md 5.

## 6 Relations in the body text: openings, carry-overs, between layers, and closes (moved to FICCVoice.md)

(moved to FICCVoice.md, and on 2026-10-17 mostly on to FICCCompose.md; map: references/migration-2026-10-17.md)

## 7 Relations in paragraphs and sentences (moved to FICCVoice.md)

(moved to FICCVoice.md, and on 2026-10-17 mostly on to FICCCompose.md; map: references/migration-2026-10-17.md)

## 8 Seams: where to mark relations (moved to FICCVoice.md)

(moved to FICCVoice.md, and on 2026-10-17 mostly on to FICCCompose.md; map: references/migration-2026-10-17.md)

## 9 Relation sheet: what goes to the writer

- **S74** **Write the results of relation judgment and seam relation classes into a relation sheet for Compose and Voice.**
  - The relation sheet records only relations: for each, the endpoints, the type, the grounds, and the limits or open items.
  - The placement record decides where this content goes: add, move, merge, replace, or leave out.
  - Relation sheet format: see references/relation-sheet-template.md.

### 9.1 Items per node

- **S75** **Write the items the relation-sheet template defines (references/relation-sheet-template.md is the single definition of the fields).**
  - With no new placement, do not ask for a placement record just to go through the procedure.
- **S76** **relation-sheet-template.md 2.1, upward relation and downward unfolding: state how it unfolds the parent node.**
  - Judge by the relation library type and its arrangement (S05, 2), and by whether the child nodes together complete this node's task (S32).
- **S77** **relation-sheet-template.md 2.2, same-layer relation and reasons for order: state what relation it has with which existing branch.**
  - Judge how this relation holds in content (1 to 3).
  - Order reason: confirm the reason in the outline's order line (`顺序：`).
    - The reasons are whose premises it uses, and who later relies on it for setup.
- **S78** **relation-sheet-template.md 2.3, cross-branch links: write cross-branch dependencies, echoes, foreshadowing, and contrasts.**
  - Judge per S33. How each piece of foreshadowing lands on the page: FICCCompose.md C15.
- **S79** **relation-sheet-template.md 2.6 and 2.7, facts and author's original sentences: cite where they are, do not copy them. The packet attaches readable source excerpts.**
  - Facts to be verified: per relation-sheet-template.md 2.6, with the writer's handling in FICCVoice.md.
  - Writing rules: FICCCompose.md 1–5 and FICCVoice.md 3–4. The writer's at-hand summary is references/writing-checklist.md.
- **S80** → FICCCompose.md C12. Length caps and full-statement places: FICCOutline.md O44, O51.
- **S81** **relation-sheet-template.md 4, to-do items for other nodes: per S84.**
- **S82** **Which name the whole piece uses for the same thing: per the name table in the outline header.**
  - The name table: see FICCOutline.md 4.2. The writer uses it as given. Rules: see FICCVoice.md 5.
  - When the relation agent finds names missing from the table in the outline or the finished draft, list them as to-do items for the outline agent.
- **S83** **Who controls what at handover: SKILL.md 2.**
  - The relation agent sets relations in the sheet.
  - Do not write a relation you know to be wrong as a settled fact.
  - Send the specific disagreement to T0, who forwards relations to the relation agent and placement or order to the outline agent. Finish the conflict-free part first.

### 9.2 To-do items for other nodes

- **S84** **What the writer may change outside this node: references/dispatch-notes.md 2.**
  - When a block is placed here and relations change, list as to-do items the body text elsewhere that must change accordingly:
    - The step the parent node's carry-over gives it.
    - The linking-back sentences of the preceding and following sibling nodes.
    - Sentences elsewhere that echo it or set it up.
  - List items the outline needs maintained for the outline agent to carry out.
    - Items include nodes, claims, tasks, unfoldings, headings, the name table, order lines, relation lines, and annotation lines.
  - When carrying out settled decisions, do not judge them again.
  - When outline maintenance substantively changes a settled claim, content, or order, add the affected relations.

## 10 Check relations layer by layer

- **S85** **Check layer by layer, pair by pair, group by group, and seam by seam. Every piece goes through this.**
  - First check whether the relations on the tree hold.
  - Then check that each relation the sheet names holds in the body text as a proposition.
  - The outline itself, and whether decisions are carried out, are checked under FICCOutline.md 9.
  - Before submitting, and before drafting body text for new writing or an authorized reorganization, check in this order:
    - Check each node's focus by its layer (S86).
    - Check several kinds of representative parallel nodes by their checks (S88).
    - Check grouping and whole sets group by group (S24, S32).
    - Check from places with deeper unfolding and more turns all the way down to clauses (S91).

### 10.1 Check by layer

- **S86** **The focus of the check changes with the layer the node is in.**
  - Whether the whole book's or article's center is clear and whether necessary tasks are covered: check per FICCOutline.md 9.
    - This file checks whether the overall structure serves this goal, and what the reader finally gets.
  - For chapters or main parts, check what relatively complete task each part carries.
    - Check how it divides work with other parts, and why it appears in this order.
    - Check what it prepares for later content.
  - Parallel parts may be relatively independent. Among parts with dependencies, the depended-on block comes first.
  - Paragraph-layer expression and markers: FICCCompose.md 7. Wording checks on information cohesion, reference, and consistency of concepts: FICCVoice.md 7.
  - For sentences, check logical relations per 3, then check these three:
    - Whether judgments get explanation, support, or necessary qualification (FICCOutline.md 2.3).
    - Whether restatements add clarity, and whether turns have grounds in content (3.4).
    - Whether there are missing links in reasoning, leaps in meaning, or needless repetition.
- **S87** **When keeping suspense, information gaps, and deliberate blanks in literary narrative, state their function.**
  - State what role it plays in the whole.
  - State whether later text pays it off, and where.

### 10.2 Representative nodes

- **S88** **For representative parallel nodes such as several stories, points, or pieces of evidence, check the focus for each in the table below.**
  - Complementarity, contrast, progression, and counterexample in the table correspond to four relation types in 1.1: complementarity, comparison and contrast, progression and deepening, and objection and response.
  - Repeated verification means several blocks supporting the same step. Whether to keep it: check per the table's third row and 4.

| Node type | Key checks |
|---|---|
| Several stories or cases | Whether they are complementarity, contrast, progression, counterexample, or repeated verification; what each story adds |
| Several points | Whether they support the conclusion separately or derive it layer by layer; whether there are missing links or mutual contradictions |
| Several pieces of evidence | Whether they are independent, relevant, and sufficient; whether they only repeat information from the same source |
| Several narrative scenes | After a scene ends, what has changed in the situation, the characters, the relations, or the reader's understanding |
| Several character perspectives | Whether they add information, create conflicts of understanding, or reveal the limits of a single perspective |
| Several methods or steps | Whether there are sequential dependencies, conditional branches, parallel relations, and check-and-feedback loops |
| Several concepts or models | Whether they stand in inclusion, overlap, or opposition, or apply to different scales or conditions; whether they are mixed up |

### 10.3 Parent–child, grouping, subtree

- **S89** **Parent–child tests and subtree tests examine the outline itself and belong to FICCOutline.md 9. This file checks only grouping.**
  - The grouping test follows the check in S24.

### 10.4 Seam check

- **S90** **Seam check: the relation agent checks that each seam carries the relation the sheet names, as a proposition; the marker and wording check is the writer's (FICCVoice.md V22).**

### 10.5 What to check first, and where to start

- **S91** **Start from places with deeper unfolding, denser material, and more turns. Check layer by layer down to sentences and clauses.**
  - Check layer by layer whether each statement below it has a use.
- **S92** **Check these first.**
  - A relation the sheet names that the text does not carry (S21).
- **S93** **Openings check: FICCCompose.md C23. It is not this file's check.**
- **S94** **Mechanical checks do not prove the logic holds. Read the content they connect.**
  - Check for causation strengthened out of nothing, speculation turned into fact, or important qualifiers removed for smoothness.
  - Do not treat complete headings, equal paragraph counts, unchanged numbers, or “所以” (so) in every paragraph as a pass.
  - See references/FICCStructure-rationale.md 10.5.
- **S95** **When you find problems, point out the few that actually affect the writing, and give adjustments that can be carried out.**
  - Do not force fault-finding. For a simple task, hand over only the necessary part.
  - Fix hazards found in a cold read as defects before submitting. Do not let them pass by reporting a count.
    - Hazards are unclear subjects, unmarked relations, back-references that could point either way, and words the reader must decode.
  - Report to T0 when unsure whether something is a hazard.
  - How to report and who fixes: see FICCVoice.md 7.
  - See references/FICCStructure-rationale.md 10.5.
- **S96** **The tree is grown only when a traversal goes through and each layer reads as a complete small essay.**
  - Where a layer does not go through, hand that layer's opening back for rewriting per FICCCompose.md C01. Do not patch the wording.
  - Where content is misplaced or relations are mismarked, return a placement objection to the outline agent through T0.

## 11 Conclusion

What this file does as a whole: see the opening paragraph.

## 12 Appendix: Sources and on-demand references

Openings, carry-overs, and closes: FICCCompose.md. Wording and seams: FICCVoice.md, connective choice in FICCVoice.md 4.1. The user's original words and past rulings: see references/dev-notes.md section 35, and for rule history the same file. Rationale, examples, and history moved out of this file, by this file's section numbers: see references/FICCStructure-rationale.md. Classical sources and evidence grades, and the sources of examples and revision examples: see references/examples-and-rewrites.md, Appendix: Sources. Supplementary connectives, and the classification disagreements between the two classical systems: see references/connectives.md. Write the user's new corrections on relations into the section that governs them. The body text carries no date markers.
