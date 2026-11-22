# Clarity acceptance

Relay step ④ (SKILL.md 2). Read the body text first, then check it against the originals; scripts cannot replace these two readings. Checkers locate and classify; only the patch seat writes body sentences.

## 1 A01 三报五禁: cold read, source check and findings

- **Cold read before scripts.** The cold reader reads at the FICCVoice.md V34 bar and gets only the finished draft and the full name table; it opens the script output only after its findings are written. Check per FICCVoice.md V37 and V40 that the reader can restate each block's judgment, its relation to what comes before and after, and each judgment's subject and conditions of application. Run the checks item by item: the paragraph opening covers the judgments that follow (FICCVoice.md C02); each seam names its true antecedent (C13); every condition and exception of a result is found (V17); each back-reference can take the full name (V23); with word meanings known and notes dropped, no premise of the argument goes missing (V29). This is not cutting sentences short; it checks whether the reader must still pair up information alone.
  - Views are not objects: no 读法／解读／视角／判别读数, no view that 加强／占上风／站在一边 (V57).
  - Enumerated outcomes define indicators once and combine in short form (C24).
- **The source-check seat holds the originals independently** (核对席; tier: `shared-protocols/source-check.md`, Review tiers), never the writer's receipt alone. It does the two-way check of FICCVoice.md V38: from the material, find item by item the new position of each fact, number, unit, base period, scope, condition, exception, negation, judgment strength and attribution; from the new text, sentence by sentence, any added action, cause and effect, generalization or certain tone must have grounds. An old-to-new sentence map is scratch for the check, never a deliverable.
- **三报: a finding reports only** `节点与原句位置｜会误读成什么｜动作类（拆／并／移／回指／交还核源）或待核问题号`, graded A (a misreading is likely) or B (it slows reading), with the rule id where one applies. A false alarm states its reason.
- **五禁.**
  - No model-written example fix (示范改句) and no replacement wording.
  - Without the original in hand, prescribe no cause (因果), direction (方向), holder (持权人), unit (单位) or confidence (把握度).
  - A content gap goes out as a numbered question (待核问题号) to the source-check seat.
  - The verifier pastes source lines and recomputations (原件行与复算式) and never writes a body sentence.

## 2 A02 Bounded patches and the five-gate recheck

- **Scope.** A patch changes only the sentences a finding names, plus the opening sentence of their paragraph when the change directly affects it (直接波及的本段首句). Any other changed sentence sends the patch back.
- **B grade adds nothing.** A pure readability (B-grade) patch keeps the node's net CJK count from growing, on every attempt.
- **No new number in a patch.** A patch that needs a new derived number goes back to the living outline as an 算式 row (FICCOutline.md §5; FICCVoice.md V26) and returns once the row is signed.
- **Five gates for every new sentence**, T0's own hand edits included: value (数值), adjacent unit (紧邻单位), holder (持权人), direction word (方向词) and condition polarity (条件极性: 或 never becomes 和).
- **Sign-off.** A numeric or basis difference is cleared only by the source-check seat's sign-off against the original (原件签认); the writer's argument does not clear it.
- **Return routes.** A new draft may split sentences and paragraphs within the settled relations; a revision stays within its authorization. Changes to position, claim, order or length go to T0 for the outliner; changes to relations go to T0 for the structurer; paragraph organization and wording stay with the writer (FICCVoice.md V04). Do not invent content the material lacks for the sake of the prose.
- **Pace.** One patch round plus one targeted recheck of the changed sentences (dispatch-notes 2.3–2.4).

## 3 Scripts and format

The writer runs these before submitting a node, and T0 runs them after assembling the draft:

```sh
python3 ~/.claude/skills/ficc-voice/scripts/voice_check.py <稿件路径> --clarity --names <提纲路径>
```

- voice_check v4.7: H1–H6 are hard in the default mode. Under `--clarity`, H1 internal working labels, H5 quotation-mark format and H6 semicolons in prose must be fixed. Necessary retentions in verbatim quotes of the original go to T0.
- H10 (a paragraph over ten sentences; the 400-CJK hint only with `voice_check.py --max-para-cjk 400`) is a review hint, not a cut line (FICCVoice.md C08).
- A paragraph with ≥30 number strings is listed as `重段待处置`. The exit code does not change, but the paragraph must be disposed of before handover: table the isomorphic grid, split it at a sub-question or basis seam with 拆后四带, or carry the verifier-signed proof of one indivisible claim (FICCVoice.md C08).
- In clarity mode, H2 roadmap, H3 short list, and H4 antithetical headings are only listed for review. The real problems are reporting the arrangement without a judgment, using labels in place of statements, and distorting the meaning for symmetry. Clear steps, complete points, and parallel headings that aid comparison may stay.
- “！” rows (user ruling 2026-10-13): only “不是……而是” (not … but; criterion FICCVoice.md V36) and the dash (FICCVoice.md V19) are handled before submission, until the row no longer carries “！”; the rest are only counted. This is not a clarity standard. A fix must not harm the original meaning; report conflicts, such as a sentence kept verbatim, to T0.
- Verify the hazard list (`隐患清单`) item by item. Sentence length, clause count, noun-string length, and character frequency are only search clues; set no new thresholds. A hit with no reason for a misreading may pass once explained.
- `段首信噪比` lists a lead, part or section opening, or paragraph first sentence packed with numbers, asides, a source compilation or a roadmap: check that the claim leads and the detail moves later (FICCVoice.md C01).

Read the actual usage; do not replace words from a banned-word list. Fix AI-tone runs per FICCVoice.md V37 (its six items point to their home rules). Also watch for empty labels, unfounded antithesis or parallelism, strong words such as “本质上” (in essence) that stand in for reasoning, and generic prescriptive sentences with no agent. A single occurrence of these forms is not in itself an error. A numeric report cannot prove a draft clear, and zero script hits do not excuse the cold read.

Script arguments and limits: scripts/README.md. Layout: references/format-and-maintenance.md.
