# Materials package manifest: what is delivered, what it is called, what format

FICCHand delivers two files; everything else is working files, which stay where they are and are pointed to by the index. The two files are written in the task directory and posted in the conversation; they go to Drive only when the user asks.

## 1 `<文稿名>-提纲.md` (view tree)

Format per `~/.claude/skills/ficc-voice/FICCOutline.md` (nodes O18, node lines O31, fixed marks O38); the research-specific conventions (N numbering, order lines that write the ordering reason, relation lines that wait for ficc-voice's relation sheet, index ids in unfolding lines, register rows' now, 〔作者亲写·逐字〕〔可舍〕) are in `references/outline-from-research.md`; this file sets no format of its own.

## 2 `<文稿名>-资料索引.md` (main materials and data)

Pointers only, no copying of the original. Ten sections (sections 0 to 9), in fixed order:

**0交接单**: see `references/handoff.md`.

**1来源表（S）**

| 编号 | 机构（英文名；美国政府机构用中文） | 正文日期（到日） | 报告名（同一家同一天两份时加短题目） | 文件名日期（与正文差超过7天标出） | 原件路径 | tier | pivotal／skim | 摘要文件 |
|---|---|---|---|---|---|---|---|---|

Date order: the date printed on the original (cover, masthead, disclosure appendix) > the source-list date > the file name's collection date (write “M月D日收录”); “as of” is the data cutoff date, not the release date; do not infer the release date from the file name.

**2判断与数字（E）**: one row per load-bearing figure or per judgment.

| 编号 | 说的是什么（判断或数） | 口径（指标全名、存量／流量、毛／净、交易／估值调整、覆盖范围、单位原样、时间基准、基期、分母） | 谁算的（说话人类别；我们自算标出） | 版本 | 正文日期 | 锚点 | 确认／推断 | 来源数与tier | 采纳／对照 | 提示节点（给定位代理参考） | 标记 |
|---|---|---|---|---|---|---|---|---|---|---|---|

Anchor format: `D-<摘要编号>·S<源编号> L<原件行>`, or `原件路径:L<行>`; it is compatible with the `[src: …]` of shared-protocols/source-check.md (Anchors), and the writer can turn it directly into a sentence anchor. Marks: 有争议（X<编号>） (disputed), 待核实（G<编号>） (to be verified), 易混（C<编号>） (confusable), 单一来源 (single source), 登记（行号） (register, with line number). Keep each figure with its own subject: do not merge two independent assertions into one row.

**3数据序列（Q）**

| 编号 | 序列名与id | 来源 | 口径 | 单位 | 版本（vintage） | 最新一点（值、日期） | 下次发布日 | 取数脚本与缓存路径 | 提示节点 |
|---|---|---|---|---|---|---|---|---|---|

**4图候选（F）**

| 编号 | 原件图（路径、页、面板）或自画 | 显示什么（一句，带口径） | 数据文件 | 不能怎样读（两种口径不能相减、原件没给的比较） | 提示节点 |
|---|---|---|---|---|---|

Use figures from the originals for important logic (`ficc.py fig`); self-drawn figures only fill gaps, with at most three new figures. Figure titles are set by the writing side.

**5分歧（X）**, **6易混（C）**, **7观察清单（W）**, **8缺口与待核实（G）**: each lists ids and one sentence, pointing to the rows of the corresponding section of the map; do not copy the tables. Section 8 lists the important gaps only (unresolved critical dependencies (关键依赖), unresolved explicit must-answers, gaps that bear on a retained judgment), each naming the judgment or must-answer it affects; paused and closed exploratory leads stay in the map's question tree (`R/脉络图.md` section 1, reached through section 9) and are not copied into section 8.

**9工作文件**: `R/brief.md`, `R/inventory.md`, `R/questions.md`, `R/ledger.md`, `R/checks.md`, `R/脉络图.md`, `R/立论.md`, `R/dissent-map.md`, `R/open-threads.md`, `R/cache/`, `T/results/` (digests), each with its path.

## 3 Check

`scripts/tieout.py --outline <提纲> --against <资料索引> <账本>`: lists one by one every number, date and English institution name in the outline's claims, 〔标题〕 lines and name table that cannot be found in the index or the ledger (`ledger.md`), and exits with code 1 if there are any. It matches by numeric value (thousands separators and trailing zeros removed); a date range “M月D日到D日” counts as two dates; section numbers with three or more parts (6.3.1) are not counted as numbers; it does not recognize Chinese numerals or Chinese institution names, which the counter-view seat and the outline check look at.
