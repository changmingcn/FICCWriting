# FICCVoice excerpt: cold-read mode (ficc-writer cold-read)

Section 1 copies FICCVoice.md verbatim (`**` removed; checked by scripts/xref_check.py). Full rules: FICCVoice.md.

## 1 Rules

- V22 Make the relation at each seam visible to the reader, especially turn, cause and effect, condition, limitation, and concession.
  - Check: after writing, look first for the most often missing ones: inference, “但是” (but), progression, concession, explication, back-reference, and “甚至” (even) and “其实” (actually).
  - Check: read only the first few characters of each paragraph-opening sentence and node opening sentence. They show its relation to the level above and to the sibling it follows.
  - Check: after writing a paragraph, run each seam through the seven checks below. Where a seam fails, fix the wording if wording can fix it. Do not pad with added words.
    1. Preview and payoff: FICCCompose.md C20.
    2. Each same-layer seam carries a word of the class the relation sheet names (the proposition is the relation agent’s check, FICCStructure.md S90; the word is the writer’s).
    3. Back-test each marked word against its row in references/connectives.md: what precedes “所以” (so) must be a cause, what follows “而且” (moreover) must go one layer further, and the two sides of “但是” (but) sit on the same dimension. Where inference belongs, “既然、可见” (since, evidently) is present. A “因为” (because) or “所以” that only restates or splits the first half: FICCStructure.md S28.
    4. Latter-clause markers not omitted, and the relation of each paragraph opening and node opening sentence shown: this rule.
    5. The antecedent of paragraph-opening and sentence-opening connectives: V53.
    6. Suppositions and conditions stay hypothetical: V17.
    7. Items after a colon or dash: V19.
- V23 Keep the same name pointing to the same object.
  - After intervening material, or when carrying over from an earlier sibling, name the object again.
  - For a concept with a count, list all its members at first mention. Do not silently change the referent later.
  - Check: replace each “这、它、前者、上述” (this, it, the former, the above) with the full name. Where two objects fit, change it to a naming form such as “这笔贷款、这一偿还义务” (this loan, this repayment obligation). Where no antecedent can be found, reintroduce the object.
- V32 Explain the one point the reader lacks. Do not let a term stand in for a mechanism.
  - For the V34 reader, you need not re-explain basic financial knowledge item by item.
  - Explain definitions, measurement bases, and ambiguous words specific to this piece at their first actual use.
  - Explain until the reader can keep reading, and stop there.
  - Where everyday words can state the action and the mechanism, say it plainly. Use necessary standard terms as they are.
  - Take names from the outline's name table:
    - The table holds only coined nouns and nouns with several variant names.
    - The table has four columns: 名字 (name) ｜ 指什么与口径 (referent and measurement basis) ｜ 本篇写法 (form used in this piece) ｜ 不许用的叫法 (forbidden names).
    - The outline agent maintains the table.
  - Every name in the body text is either in the table or a standard term. Send new names outside the table through T0 to the outline agent, which rules on them and maintains the table.
  - Use market names. For same thing, same name, see V23.
  - Do not replace indicators, data series, or groups with coined short labels.
  - Allow at most one coined name per piece. Introduce it in the lead, explain it on the spot, and keep using it.
  - In sentences with numbers, still use the indicator name.
  - Where a forbidden word in the name table carries a condition, judge by that condition.
  - Use few terms:
    - Put few new nouns in one paragraph. The fewer kinds, the better.
    - For plain-language parentheticals, see V29.
    - When something is hard to explain, give the reasoning first and the name after (“这种手法，我们叫做……”, this technique we call…).
    - Draw comparisons from things the reader has experienced.
    - Do not insert encyclopedia entries. Use the topic word directly. Do not gloss it repeatedly.
  - Do not give names to views or mechanisms. Use everyday verbs:
    - For other people's views, write who holds them and what they believe. Do not compress them into “对手的读法” (the opponent's reading).
    - State a mechanism in full the first time. Afterwards refer back with a phrase such as “这两条规则” (these two rules). Do not coin a code name.
    - Do not apply “收敛、付价、标零、兑现” (converge, pay the price, mark to zero, cash in) to economic facts.
    - Do not let “读数、口径” (reading, measurement basis) appear in place of the numbers and the method.
- V57 Views and inferences are not objects. A view, reading, explanation or inference is never the subject or object of a verb that moves it: it does not “加强、变轻、占上风、站在一边、并存”, and it is not counted (“三种读法”). Write who holds it and what they believe (“Barclays看成技术性抛售”), or what we think (“我们认为”, “在我们看来”, “更像是先后”); when several views stand side by side, write “三种说法” once and name each holder. No label for an interpretive move of ours: 读法, 解读, 视角, 框架, 判别读数 and the like are out even when the outline carries them — the outliner translates such words before they reach a claim line (FICCOutline.md O91). Check: grep the node for `读法|解读|视角|判别读数|推断加强|判断.{0,4}加强|占上风|站在.{1,8}一边` and read each hit; a hit whose subject is a company, a house, a price or 我们 passes; `voice_check.py --clarity` lists the hits as review candidates (H9), never as hard faults. 框架 is read by eye: in house drafts it is a deal or policy term.
- V36 Convert to written register while keeping information, analysis, and personality. Do not write officialese.
  - Remove classroom cues and useless restatement.
  - Lecture notes may use more characters and dialogue. Specific cases may switch back to report style.
  - Set no minimum for personal pronouns and no quota for jokes.
  - Use parallelism and strong words only where the content needs them. The second half of “不是……而是” (not… but…) must have concrete grounds.
  - Do not change original sentences that the author designated to keep verbatim.
  - See references/written-register.md: transcript details.
- V37 First use the finished draft to test whether the reader must do organising work.
  - Without the material or the relation sheet, using only the finished draft and the name table:
    - Read paragraph by paragraph. State each sentence's object, judgment, conditions, and the layer above that it serves.
  - Paragraph openings and the openings check: FICCCompose.md C23.
  - Every place lets the reader know three things:
    - What is being said now.
    - Why it is said here.
    - How the following text makes it clear.
  - Check: after reading a local passage, you can state its main meaning and why the next sentence connects here.
  - If you cannot, first handle mixed layers, stray material, missing premises, false turns, and unclear references, then revise the wording.
  - Mark the following obstacles, then fix that spot:
    - Responsibility can be matched only by rereading.
    - A pronoun must be guessed from among several names.
    - The reader must supply causes or regroup content for the author.
  - Avoid AI tone: check each paragraph for the following six. Fix them where they cluster. Handle a single occurrence per its own rule.
    - Roadmap sentences: FICCCompose.md C01, C06 (script H2).
    - Hollow claims: FICCCompose.md C02, V38, V36.
    - Template tone (every paragraph shaped the same): FICCCompose.md C09, C11, C19.
    - Term pileups: V32.
    - End-of-paragraph uplift: FICCCompose.md C17, C19 (script density row 段末升华).
    - Transition fillers: FICCCompose.md C17, V22 (script density row 本质上等五词).
  - See references/FICCVoice-rationale.md V37.
- V38 Then check both ways, from material to new text and from new text to material.
  - For each meaning split out per V02, find its new location.
  - Lose no judgment, fact, number, base period, condition, exception, negation, degree, or attribution, and do not shift any of them to another object.
  - Check the new text back sentence by sentence. Every added action, causal word, generalisation, and note of certainty must have grounds.
  - In a complex reorganisation, you may temporarily mark new locations beside the source sentences. Stop once the check is done.
  - Finally, look specifically at split and merged sentences, and check each item:
    - Whether a shared condition now governs only the first sentence.
    - Whether an exception wrongly extends to everything.
    - Whether several subjects' responsibilities have been merged.
  - Then check subject–predicate fit, modifier placement, and missing characters.
  - The writer fixes wording problems.
- V39 Handle script flags by comprehension obstacle, not by driving counts to zero.
  - When a flag such as clause count or noun-string length fires, check each item:
    - Whether the sentence core is interrupted.
    - Whether a condition must be matched back.
    - Whether a modifier can be read two ways.
  - When you find a problem, fix the matching expression. If you cannot name a misreading or a comprehension load, keep the text and state why.
  - Even when counts stay within limits, still check for missing relations, missing conditions, and wrong attribution.
  - Do not lower counts by deleting qualifiers, hiding them in parentheses, or switching to abbreviations.
  - The paragraph length cap (FICCCompose.md C08) is a hard limit. This rule covers only the script's other flags.
- V40 Report reading problems that can be located and fixed.
  - Writer: cold-read your own node before submitting. After the draft is assembled, a separate cold reader reads with only the finished draft and the name table (dispatch: SKILL.md 2).
  - The cold read reports only and does not edit. For each spot, list the node, line number, original sentence, and matching rule.
  - For each spot, write what it might be misread as or what must be looked back for, and where the text is actually lacking.
  - Mark A for a likely misreading and B for slowed reading. Do not report only “长、绕、不顺” (long, convoluted, not smooth).
  - Resolve both kinds of real problems before submitting. Send uncertain ones to T0. Give a reason for each false alarm.

## 2 Use

- Read only the full text and the name table (recheck: dispatch-notes 2.3); no scripts.
- C24 and the C rules V37's AI-tone list points to (C01, C02, C06, C09, C11, C17, C19): open FICCCompose.md at each C number (full rule and Check line); compose-excerpt.md keeps their intent lines only.
- Per finding: node, line, quote, rule, severity A/B (V40).
- Two added defect classes: nominalized views (V57) and enumerations that restate full names (C24).
