#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""findings_map.py (1.0.0, 2026-11-05) -- route check findings to outline nodes by draft line number.

Generalises a findings-mapping script of the 1105AIHouse task, whose r'\\bL(\\d{1,4})\\b' missed
"L383仍写" and took source line numbers ("1104 L1026") for draft lines: 10 nodes and 12 rows
on N0 instead of 18 nodes.  Ids are read with cjk_ids (no `\\b`), source references are stripped
first (cjk_ids.strip_source_refs: 1027／1104／提纲／账本／本篇 L…, 顿号 chains and ranges).

Inputs: the assembled draft (DRAFT), its outline (OUTLINE), the findings file (FINDINGS), an
optional ruling text (--ruling FILE, one line per node section).

1. Draft headings (level 2+, outside ``` fences) must equal, in level, text and order, the
   headings of the outline nodes that have one (heading_list.headings: 〔标题〕 mark or 〔标题〕
   line), minus the nodes named with --skip (meant to be absent, e.g. a source list the draft
   leaves out).  A draft heading with no equal outline heading, an outline heading missing
   from the draft, a count or an order difference: exit 2, every misfit named, no output
   (Codex review #07: never route findings by position alone).  --map prints the alignment.
   Lines before the first heading belong to N0 (the lead).
2. A node without its own heading (〔段群〕, 〔段落〕 with no 〔标题〕 line, N0's children) whose
   nearest aligned predecessor in outline order is its ancestor sits in that node's text and
   gets the same findings (N9.1 -> N9.1.1).  Other headless nodes have no place (stderr).
3. Finding rows: Markdown table rows with a cell matching --cell-re (default: a cell starting
   with open or new, or a cell that is exactly delta).  A row whose first cell is a unit id
   with its line in brackets (s0028（L9）) counts only that bracket; any other row counts every
   L-number left after stripping source references.
4. A line number on a heading line counts for that node when the node has body text in the
   draft; on a heading-only node (e.g. a part with no opening paragraph) it goes to the section
   "标题行" for the outline agent (〔标题〕 lines, FICCOutline O81); --no-heading-to-outliner
   counts it for the node (T0 ruling 2026-11-05: --heading-to-outliner, on by default).
   Rows with no draft line go to "未定位"; lines past the end are reported.

Output (stdout or --out): '# 发现按节点（FINDINGS name；…）', the 标题行 and 未定位 sections
(## headings, before the nodes, so a packer that cuts at '### ' never swallows them), then one
'### <id>' section per node in outline order: the ruling line, then '- <row>' lines (cut to
--max-chars, default 600; 0 = whole row).  stderr: per-node row counts.

Usage:
  findings_map.py DRAFT OUTLINE FINDINGS [--ruling FILE] [--out FILE] [--skip ID ...]
                  [--cell-re RE] [--source-prefix RE ...] [--no-heading-to-outliner]
                  [--max-chars N] [--map] [--expect FILE]
      --expect FILE: compare the node set with the '### N…' headings of FILE (an earlier
      by-node file); exit 1 when they differ
  findings_map.py --selftest
  findings_map.py --version

Exit codes: 0 ok; 1 --expect mismatch or failed self-test; 2 unreadable input, headings that
do not align (named), an unknown --skip id, bad --cell-re.  Standard library only; Python 3.9.
"""
import argparse
import collections
import contextlib
import io
import os
import re
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cjk_ids  # noqa: E402
import heading_list  # noqa: E402
import outline_slice  # noqa: E402

VERSION = '1.0.0'
DEFAULT_CELL_RE = r'^(?:open|new)(?![A-Za-z])|^delta$'
UNIT_CELL_RE = re.compile(r'^s[0-9]+\s*[（(]([^）)]*)[）)]$')
DRAFT_HEAD_RE = re.compile(r'^(#{2,6})\s+(.*?)\s*$')
EXPECT_RE = re.compile(r'^###\s+(' + cjk_ids.NODE_ID + r')\s*$', re.M)


class MapError(Exception):
    """exit 2 with the message"""


def cells(row):
    return outline_slice.cells(row)


def node_key(nd):
    return [int(x) for x in nd[1:].split('.')]


def draft_headings(lines):
    out, fence = [], False
    for i, ln in enumerate(lines, 1):
        if ln.lstrip().startswith('```'):
            fence = not fence
            continue
        m = None if fence else DRAFT_HEAD_RE.match(ln)
        if m:
            out.append((i, m.group(1), m.group(2)))
    return out


def align(outline_text, dheads, skip=()):
    """Draft headings must equal the outline headings (minus skip) in level, text and order.
    -> (pairs [(line, node)], warnings (none), all node ids in order, aligned set);
    MapError naming every misfit."""
    allh = heading_list.headings(outline_text)
    have = {nd for nd, _, _ in allh}
    unknown = [nd for nd in skip if nd not in have]
    if unknown:
        raise MapError('--skip %s: no outline heading with that id' % ', '.join(unknown))
    oheads = [h for h in allh if h[0] not in skip]
    all_ids = [nd for nd, _, _ in outline_slice.node_blocks(outline_text)]
    want = collections.Counter((h, t) for _, h, t in oheads)
    got = collections.Counter((h, t) for _, h, t in dheads)
    errs = []
    for ln, h, t in dheads:
        if (h, t) not in want:
            errs.append('draft heading L%d “%s %s” matches no outline heading (same level and text)' % (ln, h, t))
    for nd, h, t in oheads:
        if (h, t) not in got:
            errs.append('outline heading %s “%s %s” is missing from the draft (--skip %s if it is meant '
                        'to be absent)' % (nd, h, t, nd))
    for key in sorted(set(want) & set(got)):
        if want[key] != got[key]:
            errs.append('heading “%s %s”: %d in the outline, %d in the draft' % (key[0], key[1], want[key], got[key]))
    if not errs:
        for (ln, h, t), (nd, oh, ot) in zip(dheads, oheads):
            if (h, t) != (oh, ot):
                errs.append('order differs: draft heading L%d “%s %s” stands where the outline has %s “%s %s”'
                            % (ln, h, t, nd, oh, ot))
                break
    if errs:
        raise MapError('draft headings do not align with the outline; nothing written:\n  ' + '\n  '.join(errs))
    pairs = [(ln, nd) for (ln, _, _), (nd, _, _) in zip(dheads, oheads)]
    return pairs, [], all_ids, {nd for _, nd in pairs}


def hosts(all_ids, aligned, lead):
    """{headless node: host node}; nodes with no host listed separately."""
    host, homeless, last = {}, [], lead
    for nd in all_ids:
        if nd in aligned:
            last = nd
            continue
        if nd == lead:
            continue
        if last is not None and last in outline_slice.ancestors(nd):
            host[nd] = last
        else:
            homeless.append(nd)
    return host, homeless


def map_findings(draft, outline_text, findings, ruling=None, skip=(), cell_re=DEFAULT_CELL_RE,
                 prefixes=None, heading_to_outliner=True, max_chars=600, title=None):
    """-> (markdown text, {node: [rows]}, report lines for stderr)."""
    lines = draft.split('\n')
    if lines and lines[-1] == '':
        lines = lines[:-1]
    dheads = draft_headings(lines)
    pairs, warns, all_ids, aligned = align(outline_text, dheads, skip)
    lead = 'N0' if 'N0' in all_ids else None
    host, homeless = hosts(all_ids, aligned, lead)
    co = collections.defaultdict(list)
    for nd, h in host.items():
        co[h].append(nd)
    line_node, head_lines, cur, starts = {}, {}, lead, dict(pairs)
    for i in range(1, len(lines) + 1):
        if i in starts:
            cur = starts[i]
        line_node[i] = cur
    for idx, (ln, nd) in enumerate(pairs):
        nxt = pairs[idx + 1][0] if idx + 1 < len(pairs) else len(lines) + 1
        body = any(lines[k - 1].strip() for k in range(ln + 1, nxt))
        head_lines[ln] = (nd, body)
    try:
        sel = re.compile(cell_re)
    except re.error as e:
        raise MapError('bad --cell-re: %s' % e)
    by = collections.defaultdict(list)
    heads_out, unplaced, report = [], [], []
    for row in findings.split('\n'):
        if not row.startswith('|'):
            continue
        cs = cells(row)
        if not any(sel.search(c) for c in cs):
            continue
        cut = row if not max_chars else row[:max_chars]
        um = UNIT_CELL_RE.match(cs[0]) if cs else None
        refs = cjk_ids.find_lines(um.group(1)) if um else cjk_ids.line_refs(row, prefixes)
        ns, routed = set(), False
        for x in refs:
            if x not in line_node:
                report.append('L%d is past the end of the draft (%d lines): %s' % (x, len(lines), cs[0]))
                continue
            if x in head_lines:
                nd, body = head_lines[x]
                if heading_to_outliner and not body:
                    heads_out.append('- %s L%d: %s' % (nd, x, cut))
                    routed = True
                    continue
            nd = line_node[x]
            if nd is None:
                report.append('L%d lies before the first heading and the outline has no N0: %s' % (x, cs[0]))
                continue
            ns.add(nd)
            ns.update(co.get(nd, []))
        if not ns and not routed:
            unplaced.append('- ' + cut)
        for nd in ns:
            by[nd].append(cut)
    order = {nd: k for k, nd in enumerate(all_ids)}
    rule = ' '.join(ruling.split()) if ruling else None
    out = ['# 发现按节点（%s；按组装稿行号映射，来源行号已剔除；findings_map.py %s）' % (title or 'findings', VERSION), '']
    if heads_out:
        out += ['## 标题行（只有标题、没有正文的节点：交提纲席改〔标题〕，FICCOutline O81）'] + heads_out + ['']
    if unplaced:
        out += ['## 未定位（行里没有本稿行号）'] + unplaced + ['']
    for nd in sorted(by, key=lambda n: order.get(n, len(order))):
        out.append('### %s' % nd)
        if rule:
            out.append(rule)
        out += ['- %s' % r for r in by[nd]]
        out.append('')
    report = ['WARNING: ' + w for w in warns] + report
    if homeless:
        report.append('outline nodes with no place in the draft: %s' % ', '.join(homeless))
    report.append('nodes %d, rows %d, heading-only refs %d, unplaced %d: %s' % (
        len(by), sum(len(v) for v in by.values()), len(heads_out), len(unplaced),
        ', '.join('%s=%d' % (n, len(by[n])) for n in sorted(by, key=lambda n: order.get(n, 0)))))
    return '\n'.join(out), dict(by), report, pairs, warns


# ------------------------------------------------------------------ self-test
OUTLINE = """# 样例-提纲

## N0：导语〔段群〕

- 〔标题〕无（导语）
- **主旨**：根。

## N1：一〔部〕

- 〔标题〕一、部名
- **主旨**：一（不设开头段）。

### N1.1：（一）〔段落〕

- 〔标题〕（一）甲
- **主旨**：甲。

#### N1.1.1：〔段落〕不另设小标题

- **主旨**：接甲。

## N2：二〔部〕

- 〔标题〕二、部名
- **主旨**：二。

### N2.1：（一）〔段落〕

- 〔标题〕（一）乙
- **主旨**：乙。

## N3：出处清单〔不计篇幅〕

- 〔标题〕出处
- **主旨**：出处。
"""
DRAFT = '\n'.join([
    '# 样例稿',           # 1
    '',                   # 2
    '导语一段。',          # 3
    '',                   # 4
    '## 一、部名',         # 5  heading-only node N1
    '',                   # 6
    '### （一）甲',        # 7
    '',                   # 8
    '甲的正文，N1.1.1接在这里。',  # 9
    '',                   # 10
    '## 二、部名',         # 11
    '',                   # 12
    '二的开头段。',        # 13
    '',                   # 14
    '### （一）乙',        # 15
    '',                   # 16
    '乙的正文。',          # 17
]) + '\n'
FINDINGS = """# 复核

| 编号 | 处置 | 依据 | 标签 |
|---|---|---|---|
| A01 | open | L9仍写“甲”，1104 L1026、L1030另说 | fix |
| A02 | resolved | L13 | — |
| A03 | open，另有新A（N1） | 第一部分标题L5仍旧，本篇L17另有 | fix（标题要提纲席改〔标题〕） |
| A04 | open | 第二部分标题L11仍旧，首句L13 | fix |
| A05 | open | 无行号 | fix |
| A06 | new | 导语L3、提纲L148、L164 | fix |
| A07 | open | L99 | fix |

| unit_id | finding_id | class | evidence |
|---|---|---|---|
| s0001（L17） | N1 | delta | 1027 L3、1104 L9；draft L15 |
| s0002（L3） | — | ok | L9 |
"""
RULING = """**裁定**（T0）：只改本节点里点名的句子。
行号是组装稿的行。"""


def run(argv):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        try:
            code = main(argv)
        except SystemExit as e:
            code = e.code if isinstance(e.code, int) else 2
    return code, out.getvalue(), err.getvalue()


def self_test():
    print('== findings_map self-test %s' % VERSION)
    results = []

    def check(name, cond):
        results.append(bool(cond))
        print('%s: %s' % ('PASS' if cond else 'FAIL', name))

    old = re.compile(r'\bL(\d{1,4})\b')
    check('map_findings2 regex: “L9仍写”, “L1030另说” missed, source “1104 L1026” read (the defect)',
          old.findall('| A01 | open | L9仍写“甲”，1104 L1026、L1030另说 |') == ['1026'])
    with tempfile.TemporaryDirectory() as tmp:
        paths = {}
        for name, body in (('draft.md', DRAFT), ('样例-提纲.md', OUTLINE), ('recheck.md', FINDINGS),
                           ('ruling.txt', RULING)):
            paths[name] = os.path.join(tmp, name)
            with open(paths[name], 'w', encoding='utf-8') as fh:
                fh.write(body)
        plain = [paths['draft.md'], paths['样例-提纲.md'], paths['recheck.md']]
        base = plain + ['--skip', 'N3']
        c, o, e = run(base + ['--ruling', paths['ruling.txt'], '--map'])
        secs = re.findall(r'^### (\S+)$', o, re.M)
        check('node sections in outline order: N0, N1.1 + co-delivered N1.1.1, N2, N2.1',
              c == 0 and secs == ['N0', 'N1.1', 'N1.1.1', 'N2', 'N2.1'])
        sec = {s.split('\n')[0]: s for s in re.split(r'^### ', o, flags=re.M)[1:]}
        check('A01: L9 -> N1.1 (and N1.1.1); 1104 L1026、L1030 stripped',
              '| A01 |' in sec['N1.1'] and '| A01 |' in sec['N1.1.1'] and '| A01 |' not in sec['N2'])
        check('A02 resolved and s0002 ok rows are not selected', '| A02 |' not in o and 's0002' not in o)
        check('A03: heading line of heading-only N1 -> 标题行 section; 本篇L17 stripped',
              '- N1 L5: | A03 |' in o and '| A03 |' not in sec.get('N2.1', '') and 'N1' not in secs)
        check('A04: heading line of N2 (has body) counts for N2, L13 too', '| A04 |' in sec['N2']
              and '- N2 L11' not in o)
        check('A05: no draft line -> 未定位', '## 未定位' in o and '- | A05 |' in o.split('## 未定位')[1].split('###')[0])
        check('A06: 导语L3 -> N0; 提纲L148、L164 stripped', '| A06 |' in sec['N0'])
        check('A07: L99 past the end is reported, row 未定位', 'L99 is past the end' in e and '- | A07 |' in o)
        check('s0001（L17）: only the bracket counts -> N2.1, not N0/N1.1', '| s0001（L17）' in sec['N2.1']
              and 's0001' not in sec['N0'] and 's0001' not in sec['N1.1'])
        check('ruling: one line under every node heading', all(
            s.split('\n')[1] == '**裁定**（T0）：只改本节点里点名的句子。 行号是组装稿的行。' for s in sec.values()))
        check('--map: alignment on stderr', 'L5 ## N1' in e and 'L15 ### N2.1' in e)
        check('--skip N3: N3 named as having no place in the draft', 'no place in the draft: N3' in e)
        c2, o2, e2 = run(base + ['--no-heading-to-outliner'])
        check('--no-heading-to-outliner: A03 goes to N1, no 标题行 section', c2 == 0 and '### N1\n' in o2
              and '## 标题行' not in o2)
        exp = os.path.join(tmp, 'expect.md')
        with open(exp, 'w', encoding='utf-8') as fh:
            fh.write(o)
        c3, o3, e3 = run(base + ['--expect', exp])
        check('--expect: same node set exits 0', c3 == 0 and 'expect: same node set (5 nodes)' in e3)
        with open(exp, 'w', encoding='utf-8') as fh:
            fh.write(o.replace('### N2.1', '### N2.9'))
        c4, o4, e4 = run(base + ['--expect', exp])
        check('--expect: different node set exits 1 and names both sides', c4 == 1
              and 'only here: N2.1' in e4 and 'only in expect: N2.9' in e4)
        def variant(name, text, extra=('--skip', 'N3'), outline=None):
            vp = os.path.join(tmp, name)
            with open(vp, 'w', encoding='utf-8') as fh:
                fh.write(text)
            return run([vp, outline or paths['样例-提纲.md'], paths['recheck.md']] + list(extra))

        c5, o5, e5 = variant('extra.md', DRAFT + '\n#### 多出来的四级标题\n')
        check('#07: a draft heading with no equal outline heading exits 2, named, nothing written',
              c5 == 2 and o5 == '' and 'L19 “#### 多出来的四级标题” matches no outline heading' in e5)
        c5, o5, e5 = variant('nosk.md', DRAFT, extra=())
        check('#07: an outline heading missing from the draft (N3, no --skip) exits 2, named',
              c5 == 2 and o5 == '' and 'outline heading N3 “## 出处” is missing from the draft' in e5)
        c5, o5, e5 = variant('text.md', DRAFT.replace('### （一）乙\n', '### （一）乙改\n'))
        check('#07: a changed heading text exits 2, both sides named', c5 == 2 and o5 == ''
              and 'L15 “### （一）乙改” matches no outline heading' in e5
              and 'outline heading N2.1 “### （一）乙” is missing' in e5)
        swapped = DRAFT.replace('## 一、部名', '## @').replace('## 二、部名', '## 一、部名').replace('## @', '## 二、部名')
        c5, o5, e5 = variant('order.md', swapped)
        check('#07: same headings in another order exits 2', c5 == 2 and 'order differs: draft heading L5' in e5)
        c5, o5, e5 = variant('skip.md', DRAFT, extra=('--skip', 'N3', 'N9'))
        check('#07: --skip of an unknown id exits 2', c5 == 2 and '--skip N9' in e5)
        codex_outline = ('## N0：导语〔段群〕\n\n- 〔标题〕无（导语）\n- **主旨**：根。\n\n'
                         '## N1：一〔部〕\n\n- 〔标题〕一、甲部\n- **主旨**：甲。\n\n'
                         '## N2：二〔部〕\n\n- 〔标题〕二、乙部\n- **主旨**：乙。\n')
        op = os.path.join(tmp, 'codex-提纲.md')
        with open(op, 'w', encoding='utf-8') as fh:
            fh.write(codex_outline)
        c5, o5, e5 = variant('codex.md', '# 稿\n\n导语。\n\n## 二、乙部\n\n乙的正文，L5这一处要改。\n',
                             extra=(), outline=op)
        check('#07 (Codex sample): outline N1, N2, draft keeps only N2 -> exit 2 naming N1, no ### N1',
              c5 == 2 and o5 == '' and 'outline heading N1 “## 一、甲部” is missing from the draft' in e5)
        c6, o6, e6 = run(base + ['--cell-re', '('])
        check('bad --cell-re exits 2', c6 == 2 and 'bad --cell-re' in e6)
    ok = all(results)
    print('findings_map self-test: %s (%d checks)' % ('PASS' if ok else 'FAIL', len(results)))
    return 0 if ok else 1


def main(argv=None):
    for s in (sys.stdout, sys.stderr):
        if hasattr(s, 'reconfigure'):
            s.reconfigure(encoding='utf-8')
    ap = argparse.ArgumentParser(prog='findings_map.py',
                                 description='Route finding rows to outline nodes by assembled-draft line number.')
    ap.add_argument('--version', action='version', version=VERSION)
    ap.add_argument('--selftest', '--self-test', action='store_true')
    ap.add_argument('draft', nargs='?')
    ap.add_argument('outline', nargs='?')
    ap.add_argument('findings', nargs='?')
    ap.add_argument('--ruling')
    ap.add_argument('--out')
    ap.add_argument('--skip', nargs='+', default=[], metavar='ID')
    ap.add_argument('--cell-re', default=DEFAULT_CELL_RE)
    ap.add_argument('--source-prefix', action='append', metavar='RE',
                    help='replaces the default source prefixes (four digits, 提纲, 账本, 本篇); repeatable')
    ap.add_argument('--heading-to-outliner', dest='heading_to_outliner', action='store_true', default=True,
                    help='a line number on the heading of a heading-only node goes to the 标题行 section (default)')
    ap.add_argument('--no-heading-to-outliner', dest='heading_to_outliner', action='store_false',
                    help='count it for the node instead')
    ap.add_argument('--max-chars', type=int, default=600)
    ap.add_argument('--map', action='store_true', help='print the heading alignment on stderr')
    ap.add_argument('--expect', metavar='FILE')
    a = ap.parse_args(argv)
    if a.selftest:
        return self_test()
    if not (a.draft and a.outline and a.findings):
        ap.print_usage(sys.stderr)
        return 2
    try:
        draft = outline_slice.read(a.draft)
        otext = outline_slice.read(a.outline)
        ftext = outline_slice.read(a.findings)
        ruling = outline_slice.read(a.ruling) if a.ruling else None
        expect = outline_slice.read(a.expect) if a.expect else None
        text, by, report, pairs, _ = map_findings(
            draft, otext, ftext, ruling, a.skip, a.cell_re, a.source_prefix, a.heading_to_outliner,
            a.max_chars, os.path.basename(a.findings))
    except (outline_slice.SliceError, MapError) as e:
        print('findings_map.py: %s' % e, file=sys.stderr)
        return 2
    if a.map:
        dl = draft.split('\n')
        for ln, nd in pairs:
            print('L%d %s %s' % (ln, dl[ln - 1].split(' ', 1)[0], nd), file=sys.stderr)
    for r in report:
        print(r, file=sys.stderr)
    if a.out:
        with open(a.out, 'w', encoding='utf-8') as fh:
            fh.write(text + '\n')
    else:
        sys.stdout.write(text + '\n')
    if expect is not None:
        want, got = set(EXPECT_RE.findall(expect)), set(by)
        if want == got:
            print('expect: same node set (%d nodes)' % len(got), file=sys.stderr)
        else:
            print('expect: node sets differ; only here: %s; only in expect: %s' % (
                ', '.join(sorted(got - want, key=node_key)) or '-',
                ', '.join(sorted(want - got, key=node_key)) or '-'), file=sys.stderr)
            return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
