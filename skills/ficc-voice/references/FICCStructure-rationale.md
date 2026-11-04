# FICCStructure rationale and distinctions

This file holds the rationale, examples, transition sentences, and history moved out of FICCStructure.md in the terse rewrite, in sections by the section numbers of the version in force. Each entry first gives the original sentence, then one sentence on which rule it supports. The original sentences come from the FICCStructure.md then in force (first 16 hex digits of sha256: 2cbf30ff2ccbd905). Ledger numbers are in the task directory, （作者草稿）. Here each original sentence appears in English translation, and Chinese example phrases inside it stay in Chinese with an English gloss. The Chinese originals are in references/zh/FICCStructure-rationale.md. Write per FICCStructure.md. Consult this file only when a rule is unclear. “Origin” entries record the date and ruling markers that the terse version removed. For the user's original words and rulings, references/dev-notes.md section 35 governs. Section numbers here follow the FICCStructure.md layout of 2026-10-16; since 2026-11-04 sections 9, 10 and 11 here are FICCStructure.md 6, 7 and 8.

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
- Original (ledger L182a): An aside that is not brought back dilutes the close of the node it sits in:
  Supports: C19 “After a story, example, or scene, state in one sentence what it shows.” The reason to delete tails that do not lead back to the conclusion: an aside not brought back dilutes the close of its node.

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

- Original (ledger L301): With cross-branch relations also judged, the next step is to place them in positions in the body text, starting with openings, carry-overs, between layers, and closes at section level and above.
  Supports: C01 “At every layer, the conclusion comes at the opening. Keep this at each layer.” The transition from section 5 to section 6: after cross-branch relations are judged, place them first in the openings, carry-overs, between layers, and closes at section level and above.

## 6.1

- Origin (ledger L309): the original sentence carried “（依用户2026-10-10“主旨—承接—分论点—总结收尾”的格式和2026-10-11（六）用到所有层级的裁定）” (per the user's 2026-10-10 format “claim–carry-over–sub-points–summary close” and the 2026-10-11 (六) ruling applying it to all levels). Per the contract, the terse version drops the marker; the rule stays in C01.

## 6.2

- Original (ledger L350b): If it brings in facts right away, it is already the first child node;
  Supports: C06 “A carry-over sits one layer above the child nodes. It states only each step's conclusion and the relations between steps.” The reason a carry-over carries no facts: if it brings in facts right away, it is already the first child node.

## 6.3

- Origin (ledger L362): the original sentence carried “（依用户2026-10-10的格式裁定）” (per the user's 2026-10-10 format ruling). Per the contract, the terse version drops the marker; the rule stays in C13.
- Original (ledger L372): When a block sits inside the main line but is not a link of it, what follows has to be reconnected;
  Supports: C15 “A signpost sentence points only to the block right after it. Move a stray block out per the hanging rules.” The reason a stray block is moved out: it sits inside the main line without being a link of it, so what follows has to be reconnected.
- Original (ledger L375): Without all four, the reader must guess every relation.
  Supports: C14 “Allocate markers between layers by scale. Above section level, let four devices together make the relations readable.” The reason for combining the four devices: without all four, the reader must guess every relation.
- (C14) The most common group relations above section level are four: induction, sequence, deduction, and contrast.

## 6.4

- Original (ledger L377a): Openings and seams govern how a block comes in; the close governs how it goes out:
  Supports: C17 “The close gathers the child nodes back into this block's claim and moves one step forward.” The division of labor of the close: openings and seams govern how a block comes in, and the close governs how it goes out.
- Original (ledger L385): The opening foreshadows the middle, and the ending recalls the earlier claim; only then are beginning and end one body.
  Supports: C17 “A close moves one step forward. Do not restate the claim in other words.” The rationale for beginning and end as one body: the opening foreshadows the middle, and the ending recalls the earlier claim.
- Origin (ledger L396): the original sentence carried “（依用户2026-10-10“总结收尾”的格式）” (per the user's 2026-10-10 “summary close” format). Per the contract, the terse version drops the marker; the rule stays in C17.
- Original (ledger L400b): Writing it for every block turns it into end-of-paragraph uplift.
  Supports: C19 “Do not write every layer as ‘总起—分述—总之’ (overall opening–itemized account–in sum).” The reason “这意味着什么” (what this means) is not written for every block: writing it for every block turns it into end-of-paragraph uplift.
- Original (ledger L401b): It reads as a formula; better not to add it.
  Supports: C19 “Do not write every layer as ‘总起—分述—总之’ (overall opening–itemized account–in sum).” The reason not to force carry-overs and closes to fill a format: it reads as a formula, so it is better not to add them.
- (C17) This does not conflict with a claim at the opening.

## 7

- Original (ledger L408): With positions at section level and above settled, the same rules go further down to paragraphs and sentences.
  Supports: V15 “Reading a sentence, you can find who or what is in what state, did what, and mainly shows which point.” The transition from section 6 to section 7: with section level and above settled, the same rules go down to paragraphs and sentences.
- Original (ledger L413): Here we add only what is specific to paragraphs and sentences.
  Supports: V15 “Reading a sentence, you can find who or what is in what state, did what, and mainly shows which point.” The scope of section 7: it adds only what is specific to paragraphs and sentences.

## 7.1

- Origin (ledger L416): the original sentence carried “（用户2026-10-10）” (user, 2026-10-10). Per the contract, the terse version drops the marker; the rule stays in C01.
- Original (ledger L417a): The same day, item (五) added a requirement on information content:
  Supports: C01 “The first sentence summarizes the whole paragraph's view: reading only it, the reader should know what the paragraph asserts, and ideally on what main grounds.” The origin of the first sentence “stating the view itself”: the user's 10-10 item (五) added the requirement on information content.
- Origin (ledger L418a): the original sentence carried “（用户2026-10-14）” (user, 2026-10-14). Per the contract, the terse version drops the marker; the rule stays in C01.
- Original (ledger L418c): The user's example is “所谓财政重新定价的观点有很大争议” (the so-called fiscal repricing view is highly contested).
  Supports: C01 “A paragraph opening must be the paragraph's claim or its topic.” The user's example of a topic sentence, showing that “the topic states the subject's current state”.
- Original (ledger L419): The following items are defaults T0 derived on 2026-10-14 from the user's example and the 10-10 ruling; they are not the user's original words.
  Supports: C01 “A paragraph opening must be the paragraph's claim or its topic.” Origin: the items in C01 on topic, material sentences, and disagreement paragraphs are defaults T0 set on 10-14 from the user's example and the 10-10 ruling.
- Original (ledger L433b): (User 2026-10-14: “读者的眼光会第一眼落到主语上” (the reader's eye lands first on the subject), and the sentence must “体现出与上级、同级和下级节点极其明确的关系，否则很容易读偏” (show an extremely clear relation to the nodes above, beside, and below, or it is easily misread).)
  Supports: V22 “In a paragraph-opening sentence or a node's opening sentence, show at the very start its relation to the level above and to the sibling it follows.” The grounds for showing the relation at the sentence start: the user's original words of 10-14.
- Original (ledger L436): The following items are defaults T0 set the same day from the user's words; they are not the user's original words.
  Supports: V22 “In a paragraph-opening sentence or a node's opening sentence, show at the very start its relation to the level above and to the sibling it follows.” Origin: the connective list in V22 and the two exceptions in V22 are defaults T0 set the same day from the user's words.
- Origin (ledger L444): the original sentence carried “（T0同日的默认）” (T0's default of the same day). Per the contract, the terse version drops the marker; the rule stays in V22.

## 7.3

- Origin (ledger L475): the original sentence carried “（用户10-16）” (user, 10-16). Per the contract, the terse version drops the marker; the rule stays in V25.

## 7.5

- Original (ledger L512): Sentences also have main and subordinate.
  Supports: V29 “Separate main and subordinate between sentences. A note does not count as a step in a sentence group.” Lead-in sentence: sentences also have main and subordinate.
- (V29) Layout line breaks are not the only basis for judging structure.

## 8

- Original (ledger L529): With paragraphs written correctly and each sentence attached, the relations have reached the leaves;
  Supports: V52 “Put connectives at the seam between two things.” The transition from section 7 to section 8: with paragraphs and sentences each attached, the relations have reached the leaves.
- Original (ledger L530): What remains is to mark them at every seam.
  Supports: V52 “Put connectives at the seam between two things.” The transition from section 7 to section 8: what remains is to mark the relations at every seam.

## 8.1

- Origin (ledger L542): the original sentence carried “（用户2026-10-14）” (user, 2026-10-14). Per the contract, the terse version drops the marker; the rule stays in V52.
- Original (ledger L545): With an inserted sentence or route sentence in between, the reader takes the adjacent sentence as the antecedent;
  Supports: V53 “Keep a connective right next to its true antecedent.” The reason a connective stays next to its true antecedent: with an inserted sentence in between, the reader takes the adjacent sentence as the antecedent.

## 8.2

- Original (ledger L551): Grammar research calls this a general rule of colloquial complex sentences.
  Supports: V22 “Latter-clause markers bear the load and are not omitted. Add former-clause markers as needed.” The grounds for not omitting latter-clause markers: grammar research calls this a general rule of colloquial complex sentences.
- Original (ledger L552): A progression often has only a latter-clause marker; the earlier sentence carries no word, and the relation is still clear;
  Supports: V22 “Latter-clause markers bear the load and are not omitted. Add former-clause markers as needed.” A progression has only a latter-clause marker; the earlier sentence carries no word, and the relation is still clear.
- Original (ledger L553): Conversely, keeping only “虽然” (although) and dropping “但是” (but) leaves the reader unable to follow.
  Supports: V22 “Latter-clause markers bear the load and are not omitted. Add former-clause markers as needed.” Counterexample: keeping only “虽然” (although) and dropping “但是” (but) leaves the reader unable to follow.

## 8.3

- Original (ledger L561): When preview and payoff do not match, the reader thinks a paragraph is missing.
  Supports: C20 “As many steps as the claim and carry-over sentence preview, the sub-points pay off, in the same order.” The reason preview and payoff must match: if they do not, the reader thinks a paragraph is missing.

## 9

- Original (ledger L562): With relations marked, the results of judgment and placement are to be written into a relation sheet for the writer.
  Supports: S74 “Write the results of relation judgment and seam marking into a relation sheet for the writer.” The transition from section 8 to section 9: with relations marked, the results go into a relation sheet for the writer.

## 9.1

- Origin (ledger L582): the original sentence carried “用户2026-10-14” (user, 2026-10-14). Per the contract, the terse version drops the marker; the rule stays in S79.
- Original (ledger L587b): The same story placed in different positions and written in different ways can have completely different effects,
  Supports: C12 “Item 5, writing advice: set the position first, then the way of writing.” The reason to set position before the way of writing: the same story in different positions and written differently has completely different effects.
- Original (ledger L595): That the length cap still holds after adding full names and base periods rests on exactly this rule; it compresses restatement, not facts;
  Supports: C12 “Item 5, writing advice: set the position first, then the way of writing.” The role of the designated full-statement place: the length cap still holds after adding full names and base periods; it compresses restatement, not facts.

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
- Original (ledger L722): After the 2026-10-13 audit, revised in place per T0's rulings: the wording in 3.4 and elsewhere, and the sentence-level wording checks in 10.1, handed to FICCVoice.md 4.1 and 7; the parent–child and subtree checks of 10.3 handed to FICCOutline.md 9;
  Note: in-place revisions after the 10-13 audit (wording and wording checks handed to FICCVoice.md, parent–child checks handed to FICCOutline.md 9).
- Original (ledger L723): The items in FICCOutline.md 5 on figure–text correspondence, hanging sources by point, citation writing, and the subjects of parties along a chain moved into 7.3, 7.5; the check of openings at each layer of the finished draft moved from FICCOutline.md 9 into 10.5.
  Note: the items moved on 10-13 from FICCOutline.md into 7.3, 7.5 and 10.5.
- Original (ledger L724): Old records describe past versions and do not replace this file.
  Note: old records do not replace this file.
- Original (ledger L727): On 2026-10-13 the user said “重新修改一下FICC三个写作体系，不再每次都对照我给你的原文再写，你可以有自己的风格，我会逐渐纠正。” (revise the three FICC writing systems; stop writing against the original texts I gave you every time; you may have your own style, and I will correct it gradually): the “我” (I) used for argument in this file became neutral wording or explicitly “用户” (the user), and author self-descriptions such as “比我过去的文章更严” (stricter than my past articles), “我那几期月报都没有” (none of those monthly reports of mine had it), and “也是我的习惯” (also my habit) were deleted; the rules themselves did not change;
  Note: the user's 10-13 ruling to stop writing against the originals, and the author self-descriptions deleted as a result; the user's original words.
- Original (ledger L728): “这是我定的规矩” (this is a rule I set) was originally written by T0 on 2026-10-11; it now states the user ruling it rests on;
  Note: the origin of the correction to the sentence “这是我定的规矩” (this is a rule I set).
- Original (ledger L730): The same day, per T0's rulings, report titles go into the source list when citing others in 7.3, and 2.2 “必要定义放在使用前” (place necessary definitions before use) is annotated as being about order, with in-sentence hanging in FICCVoice.md 5.1.
  Note: T0 rulings of 10-13: report titles into the source list in 7.3, and the annotation on the order of definitions in 2.2.
