#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""changed_sentences.py (2026-11-03, wave 3 U09; 2.0.0 fix round r2; 2.1.0 fix round r3) -- the 「凡有改动」 sentence table for a check wave.

Wraps shared-protocols/scripts/sentence_diff.py (U02): the same split (HTML comments dropped, split on 。！？ and
newlines, stripped) and the same best-ratio match, but every sentence counts (also those without CJK, e.g. a number
or an English quote), and order is read too.  Each NEW (current) sentence is one of:
  unchanged  found verbatim in OLD and in order, same end punctuation    (not listed)
  moved      found verbatim in OLD but out of order (outside the longest in-order run)
  moved-seam found verbatim and in order, but its paragraph seam changed: it and the sentence before it follow
             each other in OLD too, and they now share a paragraph where they did not, or the reverse (a paragraph
             merge or split; paragraphs are blocks of non-blank lines)  (1.1.0, fix round r1)
  punct      found verbatim and in order, but its end punctuation (the run of 。！？ the splitter cuts off) changed,
             e.g. 。 -> ？  (2.0.0, fix round r2)
  changed    best match in OLD has ratio >= 0.6
  added      best ratio < 0.6
A changed sentence is paired only near its position (2.1.0, fix round r3).  Between the in-order verbatim sentences
around it there are two slots: the OLD position as far after the one before it as the sentence is in CURRENT, and the
OLD position as far before the one after it; the slot range runs between them (one position when the gap kept its
size).  The candidates are the OLD sentences within --window (default 2) of a slot or in a slot's paragraph; the best
ratio wins, a tie goes to the slot range, then to the nearer slot.  Every row carries pair_confidence:
  high       a verbatim row (unchanged, moved, moved-seam, punct), or a changed pair inside its slot range that crosses
             no other pair and is the only claimant of its OLD sentence
  low        any other changed pair (outside the slot range, crossing another pair, or sharing its OLD sentence)
  unpaired   added and deleted rows
number_set_diff.py counts a low pair as a difference whatever its numbers.
and each OLD sentence that no NEW sentence took (verbatim or as a changed match) is listed as
  deleted    (line = the NEW line where the next kept OLD sentence now sits; old_line = its line in OLD).
The 「凡有改动」 set is every listed row: moved + moved-seam + punct + changed + added + deleted.  The four check modes
(ficc-writer check-clarity and cold-read, ficc-structurer check, ficc-outliner check) read this table as their
changed range after a patch round (dispatch-notes 2.3).

Usage:
  changed_sentences.py FROZEN CURRENT [--glob 'B*.md'] [--window N] [--json] [--out FILE]
  changed_sentences.py --self-test
FROZEN (OLD) comes first, CURRENT (NEW) second, as number_set_diff.py (2.0.0: the order was NEW OLD before).
They are two files, or two directories whose files matching --glob (default *.md) are paired by name (a file only
in CURRENT: all added; only in FROZEN: all deleted).
Output: TSV with header  id  file  line  kind  ratio  old_line  sentence  pair_confidence  (id = <file stem>.s<NNNN>, the CURRENT
sentence's 1-based index in its file; deleted rows: <file stem>.d<NNNN>, the FROZEN index), then one '# ' summary
line naming both inputs and the low-confidence count.  --out FILE writes the same text to FILE (a temp file renamed onto it).  Refused: a
symlink or a directory; a path equal to an input (resolved, or the same file); a path inside an input directory
(resolved; any ancestor that is the same directory).  Exit: 0 ok (with or without changes); 2 usage, unreadable
input or refused output.
"""
import argparse
import bisect
import collections
import difflib
import fnmatch
import json
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'shared-protocols', 'scripts'))
import sentence_diff as sd  # noqa: E402  (U02; read-only use: sents, Refused)

VERSION = '2.1.0'
KINDS = ('moved', 'moved-seam', 'punct', 'changed', 'added', 'deleted')
COLS = ('id', 'file', 'line', 'kind', 'ratio', 'old_line', 'sentence', 'pair_confidence')   # r3: last column added
WINDOW = 2                       # r3 (R1): a changed sentence pairs only within this many OLD sentences of its slot


def _slot(j, anchors, n_new, n_old, opara, window):
    """-> (candidates, near, centre) for CURRENT sentence j (2.1.0, fix round r3, R1).  anchors = the in-order verbatim
    pairs [(current index, old index)], sorted; (ja, ia) and (jb, ib) flank j.  The two slots: ia + (j - ja) and
    ib - (jb - j), each kept inside the gap (ia, ib); near = the slot range between them; centre = the two slots (the
    clamped first slot when the gap holds no OLD sentence, near then empty); candidates = OLD sentences within
    `window` of a centre or in a centre's paragraph."""
    if not n_old:
        return set(), set(), []
    k = bisect.bisect_left(anchors, (j, -1))
    ja, ia = anchors[k - 1] if k else (-1, -1)
    jb, ib = anchors[k] if k < len(anchors) else (n_new, n_old)
    s1, s2 = ia + (j - ja), ib - (jb - j)
    if ia + 1 <= ib - 1:
        c1, c2 = min(s1, ib - 1), max(s2, ia + 1)
        near, centre = set(range(min(c1, c2), max(c1, c2) + 1)), sorted({c1, c2})
    else:
        near, centre = set(), [min(max(s1, 0), n_old - 1)]
    cands = {i for c in centre for i in range(max(0, c - window), min(n_old, c + window + 1))}
    paras = {opara[c] for c in centre if opara[c] is not None}
    cands |= {i for i, p in enumerate(opara) if p in paras}
    return cands, near, centre


def _best_near(s, olds, cands, near, centre):
    """Best difflib ratio over the candidates only; a tie goes to the slot range (near), then to the nearer slot."""
    best, bi, key = 0.0, None, None
    sm = difflib.SequenceMatcher(None, s, '')
    for i in sorted(cands):
        b = olds[i]
        if abs(len(b) - len(s)) > len(s):
            continue
        sm.set_seq2(b)
        if sm.real_quick_ratio() < best or sm.quick_ratio() < best:
            continue
        r = sm.ratio()
        k = (r, i in near, -min(abs(i - c) for c in centre))
        if key is None or k > key:
            best, bi, key = r, i, k
    return best, bi


def _confidence(match, anchors, near):
    """{current index: 'high' | 'low'} for every paired row (r3, R1).  Verbatim rows are high.  A changed pair is high
    only inside its slot range (near), crossing no anchor or other changed pair, and the only claimant of its OLD
    sentence."""
    claims = collections.Counter(m[1] for m in match if m[0] != 'added')
    pts = sorted(set(anchors) | {(j, m[1]) for j, m in enumerate(match) if m[0] == 'changed'})
    pre, hi = [], -1                 # largest old index among earlier pairs
    for _, i in pts:
        pre.append(hi); hi = max(hi, i)
    suf, lo = [0] * len(pts), float('inf')   # smallest old index among later pairs
    for n in range(len(pts) - 1, -1, -1):
        suf[n] = lo; lo = min(lo, pts[n][1])
    crossing = {pts[n][0] for n in range(len(pts)) if pre[n] > pts[n][1] or suf[n] < pts[n][1]}
    out = {}
    for j, m in enumerate(match):
        if m[0] == 'changed':
            out[j] = 'high' if (m[1] in near.get(j, ()) and j not in crossing and claims[m[1]] == 1) else 'low'
        elif m[0] != 'added':
            out[j] = 'high'
    return out


def _lis(seq):
    """indices (into seq) of one longest strictly increasing subsequence."""
    tails, tidx, prev = [], [], [None] * len(seq)
    for i, v in enumerate(seq):
        k = bisect.bisect_left(tails, v)
        if k == len(tails):
            tails.append(v); tidx.append(i)
        else:
            tails[k] = v; tidx[k] = i
        prev[i] = tidx[k - 1] if k else None
    out, i = set(), (tidx[-1] if tidx else None)
    while i is not None:
        out.add(i); i = prev[i]
    return out


def _sents(path):
    """sd.sents(path) plus each sentence's end punctuation: [(sentence, line, ends)].  The same comment strip and
    split as sentence_diff.py; ends = the run of 。！？ right after the piece ('' at a newline or the end)."""
    out = sd.sents(path)
    with open(path, encoding='utf-8', errors='ignore') as f:
        text = sd.COMMENT.sub('', f.read())
    ends = []
    for m in sd.PIECE.finditer(text):
        if m.group().strip():
            k = m.end()
            while k < len(text) and text[k] in '。！？':
                k += 1
            ends.append(text[m.end():k])
    if len(ends) != len(out):          # cannot happen with the same regexes; then punctuation is not compared
        ends = [''] * len(out)
    return [(s, line, e) for (s, line), e in zip(out, ends)]


def _paras(path):
    """{line: paragraph number}; a paragraph is a block of non-blank lines."""
    if not path:
        return {}
    with open(path, encoding='utf-8', errors='ignore') as f:
        rows = f.read().split('\n')
    out, p, blank = {}, 0, True
    for n, l in enumerate(rows, 1):
        if l.strip():
            p, blank = p + blank, False
            out[n] = p
        else:
            blank = True
    return out


def compare(old_path, new_path, label=None, every=False, window=WINDOW):
    """-> (rows, counts) for one FROZEN (old) / CURRENT (new) file pair; either path may be None (file absent).
    every=True also returns the unchanged sentences (kind 'unchanged', not counted), so a caller can resolve any
    sentence id; each row with a FROZEN counterpart carries 'old' (its text) and 'old_index' (1-based); every row
    carries 'pair_confidence' (high, low, unpaired; r3).  window: the pairing window of a changed sentence (r3, R1)."""
    A = _sents(new_path) if new_path else []
    B = _sents(old_path) if old_path else []
    stem = label or os.path.splitext(os.path.basename(new_path or old_path))[0]
    olds = [b for b, _, _ in B]
    free = {}
    for i, b in enumerate(olds):
        free.setdefault(b, []).append(i)
    match = [None] * len(A)          # (kind, old index, ratio)
    for j, (s, _, _) in enumerate(A):   # verbatim first, each OLD occurrence used once
        if free.get(s):
            match[j] = ('verbatim', free[s].pop(0), 1.0)
    for j, (s, _, _) in enumerate(A):   # a repeat of an OLD sentence already used: still not new text
        if not match[j] and s in free and not free[s]:
            match[j] = ('verbatim', olds.index(s), 1.0)
    vb = [j for j, m in enumerate(match) if m]
    keep = _lis([match[j][1] for j in vb])
    anchors = [(j, match[j][1]) for k, j in enumerate(vb) if k in keep]   # in-order verbatim pairs (r3)
    pn, po = _paras(new_path), _paras(old_path)
    opara = [po.get(line) for _, line, _ in B]
    taken, near = {m[1] for m in match if m}, {}
    for j, (s, _, _) in enumerate(A):   # r3 (R1): pair only near the slot, never anywhere in the file
        if match[j]:
            continue
        cands, near[j], centre = _slot(j, anchors, len(A), len(B), opara, window)
        r, bi = _best_near(s, olds, cands, near[j], centre)
        if bi is not None and r >= 0.6:
            match[j] = ('changed', bi, round(r, 4)); taken.add(bi)
        else:
            match[j] = ('added', bi, round(r, 4))
    rows = []
    for k, j in enumerate(vb):
        if k not in keep:
            match[j] = ('moved',) + match[j][1:]
    base = list(match)                   # judge every seam on the unmodified state (r2, C02: 3 paragraphs -> 1 is 2 seams)
    for j in range(1, len(A)):           # paragraph merge or split with verbatim sentences: the seam moved
        a, b = base[j - 1], base[j]
        if b[0] == 'verbatim' and a[0] in ('verbatim', 'moved', 'changed') and b[1] == a[1] + 1 and \
                (pn.get(A[j][1]) == pn.get(A[j - 1][1])) != (po.get(B[b[1]][1]) == po.get(B[a[1]][1])):
            match[j] = ('moved-seam',) + b[1:]
    for j, m in enumerate(match):        # same words, same place, other end punctuation (。 -> ？): listed  (r2)
        if m[0] == 'verbatim' and A[j][2] != B[m[1]][2]:
            match[j] = ('punct',) + m[1:]
    conf = _confidence(match, anchors, near)
    for j, (s, line, _) in enumerate(A):
        kind, bi, r = match[j]
        if kind == 'verbatim' and not every:
            continue
        has_old = bi is not None and kind != 'added'
        rows.append({'id': '%s.s%04d' % (stem, j + 1), 'file': stem, 'line': line,
                     'kind': 'unchanged' if kind == 'verbatim' else kind,
                     'ratio': r, 'old_line': B[bi][1] if has_old else '', 'sentence': s,
                     'old': B[bi][0] if has_old else '', 'old_index': bi + 1 if has_old else None,
                     'pair_confidence': conf.get(j, 'unpaired')})
    pos = sorted((m[1], A[j][1]) for j, m in enumerate(match) if m[0] in ('verbatim', 'moved', 'moved-seam', 'punct', 'changed'))
    keys = [p for p, _ in pos]
    last = A[-1][1] if A else 0
    for i, (b, oline, _) in enumerate(B):
        if i in taken:
            continue
        k = bisect.bisect_right(keys, i)
        rows.append({'id': '%s.d%04d' % (stem, i + 1), 'file': stem, 'line': pos[k][1] if k < len(pos) else last,
                     'kind': 'deleted', 'ratio': '', 'old_line': oline, 'sentence': b, 'old': b, 'old_index': i + 1,
                     'pair_confidence': 'unpaired'})
    rows.sort(key=lambda x: (x['line'] or 0, x['id']))
    counts = dict.fromkeys(KINDS, 0)
    for x in rows:
        if x['kind'] in counts:
            counts[x['kind']] += 1
    counts['low_confidence'] = sum(x['pair_confidence'] == 'low' for x in rows)
    counts['new_sentences'], counts['old_sentences'] = len(A), len(B)
    return rows, counts


def pairs(old, new, glob):
    """-> [(frozen file or None, current file or None, label)]: two files, or two directories paired by name."""
    if os.path.isfile(new) and os.path.isfile(old):
        return [(old, new, None)]
    if not (os.path.isdir(new) and os.path.isdir(old)):
        raise sd.Refused('FROZEN and CURRENT must be two files or two directories')
    names = sorted({n for d in (old, new) for n in os.listdir(d) if fnmatch.fnmatch(n, glob)
                    and os.path.isfile(os.path.join(d, n))})
    return [(os.path.join(old, n) if os.path.isfile(os.path.join(old, n)) else None,
             os.path.join(new, n) if os.path.isfile(os.path.join(new, n)) else None,
             os.path.splitext(n)[0]) for n in names]


def run(old, new, glob='*.md', window=WINDOW):
    """FROZEN (old) first, CURRENT (new) second -> (rows, totals)."""
    rows, tot = [], dict.fromkeys(KINDS, 0)
    tot.update(new_sentences=0, old_sentences=0, files=0, low_confidence=0, frozen=old, current=new)
    for b, a, lab in pairs(old, new, glob):
        r, c = compare(b, a, lab, window=window)
        rows += r
        tot['files'] += 1
        for k in c:
            tot[k] += c[k]
    tot['changed_set'] = sum(tot[k] for k in KINDS)
    return rows, tot


def render(rows, tot):
    out = ['\t'.join(COLS)]
    for x in rows:
        out.append('\t'.join(str(x[c]).replace('\t', ' ') for c in COLS))
    out.append('# 凡有改动 %d (moved %d, moved-seam %d, punct %d, changed %d, added %d, deleted %d) of %d CURRENT / %d FROZEN '
               'sentences in %d file(s); low-confidence pairs %d; frozen=%s current=%s' % (
                   tot['changed_set'], tot['moved'], tot['moved-seam'], tot['punct'], tot['changed'], tot['added'],
                   tot['deleted'], tot['new_sentences'], tot['old_sentences'], tot['files'], tot.get('low_confidence', 0),
                   tot.get('frozen', '?'), tot.get('current', '?')))
    return '\n'.join(out) + '\n'


def _same(a, b):
    try:
        return os.path.samefile(a, b)
    except OSError:
        return False


def guard_out(path, inputs, files=()):
    """Refuse an output that is a symlink or directory, equals an input (the two arguments or any paired input file,
    symlinks resolved, or the same file), or lies inside an input directory (resolved, or an ancestor that is the
    same directory).  Raises sd.Refused; writes nothing."""
    p = os.path.abspath(path)
    if os.path.islink(p) or os.path.isdir(p):
        raise sd.Refused('refused output (symlink or directory): %s' % path)
    rp = os.path.realpath(p)
    ups, d = [], os.path.dirname(rp)
    while True:
        ups.append(d)
        if os.path.dirname(d) == d:
            break
        d = os.path.dirname(d)
    for i in [x for x in inputs if x] + [x for x in files if x]:
        ri = os.path.realpath(os.path.abspath(i))
        if rp == ri or (os.path.exists(p) and _same(p, ri)):
            raise sd.Refused('refused output (it is an input): %s' % path)
        if os.path.isdir(ri) and any(u == ri or (os.path.isdir(u) and _same(u, ri)) for u in ups):
            raise sd.Refused('refused output (inside input directory %s): %s' % (i, path))


def write_out(path, text, inputs, files=()):
    guard_out(path, inputs, files)
    p = os.path.abspath(path)
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(p) or '.', prefix='.cs-')
    with os.fdopen(fd, 'w', encoding='utf-8') as f:
        f.write(text)
    os.replace(tmp, p)


OLD_FX = '第一句保持不变。第二句话会被小改一下。第三句将被删除掉。第四句被挪到后面去了。第五句保持原样。\n'
NEW_FX = '第一句保持不变。第二句话会被稍微小改一下。第五句保持原样。第四句被挪到后面去了。全新加入的一句话完全不同。42%\n'


def selftest():
    ok = True
    d = tempfile.mkdtemp(prefix='cs-selftest-')
    try:
        for sub, txt in (('old', OLD_FX), ('new', NEW_FX)):
            os.makedirs(os.path.join(d, sub))
            with open(os.path.join(d, sub, 'B01.md'), 'w', encoding='utf-8') as f:
                f.write(txt)
        with open(os.path.join(d, 'new', 'B02.md'), 'w', encoding='utf-8') as f:
            f.write('只在新稿里的块。\n')
        rows, tot = run(os.path.join(d, 'old'), os.path.join(d, 'new'))
        kinds = {(x['file'], x['sentence']): x['kind'] for x in rows}
        cases = [
            ('changed sentence', kinds.get(('B01', '第二句话会被稍微小改一下')) == 'changed'),
            ('deleted sentence', kinds.get(('B01', '第三句将被删除掉')) == 'deleted'),
            ('moved sentence (out of order)', ('moved' in (kinds.get(('B01', '第四句被挪到后面去了')),
                                                            kinds.get(('B01', '第五句保持原样'))))),
            ('added sentence', kinds.get(('B01', '全新加入的一句话完全不同')) == 'added'),
            ('a sentence without CJK counts (42%)', kinds.get(('B01', '42%')) == 'added'),
            ('unchanged in-order sentence not listed', ('B01', '第一句保持不变') not in kinds),
            ('file only in NEW: all added', kinds.get(('B02', '只在新稿里的块')) == 'added'),
            ('summary counts add up', tot['changed_set'] == len(rows) == 6),
        ]
        out = os.path.join(d, 'table.tsv')
        write_out(out, render(rows, tot), [])
        cases.append(('--out writes the table', open(out, encoding='utf-8').read().startswith('id\tfile')))
        os.symlink(out, os.path.join(d, 'link.tsv'))
        try:
            write_out(os.path.join(d, 'link.tsv'), 'x', [])
            cases.append(('--out refuses a symlink', False))
        except sd.Refused:
            cases.append(('--out refuses a symlink', True))
        same = main([os.path.join(d, 'new', 'B01.md'), os.path.join(d, 'new', 'B01.md')], quiet=True)
        cases.append(('identical inputs: exit 0, empty set', same == 0))
        for sub, txt in (('m-old.md', '甲句在一段。乙句在一段。\n\n丙句另起一段。\n'), ('m-new.md', '甲句在一段。乙句在一段。丙句另起一段。\n')):
            with open(os.path.join(d, sub), 'w', encoding='utf-8') as f:
                f.write(txt)
        seam = [(x['kind'], x['sentence']) for x in compare(os.path.join(d, 'm-old.md'), os.path.join(d, 'm-new.md'))[0]]
        cases.append(('paragraph merge, sentences verbatim: moved-seam', seam == [('moved-seam', '丙句另起一段')]))
        seam = [(x['kind'], x['sentence']) for x in compare(os.path.join(d, 'm-new.md'), os.path.join(d, 'm-old.md'))[0]]
        cases.append(('paragraph split, sentences verbatim: moved-seam', seam == [('moved-seam', '丙句另起一段')]))
        for n_ in (3, 4):                # r2 C02: n paragraphs merged into one -> n-1 seams
            parts = ['第%d段的一句话。' % (i + 1) for i in range(n_)]
            with open(os.path.join(d, 'n-old.md'), 'w', encoding='utf-8') as f:
                f.write('\n\n'.join(parts) + '\n')
            with open(os.path.join(d, 'n-new.md'), 'w', encoding='utf-8') as f:
                f.write(''.join(parts) + '\n')
            ks = [x['kind'] for x in compare(os.path.join(d, 'n-old.md'), os.path.join(d, 'n-new.md'))[0]]
            cases.append(('%d paragraphs merged into one: %d moved-seam rows' % (n_, n_ - 1), ks == ['moved-seam'] * (n_ - 1)))
        cases.append(('missing input: exit 2', main([os.path.join(d, 'old'), os.path.join(d, 'nope')], quiet=True) == 2))
        # r2 CX04: end punctuation only (。 -> ？) is listed as punct
        for sub, txt in (('p-old.md', '公司有偿付能力。下一句不变。\n'), ('p-new.md', '公司有偿付能力？下一句不变。\n')):
            with open(os.path.join(d, sub), 'w', encoding='utf-8') as f:
                f.write(txt)
        pk = [(x['kind'], x['sentence']) for x in compare(os.path.join(d, 'p-old.md'), os.path.join(d, 'p-new.md'))[0]]
        cases.append(('end punctuation only (。 -> ？): punct', pk == [('punct', '公司有偿付能力')]))
        # r2 CX01: FROZEN first, CURRENT second -- a sentence only in CURRENT is added, one only in FROZEN deleted
        for sub, txt in (('o-frozen.md', '甲句保持原样。旧稿独有的那句讲利差。\n'), ('o-current.md', '甲句保持原样。Only in the current draft.\n')):
            with open(os.path.join(d, sub), 'w', encoding='utf-8') as f:
                f.write(txt)
        o_out = os.path.join(d, 'order.tsv')
        main([os.path.join(d, 'o-frozen.md'), os.path.join(d, 'o-current.md'), '--out', o_out], quiet=True)
        k1 = {r.split('\t')[6]: r.split('\t')[3] for r in open(o_out, encoding='utf-8').read().splitlines()[1:-1]}
        cases.append(('CLI order FROZEN CURRENT: current-only sentence added, frozen-only deleted',
                      k1 == {'Only in the current draft.': 'added', '旧稿独有的那句讲利差': 'deleted'}))
        # r2 CX05: directory mode refuses an output that is a paired input file or lies inside an input directory
        import hashlib
        snap = lambda: {n: hashlib.sha256(open(os.path.join(d, s_, n), 'rb').read()).hexdigest()
                        for s_ in ('old', 'new') for n in os.listdir(os.path.join(d, s_))}
        before = snap()
        refused = [main([os.path.join(d, 'old'), os.path.join(d, 'new'), '--out', o], quiet=True) for o in (
            os.path.join(d, 'new', 'B01.md'), os.path.join(d, 'old', 'B01.md'), os.path.join(d, 'new', 'table.tsv'),
            os.path.join(d, 'new', '..', 'new', 'B02.md'))]
        cases.append(('directory mode: output on or inside an input refused (exit 2), inputs unchanged',
                      refused == [2, 2, 2, 2] and snap() == before))
        os.symlink(os.path.join(d, 'new'), os.path.join(d, 'newlink'))
        cases.append(('output through a symlinked input directory refused',
                      main([os.path.join(d, 'old'), os.path.join(d, 'new'), '--out', os.path.join(d, 'newlink', 'B01.md')], quiet=True) == 2
                      and snap() == before))
        ok_out = os.path.join(d, 'out', 't.tsv'); os.makedirs(os.path.dirname(ok_out))
        cases.append(('output outside the inputs written, inputs unchanged',
                      main([os.path.join(d, 'old'), os.path.join(d, 'new'), '--out', ok_out], quiet=True) == 0
                      and open(ok_out, encoding='utf-8').read().startswith('id\tfile') and snap() == before))
        # r3 R1: positional pairing and pair_confidence
        def pc(old, new, **kw):
            for sub, txt in (('x-old.md', old), ('x-new.md', new)):
                with open(os.path.join(d, sub), 'w', encoding='utf-8') as f:
                    f.write(txt)
            return [(x['kind'], x['sentence'], x['old_index'], x['pair_confidence'])
                    for x in compare(os.path.join(d, 'x-old.md'), os.path.join(d, 'x-new.md'), **kw)[0]]
        cases.append(('swap 15%/7% between similar sentences: both pairs low',
                      [c[3] for c in pc('甲行利差是15%。乙行利差是7%。\n', '甲行利差是7%。乙行利差是15%。\n')] == ['low', 'low']))
        cases.append(('swap 5%/7% (a tie): each pairs with its slot, high',
                      [(c[2], c[3]) for c in pc('甲行利差是5%。乙行利差是7%。\n', '甲行利差是7%。乙行利差是5%。\n')]
                      == [(1, 'high'), (2, 'high')]))
        far = pc('甲说明背景。\n\n甲行利差是15%。\n\n丙段一。丙段二。丙段三。丙段四。\n\n乙行利差是7%。\n',
                 '甲说明背景。\n\n甲行利差是7%。\n\n丙段一。丙段二。丙段三。丙段四。\n\n乙行利差是15%。\n')
        cases.append(('a more similar sentence outside the window and paragraph is not taken: pairs stay in place, high',
                      [(c[1], c[2], c[3]) for c in far if c[0] == 'changed'] == [('甲行利差是7%', 2, 'high'), ('乙行利差是15%', 7, 'high')]))
        mv = pc('首句不变。乙句有5%。丙句不变。丁句不变。\n\n戊段一句。\n', '首句不变。丙句不变。丁句不变。\n\n戊段一句。乙句有5%。\n')
        cases.append(('a verbatim sentence moved to another paragraph still pairs (moved, high)',
                      [c for c in mv if c[1] == '乙句有5%'] == [('moved', '乙句有5%', 2, 'high')]))
        me = pc('首句不变。乙句里有5%的利差。丙句不变。\n', '首句不变。丙句不变。乙句里有5%利差。\n')
        cases.append(('a moved and edited sentence pairs with its old sentence, low (crosses an anchor)',
                      [c for c in me if c[0] == 'changed'] == [('changed', '乙句里有5%利差', 2, 'low')]))
        cases.append(('added and deleted rows are unpaired; the TSV ends with pair_confidence',
                      {c[3] for c in pc('甲句。\n', '完全不同的新句子出现在这里。\n')} == {'unpaired'}
                      and render(*run(os.path.join(d, 'x-old.md'), os.path.join(d, 'x-new.md'))).split('\n')[0].endswith('\tpair_confidence')))
        cases.append(('--window 0 still pairs an in-place edit',
                      [c[3] for c in pc('甲句讲利差是5%。乙句不变。\n', '甲句讲利差是6%。乙句不变。\n', window=0)] == ['high']))
    finally:
        import shutil
        shutil.rmtree(d, ignore_errors=True)
    for name, good in cases:
        ok &= bool(good)
        print('  %s  %s' % ('PASS' if good else 'FAIL', name))
    print('changed_sentences self-test: %s' % ('all passed' if ok else 'FAILED'))
    return 0 if ok else 1


def main(argv=None, quiet=False):
    ap = argparse.ArgumentParser(prog='changed_sentences.py', description=__doc__.split('\n\n')[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('frozen', nargs='?', help='FROZEN (old) file or directory')
    ap.add_argument('current', nargs='?', help='CURRENT (new) file or directory')
    ap.add_argument('--glob', default='*.md', help='directory mode: files to pair (default *.md)')
    ap.add_argument('--window', type=int, default=WINDOW, help='pairing window around the slot (default %d)' % WINDOW)
    ap.add_argument('--json', action='store_true', help='one JSON object {counts, rows}')
    ap.add_argument('--out', help='write the table here instead of stdout')
    ap.add_argument('--self-test', '--selftest', action='store_true', help='built-in fixture tests')
    ap.add_argument('--version', action='version', version=VERSION)
    try:
        a = ap.parse_args(argv)
    except SystemExit as e:
        return 2 if e.code else 0
    if a.self_test:
        return selftest()
    if not (a.frozen and a.current) or a.window < 0:
        ap.print_usage(sys.stderr)
        return 2
    try:
        if a.out:                      # refuse before any work: never write onto or into an input
            guard_out(a.out, [a.frozen, a.current])
        prs = pairs(a.frozen, a.current, a.glob)
        if a.out:
            guard_out(a.out, [a.frozen, a.current], [x for b, c, _ in prs for x in (b, c)])
        rows, tot = run(a.frozen, a.current, a.glob, a.window)
        text = json.dumps({'counts': tot, 'rows': rows}, ensure_ascii=False, indent=1) + '\n' if a.json \
            else render(rows, tot)
        if a.out:
            write_out(a.out, text, [a.frozen, a.current], [x for b, c, _ in prs for x in (b, c)])
        elif not quiet:
            sys.stdout.write(text)
    except (sd.Refused, OSError) as e:
        if not quiet:
            print('changed_sentences: %s' % e, file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
