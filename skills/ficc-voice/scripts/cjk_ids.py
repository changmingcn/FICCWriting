#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cjk_ids.py (1.0.0, 2026-11-05) -- id patterns for ids inside Chinese text.

Python 3 str regexes count CJK characters as word characters, so `\\b` finds no boundary
between a digit and a following Chinese character: r'\\bL(\\d{1,4})\\b' misses "L383仍写", and
r'N\\d+(?:\\.\\d+)*\\b' cuts "N1.9总起" back to "N1".  The patterns here never use `\\b`; every
id carries explicit look-arounds and ASCII digits only:

  node   N[0-9]+(?:\\.[0-9]+)*    before (?<![A-Za-z0-9])   after (?![0-9])
  line   L[0-9]{1,4}              before (?<![A-Za-z0-9])   after (?![0-9])
  block  B[0-9]+[a-z]?            before (?<![A-Za-z0-9])   after (?![0-9A-Za-z])
  unit   U[0-9]+[a-z]?            before (?<![A-Za-z0-9])   after (?![0-9A-Za-z])

(The letter suffix of block and unit ids makes their right edge exclude letters as well:
"B11bc" and "B2B" are not ids.)

strip_source_refs(text) removes line references that point into another document before the
line numbers of the text itself are read: a prefix 1027, 1104 (any four-digit document label),
提纲, 账本 or 本篇, optional spaces (none needed: "1104L232"), then L-numbers chained by 、 , ，
(each with its L) or a range dash (– — - ~ ～ 至 到, L optional after the dash).
"1104 L1084、L1676", "1104L232–235、L296" and "本篇L363" go; "L383仍写" stays.

Module use (from a sibling script):
  sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import cjk_ids
  cjk_ids.NODE_RE, LINE_RE, BLOCK_RE, UNIT_RE        compiled patterns (LINE_RE group 1 = number)
  cjk_ids.find_nodes(text) / find_blocks / find_units  ids in order of appearance
  cjk_ids.find_lines(text)                           line numbers (int) in order of appearance
  cjk_ids.line_refs(text, prefixes=None)             find_lines(strip_source_refs(text))
  cjk_ids.strip_source_refs(text, prefixes=None)     prefixes: regex alternatives; default
                                                     DEFAULT_SOURCE_PREFIXES

CLI:
  cjk_ids.py find {node,line,block,unit} [FILE] [--strip-sources]   one id per line (stdin
                                                                    when FILE is absent)
  cjk_ids.py --selftest
  cjk_ids.py --version

Exit codes: 0 ok; 1 a failed self-test; 2 unreadable file or bad arguments.
Standard library only; Python 3.9.
"""
import argparse
import re
import sys

VERSION = '1.0.0'

PRE = r'(?<![A-Za-z0-9])'
NODE_ID = PRE + r'N[0-9]+(?:\.[0-9]+)*(?![0-9])'
LINE_ID = PRE + r'L([0-9]{1,4})(?![0-9])'
BLOCK_ID = PRE + r'B[0-9]+[a-z]?(?![0-9A-Za-z])'
UNIT_ID = PRE + r'U[0-9]+[a-z]?(?![0-9A-Za-z])'

NODE_RE = re.compile(NODE_ID)
LINE_RE = re.compile(LINE_ID)
BLOCK_RE = re.compile(BLOCK_ID)
UNIT_RE = re.compile(UNIT_ID)

# A Markdown heading whose first token is a node id; the id may be glued to the heading text
# ("## N1一、…", "### N1.10尾声").  Groups: 1 hashes, 2 id, 3 the rest.
NODE_HEADING_RE = re.compile(r'^(#{2,6})\s+(N[0-9]+(?:\.[0-9]+)*)(?![0-9])\s*(.*)$')

DEFAULT_SOURCE_PREFIXES = (r'(?<![0-9A-Za-z])[0-9]{4}', '提纲', '账本', '本篇')
_LNUM = r'L[0-9]{1,4}(?![0-9])'
_CHAIN = (r'(?:\s*[、,，]\s*' + _LNUM
          + r'|\s*(?:[–—~～-]|至|到)\s*L?[0-9]{1,4}(?![0-9]))*')


def _source_re(prefixes=None):
    alts = '|'.join(prefixes or DEFAULT_SOURCE_PREFIXES)
    # no look-behind before L here: the prefix is the anchor, so "1104L232" goes as well as "1104 L232"
    return re.compile(r'(?:' + alts + r')\s*(?:第\s*)?' + _LNUM + _CHAIN)


_SOURCE_RE = _source_re()


def strip_source_refs(text, prefixes=None):
    """text with every source line reference (prefix + L-number chain) removed."""
    rx = _SOURCE_RE if prefixes is None else _source_re(prefixes)
    return rx.sub('', text)


def find_nodes(text):
    return NODE_RE.findall(text)


def find_blocks(text):
    return BLOCK_RE.findall(text)


def find_units(text):
    return UNIT_RE.findall(text)


def find_lines(text):
    return [int(x) for x in LINE_RE.findall(text)]


def line_refs(text, prefixes=None):
    """Line numbers of the text itself: source references stripped first."""
    return find_lines(strip_source_refs(text, prefixes))


FINDERS = {'node': find_nodes, 'line': find_lines, 'block': find_blocks, 'unit': find_units}


# ------------------------------------------------------------------ self-test
def self_test():
    print('== cjk_ids self-test %s' % VERSION)
    results = []

    def check(name, got, want):
        ok = got == want
        results.append(ok)
        print('%s: %s -> %r%s' % ('PASS' if ok else 'FAIL', name, got, '' if ok else ' (want %r)' % (want,)))

    # the defect being fixed: \b sees no boundary between a digit and a Chinese character
    old_line = re.compile(r'\bL(\d{1,4})\b')
    old_node = re.compile(r'\bN\d+(?:\.\d+)*\b')
    check('old \\b line regex misses “L383仍写” (the defect)', old_line.findall('L383仍写'), [])
    check('old \\b node regex cuts “N1.9总起” to N1 (the defect)', old_node.findall('N1.9总起'), ['N1'])

    # must hit
    check('line: “L383仍写”', find_lines('L383仍写'), [383])
    check('node: “N2.2的”', find_nodes('N2.2的'), ['N2.2'])
    check('node: “〔1105〕段里的N9.1.1”', find_nodes('〔1105〕段里的N9.1.1'), ['N9.1.1'])
    check('block: “B11b，”', find_blocks('B11b，'), ['B11b'])
    check('node: “N1.9总起”', find_nodes('N1.9总起'), ['N1.9'])
    check('node: “N1.10尾声”', find_nodes('N1.10尾声'), ['N1.10'])
    check('unit: “U18、U19a的”', find_units('U18、U19a的'), ['U18', 'U19a'])
    check('line: “检验表L348仍写”', find_lines('检验表L348仍写'), [348])
    # must not take
    check('line: not in “XL383”', find_lines('XL383'), [])
    check('line: not in “L12345”', find_lines('L12345'), [])
    check('node: “N22.” gives N22, never N2', find_nodes('N22.'), ['N22'])
    check('unit and block: nothing in “UB11”', (find_units('UB11'), find_blocks('UB11')), ([], []))
    check('block: nothing in “B11bc” or “B2B”', find_blocks('B11bc B2B'), [])
    check('line: full-width digits are not ids', find_lines('L３８３'), [])

    # heading pattern (outline_slice, heading_list)
    m = NODE_HEADING_RE.match('## N1.10尾声')
    check('heading: “## N1.10尾声”', m and m.groups(), ('##', 'N1.10', '尾声'))
    m = NODE_HEADING_RE.match('### N1.9 收束〔标题〕')
    check('heading: “### N1.9 收束〔标题〕”', m and m.groups(), ('###', 'N1.9', '收束〔标题〕'))
    m = NODE_HEADING_RE.match('## N1一、外部')
    check('heading: “## N1一、外部”', m and m.groups(), ('##', 'N1', '一、外部'))
    check('heading: “## Notes” is no node', NODE_HEADING_RE.match('## Notes'), None)

    # source references
    s = '1027 L30、1104 L1054把Microsoft累计119亿美元也列为到账'
    check('strip: “1027 L30、1104 L1054” both go (the 、 between them stays)', (strip_source_refs(s), line_refs(s)),
          ('、把Microsoft累计119亿美元也列为到账', []))
    s = 'L383仍写“另两组的三条见另外五种看法（五）”。第五种看法的三条在本篇L363（九（一））'
    check('strip: 本篇L363 goes, L383 stays', line_refs(s), [383])
    check('strip: “提纲L148、L164同样写”', line_refs('提纲L148、L164同样写'), [])
    check('strip: “账本 L12–L15”', line_refs('见账本 L12–L15。'), [])
    check('strip: range “1104 L1209–L1260 另外”', line_refs('1104 L1209–L1260 另外五种看法'), [])
    check('strip: “1104 L232–235、L296；auto”', line_refs('1104 L232–235、L296；auto 6/6'), [])
    check('strip: source glued to L, “1104L232–235、L296” (Codex review #08)', line_refs('1104L232–235、L296'), [])
    check('strip: glued, several sources, “1027L30、1104L1054；L9仍写”', line_refs('1027L30、1104L1054；L9仍写'), [9])
    check('strip: “提纲L148、L164” whole chain (Codex review #08)', (strip_source_refs('提纲L148、L164'), line_refs('见提纲L148、L164')), ('', []))
    check('strip: “1104只把…（10月28日，L493”: no prefix glued, L493 stays',
          line_refs('1104只把“最宽”挂在Barclays那十家（10月28日，L493'), [493])
    check('lines: “L9的…检验表L348仍写”', line_refs('L9的“例外”已删，但检验表L348仍写'), [9, 348])
    check('strip: custom prefixes', line_refs('原稿L12、本篇L3', prefixes=['原稿']), [3])

    ok = all(results)
    print('cjk_ids self-test: %s (%d checks)' % ('PASS' if ok else 'FAIL', len(results)))
    return 0 if ok else 1


def main(argv=None):
    for s in (sys.stdout, sys.stderr):
        if hasattr(s, 'reconfigure'):
            s.reconfigure(encoding='utf-8')
    ap = argparse.ArgumentParser(prog='cjk_ids.py',
                                 description='Node, line, block and unit ids in Chinese text (no \\b).')
    ap.add_argument('--version', action='version', version=VERSION)
    ap.add_argument('--selftest', '--self-test', action='store_true', help='run the built-in checks')
    sub = ap.add_subparsers(dest='cmd')
    p = sub.add_parser('find', help='print the ids of one kind, one per line')
    p.add_argument('kind', choices=sorted(FINDERS))
    p.add_argument('file', nargs='?')
    p.add_argument('--strip-sources', action='store_true',
                   help='remove source line references (1027/1104/提纲/账本/本篇 L…) first')
    a = ap.parse_args(argv)
    if a.selftest:
        return self_test()
    if a.cmd != 'find':
        ap.print_usage(sys.stderr)
        return 2
    try:
        if a.file:
            with open(a.file, encoding='utf-8') as fh:
                text = fh.read()
        else:
            text = sys.stdin.read()
    except OSError as e:
        print('cjk_ids.py: cannot read %s: %s' % (a.file, e), file=sys.stderr)
        return 2
    if a.strip_sources:
        text = strip_source_refs(text)
    for x in FINDERS[a.kind](text):
        print(x)
    return 0


if __name__ == '__main__':
    sys.exit(main())
