# Glossary: FICC rule files, Chinese to English

Shared by the English rule files (FICCVoice.md, FICCStructure.md, FICCOutline.md, and since 2026-10-17 FICCCompose.md). Use one English term per Chinese term across all of them. First translator writes; later translators append under their own heading and do not change existing rows. Mark a disputed row with “交 T0” in the note column.

## 1 Conventions

- Section numbers stay as anchors, in numeric levels: “## 1 English title”, “### 1.1 English title”, “#### 1.1.1 …”. The rationale files (-rationale) and examples-and-rewrites follow the section numbers of the rule files, gaps allowed. Rule IDs V01–V40, S01–S96, O01–O90 are not section numbers and stay unchanged.
- Chinese kept in the English text: words, punctuation, and fixed phrases that the writer produces or must avoid in the Chinese article (connectives, quoted phrases, name-table column names, user-fixed expressions, script arguments). Write the Chinese first, then one English gloss in parentheses, e.g. “既然” (since).
- File names and pointers: point to a section with the file name, one space, and the section number, e.g. references/connectives.md, FICCStructure.md 3.4 (without .md also works: FICCStructure 3.4). In Chinese context put no space between Han characters and digits (“第35节”); in English context write “section 35”.
- Spacing: in the English files, put a space between English and kept Chinese as English usage requires. The no-space rule (cjk_space.py) governs Chinese body text only.

### 1.1 Modal words

| 中文 | English |
|---|---|
| 不／不得／不能 | Do not / must not |
| 须／必须 | must |
| 允许／可 | may |
| 只 | only |
| 优先 | prefer |
| 尽量 | as far as possible / as few as possible (user wording) |
| 按／照 | per / as in |
| 查： | Check: |
| 见 | See |
| 交回 | hand back |
| 无须 | need not |

## 2 Core terms (packet list, TR-common 2026-10-16)

| 中文 | English | Note |
|---|---|---|
| 节点 | node | |
| 主旨 | claim | a node's or paragraph's main claim |
| 任务 | task | what a node does for its parent |
| 展开 | unfolding / unfold | |
| 关系行 | relation line | |
| 顺序行 | order line | `顺序：`, why the node sits here, through the two adjacent blocks' content; the outline agent writes it (FICCOutline.md O18, O19); split from the relation line 2026-10-17 |
| 标注行 | annotation line | |
| 关系单 | relation sheet | relations only: endpoints, type, grounds, limits or open items (FICCStructure.md S74). Since 2026-10-17 it gives no opening words, writing instructions, or writing advice. Facts and verbatim sentences are cited by index number or position, not copied |
| 安放记录 | placement record | |
| 名字表 | name table | |
| 主干组 | trunk group | |
| 链 | chain | |
| 卫星 | satellite | |
| 接缝 | seam | |
| 承接 | carry-over / carry over | also the parallel-item add-on relation in connectives.md |
| 回指 | back-reference / refer back | |
| 冷读 | cold read; 冷读者 cold reader | |
| 硬伤 | hard error | |
| “！”项 | the “！” items | |
| 写作单元 | writing unit | |
| 导语 | lead | |
| 收尾 | close | |
| 段群 | paragraph group | |

## 3 Added by TR-Voice (FICCVoice.md and its rationale file)

### 3.1 Roles, artifacts, drafts

| 中文 | English | Note |
|---|---|---|
| 提纲 | outline | |
| 提纲代理 | outline agent | |
| 写手 | writer | |
| 父节点／子节点 | parent node / child node | |
| 同级 | sibling | |
| 子项 | sub-item | |
| 相邻节点 | adjacent node | |
| 块／本块 | block / this block | |
| 层 | layer | |
| 安放 | placement | |
| 归属（结构） | attachment | which node an item belongs to |
| 观点归属 | attribution | who holds a view |
| 材料／指定材料 | material / assigned material | |
| 原件 | original document | |
| 正文 | body text | |
| 成稿 | finished draft | |
| 新稿 | new draft | |
| 改稿 | revision | |
| 拼稿 | assembled draft | |
| 交稿 | submit | |
| 只改文风 | style-only edit | |
| 润色 | polishing | |
| 授权／权限 | authorization / permissions | |
| 工作标签 | working label | |
| 台账 | ledger | |

### 3.2 Judgment and argument

| 中文 | English | Note |
|---|---|---|
| 判断 | judgment | |
| 陈述 | statement | |
| 论点／分论点 | point / sub-point | 论点当主语 = make the point the subject |
| 观点／看法 | view | |
| 结论 | conclusion | |
| 理由 | reason | |
| 证据 | evidence | |
| 依据 | grounds / support | |
| 反证 | counter-evidence | |
| 限定 | qualifier | |
| 限制 | limit / limitation | |
| 前提 | premise | |
| 缺口 | gap | |
| 判断强度 | strength (of a judgment) | |
| 程度词 | degree word | |
| 出处／来源 | source | |
| 出处清单 | source list | |
| 合注 | combined citation | |
| 说话人 | speaker | |
| 双向核对 | two-way check | |
| 论证单元 | argument unit | |

### 3.3 Relations (aligned with references/connectives.md)

| 中文 | English | Note |
|---|---|---|
| 关系 | relation | |
| 并列 | parallel | |
| 并列组 | parallel group | |
| 传导链 | transmission chain | |
| 解说 | explication | |
| 先后（承接关系） | sequence | |
| 递进 | progression | |
| 转折 | turn | adversative |
| 让步 | concession | |
| 因果 | cause and effect | |
| 推断／推论 | inference | |
| 目的 | purpose | |
| 假设 | supposition / hypothetical | |
| 选择 | alternative | |
| 条件 | condition | |
| 对比 | contrast | |
| 比较 | comparison | |
| 对照 | compare side by side / directly comparable | |
| 举例／例示 | exemplification / illustrate | |
| 反复、强调、深化 | repetition, emphasis, deepening | add-on relations between parallel items |
| 连接词 | connective | |
| 连词 | conjunction | |
| 关系标记 | relation marker | |
| 后位关系标记 | latter-clause relation marker | |
| 前位成对词 | former-clause paired word | e.g. 虽然 in 虽然……但是 |
| 衔接 | cohesion | |
| 已知—新知 | given–new | |
| 句式呼应 | parallel syntax | |
| 先行项 | antecedent | |
| 统摄／统领 | govern | 段首统摄 = an opening that governs the paragraph |

### 3.4 Paragraphs and sentences

| 中文 | English | Note |
|---|---|---|
| 段首 | paragraph opening | |
| 首句 | first sentence | |
| 节点开头句 | node's opening sentence | |
| 段长上限 | paragraph length cap | |
| 句意 | sentence meaning | |
| 主干（句子） | sentence core | not 主干组 |
| 分句 | clause | |
| 复句 | complex sentence | |
| 主语／主体 | subject | 主体 also “party” when responsibility is meant |
| 施事／受事 | agent / patient | |
| 主动／被动 | active / passive | |
| 定语／状语 | attributive / adverbial | |
| 名词组 | noun phrase | |
| 中心对象 | head | |
| 修饰语 | modifier | |
| 指代 | reference / referring expression | |
| 省略 | omission | |
| 错承 | wrong carry-over | |
| 主谓搭配 | subject–predicate fit | |
| 漏字 | missing characters | |

### 3.5 Punctuation (Chinese symbol kept)

| 中文 | English |
|---|---|
| 冒号 | colon (：) |
| 分号 | semicolon (；) |
| 逗号 | comma (，) |
| 顿号 | enumeration comma (、) |
| 句号 | full stop (。) |
| 括号／括注 | parentheses / parenthetical |

### 3.6 Terms, numbers, notes, figures

| 中文 | English | Note |
|---|---|---|
| 术语／通行术语 | term / standard term | |
| 正式名称 | official name | |
| 简称 | short name | |
| 缩写 | abbreviation | |
| 别称 | alias | |
| 自造名字 | coined name | |
| 自造短标签 | coined short label | |
| 代号 | code name | |
| 市场叫法 | market name | |
| 注解／纯注解 | note / pure note | identifies a word or source, adds no premise |
| 释义 | gloss | |
| 定义 | definition | |
| 白话 | plain language | |
| 口径 | measurement basis | definition, scope, and method behind a figure |
| 指标 | indicator | |
| 数据序列 | data series | |
| 群体 | group | |
| 基期 | base period | |
| 时点 | point in time | |
| 时段 | period | |
| 样本 | sample | |
| 单位 | unit | |
| 水平与变化 | level and change | |
| 百分比与百分点 | percent and percentage point | |
| 余额与流量 | stock and flow | |
| 总量与增量 | total and increment | |
| 账面与市值 | book value and market value | |
| 图／图题／图注 | figure / figure title / figure note | |
| 比较基准 | comparison baseline | |

### 3.7 Register, persona, review

| 中文 | English | Note |
|---|---|---|
| 默认听众 | default audience | |
| 写作身份 | writing persona | |
| 亲历 | first-hand experience | |
| 比喻／类比 | metaphor / analogy | |
| 引子 | hook | |
| 兑现（引子） | pay off | |
| 排比 | parallelism | rhetorical |
| 重话 | strong words | |
| 书面化 | conversion to written register | |
| 公文 | officialese | |
| 讲义 | lecture notes | |
| 报告体 | report style | |
| 录音稿 | transcript | |
| 课堂口令 | classroom cues | |
| 戒AI腔 | avoid AI tone | |
| 路线图句 | roadmap sentence | |
| 空洞主旨 | hollow claim | |
| 模板腔 | template tone | |
| 术语堆 | term pileup | |
| 段末升华 | end-of-paragraph uplift | |
| 过渡语 | transition filler | |
| 理解障碍 | comprehension obstacle | |
| 理解负担 | comprehension load | |
| 回配／配对 | match back / pair | |
| 提示（脚本） | flag | |
| 硬线 | hard limit | |
| 误报 | false alarm | |
| 待核实 | to be verified | |

## 4 Added by TR-Outline (FICCOutline.md and its rationale file)

### 4.1 Tree, nodes, positions

| 中文 | English | Note |
|---|---|---|
| 主干（树） | trunk | tree sense; not 主干组 (trunk group), not 主干（句子） (sentence core) |
| 支线 | branch line | |
| 分支／枝 | branch | |
| 叶子 | leaf | |
| 根 | root | |
| 根主旨 | root claim | |
| 子树／核心子树／卫星子树 | subtree / core subtree / satellite subtree | |
| 中心／中心判断 | center / central judgment | |
| 暂定中心 | provisional center | |
| 主线 | main line | |
| 主干分论点 | trunk sub-point | |
| 非主干节点 | non-trunk node | |
| 尺度／八种尺度 | scale / the eight scales | |
| 全篇 | whole piece | |
| 部分 | part | |
| 节／小节 | section / subsection | |
| 句群 | sentence group | |
| 单句 | simple sentence | |
| 层数 | number of layers | |
| 四个位置 | the four positions | |
| 四件事 | the four things | |
| 定调句／定调 | tone-setting sentence / tone-setting | |
| 总结收尾 | summary close | |
| 总起 | overall opening | |
| 主旨行 | claim line | |
| 展开一行 | unfolding line | |
| 〔标题〕行 | 〔标题〕 (heading) line | tag kept in Chinese |
| 头（提纲的头） | header | |
| 承上句 | linking-back sentence | |
| 兄弟节点 | sibling node | same as 同级 |
| 节首句 | section opening sentence | |
| 主旨段 | claim paragraph | |
| 承接段 | carry-over paragraph | |
| 引领句 | leading sentence | |
| 局部分点 | local bullet points | |
| 散文节 | prose section | |
| 知识点 | knowledge point | |

### 4.2 Invariants, placement, maintenance

| 中文 | English | Note |
|---|---|---|
| 七条不变式 | the seven invariants | 概括 summarizing, 完整 completeness, 篇幅 length, 同组 grouping, 归属 attachment, 挂法 hanging, 重提 re-mention |
| 挂／挂法 | hang / hanging (hanging rules) | how a non-trunk item attaches; 交 T0 |
| 本家 | home rule | the place where a rule is written in full; 交 T0 |
| 归纳组／演绎组 | inductive group / deductive group | |
| 孤儿 | orphan | |
| 分量 | weight | |
| 立骨 | serve as the backbone | |
| 立靶子 | set up a target | |
| 先立后破 | build-then-refute | |
| 判词 | verdict | |
| 反方 | counter-view | 反方的看法 = counter-views |
| 反向证据 | contrary evidence | 反证 stays counter-evidence |
| 逆向支线 | reverse branch line | |
| 取舍（材料） | selection; 取舍权 authority to select | |
| 取舍（反方、看法） | weigh / weighing | |
| 判据 | criteria | |
| 勘误 | corrections | |
| 伏笔 | foreshadowing | |
| 呼应 | echo | |
| 跨枝／跨枝标注 | cross-branch / cross-branch annotation | |
| 标注／标法 | annotation / marks | 批注 also rendered annotations |
| 关系代理 | relation agent (ficc-structurer) | |
| 工作底稿 | working draft | |
| 初拟 | first draft (verb: make the first draft of) | |
| 局部提纲 | partial outline | |
| 临时提纲 | temporary outline | |
| 临时编号／正式编号 | temporary number / permanent number | |
| 编号对照 | number map | |
| 安放结论／材料价值／结构理由 | placement conclusion / material value / structural reason | parts of the placement record |
| 落盘 | save | |
| 贴出 | post (in the conversation) | |
| 待问／开放问题 | open question | |
| 待补充 | to be supplied | |
| 暂存／舍弃 | set aside / discard | |
| 备查数字 | reference figures | |
| 范本 | model text | |
| 名单 | list of names | |

### 4.3 Mechanism and evidence

| 中文 | English | Note |
|---|---|---|
| 机制 | mechanism | |
| 通道 | channel | |
| 阻尼 | damping | |
| 最脆弱的环节 | weakest link | |
| 沿着钱追／沿着钱走的比喻 | follow the money / follow-the-money metaphor | |
| 硬证据／带保留的证据／存疑的读数 | hard evidence / qualified evidence / doubtful readings | |
| 融资链 | financing chain | |
| 记账／分开记账 | accounts / keep separate accounts | |

### 4.4 Genres, rewriting, checks

| 中文 | English | Note |
|---|---|---|
| 体裁 | genre | |
| 文体：论述性、叙事性、说明性、方法性、混合 | text type: argumentative, narrative, expository, methodological, mixed | |
| 整体结构 | overall structure | |
| 短评 | short commentary | |
| 月报短文 | monthly short piece | |
| 长文 | long article | |
| 清单月 | list month | a month written as several adjacent stories; 交 T0 |
| 问答 | Q&A | |
| 教程 | tutorial | |
| 金融案例 | financial case | |
| 案例讲稿 | case lecture script | |
| 亲历引子 | first-hand hook | |
| 日记或系列 | diary or series | |
| 设问 | posed question | a question the writer poses and answers |
| 悲观论者 | pessimists | |
| 上期 | previous issue | |
| 序数／体例 | ordinal / established style (convention) | |
| 扩写／压缩 | expanding / compressing | |
| 改写权限 | rewrite permissions | |
| 保真改写 | faithful rewrite | |
| 重组 | reorganization | |
| 重写结构 | restructuring | |
| 重搭 | rebuild | |
| 整理录音稿 | transcript cleanup | |
| 作者亲写 | author-written | tag 〔作者亲写·逐字〕 kept in Chinese |
| 作者原句 | author's original sentence | relation-sheet column, kept in Chinese |
| 信息量测试 | information test | |
| 抽主旨 | claim extraction / extract the claims | |
| 父子检验／子树检验／同组检验 | parent–child test / subtree test / grouping test | |
| 八种毛病 | the eight faults | 中心漂移 center drift; 层级混杂 mixed levels; 功能重复 duplicated function; 逻辑跳跃 logical leap; 依据不足 insufficient support; 缺少必要环节 missing necessary links; 顺序不顺 awkward order; 篇幅失衡 length imbalance |

### 4.5 File parts and provenance

| 中文 | English | Note |
|---|---|---|
| 导言 | Introduction | file section |
| 结语 | Conclusion | file section; pointer “references/FICCOutline-rationale.md, Conclusion” |
| 附／附录 | Appendix / appendix | |
| 说理 | rationale | |
| 沿革 | history | |
| 来历 | origin / provenance | |
| 贴文 | posted text | |
| 原话／近原话／原话要点 | original words / near-verbatim / gist of the original words | user quotes kept in Chinese with gloss |
| 开发文档 | development document | references/dev-notes.md |

## 5 Added by TR-Structure (FICCStructure.md and its rationale file)

### 5.1 Modal words used

| 中文 | English | Note |
|---|---|---|
| 尽可能 | as far as possible | same as FICCOutline (O-rule on ten nodes); not “prefer” |
| 要（规则里） | plain imperative or “need” | “must” only for 须／必须 |
| 不要求 | is not required | |
| 应该考虑 | should consider | user wording, S25 |

### 5.2 Relation library (1.1, twenty-one types)

| 中文 | English | Note |
|---|---|---|
| 关系库 | relation library | |
| 关系类别 | relation type | |
| 分类与分工 | classification and division of labor | |
| 互补 | complementarity | |
| 总述与展开 | overview and unfolding | |
| 归纳与综合 | induction and synthesis | |
| 解释与澄清 | explanation and clarification | |
| 主张与支持 | assertion and support | 主张 = assertion, to keep 主旨 = claim |
| 依据与推论 | grounds and inference | |
| 因果与机制 | cause and mechanism | |
| 条件与限制 | conditions and limits | |
| 递进与深化 | progression and deepening | |
| 前提与依赖 | premise and dependency | |
| 比较与对照 | comparison and contrast | |
| 类比与迁移 | analogy and transfer | |
| 质疑与回应 | objection and response | |
| 问题与解决 | problem and solution | |
| 目标与手段 | goals and means | |
| 选择与取舍 | choice and trade-off | |
| 时间与空间 | time and space | |
| 铺垫与兑现 | setup and payoff | |
| 呼应与变奏 | echo and variation | |
| 节奏与情绪调节 | pacing and mood regulation | |
| 对照（单用） | contrast | also 对比 in FICCCompose.md C14; 交 T0 |

### 5.3 Complex-sentence relations (row names of connectives.md section “现行连接词表”, current connective table)

| 中文 | English | Note |
|---|---|---|
| 复句关系 | complex-sentence relation | |
| 判别问题 | diagnostic question | |
| 并列·附加关系 | parallel · add-on relation | S18 table keeps the Chinese row name with the gloss |
| 附加关系：承接、反复、强调、深化 | add-on relation: carry-over, repetition, emphasis, deepening | |
| 并列·解说 | parallel · explication | |
| 承接关系（先后） | sequence | 承接 as position stays carry-over |
| 转折·让步 | turn · concession | |
| 因果·推断／因果·目的 | cause and effect · inference / cause and effect · purpose | |
| 轻转／重转 | light turn / strong turn | |
| 实让／虚让／总让 | factual / hypothetical / total concession | |
| 未定选择／已定选择 | open / settled alternative | |
| 充分／必要／无条件 | sufficient / necessary / unconditional | |
| 前件／后件 | antecedent / consequent | of a connective or conditional; 先行项 is the antecedent of a reference |
| 前位／后位（标记） | former-clause / latter-clause (marker) | |
| 关联词 | connective | same as 连接词 |
| 关系词 | relation word | |
| 顺承 | straight continuation | |
| 演绎／归纳 | deduction / induction | |

### 5.4 Arrangement, seams, positions

| 中文 | English | Note |
|---|---|---|
| 排法 | arrangement | |
| 展开关系 | unfolding relation | |
| 逻辑关系 | logical relation | |
| 卫星检验 | satellite test | |
| 盖住检验 | cover test | |
| 父主旨 | parent claim | |
| 主旨栏 | claim field | |
| 划分依据 | basis of division | |
| 颗粒 | granularity | |
| 对举 | paired contrast | |
| 列举 | enumeration | |
| 分阶段／不同方面 | by stage / different aspects | |
| 话题框架 | topic frame | |
| 时间词 | time word | |
| 毛净口径 | gross and net bases | |
| 公司篮子 | company basket | |
| 整体／整体检验 | whole set / whole-set check | |
| 改挂 | re-hang | follows 挂 = hang |
| 重提 | re-mention | as in TR-Outline's invariant note |
| 承接句 | carry-over sentence | |
| 段首句 | paragraph-opening sentence | |
| 指路句 | signpost sentence | |
| 路线句 | route sentence | |
| 回扣 | tie back | |
| 表态 | state a stance | |
| 读法 | reading | |
| 体裁阶段 | genre stage | |
| 判断式标题 | judgment heading | |
| 反方看法 | counter-views | |
| 结语（文章体裁阶段） | conclusion section | file heading stays “Conclusion” |
| 材料句 | material sentence | |
| 主题（段首） | topic | |
| 亲历案例框 | first-hand case box | |
| 认错复盘 | post-mortem of one's own errors | |
| 遍历 | traversal | |
| 隐患 | hazard | cold-read hazard |
| 结果单 | result sheet | |
| 写全处 | full-statement place | |
| 待办 | to-do item | |
| 安放规范 | placement norms | |

## 6 Added by wave 4 (FICCCompose.md, 2026-10-17)

| 中文 | English | Note |
|---|---|---|
| 段落组织（Compose） | paragraph organization (FICCCompose.md) | inside a settled node: how the text opens, carries over, unfolds, moves between layers, pays off previews, and closes. The file is FICCCompose.md |
| 段落代理 | composer (ficc-composer) | writes the paragraph draft per FICCCompose.md. The writer (ficc-writer) then works on sentences per FICCVoice.md |
| 段落草稿 | paragraph draft | the composer's output. No separate paragraph plan |
| C 号 | C number (C01–C23) | rule numbers of FICCCompose.md. Old V, O and S numbers that moved: references/migration-2026-10-17.md |

## 7 Added by the English pass on SKILL.md files and agent cards (2026-10-17)

| 中文 | English | Note |
|---|---|---|
| 资料核对席 | source-check seat | the seat that checks facts against sources per shared-protocols/source-check.md; its check is the tie-out (对账) named there |
| 反方席 | counter-view seat | built from 反方 = counter-view |
| 资料索引 | materials index | FICCHand deliverable `<文稿名>-资料索引.md`; format file references/materials-manifest.md in ficc-hand |
| 表达修订稿 | revised node | the writer's output in polish mode, as in agents/ficc-writer.md |
| 观点提纲／观点树 | view outline / view tree | FICCHand deliverable `<文稿名>-提纲.md` |
| 立项 | framing | FICCHand step 0; research-agent GATE 1 (FRAME). Not 铺垫 (setup) |
| 扫改 | sweep edit; verb sweep-edit | scripted batch fix of rule hits (sweep-edit mode in dispatch-notes) |

### 7.1 Added by the English pass on references and FICCHand (2026-10-17, fix round)

One row per concept with no earlier English name, from the B1–B4 change notes and the T0 rulings of the fix round.

| 中文 | English | Note |
|---|---|---|
| 问题号 | question number (I-nn) | the ledger id of a conflict or open question, kept through the relation sheet and the placement record; defined in ~/.claude/skills/research-agent/references/analysis.md |
| 起草席 | drafting seat | composer and writer (SKILL.md, kept rulings) |
| 短稿合并模式 | short-piece merged mode | 短稿 = short piece (body text ≤600 Chinese characters); one writer draft seat does relay steps ④⑤ (dispatch-notes) |
| 只改措辞 | wording-only edit | writer patch; not 只改文风 (style-only edit) |
| 派单包 | packet | |
| 退回说明 | return note | location, conflict, decision needed (dispatch-notes) |
| 隐患清单 | hazard list | voice_check output heading, kept as the token `隐患清单` |
| 统计对象 | what is counted | in the fact tuple: who, what they did, what is counted, period, unit, qualifier |
| 改动流水 | change log | table name, kept as 《改动流水》 |
| 体例整理 | format tidy | not 体例 = established style (convention) |
| 脉络图 | map | FICCHand step 3, `R/脉络图.md` |
| 问题树 | question tree | map element; headings in map-template stay Chinese |
| 时间线与转折 | timeline and turning points | map element |
| 机制链 | mechanism chain | map element |
| 持有人与参与方 | holders and participants | map element |
| 影响矩阵 | impact matrix | map element |
| 易混淆对照 | confusables | map element |
| 分歧表 | disagreement table | map element |
| 证据强度 | evidence strength | map element |
| 缺口与待核实 | gaps and items to be verified | map element |
| 观察清单与判别读数 | watch list and discriminating readings | map element |
| 改动底稿 | change worksheet | map element; not 工作底稿 (working draft) |
| 立论 | thesis; form the thesis | `R/立论.md` |
| 摘要／摘要席 | digest / digest seat | |
| 语料盘点／盘点表 | corpus inventory / inventory | |
| 分诊 | triage | |
| 交接单 | handoff note | as agents/ficc-mapper.md |
| 查提纲 | outline check | |
| 修改（模式） | fix mode | ficc-mapper card mode |
| 研究状态目录 | research-state directory | `R/` |
| 承重数／承重判断 | load-bearing figure / load-bearing judgment | |
| 主判断 | main judgment | FICCHand; cf. 中心判断 = central judgment; 交 T0 if the same concept |
| 把握度 | confidence | |
| 限制它的那一环 | the link that limits it (limiting link) | |
| 决策问题 | decision question | |
| 时间窗 | time window | |
| 数据截止日 | data cutoff date | |
| 判别读数 | discriminating reading | |
| 改判条件 | conditions that would change the judgment | |
| 登记表／登记行 | register / register row | SUPERSEDED.md |
| 资金流第一性 | fund flow first | |
| 操作建议 | trading advice | |
| 出口 | exit | FICCHand exits |
| 先破后立 | refute then build | mirror of 先立后破 (build-then-refute) |
| 落点数 | landing figures | ambiguous; 交 T0 |
| 主口径／packet口径 | main basis / packet basis | cost weighting; not 口径 = measurement basis |
| 来源表 | source table | not 出处清单 (source list) |
| 档 | tier | model tier |
| 席 | seat | as in 反方席, 资料核对席 |
| 间隔反复 | spaced repetition | connectives.md |
| 一系（经典体系） | line | “Huang Borong and Liao Xudong, 《现代汉语》 line” |
| 混合写法／含混写法／生硬写法／展开写法 | mixed / unclear / stiff / unfolded version | example labels |
| 理解单元 | unit of understanding | clarity-rewrites.md |
| 判别例 | diagnostic example | written-register.md; cf. 判别问题 = diagnostic question |
| 纯提示语 | pure cue phrase | 课堂提示 keeps the 课堂口令 name, classroom cue |
| 原稿保护流程 | original-text protection procedure | written-register.md introduction |
| 货币银行学篇 | money and banking chapter | of 《熊猫笔记》 |
| 流动性缓冲 | liquidity buffer | lecture-terms.md note |
| 后盾表 | backstop table | lecture-terms.md note |
| 原始存款 | original deposits | lecture-terms.md note |
| 改例 | revision example | tag 〔改例〕 kept; labels 改例一… → Revision example 1… |
| 亲改 | user's own edit | tag 〔亲改〕 kept |
| 例句 | example sentence | |
| 示意改写 | illustrative rewrite | 没有发出 = not published |
| 定稿 | final version | the published version; not 成稿 (finished draft) |
| 看点 | What to note | label in examples-and-rewrites.md |
| 改法方向 | direction of the fix | |
| 树图 | tree diagram | |
| 反驳席 | refuter seat | |
| 研究席 | research seat | |
| 本文件 | this file | kept as the token glued before a numbered ref in examples-and-rewrites.md (xref_check.py) |
| 原（条号、节号） | formerly | as in “Cnn (formerly Vnn)” |
| 最早为 | originally | as in “(originally section N.N of FICCStructure)” |
| 改动对照表 | change comparison table | |
| 节点稿 | node draft | |
| 源泉（作者比喻） | wellspring | author's liquidity metaphor; not 出处 = source |
| 血包（作者比喻） | blood pack | author's metaphor |
