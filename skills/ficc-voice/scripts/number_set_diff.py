#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""number_set_diff.py (2026-11-03, wave 3 U09; 2.0.0 fix round r1; 2.1.0 r2; 2.2.0 r3) -- number tokens of a frozen
and a current draft.

Before a re-tick seat is opened after a fix or patch round, compare the numbers of the frozen (ticked) draft with
the current draft, sentence by sentence and in order.  A number token is sign + approximation + number + scale/unit
suffix + approximation: NFKC digits (full-width folded; the Chinese comma kept), thousands commas dropped, decimals
kept; a sign is an explicit + or - or the direction word right before the number (增长/上升/升/涨... -> +,
下降/下跌/降/跌/减/负... -> -; 负增长 -> -, 正增长 -> +); an approximation or comparison marker bound to the number is
kept (约, 近, 超过, 超, 不到, 不足, 低于, 高于, 逾 before it, 超过/超/低于/高于 also with 不, not 最近/附近/靠近; 以上, 以下,
左右, 以内, 以外 after it), so 约5% and 5% differ; the suffix bound to it, compound scales as one (千万亿, 万亿, 千亿, 百亿,
十亿, 千万, 百万, 十万, 亿, 万, 千, 百; then %, ‰, bp, 个百分点, 个点, pp, 倍, 次, 成, 年, 月, 日, 季度, 个月, 周, 天,
currencies, bn/tn/mn, and the counting words 家, 个, 人, 笔), so 3千亿元 and 3千万元 differ; Chinese numerals only with
such a suffix or as a fraction (三成, 两成半, 一半, 三分之一, 三季度, 两年, 两次, 三家, 三千亿元); periods Q1-Q4, H1/H2, 3Q25, 1H26,
FY25/CY25, 上半年/下半年.  `[src: …]` anchors and HTML comments are left out.  Every unit of the changed-sentence
table (changed_sentences.py) must carry the same token sequence as its frozen counterpart: a changed, moved,
moved-seam or punct sentence is compared with the frozen sentence at its old position; a pair whose sequences differ
(value, unit, sign, approximation or order), a changed pair whose pair_confidence is low (changed_sentences.py 2.1.0:
outside its slot range, crossing another pair, or sharing its frozen sentence; whatever its numbers), or an added or deleted
sentence that carries a number, is a difference.  So a swap of two numbers between sentences is a difference: the
pairs in place differ, or the crossed pairs are low (r3).  No difference -> "number sets equal: no
re-tick seat" (source-check.md, Validity of a check: ticks hold while the sentence's facts hold).  Differences ->
only the units listed are re-ticked.
Quantifier short list for T0 (read by a person, never auto-ticked): the changed or added sentences of the current
draft that carry 大半, 多数, 过半, 少数, or 近 before a number or a fraction word (近3成, 近一半; 最近一季, 近期,
更多数据 do not count).
--all-quant lists them over every sentence of the current draft.  --units FILE (one id per line, '#' comments)
restricts the verdict and the quantifier list to those units (dispatch-notes 2.3: the re-tick packet's unit list).
An id is resolved against every sentence of both drafts, changed or not: <stem>.sNNNN (current sentence NNNN),
<stem>.dNNNN (frozen sentence NNNN, deleted or kept: then its current counterpart), <stem>:LINE (every current
sentence on current line LINE, and deleted rows anchored there).  The output counts requested, resolved and
unresolved ids; an unresolved id, or a list that matches no sentence, gives no verdict (never "equal"; exit 3).
Without --units the output opens with a one-line notice that the quantifier list is unscoped.

Usage:
  number_set_diff.py FROZEN CURRENT [--glob 'B*.md'] [--window N] [--all-quant] [--units FILE] [--json]
  number_set_diff.py --self-test
FROZEN and CURRENT: two files or two directories (files matching --glob paired by name, as changed_sentences.py).
--window N: the pairing window of changed_sentences.py (default 2).  Each unit row (--json units, unit_rows) carries
pair_confidence and low_pair.
Exit: 0 number sets equal; 1 a number differs; 2 usage or unreadable input; 3 --units has an unresolved id or
matches nothing (no verdict).
"""
import argparse
import collections
import json
import os
import re
import sys
import tempfile
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import changed_sentences as cs  # noqa: E402

VERSION = '2.2.0'
_CN = '零〇一二三四五六七八九十两百千'
_SCALE = r'(?:千万亿|万亿|千亿|百亿|十亿|千万|百万|十万|亿|万|千|百(?!分))'
_CNSCALE = r'(?:万亿|亿|万)'                # Chinese numerals carry 十/百/千 themselves
# one grammar for both branches (r2, Codex C01): sign? + number + scale? + unit?, where unit lists every multi-character
# unit before its prefix (日元 before 日, 季度 before 季, 个百分点 before 百分点, 成半 before 成)
_CUR = r'(?:美元|欧元|日元|英镑|港元|元)'
_UNIT = (r'(?:' + _CUR + r'|%|‰|\s?bps?(?![A-Za-z])|个百分点|百分点|个点|\s?pp(?![A-Za-z])|倍|次(?!性)|成半|成|个季度|季度|季|'
         r'个月|年(?!代)|月|日|号|周|天|小时|家|个|人(?!民)|笔|'      # r3 (R3): counting words after every 个X unit
         r'\s?(?:bn|tn|mn|trillion|billion|million)(?![A-Za-z]))')
TOKEN = re.compile(
    r'(?P<per>(?<![A-Za-z_\d])\d[QH]\d{2}(?!\d)|(?<![A-Za-z_\d])(?:FY|CY)\d{2,4}(?!\d)|(?<![A-Za-z_])Q[1-4](?!\d)'
    r'|(?<![A-Za-z_])H[12](?!\d)|上半年|下半年)'
    r'|(?P<sign>(?<![A-Za-z_\d.])[+\-])?(?:'
    r'(?P<cn>[%s]+(?:分之[%s]+|半(?!年)|%s%s?|%s))'
    r'|(?P<num>(?<![A-Za-z_\d.])\d+(?:,\d{3})*(?:\.\d+)?)(?P<suf>%s?%s?))'
    % (_CN, _CN, _CNSCALE, _UNIT, _UNIT, _SCALE, _UNIT))
_UP = '正增长|增长|增加|上升|上涨|上调|提高|扩大|走阔|走高|反弹|加息|升|涨|增'   # r3: 正增长, 负增长 read whole
_DOWN = '负增长|下降|下跌|下调|减少|降低|回落|缩小|收窄|走低|下滑|降息|降|跌|减|负'
DIRECTION = re.compile(r'(?:(?P<up>%s)|(?P<down>%s))(?:了|约|近|逾|超过|不到|不足|低于|高于|超|达|至|到){0,2}$'
                       % (_UP, _DOWN))
# 2.1.0: bound to the number, part of the token; 2.2.0 (r3, R3): 不足, 超, 低于, 高于, and 不 before 超过/超/低于/高于
APPROX_PRE = re.compile(r'(?:(?<![最附靠])近|约|不?超过|不?超|不到|不足|不?低于|不?高于|逾)$')
APPROX_POST = re.compile(r'以上|以下|左右|以内|以外')
PERIOD = {'上半年': 'H1', '下半年': 'H2'}
STRIP = re.compile(r'\[src:[^\]]*\]|<!--.*?-->', re.S)
QUANT = re.compile(r'大半|(?<![更很许])多数(?![据字额])|过半|(?<![减缺])少数(?![据字额量])|'
                   r'(?<![最附将靠])近(?=[\d一二三四五六七八九十两半百千万成倍](?![季期月周年日天]))')


def tokens(text):
    """-> ordered list of number tokens (sign + number + suffix; Chinese numerals; periods) in text."""
    t = unicodedata.normalize('NFKC', STRIP.sub('', text).replace('，', '\ue000')).replace('\ue000', '，')
    t = t.replace('−', '-').replace('﹣', '-')
    out = []
    for m in TOKEN.finditer(t):
        if m.group('per'):
            out.append(PERIOD.get(m.group('per'), m.group('per')))
            continue
        if m.group('cn'):
            tok = m.group('cn')
        else:
            tok = m.group('num').replace(',', '') + re.sub(r'\s', '', m.group('suf') or '')
        sign = m.group('sign') or ''           # the same sign rule for Arabic and Chinese numerals (r2, C01)
        if not sign:
            d = DIRECTION.search(t[max(0, m.start() - 6):m.start()])
            sign = ('+' if d.group('up') else '-') if d else ''
        pre = APPROX_PRE.search(t[max(0, m.start() - 3):m.start()])
        post = APPROX_POST.match(t, m.end())
        out.append(sign + (pre.group() if pre else '') + tok + (post.group() if post else ''))
    return out


def nums(text):
    return collections.Counter(tokens(text))


def file_nums(path):
    if not path:
        return collections.Counter()
    with open(path, encoding='utf-8', errors='ignore') as f:
        return nums(f.read())


def _index(rows, stem):
    """{unit id: [rows]} over every sentence of a file pair (compare(..., every=True))."""
    by = {}
    for x in rows:
        keys = {x['id'], '%s:%s' % (stem, x['line'])}
        if x.get('old_index'):
            keys.add('%s.d%04d' % (stem, x['old_index']))
        for k in keys:
            by.setdefault(k, []).append(x)
    return by


def run(frozen, current, glob='*.md', all_quant=False, only=None, window=cs.WINDOW):
    files, units, quant, unit_rows, hit = [], [], [], [], set()
    compared, pairs = 0, {'changed_pairs': 0, 'pairs_with_numbers': 0, 'pairs_numbers_differ': 0, 'low_confidence_pairs': 0}
    for frz, cur, lab in cs.pairs(frozen, current, glob):
        rows, _ = cs.compare(frz, cur, lab, every=only is not None, window=window)
        stem = lab or os.path.splitext(os.path.basename(cur or frz))[0]
        nc, nf = file_nums(cur), file_nums(frz)
        plus, minus = nc - nf, nf - nc
        files.append({'file': stem, 'numbers_current': sum(nc.values()), 'numbers_frozen': sum(nf.values()),
                      'only_current': sorted(plus.elements()), 'only_frozen': sorted(minus.elements())})
        if only is not None:                  # resolve every requested id against every sentence of both drafts
            by, sel = _index(rows, stem), {}
            for u in only:
                for x in by.get(u, []):
                    sel[x['id']] = x
                    hit.add(u)
            rows = sorted(sel.values(), key=lambda x: (x['line'] or 0, x['id']))
        for x in rows:
            if x['kind'] == 'unchanged' and only is None:
                continue
            # the frozen counterpart: a moved, moved-seam, punct or changed sentence is compared with the frozen
            # sentence at its old position (x['old']); added has none; deleted has no current sentence
            t_new = tokens(x['sentence']) if x['kind'] != 'deleted' else []
            t_old = tokens(x.get('old') or '') if x['kind'] != 'added' else []
            low = x.get('pair_confidence') == 'low'      # r3 (R1): a low pair is a difference whatever its numbers
            if t_new or t_old:
                compared += 1
            if only is not None:
                unit_rows.append({'id': x['id'], 'kind': x['kind'], 'line': x['line'], 'old_index': x.get('old_index'),
                                  'pair_confidence': x.get('pair_confidence'), 'frozen': t_old, 'current': t_new})
            if x['kind'] == 'changed':
                pairs['changed_pairs'] += 1
                pairs['pairs_with_numbers'] += bool(t_new or t_old)
                pairs['pairs_numbers_differ'] += t_new != t_old
                pairs['low_confidence_pairs'] += low
            if t_new != t_old or low:
                c_new, c_old = collections.Counter(t_new), collections.Counter(t_old)
                units.append({'id': x['id'], 'line': x['line'], 'kind': x['kind'], 'current': t_new, 'frozen': t_old,
                              'only_current': sorted((c_new - c_old).elements()),
                              'only_frozen': sorted((c_old - c_new).elements()),
                              'order_only': c_new == c_old and t_new != t_old, 'low_pair': low,
                              'pair_confidence': x.get('pair_confidence'), 'old_index': x.get('old_index'),
                              'sentence': x['sentence']})
        pool = [x for x in rows if x['kind'] in ('changed', 'added', 'moved', 'moved-seam', 'punct', 'unchanged')]
        if all_quant and cur and only is None:
            import sentence_diff as sd
            pool = [{'id': '%s.s%04d' % (stem, i + 1), 'line': ln, 'kind': 'any', 'sentence': s}
                    for i, (s, ln) in enumerate(sd.sents(cur))]
        for x in pool:
            q = QUANT.findall(x['sentence'])
            if q:
                quant.append({'id': x['id'], 'line': x['line'], 'kind': x['kind'], 'words': sorted(set(q)),
                              'sentence': x['sentence']})
    differ = [f for f in files if f['only_current'] or f['only_frozen']]
    unresolved = sorted(set(only) - hit) if only is not None else []
    verdict = 'unresolved' if only is not None and (unresolved or not unit_rows) else ('differ' if units else 'equal')
    return {'tool': 'number_set_diff.py', 'version': VERSION, 'frozen': frozen, 'current': current,
            'files': len(files), 'units_with_numbers_compared': compared, 'files_differ': len(differ),
            'number_differences': sum(len(u['only_current']) + len(u['only_frozen']) + (2 if u['order_only'] else 0)
                                      + (1 if u['low_pair'] and u['current'] == u['frozen'] else 0) for u in units),
            'verdict': verdict, 'equal': verdict == 'equal', 'scope': 'units' if only is not None else 'files',
            'units_requested': len(only) if only is not None else None,
            'units_resolved': len(hit) if only is not None else None,
            'units_unresolved': len(unresolved) if only is not None else None, 'unresolved': unresolved,
            'notice': None if only is not None else NOTICE, 'pairs': pairs, 'file_rows': files, 'units': units,
            'unit_rows': unit_rows, 'quantifiers': quant}


NOTICE = ('notice: no --units given; the verdict covers every changed sentence and the quantifier list is unscoped '
          '(pass --units <the re-tick packet\'s unit list>, dispatch-notes 2.3)')


def render(res):
    out = [res['notice']] if res.get('notice') else []
    if res['scope'] == 'units':
        out.append('units: %d requested, %d resolved, %d unresolved%s' % (
            res['units_requested'], res['units_resolved'], res['units_unresolved'],
            (' (' + ', '.join(res['unresolved'][:20]) + (' …' if len(res['unresolved']) > 20 else '') + ')')
            if res['unresolved'] else ''))
    for u in res['units']:
        out.append('  %s L%s %s/%s: frozen [%s] -> current [%s]%s%s %s' % (     # r3: kind/pair_confidence
            u['id'], u['line'], u['kind'], u['pair_confidence'], ', '.join(u['frozen']), ', '.join(u['current']),
            ' (order)' if u['order_only'] else '',
            ' (low-confidence pair with frozen #%s)' % u['old_index'] if u['low_pair'] else '', u['sentence'][:80]))
    out.append('quantifier short list for T0 (%d): ' % len(res['quantifiers']))
    for q in res['quantifiers']:
        out.append('  %s L%s %s [%s] %s' % (q['id'], q['line'], q['kind'], '、'.join(q['words']), q['sentence'][:90]))
    out.append('%d file(s), %d units carrying numbers compared; %s' % (
        res['files'], res['units_with_numbers_compared'],
        'number sets equal: no re-tick seat' if res['verdict'] == 'equal' else
        'no verdict: an id of the unit list is unresolved or the list matches no sentence; fix the list (exit 3)'
        if res['verdict'] == 'unresolved' else
        'number tokens differ in %d %sunit(s)%s; re-tick only those' % (
            len(res['units']), 'listed ' if res['scope'] == 'units' else '',
            ' (%d of them low-confidence pairs)' % sum(u['low_pair'] for u in res['units'])
            if any(u['low_pair'] for u in res['units']) else '')))
    return '\n'.join(out) + '\n'


def selftest():
    import shutil
    d = tempfile.mkdtemp(prefix='nsd-selftest-')
    ok, cases = True, []
    try:
        def put(name, text):
            with open(os.path.join(d, name), 'w', encoding='utf-8') as f:
                f.write(text)
        put('frozen.md', 'CoreWeave的CDS宽到约1,130bp［1］。大半贷款在10月到期。最近利差走阔。\n')
        put('reword.md', 'CoreWeave的CDS（Barclays中值）宽到约1130bp［1］。大半的贷款在10月到期。最近利差走阔了。\n')
        put('changed.md', 'CoreWeave的CDS宽到约1,230bp［1］。大半贷款在10月到期。近3成利差走阔。\n')
        r = run(os.path.join(d, 'frozen.md'), os.path.join(d, 'reword.md'))
        cases.append(('reworded, same numbers (1,130 = 1130): equal', r['equal'] and r['number_differences'] == 0))
        cases.append(('quantifier 大半 in a changed sentence is listed', any('大半' in q['words'] for q in r['quantifiers'])))
        cases.append(('最近 is not a quantifier', not any('最近' in q['sentence'] and q['words'] == ['近'] for q in r['quantifiers'])))
        r = run(os.path.join(d, 'frozen.md'), os.path.join(d, 'changed.md'))
        cases.append(('changed number: differ, located on the unit', not r['equal'] and r['units']
                      and r['units'][0]['only_current'] == ['约1230bp'] and r['units'][0]['only_frozen'] == ['约1130bp']))
        cases.append(('近3成 is a quantifier', any(q['words'] == ['近'] for q in r['quantifiers'])))
        put('anchor.md', 'CoreWeave的CDS宽到约1,130bp［1］[src: N522 L88]。大半贷款在10月到期。最近利差走阔。\n')
        r = run(os.path.join(d, 'frozen.md'), os.path.join(d, 'anchor.md'))
        cases.append(('[src: …] anchors are not numbers', r['equal']))
        cases.append(('exit codes 0 / 1', main([os.path.join(d, 'frozen.md'), os.path.join(d, 'reword.md')], True) == 0
                      and main([os.path.join(d, 'frozen.md'), os.path.join(d, 'changed.md')], True) == 1))
        r = run(os.path.join(d, 'frozen.md'), os.path.join(d, 'changed.md'), only={'changed.s0002'})
        cases.append(('--units: an unchanged-number unit is equal though the file differs', r['equal'] and r['scope'] == 'units'))
        r = run(os.path.join(d, 'frozen.md'), os.path.join(d, 'changed.md'), only={'changed:1'})
        cases.append(('--units: the changed-number unit differs', not r['equal'] and r['units'][0]['only_current'] == ['约1230bp']))
        put('more.md', '更多数据中心租约转成经营租赁。最近一季资本开支超过现金流。占了近一半。\n')
        q = [x['sentence'] for x in run(os.path.join(d, 'frozen.md'), os.path.join(d, 'more.md'))['quantifiers']]
        cases.append(('更多数据 and 最近一季 are not quantifiers; 近一半 is', q == ['占了近一半']))
        cases.append(('unreadable input: exit 2', main([os.path.join(d, 'nope.md'), os.path.join(d, 'x.md')], True) == 2))
        for name, old, new in (('5万 -> 5亿', '规模约5万元。', '规模约5亿元。'), ('5% -> 5bp', '利差走阔了5%。', '利差走阔了5bp。'),
                               ('增长5% -> 下降5%', '营收同比增长5%。', '营收同比下降5%。'), ('-5% -> 5%', '利润率为-5%。', '利润率为5%。'),
                               ('Q3 -> Q4', '资本开支在Q3见顶。', '资本开支在Q4见顶。'), ('三成 -> 四成', '三成贷款到期。', '四成贷款到期。'),
                               ('一半 -> 三分之一', '一半贷款到期。', '三分之一贷款到期。'),
                               ('swap between sentences', '甲行利差是5%。乙行利差是7%。', '甲行利差是7%。乙行利差是5%。')):
            put('p-old.md', old + '\n'); put('p-new.md', new + '\n')
            cases.append(('probe %s: a difference' % name, not run(os.path.join(d, 'p-old.md'), os.path.join(d, 'p-new.md'))['equal']))
        # r2 (T0 follow-up to refuter 05 on F1): compound scales, 负 as a sign, approximation markers, counts
        for name, old, new in (('3千亿元 -> 3千万元', '融资3千亿元。', '融资3千万元。'), ('5千万 -> 5千', '规模5千万。', '规模5千。'),
                               ('负0.1% -> 0.1%', '利率为负0.1%。', '利率为0.1%。'), ('约5% -> 5%', '占比约5%。', '占比5%。'),
                               ('5%以上 -> 5%', '占比5%以上。', '占比5%。'), ('5%左右 -> 5%', '占比5%左右。', '占比5%。'),
                               ('超过5% -> 5%', '占比超过5%。', '占比5%。'), ('不到5% -> 5%', '占比不到5%。', '占比5%。'),
                               ('逾5% -> 5%', '占比逾5%。', '占比5%。'), ('近5% -> 5%', '占比近5%。', '占比5%。'),
                               ('两次 -> 三次', '美联储加息两次。', '美联储加息三次。'), ('三千亿元 -> 三千万元', '融资三千亿元。', '融资三千万元。'),
                               ('+三成 -> -三成', '份额+三成。', '份额-三成。'), ('5季 -> 5', '连续5季走阔。', '连续5走阔。'),
                               ('5日元 -> 5日', '支付5日元。', '支付5日。'), ('三亿元 -> 三亿美元', '融资三亿元。', '融资三亿美元。')):
            put('p-old.md', old + '\n'); put('p-new.md', new + '\n')
            cases.append(('probe %s: a difference' % name, not run(os.path.join(d, 'p-old.md'), os.path.join(d, 'p-new.md'))['equal']))
        cases.append(('最近5年 keeps no approximation marker; 负债 is no sign', tokens('最近5年，负债3亿元。') == ['5年', '3亿元']))
        # r3 (R1): swaps of unequal-length numbers between similar sentences; (R3) markers, comparators, counting words
        for name, old, new in (('swap 15% <-> 7%', '甲行利差是15%。乙行利差是7%。', '甲行利差是7%。乙行利差是15%。'),
                               ('swap 3bp <-> 12bp', '甲行的利差为3bp，比上月窄。乙行的利差为12bp，比上月窄。',
                                '甲行的利差为12bp，比上月窄。乙行的利差为3bp，比上月窄。'),
                               ('swap 1.5亿元 <-> 30亿元', '甲公司发债1.5亿元。乙公司发债30亿元。', '甲公司发债30亿元。乙公司发债1.5亿元。'),
                               ('不足5% -> 5%', '占比不足5%。', '占比5%。'), ('超5% -> 5%', '占比超5%。', '占比5%。'),
                               ('5%以内 -> 5%', '控制在5%以内。', '控制在5%。'), ('5%以外 -> 5%', '波动在5%以外。', '波动在5%。'),
                               ('负增长5% -> 增长5%', '出口负增长5%。', '出口增长5%。'), ('正增长5% -> 负增长5%', '出口正增长5%。', '出口负增长5%。'),
                               ('低于5% -> 5%', '利率低于5%。', '利率5%。'), ('高于5% -> 5%', '利率高于5%。', '利率5%。'),
                               ('不超过5% -> 超过5%', '占比不超过5%。', '占比超过5%。'), ('三家 -> 四家', '三家银行到期。', '四家银行到期。'),
                               ('3家 -> 3', '3家银行到期。', '3银行到期。'), ('三个 -> 四个', '涉及三个项目。', '涉及四个项目。'),
                               ('5人 -> 5', '董事会5人。', '董事会5。'), ('两笔 -> 三笔', '发了两笔贷款。', '发了三笔贷款。')):
            put('p-old.md', old + '\n'); put('p-new.md', new + '\n')
            r = run(os.path.join(d, 'p-old.md'), os.path.join(d, 'p-new.md'))
            cases.append(('probe %s: a difference' % name, not r['equal']
                          and (not name.startswith('swap') or len(r['units']) == 2)))
        cases.append(('r3 tokens: 不足, 超, 以内, 负增长, 低于, 家, 个, 人 (not 人民币), 笔',
                      tokens('不足5%，超3成，2%以内，负增长4%，低于6%，三家，两个，5人，3亿人民币，两笔。')
                      == ['不足5%', '超3成', '2%以内', '-4%', '低于6%', '三家', '两个', '5人', '3亿', '两笔']))
        put('w-old.md', '甲行利差是5%。乙行利差是5%。\n'); put('w-new.md', '甲行利差是5%，较上月持平。乙行利差是5%。\n')
        cases.append(('an in-place reword with the same numbers stays equal (high pair)',
                      run(os.path.join(d, 'w-old.md'), os.path.join(d, 'w-new.md'))['equal']))
        # r2 CX03: --units resolved against every sentence; unresolved or empty -> no verdict (exit 3)
        put('u-frozen.md', '利差是10bp。\n'); put('u-current.md', '利差是20bp。\n')
        put('u-unknown.txt', 'C062\n'); put('u-empty.txt', '# none\n')
        fz, cu = os.path.join(d, 'u-frozen.md'), os.path.join(d, 'u-current.md')
        r = run(fz, cu, only={'C062'})
        cases.append(('--units unknown id: unresolved, never equal, exit 3', r['verdict'] == 'unresolved' and not r['equal']
                      and r['unresolved'] == ['C062'] and main([fz, cu, '--units', os.path.join(d, 'u-unknown.txt')], True) == 3))
        cases.append(('--units empty list: no verdict, exit 3', run(fz, cu, only=set())['verdict'] == 'unresolved'
                      and main([fz, cu, '--units', os.path.join(d, 'u-empty.txt')], True) == 3))
        r = run(fz, cu, only={'u-current.s0001', 'C062'})
        cases.append(('--units one resolved (differs) and one unresolved: no verdict, the difference still listed',
                      r['verdict'] == 'unresolved' and r['units_resolved'] == 1 and r['units'][0]['only_current'] == ['20bp']))
        put('m-frozen.md', '甲行利差是5%。乙行利差是7%。丙行没有数。\n'); put('m-current.md', '乙行利差是7%。丙行没有数。甲行利差是5%。\n')
        fz, cu = os.path.join(d, 'm-frozen.md'), os.path.join(d, 'm-current.md')
        mv = [x['id'] for x in cs.compare(fz, cu)[0] if x['kind'] == 'moved']
        r = run(fz, cu, only=set(mv))
        cases.append(('--units moved sentence: resolved, frozen numbers from its old position, equal',
                      mv and r['verdict'] == 'equal' and r['units_resolved'] == 1
                      and [(u['frozen'], u['current']) for u in r['unit_rows']] == [(['5%'], ['5%'])]))
        r = run(fz, cu, only={'m-current.d0002', 'm-current:1'})
        cases.append(('--units .dNNNN of a kept frozen sentence and a Bxx:line id resolve; unchanged ids count',
                      r['verdict'] == 'equal' and r['units_unresolved'] == 0 and len(r['unit_rows']) == 3))
        cases.append(('identical files: equal, 0 units', (lambda r: r['equal'] and not r['units'])(
            run(os.path.join(d, 'p-new.md'), os.path.join(d, 'p-new.md')))))
        cases.append(('tokens: sign, unit, period, Chinese fraction', tokens('增长５%，-3.5bp的差，1,130亿美元，3Q25与上半年，两成半与三分之一，5,6两项。')
                      == ['+5%', '-3.5bp', '1130亿美元', '3Q25', 'H1', '两成半', '三分之一', '5', '6']))
    finally:
        shutil.rmtree(d, ignore_errors=True)
    for name, good in cases:
        ok &= bool(good)
        print('  %s  %s' % ('PASS' if good else 'FAIL', name))
    print('number_set_diff self-test: %s' % ('all passed' if ok else 'FAILED'))
    return 0 if ok else 1


def main(argv=None, quiet=False):
    ap = argparse.ArgumentParser(prog='number_set_diff.py', description=__doc__.split('\n\n')[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('frozen', nargs='?'); ap.add_argument('current', nargs='?')
    ap.add_argument('--glob', default='*.md')
    ap.add_argument('--window', type=int, default=cs.WINDOW, help='pairing window of changed_sentences.py (default 2)')
    ap.add_argument('--all-quant', action='store_true', help='quantifier list over every current sentence')
    ap.add_argument('--json', action='store_true')
    ap.add_argument('--units', help='file of unit ids (Bxx:line or sentence ids) the verdict covers')
    ap.add_argument('--self-test', '--selftest', action='store_true')
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
        only = None
        if a.units:
            with open(a.units, encoding='utf-8') as f:
                only = {l.split('#')[0].strip() for l in f if l.split('#')[0].strip()}
        res = run(a.frozen, a.current, a.glob, a.all_quant, only, a.window)
    except (cs.sd.Refused, OSError) as e:
        if not quiet:
            print('number_set_diff: %s' % e, file=sys.stderr)
        return 2
    if not quiet:
        sys.stdout.write(json.dumps(res, ensure_ascii=False, indent=1) + '\n' if a.json else render(res))
    return {'equal': 0, 'differ': 1}.get(res['verdict'], 3)


if __name__ == '__main__':
    sys.exit(main())
