#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""heading_list.py (1.0.0, 2026-11-05) -- the heading list of a draft, read off its FICC outline.

Generalises two task build scripts (heading lists of the
1101/1104 drafts): their node regex wanted a space after the id ('## N1 …'), so '## N1一、…'
gave 65 headings instead of 79 until it was patched in the task copy.  Here node headings are
read with cjk_ids.NODE_HEADING_RE (id glued to the text allowed) through outline_slice.node_blocks.

A node has a heading when
  (a) its heading line carries the 〔标题〕 mark: '## N1 一、…〔标题〕' or '## N1一、…〔标题〕〔本轮引入〕'
      -> the text between the id and 〔标题〕 (a leading ：/: dropped); or else
  (b) its block has a field line '- 〔标题〕text' -> text (trailing 〔…〕 marks dropped);
      '〔标题〕无…' means no heading (e.g. 〔标题〕无（导语）).
Other nodes (〔段群〕, 〔段落〕 without a 〔标题〕 line) have no heading.  The level is the outline
line's own hashes ('## part', '### （一）', '#### 1.').

Title: --title, else the outline's **题目与版次行**：题目“…”, else no title line (note on stderr).

Usage:
  heading_list.py OUTLINE [--title T] [--after ID LINE ...] [--out FILE]
      list to stdout (or FILE): '# title', then one heading per line, blank line between
      (the make_heading_list_110x layout); --after N10 '### （一）各节出处' adds a line after a
      node's heading (repeatable, in order)
  heading_list.py OUTLINE --ids        id, level, heading (tab-separated), for checks
  heading_list.py --selftest
  heading_list.py --version

Exit codes: 0 ok; 2 unreadable outline, --after on an id without a heading, or no node heading
at all; 1 a failed self-test.  Standard library only; Python 3.9.
"""
import argparse
import contextlib
import io
import os
import re
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cjk_ids  # noqa: E402
import outline_slice  # noqa: E402

VERSION = '1.0.0'
MARK_RE = re.compile(r'^(.*?)〔标题〕(?:〔[^〕]*〕)*\s*$')
FIELD_TITLE_RE = re.compile(r'^\s*(?:[-*+]\s+)?〔标题〕\s*(.*?)\s*(?:〔[^〕]*〕\s*)*$')
NONE_RE = re.compile(r'^无(?:$|[（(：:，,])')
TOPIC_RE = re.compile(r'\*\*题目与版次行\*\*[：:]\s*题目“([^”]+)”')


def headings(text):
    """[(id, hashes, heading text)] in outline order, for nodes that have a heading."""
    out = []
    for nd, _, lines in outline_slice.node_blocks(text):
        m = cjk_ids.NODE_HEADING_RE.match(lines[0])
        hashes, rest = m.group(1), m.group(3)
        mk = MARK_RE.match(rest)
        if mk:
            out.append((nd, hashes, mk.group(1).strip().lstrip('：:').strip()))
            continue
        for ln in lines[1:]:
            f = FIELD_TITLE_RE.match(ln)
            if f:
                val = f.group(1).strip()
                if val and not NONE_RE.match(val):
                    out.append((nd, hashes, val))
                break
    return out


def build(text, title=None, after=()):
    """(list text, number of headings); raises outline_slice.SliceError."""
    heads = headings(text)
    if not heads:
        raise outline_slice.SliceError('no node heading found (no 〔标题〕 mark or 〔标题〕 line)')
    extra = {}
    have = {nd for nd, _, _ in heads}
    for nd, line in after:
        if nd not in have:
            raise outline_slice.SliceError('--after %s: that node has no heading' % nd)
        extra.setdefault(nd, []).append(line)
    if title is None:
        m = TOPIC_RE.search(text)
        title = m.group(1) if m else None
        if title is None:
            print('heading_list.py: no title (no --title, no **题目与版次行**：题目“…”); list starts '
                  'with the first heading', file=sys.stderr)
    out = ['# ' + title] if title else []
    for nd, hashes, head in heads:
        out.append('%s %s' % (hashes, head))
        out += extra.get(nd, [])
    return '\n\n'.join(out) + '\n', len(out)


# ------------------------------------------------------------------ self-test
FIXTURE = """# 样例-提纲

- **题目与版次行**：题目“样例题目”，版次行照旧。

## N0 导语〔段群〕

- **主旨**：根。

## N1一、外部账户〔标题〕

- **主旨**：一。

### N1.0总起〔段群〕

- **主旨**：总起。

### N1.1 （一）零售定价〔标题〕〔本轮引入〕

- **主旨**：一一。

#### N1.1.1：〔段落〕

- 〔标题〕1. 一例〔改〕
- **主旨**：一例。

#### N1.1.2 〔段落〕不另设小标题

- **主旨**：接上段。

## N2：二〔段落组〕

- 〔标题〕二、缓冲
- **主旨**：二。

### N2.1 （一）〔段落〕

- 〔标题〕无（接上）
- **主旨**：无标题。

## 节点编号对照

| 旧 | 新 |
|---|---|
| N1 | N1 |
"""


def run(argv):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        try:
            code = main(argv)
        except SystemExit as e:
            code = e.code if isinstance(e.code, int) else 2
    return code, out.getvalue(), err.getvalue()


def self_test():
    print('== heading_list self-test %s' % VERSION)
    results = []

    def check(name, cond):
        results.append(bool(cond))
        print('%s: %s' % ('PASS' if cond else 'FAIL', name))

    old_1101 = re.compile(r'^(#{2,4}) (N\d+(?:\.\d+)*) (.*?)〔标题〕\s*$')
    check('make_heading_list_1101 regex misses the glued “## N1一、…〔标题〕” (the defect)',
          old_1101.match('## N1一、外部账户〔标题〕') is None)
    with tempfile.TemporaryDirectory() as tmp:
        p = os.path.join(tmp, '样例-提纲.md')
        with open(p, 'w', encoding='utf-8') as fh:
            fh.write(FIXTURE)
        c, o, e = run([p])
        want = ('# 样例题目\n\n## 一、外部账户\n\n### （一）零售定价\n\n#### 1. 一例\n\n## 二、缓冲\n')
        check('list: title, glued id, marks after 〔标题〕, field lines, 无 and 〔段群〕 skipped', c == 0 and o == want)
        c, o, e = run([p, '--ids'])
        check('--ids: id, level, heading', c == 0 and o.splitlines() == [
            'N1\t##\t一、外部账户', 'N1.1\t###\t（一）零售定价', 'N1.1.1\t####\t1. 一例', 'N2\t##\t二、缓冲'])
        c, o, e = run([p, '--title', '另一题', '--after', 'N2', '### （一）各节出处',
                       '--after', 'N2', '### （二）说明'])
        check('--title and --after (two lines, in order)', c == 0 and o.startswith('# 另一题\n')
              and o.endswith('## 二、缓冲\n\n### （一）各节出处\n\n### （二）说明\n'))
        c, o, e = run([p, '--after', 'N1.0', '### x'])
        check('--after on a node without a heading exits 2', c == 2 and 'N1.0' in e)
        outp = os.path.join(tmp, 'list.md')
        c, o, e = run([p, '--out', outp])
        with open(outp, encoding='utf-8') as fh:
            check('--out writes the file, stdout names it', c == 0 and fh.read() == want and outp in o)
        bare = os.path.join(tmp, 'bare-提纲.md')
        with open(bare, 'w', encoding='utf-8') as fh:
            fh.write(FIXTURE.replace('- **题目与版次行**：题目“样例题目”，版次行照旧。\n', ''))
        c, o, e = run([bare])
        check('no title: list starts with the first heading, note on stderr', c == 0
              and o.startswith('## 一、外部账户') and 'no title' in e)
        none = os.path.join(tmp, 'none-提纲.md')
        with open(none, 'w', encoding='utf-8') as fh:
            fh.write('## N0 根〔段群〕\n\n- **主旨**：根。\n')
        c, o, e = run([none])
        check('no heading at all exits 2', c == 2 and 'no node heading' in e)
        c, o, e = run([os.path.join(tmp, 'missing.md')])
        check('unreadable outline exits 2', c == 2 and 'cannot read' in e)
    ok = all(results)
    print('heading_list self-test: %s (%d checks)' % ('PASS' if ok else 'FAIL', len(results)))
    return 0 if ok else 1


def main(argv=None):
    for s in (sys.stdout, sys.stderr):
        if hasattr(s, 'reconfigure'):
            s.reconfigure(encoding='utf-8')
    ap = argparse.ArgumentParser(prog='heading_list.py',
                                 description='Heading list of a draft from its FICC outline (〔标题〕 marks or lines).')
    ap.add_argument('--version', action='version', version=VERSION)
    ap.add_argument('--selftest', '--self-test', action='store_true')
    ap.add_argument('outline', nargs='?')
    ap.add_argument('--title')
    ap.add_argument('--after', nargs=2, action='append', default=[], metavar=('ID', 'LINE'))
    ap.add_argument('--out')
    ap.add_argument('--ids', action='store_true', help='print id, level, heading per line instead')
    a = ap.parse_args(argv)
    if a.selftest:
        return self_test()
    if not a.outline:
        ap.print_usage(sys.stderr)
        return 2
    try:
        text = outline_slice.read(a.outline)
        if a.ids:
            heads = headings(text)
            if not heads:
                raise outline_slice.SliceError('no node heading found (no 〔标题〕 mark or 〔标题〕 line)')
            for nd, hashes, head in heads:
                print('%s\t%s\t%s' % (nd, hashes, head))
            return 0
        body, n = build(text, a.title, a.after)
    except outline_slice.SliceError as e:
        print('heading_list.py: %s' % e, file=sys.stderr)
        return 2
    if a.out:
        with open(a.out, 'w', encoding='utf-8') as fh:
            fh.write(body)
        print('headings %d %s' % (n, a.out))
    else:
        sys.stdout.write(body)
    return 0


if __name__ == '__main__':
    sys.exit(main())
