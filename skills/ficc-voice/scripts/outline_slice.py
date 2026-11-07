#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""outline_slice.py (2026-10-25; 1.0.1 2026-11-05) -- slice a FICC outline (<文稿名>-提纲.md) by node id.

Outline format: FICCOutline.md 4.2; node ids N-prefixed, dotted, positional (N0 is the root,
N3.1 sits under N3).  The outline file stays the one home: every slice is printed to stdout
and nothing is written back.  Standard library only; parsing adapted from kit-1.2.0
(kitlib.node_blocks) and voice_check.py (name table).  Node headings are read with
cjk_ids.NODE_HEADING_RE (same directory, required): the id may be glued to the heading text
("## N1一、…", "### N1.9总起"); 1.0.0 used `\b` there, which cut "N1.9总起" to N1 and dropped
"## N1一、…" (1104 draft task: 81 of 91 nodes found).

Usage:
  outline_slice.py nodes OUTLINE [--check]      id, depth, heading text per node block;
                                                --check exits 2 when a block lacks a **主旨** line
  outline_slice.py node OUTLINE ID [ID ...]     those node blocks verbatim, in document order
  outline_slice.py chain OUTLINE ID             ancestors of ID (root first, ID excluded): heading,
                                                〔标题〕 and 任务： lines
  outline_slice.py names OUTLINE (--ids ID ... | --text FILE ...)
                                                name-table header + the rows whose terms occur in
                                                those node blocks or files; 'kept K of N rows' on stderr
  outline_slice.py view OUTLINE                 brief view: heading, 〔标题〕, **主旨**, 任务：, 顺序：,
                                                关系： lines of every node
  outline_slice.py --self-test                  synthetic fixture, assertions for every subcommand
                                                (--selftest is an alias, K-OS-2)
  outline_slice.py --version

Exit codes: 0 ok; 2 unknown id, a node block without a **主旨** line (nodes --check), duplicate
node ids (nodes --check), no name table (names), unreadable file; 1 a failed self-test.
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

VERSION = '1.0.1'
NODE_RE = cjk_ids.NODE_HEADING_RE
TREE_END_RE = re.compile(r'^#{1,2}\s+(?!N\d)')          # a non-node '#'/'##' heading ends the tree
FIELD_RE = r'^\s*(?:[-*+]\s+)?'
GIST_RE = re.compile(FIELD_RE + r'\*\*主旨(?:\*\*|：\*\*)')
TITLE_RE = re.compile(FIELD_RE + r'〔标题〕')
TASK_RE = re.compile(FIELD_RE + r'任务[：:]')
VIEW_RE = re.compile(FIELD_RE + r'(?:〔标题〕|\*\*主旨(?:\*\*|：\*\*)|任务[：:]|顺序[：:]|关系[：:])')
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
    if not a.check:
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
    return 2 if missing or dup else 0


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


def cmd_chain(a, out):
    idx = index(node_blocks(read(a.outline)))
    require(idx, [a.id])
    parts = []
    for nd in ancestors(a.id):
        if nd not in idx:
            print('WARNING: ancestor %s of %s has no node block' % (nd, a.id), file=sys.stderr)
            continue
        lines = idx[nd][1]
        parts.append('\n'.join([lines[0]] + [l for l in lines[1:] if TITLE_RE.match(l) or TASK_RE.match(l)]))
    out.write('<!-- ancestor chain of %s, outline_slice.py %s -->\n' % (a.id, VERSION))
    if parts:
        out.write('\n\n'.join(parts) + '\n')
    return 0


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

        c, o, e = run(['chain', good, 'N1.1.1'])
        lines = o.splitlines()
        check('chain: header line', c == 0 and lines[0] == '<!-- ancestor chain of N1.1.1, outline_slice.py %s -->' % VERSION)
        heads = [l for l in lines if l.startswith('#')]
        check('chain: ancestors root first, ID excluded', heads == ['## N0 根主旨', '### N1 一、外部账户', '#### N1.1 （一）零售定价'])
        check('chain: only 〔标题〕 and 任务： lines', '- 任务：分渠道。' in o and '- 〔标题〕样例根标题' in o
              and '**主旨**' not in o and '顺序' not in o and '展开' not in o)
        c, o, e = run(['chain', good, 'N0'])
        check('chain: N0 has no ancestors', c == 0 and o.strip().count('\n') == 0)
        c, o, e = run(['chain', good, 'N3'])
        check('chain: unknown id exits 2', c == 2 and 'N3' in e)

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
    p = sub.add_parser('node', help='print node blocks verbatim, in document order')
    p.add_argument('outline')
    p.add_argument('ids', nargs='+', metavar='ID')
    p = sub.add_parser('chain', help='ancestor chain of a node (heading, 〔标题〕, 任务： lines)')
    p.add_argument('outline')
    p.add_argument('id', metavar='ID')
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
