# FICCStructure rationale and distinctions

This file holds the rationale, examples, transition sentences, and history moved out of FICCStructure.md in the terse rewrite, in sections by the section numbers of the version in force. Each entry first gives the original sentence, then one sentence on which rule it supports. The original sentences come from the FICCStructure.md then in force (first 16 hex digits of sha256: 2cbf30ff2ccbd905). Ledger numbers are in the task directory, （作者草稿）. Here each original sentence appears in English translation, and Chinese example phrases inside it stay in Chinese with an English gloss. The Chinese originals are kept in the author's archive and are not included in this release. Write per FICCStructure.md. Consult this file only when a rule is unclear. “Origin” entries record the date and ruling markers that the terse version removed. For the user's original words and rulings, references/dev-notes.md section 35 governs. Section numbers here follow the FICCStructure.md layout of 2026-10-16; since 2026-11-04 sections 9 and 10 here are FICCStructure.md 6 and 7, and since 2026-11-21 section 11 here (Conclusion) has no section of its own in FICCStructure.md. On 2026-11-21 the entries on C and V rules (sections 6 to 8.3, the C19 entry of 2.4 and the C12 entries of 9.1) moved to references/FICCVoice-rationale.md, under their rule ids; each section they left keeps a one-line pointer.

## 1.2

- Original (ledger L055): A chapter and another chapter, or a paragraph and a distant sentence, may also stand in a relation.
  Supports: S02 “When you identify a relation type, state in full which item relates to which, through what content, and what relation it forms.” An example of “used across levels”: relations may hold between chapters, and between a paragraph and a distant sentence.

## 1.3

- Original (ledger L027): Since relations may overlap, the most easily confused points must be distinguished first;
  Supports: S04 “Before using the relation library, distinguish the six most error-prone points.” Why the six distinctions come first: relations may overlap, so the most confusable points are separated first.

## 1.4

- Original (ledger L086): Once the unfolding is set, the arrangement is set.
  Supports: S05 “First judge how the child nodes unfold the parent node. The unfolding decides the arrangement.” The reason for judging the unfolding first: once the unfolding is set, the arrangement is set.

## 2

- Original (ledger L112): With the relation library in hand, what this block does upward for the trunk it belongs to can also be stated: how it unfolds the parent node decides how it hangs.
  Supports: S07 “Before hanging a block, state what it does for the parent node.” The transition from section 1 to section 2: with the relation library in hand, judge what a block does upward and how it hangs.

## 2.1

- Origin (ledger L127a): the original sentence carried “（用户2026-10-11（七））” (user, 2026-10-11, item 七). Per the contract, the terse version drops the marker; the rule stays in S09.

## 2.4

- Original (ledger L171): These uses differ, and they must not be set side by side just because “都有关” (they are all related).
  Supports: S14 “Hang a satellite beside the step it serves. Do not set it side by side with the trunk.” The reason a satellite states which kind of unfolding it is: the uses differ, so “都有关” (all related) is no reason to set them side by side.
- Moved (2026-11-21): the C19 entry (ledger L182a) is in references/FICCVoice-rationale.md, under C19.

## 3

- Original (ledger L183): Once the vertical relations are set, how the several blocks under one parent node connect is a relation in another direction.
  Supports: S17 “For horizontal relations, look first at sibling nodes under the same parent node.” The transition from section 2 to section 3: once the vertical is set, judge the horizontal relations among the blocks under one parent node.
- (S17) Only a correct judgment yields an order.

## 3.1

- Origin (ledger L205): the original sentence carried “（10-10（三）裁定）” (ruling of 10-10, item 三). Per the contract, the terse version drops the marker; the rule stays in S21.
- Original (ledger L224b): side by side in expression, yet still growing heavier step by step in meaning,
  Supports: S23 “Treat a short progression as parallel in writing, and mark ‘而且’ (moreover) and ‘甚至’ (even) as usual.” The reason a short progression is written as parallel but still judged as progression: the expression is side by side, and the meaning grows heavier step by step.
- (S21) Numbering reports only position.

## 3.2

- Origin (ledger L232): the original sentence carried “（用户10-16）” (user, 10-16). Per the contract, the terse version drops the marker; the rule stays in S25.
- Origin (ledger L233b): the original sentence carried “（以下是T0默认）” (the following are T0 defaults). Per the contract, the terse version drops the marker; the rule stays in S25.

## 3.3

- Original (ledger L244): The markers of stages and aspects only tell the reader which stage or which aspect the text has reached;
  Supports: S26 “Stages and different aspects are ways of unfolding. Judge the relations between stages and between aspects per S18.” Stage and aspect markers only report position; the meaning rests on each sub-point's first sentence and on the connectives.

## 3.4

- Original (ledger L247a): Using the wrong one is worse than using none: change one connective, and the complex-sentence relation changes with it,
  Supports: S27 “Separate easily confused relations pair by pair. Put both sides of a turn on the same dimension.” The reason to separate confusable relations pair by pair: change one connective, and the complex-sentence relation changes with it.

## 3.5

- Original (ledger L266): At one seam, a logical relation and an unfolding relation may hold at once: the later sentence gives a cause, which is at the same time the grounds for the earlier sentence's judgment, so this seam is both cause and effect and assertion and support;
  Supports: S29 “When one seam carries two layers of relation, identify both. Mark the layer the reader needs most.” An example of two layers at one seam: the later sentence gives a cause, which is at the same time the grounds for the earlier judgment.
- Original (ledger L267): The later sentence explains a statement in the earlier sentence, and in doing so also sets its scope, so this seam is both explanation and qualification.
  Supports: S29 “When one seam carries two layers of relation, identify both. Mark the layer the reader needs most.” An example of two layers at one seam: the later sentence explains a statement and at the same time sets its scope.
- Original (ledger L270): Marking an add-on relation above parallel, and writing a short progression as parallel, are both cases of two layers at one seam (3.1).
  Supports: S29 “When one seam carries two layers of relation, identify both. Mark the layer the reader needs most.” Marking the add-on relation above parallel and writing a short progression as parallel are both cases of two layers at one seam (see S21, S23).
- Original (ledger L271): This differs from two layers of relation nested together: there, two seams each carry one layer, and the outer and inner layers each get their own markers (8.1).
  Supports: S29 “When one seam carries two layers of relation, identify both. Mark the layer the reader needs most.” The difference between two layers at one seam and nested layers: in nesting, two seams each carry one layer, each with its own marker.
- Original (ledger L272): Relations are not only between two adjacent sentences either: the third sentence may explain the first, and the last sentence may summarize the four before it.
  Supports: S30 “Judge relations by where a node hangs on the tree, not by which sentence it sits next to.” Relations are not only between adjacent sentences: the third sentence explains the first, and the last sentence summarizes the four before it.
- Original (ledger L275): Sibling nodes may also stand in argument (assertion and support) or rebuttal (objection and response);
  Supports: S31 “When siblings stand in argument or rebuttal, arrange them as siblings first. Re-hang only after the satellite test.” Siblings may stand in argument (assertion and support) or rebuttal (objection and response); before re-hanging, pass the satellite test first.
- (S30) The tree already draws relations across intervening sentences: those sentences are child nodes or satellites under the same parent node (for the tree, see FICCOutline.md 1).

## 4

- Original (ledger L277): Once relations are judged pair by pair, a whole group must still be looked at together: whether, combined, they are enough to complete the parent node's task.
  Supports: S32 “Make the child nodes under one parent node together sufficient to complete the parent node's task.” The transition from section 3 to section 4: after judging pair by pair, look at the whole group together.

## 5

- Original (ledger L289): Once a whole group is enough, still see whether it relates to distant nodes.
  Supports: S33 “Judge relations with distant nodes by the relation library too. Write them as outline annotations. Do not change this branch's arrangement.” The transition from section 4 to section 5: once a whole group is enough, look at its relations with distant nodes.
- Original (ledger L291b): A tree outline shows only where content mainly sits;
  Supports: S33 “Judge relations with distant nodes by the relation library too. Write them as outline annotations. Do not change this branch's arrangement.” The reason cross-branch relations are written as annotations: a tree outline shows only where content mainly sits.
- Original (ledger L292): Echoes, foreshadowing, contrasts, and dependencies across chapters cannot be drawn on the tree.
  Supports: S33 “Judge relations with distant nodes by the relation library too. Write them as outline annotations. Do not change this branch's arrangement.” The reason cross-branch relations are written as annotations: echoes, foreshadowing, contrasts, and dependencies across chapters cannot be drawn on the tree.

## 6

- Moved (2026-11-21) to references/FICCVoice-rationale.md, under C01.

## 6.1

- Moved (2026-11-21) to references/FICCVoice-rationale.md, under C01.

## 6.2

- Moved (2026-11-21) to references/FICCVoice-rationale.md, under C06.

## 6.3

- Moved (2026-11-21) to references/FICCVoice-rationale.md, under C13, C14 and C15.

## 6.4

- Moved (2026-11-21) to references/FICCVoice-rationale.md, under C17 and C19.

## 7

- Moved (2026-11-21) to references/FICCVoice-rationale.md, under V15.

## 7.1

- Moved (2026-11-21) to references/FICCVoice-rationale.md, under C01 and V22.

## 7.3

- Moved (2026-11-21) to references/FICCVoice-rationale.md, under V25.

## 7.5

- Moved (2026-11-21) to references/FICCVoice-rationale.md, under V29.

## 8

- Moved (2026-11-21) to references/FICCVoice-rationale.md, under V22.

## 8.1

- Moved (2026-11-21) to references/FICCVoice-rationale.md, under V22 and V53.

## 8.2

- Moved (2026-11-21) to references/FICCVoice-rationale.md, under V22.

## 8.3

- Moved (2026-11-21) to references/FICCVoice-rationale.md, under C20.

## 9

- Original (ledger L562): With relations marked, the results of judgment and placement are to be written into a relation sheet for the writer.
  Supports: S74 “Give each relation one home (`分担`, `接前`, `关键边表`) and unseal an edge only with one linking source sentence.” The transition from section 8 to section 9: with relations marked, the results are written down for the writer, each relation in its one slot of the living outline.

## 9.1

- Origin (ledger L582): the original sentence carried “用户2026-10-14” (user, 2026-10-14). Per the contract, the terse version drops the marker; the rule stays in S79.
- Moved (2026-11-21): the C12 entries (ledger L587b, L595) are in references/FICCVoice-rationale.md, under C12.

## 10

- Origin (ledger L621): the original sentence carried “（依用户2026-10-12（十五）的结构编辑规格）” (per the user's 2026-10-12 (十五) structural editing specification). Per the contract, the terse version drops the marker; the rule stays in S85.

## 10.1

- Origin (ledger L629): the original sentence carried “段首是主旨或主题是用户2026-10-14裁定，细则是T0同日默认” (paragraph opening as claim or topic is the user's 2026-10-14 ruling; the details are T0's defaults of the same day). Per the contract, the terse version drops the marker; the rule stays in S86.
- Origin (ledger L636): the original sentence carried “（用户10-16）” (user, 10-16). Per the contract, the terse version drops the marker; the rule stays in S86.

## 10.4

- Origin (ledger L678): the original sentence carried “（用户2026-10-14）” (user, 2026-10-14). Per the contract, the terse version drops the marker; the rule stays in S90.

## 10.5

- Original (ledger L689): Mechanical checks can find numbering gaps, working labels, and spaces; they cannot prove the logic holds.
  Supports: S94 “Mechanical checks do not prove the logic holds. Read the content they connect.” The limit of mechanical checks: they can find numbering gaps, working labels, and spaces, but cannot prove the logic holds.
- Origin (ledger L694): the original sentence carried “（T0同日据此定的默认；拿不准是不是隐患的，报T0）” (T0's default set on this basis the same day; when unsure whether something is a hazard, report to T0). Per the contract, the terse version drops the marker; the rule stays in S95.
- Original (ledger L695): The grounds are the user's original words of 2026-10-14: “冷读有隐患的句子绝大多数给其他读者读都有严重问题” (sentences with hazards in a cold read almost all cause serious problems for other readers).
  Supports: S95 “When you find problems, point out the few that actually affect the writing, and give adjustments that can be carried out.” The grounds for fixing cold-read hazards as defects: the user's original words of 10-14.

## 11 Conclusion

- Original (ledger L706): If you can answer, the later checks are only adding markers;
  Supports: S96 “The tree is grown only when a traversal goes through and each layer reads as a complete small essay.” When the three questions can be answered, the later checks only add markers.
- Original (ledger L707): If you cannot answer, the fault is in position; what must move is this block of content, and adding words to sentences cannot make up for it.
  Supports: S96 “The tree is grown only when a traversal goes through and each layer reads as a complete small essay.” When the three questions cannot be answered, the fault is in position: move the content, and do not add words to sentences.

## Appendix

- Original (ledger L709): The following records the history of the rules;
  Note: the lead-in sentence of the history record.
- Original (ledger L710): Currently, per the user's latest requirement of 2026-10-15, Structure judges placement and the relations above, beside, and below; Outline maintains the outline; and Voice writes the settled relations clearly and accurately.
  Note: the current grounds for the division of labor among the three agents (user, 10-15).
- Original (ledger L714): The division of labor among the three files (FICCOutline generates and maintains the outline, FICCStructure sets relations, FICCVoice governs style, rhetoric, and expression), and the four boundaries of connectives, node templates, leads and headings, and the counter-view, follow the user's approval of 2026-10-12; of these, where the counter-view goes moved on 2026-10-13, together with position-setting, to FICCOutline.md 5.3, and this file governs only its relation to the main line and its linking-back sentence;
  Note: the origin of the three files' division of labor and the four boundaries (user approval 10-12; the position of the counter-view moved to FICCOutline.md 5.3 on 10-13).
- Original (ledger L715): The former 1 “定位置” (set position) (placing material by task, and the handling of new stories or new material; sources are there) moved on 2026-10-13 to FICCOutline.md 5 under the three-agent relay plan the user approved; 5 cross-branch links and 9 relation sheet were created the same day; the former 7 hand-back part was split into the placement record of FICCOutline.md 5 and the relation sheet of 9;
  Note: the former 1 “定位置” (set position) moved to FICCOutline.md 5 on 10-13; 5 and 9 were created the same day.
- Original (ledger L716): The three types of unfolding relation (now merged into 1.4) and two layers of relation at one seam follow the split the user approved the same day; the content comes from the user's first post that day (three layers: logical relation, unfolding relation, cohesion relation);
  Note: the origin of the three unfolding types and of two layers at one seam (user approval 10-12).
- Original (ledger L717): Treating carry-over–transition as position rather than listing it among unfolding relations (the user's post listed it among unfolding relations), and marking the layer the reader needs most when one seam has two layers, were defaults T0 proposed the same day, which the user endorsed the same day with “按你的建议来” (go with your suggestion);
  Note: the origin of treating carry-over–transition as position and of marking the most-needed layer at a two-layer seam (user 10-12, “按你的建议来” (go with your suggestion)).
- Original (ledger L718): Arranging carry-over paragraphs as a progressing chain follows the user's approval of 2026-10-11.
  Note: the origin of arranging carry-over paragraphs as a progressing chain (user, 10-11).
- Original (ledger L719): The measurement-basis splicing of 2.4, stating what is worth seeing after giving numbers in 7.3, and completing hook material in 6.1 were moved here from FICCVoice.md on 2026-10-12 per the user's instruction in the FICCVoice audit.
  Note: the three items in 2.4, 7.3, and 6.1 moved here from FICCVoice.md on 10-12.
- Original (ledger L720): The relation library, the whole-set check, the layer-by-layer check, the representative node table, and the 7 hand-back part follow the user's requirement of 2026-10-12;
  Note: the origin of the relation library, the whole-set check, the layer-by-layer check, and the representative node table (user, 10-12).
- Original (ledger L721): The mapping table in 1.4 and the sibling re-hang test in 3.5 are T0's application of this, replacing the earlier same-day default “同级节点判成观点与论据、补充与限定、异议与回应时改挂卫星” (re-hang as a satellite when sibling nodes are judged as view and argument, supplement and qualification, or objection and response).
  Note: the mapping table in 1.4 and the re-hang test in 3.5 are T0's application.
- Original (ledger L722): After the 2026-10-13 audit, revised in place per T0's rulings: the wording in 3.4 and elsewhere, and the sentence-level wording checks in 10.1, handed to FICCVoice.md (then its 4.1 and 7; now FICCVoice.md V13 and FICCVoice.md §4); the parent–child and subtree checks of 10.3 handed to FICCOutline.md 9;
  Note: in-place revisions after the 10-13 audit (wording and wording checks handed to FICCVoice.md, parent–child checks handed to FICCOutline.md 9).
- Original (ledger L723): The items in FICCOutline.md 5 on figure–text correspondence, hanging sources by point, citation writing, and the subjects of parties along a chain moved into 7.3, 7.5; the check of openings at each layer of the finished draft moved from FICCOutline.md 9 into 10.5.
  Note: the items moved on 10-13 from FICCOutline.md into 7.3, 7.5 and 10.5.
- Original (ledger L724): Old records describe past versions and do not replace this file.
  Note: old records do not replace this file.
- Original (ledger L727): On 2026-10-13 the user said “重新修改一下FICC三个写作体系，不再每次都对照我给你的原文再写，你可以有自己的风格，我会逐渐纠正。” (revise the three FICC writing systems; stop writing against the original texts I gave you every time; you may have your own style, and I will correct it gradually): the “我” (I) used for argument in this file became neutral wording or explicitly “用户” (the user), and author self-descriptions such as “比我过去的文章更严” (stricter than my past articles), “我那几期月报都没有” (none of those monthly reports of mine had it), and “也是我的习惯” (also my habit) were deleted; the rules themselves did not change;
  Note: the user's 10-13 ruling to stop writing against the originals, and the author self-descriptions deleted as a result; the user's original words.
- Original (ledger L728): “这是我定的规矩” (this is a rule I set) was originally written by T0 on 2026-10-11; it now states the user ruling it rests on;
  Note: the origin of the correction to the sentence “这是我定的规矩” (this is a rule I set).
- Original (ledger L730): The same day, per T0's rulings, report titles go into the source list when citing others in 7.3, and 2.2 “必要定义放在使用前” (place necessary definitions before use) is annotated as being about order, with in-sentence hanging in FICCVoice.md V32 (then its 5.1).
  Note: T0 rulings of 10-13: report titles into the source list in 7.3, and the annotation on the order of definitions in 2.2.
