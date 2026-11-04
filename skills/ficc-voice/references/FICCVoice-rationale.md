# FICCVoice rationale and distinctions

This file holds the rationale and examples moved out of FICCVoice.md in the terse rewrite, in sections by rule number. Each section first gives the original sentence, then one sentence on which rule it supports. The original sentences come from the FICCVoice.md then in force (first 16 hex digits of sha256: c62441e813405456). Ledger numbers are in （作者草稿）. Here each original sentence appears in English translation, and Chinese example phrases inside it stay in Chinese with an English gloss. The Chinese originals are in references/zh/FICCVoice-rationale.md. Write per FICCVoice.md. Consult this file only when a rule is unclear.

## Introduction

- Original (ledger #2): The first task of writing is to let the reader understand one thing accurately, together with its relation to what comes before and after.
  Supports: the introduction's “Give the whole first, then give information layer by layer”, the goal that all the rules serve together.
- Original (ledger #4): This file borrows the methods of the SEC handbook and ASD-STE100 for controlling comprehension load:
  Supports: the source of the introduction's method. For the borrowed texts and their scope, see FICCVoice-provenance.md.

## C01

- Original (ledger #43): Not merely saying “下文看总量和分组” (below we look at the total and the groups), but stating what different things the total and the groups reveal.
  Supports: C01 “Replace material lists with content judgments”, showing the content judgment an opening should state.

## C02

- Original (ledger #53): For example, if the text below says both that the overall burden has fallen and that one group is still under pressure, the opening should name both the whole and the divergence. It cannot just say “压力已缓解” (pressure has eased).
  Supports: C02 “When both sides of a contrast or turn belong to this paragraph, make the opening hold both sides”.

## C08

- Original (ledger #61): A paragraph serves to show one recognisable argument unit:
  Supports: the basis for C08's paragraphing actions (staying in the same paragraph, carrying over in a new paragraph, starting a new paragraph by argument unit).
- Original (wave-3 ledger L2-Voice, L177): Insisting on the original paragraph breaks does not count as faithfulness.
  Supports: C08 “Reorganize paragraphs by relation, not by length”. Keeping the source's paragraph breaks is no reason to skip reorganizing by relation.

## V07

- User ruling (2026-10-17): the earlier wording “use as few semicolons as possible” was judged too weak. V07 now bans semicolons in body prose, with no exceptions, and gives a search check and a fix, so that an AI writer has a rule rather than a preference. Semicolons that separate items inside a table cell or a list line are not body prose. This is the only semicolon rule. V19 no longer carries one.

## V11

- Original (ledger #96): For example, when the material establishes “A发行债券、B只为其中200万元担保” (A issues the bonds, and B guarantees only 2 million yuan of them), state each party's responsibility separately. It cannot be shortened to “A和B负责偿债” (A and B are responsible for repayment).
  Supports: V11, qualifiers still govern the original judgment after a split, and V15 “Do not merge several parties' responsibilities into one subject”.
- Original (ledger #97): A comparison, condition, or turn can itself form a complete judgment,
  Supports: V11 “Conditions, scope, and exceptions that directly qualify that judgment may stay in the same sentence”.
- Original (ledger #101): Short sentences serve to reduce the load of holding information and matching it back,
  Supports: V11 “If a sentence contains several judgments or actions that need separate statement, split them into several sentences”. Split sentences by the reader's load of holding and matching back.

## V15

- Original (ledger #122): “传输期间数据受损” (data were damaged during transmission) cannot be changed into “传输导致数据受损” (transmission damaged the data).
  Supports: V15 “If the agent is unknown, or you want to keep the patient as the topic, you may keep the passive”. When changing to the active, do not supply an agent that the material lacks.
- (V15) Sentence groups and complex sentences below the paragraph also have a center, all the way down to clauses.
- Moved here (2026-11-04, voice-trim): A complex sentence may be a complete small tree: the central clause comes first and may refer back to the previous sentence's claim. Several reasons stand side by side and grow heavier step by step; the conclusion clause brings out the conclusion and may nest concessions and conditions inside.
  Supports: V15 “Within a simple sentence, require only a clear sentence core and clear attachment of modifiers” and V16 “Do not force every sentence into one subject–verb–object template”: a complex sentence is not split by count. Example: references/examples-and-rewrites.md, block “FICCVoice V15, V19”.

## V16

- Original (ledger #128): For example, when it is known that “基金借钱购买债券” (the fund borrows money to buy bonds), write that action directly. Do not use “基金债券融资安排” (fund bond financing arrangement) and leave the reader to guess.
  Supports: V16, use a preposition, a verb, or a separate clause to state the relation inside a noun phrase that the material settles.

## V21

- (V21) That table keeps every word the user specified.

## V33

- Ruling 2026-10-11 (user): 统一，术语公司名之类的都用英文 (unify: terms, company names and the like all in English); home: FICCOutline.md O33, the language rule after the name table. The same day added: 承购方、兜底、残值担保用中文，中国机构不改英文，人名改英文 (offtaker, backstop and residual-value guarantee in Chinese; Chinese institutions stay in Chinese; personal names in English). V33 keeps only the order of precedence and the note that standard terms the table does not list follow O33.

## V37

- Original (ledger #321): A reader who knows finance does not thereby know the names and relations that this piece has not introduced.
  Supports: V37, the cold read uses only the finished draft and the name table, and tests as a reader who does not know this piece's names and relations.
- Original (ledger #323): When the six appear in clusters, they bury the judgment —
  Supports: V37 “Avoid AI tone”, explaining why the six are fixed only when they cluster.
- Change (2026-10-24): the six AI-tone items point to their home rules (one home per tell, MAINTAINERS.md “Where a rule lives”), so the cold reader takes each item's definition and check from the home. The 09-03 names and the cluster test are unchanged.

## V57

- Change (2026-10-24): the Check regex now equals voice_check H9 after the data-based trim (框架, 让步, 的分量 removed: 0 true hits in the 10 that voice_check gave on the 1009, 1012 and 1018 finals and the 3 on the 1009 pre-clean draft; counts and scopes in FICCVoice-provenance.md 33). The prose is unchanged.
