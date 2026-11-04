#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""voice_check.py v4.5 (2026-10-24) -- FICCVoice fingerprint report.

Default mode keeps six hard checks (H1-H6) and the existing result schema,
plus semantic_reviews holding H7 only (v4.3).
With --clarity, H2-H4 are semantic-review candidates, not hard failures;
only H1, H5 and H6 set exit code 1.  The heuristics do not prove clarity.
H7 (cross-paragraph repetition: trigger A long verbatim run, trigger B an
opening that echoes an earlier preview) is a review candidate in both modes
and never sets the exit code.

Density counts never change the exit code.  Handling of the flagged rows
before handoff is defined in references/clarity-acceptance.md; density
rows are report-only.  Since v4.5 the 不是……而是 and
段末升华 rows list each hit's line and quote under the row (text report) and
in density_hits (--json); positions are reporting only.  The author corpus and 2026.02
control columns are descriptive, not evidence that a sentence is clear.

The v4 hazard list (隐患清单) remains report-only: 承前省略, 句首代词,
分句过多, 的≥3, 无施事被动, 而则并且, 双重否定, 名词化, and, with
--names <outline.md>, 名字表禁用词.  It never carries a "！".

Usage:
  voice_check.py <file.md> [--clarity] [--lecture] [--json] [--names OUTLINE.md] [--hazards-only]
  voice_check.py --selftest [--clarity] [--letters PATH]
  voice_check.py --baseline [--letters PATH] [--extra FILE ...] [--per-doc]

Checks (H2-H4 are hard only in the compatibility default):
  H1 internal working labels in the prose: 【S12】, [src:, 〔〕 holding a file
     name or a line marker (〔nine-sections.md〕, 〔L120〕, 〔L12-L30〕, 〔x#L5〕, 〔第3行〕)
  H2 opening that announces the plan (first two paragraphs)
  H3 one-point-per-line tag list (>=3 consecutive marked lines, each <=20 zi)
  H4 paired / antithetical headings
  H5 corner-bracket quotes 「」『』 anywhere in the file (appendix, tables and
     headings included); only fenced code and inline backtick code are skipped
  H6 full-width semicolon ； in a prose line (user ruling 2026-10-17, FICCVoice V07);
     table rows, list rows (-, *, + or 1. / 1．), headings, fenced and inline code
     and anything after the first 附 heading are skipped
  H7 (review only, both modes; same scope as H6; only CJK characters and
     digits are counted) A: two paragraphs share a run of >= H7_MIN_RUN (20)
     counted characters.  B: >= H7_ECHO_GROUP (3) later paragraph openings
     each echo a sentence or clause of the same earlier paragraph (contained,
     or difflib ratio >= H7_ECHO_RATIO 0.75; opening >= H7_ECHO_MIN 8 counted
     characters).  FICCCompose.md C23 check items, C04, C20; a re-mention
     carries one more layer per C07
  H9 (review only, --clarity only, v4.4; trimmed v4.5) nominalized views
     (FICCVoice V57): 读法, 解读, 视角, 判别读数, 推断加强, 判断…加强, 占上风,
     站在…一边 in prose lines (list rows included, inline code masked); one
     entry per hit.  框架, 让步 and 的分量 were removed on 2026-10-24
Current review: FICCVoice.md V02/V10/V13/V25/V37-V40, FICCCompose.md C01
and references/clarity-acceptance.md.  H1 also follows FICCOutline.md 4.2;
H5 follows references/format-and-maintenance.md 1 (user ruling 2026-10-12:
quotes are “”, with ‘’ inside).  H6 follows FICCVoice.md V07 (user ruling
2026-10-17: no semicolons in prose; tables and real lists excepted).
Details: scripts/README.md.
"""
import argparse
import difflib
import io
import json
import os
import re
import sys
import unicodedata

VERSION = '4.5'
VERSION_DATE = '2026-10-24'
HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(HERE)
CORPUS_DIR = os.path.join(SKILL_DIR, 'references', 'corpus')
EXEMPLARS = ['nine-sections.md', 'panda-on-options.md']
DEFAULT_LETTERS = os.path.expanduser(
    '~/ficc-letters/letters.txt')
CONTROL_ISSUE = '2026.02'  # AI-assisted: excluded from the baseline, used as control
DEDUP_ISSUE = '2025.12'    # same text as 《九节》: counted once, via nine-sections.md
SHORT_TEXT = 1500          # below this many CJK chars densities are noisy

# ---------------------------------------------------------------------------
# Baseline (author corpus).  Regenerate with:  voice_check.py --baseline ...
# Per document: count / CJK chars * 10000 over the same scope the checker uses.
# median / p90 = linear interpolation over documents (numpy default method).
# ---------------------------------------------------------------------------
# BEGIN BASELINE
BASELINE = {
    '_meta': {'date': '2026-10-08', 'docs': 82, 'control': '2026.02', 'dedup': '2025.12=nine-sections.md',
              'method': 'per-doc count/CJK*1e4; median & p90 by linear interpolation'},
    'bushi': {'median': 0.00, 'p90': 6.50, 'control': 53.28},
    'dash': {'median': 0.00, 'p90': 0.30, 'control': 0.00},
    'coda': {'median': 0.00, 'p90': 0.00, 'control': 0.00},
    'short3': {'median': 0.00, 'p90': 0.00, 'control': 0.00},
    'filler': {'median': 0.00, 'p90': 2.68, 'control': 5.92},
    'normative': {'median': 0.00, 'p90': 0.00, 'control': 0.00},
    'women': {'median': 79.72, 'p90': 114.79, 'control': 9.87},
    'wo': {'median': 0.00, 'p90': 15.92, 'control': 10.85},
    'paren': {'median': 1.91, 'p90': 10.31, 'control': 0.00},
    'parallel3': {'median': 0.00, 'p90': 0.00, 'control': 10.85},
}
# END BASELINE

METRICS = [
    ('bushi', '不是……而是'),
    ('dash', '破折号——'),
    ('coda', '段末升华'),
    ('short3', '连续三短句'),
    ('filler', '本质上等五词'),
    ('normative', '无人称规范句'),
    ('women', '「我们」'),
    ('wo', '「我」(不含我们)'),
    ('paren', '括号插话'),
    ('parallel3', '三连排比'),
]
LECTURE_SILENT = {'wo', 'paren'}
SEMANTIC_REVIEW_CODES = {'H2', 'H3', 'H4', 'H7', 'H9'}
FLAG_MIN_COUNT = 3  # "一篇里出现一两处是文章" -- one or two hits never get a flag

# ---------------------------------------------------------------------------
# Character helpers
# ---------------------------------------------------------------------------
CJK_RE = re.compile(r'[一-鿿]')
ZI_RE = re.compile(r'[一-鿿A-Za-z0-9]')


def cjk(s):
    """CJK ideographs (the per-10k denominator)."""
    return len(CJK_RE.findall(s))


def zi(s):
    """Length in 'zi': CJK ideographs + ASCII letters/digits; punctuation and spaces excluded."""
    return len(ZI_RE.findall(s))


def dwidth(s):
    return sum(2 if unicodedata.east_asian_width(c) in 'WF' else 1 for c in s)


def pad(s, w, right=False):
    gap = ' ' * max(0, w - dwidth(s))
    return gap + s if right else s + gap


# ---------------------------------------------------------------------------
# Line model
# ---------------------------------------------------------------------------
FENCE_RE = re.compile(r'^\s{0,3}(```|~~~)')
APPENDIX_RE = re.compile(r'^\s{0,3}#{1,2}\s*附')
ATX_RE = re.compile(r'^\s{0,3}(#{1,6})\s+(.*?)\s*#*\s*$')
IMG_RE = re.compile(r'^!\[')
EMPH_RE = re.compile(r'\*\*|__|`')

# Plain-text section lines: 第X章/节/部分, 一、 / 一． / 一， , （一）
PLAIN_HEAD_RE = re.compile(
    r'^(?:(?P<l1>第[一二三四五六七八九十百零〇\d]{1,4}[章节部分篇讲课])[\s：:、．.]*'
    r'|(?P<l2>[一二三四五六七八九十]{1,3}(?:[、，,]|[．.](?!\d)))\s*'
    r'|(?P<l3>[（(][一二三四五六七八九十]{1,3}[）)])\s*)')

# List-item starters for H3 (packet list + bullet glyphs + （1）)
LIST_START_RE = re.compile(
    r'^(?:[-*+](?=\s)|[•·●▪◦‧∙]'
    r'|\d{1,2}[.．](?!\d)|\d{1,2}[、)）]|[（(]\d{1,2}[）)]'
    r'|第[一二三四五六七八九十\d]{1,3}[、，,：:]'
    r'|其[一二三四五六七八九十](?=[、，,：:\s]))\s*')

# Heading ordinal prefixes stripped before H4 comparisons
HEAD_ORD_RE = re.compile(
    r'^(?:第[一二三四五六七八九十百零〇\d]{1,4}[章节部分篇讲课][\s：:、．.]*'
    r'|[一二三四五六七八九十]{1,3}(?:[、，,]|[．.](?!\d))\s*'
    r'|[（(][一二三四五六七八九十\d]{1,3}[）)]\s*'
    r'|\d{1,2}(?:\.\d{1,2})*(?:、|[.．](?!\d))\s*'
    r'|\d{1,2}(?:\.\d{1,2})+\s+)')


class Line(object):
    __slots__ = ('no', 'raw', 'kind', 'content', 'quote', 'level', 'title',
                 'otype', 'starter', 'rest')

    def __init__(self, no, raw, kind, content='', quote=False):
        self.no, self.raw, self.kind, self.content, self.quote = no, raw, kind, content, quote
        self.level = 0
        self.title = ''
        self.otype = ''
        self.starter = ''
        self.rest = ''


def is_table(st):
    return st.startswith('|') or st.count('|') >= 2


def plain_heading(st):
    m = PLAIN_HEAD_RE.match(st)
    if not m:
        return None
    rest = st[m.end():].strip()
    if len(rest.replace(' ', '')) > 40:
        return None
    if re.search(r'[。；;]', rest) or re.search(r'[，,、]$', rest):
        return None
    if m.group('l1'):
        return 11, 'l1', rest
    if m.group('l2'):
        return 12, 'l2', rest
    return 13, 'l3', rest


def split_starter(content):
    """Return (starter, rest) if the line opens with a list marker, else ('', content)."""
    norm = re.sub(r'^(?:\*\*|__)+', '', content)
    m = LIST_START_RE.match(norm)
    if not m:
        return '', content
    rest = EMPH_RE.sub('', norm[m.end():]).strip().lstrip('、，,：:').strip()
    return norm[:m.end()].strip(), rest


def classify(text):
    text = text.lstrip('﻿').replace('\r\n', '\n').replace('\r', '\n')
    text = re.sub(r'<!--.*?-->', lambda m: '\n' * m.group(0).count('\n'), text, flags=re.S)
    lines = []
    in_code = False
    for no, ln in enumerate(text.split('\n'), 1):
        if not in_code and APPENDIX_RE.match(ln):
            break
        if FENCE_RE.match(ln):
            in_code = not in_code
            lines.append(Line(no, ln, 'code'))
            continue
        if in_code:
            lines.append(Line(no, ln, 'code'))
            continue
        st = ln.strip()
        if not st:
            lines.append(Line(no, ln, 'blank'))
            continue
        quote = False
        if st.startswith('>'):
            quote = True
            st = re.sub(r'^(?:>\s?)+', '', st).strip()
            if not st:
                lines.append(Line(no, ln, 'blank', quote=True))
                continue
        if IMG_RE.match(st):
            lines.append(Line(no, ln, 'image', st, quote))
            continue
        if is_table(st):
            lines.append(Line(no, ln, 'table', st, quote))
            continue
        m = ATX_RE.match(st) if not quote else None
        if m:
            L = Line(no, ln, 'heading', st)
            L.level = len(m.group(1))
            L.title = m.group(2)
            lines.append(L)
            continue
        ph = plain_heading(st) if not quote else None
        if ph:
            L = Line(no, ln, 'cand', st)
            L.level, L.otype, L.title = ph
            lines.append(L)
            continue
        L = Line(no, ln, 'prose', st, quote)
        L.starter, L.rest = split_starter(st)
        lines.append(L)
    # Three or more consecutive same-type plain ordinal lines with no prose
    # between them are a list, not headings.
    i, n = 0, len(lines)
    while i < n:
        if lines[i].kind != 'cand':
            i += 1
            continue
        group, j = [lines[i]], i + 1
        while j < n and lines[j].kind in ('blank', 'cand'):
            if lines[j].kind == 'cand':
                if lines[j].otype != group[0].otype:
                    break
                group.append(lines[j])
            j += 1
        if len(group) >= 3:
            for L in group:
                L.kind = 'prose'
                m = PLAIN_HEAD_RE.match(L.content)
                L.starter = L.content[:m.end()].strip()
                L.rest = EMPH_RE.sub('', L.title).strip()
        else:
            for L in group:
                L.kind = 'heading'
        i = j
    return lines


# ---------------------------------------------------------------------------
# Hard failures
# ---------------------------------------------------------------------------
H1_TAG_RE = re.compile(r'【S\d+|〔S\d+〕')
H1_SRC_RE = re.compile(r'\[src:', re.I)
H1_BRACKET_RE = re.compile(r'〔([^〔〕\n]{1,120})〕')
FILE_EXT = (r'(?:md|markdown|txt|py|json|jsonl|csv|tsv|xlsx?|docx?|pdf|html?|ya?ml|'
            r'ipynb|pptx?|png|jpe?g|gif|svg|sh|tex|bib|log)')
H1_FILE_RE = re.compile(r'[\w\-~/]+\.' + FILE_EXT + r'(?![A-Za-z0-9])|~/|\.\.?/|/Users/', re.I)
H1_LINE_RE = re.compile(
    r'(?<![A-Za-z])L\d+\s*[-–—~～至到]\s*L?\d+'
    r'|(?<![A-Za-z])L\d{3,}(?![A-Za-z0-9])'
    r'|#L?\d+'
    r'|[:：]\s*L\d+(?![A-Za-z0-9])'
    r'|第\s*\d+\s*行')

# 本文将/本篇将 count only when an arrangement verb follows: the author's own
# 「本文将大量使用案例而不是公式」(熊猫讲期权 L3) is a promise about method, not a plan.
H2_PHRASE_RE = re.compile(
    r'本文旨在|本篇旨在|本文分(?:为|成|别|[一二三四五六七八九十两\d])|下面将从|以下将从'
    r'|(?:本文|本篇|下文|以下|下面)(?:将|拟)会?'
    r'(?:重点|主要|简要|着重|首先|先|依次|逐一|分别|集中|进一步)?'
    r'(?:从|分[为成别]|围绕|按照?|讨论|探讨|分析|梳理|回顾|介绍|阐述|论述|展开|聚焦|考察|解读|剖析|总结|说明|对)')
H2_SEQ_RE = re.compile(r'首先.*?其次.*?最后')
H2_PART_RE = re.compile(r'第一部分.*?第二部分')

H3_MAX_ZI = 20
H4_MIN_LEN = 6
H4_PATTERNS = [
    (re.compile(r'不是.*?而是'), '标题含「不是……而是」'),
    (re.compile(r'[：:]\s*不是'), '标题含「：不是」'),
    (re.compile(r'(?<![A-Za-z])vs\.?(?![A-Za-z])', re.I), '标题含「vs」'),
]
PUNCT = set('，。、；：？！“”‘’「」『』（）()《》〈〉【】〔〕—…·,.;:?!\'"-/|~～')


def snippet(s, n=60):
    s = s.strip()
    return s if len(s) <= n else s[:n] + '…'


def check_h1(lines):
    out = []
    for L in lines:
        if L.kind != 'prose':
            continue
        c = L.content
        hits = []
        m = H1_TAG_RE.search(c)
        if m:
            hits.append(m.group(0))
        m = H1_SRC_RE.search(c)
        if m:
            hits.append('[src:')
        for bm in H1_BRACKET_RE.finditer(c):
            inner = bm.group(1)
            if H1_FILE_RE.search(inner) or H1_LINE_RE.search(inner):
                hits.append(bm.group(0))
        if hits:
            out.append({'code': 'H1', 'line': L.no, 'quote': L.quote,
                        'desc': '正文出现内部标签：' + '、'.join(hits[:4]),
                        'text': snippet(c)})
    return out


def check_h2(lines):
    paras = [L for L in lines if L.kind == 'prose']
    window = []
    for L in paras[:2] + [P for P in paras if not P.quote][:2]:
        if L not in window:
            window.append(L)
    for L in window:
        m = H2_PHRASE_RE.search(L.content)
        if m:
            return [{'code': 'H2', 'line': L.no, 'quote': L.quote,
                     'desc': '开头交代安排：「%s」' % m.group(0), 'text': snippet(L.content)}]
        if H2_SEQ_RE.search(L.content):
            return [{'code': 'H2', 'line': L.no, 'quote': L.quote,
                     'desc': '开头交代安排：同段「首先……其次……最后」', 'text': snippet(L.content)}]
    joined = ''.join(L.content for L in window)
    if H2_PART_RE.search(joined):
        L = next((P for P in window if '第一部分' in P.content), window[0])
        return [{'code': 'H2', 'line': L.no, 'quote': L.quote,
                 'desc': '开头交代安排：「第一部分……第二部分」', 'text': snippet(L.content)}]
    return []


def check_h3(lines):
    out, run = [], []

    def flush():
        if len(run) >= 3:
            out.append({'code': 'H3', 'line': run[0].no, 'end_line': run[-1].no,
                        'quote': any(L.quote for L in run),
                        'desc': '每点一行的标签清单（连续 %d 行，每行去掉起头后不超过 %d 字）'
                                % (len(run), H3_MAX_ZI),
                        'text': ' / '.join(snippet(L.content, 24) for L in run[:4])})

    for L in lines:
        if L.kind == 'blank':
            continue
        if L.kind == 'prose' and L.starter and L.rest and zi(L.rest) <= H3_MAX_ZI:
            run.append(L)
            continue
        flush()
        run = []
    flush()
    return out


def head_core(title):
    t = EMPH_RE.sub('', title).strip()
    t = HEAD_ORD_RE.sub('', t, count=1).strip()
    return t


def skeleton(core):
    t = core.rstrip('？?！!。：: ')
    return ''.join(c for c in t if c in PUNCT)


def check_h4(lines):
    out = []
    heads = [L for L in lines if L.kind == 'heading']
    prev = {}
    for L in heads:
        core = head_core(L.title)
        for rx, desc in H4_PATTERNS:
            if rx.search(core):
                out.append({'code': 'H4', 'line': L.no, 'quote': False,
                            'desc': '对偶小标题：' + desc, 'text': snippet(L.content)})
                break
        for lv in list(prev):
            if lv > L.level:
                del prev[lv]
        P = prev.get(L.level)
        if P is not None:
            a, b = head_core(P.title), core
            na, nb = a.replace(' ', ''), b.replace(' ', '')
            sk = skeleton(a)
            common = len(os.path.commonprefix([na, nb]))
            if (len(na) == len(nb) >= H4_MIN_LEN and sk and sk == skeleton(b)
                    and common * 2 < len(na)):  # 上篇/下篇 series titles are not couplets
                out.append({'code': 'H4', 'line': L.no, 'quote': False,
                            'desc': '对偶小标题：与 L%d 等长（%d 字）且标点骨架相同（%s）'
                                    % (P.no, len(nb), sk),
                            'text': snippet(P.content, 30) + ' ｜ ' + snippet(L.content, 30)})
        prev[L.level] = L
    return out


H5_RE = re.compile(r'[「」『』]')
H5_CODE_RE = re.compile(r'(`+)[^\n]+?\1')
H5_CTX = 12


def check_h5(text):
    # Whole file, unlike H1-H4: appendix, tables, headings and quote blocks too.
    # Only fenced code and inline backtick code are skipped. One hit per bracket.
    text = text.lstrip('\ufeff').replace('\r\n', '\n').replace('\r', '\n')
    out = []
    in_code = False
    for no, ln in enumerate(text.split('\n'), 1):
        if FENCE_RE.match(ln):
            in_code = not in_code
            continue
        if in_code:
            continue
        masked = H5_CODE_RE.sub(lambda m: ' ' * len(m.group(0)), ln)
        for m in H5_RE.finditer(masked):
            i = m.start()
            out.append({'code': 'H5', 'line': no, 'quote': ln.lstrip().startswith('>'),
                        'desc': '直角引号%s：引号用“”，里层用‘’' % m.group(0),
                        'text': ln[max(0, i - H5_CTX):i + H5_CTX + 1].strip()})
    return out


# H6: full-width semicolon in prose (FICCVoice V07, user ruling 2026-10-17).
# Same scope as H1 (classify: before the first 附 heading; fenced code, tables,
# images and headings already excluded).  Real list rows are exempt: a line that
# opens with -, *, + (followed by a space) or 1. / 1． .  Inline backtick code is
# masked.  One hit per line; the count of ； goes into the description.
H6_RE = re.compile(r'；')
H6_LIST_RE = re.compile(r'^(?:\*\*|__)*(?:[-*+]\s|\d{1,3}[.．](?!\d))')
H6_CTX = 12


def check_h6(lines):
    out = []
    for L in lines:
        if L.kind != 'prose' or H6_LIST_RE.match(L.content):
            continue
        masked = H5_CODE_RE.sub(lambda m: ' ' * len(m.group(0)), L.content)
        hits = [m.start() for m in H6_RE.finditer(masked)]
        if not hits:
            continue
        i = hits[0]
        out.append({'code': 'H6', 'line': L.no, 'quote': L.quote,
                    'desc': '正文分号 %d 处：改成句号、拆成短句（FICCVoice V07；表格行、清单行例外）'
                            % len(hits),
                    'text': L.content[max(0, i - H6_CTX):i + H6_CTX + 1].strip()})
    return out


# H7: verbatim or near-verbatim repetition across paragraphs (v4.3; review only,
# never in `hard`).  FICCCompose.md C23 check items with C04 and C20: a claim or
# carry-over paragraph that previews the later openings word for word is a table
# of contents, not a step on the chain; a re-mention carries one more layer (C07).
# Scope as H6 (classify; list rows skipped too).  A paragraph is a run of
# consecutive prose lines; a blank line or any skipped line (heading, table,
# image, list row, code) ends it, and so does a switch into or out of a quote
# block.  Only CJK characters and digits are counted ("counted text"); Latin
# letters, punctuation, spaces and markup are dropped before comparing.
# Trigger A (long run): two paragraphs share a run of >= H7_MIN_RUN counted
#   characters; 20-gram index on the counted text, one entry per pair, the longest.
# Trigger B (opening echo): the first sentence of a paragraph after the first (up
#   to 。！？； or ：, leading connectives in H7_CONNECTIVES and "，" removed) has
#   >= H7_ECHO_MIN counted characters and is contained in, or has a
#   difflib ratio >= H7_ECHO_RATIO with, a sentence (split on 。！？；：) or a
#   clause (split on ，、) of an earlier paragraph.  Reported only when at least
#   H7_ECHO_GROUP later openings echo the same earlier paragraph (a preview that
#   copies several openings); one entry per pair, the best match; a pair already
#   reported by trigger A is not repeated.
H7_MIN_RUN = 20       # trigger A: counted characters (CJK + digits)
H7_ECHO_MIN = 8       # trigger B: counted characters in the opening
H7_ECHO_RATIO = 0.75  # trigger B: difflib ratio, counted text
H7_ECHO_GROUP = 3     # trigger B: later openings echoing one earlier paragraph
H7_CTX = 30
H7_STRIP_RE = re.compile(r'\s+|\*\*|__|`')
H7_COUNT_RE = re.compile(r'[一-鿿0-9]')
H7_CONNECTIVES = ('更要紧的是', '而且', '所以', '但是', '可是', '既然', '那么', '同时', '其次', '此外',
                  '不过', '因此', '于是', '然而', '先看', '再看', '这个', '第一，', '第二，', '第三，')
H7_OPEN_END_RE = re.compile(r'[。！？；：!?;:]')
H7_SENT_RE = re.compile(r'[。！？；：!?;:]')
H7_CLAUSE_RE = re.compile(r'[，、,]')


def h7_counted(s):
    """-> (counted text, index of each counted character in s)"""
    pos = [i for i, ch in enumerate(s) if H7_COUNT_RE.match(ch)]
    return ''.join(s[i] for i in pos), pos


def h7_strip_lead(s):
    while True:
        t = s.lstrip('，,')
        for c in H7_CONNECTIVES:
            if t.startswith(c):
                t = t[len(c):]
                break
        t = t.lstrip('，,')
        if t == s:
            return s
        s = t


def h7_paragraphs(lines):
    """-> [(first line, last line, quote, text with spaces and markup removed)]"""
    paras, cur = [], None
    for L in lines:
        if L.kind == 'prose' and not H6_LIST_RE.match(L.content):
            t = H7_STRIP_RE.sub('', L.content)
            if cur is not None and cur[2] == L.quote:
                cur[1], cur[3] = L.no, cur[3] + t
                continue
            if cur is not None:
                paras.append(tuple(cur))
            cur = [L.no, L.no, L.quote, t]
            continue
        if cur is not None:
            paras.append(tuple(cur))
            cur = None
    if cur is not None:
        paras.append(tuple(cur))
    return paras


def h7_loc(P):
    return 'L%d' % P[0] + ('–L%d' % P[1] if P[1] != P[0] else '')


def h7_long_runs(paras):
    k, index, best = H7_MIN_RUN, {}, {}
    cnt = [h7_counted(p[3]) for p in paras]
    for pi, (s, _) in enumerate(cnt):
        for i in range(len(s) - k + 1):
            index.setdefault(s[i:i + k], []).append((pi, i))
    for occ in index.values():
        for x in range(len(occ)):
            p, i = occ[x]
            a = cnt[p][0]
            for y in range(x + 1, len(occ)):
                q, j = occ[y]
                if q == p:
                    continue
                b = cnt[q][0]
                if i and j and a[i - 1] == b[j - 1]:
                    continue  # not the start of the run; counted from its start
                n = k
                while i + n < len(a) and j + n < len(b) and a[i + n] == b[j + n]:
                    n += 1
                if (p, q) not in best or n > best[(p, q)][0]:
                    best[(p, q)] = (n, i)
    out = {}
    for (p, q), (n, i) in best.items():
        pos = cnt[p][1]
        out[(p, q)] = (n, paras[p][3][pos[i]:pos[i + n - 1] + 1])
    return out


def h7_echoes(paras):
    """-> {(earlier p, later q): (ratio, contained, opening, matched sentence or clause, its sentence)}"""
    units = []   # per paragraph: [(counted text, display sentence)]
    for P in paras:
        u = []
        for sent in H7_SENT_RE.split(P[3]):
            if not sent:
                continue
            c = h7_counted(h7_strip_lead(sent))[0]
            if c:
                u.append((c, sent, sent))
            parts = H7_CLAUSE_RE.split(sent)
            if len(parts) > 1:
                for cl in parts:
                    c = h7_counted(h7_strip_lead(cl))[0]
                    if c:
                        u.append((c, cl, sent))
        units.append(u)
    out = {}
    for q in range(1, len(paras)):
        first = H7_OPEN_END_RE.split(paras[q][3], 1)[0]
        opening = h7_strip_lead(first)
        o = h7_counted(opening)[0]
        if len(o) < H7_ECHO_MIN:
            continue
        for p in range(q):
            best = None
            for c, unit, sent in units[p]:
                contained = o in c
                r = difflib.SequenceMatcher(None, o, c, autojunk=False).ratio()
                if not (contained or r >= H7_ECHO_RATIO):
                    continue
                if best is None or (contained, r) > (best[1], best[0]):
                    best = (round(r, 2), contained, opening, unit, sent)
            if best:
                out[(p, q)] = best
    return out


def check_h7(lines):
    paras = h7_paragraphs(lines)
    runs = h7_long_runs(paras)
    echoes = h7_echoes(paras)
    group = {}
    for (p, q) in echoes:
        group.setdefault(p, set()).add(q)
    out = []
    for (p, q), (n, run) in runs.items():
        A, B = paras[p], paras[q]
        h = {'code': 'H7', 'trigger': 'A', 'line': A[0], 'quote': A[2] or B[2], 'pair_line': B[0],
             'pair_end_line': B[1], 'length': n, 'overlap': run,
             'desc': '与 %s 逐字重合 %d 字（只计汉字和数字）：再提要多带一层，不照抄（FICCCompose C07、C23；'
                     '预告与段首重复见 C04、C20）' % (h7_loc(B), n),
             'text': run[:H7_CTX] + ('…' if len(run) > H7_CTX else '')}
        if A[1] != A[0]:
            h['end_line'] = A[1]
        out.append(h)
    for (p, q), (r, contained, opening, unit, sent) in echoes.items():
        if (p, q) in runs or len(group[p]) < H7_ECHO_GROUP:
            continue
        A, B = paras[p], paras[q]
        h = {'code': 'H7', 'trigger': 'B', 'line': A[0], 'quote': A[2] or B[2], 'pair_line': B[0],
             'pair_end_line': B[1], 'ratio': r, 'contained': contained, 'opening': opening,
             'matched': unit, 'matched_sentence': sent, 'echo_count': len(group[p]),
             'desc': '被 %s 段首复述（%s，相似度 %.2f；本段共被 %d 个后文段首复述）：本段“%s”｜段首“%s”。'
                     '预告只给结论和步骤关系，不照抄段首（FICCCompose C04、C20、C23）'
                     % (h7_loc(B), '包含' if contained else '近似', r, len(group[p]),
                        snippet(unit, H7_CTX), snippet(opening, H7_CTX)),
             'text': snippet(opening, H7_CTX)}
        if A[1] != A[0]:
            h['end_line'] = A[1]
        out.append(h)
    out.sort(key=lambda h: (h['line'], h['pair_line'], h['trigger']))
    return out


# ---------------------------------------------------------------------------
# Report-only metrics (per paragraph = per non-blank prose line)
# ---------------------------------------------------------------------------
SENT_SPLIT_RE = re.compile(r'[。！？!?]+[”’」』"]*')
BUSHI_RE = re.compile(r'不是[^。！？!?；;\n]{1,30}?而是')
DASH_RE = re.compile(r'[—―]{2,}')
CODA_RE = re.compile(
    r'^(?:而|所以|因此|所以说|可见)?[，,]?\s*(?:这就是|这才是|这正是|归根结底|归根到底|说到底)')
FILLERS = ['本质上', '值得注意的是', '不难发现', '换言之', '总而言之']
NORM_RE = re.compile(r'(?:^|[。！？!?；;：:])\s*[“"「]?\s*(?:以下适用于|不因(?!为)|仅凭)')
PAREN_RE = re.compile(r'（([^（）\n]{1,200})）')
CLAUSE_SPLIT_RE = re.compile(r'[，；：,;:]')
LEAD_STRIP = '“”"「」『』（）()《》 \t'


def sentences(text):
    return [s for s in SENT_SPLIT_RE.split(text) if zi(s) > 0]


DENSITY_HIT_KEYS = ('bushi', 'coda')  # rows whose hits are listed (v4.5; reporting only)
DENSITY_QUOTE_MAX = 40


def density_quote(s):
    s = s.strip()
    return s if len(s) <= DENSITY_QUOTE_MAX else s[:DENSITY_QUOTE_MAX - 1] + '…'


def para_hits(text):
    """Quotes of the hits counted by para_counts for the rows in DENSITY_HIT_KEYS."""
    h = {}
    h['bushi'] = [density_quote(text[m.start():m.end() + 6]) for m in BUSHI_RE.finditer(text)]
    ss = sentences(text)
    last = ss[-1].strip().lstrip(LEAD_STRIP) if ss else ''
    h['coda'] = [density_quote(last)] if (last and CODA_RE.match(last)) else []
    return h


def para_counts(text):
    c = {}
    c['bushi'] = len(BUSHI_RE.findall(text))
    c['dash'] = len(DASH_RE.findall(text))
    ss = sentences(text)
    last = ss[-1].strip().lstrip(LEAD_STRIP) if ss else ''
    c['coda'] = 1 if (last and CODA_RE.match(last)) else 0
    n, run = 0, 0
    for s in ss:
        if zi(s) < 15:
            run += 1
        else:
            n += 1 if run >= 3 else 0
            run = 0
    n += 1 if run >= 3 else 0
    c['short3'] = n
    c['filler'] = sum(text.count(w) for w in FILLERS)
    c['normative'] = len(NORM_RE.findall(text))
    c['women'] = text.count('我们')
    c['wo'] = len(re.findall(r'我(?!们)', text))
    c['paren'] = sum(1 for m in PAREN_RE.finditer(text) if 6 <= cjk(m.group(1)) <= 60)
    par = 0
    for s in ss:
        pref = {}
        for cl in CLAUSE_SPLIT_RE.split(s):
            cl = cl.strip(LEAD_STRIP)
            if len(cl) >= 3 and CJK_RE.match(cl[0]) and CJK_RE.match(cl[1]):
                pref[cl[:2]] = pref.get(cl[:2], 0) + 1
        if pref and max(pref.values()) >= 3:
            par += 1
    c['parallel3'] = par
    return c


# ---------------------------------------------------------------------------
# Hazard list (v4): cold-read candidates, report-only (FICCVoice.md 7).
# Never touches the exit code and never carries a "！".  Regex and character
# rules only (no segmenter on this machine): heuristic, biased towards missing.
# Scope = the metrics scope (prose lines before the first 附 heading, quote
# blocks included and marked); headings are checked only for 名字表禁用词.
# ---------------------------------------------------------------------------
HZ_CLAUSE_JSON_MIN = 4   # 分句过多: every sentence with >= 4 clauses goes into --json
HZ_CLAUSE_LIST_MIN = 6   # ... the text report and hazard_counts take >= 6 (no upper limit is a rule)
HAZARD_KINDS = ['承前省略', '句首代词', '分句过多', '的≥3', '无施事被动',
                '而则并且', '双重否定', '名词化', '名字表禁用词']
HAZARD_NOTES = {
    '承前省略': '承前省略，核上一句主语是否唯一',
    '句首代词': '句首裸代词，核它指哪一个；指得出名字就写名字',
    '分句过多': '一句分句很多，核能否拆句（不设上限；文本只列 ≥6 个分句的句子，≥4 的见 --json；列举句另计）',
    '的≥3': '同一分句三个及以上“的”，核定语是否超过两层',
    '无施事被动': '没写施事，核是谁这样认为',
    '而则并且': '分句起头的多义连接词，确认它标什么关系',
    '双重否定': '双重否定，核能否改成正说',
    '名词化': '名词化，核能否改回动词句',
    '名字表禁用词': '名字表“不许用”一栏的说法，改成正名',
}
HAZARD_ENUM_KEY = '分句过多（列举句，未列）'
HAZARD_COND_MAX = 10  # conditional 名字表 hits listed in the text report
HAZARD_LIST_MAX = 40
HZ_SNIP = 60

HZ_TAG_RE = re.compile(r'\[src:[^\]\n]*\]|【S\d[^】\n]*】|〔S\d+〕', re.I)
HZ_FOOT_RE = re.compile(r'\[\^[^\]\n]*\]')
HZ_LINK_RE = re.compile(r'!?\[([^\]\n]*)\]\([^)\n]*\)')
HZ_BULLET_RE = re.compile(r'^(?:[-*+](?=\s)|[•·●▪◦‧∙]|\d{1,2}[.．、)）](?!\d)|[（(]\d{1,2}[）)])\s*')
HZ_HEAD_RE = re.compile(r'^\s{0,3}#{1,6}\s+')
HZ_LEAD = '“”"‘’「」『』（）()《》〈〉【】[] \t　'
HZ_SENT_END = '。！？'
HZ_SENT_TAIL = '”’」』'
HZ_CLAUSE = '，；：'

# Start-of-sentence / clause patterns are used as rx.match(t, pos, endpos):
# no '^' (it would only match at index 0).
# 1 承前省略: sentence opens (optionally after one connective) with a bare adverb.
HZ_CONN = '但是|但|所以|因此|因为|而且|不过|然而|于是|可是|只是|同时|结果'
HZ_ELL_RE = re.compile(r'(?:(?:%s)[，,]?\s*)?(甚至|反而|也|还|却|就|才|都|并|更|则)' % HZ_CONN)
HZ_ELL_SKIP_RE = re.compile(
    r'^(?:并不|并非|并没|并未|并且|也就是说|也就是|也许|更何况|还有|就这样'
    r'|更[^，。；：！？]{0,6}的是|就[^，。；：！？]{1,15}?(?:而言|来说|来看))')
# 2 句首代词: bare pronoun at a sentence / clause start followed directly by a predicate.
HZ_PRON_RE = re.compile(
    r'(?:(?:%s)[，,]?\s*)?(它们|前者|后者|两者|二者|三者|这|那|它|其|此)'
    r'(?=意味|说明|导致|反映|表明|解释|等于|相当|是|也|就|会|使|让|正|才|并|不|没|对|在|和|与|从|把|被|要|能|可|比|有|成|为)'
    % HZ_CONN)
HZ_META_RE = re.compile(
    r'(?:(?:%s)[，,]?\s*)?(这一点|这个问题|这个回答|这件事|这一判断|这个判断|这个说法)' % HZ_CONN)
# 3 分句过多: enumeration clauses (第一／第二／一是／二是／其一) are counted apart.
HZ_ENUM_RE = re.compile(
    r'^(?:第[一二三四五六七八九十]{1,2}(?=$|[、．.])|[一二三四五六七八九十]是'
    r'|其[一二三四五六七八九十](?=$|[、．.]))')
# 4 的≥3: lexical 的 that is not a modifier marker.
HZ_DE_LEX_RE = re.compile(r'的确|目的|的话')
# 5 无施事被动
HZ_PASSIVE_RE = re.compile(
    r'被(?:普遍|广泛|一般)?(?:认为|视为|视作|看作|看成|当作|当成|解读为|理解为|称为|称作|定义为|描述为|归为)'
    r'|被(?:普遍|广泛)'
    r'|(?:普遍|一般|通常|广泛)(?:认为|预期|相信|接受|理解)'
    r'|据信|据悉|据称|据说|据报道'
    r'|有人认为|有观点|有说法|市场认为|市场预期|业内认为|外界认为|人们认为')
HZ_PASSIVE_VERB_RE = re.compile(r'(?:认为|预期|相信|接受|理解)$')
HZ_ADVERB_RE = re.compile(r'普遍|广泛|一般|通常')
# 6 而则并且: one-character connectives that open a clause.
HZ_ER_PAIR_RE = re.compile(r'不在|不是|不只|不仅|不光|并非|非')  # 不在X而在Y: 而 is the second half
HZ_ERZE_RE = re.compile(r'(而(?!且|是|非|言|已|后|今|不是)|则|并(?!不|非|没|未|无|且)|且)')
# 7 双重否定 (不得不、不乏 are idioms and not listed; the second 不 of a lexical
# word such as 不同、不仅 does not negate).
HZ_DNEG_RE = re.compile(
    r'(?:并非没有|并非不|未必不|不可能不|不是没有|不是不|没有不|不能不|不会不|未尝不|不无|无不)'
    r'(?!同|仅|但|过|断|管|论|久|良)')
# 8 名词化
HZ_NOM_RE = re.compile(
    r'进行(?:了|一次|一番)?(?:分析|讨论|评估|考察|调整|观察|比较|研究|计算|处理|应对|定价|修正|核算|测算|判断)'
    r'|(?:加以|予以)(?:分析|讨论|评估|考察|调整|观察|比较|研究|计算|处理|应对|修正)'
    r'|(?:做出|作出)(?:判断|评估|调整|反应|解释|预测)'
    r'|(?:(?<![相绝针面反核比应敌配校查一成派作入不])对于?(?![冲比应手称照标立齐接话折决口错开半象])'
    r'|(?<![也成早造迁将])就(?![业是算像要会能可在已不没有此这那得很越更把被让使从用按以只连都也还]))'
    r'[^，。；：！？、“”（）()\n]{1,12}?的(?:考察|分析|讨论|研究|评估|观察|测算|判断)(?![师员者])')

NAMES_PAREN_RE = re.compile(r'[（(][^（）()]*[）)]')
NAMES_QUOTE_RE = re.compile(r'[“"]([^“”"]+)[”"]')
NAMES_DROP = ('除外', '照引', '写')


def hz_clean(s):
    """Prose as a reader sees it: internal tags, footnote marks, link targets,
    emphasis marks and a leading bullet removed."""
    s = HZ_TAG_RE.sub('', s)
    s = HZ_FOOT_RE.sub('', s)
    s = HZ_LINK_RE.sub(lambda m: m.group(1), s)
    s = EMPH_RE.sub('', s)
    return HZ_BULLET_RE.sub('', s.strip(), count=1).strip()


def hz_inside(t):
    """inside[i] is True for characters strictly inside a matched （）/() pair."""
    inside, stack = [False] * len(t), []
    for i, ch in enumerate(t):
        if ch in '（(':
            stack.append(i)
        elif ch in '）)' and stack:
            j = stack.pop()
            for k in range(j + 1, i):
                inside[k] = True
    return inside


def hz_sentences(t, inside):
    """Sentence spans: split after 。！？ outside brackets (closing quotes stay with the
    sentence), after a bracketed whole sentence such as （……。）, and after a quoted
    English sentence that closes the Chinese one (“… growing.”)."""
    spans, s, i, n = [], 0, 0, len(t)
    while i < n:
        if (t[i] in HZ_SENT_END and not inside[i]) or (
                t[i] in '）)' and not inside[i] and i > 0 and t[i - 1] in HZ_SENT_END) or (
                t[i] in '”’' and not inside[i] and i > 0 and t[i - 1] in '.!?'):
            j = i + 1
            while j < n and (t[j] in HZ_SENT_END or t[j] in HZ_SENT_TAIL):
                j += 1
            spans.append((s, j))
            s = i = j
            continue
        i += 1
    if s < n:
        spans.append((s, n))
    return [(a, b) for a, b in spans if zi(t[a:b]) > 0]


def hz_clauses(t, inside, a, b):
    """Clause spans inside one sentence: split at ，；： outside brackets, never between two digits."""
    out, s = [], a
    for i in range(a, b):
        if t[i] in HZ_CLAUSE and not inside[i]:
            if 0 < i < len(t) - 1 and t[i - 1].isdigit() and t[i + 1].isdigit():
                continue
            out.append((s, i))
            s = i + 1
    out.append((s, b))
    return out


def hz_lead(t, a, b):
    while a < b and t[a] in HZ_LEAD:
        a += 1
    return a


def hz_snip(t, a, b, hs=None, he=None):
    """The sentence t[a:b] cut to at most 60 characters around the hit; the hit wrapped in 〔〕."""
    while a < b and t[a].isspace():
        a += 1
    while b > a and t[b - 1].isspace():
        b -= 1
    if hs is None:
        seg = t[a:b]
        return seg if len(seg) <= HZ_SNIP else seg[:HZ_SNIP] + '…'
    hs, he = max(hs, a), min(max(he, hs), b)
    if b - a <= HZ_SNIP:
        ws, we = a, b
    else:
        ws = max(a, hs - 20)
        we = min(b, ws + HZ_SNIP)
        ws = max(a, we - HZ_SNIP)
        he = min(he, we)
    s = t[ws:hs] + '〔' + t[hs:he] + '〕' + t[he:we]
    return ('…' if ws > a else '') + s + ('…' if we < b else '')


def hz_item(L, kind, t, a, b, hs=None, he=None, hit=None, note=None):
    return {'line': L.no, 'kind': kind, 'text': hz_snip(t, a, b, hs, he),
            'hit': hit if hit is not None else t[hs:he],
            'note': note or HAZARD_NOTES[kind], 'quote': L.quote}


def hz_prose(L, t, out, skipped):
    inside = hz_inside(t)
    for a, b in hz_sentences(t, inside):
        # 1 承前省略
        s0 = hz_lead(t, a, b)
        m = HZ_ELL_RE.match(t, s0, b)
        if m and not HZ_ELL_SKIP_RE.match(t[m.start(1):b]):
            out.append(hz_item(L, '承前省略', t, a, b, m.start(1), m.end(1)))
        clauses = hz_clauses(t, inside, a, b)
        n_cl, enum = 0, False
        for k, (cs, ce) in enumerate(clauses):
            c0 = hz_lead(t, cs, ce)
            if zi(t[cs:ce]) >= 2:
                n_cl += 1
            if HZ_ENUM_RE.match(t[c0:ce].strip()):
                enum = True
            # 2 句首代词 (元话语主语 listed under the same kind)
            m = HZ_META_RE.match(t, c0, ce)
            if m:
                out.append(hz_item(L, '句首代词', t, a, b, m.start(1), m.end(1),
                                   note='元话语主语：指得出名字就写名字（FICCVoice 4.4）'))
            else:
                m = HZ_PRON_RE.match(t, c0, ce)
                if m:
                    out.append(hz_item(L, '句首代词', t, a, b, m.start(1), m.end(1)))
            # 4 的≥3: counted per 顿号 item (、 outside brackets); bracketed text and an
            # item-final 的 (是……的) not counted
            segs, gs = [], cs
            for j in range(cs, ce):
                if t[j] == '、' and not inside[j]:
                    segs.append((gs, j))
                    gs = j + 1
            segs.append((gs, ce))
            for gs, ge in segs:
                core = ''.join(ch for j, ch in enumerate(t[gs:ge], gs)
                               if not inside[j] and ch not in '（）()')
                core = core.rstrip(' \t\u3000。！？，；：、”’"」』…—')
                nde = core.count('的') - len(HZ_DE_LEX_RE.findall(core))
                if core.endswith('的') and not core.endswith('目的'):
                    nde -= 1
                if nde >= 3:
                    g0 = hz_lead(t, gs, ge)
                    out.append(hz_item(L, '的≥3', t, a, b, g0, ge, hit=t[g0:ge].strip(),
                                       note='%d 个“的”' % nde))
            # 6 而则并且
            m = HZ_ERZE_RE.match(t, c0, ce)
            # 而 not listed: second half of a pair (不在X，而在Y) or 而……也 later in the
            # same sentence (a parallel / repetition marker, FICCVoice 4.1)
            if m and not (m.group(1) == '则' and '与其' in t[a:c0]) and not (
                    m.group(1) == '而' and (HZ_ER_PAIR_RE.search(t[a:c0])
                                           or '也' in t[m.end(1):b])):
                out.append(hz_item(L, '而则并且', t, a, b, m.start(1), m.end(1)))
        # 3 分句过多 (no limit is a rule: >= 4 go to --json, >= 6 to the text report)
        if n_cl >= HZ_CLAUSE_JSON_MIN:
            if enum:
                skipped[HAZARD_ENUM_KEY] = skipped.get(HAZARD_ENUM_KEY, 0) + 1
            else:
                it = hz_item(L, '分句过多', t, a, b, hit=t[a:b].strip(), note='%d 个分句' % n_cl)
                it['clauses'] = n_cl
                out.append(it)
        # 5 无施事被动 ("被 + 施事 + 认为" is not agentless)
        for m in HZ_PASSIVE_RE.finditer(t, a, b):
            h = m.group(0)
            if not h.startswith('被') and HZ_PASSIVE_VERB_RE.search(h):
                pre = re.search(r'被([^，。；：！？\s]{0,8})$', t[a:m.start()])
                if pre:
                    between = pre.group(1) + h[:-2]
                    if 1 <= len(between) <= 8 and HZ_ADVERB_RE.sub('', between):
                        continue
            out.append(hz_item(L, '无施事被动', t, a, b, m.start(), m.end()))
        # 7 双重否定, 8 名词化
        for kind, rx in (('双重否定', HZ_DNEG_RE), ('名词化', HZ_NOM_RE)):
            for m in rx.finditer(t, a, b):
                out.append(hz_item(L, kind, t, a, b, m.start(), m.end()))


def hz_names(L, t, names, out):
    if not t:
        return
    allowed = [(m.start(), m.end()) for rx in names['allowed_rx'] for m in rx.finditer(t)]
    books = [(m.start(), m.end()) for m in re.finditer(r'《[^《》\n]*》', t)]
    hits = []
    for term, rx, advice, cond, own_rx in names['terms']:
        own = [(m.start(), m.end()) for orx in own_rx for m in orx.finditer(t)]
        for m in rx.finditer(t):
            s, e = m.start(), m.end()
            if e <= s or any(x <= s and e <= y for x, y in allowed) or any(
                    s < y and x < e for x, y in books):
                continue
            # right next to its own row's name ("五家Hyperscalers", "Hyperscalers 五家"):
            # only whitespace in between counts as zero distance
            if any((x >= e and not t[e:x].strip()) or (y <= s and not t[y:s].strip())
                   for x, y in own):
                continue
            hits.append((s, -(e - s), e, term, advice, cond))
    if not hits:
        return
    hits.sort()
    sents = hz_sentences(t, hz_inside(t))
    taken = []
    for s, _, e, term, advice, cond in hits:
        if any(s < y and x < e for x, y in taken):
            continue
        taken.append((s, e))
        a, b = next(((x, y) for x, y in sents if x <= s < y), (0, len(t)))
        it = hz_item(L, '名字表禁用词', t, a, b, s, e,
                     note='不许用“%s”%s，应写成 %s'
                          % (term, '（表里限定：%s）' % cond if cond else '', advice))
        it['conditional'] = bool(cond)
        it['condition'] = cond
        out.append(it)


def find_hazards(lines, names=None):
    out, skipped = [], {HAZARD_ENUM_KEY: 0}
    use_names = bool(names and names.get('terms'))
    for L in lines:
        if L.kind == 'prose':
            t = hz_clean(L.content)
            hz_prose(L, t, out, skipped)
            if use_names:
                hz_names(L, t, names, out)
        elif L.kind == 'heading' and use_names:
            hz_names(L, hz_clean(HZ_HEAD_RE.sub('', L.content)), names, out)
    order = dict((k, i) for i, k in enumerate(HAZARD_KINDS))
    out.sort(key=lambda h: (h['line'], order[h['kind']]))
    counts = dict((k, 0) for k in HAZARD_KINDS)
    hist, ncond = {}, 0
    for h in out:
        if h['kind'] == '分句过多':
            hist[h['clauses']] = hist.get(h['clauses'], 0) + 1
            if h['clauses'] < HZ_CLAUSE_LIST_MIN:
                continue
        if h.get('conditional'):
            ncond += 1
            continue
        counts[h['kind']] += 1
    if not use_names:
        counts['名字表禁用词'] = None
    extra = {'clause_histogram': dict((str(k), hist[k]) for k in sorted(hist)),
             'names_conditional_count': ncond if use_names else None}
    return out, counts, skipped, extra


# --names: the name table of an outline (FICCOutline.md 4.2)
def names_strip_parens(s):
    prev = None
    while prev != s:
        prev, s = s, NAMES_PAREN_RE.sub('', s)
    return s


def names_cells(row):
    row = row.strip()
    if row.startswith('|'):
        row = row[1:]
    if row.endswith('|'):
        row = row[:-1]
    return [c.strip() for c in row.split('|')]


def names_split(cell):
    """Split a 不许用 cell at ，、； that sit outside brackets (bracket content can hold them)."""
    out, depth, cur = [], 0, ''
    for ch in cell:
        if ch in '（(':
            depth += 1
        elif ch in '）)':
            depth = max(0, depth - 1)
        if ch in '，、；' and depth == 0:
            out.append(cur)
            cur = ''
        else:
            cur += ch
    out.append(cur)
    return out


def names_rx(term):
    core = re.sub(r'\s+', '', term)
    body = r'\s*'.join(re.escape(c) for c in core)
    pre = r'(?<![A-Za-z])' if re.match(r'[A-Za-z]', core) else ''
    post = r'(?![A-Za-z])' if re.search(r'[A-Za-z]$', core) else ''
    return re.compile(pre + body + post)


def names_unquote(s):
    return re.sub(r'[“”"‘’]', '', s).strip()


def parse_names(text, path=''):
    """First markdown table whose header has a 名字 column and a 不许用 column.
    不许用: brackets and their content removed, split at ，、；, items holding 除外／照引／写
    dropped; an item made of two or more quoted words gives those words; items of one
    zi or less dropped.  名字: brackets removed, split at ；／ (a quoted word in an item
    is the name); quoted short forms inside brackets count as allowed names too."""
    rows = text.replace('\r\n', '\n').split('\n')
    res = {'file': path, 'rows': 0, 'terms': [], 'allowed_rx': [], 'term_list': [],
           'conditional_terms': [],
           'status': '提纲里没找到名字表（表头要有“名字”和“不许用”两栏），未查'}
    for i, ln in enumerate(rows):
        if not ln.strip().startswith('|'):
            continue
        head = names_cells(ln)
        ni = next((k for k, c in enumerate(head) if '名字' in c), None)
        fi = next((k for k, c in enumerate(head) if '不许用' in c), None)
        if ni is None or fi is None or i + 1 >= len(rows):
            continue
        if not re.match(r'^\s*\|?\s*:?-{2,}', rows[i + 1]):
            continue
        terms, allowed, nrow = {}, [], 0
        for j in range(i + 2, len(rows)):
            if not rows[j].strip().startswith('|'):
                break
            cells = names_cells(rows[j])
            if len(cells) <= max(ni, fi):
                continue
            nrow += 1
            label = cells[0] if head[0] in ('#', '＃', '序号') else str(nrow)
            ncell, fcell = cells[ni], cells[fi]
            for inner in re.findall(r'[（(]([^（）()]*)[）)]', ncell):
                allowed += [names_unquote(q) for q in NAMES_QUOTE_RE.findall(inner)]
            shown = []
            for it in re.split(r'[；;／]', names_strip_parens(ncell)):
                qs = NAMES_QUOTE_RE.findall(it)
                for nm in ([names_unquote(q) for q in qs] if qs else [names_unquote(it)]):
                    if nm:
                        shown.append(nm)
            allowed += shown
            advice = '／'.join(shown) if shown else '名字表 #%s 的写法（不起名）' % label
            for raw in names_split(fcell):
                it = names_strip_parens(raw).strip()
                if not it or any(w in it for w in NAMES_DROP):
                    continue
                qual = '；'.join(q.strip() for q in re.findall(r'[（(]([^（）()]*)[）)]', raw) if q.strip())
                qs = NAMES_QUOTE_RE.findall(it)
                for term in ([names_unquote(q) for q in qs] if len(qs) >= 2 else [names_unquote(it)]):
                    if zi(term) <= 1:
                        continue
                    terms.setdefault(term, [])
                    if (advice, qual, tuple(shown)) not in terms[term]:
                        terms[term].append((advice, qual, tuple(shown)))
        res['rows'] = nrow
        res['term_list'] = list(terms)
        res['terms'] = []
        for t, ent in terms.items():
            # conditional = every row that lists the term puts a bracketed qualifier on it
            cond = '' if any(not q for _, q, _ in ent) else '；'.join(q for _, q, _ in ent)
            adv, own = [], []
            for a, _, sh in ent:
                if a not in adv:
                    adv.append(a)
                own += [x for x in sh if x not in own]
            res['terms'].append((t, names_rx(t), ' 或 '.join(adv), cond, [names_rx(x) for x in own]))
        res['conditional_terms'] = [x[0] for x in res['terms'] if x[3]]
        res['allowed_rx'] = [names_rx(a) for a in sorted(set(x for x in allowed if x))]
        res['status'] = '' if terms else '名字表“不许用”一栏是空的，未查'
        return res
    return res


def names_public(names):
    if names is None:
        return None
    return {'file': names['file'], 'rows': names['rows'], 'terms': names['term_list'],
            'conditional_terms': names['conditional_terms'], 'status': names['status'] or '已查'}


# H9: nominalized views (FICCVoice V57; report-only review candidate, --clarity
# only).  A view, reading or inference written as an object that moves or is
# counted.  Prose lines (list rows included), inline code masked as in H5.  One
# entry per hit: line number and the matched word.  Never a hard fault, never
# the exit code.  v4.5 (2026-10-24, user approval “都同意，升级吧”): 框架, 让步
# and 的分量 removed -- 0 true hits among the 10 this check gave on the 1009,
# 1012 and 1018 finals and the 3 on the 1009 pre-clean draft (框架 of a deal,
# 条款上让步, Oracle的分量 as index weight; FICCVoice-provenance.md 33);
# 占上风 and 站在…一边 kept (no observations either way).  FICCVoice V57's
# Check regex is this one.
H9_RE = re.compile(r'读法|解读|视角|判别读数|推断加强|判断.{0,4}加强|占上风|站在.{1,8}一边')
H9_CTX = 12


def check_h9(lines):
    out = []
    for L in lines:
        if L.kind != 'prose':
            continue
        masked = H5_CODE_RE.sub(lambda m: ' ' * len(m.group(0)), L.content)
        for m in H9_RE.finditer(masked):
            i = m.start()
            out.append({'code': 'H9', 'line': L.no, 'quote': L.quote, 'hit': m.group(0),
                        'desc': '名词化的看法“%s”：写谁怎么看、我们认为什么（FICCVoice V57；只报不拦）'
                                % m.group(0),
                        'text': L.content[max(0, i - H9_CTX):m.end() + H9_CTX].strip()})
    return out


def analyze(text, name, lecture=False, baseline=None, names=None, clarity=False):
    baseline = BASELINE if baseline is None else baseline
    lines = classify(text)
    hard = (check_h1(lines) + check_h2(lines) + check_h3(lines) + check_h4(lines)
            + check_h5(text) + check_h6(lines))
    hard.sort(key=lambda h: (h['line'], h['code']))
    reviews = []
    if clarity:
        reviews = [h for h in hard if h['code'] in SEMANTIC_REVIEW_CODES]
        hard = [h for h in hard if h['code'] not in SEMANTIC_REVIEW_CODES]
    # H7 is computed apart from `hard`: a review candidate in both modes, never a hard failure
    if clarity:
        reviews += check_h9(lines)  # H9 (V57): review candidate under --clarity only
    reviews = sorted(reviews + check_h7(lines), key=lambda h: (h['line'], h['code']))
    paras = [L for L in lines if L.kind == 'prose']
    total = {k: 0 for k, _ in METRICS}
    inq = {k: 0 for k, _ in METRICS}
    dhits = {k: [] for k in DENSITY_HIT_KEYS}
    n_cjk = 0
    for L in paras:
        body = L.rest if L.starter else L.content
        n_cjk += cjk(body)
        pc = para_counts(body)
        for k in total:
            total[k] += pc[k]
            if L.quote:
                inq[k] += pc[k]
        for k, qs in para_hits(body).items():
            dhits[k] += [{'line': L.no, 'quote': q} for q in qs]
    hazards, hcounts, hskipped, hextra = find_hazards(lines, names)
    rows, flags = [], 0
    for k, label in METRICS:
        dens = total[k] * 10000.0 / n_cjk if n_cjk else 0.0
        b = (baseline or {}).get(k) or {}
        med, p90, ctl = b.get('median'), b.get('p90'), b.get('control')
        silent = lecture and k in LECTURE_SILENT
        if silent:
            dhits.pop(k, None)  # positions follow the row
        flag = bool(p90 is not None and not silent and dens > p90
                    and total[k] >= FLAG_MIN_COUNT)
        flags += 1 if flag else 0
        rows.append({'key': k, 'label': label, 'count': total[k], 'quote_count': inq[k],
                     'per_10k': round(dens, 2), 'author_median': med, 'author_p90': p90,
                     'control_2026_02': ctl, 'over_p90': flag, 'silent': silent})
    result = {'file': name, 'version': '%s (%s)' % (VERSION, VERSION_DATE),
            'register': 'lecture' if lecture else 'written', 'chinese_chars': n_cjk,
            'hard': hard, 'metrics': rows, 'over_p90_count': flags,
            'short_text': n_cjk < SHORT_TEXT, 'exit_code': 1 if hard else 0,
            'hazards': hazards, 'hazard_counts': hcounts, 'hazard_skipped': hskipped,
            'clause_histogram': hextra['clause_histogram'],
            'names_conditional_count': hextra['names_conditional_count'],
            'names': names_public(names), 'semantic_reviews': reviews,
            'density_hits': dhits}
    if clarity:
        result.update(mode='clarity')
    return result


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------
def fmt(v):
    return '—' if v is None else '%.1f' % v


def render(r, hazards=True):
    out = []
    reg = '讲课档（--lecture：硬伤规则不变，「我」与括号不提示）' if r['register'] == 'lecture' else '书面档'
    out.append('voice_check v%s｜%s｜%s' % (r['version'], r['file'], reg))
    if r.get('mode') == 'clarity':
        out.append('清晰模式：H1/H5/H6 是硬伤；H2–H4、H7 与 H9 只列语义复核候选，退出码不证明清晰。')
    out.append('正文 %d 汉字（查到第一个「## 附」为止；跳过围栏代码、表格行、图片行；'
               '引用块照查并标注；标题行只查 H4；H6、H7 另跳过清单行）' % r['chinese_chars'])
    if r['short_text']:
        out.append('提示：正文不足 %d 汉字，密度只作参考。' % SHORT_TEXT)
    out.append('')
    if r['hard']:
        out.append('硬伤 %d：' % len(r['hard']))
        for h in r['hard']:
            loc = 'L%d' % h['line'] + ('–L%d' % h['end_line'] if h.get('end_line') else '')
            q = '〔引用块〕' if h.get('quote') else ''
            out.append('  %s %s %s%s｜%s' % (h['code'], loc, h['desc'], q, h['text']))
    else:
        out.append('硬伤 0')
    out.append('')
    out.append(render_semantic_reviews(r))
    out.append('')
    out.append('密度记录（每万汉字；括号里是原始次数；！＝高于作者 90 分位且不少于 %d 处）'
               % FLAG_MIN_COUNT)
    out.append('“不是……而是”、破折号两行标“！”的，按references/clarity-acceptance.md交稿前处理；其余只报数。'
               '密度不改变退出码，也不证明语义清楚。')
    w = [18, 20, 9, 11, 9]
    out.append(pad('项', w[0]) + pad('实测', w[1]) + pad('作者中位', w[2], True)
               + pad('作者90分位', w[3], True) + pad('2026.02', w[4], True))
    for m in r['metrics']:
        cell = '%.1f（%d' % (m['per_10k'], m['count'])
        cell += '，引用块 %d）' % m['quote_count'] if m['quote_count'] else '）'
        mark = '！' if m['over_p90'] else ''
        out.append(pad(m['label'], w[0]) + pad(cell, w[1]) + pad(fmt(m['author_median']), w[2], True)
                   + pad(fmt(m['author_p90']), w[3], True)
                   + pad(fmt(m['control_2026_02']), w[4], True) + ' ' + mark)
        for h in r.get('density_hits', {}).get(m['key'], []):
            out.append('    L%d: %s' % (h['line'], h['quote']))
    if BASELINE:
        meta = BASELINE.get('_meta', {})
        out.append('基线：%s，%s 篇作者文本；算法见脚本头与 README。' % (meta.get('date', '?'), meta.get('docs', '?')))
    else:
        out.append('基线：未写入（跑 --baseline 生成）。')
    out.append('')
    if hazards and 'hazards' in r:
        out.append(render_hazards(r))
        out.append('')
    out.append('结论：硬伤 %d，退出码 %d；高于作者 90 分位 %d 项（两项风格清理按上述说明处理）。'
               % (len(r['hard']), r['exit_code'], r['over_p90_count']))
    return '\n'.join(out)


# ---------------------------------------------------------------------------
# Corpus helpers, baseline, selftest
# ---------------------------------------------------------------------------
ISSUE_RE = re.compile(r'^\s*(\d{4})\.(\d{1,2})\s*$')


def read(path):
    with io.open(path, encoding='utf-8') as f:
        return f.read()


def split_issues(path):
    """Monthly-letter collection: an issue number alone on a line (e.g. 2025.12) opens an issue."""
    order, body, cur = [], {}, None
    for line in read(path).split('\n'):
        m = ISSUE_RE.match(line)
        if m:
            key = '%s.%02d' % (m.group(1), int(m.group(2)))
            while key in body:
                key += '+'
            cur = key
            order.append(key)
            body[key] = []
            continue
        if cur is not None:
            body[cur].append(line)
    return [(k, '\n'.join(body[k])) for k in order]


def quantile(xs, q):
    xs = sorted(xs)
    if not xs:
        return 0.0
    pos = (len(xs) - 1) * q
    lo = int(pos)
    hi = min(lo + 1, len(xs) - 1)
    return xs[lo] + (xs[hi] - xs[lo]) * (pos - lo)


def baseline_docs(letters, extras):
    docs, control = [], None
    for key, text in split_issues(letters):
        if key == CONTROL_ISSUE:
            control = (key, text)
        elif key == DEDUP_ISSUE:
            continue
        else:
            docs.append(('月报 ' + key, text))
    for p in extras:
        docs.append((os.path.basename(p), read(p)))
    return docs, control


def run_baseline(letters, extras, per_doc=False):
    docs, control = baseline_docs(letters, extras)
    dens = {k: [] for k, _ in METRICS}
    table = []
    for name, text in docs:
        r = analyze(text, name, baseline={})
        row = {m['key']: m['per_10k'] for m in r['metrics']}
        for k in dens:
            dens[k].append(row[k])
        table.append((name, r['chinese_chars'], len(r['hard']), row))
    ctl = analyze(control[1], CONTROL_ISSUE, baseline={}) if control else None
    ctl_row = {m['key']: m['per_10k'] for m in ctl['metrics']} if ctl else {}
    if per_doc:
        print('\t'.join(['doc', 'cjk', 'hard'] + [k for k, _ in METRICS]))
        for name, n, h, row in table:
            print('\t'.join([name, str(n), str(h)] + ['%.2f' % row[k] for k, _ in METRICS]))
        print()
    print('# %d docs; 2026.02 excluded (control); 2025.12 counted once via nine-sections.md' % len(docs))
    print('# letters: %s' % letters)
    print('# extras: %s' % ', '.join(extras))
    print(pad('项', 18) + pad('中位', 8, True) + pad('90分位', 9, True) + pad('2026.02', 9, True))
    lit = ['# BEGIN BASELINE', 'BASELINE = {',
           "    '_meta': {'date': '%s', 'docs': %d, 'control': '%s', 'dedup': '%s=nine-sections.md',"
           % (VERSION_DATE, len(docs), CONTROL_ISSUE, DEDUP_ISSUE),
           "              'method': 'per-doc count/CJK*1e4; median & p90 by linear interpolation'},"]
    for k, label in METRICS:
        med, p90 = quantile(dens[k], 0.5), quantile(dens[k], 0.9)
        c = ctl_row.get(k)
        print(pad(label, 18) + pad('%.2f' % med, 8, True) + pad('%.2f' % p90, 9, True)
              + pad('—' if c is None else '%.2f' % c, 9, True))
        lit.append("    '%s': {'median': %.2f, 'p90': %.2f, 'control': %s},"
                   % (k, med, p90, 'None' if c is None else '%.2f' % c))
    lit += ['}', '# END BASELINE']
    print()
    print('\n'.join(lit))
    return 0


SYNTH = [
    ('H1', '我们注意到出处标签【S12】混进了正文，〔nine-sections.md L45〕也是。\n'),
    ('H2', '本文将从三个方面讨论美元流动性。\n\n第二段。\n'),
    ('H3', '几点观察：\n\n- 资金面偏紧\n- 政策面观望\n- 情绪面低迷\n'),
    ('H4', '## 一、负债端：钱从哪里来\n\n正文。\n\n## 二、资产端：钱到哪里去\n\n正文。\n'),
    ('H4', '## 美元不是避险资产，而是融资货币\n\n正文。\n'),
    ('H5', '他说「美元荒」只是『表面』现象。\n'),
    ('H6', '利差走阔了；利率也在降，资金面并不宽松。\n'),
    (None, '| 项目 | 说明 |\n|---|---|\n| 利差 | 走阔；利率下行 |\n'),
    (None, '- 利差走阔；利率也在降\n\n1. 资金面偏紧；情绪低迷，市场还在等待央行下一步的公开市场操作信号\n\n2．结构越复杂；收费越高\n'),
    (None, '## 利差；利率\n\n正文没有分号。行内`a；b`不算。\n\n```\nx = 1；y = 2\n```\n\n'
           '## 附：数据\n\n附录里的分号；不算。\n'),
    (None, '他说“美元荒”只是‘表面’现象，`「代码里的」`不算。\n\n```\n『围栏里的』\n```\n'),
    (None, '我们注意到〔九节〕〔2018.11〕〔L14、L16〕〔来源：2025 年 4 月份月报〕。\n\n'
           '第一，本文将大量使用案例而不是公式，第二，本文将会尽量削弱随机分析的存在。第一个办法：打多份工。\n\n## 四、取舍节与收尾\n\n正文。\n\n## 五、第一段怎么进\n\n正文。\n\n'
           '1. 结构越复杂，塞进来的东西越多，越Exotic，Sales收费越High\n\n2. ATM附近，Gamma最大。\n\n'
           '3. 转嫁尾部风险。\n'),
]


# Hazard-list fixtures: (kind, expected hits of that kind, text).  Every kind has
# at least two positives and two negatives; the negatives cover the README's
# "不算" list (而且、否则、并不、这种X、被 Barclays 认为、不得不、列举句、
# 括号内逗号、千分位).
HZ_SYNTH = [
    ('承前省略', 1, '利差走阔了。也说明尾部在变坏。'),
    ('承前省略', 1, '杠杆率没动。但是却没人注意尾部。'),
    ('承前省略', 1, '“还要看发行。”他说。'),
    ('承前省略', 1, '利差走阔了。（数据见图1。）也说明尾部在变坏。'),
    ('承前省略', 0, '利差走阔了。并不说明尾部在变坏。'),
    ('承前省略', 0, '利差走阔了。而且尾部在变坏。'),
    ('承前省略', 0, '就投资级而言，杠杆率没动。'),
    ('承前省略', 0, '利差走阔了。就这样，尾部先变坏。'),
    ('句首代词', 1, '尾部在变坏。这说明利差会走阔。'),
    ('句首代词', 1, '利差走阔，它反映的是违约。'),
    ('句首代词', 1, '这一点很重要。'),
    ('句首代词', 0, '这种走阔只在高收益。'),
    ('句首代词', 0, '其中三分之二是支付违约。此外，回收率创新低。'),
    ('句首代词', 0, '那么利差会怎样走？'),
    # 分句过多: (kind, listed in the text report / hazard_counts, text, items in --json)
    ('分句过多', 1, '利差走阔，违约增加，回收率下降，私募信贷承压，BDC卖贷款，Hyperscalers少发债。', 1),
    ('分句过多', 1, '杠杆率没动，EBITDA增得快，利息成本上升，利润率压缩，净杠杆略降，毛杠杆也降，三家都一样。', 1),
    ('分句过多', 0, '杠杆率没动，EBITDA增得快，利息成本上升，利润率压缩，净杠杆略降。', 1),
    ('分句过多', 0, '利差走阔，违约增加，回收率下降，私募信贷承压。', 1),
    ('分句过多', 0, '第一，利差走阔，第二，违约增加，第三，回收率下降。', 0),
    ('分句过多', 0, '一是利差走阔，二是违约增加，三是回收率下降，四是私募信贷承压。', 0),
    ('分句过多', 0, '三家样本（Barclays，Morgan Stanley，Citi，各自口径不同，都剔除金融）的净杠杆都降了，靠的是EBITDA，利润率也高，债务也在涨。', 1),
    ('分句过多', 0, '发行额1，970亿美元，并购610亿美元，占比31%，比8月增1，120亿美元。', 1),
    ('的≥3', 1, '投资级的发行人的杠杆率的变化不大。'),
    ('的≥3', 1, '我们看的是公开市场的尾部的价格的变化。'),
    ('的≥3', 0, '投资级的利差的变化是最小的。'),
    ('的≥3', 0, '证据有三样：9月投资级的并购融资、高收益的再融资比例、二季度的资本开支。'),
    ('的≥3', 1, '9月的发行里的并购的部分、BBB级发行都在增。'),
    ('的≥3', 0, 'Barclays 的原话是“Debt keeps growing.” 不过我们的样本的数不同。'),
    ('的≥3', 0, '投资级的利差（Barclays 的口径，按市值加权的指数）变化不大。'),
    ('无施事被动', 1, '尾部被认为是风险最集中的地方。'),
    ('无施事被动', 1, '市场普遍预期利差会走阔。'),
    ('无施事被动', 1, '据悉，违约在增加。'),
    ('无施事被动', 0, '尾部被 Barclays 认为是风险最集中的地方。'),
    ('无施事被动', 0, '尾部被投资者普遍认为是风险所在。'),
    ('无施事被动', 0, 'Barclays 认为尾部风险最集中。'),
    ('而则并且', 1, '利差走阔，而利率在降。'),
    ('而则并且', 1, '违约增加；则回收率下降。'),
    ('而则并且', 1, '发行增加，并推高了利差。'),
    ('而则并且', 0, '利差走阔，而且违约增加。'),
    ('而则并且', 0, '否则利差会走阔。'),
    ('而则并且', 0, '发行增加，并不说明加杠杆。'),
    ('而则并且', 0, '利差走阔，从而压低了发行。'),
    ('而则并且', 0, '资金来自自有现金，而不是外部借款。'),
    ('而则并且', 0, '私募信贷的压力不在赎回申请，而在毛申购大减。'),
    ('而则并且', 0, '风险不仅在尾部，而在私募信贷。'),
    ('而则并且', 1, '利差不在高位。而利率在降。'),
    ('而则并且', 0, '利差走阔，而利率也在降。'),
    ('而则并且', 1, '利差走阔，而真正的风险是尾部。'),
    ('而则并且', 0, '与其说是加杠杆，则不如说是再融资。'),
    ('双重否定', 1, '利差走阔不无道理。'),
    ('双重否定', 1, '违约率未必不会上升。'),
    ('双重否定', 1, '我们不能不看尾部。'),
    ('双重否定', 0, '发行人不得不再融资。'),
    ('双重否定', 0, '市场上不乏买家。'),
    ('双重否定', 0, '两家不是不同的样本吗？'),
    ('名词化', 1, '我们对杠杆率进行了分析。'),
    ('名词化', 1, '9月版对尾部的判断要改。'),
    ('名词化', 1, '这一项需要加以修正。'),
    ('名词化', 0, '对冲基金的分析师认为利差会走阔。'),
    ('名词化', 0, '绝对水平的分析意义不大。'),
    ('名词化', 0, '这就要看发行人的判断。'),
    ('名词化', 0, '我们分析了杠杆率。'),
]

# --names fixture: bracketed exceptions, several names in one cell, a quoted
# short form inside brackets, and a forbidden word that is part of a name.
NAMES_TABLE = (
    '## 名字表\n\n'
    '| # | 概念 | 名字（简称） | 第一次出现时的定义 | 先定义的节点 | 不许用 |\n'
    '|---|---|---|---|---|---|\n'
    '| 1 | 净杠杆、毛杠杆 | 净杠杆；毛杠杆 | 定义 | N1 | 净杠杆率、Net leverage |\n'
    '| 2 | 杠杆率 | 杠杆率 | 定义 | N1 | 比率（题目除外）、杠杆（单用作指标时） |\n'
    '| 3 | 尾部 | 尾部 | 定义 | N0 | 尾巴、底部；正文里的“尖”“变尖”（N0 照引除外） |\n'
    '| 4 | 走阔 | 走阔 | 定义 | N0 | 扩大、bp、写成“走宽”的 |\n'
    '| 5 | 低价贷款 | 标价低于 60 美元的贷款（同段后文简称“低价贷款”） | 定义 | N2 | 低价、困境贷款 |\n'
    '| 6 | Hyperscalers | Hyperscalers | 定义 | N0 | 五家、科技巨头 |\n'
    '\n正文从这里开始，不在表里：底部。\n')
NAMES_TERMS = ['净杠杆率', 'Net leverage', '比率', '杠杆', '尾巴', '底部', '变尖', '扩大',
               'bp', '低价', '困境贷款', '五家', '科技巨头']
NAMES_COND = ['比率', '杠杆', '变尖']
# (unconditional hits, conditional hits, text)
NAMES_SYNTH = [
    (2, 0, '净杠杆率降了，Net leverage 也降了。\n'),
    (3, 1, '尾巴变坏，利差扩大 50bp，分布变尖。\n'),
    (0, 1, '## 杠杆没坏\n\n正文。\n'),
    (0, 0, '净杠杆和毛杠杆都降了，杠杆率没动，低价贷款占比升到 4.2%。\n'),
    (0, 0, '利差走宽，尖在尾部，Bigger 不算。\n'),
    (0, 0, '9 月那篇《尾巴变坏，杠杆没动，分布变尖》要改。\n'),
    (2, 0, '这五家的债务增速最高，尾部五家也一样。\n'),  # next to another row's name: reported
    (0, 0, '剔除五家Hyperscalers之后，Hyperscalers 五家的债务增速更高。\n'),
]
CLAUSE_HIST_TEXT = ('利差走阔，违约增加，回收率下降，私募信贷承压。'
                    '杠杆率没动，EBITDA增得快，利息成本上升，利润率压缩，净杠杆略降。'
                    '利差走阔，违约增加，回收率下降，私募信贷承压，BDC卖贷款，Hyperscalers少发债。\n')


def selftest_hazards():
    ok = True
    print('== 隐患清单自检（合成样例：每类正例要抓到、反例要放过；隐患只报不拦）')
    for fx in HZ_SYNTH:
        kind, want, text = fx[:3]
        hz, cnt = find_hazards(classify(text))[:2]
        got = cnt[kind]
        if len(fx) > 3:  # 分句过多: listed (>= 6) and --json (>= 4) counts both checked
            gotj = sum(1 for h in hz if h['kind'] == kind)
            good = got == want and gotj == fx[3]
            ok &= good
            print('  %s 〔%s〕%s 文本列 期望 %d，得到 %d；--json 期望 %d，得到 %d｜%s'
                  % ('通过' if good else '不通过', kind, '正例' if want else '反例',
                     want, got, fx[3], gotj, text))
            continue
        good = got == want
        ok &= good
        print('  %s 〔%s〕%s 期望 %d，得到 %d｜%s' % ('通过' if good else '不通过', kind,
              '正例' if want else '反例', want, got, text))
    hist = find_hazards(classify(CLAUSE_HIST_TEXT))[3]['clause_histogram']
    good = hist == {'4': 1, '5': 1, '6': 1}
    ok &= good
    print('  %s 〔分句过多〕clause_histogram 期望 {4:1, 5:1, 6:1}，得到 %s'
          % ('通过' if good else '不通过', hist))
    names = parse_names(NAMES_TABLE, 'selftest')
    good = (sorted(names['term_list']) == sorted(NAMES_TERMS)
            and sorted(names['conditional_terms']) == sorted(NAMES_COND))
    ok &= good
    print('  %s 〔名字表禁用词〕解析 %d 行，不许用 %s；有条件 %s' % (
        '通过' if good else '不通过', names['rows'], '、'.join(names['term_list']),
        '、'.join(names['conditional_terms'])))
    for want, wantc, text in NAMES_SYNTH:
        hz, cnt, _, ex = find_hazards(classify(text), names)
        got, gotc = cnt['名字表禁用词'], ex['names_conditional_count']
        flags = all(('conditional' in h and 'condition' in h) for h in hz if h['kind'] == '名字表禁用词')
        good = got == want and gotc == wantc and flags
        ok &= good
        print('  %s 〔名字表禁用词〕%s 无条件 期望 %d，得到 %d；有条件 期望 %d，得到 %d｜%s' % (
            '通过' if good else '不通过', '正例' if want or wantc else '反例', want, got, wantc, gotc,
            text.strip().replace('\n', ' ')))
    r = analyze('利差走阔了。也说明尾部在变坏。这说明利差会走阔。\n', 'synthetic')
    n = sum(v for v in r['hazard_counts'].values() if v)
    good = r['exit_code'] == 0 and not r['hard'] and n >= 2
    ok &= good
    print('  %s 隐患 %d 条、硬伤 %d，退出码 %d（隐患不影响退出码）'
          % ('通过' if good else '不通过', n, len(r['hard']), r['exit_code']))
    return ok


def hazard_count_line(r):
    return '隐患清单（只报）：' + '、'.join(
        '%s %s' % (k, '—' if r['hazard_counts'][k] is None else r['hazard_counts'][k])
        for k in HAZARD_KINDS)


def render_semantic_reviews(r):
    reviews = r['semantic_reviews']
    if r.get('mode') == 'clarity':
        out = ['语义复核候选 %d（H2–H4 字面命中、H7 跨段重复（A 长串重合、B 段首复述）、H9 名词化的看法，不据此判错；见 references/clarity-acceptance.md）'
               % len(reviews)]
    else:
        out = ['语义复核候选 %d（H7 跨段重复：A 长串重合、B 段首复述，只报不拦；见 FICCCompose.md C23）' % len(reviews)]
    for h in reviews:
        loc = 'L%d' % h['line'] + ('–L%d' % h['end_line'] if h.get('end_line') else '')
        q = '〔引用块〕' if h.get('quote') else ''
        out.append('  %s %s %s%s｜%s' % (h['code'], loc, h['desc'], q, h['text']))
    return '\n'.join(out)


def render_hazards(r):
    out = ['隐患清单（冷读候选，只报不拦；见 FICCVoice.md V37–V40、references/clarity-acceptance.md）',
           '范围同报数项；名字表禁用词另查标题行；[src:…] 等内部标签先剥掉再查（它们归 H1）。']
    cnt, nm = r['hazard_counts'], r.get('names')
    w = 16
    out.append(pad('类别', w) + '命中')
    for k in HAZARD_KINDS:
        v = cnt.get(k)
        if v is not None:
            cell = str(v)
            if k == '分句过多':
                cell += '（≥6 个分句；≥4 的见 --json）'
            elif k == '名字表禁用词':
                cell += '（无条件；有条件的另有 %d，见最后）' % (r.get('names_conditional_count') or 0)
        elif nm:
            cell = nm['status']
        else:
            cell = '未给提纲，未查'
        out.append(pad(k, w) + cell)
    skipped = (r.get('hazard_skipped') or {}).get(HAZARD_ENUM_KEY, 0)
    if skipped:
        out.append('另有分句≥4 的列举句 %d 句（分句起头是第一／第二／一是／二是／其一），不计入、不列。' % skipped)
    if nm and cnt.get('名字表禁用词') is not None:
        out.append('名字表：%s，%d 行，“不许用”说法 %d 个（其中有条件的 %d 个）；《》书名号里的不报。'
                   % (nm['file'], nm['rows'], len(nm['terms']), len(nm.get('conditional_terms') or [])))
    for k in HAZARD_KINDS:
        items = [h for h in r['hazards'] if h['kind'] == k and not h.get('conditional')
                 and not (k == '分句过多' and h['clauses'] < HZ_CLAUSE_LIST_MIN)]
        if not items:
            continue
        out.append('')
        out.append('%s %d 条：%s' % (k, len(items), HAZARD_NOTES[k]))
        for h in items[:HAZARD_LIST_MAX]:
            q = '〔引用块〕' if h['quote'] else ''
            tail = '｜' + h['note'] if h['note'] != HAZARD_NOTES[k] else ''
            out.append('  L%d 〔%s〕%s %s%s' % (h['line'], k, q, h['text'], tail))
        if len(items) > HAZARD_LIST_MAX:
            out.append('  另有 %d 条，--json 全列' % (len(items) - HAZARD_LIST_MAX))
    cond = [h for h in r['hazards'] if h.get('conditional')]
    if cond:
        out.append('')
        out.append('有条件的禁用词（按表里限定人工判）%d 条：表里给这个说法加了括号限定，命中不一定违规' % len(cond))
        for h in cond[:HAZARD_COND_MAX]:
            q = '〔引用块〕' if h['quote'] else ''
            out.append('  L%d 〔名字表禁用词·有条件〕%s %s｜%s' % (h['line'], q, h['text'], h['note']))
        if len(cond) > HAZARD_COND_MAX:
            out.append('  另有 %d 条，--json 全列' % (len(cond) - HAZARD_COND_MAX))
    return '\n'.join(out)


def selftest_clarity():
    print('== 清晰模式自检（有效表达不硬拦；真正的路线图仍须复核）')
    cases = [
        ('因果步骤', 'H2', '假设利率上升，首先融资成本增加，其次企业缩减投资，最后产能扩张放缓。'),
        ('完整因果列表', 'H3', '- 利率上升，因此融资成本增加。\n'
                           '- 融资成本增加，因此企业缩减投资。\n'
                           '- 企业缩减投资，因此产能扩张放缓。\n'),
        ('具体冒号标题', 'H4', '## 固定利率：利息不会改变\n\n正文。\n\n'
                           '## 浮动利率：利息随市场变\n\n正文。\n'),
        ('实际路线图', 'H2', '本文将从三个方面讨论美元流动性。'),
    ]
    ok = True
    for label, code, text in cases:
        default = analyze(text, label)
        r = analyze(text, label, clarity=True)
        good = (default['exit_code'] == 1
                and {h['code'] for h in default['hard']} == {code}
                and r['exit_code'] == 0 and not r['hard']
                and r['semantic_reviews'] == default['hard']
                and r['metrics'] == default['metrics']
                and r['hazards'] == default['hazards']
                and default['semantic_reviews'] == []
                and code in render_semantic_reviews(r))
        ok &= good
        print('  %s %s：默认退出码 %d；清晰模式退出码 %d、候选 %s'
              % ('通过' if good else '不通过', label, default['exit_code'], r['exit_code'],
                 [h['code'] for h in r['semantic_reviews']]))
    r = analyze('这不是需求回升，而是供应收缩。价格——仍在上涨。' * 3,
                '风格清理', clarity=True)
    flags = {m['key'] for m in r['metrics'] if m['over_p90']}
    good = ({'bushi', 'dash'} <= flags and r['exit_code'] == 0
            and '按references/clarity-acceptance.md交稿前处理' in render(r, hazards=False))
    ok &= good
    print('  %s 两项风格清理保留“！”提示，退出码仍为 %d；不作为清晰度证明'
          % ('通过' if good else '不通过', r['exit_code']))
    return ok


# H7 fixtures.  Trigger A: a 22-character run (>= H7_MIN_RUN counted characters)
# and its first 19 characters; the characters around the run differ in the two
# paragraphs (是/示 before, 。/， after), so the shared run is exactly the fixture
# string.  Trigger B: a thesis paragraph from the wave-4 trial 甲 (1012CNBondSep,
# L5) whose sentences three later openings copy almost word for word; the same
# thesis with three paraphrased openings (every ratio < 0.6); and the 乙 pattern,
# two later openings echoing one clause each (below H7_ECHO_GROUP).
H7_RUN22 = '离岸美元融资成本在九月中旬持续抬升了十个基点'
H7_LEAD = '9月的债市把8月的样子又走了一遍，只是走得更偏。\n\n'
H7_THESIS = ('钱挤到了超长端，10年期却几乎没动。那么它为什么下不去？基本面不再一边倒地帮多头，央行没动，'
             '市场也没在等降息，所以10年期贴在了资金价格上。而且资金价格自己也没往下走。\n\n')
H7_SYNTH = [
    ('A', '两段共享 22 字', 1, '我们的判断是%s。所以要减仓。\n\n数据显示%s，这与上月相反。\n' % (H7_RUN22, H7_RUN22)),
    ('A', '两段共享 19 字', 0, '我们的判断是%s。所以要减仓。\n\n数据显示%s，这与上月相反。\n'
     % (H7_RUN22[:19], H7_RUN22[:19])),
    ('A', '同样 22 字在表格行和清单行', 0, '| 项目 | %s |\n|---|---|\n\n- %s。\n\n数据显示%s，这与上月相反。\n'
     % (H7_RUN22, H7_RUN22, H7_RUN22)),
    ('B', '主旨段预告三个段首（甲 L5 式）', 3, H7_LEAD + H7_THESIS
     + '基本面已经不再一边倒地帮多头。贷款这一半没有好起来。\n\n'
     + '所以10年期就贴在了资金价格上：它离政策利率只剩28个bp。\n\n'
     + '而且这个资金价格自己也没往下走。资金一直很平稳。\n'),
    ('B', '三个段首都是改写，相似度都低于 0.6', 0, H7_LEAD + H7_THESIS
     + '贷款和价格两头拉扯，多头的底气只剩一半。\n\n'
     + '政策利率离10年期太近，买长债几乎没有利差可赚。\n\n'
     + '回购和存单利率整月平平，没有给长端让出空间。\n'),
    ('B', '只有两个段首各复述一句（乙 L5 式，不到 H7_ECHO_GROUP）', 0, H7_LEAD
     + '钱挤到超长端的同一个月，10年期却下不去。原因是降息没有动静，10年期就贴在了资金价格上，资金利率又没有往下走。\n\n'
     + '所以，10年期就贴在了资金价格上。10年期离政策利率只剩28个bp。\n\n'
     + '更要紧的是，资金利率自己也没有往下走。资金倒是一直很平稳。\n'),
]


def selftest_h7(clarity=False):
    global H7_ECHO_RATIO
    print('== H7 跨段重复自检（A 长串重合、B 段首复述；只进语义复核候选，不计硬伤、不改退出码）')
    ok = len(H7_RUN22) == 22
    for trig, label, want, text in H7_SYNTH:
        r = analyze(text, 'synthetic', clarity=clarity)
        h7 = [h for h in r['semantic_reviews'] if h['code'] == 'H7']
        good = (len(h7) == want and all(h['trigger'] == trig for h in h7) and not r['hard']
                and r['exit_code'] == 0 and not any(h['code'] == 'H7' for h in r['hard']))
        extra = ''
        if trig == 'A' and want and good:
            good = (h7[0]['length'] == 22 and (h7[0]['line'], h7[0]['pair_line']) == (1, 3)
                    and 'H7' in render(r, hazards=False))
            extra = '（%d 字，L%d 与 L%d）' % (h7[0]['length'], h7[0]['line'], h7[0]['pair_line'])
        if trig == 'B' and want and good:
            good = ([(h['line'], h['pair_line']) for h in h7] == [(3, 5), (3, 7), (3, 9)]
                    and all(h['contained'] or h['ratio'] >= H7_ECHO_RATIO for h in h7))
            extra = '（L3 被 %s 复述，相似度 %s）' % ('、'.join('L%d' % h['pair_line'] for h in h7),
                                               '、'.join('%.2f' % h['ratio'] for h in h7))
        if trig == 'B' and not want and label.startswith('三个段首'):
            keep = H7_ECHO_RATIO
            H7_ECHO_RATIO = 0.0   # every pair "matches": read the best ratio of each pair
            try:
                ratios = [v[0] for v in h7_echoes(h7_paragraphs(classify(text))).values()]
            finally:
                H7_ECHO_RATIO = keep
            good &= bool(ratios) and max(ratios) < 0.6
            extra = '（最高相似度 %.2f）' % max(ratios or [0])
        ok &= good
        print('  %s 〔%s〕%s：期望 H7 %d 条，得到 %d 条%s；硬伤 %d，退出码 %d' % (
            '通过' if good else '不通过', trig, label, want, len(h7), extra, len(r['hard']), r['exit_code']))
    return ok


# H9 fixture (synthetic sample, same as h9.md in the author's task directory): L3 prose
# with 读法 and 解读, L5 a list row with 推断加强, L7 读法 inside inline code, L9-L11
# a table whose cells carry 视角, 框架 and 让步.  Only the three L3/L5 hits count.
# v4.5: L13 is a prose line with the three words removed on 2026-10-24 (框架,
# 让步, 的分量) in their ordinary senses; it must give no H9 hit.
H9_NEG = '融资框架谈妥后，优先档在条款上让步，Oracle的分量还在涨。'
H9_SYNTH = ('# 测试\n\n三种读法并存，市场的解读在变。\n\n- 清单行：这个推断加强了。\n\n'
            '行内代码 `读法` 不算。\n\n| 表格 | 视角 |\n|---|---|\n| 框架 | 让步 |\n\n' + H9_NEG + '\n')
H9_WANT = [(3, '读法'), (3, '解读'), (5, '推断加强')]
H9_NEG_LINE = 13


def selftest_h9():
    print('== H9 名词化的看法自检（只在 --clarity 下算；只进语义复核候选，不计硬伤、不改退出码）')
    r = analyze(H9_SYNTH, 'synthetic', clarity=True)
    d = analyze(H9_SYNTH, 'synthetic')
    got = [(h['line'], h['hit']) for h in r['semantic_reviews'] if h['code'] == 'H9']
    skipped = not any(h['code'] == 'H9' and 7 <= h['line'] < H9_NEG_LINE
                      for h in r['semantic_reviews'])
    neg_lines = H9_SYNTH.split('\n')
    neg_ok = (neg_lines[H9_NEG_LINE - 1] == H9_NEG
              and all(w in H9_NEG for w in ('框架', '让步', '的分量'))
              and not any(h['code'] == 'H9' and h['line'] == H9_NEG_LINE
                          for h in r['semantic_reviews']))
    default_h9 = [h for h in d['semantic_reviews'] + d['hard'] if h['code'] == 'H9']
    good = (got == H9_WANT and skipped and neg_ok
            and not r['hard'] and r['exit_code'] == 0
            and not any(h['code'] == 'H9' for h in r['hard'])
            and 'H9' in render_semantic_reviews(r)
            and not default_h9 and d['exit_code'] == 0)
    print('  %s 清晰模式 H9 %d 条（%s）；行内代码 L7、表格行 L9–L11 %s；'
          'L%d 平常用法（框架、让步、的分量，10-24 移出）%s；默认模式 H9 %d 条；'
          '硬伤 %d，退出码 %d／%d' % (
              '通过' if good else '不通过', len(got), '、'.join('L%d %s' % g for g in got),
              '不报' if skipped else '误报', H9_NEG_LINE, '不报' if neg_ok else '误报',
              len(default_h9), len(r['hard']), r['exit_code'], d['exit_code']))
    return good


# Density positions fixture (v4.5): L3 one 不是……而是, L5 a paragraph whose last
# sentence is a 段末升华.  Counts stay 1 each, no flag (< FLAG_MIN_COUNT), exit 0.
DENSITY_SYNTH = ('# 测试\n\n利率上行的原因不是需求回升，而是供应收缩。\n\n'
                 '融资成本一路走高，企业只好推迟投资。这就是本轮放缓的根源。\n')
DENSITY_WANT = {'bushi': [3], 'coda': [5]}


def selftest_density(clarity=False):
    print('== 密度行位置自检（不是……而是、段末升华逐条列行号与原句；只报，不改计数、“！”和退出码）')
    r = analyze(DENSITY_SYNTH, 'synthetic', clarity=clarity)
    text = render(r, hazards=False).split('\n')
    js = json.loads(json.dumps(r, ensure_ascii=False))
    counts = dict((m['key'], m['count']) for m in r['metrics'])
    good = (counts['bushi'] == 1 and counts['coda'] == 1 and r['exit_code'] == 0
            and r['over_p90_count'] == 0)
    for key, label in (('bushi', '不是……而是'), ('coda', '段末升华')):
        want = DENSITY_WANT[key]
        got = [h['line'] for h in js.get('density_hits', {}).get(key, [])]
        rows = [i for i, ln in enumerate(text) if ln.startswith(label)]
        under = text[rows[0] + 1:rows[0] + 1 + len(want)] if rows else []
        ok = (got == want and len(rows) == 1
              and all(ln.startswith('    L%d: ' % n) for ln, n in zip(under, want))
              and len(under) == len(want)
              and all(len(h['quote']) <= DENSITY_QUOTE_MAX for h in js['density_hits'][key]))
        good &= ok
        print('  %s %s：JSON 行号 %s；文本行下 %s' % ('通过' if ok else '不通过', label, got,
                                              '｜'.join(ln.strip() for ln in under) or '无'))
    print('  %s 计数 不是……而是 %d、段末升华 %d，高于 90 分位 %d 项，退出码 %d'
          % ('通过' if good else '不通过', counts['bushi'], counts['coda'],
             r['over_p90_count'], r['exit_code']))
    return good


def selftest(letters, clarity=False):
    ok = True
    print('== 规则自检（合成样例：H1/H5/H6 保留硬伤，H2–H4 转语义复核）' if clarity else
          '== 规则自检（合成样例：每条硬伤各自要抓到，反例要放过）')
    for want, text in SYNTH:
        r = analyze(text, 'synthetic', clarity=clarity)
        got = sorted(set(h['code'] for h in r['hard']))
        expected = [] if not want or (clarity and want in SEMANTIC_REVIEW_CODES) else [want]
        good = got == expected and r['exit_code'] == bool(expected)
        if clarity:
            reviews = sorted(set(h['code'] for h in r['semantic_reviews']))
            good &= reviews == ([want] if want in SEMANTIC_REVIEW_CODES else [])
        ok &= good
        print('  %s 期望 %s，得到 %s' % ('通过' if good else '不通过', expected or '无硬伤', got or '无硬伤'))
    print()
    ok &= selftest_h7(clarity)
    print()
    ok &= selftest_density(clarity)
    print()
    if clarity:
        ok &= selftest_clarity()
        print()
        ok &= selftest_h9()
        print()
    ok &= selftest_hazards()
    print()
    for fn in EXEMPLARS:
        p = os.path.join(CORPUS_DIR, fn)
        print('== 范本 %s' % fn)
        if not os.path.exists(p):
            print('缺文件：%s' % p)
            ok = False
            continue
        r = analyze(read(p), fn, clarity=clarity)
        print(render(r, hazards=False))
        print(hazard_count_line(r))
        # H6 hits in the exemplars are true positives in pre-2026-10-17 author
        # text, not false alarms; the exemplar check guards against false alarms.
        legacy = sum(1 for h in r['hard'] if h['code'] == 'H6')
        good = len(r['hard']) == legacy
        ok &= good
        print('自检：%s 硬伤 %d（其中 H6 分号 %d 处：10-17 裁定前的作者原文，只报不计）→ %s'
              % (fn, len(r['hard']), legacy, '通过' if good else '不通过'))
        print()
    print('== 对照 2026.02（AI 辅助那期）')
    if os.path.exists(letters):
        issues = dict(split_issues(letters))
        if CONTROL_ISSUE not in issues:
            print('合辑里找不到 %s：对照不通过。' % CONTROL_ISSUE)
            ok = False
        else:
            r = analyze(issues[CONTROL_ISSUE], '月报合辑 %s（AI 辅助，对照）' % CONTROL_ISSUE,
                        clarity=clarity)
            print(render(r, hazards=False))
            print(hazard_count_line(r))
            good = len(r['hard']) >= 1 or r['over_p90_count'] >= 2
            ok &= good
            print('自检：2026.02 硬伤 %d、高于作者 90 分位 %d 项 → %s（要求硬伤 ≥1 或至少两项超 90 分位）'
                  % (len(r['hard']), r['over_p90_count'], '抓到' if good else '没抓到'))
    else:
        print('未找到月报合辑 %s：跳过 2026.02 对照（范本两篇照常自检）。' % letters)
    print()
    print('自检结果：%s' % ('全部通过' if ok else '有不通过项'))
    return 0 if ok else 1


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog='voice_check.py',
        description='FICCVoice v%s (%s): default H1-H6 set exit 1; --clarity keeps only H1/H5/H6 hard; '
                    'H7 (cross-paragraph repetition, triggers A and B) is a review candidate in both modes; '
                    'H9 (nominalized views) is a review candidate under --clarity only. '
                    'Counts never set exit 1; two flagged style rows still need cleanup; '
                    'the 不是……而是 and 段末升华 rows list each hit.' % (VERSION, VERSION_DATE))
    ap.add_argument('file', nargs='?', help='markdown file to check')
    ap.add_argument('--lecture', action='store_true', help='lecture register: no hints on 我 / brackets')
    ap.add_argument('--clarity', action='store_true',
                    help='H2-H4 become semantic-review candidates; H1/H5/H6 remain hard')
    ap.add_argument('--json', action='store_true', help='machine-readable output')
    ap.add_argument('--names', metavar='OUTLINE.md',
                    help='outline whose name table (名字 / 不许用 columns) is checked against the text')
    ap.add_argument('--hazards-only', action='store_true',
                    help='print only review candidates (H7 in both modes, H2-H4 with --clarity; exit code unchanged)')
    ap.add_argument('--selftest', action='store_true', help='exemplars must pass; 2026.02 must be caught')
    ap.add_argument('--baseline', action='store_true', help='recompute author baseline and print it')
    ap.add_argument('--letters', default=DEFAULT_LETTERS, help='monthly-letter collection (txt)')
    ap.add_argument('--extra', nargs='*', default=None,
                    help='extra author texts for --baseline (default: references/corpus/*.md)')
    ap.add_argument('--per-doc', action='store_true', help='with --baseline: print per-document densities')
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest(a.letters, clarity=a.clarity)
    if a.baseline:
        if not os.path.exists(a.letters):
            print('找不到月报合辑：%s' % a.letters, file=sys.stderr)
            return 2
        extras = a.extra if a.extra is not None else [
            os.path.join(CORPUS_DIR, f) for f in sorted(os.listdir(CORPUS_DIR)) if f.endswith('.md')]
        return run_baseline(a.letters, extras, a.per_doc)
    if not a.file:
        ap.print_help()
        return 2
    if not os.path.exists(a.file):
        print('找不到文件：%s' % a.file, file=sys.stderr)
        return 2
    names = None
    if a.names:
        if not os.path.exists(a.names):
            print('找不到提纲：%s' % a.names, file=sys.stderr)
            return 2
        names = parse_names(read(a.names), a.names)
    r = analyze(read(a.file), os.path.basename(a.file), lecture=a.lecture, names=names, clarity=a.clarity)
    if a.json and a.hazards_only:
        keys = ('file', 'version', 'hazards', 'hazard_counts', 'hazard_skipped',
                'clause_histogram', 'names_conditional_count', 'names', 'semantic_reviews')
        if a.clarity:
            keys += ('mode',)
        print(json.dumps(dict((k, r[k]) for k in keys), ensure_ascii=False, indent=2))
    elif a.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    elif a.hazards_only:
        print('voice_check v%s｜%s' % (r['version'], r['file']))
        print(render_semantic_reviews(r))
        print(render_hazards(r))
    else:
        print(render(r))
    return r['exit_code']


if __name__ == '__main__':
    sys.exit(main())
