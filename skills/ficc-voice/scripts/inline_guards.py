#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inline_guards.py 1.3.2 (2026-11-21, W1; 1.1.0 W1b on the Wave K evidence; 1.2.0 W4b review fixes; 1.3.0 W1-0to1;
1.3.1 D8 W4a; 1.3.2 D8 W4b)
-- deterministic fact guards for the
ficc-voice writers, above all the weakest one (the tool-less inline seat): what a script can settle before a call is
settled here, and every load-bearing claim a writer returns is checked clause by clause against the frozen fact source
before it may become a published draft or travel on as a trace line.

W1b (1.1.0): '## 思路' slot mismatches are diagnostics only (verify 'diagnostics'; they never reject and never clear a
正文 finding); an ordinal quarter (第一财季, 第2季度) is a period, never a duration unit, and a base heading's numbers
are base numbers; the outline's 名字表 (CJK and Latin names, quoted full names, 本篇写法 forms) and 全称（下称简称）
aliases enter the entity lexicon, and a name-table entity counts as a proper name for holder conflicts; semantic
candidates are queued (a number-free or paragraph-opening sentence with no close base counterpart, a modal or
trajectory word the base sentences lack, a citation date in parentheses that B and C lack, a citation newly attached,
a 前者／后者 whose antecedent pair changed); trace quarantine is narrowed to the evidence of a finding (diagnostics
and small counts never quarantine; semantic candidates quarantine only a trace line that quotes them).

W4b (1.2.0, the Wave 4 review): an explicit minus is part of a value (G-SIGN hard when 20 and -20 swap; a direction
word's sign still matches the bare number, and one that turns a base rise negative is a candidate); a rewrite's only
fact source is B (a number found in C alone is new); reporting periods are compared (G-PERIOD: hard when an anchored
sentence swaps its sole quarter, 第一财季 -> 第四财季, else a candidate that quarantines the trace lines naming the
period); in a rewrite with opening detail relocation on, a base opening's source, date or sample-list item gone from
the whole node and not listed in 开头后移 is a semantic candidate (G-RELOC); lint keeps a tie-out seat's fact fix whole
when every new number is in B/C; release-trace takes the node lock acceptance/.<node>.lock (inline_common.node_lock);
recompute --base lists the tokens the base lacks.

W1-0to1 (1.3.0, 算在树上，叶席零新数, V26): a draft may be written from nothing (0→1): B empty, the fact source C (the
node's 事实 source excerpts and 消歧 quotes) plus DERIVATIONS, the living outline's signed 算式 rows that pack_node
freezes: {"id","node","metric","value","denominator","basis","operands":[{"name","value","anchor"}],"expr","signed",
"raw"}. A derivation's value attests a body token only when the row is signed and the token's clause (else, when the
clause names no metric of its own, its sentence) holds the row's context: the row's metric, or its denominator with
a share/ratio cue (the context rule and SHARE_CUE_RE, one place: ctx_hit). The same value under another metric is
G-DERIV hard (row 占比/总收入 37%, body 利润率37%); an unsigned row attests nothing; a row's raw line copied into C
attests nothing by itself. In a draft a metric number absent from B, C and every context-matching signed
derivation is G-NEWNUM hard (was a candidate); dates, small counts, identifiers (the swap test: a unitless number
naming a series or model, S&P 500, Basel 3.1) and a same-unit rounding with 约 of a B/C number stay candidates.
Rewrite is unchanged. Legacy --rows (VERIFIED.jsonl text/value rows, no 'metric') attest their tokens anywhere, as
before. verify and scan run on an empty base; recompute(rows=) uses the same rule; --rows reads a JSON list or JSONL.

Subcommands (standard library only; number tokens come from number_set_diff.py beside this file):
  scan       BASE [--doc FULL_BASE] [--names OUTLINE] [--must-subject TEXT ...] [--json] [--out FILE]
             Sentence ids (s0001…) and, per sentence: number tokens, qualifier / negated-source / 我们假定 markers,
             the arithmetic status (closed, unclosed -> recompute_needed, not_formula; a coincidental a-b=c across a
             separately arranged facility, 另设…, is not a formula) and the holder of every number-bearing clause:
             (1) the clause's own explicit subject (a source adverbial 据X季报… and a source verb X统计/测算 are not
             subjects), else the sentence's subject carried over; (2) for a subjectless sentence, the same value
             (markers dropped, >= 3 significant digits, same unit) in a named clause of the full base, or a frozen
             chart note or appendix table row naming one entity; (3) else keep_subjectless (the writer adds no
             subject), or ambiguous_for_tieout when a --must-subject sentence still has two candidates. With --doc,
             cross-section tensions (same entity, metric and unit, different values in two sections) are listed for
             the tie-out seat only (d5_tensions).
  lint       FINDINGS [--draft FROZEN_DRAFT] [--base B] [--node N] [--mode refuse|warn] [--out FILE]
             [--questions tieout-questions.jsonl] [--json]
             G1 ruling pre-check. Quotes are anchored to the frozen draft under repair. An instruction keeps only the
             target sentence, the rule and allowed form actions (split, merge, delete, move, active voice, a ban on a
             word, the name-table name); replacement prose, direction, causation, certainty, holder and unit
             prescriptions, and numbers the draft does not hold are stripped and routed to the tie-out seat as
             questions; 1.2.0: a tie-out seat's entry (## n（核对席|tie-out|source-check）) keeps a number or
             replacement fix whole when every number the draft lacks is in --base (B/C). Reads both the inline by-node format (### N…, **裁定**, '- | id | open | …' rows, a
             '## 通用裁定' section = F0) and the review-ruling format ('- quote (exact):' / '- fix:' entries).
  recompute  (--sentence S | --file F) [--context C] [--profile draft|rewrite] [--base B] [--rows ROWS] [--json]
             closed | unclosed | not_formula for one sentence, and the authority: rewrite may explain a denominator
             with tokens the base already holds and may add no derived number; draft needs a signed 算式 row.
             --base B (1.2.0): new_tokens, the sentence's value tokens B lacks (an explicit minus kept), and base_ok;
             --rows (1.3.0): derivations attest under the context rule (deriv_mismatch lists the misplaced ones).
  verify     [--base B] --body NEW [--think THINK] [--answer ANSWER] [--profile draft|rewrite] [--doc FULL_BASE]
             [--sources C] [--names OUTLINE] [--before PRE_PATCH --grade B] [--rows ROWS (JSON list or JSONL)]
             [--trace-lines FILE] [--candidates-out must-tieout-candidates.jsonl] [--node N] [--relocation] [--json]
             Clause-level (holder, value + compound unit, operand role, direction, assumption identity) check of
             '## 正文', plus the semantic candidates; '## 思路' slots are checked as diagnostics (they never reject
             and never clear an error in 正文). Verdict PASS, HARD_REJECT or PUBLISH_WITH_CANDIDATES (from 正文
             alone); the 回执's 轨迹： lines split into propagable_trace and quarantined_trace;
             patch grade B: G6 fact recovery first, then U5a (net CJK of the patch <= 0, else retry).
             --base may be omitted in a draft (1.3.0: an empty base, a 0→1 draft whose fact source is --sources).
  release-trace ACCEPTANCE_JSON [--line TEXT ...|--all]
             After the tie-out seat clears a node: move quarantined trace lines back to propagable_trace (atomic,
             under the node lock acceptance/.<node>.lock that apply_node's publication takes).
  --selftest the fixtures (N005 facility, N046 denominator and its legal bridge, N040 bridge, N063 minuend and the
             小计 bypass, N023 3个财月/3次, a 上调/下调 swap, the N000 direction lock, N059 seven variants, 我们假定,
             思路 vs 正文, G1 lint, trace split, U5a, identity; 1.2.0: G-SIGN, rewrite B only, G-PERIOD and its
             trace quarantine, G-RELOC, the tie-out lint exemption, recompute --base, the release-trace lock; 1.3.0:
             the empty-base 0→1 draft, derivations under the context rule, G-DERIV, the draft G-NEWNUM ruling;
             1.3.1: the W4a false positives and their controls; 1.3.2: the core-noun context and its controls).
  1.3.1 (W4a, 2026-11-21) English wording in B/C attests its exact Chinese equivalents (w4a_fact_keys): tenors and
             durations (3-month = 3个月, 30 calendar days = 30天, five business days = 5个工作日 only), counts (25 reporting
             dealers = 25家), month names (July = 7月/七月), the prior day (前一日), both dates (两日); money scaled to the
             Chinese magnitudes in one currency ($64.0tn = 64万亿美元, JPY 96.0tn = 96万亿日元, never 96万亿美元); a
             Markdown table's column-header unit on its cells (($bn) 13.0 = 130亿美元, (bp) +3.4 = 3.4个基点). Clause and
             standard identifiers (Section 301(c), 301(c)条款, Clause 8.2, Article 4(2)) are no value tokens, and a
             phrase ending in a clause word (Under Section) is no entity. 七月 is a date; 一天, 前一日, 两个季度 are small.
  1.3.2 (D8 W4b, 2026-11-21) G-DERIV context by core noun (ctx_terms): a row's metric or denominator also matches
             without its anchors (@甲档:L04, @丙档:L02), currency/unit literals ($80bn, 37%) and parenthetical notes
             （不含…）, and a share metric X占Y的比重 names Y as a denominator; full strings match as before, the share-cue
             test is unchanged, a note's nouns are no denominator, and 利润率37% against a 占比 row still rejects.
             A date or small count that only an unsigned 算式 row holds is a hard G-NEWNUM (a derivation, V26).
Exit: 0 ok (verify: PASS or PUBLISH_WITH_CANDIDATES); 1 verify HARD_REJECT, or a failed self-test; 2 usage.
"""
import argparse
import collections
import difflib
import fcntl
import hashlib
import json
import os
import re
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import number_set_diff as nsd  # noqa: E402

VERSION = '1.3.2'
CJK = re.compile(r'[㐀-䶿一-鿿]')
MARK_RE = re.compile(r'〔[^〔〕\n]{0,80}〕|\[src:[^\]\n]*\]|<!--.*?-->', re.S)
SENT_RE = re.compile(r'[^。！？!?\n]+(?:[。！？!?]+[”’」』"）)]*)?')
DATE_RE = re.compile(r'^[+\-]?(?:约|近|逾)?(?:\d+(?:年|月|日|号)|[QH][1-4]|\d[QH]\d\d|(?:FY|CY)\d+|H[12]|\d{1,2}|20\d\d)$')
MONEY_RE = re.compile(r'(?P<neg>[-−])?\$(?P<a>\d+(?:,\d{3})*(?:\.\d+)?)\s?(?P<ua>bn|mn|tn|k)?'
                      r'(?:\s?[–\-~～至]\s?\$?(?P<b>\d+(?:,\d{3})*(?:\.\d+)?)\s?(?P<ub>bn|mn|tn|k)?)?')
PCT_RE = re.compile(r'(\d+(?:\.\d+)?)\s?%')
MULT = {'bn': 1e3, 'mn': 1.0, 'tn': 1e6, 'k': 1e-3, '': 1e-6, None: 1e-6}

# ------------------------------------------------------------------ word lists
SOFT_Q = ('约', '近', '大致', '左右', '大约')
BOUND_Q = ('而非', '并非', '至多', '最多', '不计', '未含', '未计', '不含', '逾', '不足', '超过', '低于', '以上', '以下')
JUDGE_Q = ('我们判断', '我们推断', '推断', '把握度', '较大可能', '极不可能', '大致对半', 'likely', '我们认为')
ATTR_Q = ('测算', '自算', '粗算', '估算')
SPLIT_Q = ('把握度', 'likely', '大致对半', '较大可能', '极不可能', '我们判断', '测算', '估算', '粗算')
ASSUME_RE = re.compile(r'我们假定|我们假设|(?<!不)假定')        # the rigid identity; a bare 假设 (三档假设) is a noun
DISCLOSE_RE = re.compile(r'公司披露|公司公告|财报显示|季报显示|年报显示|公告显示|披露显示|据[^，。]{0,20}(?:披露|公告|季报|年报)|已披露')
NEG_SOURCE_RE = re.compile(r'公司未提供|未提供(?:这一|此)?指引|并非公司|而非公司|测算而非|未经公司|未披露')
TAG_RE = re.compile(r'把握度[^，。；]{0,6}|（(?:likely|very likely|unlikely|very unlikely|roughly even chance|high|medium|low)[^）]*）'
                    r'|较大可能|极不可能|大致对半')
JUDGE_RE = re.compile(r'(?:我们判断|我们推断|我们认为)[，,：]?')
CONTRAST_RE = re.compile(r'(?:而在|而是|在于|取决于)([^。，；]+)')
CONJ_RE = re.compile(r'与|和|及|以及|、')
MODAL_W = ('唯一', '必然', '必将', '必定', '已定', '注定', '一定会', '无疑', '须', '必须', '只对应', '只属', '只能', '只会', '只由',
           '只在', '最终', '完全', '绝对', '根本')
CAUSAL_W = ('原因是', '原因在于', '导致', '致使', '源于', '决定了', '以致', '归因', '反映', '意味着', '无法据此', '，即')
UP_W = ('上调', '上修', '调高', '提高', '上升', '升至', '增至', '扩大', '走阔', '走高', '抬升', '加息', '上行')
DOWN_W = ('下调', '下修', '调低', '降低', '下降', '降至', '减至', '缩小', '收窄', '走低', '回落', '降息', '下行')
LOCK_RE = re.compile(r'相应改判|均须(?:相应)?改判|须相应调整|相应调整|重新评估|改判(?=[，。；）(（]|$)')
SUB_CUE = re.compile(r'减去|扣除|扣减|抵减|冲抵|减掉|减除|剔除|净额|净垫资|余额为|余下|剩余|相减|差额|−|(?<![A-Za-z])-(?=\s?\$)')
SUM_CUE = re.compile(r'合计|共计|总计|加上|加总|合共|总共|两者之和|之和')
SEP_CUE = re.compile(r'另设|另有|另外|此外|另行|另签|另借|另笔|同时设|单独')
HARD_SUB = re.compile(r'减去|扣除|扣减|减掉|减除|抵减|冲抵|相减')
BACKREF_RE = re.compile(r'(?:上述|前述|以上|这|该)[^，。]{0,16}?(?:合计|总额|总计|两项|二者|两者)')
FORMULA_CUE = re.compile(r'作分母|为分母|分母|占比?|之比|比值|覆盖率|倍数|折合|约合|相当于|粗算|测算|自算|估算|按[^，。]{0,20}计')
SOURCE_VERB = re.compile(r'^(?:统计|测算|估算|估计|预计|认为|报告|披露|指出|测得|称|表示|预测|推算|自算|研报|评级报告|报告称)')
SOURCE_ADV = re.compile(r'^(?:据|根据|按照?|依据|参照)[^，。；]{0,64}?(?:季报|年报|报告|披露|统计|申报|公告|测算|估算|口径|数据|文件|纪要|'
                        r'10-Q|10-K|8-K|S-1(?:/A)?|研报|转述)[^，。；]{0,12}')
CONT_RE = re.compile(r'^(?:其中|同期|此外|另|该|其|并|且|而|同时|期末|截至)')
DEMO_RE = re.compile(r'(这些|这类|该|此类|上述|这批|这笔)([一-鿿A-Za-z]{2,8})')
PRON_RE = re.compile(r'(?:^|[，。；])(?:同期|期末|此时|届时|目前)?(?:其|它|他们|该公司|公司)(?=[^，。；]{0,30}\d)')
METRIC_W = ('现金', '覆盖', '融资', '应收', '贷款', '利差', '杠杆', '债', '收入', '承诺', '额度', '敞口', '缺口', '余额', '估值', '预付',
            '资本开支', '投资', '负债', '利润', '核销', '违约', '订单', '租约', '垫资', '采购', '流动性', '评级', '净值', '份额')
ROLE_W = ('循环信贷协议', '母公司', '增信方', '建设银团', '发起人', '算力商', '芯片商', '云厂', '开发商', '私募信贷', '美联储', '日本银行',
          '欧洲央行', '欧元区银行', '日资三大行', '日资银行', '商业银行', '承租人')
SOURCE_ENT = ('J.P. Morgan', 'Morgan Stanley', 'Goldman Sachs', 'BofA Securities', 'BofA', 'Barclays', 'Fitch', 'S&P',
              "Moody's", 'Bloomberg', 'Reuters', 'UBS', 'Citi', 'IFR', 'BIS')
NOT_ENT = {'AI', 'GPU', 'IG', 'SPV', 'SPE', 'BDC', 'ABS', 'CDS', 'LTC', 'FCF', 'OCF', 'EBITDA', 'OEM', 'ODM', 'TPU', 'HBM',
           'GW', 'MW', 'RVG', 'WALT', 'SLA', 'EoD', 'TL', 'PIK', 'NAV', 'RWA', 'NDFI', 'SRT', 'FY', 'CY', 'Q', 'H', 'S', 'A',
           'B', 'C', 'D', 'I', 'II', 'Form', 'Ex', 'K', 'Inc', 'Corp', 'Ltd', 'LLC', 'L.P', 'pp', 'bp', 'bn', 'mn', 'tn',
           'x', 'E', 'IT', 'GDP', 'DDTL', 'SOFR', 'RPO', 'VIE', 'CMBS', 'CLO', 'LTV', 'DC', 'PE', 'CEO', 'CFO', 'IPO',
           'ETF', 'SEC', 'USD', 'EUR', 'JPY', 'RMB', 'KPI', 'ROE', 'ROA', 'TWh', 'GWh', 'kW', 'NA', 'N', 'M', 'T', 'R',
           'P', 'L', 'X', 'Y', 'Z', 'V', 'F', 'G', 'O', 'U', 'W', 'S-1', 'A-3', 'H.8', 'IG', 'HY', 'US', 'UK', 'EU', 'PO',
           'SOFR', 'XBRL', 'CPI', 'PCE', 'PMI', 'ISM', 'FOMC', 'LBO', 'EV', 'AUM', 'DSCR', 'LTM', 'TTM', 'YoY', 'QoQ'}

# lint (G1)
FORM_ACTION = re.compile(
    r'(?i)\b(?:split|break (?:it|this|the)|divide|merge|combine|join|delete|drop|remove|cut|move|reorder|put (?:it|this|the)'
    r'|lead with|open with|active voice|shorten|trim|unify|keep only one|use the name[- ]table|one sentence per|'
    r'avoid|do not (?:write|use|repeat)|don\'t (?:write|use))\b'
    r'|拆句|拆成|拆为|拆开|分成两句|并句|合并|删去|删除|删掉|去掉|删套话|前移|后移|提到段首|移到|调换|换主动|改主动|主动语态|'
    r'统一名称|换成名字表|不写|不用|别用|勿用|改用名字表')
REPL_CUE = re.compile(r'(?i)(?:replace (?:it |this |them )?(?:with|by)|rewrite (?:it |this )?(?:as|to)|reword|rephrase|'
                      r'\bwrite\b|\bsay\b|restore|insert|\badd\b|change (?:it |this )?to|\buse\b|turn (?:it )?into|read[s]? as|'
                      r'改为|改成|写成|换成|替换为|改写为|写作|补上|补出|补写|补充|加上|添上|恢复为|改作|应为|应写|写明|点明|注明|说明)')
DIR_RX = re.compile(r'(?i)上调|下调|上修|下修|调高|调低|提高|降低|上升|下降|\b(?:raise|lower|upgrade|downgrade|revise (?:up|down)'
                    r'|increase|decrease|higher|lower)\b')
CAUSE_RX = re.compile(r'(?i)原因|导致|由于|因为|所以|因此|致使|源于|\b(?:because|due to|caused?|since|therefore|as a result)\b')
CERT_RX = re.compile(r'(?i)把握度|可能|或将|较大可能|极不可能|大致对半|确定|必然|\b(?:likely|unlikely|certain(?:ty)?|confidence|'
                     r'probab(?:le|ility)|hedge|modal)\b')
HOLDER_RX = re.compile(r'(?i)归属|属于|挂给|挂到|改挂|记在|名下|主体改|\b(?:attribute[sd]? (?:it |this )?to|belongs? to|held by|'
                       r'holder|owner|whose)\b')
UNIT_RX = re.compile(r'(?i)口径|单位|换算|\b(?:unit|basis|denominat\w*|in (?:bn|mn|%|bp))\b')
CONTENT_RX = re.compile(r'(?i)\b(?:replace|rewrite|restore|insert|add|state|give|name both|cite|explain|clarify|spell out)\b'
                        r'|补|加入|写出|给出|交代|说清|讲清')
Q_RE = re.compile(r'[“"「『]([^”"」』\n]{1,200}?)[”"」』]')


# ------------------------------------------------------------------ text units
def clean(text):
    return MARK_RE.sub('', text or '')


def ncjk(s):
    return len(CJK.findall(s or ''))


def norm(s):
    return re.sub(r'[\s*`“”"‘’]', '', s or '')


def paragraphs(text):
    """-> [(kind, text, first line)] kind: prose | table | note | list. Headings, fences, images and blank lines
    end a paragraph and are never one."""
    out, cur, start, fence = [], [], 0, False
    lines = clean(text).replace('\r\n', '\n').split('\n')

    def flush():
        if cur:
            out.append(('prose', ''.join(x.strip() for x in cur), start))
        cur.clear()
    for no, ln in enumerate(lines, 1):
        st = ln.strip()
        if st.startswith('```') or st.startswith('~~~'):
            flush()
            fence = not fence
            continue
        if fence:
            continue
        if not st or st.startswith('#') or st.startswith('!['):
            flush()
            continue
        if st.startswith('|'):
            flush()
            if not re.match(r'^\|?\s*:?-{2,}', st):
                out.append(('table', st, no))
            continue
        if re.match(r'^\*?注[：:]|^资料来源|^\*资料来源|^数据来源', st):
            flush()
            out.append(('note', st, no))
            continue
        if re.match(r'^(?:[-*+]\s|\d{1,2}[.．、]\s?)', st):
            flush()
            out.append(('list', re.sub(r'^(?:[-*+]\s|\d{1,2}[.．、]\s?)', '', st), no))
            continue
        if st.startswith('>'):
            st = st.lstrip('> ').strip()
        if not cur:
            start = no
        cur.append(st)
    flush()
    return out


def split_sentences(text):
    """-> [dict(id, para, idx, kind, text, line)] over prose, list and note paragraphs (table rows: one unit)."""
    out, pi = [], 0
    for kind, para, line in paragraphs(text):
        if kind == 'table':
            out.append({'id': 's%04d' % (len(out) + 1), 'para': pi, 'idx': 0, 'kind': 'table', 'text': para,
                        'line': line})
            pi += 1
            continue
        k = 0
        for m in SENT_RE.finditer(para):
            s = m.group(0).strip()
            if s and (CJK.search(s) or re.search(r'\d', s)):
                out.append({'id': 's%04d' % (len(out) + 1), 'para': pi, 'idx': k, 'kind': kind, 'text': s,
                            'line': line})
                k += 1
        pi += 1
    return out


def split_clauses(s):
    """Clauses of one sentence: split on ，；：,; outside parentheses; -> [(start, text)]."""
    out, depth, buf, start = [], 0, '', 0
    for i, ch in enumerate(s):
        if ch in '（(':
            depth += 1
        elif ch in '）)':
            depth = max(0, depth - 1)
        if ch in '，；：,;' and depth == 0:
            if buf.strip():
                out.append((start, buf))
            buf, start = '', i + 1
            continue
        buf += ch
    if buf.strip():
        out.append((start, buf))
    return out


_SM = difflib.SequenceMatcher(autojunk=False)


def coverage(new, old, min_block=2):
    if not new or not old:
        return 0.0
    _SM.set_seqs(new, old)
    return sum(b.size for b in _SM.get_matching_blocks() if b.size >= min_block) / float(len(new))


# ------------------------------------------------------------------ numbers
_CN_DIG = {'零': 0, '〇': 0, '一': 1, '二': 2, '两': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9}


def cn_int(s):
    """A plain Chinese integer numeral (一 … 九千九百九十九) -> int, else None."""
    if not s or any(ch not in _CN_DIG and ch not in '十百千' for ch in s):
        return None
    total, cur = 0, 0
    for ch in s:
        if ch in _CN_DIG:
            cur = _CN_DIG[ch]
        else:
            mult = {'十': 10, '百': 100, '千': 1000}[ch]
            total += (cur or 1) * mult
            cur = 0
    return total + cur


UNIT_EQ = {'个基点': 'bp', '基点': 'bp', 'bps': 'bp', '个百分点': 'pp', '百分点': 'pp', '倍': 'x'}
USD_SCALE = {'万亿美元': (1e3, 'bn'), '千亿美元': (1e2, 'bn'), '百亿美元': (10.0, 'bn'), '十亿美元': (1.0, 'bn'),
             '亿美元': (0.1, 'bn'), '千万美元': (10.0, 'mn'), '百万美元': (1.0, 'mn'), '万美元': (0.01, 'mn'), '美元': (1.0, '')}
# W4a (C3): the other currencies scale the same way, tagged so that a yen amount never attests a dollar one
# (96万亿日元 = 96000bnJPY = C's JPY 96.0tn; 1,205亿元 = 120.5bnCNY)
_CN_MAG = (('万亿', 1e3, 'bn'), ('千亿', 1e2, 'bn'), ('百亿', 10.0, 'bn'), ('十亿', 1.0, 'bn'), ('亿', 0.1, 'bn'),
           ('千万', 10.0, 'mn'), ('百万', 1.0, 'mn'), ('万', 0.01, 'mn'))
CUR_TAG = (('日元', 'JPY'), ('欧元', 'EUR'), ('英镑', 'GBP'), ('港元', 'HKD'), ('人民币', 'CNY'), ('元', 'CNY'))
for _cn, _tag in CUR_TAG:
    for _mag, _f, _u in _CN_MAG:
        USD_SCALE.setdefault(_mag + _cn, (_f, _u + _tag))


def _num(x):
    return ('%.6f' % x).rstrip('0').rstrip('.')


def vkey(tok):
    """Value key: sign + value + unit with every marker dropped, Chinese integers as digits (三次 -> 3次); W1b: one
    spelling per unit (329个基点 = 329bp, 4.5倍 = 4.5x, 1172亿美元 = 117.2bn, 1美元 = a bare $1)."""
    k = nsd.value_key(tok)
    m = re.match(r'^([+\-]?)([零〇一二两三四五六七八九十百千]+)(.*)$', k)
    if m and '分之' not in k:
        n = cn_int(m.group(2))
        if n is not None:
            k = m.group(1) + str(n) + m.group(3)
    m = re.match(r'^([+\-]?)(\d+(?:\.\d+)?)(.+)$', k)
    if m:
        sign, num, unit = m.group(1), m.group(2), m.group(3).strip()
        if unit in UNIT_EQ:
            return sign + num + UNIT_EQ[unit]
        if unit in USD_SCALE:
            f, u = USD_SCALE[unit]
            return sign + _num(float(num) * f) + u
    return k


def is_date(tok):
    return bool(DATE_RE.match(tok)) or bool(re.fullmatch(r'[QH][1-4]|\d[QH]\d\d|(?:FY|CY)\d{2,4}|H[12]', tok)) \
        or bool(re.fullmatch(r'[+\-]?[一二三四]季度?|[+\-]?[1-4]季度', tok)) \
        or bool(re.fullmatch(r'(?:[一二三四五六七八九十]|十[一二])月份?', tok))      # W4a: 七月 is a date like 7月


REF_AFTER = re.compile(r'^(?:\.\d+)*\s?(?:节|章|部分|条|款|段|小节|期|号文)')
REF_BEFORE = re.compile(r'(?:第|图|表|附录|见|如|Fig\.?\s?|DDTL\s?|Financing\s?)$')
# W4a (C2): clause, section and standard identifiers name an object, never a quantity (Section 301(c), 第301(c)条,
# 301(c)条款, Clause 8.2, Article 4(2), IFRS 9, Pillar-1, Form FR 2004, FR Y-9C, H.4.1); a unitless number only
ID_KW_BEFORE = re.compile(r'(?:(?<![A-Za-z])(?:Section|Sec\.|Sections|Clause|Clauses|Article|Art\.|Articles|Rule|Rules|'
                          r'Regulation|Reg\.|Part|Chapter|Schedule|Annex|Appendix|Exhibit|Item|Form|Pillar|Tier|'
                          r'Basel|IFRS|IAS|ASC|FAS|SFAS|FRS|Title|Paragraph|Para\.|Subpart|Release|Line|Table)'
                          r'\s?-?\s?|§\s?|[A-Za-z]\.(?:\d+\.)*)$')
PAREN_ID_AFTER = re.compile(r'^\s?[（(](?:[a-z]{1,3}|[ivx]{1,4}|\d{1,2})[）)]')


SAME_ONE = re.compile(r'[同单唯统每任某另之]$')      # 同一财季, 单一, 唯一, 每一: no quantity (W1b)


def is_identifier(p, t):
    """W4a (C2): a unitless token named by a clause/section/standard keyword before it, or followed by a (c), (2), (iv)
    sub-clause mark (Section 301(c), 301(c)条款), is an identifier."""
    if t['unit']:
        return False
    return bool(ID_KW_BEFORE.search(p[max(0, t['start'] - 14):t['start']])
                or PAREN_ID_AFTER.match(p[t['end']:t['end'] + 6]))


def value_tokens(s):
    """Number tokens of S that are values (dates, years, periods, bare 1–2 digit integers and section or figure
    references such as 1.1节, 第3.3.1节, 图21 left out; W1b: 一 in 同一, 单一, 唯一, 每一 … left out; W4a: clause and
    standard identifiers such as Section 301(c), 301(c)条款, Clause 8.2 left out)."""
    p = nsd.prep(s)
    return [t for t in nsd.token_spans(s) if not t['period'] and not is_date(t['tok'])
            and not re.fullmatch(r'20\d\d', t['core']) and not REF_AFTER.match(p[t['end']:t['end'] + 4])
            and not REF_BEFORE.search(p[max(0, t['start'] - 10):t['start']])
            and not (t['core'] == '一' and SAME_ONE.search(p[max(0, t['start'] - 1):t['start']]))
            and not is_identifier(p, t)]


SMALL_COUNT = re.compile(r'[+\-]?(?:\d|1[0-2]|[一二两三四五六七八九十])(?:家|个|类|项|次|条|笔|人|位|档|组|处|层|期|台)')


def qty_tokens(s):
    """Value tokens that are quantities (small counts such as 一家, 3类 left out)."""
    return [t for t in value_tokens(s) if not SMALL_COUNT.fullmatch(t['tok'])]


def sig_figs(core):
    d = re.sub(r'[^\d.]', '', core or '')
    if not d:
        return 0
    if '.' in d:
        a, b = d.split('.', 1)
        digits = (a.lstrip('0') + b) if a.strip('0') else b.lstrip('0')
        return len(digits)
    return len(d.strip('0')) if d.strip('0') else 1


def money(s):
    """[(lo $mn, hi $mn, raw, pos)] for every $ amount (a range keeps both ends; a bare first end takes the second
    end's unit: $29–35bn)."""
    out = []
    for m in MONEY_RE.finditer(s or ''):
        ua, ub = m.group('ua'), m.group('ub')
        a = float(m.group('a').replace(',', '')) * MULT[ua or ub or '']
        b = float(m.group('b').replace(',', '')) * MULT[ub or ua or ''] if m.group('b') else a
        sgn = -1.0 if m.group('neg') else 1.0
        out.append((sgn * a, sgn * b, m.group(0), m.start()))
    return out


def half_ulp(raw):
    m = MONEY_RE.match(raw.lstrip()) if raw.lstrip().startswith(('$', '-', '−')) else None
    if not m:
        return 0.5
    dec = len(m.group('a').split('.')[1]) if '.' in m.group('a') else 0
    return 0.5 * (10 ** -dec) * MULT[m.group('ua') or m.group('ub') or '']


# ------------------------------------------------------------------ entities
class Lexicon(object):
    def __init__(self, names, aliases, proper=()):
        self.names = sorted(set(n for n in names if n), key=len, reverse=True)
        self.aliases = aliases          # long form -> canonical short form
        self.proper = set(proper)       # W1b: name-table entities (CJK too) that count as proper names
        self.rx = re.compile('|'.join(re.escape(n) for n in self.names)) if self.names else None
        self._memo = {}

    def canon(self, e):
        return self.aliases.get(e, e)

    def find(self, s):
        """[(pos, canonical entity)] leftmost-longest, non-overlapping, in text order (one compiled alternation,
        longest names first); a Latin name must not run on into Latin letters or digits."""
        if not self.rx or not s:
            return []
        hit = self._memo.get(s)
        if hit is not None:
            return hit
        out, pos = [], 0
        while True:
            m = self.rx.search(s, pos)
            if not m:
                break
            e = m.group(0)
            if e.isascii() and ((m.start() > 0 and s[m.start() - 1].isascii() and s[m.start() - 1].isalnum())
                                or (m.end() < len(s) and s[m.end()].isascii() and s[m.end()].isalnum())):
                pos = m.start() + 1
                continue
            out.append((m.start(), self.canon(e)))
            pos = m.end()
        if len(self._memo) < 200000:
            self._memo[s] = out
        return out


NT_ENT_TAIL = re.compile(r'(?:集团|公司|事业|银行|平台|基金|信托|服务商|交易|发行人|借款人|主体|政府|机构|证券|资本|保险|控股|交投|'
                         r'城投|子公司|Capital|Inc\.?|Corp\.?|LLC|Ltd\.?|Trust|Fund|Bank|Group|Holdings)$')
NT_QUOTE = re.compile(r'[“"「『]([^”"」』\n]{2,40})[”"」』]')
CJK_ALIAS_RE = re.compile(r'(?:^|(?<=[，。；：、\s（(“"]))([一-鿿A-Za-z0-9&·\- ]{2,16}?)（下称([^）\s，。]{1,16})）')


def _nt_cells(ln):
    return [c.strip() for c in ln.strip().strip('|').split('|')]


def _nt_unquote(s):
    return re.sub(r'^[*`“"「『\s]+|[*`”"」』\s]+$', '', s or '')


def _nt_entity(name, desc):
    """A name-table row names an entity (a holder) when the name has a Latin letter, or the name or the tail of its
    指什么 cell (brackets cut) is an organisation word; concept rows (对冲比率, 再融资专项债额度) are not."""
    tail = re.sub(r'[（(][^（）()]*[）)]', '', desc or '').strip(' 。；;，,')
    return bool(re.search(r'[A-Za-z]', name)) or bool(NT_ENT_TAIL.search(name)) or bool(NT_ENT_TAIL.search(tail))


def name_table(text):
    """-> (names, aliases {variant: canonical}, proper) from the first markdown table whose header has a 名字 column
    (W1b; the outline's 名字表). The 名字 cell gives the canonical name (several split at ；／ alias the first); a
    quoted full name in the row (第一次写全称“甲省城投平台”) and a 本篇写法 form that holds the name (主服务商Midland)
    alias it. Entity rows only (_nt_entity); banned forms (不许用) are never aliases. Role words stay non-proper."""
    names, aliases, proper = set(), {}, set()
    lines = (text or '').replace('\r\n', '\n').split('\n')
    for i, ln in enumerate(lines):
        if not ln.strip().startswith('|') or i + 1 >= len(lines):
            continue
        head = _nt_cells(ln)
        ni = next((k for k, c in enumerate(head) if '名字' in c), None)
        if ni is None or not re.match(r'^\s*\|?\s*:?-{2,}', lines[i + 1]):
            continue
        di = next((k for k, c in enumerate(head) if k != ni and ('指什么' in c or '口径' in c or '含义' in c)), None)
        wi = next((k for k, c in enumerate(head) if k != ni and '写法' in c and '不许' not in c), None)
        for ln2 in lines[i + 2:]:
            if not ln2.strip().startswith('|'):
                break
            cells = _nt_cells(ln2)
            if len(cells) <= ni:
                continue
            raw = cells[ni]
            items = [_nt_unquote(x) for x in re.split(r'[；;／/]', re.sub(r'[（(][^（）()]*[）)]', '', raw))]
            items = [x for x in items if len(x) >= 2]
            if not items:
                continue
            canon = items[0]
            desc = cells[di] if di is not None and di < len(cells) else ''
            if not _nt_entity(canon, desc):
                continue
            names.add(canon)
            if canon not in ROLE_W:
                proper.add(canon)
            variants = items[1:] + [q for q in NT_QUOTE.findall(raw + ' ' + desc)]
            if wi is not None and wi < len(cells):
                variants += [_nt_unquote(x) for x in re.split(r'[；;／/、]', cells[wi])]
            for v in variants:
                v = v.strip()
                if len(v) >= 2 and v != canon and v not in NOT_ENT and (canon in v or v in items or v in desc):
                    aliases[v] = canon
                    names.add(v)
        break
    return names, aliases, proper


# W4a (C2): a capitalised phrase ending in a clause word (Under Section, Article) is an identifier, never a holder
ID_PHRASE = re.compile(r'(?:^|\s)(?:Section|Sections|Clause|Clauses|Article|Articles|Rule|Part|Paragraph|Item|'
                       r'Schedule|Annex|Chapter|Appendix|Exhibit|Subpart)$')


def build_lexicon(texts, names_outline=None, extra=()):
    text = '\n'.join(clean(t) for t in texts if t)
    cnt = collections.Counter(m.group(0).strip() for m in re.finditer(
        r"(?<![A-Za-z])[A-Z][A-Za-z&\.\-']*(?:\s(?:[A-Z][A-Za-z&\.\-']*|\d\.\d))*", text))
    names = {e for e in cnt if e not in NOT_ENT and len(e) >= 2 and not re.fullmatch(r'[A-Z]\d*', e)
             and not re.fullmatch(r'[A-Z]{1,2}\d.*', e) and not ID_PHRASE.search(e)}
    aliases, proper = {}, set()
    for m in re.finditer(r'([A-Z][A-Za-z&\.\- ]{1,48}?)（下称([A-Za-z][A-Za-z&\.\-]{1,20})）', text):
        aliases[m.group(1).strip()] = m.group(2)
        names.add(m.group(2))
        names.add(m.group(1).strip())
    nt_names, nt_alias, nt_proper = set(), {}, set()
    if names_outline and os.path.isfile(names_outline):
        try:
            nt_names, nt_alias, nt_proper = name_table(_read(names_outline))
        except (OSError, UnicodeDecodeError):  # a name table is optional
            pass
    names |= nt_names
    aliases.update(nt_alias)
    proper |= nt_proper
    # W1b: CJK 全称（下称简称）: the pair enters only when the short form is a name-table name or an entity word
    for m in CJK_ALIAS_RE.finditer(text):
        long_, short = m.group(1).strip(), m.group(2).strip()
        if long_ == short or short in NOT_ENT or not CJK.search(long_ + short):
            continue
        canon = nt_alias.get(short, short)
        if canon in nt_names or (NT_ENT_TAIL.search(short) and short not in ROLE_W):
            aliases[long_] = canon
            names |= {long_, canon}
            if canon not in ROLE_W:
                proper.add(canon)
    names |= set(ROLE_W) | set(extra)
    return Lexicon(names, aliases, proper)


def strip_source(clause, lex):
    """(clause text with a leading source adverbial cut, the source entities)."""
    m = SOURCE_ADV.match(clause.strip())
    srcs = []
    if m:
        srcs = [e for _p, e in lex.find(m.group(0))]
        clause = clause.strip()[m.end():]
    return clause, srcs


RATING_RE = re.compile(r'^(?:AAA|AA|A|BBB|BB|B|CCC|CC|C|Aaa|Aa|Baa|Ba|Caa|Ca)[+\-]?[123]?$')
LEAD_JUNK = re.compile(r'^(?:\s|[“"（(]|但是|但|而且|而|并且|并|且|同时|此外|另外|其中|另|再|也|还|即|则|因此|所以|由于|如果|若|'
                       r'不过|然而|于是|尽管|虽然|即便|即使|不论|无论|只要|一旦|对于|关于|就|'
                       r'第[一二三四五六七八九十]+|[一二三四五六]是|首先|其次|最后|截至|截止|到|在|于|自|从|'
                       r'\d{4}年(?:\d{1,2}月(?:\d{1,2}日)?)?(?:末|底|初|起|前|后|以来|期间)?|同期|期末|目前|当前|此时|届时|'
                       r'前[一二三四五六七八九十\d]+个?(?:月|季度?)|[一二三四五六七八九十\d]+至[一二三四五六七八九十\d]+月|'
                       r'当季|当期|上半年|下半年|全年|年内|季末|年末|年初|[，、])+')
OBJ_VERB = re.compile(r'约束|压回|覆盖|向|对|给|把|将|为|与|和|及|超过|低于|高于|相当于|占|落后于|短于|长于|高出|低出|镜像|要求|涵盖|'
                      r'包括|含|来自|流向|挂给|归入|计入|由|被|让|替|按|依|经|以|通过|同|比照|参照|仿照|类似|如同|像|看|跟')
PRON_LEAD = re.compile(r'^(?:其|该公司|该行|该集团|该基金|该|公司|这家|它|此|上述公司|本公司|集团)')


def lead_holder(clause, lex):
    """(entity or None, kind) of a clause's subject: kind 'explicit' (a lexicon entity in subject position:
    after connectives and time phrases, before any object-taking verb), 'pronoun' (其, 该公司, 公司 …) or None.
    A source adverbial (据X季报…), a source verb (X统计, X测算) and a credit rating are never the subject."""
    body, srcs = strip_source(clause, lex)
    body = re.sub(r'（[^）]*）|\([^)]*\)', lambda m: ' ' * len(m.group(0)), body)
    j = LEAD_JUNK.match(body)
    head = body[j.end():] if j else body
    if PRON_LEAD.match(head):
        return None, 'pronoun', srcs
    if re.match(r'^(?:我们|我方|本文|作者|笔者)', head):
        return None, 'self', srcs
    for p, e in lex.find(head):
        pre = head[:p]
        after = head[p:].split(e, 1)[-1] if e in head[p:] else head[p + 1:]
        if RATING_RE.match(e):
            continue
        if SOURCE_VERB.match(after.lstrip('于的在 ')) or re.match(r'^(?:估|测|称|指|预计|认为|报告|发布|于\d)', after) \
                or re.search(r'^[^，。；]{0,30}?(?:估算|测算|统计|报告|预计|认为|披露|指出|预测|测得)', after):
            srcs.append(e)
            continue
        if OBJ_VERB.search(pre) or p > 24:
            return None, None, srcs
        rest = head[p + len(e):] if head[p:p + len(e)] == e else ''
        nxt = lex.find(rest[1:20]) if rest.startswith('的') else []
        if nxt and nxt[0][0] == 0 and not RATING_RE.match(nxt[0][1]):
            return nxt[0][1], 'explicit', srcs          # X的Y: the head noun Y is the subject
        return e, 'explicit', srcs
    return None, None, srcs


def clause_holders(clause, lex):
    """Holders of a clause: entities outside parentheses, after a source adverbial, not used as a source (X统计)."""
    body, srcs = strip_source(clause, lex)
    body_np = re.sub(r'（[^）]*）|\([^)]*\)', lambda m: ' ' * len(m.group(0)), body)
    out = []
    for p, e in lex.find(body_np):
        tail = body_np[p + len(e):p + len(e) + 6] if e in body_np[p:p + len(e) + 1] else body_np[p:p + 8]
        after = body_np[p:].split(e, 1)[-1] if e in body_np[p:] else ''
        if e in SOURCE_ENT and SOURCE_VERB.match(after.lstrip('于的在 ')):
            srcs.append(e)
            continue
        if SOURCE_VERB.match(after) or re.match(r'^(?:于\d|于[一-鿿]{0,6}(?:报告|发布))', after):
            srcs.append(e)
            continue
        del tail
        out.append(e)
    return out, srcs


# ------------------------------------------------------------------ binding (scan)
_INDEX_CACHE = {}


def doc_index(doc_text, lex):
    """{value key: {holders}} from explicitly named clauses of the full base, and {numeric core: {holders}} from
    table rows and chart notes (cached per document and lexicon)."""
    key = (sha256_text(doc_text or ''), id(lex))
    if key in _INDEX_CACHE:
        return _INDEX_CACHE[key]
    res = _doc_index(doc_text, lex)
    _INDEX_CACHE[key] = res
    return res


def _doc_index(doc_text, lex):
    by_val, by_core = collections.defaultdict(set), collections.defaultdict(set)
    for s in split_sentences(doc_text or ''):
        if s['kind'] == 'table':
            cells = [c.strip() for c in s['text'].strip('|').split('|')]
            ent = next((lex.find(c)[0][1] for c in cells[:2] if lex.find(c)), None)
            if ent:
                for c in cells:
                    for t in re.findall(r'(?<![\d.])\d+\.\d+(?![\d.])', c):
                        if sig_figs(t) >= 2:
                            by_core[t].add(ent)
            continue
        for _st, cl in split_clauses(s['text']):
            e, kind, _src = lead_holder(cl, lex)
            hs = [e] if e else [x for _p, x in lex.find(cl) if not RATING_RE.match(x)][-1:] if s['kind'] == 'note' else []
            if len(set(hs)) != 1:
                continue
            for t in value_tokens(cl):
                if sig_figs(t['core']) >= 3 and t['unit']:
                    by_val[vkey(t['tok'])].add(hs[0])
            if s['kind'] == 'note':
                for t in value_tokens(cl):
                    if '.' in t['core'] and sig_figs(t['core']) >= 2:
                        (by_val[vkey(t['tok'])] if t['unit'] else by_core[t['core']]).add(hs[0])
        for m in re.finditer(r'([A-Za-z][A-Za-z&.\- ]{0,30}?)(?:的|（)\$?(\d+(?:\.\d+)?)\s?(x|季|倍|%|bn|mn)', s['text']):
            ents = lex.find(m.group(1).strip())
            if ents and sig_figs(m.group(2)) >= 3:
                by_val[vkey(m.group(2) + m.group(3))].add(ents[-1][1])
    return {'val': by_val, 'core': by_core}


def bind_sentences(text, lex, index=None, must=()):
    """Sentence units of TEXT with clause holders and binding: clause | sentence | cross-base | prev-sentence |
    keep_subjectless | ambiguous_for_tieout."""
    units = split_sentences(text)
    prev_holder = {}
    for u in units:
        cls = []
        last = None
        pron = False
        for st, cl in split_clauses(u['text']):
            e, kind, srcs = lead_holder(cl, lex)
            vals = value_tokens(cl)
            hs = [e] if e else []
            h, how = (e, 'clause') if e else (None, None)
            if kind in ('pronoun', 'self'):
                pron = True
                h, how, last = None, kind, 'PRONOUN'
            elif not h and last:
                h, how = (None, 'pronoun') if last == 'PRONOUN' else (last, 'sentence')
            if e:
                last = e
            cls.append({'start': st, 'text': cl, 'holders': hs, 'sources': srcs, 'values': [v['tok'] for v in vals],
                        'holder': h, 'bind': how})
        u['clauses'] = cls
        own = [x for c in cls for x in c['sources']
               if re.search(r'季报|年报|10-Q|10-K|8-K|申报|财报|公告|S-1', c['text']) and _proper(x, lex)]
        if own and not any(c['holders'] for c in cls):
            for c in cls:
                if not c['holder']:
                    c['holder'], c['bind'] = own[0], 'own-filing'
            pron = True
        u['pronoun'] = pron
        named = [e for _p, e in lex.find(u['text']) if not RATING_RE.match(e)
                 and e not in {x for c in cls for x in c['sources']}]
        u['named'] = named
        u['subjectless'] = not any(c['holders'] for c in cls) and not pron and not named
        u['values'] = [v['tok'] for v in value_tokens(u['text'])]
        if u['kind'] == 'table':
            cells = [c.strip() for c in u['text'].strip('|').split('|')]
            ent = next((lex.find(c)[0][1] for c in cells[:2] if lex.find(c)), None)
            for c in cls:
                c['holder'], c['bind'] = (ent, 'table-row') if ent else (None, None)
            u['subjectless'] = not ent
    for u in units:
        if not u['subjectless'] or u['kind'] == 'table':
            if u['kind'] != 'table':
                prev_holder[u['para']] = next((c['holders'][0] for c in u['clauses'] if c['holders']), None)
            continue
        cands = collections.Counter()
        why = []
        if index:
            for c in u['clauses']:
                for t in value_tokens(c['text']):
                    hs = set()
                    if sig_figs(t['core']) >= 3 and t['unit']:
                        hs |= index['val'].get(vkey(t['tok']), set())
                    if '.' in t['core'] and sig_figs(t['core']) >= 2:
                        hs |= index['core'].get(t['core'], set())
                    hs.discard(None)
                    for h in hs:
                        cands[h] += 1
                        why.append('%s->%s' % (t['tok'], h))
        strong = {h for h in cands if len({w.split('->')[0] for w in why if w.endswith('->' + h)}) >= 2}
        if len(cands) == 1 and strong:
            h = next(iter(cands))
            for c in u['clauses']:
                c['holder'], c['bind'] = h, 'cross-base'
            u['binding'] = {'holder': h, 'how': 'cross-base', 'evidence': why[:6]}
        else:
            ph = prev_holder.get(u['para']) if CONT_RE.match(u['text']) else None
            if len(cands) > 1:
                how = 'ambiguous_for_tieout' if any(m and m in u['text'] for m in must) else 'keep_subjectless'
                u['binding'] = {'holder': None, 'how': how, 'candidates': sorted(cands), 'evidence': why[:6]}
            elif ph and u['values']:
                for c in u['clauses']:
                    c['holder'], c['bind'] = ph, 'prev-sentence'
                u['binding'] = {'holder': ph, 'how': 'prev-sentence'}
            else:
                how = 'keep_subjectless'
                if any(m and m in u['text'] for m in must):
                    how = 'ambiguous_for_tieout'
                u['binding'] = {'holder': None, 'how': how if u['values'] else 'no_numbers'}
                for c in u['clauses']:
                    if not c['holder']:
                        c['bind'] = how
        if u['kind'] != 'table' and not u['subjectless']:
            prev_holder[u['para']] = next((c['holders'][0] for c in u['clauses'] if c['holders']), None)
    for u in units:
        if 'binding' not in u:
            h = next((c['holder'] for c in u['clauses'] if c['holder']), None)
            u['binding'] = {'holder': h, 'how': 'clause' if h else ('no_numbers' if not u['values'] else 'keep_subjectless')}
    return units


def markers(s):
    out = []
    for q in SOFT_Q + BOUND_Q + JUDGE_Q + ATTR_Q:
        if q in s:
            out.append(q)
    if ASSUME_RE.search(s):
        out.append('我们假定')
    if NEG_SOURCE_RE.search(s):
        out.append('negated-source')
    return sorted(set(out))


# ------------------------------------------------------------------ arithmetic
def relations(s):
    """[(op, a_raw, b_raw, c_raw)] among the $ amounts of one sentence, exact to the shown precision:
    a - b = c or a + b = c."""
    vals, seen = [], set()
    for lo, hi, raw, _p in money(s):
        if lo == hi and round(lo, 6) not in seen:
            seen.add(round(lo, 6))
            vals.append((lo, raw))
    rel = []
    for i, (a, ra) in enumerate(vals):
        for j, (b, rb) in enumerate(vals):
            if i == j:
                continue
            for k, (c, rc) in enumerate(vals):
                if k in (i, j):
                    continue
                tol = max(half_ulp(ra), half_ulp(rb), half_ulp(rc)) + 1e-9
                if a > b and abs((a - b) - c) <= tol:
                    rel.append(('-', ra, rb, rc))
                if i < j and abs((a + b) - c) <= tol and c > a and c > b:
                    rel.append(('+', ra, rb, rc))
    return rel


def _pos(s, raw):
    return s.find(raw)


def recompute(sentence, context='', profile='rewrite', base_text='', rows=()):
    """-> dict(status closed|unclosed|not_formula, relations, hint, authority). 1.2.0 (F16): with BASE_TEXT, also
    new_tokens (value tokens of the sentence that the base and ROWS lack, an explicit minus kept) and base_ok.
    1.3.0 (W1-0to1): legacy ROWS (text/value) attest their tokens anywhere; a derivation row (with 'metric') attests
    only when signed and in its context (ctx_hit); a value it holds under another metric is listed in deriv_mismatch.
    An empty base with ROWS is a 0→1 draft: every token not attested by a row is new."""
    res = _recompute(sentence, context, profile)
    legacy, drows = split_rows(rows)
    if base_text or rows:
        bvk = signed_keys(clean(base_text)) if base_text else set()
        bvk |= legacy_keys(legacy)
        s = clean(sentence)
        new, mism = [], []
        for t in value_tokens(s):
            if match_key(s, t, bvk)[0] not in ('new', 'minus-added', 'minus-dropped'):
                continue
            dm, drow, said = deriv_attest(s, t, drows)
            if dm == 'ok':
                continue
            new.append(t['tok'])
            if dm == 'mismatch':
                mism.append(deriv_why(drow, said, t))
        res['new_tokens'], res['base_ok'] = new, not new
        if mism:
            res['deriv_mismatch'] = mism
        if new:
            res['authority'] = ('rewrite: %s absent from the base; a rewrite adds no number (V26)' % '、'.join(new)
                                if profile == 'rewrite' else 'draft: %s absent from the base: a new derived number '
                                'needs a signed 算式 row in its context (V26)' % '、'.join(new))
    return res


def _recompute(sentence, context='', profile='rewrite'):
    s = clean(sentence)
    rel = relations(s)
    res = {'status': 'not_formula', 'relations': [], 'hint': '', 'authority': ''}
    good = []
    for op, a, b, c in rel:
        pa, pb, pc = _pos(s, a), _pos(s, b), _pos(s, c)
        seg_bc = s[min(pb, pc):max(pb, pc)]
        seg_ab = s[min(pa, pb):max(pa, pb)]
        if op == '-':
            if SEP_CUE.search(s[min(pa, pb, pc):max(pa, pb, pc) + 1]) and not SUB_CUE.search(s):
                res['coincidental'] = res.get('coincidental', []) + ['%s - %s = %s' % (a, b, c)]
                continue
            if SUB_CUE.search(s) or re.search(r'后|净|余', seg_bc + seg_ab):
                good.append('%s - %s = %s' % (a, b, c))
        elif SUM_CUE.search(s):
            good.append('%s + %s = %s' % (a, b, c))
    if good:
        res.update(status='closed', relations=good)
        return res
    # percent threshold over a literal denominator: R = p x D (literal) or R = p x D / (1 - p) (x / (D + x) = p)
    m = money(s)
    pcts = [float(x) / 100 for x in PCT_RE.findall(s)] or [float(x) / 100 for x in PCT_RE.findall(clean(context))]
    ranges = [(lo, hi, raw) for lo, hi, raw, _p in m]
    for i in range(len(m) - 1):     # two amounts joined by 至/到 (约$117.2bn至总债务约$140bn) are one range too
        gap = s[m[i][3] + len(m[i][2]):m[i + 1][3]]
        if re.fullmatch(r'\s?(?:至|到|–|-|~|～)[^$，。；\d]{0,8}', gap):
            ranges.append((m[i][0], m[i + 1][1], m[i][2] + gap + m[i + 1][2]))
    if FORMULA_CUE.search(s) and pcts and len(ranges) >= 2:
        res['status'] = 'unclosed'
        for p in pcts:
            for i, (dlo, dhi, draw) in enumerate(ranges):
                for j, (rlo, rhi, rraw) in enumerate(ranges):
                    if i == j:
                        continue
                    lit = (p * dlo, p * dhi)
                    if _close(lit, (rlo, rhi)):
                        res.update(status='closed', relations=['%g%% x %s = %s' % (p * 100, draw, rraw)])
                        return res
                    inc = (p * dlo / (1 - p), p * dhi / (1 - p)) if p < 1 else None
                    if inc and _close(inc, (rlo, rhi)):
                        res['hint'] = ('%s is not %g%% of the literal denominator %s (that is %s); it closes as '
                                       'x / (D + x) = %g%%' % (rraw, p * 100, draw, _fmt(lit), p * 100))
        if not res['hint'] and len(ranges) >= 2:
            res['hint'] = 'the stated result does not follow from the literal operands'
    elif FORMULA_CUE.search(s) and len(ranges) >= 3 and SUB_CUE.search(s):
        res['status'] = 'unclosed'
        res['hint'] = 'a subtraction cue with $ amounts that do not close'
    if res['status'] == 'unclosed':
        res['authority'] = ('rewrite: explain the denominator with tokens the base already holds; add no derived number'
                            if profile == 'rewrite' else 'draft: a new derived number needs a signed 算式 row (V26)')
    return res


def _close(x, y, rel_tol=0.03):
    return all(abs(a - b) <= rel_tol * max(abs(b), 1e-9) + 0.051 * 1000 * 0 + 0.5 for a, b in zip(x, y)) and \
        all(abs(a - b) <= max(rel_tol * abs(b), 0.6) for a, b in zip(x, y))


def _fmt(r):
    return '$%.1f–%.1fbn' % (r[0] / 1e3, r[1] / 1e3)


# ------------------------------------------------------------------ scan
def scan(base_text, doc_text=None, lex=None, must=(), node=None):
    base_text = base_text or ''         # 1.3.0: an empty base (a 0→1 draft scans C, 算式 raw lines, 消歧 quotes)
    lex = lex or build_lexicon([doc_text or base_text, base_text])
    index = doc_index(doc_text, lex) if doc_text else None
    units = bind_sentences(base_text, lex, index, must)
    rows = []
    for k, u in enumerate(units):
        ctx = ' '.join(x['text'] for x in units[max(0, k - 2):k] if x['para'] == u['para'])
        rc = recompute(u['text'], ctx)
        row = {'id': u['id'], 'para': u['para'], 'kind': u['kind'], 'text': u['text'], 'values': u['values'],
               'markers': markers(u['text']), 'arith': rc['status'], 'binding': u['binding'],
               'clauses': [{'text': c['text'], 'holder': c['holder'], 'bind': c['bind'], 'values': c['values'],
                            'sources': c['sources']} for c in u['clauses'] if c['values']]}
        if rc['status'] == 'unclosed':
            row['recompute_needed'] = rc['hint']
        if rc.get('coincidental'):
            row['coincidental'] = rc['coincidental']
        if rc['relations']:
            row['relations'] = rc['relations']
        rows.append(row)
    res = {'tool': 'inline_guards.py scan', 'version': VERSION, 'node': node, 'sentences': rows,
           'summary': {'sentences': len(rows), 'with_numbers': sum(1 for r in rows if r['values']),
                       'arith_closed': sum(r['arith'] == 'closed' for r in rows),
                       'recompute_needed': sum('recompute_needed' in r for r in rows),
                       'marked': sum(1 for r in rows if r['markers']),
                       'keep_subjectless': sum(r['binding']['how'] == 'keep_subjectless' for r in rows),
                       'cross_base': sum(r['binding']['how'] == 'cross-base' for r in rows),
                       'ambiguous_for_tieout': sum(r['binding']['how'] == 'ambiguous_for_tieout' for r in rows)}}
    if doc_text:
        res['d5_tensions'] = d5_tensions(doc_text, lex)
    return res


def guard_rows(scan_res, max_rows=40):
    """English guard lines for a writer packet (Chinese only inside quotes)."""
    out = []
    for r in scan_res['sentences']:
        if not r['values'] or r['kind'] == 'table':
            continue
        b = r['binding']
        q = r['text'] if len(r['text']) <= 60 else r['text'][:58] + '…'
        parts = ['- G%s “%s”' % (r['id'][1:], q)]
        if b['how'] in ('clause', 'sentence'):
            parts.append('holder %s' % b['holder'])
        elif b['how'] == 'cross-base':
            parts.append('holder %s (bound from the base elsewhere)' % b['holder'])
        elif b['how'] == 'prev-sentence':
            parts.append('holder probably %s (carried from the sentence before; do not change it)' % b['holder'])
        elif b['how'] in ('keep_subjectless', 'ambiguous_for_tieout'):
            parts.append('no holder in the base: keep it subjectless, add no name-table subject')
        if r['markers']:
            parts.append('keep the markers “%s”' % '、'.join(m for m in r['markers'] if m != 'negated-source')
                         + (' and the negated source' if 'negated-source' in r['markers'] else ''))
        if r.get('recompute_needed'):
            parts.append('recompute needed: do not compute a new number; only name the denominator with numbers '
                         'already in the base')
        if r.get('coincidental'):
            parts.append('separate arrangements: not a subtraction')
        out.append(' | '.join(parts))
        if len(out) >= max_rows:
            break
    return out


def d5_tensions(doc_text, lex, max_groups=200):
    """Same entity + metric word + unit with different values in two different sections (headings): for the tie-out
    seat only. Sections are split on headings; scenario and basis words (情景, 口径, 假设, 区间) drop a pair."""
    sec, cur, out = collections.defaultdict(list), 'head', []
    for ln in (doc_text or '').split('\n'):
        m = re.match(r'^#{1,6}\s+(.*)$', ln)
        if m:
            cur = m.group(1)[:40]
            continue
        sec[cur].append(ln)
    table = collections.defaultdict(list)
    for name, lines in sec.items():
        for u in split_sentences('\n'.join(lines)):
            if u['kind'] == 'table' or re.search(r'情景|口径|假设|区间|敏感性', u['text']):
                continue
            for _st, cl in split_clauses(u['text']):
                hs, _ = clause_holders(cl, lex)
                if len(set(hs)) != 1:
                    continue
                mets = [w for w in METRIC_W if w in cl]
                for t in value_tokens(cl):
                    if not t['unit'] or not mets:
                        continue
                    table[(hs[0], mets[0], t['unit'])].append((name, vkey(t['tok']), cl.strip()[:60]))
    for (e, met, unit), hits in table.items():
        vals = {v for _n, v, _c in hits}
        secs = {n for n, _v, _c in hits}
        if len(vals) > 1 and len(secs) > 1:
            out.append({'entity': e, 'metric': met, 'unit': unit, 'values': sorted(vals)[:6],
                        'sections': sorted(secs)[:4], 'examples': [c for _n, _v, c in hits[:3]]})
        if len(out) >= max_groups:
            break
    return out


# ------------------------------------------------------------------ verify
def align(base_units, new_units):
    bset = {norm(u['text']) for u in base_units}
    rows = []
    for u in new_units:
        r = {'u': u, 'verbatim': norm(u['text']) in bset, 'anchor': None, 'cov': 0.0, 'covs': []}
        if not r['verbatim']:
            covs = sorted(((coverage(norm(u['text']), norm(b['text'])), i) for i, b in enumerate(base_units)),
                          reverse=True)
            r['covs'] = covs[:3]
            if covs and covs[0][0] >= 0.3:
                r['cov'], r['anchor'] = covs[0]
        rows.append(r)
    return rows


def _finding(code, field, sev, u, why, b=None, where='正文', **kw):
    f = {'code': code, 'field': field, 'severity': sev, 'where': where, 'sid': u['id'] if u else None,
         'sentence': u['text'] if u else '', 'why': why}
    if b is not None:
        f['base'] = b['text'] if isinstance(b, dict) else b
    f.update(kw)
    return f


def _dirs(s):
    ups = [w for w in UP_W if w in s]
    downs = [w for w in DOWN_W if w in s]
    return ('up' if ups and not downs else 'down' if downs and not ups else 'mixed' if ups and downs else ''), ups + downs


def _base_holder_for(clause, base_units, lex, e=None):
    """(holder, how, base clause text) of the base clause a new clause rests on: by a shared value first, else by
    coverage with a shared metric word."""
    nv = {vkey(t['tok']) for t in value_tokens(clause) if sig_figs(t['core']) >= 2 or re.search(r'bn|mn|tn', t['unit'])}
    best, best_cov, by_val = None, 0.0, None
    for bu in base_units:
        if bu['kind'] == 'table':
            continue
        for bc in bu['clauses']:
            bv = {vkey(t) for t in bc['values']}
            if nv and nv & bv:
                if e and bc['holder'] and _same_entity(e, bc['holder'], lex):
                    return bc['holder'], bc['bind'] or bu['binding']['how'], bc['text'], bu
                cv = coverage(norm(clause), norm(bc['text']))
                if by_val is None or cv > by_val[2]:
                    by_val = (bc, bu, cv)
            cov = coverage(norm(clause), norm(bc['text']))
            if cov > best_cov:
                best, best_cov = (bc, bu), cov
    if by_val:
        bc, bu, _cv = by_val
        return bc['holder'], bc['bind'] or bu['binding']['how'], bc['text'], bu
    if best and best_cov >= 0.5:
        bc, bu = best
        return bc['holder'], bc['bind'] or bu['binding']['how'], bc['text'], bu
    best_cov = 0.0
    for bu in base_units:
        if bu['kind'] == 'table':
            continue
        for bc in bu['clauses']:
            cov = coverage(norm(_strip_ents(clause, lex)), norm(bc['text']))
            if cov > best_cov:
                best, best_cov = (bc, bu), cov
    if best and (best_cov >= 0.3 or (best_cov >= 0.2 and any(w in clause and w in best[0]['text'] for w in METRIC_W))):
        bc, bu = best
        if bc['values'] or bu['values']:
            return bc['holder'], bc['bind'] or bu['binding']['how'], bc['text'], bu
    return None, None, None, None


def _para_topic(bu, base_units):
    """The last explicit holder named before BU in its base paragraph (the paragraph's topic), or None."""
    out = None
    for x in base_units:
        if x is bu:
            break
        if x['para'] == bu['para'] and x['kind'] != 'table':
            for c in x['clauses']:
                if c['holders']:
                    out = c['holders'][0]
    return out


def _proper(e, lex=None):
    """A proper name (Dell, DFS, J.P. Morgan, DDTL 5.0; W1b: a name-table entity such as H集团 or 平台), not a role
    word (云厂, 私募信贷, 母公司)."""
    if not e or e in ROLE_W:
        return False
    return bool(re.search(r'[A-Za-z]', e)) or bool(lex is not None and e in getattr(lex, 'proper', ()))


def _strip_ents(s, lex):
    for _p, e in lex.find(s):
        s = s.replace(e, '')
    return s


def _same_entity(a, b, lex):
    a, b = lex.canon(a), lex.canon(b)
    return a == b or a in b or b in a


def explicit_sign(text, span):
    """'+' or '-' when SPAN's sign is written as a character in TEXT (a token_spans dict), '' when the token is
    unsigned or its sign is read off a direction word (升至, 下降): 1.2.0, F12. W4c (F03): a 负 right before the
    number (负20亿美元, 负约20亿美元) is an explicit minus, as in number_set_diff; 负增长5% and 负债3亿元 are not."""
    p = nsd.prep(text)
    raw = p[span['start']:span['end']]
    if span.get('mark') and raw.startswith(span['mark']):
        raw = raw[len(span['mark']):]
    raw = raw.lstrip()
    if raw[:1] in '+-' and raw[:1]:
        return raw[:1]
    return '-' if span.get('sign') == '-' and span['start'] >= 1 and p[span['start'] - 1] == '负' else ''


def ambiguous_minus(text, span):
    """True when a minus stands right after a Latin letter before an unsigned token (GDP−0.76%, S-1): the tokenizer
    does not read it as a sign, so the value may be negative or not (1.2.0, F12)."""
    if span.get('sign'):
        return False
    p = nsd.prep(text)
    i = span['start'] + len(span.get('mark') or '')
    return i >= 2 and p[i - 1] == '-' and bool(re.match(r'[A-Za-z]', p[i - 2]))


def signed_keys(text):
    """Value keys of TEXT's numbers for matching (1.2.0, F12): each token's own key, plus its magnitude when its
    sign is a '+' or a direction word's '-' (下降20% matches a bare 20%); an explicit minus (-20亿美元) is part of the
    value and never matches an unsigned or positive 20; an ambiguous minus (GDP−0.76%) gives both keys."""
    out = set()
    for s in nsd.token_spans(text):
        k = vkey(s['tok'])
        out.add(k)
        if k.startswith('+') or (k.startswith('-') and explicit_sign(text, s) != '-'):
            out.add(k[1:])
        elif not k.startswith('-') and ambiguous_minus(text, s):
            out.add('-' + k)
    return out


def match_key(text, span, bvk):
    """-> (status, key) of one token of TEXT against the value keys BVK (signed_keys of the fact source): 'ok' (key
    found, KEY the matching form), 'minus-added' (an explicit minus where the base holds the positive value),
    'minus-dropped' (unsigned or + where the base holds only an explicit minus), 'dir-turned' (a direction word's
    minus where the base holds +value; KEY the magnitude), 'new' (absent). 1.2.0, F12."""
    vk = vkey(span['tok'])
    if vk in bvk:
        return 'ok', vk
    mag = vk.lstrip('+-')
    if ambiguous_minus(text, span) and ('-' + mag in bvk or mag in bvk):
        return 'ok', '-' + mag if '-' + mag in bvk else mag
    if vk.startswith('-') and explicit_sign(text, span) == '-' and (mag in bvk or '+' + mag in bvk):
        return 'minus-added', vk
    if not vk.startswith('-') and mag not in bvk and '-' + mag in bvk:
        return 'minus-dropped', vk
    if mag in bvk:
        return ('dir-turned' if vk.startswith('-') and '+' + mag in bvk else 'ok'), mag
    return 'new', vk


# ------------------------------------------------------------------ derivations (W1-0to1, 1.3.0)
# 算在树上，叶席零新数 (V26). A derivation is a living-outline 算式 row frozen by pack_node: {"id","node","metric",
# "value","denominator","basis","operands":[{"name","value","anchor"}],"expr","signed","raw"}. THE CONTEXT RULE, kept
# here alone (verify and recompute both call ctx_hit / deriv_attest): a signed row attests a body value token that
# matches its value only when the token's clause holds the row's context, that is the row's metric, or its
# denominator together with a share/ratio cue (SHARE_CUE_RE) found outside the denominator itself; when the clause
# names no metric of its own (no cue, no METRIC_KIND word: 2025年为37%), its sentence is read instead. 比 in a
# comparison (同比, 环比, 相比, 对比, 比较, 比上年) and 率 of a growth rate (增长率, 增速率) are not share cues.
SHARE_CUE_RE = re.compile(r'占|之比|比重|比例|比率|比值|(?<![同环相对])比(?![较上去前])|(?<!增长|增速)率|倍|覆盖|份额|相当于'
                          r'|折合')
METRIC_KIND = re.compile(r'增速|增长|增幅|降幅|涨幅|跌幅|利差|杠杆|久期|收益|回报|毛利|净利|利润|估值|市盈|乘数|缺口|盈余|余额'
                         r'|规模|敞口')
SIGNED_WORDS = ('true', 'yes', 'signed', '已签', '是')
# the swap test (O20): a unitless number right after a Latin name or before a series word names an object (S&P 500,
# Basel 3.1, 第5轮): an identifier, never a metric; any unit makes a number a metric, even inside a nickname
ID_BEFORE = re.compile(r'(?:[A-Za-z&][A-Za-z&.]*\s?-?\s?|编号|代码|型号|No\.?\s?|#)$')
ID_AFTER = re.compile(r'^(?:系列|号|型|版|代|批|款|轮|期(?![限间末初内])|档|类|级)')


def split_rows(rows):
    """-> (legacy, derivations). A row with a 'metric' key is a derivation (W1-0to1); the rest are the --rows
    VERIFIED.jsonl tie-out rows (text/value), which attest their value tokens anywhere, as before 1.3.0."""
    leg, der = [], []
    for r in rows or ():
        if isinstance(r, dict):
            (der if 'metric' in r else leg).append(r)
    return leg, der


def legacy_keys(rows):
    return {vkey(t) for r in rows for t in nsd.tokens('%s %s' % (r.get('text') or '', r.get('value') or ''))}


def row_signed(row):
    v = row.get('signed')
    return v is True or (type(v) is int and v == 1) or (isinstance(v, str) and v.strip().lower() in SIGNED_WORDS)


# 1.3.2 (W4b): the core noun of a row's metric or denominator. An outline 算式 row often writes its denominator with
# the operand's value, its anchor and a scope note (合并营业收入80.0亿元@甲档:L12（不含其他业务收入6.0亿元…）),
# which prose never repeats; the core strips anchors (@甲档:L04, @丙档:L02), currency and unit-bearing numeric
# literals ($80bn, 37%, 120亿美元; a bare 2026年 or 3个月 stays) and parenthetical notes （…）/(…), whose nouns are
# no denominator (a 不含… note names what the row excludes). A share metric X占Y的比重 also names Y as a denominator
# noun. The full strings still match as before; the cue test is unchanged, so a different head noun (利润率37% against
# a 占比 row) still fails.
CORE_PAREN = re.compile(r'（[^（）]*）|\([^()]*\)')
CORE_ANCHOR = re.compile(r'@[^\s:：@|｜]+[:：]\s*L\d+(?:\s*[–—\-~～至]+\s*L?\d+)?|@[A-Za-z0-9_.:：\-]+')
_CORE_UNIT = r'(?:bn|tn|mn|k|bps?|pp|%|％|个基点|基点|个百分点|百分点|万亿|亿|万)'
_CORE_CUR = r'(?:美元|日元|欧元|英镑|港元|人民币|元)'
CORE_LIT = re.compile(r'(?:US\$|HK\$|USD|EUR|JPY|GBP|CNY|RMB|[$€¥£])\s?[+\-−]?\d[\d,]*(?:\.\d+)?\s?' + _CORE_UNIT + '?'
                      + _CORE_CUR + r'?(?![A-Za-z])|[+\-−]?\d[\d,]*(?:\.\d+)?\s?(?:' + _CORE_UNIT + _CORE_CUR + '?|'
                      + _CORE_CUR + r')(?![A-Za-z])|(?:US\$|HK\$|[$€¥£])(?!\s?\d)')
SHARE_METRIC = re.compile(r'占(?P<den>.+?)的?(?:比重|比例|占比|份额|之比|比率)$')


def core_term(s):
    """-> S without its anchors, currency/numeric literals and parenthetical notes, normalised; '' when fewer than two
    characters are left (合并营业收入80.0亿元@甲档:L12（不含…） -> 合并营业收入; 占比（折年）@A:L1 -> 占比)."""
    t, prev = str(s or ''), None
    while prev != t:
        prev, t = t, CORE_PAREN.sub('', t)
    t = norm(CORE_LIT.sub('', CORE_ANCHOR.sub('', t)))
    t = re.sub(r'^[的之，,、：:；;｜|]+|[的之，,、：:；;｜|＝=]+$', '', t)
    return t if len(t) >= 2 else ''


# a core that is only a generic metric word names no metric of its own (占比（海外收入/总收入） -> 占比 would let 国内收入占比
# pass): such a core is never matched alone; the full strings still are, as before 1.3.2
GENERIC_CORE = re.compile(r'(?:占比|比重|比例|比率|份额|之比|比值|倍数|增速|增幅|降幅|涨幅|跌幅|增长率?|规模|余额|差额|缺口|合计|总额'
                          r'|总计|余量|净额)')


def ctx_terms(row):
    """-> (metric forms, denominator forms) of ROW: the full strings first (as before 1.3.2), then their cores and the
    Y of a share metric X占Y的比重; a core that is only a generic metric word (GENERIC_CORE) is left out."""
    mets, dens = [], []
    for out, x, core in ((mets, norm(str(row.get('metric') or '')), False), (mets, core_term(row.get('metric')), True),
                         (dens, norm(str(row.get('denominator') or '')), False),
                         (dens, core_term(row.get('denominator')), True)):
        if x and x not in out and not (core and GENERIC_CORE.fullmatch(x)):
            out.append(x)
    m = SHARE_METRIC.search(core_term(row.get('metric')))
    y = core_term(m.group('den')) if m else ''
    if y and y not in dens and not GENERIC_CORE.fullmatch(y):
        dens.append(y)
    return mets, dens


def ctx_hit(text, row):
    """The context rule on one span: TEXT holds ROW's metric, or its denominator with a share/ratio cue outside it
    (1.3.2: either in full or by its core noun, ctx_terms)."""
    t = norm(text)
    mets, dens = ctx_terms(row)
    if any(m in t for m in mets):
        return True
    return any(d in t and SHARE_CUE_RE.search(t.replace(d, '|')) for d in dens)


def _span_clause(p, span):
    for st, cl in split_clauses(p):
        if st <= span['start'] < st + len(cl):
            return st, cl
    return 0, p


def deriv_context(text, span, row):
    """-> (hit, said): the clause of SPAN (else its sentence, when the clause names no metric of its own) against
    ROW's context; SAID is the clause's own wording before the number (利润率) for the finding."""
    p = nsd.prep(text)
    st, cl = _span_clause(p, span)
    if ctx_hit(cl, row):
        return True, ''
    k = span['start'] - st
    own = cl[:k] + ' ' + cl[k + span['end'] - span['start']:]
    said = re.sub(r'[为达是约近的至于在：:\s]+$', '', cl[:k].strip())[-16:] or cl[k + span['end'] - span['start']:].strip()[:16]
    if not (SHARE_CUE_RE.search(own) or METRIC_KIND.search(own)) and ctx_hit(p, row):
        return True, ''
    return False, said or cl.strip()[:16]


def deriv_attest(text, span, drows):
    """-> (status, row, said) for one value token of TEXT against the derivation rows: 'ok' (a signed row whose value
    matches and whose context the clause holds), 'mismatch' (only signed rows out of context: G-DERIV), 'unsigned'
    (only unsigned rows hold the value: they attest nothing), or None (no row holds it)."""
    hits = [r for r in drows or () if match_key(text, span, signed_keys(str(r.get('value') if r.get('value')
                                                                              is not None else '')))[0]
            in ('ok', 'dir-turned')]
    if not hits:
        return None, None, ''
    signed = [r for r in hits if row_signed(r)]
    if not signed:
        return 'unsigned', hits[0], ''
    said = ''
    for r in signed:
        ok, s = deriv_context(text, span, r)
        if ok:
            return 'ok', r, ''
        said = said or s
    return 'mismatch', signed[0], said


def deriv_why(row, said, span):
    den = str(row.get('denominator') or '')
    met = str(row.get('metric') or '')
    ctx = ('metric %s%s' % (met, '/分母 %s' % den if den else '') if met else
           ('分母 %s' % den if den else 'no metric or denominator (its context cannot be checked)'))
    return 'derivation context mismatch: row %s %s, clause says %s (%s)' % (row.get('id') or '?', ctx, said or '?',
                                                                          span['tok'])


def is_metric(text, span):
    """The swap test (O20) on a token that is no date and no small count: a unit makes it a metric; a unitless number
    after a Latin name or before a series word is an identifier."""
    if span['unit']:
        return True
    p = nsd.prep(text)
    return not (ID_BEFORE.search(p[max(0, span['start'] - 12):span['start']])
                or ID_AFTER.match(p[span['end']:span['end'] + 3]))


def rounds_from(span, fact_spans):
    """V26: a same-unit rounding with 约 needs no 算式 row -> the B/C token SPAN rounds (约44亿美元 <- 44.4亿美元)."""
    if nsd.parse_token(span['tok'])['bound'] != 'soft' or not re.fullmatch(r'\d+(?:\.\d+)?', span['core']):
        return None
    dec = len(span['core'].split('.')[1]) if '.' in span['core'] else 0
    v = float(span['core'])
    for o in fact_spans:
        if o['period'] or o['unit'] != span['unit'] or not re.fullmatch(r'\d+(?:\.\d+)?', o['core']):
            continue
        od = len(o['core'].split('.')[1]) if '.' in o['core'] else 0
        if od > dec and abs(float(o['core']) - v) <= 0.5 * 10 ** -dec + 1e-9:
            return o['tok']
    return None


def strip_raw_lines(text, drows):
    """C without the derivations' raw lines: a 算式 row copied into C attests nothing by itself (the row does, in its
    context)."""
    raws = [norm(str(r.get('raw') or '')) for r in drows]
    raws = [x for x in raws if len(x) >= 6]
    if not raws or not text:
        return text
    return '\n'.join(ln for ln in text.split('\n') if not any(x in norm(ln) for x in raws))


# ------------------------------------------------------------------ W4a (Stage-2 hotfix, C1, C3, C4)
# English wording in C attests its exact Chinese equivalents (more keys for base_vk, never a looser match): tenors and
# durations (3-month = 3个月/三个月, 30 calendar days = 30天/30个日历日, five business days = 5个工作日, 3-Year = 3年期),
# counts of named things (the 25 reporting primary dealers = 25家), month names (July = 7月/七月), the prior day (前一日)
# and both dates (两日/两天); English money amounts scaled to the Chinese magnitudes in the same currency ($585bn =
# 5,850亿美元, $64.0tn = 64万亿美元, JPY 96.0tn = 96万亿日元); a Markdown table's column-header unit bound to that
# column's numeric cells (| 20-Year Bond | … | 13.0 | … | +3.4 | under ($bn) and (bp) attests $13.0bn, 3.4bp, 3.4个基点).
EN_NUM = {'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9,
          'ten': 10, 'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14, 'fifteen': 15, 'sixteen': 16,
          'seventeen': 17, 'eighteen': 18, 'nineteen': 19, 'twenty': 20, 'thirty': 30, 'forty': 40, 'fifty': 50,
          'sixty': 60, 'seventy': 70, 'eighty': 80, 'ninety': 90, 'hundred': 100, 'both': 2, 'single': 1}
_EN_N = r'\d+(?:\.\d+)?|' + '|'.join(sorted(EN_NUM, key=len, reverse=True))
TENOR_EN = re.compile(r'(?i)(?<![A-Za-z0-9.])(?P<n>' + _EN_N + r')(?:\s*\(\s*\d+\s*\))?(?:\s*-\s*|\s+)'
                      r'(?:(?P<q>calendar|business|working|trading|banking|consecutive|full|reporting)[\s-]+)?'
                      r'(?P<u>days?|dates?|weeks?|months?|quarters?|years?|yrs?)(?![A-Za-z])')
TENOR_ABBR = re.compile(r'(?<![A-Za-z0-9.])(?P<n>\d+)\s?(?P<u>[YMW])(?![A-Za-z0-9])')
SAME_DAY_EN = re.compile(r'(?i)\b(?:prior|previous|preceding|next|following|same|one|single|a)\s+(?:calendar\s+|business\s+)?day\b')
MONTH_EN = re.compile(r'(?<![A-Za-z])(January|February|March|April|May|June|July|August|September|October|November|'
                      r'December|Jan\.|Feb\.|Mar\.|Apr\.|Jun\.|Jul\.|Aug\.|Sept?\.|Oct\.|Nov\.|Dec\.)(?![A-Za-z])')
MONTH_NO = {m[:3].lower(): k for k, m in enumerate(('jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct',
                                                     'nov', 'dec'), 1)}
COUNT_EN = re.compile(r'(?i)(?<![A-Za-z0-9.$€£¥\-])(?P<n>' + _EN_N + r')(?P<w>(?:\s+[A-Za-z][A-Za-z\-&.]*){1,4})')
COUNT_NOT = re.compile(r'(?i)^(?:bn|mn|tn|k|bp|bps|pp|percent|per|basis|times|x|days?|dates?|weeks?|months?|quarters?|'
                       r'years?|yrs?|hours?|minutes?|of|to|and|or|by|in|on|at|from|for|the|a|an|is|are|was|were|than)$')
COUNT_CN = ('家', '个', '名', '位', '只', '所', '项', '类', '笔', '条', '支', '种', '场', '次', '份')
TENOR_CN = {'day': ('天', '日'), 'date': ('日', '天', '个日期'), 'week': ('周', '个星期', '星期', '个礼拜'),
            'month': ('个月',), 'quarter': ('个季度',), 'year': ('年', '年期', '个年度'), 'yr': ('年', '年期')}
# a qualified day is that kind of day only (five business days = 5个工作日, never 5天); a calendar day or month is also
# the plain one (30 calendar days = 30天, 30个日历日)
TENOR_Q = {('day', 'calendar'): ('天', '日', '个日历日'), ('month', 'calendar'): ('个月', '个日历月'),
           ('day', 'business'): ('个工作日', '工作日'), ('day', 'working'): ('个工作日', '工作日'),
           ('day', 'banking'): ('个工作日', '工作日'), ('day', 'trading'): ('个交易日', '交易日')}
CUR_BEFORE = re.compile(r'(US\$|\$|USD|€|EUR|¥|JPY|£|GBP|HKD|HK\$|CNY|RMB)\s?$')
CUR_CODE = {'US$': '', '$': '', 'USD': '', '€': 'EUR', 'EUR': 'EUR', '¥': 'JPY', 'JPY': 'JPY', '£': 'GBP', 'GBP': 'GBP',
            'HKD': 'HKD', 'HK$': 'HKD', 'CNY': 'CNY', 'RMB': 'CNY'}
EN_MAG = {'bn': 1.0, 'tn': 1e3, 'mn': 1e-3, 'k': 1e-6}
HEAD_UNIT = re.compile(r'[（(]\s*`?\s*(?P<c>US\$|\$|USD|EUR|€|JPY|¥|GBP|£)?\s?(?P<u>bn|mn|tn|bps?|pp|%|x)\s*`?\s*[）)]')
CELL_NUM = re.compile(r'^[+\-−]?\d+(?:[.,]\d+)*$')


def _en_n(s):
    s = s.lower()
    if s in EN_NUM:
        return EN_NUM[s]
    try:
        return float(s) if '.' in s else int(s)
    except ValueError:
        return None


def _keys_of(*texts):
    out = set()
    for t in texts:
        out |= signed_keys(t)
    return out


def money_keys(val, unit, cur, raw=None):
    """Value keys of an English amount VAL UNIT (bn, mn, tn, k) in currency CUR ('' = dollars or unnamed): its own
    spelling RAW+unit, the same unit without trailing zeros (13.0bn = 13bn) and the bn and mn magnitudes the Chinese
    forms reduce to (1 bn = 10 亿, 1 tn = 1 万亿, 1 mn = 100 万)."""
    if unit not in EN_MAG:
        return set()
    bn = val * EN_MAG[unit]
    out = {_num(val) + unit, _num(bn) + 'bn' + cur, _num(bn * 1e3) + 'mn' + cur}
    if raw:
        out.add(raw + unit)
    return out


def table_keys(text):
    """Keys of a Markdown pipe table's numeric cells under a column header that names a unit (rows on lines or folded
    with ⏎)."""
    out = set()
    for block in re.split(r'\n\s*\n', text):
        rows = [r.strip() for r in re.split(r'\n|⏎', block) if r.strip().startswith('|')]
        units = None
        for r in rows:
            cells = [c.strip() for c in r.strip().strip('|').split('|')]
            if all(re.fullmatch(r':?-{2,}:?', c) for c in cells if c):
                continue
            hu = [HEAD_UNIT.search(c) for c in cells]
            if any(hu) and not any(CELL_NUM.match(c.replace('`', '').replace('%', '')) for c in cells):
                units = [(m.group('u'), CUR_CODE.get(m.group('c') or '', '')) if m else None for m in hu]
                continue
            if not units:
                continue
            for j, c in enumerate(cells):
                if j >= len(units) or not units[j]:
                    continue
                v = c.replace('`', '').replace('−', '-').replace(',', '')
                u, cur = units[j]
                if u == '%':
                    v = v.rstrip('%')
                if not CELL_NUM.match(v):
                    continue
                mag = v.lstrip('+-')
                if u in EN_MAG:
                    ks = money_keys(float(mag), u, cur, mag)
                    out |= {'-' + k for k in ks} if v.startswith('-') else ks
                else:
                    uu = 'bp' if u.startswith('bp') else u
                    out |= _keys_of(v + uu, mag + uu)
    return out


def w4a_fact_keys(fact_text):
    """The W4a attestation keys of the fact source FACT_TEXT (added to base_vk; each is an exact equivalent)."""
    t = (fact_text or '').replace('`', '')
    keys = set()
    for m in TENOR_EN.finditer(t):
        n = _en_n(m.group('n'))
        if n is None or n > 10000:
            continue
        u = m.group('u').lower().rstrip('s')
        q = (m.group('q') or '').lower()
        ns = _num(float(n))
        forms = TENOR_Q.get((u, q)) or TENOR_CN.get(u, ())
        keys |= _keys_of(*[ns + f for f in forms])
    for m in TENOR_ABBR.finditer(t):
        keys |= _keys_of(*[m.group('n') + f for f in {'Y': ('年', '年期'), 'M': ('个月',), 'W': ('周',)}[m.group('u')]])
    if SAME_DAY_EN.search(t):
        keys |= _keys_of('1日', '1天')
    for m in MONTH_EN.finditer(t):
        k = MONTH_NO.get(m.group(1)[:3].lower())
        if k:
            keys |= _keys_of('%d月' % k)
    for m in COUNT_EN.finditer(t):
        words = m.group('w').split()
        if not words or COUNT_NOT.match(words[0]) or re.match(r'(?i)^(?:bn|mn|tn|bps?|pp)\b', words[0]):
            continue
        if not any(len(w) > 3 and w.lower().endswith('s') and not COUNT_NOT.match(w) for w in words):
            continue
        n = _en_n(m.group('n'))
        if n is None or isinstance(n, float) or n > 100000 or 1900 <= n <= 2100:  # a year is no count
            continue
        keys |= _keys_of(*['%d%s' % (n, c) for c in COUNT_CN])
    p = nsd.prep(t)
    for s in nsd.token_spans(t):
        if s['unit'] not in EN_MAG or not re.fullmatch(r'\d+(?:\.\d+)?', s['core'] or ''):
            continue
        cm = CUR_BEFORE.search(p[max(0, s['start'] - 5):s['start']])
        cur = CUR_CODE.get(cm.group(1), '') if cm else ''
        ks = money_keys(float(s['core']), s['unit'], cur)
        if s['tok'].startswith('-') or s.get('sign') == '-':
            ks = {'-' + k for k in ks}
        keys |= ks
    keys |= table_keys(t)
    return keys


QUARTER_DATE = re.compile(r'^(?:第)?([一二三四1-4])季度$')
CN_Q = {'一': 1, '二': 2, '三': 3, '四': 4, '1': 1, '2': 2, '3': 3, '4': 4}


def period_key(span, loose=False):
    """A reporting period as a comparable key (1.2.0, F14): 第一财季 / 第1季度 / Q1 / 一季度 -> ('Q', 1), H1 / 上半年
    -> ('H', 1), 3Q25 -> ('Q', 3, '25'), FY2025 / FY25 -> ('FY', '25'); None for anything else. LOOSE also reads a
    bare 三季 (fact side only)."""
    tok = span['tok']
    if span.get('period'):
        m = re.fullmatch(r'Q([1-4])', tok)
        if m:
            return ('Q', int(m.group(1)))
        m = re.fullmatch(r'H([12])', tok)
        if m:
            return ('H', int(m.group(1)))
        m = re.fullmatch(r'([1-4])Q(\d\d)', tok)
        if m:
            return ('Q', int(m.group(1)), m.group(2))
        m = re.fullmatch(r'([1-2])H(\d\d)', tok)
        if m:
            return ('H', int(m.group(1)), m.group(2))
        m = re.fullmatch(r'(FY|CY)(\d{2,4})', tok)
        if m:
            return (m.group(1), m.group(2)[-2:])
        if span.get('core') in CN_Q and span.get('unit') in nsd.ORD_PERIOD_UNITS:
            return ('Q', CN_Q[span['core']])
        return None
    m = QUARTER_DATE.match(tok) or (re.fullmatch(r'([一二三四1-4])季', tok) if loose else None)
    return ('Q', CN_Q[m.group(1)]) if m else None


def period_spans(text, loose=False):
    """[(span, key)] of the reporting periods in TEXT (1.2.0, F14); an ordinal quarter's span tok gets its 第 back."""
    out = []
    for s in nsd.token_spans(text):
        k = period_key(s, loose)
        if k:
            if s.get('period') and s.get('unit') in nsd.ORD_PERIOD_UNITS:
                s = dict(s, tok='第' + s['tok'])
            out.append((s, k))
    return out


def _period_match(k, fact_keys):
    return k in fact_keys or (len(k) == 3 and k[:2] in fact_keys)


TIEOUT_SEAT = re.compile(r'(?i)核对席|核数席|核对|tie-?out|source-?check')
CITE_INNER_SPLIT = re.compile(r'[，,、；;／/]')
ENUM_RE = re.compile(r'[^，。；：、（）()\s]{1,14}(?:、[^，。；：、（）()\s]{1,14})+(?:和|及|与|以及|、)[^，。；：、（）()\s]{1,14}')
ENUM_HEAD = re.compile(r'^.*(?:即|包括|包含|如|含|有|为|是|涵盖|：|:)')
ENUM_TAIL = re.compile(r'(?:都|均|等|各|也|在|的|将|已|受|合计|共|分别|占|是|为|[一二三四五六七八九十两几多]+(?:处|类|项|个|种|条|家|方面|大|重|层|端)).*$')
INST_RE = re.compile(r'(?:穆迪|标普|惠誉|彭博|路透|摩根士丹利|摩根大通|高盛|花旗|瑞银|美银|巴克莱|美联储|财政部|统计局|央行|国际清算银行)'
                     r'|[^\s]{1,10}(?:银行|证券|评级|资本|集团|公司|协会|统计局|研究院|研究所|交易所|委员会|基金会|财政部|央行)$')
ENUM_ITEM_MAX = 8
RELOC_LINE = re.compile(r'开头后移|后移|relocat', re.I)


def _opening_items(s, lex):
    """Attribution and list items of one base opening sentence (1.2.0, F03): the institutions and dates inside a
    parenthetical citation (（穆迪，10月30日）), the entity and date of a 据…报告 source adverbial, and the items of a
    sample list of three or more (BDC、保险、养老金和主权基金) -> [(kind, item)]."""
    out = []
    for m in CITE_RE.finditer(s):
        inner = m.group(1)
        dates = CITE_DATE_RE.findall(inner)
        if inner.startswith(('下称', '即', '见', '以下简称', '简称')) or not (
                dates or any(x in inner for x in SOURCE_ENT) or INST_RE.search(inner)):
            continue        # a citation only (a date or a source name), never an alias or a gloss
        out += [('source', d) for d in dates]
        rest = CITE_DATE_RE.sub('', inner)
        for part in CITE_INNER_SPLIT.split(rest):
            part = part.strip(' 　于在的')
            # an institution only: a lexicon entity, a known source name or an institution word (银行, 证券, 评级 …)
            if 2 <= len(part) <= 16 and not re.search(r'\d', part) and (
                    lex.find(part) or any(x in part for x in SOURCE_ENT) or INST_RE.search(part)):
                out.append(('source', part))
    sa = SOURCE_ADV.match(s)
    if sa:
        adv = sa.group(0)
        out += [('source', e) for _p, e in lex.find(adv)] + [('source', d) for d in CITE_DATE_RE.findall(adv)]
    for m in ENUM_RE.finditer(re.sub(r'（[^（）]*）', '', s)):
        items = re.split(r'、|和|及|与|以及', m.group(0))
        if len(items) < 3:
            continue
        items[0] = ENUM_HEAD.sub('', items[0])
        items[-1] = ENUM_TAIL.sub('', items[-1]) or items[-1]
        items = [norm(x) for x in items]
        # a sample list only: every item short (<= ENUM_ITEM_MAX characters), named, number-free
        if all(2 <= len(x) <= ENUM_ITEM_MAX and not re.search(r'\d', x) for x in items):
            out += [('list', x) for x in items]
    seen, uniq = set(), []
    for k, x in out:
        if norm(x) and norm(x) not in seen:
            seen.add(norm(x))
            uniq.append((k, x))
    return uniq


def _relocation_check(base_units, rws, body, think, relocated, lex, add):
    """G-RELOC (1.2.0, F03): in a rewrite with opening detail relocation on (O73), a source, date or list item of a
    base opening sentence (the first sentence of a base paragraph) that appears nowhere in the rewritten node and is
    not listed in an 开头后移 line (思路, or RELOCATED) is queued as a semantic candidate: a moved item must land in
    its destination, and a kept number keeps its source and date."""
    flat = norm(clean(body))
    moved = norm(' '.join([ln for ln in (think or '').split('\n') if RELOC_LINE.search(ln)] + list(relocated or ())))

    def present(x, where):
        x = norm(x)
        if x in where:
            return True
        need = max(2, len(x) - 1) if len(x) <= 4 else -(-3 * len(x) // 4)
        return difflib.SequenceMatcher(None, x, where, autojunk=False).find_longest_match(
            0, len(x), 0, len(where)).size >= need
    for bu in base_units:
        if bu['idx'] != 0 or bu['kind'] != 'prose':
            continue
        lost = [(k, x) for k, x in _opening_items(bu['text'], lex) if not present(x, flat) and not present(x, moved)]
        if not lost:
            continue
        best = max(rws, key=lambda r: coverage(norm(r['u']['text']), norm(bu['text'])), default=None)
        u = best['u'] if best else {'id': None, 'text': ''}
        f = _finding('G-RELOC', 'attribution' if any(k == 'source' for k, _x in lost) else 'claim', 'candidate', u,
                     'opening detail of the base gone from the whole node, not listed in 开头后移: %s'
                     % '、'.join(x for _k, x in lost[:6]), bu)
        f['class'] = 'semantic'
        add(f)


def verify(base_text, body, think='', profile='rewrite', doc_text=None, sources_text='', lex=None, before=None,
           grade=None, rows=(), trace_lines=(), node=None, must=(), relocation=False, relocated=()):
    # 1.3.0 (W1-0to1): B may be empty or None (a 0→1 draft: C, the derivations and the 消歧 quotes are the source)
    base_text, sources_text, body = base_text or '', sources_text or '', body or ''
    legacy, drows = split_rows(rows)
    sources_text = strip_raw_lines(sources_text, drows)
    lex = lex or build_lexicon([doc_text or base_text, base_text, sources_text])
    index = doc_index(doc_text, lex) if doc_text else None
    # 1.2.0 (F13): a rewrite's only fact source is the frozen base B; C is a fact source of a draft alone
    fact_text = base_text if profile == 'rewrite' else base_text + ('\n\n' + sources_text if sources_text else '')
    base_units = bind_sentences(fact_text, lex, index, must)
    new_units = bind_sentences(body, lex, None)
    rws = align(base_units, new_units)
    # W1b: a base heading's numbers are base numbers (a rewrite restating the heading's 一季以上 adds nothing)
    # 1.2.0 (F12): only '+' and a direction word's sign are dropped for matching; an explicit minus stays
    base_vk = set()
    for u in base_units:
        base_vk |= signed_keys(u['text'])
    for ln in clean(fact_text).split('\n'):
        if ln.lstrip().startswith('#'):
            base_vk |= signed_keys(ln)
    base_vk |= w4a_fact_keys(fact_text)  # W4a: English tenors, counts, months, magnitudes and table units in B/C
    fact_periods = {k for _s, k in period_spans(clean(fact_text), loose=True)}
    row_vk = legacy_keys(legacy)        # legacy tie-out rows: bare values, attested anywhere (as before 1.3.0)
    findings = []
    seen = set()
    fact_spans = [o for o in nsd.token_spans(fact_text) if o['unit'] and not o['period']]

    def add(f):
        key = (f['code'], f['sid'], f['why'][:40], f['where'])
        if key not in seen:
            seen.add(key)
            findings.append(f)

    # V-NUM / unit / bounds
    for r in rws:
        u = r['u']
        if r['verbatim']:
            continue
        cand = [r['anchor']] + [i for c, i in r['covs'] if c >= 0.2 and i != r['anchor']] if r['anchor'] is not None \
            else []
        old_spans = [t for i in cand for t in nsd.token_spans(base_units[i]['text'])]
        anc_spans = nsd.token_spans(base_units[r['anchor']]['text']) if r['anchor'] is not None else []
        old_vk = {vkey(o['tok']) for o in anc_spans}
        new_vk_s = {vkey(x['tok']) for x in nsd.token_spans(u['text'])}
        vt_ok = {(x['start'], x['end']) for x in value_tokens(u['text'])}
        # 1.2.0 (F14): reporting periods (第一财季, 第2季度, Q3, 一季度, FY25, 3Q25, H1) are compared, never skipped
        ups = period_spans(u['text'])
        per_pos = {(s['start'], s['end']) for s, _k in ups}
        nps = [(s, k) for s, k in ups if not _period_match(k, fact_periods)]
        # W4c (F01): the anchored sentence's own quarter is compared first; a quarter named elsewhere in B no longer
        # hides a swap (第一财季 -> 第四财季 while another base sentence names 第四财季)
        aqn = {k[1] for _s, k in period_spans(base_units[r['anchor']]['text'], loose=True) if k[0] == 'Q'} \
            if r['anchor'] is not None else set()
        uqn = {k[1] for _s, k in ups if k[0] == 'Q'}
        if r['anchor'] is not None and r['cov'] >= 0.5 and len(aqn) == 1 and len(uqn) == 1 and aqn != uqn:
            sw = [(s, k) for s, k in ups if k[0] == 'Q']
            add(_finding('G-PERIOD', 'value', 'hard', u, 'reporting period swapped: its base sentence names quarter '
                         '%d, this one %s' % (list(aqn)[0], '、'.join(s['tok'] for s, _k in sw)), base_units[r['anchor']],
                         period_keys=[list(k) for _s, k in sw]))
        elif nps:
            add(_finding('G-PERIOD', 'period', 'candidate', u, 'reporting period absent from the base: %s'
                         % '、'.join(s['tok'] for s, _k in nps), base_units[r['anchor']] if r['anchor'] is not None
                         else None, period_keys=[list(k) for _s, k in nps]))
        for t in nsd.token_spans(u['text']):
            if (t['start'], t['end']) in per_pos:
                continue
            if t['period'] or (t['start'], t['end']) not in vt_ok and not is_date(t['tok']):
                continue
            # 1.2.0 (F12): an explicit minus is part of the value; a sign turned against the base is hard
            st_k, vk = match_key(u['text'], t, base_vk)
            mag = vk.lstrip('+-')
            # W4c (F08): when the anchored base sentence holds this magnitude, its sign is checked there first; the
            # same number with the other sign elsewhere in B no longer passes it (净流入20亿美元 -> -20亿美元 while
            # another base sentence holds 投资收益为-20亿美元)
            if r['anchor'] is not None and st_k not in ('minus-added', 'minus-dropped'):
                anc_k = signed_keys(base_units[r['anchor']]['text'])
                if mag in {x.lstrip('+-') for x in anc_k}:
                    st_a, vk_a = match_key(u['text'], t, anc_k)
                    if st_a in ('minus-added', 'minus-dropped'):
                        st_k, vk = st_a, vk_a
                        mag = vk.lstrip('+-')
            # W4c (F05): an ambiguous minus after a Latin letter (PPI−2.8%) still matches either sign, but against a
            # base sentence that holds only the unsigned or rising value it is queued for the tie-out seat
            if st_k == 'ok' and r['anchor'] is not None and ambiguous_minus(u['text'], t):
                anc_t = base_units[r['anchor']]['text']
                same = [o for o in nsd.token_spans(anc_t) if vkey(o['tok']).lstrip('+-') == mag]
                if same and all(not vkey(o['tok']).startswith('-') and not ambiguous_minus(anc_t, o) for o in same):
                    f = _finding('G-SIGN', 'claim', 'candidate', u, 'a minus after a Latin letter (%s) may read as a '
                                 'sign; the base sentence holds %s (unsigned or a rise)' % (t['tok'], '/'.join(
                                     o['tok'] for o in same)), base_units[r['anchor']], tokens=[t['tok']])
                    f['class'] = 'semantic'
                    add(f)
            if st_k == 'minus-added':
                add(_finding('G-SIGN', 'value', 'hard', u, 'sign turned: the base holds %s, this sentence writes an '
                             'explicit minus (%s)' % (mag, t['tok']), base_units[cand[0]] if cand else None,
                             tokens=[t['tok']]))
                continue
            if st_k == 'minus-dropped':
                add(_finding('G-SIGN', 'value', 'hard', u, 'sign turned: the base holds -%s (an explicit minus), this '
                             'sentence %s' % (mag, t['tok']), base_units[cand[0]] if cand else None, tokens=[t['tok']]))
                continue
            if st_k == 'dir-turned':
                add(_finding('G-SIGN', 'direction', 'candidate', u, 'a direction word turns %s negative; the base reads '
                             'it as a rise (+%s)' % (t['tok'], mag), base_units[cand[0]] if cand else None,
                             tokens=[t['tok']]))
            shift = [o for o in anc_spans if o['core'] == t['core'] and o['unit'] and t['unit'] and o['unit'] != t['unit']
                     and vk not in old_vk and vkey(o['tok']) not in new_vk_s and not o['period']
                     and _unit_family(o['unit']) == _unit_family(t['unit']) and not re.fullmatch(r'20\d\d', t['core'])
                     and not is_date(o['tok']) and not is_date(t['tok'])]
            if shift:
                add(_finding('G-UNIT', 'value', 'hard', u, 'unit shift: %s -> %s (same value, unit changed)'
                             % (shift[0]['tok'], t['tok']), base_units[cand[0]] if cand else None))
                continue
            if vk in base_vk:
                # bound kept? a hard bound turned or dropped
                same = [o for o in old_spans if vkey(o['tok']) == vk]
                pb = nsd.parse_token(t['tok'])['bound']
                obs = {nsd.parse_token(o['tok'])['bound'] for o in same}
                if same and obs and pb not in obs:
                    if {'lower', 'upper'} & obs and pb in ('lower', 'upper'):
                        add(_finding('G-BOUND', 'value', 'hard', u, 'bound turned: %s in the base, %s here'
                                     % ('/'.join(o['tok'] for o in same), t['tok']), base_units[cand[0]]))
                    elif {'lower', 'upper'} & obs and not pb:
                        add(_finding('G-BOUND', 'value', 'candidate', u, 'hard bound dropped: %s in the base, %s here'
                                     % ('/'.join(o['tok'] for o in same), t['tok']), base_units[cand[0]]))
                continue
            # 1.3.0: a legacy row matches as recompute matches it (a direction word's sign dropped: 增长15% = 15%)
            if vk in row_vk or (row_vk and match_key(u['text'], t, row_vk)[0] == 'ok'):
                continue
            # 1.3.0 (W1-0to1): a derivation attests its value only signed and in its context (ctx_hit)
            dm, drow, said = deriv_attest(u['text'], t, drows)
            if dm == 'ok':
                continue
            if dm == 'mismatch':
                add(_finding('G-DERIV', 'value', 'hard', u, deriv_why(drow, said, t), drow.get('raw') or None,
                             tokens=[t['tok']], row=drow.get('id')))
                continue
            unsigned = (' (only the unsigned derivation row %s holds it; an unsigned row attests nothing)'
                        % (drow.get('id') or '?')) if dm == 'unsigned' else ''
            same_core = [o for o in old_spans if o['core'] == t['core'] and o['unit'] != t['unit'] and o['unit']
                         and t['unit'] and not o['period'] and not is_date(o['tok'])]
            if not same_core:
                same_core = [o for o in fact_spans if o['core'] == t['core'] and o['unit']
                             and t['unit'] and o['unit'] != t['unit'] and not o['period'] and not is_date(o['tok'])
                             and _unit_family(o['unit']) == _unit_family(t['unit']) and len(t['core']) >= 1
                             and r['anchor'] is not None]
            if same_core:
                add(_finding('G-UNIT', 'value', 'hard', u, 'unit shift: %s -> %s (same value, unit changed)'
                             % (same_core[0]['tok'], t['tok']), base_units[cand[0]] if cand else None))
                continue
            # W4a: one day, week, month, quarter or year (一天, 前一日, 一年内) and a count of quarters (两个季度) are small
            small = re.fullmatch(r'[+\-]?(?:(?:\d|1[0-2])(?:家|个|类|项|次|条|笔|人|位|档|组|处|层|期|个季度)'
                                 r'|1(?:天|日|周|个星期|个月|年|季度))', vkey(t['tok']))
            if (dm == 'unsigned' and profile != 'rewrite' and (is_date(t['tok']) or small)
                    and norm(str(drow.get('value') or '')) and norm(str(drow.get('value'))) in norm(u['text'])):
                # W4b (1.3.2): a date or small count of a sentence that writes an unsigned 算式 row's whole value (a
                # sum of counts, a date roll-forward: V26) is a derivation, never a casual date or count: hard (a part
                # of the value alone, as 2027年 of 2027年3月31日, and identifiers or 约 roundings keep their own paths)
                add(_finding('G-NEWNUM', 'value', 'hard', u, 'derived number with no signed 算式 row (draft: 算在树上，'
                             '叶席零新数, V26): %s%s' % (t['tok'], unsigned)))
            elif is_date(t['tok']) or small:
                add(_finding('G-NEWNUM', 'value', 'candidate', u, 'date or small count absent from the base: %s%s'
                             % (t['tok'], unsigned)))
            elif profile == 'rewrite':
                add(_finding('G-NEWNUM', 'value', 'hard', u, 'number token absent from the base (a rewrite adds no '
                             'number, V26): %s%s' % (t['tok'], unsigned)))
            elif not is_metric(u['text'], t):
                add(_finding('G-NEWNUM', 'value', 'candidate', u, 'identifier absent from B and C (no metric by the '
                             'swap test): %s' % t['tok']))
            elif rounds_from(t, fact_spans):
                add(_finding('G-NEWNUM', 'value', 'candidate', u, 'same-unit rounding with 约 of %s in B/C (V26: no '
                             '算式 row needed; tie-out confirms): %s' % (rounds_from(t, fact_spans), t['tok'])))
            else:
                # 1.3.0 (W1-0to1, V26 算在树上，叶席零新数): a draft's unattested metric number is hard (was a candidate)
                add(_finding('G-NEWNUM', 'value', 'hard', u, 'metric number absent from B, C and every signed '
                             'derivation in its context (draft: 算在树上，叶席零新数, V26): %s%s' % (t['tok'], unsigned)))
    # holder (clause level)
    for r in rws:
        u = r['u']
        if r['verbatim'] or u['kind'] == 'table':
            continue
        for c in u['clauses']:
            if not qty_tokens(c['text']) or not (c['holders'] or c['bind'] == 'sentence'):
                continue
            e = c['holders'][0] if c['holders'] else c['holder']
            inherited = not c['holders']
            h, how, btxt, bu = _base_holder_for(c['text'], base_units, lex, e)
            if btxt is None:
                continue
            if h and _same_entity(e, h, lex):
                continue
            if how == 'own-filing':
                add(_finding('G-HOLDER', 'holder', 'candidate', u, 'holder %s here; the base reads it from %s\'s own '
                             'filing' % (e, h), btxt))
                continue
            strong = how in ('clause', 'cross-base', 'table-row') and _proper(e, lex) and _proper(h, lex)
            if btxt and e in btxt:
                continue
            if h and strong and not inherited and not any(_same_entity(h, x, lex) for _p, x in lex.find(u['text'])):
                add(_finding('G-HOLDER', 'holder', 'hard', u, 'holder %s here, the base binds this quantity to %s (%s)'
                             % (e, h, how), btxt))
            elif h:
                add(_finding('G-HOLDER', 'holder', 'candidate', u, 'holder %s here%s, the base has %s (%s)'
                             % (e, ' (carried over)' if inherited else '', h, how), btxt))
            elif bu and bu['subjectless'] and how in ('keep_subjectless', None) and not inherited:
                topic = _para_topic(bu, base_units)
                if topic and _same_entity(e, topic, lex):
                    add(_finding('G-HOLDER', 'holder', 'candidate', u, 'subject %s added to a subjectless base quantity; '
                                 'it is the base paragraph\'s named topic (tie-out confirms)' % e, btxt))
                elif profile == 'rewrite' and _proper(e, lex):
                    add(_finding('G-HOLDER', 'holder', 'hard', u, 'a name-table subject %s is attached to a quantity '
                                 'whose base sentence is subjectless and unverified (keep it subjectless)' % e, btxt))
                else:
                    add(_finding('G-HOLDER', 'holder', 'candidate', u, 'subject %s added to a subjectless base '
                                 'quantity' % e, btxt))
            elif how in ('pronoun', 'ambiguous_for_tieout') and not inherited:
                add(_finding('G-HOLDER', 'holder', 'candidate', u, 'subject %s resolves a base %s: check it'
                             % (e, 'pronoun' if how == 'pronoun' else 'ambiguous subject'), btxt))
        for m in PRON_RE.finditer(u['text']):
            if r['anchor'] is not None and m.group(0).strip('，。；') not in base_units[r['anchor']]['text']:
                add(_finding('G-REF', 'holder', 'candidate', u, 'pronoun “%s” before a quantity: check its referent'
                             % m.group(0).strip('，。；')))
        if r['anchor'] is not None:
            b = base_units[r['anchor']]['text']
            for m in DEMO_RE.finditer(u['text']):
                noun = m.group(2)[:4]
                fresh = m.group(0)[:len(m.group(1)) + 2] not in fact_text and m.group(1) in ('这些', '这类', '此类', '上述')
                if (noun in b or fresh) and m.group(1) not in b and \
                        not re.search('(这些|这类|该|此类|上述|这批|这笔)' + re.escape(noun), b):
                    add(_finding('G-REF', 'holder', 'candidate', u, 'demonstrative “%s” newly put before “%s”: check '
                                 'the referent' % (m.group(1), noun), b))
                    break
    # entity attachment shift (old D6) as a candidate
    for r in rws:
        u = r['u']
        if r['verbatim'] or r['anchor'] is None:
            continue
        b = base_units[r['anchor']]['text']
        bcl = [x for _s, x in split_clauses(b)]
        for _s, c in split_clauses(u['text']):
            co = re.sub(r'（[^）]*）', '', c)
            ec = {e for _p, e in lex.find(co)}
            if not ec:
                continue
            best = max(bcl, key=lambda x: coverage(c, x)) if bcl else ''
            if coverage(c, best) < 0.45:
                continue
            eb = {e for _p, e in lex.find(re.sub(r'（[^）]*）', '', best))}
            newe = [e for e in ec - eb if not any(_same_entity(e, x, lex) for x in eb)]
            if newe and eb and not re.search(r'公司|^其|，其|该|它', best):
                add(_finding('G-HOLDER', 'holder', 'candidate', u, 'entity %s now attached in a clause whose base '
                             'names %s' % ('、'.join(newe), '、'.join(sorted(eb))), b))
                break
    # direction
    base_has_dir = {w for w in UP_W + DOWN_W if w in fact_text}
    for r in rws:
        u = r['u']
        if r['verbatim']:
            continue
        d, words = _dirs(u['text'])
        if not words:
            continue
        b = base_units[r['anchor']] if r['anchor'] is not None else None
        locked = []
        for bu in base_units:
            for _s0, bc in split_clauses(bu['text']):
                if LOCK_RE.search(bc) and not _dirs(bc)[1]:
                    for _s1, nc in split_clauses(u['text']):
                        if _dirs(nc)[1] and coverage(norm(nc), norm(bc)) >= 0.3:
                            locked.append(bc)
        if locked:
            add(_finding('G-DIR', 'direction', 'hard', u, 'direction “%s” added where the base locks the direction '
                         'empty (“%s”)' % ('、'.join(words), locked[0].strip()[:40]), locked[0]))
            continue
        for _s, c in split_clauses(u['text']):
            cd, cw = _dirs(c)
            ce = [e for _p, e in lex.find(c)]
            if not cd or cd == 'mixed' or not ce:
                continue
            opp = []
            same = False
            for bu in base_units:
                for _s2, bc in split_clauses(bu['text']):
                    bd, _bw = _dirs(bc)
                    be = [e for _p, e in lex.find(bc)]
                    if not bd or bd == 'mixed' or not be or not _same_entity(ce[0], be[0], lex):
                        continue
                    if coverage(norm(_strip_ents(c, lex)), norm(_strip_ents(bc, lex))) < 0.3:
                        continue
                    if bd == cd:
                        same = True
                    else:
                        opp.append(bc)
            if opp and not same:
                add(_finding('G-DIR', 'direction', 'hard', u, 'direction of %s turned: the base says “%s”'
                             % (ce[0], opp[0].strip()[:40]), opp[0]))
        new_words = [w for w in words if w not in base_has_dir or (b and w not in b['text'] and
                                                                   fact_text.count(w) < body.count(w))]
        if new_words and not any(f['sid'] == u['id'] and f['code'] == 'G-DIR' for f in findings):
            add(_finding('G-DIR', 'direction', 'candidate', u, 'direction word “%s” added' % '、'.join(new_words), b))
    # arithmetic: operand roles
    for k, r in enumerate(rws):
        u = r['u']
        if r['verbatim']:
            continue
        mv = money(u['text'])
        if not mv:
            continue
        raws_new = {x[2].strip() for x in mv}
        for bu in base_units:
            for op, a, bb, c in relations(bu['text']):
                if op != '-' or c not in u['text']:
                    continue
                rc = recompute(bu['text'])
                if rc['status'] != 'closed':
                    continue
                if bb not in u['text']:
                    continue
                if a in u['text']:
                    continue
                # the minuend: a back-reference to a total in the sentence before, or a wrong amount
                prev = ' '.join(x['u']['text'] for x in rws[max(0, k - 2):k])
                if BACKREF_RE.search(u['text']) and (a in prev or a in u['text']):
                    continue
                if BACKREF_RE.search(u['text']) and a in bu['text'] and any(a in x['u']['text'] for x in rws[:k]):
                    continue
                cue = HARD_SUB.search(u['text'])
                others = [x for x in raws_new if x not in (bb, c) and cue and u['text'].find(x) < cue.start()]
                if others:
                    lo = [x for x in mv if x[2].strip() == others[0]][0][0]
                    add(_finding('G-ARITH', 'operand_role', 'hard', u, 'wrong minuend: the base computes %s - %s = %s; '
                                 'here %s stands in the minuend place (%s - %s does not give %s)'
                                 % (a, bb, c, others[0], others[0], bb, c), bu, relation=[a, '-', bb, c],
                                 value=lo))
                else:
                    add(_finding('G-ARITH', 'operand_role', 'candidate', u, 'states %s with %s but without the base '
                                 'minuend %s' % (c, bb, a), bu))
        rc = recompute(u['text'], ' '.join(x['u']['text'] for x in rws[max(0, k - 2):k]), profile)
        if rc['status'] == 'unclosed' and r['anchor'] is not None:
            brc = recompute(base_units[r['anchor']]['text'])
            if brc['status'] == 'closed':
                add(_finding('G-ARITH', 'operand_role', 'hard', u, 'the base sentence closes (%s); this one does not: %s'
                             % ('; '.join(brc['relations']), rc['hint']), base_units[r['anchor']]))
    # qualifiers, attribution, assumption identity
    _qualifiers(rws, base_units, fact_text, body, add)
    na, nb = len(ASSUME_RE.findall(body)), len(ASSUME_RE.findall(fact_text))
    if nb > na:
        lost = [bu for bu in base_units if ASSUME_RE.search(bu['text'])]
        for bu in lost:
            best = max((x for x in rws if not x['verbatim']), key=lambda x: coverage(norm(bu['text']), norm(x['u']['text'])),
                       default=None)
            if best and coverage(norm(bu['text']), norm(best['u']['text'])) >= 0.3 \
                    and not ASSUME_RE.search(best['u']['text']):
                why = 'assumption identity lost: the base says “%s”' % ASSUME_RE.search(bu['text']).group(0)
                if DISCLOSE_RE.search(best['u']['text']):
                    why += '; this sentence presents it as disclosed'
                add(_finding('G-ASSUME', 'assumption_identity', 'hard', best['u'], why, bu))
    for r in rws:
        if not r['verbatim'] and r['anchor'] is not None and ASSUME_RE.search(base_units[r['anchor']]['text']) \
                and DISCLOSE_RE.search(r['u']['text']) and not ASSUME_RE.search(r['u']['text']):
            add(_finding('G-ASSUME', 'assumption_identity', 'hard', r['u'], 'an assumption (我们假定) rewritten as a '
                         'disclosure', base_units[r['anchor']]))
    # modal / causal additions
    for kind, words in (('modal', MODAL_W), ('causal/link', CAUSAL_W)):
        for w in words:
            if body.count(w) <= fact_text.count(w):
                continue
            for r in rws:
                if r['verbatim'] or w not in r['u']['text']:
                    continue
                if w == '须' and any(x in r['u']['text'] for x in ('必须', '无须', '须知')):
                    continue
                if r['anchor'] is not None and w in base_units[r['anchor']]['text']:
                    continue
                add(_finding('G-MODAL' if kind == 'modal' else 'G-CAUSAL', 'certainty' if kind == 'modal' else
                             'causation', 'candidate', r['u'], '%s word “%s” added' % (kind, w.strip('，'))))
    # W1b semantic candidates: new claims, modal / trajectory words, citation dates, 前者／后者 antecedents
    _semantic(rws, base_units, fact_text, add, lex, findings)
    if profile == 'rewrite' and relocation:
        _relocation_check(base_units, rws, body, think, relocated, lex, add)
    # 思路 slots (W1b): diagnostics only; they never reject, never clear a 正文 finding, never quarantine a trace line
    diags = []
    for f in _think_check(think, base_units, lex):
        f['would_be'], f['severity'] = f['severity'], 'diagnostic'
        diags.append(f)
    hard = [f for f in findings if f['severity'] == 'hard']
    cands = [f for f in findings if f['severity'] == 'candidate']
    res = {'tool': 'inline_guards.py verify', 'version': VERSION, 'node': node, 'profile': profile,
           'verdict': 'HARD_REJECT' if hard else ('PUBLISH_WITH_CANDIDATES' if cands else 'PASS'),
           'hard': hard, 'candidates': cands, 'diagnostics': diags, 'sentences': len(new_units),
           'verbatim': sum(1 for r in rws if r['verbatim'])}
    if before is not None and grade:
        res['u5a'] = u5a(before, body, fact_text, grade)
        if not res['u5a']['ok']:
            res['retry'] = [{'code': 'U5a', 'field': 'length', 'severity': 'retry',
                             'why': 'B-grade patch grew by %d CJK net of %d recovered (U5a: <= 0)'
                                    % (res['u5a']['net_cjk'], res['u5a']['recovered_cjk'])}]
    pt, qt = split_trace(trace_lines, findings, lex)
    res['propagable_trace'], res['quarantined_trace'] = pt, qt
    return res


def _marker_covers(s, q, t):
    """True when marker Q covers token T in base sentence S: Q before T, or Q in T's clause."""
    ps = nsd.prep(s)
    k = ps.find(q)
    spans = [x for x in nsd.token_spans(s) if x['tok'] == t['tok']]
    if k < 0 or not spans:
        return False
    if k < spans[0]['start']:
        return True
    for st, cl in split_clauses(ps):
        if st <= spans[0]['start'] < st + len(cl) + 1 and q in cl:
            return True
    return False


def _unit_family(u):
    if re.search(r'月|季|年|日|周|天|次|小时', u or ''):
        return 'time-count'
    if re.search(r'%|bp|pp|点', u or ''):
        return 'ratio'
    if re.search(r'bn|mn|tn|元|亿|万', u or ''):
        return 'money'
    return u


def _qualifiers(rws, base_units, fact_text, body, add):
    frag = collections.defaultdict(list)
    for r in rws:
        if not r['verbatim'] and r['anchor'] is not None:
            frag[r['anchor']].append(r)
    for bi, bu in enumerate(base_units):
        fr = frag.get(bi, [])
        if not fr:
            continue
        b = bu['text']
        bt = nsd.prep(b)
        bspans = value_tokens(b)
        for q in SPLIT_Q:
            if q not in b:
                continue
            qpos = bt.find(q)
            scoped = [t for t in bspans if (t['start'] > qpos if q in ('我们判断', '我们推断', '推断') + ATTR_Q else True)]
            for r in fr:
                if q in r['u']['text']:
                    continue
                carried = [t['tok'] for t in scoped if t['tok'] in nsd.tokens(r['u']['text'])]
                judged = q in JUDGE_Q and len(fr) >= 2 and any(q in x['u']['text'] for x in fr) \
                    and coverage(r['u']['text'], b) >= 0.6
                if (carried and q != '我们判断') or judged:
                    sib = next((x['u']['text'] for x in fr if q in x['u']['text']), None)
                    add(_finding('G-QUAL', 'qualifier', 'candidate', r['u'], 'marker %s of the base sentence is not on '
                                 'this fragment%s' % (q, (' (carries %s)' % '、'.join(carried[:3])) if carried else
                                                      ' (judged claim split off)'), bu, pair=sib, tokens=carried[:6]))
        for q in ('而非', '并非', '至多', '最多', '不计', '未含', '未计', '不含'):
            if q not in b:
                continue
            for t in bspans:
                cl = next((c for st, c in split_clauses(bt) if st <= t['start'] < st + len(c) + 1), bt)
                if q not in cl:
                    continue
                for r in fr:
                    rt = nsd.prep(r['u']['text'])
                    if t['tok'] in nsd.tokens(r['u']['text']):
                        rc = next((c for st, c in split_clauses(rt) if t['core'] in c), rt)
                        if q not in rc:
                            add(_finding('G-QUAL', 'qualifier', 'candidate', r['u'], 'bound qualifier %s no longer '
                                         'next to %s' % (q, t['tok']), bu, tokens=[t['tok']]))
    # W1b: joint-cause and either-or markers too (配合 次年库存回补 -> 库存回补 alone; 并购或银行发债 -> 与)
    for q in ('而非', '并非', '至多', '最多', '不计', '未含', '未计', '不含', '仅', '口径', '配合', '共同', '叠加', '连同', '主要',
              '或') + JUDGE_Q + ATTR_Q:
        nb, nx = fact_text.count(q), body.count(q)
        if nx >= nb:
            continue
        for bu in base_units:
            b = bu['text']
            if q not in b or any(norm(b) == norm(r['u']['text']) for r in rws):
                continue
            bc = next((c for _s, c in split_clauses(b) if q in c), b)
            cands = [r for r in rws if not r['verbatim']]
            if not cands:
                continue
            best = max(cands, key=lambda r: coverage(bc, r['u']['text']))
            if coverage(bc, best['u']['text']) >= 0.35 and q not in best['u']['text']:
                add(_finding('G-QUAL', 'qualifier', 'candidate', best['u'], 'node lost marker %s (base %d, here %d); '
                             'base clause: %s' % (q, nb, nx, bc[:40]), bu))
    for r in rws:
        if r['verbatim']:
            continue
        rt = nsd.prep(r['u']['text'])
        for q in ATTR_Q + ('我们判断', '我们推断'):
            qp = rt.find(q)
            if qp < 0:
                continue
            for t in value_tokens(r['u']['text']):
                if t['start'] < qp:
                    continue
                srcs = [bu['text'] for bu in base_units if t['tok'] in nsd.tokens(bu['text'])]
                if srcs and not any(_marker_covers(s, q, t) for s in srcs):
                    add(_finding('G-QUAL', 'qualifier', 'candidate', r['u'], 'marker %s now covers %s, which the base '
                                 'states without it' % (q, t['tok']), srcs[0], tokens=[t['tok']]))
                    break
        if r['anchor'] is None:
            continue
        s, b = r['u']['text'], base_units[r['anchor']]['text']
        ts, tb = TAG_RE.search(s), TAG_RE.search(b)
        js, jb = JUDGE_RE.search(s), JUDGE_RE.search(b)
        if ts and tb and js and jb and ts.group() == tb.group():
            cs, cb = s[js.end():ts.start()], b[jb.end():tb.start()]
            if cs and cb and difflib.SequenceMatcher(None, cs, cb).ratio() < 0.5:
                add(_finding('G-QUAL', 'certainty', 'candidate', r['u'], 'confidence tag %s now bound to a different '
                             'claim' % ts.group(), b))
        mb, ms = CONTRAST_RE.search(b), CONTRAST_RE.search(s)
        if mb and ms:
            ib = [x for x in CONJ_RE.split(mb.group(1)) if x]
            is_ = [x for x in CONJ_RE.split(ms.group(1)) if x]
            if len(ib) > len(is_) and all(any(norm(y) in norm(x) or norm(x) in norm(y) for x in ib) for y in is_):
                add(_finding('G-QUAL', 'qualifier', 'candidate', r['u'], 'coordinated judgment lost a member: “%s” -> '
                             '“%s”' % (mb.group(1), ms.group(1)), b))
        if NEG_SOURCE_RE.search(b) and not NEG_SOURCE_RE.search(s) and coverage(norm(s), norm(b)) >= 0.5 \
                and body.count(NEG_SOURCE_RE.search(b).group(0)) < fact_text.count(NEG_SOURCE_RE.search(b).group(0)):
            add(_finding('G-QUAL', 'qualifier', 'candidate', r['u'], 'negated source dropped: the base says “%s”'
                         % NEG_SOURCE_RE.search(b).group(0), b))


# ------------------------------------------------------------------ W1b semantic candidates
SEM_NEW_COV = 0.7      # coverage of a sentence by its 3 nearest base sentences below which it is a new claim
TRAJ_W = ('先降后升', '先升后降', '由降转升', '由升转降', '并未', '未随', '不再', '率先', '更早', '更晚', '接棒', '只有', '只用于',
          '已经', '仍能', '就是', '主要', '只', '仅', '已')
TRAJ_SKIP = ('只要', '不只', '而已', '已知', '仅供', '不仅')
CITE_RE = re.compile(r'（([^（）\n]{2,60})）')
CITE_DATE_RE = re.compile(r'20\d\d年\d{1,2}月(?:\d{1,2}日)?|\d{1,2}月\d{1,2}日|20\d\d年(?!\d{1,2}月)')
FORE_RE = re.compile(r'前者|后者')
HEDGE_W = ('我们判断', '预计', '或将', '可能', '将')     # W1b replay: 若, 一旦, 我们推断, 我们假定 lost hit 0 of 100+ errors


def _semantic(rws, base_units, fact_text, add, lex=None, findings=()):
    """W1b: queue the semantic classes the deterministic checks cannot settle (Wave K: they were most of 过门错).
    All candidates, never hard: (a) G-ADDED claim: a number-free sentence or a paragraph opening whose 3 nearest base
    sentences cover less than SEM_NEW_COV of it (a new interpretive or causal claim, often a new opening after a
    split); (a2) G-QUAL qualifier: a hedge or judgment marker (我们判断, 将, 若 …) of the anchored base sentence is
    gone from this one; (b) G-MODAL certainty: a modal or trajectory word (只, 已, 并未, 先降后升 …) none of those base sentences
    holds; (c) G-CITE attribution: a date inside a parenthetical citation that B and C lack; (d) G-REF antecedent:
    前者／后者 whose antecedent pair changed order or text. Every one carries class 'semantic' (the tie-out seat may
    sort the queue by it)."""
    lex = lex or Lexicon([], {})
    flat = norm(clean(fact_text))
    have = {(f['code'], f['sid']) for f in findings}
    bidx = {norm(b['text']): i for i, b in enumerate(base_units)}

    def emit(f):
        f['class'] = 'semantic'
        add(f)
    for k, r in enumerate(rws):
        u = r['u']
        if u['kind'] not in ('prose', 'list'):
            continue
        if FORE_RE.search(u['text']):
            _fore_latter(rws, k, base_units, bidx.get(norm(u['text'])) if r['verbatim'] else r['anchor'], lex, emit)
        if r['verbatim'] or ncjk(u['text']) < 6:
            continue
        idx = sorted({i for _c, i in r['covs']}) if r['covs'] else []
        near_raw = ''.join(base_units[i]['text'] for i in idx)
        near_cov = coverage(norm(u['text']), norm(near_raw), 3) if near_raw else 0.0
        numfree = not value_tokens(u['text'])
        opening = u['idx'] == 0 and u['kind'] == 'prose'
        if (numfree or opening) and near_cov < SEM_NEW_COV:
            emit(_finding('G-ADDED', 'claim', 'candidate', u, '%s with no close base counterpart (its 3 nearest base '
                         'sentences cover %.2f of it): a claim the base may not make' %
                         ('paragraph opening' if opening else 'number-free sentence', near_cov),
                         base_units[idx[0]] if idx else None))
        if r['anchor'] is not None and r['cov'] >= 0.5 and ('G-QUAL', u['id']) not in have:
            b = base_units[r['anchor']]['text']
            lost = [q for q in HEDGE_W if b.count(q) > u['text'].count(q)]
            lost = [q for q in lost if not any(q != x and q in x for x in lost)]
            if lost:
                emit(_finding('G-QUAL', 'qualifier', 'candidate', u, 'hedge or judgment marker “%s” of its base sentence '
                             'is gone: a conditional or judged claim may now read as fact' % '、'.join(lost[:3]),
                             base_units[r['anchor']]))
        if ('G-MODAL', u['id']) not in have:
            for w in TRAJ_W:
                pos = u['text'].find(w)
                if pos < 0 or any(sk in u['text'][max(0, pos - 2):pos + len(w) + 2] for sk in TRAJ_SKIP):
                    continue
                if w not in near_raw:
                    emit(_finding('G-MODAL', 'certainty', 'candidate', u, 'modal or trajectory word “%s” absent from the '
                                 'base sentences this one rests on' % w, base_units[idx[0]] if idx else None))
                    break
        for m in CITE_RE.finditer(u['text']):
            inner = m.group(1)
            dates = CITE_DATE_RE.findall(inner)
            ents = [e for _p, e in lex.find(inner)]
            if not dates and not ents:
                continue
            lost = [d for d in dates if d not in flat]
            if lost:
                emit(_finding('G-CITE', 'attribution', 'candidate', u, 'citation date “%s” is absent from B and C'
                             % '、'.join(lost)))


def _fore_latter(rws, k, base_units, a, lex, emit):
    """G-REF antecedent (W1b): 前者／后者 in body unit K (verbatim or not) whose antecedent text (the sentence before
    and the part of its own sentence before the word) differs from the base's, or names its first two entities in
    another order (a reorder can flip which is which while the 前者 sentence itself stays word for word)."""
    u = rws[k]['u']
    prev = rws[k - 1]['u']['text'] if k else ''
    bprev = base_units[a - 1]['text'] if a is not None and a > 0 else ''
    btext = base_units[a]['text'] if a is not None else ''
    ante_new = prev + u['text'][:FORE_RE.search(u['text']).start()]
    bm = FORE_RE.search(btext)
    ante_old = bprev + (btext[:bm.start()] if bm else btext)
    en = [e for _p, e in lex.find(ante_new)]
    eo = [e for _p, e in lex.find(ante_old)]
    en = [e for i, e in enumerate(en) if e not in en[:i]]
    eo = [e for i, e in enumerate(eo) if e not in eo[:i]]
    if not bm:
        why = '前者／后者 here; its base sentence has none: check the antecedent pair'
    elif len(en) >= 2 and len(eo) >= 2 and en[:2] != eo[:2]:
        why = '前者／后者 antecedent order changed: %s here, %s in the base' % ('、'.join(en[:2]), '、'.join(eo[:2]))
    elif coverage(norm(ante_new), norm(ante_old)) < 0.8:
        why = '前者／后者 after a rewritten or moved antecedent: check which is which'
    else:
        return
    emit(_finding('G-REF', 'antecedent', 'candidate', u, why, btext or None))


SLOT_RE = re.compile(r'^\s*(?:[-*]\s*|\d+[.、]\s*)?\[?(?:G|A|断言)?\s?(?P<id>[\w.\-，,、 ]{1,30}?)\]?\s*[：:｜|]?\s*'
                     r'(?P<holder>[^｜|\n]{1,40})[｜|](?P<metric>[^｜|\n]{0,60})[｜|](?P<value>[^｜|\n]{1,60})'
                     r'(?:[｜|](?P<base>[^｜|\n]{0,80}))?(?:[｜|](?P<qual>[^｜|\n]{0,80}))?')


def _think_check(think, base_units, lex):
    out = []
    for no, ln in enumerate((think or '').split('\n'), 1):
        m = SLOT_RE.match(ln)
        if not m:
            continue
        holder = m.group('holder').strip()
        if holder in ('无', '—', '-', '未绑定', 'none', '无主语', '（无）') or not lex.find(holder):
            continue
        e = lex.find(holder)[0][1]
        u = {'id': 't%03d' % no, 'text': ln.strip()}
        for t in value_tokens(m.group('value')):
            vk = vkey(t['tok']).lstrip('+-')
            for bu in base_units:
                for bc in bu['clauses']:
                    if vk in {vkey(x).lstrip('+-') for x in bc['values']}:
                        if bc['holder'] and bc['bind'] in ('clause', 'sentence', 'cross-base', 'table-row') \
                                and not _same_entity(e, bc['holder'], lex):
                            out.append(_finding('G-THINK', 'holder', 'hard', u, '思路 slot binds %s to %s; the base '
                                                'binds it to %s' % (t['tok'], e, bc['holder']), bc['text'],
                                                where='思路'))
                        elif not bc['holder']:
                            out.append(_finding('G-THINK', 'holder', 'candidate', u, '思路 slot gives %s a holder %s; '
                                                'the base clause is subjectless' % (t['tok'], e), bc['text'],
                                                where='思路'))
    return out


# ------------------------------------------------------------------ G6 + U5a
def u5a(before, after, fact_text, grade):
    """Patch grade B: G6 first (sentences of AFTER that bring back base facts the pre-patch draft lost are the
    recovery and form the new baseline), then U5a: net CJK growth of the rest <= 0."""
    b_units = split_sentences(before)
    a_units = split_sentences(after)
    bset = {norm(u['text']) for u in b_units}
    btoks = collections.Counter(vkey(t) for u in b_units for t in nsd.tokens(u['text']))
    ftoks = {vkey(t) for t in nsd.tokens(fact_text)}
    fsents = {norm(u['text']) for u in split_sentences(fact_text)}
    recovered, rec_cjk = [], 0
    for u in a_units:
        if norm(u['text']) in bset:
            continue
        toks = [vkey(t) for t in nsd.tokens(u['text'])]
        back = [t for t in toks if t in ftoks and btoks[t] == 0]
        if back or norm(u['text']) in fsents:
            recovered.append(u['text'])
            rec_cjk += ncjk(u['text'])
    net = ncjk(after) - ncjk(before) - rec_cjk
    ok = str(grade).upper() != 'B' or net <= 0
    return {'grade': grade, 'cjk_before': ncjk(before), 'cjk_after': ncjk(after), 'recovered': recovered[:8],
            'recovered_cjk': rec_cjk, 'net_cjk': net, 'ok': ok}


# ------------------------------------------------------------------ trace split
TRACE_RE = re.compile(r'^\s*(?:[-*]\s+)?(?:N[\d.]+\s+)?(轨迹[：:].*\S)\s*$')


SEM_FIELDS = ('claim', 'attribution', 'qualifier', 'certainty', 'causation', 'antecedent')


def _quotes(t, s, n=12):
    a, b = norm(t), norm(s)
    if not a or not b:
        return False
    m = difflib.SequenceMatcher(None, a, b, autojunk=False).find_longest_match(0, len(a), 0, len(b))
    return m.size >= min(n, len(b))


def split_trace(lines, findings, lex=None):
    """(propagable, quarantined). W1b, narrowed to a finding's own evidence: a trace line is quarantined when it
    carries a quantity token (small counts such as 4家 left out) of a hard finding or of a value, holder, direction or
    operand candidate, a direction word of a hard or direction finding, an entity of a G-HOLDER finding, or two or
    more entities while a hard G-HOLDER finding is open; a semantic or qualifier candidate (claim, attribution,
    qualifier, certainty, causation, antecedent) quarantines only a line quoting its sentence (a shared run of 12
    characters) or carrying the tokens it names. '## 思路' diagnostics never quarantine."""
    lex = lex or Lexicon([], {})
    bad_tok, bad_dir, bad_ent, holder_open, quoted, bad_per = set(), set(), set(), False, [], set()
    for f in findings:
        if f.get('severity') == 'diagnostic':
            continue
        s = f.get('sentence') or ''
        named = {vkey(x) for x in f.get('tokens') or []}
        if f['code'] == 'G-PERIOD':      # 1.2.0 (F14): a changed period quarantines the trace lines naming it
            bad_per |= {tuple(k) for k in f.get('period_keys') or []}
            if f['severity'] == 'candidate':
                continue
        if f['severity'] == 'candidate' and f['field'] in SEM_FIELDS:
            bad_tok |= named
            quoted.append(s)
            continue
        bad_tok |= {vkey(t['tok']) for t in qty_tokens(s)} | named
        if f['severity'] == 'hard' or f['field'] == 'direction':
            bad_dir |= set(_dirs(s)[1])
        if f['code'] == 'G-HOLDER':
            bad_ent |= {e for _p, e in lex.find(s)}
            holder_open |= f['severity'] == 'hard'
    bad_per |= {k[:2] for k in bad_per}
    prop, quar = [], []
    for ln in lines or []:
        m = TRACE_RE.match(ln)
        if not m:
            continue
        t = m.group(1)
        toks = {vkey(x['tok']) for x in qty_tokens(t)}
        ents = {e for _p, e in lex.find(t)}
        why = []
        if toks & bad_tok:
            why.append('token ' + '、'.join(sorted(toks & bad_tok))[:60])
        if set(_dirs(t)[1]) & bad_dir:
            why.append('direction')
        if ents & bad_ent or (holder_open and len(ents) >= 2):
            why.append('entity')
        if any(_quotes(t, s) for s in quoted):
            why.append('quotes a candidate sentence')
        if bad_per and any(k in bad_per or k[:2] in bad_per for _s, k in period_spans(t, loose=True)):
            why.append('period')
        (quar if why else prop).append(t if not why else {'line': t, 'why': '; '.join(why)})
    return prop, quar


# ------------------------------------------------------------------ G1 lint
def _sentences_simple(t):
    return [x for x in re.split(r'(?<=[.;。；])\s*|\s+(?=or\b)|(?<=，)或|；或|, or ', t) if x and x.strip()]


def lint_text(instr, draft_norm, base_norm='', verify_vk=None, verified=None):
    """-> (kept text, [stripped pieces with categories]). INSTR is one ruling's instruction text. 1.2.0 (F02): with
    VERIFY_VK (the value keys of B and C), a piece whose only categories are number and replacement and whose every
    number the draft lacks is in B or C is a verified fact fix and stays whole (appended to VERIFIED); lint() passes
    it for a tie-out seat's entries only."""
    kept, stripped = [], []
    for piece in re.split(r'(?<=[.;。；])\s+|(?<=[。；])|\s(?=[Oo]r\s)|(?<=，)(?=或)', instr or ''):
        p = piece.strip()
        if not p:
            continue
        cats = []
        quotes = [q for q in Q_RE.findall(p)]
        non_anchor = [q for q in quotes if norm(q) and norm(q) not in draft_norm]
        for q in non_anchor:
            pos = p.find(q)
            pre = p[max(0, pos - 24):pos]
            ban = re.search(r'(?i)不写|不用|别用|勿用|avoid|do not (?:write|use)|don\'t (?:write|use)|instead of|而不是', pre)
            if ban and not REPL_CUE.search(pre.split(ban.group(0))[-1] if ban else pre):
                continue
            if REPL_CUE.search(pre) or ncjk(q) >= 8 or re.search(r'(?i)instead', p[pos:pos + len(q) + 16]):
                if not (base_norm and norm(q) in base_norm and re.search(r'(?i)restore|恢复|base|底稿|B:', p)):
                    cats.append('replacement')
                    break
        bare = Q_RE.sub(lambda m: '“%s”' % m.group(1) if norm(m.group(1)) in draft_norm else '“…”', p)
        bare_nq = Q_RE.sub('', p)
        if DIR_RX.search(bare_nq):
            cats.append('direction')
        if CAUSE_RX.search(bare_nq) and not FORM_ACTION.search(bare_nq):
            cats.append('causation')
        if CERT_RX.search(bare_nq) and CONTENT_RX.search(bare_nq + ' '):
            cats.append('certainty')
        if HOLDER_RX.search(bare_nq):
            cats.append('holder')
        if UNIT_RX.search(bare_nq) and (CONTENT_RX.search(bare_nq) or REPL_CUE.search(bare_nq) or '补' in bare_nq):
            cats.append('unit')
        nums = [t for t in nsd.tokens(bare_nq) if not is_date(t)]
        if nums and any(norm(t) not in draft_norm for t in nums):
            cats.append('number')
        if not cats and CONTENT_RX.search(bare_nq) and not FORM_ACTION.search(bare_nq):
            cats.append('content')
        if REPL_CUE.search(bare_nq) and not FORM_ACTION.search(bare_nq) and 'replacement' not in cats and non_anchor:
            cats.append('replacement')
        if cats and verify_vk is not None and set(cats) <= {'number', 'replacement'}:
            newk = [vkey(t) for t in nsd.tokens(p) if not is_date(t) and norm(t) not in draft_norm]
            if newk and all(k in verify_vk or k.lstrip('+') in verify_vk for k in newk):
                if verified is not None:
                    verified.append({'text': p, 'categories': sorted(set(cats))})
                kept.append(p)
                continue
        if cats:
            anchors = ['“%s”' % q for q in quotes if norm(q) and norm(q) in draft_norm]
            stripped.append({'text': p, 'categories': sorted(set(cats)), 'anchors': anchors})
            if anchors:   # the target sentence stays named; only the prescription goes to the tie-out seat
                kept.append(' '.join(anchors))
        else:
            kept.append(bare)
    return ' '.join(kept).strip(), stripped


def residual(text, draft_norm, verify_vk=None):
    """Prescriptions left in a sanitized instruction (must be 0; a tie-out seat's verified fact fix is not one)."""
    _kept, st = lint_text(text, draft_norm, '', verify_vk)
    return st


ENTRY_RE = re.compile(r'^##\s+(\d+)\s*（([^）]*)）\s*$')
# W4c (F02): in the by-node format a bullet or table row tagged [核对席] / （核对席） / [tie-out] is a tie-out seat's
# entry (a '## n（核对席）' heading inside '### <NODE>' would end the node's section in pack_node)
TIEOUT_TAG = re.compile(r'^(?:[-*+]\s+)?(?:\|\s*)?(?:\[\s*(?:核对席|核数席|tie-?out)\s*\]|[（(]\s*(?:核对席|核数席|tie-?out)\s*[）)])',
                        re.I)


def parse_rulings(text):
    """Entries of the review-ruling format ('## n（seat）' then '- quote (exact):', '- rule:', '- problem:',
    '- fix:', '- sev:') -> [dict]."""
    out, cur = [], None
    for ln in (text or '').split('\n'):
        m = ENTRY_RE.match(ln)
        if m:
            cur = {'n': m.group(1), 'seat': m.group(2), 'quote': '', 'rule': '', 'problem': '', 'fix': '', 'sev': ''}
            out.append(cur)
            continue
        if cur is None:
            continue
        m = re.match(r'^-\s*(quote(?: \(exact\))?|rule|problem|fix|sev|#|T0)\s*:\s*(.*)$', ln)
        if m:
            k = m.group(1).split(' ')[0]
            if k in cur:
                cur[k] = m.group(2).strip().strip('`')
    return out


def lint(findings_text, draft='', base='', node=None, mode='refuse'):
    """-> dict(text: sanitized findings (refuse) or the input (warn), questions, entries, stripped)."""
    dn, bn = norm(clean(draft)), norm(clean(base))
    questions, stats = [], collections.Counter()
    entries = parse_rulings(findings_text)
    base_vk = signed_keys(clean(base)) if (base or '').strip() else None
    if entries:
        out = []
        for e in entries:
            stats['entries'] += 1
            anchored = bool(e['quote']) and norm(e['quote']) in dn if dn else None
            # 1.2.0 (F02): a tie-out seat's fix whose new numbers are verified against B/C travels whole
            tie_vk = base_vk if base_vk and TIEOUT_SEAT.search(e.get('seat') or '') else None
            ver = []
            kept_fix, st_fix = lint_text(e['fix'], dn, bn, tie_vk, ver)
            kept_pb, st_pb = lint_text(e['problem'], dn, bn, tie_vk, ver)
            if ver:
                stats['tieout_verified'] += 1
                e = dict(e, tieout_verified=ver)
            st_pb = [x for x in st_pb if 'replacement' in x['categories'] or 'direction' in x['categories']
                     or 'number' in x['categories']]
            if st_fix or st_pb:
                stats['stripped'] += 1
                for x in st_fix + st_pb:
                    for c in x['categories']:
                        stats['cat_' + c] += 1
                questions.append({'node': node, 'seat': e['seat'], 'n': e['n'], 'quote': e['quote'],
                                  'rule': e['rule'], 'problem': e['problem'], 'stripped': st_fix + st_pb,
                                  'question': 'Content point for the tie-out seat (the cold reader holds no source): '
                                              + ' | '.join(x['text'] for x in st_fix + st_pb)})
            if anchored is False:
                stats['unanchored'] += 1
            out.append(dict(e, fix=kept_fix if st_fix else e['fix'], problem=kept_pb if st_pb else e['problem'],
                            anchored=anchored, stripped=[x['categories'] for x in st_fix + st_pb]))
        res_left = sum(len(residual(x['fix'], dn, base_vk if x.get('tieout_verified') else None)) for x in out)
        return {'entries': out, 'questions': questions, 'stats': dict(stats), 'residual': res_left,
                'text': findings_text if mode != 'refuse' else render_rulings(out)}
    # inline by-node format: every row / line is one instruction
    lines_out, tie_lines = [], set()
    for ln in (findings_text or '').split('\n'):
        st = ln.strip()
        body = st
        if not st or re.match(r'^#{1,6}\s', st) or re.match(r'^\|?\s*:?-{2,}', st):
            lines_out.append(ln)
            continue
        stats['lines'] += 1
        tie_vk = base_vk if base_vk and TIEOUT_TAG.match(st) else None
        ver = []
        if st.startswith('- |') or st.startswith('|'):
            cells = [c.strip() for c in st.lstrip('- ').strip('|').split('|')]
            new_cells, stripped = [], []
            for c in cells:
                k, s2 = lint_text(c, dn, bn, tie_vk, ver)
                if s2:
                    stripped += s2
                    new_cells.append((k + ' ' if k else '') + '(content point routed to the tie-out seat; leave '
                                     'this sentence\'s facts as they are)')
                else:
                    new_cells.append(c)
            out_ln = ('- | ' if st.startswith('- |') else '| ') + ' | '.join(new_cells) + ' |'
        else:
            k, stripped = lint_text(body, dn, bn, tie_vk, ver)
            out_ln = ln if not stripped else (ln[:len(ln) - len(ln.lstrip())] + (k + ' ' if k else '')
                                               + '(content point routed to the tie-out seat)')
        if ver:
            stats['tieout_verified'] += 1
            tie_lines.add(len(lines_out))
        if stripped:
            stats['stripped'] += 1
            for x in stripped:
                for c in x['categories']:
                    stats['cat_' + c] += 1
            questions.append({'node': node, 'line': st[:300], 'stripped': stripped,
                              'question': 'Content point for the tie-out seat: ' + ' | '.join(x['text'] for x in stripped)})
        lines_out.append(out_ln if mode == 'refuse' else ln)
    return {'text': '\n'.join(lines_out), 'questions': questions, 'stats': dict(stats),
            'residual': 0 if mode != 'refuse' else sum(len(residual(x, dn, base_vk if i in tie_lines else None))
                                                       for i, x in enumerate(lines_out) if 'tie-out' not in x
                                                       or i in tie_lines)}


def render_rulings(entries):
    out = []
    for e in entries:
        out += ['## %s（%s）' % (e['n'], e['seat']), '', '- quote (exact): %s' % e['quote'], '- rule: %s' % e['rule'],
                '- problem: %s' % e['problem'],
                '- fix: %s' % (e['fix'] or '(content point routed to the tie-out seat; change only the form)'),
                '- sev: %s' % e['sev'], '']
    return '\n'.join(out)


# ------------------------------------------------------------------ acceptance / release
def sha256_text(t):
    return hashlib.sha256((t or '').encode('utf-8')).hexdigest()


def atomic_write(path, text):
    d = os.path.dirname(os.path.abspath(path))
    os.makedirs(d, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=d, prefix='.' + os.path.basename(path) + '.')
    with os.fdopen(fd, 'w', encoding='utf-8') as fh:
        fh.write(text)
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp, path)


def node_lock_path(acceptance_json):
    """The node lock of an acceptance record <drafts>/acceptance/<node>.json: acceptance/.<node>.lock, the same file
    inline_common.node_lock takes (1.2.0, F07: one lock for every read-modify-write of a node's record)."""
    d, b = os.path.split(os.path.abspath(acceptance_json))
    return os.path.join(d, '.' + (b[:-5] if b.endswith('.json') else b) + '.lock')


def release_trace(path, lines=None, release_all=False):
    lock = node_lock_path(path)
    with open(lock, 'a') as lf:
        fcntl.flock(lf, fcntl.LOCK_EX)
        with open(path, encoding='utf-8') as fh:
            acc = json.load(fh)
        keep, moved = [], []
        for q in acc.get('quarantined_trace', []):
            t = q['line'] if isinstance(q, dict) else q
            if release_all or (lines and any(x in t for x in lines)):
                moved.append(t)
            else:
                keep.append(q)
        acc['propagable_trace'] = list(acc.get('propagable_trace', [])) + moved
        acc['quarantined_trace'] = keep
        acc.setdefault('releases', []).append({'moved': moved})
        atomic_write(path, json.dumps(acc, ensure_ascii=False, indent=1) + '\n')
    return moved


# ------------------------------------------------------------------ CLI
def _read(p):
    with open(p, encoding='utf-8') as fh:
        return fh.read().replace('\r\n', '\n')


def load_rows(path):
    """--rows FILE (1.3.0): a JSON list, a JSON object (one row, or {"derivations": [...]}, with 1.3.2 its
    "unsigned_rows" added as signed false), or JSONL (one row or a list per line) -> [dict]; legacy text/value rows and
    derivation rows alike. Raises ValueError on a non-object."""
    txt = _read(path).strip()
    if not txt:
        return []
    try:
        data = json.loads(txt)
        items = data if isinstance(data, list) else (data.get('derivations', [data]) if isinstance(data, dict)
                                                     else [data])
        if isinstance(data, dict):  # W4b: pack_node's derivations.json carries its unsigned rows (never signed)
            items = list(items) + [dict(r, signed=False) for r in data.get('unsigned_rows') or ()
                                   if isinstance(r, dict)]
    except ValueError:
        items = []
        for ln in txt.split('\n'):
            if ln.strip():
                x = json.loads(ln)
                items.extend(x if isinstance(x, list) else [x])
    bad = [x for x in items if not isinstance(x, dict)]
    if bad:
        raise ValueError('--rows: every row must be a JSON object, got %r' % (bad[0],))
    return items


def _answer_parts(text):
    out = {}
    heads = [(m.start(), m.end(), m.group(1)) for m in re.finditer(r'(?m)^##\s*(思路|正文|回执)\s*$', text or '')]
    for k, (_s, e, name) in enumerate(heads):
        end = heads[k + 1][0] if k + 1 < len(heads) else len(text)
        out.setdefault(name, text[e:end].strip('\n'))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(prog='inline_guards.py', description=__doc__.split('\n')[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter, epilog=__doc__.split('\n', 2)[2])
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--version', action='version', version=VERSION)
    sub = ap.add_subparsers(dest='cmd')
    s = sub.add_parser('scan')
    s.add_argument('base')
    s.add_argument('--doc')
    s.add_argument('--names')
    s.add_argument('--must-subject', nargs='*', default=[])
    s.add_argument('--node')
    s.add_argument('--json', action='store_true')
    s.add_argument('--out')
    li = sub.add_parser('lint')
    li.add_argument('findings')
    li.add_argument('--draft')
    li.add_argument('--base')
    li.add_argument('--node')
    li.add_argument('--mode', choices=('refuse', 'warn'), default='refuse')
    li.add_argument('--out')
    li.add_argument('--questions')
    li.add_argument('--json', action='store_true')
    rc = sub.add_parser('recompute')
    rc.add_argument('--sentence')
    rc.add_argument('--file')
    rc.add_argument('--context', default='')
    rc.add_argument('--profile', choices=('draft', 'rewrite'), default='rewrite')
    rc.add_argument('--base', help='frozen base B (1.2.0): list the sentence\'s value tokens the base lacks')
    rc.add_argument('--rows', help='1.3.0: tie-out or derivation rows (JSON list or JSONL), the context rule applies')
    rc.add_argument('--json', action='store_true')
    v = sub.add_parser('verify')
    v.add_argument('--base', help='frozen base B; a draft may omit it (1.3.0: an empty base, C via --sources)')
    v.add_argument('--body')
    v.add_argument('--think')
    v.add_argument('--answer')
    v.add_argument('--profile', choices=('draft', 'rewrite'), default='rewrite')
    v.add_argument('--doc')
    v.add_argument('--sources')
    v.add_argument('--names')
    v.add_argument('--before')
    v.add_argument('--grade')
    v.add_argument('--rows')
    v.add_argument('--trace-lines')
    v.add_argument('--candidates-out')
    v.add_argument('--node')
    v.add_argument('--relocation', action='store_true', help='rewrite with opening detail relocation on (O73): G-RELOC')
    v.add_argument('--json', action='store_true')
    r = sub.add_parser('release-trace')
    r.add_argument('acceptance')
    r.add_argument('--line', nargs='*', default=[])
    r.add_argument('--all', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if a.cmd == 'scan':
        base = _read(a.base)
        doc = _read(a.doc) if a.doc else None
        lex = build_lexicon([doc or base, base], a.names)
        res = scan(base, doc, lex, a.must_subject, a.node)
        txt = json.dumps(res, ensure_ascii=False, indent=1) if a.json else '\n'.join(guard_rows(res))
        if a.out:
            atomic_write(a.out, txt + '\n')
        else:
            print(txt)
        if not a.json:
            print('scan: %s' % json.dumps(res['summary'], ensure_ascii=False), file=sys.stderr)
        return 0
    if a.cmd == 'lint':
        res = lint(_read(a.findings), _read(a.draft) if a.draft else '', _read(a.base) if a.base else '', a.node,
                   a.mode)
        if a.out:
            atomic_write(a.out, res['text'] + ('\n' if not res['text'].endswith('\n') else ''))
        if a.questions and res['questions']:
            with open(a.questions, 'a', encoding='utf-8') as fh:
                for q in res['questions']:
                    fh.write(json.dumps(q, ensure_ascii=False) + '\n')
        if a.json:
            print(json.dumps({k: res[k] for k in ('stats', 'questions', 'residual')}, ensure_ascii=False, indent=1))
        else:
            print('lint: %s; %d questions; residual prescriptions %d' % (json.dumps(res['stats'], ensure_ascii=False),
                                                                        len(res['questions']), res['residual']))
            if not a.out:
                print(res['text'])
        return 0
    if a.cmd == 'recompute':
        sent = a.sentence or (_read(a.file) if a.file else '')
        try:
            rrows = load_rows(a.rows) if a.rows else []
        except ValueError as e:
            print('recompute: %s' % e, file=sys.stderr)
            return 2
        res = recompute(sent, a.context, a.profile, _read(a.base) if a.base else '', rrows)
        txt = '%s %s' % (res['status'], res['hint'])
        if 'new_tokens' in res:
            txt += '\nbase: %s' % ('ok (no token absent from the base)' if res['base_ok'] else
                                   'absent from the base: %s; %s' % ('、'.join(res['new_tokens']), res['authority']))
        print(json.dumps(res, ensure_ascii=False, indent=1) if a.json else txt)
        return 0
    if a.cmd == 'verify':
        think, body, trace = '', '', []
        if a.answer:
            parts = _answer_parts(_read(a.answer))
            think, body = parts.get('思路', ''), parts.get('正文', '')
            trace = [ln for ln in parts.get('回执', '').split('\n') if TRACE_RE.match(ln)]
        if a.body:
            body = _read(a.body)
        if a.think:
            think = _read(a.think)
        if a.trace_lines:
            trace = [ln for ln in _read(a.trace_lines).split('\n') if TRACE_RE.match(ln)]
        if not a.base and a.profile == 'rewrite':
            print('verify: a rewrite needs --base (only a draft may run on an empty base)', file=sys.stderr)
            return 2
        base = _read(a.base) if a.base else ''
        doc = _read(a.doc) if a.doc else None
        src = _read(a.sources) if a.sources else ''
        try:
            rows = load_rows(a.rows) if a.rows else []
        except ValueError as e:
            print('verify: %s' % e, file=sys.stderr)
            return 2
        lex = build_lexicon([doc or base, base, src], a.names)
        res = verify(base, body, think, a.profile, doc, src, lex, _read(a.before) if a.before else None, a.grade,
                     rows, trace, a.node, relocation=a.relocation)
        if a.candidates_out and res['candidates']:
            with open(a.candidates_out, 'a', encoding='utf-8') as fh:
                for c in res['candidates']:
                    fh.write(json.dumps(dict(c, node=a.node), ensure_ascii=False) + '\n')
        if a.json:
            print(json.dumps(res, ensure_ascii=False, indent=1))
        else:
            print('verify: %s (hard %d, candidates %d)' % (res['verdict'], len(res['hard']), len(res['candidates'])))
            for f in res['hard'] + res['candidates']:
                print('  %s %s %s %s: %s' % (f['severity'], f['code'], f['where'], f['sid'], f['why'][:160]))
        return 1 if res['verdict'] == 'HARD_REJECT' else 0
    if a.cmd == 'release-trace':
        moved = release_trace(a.acceptance, a.line, a.all)
        print('release-trace: %d line(s) moved to propagable_trace' % len(moved))
        return 0
    ap.print_help()
    return 2


# ------------------------------------------------------------------ self-test
SELF_BASE = {
    'N005': ('股东出资端，SoftBank除2026年一季度签下$40.0bn过桥贷款并于9月15日前将已提$30.0bn全额提前偿还外，'
             '另设SoftBank借入的$10.0bn（不质押OpenAI股份，集团担保）。'),
    'N046': ('据Morgan Stanley于11月10日报告，若后续供应商融资比照Amazon采用有担保结构，可能优先于无担保债权人受偿，'
             '进而引出约20%有担保债门槛的问题，令无担保票据与公司家族评级的平价受到质疑。我们假定Oracle无既有有担保债，'
             '按指数债约$117.2bn至总债务约$140bn作分母粗算，门槛约合$29–35bn，Oracle是否采用有担保结构尚未披露。'),
    'N063': ('交付前阶段，公司应收账款与合同资产合计$1,493mn，其中交付前合同资产$858.6mn，减去含$661.4mn部分可退定金在内的'
             '定金与递延收入$754mn后，净垫资达$739mn。'),
    'N023': ('站点宽限日后仍未稳定时，借款人须缩额或追加摊还本金以重回预计偿债覆盖率下限，'
             '且无限次股权补救截止日后每连续12个月最多动用3个财月。DDTL 3.0每笔贷款最多补救3次。'),
    'N000': ('若后续核心租约提前解约、私募信贷集中提用银行授信，或非AI投资与库存加速收缩、美联储重获降息缓冲，'
             '上述违约与衰退概率均须相应改判（见图1）。'),
    'DIR': 'Fitch上调Oracle的展望。Moody\'s下调CoreWeave的评级。',
    'N059': ('同处整机层的Dell通过旗下Dell Financial Services（下称DFS）一边卖服务器一边向算力买方放款。'
             '据Dell截至2026年7月31日的2027财年第二财季10-Q季报，DFS单季新发放融资由上年同期的$2.4bn跃升至$7.5bn，'
             '融资应收净额半年内由$14.3bn增至$20.4bn。同期期末现金$11.57bn对含跨年采购义务总额$34.8bn及在制品的纯现金口径'
             '覆盖率为0.30x，现金毛覆盖约1.33季，若只计12个月内到期的$24.6bn则为1.88季。'),
}
SELF_DOC = (SELF_BASE['N059'] + '\n\n现金只够覆盖0.83季，短于同为整机商的Dell的1.33季。\n\n'
            '| 服务器整机与ODM | Dell | DELL | 核心链 | 0.30 | 0.26 |\n')


def selftest():
    res = []

    def check(name, ok, detail=''):
        res.append(bool(ok))
        print('  %s %s%s' % ('PASS' if ok else 'FAIL', name, ('  [%s]' % detail) if (detail and not ok) else ''))

    def V(base, body, profile='rewrite', doc=None, think='', **kw):
        lex = build_lexicon([doc or base, base])
        return verify(base, body, think, profile, doc, '', lex, **kw)

    def codes(r, sev='hard'):
        return sorted({f['code'] for f in (r['hard'] if sev == 'hard' else r['candidates'])})

    print('[inline_guards self-test %s]' % VERSION)
    # identity
    for k, b in SELF_BASE.items():
        r = V(b, b, doc=SELF_DOC if k == 'N059' else None)
        check('identity %s: PASS, no finding' % k, r['verdict'] == 'PASS' and not r['hard'] and not r['candidates'],
              json.dumps(r['hard'] + r['candidates'], ensure_ascii=False)[:300])
    # N005: a separately arranged facility is no subtraction
    sc = scan(SELF_BASE['N005'])
    row = sc['sentences'][0]
    check('N005 $40bn/$30bn/$10bn: coincidental, not a formula (另设)', row['arith'] == 'not_formula'
          and row.get('coincidental'), json.dumps(row, ensure_ascii=False)[:300])
    # N046: unclosed literal denominator, legal bridge, new derived numbers
    sc = scan(SELF_BASE['N046'])
    row = [x for x in sc['sentences'] if '作分母' in x['text']][0]
    check('N046 literal denominator: recompute_needed (closes only as x/(D+x))', row['arith'] == 'unclosed'
          and 'x / (D + x)' in row.get('recompute_needed', ''), json.dumps(row, ensure_ascii=False)[:400])
    bridge = SELF_BASE['N046'].replace('按指数债约$117.2bn至总债务约$140bn作分母粗算',
                                       '存量债取指数债约$117.2bn至总债务约$140bn，按新增有担保债占（存量债＋新增有担保债）的20%粗算')
    r = V(SELF_BASE['N046'], bridge)
    check('N046 Opus bridge (20% restates 约20%, no new number): PASS', r['verdict'] == 'PASS',
          json.dumps(r['hard'] + r['candidates'], ensure_ascii=False)[:400])
    der = SELF_BASE['N046'].replace('门槛约合$29–35bn', '即新增债占存量的25%，约四分之一，门槛约合$29–35bn')
    r = V(SELF_BASE['N046'], der)
    check('N046 new derived 25% / 四分之一 in rewrite: HARD_REJECT (G-NEWNUM)', r['verdict'] == 'HARD_REJECT'
          and 'G-NEWNUM' in codes(r), str(codes(r)))
    r = V(SELF_BASE['N046'], der, profile='draft')
    check('N046 the same in draft (1.3.0 W1-0to1 ruling, was a candidate before 1.3.0): HARD_REJECT (G-NEWNUM, '
          '算在树上，叶席零新数)', r['verdict'] == 'HARD_REJECT' and 'G-NEWNUM' in codes(r),
          str(codes(r)) + str(codes(r, 'cand')))
    # N040 bridge
    b40 = ('AI资本开支全基数削减50%、毛冲击占GDP的1.23%时，设备净进口泄漏系数取1.0、0.8与0.5三档假设下，进口收缩分别抵消'
           '1.12%、0.90%与0.56%的GDP，国内首年净拖累依次为0.11%、0.33%与0.67%。')
    n40 = ('该情景设定AI资本开支全基数削减50%，毛冲击占GDP的1.23%。设备净进口泄漏系数乘的是其中的设备部分（占GDP的1.12%），'
           '系数取1.0、0.8与0.5三档假设时，进口收缩分别抵消1.12%、0.90%与0.56%的GDP，国内首年净拖累依次为0.11%、0.33%与0.67%。')
    r = V(b40, n40)
    check('N040 Opus bridge (the base the coefficient multiplies, existing 1.12%): no hard finding',
          r['verdict'] != 'HARD_REJECT', json.dumps(r['hard'], ensure_ascii=False)[:300])
    # N063 minuend, 小计 bypass, legal back-reference
    b63 = SELF_BASE['N063']
    r = V(b63, '交付前合同资产$858.6mn减去含$661.4mn部分可退定金在内的定金与递延收入$754mn后，净垫资达$739mn。')
    check('N063 wrong minuend $858.6mn: HARD_REJECT (G-ARITH operand_role)', 'G-ARITH' in codes(r), str(codes(r)))
    r = V(b63, '交付前合同资产小计$858.6mn减去定金与递延收入$754mn后，净垫资达$739mn。')
    check('N063 adversarial 小计 label on the wrong minuend: still HARD_REJECT', 'G-ARITH' in codes(r), str(codes(r)))
    r = V(b63, '交付前阶段，公司应收账款与合同资产合计$1,493mn，其中交付前合同资产$858.6mn。上述应收账款与合同资产合计减去'
               '含$661.4mn部分可退定金在内的定金与递延收入$754mn后，净垫资达$739mn。')
    check('N063 legal patch (上述…合计 = $1,493mn): no G-ARITH', 'G-ARITH' not in codes(r) + codes(r, 'cand'),
          json.dumps(r['hard'] + r['candidates'], ensure_ascii=False)[:300])
    # N023 compound unit, swap between two contracts
    b23 = SELF_BASE['N023']
    r = V(b23, b23.replace('最多动用3个财月', '最多动用3次'))
    check('N023 3个财月 -> 3次: HARD_REJECT (G-UNIT)', 'G-UNIT' in codes(r), str(codes(r)))
    r = V(b23, b23.replace('最多动用3个财月', '最多动用3次').replace('最多补救3次', '最多补救3个财月'))
    check('N023 adversarial swap 3次 <-> 3个财月 between two contracts: HARD_REJECT', 'G-UNIT' in codes(r)
          and len(r['hard']) >= 2, str(r['hard'])[:300])
    # direction swap and the N000 lock
    r = V(SELF_BASE['DIR'], 'Fitch下调Oracle的展望。Moody\'s上调CoreWeave的评级。')
    check('adversarial 上调/下调 swap between two companies: HARD_REJECT (G-DIR)', 'G-DIR' in codes(r)
          and len([f for f in r['hard'] if f['code'] == 'G-DIR']) == 2, str(r['hard'])[:300])
    r = V(SELF_BASE['N000'], SELF_BASE['N000'].replace('上述违约与衰退概率均须相应改判', '须上调相应的违约或衰退概率'))
    check('N000 direction lock: 相应改判 -> 须上调: HARD_REJECT (G-DIR)', 'G-DIR' in codes(r), str(codes(r)))
    # N059 seven variants
    b59, doc = SELF_BASE['N059'], SELF_DOC
    tail = '同期期末现金$11.57bn对含跨年采购义务总额$34.8bn及在制品的纯现金口径覆盖率为0.30x，现金毛覆盖约1.33季，若只计12个月内到期的$24.6bn则为1.88季。'
    head = b59.replace(tail, '')
    variants = [
        ('historical: DFS的现金…一个季度以上', head + '留表放贷扩张的同时，DFS的现金对采购承诺覆盖仍在一个季度以上。', 'hard'),
        ('role swap: DFS期末现金…0.30x', head + tail.replace('同期期末现金', '同期DFS期末现金'), 'hard'),
        ('strong-seat wrong fill: DFS现金毛覆盖约1.33季', head + tail.replace('现金毛覆盖约1.33季', 'DFS现金毛覆盖约1.33季'),
         'hard'),
        ('legal reorder, subjectless', head + '同期现金毛覆盖约1.33季，若只计12个月内到期的$24.6bn则为1.88季，期末现金$11.57bn'
         '对含跨年采购义务总额$34.8bn及在制品的纯现金口径覆盖率为0.30x。', 'pass'),
        ('legal subject Dell', head + tail.replace('同期期末现金', '同期Dell期末现金'), 'pass'),
        ('pronoun 其 before the quantity', head + tail.replace('现金毛覆盖约1.33季', '其现金毛覆盖约1.33季'), 'cand'),
        ('公司 before the quantity', head + tail.replace('同期期末现金', '同期公司期末现金'), 'cand')]
    for name, body, want in variants:
        r = V(b59, body, doc=doc)
        got = 'hard' if r['verdict'] == 'HARD_REJECT' else 'cand' if r['verdict'] == 'PUBLISH_WITH_CANDIDATES' else 'pass'
        check('N059 %s: %s' % (name, want), got == want, '%s %s' % (got, json.dumps(r['hard'] + r['candidates'],
                                                                                     ensure_ascii=False)[:300]))
    # 我们假定 identity, source adverbial
    r = V(SELF_BASE['N046'], SELF_BASE['N046'].replace('我们假定Oracle无既有有担保债', '公司披露Oracle无既有有担保债'))
    check('我们假定 -> 公司披露: HARD_REJECT (G-ASSUME)', 'G-ASSUME' in codes(r), str(codes(r)))
    units = bind_sentences(b59, build_lexicon([doc]), doc_index(doc, build_lexicon([doc])))
    cl = [c for u in units for c in u['clauses'] if '7.5bn' in c['text']]
    check('据Dell…季报 is a source adverbial: the $7.5bn clause binds to DFS', cl and cl[0]['holder'] == 'DFS',
          str(cl[:1]))
    t = [u for u in units if '11.57bn' in u['text']][0]
    check('N059 subjectless cash sentence binds to Dell by cross-base (1.33季, table row 0.30)',
          t['binding']['how'] == 'cross-base' and t['binding']['holder'] == 'Dell', str(t['binding']))
    # 思路 vs 正文
    wrong = head + tail.replace('现金毛覆盖约1.33季', 'DFS现金毛覆盖约1.33季')
    r = V(b59, wrong, doc=doc, think='1. [G1] Dell｜现金毛覆盖｜1.33季｜季度化采购承诺｜约')
    check('思路 right, 正文 wrong: still HARD_REJECT (思路 never clears 正文)', r['verdict'] == 'HARD_REJECT'
          and any(f['where'] == '正文' for f in r['hard']), str(r['hard'])[:200])
    r = V(b59, b59, doc=doc, think='1. [G1] DFS｜现金毛覆盖｜1.33季｜季度化采购承诺｜约',
          trace_lines=['轨迹：现金毛覆盖约1.33季'])
    check('W1b fix 1: 思路 slot binds 1.33季 to DFS, 正文 clean: PASS, a 思路 diagnostic (would be hard), the trace '
          'line propagates', r['verdict'] == 'PASS' and not r['hard']
          and any(f['where'] == '思路' and f['would_be'] == 'hard' for f in r['diagnostics'])
          and r['propagable_trace'] == ['轨迹：现金毛覆盖约1.33季'], str((r['hard'], r['diagnostics']))[:300])
    # W1b fix 2: ordinal quarters, heading numbers, unit spellings
    u5_base = ('### 2.2 H集团借融资子公司扩表放贷，集团现金对采购承诺的毛覆盖仍在一季以上\n\n'
               'H集团通过全资子公司H Capital向下游设备买方提供分期融资。据H集团截至2026年8月31日的2027财年第一财季季报，'
               'H Capital单季新发放融资由上年同期的$1.6bn增至$4.9bn。同期期末现金$8.24bn对含跨年采购义务总额$27.5bn的'
               '纯现金口径覆盖率为0.30x，现金毛覆盖约1.20季。')
    r = V(u5_base, u5_base + '现金对采购承诺的覆盖仍在一季以上。')
    check('W1b fix 2: 第一财季 is a period, the heading holds 一季以上: no G-UNIT, no G-NEWNUM',
          not ({'G-UNIT', 'G-NEWNUM'} & set(codes(r) + codes(r, 'cand'))), json.dumps(r['hard'], ensure_ascii=False)[:300])
    b_sp = '关联项目债利差已由发行时的329bp走阔至416bp，指数债约$117.2bn，杠杆约4.5x。'
    r = V(b_sp, '关联项目债利差已由发行时的329个基点走阔至416个基点，指数债约1172亿美元，杠杆约4.5倍。')
    check('W1b fix 2: unit spellings 329bp = 329个基点, $117.2bn = 1172亿美元, 4.5x = 4.5倍: no hard finding',
          r['verdict'] != 'HARD_REJECT', json.dumps(r['hard'], ensure_ascii=False)[:300])
    r = V(b_sp, '关联项目债利差已由发行时的329bp走阔至416bp，指数债约117.2亿美元，杠杆约4.5x。')
    check('W1b fix 2: a 10x slip $117.2bn -> 117.2亿美元 is still HARD_REJECT', r['verdict'] == 'HARD_REJECT',
          str(codes(r)))
    check('W1b fix 2: 同一财季 holds no number', not value_tokens('同一财季，DFS单季新发放融资升至$7.5bn')[0]['tok'].endswith('财季'),
          str([t['tok'] for t in value_tokens('同一财季，DFS单季新发放融资升至$7.5bn')]))
    # W1b fix 3: the 名字表 (CJK names, quoted full names) in the lexicon; a name-table entity is a proper holder
    nt = ('## 名字表\n\n| 名字 | 指什么与口径 | 本篇写法 | 不许用的叫法 |\n|---|---|---|---|\n'
          '| H集团 | 合并口径的集团 | H集团 | “H公司” |\n| H Capital | H集团的全资融资子公司 | H Capital | “H金融” |\n'
          '| 平台 | 甲省城投平台（第一次写全称“甲省城投平台”） | 平台 | “城投公司” |\n'
          '| 对冲比率 | 美元资产的外汇对冲比率 | 对冲比率 | “对冲率” |\n')
    names, aliases, proper = name_table(nt)
    check('W1b fix 3: name table: H集团 and 平台 are proper entities, 甲省城投平台 aliases 平台, 对冲比率 (a concept) '
          'stays out', {'H集团', 'H Capital', '平台'} <= proper and aliases.get('甲省城投平台') == '平台'
          and '对冲比率' not in names, str((sorted(names), aliases, sorted(proper))))
    u5_doc = u5_base + '\n\n| H集团（合并口径，2026年8月31日） | $8.24bn | $27.5bn | 0.30x | 约1.20季 |\n'
    tmpd = tempfile.mkdtemp(prefix='ig-selftest-')
    try:
        onp = os.path.join(tmpd, '提纲.md')
        with open(onp, 'w', encoding='utf-8') as fh:
            fh.write(nt)
        lx = build_lexicon([u5_doc, u5_base], onp)
        swap = u5_base.replace('同期期末现金', '同期H Capital期末现金')
        r = verify(u5_base, swap, '', 'rewrite', u5_doc, '', lx)
        check('W1b fix 3: “H Capital期末现金$8.24bn” (the table row binds it to H集团): HARD_REJECT (G-HOLDER)',
              'G-HOLDER' in codes(r), json.dumps(r['hard'] + r['candidates'], ensure_ascii=False)[:300])
        r = verify(u5_base, u5_base.replace('同期期末现金', '同期H集团期末现金'), '', 'rewrite', u5_doc, '', lx)
        check('W1b fix 3: the legal subject H集团: no hard finding', r['verdict'] != 'HARD_REJECT',
              json.dumps(r['hard'], ensure_ascii=False)[:300])
        r = verify(u5_base, u5_base, '', 'rewrite', u5_doc, '', lx)
        check('W1b fix 3: identity with the name table: PASS', r['verdict'] == 'PASS',
              json.dumps(r['hard'] + r['candidates'], ensure_ascii=False)[:300])
    finally:
        import shutil
        shutil.rmtree(tmpd, ignore_errors=True)
    # W1b fix 4: semantic candidates (never hard) and the narrowed trace split
    def sem(base, body, code, field):
        rr = V(base, body)
        hit = [f for f in rr['candidates'] if f['code'] == code and f['field'] == field and f.get('class') == 'semantic']
        return rr['verdict'] == 'PUBLISH_WITH_CANDIDATES' and bool(hit), json.dumps(rr['hard'] + rr['candidates'],
                                                                                     ensure_ascii=False)[:300]
    ba = '甲公司收入增长10%，利润增长8%。乙公司现金流稳定。'
    check('W1b fix 4a: a new number-free paragraph opening: G-ADDED candidate',
          *sem(ba, '利润端的改善由定价权驱动。甲公司收入增长10%，利润增长8%。乙公司现金流稳定。', 'G-ADDED', 'claim'))
    check('W1b fix 4b: a citation date B and C lack: G-CITE candidate',
          *sem('据Morgan Stanley报告，Oracle的利差走阔至416bp。', 'Oracle的利差走阔至416bp（Morgan Stanley，2026年11月10日）。',
               'G-CITE', 'attribution'))
    check('W1b fix 4c: 前者／后者 after the antecedent pair was reordered: G-REF antecedent candidate',
          *sem('Oracle与CoreWeave都在加杠杆。前者靠发债，后者靠GPU抵押贷款。',
               'CoreWeave与Oracle都在加杠杆。前者靠发债，后者靠GPU抵押贷款。', 'G-REF', 'antecedent'))
    check('W1b fix 4d: an added 只 the base sentence lacks: G-MODAL candidate',
          *sem('循环额度服务于日常流动性，不能用来偿还过桥贷款。', '循环额度只用于日常流动性，不能用来偿还过桥贷款。',
               'G-MODAL', 'certainty'))
    check('W1b fix 4e: the base sentence\'s 将 dropped (a forecast read as fact): G-QUAL candidate',
          *sem('若需求放缓，银行建设贷与GPU抵押贷款将最先触发停提。', '若需求放缓，银行建设贷与GPU抵押贷款最先触发停提。',
               'G-QUAL', 'qualifier'))
    r = V(b59, head + tail.replace('现金毛覆盖约1.33季', '其现金毛覆盖约1.33季'), doc=doc,
          trace_lines=['轨迹：Dell与DFS的4家同业口径分开写', '轨迹：现金毛覆盖约1.33季'])
    check('W1b fix 4f: trace split narrowed: a pronoun candidate open, a line naming two entities and a small count '
          'propagates; the line with the candidate\'s 1.33季 is quarantined',
          r['propagable_trace'] == ['轨迹：Dell与DFS的4家同业口径分开写'] and len(r['quarantined_trace']) == 1,
          str((r['propagable_trace'], r['quarantined_trace'], codes(r, 'cand'))))
    # lint
    draft = '我们判断外部融资压力正在逐级下沉。前三项指标仍在扩张。'
    fl = ('### N1\n**裁定**：只改点名的句子。\n- | F1 | open | “前三项指标仍在扩张”应改为前三项上调、第四项下调 |\n'
          '- | F2 | open | “我们判断外部融资压力正在逐级下沉”拆成两句 |\n- | F3 | open | 不写“落回” |\n')
    lr = lint(fl, draft, node='N1')
    txt = lr['text']
    check('G1 lint: direction prescription stripped and routed; split kept; ban kept', '上调' not in txt
          and '拆成两句' in txt and '不写“落回”' in txt and len(lr['questions']) == 1 and lr['residual'] == 0,
          txt + json.dumps(lr['questions'], ensure_ascii=False)[:300])
    rl = ('## 1（K-cold-x）\n\n- quote (exact): 前三项指标仍在扩张\n- rule: V26\n- problem: The basis is unclear.\n'
          '- fix: Delete the sentence, or replace it with “前三项指标的融资规模同比上调”.\n- sev: B\n\n'
          '## 2（K-struct-x）\n\n- quote (exact): 我们判断外部融资压力正在逐级下沉\n- rule: C01\n'
          '- problem: Two judgments in one sentence.\n- fix: Split it into two sentences.\n- sev: B\n')
    lr = lint(rl, draft)
    e1, e2 = lr['entries']
    check('G1 lint (ruling format): replacement stripped, delete kept; a pure split untouched; residual 0',
          'Delete the sentence' in e1['fix'] and '上调' not in e1['fix'] and e2['fix'] == 'Split it into two sentences.'
          and lr['residual'] == 0 and len(lr['questions']) == 1, json.dumps(lr['entries'], ensure_ascii=False)[:400])
    # trace split
    r = V(b63, '交付前合同资产$858.6mn减去定金与递延收入$754mn后，净垫资达$739mn。',
          trace_lines=['轨迹：净垫资$739mn', '轨迹：下称Bloom为承接方'])
    check('trace split: a line with a token of a hard finding is quarantined, a clean line propagates',
          r['propagable_trace'] == ['轨迹：下称Bloom为承接方'] and len(r['quarantined_trace']) == 1,
          str((r['propagable_trace'], r['quarantined_trace'])))
    # U5a
    before = '甲公司收入增长10%。乙公司现金流稳定。'
    r = V(before, '甲公司收入增长10%，这一点非常重要而且值得注意。乙公司现金流稳定。', before=before, grade='B')
    check('U5a: a B-grade patch that grows -> retry', not r['u5a']['ok'] and r['retry'][0]['code'] == 'U5a',
          str(r.get('u5a')))
    base_u = '甲公司收入增长10%，利润增长8%。乙公司现金流稳定。'
    r = V(base_u, '甲公司收入增长10%，利润增长8%。乙公司现金流稳定。', before=before, grade='B')
    check('G6 then U5a: restoring a lost fact is not growth', r['u5a']['ok'] and r['u5a']['recovered'],
          str(r.get('u5a')))
    # 1.2.0 (W4b review fixes)
    r = V('甲公司本季净流入20亿美元，较上季增长5%。', '甲公司本季净流入-20亿美元，较上季增长5%。',
          trace_lines=['轨迹：净流入-20亿美元'])
    check('F12 20亿美元 -> -20亿美元: HARD_REJECT (G-SIGN), the trace line quarantined', 'G-SIGN' in codes(r)
          and not r['propagable_trace'], str(codes(r)) + str(r['quarantined_trace']))
    b_neg = '甲公司本季净流出-20亿美元，较上季增长5%。'
    r1, r2 = V(b_neg, b_neg.replace('-20亿美元', '20亿美元')), V(b_neg, b_neg.replace('-20亿美元', '+20亿美元'))
    check('F12 -20 -> 20 and -20 -> +20: HARD_REJECT (G-SIGN); identity with the minus: PASS', 'G-SIGN' in codes(r1)
          and 'G-SIGN' in codes(r2) and V(b_neg, b_neg)['verdict'] == 'PASS', str((codes(r1), codes(r2))))
    r = V('甲公司的利率降至5.2%，乙公司持平。', '甲公司的利率为5.2%，乙公司持平。')
    r2 = V('甲公司收入增长20%。', '甲公司收入下降20%。')
    check('F12 a direction word\'s minus still matches the bare number (降至5.2% -> 为5.2%: PASS); 增长20% -> '
          '下降20%: a G-SIGN candidate, not hard', r['verdict'] == 'PASS' and r2['verdict'] != 'HARD_REJECT'
          and 'G-SIGN' in codes(r2, 'cand'), str((codes(r), codes(r2, 'cand'))))
    bg = '我们自算设备投资自峰值降$78.9bn、占GDP的−0.76%，国内净拖累仅−0.25%。'
    ng = '设备投资自峰值降$78.9bn、占GDP−0.76%，国内净拖累−0.25%。'
    check('F12 a minus right after a Latin letter (GDP−0.76%) is read either way: no G-SIGN in both directions '
          '(Wave-2 N4.4.2 false reject)', 'G-SIGN' not in codes(V(bg, ng)) + codes(V(ng, bg)),
          str((codes(V(bg, ng)), codes(V(ng, bg)))))
    lx = build_lexicon(['甲公司收入为20亿美元。'])
    r = verify('甲公司收入为20亿美元。', '甲公司收入为30亿美元。', '', 'rewrite', None, '乙公司收入为30亿美元。', lx)
    r2 = verify('甲公司收入为20亿美元。', '甲公司收入为30亿美元。', '', 'draft', None, '乙公司收入为30亿美元。', lx)
    check('F13 rewrite: a number found only in C is new (HARD_REJECT G-NEWNUM); draft still reads C (no G-NEWNUM)',
          'G-NEWNUM' in codes(r) and 'G-NEWNUM' not in codes(r2) + codes(r2, 'cand'), str((codes(r), codes(r2))))
    bp = '据H集团2027财年第一财季季报，H Capital单季新发放融资由上年同期的$1.6bn增至$4.9bn。'
    r = V(bp, bp.replace('第一财季', '第四财季'), trace_lines=['轨迹：第四财季口径', '轨迹：H Capital口径分开'])
    check('F14 第一财季 -> 第四财季 in the anchored sentence: HARD_REJECT (G-PERIOD), the trace line naming it '
          'quarantined', 'G-PERIOD' in codes(r) and r['propagable_trace'] == ['轨迹：H Capital口径分开'],
          str((codes(r), r['quarantined_trace'])))
    r2 = V(bp, bp.replace('第一财季', 'Q1'))
    r3 = V('公司收入增长5%。', '公司三季度收入增长5%。', trace_lines=['轨迹：三季度增长', '轨迹：别的'])
    check('F14 第一财季 = Q1: PASS; a period the base lacks: a G-PERIOD candidate that quarantines only the line '
          'naming it', r2['verdict'] == 'PASS' and 'G-PERIOD' in codes(r3, 'cand') and 'G-PERIOD' not in codes(r3)
          and r3['propagable_trace'] == ['轨迹：别的'], str((codes(r2), codes(r3, 'cand'), r3['propagable_trace'])))
    br = ('私募信贷违约率升至5.2%（穆迪，10月30日），四类机构即BDC、保险、养老金和主权基金都受影响，敞口集中在软件贷款。\n\n'
          '第二段说明敞口集中在软件贷款，规模有限。')
    lost = br.replace('（穆迪，10月30日）', '').replace('四类机构即BDC、保险、养老金和主权基金', '多类机构')
    kept = ('私募信贷违约率升至5.2%，多类机构都受影响。\n\n据穆迪10月30日的数据，BDC、保险、养老金和主权基金都有敞口，'
            '敞口集中在软件贷款，规模有限。')
    r = V(br, lost, relocation=True)
    hit = [f for f in r['candidates'] if f['code'] == 'G-RELOC']
    check('F03 rewrite relocation: a source, date and list items gone from the whole node -> a G-RELOC semantic '
          'candidate (PASS before 1.2.0); moved within the node, listed in 开头后移, or relocation off: none',
          hit and hit[0].get('class') == 'semantic' and '穆迪' in hit[0]['why'] and 'BDC' in hit[0]['why']
          and 'G-RELOC' not in codes(V(br, kept, relocation=True), 'cand')
          and 'G-RELOC' not in codes(V(br, lost, think='开头后移：穆迪、10月30日、BDC、保险、养老金和主权基金 → N2',
                                       relocation=True), 'cand')
          and 'G-RELOC' not in codes(V(br, lost), 'cand') and V(br, br, relocation=True)['verdict'] == 'PASS',
          json.dumps(r['candidates'], ensure_ascii=False)[:300])
    dr = '美联储持有的国债占比为12%（10月30日）。第二句照旧。'
    rl2 = ('## 1（核对席）\n\n- quote (exact): 美联储持有的国债占比为12%\n- rule: tie-out\n- problem: 数与来源不符。\n'
           '- fix: 把12%改为13%（来源C：H.8，10月30日）\n- sev: A\n\n## 2（K-cold-x）\n\n- quote (exact): 第二句照旧\n'
           '- rule: V26\n- problem: x\n- fix: 把12%改为13%\n- sev: B\n')
    bc = 'H.8显示，美联储持有的国债占比为13%（10月30日）。'
    lr = lint(rl2, dr, base=bc)
    e1, e2 = lr['entries']
    lr3 = lint(rl2.replace('13%（来源C', '14%（来源C'), dr, base=bc)
    check('F02 lint: a tie-out seat\'s fix with 13% verified in B/C stays whole; a cold reader\'s same fix and an '
          'unverified 14% are stripped and routed; residual 0', '13%' in e1['fix'] and e1.get('tieout_verified')
          and not e2['fix'] and len(lr['questions']) == 1 and lr['residual'] == 0
          and '14%' not in lr3['entries'][0]['fix'] and lr3['residual'] == 0,
          json.dumps(lr['entries'], ensure_ascii=False)[:300])
    # W4c (the re-read residuals F01 F02 F03 F05 F06 F08; F06 is in inline-seat/selftest.py)
    b3, n3 = '甲公司本季净流入20亿美元。', '甲公司本季净流入负20亿美元。'
    r1, r2 = V(b3, n3), V(n3, b3)
    r3, r4 = V('实际利率为负1.2%。', '实际利率为-1.2%。'), V('实际利率为-1.2%。', '实际利率为负1.2%。')
    r5 = V('实际利率为1.2%。', '实际利率为负1.2%。')
    nz = '出口负增长5%，负债3亿元。'
    check('W4c F03 负 before the number is an explicit minus: 20亿美元 <-> 负20亿美元 and 1.2% -> 负1.2% HARD_REJECT '
          '(G-SIGN); 负1.2% <-> -1.2% PASS; 负增长5%, 负债3亿元 unchanged: PASS', all('G-SIGN' in codes(x)
                                                                                   for x in (r1, r2, r5))
          and r3['verdict'] == r4['verdict'] == 'PASS' and V(nz, nz)['verdict'] == 'PASS',
          str([(codes(x), x['verdict']) for x in (r1, r2, r3, r4, r5)]))
    b8 = '甲公司本季净流入20亿美元。甲公司本季投资收益为-20亿美元。'
    r = V(b8, b8.replace('净流入20亿美元', '净流入-20亿美元'), trace_lines=['轨迹：净流入-20亿美元'])
    r2 = V(b8, b8.replace('收益为-20亿美元', '收益为20亿美元'))
    check('W4c F08 the sign is checked against the anchored sentence first: 净流入20亿美元 -> -20亿美元 while B also '
          'holds 投资收益为-20亿美元: HARD_REJECT (G-SIGN), the trace line quarantined; the reverse flip too; identity '
          'PASS', 'G-SIGN' in codes(r) and not r['propagable_trace'] and 'G-SIGN' in codes(r2)
          and V(b8, b8)['verdict'] == 'PASS', str((codes(r), codes(r2), r['propagable_trace'])))
    b1 = '甲公司第一财季收入为20亿美元。第四财季将公布全年展望。'
    r = V(b1, b1.replace('第一财季', '第四财季'), trace_lines=['轨迹：第四财季收入20亿美元', '轨迹：别的'])
    check('W4c F01 第一财季 -> 第四财季 in the anchored sentence while another base sentence names 第四财季: '
          'HARD_REJECT (G-PERIOD), the line naming it quarantined; identity PASS', 'G-PERIOD' in codes(r)
          and r['propagable_trace'] == ['轨迹：别的'] and V(b1, b1)['verdict'] == 'PASS',
          str((codes(r), r['propagable_trace'])))
    r = V('PPI同比上涨2.8%。', 'PPI−2.8%。')
    hit = [f for f in r['candidates'] if f['code'] == 'G-SIGN' and f.get('class') == 'semantic']
    check('W4c F05 PPI同比上涨2.8% -> PPI−2.8% (a minus after a Latin letter): not hard, a semantic G-SIGN candidate; '
          'the Wave-2 N4.4.2 pair (GDP−0.76% both sides): no G-SIGN candidate', r['verdict'] != 'HARD_REJECT'
          and hit and 'G-SIGN' not in codes(V(bg, ng), 'cand') + codes(V(ng, bg), 'cand'),
          str((r['verdict'], codes(r, 'cand'), codes(V(bg, ng), 'cand'))))
    fn = ('### N1.1\n\n**裁定**：只改点名的句子。\n\n- [核对席] “美联储持有的国债占比为12%”中的12%改为13%（来源C：H.8）\n'
          '- “第二句照旧”中的12%改为13%\n| （核对席） | “美联储持有的国债占比为12%”中的12%改为13% |\n'
          '- [tie-out] “第二句照旧”中的12%改为14%\n')
    lr = lint(fn, dr, base=bc)
    tl = lr['text'].split('\n')
    check('W4c F02 by-node lint: a [核对席] bullet and a （核对席） row whose 13% is verified in B/C stay whole; the '
          'untagged same fix and a [tie-out] 14% are routed; residual 0; the ### heading kept',
          tl[0] == '### N1.1' and tl[4] == fn.split('\n')[4] and tl[6] == fn.split('\n')[6]
          and '13%' not in tl[5] and '14%' not in tl[7] and lr['stats'].get('tieout_verified') == 2
          and len(lr['questions']) == 2 and lr['residual'] == 0, json.dumps(lr, ensure_ascii=False)[:400])
    rcb = recompute('门槛约合$29–35bn，占比25%', '', 'rewrite', '门槛约合$29–35bn。')
    rcn = recompute('净流入-20亿美元', '', 'rewrite', '净流入20亿美元。')
    check('F16 recompute --base: 25% and an explicit -20亿美元 the base lacks are listed (base_ok false); the base\'s '
          'own tokens pass', rcb['new_tokens'] == ['25%'] and not rcb['base_ok'] and rcn['new_tokens'] == ['-20亿美元']
          and recompute('门槛约合$29–35bn', '', 'rewrite', '门槛约合$29–35bn。')['base_ok'], str((rcb, rcn)))
    tmpd = tempfile.mkdtemp(prefix='ig-lock-')
    try:
        import subprocess
        import time
        accd = os.path.join(tmpd, 'acceptance')
        os.makedirs(accd)
        accp = os.path.join(accd, 'N1.json')
        with open(accp, 'w', encoding='utf-8') as fh:
            json.dump({'node': 'N1', 'propagable_trace': [], 'quarantined_trace': ['轨迹：x']}, fh)
        with open(os.path.join(accd, '.N1.lock'), 'a') as lf:
            fcntl.flock(lf, fcntl.LOCK_EX)
            pp = subprocess.Popen([sys.executable, os.path.abspath(__file__), 'release-trace', accp, '--all'],
                                  stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            time.sleep(1.0)
            waited = pp.poll() is None and json.load(open(accp, encoding='utf-8'))['quarantined_trace'] == ['轨迹：x']
            fcntl.flock(lf, fcntl.LOCK_UN)
        pp.communicate(timeout=60)
        acc_after = json.load(open(accp, encoding='utf-8'))
        check('F07 release-trace waits on acceptance/.N1.lock (the node lock of publication), then moves the line',
              waited and pp.returncode == 0 and acc_after['propagable_trace'] == ['轨迹：x']
              and node_lock_path(accp) == os.path.join(accd, '.N1.lock'), str(acc_after))
    finally:
        import shutil
        shutil.rmtree(tmpd, ignore_errors=True)
    # 1.3.0 (W1-0to1: 算在树上，叶席零新数): the empty-base draft, derivations under the context rule, G-DERIV
    c0 = '据甲公司2025年年报，甲公司2025年总收入为120亿美元，其中海外收入44.4亿美元。'
    d1 = {'id': 'D1', 'node': 'N1', 'metric': '占比', 'value': '37%', 'denominator': '总收入', 'basis': '2025年',
          'operands': [{'name': '海外收入', 'value': '44.4亿美元', 'anchor': 'C1'},
                       {'name': '总收入', 'value': '120亿美元', 'anchor': 'C1'}],
          'expr': '44.4亿美元 / 120亿美元 = 37%', 'signed': True,
          'raw': '- 算式 D1｜海外收入占比｜44.4亿美元/120亿美元 = 37%｜分母 总收入｜已签'}

    def D(body, rows=(), src=c0, base=''):
        return verify(base, body, '', 'draft', None, src, build_lexicon([base, base, src]), rows=rows)

    r = D('甲公司2025年总收入为120亿美元，其中海外收入44.4亿美元。')
    sc = scan(c0 + '\n\n' + d1['raw'] + '\n\n消歧：“其中海外收入44.4亿美元”')
    check('W1-0to1 empty base + C: a body restating C passes (PASS); verify on base None and scan of an empty base or '
          'of C + 算式 raw line + 消歧 quote run (3 sentences, all with numbers)', r['verdict'] == 'PASS'
          and verify(None, '甲公司海外收入44.4亿美元。', '', 'draft', None, c0)['verdict'] != 'HARD_REJECT'
          and scan('')['summary']['sentences'] == 0 and sc['summary']['sentences'] == 3
          and sc['summary']['with_numbers'] == 3, json.dumps(r['hard'] + r['candidates'], ensure_ascii=False)[:300]
          + str(sc['summary']))
    r1, r2, r3 = D('甲公司海外收入占比37%。', [d1]), D('甲公司海外收入占总收入的37%。', [d1]), \
        D('甲公司海外收入占总收入的比重，2025年为37%。', [d1])
    check('W1-0to1 a signed derivation in its context attests 37%: 占比37%, 占总收入的37%, and a bare clause whose '
          'sentence holds 占…总收入 (no hard finding, no G-NEWNUM)',
          all(x['verdict'] != 'HARD_REJECT' and 'G-NEWNUM' not in codes(x, 'cand') for x in (r1, r2, r3)),
          str([(codes(x), codes(x, 'cand')) for x in (r1, r2, r3)]))
    r = D('甲公司利润率37%。', [d1])
    rr = D('甲公司利润率37%。', [d1], src=c0 + '\n' + d1['raw'])
    rg = D('甲公司总收入同比增长37%。', [d1])
    g = [f for f in r['hard'] if f['code'] == 'G-DERIV']
    check('W1-0to1 wrong metric: row 占比/总收入 37%, body 利润率37%: HARD_REJECT (G-DERIV, the why names both); the '
          'row\'s raw line copied into C still rejects; 总收入同比增长37% (比 of a comparison is no share cue) rejects',
          r['verdict'] == 'HARD_REJECT' and g and '占比' in g[0]['why'] and '利润率' in g[0]['why']
          and 'G-DERIV' in codes(rr) and rg['verdict'] == 'HARD_REJECT',
          json.dumps(r['hard'], ensure_ascii=False)[:300] + str((codes(rr), codes(rg))))
    r = D('甲公司海外收入占比37%。', [dict(d1, signed=False)])
    check('W1-0to1 an unsigned derivation attests nothing: HARD_REJECT (G-NEWNUM)', r['verdict'] == 'HARD_REJECT'
          and 'G-NEWNUM' in codes(r) and 'unsigned' in json.dumps(r['hard'], ensure_ascii=False), str(codes(r)))
    r = D('甲公司海外收入增长15%。', [d1])
    check('W1-0to1 an unattested metric number in a draft (empty base): HARD_REJECT (G-NEWNUM)',
          r['verdict'] == 'HARD_REJECT' and 'G-NEWNUM' in codes(r), str(codes(r)))
    # W4a (Stage-2 hotfix, C1–C4): the W3b false positives, against English C lines of the W3b shape
    cw = ('1. Over the two weeks ended July 1, 2026, ON RRP balances fell `$140bn`; funds bought 4-week and 8-week '
          'T-bills; three-month basis widened; 7-day operations; the projected 30-day net cash outflow (`estimated at '
          '$520bn`); 30 calendar days; two (2) calendar months; five business days; a 90-day bill; the 3-Year Note.\n'
          '2. The `25` reporting primary dealers held `$286bn`; `$585bn`, `$120.5bn`, `$64.0tn`, `$4.8bn`, JPY 96.0tn; '
          'the prior day\'s principal; checks on both dates; foreign holdings fell over the four weeks ended July 15.\n'
          '3. Under Section 301(c) of the Protocol and Clause 8.2, Article 4(2), IFRS 9, Pillar-1, Form FR 2004, FR Y-9C '
          'and H.4.1, Treasury holds cash.\n'
          '4. July auctions: ⏎ | Tenor | Offering Size (`$bn`) | Tail vs When-Issued (`bp`) | Allotment (`%`) | ⏎ '
          '|---|---|---|---| ⏎ | 10-Year Note | 39.0 | +1.1 | 16.5% | ⏎ | 20-Year Bond | 13.0 | +3.4 | 24.6% |\n')
    good = ('截至7月1日的两周内，ON RRP余额减少$140bn，资金买入4周、8周T-bill。三个月基差走阔，7天操作照常。恢复日后30天'
            '预计净现金流出估算为5,200亿美元，即30个日历日。两个日历月内，5个工作日内，90天票据，3年期票据。25家一级交易商'
            '持有2,860亿美元。5,850亿美元、1,205亿美元、64万亿美元、48亿美元、96万亿日元。恢复日前一日的本金，两日都满足。'
            '四周内外国官方持仓下降。七月拍卖中，20年期获配130亿美元，尾差3.4个基点；10年期尾差1.1bp。TGA不得高于301(c)'
            '条款的上限，见Clause 8.2与Article 4(2)，按IFRS 9与Pillar-1，据Form FR 2004、FR Y-9C与H.4.1。')
    r = D(good, src=cw)
    hard_tok = [t for f in r['hard'] for t in re.findall(r'[:：]\s*(\S+)$', f['why'])]
    check('W4a C1–C4: tenors and durations (两周, 4周, 三个月, 7天, 30天, 30个日历日, 两个日历月, 5个工作日, 90天, 3年期, 四周), '
          'counts (25家), the prior day (前一日), both dates (两日), months (七月), magnitudes ($585bn = 5,850亿美元, $64.0tn '
          '= 64万亿美元, JPY 96.0tn = 96万亿日元), identifiers (301(c)条款, Clause 8.2, Article 4(2), IFRS 9, Pillar-1, FR '
          '2004, FR Y-9C, H.4.1) and table header units (130亿美元, 3.4个基点, 1.1bp): no G-NEWNUM at all',
          'G-NEWNUM' not in codes(r) + codes(r, 'cand') and r['verdict'] != 'HARD_REJECT',
          json.dumps([f['why'][-40:] for f in r['hard'] + r['candidates'] if f['code'] == 'G-NEWNUM'],
                     ensure_ascii=False)[:600] + str(hard_tok))
    bad = [('增速12%', '甲公司增速12%。'), ('6个月', '六个月基差走阔。'), ('30个工作日', '30个工作日内偿还。'),
           ('5天 (five business days)', '5天内结算。'), ('96万亿美元 (C: JPY)', '寿险持有96万亿美元。'),
           ('39亿美元 (table 39.0 $bn)', '10年期获配39亿美元。'), ('4.1bp (table +1.1)', '10年期尾差4.1bp。'),
           ('26家', '26家一级交易商持仓。'), ('301bn (Section 301)', '余额为$301bn。')]
    miss = [lab for lab, b in bad if 'G-NEWNUM' not in codes(D(b, src=cw))]
    check('W4a C1–C4 keep the guard: an unattested metric (增速12%), a tenor C lacks (六个月), a qualified day that is not '
          'C\'s (30个工作日 vs 30 calendar days; 5天 vs five business days), a currency swap (96万亿美元 vs JPY 96.0tn), a '
          'mis-scaled table cell (39亿美元 vs 39.0 $bn), a cell C lacks (4.1bp), a count C lacks (26家) and a metric '
          'reusing an identifier digit ($301bn) all stay HARD_REJECT (G-NEWNUM)', not miss, str(miss))
    rd = D('甲公司利润率37%。', [d1], src=c0 + '\n' + cw)
    check('W4a C1–C4 leave the derivation context rule alone: 利润率37% against a 占比 row still HARD_REJECT (G-DERIV)',
          rd['verdict'] == 'HARD_REJECT' and 'G-DERIV' in codes(rd), str(codes(rd)))
    # 1.3.2 (W4b): the core noun of a decorated metric/denominator (anchor, literal, scope note stripped)
    d2 = dict(d1, id='D2', metric='海外收入占比@甲档:L04（折年口径）',
              denominator='总收入$120亿美元@甲档:L04（折年口径，不含利润率口径）')
    d3 = dict(d1, id='D3', metric='海外收入占主营收入的比重', value='37%',
              denominator='合并营业收入80.0亿元@丙档:L12（不含其他业务收入6.0亿元@丙档:L13）')
    rp = [D(b, [x]) for b, x in (('甲公司海外收入占比37%。', d2), ('甲公司海外收入占总收入的37%。', d2),
                                 ('海外收入占这笔合并营业收入的37%。', d3),
                                 ('与主营收入里37%的海外占比分属两个口径。', d3))]
    check('W4b 1.3.2 core noun: a signed row whose metric/denominator carries @甲档:L04, a value literal and （折年口径） '
          'attests 37% when the clause names the core metric (海外收入占比) or the core denominator with a share cue '
          '(占总收入, 占…合并营业收入, 主营收入…占比 from X占Y的比重): no hard finding, 37% no G-NEWNUM',
          all(x['verdict'] != 'HARD_REJECT' and not any(f['code'] == 'G-NEWNUM' and '37' in f['why']
                                                         for f in x['candidates']) for x in rp)
          and core_term(d2['denominator']) == '总收入' and core_term(d3['denominator']) == '合并营业收入' and core_term('占比（折年）@A:L1') == '占比',
          str([(codes(x), codes(x, 'cand')) for x in rp]) + core_term(d3['denominator']))
    d4 = dict(d1, id='D4', metric='占比（折年）@A:L1', denominator='总收入@A:L1（折年）')
    rn = [D(b, [x]) for b, x in (('甲公司利润率37%。', d4), ('甲公司利润率37%。', d2),
                                 ('国内收入占比37%。', dict(d1, metric='占比（海外收入/总收入）', denominator=None)),
                                 ('其他业务收入占比37%。', dict(d3, metric='主营收入比重')),
                                 ('其他业务收入为37%。', d3))]
    d5 = dict(d1, id='D5', metric='子公司合计', value='3家', denominator=None, signed='待核',
              expr='甲子公司2家@甲档:L3+乙子公司1家@甲档:L4＝3家')
    d6 = dict(d1, id='D6', metric='新到期日', value='2027年3月31日', denominator=None, signed=False,
              expr='到期日2026年12月31日@甲档:L5+展期3个月@甲档:L6＝2027年3月31日')
    ru, rv, rw = D('甲公司子公司合计3家。', [d5]), D('新到期日为2027年3月31日。', [d6]), D('甲公司覆盖3家客户。', [d1])
    rx = D('甲公司2027年起执行新到期安排。', [d6])
    check('W4b 1.3.2 an unsigned 算式 row is no exemption for its date or small count: 子公司合计3家 and a date roll-'
          'forward 2027年3月31日 held only by unsigned rows are HARD_REJECT (G-NEWNUM, V26); a small count no row holds, '
          'and a part of the row value (2027年 of 2027年3月31日), stay candidates', ru['verdict'] == 'HARD_REJECT' and 'G-NEWNUM' in codes(ru)
          and rv['verdict'] == 'HARD_REJECT' and 'G-NEWNUM' in codes(rv)
          and rw['verdict'] != 'HARD_REJECT' and 'G-NEWNUM' in codes(rw, 'cand') and rx['verdict'] != 'HARD_REJECT',
          str((codes(ru), codes(rv), codes(rw), codes(rw, 'cand'), codes(rx))))
    check('W4b 1.3.2 keeps the guard: 利润率37% against 占比（折年）@A:L1 and against the decorated 海外收入占比 row, '
          '国内收入占比37% against 占比（海外收入/总收入） (a generic core never matches alone), a '
          'scope-note noun (其他业务收入: a 不含 note is no denominator) all stay HARD_REJECT (G-DERIV)',
          all(x['verdict'] == 'HARD_REJECT' and 'G-DERIV' in codes(x) for x in rn), str([codes(x) for x in rn]))
    lx = build_lexicon(['Under Section 301(c) of the Debt-Limit Operating Protocol, Treasury is prohibited.'])
    check('W4a C2: a capitalised phrase ending in a clause word (Under Section) is no lexicon entity (no G-HOLDER '
          'binding to it); the protocol name stays', 'Under Section' not in lx.names
          and 'Debt-Limit Operating Protocol' in lx.names, str(sorted(lx.names)[:6]))
    r = D('甲公司覆盖3类客户，计划于2026年3月披露。甲公司纳入S&P 500。甲公司海外收入约44亿美元。')
    check('W1-0to1 dates, small counts, an identifier (S&P 500) and a same-unit 约 rounding (约44亿美元 <- 44.4亿美元) '
          'stay candidates: PUBLISH_WITH_CANDIDATES, G-NEWNUM candidates, nothing hard', r['verdict'] ==
          'PUBLISH_WITH_CANDIDATES' and 'G-NEWNUM' in codes(r, 'cand') and not r['hard']
          and len([f for f in r['candidates'] if f['code'] == 'G-NEWNUM']) >= 3,
          json.dumps(r['hard'] + r['candidates'], ensure_ascii=False)[:400])
    leg = [{'text': '海外收入占比37%', 'value': '37%'}]
    r, r2 = D('甲公司利润率37%。', leg), V(c0, c0.replace('。', '，利润率37%。'), rows=leg)
    rc1, rc2 = recompute('甲公司利润率37%', '', 'draft', c0, rows=[d1]), recompute('甲公司海外收入占比37%', '', 'draft',
                                                                                 '', rows=[d1])
    check('W1-0to1 legacy text/value rows unchanged (bare value, any context: 利润率37% attested in draft and rewrite); '
          'recompute(rows=) applies the context rule (利润率37%: new, deriv_mismatch; 占比37% on an empty base: base_ok)',
          r['verdict'] != 'HARD_REJECT' and 'G-NEWNUM' not in codes(r2) + codes(r2, 'cand')
          and 'G-NEWNUM' not in codes(D('甲公司海外收入增长15%。', [{'text': 'x', 'value': '15%'}]))
          and 'G-NEWNUM' in codes(D('甲公司海外收入-15%。', [{'text': 'x', 'value': '15%'}]))
          and rc1['new_tokens'] == ['37%'] and rc1.get('deriv_mismatch') and rc2['base_ok'],
          str((codes(r), codes(r2), rc1, rc2)))
    tmpd = tempfile.mkdtemp(prefix='ig-rows-')
    try:
        import contextlib
        import io
        pj, pl, pb, pc = (os.path.join(tmpd, x) for x in ('rows.json', 'rows.jsonl', 'body.md', 'c.md'))
        for p, txt in ((pj, json.dumps([d1], ensure_ascii=False)), (pl, json.dumps(d1, ensure_ascii=False) + '\n'),
                       (pb, '甲公司利润率37%。'), (pc, c0)):
            with open(p, 'w', encoding='utf-8') as fh:
                fh.write(txt)
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            rcs = [main(['verify', '--profile', 'draft', '--sources', pc, '--body', pb, '--rows', x]) for x in (pj, pl)]
            ok_ = main(['verify', '--profile', 'draft', '--sources', pc, '--body', pc, '--rows', pj])
            rw = main(['verify', '--body', pb])
        check('W1-0to1 CLI verify --rows reads a JSON list and JSONL alike (利润率37% -> exit 1 both); no --base in a '
              'draft runs on an empty base (exit 0 on C itself); a rewrite without --base is a usage error (exit 2)',
              rcs == [1, 1] and ok_ == 0 and rw == 2, str((rcs, ok_, rw)))
    finally:
        import shutil
        shutil.rmtree(tmpd, ignore_errors=True)
    ok = all(res) and res
    print('inline_guards self-test: %d of %d PASS' % (sum(res), len(res)))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
