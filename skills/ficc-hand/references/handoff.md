# Handoff: FICCHand to ficc-voice

## 1 What is handed over

| File | What it is | Who maintains it |
|---|---|---|
| `<文稿名>-提纲.md` | view tree, FICCOutline format, unfolded to paragraph groups; order lines only; relation lines wait for ficc-voice's relation sheet | ficc-outliner (builds it at Hand step 5b, maintains it per FICCOutline after handoff) |
| `<文稿名>-资料索引.md` | index of main materials and data; its head is this handoff note | after handoff, append only and do not change old rows; mark a changed row “已改，见新行” |

Working files are not copied with the handoff; section 9 of the index gives their paths.

## 2 Handoff note (written in section 0 of the materials index)

This section is the only definition of the handoff note's fields.

1. `决策问题与根主旨` (decision question and root claim): one sentence; time window, data cutoff date; then the explicit must-answers (`明确必答项`), each with its delivery place (node id or appendix) and whether it is answered or undetermined.
2. `两份文件的路径` (paths of the two files).
3. `当前生效的用户裁定清单` (list of the user rulings currently in force): section number or node number + original text; overturned rulings are not listed. A ruling that changes the strength of a judgment is written as “全文凡……”, so that the writer searches the whole text, not just a list of line numbers.
4. `生效的登记行` (register rows in force): `SUPERSEDED.md` line number, keys, now.
5. `已在提纲上定好的项` (items already settled on the outline): the choice of measurement bases and indicators, data windows, the name table, the change worksheet; items not yet settled are listed as open questions; node positions follow the tree ficc-outliner built, and the index's “提示节点” are hints only. The format of the change section is fixed as two columns “旧版原话｜新说法”; the section opening states which items changed the conclusion and which changed only the degree.
6. `开放问题与待核实` (open questions and items to be verified): the items of section 8 of the index by their numbers (unresolved critical dependencies (关键依赖), unresolved explicit must-answers, gaps that bear on a retained judgment, each with the judgment or node it limits), the disagreements T0 has not ruled (FICCHand 3.6), the items of field 5 not yet settled and any scope decision still pending (FICCHand 3.1 ⑥), each with the node it affects; exploratory leads appear only as one pointer to the exploratory records (`R/脉络图.md` section 1), never one by one. These items stay with T0, who reopens them per FICCHand 3.8 “After handoff”; the writer writes each limited, suspended or undetermined judgment as the outline states it and owes answers only to the decision question and the explicit must-answers.
7. `top spark` (top spark): one line: the best anomaly or opportunity, the cost of probing it, what it would change (research-agent/SKILL.md (Before you send)).
8. `最可能错的一条判断和最便宜的检验` (the judgment most likely to be wrong and the cheapest test of it).
9. `验收记录` (acceptance record): the paths and conclusions of the three results (outline check, tieout, counter-view), one line each.
10. `出口` (exit): whether the task's acceptance goal is the research outline only or a finished draft (per the acceptance items of `work.py define`). Outline only: settle after verifying delivery; finished draft: record “研究阶段已完成” (research stage complete), do not settle, continue along the original task goal into ficc-voice, and settle after the finished draft is delivered.
11. `ficc-voice从哪一步接` (the step at which ficc-voice takes over): per section 3.
12. `各接手席的读单与不读清单` (read list and do-not-read list per taking-over seat): one list per seat (writing-stage T0 or ficc-conductor, structurer, composer and writer seats, an external route): read first, read next, readable only for a stated purpose; history files listed by name, each marked “不作现行依据” (not a current basis; may be read for comparison) or “禁读” (do not read); do-not-read reasons by category only (史, 旧稿, 已被取代, 他席范围), never figures or field names. State-card block 6 (2.1).

### 2.1 子项映射（W2）

Written as the stage-handoff state card (the seven blocks of dynamic-workflow references/artifact-schema.md), the note's fields land as below. Every sub-item has a place and none is dropped; a long one goes on the card as a `path:line` pointer. Field 8 goes to `claims.md` (block 4), never to block 2. Blocks 2 (lessons rows) and 7 (writer, time, sha256 of the two files) are generated, not taken from fields. Examples are illustrative.

| 字段 | 子项 | 七块卡的块 | 实例 |
|---|---|---|---|
| 1 | 决策问题 | 1 位置·全局 | 全局：四季度高等级信用债要不要加久期 |
| 1 | 根主旨 | 4 轨迹·已成判断 | 根主旨：利差下行空间有限，以持有为主（较可能） |
| 1 | 时间窗 | 5 约束·本单元裁定行 | 资料索引:L4 时间窗 2026-10-01 至 2026-12-31 |
| 1 | 数据截止日 | 5 约束·本单元裁定行 | 资料索引:L4 数据截止 2026-10-28 |
| 1 | 明确必答项 | 5 约束·验收项 | 必答 Q1 加不加久期；Q2 城投与产业债谁先 |
| 1 | 必答项交付位置 | 5 约束·验收项 | Q1 → 节点 3.2；Q2 → 附录 B |
| 1 | 必答项状态（已答／待定） | 4 轨迹（已答入已成判断，待定入未决分歧） | Q1 已答；Q2 待定，见字段 6 |
| 2 | 提纲路径 | 3 现行入口·现行 | 现行：四季度信用-提纲.md（sha256 a1b2c3d4） |
| 2 | 资料索引路径 | 3 现行入口·现行 | 现行：四季度信用-资料索引.md（sha256 e5f6a7b8） |
| 3 | 裁定（节号或节点号＋原文） | 5 约束·本单元裁定行 | 节点 2.1：“不写目标价” |
| 3 | 改判断强度的裁定（“全文凡……”） | 5 约束·本单元裁定行 | 全文凡“必然”改“较可能” |
| 3 | 已推翻的裁定 | 不上卡；其文件若在，入 6 读序与不读·不读 | 不读：旧裁定稿（已被取代） |
| 4 | `SUPERSEDED.md` 行号、键、现值 | 5 约束·登记行 | SUPERSEDED.md:14 · 某公告日期 · 现：以 10-27 版为准 |
| 5 | 口径与指标 | 5 约束·本单元裁定行 | 提纲:L12 利差＝AAA 中票 3 年减国开 3 年 |
| 5 | 数据窗 | 5 约束·本单元裁定行 | 提纲:L13 2023-01 至 2026-09，月度 |
| 5 | 名字表 | 5 约束·本单元裁定行 | 提纲:L20–L34 名字表 |
| 5 | 改动表 | 3 现行入口（现行，旧版入史） | 现行：提纲改动节；史：提纲-v1.md |
| 5 | 改动节格式与开头 | 5 约束·本单元裁定行 | 两列“旧版原话｜新说法”；开头分列改结论项与只改程度项 |
| 5 | 未定项 | 4 轨迹·未决分歧（随字段 6） | 数据窗起点未定，影响节点 2.3 |
| 5 | 节点位置以提纲的树为准 | 3 现行入口·现行 | 现行：提纲的树；索引“提示节点”只作提示 |
| 6 | 索引第 8 节各项（关键依赖、未答必答项、缺口，各带所限判断或节点） | 4 轨迹·未决分歧与改变条件 | 索引 8.2：某关键数据未发布，限节点 2.3 |
| 6 | T0 未裁的分歧（FICCHand 3.6） | 4 轨迹·未决分歧与改变条件 | 分歧 D2：利差季节性强弱，待 T0 裁 |
| 6 | 字段 5 未定项与待定的范围决定（FICCHand 3.1 ⑥） | 4 轨迹·未决分歧与改变条件 | 范围决定待用户：是否纳入城投，影响节点 4 |
| 6 | 探索线索的指针 | 6 读序与不读·可读 | 可读：R/脉络图.md 第 1 节（只为探索线索） |
| 6 | 归属与写手的义务 | 1 位置·下级 | 下级：上列各项归 T0；写手照提纲写受限与待定判断，只答决策问题与必答项 |
| 7 | top spark（异常或机会、探查成本、会改变什么） | 4 轨迹·未决分歧与改变条件 | spark：利差与基本面背离；查一张表；成立则降节点 2 的强度 |
| 8 | 最可能错的判断 | 4 轨迹（`claims.md`，不进第 2 块） | claims.md C-05：节点 2.1 的季节性判断 |
| 8 | 最便宜的检验 | 4 轨迹·改变条件（`claims.md`） | 检验：比对 2023–2025 同月利差 |
| 9 | 三份结果（提纲检查、核数、counter-view）的路径与结论 | 5 约束·验收项 | 提纲检查 R/outline-check.md 通过；核数 R/tieout.md 漏项 0；counter-view R/counter.md 已逐条裁 |
| 10 | 出口（只要提纲／要成稿） | 1 位置·下级 | 下级：成稿，交 ficc-voice |
| 10 | settle 时点与“研究阶段已完成” | 5 约束·验收项 | 已记“研究阶段已完成”；成稿交付后 settle |
| 11 | 接手步 | 1 位置·下级 | 下级：ficc-voice 接力表第 ③ 步 |
| 11 | 试验期的接手协议（第 3 节） | 1 位置·下级 | handoff_trial.py status 报甲臂：T0 停手，交用户恢复行 |
| 12 | 各接手席的读单 | 6 读序与不读·先读／再读／可读 | structurer 先读：提纲节点 2；可读：索引第 8 节（只为依赖） |
| 12 | 史文件 | 3 现行入口·史，6 读序与不读标“不作现行依据” | 史：提纲-v1.md（不作现行依据，可读只为比较） |
| 12 | 禁读 | 6 读序与不读·不读 | 不读：旧稿-v0.md（禁读；类别：旧稿） |

## 3 Where ficc-voice takes over

Take over at step 3 of the relay table in ficc-voice/SKILL.md (judge relations, issue the relation sheet). The outline has already been checked by ficc-outliner in check mode (FICCOutline 9); do not rebuild it. The finished draft passes through ④ paragraph organization (ficc-composer) and ⑤ sentences and wording (ficc-writer); for a short draft one ficc-writer seat does ④ and ⑤ in a row.

Trial (2026-10-25): while `handoff_trial.py status` (first-secretary `scripts/`) reports an active trial, the takeover follows the protocol it names: under arm 甲 T0 stops and hands the user the resume line, under arm 甲′ T0 dispatches `ficc-conductor`.

This skill changes no file of ficc-voice.

## 4 After handoff

When a user correction of a view or new material changes a judgment: change the tree first (FICCOutline 6.2, owned by ficc-outliner) and do not go back to FICCHand to rerun; changing the tree is more than changing the table of contents and the wording; reopen the affected evidence and conclusion checks per shared-protocols/source-check.md (Validity of a check; Reread on a changed binding), and do not build a separate process; only when the decision question itself has changed (a scope decision the user makes, FICCHand 3.1 ⑥), go back to FICCHand and start again from framing.
