#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""outline_slice.py (2026-10-25; 1.0.1 2026-11-05; 1.1.0 2026-11-11) -- slice a FICC outline (<文稿名>-提纲.md) by node id.

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
                                                '- 收尾（本单元写；照 FICCCompose C17：…）：<text>' at the end
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
  outline_slice.py --self-test                  synthetic fixture, assertions for every subcommand
                                                (--selftest is an alias, K-OS-2)
  outline_slice.py --version

Exit codes: 0 ok; 2 unknown id, a node block without a **主旨** line (nodes --check), duplicate
node ids (nodes --check), a close finding (nodes --closes), N after --path not an integer >= 1,
no name table (names), unreadable file; 1 a failed self-test.
"""
import argparse
import contextlib
import io
import os
import re
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cjk_ids  # noqa: E402  (sibling module; the one home of the id patterns)

VERSION = '1.1.0'
NODE_RE = cjk_ids.NODE_HEADING_RE
TREE_END_RE = re.compile(r'^#{1,2}\s+(?!N\d)')          # a non-node '#'/'##' heading ends the tree
FIELD_RE = r'^\s*(?:[-*+]\s+)?'
FIELD_LABELS = ('任务', '顺序', '关系', '标注', '展开', '收尾')
ID_CORE = r'N\d+(?:\.\d+)*'
ID_END = r'(?![A-Za-z0-9_]|\.[A-Za-z0-9_])'          # R6: a whole token (N1.3X, N1.3.abc, N1.3e2, N1X are not ids)


def field_label(label):
    """Unanchored pattern for one field label in either spelling: '任务：', '**任务**：', '**任务：**'
    (full-width or ASCII colon).  The one home of the field spellings (1.1.0, K-OS-1 wave)."""
    lab = re.escape(label)
    return r'(?:\*\*%s(?:\*\*\s*[：:]|[：:]\*\*)|%s[：:])' % (lab, lab)


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
CLOSE_DUTY = '- 收尾（本单元写；照 FICCCompose C17：收拢已立的判断并往前一步，不换说法重申主旨）：'   # R12
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


def node_blocks(text):
    """[(id, heading text, [lines])] in document order, as kitlib.node_blocks (trailing blanks cut)."""
    blocks, cur = [], None
    for line in text.split('\n'):
        m = NODE_RE.match(line)
        if m:
            cur = (m.group(2), m.group(3).strip(), [line])
            blocks.append(cur)
        elif cur is not None:
            if TREE_END_RE.match(line):
                cur = None
                continue
            cur[2].append(line)
    for _, _, lines in blocks:
        while lines and not lines[-1].strip():
            lines.pop()
    return blocks


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
    blocks = node_blocks(read(a.outline))
    for nd, head, _ in blocks:
        out.write('%s\t%d\t%s\n' % (nd, depth(nd), head))
    if not (a.check or a.closes):
        return 0
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


def relation_lines(body):
    """The node's 关系 lines with their continuation lines (deeper indent, or a bare '和N…' line), verbatim.
    A placeholder entry (no text after the label, continuation included, or text starting with 待回填) is
    left out (T0 ruling R2, 2026-11-11)."""
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
            out += entry
    return out


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
    check('R12 the duty label carries the C17 clause', '\n- 收尾（本单元写；照 FICCCompose C17：收拢已立的判断并往前一步，'
          '不换说法重申主旨）：N4.2；' in o5)
    lines = o1.splitlines()
    check('R13 the --path usage line says the chain is read-only background except the 收尾（本单元写…） line',
          len(lines) > 1 and lines[1] == CHAIN_USAGE and '“收尾（本单元写…）”一行除外' in lines[1])


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
    a = ap.parse_args(argv)
    if a.self_test:
        return self_test()
    if not a.cmd:
        ap.print_usage(sys.stderr)
        return 2
    try:
        return {'nodes': cmd_nodes, 'node': cmd_node, 'chain': cmd_chain,
                'names': cmd_names, 'view': cmd_view}[a.cmd](a, sys.stdout)
    except SliceError as e:
        print('outline_slice.py: %s' % e, file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
