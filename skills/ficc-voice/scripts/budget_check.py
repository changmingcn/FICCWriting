#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""budget_check.py (2026-10-24) -- character budget for the FICC rule cards and seat-read files.

Measure: len(text) of each file read as UTF-8 (characters, not bytes).  Caps and their
history live in budget.json next to this script; paths there are relative to its "root".

Usage:
  budget_check.py [check]                        used / cap / headroom per file
  budget_check.py --set-baseline --reason TEXT   every cap := current size, history entry
  budget_check.py --raise PATH N --reason TEXT   one cap := N (N > old cap), history entry
  budget_check.py --selftest                     +1 character on a temp copy of each budgeted
                                                 file must exit 1; then the real check must pass

Exit codes (check): 0 every file within its cap; 1 a file is over its cap; 2 a budgeted file
is missing or budget.json is unreadable.  --set-baseline and --raise exit 2 when refused.
Raise rule (MAINTAINERS.md lesson 19): raise a cap only by the size of a user ruling that no
retired duplicate can house; the reason goes into the history here and into the skill's
provenance.  Checked by shared-protocols/regression/run-local-checks.sh.
"""
import argparse
import datetime
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
BUDGET = os.path.join(HERE, 'budget.json')
RAISE_RULE = ('Raise a cap only by the size of a user ruling that no retired duplicate can house '
              '(reason recorded in the budget history and the skill provenance).')


class BudgetError(Exception):
    pass


def load(path):
    try:
        with open(path, encoding='utf-8') as f:
            b = json.load(f)
    except (OSError, ValueError) as e:
        raise BudgetError('budget.json unreadable: %s (%s)' % (path, e))
    if not isinstance(b, dict) or not isinstance(b.get('files'), dict) or not b['files']:
        raise BudgetError('budget.json has no "files" table: %s' % path)
    for k, v in b['files'].items():
        if not isinstance(v, int) or isinstance(v, bool) or v < 0:
            raise BudgetError('cap for %s is not a non-negative integer: %r' % (k, v))
    b.setdefault('history', [])
    return b


def save(b, path):
    tmp = path + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(b, f, ensure_ascii=False, indent=2)
        f.write('\n')
    os.replace(tmp, path)


def root_of(b):
    return os.path.expanduser(b.get('root') or '~/.claude')


def size(root, rel):
    """Characters of the UTF-8 file, or None when it is missing."""
    p = os.path.join(root, rel)
    if not os.path.isfile(p):
        return None
    with open(p, encoding='utf-8') as f:
        return len(f.read())


def check(b, out=sys.stdout):
    root = root_of(b)
    w = max(len(k) for k in b['files'])
    print('budget_check: %s = %s, root %s' % (b.get('unit', 'chars'), b.get('measure', 'len(text) of the UTF-8 file'),
                                               root), file=out)
    print('%-*s %8s %8s %9s' % (w, 'file', 'used', 'cap', 'headroom'), file=out)
    over, missing = [], []
    for rel, cap in b['files'].items():
        used = size(root, rel)
        if used is None:
            missing.append(rel)
            print('%-*s %8s %8d %9s  MISSING' % (w, rel, '-', cap, '-'), file=out)
            continue
        mark = '  OVER' if used > cap else ''
        if used > cap:
            over.append((rel, used - cap))
        print('%-*s %8d %8d %9d%s' % (w, rel, used, cap, cap - used, mark), file=out)
    if missing:
        print('budget_check: MISSING %s' % ', '.join(missing), file=out)
        return 2
    if over:
        print('budget_check: OVER %s' % ', '.join('%s (+%d)' % o for o in over), file=out)
        print('  ' + RAISE_RULE, file=out)
        return 1
    print('budget_check: OK, %d files within cap' % len(b['files']), file=out)
    return 0


def entry(reason, changes):
    return {'date': datetime.date.today().isoformat(), 'reason': reason, 'changes': changes}


def set_baseline(b, path, reason):
    root = root_of(b)
    changes = {}
    for rel, cap in b['files'].items():
        used = size(root, rel)
        if used is None:
            raise BudgetError('budgeted file missing: %s' % os.path.join(root, rel))
        if used != cap:
            changes[rel] = [cap, used]
    for rel, (old, new) in changes.items():
        b['files'][rel] = new
    b['history'].append(entry(reason, changes))
    save(b, path)
    print('budget_check: baseline set (%d caps changed); history entry appended' % len(changes))
    return 0


def raise_cap(b, path, rel, n, reason):
    if rel not in b['files']:
        raise BudgetError('not a budgeted file: %s' % rel)
    old = b['files'][rel]
    if n <= old:
        raise BudgetError('--raise needs N above the current cap %d (got %d)' % (old, n))
    b['files'][rel] = n
    b['history'].append(entry(reason, {rel: [old, n]}))
    save(b, path)
    print('budget_check: %s cap %d -> %d (+%d); history entry appended' % (rel, old, n, n - old))
    return 0


def selftest(path):
    print('== budget_check selftest')
    b = load(path)
    root = root_of(b)
    ok = True
    tmp = tempfile.mkdtemp(prefix='budget_check-')
    sink = open(os.devnull, 'w')
    try:
        for rel in b['files']:
            src = os.path.join(root, rel)
            if not os.path.isfile(src):
                print('  FAIL %s missing in the live tree' % rel)
                ok = False
                continue
            dst = os.path.join(tmp, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copyfile(src, dst)
            tb = {'root': tmp, 'files': {rel: size(tmp, rel)}, 'history': []}
            same = check(tb, sink)
            with open(dst, 'a', encoding='utf-8') as f:
                f.write('x')
            plus = check(tb, sink)
            good = same == 0 and plus == 1
            ok &= good
            print('  %s %s: copy at cap -> exit %d, +1 character -> exit %d (want 0, 1)'
                  % ('ok  ' if good else 'FAIL', rel, same, plus))
        gone = check({'root': tmp, 'files': {'no/such/file.md': 1}, 'history': []}, sink)
        bad = os.path.join(tmp, 'bad.json')
        with open(bad, 'w', encoding='utf-8') as f:
            f.write('{not json')
        try:
            load(bad)
            unreadable = 0
        except BudgetError:
            unreadable = 2
        good = gone == 2 and unreadable == 2
        ok &= good
        print('  %s missing file -> exit %d, unreadable budget.json -> exit %d (want 2, 2)'
              % ('ok  ' if good else 'FAIL', gone, unreadable))
    finally:
        sink.close()
        shutil.rmtree(tmp, ignore_errors=True)
    print('== real check')
    real = check(b)
    ok &= real == 0
    print('budget_check selftest: %s' % ('PASS' if ok else 'FAIL'))
    return 0 if ok else 1


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog='budget_check.py',
        description='Character budget (len(text) of the UTF-8 file) for the FICC rule cards and '
                    'seat-read files listed in budget.json. Default: check; exit 1 when a file is over '
                    'its cap, 2 when a budgeted file is missing or budget.json is unreadable.',
        epilog=RAISE_RULE)
    ap.add_argument('command', nargs='?', default='check', choices=['check'], help='check (default)')
    ap.add_argument('--budget', default=BUDGET, help='budget file (default: budget.json next to this script)')
    ap.add_argument('--set-baseline', action='store_true', help='set every cap to the current size (needs --reason)')
    ap.add_argument('--raise', dest='raise_', nargs=2, metavar=('PATH', 'N'),
                    help='raise one cap to N characters (needs --reason)')
    ap.add_argument('--reason', help='why the caps change; recorded in the budget history')
    ap.add_argument('--selftest', action='store_true',
                    help='+1 character on a temp copy of each budgeted file must exit 1, then the real check must pass')
    a = ap.parse_args(argv)
    try:
        if a.selftest:
            return selftest(a.budget)
        if (a.set_baseline or a.raise_) and not (a.reason and a.reason.strip()):
            print('budget_check: refused, --set-baseline and --raise need --reason TEXT', file=sys.stderr)
            return 2
        if a.set_baseline and a.raise_:
            print('budget_check: refused, give --set-baseline or --raise, not both', file=sys.stderr)
            return 2
        b = load(a.budget)
        if a.set_baseline:
            return set_baseline(b, a.budget, a.reason.strip())
        if a.raise_:
            rel, n = a.raise_
            try:
                n = int(n)
            except ValueError:
                print('budget_check: refused, N must be an integer: %s' % n, file=sys.stderr)
                return 2
            return raise_cap(b, a.budget, rel, n, a.reason.strip())
        return check(b)
    except BudgetError as e:
        print('budget_check: %s' % e, file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
