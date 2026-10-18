# Clarity acceptance

Read the body text first, then check it against the material. Scripts cannot replace these two readings.

## 1 Can the reader understand it

Cold-read per FICCVoice.md 7, V37 and V40. Give only the finished draft and the name table, and check whether the reader can restate this block's judgment, its relation to what comes before and after, and each judgment's subject and conditions of application. Report each problem with node, line number, original sentence, rule, and the specific misreading. Mark A when a misreading is likely; mark B when it slows reading. Fix the real problems of both classes; for a false alarm, state the reason.

Run the rule files' checks item by item: test the paragraph opening's coverage against the judgments that follow (FICCCompose.md C02); name the true antecedent at each seam (FICCCompose.md C13); find every condition and exception for each result (V17); replace each back-reference with the full name (V23); assume the word meanings are known, drop the notes, and check whether an extra premise of the argument goes missing (V29–30). This is not cutting every sentence short; it checks whether the reader still has to organize and pair up information on their own.

## 2 Is the meaning preserved

Do the two-way check per V38. From the material (the source excerpts and qualifiers the packet attaches), find item by item the new position of each fact, number, unit, base period, scope, condition, exception, negation, judgment strength, and attribution. Then check back from the new text sentence by sentence: any added action, cause and effect, generalization, or certain tone must have grounds. When reorganizing a complex paragraph, you may map old sentences to new positions for the moment; stop once the check is done, and make no fixed deliverable of it. Do not invent content the material lacks for the sake of the prose.

A new draft may split sentences and paragraphs within the settled relations; a revision stays within its authorization. Changes to position, claim, order, or length go to T0 for the outline agent; changes to relations go to T0 for the relation agent; splitting or merging paragraphs and changing a paragraph's task go to T0 for the composer (FICCVoice.md V04); the writer solves pure wording problems.

## 3 Scripts and format

The writer runs these before submitting a node, and T0 runs them after assembling the draft:

```sh
python3 ~/.claude/skills/ficc-voice/scripts/voice_check.py <稿件路径> --clarity --names <提纲路径>
python3 ~/.claude/skills/ficc-voice/scripts/cjk_space.py <稿件路径> --check
```

- H1 internal working labels, H5 quotation-mark format, and spacing errors between Chinese and English must be fixed. Necessary retentions in verbatim quotes of the original go to T0.
- In clarity mode, H2 roadmap, H3 short list, and H4 antithetical headings are only listed for review. The real problems are reporting the arrangement without a judgment, using labels in place of statements, and distorting the meaning for symmetry. Clear steps, complete points, and parallel headings that aid comparison may stay.
- The “！” items still follow the user's two existing style preferences: only the two lines “不是……而是” (not … but) and the dash are handled before submission; the rest are only counted. This is not a clarity standard. A fix must not harm the original meaning; report conflicts, such as a sentence kept verbatim, to T0.
- Verify the hazard list (`隐患清单`) item by item. Sentence length, clause count, noun-string length, and character frequency are only search clues; set no new thresholds (except the ten-sentence paragraph cap of FICCCompose.md C08). A hit with no reason for a misreading may pass once explained.

Read the actual usage; do not replace words from a banned-word list. Fix runs of roadmap sentences, hollow claims, template tone, term pileups, end-of-paragraph uplift, and transition filler per FICCVoice.md V37 (avoid AI tone). Also watch for empty labels, unfounded antithesis or parallelism, strong words such as “本质上” (in essence) that stand in for reasoning, and generic prescriptive sentences with no agent. A single occurrence of these forms is not in itself an error. A numeric report cannot prove a draft clear, and zero script hits do not excuse the cold read.

Script arguments and limits: scripts/README.md. Layout: references/format-and-maintenance.md.
