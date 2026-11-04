# FICCVoice.md精简审计

日期2026-11-04。对象`skills/ficc-voice/FICCVoice.md`（1.1.0，449行）。本报告只读不改。第2步按批注执行，每处改动前再核一遍引用。

## 结论

| 项 | 数值 |
|---|---|
| 现状 | 44,267字节，42,635字符（budget.json按字符封顶42,635，余量0） |
| 稳妥合计 | 约2.5K字节（稳妥表S1–S13） |
| 待裁合计 | 约2.1K字节（D1取压缩版、不含D9）到2.6K字节（D1取纯指针版）（待裁表D1–D9） |
| 全部采纳后 | 约39.2K–39.7K字节，约38.2K–38.7K字符 |
| 目标32–35K | 达不到，差4–8K |

达不到的原因不是没找够，是锁住的部分太大。不动集合合计约15K字节（释义与前两项有少量重叠）：摘录点名“in full”的13条规则（V07、V10–V14、V20、V26–V28、V32、V36、V37）11.9K，V57（2026-10-21回装、10-24改查法、voice_check H9绑定）1.1K，14条退役号指针0.5K，84处中文引文的英文释义1.8K。剩下的29K里，纯重复、内嵌清单和说理只有5K出头。要再降，只能动“in full”集合，这超出本次授权，所以如实报到这里。FICCOutline上次53K里找到2.3K稳妥可删，本次稳妥2.5K，比例相当。

另一个发现：稳妥集合S1–S13一行都不碰polish摘录，只碰patch一行（S9）和coldread一行（S2的L437）。写手席平时读的polish摘录19.5K，主要靠待裁的D1（九项检查）才降得下来。

## 每条规则的字节数和它所在的摘录

字节、字符按规则下非空行合计。摘录列：润=voice-excerpt-polish，初=draft，补=patch，冷=coldread；全=该摘录逐行收了整条，意=只收意图行，意查=收意图行加Check行及其父项。外部点名：FICCVoice.md、四份摘录、rationale、migration、examples-and-rewrites、CHANGELOG、provenance、dev-notes之外的文件（ref=references/，sc=scripts/，ag=agents/）。

| 规则 | 起始行 | 字节 | 字符 | 摘录 | 外部点名 |
|---|---|---|---|---|---|
| V01 | 7 | 565 | 545 | 润意查、初全 | ref/dispatch-notes.md |
| V02 | 13 | 613 | 609 | 润意、初全 | sc/voice_check.py, sc/README.md |
| V03 | 19 | 540 | 520 | 润意查、初全 | 无 |
| V04 | 24 | 956 | 954 | 润意、初全、补全 | ref/compose-excerpt.md, ref/clarity-acceptance.md, FICCCompose.md, ag/ficc-composer.md |
| V05 | 37 | 33 | 31 | 指针 | sc/voice_check.py, sc/README.md, FICCCompose.md |
| V06 | 38 | 33 | 31 | 指针 | sc/README.md, FICCCompose.md |
| V41 | 39 | 33 | 31 | 指针 | FICCCompose.md |
| V42 | 40 | 33 | 31 | 指针 | 无 |
| V43 | 41 | 33 | 31 | 指针 | sc/README.md |
| V44 | 42 | 33 | 31 | 指针 | FICCCompose.md |
| V07 | 43 | 622 | 599 | 润全、补全 | ref/connectives.md, sc/voice_check.py, sc/README.md, FICCStructure.md, FICCCompose.md, ag/ficc-writer.md |
| V45 | 48 | 33 | 31 | 指针 | 无 |
| V46 | 49 | 33 | 31 | 指针 | FICCCompose.md |
| V47 | 50 | 33 | 31 | 指针 | 无 |
| V08 | 51 | 338 | 323 | 无 | sc/README.md, FICCCompose.md |
| V48 | 53 | 33 | 31 | 指针 | 无 |
| V49 | 54 | 33 | 31 | 指针 | 无 |
| V09 | 55 | 33 | 31 | 指针 | FICCCompose.md |
| V50 | 56 | 33 | 31 | 指针 | 无 |
| V51 | 57 | 33 | 31 | 指针 | 无 |
| V10 | 61 | 303 | 303 | 润全、补全 | sc/voice_check.py, sc/README.md, ag/ficc-writer.md |
| V11 | 64 | 425 | 425 | 润全、补全 | 无 |
| V12 | 67 | 390 | 368 | 润全、补全 | sc/README.md |
| V13 | 70 | 480 | 480 | 润全、补全 | sc/voice_check.py, sc/README.md |
| V14 | 73 | 757 | 757 | 润全、补全 | ag/ficc-writer.md |
| V15 | 81 | 2178 | 2088 | 润意查 | ref/writing-checklist.md, FICCOutline.md |
| V16 | 99 | 1695 | 1631 | 润意 | FICCOutline.md |
| V17 | 115 | 1530 | 1412 | 润意查 | ref/clarity-acceptance.md |
| V18 | 128 | 711 | 685 | 润意查 | 无 |
| V19 | 134 | 874 | 866 | 润意查 | ref/writing-checklist.md, ref/clarity-acceptance.md |
| V20 | 141 | 793 | 713 | 润全、补全 | FICCOutline.md |
| V21 | 153 | 610 | 594 | 润意 | ref/writing-checklist.md |
| V22 | 160 | 6082 | 5651 | 润意查、冷意查 | ref/connectives.md, ref/writing-checklist.md, FICCStructure.md, FICCCompose.md |
| V52 | 215 | 202 | 189 | 润意 | ref/connectives.md, ref/writing-checklist.md, FICCStructure.md, FICCCompose.md |
| V53 | 217 | 736 | 736 | 润意查 | ref/writing-checklist.md, FICCCompose.md |
| V54 | 224 | 139 | 139 | 润全 | ref/connectives.md, ref/writing-checklist.md |
| V55 | 225 | 33 | 31 | 指针 | 无 |
| V23 | 229 | 586 | 538 | 润意查、冷全 | ref/clarity-acceptance.md, sc/README.md |
| V24 | 236 | 1638 | 1590 | 润意查、补全 | 无 |
| V25 | 254 | 1221 | 1203 | 润意 | ref/connectives.md, sc/voice_check.py, sc/README.md |
| V26 | 269 | 1155 | 1135 | 润全、初全、补全 | 无 |
| V27 | 279 | 1525 | 1495 | 润全、初全、补全 | ref/writing-checklist.md |
| V28 | 294 | 645 | 633 | 润全、初全、补全 | 无 |
| V29 | 303 | 1577 | 1567 | 润意查 | ref/clarity-acceptance.md, sc/README.md |
| V30 | 318 | 802 | 768 | 润意查 | 无 |
| V31 | 327 | 408 | 408 | 润意 | ref/writing-checklist.md, FICCCompose.md |
| V32 | 335 | 2507 | 2369 | 润全、冷全 | 无 |
| V33 | 361 | 948 | 946 | 润意 | 无 |
| V57 | 367 | 1126 | 922 | 润全、补全、冷全 | ref/clarity-acceptance.md, sc/voice_check.py, sc/README.md |
| V34 | 371 | 773 | 753 | 润意 | 无 |
| V35 | 378 | 526 | 526 | 润意 | 无 |
| V36 | 385 | 644 | 624 | 润全、冷全 | ref/clarity-acceptance.md |
| V37 | 395 | 1618 | 1598 | 润全、冷全 | ref/compose-excerpt.md, ref/clarity-acceptance.md, sc/voice_check.py, sc/README.md, FICCCompose.md |
| V38 | 417 | 980 | 978 | 润意、初全、补全、冷全 | ref/clarity-acceptance.md, FICCCompose.md |
| V39 | 428 | 905 | 905 | 润意、冷全 | 无 |
| V40 | 438 | 771 | 755 | 润意、冷全 | ref/compose-excerpt.md, ref/dispatch-notes.md, ref/clarity-acceptance.md, sc/voice_check.py, sc/README.md, FICCCompose.md |

规则之外的部分：导言L3为487字节，第2节引言L35为143字节，第8节两段641字节，各级标题约300字节，空行约60字节。

## 候选改动

每条写改法、省多少字节、动哪些摘录和引用。行号指现行FICCVoice.md。字节是估算，含换行，误差在±10。

### 稳妥（纯重复、与参考文件重复的内嵌清单、可挪去rationale或examples的说理和例子）

| 编号 | 位置 | 改法 | 省 | 摘录 | 引用 |
|---|---|---|---|---|---|
| S1 | L35、L449 | 两处都写了migration-2026-10-17.md的指针。L35改为“Retired numbers; map: references/migration-2026-10-17.md.”，L449删去末句“The rest moved on to FICCCompose.md (map: …)” | 约120 | 无 | 无 |
| S2 | L98、L114、L214、L223、L317、L331、L437 | 删七行“See references/…”。L98、L114指FICCVoice-rationale.md V15、V16，该文件本来就按V号分节；L214、L223、L317指FICCStructure-rationale.md 7.1、8.2、8.1、7.5，第8节L449已经整体给了这组指针；L331（format）和L437（clarity-acceptance）第8节各有一句。第8节补一句“Rationale by V number: references/FICCVoice-rationale.md.”（约60字节） | 约350 | coldread删L437（V39冷全） | 无。V07、V37的See行属“in full”不动 |
| S3 | L161、L162、L171、L174 | V22里与connectives.md重复的用词清单。L161（第一第二、首先然后接着）和L162（一是二是）与connectives.md第1节并列、承接两行及第6节重复，删。L171 `Use fixed words and 而……也 as the table specifies` 与connectives.md第6节末条重复，删，L170末尾加“; fixed words are exempt (references/connectives.md 6)”。L174（第一，在句内或段首、冒号小标题）与connectives.md第6节和C10重复，改为“Numbering inside a sentence or at a paragraph opening: references/connectives.md 6, FICCCompose.md C10.” | 约400 | 无（polish、coldread对V22只收L160、L172、L175、L202–L213） | connectives.md第13行“See FICCVoice.md V22”指的是后分句标记不省略（L163–L167），不受影响 |
| S4 | L173 | “Mark every seam that has a relation. Between same-level parallel items, mark carry-over, repetition, emphasis, and deepening.”前半与V52意图行相同，后半与V08正文相同（C13第192行“Which marker: FICCVoice.md V08, V22”），且九项检查第2项再说一遍。删 | 约130 | 无 | 无 |
| S5 | L192 | 压成“The relation to the level below is carried by preview and payoff (FICCCompose.md C20), not marked at the sentence start.” | 约80 | 无 | 无 |
| S6 | L200、L201 | L200“Use conjunctions only to join sentences whose logical relation is very clear. See V13.”是V13和V21 L156的复述；L201“When you cannot identify the relation with confidence, hand it back to T0.”是V04的复述（V01、V03的Check行已各写一次“hand it back per V04”）。删 | 约170 | 无 | 无 |
| S7 | L84、L93 | V15。L84“A complex sentence may be a complete small tree: …”是对复句形态的描述，规则形态在V16 L105（“Do not force every sentence into the same subject–verb–object template”），例句已在examples-and-rewrites.md“FICCVoice V15, V19 (formerly section 7.5…)”块。挪去FICCVoice-rationale.md V15节。L93“Such as both renting server rooms…”是例子，挪去examples-and-rewrites.md“FICCVoice 3”块 | 约410 | 无（polish对V15只收L81、L97） | FICCOutline.md第26行引的是L83，保留 |
| S8 | L154 | V21。“Prefer the words in references/connectives.md, section “现行连接词表”… See that table for the full relation classification.”压成“Words and relation classes: references/connectives.md 1.” | 约100 | 无 | 无 |
| S9 | L250 | V24末行“Showing the relation at a paragraph or node opening, which connective to use, and when a relation may stay unmarked: see V22.”压成“Relation at the opening: V22.” | 约95 | patch同步改这一行（V24补全） | 无 |
| S10 | L262、L263 | V25。L262 `In a paragraph that enters directly with 第一，…` 与connectives.md第6节第3条和C10重复，删。L263同层十条、超十二拆分，逐字等于FICCStructure.md S25（L237–L238），FICCOutline.md L208又有一份；改为“Group size: FICCStructure.md S25.” | 约360 | 无（polish对V25只收L254） | dev-notes第3节记这是用户2026-10-16的上限裁定，裁定的家在S25，V25留指针即可 |
| S11 | L308 | V29。“Give definitions and glosses at the first real use of the word.”与V32 L337重复。压成“A short gloss may merge directly into the sentence (first use: V32).” | 约50 | 无 | 无 |
| S12 | L105 | V16。只改措辞：“A mechanism sentence may run several steps, a comparison several parts, a judgment its conditions and reservations. Do not force every sentence into one subject–verb–object template.” | 约100 | 无 | 无 |
| S13 | L3 | 导言前三句（Outline、Structure、Compose各管什么）是SKILL.md和README的内容。改为“FICCVoice writes the judgments settled by FICCOutline, FICCStructure and FICCCompose as clear, explicit, concrete sentences.”后文不动 | 约100 | 无 | FICCVoice-rationale.md“Introduction”节引的两句（“Give the whole first…”、SEC handbook）现行导言本来就没有，不受影响 |

稳妥小计约2,465字节。

### 待裁

| 编号 | 位置 | 改法 | 省 | 摘录 | 引用、顾虑 |
|---|---|---|---|---|---|
| D1 | L203–L213 | V22九项检查，1,354字节。两个方案。(a)只指向：“Check: run each seam through FICCCompose.md C20 and C23, the Check lines of V17, V19, V53, and its row in references/connectives.md.”，省约1,150，但丢掉第2项（词的类别对关系单）、第3项（所以前是因、而且后进一层、但是两侧同一维度）、第7项（既然可见；因为所以写成复述）。(b)压缩：保留九项的内容，合成七项约600字节，省约750。第1项C20；第2项加注S90（关系席查命题，写手查词）；第3项与第7项合并，“因为/所以写成复述”指FICCStructure.md S28的Check行（L276–L278与第7项几乎逐字相同）；第4项和第9项合成“this rule”一项；第5、6、8项保留为指针。L204“Where a seam fails…”并入Check行 | (a)约1,150 (b)约750 | polish和coldread同步换成新文本（两份都收L203–L213） | budget.json 2026-11-03 r1记录：按refuter F4/F5和lesson L2，polish、coldread、patch须收“载重规则的全文（V22 nine checks）”。该裁定说的是摘录要照抄全文，不是九项不能压，压缩后摘录照抄新文本仍合规。但C23查的是各层开头是否说出主旨，不查接缝的词，所以方案(a)“只指向C20/C23”会丢第2、3、7项的内容，建议取(b) |
| D2 | L182–L188 | V22按关系选词菜单，392字节。FICCStructure-rationale.md 7.1 L436明说这张菜单是T0由用户话语定的默认项，不是用户原话。(a)合成一行：`Choose the word by relation from references/connectives.md 1: turn 但是、不过; cause 所以、因此; condition or limit 只是, 但……只有; concession 虽然; progression 而且、更.` 省约215。(b)纯指针“Which word: references/connectives.md 1.”省约300，但“但……只有”不在connectives.md任何一行，要补到转折行 | (a)约215 (b)约300 | 无 | (b)要改connectives.md一行 |
| D3 | L189–L191 | “The two revisions the user gave are exactly the two ways (references/examples-and-rewrites.md, block …, Revision example 4)”是指向例子的说明，L190、L191是那两个改法的提炼。改法：删L189；L190并入L179（“Put a connective that states the relation at the start of the sentence, with the named judgment as the subject.”）；L191保留，缩进到L178之下；第8节补“Examples and the user's own edits: references/examples-and-rewrites.md (headings by section and V number).”（第8节现在没有这个文件的指针） | 约170 | 无 | 2026-10-14用户亲改〔亲改〕的痕迹。规则句本身是T0写的，亲改原文在examples-and-rewrites.md不动，所以列待裁 |
| D4 | L181 | `Such as 这个判断 or 上面说的两路. For back-reference wording, see 4.3.` 例子部分挪去examples-and-rewrites.md“FICCVoice V22”块，指针并入L180括注“(wording: 4.3)” | 约125 | 无 | 中文例句按规矩可留，所以不算稳妥 |
| D5 | L172 | S3、S4之后“Use connectives heavily:”之下只剩L175一行Check，可把L175升一级、删L172 | 约30 | polish、coldread删L172 | 随D1一起做 |
| D6 | V30→V29 | V29 L316的Check（去掉注解读下去，若后文还要它，按V30处理）和V30 L326的Check（跳过括号重读主判断）是同一个测试的两面。把V30正文（L319–L326）压成两行并入V29，V30留指针“- **V30** → V29” | 约330 | polish收V30的意图行和Check行（L318、L326）。退役后摘录不能再写“- V30 …”，否则xref_check报RETIRED-RULE，所以要把xref_check.py第229行VOICE_EXCERPTS的polish元组里的'V30'删掉 | 要改引用：FICCVoice.md L31“See V29–V30”、clarity-acceptance.md第1节“(V29–30)”。要改脚本一个元组。clarity-acceptance.md余量0，这一改只会变短 |
| D7 | L362 | V33首条551字节，复述FICCOutline.md O33名字表后的语言规则（外国人名、公司、机构、媒体、标准英文术语用英文；中国的用中文）。压成“Choose a name and its language in this order: the name table's ruling (FICCOutline.md O32–O33); then the language rule after the table (O33), which also governs standard terms the table does not list; only where both leave the choice open, the readability choice below.” | 约300 | 无 | 这条“标准英文术语写英文”可能是2026-10的裁定，FICCOutline-rationale.md和公开版dev-notes只剩标题，查不到日期。裁定的家在O33，V33留的是指针加一句适用范围，请确认 |
| D8 | L109、L110 | V16。L109“Keep standard terms and official names whole…”与V32 L339、V29 L312部分重复，但它在V16里是“不要拆标准术语”的例外，有位置意义。L110 `Do not delete words by counting nouns or 的` 与导言“not by cutting at a character count”和V39 L435重复 | 约195 | 无 | 两行都是重复，但位置上各有理由，请裁 |
| D9 | 第2节14条指针 | 并成一张两列迁移表，省约250。但xref_check.py的RULE_DEF（第194行）和RULE_PTR（第201行）只认“- **Vnn** → …”独立行，表格行不算定义也不算退役，改表后所有引这些号的地方都报MISSING-RULE。要同时改两条正则和第994–998行的自检样例 | 约250 | 无 | 建议不做：省250字节，换一次脚本改动和自检样例改动 |

待裁小计：取D1(b)、D2(a)、不含D9约2,100字节；取D1(a)、D2(b)约2,600字节；D9另加250。

### 不动

- “in full”集合：V07、V10–V14、V20、V26–V28、V32、V36、V37，共11.9K。其中V07的See行（L47）、V37的See行（L416）、V36的See行（L391）也不动。
- V57：2026-10-21回装、10-24改查法，正则与voice_check.py H9绑定，clarity-acceptance.md第1节点名。
- V22 L176–L177：FICCStructure-rationale.md 7.1 L433b记为用户2026-10-14原话（“读者的眼光会第一眼落到主语上”）的直接依据。L194–L199两个例外是T0同日默认项，但它们是这条规则的判据，不是说理，留。
- V34 L373“Publish as the author. Your own style is allowed…”：用户2026-10-13裁定（FICCStructure-rationale.md L259）。
- V52、V53、V54：合并进V22省不到200字节，而C13、S27附近、connectives.md第116行、writing-checklist.md第12–13条都按号引用，合并后全要改。
- V08：有正文的活指针。它的正文是C13“Which marker: FICCVoice.md V08, V22”的答案，S4删L173后它是唯一的家。
- V12与V23、V13与V21：V12、V13不动，V23、V21各有对方没有的内容（V23列举成员、替换“这它前者上述”的Check行被clarity-acceptance.md点名；V21的示例与证明、解说与递进之分被writing-checklist.md第14条点名）。不合并。
- V01–V04、V38：draft摘录第2节说“this file adds V01–V04 and V38 in full”。本次没找到可删行，顺带不动。
- 14条退役号指针、“## 5”与“### 5.1”同名标题（“FICCVoice.md 5.1”在14个文件里被引用，标题是xref目标）、84处中文引文的英文释义。

### 改后各文件估算

| 文件 | 现字符 | 稳妥后 | 稳妥加待裁后（D1取b） |
|---|---|---|---|
| FICCVoice.md | 42,635 | 约40,250 | 约38,200 |
| voice-excerpt-polish.md | 18,691 | 18,691 | 约17,600 |
| voice-excerpt-coldread.md | 11,069 | 约10,970 | 约10,200 |
| voice-excerpt-patch.md | 11,895 | 约11,800 | 约11,800 |
| voice-excerpt-draft.md | 7,312 | 7,312 | 7,312 |
| clarity-acceptance.md | 4,515 | 4,515 | 约4,510（只在D6） |

封顶处理：budget.json只能降。改完后在仓库副本上跑`budget_check.py --set-baseline --reason`取得新尺寸，再把files里的数字和history新条目抄回`skills/ficc-voice/scripts/budget.json`，root仍写`~/.claude`。

## 第5节是否拆出

第5节（5.1 V26–V31，5.2 V32、V33、V57）共10.8K字节。拆成新文件后FICCVoice.md约33.5K，正好落在目标区间，这是它唯一的好处。改动面如下。

| 要改的东西 | 说明 |
|---|---|
| scripts/xref_check.py | 第195行RULE_FILE把V绑在FICCVoice.md，定义查找（第686–690行）只读这一个文件；要么加一张“号→文件”的例外表，要么让V在两个文件里找。check_voice_excerpts（第554行）只拿FICCVoice.md的行建逐字池，draft、patch、polish收的V26–V28、V29–V33、V57全会报EXCERPT-MISMATCH，要并入新文件的行。FILES、REQUIRED元组，文件头说明，第994–1012行自检样例和selftest_voice_excerpts都要跟着改。全文46处提到FICCVoice |
| 规则号约定 | 四个规则文件和五张卡都按“字母=文件”引用（“FICCVoice.md V27”）。拆后V号跨两个文件，这个约定第一次破例；不能换字母，因为号冻结 |
| SKILL.md | 第2节⑤“FICCVoice.md by V number”，第3节验收表“FICCVoice.md 5, name table”一行，第4节第10条“The four rule files” |
| 四份摘录 | 第3行“Full rules: FICCVoice.md”；draft、patch、polish收V26–V28，polish收V29–V33，三份收V57 |
| “FICCVoice.md 5／5.1／5.2”节引用 | 14个文件约30处：examples-and-rewrites.md 7处（含“## FICCVoice 5.1”“## FICCVoice 5.2”两个H型标题）、FICCOutline.md 6处、writing-checklist.md 4处、FICCOutline-rationale.md 2处、FICCStructure.md 2处、FICCCompose.md 2处、connectives.md、clarity-rewrites.md、lecture-terms.md、FICCStructure-rationale.md、SKILL.md、scripts/README.md、ficc-hand/references/map-template.md各1处。第5节标题要留在FICCVoice.md作锚点并各留一行指针（照FICCStructure 6–8的做法），所以实际省的是10.8K减约200 |
| “FICCVoice.md V26–V33、V57”规则引用 | scripts/README.md 6处、voice_check.py 5处（H9注释）、migration-2026-10-17.md 5处、CHANGELOG 4处、writing-checklist.md 3处、FICCOutline-rationale.md 3处、clarity-acceptance.md 2处、provenance 2处、FICCStructure-rationale.md 2处、FICCCompose.md第273行、dev-notes、FICCVoice-rationale.md各1处 |
| budget.json | 新文件入表，FICCVoice.md封顶下调 |
| README、CHANGELOG、docs/CLAUDE-snippet.md、agents/ficc-writer.md | 技能表和卡上“FICCVoice.md”的说法 |

建议不拆。理由：按SKILL.md第2节和写手卡，没有哪个席位整读FICCVoice.md。T0只读SKILL.md，写手读四份摘录，“Open FICCVoice.md at a V number when its action is unclear”是按号查，不是整读。所以FICCVoice.md的大小不进任何席位的上下文，进上下文的是polish摘录19.5K。拆第5节对写手的实际读量一个字不省，却要改一个脚本的核心约定和十几个文件的引用。要降写手的读量，做D1（九项检查）比拆文件管用：polish从18,691降到约17,600字符。

如果仍想拆，最省事的做法是xref_check.py加一张显式例外表（{'V26': 'FICCTerms.md', …}），其余按上表逐项改，估计一个工作单元，自检要全过。

## 请你裁定

1. D1取(a)还是(b)。我建议(b)。
2. D2取(a)还是(b)。取(b)要在connectives.md转折行补“但……只有”。
3. D3、D4带2026-10-14亲改的痕迹，是否允许动。
4. D6（V30并入V29）要改xref_check.py第229行一个元组、FICCVoice.md L31和clarity-acceptance.md一处。是否做。
5. D7（V33首条压缩）：“标准英文术语写英文”是否是有日期的裁定。查不到就按O33是它的家处理。
6. D8两行是否删。
7. D9（指针并表）建议不做，请确认。
8. 封顶：改完把各文件封顶降到新尺寸，history里reason写“voice-trim per docs/FICCVoice-trim-audit.md, user approval <日期>”。请确认措辞。

## 第二步的执行顺序（供参考）

1. 新建分支voice-trim。
2. 按批注改FICCVoice.md，每改一行就同步四份摘录里的同一行。
3. 挪出去的说理写进FICCVoice-rationale.md V15节，例子写进examples-and-rewrites.md对应块。
4. 跑六项检查：xref_check -q、xref_check --selftest、voice_check --selftest、voice_check --selftest --clarity、budget_check（root改为仓库根的副本）、cjk_space --check本报告。
5. 降封顶，CHANGELOG加Unreleased。
6. PR描述贴“原号→去向”表和各文件改前改后字节数。

## 裁定（2026-11-04）

1. D1取(b)压缩版。补一条理由：budget.json里2026-11-03 r1那条记录的起因，正是写手拿到只有指针的摘录就跳过接缝检查（lesson L2），(a)纯指针会把这个问题重新打开。压缩后七项的新文本照抄进polish和coldread两份摘录。
2. D2取(a)，合成一行留在V22里，不改connectives.md。“但……只有”来自用户2026-10-14的改句“但是这个回答我们只有中偏低的把握”，那里的“只有”是“只有中偏低的把握”的只有，不是连接词“只有……才”，不宜写进连接词表当固定搭配。
3. D3、D4都可以动。L176–L177是用户2026-10-14原话（“读者的眼光会第一眼落到主语上”）的直接依据，照你的方案不动。L189–L191是T0根据那两处亲改提炼的，亲改原文在examples-and-rewrites.md的Revision example 4里不动。条件一个：别只在第8节放一个泛指针，V22正文里要留一个具体指针，把L178改成“There are two ways to show it (the user's two edits of 2026-10-14: references/examples-and-rewrites.md, Revision example 4):”，让人打开V22一跳就能找到那两处亲改。省的字节比你估的少几十，接受。
4. D6做。补两处你表里没列的：L31那行“See V29–V30”也在patch摘录L14和draft摘录L31里（都在V04块内），要一起改，不只是polish。V30正文压成两行时，“The following are argument steps”下面四种情形（定义是本段核心、下句要靠它、口径定结论、本段要解释为什么成立）要在一行里都点到，不能只剩premises一个词。xref_check.py第229行元组删'V30'，可以。
5. D7做。你查不到日期是因为公开版dev-notes.md只剩标题。本机记录：2026-10-11用户裁定“统一，术语公司名之类的都用英文”，同日补“承购方、兜底、残值担保用中文，中国机构不改英文，人名改英文”。当时的家是Voice第四节，2026-10-15名字表改四栏后，这条语言规则落在O33表后那两行，所以家在O33没错。请在references/FICCVoice-rationale.md加一节“## V33”，写一行“Ruling 2026-10-11 (user): 统一，术语公司名之类的都用英文; home: FICCOutline.md O33, the language rule after the name table.”，让公开版也带上出处。压缩句里“standard terms the table does not list”这一句保留。
6. D8：删L110（导言和V39 L435各有一份）。L109不删、改成一行指针“Standard terms and official names stay whole (V32).”，它是V16“拆名词”的例外，位置要留。本机核过，这两行来自英文化之前的中文版，没有带日期的用户裁定。
7. D9不做，确认。
8. 封顶措辞可以。reason写“voice-trim per docs/FICCVoice-trim-audit.md, user approval 2026-11-04”，改动的每个文件（FICCVoice.md、三份摘录、clarity-acceptance.md）都降到改后尺寸，root仍写~/.claude。FICCVoice-rationale.md、examples-and-rewrites.md、connectives.md不在封顶表里，往那里挪东西不受限。

其他：分支不改名，PR从claude/gifted-johnson-r902bf开到main；审计报告随PR一起走；不改VERSION，只加CHANGELOG的Unreleased；第5节不拆。
