#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tieout.py: 提纲主旨、〔标题〕和名字表里的数、日期、英文名称，是否都在资料索引或账本里找得到。

用法：
    python3 tieout.py --outline <提纲.md> --against <资料索引.md> [<账本.md> ...]
    python3 tieout.py --self-test        # 跑同目录 tieout_probes.json 回归集，逐例报实际未匹配数，与预期一致才 PASS
    （2026-10-17 第四轮修订：命令行参数不变；新增数型分开、单位补全和顺序行检查，见下。）

查哪些行：含“**主旨**”或“〔标题”的行（〔标题〕和〔标题 一、〕两种写法都认），以及“名字表”一节（# 标题行起，到下一个同级或更高标题为止）。
候选行：其余以“主旨”“名字表”作行首标签的行（行首只许 # 标题号、列表号、加粗、N 编号和“根”字，后面紧跟冒号或行尾，可隔 **、括注），
    如“- 主旨：”“**主旨：**”“### 主旨：”“- N1 主旨：”“N0 根主旨：”“- **根主旨**：”“**名字表**”“**名字表：**”。
    这些行逐行列为“写法不认”，按未检查处理。例外：只有标签没有内容的 # 标题（如“## 根主旨”），其下一节里有“**主旨**”行就算已覆盖。
    词在句中（如“回到根主旨”“见名字表的机构一栏”“- 信息量测试，只读根和各节点主旨：……”）不是候选行，不查也不报，只在末行计数。
抽什么：
    日期：YYYY年M月D日、M月D日、YYYY-MM-DD、YYYY/MM/DD、YYYY年M月；范围“M月D日到D日”（到、至、—、–、-、~）按两个日期认。
        年份参与比较：提纲日期带年时，索引里同月同日必须同年，或不带年；2026年9月30日不认 2025-09-30。
    短写法（a-b、a/b、a:b，a、b 是一两位整数）按语境分：
        日期：前面紧跟“日期”“截至”“截止”，后面紧跟“至今”“以来”“当天”“当日”“收盘”“开盘”“盘中”，在表头含“日期”“哪天”“date”的列里，或带前导零（09-22、09/23）。
        区间：a-b 后面紧跟单位（%、bp、bn、tn、mn、k、x、pct、pp、个、倍、万、亿、万亿、十亿、年、月……），
            或 a、b 不像月日（3-40）；两端按数。“3至5bn”“3-5bn”“3–5bn”“3~5bn”等价，都抽 3 和 5。
        分数、比值：a/b、a:b（1/3、45/50、1:3）按整体一个数比，提纲写 1/3 要在索引里找到 1/3，拆开的 1 和 3 不算。
            a/b 前面紧跟“比例”“占比”“比重”“约”“近”“超过”“不到”等，或后面紧跟“的”“以上”“以下”“左右”，按分数认。
        歧义：其余像月日的写法（孤立的 10-15；a/b 两边合月日的，如 1/3、9/10、9/22）。
    类型分开（日期、分数、歧义各算各的；跨类型只报“待核”，不算过）：
        同一字面两边都算找到（提纲 1/3 对索引 1/3）。
        索引的歧义写法可以支持提纲里不带年的同月同日日期（9/10 支持 9月10日，短日期兼容）；
            不当成确定的无年日期：提纲日期带年时只报待核，索引另有同月日的别年日期时照报年份不符。
        提纲的分数或歧义写法（1/3）在索引里只见同月日的日期（1月3日）、提纲日期在索引里只见同月日的分数（比例为1/3）：待核。
        数只靠歧义写法或分数的一位才找到时报“待核”，不算缺、也不算过。
    数：去掉日期后的阿拉伯数字（去千分位、去小数末尾的零），数字后面紧跟的单位（bp、bn、tn、% 等）不截断数字：25bp 抽成 25，4.2bp 抽成 4.2；按数值字符串比，不按子串。
        索引里的日期和分数各位不拿来满足提纲的金额：9月22日、09-22 里的 22 不算有 22 万亿；1/3 里的 3 只能报待核。
    英文名称：大写字母开头的拉丁词或词组（如 JPMorgan、Goldman Sachs、ACM、T10YIE）；区分大小写，按子串比。
不抽：编号（R12、G2、N1.2、RT13、S02、L123、Q3 这类字母加数字）、三段以上的节号（6.3.1）、反引号里的内容、中文数词、中文机构名。
约定：提纲的节点编号只用 N 前缀；引别的文件的行号、文件号放进反引号，否则会被当数报出。
顺序行（--outline 同一份提纲，只看提纲，不看索引）：每个有“任务”行的节点（# 标题下一节；一节里有几行“**主旨**”就按主旨行再分），
    要有“顺序：”行（“- **顺序**：”“- 顺序：”，或合写的“任务与顺序：”、任务行里的“顺序：”）；段群级用“挂法”行合写任务与顺序的，算有。
    缺了或只有空行、“待补充”，报“顺序行缺失：<节点>”；顺序行除关系库类别名、节点号和虚词外不剩内容（如“并列”“和N1是因果关系”），
    报“顺序行只写关系名：<节点>”；顺序行里既没有相邻节点的编号（N 编号或 2.3 这类节号），也没有相邻节点主旨行里的实词
    （两字汉字词，不含虚字；三个字母以上的英文词；两位以上的数），报“顺序行只写套话：<节点>”（如“承上启下”）。
    相邻节点标题里的中文序号（“### N2 二、……”的“二”、“（二）”，以及“## 2 ……”整数节号对应的“二”）也算它的编号，顺序行里单独出现即可（“二到五”“七之前”算；
    “二者”“一半”“第一”不算）。
    相邻节点：同级的前一个、后一个节点；某一边没有同级，取文中紧挨着的那个节点；整份只有一个节点时不查套话。类别名：FICCStructure.md 1.1 二十一类（中文名照 glossary.md，连同“与”前后两半）
    和 connectives.md“现行连接词表”的行名（并列、承接、递进、转折、让步、因果、推断、目的、假设、选择、条件等）。
    兼容（FICCOutline O38）：2026-10-17 以前的旧提纲（全文没有一行“顺序：”），节点和任务行同级的“关系：”行算顺序与关系合写，不报缺失，
    只查它是否只写关系名；有“顺序：”行的新提纲里，旧式“关系：”行（不是“和<节点>，通过……”的写法）照旧算合写，新式关系行不算顺序行。
    三类都按“待核”报。
范围：只查词元在索引或账本里是否出现过，不查语义、不查是否同一行；原文对账、查提纲和反方席仍要做。
输出：每行“L行号<TAB>类型<TAB>词元<TAB>原句”；类型是 日期／年月／数／名称（未匹配）、待核、未检查。
退出码：0 全部找到；1 有未匹配（逐条列出）；2 用法或读文件错误；
    3 未检查：0 行目标行，或有任何一行写法不认（有未匹配也报 3），或没有未匹配但有待核（数型待核、顺序行待核都算）。
"""
import argparse
import json
import os
import re
import sys

ID_RE = re.compile(r"(?<![A-Za-z0-9])[A-Za-z]{1,4}\d+(?:[.·]\d+)*[a-z]?(?![A-Za-z0-9])|\d+:L\d+")
CODE_RE = re.compile(r"`[^`]*`")
SECNUM_RE = re.compile(r"(?<![\d.])\d+(?:\.\d+){2,}(?![\d.])")
DATE_RANGE = re.compile(r"(?:(\d{4})年)?(\d{1,2})月(\d{1,2})日\s*(?:到|至|—|–|-|~|～)\s*(\d{1,2})日")
DATE_YMD = re.compile(r"(\d{4})年(\d{1,2})月(\d{1,2})日")
DATE_MD = re.compile(r"(?<![\d年])(\d{1,2})月(\d{1,2})日")
DATE_ISO = re.compile(r"(?<!\d)(\d{4})[-/](\d{1,2})[-/](\d{1,2})(?!\d)")
DATE_YM = re.compile(r"(\d{4})年(\d{1,2})月(?!\d{1,2}日)")
# 短写法 a-b、a/b、a:b；先按语境分成日期、区间、分数、比值、歧义，再决定怎么用（见 classify_short）。
SHORT_RE = re.compile(r"(?<![\d.\-/:])(\d{1,4}(?:\.\d+)?)\s*([-/:])\s*(\d{1,4}(?:\.\d+)?)(?![\d.\-/:])")
UNIT_AFTER = re.compile(r"\s*(?:%|％|[bB][pP][sS]?|[bBtTmM][nN](?![A-Za-z])|[kK](?![A-Za-z])|[xX×](?![A-Za-z])"
                        r"|[pP][cC][tT](?![A-Za-z])|[pP][pP](?![A-Za-z])"
                        r"|个|倍|万亿|万|十亿|十|亿|千|百|年|岁|天|日|周|月|季|家|只|笔|次|点|成|元|美元|人|户|项|条|篇|轮|级|码)")
# a/b 的分数语境：前面紧跟比例、占比、约、近……，或后面紧跟“的”“以上”“以下”“左右”（约1/3的资金、比例为1/3）。
FRAC_BEFORE = re.compile(r"(?:比例|占比|比重|比率|份额|约占|约|近|逾|超过|不到|不足|大约|将近|接近|大概|仅|只有|达到|达)"
                         r"\s*(?:为|是|达|约|近)?\s*[:：]?\s*$")
FRAC_AFTER = re.compile(r"^\s*(?:的|以上|以下|左右)")
CTX_BEFORE = re.compile(r"(?:日期|截至|截止)\s*[:：]?\s*$")
CTX_AFTER = re.compile(r"^\s*(?:至今|以来|当天|当日|收盘|开盘|盘中)")
DATE_HEADER = re.compile(r"日期|哪天|date", re.I)
SEP_ROW = re.compile(r"^\s*\|?\s*:?-{3,}")
# 数字整体匹配：结尾只要求后面不是数字，单位字母（bp、bn、tn）可以紧跟，不再回退截短。
NUM_RE = re.compile(r"(?<![\d.A-Za-z])(\d{1,3}(?:,\d{3})+|\d+)(?:\.(\d+))?(?!\d)")
NAME_RE = re.compile(r"[A-Z][A-Za-z0-9&'\-]*(?:\s+[A-Z][A-Za-z0-9&'\-]*)*")
# 候选行：“主旨”“名字表”是行首标签（行首只许 # 标题号、列表号、加粗、N 编号、“根”字；后面紧跟冒号或行尾，可隔 **、括注）。
CAND_RE = re.compile(r"^\s*(?:#+\s*)?(?:[-*+]\s+|\d+[.、)]\s*)?(?:\*{1,2}|_{1,2})?\s*"
                     r"(?:[A-Z]{1,2}\d+(?:\.\d+)*[a-z]?\s*)?根?"
                     r"(?:主旨[句行段]?|名字表)\s*(?:\*{1,2}|_{1,2})?\s*(?:[（(][^）)]*[）)])?"
                     r"\s*(?:\*{1,2}|_{1,2})?\s*(?:[:：]|$)")
HEAD_RE = re.compile(r"^(#+)\s")


def norm_num(intpart, frac):
    intpart = intpart.replace(",", "").lstrip("0") or "0"
    frac = (frac or "").rstrip("0")
    return intpart + ("." + frac if frac else "")


def nnum(s):
    i, _, f = s.partition(".")
    return norm_num(i, f)


def strip_ids(text):
    return SECNUM_RE.sub(" ", ID_RE.sub(" ", CODE_RE.sub(" ", text)))


def classify_short(a, sep, b, before, after):
    """短写法分类：date／range／frac／ratio／amb。a、b 是原样数字串。"""
    if sep == ":":
        return "ratio"
    small = "." not in a + b and len(a) <= 2 and len(b) <= 2
    if sep == "-":
        if not small or UNIT_AFTER.match(after):
            return "range"
    elif not small:
        return "frac"
    m, d = int(a), int(b)
    if not (1 <= m <= 12 and 1 <= d <= 31):
        return "range" if sep == "-" else "frac"
    if CTX_BEFORE.search(before) or CTX_AFTER.match(after):
        return "date"
    if (len(a) == 2 and a[0] == "0") or (len(b) == 2 and b[0] == "0"):
        return "date"
    if sep == "/" and (FRAC_BEFORE.search(before) or FRAC_AFTER.match(after)):
        return "frac"
    return "amb"  # a-b：区间或日期；a/b：分数或日期


def mark_date_cells(text):
    """表头含“日期”“哪天”“date”的列里，短写法 a-b、a/b 改写成 M月D日。"""
    lines = text.split("\n")
    cols = set()
    for i, line in enumerate(lines):
        if not line.lstrip().startswith("|"):
            cols = set()
            continue
        if i + 1 < len(lines) and SEP_ROW.match(lines[i + 1]) and not SEP_ROW.match(line):
            cols = {j for j, c in enumerate(line.split("|")) if DATE_HEADER.search(c)}
            continue
        if not cols or SEP_ROW.match(line):
            continue
        cells = line.split("|")
        for j in cols:
            if j < len(cells):
                cells[j] = re.sub(
                    r"^(\s*)0?(\d{1,2})[-/]0?(\d{1,2})(?!\d)",
                    lambda mo: (f"{mo.group(1)}{int(mo.group(2))}月{int(mo.group(3))}日"
                                if 1 <= int(mo.group(2)) <= 12 and 1 <= int(mo.group(3)) <= 31
                                else mo.group(0)),
                    cells[j])
        lines[i] = "|".join(cells)
    return "\n".join(lines)


def extract(text, for_index=False):
    """Return dict: dates, yms, nums, names, amb_nums{num: {src}}, amb_tokens{tok: (m, d, a, b, sep)},
    amb_md{(m, d): {src}}, frac_md{(m, d): {src}}。

    类型分开：dates 只放确定的日期。索引（for_index）：歧义写法的月日进 amb_md（不进 dates，不当确定的无年日期），
    两端数进 amb_nums（只能报待核），a/b 整体进 nums（同一字面的分数照样找到）；
    分数、比值整体进 nums，各位进 amb_nums，像月日的 a/b 分数另记 frac_md（只供跨类型报待核）。
    提纲：分数、比值整体进 nums；歧义写法进 amb_tokens 另查。
    """
    t = strip_ids(text)
    if for_index:
        t = mark_date_cells(t)
    dates, yms = set(), set()
    nums, amb_nums, amb_tokens = set(), {}, {}
    amb_md, frac_md = {}, {}
    for y, m, d1, d2 in DATE_RANGE.findall(t):
        dates.add((y or None, int(m), int(d1)))
        dates.add((y or None, int(m), int(d2)))
    t = DATE_RANGE.sub(" ", t)
    for y, m, d in DATE_YMD.findall(t):
        dates.add((y, int(m), int(d)))
    t2 = DATE_YMD.sub(" ", t)
    for y, m, d in DATE_ISO.findall(t2):
        dates.add((y, int(m), int(d)))
    t2 = DATE_ISO.sub(" ", t2)
    for m, d in DATE_MD.findall(t2):
        dates.add((None, int(m), int(d)))
    t2 = DATE_MD.sub(" ", t2)
    for y, m in DATE_YM.findall(t2):
        yms.add((y, int(m)))
    t2 = DATE_YM.sub(" ", t2)

    def repl(mo):
        a, sep, b = mo.group(1), mo.group(2), mo.group(3)
        line_start = mo.string.rfind("\n", 0, mo.start()) + 1
        line_end = mo.string.find("\n", mo.end())
        before = mo.string[line_start:mo.start()]
        after = mo.string[mo.end():line_end if line_end >= 0 else len(mo.string)]
        kind = classify_short(a, sep, b, before, after)
        whole = f"{nnum(a)}{sep}{nnum(b)}"
        if kind == "range":
            return mo.group(0)
        if kind == "date":
            dates.add((None, int(a), int(b)))
            return " "
        src = mo.group(0).replace(" ", "")
        if kind in ("frac", "ratio"):
            nums.add(whole)
            if for_index:
                for x in (nnum(a), nnum(b)):
                    amb_nums.setdefault(x, set()).add(src)
                if sep == "/" and "." not in a + b and 1 <= int(a) <= 12 and 1 <= int(b) <= 31:
                    frac_md.setdefault((int(a), int(b)), set()).add(src)
            return " "
        # 歧义：不删两端数，也不让它们满足金额；索引里同月同日只记进 amb_md，不当确定日期。
        # a/b 同时是分数候选：整体也进 nums，提纲写同一个分数照样找到。
        amb_tokens[whole] = (int(a), int(b), nnum(a), nnum(b), sep)
        if for_index:
            amb_md.setdefault((int(a), int(b)), set()).add(src)
            if sep == "/":
                nums.add(whole)
            for x in (nnum(a), nnum(b)):
                amb_nums.setdefault(x, set()).add(src)
        return " "

    t2 = SHORT_RE.sub(repl, t2)
    nums |= {norm_num(a, b) for a, b in NUM_RE.findall(t2)}
    names = {n.strip() for n in NAME_RE.findall(t2) if len(n.strip()) >= 2}
    return {"dates": dates, "yms": yms, "nums": nums, "names": names,
            "amb_nums": amb_nums, "amb_tokens": amb_tokens, "amb_md": amb_md, "frac_md": frac_md}


def scan(lines):
    """Return (targets, loose, mentions)：目标行、写法不认的候选行、句中提到主旨／名字表的行数。"""
    targets, loose, mentions = [], [], 0
    claim_heads = []  # (行号, 原行, 级别)：只有标签没有内容的主旨标题，看下一节有没有目标行
    heads = []        # (行号, 级别)
    in_names, level = False, 0
    for i, line in enumerate(lines, 1):
        s = line.rstrip("\n")
        h = HEAD_RE.match(s)
        if h:
            heads.append((i, len(h.group(1))))
            if in_names and len(h.group(1)) <= level:
                in_names = False
            if "名字表" in s:
                in_names, level = True, len(h.group(1))
                continue
        if in_names or "**主旨**" in s or "〔标题" in s:
            targets.append((i, s))
            continue
        if "主旨" not in s and "名字表" not in s:
            continue
        mo = CAND_RE.search(s)
        if not mo:
            mentions += 1
        elif h and not re.sub(r"[\s*_]", "", s[mo.end():]):
            claim_heads.append((i, s, len(h.group(1))))
        else:
            loose.append((i, s))
    target_nums = [ln for ln, _ in targets]
    for i, s, lv in claim_heads:
        end = next((j for j, l2 in heads if j > i and l2 <= lv), len(lines) + 1)
        if not any(i < ln < end for ln in target_nums):
            loose.append((i, s))
    loose.sort()
    return targets, loose, mentions


def target_lines(lines):
    return scan(lines)[0]


def loose_lines(lines):
    return scan(lines)[1]


def run(outline_text, against_texts):
    """Return (misses, pending)：每项 (行号, 类型, 词元, 原句)；pending 的类型是“待核”。

    日期、分数、歧义写法各保类型：同一字面或同类型找到才算过；只靠别的类型同月日找到，报待核（见文件头“类型分开”）。
    """
    a_dates, a_yms, a_nums, a_amb_nums, a_amb_tokens = set(), set(), set(), {}, set()
    a_amb_md, a_frac_md = {}, {}
    blob = "\n".join(against_texts)
    for tx in against_texts:
        e = extract(tx, for_index=True)
        a_dates |= e["dates"]
        a_yms |= e["yms"]
        a_nums |= e["nums"]
        for k, v in e["amb_nums"].items():
            a_amb_nums.setdefault(k, set()).update(v)
        a_amb_tokens |= set(e["amb_tokens"])
        for k, v in e["amb_md"].items():
            a_amb_md.setdefault(k, set()).update(v)
        for k, v in e["frac_md"].items():
            a_frac_md.setdefault(k, set()).update(v)
    a_md = {(m, d) for _, m, d in a_dates}  # 确定日期的月日（任何年份，或不带年）
    a_ym_all = a_yms | {(y, m) for y, m, _ in a_dates if y}
    misses, pending = [], []

    def amb_src(n):
        return "、".join(f"“{s}”" for s in sorted(a_amb_nums[n]))

    def md_note(md, kinds):
        """索引里同月日的别类写法，供待核说明：kinds 取 date／amb／frac。"""
        parts = []
        if "date" in kinds and md in a_md:
            parts.append(f"日期{md[0]}月{md[1]}日")
        if "amb" in kinds and md in a_amb_md:
            parts.append("歧义写法" + "、".join(f"“{s}”" for s in sorted(a_amb_md[md])))
        if "frac" in kinds and md in a_frac_md:
            parts.append("分数" + "、".join(f"“{s}”" for s in sorted(a_frac_md[md])))
        return "、".join(parts)

    def frac_md_of(n):
        """像月日的 a/b 分数（1/3、9/10）返回 (a, b)，否则 None。"""
        mo = re.fullmatch(r"(\d{1,2})/(\d{1,2})", n)
        if mo and 1 <= int(mo.group(1)) <= 12 and 1 <= int(mo.group(2)) <= 31:
            return int(mo.group(1)), int(mo.group(2))
        return None

    for ln, line in scan(outline_text.splitlines())[0]:
        e = extract(line)
        for y, m, d in sorted(e["dates"], key=str):
            tok = f"{y + '年' if y else ''}{m}月{d}日"
            if y:
                # 年份参与比较：同年同月同日，或索引里不带年的同月同日（确定日期）
                if (y, m, d) in a_dates or (None, m, d) in a_dates:
                    continue
                if (m, d) in a_md:
                    # 同月日只见别的年份：年份不符；歧义写法、分数不能顶替成无年日期
                    misses.append((ln, "日期", tok, line))
                elif (m, d) in a_amb_md or (m, d) in a_frac_md:
                    pending.append((ln, "待核", f"{tok}（索引只见{md_note((m, d), ('amb', 'frac'))}，不是带年的日期）", line))
                else:
                    misses.append((ln, "日期", tok, line))
            else:
                # 不带年：确定日期同月日即可；歧义写法也可支持（短日期兼容）
                if (m, d) in a_md or (m, d) in a_amb_md:
                    continue
                if (m, d) in a_frac_md:
                    pending.append((ln, "待核", f"{tok}（索引只见{md_note((m, d), ('frac',))}，类型不同）", line))
                else:
                    misses.append((ln, "日期", tok, line))
        for y, m in sorted(e["yms"]):
            if (y, m) not in a_ym_all:
                misses.append((ln, "年月", f"{y}年{m}月", line))
        for n in sorted(e["nums"]):
            if n in a_nums:
                continue
            md = frac_md_of(n)
            if md and (md in a_md or md in a_amb_md):
                # 提纲的分数只见同月日的日期或歧义写法：跨类型，待核
                pending.append((ln, "待核", f"{n}（索引只见{md_note(md, ('date', 'amb'))}，类型不同）", line))
            elif n in a_amb_nums:
                pending.append((ln, "待核", f"{n}（索引只见{amb_src(n)}）", line))
            else:
                misses.append((ln, "数", n, line))
        for tok, (m, d, x, z, sep) in sorted(e["amb_tokens"].items()):
            # 提纲里的歧义写法：同一字面，或（a-b）两端数都在，算找到；a/b 不拆开比
            if tok in a_amb_tokens or tok in a_nums:
                continue
            if sep == "-" and x in a_nums and z in a_nums:
                continue
            if (m, d) in a_md or (m, d) in a_amb_md or (m, d) in a_frac_md:
                # 只见同月日的日期、别的歧义写法或分数：跨类型，待核
                pending.append((ln, "待核", f"{tok}（索引只见{md_note((m, d), ('date', 'amb', 'frac'))}，类型不同）", line))
            elif sep == "-" and all(v in a_nums or v in a_amb_nums for v in (x, z)):
                src = "、".join(amb_src(v) for v in (x, z) if v in a_amb_nums)
                pending.append((ln, "待核", f"{tok}（索引只见{src}）", line))
            else:
                misses.append((ln, "数", tok, line))
        for n in sorted(e["names"]):
            if n not in blob:
                misses.append((ln, "名称", n, line))
    return misses, pending


# 顺序行检查：关系库类别名。二十一类照 ficc-voice/FICCStructure.md 1.1（中文名照 references/glossary.md），
# 连接词表行名照 ficc-voice/references/connectives.md“1 现行连接词表”。两处改了，这里同步。
REL_TYPES_21 = ("分类与分工", "互补", "总述与展开", "归纳与综合", "解释与澄清", "主张与支持", "依据与推论",
                "因果与机制", "条件与限制", "递进与深化", "前提与依赖", "比较与对照", "类比与迁移", "质疑与回应",
                "问题与解决", "目标与手段", "选择与取舍", "时间与空间", "铺垫与兑现", "呼应与变奏", "节奏与情绪调节")
REL_TYPES_EN = ("classification and division of labor", "complementarity", "overview and unfolding",
                "induction and synthesis", "explanation and clarification", "assertion and support",
                "grounds and inference", "cause and mechanism", "conditions and limits", "progression and deepening",
                "premise and dependency", "comparison and contrast", "analogy and transfer", "objection and response",
                "problem and solution", "goals and means", "choice and trade-off", "time and space",
                "setup and payoff", "echo and variation", "pacing and mood regulation")
CONNECTIVE_ROWS = ("并列", "并列·附加关系", "并列·解说", "承接关系（先后）", "递进", "转折", "转折·让步",
                   "因果", "因果·推断", "因果·目的", "假设", "选择", "条件")


def _relation_names():
    names = set(REL_TYPES_21) | set(REL_TYPES_EN)
    for n in REL_TYPES_21:
        names.update(x for x in n.split("与") if x)
    for n in CONNECTIVE_ROWS:
        names.add(n)
        names.update(x for x in re.split(r"[·（）]", n) if x)
    names.add("承接")
    return sorted(names, key=len, reverse=True)


REL_NAMES = _relation_names()
ORDER_FILLER = sorted(("关系库", "关系", "接缝", "一类", "之间", "属于", "构成", "形成", "两者", "二者", "两节", "两块",
                       "彼此", "相互", "互相", "本节", "上一节", "下一节", "前一节", "后一节", "上节", "下节", "前节",
                       "后节", "同级", "节点", "上级", "下级", "相邻", "兄弟", "是", "为", "属", "类", "和", "与", "同",
                       "跟", "对", "的", "在", "排", "前", "后", "先", "再", "接", "即", "型", "式", "按", "照", "组",
                       "种", "也", "都", "又", "根", "可以对调", "可对调", "能对调", "可互换", "可调换",
                       "and", "is", "the", "with"), key=len, reverse=True)
NODE_REF_RE = re.compile(r"[NnSs]?\d+(?:\.\d+)*|[（(][一二三四五六七八九十\d]{1,3}[）)]"
                         r"|[一二三四五六七八九十]{1,3}(?=[、，,。；;：:\s→←↔\-–—~～/／和与跟同对在之前后]|$)")
NODE_LABEL_RE = re.compile(r"^\s*(?:[-*+]\s+|\d+[.、)]\s*)?(?:\*{1,2}|_{1,2})?`?\s*"
                           r"([\u4e00-\u9fff][\u4e00-\u9fff／/、与和及·]{0,9}?)\s*`?\s*(?:\*{1,2}|_{1,2})?\s*[:：]"
                           r"\s*`?\s*(?:\*{1,2}|_{1,2})?\s*(.*)$")
LABEL_OK = re.compile(r"(?:任务|顺序|关系|挂法|展开|主旨)(?:[／/、与和及·](?:任务|顺序|关系|挂法|展开|主旨))*")
CLAIM_START = re.compile(r"^\s*(?:[-*+]\s+)?\*\*主旨\*\*")
NEW_REL = re.compile(r"^\s*和\s*\S{1,24}?\s*[，,]\s*通过")
FENCE_RE = re.compile(r"^\s{0,3}(```|~~~)")


# 套话检查：两字词的两个字都不在虚字表里才算实词；关系库类别名先去掉，不拿来比。
STOP_CHARS = set("的是在了和与及或也都这那其此之一不有为把被对从到由于让使将还又更很最就才而但所以因如果则并且即便虽然却只仅"
                 "再先后前上下中里外内个些种类每各该本们你我他她它吗呢吧么什怎样何多少几第两二三四五六七八九十节点级同读者排放写说讲"
                 "看要会能可来去出起过着地得给")
NODE_ID_RE = re.compile(r"N\d+(?:\.\d+)*|(?<![\d.])\d+\.\d+(?:\.\d+)*(?![\d.])")
CN_NUM = "一二三四五六七八九十"
HEAD_ORD_RE = re.compile(r"^#+\s*(?:N?\d+(?:\.\d+)*\s+)?(?:〔[^〕]*〕\s*)?(?:([%s]{1,3})、|[（(]([%s]{1,3})[）)])" % (CN_NUM, CN_NUM))
CN_ORD = [""] + list(CN_NUM) + ["十" + c for c in CN_NUM[:9]] + ["二十"]   # 1→一 … 20→二十：“## 2 ……”这种整数节号的中文序号
ORD_IN_LINE = re.compile(r"(?<![%s第])([%s]{1,3})(?![%s者手级成半方些个种次是起样致般直定旦边面切共同])"
                         % (CN_NUM, CN_NUM, CN_NUM))


def content_terms(text):
    """实词：两字汉字词（两个字都不是虚字）、三个字母以上的英文词、两位以上的数。"""
    t = re.sub(r"`[^`]*`|\*\*|__", " ", text)
    for name in REL_NAMES:
        t = t.replace(name, " ")
    terms = set()
    for run in re.findall(r"[\u4e00-\u9fff]+", t):
        for i in range(len(run) - 1):
            if run[i] not in STOP_CHARS and run[i + 1] not in STOP_CHARS:
                terms.add(run[i:i + 2])
    terms |= set(re.findall(r"[A-Za-z][A-Za-z0-9&\-]{2,}", t))
    terms |= {n for n in re.findall(r"\d+(?:\.\d+)?", t) if len(n) >= 2}
    return terms


def node_label(line):
    """取行首 # 号；N 编号或节号优先（### N1 一、〔标题〕… → N1；#### 1.1 段群 → 1.1）。"""
    t = line.lstrip("#").strip()
    mo = re.match(r"(N\d+(?:\.\d+)*|\d+(?:\.\d+)*)(?=[\s　]|$)", t)
    return mo.group(1) if mo else (t[:20] or "（无标题）")


def is_placeholder(body):
    t = re.sub(r"[\W_]+", "", body)
    return not t or bool(re.fullmatch(r"待[\u4e00-\u9fff]{0,6}|空|无|TBD|tbd", t))


def relation_only(body):
    """顺序行去掉关系库类别名、节点号和虚词后不剩内容：返回见到的类别名；否则返回 []。"""
    t = re.sub(r"`[^`]*`|\*\*|__", " ", body).lower()
    hit = []
    for name in REL_NAMES:
        if name in t:
            hit.append(name)
            t = t.replace(name, " ")
    if not hit:
        return []
    t = NODE_REF_RE.sub(" ", t)
    for w in ORDER_FILLER:
        t = t.replace(w, " ")
    rest = re.sub(r"[\W\d_]+", "", t)
    return hit if len(rest) < 3 else []


def order_issues(lines):
    """每个有“任务”行的节点要有“顺序：”行，且不只写关系名。返回 [(行号, "待核", 词元, 原句)]。"""
    parsed, fence = [], False
    for i, s in enumerate(lines, 1):
        if FENCE_RE.match(s):
            fence = not fence
            continue
        if fence:
            continue
        kinds, ind, body = set(), None, ""
        mo = NODE_LABEL_RE.match(s)
        if mo and LABEL_OK.fullmatch(mo.group(1)):
            lab, body = mo.group(1), mo.group(2)
            ind = len(s) - len(s.lstrip())
            kinds = {k for k, w in (("task", "任务"), ("order", "顺序"), ("rel", "关系"), ("hang", "挂法")) if w in lab}
        parsed.append((i, s, kinds, ind, body))
    old_outline = not any("order" in k for _, _, k, _, _ in parsed)

    blocks, cur = [], None
    for i, s, kinds, ind, body in parsed:
        h = HEAD_RE.match(s)
        if h:
            om = HEAD_ORD_RE.match(s)
            cur = {"label": node_label(s), "rows": [], "claim": False, "level": len(h.group(1)), "text": "",
                   "ord": (om.group(1) or om.group(2)) if om else None}
            blocks.append(cur)
            continue
        if cur is None:
            cur = {"label": "（无标题）", "rows": [], "claim": False, "level": 0, "text": "", "ord": None}
            blocks.append(cur)
        if CLAIM_START.match(s):
            if cur["claim"]:
                cur = {"label": cur["label"], "rows": [], "claim": True, "sub": True, "level": cur["level"], "text": "",
                       "ord": None}
                blocks.append(cur)
            cur["claim"] = True
            cur["text"] = s
        cur["rows"].append((i, s, kinds, ind, body))
    nodes = [b for b in blocks if b["claim"]]

    def neighbours(b):
        """同级的前一个、后一个节点；某一边没有同级，取文中紧挨着的节点。"""
        if b not in nodes:
            return []
        k, out = nodes.index(b), []
        for rng in (range(k - 1, -1, -1), range(k + 1, len(nodes))):
            near = next(iter([nodes[j] for j in rng]), None)
            sib = None
            for j in rng:
                if nodes[j]["level"] < b["level"]:
                    break
                if nodes[j]["level"] == b["level"]:
                    sib = nodes[j]
                    break
            if sib or near:
                out.append(sib or near)
        return out

    out = []
    for k, b in enumerate(blocks):
        tasks = [r for r in b["rows"] if "task" in r[2]]
        if not tasks:
            continue
        label = b["label"]
        if b.get("sub") or (k + 1 < len(blocks) and blocks[k + 1].get("sub")):
            label += f"·L{b['rows'][0][0]}"
        t_ln, t_s, _, t_ind, _ = tasks[0]
        src = next((r for r in b["rows"] if "order" in r[2]), None)
        if src is None:
            for r in b["rows"]:
                if r[2] & {"task", "hang"}:
                    mo = re.search(r"顺序\s*[:：]\s*(.*)$", r[4])
                    if mo:
                        src = (r[0], r[1], r[2], r[3], mo.group(1))
                        break
        if src is None:
            src = next((r for r in b["rows"] if "hang" in r[2]), None)
        if src is None:
            rels = [r for r in b["rows"] if "rel" in r[2] and r[3] <= t_ind and not is_placeholder(r[4])]
            if rels and (old_outline or not NEW_REL.match(rels[0][4])):
                src = rels[0]  # O38 兼容：旧式关系行算顺序与关系合写
        if src is None or is_placeholder(src[4]):
            why = "顺序行为空" if src is not None else "没有顺序行"
            out.append((t_ln, "待核", f"顺序行缺失：{label}（{why}）", t_s))
            continue
        names = relation_only(src[4])
        if names:
            out.append((src[0], "待核", f"顺序行只写关系名：{label}（只见{'、'.join(names)}）", src[1]))
            continue
        nb = neighbours(b)
        if not nb:
            continue  # 整份只有一个节点：没有相邻节点可比
        ids = {x["label"].split("·")[0] for x in nb}
        ords = {x["ord"] for x in nb if x.get("ord")}
        ords |= {CN_ORD[int(x["label"])] for x in nb if x["label"].isdigit() and 0 < int(x["label"]) < len(CN_ORD)}
        if ids & set(NODE_ID_RE.findall(src[4])) or ords & set(ORD_IN_LINE.findall(src[4])):
            continue
        near_terms = set().union(*(content_terms(x["text"].split("**主旨**", 1)[-1]) for x in nb))
        if content_terms(src[4]) & near_terms:
            continue
        out.append((src[0], "待核", f"顺序行只写套话：{label}（不见相邻节点{'、'.join(sorted(ids))}的编号，"
                                     f"也不见它们主旨行里的实词）", src[1]))
    return out


def check(outline_text, against_texts):
    """Return (exit_code, misses, n_targets, loose, pending, mentions)."""
    lines = outline_text.splitlines()
    targets, loose, mentions = scan(lines)
    misses, pending = run(outline_text, against_texts)
    pending = pending + order_issues(lines)
    if loose or not targets:
        code = 3
    elif misses:
        code = 1
    elif pending:
        code = 3
    else:
        code = 0
    return code, misses, len(targets), loose, pending, mentions


# 回归集不在时的后备用例：(名字, 提纲, 索引, 预期退出码, 预期未匹配[(类, 词元)])
SELF_OUTLINE = """# 提纲
## 名字表
- 期限溢价（ACM）：按 ACM 模型算
## 根主旨
- **主旨**：9月22日到30日长端领涨，长端升了39个基点（R01，见 6.3.1），JPMorgan 说政策路径占40。
- **主旨**：Barclays 估计4.2万亿。〔标题〕长端：九月先涨在加息
### N1 〔标题 一、〕Citi 看长端：九月先涨在加息
"""
SELF_INDEX = """| E1 | 长端 9月30日 5.64%，升39个基点 | 09-22 起长端领涨 | ACM | JPMorgan 2026-09-12 政策路径占 40 |"""
SELF_CASES = [
    ("基础", SELF_OUTLINE, SELF_INDEX, 1,
     [("名称", "Barclays"), ("名称", "Citi"), ("数", "4.2")]),
    ("单位不截数", "- **主旨**：收益率上升25bp，另一段升4.2bp。",
     "收益率上升2个基点，另一段升4个基点。", 1, [("数", "25"), ("数", "4.2")]),
    ("年份参与比较", "- **主旨**：2026年9月30日见顶。",
     "| E1 | 2025-09-30 见顶 |", 1, [("日期", "2026年9月30日")]),
    ("短日期不当数", "- **主旨**：增加22万亿美元。",
     "| E1 | 09-22 | 09/23 |", 1, [("数", "22")]),
    ("零覆盖不当通过", "- 主旨：4.2万亿美元。\n\n**名字表**\n\n| Barclays | 机构 |",
     "无相关资料", 3, []),
]
PROBES_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tieout_probes.json")


def load_cases(path=PROBES_FILE):
    """读回归集；文件不在时用内置五组。返回 (cases, 来源说明)。"""
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)["cases"], os.path.basename(path)
    cases = [{"id": n, "outline": o, "against": [a],
              "expect": {"exit": c, "misses": [list(x) for x in w], "pending": [], "unchecked": None}}
             for n, o, a, c, w in SELF_CASES]
    return cases, "内置五组（未找到 tieout_probes.json）"


def compare(case, code, misses, n_targets, loose, pending):
    """与预期比：退出码、未匹配(类,词元)、待核词元、写法不认行数、目标行数（预期里有才比）。返回差异列表。"""
    exp = case["expect"]
    got_m = sorted([k, v] for _, k, v, _ in misses)
    got_p = sorted(v.split("（")[0] for _, _, v, _ in pending)
    diffs = []
    if code != exp["exit"]:
        diffs.append(f"退出码 {code}≠{exp['exit']}")
    if got_m != sorted(exp.get("misses", [])):
        diffs.append(f"未匹配 {got_m}≠{sorted(exp.get('misses', []))}")
    if got_p != sorted(exp.get("pending", [])):
        diffs.append(f"待核 {got_p}≠{sorted(exp.get('pending', []))}")
    if exp.get("unchecked") is not None and len(loose) != exp["unchecked"]:
        diffs.append(f"写法不认 {len(loose)}≠{exp['unchecked']}")
    if exp.get("targets") is not None and n_targets != exp["targets"]:
        diffs.append(f"目标行 {n_targets}≠{exp['targets']}")
    return diffs


def self_test():
    cases, src = load_cases()
    n_fail, total = 0, 0
    for case in cases:
        against = case["against"] if isinstance(case["against"], list) else [case["against"]]
        code, misses, n_targets, loose, pending, _ = check(case["outline"], against)
        diffs = compare(case, code, misses, n_targets, loose, pending)
        n_fail += bool(diffs)
        total += len(misses)
        got = sorted((k, v) for _, k, v, _ in misses)
        print(f"  {case['id']}: {'FAIL' if diffs else 'PASS'} 退出码 {code}（预期 {case['expect']['exit']}）；"
              f"目标行 {n_targets}，不认的行 {len(loose)}，待核 {len(pending)}；未匹配 {len(got)} 处 {got}"
              + (f"；差异：{'；'.join(diffs)}" if diffs else ""))
    ok = n_fail == 0 and total > 0
    print("self-test", "PASS" if ok else "FAIL",
          f"：{src} {len(cases)} 例，失败 {n_fail} 例，共报出未匹配 {total} 处")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--outline")
    ap.add_argument("--against", nargs="+")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    if not a.outline or not a.against:
        ap.print_usage(sys.stderr)
        return 2
    try:
        outline = open(a.outline, encoding="utf-8").read()
        against = [open(p, encoding="utf-8").read() for p in a.against]
    except OSError as e:
        print(f"读文件失败：{e}", file=sys.stderr)
        return 2
    code, misses, n_lines, loose, pending, mentions = check(outline, against)
    for ln, kind, tok, line in misses + pending:
        print(f"L{ln}\t{kind}\t{tok}\t{line.strip()[:80]}")
    for ln, line in loose:
        print(f"L{ln}\t未检查\t写法不认\t{line.strip()[:80]}")
    if n_lines == 0:
        print("未检查：0 行（没有含“**主旨**”“〔标题”的行，也没有 # 名字表 一节）")
    n_order = sum(1 for p in pending if p[2].startswith("顺序行"))
    print(f"查了 {n_lines} 行；未匹配 {len(misses)} 处；待核 {len(pending)} 处"
          + (f"（其中顺序行 {n_order} 处）" if n_order else "") + f"；写法不认 {len(loose)} 行"
          + (f"；句中提到主旨／名字表 {mentions} 行（不是目标行，不查）" if mentions else ""))
    return code


if __name__ == "__main__":
    sys.exit(main())
