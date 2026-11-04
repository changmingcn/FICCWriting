# Map template

ficc-mapper fills `R/脉络图.md` per this file in map mode (the packet's path prevails). The eleven elements each take one section, in the order below; copy the table headers as they are; where there is no content, write “缺：原因” and do not delete the section. The whole map stays under about 25KB; if it is over, first merge rows of the same kind, and leave details in the ledger (`ledger.md`) and the digests, pointing to them with anchors.

General requirements: every row carries an anchor pointing to a digest's fact row or a ledger row (`D-<编号> F<n>`, `R<nn>`; where needed `原件路径:L<行>`); a question-tree row not yet explored points to the user's words or `R/brief.md` instead (section 1); open those lines of the original only at a conflict or a doubtful point. Only lay out the material and mark conflicts; do not rule: ruling is T0's thesis. Do not write article sentences; use phrases in the tables. Speakers at the strength of the original: analysts, management, media retelling, filings, our own calculation (我们自算), each marked clearly; mark our inferences “我们推断” and do not write them as sources.

## 1 问题树

The root is the decision question (the trunk question, 主干问题) and the provisional answer; under it hangs the spine of questions and leads (consistent with `R/questions.md`), divided into main line, branch lines and layers. Copy each row's task role (任务角色) from the packet's role list (`R/brief.md`, and `R/questions.md` for rows added later); never infer it; a row with no role in the list gets “缺：角色未定” and a flag for T0. Never derive the role from the 主线／支线 column (role ≠ position: FICCHand 3.1 ⑥).

| 编号 | 问题／线索 | 任务角色（主干／明确必答／探索线索） | 主线／支线 | 上级 | 对主干的作用／是否关键依赖 | 什么发现会翻转结论 | 状态与继续／暂停理由 | 当前发现（可未定）与证据锚点 | 成文去向（论证节点／必答位置／背景／仅工作记录） | 成文排序依据（仅拟纳入项；为什么排在这里，用相邻两块的内容说；提纲顺序行照这一列写） |
|---|---|---|---|---|---|---|---|---|---|---|

Columns:
- 状态 (status) words: 未开始、探索中、已有发现、已答、待核实、受阻、暂缓、关闭 (not started, exploring, has findings, answered, to be verified, blocked, paused, closed); after the word, the reason to continue, pause or close. Write 已答 only when the question is answered; a finding short of an answer is 已有发现. For a lead: its test settled its use = 已答; stopped for low contribution = 关闭; stopped for now with a reason to resume = 暂缓. Mapping to `R/questions.md`: 未开始 = not started, 探索中 = in progress, 已答 = answered, 待核实 = to be confirmed, 受阻 = blocked; 已有发现, 暂缓 and 关闭 are kept here only.
- 对主干的作用 (use for the trunk): which part of the trunk the row is expected to explain or test; write 关键依赖 (critical dependency) and name the judgment when the trunk answer or an explicit must-answer depends on the row's finding and the finding does not yet suffice for that use.
- 当前发现 (current finding): an evidence finding carries its anchor; an unexplored row points to the user's words or `R/brief.md` (“见brief”), never to invented evidence.
- 成文去向 (destination in the text) and 成文排序依据 are proposals for T0: 必答位置 = an explicit must-answer's own node or appendix (`report-skeleton.md`); fill 成文排序依据 only for rows bound for the text; a row bound for 仅工作记录 writes “不入稿”. Research order never sets the article's order.

Revise the spine once evidence comes in: record under the table which question changed and why (example: Q4 changed from “净买还是净卖” to “谁在卖、卖什么”). Record a lead rewritten, merged, paused or closed, or a new lead, with its reason, as a proposal for T0; never rewrite the root's trunk question.

## 2 时间线与转折

Cut the window into several segments with fixed start and end dates (to the day), each with its drivers and evidence.

| 段 | 起（日期） | 止（日期） | 这一段发生了什么 | 驱动 | 证据锚点 | 转折点与依据 |
|---|---|---|---|---|---|---|

Check: replace “今年” and “上月” with a specific year, month and day, checking each against the original; check the order of events against the original; check whether the facts hold over the period the judgment speaks of (a rate-cut window must not be written as “利率上升”).

## 3 机制链

Where the money comes from, where it goes, whose balance sheet it passes through; one row per link.

| 环 | 从（谁的表、哪一项） | 到 | 渠道与摩擦（过不过得去、阀门在哪） | 边际定价者 | 状态（坐实／被反驳／反向／未检验） | 证据锚点 |
|---|---|---|---|---|---|---|

Check: a total-to-total inference first passes the distribution and transmission check; for a column of a table such as Z.1, first establish who the holders are (example: the “家庭” column is in fact the cash leg of the basis trade).

## 4 持有人与参与方

| 参与方 | 持有什么（存量） | 在买／在退／在接（流量，期间） | 约束（被迫还是自愿） | 计数单位（人、账户、机构） | 证据锚点 |
|---|---|---|---|---|---|

Check: tell apart the party, the holder, the custodian and the channel; whether accounts or people are counted; what is mixed into a balance (example: margin balances include strategy margin).

## 5 影响矩阵

| 条件（触发什么） | 渠道 | 受影响者 | 信号（序列id） | 时间窗 | 证据强度 | 锚点 |
|---|---|---|---|---|---|---|

Write only conditions and implications; write no predictions and no trading advice.

## 6 易混淆对照

| 编号 | 容易混的两样 | 区别（口径、主体、时点、单位） | 不能怎样用（不相接、不加总、不并排） | 提纲上定的名字 | 首次定义（指标名、口径、谁算的） | 先定义的节点（ficc-outliner搭树时补） |
|---|---|---|---|---|---|---|

Check item by item: two things with one name; each house's own measurement basis (do not merge them into one word); stock and flow; valuation effects and fund flows; transaction basis and valuation-adjustment basis; coverage (all members or retail, all long-term securities or Treasuries, private included or foreign official); absolute and relative, and who is doing what when the indicator rises; current state and historical pattern; trend words (低点, 一路, 见顶, 创新高) checked point by point against the whole series; units and denominators ($bn→亿: multiply by 10, do not convert by hand, record the original unit as is); statistical revisions and vintages (a conclusion holds only for its vintage). Set names per the original; do not coin them. After the table, list “不许用的说法” and how institution names are written (rules in FICCVoice 5.2). The name table comes from this table: ficc-outliner fills in its first version from it when building the tree (the report skeleton's header, FICCHand 3.6), and also maintains it after handoff; the name table has four columns (名字｜指什么与口径｜本篇写法｜不许用的叫法) and takes only coined nouns or nouns with several names, not standard terms (FICCOutline 4.2, user 2026-10-15).

## 7 分歧表

| 编号 | 议题 | 谁（机构、说话人类别） | 哪天（正文日期到日） | 怎么说（照原强度） | 依据（模型、样本、数据） | 我们的读法（建议，待T0裁） | 判别读数 |
|---|---|---|---|---|---|---|---|

Write models side by side and institutions side by side, and report each house's figures together; in outline claims, report each model's result separately, name the model and explain the difference, without merging them into one degree word (example: ACM about nine tenths, Kim–Wright about four tenths, BofA says almost all; about four tenths cannot carry “多数”, so report all three figures); to adopt one of the explanations, you must give the reason (written into “我们的读法”, pending T0's ruling), and keep the others as contrast; before combining them into a range, check that indicator, window and measurement basis are comparable; when the same institution says different things at different times, record a version chain (date plus original words) and do not treat it as a misquote; a reprint does not count as a second house.

## 8 证据强度

For each candidate judgment (from the 当前发现 column of the question tree):

| 判断 | 来源数（同源合并后，列名） | 最好的tier | 确认／推断／我们自算 | 说话人类别 | 单一来源或单一模型（写明是谁的） | 时间窗是否对上 | 范畴（情绪、活跃度、资金流…）是否一致 | 程度词有无出处（创新高、仍、几乎、主要） |
|---|---|---|---|---|---|---|---|---|

## 9 缺口与待核实

| 编号 | 缺什么 | 写法（“材料没说X和Y是什么关系”，不写成否定） | 为什么缺（查实的原因） | 怎样补、何时能补（数据发布日） | 影响哪条判断 |
|---|---|---|---|---|---|

List a gap here only when it affects a candidate judgment on the trunk, an explicit must-answer or a critical dependency, named in 影响哪条判断; a paused or closed lead's own unanswered remainder stays in section 1 with its reason and is not copied here.

## 10 观察清单与判别读数

| 编号 | 数据或事件 | 下次发布日 | 阈值（与原数据同一口径） | 看到什么算哪种判读、改判什么 | 能否真检验本文判断（能／只作背景） | 序列id |
|---|---|---|---|---|---|---|

Discriminating reading: when two readings point to the same observable, state the threshold and the cost of fetching the data. When the same condition appears again elsewhere, word it identically, character for character.

## 11 改动底稿（更新类题目）

| 旧版原话（照引，带行号） | 新证据锚点 | 补强／限定／推翻／新增 | 改结论还是改程度 | 冲突 |
|---|---|---|---|---|

Order the rows by the old version's sentences; what the old version did not cover goes under “新槽位”.
