#!/usr/bin/env python3
"""Sentence-level diff of a new draft against an old one: CJK characters carried verbatim, lightly edited, changed or new.

Usage:
  sentence_diff.py NEW OLD [--json] [--out DIR [--task-dir DIR]]
  sentence_diff.py --selftest

Method (the author's 1101 audit; unchanged): drop HTML comments, split on 。！？ and newlines, strip, count CJK
U+4E00–U+9FFF; each NEW sentence found verbatim in OLD is verbatim, else it takes its best difflib ratio against the OLD
sentences (real_quick_ratio / quick_ratio prefilter, stop above 0.95). Buckets verbatim / >=0.9 / 0.8-0.9 / 0.6-0.8 / <0.6,
weighted by CJK count. Printed: the audit script's two lines (new-or-changed: <0.6, <0.8, any change), then the shares of
the NEW total. --json prints one JSON object instead.
--out DIR writes sentences.tsv (one row per NEW sentence with CJK: id, line, cjk, bucket, ratio, old_line, changed,
sentence; plain TSV, no quoting; id = s + the sentence's 1-based index in NEW, line = its first character's line in NEW) and summary.json. DIR must
lie inside a task dir (a dir holding work.json: --task-dir, else the nearest ancestor of DIR); anything else exits 2 before
a file is read. An output that is a symlink, a hard link (more than one link), or NEW or OLD (same path or same file) is
refused the same way, as is one that is not a regular file (a directory, say), and each output is written to a temp file
in DIR and renamed onto its name (os.replace), so no link is ever written through. A replaced output keeps its permission
bits; a new one gets 0666 less the umask, as open() gives. Without --out nothing is written.
Update estimates (ficc-hand references/cost-estimate.md §2): run it on the line's last update (its final against the
version before) or on the frozen draft against the previous final, and take the "<0.8" share (rewritten or new) as the
changed volume. The "any change" share is for changed-sentence coverage (the changed column of sentences.tsv), not for
estimates.
Exit: 0 ok; 2 usage, unreadable input or refused (unknown arguments included).
"""
from __future__ import annotations

import argparse
import bisect
import contextlib
import csv
import difflib
import io
import json
import os
import re
import shutil
import stat
import sys
import tempfile

VERSION = '1.1.0'
COMMENT = re.compile(r'<!--.*?-->', re.S)
PIECE = re.compile(r'[^。！？\n]+')
CJK = re.compile(r'[一-鿿]')
BUCKETS = ('verbatim', '>=0.9', '0.8-0.9', '0.6-0.8', '<0.6')
OUTPUTS = ('sentences.tsv', 'summary.json')


class Refused(Exception):
    pass


def cj(s): return len(CJK.findall(s))


def sents(path):
    """[(sentence, line)] exactly as the audit script splits (re.sub comments; re.split on 。！？\\n; strip; drop empty),
    each with the line of its first character in the original file."""
    try:
        with open(path, encoding='utf-8', errors='ignore') as f:
            raw = f.read()
    except OSError as exc:
        raise Refused(f'cannot read {path}: {exc.strerror}')
    parts, starts, pos, kept = [], [], 0, 0          # starts: (offset in the stripped text, offset in raw)
    for m in COMMENT.finditer(raw):
        parts.append(raw[pos:m.start()]); starts.append((kept, pos)); kept += m.start() - pos; pos = m.end()
    parts.append(raw[pos:]); starts.append((kept, pos))
    text = ''.join(parts); keys = [a for a, _ in starts]
    nl = [i for i, ch in enumerate(raw) if ch == '\n']
    out = []
    for m in PIECE.finditer(text):
        s = m.group(); st = s.strip()
        if not st:
            continue
        k = m.start() + (len(s) - len(s.lstrip()))
        j = bisect.bisect_right(keys, k) - 1
        r = starts[j][1] + (k - starts[j][0])
        out.append((st, bisect.bisect_left(nl, r) + 1))
    return out


def bucket_of(best):
    return '>=0.9' if best >= 0.9 else '0.8-0.9' if best >= 0.8 else '0.6-0.8' if best >= 0.6 else '<0.6'


def diff(new, old):
    A = sents(new); B = sents(old)
    Bs = [b for b, _ in B]; first_line = {}
    for b, ln in B:
        first_line.setdefault(b, ln)
    buckets = dict.fromkeys(BUCKETS, 0); rows = []
    for idx, (s, line) in enumerate(A, 1):
        n = cj(s)
        if n == 0:
            continue
        if s in first_line:
            buckets['verbatim'] += n
            rows.append({'id': f's{idx:04d}', 'line': line, 'cjk': n, 'bucket': 'verbatim', 'ratio': 1.0, 'old_line': first_line[s], 'changed': 0, 'sentence': s})
            continue
        best = 0.0; bi = None; sm = difflib.SequenceMatcher(None, s, '')
        for i, b in enumerate(Bs):
            if abs(len(b) - len(s)) > len(s): continue
            sm.set_seq2(b)
            if sm.real_quick_ratio() <= best or sm.quick_ratio() <= best: continue
            r = sm.ratio()
            if r > best: best = r; bi = i
            if best > 0.95: break
        k = bucket_of(best); buckets[k] += n
        rows.append({'id': f's{idx:04d}', 'line': line, 'cjk': n, 'bucket': k, 'ratio': round(best, 4),
                     'old_line': B[bi][1] if bi is not None else '', 'changed': 1, 'sentence': s})
    tot = sum(buckets.values())
    noc = {'lt_0.6': buckets['<0.6'], 'lt_0.8': buckets['<0.6'] + buckets['0.6-0.8'], 'any_change': tot - buckets['verbatim']}
    share = {k: (v / tot if tot else 0.0) for k, v in noc.items()}
    return {'tool': 'sentence_diff.py', 'version': VERSION, 'new': new, 'old': old, 'total_cjk': tot, 'buckets': buckets,
            'new_or_changed': noc, 'share': share, 'sentences_with_cjk': len(rows)}, rows


def inside(p, root): return p == root or p.startswith(root.rstrip(os.sep) + os.sep)


def task_dir_for(out, task_dir):
    o = os.path.realpath(out)
    if task_dir:
        t = os.path.realpath(task_dir)
        if not os.path.isfile(os.path.join(t, 'work.json')):
            raise Refused(f'--task-dir {task_dir} holds no work.json (not a task dir)')
        if not inside(o, t):
            raise Refused(f'refusing to write outside the task dir: --out {out} is not inside {task_dir}')
        return t
    p = o
    while True:
        if os.path.isfile(os.path.join(p, 'work.json')):
            return p
        q = os.path.dirname(p)
        if q == p:
            raise Refused(f'refusing to write outside a task dir: no work.json at or above --out {out}')
        p = q


def same_file(a, b):
    try: return os.path.samefile(a, b)
    except OSError: return False


def guard_outputs(out, t, inputs):
    """Each output: not a symlink (never written through a link, wherever it points), inside the task dir, not a hard
    link (st_nlink > 1: another task file may share it), and not NEW or OLD, by path or by file (a hard
    link) (W1 review F3); an existing name that is not a regular file (a directory has st_nlink >= 2) is refused as such,
    before the link count (W2 NF2). Runs before a file is read and again before the writes."""
    reals = {os.path.realpath(i) for i in inputs}
    for n in OUTPUTS:
        p = os.path.join(out, n)
        if os.path.islink(p):
            raise Refused(f'refusing: {n} under --out is a symlink (-> {os.readlink(p)}); outputs are never written through a link')
        r = os.path.realpath(p)
        if not inside(r, t):
            raise Refused(f'refusing: {n} under --out resolves outside the task dir ({r})')
        if r in reals or (os.path.lexists(p) and any(same_file(p, i) for i in inputs)):
            raise Refused(f'refusing: {n} under --out is an input file ({r})')
        st = os.lstat(p) if os.path.lexists(p) else None
        if st is not None and not stat.S_ISREG(st.st_mode):
            kind = 'a directory' if stat.S_ISDIR(st.st_mode) else 'a special file'
            raise Refused(f'refusing: {n} under --out is {kind}, not a regular file; outputs replace regular files only')
        if st is not None and st.st_nlink > 1:
            raise Refused(f'refusing: {n} under --out is a hard link ({st.st_nlink} links); another file shares it')


def output_mode(path):
    """Permission bits for an output about to replace path: those of the existing regular file at path (lstat, never
    followed), as an in-place write would keep them; else 0666 less the process umask, as open() would create it (W2 N2).
    The umask is read by setting 077 for an instant, so nothing made meanwhile is more open than it."""
    with contextlib.suppress(FileNotFoundError):
        st = os.lstat(path)
        if stat.S_ISREG(st.st_mode):
            return stat.S_IMODE(st.st_mode) & 0o777
    mask = os.umask(0o077)
    os.umask(mask)
    return 0o666 & ~mask


def _replace_out(path, write, newline=None):
    """Write to a temp file beside path, then os.replace it onto path: the old name is unlinked, never written
    through, so a symlink or hard link made after the guard keeps its bytes. The temp file (mkstemp:
    0600) takes output_mode(path) before the rename, so neither the umask nor a restrictive mode on the old file is lost
    (W2 N2)."""
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path), prefix='.' + os.path.basename(path) + '.', suffix='.tmp')
    try:
        os.fchmod(fd, output_mode(path))
        with io.open(fd, 'w', encoding='utf-8', newline=newline) as f:
            write(f)
        os.replace(tmp, path)
    except BaseException:
        with contextlib.suppress(OSError):
            os.unlink(tmp)
        raise


def _write_tsv(rows, cols):
    def write(f):                                                       # plain TSV, no quoting
        f.write('\t'.join(cols) + '\n')
        for r in rows:
            f.write('\t'.join(re.sub(r'[\t\r\n]', ' ', str(r[c])) for c in cols) + '\n')
    return write


def write_out(out, t, summary, rows, inputs=()):
    os.makedirs(out, exist_ok=True)
    guard_outputs(out, t, inputs)
    cols = ['id', 'line', 'cjk', 'bucket', 'ratio', 'old_line', 'changed', 'sentence']
    try:
        _replace_out(os.path.join(out, 'sentences.tsv'), _write_tsv(rows, cols), newline='')
        _replace_out(os.path.join(out, 'summary.json'), lambda f: json.dump(summary, f, ensure_ascii=False, indent=1))
    except OSError as exc:
        raise Refused(f'cannot write under --out {out}: {exc.strerror}')


def run(args):
    t = task_dir_for(args.out, args.task_dir) if args.out else None   # write protection first
    if args.task_dir and not args.out:
        raise Refused('--task-dir only goes with --out')
    for p in (args.new, args.old):
        if not os.path.isfile(p):
            raise Refused(f'not a file: {p}')
    if args.out:
        guard_outputs(os.path.realpath(args.out), t, (args.new, args.old))   # before a file is read
    summary, rows = diff(args.new, args.old)
    if args.out:
        write_out(os.path.realpath(args.out), t, summary, rows, (args.new, args.old))
    if args.json:
        print(json.dumps(summary, ensure_ascii=False))
        return 0
    b = summary['buckets']; noc = summary['new_or_changed']; sh = summary['share']
    print(f'{args.new}\n vs {args.old}\n total CJK {summary["total_cjk"]}; ' + '; '.join(f'{k} {v}' for k, v in b.items()))
    print(f" new-or-changed: <0.6 {noc['lt_0.6']}; <0.8 {noc['lt_0.8']}; any change {noc['any_change']}")
    print(f" share of NEW CJK: <0.6 {100 * sh['lt_0.6']:.1f}%; <0.8 {100 * sh['lt_0.8']:.1f}%; any change {100 * sh['any_change']:.1f}%"
          + (f'; rows -> {os.path.realpath(args.out)}/sentences.tsv' if args.out else ''))
    return 0


def build_parser():
    ap = argparse.ArgumentParser(prog='sentence_diff.py', description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('new', nargs='?', metavar='NEW')
    ap.add_argument('old', nargs='?', metavar='OLD')
    ap.add_argument('--json', action='store_true', help='print one JSON object')
    ap.add_argument('--out', default=None, help='write sentences.tsv and summary.json here (inside a task dir)')
    ap.add_argument('--task-dir', default=None, help='the task dir --out must lie in (default: nearest ancestor holding work.json)')
    ap.add_argument('--selftest', action='store_true', help='run the built-in check and exit')
    return ap


def main(argv=None):
    args = build_parser().parse_args(argv)        # unknown arguments: argparse exits 2
    if args.selftest:
        if args.new or args.old or args.out or args.task_dir or args.json:
            print('sentence_diff: refused — --selftest takes no other arguments', file=sys.stderr); return 2
        return selftest()
    if not (args.new and args.old):
        print('sentence_diff: refused — NEW and OLD are required', file=sys.stderr); return 2
    try:
        return run(args)
    except Refused as exc:
        print(f'sentence_diff: refused — {exc}', file=sys.stderr)
        return 2


FX_OLD = '第一句完全相同。第二句话在这里有一些内容\n<!-- 注释里的汉字不算 -->\n第三句将被彻底改写成别的样子！\n'
FX_NEW = '第一句完全相同。<!-- 注释\n跨行 -->第二句话在这里有一些内容呀\n全新的句子与旧稿毫无关系？\n'


def _write(path, text):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)


def _call(argv):
    so, se = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(so), contextlib.redirect_stderr(se):
        try: rc = main(argv)
        except SystemExit as exc: rc = exc.code if isinstance(exc.code, int) else 2
    return rc, so.getvalue(), se.getvalue()


def selftest():
    root = tempfile.mkdtemp(prefix='sentence-diff-selftest-'); res = []
    def check(name, cond): res.append((name, bool(cond)))
    try:
        new, old = os.path.join(root, 'new.md'), os.path.join(root, 'old.md')
        _write(new, FX_NEW); _write(old, FX_OLD)
        task = os.path.join(root, 'task'); os.makedirs(task); _write(os.path.join(task, 'work.json'), '{}')
        out = os.path.join(task, 'results', 'diff')
        rc, so, _ = _call([new, old, '--json', '--out', out])
        s = json.loads(so) if rc == 0 else {}
        check('exit 0', rc == 0)
        check('buckets (comments dropped)', s.get('buckets') == {'verbatim': 7, '>=0.9': 13, '0.8-0.9': 0, '0.6-0.8': 0, '<0.6': 12})
        check('new-or-changed', s.get('new_or_changed') == {'lt_0.6': 12, 'lt_0.8': 12, 'any_change': 25})
        rows = []
        if rc == 0:
            with open(os.path.join(out, 'sentences.tsv'), encoding='utf-8') as f:
                rows = list(csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE))
        check('rows: ids, lines across a multi-line comment, changed flags',
              [(r['id'], r['line'], r['bucket'], r['changed']) for r in rows]
              == [('s0001', '1', 'verbatim', '0'), ('s0002', '2', '>=0.9', '1'), ('s0003', '3', '<0.6', '1')])
        check('old_line of the best match', rows and rows[1]['old_line'] == '1')
        rc2, so2, _ = _call([new, old])
        check('text output keeps the audit lines', rc2 == 0 and ' new-or-changed: <0.6 12; <0.8 12; any change 25' in so2)
        rc3, _, se3 = _call([new, old, '--out', os.path.join(root, 'elsewhere')])
        check('out outside a task dir refused, nothing created', rc3 == 2 and 'refus' in se3 and not os.path.exists(os.path.join(root, 'elsewhere')))
        draft = os.path.join(task, 'draft.md'); _write(draft, FX_NEW)
        alias = os.path.join(task, 'results', 'alias'); os.makedirs(alias)
        os.symlink(draft, os.path.join(alias, 'sentences.tsv'))
        rc3b, _, se3b = _call([draft, old, '--out', alias])
        with open(draft, encoding='utf-8') as f:
            kept = f.read() == FX_NEW
        check('output symlink to the NEW input refused, input unchanged', rc3b == 2 and 'symlink' in se3b and kept
              and os.listdir(alias) == ['sentences.tsv'])
        rc4, _, _ = _call([new, old, '--bogus'])
        check('unknown argument exits 2', rc4 == 2)
        rc5, _, _ = _call([new, os.path.join(root, 'missing.md')])
        check('missing input refused', rc5 == 2)
    finally:
        shutil.rmtree(root, ignore_errors=True)
    bad = [n for n, ok in res if not ok]
    for n, ok in res:
        print(f"  [{'ok' if ok else 'FAIL'}] {n}")
    print(f'sentence_diff selftest: {len(res) - len(bad)}/{len(res)} passed')
    return 0 if not bad else 1


if __name__ == '__main__':
    sys.exit(main())
