#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""outline_slice.py (2026-10-25; 1.0.1 2026-11-05; 1.1.0 2026-11-11; 1.2.0 2026-11-21) -- slice a FICC outline (<文稿名>-提纲.md) by node id.

Outline format: FICCOutline.md 4.2; node ids N-prefixed, dotted, positional (N0 is the root,
N3.1 sits under N3).  The outline file stays the one home: every slice is printed to stdout
and nothing is written back.  Standard library only; parsing adapted from kit-1.2.0
(kitlib.node_blocks) and voice_check.py (name table).  Node headings are read with
cjk_ids.NODE_HEADING_RE (same directory, required): the id may be glued to the heading text
("## N1一、…", "### N1.9总起"); 1.0.0 used `\b` there, which cut "N1.9总起" to N1 and dropped
"## N1一、…" (1104 draft task: 81 of 91 nodes found).
Field lines (任务, 顺序, 关系, 标注, 展开, 收尾) are read in both spellings, '任务：' and '**任务**：' / '**任务：**'
(1.1.0; 1.0.1 read only the plain one, so a bold outline lost every 任务, 顺序 and 关系 line in chain and view).
'收尾：' (1.1.0, second part) assigns a section's close: its text starts with the id of the node whose unit
writes the close (a whole token, R6; free text may follow) or is a waiver '不设（<who ruled, why>）' (R7; never on
N0).  Only a top-level bullet counts, read with its continuation lines (R11).
1.2.0 reads the single living outline (FICCOutline.md §4.2) as JSON (`fields`): the H1 revisions
'# …｜树r3｜材料r2｜截至…', the question card (研究问题, 目标读者, 范围排除, Q-rows split on '｜' into 判断, 门槛, 分母,
窗口, 删去后…, 若材料未决), the edge table (ends sorted by numeric id tuple, key 'N2.1—N3.2', status 已定/待据/不成立;
edge_conflicts: one sorted key on two or more rows), the renumber list ('- 旧号→新号｜树r<k>'), and per node the
slot lines 〔标题〕 **主旨** 任务 顺序 接前 分担 边 展开 收尾 事实 算式 消歧 段k/段 (repeated labels kept in order) plus the
legacy 关系 and 标注.  Both label spellings, top-level lines only, continuation lines joined, cells split on '｜',
placeholder text <…> kept raw (a gate decides).  Library: living_fields(block_lines), tree_head(text), fields_json.
1.2.0 (W1-O2) adds `check-0to1`, the pre-prose gates of FICCOutline.md §9 and FICCStructure.md §7 in machine form, read off fields_json:
(a) Z-SWAP a metric (number with a METRIC_UNITS unit or a currency) in a 主旨 判断/因 slot, N0 included; identifiers
pass the swap test (ids, years, quarters, FY25, 第2期, months, dates); a bare number is Z-SWAP? (warning).
(b) Z-DENOM a ratio 门槛 (% / x 倍 率 比 bp) with an empty or <…> 分母; Z-Q no Q row, more than 4, or a Q whose 门槛,
窗口 or 删去后会答错什么 is empty, <…> or a bare 会/是/无.  (c) Z-SHARE a node with children lacking a 分担 row, a
无人担/重复担/子项合计仍证不出 cell not reading 无, an item naming a non-child, a child in no item.  (d) Z-EDGE one
sorted key on rows of different status (both ids named; same status: Z-EDGE?, warning), an endpoint not two node
ids with blocks, no status, 已定 with an empty/<…> 凭据, 已定 causal (CAUSAL_WORDS) with no '@' in 凭据, a causal
接前 (node or 段 row) with no '@'.  (e) Z-FACT one anchor 写全 in two nodes, a 回指 to an anchor 写全 nowhere or naming
the wrong 写全处; Z-QUOTE (with --sources NAME=PATH) a 消歧 quote not a verbatim substring of its anchor's source,
whitespace-normalised, or a source not given; without --sources Z-QUOTE-SKIP.  (f) Z-PARA a heavy node (>5 写全
facts or any 算式) with no 段k row (段：不拆 does not excuse it), a 段 row citing >5 facts; Z-SIGN (warning) an
unsigned 算式 row.  Library: gate_findings(text, sources), swap_tokens(text).

Usage:
  outline_slice.py nodes OUTLINE [--check] [--closes]
                                                id, depth, heading text per node block;
                                                --check exits 2 when a block lacks a **主旨** line;
                                                --closes (implies --check): every node with three or more
                                                children, N0 included, needs a 收尾 line (CLOSE-UNASSIGNED);
                                                a 收尾 line on any node is validated (R10): it names a
                                                descendant with a block (CLOSE-BAD-TARGET), starts with a
                                                whole id or 不设 (CLOSE-UNREADABLE), a waiver carries a
                                                non-empty parenthesis (CLOSE-WAIVER-NO-REASON) and is not on
                                                N0 (CLOSE-WAIVED-ROOT), one per block (CLOSE-DUPLICATE); exit 2
  outline_slice.py node OUTLINE ID [ID ...]     those node blocks verbatim, in document order
  outline_slice.py chain OUTLINE ID [ID ...] [--path [N]]
                                                ancestors of ID (root first, ID excluded).  Default: per
                                                ancestor the heading, its own 〔标题〕 line (dropped when it
                                                repeats the heading text, enclosing 《》 ignored) and its 任务
                                                line, in document order; nothing else.
                                                --path: after a usage line, per ancestor the heading; the
                                                〔标题〕 line as above; for N0 and for an ancestor with no
                                                〔标题〕 or only '〔标题〕无…', '- 主旨（开头）：' (asides cut,
                                                two sentences or 200 characters, then a pointer); the 任务
                                                line; below the root, '- 关系（对上一级）：' (the clause naming
                                                its parent, else its 关系 lines verbatim; a placeholder 关系
                                                line, empty or 待回填…, prints nothing) and, when ID sits on
                                                that ancestor's first or last edge, its 顺序 line.
                                                --path N (integer >= 1): as --path for the nearest N ancestors
                                                of each id only.  Put --path after the ids.
                                                Every mode: an ancestor whose single 收尾 line names a node
                                                under it whose subtree's last node (document order; the
                                                node itself when childless) is one of the ids (R8) gets
                                                '- 收尾（本单元写；照 FICCVoice.md C17：…）：<text>' at the end
                                                of its block (R12); outside --path N it prints as its
                                                heading and that line only.
                                                Several ids (a writing unit, R5): one comment line naming
                                                them, the usage line once (--path), every ancestor of any
                                                id once (root first, document order; an ancestor that is
                                                itself one of the ids is left out), the fields being the
                                                union over the ids (顺序 when at least one id is on its edge)
  outline_slice.py names OUTLINE (--ids ID ... | --text FILE ...)
                                                name-table header + the rows whose terms occur in
                                                those node blocks or files; 'kept K of N rows' on stderr
  outline_slice.py view OUTLINE                 brief view: heading, 〔标题〕, **主旨**, 任务：, 顺序：,
                                                关系：, 收尾： lines of every node
  outline_slice.py fields OUTLINE [ID ...]      JSON on stdout (always JSON): version, outline, tree_rev, material_rev,
                                                card, edges, edge_conflicts, renumber, nodes {id: heading, line, parent,
                                                children, gist, task, order, follows, edges, share, expand, close, title,
                                                facts, derivations, disambig, paras, legacy}; no ids = every node
  outline_slice.py check-0to1 OUTLINE [--sources NAME=PATH ...] [--json]
                                                the pre-prose gates: one line per finding 'CODE where: why
                                                (line N)' (where = node, Q, edge id or sorted key, 'N1.2 段2',
                                                fact anchor, '-'), or --json: a list of {code, sev, where, why,
                                                line}, sev hard / warn / skip; counts on stderr; exit 2 on any
                                                hard finding.  Also `nodes OUTLINE --check-0to1 [--sources …]`:
                                                the node rows (and --check/--closes lines), then the findings
  outline_slice.py --self-test                  synthetic fixture, assertions for every subcommand
                                                (--selftest is an alias, K-OS-2)
  outline_slice.py --version

Exit codes: 0 ok; 2 unknown id, a node block without a **主旨** line (nodes --check), duplicate
node ids (nodes --check), a close finding (nodes --closes), N after --path not an integer >= 1,
no name table (names), unreadable file (fields and --sources included), a hard gate finding (check-0to1, nodes
--check-0to1), a bad --sources entry or --sources without --check-0to1; 1 a failed self-test.
"""
import argparse
import contextlib
import io
import json
import os
import re
import sys
import tempfile
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cjk_ids  # noqa: E402  (sibling module; the one home of the id patterns)

VERSION = '1.2.0'
NODE_RE = cjk_ids.NODE_HEADING_RE
TREE_END_RE = re.compile(r'^#{1,2}\s+(?!N\d)')          # a non-node '#'/'##' heading ends the tree
FIELD_RE = r'^\s*(?:[-*+]\s+)?'
FIELD_LABELS = ('任务', '顺序', '关系', '标注', '展开', '收尾')
ID_CORE = r'N\d+(?:\.\d+)*'
ID_END = r'(?![A-Za-z0-9_]|\.[A-Za-z0-9_])'          # R6: a whole token (N1.3X, N1.3.abc, N1.3e2, N1X are not ids)


def label_pat(pat):
    """field_label for a label given as a regex (1.2.0: '段([0-9]*)', '范围排除（…）')."""
    return r'(?:\*\*(?:%s)(?:\*\*\s*[：:]|[：:]\*\*)|(?:%s)[：:])' % (pat, pat)


def field_label(label):
    """Unanchored pattern for one field label in either spelling: '任务：', '**任务**：', '**任务：**'
    (full-width or ASCII colon).  The one home of the field spellings (1.1.0, K-OS-1 wave)."""
    return label_pat(re.escape(label))


def field_re(label):
    return re.compile(FIELD_RE + field_label(label))


GIST_RE = re.compile(FIELD_RE + r'\*\*主旨(?:\*\*|：\*\*)')
GIST_LABEL_RE = re.compile(FIELD_RE + r'\*\*主旨(?:\*\*\s*[：:]?|[：:]\*\*)\s*')
TITLE_RE = re.compile(FIELD_RE + r'〔标题〕')
TITLE_LABEL_RE = re.compile(FIELD_RE + r'〔标题〕\s*')
TASK_RE = field_re('任务')
ORDER_RE = field_re('顺序')
REL_RE = field_re('关系')
REL_LABEL_RE = re.compile(FIELD_RE + field_label('关系') + r'\s*')
CLOSE_RE = field_re('收尾')
CLOSE_LABEL_RE = re.compile(FIELD_RE + field_label('收尾') + r'\s*')
CLOSE_ID_RE = re.compile('(' + ID_CORE + ')' + ID_END)
CLOSE_DUTY = '- 收尾（本单元写；照 FICCVoice.md C17：收拢已立的判断并往前一步，不换说法重申主旨）：'   # R12
VIEW_RE = re.compile(FIELD_RE + r'(?:〔标题〕|\*\*主旨(?:\*\*|：\*\*)|'
                     + '|'.join(field_label(x) for x in ('任务', '顺序', '关系', '收尾')) + ')')
ANY_FIELD_RE = re.compile(FIELD_RE + r'(?:(?:\*\*)?〔标题〕|\*\*主旨(?:\*\*|：\*\*)|把握[：:]|'
                          + '|'.join(field_label(x) for x in FIELD_LABELS) + ')')
BULLET_RE = re.compile(FIELD_RE)
CLAUSE_RE = re.compile(r'(?:^|[，；。,;：:])[ \t]*(和)\s*(?=N\d)', re.M)  # clause start: '和<ids>，通过…，是…'
VIA_RE = re.compile(r'[，,]\s*通过')
ID_TOKEN_RE = re.compile(r'(?<![A-Za-z0-9_.])' + ID_CORE + ID_END)
SENT_END_RE = re.compile(r'[。！？][”’」』]*')
HEAD_MARK_RE = re.compile(r'\s*〔[^〔〕]*〕\s*$')
GIST_CAP = 200
CHAIN_USAGE = ('上级链（根在前；只读，不写进正文，“收尾（本单元写…）”一行除外：那一行是本单元要写的收尾）：用它判断本节点在全文里走的是哪一步、材料的哪一面承重、把握度写到哪一档。'
               '正文只写本节点对父节点的那一步，不重申上级主旨，不解释本节点为什么重要。')
SEP_RE = re.compile(r'^\s*\|?\s*:?-{2,}')
ASIDE_RE = re.compile(r'（[^（）]*）|\([^()]*\)|【[^【】]*】|\[[^\[\]]*\]')
TERM_SPLIT_RE = re.compile(r'[、，,；;/／]')
TERM_STRIP = '“”"‘’\'「」『』《》〈〉`'


class SliceError(Exception):
    """A loud failure: message on stderr, exit 2."""


# ------------------------------------------------------------------ parsing
def read(path):
    try:
        with open(path, encoding='utf-8') as fh:
            return fh.read().replace('\r\n', '\n')
    except OSError as e:
        raise SliceError('cannot read %s: %s' % (path, e))


def node_blocks_at(text):
    """[(id, heading text, [lines], heading line number from 1)] in document order (1.2.0, for fields)."""
    blocks, cur = [], None
    for no, line in enumerate(text.split('\n'), 1):
        m = NODE_RE.match(line)
        if m:
            cur = (m.group(2), m.group(3).strip(), [line], no)
            blocks.append(cur)
        elif cur is not None:
            if TREE_END_RE.match(line):
                cur = None
                continue
            cur[2].append(line)
    for _, _, lines, _ in blocks:
        while lines and not lines[-1].strip():
            lines.pop()
    return blocks


def node_blocks(text):
    """[(id, heading text, [lines])] in document order, as kitlib.node_blocks (trailing blanks cut)."""
    return [(nd, head, lines) for nd, head, lines, _ in node_blocks_at(text)]


def index(blocks):
    out = {}
    for nd, head, lines in blocks:
        out.setdefault(nd, (head, lines))
    return out


def duplicates(blocks):
    seen, dup = set(), []
    for nd, _, _ in blocks:
        if nd in seen and nd not in dup:
            dup.append(nd)
        seen.add(nd)
    return dup


def depth(nd):
    return 0 if nd == 'N0' else nd.count('.') + 1


def ancestors(nd):
    """N3.1.2 -> [N0, N3, N3.1]; N3 -> [N0]; N0 -> []."""
    if nd == 'N0':
        return []
    parts = nd[1:].split('.')
    return ['N0'] + ['N' + '.'.join(parts[:k]) for k in range(1, len(parts))]


def require(idx, ids):
    unknown = [nd for nd in ids if nd not in idx]
    if unknown:
        raise SliceError('unknown node id: %s' % ', '.join(unknown))


def cells(row):
    row = row.strip()
    if row.startswith('|'):
        row = row[1:]
    if row.endswith('|'):
        row = row[:-1]
    return [c.strip() for c in row.split('|')]


def name_table(text):
    """(header, separator, rows, (名字, 本篇写法, 不许用) column indexes) of the first Markdown
    table whose header has a 名字 column and a 不许用 column, as voice_check.parse_names."""
    lines = text.split('\n')
    for i, ln in enumerate(lines):
        if not ln.strip().startswith('|') or i + 1 >= len(lines):
            continue
        head = cells(ln)
        ni = next((k for k, c in enumerate(head) if '名字' in c), None)
        fi = next((k for k, c in enumerate(head) if '不许用' in c), None)
        if ni is None or fi is None or not SEP_RE.match(lines[i + 1]):
            continue
        wi = next((k for k, c in enumerate(head) if '本篇写法' in c), None)
        rows = []
        for j in range(i + 2, len(lines)):
            if not lines[j].strip().startswith('|'):
                break
            rows.append(lines[j])
        return ln, lines[i + 1], rows, tuple(k for k in (ni, wi, fi) if k is not None)
    raise SliceError('no name table (a Markdown table whose header has a 名字 column and a '
                     '不许用 column)')


def terms(cell):
    """Terms of one cell: bracketed asides dropped, split on 、，,；;/／, quotes/backticks/brackets
    stripped, terms of at least 2 characters."""
    prev = None
    while prev != cell:
        prev, cell = cell, ASIDE_RE.sub('', cell)
    out = []
    for t in TERM_SPLIT_RE.split(cell):
        t = t.strip().strip(TERM_STRIP).strip()
        t = ''.join(ch for ch in t if ch not in TERM_STRIP)
        if len(t) >= 2:
            out.append(t)
    return out


# ------------------------------------------------------------------ subcommands
def cmd_nodes(a, out):
    text = read(a.outline)
    if a.sources is not None and not a.check_0to1:
        raise SliceError('--sources goes with --check-0to1')
    sources = parse_sources(a.sources) if a.check_0to1 else None
    blocks = node_blocks(text)
    for nd, head, _ in blocks:
        out.write('%s\t%d\t%s\n' % (nd, depth(nd), head))
    code = nodes_check(a, blocks, out) if (a.check or a.closes) else 0
    if a.check_0to1:
        code = max(code, emit_findings(gate_findings(text, sources), out))
    return code


def nodes_check(a, blocks, out):
    """nodes --check / --closes on the blocks (1.1.0 behaviour, output unchanged)."""
    missing = [nd for nd, _, lines in blocks if not any(GIST_RE.match(l) for l in lines)]
    dup = duplicates(blocks)
    n = len(blocks)
    out.write('check: %d node blocks, %d with a **主旨** line, %d duplicate ids\n'
              % (n, n - len(missing), len(dup)))
    if missing:
        print('nodes --check: no **主旨** line in: ' + ', '.join(missing), file=sys.stderr)
    if dup:
        print('nodes --check: duplicate node ids: ' + ', '.join(dup), file=sys.stderr)
    found = []
    if a.closes:
        k, found = close_findings(blocks)
        out.write('closes: %d nodes with three or more children, %d findings\n' % (k, len(found)))
        out.write(''.join(f + '\n' for f in found))
        if found:
            print('nodes --check --closes: %d close findings' % len(found), file=sys.stderr)
    return 2 if missing or dup or found else 0


def indent(l):
    return len(l) - len(l.lstrip())


def join_cont(parts):
    """Join a field line's text and its continuation texts: no space between two CJK sides, else one space."""
    out = parts[0]
    for x in parts[1:]:
        out += ('' if out and ord(out[-1]) > 0x2E7F and ord(x[0]) > 0x2E7F else ' ') + x
    return out


def close_entries(lines):
    """The block's 收尾 entries, each the text after the label joined with its continuation lines (deeper indent,
    not a field line).  Only lines at the block's top indent count; a nested sub-bullet is not the node's (R11)."""
    body = lines[1:]
    inds = [indent(l) for l in body if l.strip()]
    top = min(inds) if inds else 0
    out, k = [], 0
    while k < len(body):
        l = body[k]
        k += 1
        if not CLOSE_RE.match(l) or indent(l) != top:
            continue
        parts = [CLOSE_LABEL_RE.sub('', l, count=1).strip()]
        while k < len(body) and body[k].strip() and not ANY_FIELD_RE.match(body[k]) and indent(body[k]) > indent(l):
            parts.append(BULLET_RE.sub('', body[k], count=1).strip())
            k += 1
        out.append(join_cont([x for x in parts if x] or ['']))
    return out


def close_target(text):
    """'不设' (a waiver), the node id the 收尾 text starts with (a whole token, R6), or None (unreadable)."""
    t = text.lstrip('*').strip()
    if t.startswith('不设'):
        return '不设'
    m = CLOSE_ID_RE.match(t)
    return m.group(1) if m else None


def waiver_ground(text):
    """The text of the parenthesis right after 不设 (full-width or ASCII, nesting allowed), stripped; '' if none (R7)."""
    t = text.lstrip('*').strip()[2:].lstrip()
    if not t or t[0] not in '（(':
        return ''
    depth, got = 0, []
    for ch in t:
        if ch in '（(':
            depth += 1
            if depth == 1:
                continue
        elif ch in '）)':
            depth -= 1
            if depth == 0:
                return ''.join(got).strip()
        got.append(ch)
    return ''


def subtree_last(blocks):
    """{id: the last node, in document order, of its subtree (itself when childless)} over the node blocks."""
    last = {}
    for nd, _, _ in blocks:
        for x in [nd] + ancestors(nd):
            last[x] = nd
    return last


def close_findings(blocks):
    """(number of nodes with three or more children, [finding lines]) in document order."""
    idx, kids = index(blocks), children(blocks)
    k, out = 0, []
    for nd, (_, lines) in idx.items():
        n = len(kids.get(nd, []))
        k += n >= 3
        ents = close_entries(lines)
        tg = close_target(ents[0]) if len(ents) == 1 else None
        if not ents:
            if n >= 3:                                                  # R10: only this one needs 3+ children
                out.append('CLOSE-UNASSIGNED %s (%d children)' % (nd, n))
        elif len(ents) > 1:
            out.append('CLOSE-DUPLICATE %s' % nd)                       # R9
        elif tg is None:
            out.append('CLOSE-UNREADABLE %s' % nd)
        elif tg == '不设':
            if nd == 'N0':
                out.append('CLOSE-WAIVED-ROOT %s' % nd)                 # R7
            elif not waiver_ground(ents[0]):
                out.append('CLOSE-WAIVER-NO-REASON %s' % nd)            # R7
        elif tg not in idx or nd not in ancestors(tg):
            out.append('CLOSE-BAD-TARGET %s -> %s' % (nd, tg))
    return k, out


def cmd_node(a, out):
    blocks = node_blocks(read(a.outline))
    require(index(blocks), a.ids)
    want = set(a.ids)
    done = set()
    parts = []
    for nd, _, lines in blocks:
        if nd in want and nd not in done:
            parts.append('\n'.join(lines))
            done.add(nd)
    out.write('\n\n'.join(parts) + '\n')
    return 0


def children(blocks):
    """{parent id: [child ids in document order]} over the node blocks present."""
    kids = {}
    for nd, _, _ in blocks:
        if nd == 'N0':
            continue
        sib = kids.setdefault(ancestors(nd)[-1], [])
        if nd not in sib:
            sib.append(nd)
    return kids


def on_edge(anc, nd, kids):
    """True when every node on the path from anc's child down to nd is the first child of its parent, or
    every one is the last (document order; an only child is both)."""
    path = ancestors(nd) + [nd]
    sub = path[path.index(anc) + 1:]
    sibs = [kids.get(ancestors(x)[-1]) or [None] for x in sub]
    return all(s[0] == x for s, x in zip(sibs, sub)) or all(s[-1] == x for s, x in zip(sibs, sub))


def strip_asides(text):
    prev = None
    while prev != text:
        prev, text = text, ASIDE_RE.sub('', text)
    return text


def gist_opening(nd, body):
    """'- 主旨（开头）：…' for an ancestor without 〔标题〕: asides cut, then up to the second sentence end or
    GIST_CAP characters, whichever comes first, and a pointer when that is shorter than the cut 主旨."""
    g = next((l for l in body if GIST_RE.match(l)), None)
    if g is None:
        return None
    text = strip_asides(GIST_LABEL_RE.sub('', g, count=1)).strip()
    ends = [m.end() for m in SENT_END_RE.finditer(text)]
    cut = min(ends[1] if len(ends) >= 2 else len(text), GIST_CAP)
    head = text[:cut]
    if len(head) < len(text):
        head += '……（全文：node %s）' % nd
    return '- 主旨（开头）：' + head


def rel_text(rel):
    """The text of 关系 lines: label and list bullets cut, lines joined by newlines."""
    return '\n'.join(REL_LABEL_RE.sub('', l, count=1) if REL_RE.match(l) else BULLET_RE.sub('', l, count=1)
                     for l in rel)


def relation_entries(body):
    """[(entry lines, text)] of the node's 关系 entries: a 关系 line with its continuation lines (deeper indent, or
    a bare '和N…' line), verbatim, and its text (rel_text, stripped).  A placeholder entry (no text after the
    label, continuation included, or text starting with 待回填) is left out (T0 ruling R2, 2026-11-11)."""
    out, k = [], 0
    while k < len(body):
        if not REL_RE.match(body[k]):
            k += 1
            continue
        ind = len(body[k]) - len(body[k].lstrip())
        entry = [body[k]]
        k += 1
        while k < len(body) and body[k].strip() and not ANY_FIELD_RE.match(body[k]) and (
                len(body[k]) - len(body[k].lstrip()) > ind or BULLET_RE.sub('', body[k], count=1).startswith('和')):
            entry.append(body[k])
            k += 1
        text = rel_text(entry).strip().strip('*').strip()
        if text and not text.startswith('待回填'):
            out.append((entry, text))
    return out


def relation_lines(body):
    """The node's 关系 lines with their continuation lines, verbatim; placeholder entries left out (R2)."""
    return [l for entry, _ in relation_entries(body) for l in entry]


def parent_clauses(rel, parent):
    """Clauses '和<ids>，通过…，是…' of the 关系 lines whose endpoint (between 和 and the first '，通过'; without
    a '，通过', up to the first comma) holds parent as an exact id token (N3 never matches N3.1 or N31)."""
    text = rel_text(rel)
    starts = [m.start(1) for m in CLAUSE_RE.finditer(text)]
    out = []
    for i, s in enumerate(starts):
        cl = text[s:starts[i + 1] if i + 1 < len(starts) else len(text)].rstrip('，；。,;：: \t\n')
        m = VIA_RE.search(cl)
        end = cl[1:m.start()] if m else re.split(r'[，,；;。]', cl[1:], maxsplit=1)[0]
        if parent in ID_TOKEN_RE.findall(end):
            out.append(' '.join(cl.split()))
    return out


def unquote(s):
    """Drop one pair of enclosing 《》 (K-OS-1 comparison, T0 ruling R3, 2026-11-11)."""
    return s[1:-1].strip() if len(s) >= 2 and s[0] == '《' and s[-1] == '》' else s


def heading_core(head):
    """Heading text without the leading colon and trailing 〔…〕 marks, for the K-OS-1 comparison."""
    head = head.lstrip('：: ').strip()
    prev = None
    while prev != head:
        prev, head = head, HEAD_MARK_RE.sub('', head).strip()
    return head


def title_text(l):
    """Text of a 〔标题〕 line after the label."""
    return TITLE_LABEL_RE.sub('', l, count=1).strip().strip('*').strip()


def repeats_heading(t, head):
    """K-OS-1: the 〔标题〕 text t repeats the heading text (enclosing 《》 ignored, R3)."""
    return unquote(t) == unquote(heading_core(head))


def default_lines(entry):
    """Default chain lines of one ancestor: heading, own 〔标题〕 lines (not repeating the heading) and 任务
    lines, in document order (1.1.0 second part: the path-to-root content sits behind --path)."""
    head, lines = entry
    return [lines[0]] + [l for l in lines[1:] if TASK_RE.match(l)
                         or (TITLE_RE.match(l) and not repeats_heading(title_text(l), head))]


def duty_line(anc, entry, ids, idx, last):
    """CLOSE_DUTY + text when anc's one 收尾 line names a node with a block under anc and the last node of that
    node's subtree (document order) is one of ids (R8); None otherwise (no 收尾 line, two (R9), 不设, unreadable,
    a target outside anc or without a block)."""
    ents = close_entries(entry[1])
    tg = close_target(ents[0]) if len(ents) == 1 else None
    if tg in (None, '不设') or tg not in idx or anc not in ancestors(tg):
        return None
    return CLOSE_DUTY + ents[0] if last[tg] in ids else None


def ancestor_lines(anc, entry, nds, kids):
    """Chain lines of one ancestor for the ids nds below it (one id, or the unit's ids under anc)."""
    head, lines = entry
    body = lines[1:]
    out = [lines[0]]
    titled = '〔标题〕' in lines[0]
    for l in body:
        if TITLE_RE.match(l):
            t = title_text(l)
            titled = titled or not t.startswith('无')                   # R1: '〔标题〕无…' is untitled
            if not repeats_heading(t, head):
                out.append(l)                                           # K-OS-1: no line repeating the heading
    if not titled or anc == 'N0':                                       # R4: the root always gets it
        g = gist_opening(anc, body)
        if g:
            out.append(g)
    out += [l for l in body if TASK_RE.match(l)]
    if anc != 'N0':
        rel = relation_lines(body)
        if rel:
            cl = parent_clauses(rel, ancestors(anc)[-1])
            out += ['- 关系（对上一级）：' + c for c in cl] if cl else rel
        if any(on_edge(anc, nd, kids) for nd in nds):
            out += [l for l in body if ORDER_RE.match(l)]
    return out


def cmd_chain(a, out):
    blocks = node_blocks(read(a.outline))
    idx = index(blocks)
    ids = list(dict.fromkeys(a.ids))
    require(idx, ids)
    kids, last = children(blocks), subtree_last(blocks)
    order, first_of = [], {}                       # ancestors of any id, each once; the first id naming it
    for nd in ids:
        for anc in ancestors(nd):
            if anc not in ids and anc not in first_of:
                first_of[anc] = nd
                order.append(anc)
    if len(ids) > 1:                               # R5: root first, then document order
        pos = dict((nd, k) for k, (nd, _, _) in reversed(list(enumerate(blocks))))
        order.sort(key=lambda x: (x != 'N0', pos.get(x, len(blocks))))
    path = a.path is not None                      # --path [N]; const 0 = every ancestor
    near = None if not a.path else set(x for nd in ids for x in ancestors(nd)[-a.path:])
    parts = []
    for anc in order:
        if anc not in idx:
            if near is None or anc in near:
                print('WARNING: ancestor %s of %s has no node block' % (anc, first_of[anc]), file=sys.stderr)
            continue
        duty = duty_line(anc, idx[anc], ids, idx, last)
        if near is not None and anc not in near:   # outside --path N: heading and duty line only
            if duty:
                parts.append(idx[anc][1][0] + '\n' + duty)
            continue
        if path:
            nds = [nd for nd in ids if anc in ancestors(nd)]
            lines = ancestor_lines(anc, idx[anc], nds, kids)
        else:
            lines = default_lines(idx[anc])
        parts.append('\n'.join(lines + ([duty] if duty else [])))
    out.write('<!-- ancestor chain of %s, outline_slice.py %s -->\n' % (' '.join(ids), VERSION))
    if parts:
        out.write((CHAIN_USAGE + '\n\n' if path else '') + '\n\n'.join(parts) + '\n')
    return 0


def path_n(s):
    """N after --path: an integer >= 1 (ASCII digits)."""
    if not re.fullmatch(r'[0-9]+', s) or int(s) < 1:
        raise argparse.ArgumentTypeError('N must be an integer >= 1, got %r' % s)
    return int(s)


def cmd_names(a, out):
    text = read(a.outline)
    head, sep, rows, cols = name_table(text)
    if a.ids:
        idx = index(node_blocks(text))
        require(idx, a.ids)
        body = '\n'.join('\n'.join(idx[nd][1]) for nd in a.ids)
    else:
        body = '\n'.join(read(p) for p in a.text)
    kept = []
    for r in rows:
        c = cells(r)
        if any(t in body for k in cols if k < len(c) for t in terms(c[k])):
            kept.append(r)
    out.write('\n'.join([head, sep] + kept) + '\n')
    print('kept %d of %d rows' % (len(kept), len(rows)), file=sys.stderr)
    return 0


def cmd_view(a, out):
    blocks = node_blocks(read(a.outline))
    parts = ['\n'.join([lines[0]] + [l for l in lines[1:] if VIEW_RE.match(l)]) for _, _, lines in blocks]
    out.write('<!-- brief view, outline_slice.py %s; the outline file stays the one home -->\n' % VERSION)
    if parts:
        out.write('\n\n'.join(parts) + '\n')
    return 0


# ------------------------------------------------------------------ living outline (fields, 1.2.0)
# The single living outline <文稿>-提纲.md (FICCOutline.md §4.2): a tree head (H1 revisions, question card, edge table,
# renumber list) and per-node slot lines.  Labels in both spellings; only a node's top-level lines count (R11);
# cells split on '｜'; placeholder text in <…> is kept raw (a gate decides, W1-O2).
PARA_PAT = r'段([0-9]*)'
LIVING_LABELS = ('任务', '顺序', '接前', '分担', '边', '展开', '收尾', '事实', '算式', '消歧', '关系', '标注')
GIST_PAT = r'\*\*主旨(?:\*\*\s*[：:]?|[：:]\*\*)|主旨[：:]'
TITLE_PAT = r'(?:\*\*)?〔标题〕(?:\*\*)?'
LIVING_RES = ([('title', re.compile(r'^(?:%s)\s*' % TITLE_PAT)), ('gist', re.compile(r'^(?:%s)\s*' % GIST_PAT)),
               ('para', re.compile(r'^%s\s*' % label_pat(PARA_PAT)))]
              + [(lab, re.compile(r'^%s\s*' % field_label(lab))) for lab in LIVING_LABELS])
LIVING_FIELD_RE = re.compile(FIELD_RE + r'(?:%s|%s|把握[：:]|%s|%s)' % (
    TITLE_PAT, GIST_PAT, label_pat(PARA_PAT), '|'.join(field_label(x) for x in LIVING_LABELS)))
BULLET_ONLY_RE = re.compile(r'^\s*[-*+]\s+')
H1_RE = re.compile(r'^#\s')
Q_RE = re.compile(r'^(?:\*\*)?(Q[0-9]+)(?:\*\*)?\s*｜')
CARD_LABELS = (('research_q', '研究问题'), ('reader', '目标读者'), ('scope_out', r'范围排除(?:（[^（）]*）|\([^()]*\))?'))
Q_CELLS = (('threshold', r'(?:必带判据\s*[：:]\s*)?门槛', False), ('denominator', '分母', False),
           ('window', '窗口', False), ('misread', '删去后[^：:｜]*', True), ('unresolved', '若?材料未决', True))
EDGE_COLS = (('id', r'ID'), ('ends', '端点'), ('relation', '关系'), ('evidence', '凭据|连接句'), ('status', '状态'),
             ('bounds', '禁写|边界'), ('rev', '版本|判于'))
EDGE_STATUS = ('已定', '待据', '不成立')
EDGE_ID_RE = re.compile(r'(?<![A-Za-z0-9_])X[0-9]+(?![A-Za-z0-9_])')
ARROW = r'(?:→|->|⟶)'
RENUM_RE = re.compile(r'^\s*[-*+]\s+(?:\*\*)?(' + ID_CORE + ')' + ID_END + r'\s*' + ARROW + r'\s*(' + ID_CORE + ')'
                      + ID_END + r'(.*)$')
SHARE_ITEM_RE = re.compile(r'^(.*?)\s*' + ARROW + r'\s*(' + ID_CORE + ')' + ID_END + r'\s*(?:[·・•‧]\s*(.*))?$', re.S)
SHARE_CELLS = (('cover_test', '遮住[^：:｜]*'), ('uncovered', '无人担'), ('duplicate', '重复担'),
               ('insufficient', '子项合计仍证不出'))
REV_MARK_RE = re.compile(r'〔判于\s*([^〔〕]*?)\s*〕')
QUOTES = '“”"‘’「」『』'
QUOTE_RE = re.compile(r'[“"「『]([^”"」』]*)[”"」』]')
FACT_MODE_RE = re.compile(r'^(?:\*\*)?(写全|回指|留表)(?:\*\*)?\s*[：:]?\s*')
FACT_ID_RE = re.compile(r'[A-Za-z]+[0-9][A-Za-z0-9_\-]*')
FACT_ID_TAIL_RE = re.compile(r'[A-Za-z]+[0-9][A-Za-z0-9_\-]*$')
ANCHOR_LINES_RE = re.compile(r'L([0-9]+)(?:\s*[–—\-~～至]+\s*L?([0-9]+))?\s*$')
OP_SPLIT_RE = re.compile(r'(＋|\+|－|−|×|\*|÷|/|\s-\s)')
NUM_RE = re.compile(r'[-−+]?[0-9][0-9,，]*(?:\.[0-9]+)?')
DERIV_CELLS = (('direction', '方向'), ('assume', '假设'), ('check', '复算闭合值|复算值|复算'), ('den', '分母'),
               ('sign', '签认'), ('basis', '口径|对齐说明|对齐'))
OPEN_BR, CLOSE_BR = '（(〔<【', '）)〕>】'


def split_cells(text):
    return [c.strip() for c in text.split('｜')]


def cell_value(cell, pat, colon=True):
    """The text after a cell label (regex pat, optional bold, colon required unless colon=False), or None."""
    m = re.match(r'(?:\*\*)?(?:%s)(?:\*\*)?\s*%s(?:\*\*)?\s*' % (pat, '[：:]' if colon else '[：:]?'), cell)
    return cell[m.end():].strip() if m else None


def split_top(text, seps='、，,；;'):
    """Split text at seps outside （）()〔〕<>【】 brackets."""
    out, cur, depth = [], '', 0
    for ch in text:
        if ch in OPEN_BR:
            depth += 1
        elif ch in CLOSE_BR and depth:
            depth -= 1
        elif ch in seps and not depth:
            out.append(cur)
            cur = ''
            continue
        cur += ch
    return [x.strip() for x in out + [cur] if x.strip()]


def placeholder(text):
    return (text or '').strip().startswith(('<', '＜'))


def id_key(nd):
    return tuple(int(x) for x in nd[1:].split('.'))


def top_entries(lines, first_line=1):
    """[(file line, text)] of a node block's top-level lines (the block's least indent, R11), heading skipped:
    bullet cut, continuation lines (deeper indent, not a field line) joined (join_cont)."""
    body = lines[1:]
    inds = [indent(l) for l in body if l.strip()]
    top = min(inds) if inds else 0
    out, k = [], 0
    while k < len(body):
        l = body[k]
        k += 1
        if not l.strip() or indent(l) != top:
            continue
        at = first_line + k
        parts = [BULLET_RE.sub('', l, count=1).strip()]
        while k < len(body) and body[k].strip() and not LIVING_FIELD_RE.match(body[k]) and indent(body[k]) > indent(l):
            parts.append(BULLET_RE.sub('', body[k], count=1).strip())
            k += 1
        out.append((at, join_cont([x for x in parts if x] or [''])))
    return out


def parse_gist(text):
    """'<判断>｜因：…｜限：…｜性质与把握：…' -> judgment, cause, limit, modality, raw (all None without a 主旨 line)."""
    out = dict(judgment=None, cause=None, limit=None, modality=None, raw=text)
    if text is None:
        return out
    rest = []
    for c in split_cells(text):
        for key, pat in (('cause', '因'), ('limit', '限'), ('modality', '性质与把握|把握')):
            v = cell_value(c, pat)
            if v is not None:
                out[key] = v if out[key] is None else out[key]
                break
        else:
            rest.append(c)
    out['judgment'] = rest[0] if rest else None
    return out


def parse_share(text):
    """'“<环>”→N1·主干｜…｜遮住…：…｜无人担：…｜重复担：…｜子项合计仍证不出：…〔判于r<k>〕' or None."""
    if text is None:
        return None
    out = dict(items=[], cover_test=None, uncovered=None, duplicate=None, insufficient=None, rev=None, raw=text)
    m = REV_MARK_RE.search(text)
    if m:
        out['rev'] = m.group(1) or None
    for c in split_cells(REV_MARK_RE.sub('', text)):
        for key, pat in SHARE_CELLS:
            v = cell_value(c, pat)
            if v is not None:
                out[key] = v
                break
        else:
            m = SHARE_ITEM_RE.match(c)
            if m:
                el = m.group(1).strip().strip(QUOTES).strip()
                out['items'].append(dict(element=el or None, child=m.group(2), role=(m.group(3) or '').strip() or None))
    return out


def parse_anchor(tok):
    """{'anchor', 'id', 'doc', 'lines'} of 'E012@档名:L85', '@档名:L120–L130', '档名@L120' or 'E012' (id only: doc
    and lines None); lines [a, b] (one line: [a, a]); a placeholder <…> is kept raw with the parts None."""
    tok = tok.strip()
    out = dict(anchor=tok, id=None, doc=None, lines=None)
    if not tok or placeholder(tok):
        return out
    pre, at, post = tok.partition('@')
    if not at:
        if FACT_ID_RE.fullmatch(tok):
            out['id'] = tok
        return out
    m = ANCHOR_LINES_RE.search(post)
    if m:
        a = int(m.group(1))
        out['lines'] = [a, int(m.group(2)) if m.group(2) else a]
        post = post[:m.start()]
    doc = post.rstrip(':：').strip() or None
    if pre and FACT_ID_RE.fullmatch(pre):
        out['id'] = pre
    elif pre:
        doc = doc or pre
    out['doc'] = doc
    return out


def parse_facts(text):
    """'写全 <锚点>｜回指 <锚点（写全处N号）>｜留表 <锚点（入表m…）>' -> [{mode, anchor, id, doc, lines, note, raw}].
    A cell without a mode word keeps the previous cell's mode (None at the start); '无…' -> []."""
    out, mode = [], None
    if text is None or text.strip().startswith('无'):
        return out
    for cell in split_cells(text):
        m = FACT_MODE_RE.match(cell)
        if m:
            mode, cell = m.group(1), cell[m.end():]
        for piece in split_top(cell):
            if placeholder(piece):
                anc, note = piece, ''
            else:
                mm = re.match(r'([^\s（(]*)\s*(.*)$', piece, re.S)
                anc, note = mm.group(1), mm.group(2).strip()
                if note[:1] in '（(' and note[-1:] in '）)':
                    note = note[1:-1].strip()
            d = parse_anchor(anc)
            out.append(dict(mode=mode, anchor=d['anchor'], id=d['id'], doc=d['doc'], lines=d['lines'],
                            note=note or None, raw=piece))
    return out


def parse_operand(t):
    """{'name', 'value', 'anchor'} of one operand: '应收账款12.0亿元@甲档:L40' -> 应收账款, 12.0亿元, @甲档:L40
    (the last number and what follows it is the value; an id glued before '@' belongs to the anchor)."""
    t = t.strip().strip('（）() ')
    anchor = None
    i = t.find('@')
    if i >= 0:
        m = FACT_ID_TAIL_RE.search(t[:i])
        s = m.start() if m else i
        anchor = t[s:].strip().strip('（）()') or None
        t = t[:s].rstrip(' （(')
    nums = list(NUM_RE.finditer(t))
    if nums:
        n = nums[-1]
        name, value = t[:n.start()].strip().rstrip('：:').strip(), t[n.start():].strip()
    else:
        name, value = t.strip(), None
    return dict(name=name or None, value=value or None, anchor=anchor)


def operands(body):
    """[(operator before it or None, operand dict)] of an expression; a '/' whose right side is a short unit
    (no digit, no '@', at most 2 characters: 元/吨) stays inside the operand."""
    parts = OP_SPLIT_RE.split(body)
    terms, ops = [parts[0]], [None]
    for k in range(1, len(parts), 2):
        op, nxt = parts[k].strip() or '-', parts[k + 1]
        bare = nxt.strip().strip('（）() ')
        if op == '/' and terms and not re.search(r'[0-9@]', bare) and 0 < len(bare) <= 2:
            terms[-1] += '/' + nxt
            continue
        terms.append(nxt)
        ops.append(op)
    return [(op, parse_operand(t)) for op, t in zip(ops, terms) if t.strip().strip('（）() ')]


PENDING_WORD = re.compile(r'(?i)(?:待|未)(?:签|核|复|确|定|补|填|审|认)|无签|缺签|拟|预计|前(?:签|核|复)|(?:签|核|复核|复算)中'
                          r'|pending|tbd|todo')
PENDING_PART = re.compile(r'(?:^|[·・•/／|｜,，、;；:：\s（(\-—])\s*(?:待|未)')  # a part opening 待／未 (not 无: 无误 stays)
SIGN_DATE = re.compile(r'(?<![A-Za-z0-9.．表L])(?:\d{4}\s*[-/.年]\s*\d{1,2}\s*[-/.月]\s*\d{1,2}日?|\d{1,2}\s*月\s*\d{1,2}\s*日'
                       r'|\d{1,2}-\d{1,2})(?![\d.])')


def signed_cell(v):
    """A 签认 cell counts as signed only with positive evidence: the template's <席或脚本·日期> filled, that is a date
    (2026-11-20, 11-20, 2026年11月20日; never python3.11, 表3.2, L12-15), no pending word (待签, 未签, 待核, 拟于…, 预计…,
    …前复核, 复核中, pending) and no part opening 待／未 (核对席·待·2026-11-25), W4b; <…> placeholders and a cell
    ending in '>' are unsigned."""
    v = (v or '').strip().strip('*').strip()
    return (bool(v) and not placeholder(v) and not v.endswith(('>', '＞')) and not v.startswith(('待', '未', '无'))
            and not PENDING_WORD.search(v) and not PENDING_PART.search(v) and bool(SIGN_DATE.search(v)))


def parse_derivation(text, line):
    """'结果名＝expr｜方向：…｜<对齐说明>｜假设：…｜复算闭合值：v｜签认：…' -> the contract's derivation dict."""
    d = dict(metric=None, expr=None, operands=[], denominator=None, basis=None, direction=None, assume=None,
             value=None, signed=False, signer=None, raw=text, line=line)
    cells = split_cells(text)
    m = re.match(r'^(.*?)[＝=](.*)$', cells[0], re.S)
    if m:
        d['metric'], d['expr'] = m.group(1).strip() or None, m.group(2).strip()
    else:
        d['expr'] = cells[0]
    got, loose = {}, []
    for c in cells[1:]:
        if not c:
            continue
        for key, pat in DERIV_CELLS:
            v = cell_value(c, pat)
            if v is not None:
                got.setdefault(key, v)
                break
        else:
            loose.append(c)
    d['direction'], d['assume'] = got.get('direction'), got.get('assume')
    d['basis'] = got.get('basis') or ('｜'.join(loose) if loose else None)
    sides = re.split(r'[＝=]', d['expr'] or '')
    d['operands'] = [o for _, o in operands(sides[0])]
    d['value'] = got.get('check') or (sides[-1].strip() or None if len(sides) > 1 else None)
    if got.get('den'):
        d['denominator'] = got['den']
    else:
        after = [o for op, o in operands(sides[0]) if op in ('÷', '/')]
        if after:
            d['denominator'] = after[0]['name'] or after[0]['value']
    if 'sign' in got:
        d['signer'] = got['sign'] or None
        d['signed'] = signed_cell(got['sign']) and not placeholder(text)     # a whole-row placeholder never signs
    return d


def parse_disambig(text):
    """'类名｜锚点｜“原件字面子串”→固定写法｜禁写：…' or '类名｜锚点｜反查：“检索词”@全文0次（范围）→固定写法｜禁写：…';
    '无（六类已查）' -> none True."""
    d = dict(cls=None, anchor=None, quote=None, reverse=None, fixed=None, banned=None, none=False, raw=text)
    t = (text or '').strip()
    if not t or t.startswith('无'):
        d['none'] = True
        return d
    cells = split_cells(t)
    d['cls'] = cells[0] or None
    for c in cells[1:]:
        if not c:
            continue
        v = cell_value(c, '禁写')
        if v is not None:
            d['banned'] = v
            continue
        v = cell_value(c, '固定写法')
        if v is not None:
            d['fixed'] = v
            continue
        rev = cell_value(c, '反查')
        q = QUOTE_RE.search(c)
        if rev is None and q is None:
            d['anchor'] = d['anchor'] or c
            continue
        body, arrow, fixed = (rev if rev is not None else c).partition('→')
        if arrow:
            d['fixed'] = cell_value(fixed.strip(), '固定写法') or fixed.strip() or None
        if rev is not None:
            d['reverse'] = body.strip() or None
        else:
            d['quote'] = q.group(1)
    return d


def parse_para(k, text):
    """'段k：<主判断>｜接前：…｜事实：<锚点…>' -> {k, claim, follows, facts, no_split, raw}; '段：不拆（…）' -> no_split."""
    d = dict(k=k, claim=None, follows=None, facts=[], no_split=False, raw=text)
    t = text.strip()
    if k is None and t.startswith('不拆'):
        d['no_split'] = True
        return d
    rest = []
    for c in split_cells(t):
        v = cell_value(c, '接前')
        if v is not None:
            d['follows'] = v
            continue
        v = cell_value(c, '事实')
        if v is not None:
            if not v.startswith('无'):
                d['facts'] += [FACT_MODE_RE.sub('', p, count=1).strip() for p in split_top(v)]
            continue
        rest.append(c)
    d['claim'] = rest[0] if rest else None
    return d


def living_fields(block_lines, first_line=1):
    """The living-outline fields of one node block (its lines, heading first): gist, task, order, follows, edges,
    share, expand, close, title, facts, derivations, disambig, paras, legacy {关系, 标注}.  Line numbers count from
    first_line (the heading's; 1 when the block is read alone).  收尾 is read as close_entries/close_target read
    it; 关系 as relation_entries (any indent); every other field from the top-level lines."""
    got = {}
    for at, text in top_entries(block_lines, first_line):
        for name, rx in LIVING_RES:
            m = rx.match(text)
            if m:
                k = None
                if name == 'para':
                    num = next((g for g in m.groups() if g), '')
                    k = int(num) if num else None
                got.setdefault(name, []).append((at, text[m.end():].strip(), k))
                break

    def first(name):
        return got[name][0][1] if name in got else None

    def every(name):
        return got.get(name, [])

    title = first('title')
    edges = []
    for _, t, _ in every('边'):
        if not placeholder(t):
            edges += [x for x in EDGE_ID_RE.findall(t) if x not in edges]
    ents = close_entries(block_lines)
    return dict(
        gist=parse_gist(first('gist')), task=first('任务'), order=first('顺序'), follows=first('接前'),
        edges=edges, share=parse_share(first('分担')), expand=first('展开'),
        close=dict(target=close_target(ents[0]), text=ents[0]) if ents else None,
        title=title.strip('*').strip() if title is not None else None,
        facts=[f for _, t, _ in every('事实') for f in parse_facts(t)],
        derivations=[parse_derivation(t, at) for at, t, _ in every('算式') if not t.startswith('无')],
        disambig=[parse_disambig(t) for _, t, _ in every('消歧')],
        paras=[parse_para(k, t) for _, t, k in every('para')],
        legacy={'关系': [t for _, t in relation_entries(block_lines[1:])], '标注': [t for _, t, _ in every('标注')]})


def outside_mask(lines):
    """[True when the line sits outside every node block] (a block runs from its heading to the next node heading or
    a non-node '#'/'##' heading, as node_blocks reads it)."""
    mask, cur = [], False
    for l in lines:
        if NODE_RE.match(l):
            cur = True
            mask.append(False)
        elif cur and TREE_END_RE.match(l):
            cur = False
            mask.append(True)
        else:
            mask.append(not cur)
    return mask


def head_entries(lines, mask):
    """[(file line, text)] of the bullets outside the node blocks: bullet cut, continuation lines (deeper indent,
    not a bullet, a table row or a heading) joined."""
    out, k = [], 0
    while k < len(lines):
        l = lines[k]
        k += 1
        if not mask[k - 1] or not BULLET_ONLY_RE.match(l):
            continue
        at, parts = k, [BULLET_RE.sub('', l, count=1).strip()]
        while (k < len(lines) and mask[k] and lines[k].strip() and not BULLET_ONLY_RE.match(lines[k])
               and indent(lines[k]) > indent(l) and not lines[k].lstrip().startswith(('|', '#'))):
            parts.append(lines[k].strip())
            k += 1
        out.append((at, join_cont([x for x in parts if x] or [''])))
    return out


def parse_question(text, line):
    q = dict(id=Q_RE.match(text).group(1), judgment=None, threshold=None, denominator=None, window=None,
             misread=None, unresolved=None, raw=text, line=line)
    rest = []
    for c in split_cells(text)[1:]:
        for key, pat, colon in Q_CELLS:
            v = cell_value(c, pat, colon)
            if v is not None:
                q[key] = v if q[key] is None else q[key]
                break
        else:
            rest.append(c)
    q['judgment'] = rest[0] if rest else None
    return q


def parse_edge_table(lines, mask):
    """The rows of the first table outside the node blocks whose header has an ID column and a 端点 column."""
    for i, ln in enumerate(lines):
        if not mask[i] or not ln.strip().startswith('|') or i + 1 >= len(lines) or not SEP_RE.match(lines[i + 1]):
            continue
        head = cells(ln)
        if not (any('ID' in c.upper() for c in head) and any('端点' in c for c in head)):
            continue
        col = {}
        for role, pat in EDGE_COLS:
            col[role] = next((k for k, c in enumerate(head) if k not in col.values()
                              and re.search(pat, c.upper() if role == 'id' else c)), None)
        out = []
        for j in range(i + 2, len(lines)):
            if not lines[j].strip().startswith('|'):
                break
            c = cells(lines[j])

            def get(role):
                k = col[role]
                return c[k] if k is not None and k < len(c) else None
            ends = sorted(ID_TOKEN_RE.findall(get('ends') or ''), key=id_key)
            sr = get('status')
            s = (sr or '').strip().strip('*').strip()
            out.append(dict(id=get('id'), ends=ends, key='—'.join(ends), relation=get('relation'),
                            evidence=get('evidence'), status=next((w for w in EDGE_STATUS if s.startswith(w)), None),
                            status_raw=sr, bounds=get('bounds'), rev=get('rev'), raw=lines[j], line=j + 1))
        return out
    return []


def edge_conflicts(edges):
    """[{key, ids, statuses}] of every sorted end pair on two or more rows (one proposition is ruled once, gate 3)."""
    groups = {}
    for e in edges:
        if len(e['ends']) >= 2:
            groups.setdefault(e['key'], []).append(e)
    return [dict(key=k, ids=[e['id'] for e in g], statuses=[e['status'] for e in g])
            for k, g in groups.items() if len(g) > 1]


def tree_head(text):
    """The tree head of a living outline: {tree_rev, material_rev, card, edges, edge_conflicts, renumber}
    (revisions from the H1 '# …｜树r3｜材料r2｜截至…'; card, edge table and renumber list from the lines outside
    the node blocks)."""
    lines = text.split('\n')
    mask = outside_mask(lines)
    h1 = next((l for l, m in zip(lines, mask) if m and H1_RE.match(l)), '')
    revs = [re.search(p + r'\s*(r[0-9]+)', h1) for p in ('树', '材料')]
    card = dict(research_q=None, reader=None, scope_out=None, questions=[])
    for at, t in head_entries(lines, mask):
        if Q_RE.match(t):
            card['questions'].append(parse_question(t, at))
            continue
        for key, pat in CARD_LABELS:
            m = re.match(r'^%s\s*' % label_pat(pat), t)
            if m and card[key] is None:
                card[key] = t[m.end():].strip()
                break
    renumber = []
    for l, m in zip(lines, mask):
        r = RENUM_RE.match(l) if m else None
        if r:
            rv = re.search(r'树\s*(r[^｜|，,；;\s）)]*)', r.group(3)) or re.search(r'(?<![A-Za-z])(r[0-9]+)', r.group(3))
            renumber.append(dict(old=r.group(1), new=r.group(2), rev=rv.group(1) if rv else None,
                                 raw=BULLET_RE.sub('', l, count=1).strip()))
    edges = parse_edge_table(lines, mask)
    return dict(tree_rev=revs[0].group(1) if revs[0] else None, material_rev=revs[1].group(1) if revs[1] else None,
                card=card, edges=edges, edge_conflicts=edge_conflicts(edges), renumber=renumber)


def fields_json(text, ids=None, outline=None):
    """The fields contract as a dict: version, outline, the tree head, nodes {id: fields} in document order (only ids
    when given; an unknown id raises SliceError).  The first block of a duplicate id counts (as index does)."""
    blocks = node_blocks_at(text)
    idx = {}
    for nd, head, lines, at in blocks:
        idx.setdefault(nd, (head, lines, at))
    want = list(dict.fromkeys(ids or []))
    require(idx, want)
    kids = children([(nd, head, lines) for nd, head, lines, _ in blocks])
    nodes = {}
    for nd, (head, lines, at) in idx.items():
        if want and nd not in want:
            continue
        nodes[nd] = dict(heading=head, line=at, parent=None if nd == 'N0' else ancestors(nd)[-1],
                         children=kids.get(nd, []), **living_fields(lines, at))
    out = dict(version=VERSION, outline=outline)
    out.update(tree_head(text))
    out['nodes'] = nodes
    return out


def cmd_fields(a, out):
    out.write(json.dumps(fields_json(read(a.outline), a.ids, a.outline), ensure_ascii=False, indent=1) + '\n')
    return 0


# ------------------------------------------------------------------ pre-prose gates (check-0to1, 1.2.0 W1-O2)
# The pre-prose gates 1-5 (FICCOutline.md §9, FICCStructure.md §7) in machine form, read off fields_json (no second parse).  One finding per defect,
# {code, sev, where, why, line}: sev hard (exit 2), warn or skip.  Codes: (a) Z-SWAP, Z-SWAP?; (b) Z-DENOM, Z-Q;
# (c) Z-SHARE; (d) Z-EDGE, Z-EDGE?; (e) Z-FACT, Z-QUOTE, Z-QUOTE-SKIP; (f) Z-PARA, Z-SIGN.  The gates read neither
# 收尾 nor 关系, so the legacy continuation reader (ANY_FIELD_RE) does not touch them.
METRIC_UNITS = sorted((                         # the one list of metric units (gate a, swap test; FICCOutline.md O20)
    '%', '‰', 'bp', 'bps', 'BP', 'x', 'X', '倍', '亿', '万', '千', '百万', '千万', '兆', 'GW', 'GWh', 'MW', 'MWh',
    'kW', 'kWh', 'TWh', '吨', '元', '美元', '港元', '欧元', '日元', '英镑', '人民币', '年期', '个百分点', '百分点',
    '个基点', '基点', '个月', '天', '家', '笔'), key=len, reverse=True)
UNIT_ALT = '|'.join(re.escape(u) + ('(?![A-Za-z])' if u[-1].isascii() and u[-1].isalpha() else '')
                    for u in METRIC_UNITS)
UNIT_RE = re.compile(r'\s*(?:%s)' % UNIT_ALT)
CURRENCY_RE = re.compile(r'(?:US\$|HK\$|A\$|S\$|\$|¥|€|£|USD|RMB|CNY|HKD|EUR|JPY|GBP)\s*$')
CCY_CODES = r'(?:USD|RMB|CNY|HKD|EUR|JPY|GBP|US|HK)'
IDENT_RES = [re.compile(p) for p in (            # identifiers pass the swap test (masked in this order)
    r'(?<![0-9])(?:19|20)[0-9]{2}\s*(?:Q[1-4]|H[12])(?![0-9A-Za-z])',                     # 2026Q3, 2025H1
    r'(?<![0-9A-Za-z])[1-4][QH](?:19|20)?[0-9]{2}(?![0-9])',                               # 3Q24, 1H25
    r'(?<![A-Za-z0-9$])(?!%s[0-9])[A-Za-z]{1,4}[0-9]+(?:\.[0-9]+)*(?![0-9])' % CCY_CODES,  # N1.2 Q1 X01 E012 FY25
    r'(?<![0-9])(?:19|20)[0-9]{2}(?:[-/.][0-9]{1,2}(?:[-/.][0-9]{1,2})?(?![0-9])|年[0-9]{1,2}月(?:[0-9]{1,2}日)?)',
    r'(?<![0-9.])(?:19|20)[0-9]{2}(?:\s*[–—\-~～至到]\s*(?:19|20)?[0-9]{2})?(?![0-9])(?!\.[0-9])(?!\s*(?:%s))'
    % UNIT_ALT,                                                                            # years, year ranges
    r'第\s*[0-9]+\s*(?:期|档|批|次|号|条|款|项|章|节|部分|轮|版|季度|季|届|名|位|年)',      # 第2期, 第3条
    r'(?<![0-9.])[0-9]{1,2}\s*(?:月份?(?:\s*[0-9]{1,2}\s*日)?|季度|季报)',                 # 12月, 3季度
    r'(?<![0-9.])[0-9]+\s*号')]                                                            # 7号条款
NUM_TOKEN_RE = re.compile(r'[0-9]+(?:[.,][0-9]+)*')
CJK_METRIC_RE = re.compile(r'[一二两三四五六七八九十百千半]+(?:倍|个百分点|个基点)')
RATIO_RE = re.compile(r'[%‰/]|(?<=[0-9])\s*[xX](?![A-Za-z])|倍|率|比|bps?|BP|基点|百分点')   # gate b
BARE_CELLS = ('会', '是', '无')
NIL_RE = re.compile(r'^无(?:\s*[（(〔【][^）)〕】]*[）)〕】])?\s*[。.]?$')                         # gate c: reads 无
CAUSAL_WORDS = ('因果', '导致', '依赖', '偿付', '因为', '因此', '所以', '致使', '引起', '造成', '由于', '驱动', '传导',
                '推断')                                                                     # gate d
FINDING_KEYS = ('code', 'sev', 'where', 'why', 'line')


def swap_tokens(text):
    """[(token, 'metric' | 'bare')] in text order: the digits of a 主旨 slot under the swap test (FICCOutline.md O20).
    Identifiers pass (node/rule/fact/edge/Q ids, years and year ranges, report quarters and halves, dates, months,
    第N期-style series, N号); a number with a unit from METRIC_UNITS, or after a currency sign or code, is a metric;
    any other number is bare (the swap test is the reader's).  Read on the NFKC form (full-width digits, ％)."""
    s = unicodedata.normalize('NFKC', text or '')
    for rx in IDENT_RES:
        s = rx.sub(lambda m: '\x00' * len(m.group(0)), s)
    out = [(m.start(), m.group(0), 'metric') for m in CJK_METRIC_RE.finditer(s)]
    for m in NUM_TOKEN_RE.finditer(s):
        before = s[:m.start()]
        cur = CURRENCY_RE.search(before)
        if not cur and before[-1:].isascii() and before[-1:].isalpha():
            continue                                            # glued to a Latin word: part of a name
        u = UNIT_RE.match(s, m.end())
        if cur or u:
            out.append((cur.start() if cur else m.start(),
                        (cur.group(0) if cur else '') + m.group(0) + (u.group(0).strip() if u else ''), 'metric'))
        else:
            out.append((m.start(), m.group(0), 'bare'))
    return [(t, k) for _, t, k in sorted(out)]


def blank_cell(v):
    """True for an empty cell, a placeholder <…> or a bare 会/是/无 (gate b)."""
    t = (v or '').strip().strip('*').strip().rstrip('。.；;，,').strip()
    return not t or placeholder(t) or t in BARE_CELLS


# W4a (S77): a causal word under a prohibition in its own clause names no causal relation ("只是并列，不写成因果或递进",
# "不写“因为…，所以…”"): the clause runs to the next ，,；;。：:｜|—— outside quotes, and a quote opened after the marker
# stays inside that clause
NEG_CAUSAL = ('不写成', '不写', '不作', '非因果', '不是因果', '禁写', '严禁', '不得写成', '不得', '不构成因果', '不构成',
              '不能写成', '勿写', '不当作', '不视为')
_CLAUSE_CUT = set('，,；;。：:｜|')
_Q_OPEN, _Q_CLOSE = '“「『', '”」』'


def _clauses(text):
    """Clauses of TEXT, cut at ，,；;。：:｜|—— outside “…” quotes."""
    out, cur, depth, i = [], [], 0, 0
    while i < len(text):
        ch = text[i]
        if ch in _Q_OPEN:
            depth += 1
        elif ch in _Q_CLOSE and depth:
            depth -= 1
        if not depth and (ch in _CLAUSE_CUT or text.startswith('——', i)):
            out.append(''.join(cur))
            cur = []
            i += 2 if text.startswith('——', i) else 1
            continue
        cur.append(ch)
        i += 1
    out.append(''.join(cur))
    return out


def causal_word(text):
    """The first causal word of TEXT that no prohibition marker (NEG_CAUSAL) precedes in its own clause, else None."""
    for cl in _clauses(text or ''):
        for w in CAUSAL_WORDS:
            k = cl.find(w)
            while k >= 0:
                if not any(m in cl[:k + len(w)] for m in NEG_CAUSAL):  # 非因果 / 不是因果 hold the word itself
                    return w
                k = cl.find(w, k + 1)
    return None


def ws_norm(s):
    """Whitespace-normalised text for the quote check: runs collapsed to one space, a space next to a non-ASCII
    character dropped (a line break inside a CJK sentence)."""
    s = re.sub(r'\s+', ' ', s or '').strip()
    return re.sub(r'(?<=[^\x00-\x7f]) | (?=[^\x00-\x7f])', '', s)


def quoted(items):
    return '、'.join('“%s”' % x for x in items)


def gate_findings(text, sources=None):
    """The pre-prose gate findings of a living outline (FICCOutline.md §9 and FICCStructure.md §7; W1-O2) in gate order a-f, document order
    within a gate.  sources: {document name: text} for the 消歧 quote check, or None (reported as skipped)."""
    d = fields_json(text)
    nodes, card, edges = d['nodes'], d['card'], d['edges']
    out = []

    def add(code, sev, where, why, line=None):
        out.append(dict(code=code, sev=sev, where=where, why=why, line=line))

    # (a) Z-SWAP: no metric in a 主旨 判断 or 因 slot (N0 included); a bare number is a warning
    for nd, f in nodes.items():
        for slot, key in (('判断', 'judgment'), ('因', 'cause')):
            v = f['gist'][key]
            if not v or placeholder(v):
                continue
            toks = swap_tokens(v)
            met, bare = [t for t, k in toks if k == 'metric'], [t for t, k in toks if k == 'bare']
            if met:
                add('Z-SWAP', 'hard', nd, '主旨 %s carries the metric %s: a number with a unit is barred from 判断 and 因 '
                    '(swap test); move it to 限, 事实 or 算式' % (slot, quoted(met)), f['line'])
            if bare:
                add('Z-SWAP?', 'warn', nd, '主旨 %s carries the bare number %s: swap test (names another object = '
                    'identifier, same object resized = metric, barred)' % (slot, quoted(bare)), f['line'])

    # (b) Z-DENOM / Z-Q: the question card
    qs = card['questions']
    if not qs:
        add('Z-Q', 'hard', '-', 'no 开工问 Q row in the question card (one to four, FICCOutline.md O10)')
    elif len(qs) > 4:
        add('Z-Q', 'hard', qs[4]['id'], '%d 开工问 rows: at most 4' % len(qs), qs[4]['line'])
    for q in qs:
        th = q['threshold']
        if th and not placeholder(th) and RATIO_RE.search(unicodedata.normalize('NFKC', th)) \
                and blank_cell(q['denominator']):
            add('Z-DENOM', 'hard', q['id'], 'ratio 门槛 “%s” with an empty or placeholder 分母 (name, base, @anchor; '
                'say whether new issuance enters it)' % th, q['line'])
        miss = [lab for lab, key in (('门槛', 'threshold'), ('窗口', 'window'), ('删去后会答错什么', 'misread'))
                if blank_cell(q[key])]
        if miss:
            add('Z-Q', 'hard', q['id'], '%s empty, a placeholder or a bare 会/是/无' % '、'.join(miss), q['line'])

    # (c) Z-SHARE: every node with children has a 分担 row that clears the three cells and maps its children
    for nd, f in nodes.items():
        kids, s = f['children'], f['share']
        if not kids:
            continue
        if s is None:
            add('Z-SHARE', 'hard', nd, 'node with children %s has no 分担 row' % '、'.join(kids), f['line'])
            continue
        bad = []
        for lab, key in (('无人担', 'uncovered'), ('重复担', 'duplicate'), ('子项合计仍证不出', 'insufficient')):
            v = s[key]
            if v is None:
                bad.append('%s missing' % lab)
            elif not NIL_RE.match(v.strip()):
                bad.append('%s reads “%s”' % (lab, v))
        if bad:
            add('Z-SHARE', 'hard', nd, '分担 must read 无 in 无人担, 重复担 and 子项合计仍证不出 (else add the missing node '
                'or narrow the parent 主旨): ' + '; '.join(bad), f['line'])
        named = []
        for it in s['items']:
            if it['child'] not in kids:
                add('Z-SHARE', 'hard', nd, '分担 item “%s”→%s names no child of %s (children: %s)'
                    % (it['element'] or '', it['child'], nd, '、'.join(kids)), f['line'])
                continue
            if not it['element'] or placeholder(it['element']):
                add('Z-SHARE', 'hard', nd, '分担 item →%s has an empty or placeholder element' % it['child'], f['line'])
            named.append(it['child'])
        lost = [k for k in kids if k not in named]
        if lost:
            add('Z-SHARE', 'hard', nd, 'children %s carry no 分担 item' % '、'.join(lost), f['line'])

    # (d) Z-EDGE: the edge table (one sorted key, one ruling) and causal 接前
    for e in edges:
        where, ends = e['id'] or 'row', e['ends']
        if len(set(ends)) != 2:
            add('Z-EDGE', 'hard', where, '端点 must name two different node ids (read: %s)'
                % ('、'.join(ends) or 'none'), e['line'])
        else:
            unk = [x for x in ends if x not in nodes]
            if unk:
                add('Z-EDGE', 'hard', where, 'endpoint %s has no node block' % '、'.join(unk), e['line'])
        ev = (e['evidence'] or '').strip()
        if e['status'] is None:
            add('Z-EDGE', 'hard', where, 'no status: 状态 reads “%s”, needs 已定／待据／不成立' % (e['status_raw'] or ''),
                e['line'])
        elif e['status'] == '已定' and (not ev or placeholder(ev)):
            add('Z-EDGE', 'hard', where, '已定 with an empty or placeholder 连接句凭据', e['line'])
        elif e['status'] == '已定' and causal_word(e['relation']) and '@' not in ev:
            add('Z-EDGE', 'hard', where, '已定 causal/dependency edge (%s) whose 凭据 has no @ anchor: quote one source '
                'sentence linking both ends, or seal it 待据' % causal_word(e['relation']), e['line'])
    for c in d['edge_conflicts']:
        rows = [e for e in edges if e['key'] == c['key']]
        pairs = '、'.join('%s %s' % (i, s or '(no status)') for i, s in zip(c['ids'], c['statuses']))
        if len(set(s for s in c['statuses'] if s)) > 1:
            add('Z-EDGE', 'hard', c['key'], '%s on one sorted key with conflicting status: refused; rule the pair once '
                'side by side, sealed 待据 until one linking sentence' % pairs, rows[1]['line'])
        else:
            add('Z-EDGE?', 'warn', c['key'], '%s on one sorted key: review side by side (merge, keep distinct relation '
                'classes, or rule)' % pairs, rows[1]['line'])
    for nd, f in nodes.items():
        follows = [(nd, f['follows'])] + [('%s 段%s' % (nd, '' if p['k'] is None else p['k']), p['follows'])
                                          for p in f['paras']]
        for where, t in follows:
            if t and not placeholder(t) and causal_word(t) and '@' not in t:
                add('Z-EDGE', 'hard', where, '接前 names a causal relation (%s) with no @ anchor: paste the linking '
                    'sentence (凭：@原件锚点) or seal it 待据' % causal_word(t), f['line'])

    # (e) Z-FACT: one 写全 owner per fact anchor, every 回指 points at one; Z-QUOTE: 消歧 quotes verbatim in the source
    def fkey(x):
        return x['id'] or x['anchor']
    owners = {}
    for nd, f in nodes.items():
        for x in f['facts']:
            if x['mode'] == '写全' and x['anchor'] and not placeholder(x['anchor']):
                own = owners.setdefault(fkey(x), [])
                if nd not in own:
                    own.append(nd)
    for key, own in owners.items():
        if len(own) > 1:
            add('Z-FACT', 'hard', key, 'written in full (写全) in %s: one owner per fact anchor, the others 回指 it'
                % '、'.join(own), nodes[own[1]]['line'])
    for nd, f in nodes.items():
        for x in f['facts']:
            if x['mode'] != '回指' or not x['anchor'] or placeholder(x['anchor']):
                continue
            own, named = owners.get(fkey(x)), ID_TOKEN_RE.findall(x['note'] or '')
            if not own:
                add('Z-FACT', 'hard', nd, '回指 %s: the anchor is written in full (写全) in no node' % fkey(x), f['line'])
            elif named and named[0] not in own:
                add('Z-FACT', 'hard', nd, '回指 %s names 写全处%s, but %s writes it in full'
                    % (fkey(x), named[0], '、'.join(own)), f['line'])
    quotes = [(nd, f, m) for nd, f in nodes.items() for m in f['disambig']
              if m['quote'] and not m['none'] and not placeholder(m['raw'])]
    if sources is None:
        if quotes:
            add('Z-QUOTE-SKIP', 'skip', '-', '%d 消歧 quote(s) not checked against the sources (pass --sources '
                'NAME=PATH)' % len(quotes))
    else:
        doc_of = {}
        for f in nodes.values():
            for x in f['facts']:
                if x['id'] and x['doc']:
                    doc_of.setdefault(x['id'], x['doc'])
        for nd, f, m in quotes:
            a = parse_anchor(m['anchor'] or '')
            doc = a['doc'] or doc_of.get(a['id'])
            if not doc:
                add('Z-QUOTE', 'hard', nd, '消歧 quote “%s”: its anchor “%s” names no source document'
                    % (m['quote'], m['anchor'] or ''), f['line'])
            elif doc not in sources:
                add('Z-QUOTE', 'hard', nd, '消歧 quote “%s”: source %s not given in --sources' % (m['quote'], doc),
                    f['line'])
            elif ws_norm(m['quote']) not in ws_norm(sources[doc]):
                add('Z-QUOTE', 'hard', nd, '消歧 quote “%s” is not a verbatim substring of %s (whitespace-normalised)'
                    % (m['quote'], doc), f['line'])

    # (f) Z-PARA: a heavy node (>5 写全 facts, or any 算式) needs 段k rows; a 段 row cites <=5 facts; Z-SIGN warning
    for nd, f in nodes.items():
        full = [x for x in f['facts'] if x['mode'] == '写全']
        why = (['%d 写全 facts' % len(full)] if len(full) > 5 else []) + (
            ['%d 算式 row(s)' % len(f['derivations'])] if f['derivations'] else [])
        ks = [p for p in f['paras'] if p['k'] is not None]
        if why and not ks:
            waiver = any(p['no_split'] for p in f['paras'])
            add('Z-PARA', 'hard', nd, 'heavy node (%s) %s: list 段1…段k rows (<=5 facts each)'
                % ('、'.join(why), 'claims 段：不拆, which only a light node may' if waiver else 'has no 段k row'),
                f['line'])
        for p in ks:
            if len(p['facts']) > 5:
                add('Z-PARA', 'hard', '%s 段%d' % (nd, p['k']), '段 row cites %d facts (at most 5)' % len(p['facts']),
                    f['line'])
        for dv in f['derivations']:
            if not dv['signed']:
                add('Z-SIGN', 'warn', nd, '算式 %s is unsigned (签认: %s): a leaf may not use its numbers'
                    % (dv['metric'] or dv['expr'] or '', dv['signer'] or 'none'), dv['line'])
    return out


def parse_sources(items):
    """{name: text} of the --sources NAME=PATH entries (None when none given); a bad entry or file raises SliceError."""
    if items is None:
        return None
    out = {}
    for it in [x for group in items for x in group]:
        name, eq, path = it.partition('=')
        if not eq or not name.strip() or not path.strip():
            raise SliceError('bad --sources entry %r (NAME=PATH)' % it)
        out[name.strip()] = read(path.strip())
    return out


def emit_findings(found, out, as_json=False):
    """Findings on out, one line each ('CODE where: why (line N)') or as a JSON list; a count line on stderr.
    Returns 2 when any finding is hard, else 0."""
    if as_json:
        out.write(json.dumps(found, ensure_ascii=False, indent=1) + '\n')
    else:
        out.write(''.join('%s %s: %s%s\n' % (f['code'], f['where'], f['why'], '' if f['line'] is None
                                              else ' (line %d)' % f['line']) for f in found))
    n = dict((s, sum(1 for f in found if f['sev'] == s)) for s in ('hard', 'warn', 'skip'))
    print('check-0to1: %d hard, %d warnings, %d skipped' % (n['hard'], n['warn'], n['skip']), file=sys.stderr)
    return 2 if n['hard'] else 0


def cmd_check0(a, out):
    text, sources = read(a.outline), parse_sources(a.sources)
    return emit_findings(gate_findings(text, sources), out, a.json)


# ------------------------------------------------------------------ self-test
FIXTURE = """# 样例-提纲

## 头

- 决策问题：样例。

## 名字表

| 名字 | 指什么与口径 | 本篇写法 | 不许用的叫法 |
|---|---|---|---|
| 外部账户（第一次之后） | 经常账户与外储 | “看外部账户” | “外部位置”；“外部平衡”（原题除外） |
| 零售定价 | 定价安排 | 零售定价 | “油价传导” |
| 缓冲 | 财政余量 | 缓冲 | “护城河”、`安全垫` |
| 冷门词 | 全篇不出现 | 冷门词 | “无此词” |

## N0 根主旨

- 〔标题〕样例根标题
- **主旨**：根判断。
  把握：likely
- 任务：答决策问题。
- 顺序：树根。
- 关系：和N1，是呼应。
- 展开：N1、N2。

### N1 一、外部账户

- 〔标题〕一、外部账户
- **主旨**：落点看外部账户。
- 任务：立排序依据。
- 顺序：在N2之前。
- 关系：和N2，是前提。

#### N1.1 （一）零售定价

- 〔标题〕（一）零售定价
- **主旨**：形式看零售定价。
- 任务：分渠道。
- 展开：一段。

##### N1.1.1 1. 一例

- **主旨**：一例里的护城河说法要改。
- 任务：举一例。

### N2 二、缓冲

- 〔标题〕二、缓冲
- **主旨**：缓冲先到期。
- 任务：收束。
- 关系：和N1，是对照。

## 开放问题

- 不属于任何节点的一行。
"""

# 1.0.1 regression: ids glued to the heading text (1104 draft task, 81 of 91 nodes found).
GLUED = """# 粘连-提纲

## N0 根〔段群〕

- **主旨**：根。

## N1一、外部账户〔标题〕

- **主旨**：一。

### N1.0总起〔段群〕

- **主旨**：总起。

### N1.1 （一）零售〔标题〕

- **主旨**：一一。

### N1.9收束〔段群〕

- **主旨**：收束。

### N1.10尾声

- **主旨**：尾声。

## N2：二、缓冲

- **主旨**：二。
"""
OLD_NODE_RE = re.compile(r'^(#{2,6})\s+(N\d+(?:\.\d+)*)\b\s*(.*)$')  # 1.0.0, kept as the oracle

# 1.1.0: the bold spelling of the same outline (both bold forms), and a chain fixture for the ancestor lines.
BOLD = (FIXTURE.replace('- 任务：', '- **任务**：').replace('- 顺序：', '- **顺序：**')
        .replace('- 关系：', '- **关系**：').replace('- 展开：', '- **展开**：'))
CHAIN = """# 链-提纲

## N0 根

- **主旨**：根判断第一句（旁注甲（内层））。根判断第二句！根判断第三句。
- 任务：答决策问题。
- 顺序：树根。

## N1 一、甲〔标题〕

- **主旨**：甲的主旨。
- **任务**：立排序依据。
- **顺序**：甲在乙之前。
- **关系**：和N0，通过排序依据，是主张与支持，和N2，通过先后，是前提与依赖

### N1.1 段群：甲一

- **主旨**：%s
- 任务：分渠道。
- 顺序：甲一放第一。
- 关系：和N1.2，通过渠道，是递进与深化
  - 和N1，通过分渠道，是论断与支持

#### N1.1.1 段群：甲一一

- **主旨**：一例。
- 任务：举一例。

### N1.2 段群：甲二

- **主旨**：甲二。
- 任务：承接。
- 关系：和N1.1，通过续写，是承接关系

### N1.3 段群：甲三

- **主旨**：甲三短句。
- **任务：**收束甲。
- **顺序：**甲三放最后。
- 关系：和N11，通过错号，是比较与对照；和N1.3.1，通过子段，是总述与展开

#### N1.3.1 段群：甲三一

- **主旨**：甲三一。
- 任务：甲三一。
- 顺序：甲三一在前。

#### N1.3.2 段群：甲三二

- **主旨**：甲三二。
- 任务：甲三二。

## N2 二、乙

- 〔标题〕二、乙
- **主旨**：乙。
- 任务：收束全篇。
- 顺序：乙放最后。
- 关系：和N1，通过对照，是比较与对照。
- 关系：和N0，通过收束，是归纳与综合。

### N2.1 段群：乙一

- **主旨**：乙一。
- 任务：乙一。
""" % ('甲一' * 110)
# Fix round 1 (T0 rulings R1-R3, 2026-11-11).
RULINGS = """# 裁定-提纲

## N0：样稿

- 〔标题〕《样稿》
- **主旨**：根主旨。
- 任务：答问题。

## N1 导语〔段群〕

- 〔标题〕无（导语）
- **主旨**：导语主旨一句。导语第二句。导语第三句。
- 任务：给答案。
- 关系：待回填。

### N1.1 段群：一

- **主旨**：一。
- 任务：一。
- **关系**：
- 顺序：一在前。

#### N1.1.1 段群：一一

- **主旨**：一一。
- 任务：一一。
"""
FIELD_COUNT_RE = re.compile(r'^\s*(?:- )?(?:\*\*)?(任务|顺序|关系)(?:\*\*)?\s*[：:]')


def ruling_checks(tmp, run, check):
    """One assertion per T0 ruling R1-R4 (fix rounds 1 and 2); each fails on 1.0.1 and on the stage copy before
    its fix round."""
    path = os.path.join(tmp, 'rulings-提纲.md')
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(RULINGS)
    c, o, e = run(['chain', path, 'N1.1.1', '--path'])
    n1 = re.search(r'^## N1 .*?(?=^#{2,6} N|\Z)', o, re.M | re.S)
    n1 = n1.group(0) if n1 else ''
    check('R1 an ancestor whose 〔标题〕 reads 无… is untitled: it gets the 主旨 opening', c == 0
          and '- 主旨（开头）：导语主旨一句。导语第二句。……（全文：node N1）' in n1)
    cv, ov, ev = run(['view', path])
    check('R2 placeholder 关系 lines (待回填…, empty) print nothing in chain; view keeps them; edge 顺序 still there',
          c == 0 and '关系' not in o and '- 顺序：一在前。' in o
          and '- 关系：待回填。' in ov and '- **关系**：' in ov)
    check('R3 K-OS-1 ignores enclosing 《》: 〔标题〕《样稿》 under heading “样稿” is dropped, usage line kept',
          c == 0 and '## N0：样稿' in o and '〔标题〕' not in o.split('## N1 ')[0] and CHAIN_USAGE in o)
    check('R4 a titled N0 still gets the 主旨 opening (right after its heading, before its 任务 line)',
          c == 0 and '## N0：样稿\n- 主旨（开头）：根主旨。\n- 任务：答问题。' in o)


# Fix round 3 (R5): the single-id chain of CHAIN N1.3.2 as the fix-round-2 copy printed it, byte for byte.
GOLDEN_N132 = ('<!-- ancestor chain of N1.3.2, outline_slice.py %s -->\n' + CHAIN_USAGE + '\n\n'
               '## N0 根\n- 主旨（开头）：根判断第一句。根判断第二句！……（全文：node N0）\n- 任务：答决策问题。\n\n'
               '## N1 一、甲〔标题〕\n- **任务**：立排序依据。\n- 关系（对上一级）：和N0，通过排序依据，是主张与支持\n'
               '- **顺序**：甲在乙之前。\n\n'
               '### N1.3 段群：甲三\n- 主旨（开头）：甲三短句。\n- **任务：**收束甲。\n'
               '- 关系：和N11，通过错号，是比较与对照；和N1.3.1，通过子段，是总述与展开\n- **顺序：**甲三放最后。\n')


def unit_checks(tmp, run, check):
    """R5 (fix round 3): chain with several ids prints one chain for the writing unit."""
    path = os.path.join(tmp, 'unit-chain-提纲.md')
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(CHAIN)

    def heads(o):
        return [l for l in o.splitlines() if re.match(r'^#{2,6} N', l)]

    c, o, e = run(['chain', path, 'N1.3.2', '--path'])
    check('R5 one id: output byte for byte as the fix-round-2 copy, usage line as of R13 (CHAIN N1.3.2)', c == 0 and o == GOLDEN_N132 % VERSION)
    c, o, e = run(['chain', path, 'N1.2', 'N1.3.1', '--path'])
    check('R5 unit: one comment line naming the ids, the usage line once, each ancestor once, root first', c == 0
          and o.splitlines()[0] == '<!-- ancestor chain of N1.2 N1.3.1, outline_slice.py %s -->' % VERSION
          and o.count(CHAIN_USAGE) == 1
          and heads(o) == ['## N0 根', '## N1 一、甲〔标题〕', '### N1.3 段群：甲三'])
    c, o, e = run(['chain', path, 'N1.3', 'N1.3.1', 'N1.3.2', '--path'])
    check('R5 unit: an ancestor that is one of the ids is left out (N1.3); ancestors N0, N1', c == 0
          and heads(o) == ['## N0 根', '## N1 一、甲〔标题〕'] and '甲三短句' not in o)
    c, o, e = run(['chain', path, 'N1.2', 'N1.3', '--path'])
    n1 = o.split('## N1 一、甲〔标题〕\n', 1)[-1].split('\n\n', 1)[0]
    check('R5 unit: the edge 顺序 line (N1.3 last, N1.2 middle) sits once, under its heading', c == 0
          and o.count('甲在乙之前') == 1 and '- **顺序**：甲在乙之前。' in n1)
    c, o, e = run(['chain', path, 'N1.1.1', 'N1.2', '--path'])
    check('R5 unit: fields are the union (N1 顺序 through N1.1.1; N1.1 only for N1.1.1, once)', c == 0
          and heads(o) == ['## N0 根', '## N1 一、甲〔标题〕', '### N1.1 段群：甲一'] and o.count('甲在乙之前') == 1
          and '- 顺序：甲一放第一。' in o)
    c, o, e = run(['chain', path, 'N1.2', 'N9.9', '--path'])
    check('R5 unit: an unknown id among several exits 2 with the unknown-id message (R14)', c == 2
          and 'unknown node id: N9.9' in e and o == '')


# 1.1.0 second part: the 收尾 field (three spellings), close findings and duty lines.
def _three(p, name):
    return ''.join('### %s.%d 段群：%s%d\n- **主旨**：%s%d。\n- 任务：%s%d。\n\n' % (p, k, name, k, name, k, name, k)
                   for k in (1, 2, 3))


CLOSES = ("""# 收尾-提纲

## N0 根

- **主旨**：根。
- 任务：答问题。
- 收尾：N3.3；全篇的收尾在丙三。

## N1 一、甲〔标题〕

- **主旨**：甲。
- **任务**：立甲。
- **顺序**：甲在前。
- **收尾**：N1.3；末段收拢甲的三个子节，交给 N2。

### N1.1 段群：甲一
- **主旨**：甲一。
- 任务：甲一。

### N1.2 段群：甲二
- **主旨**：甲二。
- 任务：甲二。

### N1.3 段群：甲三
- **主旨**：甲三。
- 任务：甲三。
- 收尾：N1.3.2；甲三自己的收尾。

#### N1.3.1 段群：甲三一
- **主旨**：甲三一。
- 任务：甲三一。

#### N1.3.2 段群：甲三二
- **主旨**：甲三二。
- 任务：甲三二。

## N2 二、乙
- 〔标题〕二、乙
- **主旨**：乙。
- 任务：立乙。
- **收尾：**不设（T0 裁：三段并列，各段自带落点）。

""" + _three('N2', '乙') + """## N3 三、丙
- **主旨**：丙。
- 任务：立丙。
- 收尾：N2.1；挂错了地方。

""" + _three('N3', '丙') + """## N4 四、丁
- **主旨**：丁。
- 任务：立丁。

""" + _three('N4', '丁') + """## N5 五、戊
- **主旨**：戊。
- 任务：立戊。
- 收尾：N5.9。

""" + _three('N5', '戊') + """## N6 六、己
- **主旨**：己。
- 任务：立己。
- 收尾：待定。

""" + _three('N6', '己'))
CLOSE_FINDINGS = ['CLOSE-BAD-TARGET N3 -> N2.1', 'CLOSE-UNASSIGNED N4 (3 children)', 'CLOSE-BAD-TARGET N5 -> N5.9',
                  'CLOSE-UNREADABLE N6']


def wave2_checks(tmp, run, check):
    """1.1.0 second part (P1-P3): default chain, --path [N], 收尾 findings and duty lines.  Each assertion holds a
    part the fix-round-3 copy cannot print, so each fails there."""
    paths = {}
    for name, text in (('fixture', FIXTURE), ('bold', BOLD), ('chain', CHAIN), ('rulings', RULINGS),
                       ('closes', CLOSES),
                       ('closes_ok', CLOSES.split('## N3 ')[0].replace('收尾：N3.3；全篇的收尾在丙三', '收尾：N2.3；全篇的收尾在乙三'))):
        paths[name] = os.path.join(tmp, 'w2-%s-提纲.md' % name)
        with open(paths[name], 'w', encoding='utf-8') as fh:
            fh.write(text)

    def com(*ids):
        return '<!-- ancestor chain of %s, outline_slice.py %s -->\n' % (' '.join(ids), VERSION)

    def heads(o):
        return [l for l in o.splitlines() if re.match(r'^#{2,6} N', l)]

    duty1 = CLOSE_DUTY + 'N1.3；末段收拢甲的三个子节，交给 N2。'
    duty0 = CLOSE_DUTY + 'N3.3；全篇的收尾在丙三。'
    # P1 default mode
    c, o, e = run(['chain', paths['chain'], 'N1.3.2'])
    check('P1 default chain: heading, 〔标题〕 and 任务 lines only (no usage line, 主旨 opening, 关系, 顺序)', c == 0
          and o == com('N1.3.2') + '## N0 根\n- 任务：答决策问题。\n\n## N1 一、甲〔标题〕\n- **任务**：立排序依据。\n\n'
          '### N1.3 段群：甲三\n- **任务：**收束甲。\n')
    want = (com('N1.1.1') + '## N0 根主旨\n- 〔标题〕样例根标题\n- 任务：答决策问题。\n\n### N1 一、外部账户\n'
            '- 任务：立排序依据。\n\n#### N1.1 （一）零售定价\n- 任务：分渠道。\n')
    c, o, e = run(['chain', paths['fixture'], 'N1.1.1'])
    cb, ob, eb = run(['chain', paths['bold'], 'N1.1.1'])
    check('P1 default chain: own 〔标题〕 kept, one repeating the heading dropped (K-OS-1); plain and bold 任务',
          c == 0 and o == want and cb == 0 and ob == want.replace('- 任务：', '- **任务**：'))
    c, o, e = run(['chain', paths['rulings'], 'N1.1.1'])
    check('P1 default chain: 〔标题〕无… kept, 《样稿》 dropped, no 主旨 opening even for N0, placeholder 关系 and 顺序 out',
          c == 0 and o == com('N1.1.1') + '## N0：样稿\n- 任务：答问题。\n\n## N1 导语〔段群〕\n- 〔标题〕无（导语）\n'
          '- 任务：给答案。\n\n### N1.1 段群：一\n- 任务：一。\n')
    c, o, e = run(['chain', paths['chain'], 'N1.2', 'N1.3.1'])
    check('P1 default chain, several ids: comment line naming them, each ancestor once, root first (R5 kept)', c == 0
          and o == com('N1.2', 'N1.3.1') + '## N0 根\n- 任务：答决策问题。\n\n## N1 一、甲〔标题〕\n'
          '- **任务**：立排序依据。\n\n### N1.3 段群：甲三\n- **任务：**收束甲。\n')
    # P1 --path N
    g = GOLDEN_N132 % VERSION
    top = g.split('## N0 ')[0]
    c1, o1, e1 = run(['chain', paths['chain'], 'N1.3.2', '--path', '1'])
    c2, o2, e2 = run(['chain', paths['chain'], 'N1.3.2', '--path', '2'])
    c9, o9, e9 = run(['chain', paths['chain'], 'N1.3.2', '--path', '9'])
    check('P1 --path N: the nearest N ancestors as --path prints them, farther ones (N0 included) left out; N >= depth '
          '= --path', c1 == c2 == c9 == 0 and o1 == top + '### N1.3 ' + g.split('### N1.3 ')[1]
          and o2 == top + '## N1 ' + g.split('## N1 ')[1] and o9 == g)
    c, o, e = run(['chain', paths['chain'], 'N1.1.1', 'N1.2', '--path', '1'])
    check('P1 --path N, several ids: the union of each id\'s nearest N (N1.1 for N1.1.1, N1 for N1.2), N0 out', c == 0
          and heads(o) == ['## N1 一、甲〔标题〕', '### N1.1 段群：甲一'] and o.count(CHAIN_USAGE) == 1
          and '主旨（开头）：根' not in o and '- 顺序：甲一放第一。' in o)
    bad = [run(['chain', paths['chain'], 'N1.3.2', '--path', v]) for v in ('0', 'x', '-1', '1.5', '')]
    check('P1 --path N: N not an integer >= 1 (0, x, -1, 1.5, empty) exits 2 with a message, nothing on stdout',
          all(c == 2 and o == '' and 'integer >= 1' in e for c, o, e in bad))
    # P2 close findings and view
    c, o, e = run(['nodes', paths['closes'], '--check', '--closes'])
    fl = [l for l in o.splitlines() if l.startswith('CLOSE-')]
    check('P2 nodes --check --closes: unassigned, bad target (outside the node; no block), unreadable; 不设 and a '
          'valid target pass; exit 2', c == 2 and fl == CLOSE_FINDINGS
          and 'closes: 7 nodes with three or more children, 4 findings' in o and 'close findings' in e)
    c2, o2, e2 = run(['nodes', paths['closes'], '--closes'])
    c3, o3, e3 = run(['nodes', paths['closes_ok'], '--check', '--closes'])
    check('P2 --closes implies --check; plain, **收尾**： and **收尾：** spellings read; all assigned -> exit 0',
          c2 == 2 and o2 == o and c3 == 0 and 'closes: 2 nodes with three or more children, 0 findings' in o3
          and 'CLOSE-' not in o3)
    c, o, e = run(['view', paths['closes']])
    check('P2 view prints 收尾 lines (three spellings)', c == 0 and '- 收尾：N3.3；全篇的收尾在丙三。' in o
          and '- **收尾**：N1.3；末段收拢甲的三个子节，交给 N2。' in o and '- **收尾：**不设（T0 裁：三段并列，各段自带落点）。' in o)
    # P3 duty line
    duty13 = CLOSE_DUTY + 'N1.3.2；甲三自己的收尾。'
    c, o, e = run(['chain', paths['closes'], 'N1.3.1', 'N1.3.2'])
    check('P3 default chain: the unit holding the target\'s last node gets the duty line under each assigning ancestor '
          '(N1 -> N1.3, N1.3 -> N1.3.2, a node with two children)', c == 0
          and o == com('N1.3.1', 'N1.3.2') + '## N0 根\n- 任务：答问题。\n\n## N1 一、甲〔标题〕\n- **任务**：立甲。\n'
          + duty1 + '\n\n### N1.3 段群：甲三\n- 任务：甲三。\n' + duty13 + '\n')
    c, o, e = run(['chain', paths['closes'], 'N1.1'])
    check('P3 a unit not holding the target gets no duty line', c == 0 and o == com('N1.1')
          + '## N0 根\n- 任务：答问题。\n\n## N1 一、甲〔标题〕\n- **任务**：立甲。\n')
    c, o, e = run(['chain', paths['closes'], 'N1.3.1', 'N1.3.2', '--path'])
    check('P3 --path: the duty line closes the ancestor\'s block, after its edge 顺序 line', c == 0
          and o.startswith(com('N1.3.1', 'N1.3.2') + CHAIN_USAGE + '\n\n') and o.count(CLOSE_DUTY) == 2
          and '- **顺序**：甲在前。\n' + duty1 + '\n\n### N1.3 ' in o and o.endswith('- 任务：甲三。\n' + duty13 + '\n'))
    c, o, e = run(['chain', paths['closes'], 'N3.3', '--path', '1'])
    check('P3 --path 1: an ancestor outside N with a duty prints as its heading and the duty line only', c == 0
          and o == com('N3.3') + CHAIN_USAGE + '\n\n## N0 根\n' + duty0 + '\n\n## N3 三、丙\n- 主旨（开头）：丙。\n'
          '- 任务：立丙。\n')
    c, o, e = run(['chain', paths['closes'], 'N3.1', 'N2.1'])
    check('P3 收尾：不设 prints nothing; a 收尾 naming a node outside its own subtree (N3 -> N2.1) prints nothing', c == 0
          and o == com('N3.1', 'N2.1') + '## N0 根\n- 任务：答问题。\n\n## N2 二、乙\n- 任务：立乙。\n\n## N3 三、丙\n'
          '- 任务：立丙。\n')
    c, o, e = run(['chain', paths['closes'], 'N1', 'N1.3'])
    check('P3 an assigning node that is one of the ids is not printed (its 收尾 travels in the slice)', c == 0
          and o == com('N1', 'N1.3') + '## N0 根\n- 任务：答问题。\n')


# Fix round after the change-protocol review (T0 rulings R6-R14, 2026-11-11): edge cases for 收尾 and ids.
def _kids(p, n):
    return ''.join('### %s.%d 段群：%d\n- **主旨**：%d。\n- 任务：%d。\n\n' % (p, k, k, k, k) for k in range(1, n + 1))


EDGE = ("""# 边界-提纲

## N0 根
- **主旨**：根。
- 任务：答问题。
- 收尾：不设（全篇不收）。

## N1 一、甲
- **主旨**：甲。
- 任务：立甲。
- 关系：和N0X，通过错号，是支持
- 收尾：N1.3X；看着像编号。

""" + _kids('N1', 3) + """## N2 二、乙
- **主旨**：乙。
- 任务：立乙。
- 收尾：不设。

""" + _kids('N2', 1) + """## N3 三、丙
- **主旨**：丙。
- 任务：立丙。
- 收尾：N3.1；甲。
- 收尾：N3.2；乙。

""" + _kids('N3', 2) + """## N4 四、丁
- **主旨**：丁。
- 任务：立丁。
- 收尾：N4.2；第一行，
  续行：交给N5的是什么。
- 展开：两段。
  - 收尾：这是展开里的子项

""" + _kids('N4', 2) + """## N5 五、戊
- **主旨**：戊。
- 任务：立戊。
- 展开：三段。
  - 收尾：这是展开里的子项

""" + _kids('N5', 3) + """## N6 六、己
- **主旨**：己。
- 任务：立己。
- 收尾：N6.2.9；不存在的孙。

""" + _kids('N6', 2))
EDGE_FINDINGS = ['CLOSE-WAIVED-ROOT N0', 'CLOSE-UNREADABLE N1', 'CLOSE-WAIVER-NO-REASON N2', 'CLOSE-DUPLICATE N3',
                 'CLOSE-UNASSIGNED N5 (3 children)', 'CLOSE-BAD-TARGET N6 -> N6.2.9']


def fix_checks(tmp, run, check):
    """One assertion per ruling R6-R13 (outline side); each fails on the copy before this fix round."""
    path = os.path.join(tmp, 'edge-提纲.md')
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(EDGE)
    cpath = os.path.join(tmp, 'fx-closes-提纲.md')
    with open(cpath, 'w', encoding='utf-8') as fh:
        fh.write(CLOSES)
    c, o, e = run(['nodes', path, '--check', '--closes'])
    fl = [l for l in o.splitlines() if l.startswith('CLOSE-')]

    def one(token):
        m = os.path.join(tmp, 'tok-提纲.md')
        with open(m, 'w', encoding='utf-8') as fh:
            fh.write('## N0 根\n- **主旨**：根。\n- 收尾：N1；收。\n\n## N1 一\n- **主旨**：一。\n- 收尾：%s\n\n%s'
                     % (token, _kids('N1', 3)))
        return [l for l in run(['nodes', m, '--closes'])[1].splitlines() if l.startswith('CLOSE-')]
    bad = [one(t + '；看着像编号。') for t in ('N1.3X', 'N1.3.abc', 'N1.3e2', 'N1X')]
    good = [one(t) for t in ('N1.3；收拢。', 'N1.3收拢三段。', 'N1.3 收拢', 'N1.3', 'N1.3。')]
    check('R6 收尾 target: N1.3X, N1.3.abc, N1.3e2, N1X -> CLOSE-UNREADABLE; N1.3 before Chinese, punctuation, '
          'space or line end is the id', all(b == ['CLOSE-UNREADABLE N1'] for b in bad) and all(g == [] for g in good))
    c1, o1, e1 = run(['chain', path, 'N1.1', '--path'])
    check('R6 relation endpoint: 和N0X is not a clause naming N0 (the 关系 line prints verbatim)', c1 == 0
          and '- 关系：和N0X，通过错号，是支持' in o1 and '关系（对上一级）' not in o1)
    check('R7 a waiver needs its ground (CLOSE-WAIVER-NO-REASON N2) and is refused on N0 (CLOSE-WAIVED-ROOT); '
          'a grounded waiver below the root passes (CLOSES N2)', c == 2 and 'CLOSE-WAIVED-ROOT N0' in fl
          and 'CLOSE-WAIVER-NO-REASON N2' in fl and not [l for l in run(['nodes', cpath, '--closes'])[1].splitlines()
                                                        if l.startswith('CLOSE-') and l.split()[1] == 'N2'])
    got = dict((tuple(ids), run(['chain', cpath] + ids)[1].count(CLOSE_DUTY)) for ids in (
        ['N1.3'], ['N1.3.2'], ['N3'], ['N3.3']))
    check('R8 the duty reaches the unit holding the last node of the target\'s subtree: N1 -> N1.3 at N1.3.2 (not '
          'N1.3); N0 -> N3.3 (childless) at N3.3, not N3', got == {('N1.3',): 0, ('N1.3.2',): 2, ('N3',): 0,
                                                              ('N3.3',): 1})
    c3, o3, e3 = run(['chain', path, 'N3.1'])
    c4, o4, e4 = run(['chain', path, 'N3.2'])
    check('R9 two 收尾 lines in a block -> CLOSE-DUPLICATE, and chain prints no duty from that block',
          'CLOSE-DUPLICATE N3' in fl and c3 == c4 == 0 and CLOSE_DUTY not in o3 + o4)
    c6, o6, e6 = run(['chain', path, 'N6.2'])
    check('R10 a 收尾 line is validated on a node with fewer than three children (N6 -> N6.2.9, N2 waiver); no duty '
          'to a target without a block', 'CLOSE-BAD-TARGET N6 -> N6.2.9' in fl and 'CLOSE-WAIVER-NO-REASON N2' in fl
          and c6 == 0 and CLOSE_DUTY not in o6)
    c5, o5, e5 = run(['chain', path, 'N4.2'])
    check('R11 a 收尾 line carries its continuation lines; a nested sub-bullet is not the node\'s 收尾 (N4 passes, '
          'N5 is unassigned, not unreadable)', c5 == 0 and CLOSE_DUTY + 'N4.2；第一行，续行：交给N5的是什么。\n' in o5
          and not [l for l in fl if ' N4' in l] and 'CLOSE-UNASSIGNED N5 (3 children)' in fl and fl == EDGE_FINDINGS)
    check('R12 the duty label carries the C17 clause', '\n- 收尾（本单元写；照 FICCVoice.md C17：收拢已立的判断并往前一步，'
          '不换说法重申主旨）：N4.2；' in o5)
    lines = o1.splitlines()
    check('R13 the --path usage line says the chain is read-only background except the 收尾（本单元写…） line',
          len(lines) > 1 and lines[1] == CHAIN_USAGE and '“收尾（本单元写…）”一行除外' in lines[1])


# 1.2.0: the §3.2 living-outline template filled with neutral generic content (甲公司, 甲档/乙档; no task material).
LIVING = """# 样例文稿-提纲｜树r3｜材料r2｜截至2026-11-20

## 1. 问题与开工必判卡
- 研究问题：甲公司｜2024–2025年报合并口径｜回款放缓是否压住偿债能力
- 目标读者：具备FICC基础的专业读者｜读完导语即可启动的决策动作：决定是否调整持仓
- 开工问（至多4问，每问只作1个判断，生人仅读标题＋N0导语即可答齐，比率型门槛必填分母）：
  - Q1｜回款放缓是否到了压住偿债的程度｜必带判据：门槛应收占收入20%｜分母营业收入80.0亿元@甲档:L12，新增额不入分母｜窗口2025年报至2026年中报｜删去后会答错什么：会把应收增长误读为收入扩张｜若材料未决：卡在账龄分布，看下期账龄表
  - Q2｜短债能否靠现金覆盖｜必带判据：门槛1.0倍｜分母短期借款@甲档:L30｜窗口2025年末
    ｜删去后会答错什么：会把总现金当成可动用现金｜若材料未决：卡在受限现金，看附注
- 范围排除（不做什么）：不评估股价，不做同业比较

## 2. 名字表
| 名字 | 指代与口径 | 本篇写法 | 不许用 |
|---|---|---|---|
| 甲公司 | 合并报表主体@甲档:L1 | 甲公司 | 甲集团 |

## 3. 关键边表（跨枝、不相邻或有争议接缝，按排序端点对立键，一条命题只裁一次）
| 边ID | 端点对（排序键） | 关系类（S18）与作用方向 | 连接句凭据@原件锚点 | 状态（已定／待据／不成立） | 两端禁写边界 | 判于版本 |
|---|---|---|---|---|---|---|
| X01 | N2.1—N1.2 | 铺垫与回应（N1.2→N2.1） | E020@甲档:L88 | 已定 | N1.2只摆回款数，偿债推论留N2.1 | r2 |
| X02 | N1.2—N2.1 | 拟议因果（回款→偿债） | 甲档@L40与乙档@L7各述一端，无连接句 | 待据（转核源） | 两端禁写成因果 | r3 |
| X03 | N1.10—N1.9 | 比较与对照 | E031@乙档:L5 | 不成立 | 无 | r1 |

## 4. 改号表（节点号永不复用，改挂时发新号并由脚本同步全树引用）
- N1.3→N1.10｜树r2

## 5. 提纲树

### N0 导语
- 〔标题〕无（导语不设标题）
- **主旨**：甲公司回款放缓尚未压住偿债｜因：现金覆盖短债｜限：见问题卡Q1、Q2｜性质与把握：我们推断·大概率
- 分担：“回款放缓”→N1·主干｜“偿债未受压”→N2·链环｜遮住任一部少哪一步：遮住N2只剩回款事实｜无人担：无｜重复担：无｜子项合计仍证不出：无〔判于r3〕
- 展开：上限600字｜本单元写：全篇导语
- 收尾：N2.1｜收拢全篇各环结论并交付检验窗口

### N1 回款
- 〔标题〕回款放缓但仍在门槛内
- **主旨**：回款放缓｜因：应收增速快于收入｜限：无｜性质与把握：披露
- 任务：担N0主旨中“回款放缓”这一环
- 顺序：先立回款事实，再交N2
- 接前：直承N0总题
- 分担：“应收上升”→N1.2·主干｜“账龄”→N1.9·链环｜遮住测试：遮住N1.2则无数据｜无人担：无｜重复担：无｜子项合计仍证不出：无〔判于r2〕
- 边：无
- 展开：子节点N1.2、N1.9、N1.10｜上限900字｜本单元写：部章导语
- 收尾：N1.10｜收拢回款结论，向N2移交偿债判断

#### N1.2 应收
- 〔标题〕应收占收入升至15%
- **主旨**：应收占收入升至15%｜因：赊销增加｜限：分母为营业收入｜性质与把握：我们自算·确定
- 任务：担N1主旨中“应收上升”这一环
- 顺序：第一步
- 接前：承N1题
- 边：X01、X02
- 展开：上限400字｜本单元写：节首＋正文
- 事实：写全 E012@甲档:L40｜回指 E020@甲档:L88（写全处N2.1）｜留表 @乙档:L120–L130（入表1，正文禁复述分档明细）
- 事实：写全 E013
- 算式：应收占比＝应收账款12.0亿元@甲档:L40÷营业收入80.0亿元@甲档:L12＝15.0%｜方向：缺口｜合并口径、2025年末、亿元｜假设：无｜复算闭合值：15.0%｜签认：核对席·2026-11-20
- 算式：应收增量＝期末应收12.0亿元@甲档:L40－期初应收9.5亿元@甲档:L38＝2.5亿元｜方向：净流向｜合并口径｜假设：期初未重述｜签认：<席或脚本·日期>
- 消歧：条件｜E012@甲档:L40｜“仅含合并范围内应收”→固定写法：合并口径应收｜禁写：全部应收
- 消歧：缺口或否定反查｜@乙档:L1–L300｜反查：“保理”@全文0次（已核附注全部条款）→固定写法：未披露保理｜禁写：已保理
- 段1：应收占收入升至15%｜接前：承节题｜事实：E012@甲档:L40、E013
- 段2：仍低于20%门槛｜接前：递进·凭：@甲档:L12｜事实：写全 E020@甲档:L88

#### N1.9 账龄
- **主旨**：账龄未拉长
- 任务：担N1主旨中“账龄”这一环
- 消歧：无（六类已查）
- 算式：无
- 段：不拆（写全陈述<=5条、无多维比较网格、无算式或推断）

#### N1.10 收束
- **主旨**：回款放缓仍在门槛内
- 关系：和N1，通过收束，是归纳与综合
- 标注：本节为改号后新号

### N2 偿债
- **主旨**：偿债未受压
- 任务：担N0主旨中“偿债未受压”这一环

#### N2.1 现金覆盖
- **主旨**：现金覆盖短债1.2倍
- 任务：担N2主旨
- 边：X01
- 算式：现金覆盖倍数＝货币资金36.0亿元@甲档:L22/短期借款30.0亿元@甲档:L30＝1.2倍｜分母：短期借款（不含一年内到期长债）｜方向：盈余｜口径：合并口径｜复算闭合值：1.2倍｜签认：未签
"""


FIELDS_KEYS = ['version', 'outline', 'tree_rev', 'material_rev', 'card', 'edges', 'edge_conflicts', 'renumber', 'nodes']
NODE_KEYS = ['heading', 'line', 'parent', 'children', 'gist', 'task', 'order', 'follows', 'edges', 'share', 'expand',
             'close', 'title', 'facts', 'derivations', 'disambig', 'paras', 'legacy']
BOLD_LABELS_RE = re.compile(r'^- (任务|顺序|接前|分担|边|展开|收尾|事实|算式|消歧|段[0-9]*|关系|标注|研究问题|目标读者'
                            r'|范围排除（不做什么）)：', re.M)


def living_checks(tmp, run, check):
    """1.2.0 fields: the §3.2 template filled (LIVING) parsed into the fixed JSON contract (W1-O1)."""
    path = os.path.join(tmp, 'living-提纲.md')
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(LIVING)
    ln = LIVING.split('\n')

    def at(prefix):  # file line (from 1) of the first line starting with prefix
        return next(k for k, l in enumerate(ln, 1) if l.startswith(prefix))

    def fields(argv):
        c, o, e = run(['fields'] + argv)
        try:
            return c, json.loads(o), e
        except ValueError:
            return c, None, e + o
    c, d, e = fields([path])
    ok = c == 0 and d is not None
    d = d or {'card': {'questions': [{}, {}]}, 'edges': [{}] * 3, 'nodes': {}}
    n = d['nodes']
    nd = dict((k, n.get(k, {})) for k in ('N0', 'N1', 'N1.2', 'N1.9', 'N1.10', 'N2', 'N2.1'))
    check('L1 fields: exit 0, one JSON object, top-level keys in contract order; H1 revisions 树r3 材料r2', ok
          and list(d) == FIELDS_KEYS and d['version'] == VERSION and d['outline'] == path
          and d['tree_rev'] == 'r3' and d['material_rev'] == 'r2')
    q1, q2 = (d['card']['questions'] + [{}, {}])[:2]
    check('L2 card: 研究问题, 目标读者, 范围排除（…）; Q rows split on ｜ into the six cells, a continuation line joined (Q2)',
          d['card'].get('research_q') == '甲公司｜2024–2025年报合并口径｜回款放缓是否压住偿债能力'
          and d['card'].get('reader', '').endswith('决策动作：决定是否调整持仓')
          and d['card'].get('scope_out') == '不评估股价，不做同业比较' and len(d['card']['questions']) == 2
          and q1 == dict(id='Q1', judgment='回款放缓是否到了压住偿债的程度', threshold='应收占收入20%',
                         denominator='营业收入80.0亿元@甲档:L12，新增额不入分母', window='2025年报至2026年中报',
                         misread='会把应收增长误读为收入扩张', unresolved='卡在账龄分布，看下期账龄表',
                         raw=ln[at('  - Q1') - 1].split('- ', 1)[1], line=at('  - Q1'))
          and q2.get('threshold') == '1.0倍' and q2.get('denominator') == '短期借款@甲档:L30'
          and q2.get('misread') == '会把总现金当成可动用现金' and q2.get('line') == at('  - Q2'))
    x1, x2, x3 = (d['edges'] + [{}] * 3)[:3]
    check('L3 edges: ends sorted by numeric id tuple (N1.9 before N1.10), key joined by —, status read off status_raw',
          len(d['edges']) == 3 and x1.get('ends') == ['N1.2', 'N2.1'] and x1.get('key') == 'N1.2—N2.1'
          and x3.get('key') == 'N1.9—N1.10' and [x.get('status') for x in (x1, x2, x3)] == ['已定', '待据', '不成立']
          and x2.get('status_raw') == '待据（转核源）' and x1.get('relation') == '铺垫与回应（N1.2→N2.1）'
          and x1.get('evidence') == 'E020@甲档:L88' and x2.get('bounds') == '两端禁写成因果' and x2.get('rev') == 'r3'
          and x1.get('line') == at('| X01') and x1.get('raw') == ln[at('| X01') - 1] and x1.get('id') == 'X01')
    check('L4 edge_conflicts: one key on two rows (X01 已定, X02 待据, ends written in either order); X03 alone is none',
          d.get('edge_conflicts') == [dict(key='N1.2—N2.1', ids=['X01', 'X02'], statuses=['已定', '待据'])])
    check('L5 renumber: 旧号→新号｜树r<k>', d.get('renumber') == [dict(old='N1.3', new='N1.10', rev='r2',
                                                                  raw='N1.3→N1.10｜树r2')])
    check('L6 nodes: document order, node keys in contract order, heading, heading line, parent, children', list(n) == [
        'N0', 'N1', 'N1.2', 'N1.9', 'N1.10', 'N2', 'N2.1'] and all(list(v) == NODE_KEYS for v in n.values())
        and nd['N1.2'].get('heading') == '应收' and nd['N1.2'].get('line') == at('#### N1.2 ')
        and nd['N0'].get('parent') is None and nd['N1.10'].get('parent') == 'N1'
        and nd['N1'].get('children') == ['N1.2', 'N1.9', 'N1.10'] and nd['N2.1'].get('children') == [])
    g0, s0, s1 = nd['N0'].get('gist') or {}, nd['N0'].get('share') or {}, nd['N1'].get('share') or {}
    check('L7 gist cells, 分担 items/tests/rev, 收尾 target, 〔标题〕, 任务, 顺序, 接前, 展开, 边 (无 -> [], ids)',
          g0.get('judgment') == '甲公司回款放缓尚未压住偿债' and g0.get('cause') == '现金覆盖短债'
          and g0.get('limit') == '见问题卡Q1、Q2' and g0.get('modality') == '我们推断·大概率'
          and s0.get('items') == [dict(element='回款放缓', child='N1', role='主干'),
                                  dict(element='偿债未受压', child='N2', role='链环')]
          and s0.get('cover_test') == '遮住N2只剩回款事实' and s0.get('uncovered') == '无' and s0.get('duplicate') == '无'
          and s0.get('insufficient') == '无' and s0.get('rev') == 'r3' and s1.get('rev') == 'r2'
          and s1.get('cover_test') == '遮住N1.2则无数据' and nd['N1.2'].get('share') is None
          and nd['N0'].get('close') == dict(target='N2.1', text='N2.1｜收拢全篇各环结论并交付检验窗口')
          and (nd['N1'].get('close') or {}).get('target') == 'N1.10' and nd['N1.2'].get('close') is None
          and nd['N0'].get('title') == '无（导语不设标题）' and nd['N1'].get('task') == '担N0主旨中“回款放缓”这一环'
          and nd['N1'].get('order') == '先立回款事实，再交N2' and nd['N1'].get('follows') == '直承N0总题'
          and nd['N1.2'].get('expand') == '上限400字｜本单元写：节首＋正文' and nd['N1'].get('edges') == []
          and nd['N1.2'].get('edges') == ['X01', 'X02'] and nd['N2.1'].get('edges') == ['X01'])
    f = nd['N1.2'].get('facts') or [{}] * 4
    check('L8 事实 (two lines, kept in order): modes 写全/回指/留表; anchors id@doc:L, @doc:La–Lb, id only; notes',
          [(x.get('mode'), x.get('id'), x.get('doc'), x.get('lines'), x.get('note')) for x in f] == [
              ('写全', 'E012', '甲档', [40, 40], None), ('回指', 'E020', '甲档', [88, 88], '写全处N2.1'),
              ('留表', None, '乙档', [120, 130], '入表1，正文禁复述分档明细'), ('写全', 'E013', None, None, None)]
          and f[2].get('anchor') == '@乙档:L120–L130' and f[1].get('raw') == 'E020@甲档:L88（写全处N2.1）')
    dv = (nd['N1.2'].get('derivations') or []) + (nd['N2.1'].get('derivations') or [])
    a, b, z = (dv + [{}] * 3)[:3]
    check('L9 算式: signed vs unsigned (<…>, 未签); metric; value from 复算 or the expr tail; denominator after ÷, '
          'explicit 分母 wins; operands name/value/anchor; line', len(dv) == 3
          and [x.get('signed') for x in dv] == [True, False, False]
          and [x.get('signer') for x in dv] == ['核对席·2026-11-20', '<席或脚本·日期>', '未签']
          and [x.get('metric') for x in dv] == ['应收占比', '应收增量', '现金覆盖倍数']
          and [x.get('value') for x in dv] == ['15.0%', '2.5亿元', '1.2倍']
          and [x.get('denominator') for x in dv] == ['营业收入', None, '短期借款（不含一年内到期长债）']
          and a.get('operands') == [dict(name='应收账款', value='12.0亿元', anchor='@甲档:L40'),
                                    dict(name='营业收入', value='80.0亿元', anchor='@甲档:L12')]
          and a.get('expr') == '应收账款12.0亿元@甲档:L40÷营业收入80.0亿元@甲档:L12＝15.0%'
          and a.get('basis') == '合并口径、2025年末、亿元' and a.get('direction') == '缺口' and a.get('assume') == '无'
          and z.get('basis') == '合并口径' and z.get('direction') == '盈余' and b.get('assume') == '期初未重述'
          and a.get('line') == at('- 算式：应收占比') and z.get('line') == at('- 算式：现金覆盖倍数')
          and nd['N1.9'].get('derivations') == [])
    check('L9b (W4b) a 签认 cell is signed only with a date and no pending word: 核对席·未签, 核对席（待核）, 核对席-待核, '
          '核对席待核, a dated cell with 待复核, a bare seat or 已签 are unsigned; seat·date, seat·method·date, 11-20 and '
          '2026年11月20日 are signed',
          [signed_cell(v) for v in ('核对席·未签', '核对席·待核', '提纲席·待复算', '核对席 未签', '待签', '核对席（待核）',
                                    '核对席-待核', '核对席待核', '核对席·2026-11-20·待复核', '核对席', '已签',
                                    '核对席·待·2026-11-25', '核对席·2026-11-20·待', '核对席·未·2026-11-20', '核对席 未 11-20',
                                    '拟于2026-11-25复核', '2026-11-25前复核', '复核中·2026-11-20', '预计11-25签',
                                    'pending 2026-11-25', '提纲席·python3.11复算', '核对席·见表3.2', '核对席·L12-15')] == [False] * 23
          and signed_cell('核对席·无误·2026-11-20')
          and signed_cell('核对席·2026-11-20') and signed_cell('提纲席·python复算·2026-11-21')
          and signed_cell('提纲席（脚本复算）·2026-11-21') and signed_cell('python3复算·2026-11-21')
          and signed_cell('核对席·11-20') and signed_cell('核对席·2026年11月20日')
          and parse_derivation('占比＝甲12.0亿元@甲档:L40÷乙80.0亿元@甲档:L12＝15.0%｜签认：核对席·未签', 1)['signed']
          is False)
    m1, m2 = ((nd['N1.2'].get('disambig') or []) + [{}, {}])[:2]
    check('L10 消歧: quote → fixed, banned; 反查 → reverse, fixed; 无（六类已查） -> none', [
        m1.get(k) for k in ('cls', 'anchor', 'quote', 'reverse', 'fixed', 'banned', 'none')] == [
        '条件', 'E012@甲档:L40', '仅含合并范围内应收', None, '合并口径应收', '全部应收', False]
        and [m2.get(k) for k in ('cls', 'anchor', 'quote', 'reverse', 'fixed', 'banned')] == [
        '缺口或否定反查', '@乙档:L1–L300', None, '“保理”@全文0次（已核附注全部条款）', '未披露保理', '已保理']
        and [x.get('none') for x in nd['N1.9'].get('disambig') or []] == [True])
    p = nd['N1.2'].get('paras') or [{}, {}]
    check('L11 段1/段2: k, claim, follows, facts (mode word cut); 段：不拆 -> k null, no_split', [
        (x.get('k'), x.get('claim'), x.get('follows'), x.get('facts'), x.get('no_split')) for x in p] == [
        (1, '应收占收入升至15%', '承节题', ['E012@甲档:L40', 'E013'], False),
        (2, '仍低于20%门槛', '递进·凭：@甲档:L12', ['E020@甲档:L88'], False)]
        and [(x.get('k'), x.get('no_split'), x.get('claim')) for x in nd['N1.9'].get('paras') or []] == [
        (None, True, None)])
    check('L12 legacy 关系 (label cut, current reader) and 标注', nd['N1.10'].get('legacy') == {
        '关系': ['和N1，通过收束，是归纳与综合'], '标注': ['本节为改号后新号']} and nd['N1'].get('legacy') == {
        '关系': [], '标注': []})
    flip = iter(range(1000))
    bold = os.path.join(tmp, 'living-bold-提纲.md')
    with open(bold, 'w', encoding='utf-8') as fh:
        fh.write(BOLD_LABELS_RE.sub(lambda m: '- **%s%s' % (m.group(1), '**：' if next(flip) % 2 else '：**'), LIVING))
    cb, db, eb = fields([bold])
    check('L13 both label spellings (**X**： and **X：**) give the same head and nodes', cb == 0 and db is not None
          and dict(db, outline=path) == d and LIVING.count('- 算式：') == 4 and '- **算式' in open(bold, encoding='utf-8').read())
    c2, d2, e2 = fields([path, 'N1.2', 'N0', 'N1.2'])
    c3, o3, e3 = run(['fields', path, 'N1.2', 'N9.9'])
    c4, o4, e4 = run(['fields', os.path.join(tmp, 'missing-提纲.md')])
    check('L14 fields with ids: those nodes only, document order, head kept; unknown id or unreadable file -> exit 2, '
          'message, nothing on stdout', c2 == 0 and d2 is not None and list(d2['nodes']) == ['N0', 'N1.2']
          and d2['nodes']['N1.2'] == n.get('N1.2') and d2['edges'] == d['edges'] and c3 == 2
          and 'unknown node id: N9.9' in e3 and o3 == '' and c4 == 2 and 'cannot read' in e4 and o4 == '')
    blk = index(node_blocks(LIVING))['N1.2'][1]
    lf, th = living_fields(blk), tree_head(LIVING)
    rel = [at(s) - at('#### N1.2 ') + 1 for s in ('- 算式：应收占比', '- 算式：应收增量')]
    check('L15 library: living_fields(block_lines) (lines from 1 = heading) and tree_head(text) match fields',
          [x['line'] for x in lf['derivations']] == rel
          and all(lf[k] == n.get('N1.2', {}).get(k) for k in lf if k != 'derivations')
          and list(th) == FIELDS_KEYS[2:8] and all(th[k] == d.get(k) for k in th))
    old = os.path.join(tmp, 'living-old-提纲.md')
    with open(old, 'w', encoding='utf-8') as fh:
        fh.write(FIXTURE)
    c5, d5, e5 = fields([old])
    o5 = (d5 or {}).get('nodes', {})
    c6, o6, e6 = run(['nodes', path, '--check', '--closes'])
    c7, o7, e7 = run(['chain', path, 'N1.2'])
    check('L16 a 1.1.0 outline reads (no revisions, empty card and tables, legacy fields); the template fixture passes '
          'nodes --check --closes and chain', c5 == 0 and d5 is not None and d5['tree_rev'] is None
          and d5['card'] == dict(research_q=None, reader=None, scope_out=None, questions=[]) and d5['edges'] == []
          and d5['renumber'] == [] and list(o5) == ['N0', 'N1', 'N1.1', 'N1.1.1', 'N2']
          and o5['N0']['legacy']['关系'] == ['和N1，是呼应。'] and o5['N0']['gist']['judgment'] == '根判断。'
          and o5['N1']['task'] == '立排序依据。' and o5['N1.1']['expand'] == '一段。' and o5['N0']['title'] == '样例根标题'
          and c6 == 0 and 'closes: 1 nodes with three or more children, 0 findings' in o6
          and c7 == 0 and '- 任务：担N0主旨中“回款放缓”这一环' in o7)
    tpl = ('<无，或 结果名＝操作数名与值@原件直出锚点…｜方向：缺口／盈余／净流向｜层级、期间、单位、口径对齐说明｜假设｜'
           '复算闭合值｜签认：席或脚本·日期>')
    check('L17 the template unfilled 算式 row (placeholder opening the row, closing in the 签认 cell) is unsigned; '
          'a row whose 签认 cell is a whole placeholder too; W4b: a bare seat with no date is unsigned (the contract is '
          '<席或脚本·日期>, FICCOutline.md O-template)', parse_derivation(tpl, 1)['signed'] is False
          and parse_derivation('甲＝1＋2＝3｜签认：<席>', 1)['signed'] is False
          and parse_derivation('甲＝1＋2＝3｜签认：核对席', 1)['signed'] is False
          and parse_derivation('甲＝1＋2＝3｜签认：核对席·2026-01-31', 1)['signed'] is True)


# W1-O2: a living outline that passes every pre-prose gate (neutral content; identifiers in 主旨 on purpose).
GATED_X03 = ('| X03 | N1.1—N1.2 | 因果（账期延长导致应收增加） | “账期由九十天延至一百二十天，应收随之增加”@甲档:L41 | 已定 '
             '| 无 | r2 |')
GATED = """# 闸样例-提纲｜树r2｜材料r1｜截至2026-11-20

## 1. 问题与开工必判卡
- 研究问题：甲公司｜2025年报合并口径｜短债能否靠现金覆盖
- 目标读者：具备FICC基础的专业读者｜读完导语即可启动的决策动作：决定是否续作
- 开工问（至多4问，每问只作1个判断）：
  - Q1｜短债能否靠现金覆盖｜必带判据：门槛现金覆盖短债1.0倍｜分母短期借款30.0亿元@甲档:L30，新增额不入分母｜窗口2025年末至2026年中报｜删去后会答错什么：会把总现金当成可动用现金
  - Q2｜账龄是否拉长｜必带判据：门槛一年以上应收出现增加｜窗口2026年中报｜删去后会答错什么：会把回款放缓当成坏账上升
- 范围排除（不做什么）：不评估股价

## 2. 名字表
| 名字 | 指代与口径 | 本篇写法 | 不许用 |
|---|---|---|---|
| 甲公司 | 合并报表主体@甲档:L1 | 甲公司 | 甲集团 |

## 3. 关键边表
| 边ID | 端点对（排序键） | 关系类（S18）与作用方向 | 连接句凭据@原件锚点 | 状态（已定／待据／不成立） | 两端禁写边界 | 判于版本 |
|---|---|---|---|---|---|---|
| X01 | N1.2—N2.1 | 铺垫与回应（N1.2→N2.1） | E021@甲档:L22 | 已定 | N1.2只摆回款数 | r2 |
| X02 | N1.1—N2.1 | 拟议因果（账期→偿债） | 甲档@L41与乙档@L7各述一端，无连接句 | 待据（转核源） | 两端禁写成因果 | r2 |
""" + GATED_X03 + """

## 4. 改号表
- 无

## 5. 提纲树

### N0 导语
- 〔标题〕无（导语不设标题）
- **主旨**：甲公司2025年末短债可由现金覆盖｜因：甲档第2期账期条款未改，回款节奏与FY25同口径持平｜限：见问题卡Q1、Q2｜性质与把握：我们推断·大概率
- 分担：“回款未失速”→N1·主干｜“现金覆盖短债”→N2·链环｜遮住任一部少哪一步：遮住N2只剩回款事实｜无人担：无｜重复担：无｜子项合计仍证不出：无〔判于r2〕
- 展开：上限600字｜本单元写：全篇导语
- 收尾：N2.1｜收拢全篇结论并交付检验窗口

### N1 回款
- 〔标题〕回款放缓但账期未改
- **主旨**：回款在2026Q3前未失速｜因：E011所载账期条款第三季度未变，应收增量由N1.2承担｜限：无｜性质与把握：披露
- 任务：担N0主旨中“回款未失速”这一环
- 顺序：先立账期，再立应收
- 接前：直承N0总题
- 分担：“账期未改”→N1.1·主干｜“应收增量”→N1.2·链环｜遮住测试：遮住N1.1则应收增量无从解释｜无人担：无｜重复担：无｜子项合计仍证不出：无〔判于r2〕
- 边：无
- 展开：子节点N1.1、N1.2｜上限900字｜本单元写：部章导语

#### N1.1 账期
- **主旨**：账期条款未改｜因：甲档A档合同仍按原条款结算｜限：无｜性质与把握：披露
- 任务：担N1主旨中“账期未改”这一环
- 接前：承N1题
- 边：X02、X03
- 事实：写全 E011@甲档:L41
- 消歧：条件｜E011@甲档:L41｜“仅含合并范围内应收”→固定写法：合并口径应收｜禁写：全部应收
- 段：不拆（写全陈述<=5条、无多维比较网格、无算式或推断）

#### N1.2 应收
- **主旨**：应收增量来自赊销｜因：E012口径下赊销扩大｜限：分母为营业收入｜性质与把握：我们自算·确定
- 任务：担N1主旨中“应收增量”这一环
- 接前：因果·账期延长导致应收增加·凭：@甲档:L41
- 边：X01、X03
- 事实：写全 E012@甲档:L40、E013@甲档:L12
- 算式：应收增量＝期末应收12.0亿元@甲档:L40－期初应收9.5亿元@甲档:L38＝2.5亿元｜方向：净流向｜合并口径｜假设：期初未重述｜复算闭合值：2.5亿元｜签认：核对席·2026-11-20
- 消歧：无（六类已查）
- 段1：应收增量来自赊销｜接前：承节题｜事实：E012@甲档:L40
- 段2：增量仍小于收入增量｜接前：对照·凭：@甲档:L12｜事实：E013@甲档:L12

### N2 偿债
- **主旨**：现金覆盖短债｜因：不受限现金大于短期借款｜限：无｜性质与把握：我们自算·确定
- 任务：担N0主旨中“现金覆盖短债”这一环
- 分担：“现金大于短债”→N2.1·主干｜遮住测试：遮住N2.1则无覆盖结论｜无人担：无｜重复担：无｜子项合计仍证不出：无〔判于r2〕

#### N2.1 现金覆盖
- **主旨**：不受限现金足以覆盖短债｜因：货币资金扣除受限部分后仍大于短期借款，答Q1（见X01）｜限：无｜性质与把握：我们自算·确定
- 任务：担N2主旨
- 接前：承N2题
- 边：X01、X02
- 事实：写全 E021@甲档:L22｜回指 E012@甲档:L40（写全处N1.2）
- 算式：现金覆盖倍数＝货币资金36.0亿元@甲档:L22/短期借款30.0亿元@甲档:L30＝1.2倍｜分母：短期借款｜方向：盈余｜口径：合并口径｜复算闭合值：1.2倍｜签认：核对席·2026-11-20
- 段1：不受限现金足以覆盖短债｜接前：承节题｜事实：E021@甲档:L22
"""
GATED_SRC = """甲档（样例原件）
L40 期末应收账款12.0亿元。
L41 账期由九十天延至一百二十天，应收随之增加；本项仅含合并
    范围内应收，不含已转让部分。
"""
LIVING_GATES = [('Z-SWAP', 'N1.2', 'hard'), ('Z-SWAP', 'N2.1', 'hard'), ('Z-SHARE', 'N1', 'hard'),
                ('Z-SHARE', 'N2', 'hard'), ('Z-EDGE', 'N1.2—N2.1', 'hard'), ('Z-FACT', 'N1.2', 'hard'),
                ('Z-QUOTE-SKIP', '-', 'skip'), ('Z-SIGN', 'N1.2', 'warn'), ('Z-PARA', 'N2.1', 'hard'),
                ('Z-SIGN', 'N2.1', 'warn')]
SWAP_TABLE = [  # (slot text, [(token, kind)]) for swap_tokens
    ('N1.2与N1.10，答Q1（见X01），E012口径，S18', []), ('2025年末、2024–2025年报、2024-25', []),
    ('2026Q3前、第三季度、FY25同口径、1H25、3季度', []), ('甲档A档第2期、第3条、7号条款、12月末、2026-11-20', []),
    ('升至15%', [('15%', 'metric')]), ('覆盖1.2倍', [('1.2倍', 'metric')]), ('借款30.0亿元', [('30.0亿', 'metric')]),
    ('10年期国债', [('10年期', 'metric')]), ('利差50bp、装机3GW、2.5x', [('50bp', 'metric'), ('3GW', 'metric'),
                                                                      ('2.5x', 'metric')]),
    ('$5与USD 5亿', [('$5', 'metric'), ('USD 5亿', 'metric')]), ('翻两倍', [('两倍', 'metric')]),
    ('2000亿元', [('2000亿', 'metric')]), ('升至１５％', [('15%', 'metric')]),
    ('账期中枢45', [('45', 'bare')]), ('3年内', [('3', 'bare')])]


def gate_checks(tmp, run, check):
    """W1-O2 check-0to1: the clean GATED outline passes; one mutation per defect trips its code (positive and negative
    per gate); the W1-O1 LIVING fixture is the negative whole outline."""
    def put(name, text):
        p = os.path.join(tmp, name)
        with open(p, 'w', encoding='utf-8') as fh:
            fh.write(text)
        return p
    src = put('甲档.txt', GATED_SRC)
    srcs = ['--sources', '甲档=' + src]

    def gate(text, extra=()):
        c, o, e = run(['check-0to1', put('gate-提纲.md', text), '--json'] + list(extra))
        try:
            return c, json.loads(o), e
        except ValueError:
            return c, None, e + o

    def mut(*pairs):  # GATED with each (old, new) applied; '' when an old text is not unique (the check then fails)
        t = GATED
        for old, new in pairs:
            if t.count(old) != 1:
                return ''
            t = t.replace(old, new)
        return t

    def trips(text, want, code=2, extra=srcs, has=()):  # exactly these (code, where), exit code, why fragments
        c, f, e = gate(text, extra)
        return (c == code and f is not None and [(x['code'], x['where']) for x in f] == want
                and all(any(h in x['why'] for x in f) for h in has))

    clean = put('clean-提纲.md', GATED)
    c, f, e = gate(GATED, srcs)
    c2, o2, e2 = run(['check-0to1', clean])
    check('G1 clean living outline: check-0to1 --sources exits 0, no finding; without --sources only the quote check '
          'is reported skipped', c == 0 and f == [] and 'check-0to1: 0 hard, 0 warnings, 0 skipped' in e and c2 == 0
          and o2 == 'Z-QUOTE-SKIP -: 1 消歧 quote(s) not checked against the sources (pass --sources NAME=PATH)\n'
          and 'check-0to1: 0 hard, 0 warnings, 1 skipped' in e2)
    living = put('living-gates-提纲.md', LIVING)
    c, f, e = gate(LIVING, ())
    check('G2 the W1-O1 fixture (negative whole outline): exit 2, the ten findings in gate order, JSON keys '
          '{code, sev, where, why, line}', c == 2 and f is not None
          and [(x['code'], x['where'], x['sev']) for x in f] == LIVING_GATES
          and all(tuple(x) == FINDING_KEYS for x in f) and f[0]['line'] == LIVING.split('\n').index('#### N1.2 应收') + 1
          and 'X01 已定、X02 待据' in f[4]['why'])
    c, o, e = run(['nodes', living, '--check-0to1'])
    c3, o3, e3 = run(['nodes', clean, '--check-0to1', '--sources', '甲档=' + src])
    c4, o4, e4 = run(['nodes', clean, '--sources', '甲档=' + src])
    check('G3 nodes OUTLINE --check-0to1: node rows, then the finding lines; exit 2 on a hard finding, 0 when clean; '
          '--sources alone refused', c == 2 and o.startswith('N0\t0\t导语\n') and '\nZ-EDGE N1.2—N2.1: X01 已定、X02 待据' in o
          and o.count('\n') == 7 + 10 and c3 == 0 and o3.count('\n') == 6 and c4 == 2
          and 'goes with --check-0to1' in e4)
    got = [(t, swap_tokens(t)) for t, _ in SWAP_TABLE]
    check('G4 swap test: identifiers (ids, years, quarters, FY/H, series, clauses, months, dates) pass; metrics carry '
          'a unit or currency (full-width too); a bare number is told apart', got == SWAP_TABLE)
    check('G5 Z-SWAP: a metric in a 判断 slot (N1.2) and in N0 因 is hard; a bare number is a Z-SWAP? warning, exit 0',
          trips(mut(('**主旨**：应收增量来自赊销', '**主旨**：应收增量2.5亿元来自赊销')), [('Z-SWAP', 'N1.2')],
                has=['判断 carries the metric “2.5亿”'])
          and trips(mut(('回款节奏与FY25同口径持平', '回款增速高于5%')), [('Z-SWAP', 'N0')], has=['因 carries the metric “5%”'])
          and trips(mut(('因：甲档A档合同仍按原条款结算', '因：甲档A档合同账期中枢45')), [('Z-SWAP?', 'N1.1')], 0))
    q1d = '｜分母短期借款30.0亿元@甲档:L30，新增额不入分母'
    check('G6 Z-DENOM: a ratio 门槛 (倍) with no 分母 cell or a placeholder one is hard; a non-ratio 门槛 (Q2) needs none',
          trips(mut((q1d, '')), [('Z-DENOM', 'Q1')]) and trips(mut((q1d, '｜分母<名称与基数@原件锚点>')), [('Z-DENOM', 'Q1')]))
    check('G7 Z-Q: 删去后会答错什么 a bare 会, or no 窗口 cell, is hard',
          trips(mut(('删去后会答错什么：会把回款放缓当成坏账上升', '删去后会答错什么：会')), [('Z-Q', 'Q2')], has=['删去后会答错什么'])
          and trips(mut(('｜窗口2026年中报', '')), [('Z-Q', 'Q2')], has=['窗口 empty']))
    check('G8 Z-SHARE: a parent without 分担 (N2); 重复担 not 无 (N0); an item naming a non-child plus a child left out (N1)',
          trips(mut(('- 分担：“现金大于短债”→N2.1·主干｜遮住测试：遮住N2.1则无覆盖结论｜无人担：无｜重复担：无｜子项合计仍证不出：无'
                     '〔判于r2〕\n', '')), [('Z-SHARE', 'N2')])
          and trips(mut(('遮住N2只剩回款事实｜无人担：无｜重复担：无', '遮住N2只剩回款事实｜无人担：无｜重复担：N1与N2都担覆盖')),
                    [('Z-SHARE', 'N0')], has=['重复担 reads “N1与N2都担覆盖”'])
          and trips(mut(('“应收增量”→N1.2·链环', '“应收增量”→N2.1·链环')), [('Z-SHARE', 'N1'), ('Z-SHARE', 'N1')],
                    has=['names no child of N1', 'children N1.2 carry no 分担 item']))
    x4 = GATED_X03 + '\n| X04 | %s | %s | %s | %s | 无 | r2 |'
    check('G9 Z-EDGE: one sorted key 已定 vs 待据 refused naming both ids; same status a Z-EDGE? warning (exit 0); unknown '
          'endpoint; no status; 已定 causal 凭据 without @; causal 接前 without @',
          trips(mut((GATED_X03, x4 % ('N2.1—N1.2', '拟议因果（回款→现金）', '无连接句', '待据'))), [('Z-EDGE', 'N1.2—N2.1')],
                has=['X01 已定、X04 待据'])
          and trips(mut((GATED_X03, x4 % ('N2.1—N1.2', '铺垫与回应', 'E022@甲档:L23', '已定'))),
                    [('Z-EDGE?', 'N1.2—N2.1')], 0)
          and trips(mut((GATED_X03, x4 % ('N9—N1.2', '比较与对照', 'E022@甲档:L23', '待据'))), [('Z-EDGE', 'X04')],
                    has=['endpoint N9 has no node block'])
          and trips(mut((GATED_X03, x4 % ('N0—N2', '比较与对照', 'E022@甲档:L23', ''))), [('Z-EDGE', 'X04')],
                    has=['no status'])
          and trips(mut(('“账期由九十天延至一百二十天，应收随之增加”@甲档:L41', '甲档所述账期延长')), [('Z-EDGE', 'X03')],
                    has=['no @ anchor'])
          and trips(mut(('因果·账期延长导致应收增加·凭：@甲档:L41', '因果·账期延长导致应收增加')), [('Z-EDGE', 'N1.2')],
                    has=['接前 names a causal relation (因果)']))
    neg = ('只是并列，不写成因果或递进', '并列（非因果）', '不写“因为账期延长，所以应收增加”', '严禁写成导致', '不构成因果')
    pos = ('并列，因果·账期延长导致应收增加', '不写成递进；因为账期延长')
    check('W4a D: Z-EDGE reads a causal word under a prohibition marker in its own clause (S77 “只是并列，不写成因果或递进”, '
          'a negated quote) as no causal relation; an unnegated one, or one in the next clause, still trips',
          all(causal_word(t) is None for t in neg) and all(causal_word(t) for t in pos)
          and trips(mut(('因果·账期延长导致应收增加·凭：@甲档:L41', '段1·并列，只是并列，不写成因果或递进')), [], 0))
    check('G10 Z-FACT: one anchor 写全 in two nodes; a 回指 to an anchor written in full nowhere; a 回指 naming the wrong '
          '写全处', trips(mut(('回指 E012@甲档:L40（写全处N1.2）', '写全 E012@甲档:L40')), [('Z-FACT', 'E012')],
                         has=['写全) in N1.2、N2.1'])
          and trips(mut(('回指 E012@甲档:L40', '回指 E099@甲档:L90')), [('Z-FACT', 'N2.1')], has=['回指 E099'])
          and trips(mut(('（写全处N1.2）', '（写全处N1.1）')), [('Z-FACT', 'N2.1')], has=['names 写全处N1.1, but N1.2']))
    check('G11 Z-QUOTE with --sources: the quote found across a line break (whitespace-normalised) passes (G1); an '
          'altered quote or an anchor document not among --sources is hard; a bad --sources entry exits 2',
          trips(mut(('“仅含合并范围内应收”', '“仅含合并范围内全部应收”')), [('Z-QUOTE', 'N1.1')], has=['not a verbatim'])
          and trips(mut(('条件｜E011@甲档:L41', '条件｜E011@乙档:L41')), [('Z-QUOTE', 'N1.1')], has=['source 乙档 not given'])
          and gate(GATED, ['--sources', '甲档'])[0] == 2 and 'bad --sources entry' in gate(GATED, ['--sources', '甲档'])[2])
    check('G12 Z-PARA: an 算式 node without 段k rows; a 段 row citing 6 facts; 6 写全 facts under 段：不拆',
          trips(mut(('- 段1：应收增量来自赊销｜接前：承节题｜事实：E012@甲档:L40\n- 段2：增量仍小于收入增量｜接前：对照·凭：@甲档:L12'
                     '｜事实：E013@甲档:L12\n', '')), [('Z-PARA', 'N1.2')], has=['has no 段k row'])
          and trips(mut(('｜事实：E021@甲档:L22', '｜事实：E021@甲档:L22、E031、E032、E033、E034、E035')),
                    [('Z-PARA', 'N2.1 段1')], has=['cites 6 facts'])
          and trips(mut(('- 事实：写全 E011@甲档:L41', '- 事实：写全 E011@甲档:L41、E014、E015、E016、E017、E018')),
                    [('Z-PARA', 'N1.1')], has=['claims 段：不拆']))
    check('G13 Z-SIGN: an unsigned 算式 row is a warning only (exit 0)',
          trips(mut(('｜复算闭合值：1.2倍｜签认：核对席·2026-11-20', '｜复算闭合值：1.2倍｜签认：<席或脚本·日期>')),
                [('Z-SIGN', 'N2.1')], 0, has=['a leaf may not use its numbers']))
    c, o, e = run(['fields', clean])
    try:
        fj = json.loads(o)
    except ValueError:
        fj = {}
    check('G14 the fields contract is untouched by the gates: same top-level and node keys on the gated outline',
          c == 0 and list(fj) == FIELDS_KEYS and all(list(v) == NODE_KEYS for v in fj.get('nodes', {}).values())
          and len(fj.get('nodes', {})) == 6)


PATH_GOLDENS = [  # captured from the fix-round-3 copy (1.1.0)
    ('FIXTURE N1.1.1', ['chain', '@fixture', 'N1.1.1'], 0,
     '<!-- ancestor chain of N1.1.1, outline_slice.py {V} -->\n{U}\n\n## N0 根主旨\n- 〔标题〕样例根标题\n- 主旨（开头）：根判断。\n- 任务：答决策问题。\n\n### N1 一、外部账户\n- 任务：立排序依据。\n- 关系：和N2，是前提。\n- 顺序：在N2之前。\n\n#### N1.1 （一）零售定价\n- 任务：分渠道。\n'),
    ('BOLD N1.1.1', ['chain', '@bold', 'N1.1.1'], 0,
     '<!-- ancestor chain of N1.1.1, outline_slice.py {V} -->\n{U}\n\n## N0 根主旨\n- 〔标题〕样例根标题\n- 主旨（开头）：根判断。\n- **任务**：答决策问题。\n\n### N1 一、外部账户\n- **任务**：立排序依据。\n- **关系**：和N2，是前提。\n- **顺序：**在N2之前。\n\n#### N1.1 （一）零售定价\n- **任务**：分渠道。\n'),
    ('RULINGS N1.1.1', ['chain', '@rulings', 'N1.1.1'], 0,
     '<!-- ancestor chain of N1.1.1, outline_slice.py {V} -->\n{U}\n\n## N0：样稿\n- 主旨（开头）：根主旨。\n- 任务：答问题。\n\n## N1 导语〔段群〕\n- 〔标题〕无（导语）\n- 主旨（开头）：导语主旨一句。导语第二句。……（全文：node N1）\n- 任务：给答案。\n\n### N1.1 段群：一\n- 主旨（开头）：一。\n- 任务：一。\n- 顺序：一在前。\n'),
    ('CHAIN N1.1.1 N1.2', ['chain', '@chain', 'N1.1.1', 'N1.2'], 0,
     '<!-- ancestor chain of N1.1.1 N1.2, outline_slice.py {V} -->\n{U}\n\n## N0 根\n- 主旨（开头）：根判断第一句。根判断第二句！……（全文：node N0）\n- 任务：答决策问题。\n\n## N1 一、甲〔标题〕\n- **任务**：立排序依据。\n- 关系（对上一级）：和N0，通过排序依据，是主张与支持\n- **顺序**：甲在乙之前。\n\n### N1.1 段群：甲一\n- 主旨（开头）：甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一甲一……（全文：node N1.1）\n- 任务：分渠道。\n- 关系（对上一级）：和N1，通过分渠道，是论断与支持\n- 顺序：甲一放第一。\n'),
    ('CLOSES N1.1 (收尾 lines stay out)', ['chain', '@closes', 'N1.1'], 0,
     '<!-- ancestor chain of N1.1, outline_slice.py {V} -->\n{U}\n\n## N0 根\n- 主旨（开头）：根。\n- 任务：答问题。\n\n## N1 一、甲〔标题〕\n- **任务**：立甲。\n- **顺序**：甲在前。\n'),
    ('nodes --check CLOSES (no --closes)', ['nodes', '@closes', '--check'], 0,
     'N0\t0\t根\nN1\t1\t一、甲〔标题〕\nN1.1\t2\t段群：甲一\nN1.2\t2\t段群：甲二\nN1.3\t2\t段群：甲三\nN1.3.1\t3\t段群：甲三一\nN1.3.2\t3\t段群：甲三二\nN2\t1\t二、乙\nN2.1\t2\t段群：乙1\nN2.2\t2\t段群：乙2\nN2.3\t2\t段群：乙3\nN3\t1\t三、丙\nN3.1\t2\t段群：丙1\nN3.2\t2\t段群：丙2\nN3.3\t2\t段群：丙3\nN4\t1\t四、丁\nN4.1\t2\t段群：丁1\nN4.2\t2\t段群：丁2\nN4.3\t2\t段群：丁3\nN5\t1\t五、戊\nN5.1\t2\t段群：戊1\nN5.2\t2\t段群：戊2\nN5.3\t2\t段群：戊3\nN6\t1\t六、己\nN6.1\t2\t段群：己1\nN6.2\t2\t段群：己2\nN6.3\t2\t段群：己3\ncheck: 27 node blocks, 27 with a **主旨** line, 0 duplicate ids\n'),
]


def path_regressions(tmp, run, check, flag=('--path',), usage=None):
    """P1 byte-for-byte regressions: chain with flag (staged: --path) and nodes --check without --closes print what
    the fix-round-3 copy printed with no flag, the usage line being this version's (R13).  Run against
    that copy with flag=() and usage=<its usage line> they pass there."""
    texts = {'fixture': FIXTURE, 'bold': BOLD, 'chain': CHAIN, 'rulings': RULINGS, 'closes': CLOSES}
    paths = {}
    for name, text in texts.items():
        paths['@' + name] = os.path.join(tmp, 'rg-%s-提纲.md' % name)
        with open(paths['@' + name], 'w', encoding='utf-8') as fh:
            fh.write(text)
    for name, argv, code, want in PATH_GOLDENS:
        argv = [paths.get(x, x) for x in argv]
        c, o, e = run(argv + (list(flag) if argv[0] == 'chain' else []))
        check('P1 regression %s: byte for byte as the fix-round-3 copy (usage line aside)' % name, c == code
              and o == want.replace('{V}', VERSION).replace('{U}', usage or CHAIN_USAGE))


def new_checks(tmp, run, check):
    """The 1.1.0 assertions.  Each holds a positive part that 1.0.1 cannot print, so each fails on 1.0.1;
    run(argv) -> (exit code, stdout, stderr) may run another script (the before/after proof)."""
    paths = {}
    for name, text in (('bold', BOLD), ('chain', CHAIN)):
        paths[name] = os.path.join(tmp, name + '-提纲.md')
        with open(paths[name], 'w', encoding='utf-8') as fh:
            fh.write(text)

    def block(o, nd):  # the chain lines of one ancestor
        m = re.search(r'^#{2,6} %s(?![0-9.]).*?(?=^#{2,6} N|\Z)' % re.escape(nd), o, re.M | re.S)
        return m.group(0) if m else ''

    def counts(o):
        got = [FIELD_COUNT_RE.match(l) for l in o.splitlines()]
        return [sum(1 for m in got if m and m.group(1) == k) for k in ('任务', '顺序', '关系')]

    c, o, e = run(['view', paths['bold']])
    check('1.1 view, bold spelling: 任务/顺序/关系 lines 5/2/3, as the plain fixture', c == 0
          and counts(o) == [5, 2, 3] and '- **任务**：分渠道。' in o and '- **关系**：和N2，是前提。' in o)
    c, o, e = run(['chain', paths['bold'], 'N1.1.1', '--path'])
    check('1.1 chain, bold spelling: 任务 lines and the edge 顺序 line', c == 0 and '- **任务**：分渠道。' in o
          and '- **任务**：立排序依据。' in o and '- **顺序：**在N2之前。' in o)

    c, o, e = run(['chain', paths['chain'], 'N1.1.1', '--path'])
    lines = o.splitlines()
    check('1.1 chain: usage line right after the comment line', c == 0 and len(lines) > 1 and lines[1] == CHAIN_USAGE)
    check('1.1 chain: bold task line of an ancestor', '- **任务**：立排序依据。' in o)
    check('1.1 主旨 opening: asides cut (nested too), cut after the second sentence end, pointer',
          '- 主旨（开头）：根判断第一句。根判断第二句！……（全文：node N0）' in o and '旁注' not in o)
    check('1.1 主旨 opening: 200-character cap, pointer',
          '- 主旨（开头）：' + '甲一' * 100 + '……（全文：node N1.1）' in o)
    check('1.1 主旨 opening: only untitled ancestors (N0, N1.1), none for N1 (〔标题〕 in its heading)',
          o.count('主旨（开头）') == 2 and '主旨（开头）' not in block(o, 'N1') and '甲的主旨' not in o)
    check('1.1 关系: several clauses in one line, only the one naming the parent',
          '- 关系（对上一级）：和N0，通过排序依据，是主张与支持' in block(o, 'N1') and '和N2，通过先后' not in o)
    check('1.1 关系: one clause per line (continuation line); N1.2 is not N1',
          '- 关系（对上一级）：和N1，通过分渠道，是论断与支持' in block(o, 'N1.1') and '和N1.2，通过渠道' not in o)
    check('1.1 顺序 on an edge: first child (N1 over N1.1, N1.1.1) and only child (N1.1 over N1.1.1)',
          '- **顺序**：甲在乙之前。' in block(o, 'N1') and '- 顺序：甲一放第一。' in block(o, 'N1.1')
          and '树根' not in o)

    c, o, e = run(['chain', paths['chain'], 'N1.2', '--path'])
    check('1.1 顺序: a middle child gets no 顺序 line of its parent (关系 clause still there)', c == 0
          and '- 关系（对上一级）：和N0，通过排序依据，是主张与支持' in o and '甲在乙之前' not in o)
    c, o, e = run(['chain', paths['chain'], 'N1.3.2', '--path'])
    check('1.1 顺序: last of last, two levels up (N1 and N1.3 both print theirs)', c == 0
          and '- **顺序**：甲在乙之前。' in block(o, 'N1') and '- **顺序：**甲三放最后。' in block(o, 'N1.3'))
    check('1.1 关系: no exact parent token (N11, N1.3.1 are not N1) -> the 关系 line verbatim; short 主旨, no pointer',
          '- 关系：和N11，通过错号，是比较与对照；和N1.3.1，通过子段，是总述与展开' in block(o, 'N1.3')
          and '关系（对上一级）：和N11' not in o and '- 主旨（开头）：甲三短句。\n' in o and '甲三短句。……' not in o)
    c, o, e = run(['chain', paths['chain'], 'N1.3.1', '--path'])
    check('1.1 顺序: last then first is no edge for N1; first child is an edge for N1.3', c == 0
          and '甲在乙之前' not in o and '- **顺序：**甲三放最后。' in block(o, 'N1.3'))
    c, o, e = run(['chain', paths['chain'], 'N2.1', '--path'])
    check('1.1 K-OS-1: a 〔标题〕 line repeating the heading is dropped, and that ancestor gets no 主旨 opening',
          c == 0 and '## N2 二、乙' in o and '〔标题〕' not in o and '主旨（开头）' not in block(o, 'N2')
          and '- 主旨（开头）：根判断第一句。' in o)
    check('1.1 关系: one clause per 关系 line, the parent one kept; only child gets 顺序',
          '- 关系（对上一级）：和N0，通过收束，是归纳与综合' in o and '和N1，通过对照' not in o
          and '- 顺序：乙放最后。' in o)


def run(argv):
    """main(argv) in-process -> (exit code, stdout, stderr)."""
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        try:
            code = main(argv)
        except SystemExit as e:
            code = e.code if isinstance(e.code, int) else 2
    return code, out.getvalue(), err.getvalue()


def self_test():
    print('== outline_slice self-test %s' % VERSION)
    results = []

    def check(name, cond):
        results.append(bool(cond))
        print('%s: %s' % ('PASS' if cond else 'FAIL', name))

    with tempfile.TemporaryDirectory() as tmp:
        good = os.path.join(tmp, '样例-提纲.md')
        with open(good, 'w', encoding='utf-8') as fh:
            fh.write(FIXTURE)
        nogist = os.path.join(tmp, 'nogist-提纲.md')
        with open(nogist, 'w', encoding='utf-8') as fh:
            fh.write(FIXTURE.replace('- **主旨**：缓冲先到期。\n', ''))
        notable = os.path.join(tmp, 'notable-提纲.md')
        with open(notable, 'w', encoding='utf-8') as fh:
            fh.write(re.sub(r'\| 名字 \|.*?\n\n', '', FIXTURE, flags=re.S))
        unit = os.path.join(tmp, 'unit.md')
        with open(unit, 'w', encoding='utf-8') as fh:
            fh.write('正文写到缓冲与外部账户。\n')

        c, o, e = run(['nodes', good, '--check'])
        rows = [l.split('\t') for l in o.splitlines() if '\t' in l]
        check('nodes --check: 5 blocks = 5 主旨 lines, exit 0', c == 0 and len(rows) == 5
              and 'check: 5 node blocks, 5 with a **主旨** line, 0 duplicate ids' in o)
        check('nodes: ids, depths, heading text', [r[:2] for r in rows] == [
            ['N0', '0'], ['N1', '1'], ['N1.1', '2'], ['N1.1.1', '3'], ['N2', '1']]
            and rows[1][2] == '一、外部账户')
        c, o, e = run(['nodes', nogist, '--check'])
        check('nodes --check: block without 主旨 exits 2 and is named', c == 2 and 'N2' in e)

        c, o, e = run(['node', good, 'N2', 'N1.1'])
        check('node: verbatim blocks in document order', c == 0
              and o.index('#### N1.1 ') < o.index('### N2 ') and '- 展开：一段。' in o
              and '##### N1.1.1' not in o)
        check('node: a non-node ## section ends the tree', '开放问题' not in o and '不属于' not in o)
        c, o, e = run(['node', good, 'N1', 'N9.9'])
        check('node: unknown id exits 2', c == 2 and 'N9.9' in e and o == '')

        c, o, e = run(['chain', good, 'N1.1.1', '--path'])
        lines = o.splitlines()
        check('chain: header line', c == 0 and lines[0] == '<!-- ancestor chain of N1.1.1, outline_slice.py %s -->' % VERSION)
        heads = [l for l in lines if l.startswith('#')]
        check('chain: ancestors root first, ID excluded', heads == ['## N0 根主旨', '### N1 一、外部账户', '#### N1.1 （一）零售定价'])
        check('chain: 〔标题〕, 任务, 关系, edge 顺序 lines; no **主旨** or 展开 line', '- 任务：分渠道。' in o
              and '- 〔标题〕样例根标题' in o and '- 关系：和N2，是前提。' in o and '- 顺序：在N2之前。' in o
              and '**主旨**' not in o and o.count('主旨（开头）') == 1 and '- 主旨（开头）：根判断。\n' in o
              and '展开' not in o and '树根' not in o)
        c, o, e = run(['chain', good, 'N0'])
        check('chain: N0 has no ancestors', c == 0 and o.strip().count('\n') == 0)
        c, o, e = run(['chain', good, 'N3'])
        check('chain: unknown id exits 2', c == 2 and 'N3' in e)
        gap = os.path.join(tmp, 'gap-提纲.md')
        with open(gap, 'w', encoding='utf-8') as fh:
            fh.write(FIXTURE.replace('### N1 一、外部账户', '### X1 一、外部账户'))
        c, o, e = run(['chain', gap, 'N1.1.1'])
        check('chain: an ancestor without a block -> stderr WARNING, exit 0, the rest printed', c == 0
              and 'WARNING: ancestor N1 of N1.1.1 has no node block' in e and '#### N1.1 ' in o)

        c, o, e = run(['names', good, '--ids', 'N1'])
        check('names --ids: header, separator, matching rows', c == 0 and o.splitlines()[:2] == [
            '| 名字 | 指什么与口径 | 本篇写法 | 不许用的叫法 |', '|---|---|---|---|']
            and '| 外部账户（第一次之后）' in o and '| 缓冲 ' not in o and e.strip() == 'kept 1 of 4 rows')
        c, o, e = run(['names', good, '--ids', 'N1.1.1'])
        check('names: a 不许用 term counts', c == 0 and '| 缓冲 ' in o and e.strip() == 'kept 1 of 4 rows')
        c, o, e = run(['names', good, '--text', unit])
        check('names --text: rows found in a file', c == 0 and e.strip() == 'kept 2 of 4 rows' and '冷门词' not in o)
        c, o, e = run(['names', notable, '--ids', 'N1'])
        check('names: missing name table exits 2 with a message', c == 2 and 'no name table' in e and o == '')
        c, o, e = run(['names', good, '--ids', 'N7'])
        check('names: unknown id exits 2', c == 2 and 'N7' in e)

        c, o, e = run(['view', good])
        check('view: header line', c == 0 and o.splitlines()[0]
              == '<!-- brief view, outline_slice.py %s; the outline file stays the one home -->' % VERSION)
        check('view: heading and the five field lines, in order', o.count('**主旨**') == 5
              and '- 顺序：在N2之前。' in o and '- 关系：和N2，是前提。' in o
              and o.index('### N1 ') < o.index('#### N1.1 ') < o.index('### N2 '))
        check('view: other lines left out', '展开' not in o and '把握' not in o and '开放问题' not in o)

        c, o, e = run(['--version'])
        check('--version', c == 0 and o.strip() == VERSION)

        glued = os.path.join(tmp, 'glued-提纲.md')
        with open(glued, 'w', encoding='utf-8') as fh:
            fh.write(GLUED)
        old_ids = [m.group(2) for m in map(OLD_NODE_RE.match, GLUED.split('\n')) if m]
        check('glued ids, 1.0.0 regex: “## N1一” lost, N1.0/N1.9/N1.10 read as N1 (the defect)',
              old_ids == ['N0', 'N1', 'N1.1', 'N1', 'N1', 'N2'])
        c, o, e = run(['nodes', glued, '--check'])
        rows = [l.split('\t') for l in o.splitlines() if '\t' in l]
        check('glued ids: 7 blocks, ids and heading text cut right, --check exit 0', c == 0
              and [r[0] for r in rows] == ['N0', 'N1', 'N1.0', 'N1.1', 'N1.9', 'N1.10', 'N2']
              and rows[1][2] == '一、外部账户〔标题〕' and rows[4][2] == '收束〔段群〕'
              and rows[5][2] == '尾声' and rows[6][2] == '：二、缓冲'
              and 'check: 7 node blocks, 7 with a **主旨** line, 0 duplicate ids' in o)
        c, o, e = run(['node', glued, 'N1.9'])
        check('glued ids: node N1.9 is its own block', c == 0 and o == '### N1.9收束〔段群〕\n\n- **主旨**：收束。\n')
        c, o, e = run(['chain', glued, 'N1.10'])
        check('glued ids: chain of N1.10 = N0, N1', c == 0
              and [l for l in o.splitlines() if l.startswith('#')] == ['## N0 根〔段群〕', '## N1一、外部账户〔标题〕'])

        new_checks(tmp, run, check)
        ruling_checks(tmp, run, check)
        unit_checks(tmp, run, check)
        wave2_checks(tmp, run, check)
        path_regressions(tmp, run, check)
        fix_checks(tmp, run, check)
        living_checks(tmp, run, check)
        gate_checks(tmp, run, check)

    ok = all(results)
    print('outline_slice self-test: %s (%d checks)' % ('PASS' if ok else 'FAIL', len(results)))
    return 0 if ok else 1


# ------------------------------------------------------------------ main
def main(argv=None):
    for s in (sys.stdout, sys.stderr):
        if hasattr(s, 'reconfigure'):
            s.reconfigure(encoding='utf-8')
    ap = argparse.ArgumentParser(
        prog='outline_slice.py',
        description='Slice a FICC outline (FICCOutline.md 4.2) by node id; output goes to stdout.')
    ap.add_argument('--version', action='version', version=VERSION)
    ap.add_argument('--self-test', '--selftest', action='store_true', help='run the built-in fixture tests')
    sub = ap.add_subparsers(dest='cmd')
    p = sub.add_parser('nodes', help='list id, depth, heading text')
    p.add_argument('outline')
    p.add_argument('--check', action='store_true', help='exit 2 if a node block lacks a **主旨** line')
    p.add_argument('--closes', action='store_true', help='implies --check; exit 2 if a node with three or '
                   'more children has no readable 收尾 line naming a descendant with a block, or 不设')
    p.add_argument('--check-0to1', action='store_true', help='also run the pre-prose gates (as check-0to1)')
    p.add_argument('--sources', nargs='+', action='append', metavar='NAME=PATH', help='with --check-0to1')
    p = sub.add_parser('node', help='print node blocks verbatim, in document order')
    p.add_argument('outline')
    p.add_argument('ids', nargs='+', metavar='ID')
    p = sub.add_parser('chain', help='ancestor chain of a node or a unit of nodes (default: heading, 〔标题〕, '
                                     '任务; --path adds the usage line, 主旨 opening, 关系 to its parent, edge '
                                     '顺序); 收尾 duty line in every mode')
    p.add_argument('outline')
    p.add_argument('ids', nargs='+', metavar='ID')
    p.add_argument('--path', nargs='?', const=0, default=None, type=path_n, metavar='N',
                   help='path-to-root content; N (>= 1) keeps the nearest N ancestors of each id')
    p = sub.add_parser('names', help='name-table rows used by node blocks or files')
    p.add_argument('outline')
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument('--ids', nargs='+', metavar='ID')
    g.add_argument('--text', nargs='+', metavar='FILE')
    p = sub.add_parser('view', help='brief view of every node')
    p.add_argument('outline')
    p = sub.add_parser('fields', help='the living outline as JSON: tree head (revisions, card, edges, renumber) and '
                                      'the slot fields of every node, or of the ids given')
    p.add_argument('outline')
    p.add_argument('ids', nargs='*', metavar='ID')
    p = sub.add_parser('check-0to1', help='pre-prose gates on the living outline (FICCOutline.md §9, FICCStructure.md §7): Z-SWAP Z-DENOM Z-Q '
                                          'Z-SHARE Z-EDGE Z-FACT Z-QUOTE Z-PARA Z-SIGN; exit 2 on a hard finding')
    p.add_argument('outline')
    p.add_argument('--sources', nargs='+', action='append', metavar='NAME=PATH',
                   help='source files by anchor document name, for the 消歧 quote check')
    p.add_argument('--json', action='store_true', help='findings as a JSON list of {code, sev, where, why, line}')
    a = ap.parse_args(argv)
    if a.self_test:
        return self_test()
    if not a.cmd:
        ap.print_usage(sys.stderr)
        return 2
    try:
        return {'nodes': cmd_nodes, 'node': cmd_node, 'chain': cmd_chain,
                'names': cmd_names, 'view': cmd_view, 'fields': cmd_fields,
                'check-0to1': cmd_check0}[a.cmd](a, sys.stdout)
    except SliceError as e:
        print('outline_slice.py: %s' % e, file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
