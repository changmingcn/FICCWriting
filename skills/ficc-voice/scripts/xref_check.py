# -*- coding: utf-8 -*-
r"""xref_check.py (2026-10-17, wave 4) -- section references must resolve to numbered
headings; V/S/O/C rule numbers must be defined and not retired.

Checks that every reference to a section of FICCOutline.md, FICCStructure.md,
FICCVoice.md or FICCCompose.md (and to a numbered section of any other .md file in
the skill, named by file) points at an existing heading, and that every quoted title
still matches the heading text.  Stdlib only; Python 3.9+.

Usage:
  xref_check.py [--root DIR] [--json] [-q] [--selftest]
  xref_check.py [--root DIR] --selftest-excerpt

Targets: numbered headings "## N title", "### N.M title", "#### N.M.N title" (title
may be absent, as in "## 1.2" of the rationale files).  An unnumbered ## heading
closes the section above it.  Main files: <root>/FICCOutline.md, FICCStructure.md,
FICCVoice.md (required) and FICCCompose.md (optional: when absent, refs to it are
MISSING and C numbers are MISSING-RULE).  A file under references/zh/ that names a main file is checked against
its Chinese mirror references/zh/<F>.md (same numbers, Chinese titles).

Scanned: every *.md and *.py under <root>, except
  references/corpus/                  author texts (regression corpus, not rules)
  references/history.md               historical record: old numbering stays as it was
  references/dev-notes.md             historical development record, body not renumbered
  references/FICCVoice-provenance.md  provenance and migration history, not active rules
  scripts/xref_check.py               this script (its fixtures are deliberately broken)
  symlinks (ficc-voice.md -> FICCVoice.md is scanned once, under its real name)
  hidden directories.
Excluded files are still valid targets; their raw match counts are listed.

Recognised references (F = FICCOutline|FICCStructure|FICCVoice|FICCCompose, optional .md; any
other target must be written as a file name ending .md, optionally with a path;
optional markdown link target "](...)", optional backtick, optional one space):
  N  numbered       F 4 / F 4.2 / F4.2 / F.md 4.2 / dev-notes.md section 35 /
                    dev-notes.md第35节 / FICCVoice 5.1 V29 (V/S/O/C numbers are not
                    sections).  Not refs: a number followed by a digit, ",5", "%",
                    "-5", a measure word (F.md 40条, 3份) or KB/bytes/lines/times.
                    A file name that resolves to no file in the tree, or to a file
                    with no numbered headings, is not a ref (results/J-trees.md第3节).
  Q  quoted title   F “4.2 How to write the outline, and where it goes”: the title
                    must equal the heading title.  Unprefixed “4.2 title” inside a
                    main file (or its zh mirror) is checked against that file; in
                    other files it counts only when it equals a main-file heading.
  +q attached quote F 2「原文……片段」 after a numbered ref: equal to the heading title,
                    or every fragment (split on …… / ...) found in that section's
                    body (in examples-and-rewrites.md also in its own block for that
                    section); otherwise STALE?
  H  headings of references/examples-and-rewrites.md: "## F 4.2" or "## F 4.2 title"
                    (a title, when given, must equal the heading title)
  C  continuation   a list after a recognised ref inherits its file:
                    F 4.3 and 4.5, F 1 to 3, F 1到3, F 3、8, F 2.2, 2.3, F 4.1和7
                    (a range -- to / 到 / 至 / dash -- must ascend: "F 10.3 to 9.3"
                    is a move and stops the list; "，" ends the list)
  B  bare in-file   inside the four main files and their zh mirrors only, resolved
                    against that file: any N.M / N.M.N not preceded by a letter,
                    digit, "." "-" "/" (see 4.2, (2.2, 2.3), the 1.4 table, 见4.2,
                    （4.2）); section 5 / 第5节; a single number right after
                    see / 见 (see 7.  见7。).  Heading lines and fenced code are skipped.
  L  legacy         old Chinese numbering after F (F四（二）, F七, F“七、标题”):
                    always MISSING -- rewrite it as F 4.2 / F 7 / F “7 title”.
  本文件 in examples-and-rewrites.md: a ref right after 本文件 must also be a heading
                    of that file.

Results per ref: the resolved heading, MISSING (no such section / no such heading in
examples-and-rewrites.md / legacy numbering), or STALE? (quoted title or quotation no
longer matches).

Rule numbers (added 2026-10-17): every V\d\d, S\d\d, O\d\d, C\d\d in a scanned file (not
preceded by a letter, digit or "_", not followed by a digit) must be defined as "- **Vnn**"
in FICCVoice.md, "- **Snn**" in FICCStructure.md, "- **Onn**" in FICCOutline.md, "- **Cnn**"
in FICCCompose.md; otherwise MISSING-RULE.  Not checked for rule numbers: the files excluded
above, everything under references/zh/, and references/migration-2026-10-17.md as a whole
(its purpose is the old numbers).  A retired number written as a pointer to its new home,
"Vnn (formerly Snn)", "Cnn (formerly Vnn)", "Cnn (formerly FICCVoice V05, V06)", "Vnn (Snn
merged)" or "Cnn（原 FICCVoice Vnn、Vnn）", is not a ref; the number in front is checked as usual.

Retired numbers (added 2026-10-17, wave 4): a V/S/O definition that is only a pointer line,
"- **V05** → FICCCompose.md C01" with no indented body line under it, retires that number.
Its target (C01) is checked as a ref like any other.  Any other ref to a retired number is
RETIRED-RULE: cite the new number, or write "C01 (formerly V05)".  A pointer line that keeps an
indented body ("- **V08** → FICCCompose.md C13" followed by "  - ...") is still a live rule.
Rationale anchors are exempt (counted, not failed): refs inside references/*-rationale.md
(those files stay keyed by the number a rule had when it was argued), and refs after a
"-rationale.md" mention up to the end of that sentence ("See references/FICCVoice-rationale.md
V06.").

Excerpt (added 2026-10-17, wave 6): references/compose-excerpt.md must copy FICCCompose.md
verbatim before its "## 3" heading.  Checked lines there (fenced code skipped; other lines are
captions and not checked):
  "- Cnn <sentence>"  equals the Compose definition "- **Cnn** **<sentence>**" once "**" is
                      removed (leading and trailing blanks ignored)
  "- <sentence>"      equals the text of some Compose list line "- <sentence>" (any depth)
  "  - <sentence>"    equals the text of some indented Compose list line (indent not counted)
  "| ... |"           equals some Compose table row (leading and trailing blanks ignored)
Results: EXCERPT-MISMATCH (the line has no verbatim Compose counterpart; the report gives the
excerpt line number and the closest Compose line), EXCERPT-MISSING (a C number defined in
FICCCompose.md has no "- Cnn" intent line in excerpt section 1), EXCERPT-MISSING-FILE (root has
FICCCompose.md but no references/compose-excerpt.md).  No FICCCompose.md under the root: excerpt
skipped.
Section 3 (added 2026-10-24): "## 3" and after is not compared word for word; its C numbers go
through the rule-number check above, and its "- C23 ..." lines, taken together, must cite exactly
the C numbers that FICCCompose.md C23's body cites (from "- **C23**" to the next "- **Cnn**" or
"## " line; C23 itself and fenced code left out on both sides; ids read as by the rule-number
check).  Any missing or extra number is one EXCERPT-MISMATCH item, kind ids, on the first "- C23"
line: "C23 ids: missing [..] extra [..]".  No "- C23" line in section 3 is one EXCERPT-MISSING,
kind ids.  FICCCompose.md without a C23 definition: this part skipped.
Key-line completeness (wave 6 patch): each line in EXCERPT_REQUIRED (the limited-grant lead-in,
two C08 sub-lines, the C17 close condition) is recognised by its opening text; some list line
before "## 3" must open with it (its wording is checked line by line above), else
EXCERPT-MISSING "required line ... (Compose Lnn)".  Every table row under C01 in FICCCompose.md
(each table from its header to the first non-"|" line) must appear verbatim in excerpt section
2 ("## 2"), else EXCERPT-MISSING "table row ... (Compose Lnn)"; a row that is there but altered
is EXCERPT-MISMATCH only.  Section 2 must hold as many table rows as C01 has; a surplus left
after the missing rows adds one EXCERPT-MISSING "table rows: ...".  All count as EXCERPT-MISSING.

Exit codes: 0 clean; 1 any MISSING, STALE?, MISSING-RULE, RETIRED-RULE, EXCERPT-MISMATCH,
EXCERPT-MISSING or EXCERPT-MISSING-FILE; 2 usage error (root lacks FICCOutline.md,
FICCStructure.md or FICCVoice.md).
Last line of the text report:
  refs N · MISSING m · STALE? s · rule refs R · MISSING-RULE r · RETIRED-RULE t
    · excerpt lines N · EXCERPT-MISMATCH m · EXCERPT-MISSING k · excerpt §3 C23 ids OK
  (one line; the last item reads OK, MISMATCH, MISSING or skipped as in "Section 3" above;
  " · EXCERPT-MISSING-FILE 1" replaces the section-3 item when the excerpt is missing; " · excerpt
  skipped" instead of the excerpt items when the root has no FICCCompose.md)
Voice excerpts (wave 3, 2026-11-03): each file in VOICE_EXCERPTS (references/voice-excerpt-{patch,polish,draft,
coldread}.md) must copy FICCVoice.md lines verbatim in its section 1 ("**" removed) and hold the intent line of each V
number listed for it; results EXCERPT-MISMATCH / EXCERPT-MISSING / EXCERPT-MISSING-FILE (exit 1), one report line per
file before the last line.  --selftest-excerpt also runs, per voice excerpt, a changed word, a dropped intent line
and a removed file on a temp copy.
--selftest-excerpt (2026-10-24): on a temp copy of --root, drop one C number from the excerpt's
"- C23" lines, add a defined C number C23 does not cite, and drop every "- C23" line; each must
be reported (EXCERPT-MISMATCH ids, EXCERPT-MISSING ids) with exit 1 and no other count changed;
then --root itself must pass (exit 0, section 3 OK).  Exit 0 all passed, 1 otherwise.
When to run: after any change to a heading or a section number of the main files (or of a
numbered reference file), or to a rule definition, before installing.  Details: scripts/README.md.
"""
import argparse
import collections
import difflib
import json
import os
import re
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(HERE)
FILES = ('FICCOutline', 'FICCStructure', 'FICCVoice', 'FICCCompose')
REQUIRED = FILES[:3]   # FICCCompose.md (2026-10-17) is optional: older trees lack it
FNAMES = '|'.join(FILES)
ZH = 'references/zh/'
EXAMPLES = 'references/examples-and-rewrites.md'
EXCLUDE_DIRS = {'references/corpus': 'author texts, not rules'}
EXCLUDE_FILES = {
    'references/history.md': 'historical record, old numbering kept',
    'references/dev-notes.md': 'historical development record',
    'references/FICCVoice-provenance.md': 'historical provenance and rule migration',
    'scripts/xref_check.py': 'this script; fixtures are deliberately broken',
}

NUMS = r'\d{1,2}(?:\.\d{1,2}){0,2}'
MEASURE = '份个条种句层处步件类篇段节章样项次点方者行字倍万亿元年月日天岁遍轮'
# an en dash "–" starts a section range ("6.1–6.4", "1–5") unless the number after it is a quantity
# ("1.5–2.0%", "3–5份", "1–2 KB"; the lookahead pins the whole number, no backtracking into it);
# "-" and "/" before a digit still end the ref
_QTY = r'(?:[0-9%%‰]|[.,][0-9]|[%s]|\s?(?:KB|bytes?|lines?|times|percent)\b)' % MEASURE
GUARD = (r'(?![0-9]|[.,][0-9]|[%%‰]|\s?[-/][0-9]|\s?–\s?(?=(?P<gq>\d{1,2}(?:\.\d{1,2}){0,2}))(?P=gq)%s|\s?–\s?\d{3}|[%s]'
         r'|\s?(?:KB|bytes?|lines?|times|percent)\b)' % (_QTY, MEASURE))
PATH = r'[A-Za-z0-9_~./-]*/'
PFX = (r'(?P<path>(?:%s)?(?:%s)(?![A-Za-z_-])(?:\.md)?'
       r'|(?:%s)?[A-Za-z0-9_-]+\.md)(?:\]\([^)]*\))?`?\s?') % (PATH, FNAMES, PATH)
RREF = re.compile(PFX + r'(?:(?P<sec>[Ss]ections?\s)|(?P<di>第\s?))?(?P<n>%s)(?(di)\s?节)%s'
                  % (NUMS, GUARD))
QT = r'[“"「](?P<qn>%s) (?P<qt>[^”"」\n]{1,80})[”"」]' % NUMS
RQF = re.compile(PFX + QT)
RQB = re.compile(QT)
RH = re.compile(r'^## (%s) (%s)(?:\s+(.*?))?\s*$' % (FNAMES, NUMS))
RQUOTE = re.compile(r'\s?(?:「([^」]{1,60})」|“([^”]{1,60})”|"([^"]{1,60})")')
CN = '一二三四五六七八九十'
OLDM = '份个条种句层处步件类篇段节章样项次点方者'
RLEG = re.compile(r'(?<![A-Za-z0-9_-])(%s)(?:\.md)?(?:\]\([^)]*\))?`?\s?'
                  r'(?:[“"「][%s]{1,2}、[^”"」\n]{1,30}[”"」]|[%s]{1,2}(?![%s%s])(?:（[%s]{1,2}）)?)'
                  % (FNAMES, CN, CN, CN, OLDM, CN))
CONN = r'(?:\s?(?:和|与|及|或|、|到|至|—|–)\s?|,\s(?:(?:and|or)\s)?|\s(?:and|or|to)\s)'   # ", and 8.3" too
RCONT = re.compile('(' + CONN + r')(%s)%s' % (NUMS, GUARD))
RANGE = ('到', '至', '—', '–', 'to')   # a range must ascend: "10.3 to 9.3" is a move, not a range
B_DOT = re.compile(r'(?<![A-Za-z0-9_./\-$¥])(\d{1,2}\.\d{1,2}(?:\.\d{1,2})?)%s' % GUARD)
B_SECT = re.compile(r'(?:(?<![A-Za-z])[Ss]ection\s|(?P<di>第\s?))(\d{1,2}(?:\.\d{1,2}){0,2})(?(di)\s?节)%s' % GUARD)
B_SEE = re.compile(r'(?:(?<=见)|(?<=[Ss]ee ))(\d{1,2})(?=[。，；：）、)\s,.;:]|$|和|与|及)')
HEADNUM = re.compile(r'^#{2,4} (%s)(?:\s+(.*?))?\s*$' % NUMS)
FENCE = re.compile(r'^\s{0,3}(```|~~~)')
RULE_REF = re.compile(r'(?<![A-Za-z0-9_])([VSOC])(\d{2})(?![0-9])')
RULE_DEF = re.compile(r'^\s*-\s+\*\*([VSOC]\d{2})\*\*')
RULE_FILE = {'V': 'FICCVoice.md', 'S': 'FICCStructure.md', 'O': 'FICCOutline.md', 'C': 'FICCCompose.md'}
MIGRATION = 'references/migration-2026-10-17.md'   # old-to-new record: not scanned for rule numbers
_OLDN = r'(?:FICC[A-Za-z]+(?:\.md)?\s?)?[VSO]\d{2}'
RULE_OLD = re.compile(r'\(formerly %s(?:(?:, |、| and )%s)*\)|\([VSO]\d{2} merged\)|（原\s?%s(?:[、，,]\s?%s)*）'
                      % (_OLDN, _OLDN, _OLDN, _OLDN))   # "V43 (formerly S40)", "V05 (S34 merged)", "C01（原 V05）"
# retired number: "- **V05** → FICCCompose.md C01" with no indented body line under it
RULE_PTR = re.compile(r'^\s*-\s+\*\*([VSO]\d{2})\*\*\s*→\s*(?:(FICC[A-Za-z]+)(?:\.md)?\s+)?([VSOC]\d{2})')
RATIONALE = re.compile(r'-rationale\.md\b')        # "references/FICCVoice-rationale.md V06": an anchor there
SENT_END = re.compile(r'。|\.(?=\s|$)')
# compose-excerpt.md vs FICCCompose.md (wave 6)
EXCERPT = 'references/compose-excerpt.md'
EX_C = re.compile(r'^-\s+(C\d{2})\s+(.*?)\s*$')        # excerpt intent line "- C01 <sentence>"
EX_LIST = re.compile(r'^(\s*)-\s+(.*?)\s*$')            # list line; group 1 = indent
EX_SEC1 = re.compile(r'^##\s+1(?:\s|$)')
EX_SEC3 = re.compile(r'^##\s+3(?:\s|$)')
EX_SEC2 = re.compile(r'^##\s+2(?:\s|$)')
C_DEF = re.compile(r'^\s*-\s+\*\*(C\d{2})\*\*')
# key Compose lines the excerpt must keep before "## 3", recognised by opening text (wave 6 patch)
EXCERPT_REQUIRED = (
    'Under a grant limited to splitting or merging paragraphs,',     # lead-in: limited grant
    'When moving to a sub-question that needs its own unfolding,',   # C08
    'Paragraphs: make sure each paragraph has only one topic.',      # C08
    'The whole piece and each part must have a close.',              # C17
)
EX_TABLE_RULE = 'C01'   # every table row under this C number must appear in excerpt section 2
EX_S3_RULE = 'C23'      # excerpt section 3: its "- C23" lines must cite exactly the C ids of C23's body
C_ID = re.compile(r'(?<![A-Za-z0-9_])C\d{2}(?![0-9])')   # a C id as the rule-number check reads it
# FICCVoice mode excerpts vs FICCVoice.md (wave 3 U09/U10, 2026-11-03): every non-blank line of section 1 equals a
# FICCVoice.md line once "**" is removed (blanks at both ends ignored); each listed V number has its intent line there.
VOICE_EXCERPTS = {
    'references/voice-excerpt-patch.md': ('V04', 'V07', 'V10', 'V11', 'V12', 'V13', 'V14', 'V20', 'V24', 'V26', 'V27',
                                          'V28', 'V38', 'V57'),
    'references/voice-excerpt-polish.md': ('V01', 'V02', 'V03', 'V04', 'V07', 'V10', 'V11', 'V12', 'V13', 'V14', 'V15',
                                           'V16', 'V17', 'V18', 'V19', 'V20', 'V21', 'V22', 'V23', 'V24', 'V25', 'V26',
                                           'V27', 'V28', 'V29', 'V30', 'V31', 'V32', 'V33', 'V34', 'V35', 'V36', 'V37',
                                           'V38', 'V39', 'V40', 'V52', 'V53', 'V54', 'V57'),
    'references/voice-excerpt-draft.md': ('V01', 'V02', 'V03', 'V04', 'V26', 'V27', 'V28', 'V38'),
    'references/voice-excerpt-coldread.md': ('V22', 'V23', 'V32', 'V36', 'V37', 'V38', 'V39', 'V40', 'V57'),
}
EX_V = re.compile(r'^-\s+(V\d{2})\s')


def read(path):
    with open(path, encoding='utf-8') as fh:
        return fh.read()


def outline(path):
    """-> (heads {num: title}, bodies {num: text}); a section body includes its subsections."""
    heads, body, cur, fence = {}, {}, None, False
    for l in read(path).split('\n'):
        if FENCE.match(l):
            fence = not fence
        if not fence:
            m = HEADNUM.match(l)
            if m:
                cur = m.group(1)
                heads[cur] = (m.group(2) or '').strip()
                body.setdefault(cur, [])
                continue
            if re.match(r'^#{1,2} ', l):
                cur = None
                continue
        if cur:
            parts = cur.split('.')
            for k in range(1, len(parts) + 1):
                p = '.'.join(parts[:k])
                if p in body:
                    body[p].append(l)
    return heads, {k: '\n'.join(v) for k, v in body.items()}


def exblocks(path):
    """examples-and-rewrites.md: (F, num) -> block text under that ## heading."""
    out, cur = {}, None
    if not os.path.exists(path):
        return out
    for l in read(path).split('\n'):
        m = RH.match(l)
        if m:
            cur = (m.group(1), m.group(2))
            out[cur] = []
            continue
        if l.startswith('## '):
            cur = None
            continue
        if cur:
            out[cur].append(l)
    return {k: '\n'.join(v) for k, v in out.items()}


def quote_in(q, text):
    frags = [x.strip() for x in re.split(r'……|\.\.\.|…', q) if len(x.strip()) >= 2]
    return bool(frags) and all(x in text for x in frags)


def disp(rel):
    """display name of a target: FICCOutline, zh/FICCOutline, or the relative path."""
    stem = rel[:-3]
    if stem in FILES:
        return stem
    if rel.startswith(ZH) and stem[len(ZH):] in FILES:
        return 'zh/' + stem[len(ZH):]
    return rel


def attached_quote(line, pos):
    m = RQUOTE.match(line, pos)
    if not m:
        return None, pos
    return next(g for g in m.groups() if g is not None).strip(), m.end()


def chain(line, pos, prev):
    """Continuations after ref `prev` ending at pos; yields (num, quote, start, end)."""
    out = []
    while True:
        m = RCONT.match(line, pos)
        if not m:
            return out
        if m.group(1).strip() in RANGE and \
                [int(x) for x in m.group(2).split('.')] <= [int(x) for x in prev.split('.')]:
            return out
        q, end = attached_quote(line, m.end())
        out.append((m.group(2), q, m.start(2), end))
        pos, prev = end, m.group(2)


def scan_files(root):
    """-> (scanned rel paths, excluded [(rel, why)], all .md rel paths)"""
    scanned, excluded, allmd = [], [], []
    for d, dirs, files in os.walk(root):
        reld = os.path.relpath(d, root).replace(os.sep, '/')
        reld = '' if reld == '.' else reld
        keep = []
        for x in sorted(dirs):
            rx = (reld + '/' + x) if reld else x
            if x.startswith('.'):
                continue
            if rx in EXCLUDE_DIRS:
                for dd, _, ff in os.walk(os.path.join(d, x)):
                    for fn in sorted(ff):
                        if fn.endswith(('.md', '.py')):
                            excluded.append((os.path.relpath(os.path.join(dd, fn), root).replace(os.sep, '/'),
                                             EXCLUDE_DIRS[rx]))
                continue
            keep.append(x)
        dirs[:] = keep
        for fn in sorted(files):
            if not fn.endswith(('.md', '.py')):
                continue
            rel = (reld + '/' + fn) if reld else fn
            p = os.path.join(d, fn)
            if fn.endswith('.md') and not os.path.islink(p):
                allmd.append(rel)
            if os.path.islink(p):
                excluded.append((rel, 'symlink -> %s' % os.readlink(p)))
            elif rel in EXCLUDE_FILES:
                excluded.append((rel, EXCLUDE_FILES[rel]))
            else:
                scanned.append(rel)
    return sorted(scanned), sorted(excluded), allmd


def _nearest(text, cands):
    """-> (line, text, similarity) of the candidate closest to text, or (None, '', 0.0)."""
    best = (None, '', 0.0)
    for no, c in cands:
        sm = difflib.SequenceMatcher(None, text, c, autojunk=False)
        if sm.real_quick_ratio() <= best[2] or sm.quick_ratio() <= best[2]:
            continue
        r = sm.ratio()
        if r > best[2]:
            best = (no, c, r)
    return best[0], best[1], round(best[2], 2)


def check_excerpt(root, required=EXCERPT_REQUIRED):
    """compose-excerpt.md before "## 3" must copy FICCCompose.md verbatim, section 1 must hold
    an intent line for every C number, the lines opening with `required` must be there and section
    2 must hold every C01 table row; section 3 is checked by check_excerpt_s3.  -> None when root
    has no FICCCompose.md, else {file, lines, items, missing, missing_file, required, table_rows,
    sec3}; items are the checked excerpt lines (plus one kind-ids item on a section-3 mismatch);
    missing entries carry kind rule | required | table | table-count | ids."""
    cp = os.path.join(root, 'FICCCompose.md')
    if not os.path.isfile(cp):
        return None
    out = {'file': EXCERPT, 'lines': 0, 'items': [], 'missing': [], 'missing_file': False,
           'required': [], 'table_rows': None, 'sec3': None}
    ep = os.path.join(root, EXCERPT)
    if not os.path.isfile(ep):
        out['missing_file'] = True
        return out
    cdef, lists, subs, tables, fence = {}, [], [], [], False
    cur, trows = None, []              # cur: C number whose body we are in; trows: its table rows
    for no, l in enumerate(read(cp).split('\n'), 1):
        if FENCE.match(l):
            fence = not fence
            continue
        if fence:
            continue
        if l.startswith('## '):
            cur = None
        m = C_DEF.match(l)
        if m:
            cur = m.group(1)
        if m and m.group(1) not in cdef:
            cdef[m.group(1)] = (no, l.strip()[1:].replace('**', '').strip())   # "C01 <sentence>"
        m = EX_LIST.match(l)
        if m:
            lists.append((no, m.group(2)))
            if m.group(1):
                subs.append((no, m.group(2)))
        elif l.strip().startswith('|'):
            tables.append((no, l.strip()))
            if cur == EX_TABLE_RULE:
                trows.append((no, l.strip()))
    sets = {'list': set(t for _, t in lists), 'sub': set(t for _, t in subs),
            'table': set(t for _, t in tables)}
    pools = {'C': sorted(cdef.values()), 'list': lists, 'sub': subs, 'table': tables}
    seen, in1, in2, sec2, fence = set(), False, False, [], False
    for no, l in enumerate(read(ep).split('\n'), 1):
        if FENCE.match(l):
            fence = not fence
            continue
        if fence:
            continue
        if EX_SEC3.match(l):
            break
        if l.startswith('## '):
            in1, in2 = bool(EX_SEC1.match(l)), bool(EX_SEC2.match(l))
            continue
        st = l.strip()
        mc, ml = EX_C.match(l), EX_LIST.match(l)
        if mc:
            kind, text = 'C', ('%s %s' % (mc.group(1), mc.group(2))).replace('**', '').strip()
            if in1:
                seen.add(mc.group(1))
            want = cdef.get(mc.group(1))
            ok = bool(want) and want[1] == text
            near = (want[0], want[1], round(difflib.SequenceMatcher(None, text, want[1]).ratio(), 2)) \
                if want else _nearest(text, pools['C'])
        elif ml:
            kind, text = ('sub' if ml.group(1) else 'list'), ml.group(2)
            ok = text in sets[kind]
            near = None if ok else _nearest(text, pools[kind])
        elif st.startswith('|'):
            kind, text = 'table', st
            ok = text in sets['table']
            near = None if ok else _nearest(text, pools['table'])
        else:
            continue
        item = {'line': no, 'kind': kind, 'text': text, 'result': 'OK' if ok else 'EXCERPT-MISMATCH'}
        if not ok:
            item.update(nearest_line=near[0], nearest=near[1], similarity=near[2],
                        note='' if kind != 'C' or mc.group(1) in cdef
                        else '%s is not defined in FICCCompose.md' % mc.group(1))
        out['items'].append(item)
        if in2 and kind == 'table':
            sec2.append(item)
    out['lines'] = len(out['items'])
    for c in sorted(cdef):
        if c not in seen:
            out['missing'].append({'kind': 'rule', 'rule': c, 'compose_line': cdef[c][0],
                                   'result': 'EXCERPT-MISSING', 'text': cdef[c][1]})
    # key lines: present when some list line before "## 3" opens with the text (wording: MISMATCH above)
    for pre in required:
        src = next(((n, x) for n, x in lists if x.startswith(pre)), None)
        hit = next((x['line'] for x in out['items'] if x['kind'] in ('list', 'sub')
                    and x['text'].startswith(pre)), None)
        out['required'].append({'prefix': pre, 'compose_line': src[0] if src else None, 'excerpt_line': hit})
        if src is None or hit is None:
            out['missing'].append({
                'kind': 'required', 'compose_line': src[0] if src else None, 'result': 'EXCERPT-MISSING',
                'text': src[1] if src else pre,
                'detail': 'required line "%s" (%s)' % (pre, ('Compose L%d' % src[0]) if src else
                                                       'not in FICCCompose.md: update EXCERPT_REQUIRED')})
    # C01 tables: every row verbatim in section 2; a row present but altered is MISMATCH only
    pool = collections.Counter(x['text'] for x in sec2 if x['result'] == 'OK')
    alt = collections.Counter(x['nearest'] for x in sec2 if x['result'] != 'OK')
    gone = 0
    for n, x in trows:
        if pool[x]:
            pool[x] -= 1
        elif alt[x]:
            alt[x] -= 1
        else:
            gone += 1
            out['missing'].append({'kind': 'table', 'compose_line': n, 'result': 'EXCERPT-MISSING', 'text': x,
                                   'detail': 'table row "%s" (Compose L%d)' % (snip(x, 70), n)})
    span = ('Compose L%d–L%d' % (trows[0][0], trows[-1][0])) if trows else 'no table in FICCCompose.md'
    out['table_rows'] = {'rule': EX_TABLE_RULE, 'compose': len(trows), 'excerpt': len(sec2), 'span': span}
    if len(sec2) + gone != len(trows):
        out['missing'].append({'kind': 'table-count', 'compose_line': trows[0][0] if trows else None,
                               'result': 'EXCERPT-MISSING', 'text': '',
                               'detail': 'table rows: excerpt section 2 has %d, %s tables have %d (%s)' % (
                                   len(sec2), EX_TABLE_RULE, len(trows), span)})
    # section 3 (2026-10-24): the "- C23" lines must cite exactly the C ids of C23's body
    s3 = out['sec3'] = check_excerpt_s3(cp, ep)
    if s3 and s3['result'] == 'EXCERPT-MISMATCH':
        out['items'].append({'line': s3['lines'][0], 'kind': 'ids', 'result': 'EXCERPT-MISMATCH',
                             'text': '%s ids: missing [%s] extra [%s]' % (
                                 s3['rule'], ', '.join(s3['missing']), ', '.join(s3['extra'])),
                             'note': s3['where']})
    elif s3 and s3['result'] == 'EXCERPT-MISSING':
        out['missing'].append({'kind': 'ids', 'compose_line': s3['compose_span'][0], 'result': 'EXCERPT-MISSING',
                               'text': '', 'detail': 'no "- %s" line in excerpt section 3 (%s cites %s)' % (
                                   s3['rule'], s3['where'], ', '.join(s3['required']) or 'no C id')})
    return out


def check_excerpt_s3(compose_path, excerpt_path, rule=EX_S3_RULE):
    """Excerpt section 3 ("## 3" to the end) against one Compose rule (2026-10-24): the C ids on
    the excerpt's "- C23" lines, taken together, must equal the C ids in FICCCompose.md C23's body
    (from "- **C23**" to the next "- **Cnn**" or "## " line); C23 itself and fenced code are left
    out on both sides.  -> None when FICCCompose.md defines no C23, else {rule, compose_span,
    required, lines, found, missing, extra, where, result}; result OK | EXCERPT-MISMATCH (an id
    missing or extra) | EXCERPT-MISSING (no "- C23" line in section 3)."""
    ids = lambda l: set(C_ID.findall(l)) - {rule}
    req, span, fence = set(), None, False
    for no, l in enumerate(read(compose_path).split('\n'), 1):
        if FENCE.match(l):
            fence = not fence
            continue
        if fence:
            continue
        m = C_DEF.match(l)
        if span and (m or l.startswith('## ')):
            break
        if m and m.group(1) == rule:
            span = [no, no]
        if span:
            req |= ids(l)
            if l.strip():
                span[1] = no
    if span is None:
        return None
    line_re = re.compile(r'^-\s+%s\s' % re.escape(rule))
    found, lines, in3, fence = set(), [], False, False
    for no, l in enumerate(read(excerpt_path).split('\n'), 1):
        if FENCE.match(l):
            fence = not fence
            continue
        if fence:
            continue
        if EX_SEC3.match(l):
            in3 = True
        elif in3 and line_re.match(l):
            lines.append(no)
            found |= ids(l)
    missing, extra = sorted(req - found), sorted(found - req)
    where = 'FICCCompose.md %s L%d–L%d' % (rule, span[0], span[1])
    if lines:
        where = 'excerpt section 3 "- %s" lines %s vs %s' % (rule, ', '.join('L%d' % n for n in lines), where)
    return {'rule': rule, 'compose_span': span, 'required': sorted(req), 'lines': lines,
            'found': sorted(found), 'missing': missing, 'extra': extra, 'where': where,
            'result': 'EXCERPT-MISSING' if not lines else 'EXCERPT-MISMATCH' if missing or extra else 'OK'}


def check_voice_excerpts(root, table=None):
    """FICCVoice mode excerpts (wave 3): section 1 ("## 1" to the next "## ") of each file in VOICE_EXCERPTS must copy
    FICCVoice.md lines verbatim ("**" removed, blanks at both ends ignored, fenced code skipped) and hold the intent
    line "- Vnn ..." of each V number listed for it.  -> [] when root has no FICCVoice.md, else one dict per file:
    {file, lines, mismatch [(line, text)], missing [V], required, missing_file}."""
    vp = os.path.join(root, 'FICCVoice.md')
    if not os.path.isfile(vp):
        return []
    pool = {l.replace('**', '').strip() for l in read(vp).split('\n') if l.strip()}
    out = []
    for rel, req in sorted((table or VOICE_EXCERPTS).items()):
        r = {'file': rel, 'lines': 0, 'mismatch': [], 'missing': [], 'required': list(req), 'missing_file': False}
        ep = os.path.join(root, rel)
        if not os.path.isfile(ep):
            r['missing_file'] = True
            out.append(r)
            continue
        in1, fence, seen = False, False, set()
        for no, l in enumerate(read(ep).split('\n'), 1):
            if FENCE.match(l):
                fence = not fence
                continue
            if fence:
                continue
            if l.startswith('## '):
                in1 = bool(EX_SEC1.match(l))
                continue
            if not in1 or not l.strip():
                continue
            r['lines'] += 1
            if l.strip() not in pool:
                r['mismatch'].append((no, l.strip()))
            m = EX_V.match(l)
            if m:
                seen.add(m.group(1))
        r['missing'] = [v for v in req if v not in seen]
        out.append(r)
    return out


def selftest_voice_excerpts(root=SKILL_DIR):
    """--selftest-excerpt, part 2 (wave 3): on a temp copy of root, per voice excerpt: one word changed in a section-1
    line -> EXCERPT-MISMATCH; one required intent line dropped -> EXCERPT-MISSING; the file removed ->
    EXCERPT-MISSING-FILE; each with exit 1.  Then root itself must pass.  -> 0 or 1."""
    print('== voice excerpt selftest (%d files vs FICCVoice.md; temp copy of %s)' % (len(VOICE_EXCERPTS), root))
    live = check(root)
    ok = live['exit_code'] == 0 and all(v['lines'] and not (v['mismatch'] or v['missing'] or v['missing_file'])
                                        for v in live['voice_excerpts'])
    tmp = tempfile.mkdtemp(prefix='xref_voice_')
    try:
        dst = os.path.join(tmp, 'skill')
        shutil.copytree(root, dst, symlinks=True, ignore=shutil.ignore_patterns('.*', '__pycache__'))
        for rel, req in sorted(VOICE_EXCERPTS.items()):
            path = os.path.join(dst, rel)
            orig = read(path)
            rows = orig.split('\n')
            vline = next(i for i, l in enumerate(rows) if EX_V.match(l) and EX_V.match(l).group(1) == req[0])
            changed = list(rows)
            changed[vline] = changed[vline].rstrip('.') + ' always.'
            dropped = [l for i, l in enumerate(rows) if i != vline]
            for name, text, key in (('one word changed at L%d' % (vline + 1), changed, 'voice_mismatch'),
                                    ('%s intent line dropped' % req[0], dropped, 'voice_missing'),
                                    ('file removed', None, 'voice_missing_file')):
                if text is None:
                    os.remove(path)
                else:
                    with open(path, 'w', encoding='utf-8') as fh:
                        fh.write('\n'.join(text))
                res = check(dst)
                c = res['counts']
                good = res['exit_code'] == 1 and c[key] >= 1 and all(
                    c[k] == live['counts'][k] for k in ('missing', 'stale', 'missing_rule', 'excerpt_mismatch',
                                                        'excerpt_missing', 'excerpt_missing_file'))
                ok &= good
                print('  %s  %s: %s -> %s (exit %d)' % ('PASS' if good else 'FAIL', rel, name, key, res['exit_code']))
                with open(path, 'w', encoding='utf-8') as fh:
                    fh.write(orig)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print('  %s  live tree passes (exit %d; voice excerpts %s)' % (
        'PASS' if ok else 'FAIL', live['exit_code'],
        ', '.join('%s %d lines' % (os.path.basename(v['file']), v['lines']) for v in live['voice_excerpts'])))
    print('selftest-excerpt (voice): %s' % ('all passed' if ok else 'FAILED'))
    return 0 if ok else 1


def check(root):
    root = os.path.abspath(os.path.expanduser(root))
    for f in REQUIRED:
        if not os.path.isfile(os.path.join(root, f + '.md')):
            raise IOError('not a ficc-voice root (no %s.md): %s' % (f, root))
    scanned, excluded, allmd = scan_files(root)
    cache = {}

    def target(rel):
        if rel not in cache:
            p = os.path.join(root, rel)
            cache[rel] = outline(p) if os.path.isfile(p) else ({}, {})
        return cache[rel]

    def main_view(f, src):
        """main file F as seen from src: the zh mirror for files under references/zh/."""
        if src.startswith(ZH) and os.path.isfile(os.path.join(root, ZH + f + '.md')):
            return ZH + f + '.md'
        return f + '.md'

    def resolve_path(path, src):
        """path text of a ref -> target rel, or None when it names no numbered file here."""
        p = path.replace('\\', '/')
        stem = os.path.basename(p)
        stem = stem[:-3] if stem.endswith('.md') else stem
        if stem in FILES:
            return ZH + stem + '.md' if '/zh/' in '/' + p else main_view(stem, src)
        for mark in ('skills/ficc-voice/', '.claude/skills/ficc-voice/'):
            if mark in p:
                p = p.split(mark, 1)[1]
        if '/skills/' in p or p.startswith('/'):
            return None
        while p.startswith(('./', '../')):
            p = p[2:] if p.startswith('./') else p[3:]
        cands = [p, os.path.normpath(os.path.join(os.path.dirname(src), p)).replace(os.sep, '/')]
        if '/' not in p:
            cands = ([ZH + p] if src.startswith(ZH) else []) + ['references/' + p, p] + \
                    [x for x in allmd if x.rsplit('/', 1)[-1] == p]
        for c in cands:
            if c in allmd or (c.endswith('.md') and os.path.isfile(os.path.join(root, c))):
                return c if target(c)[0] else None
        return None

    exb = exblocks(os.path.join(root, EXAMPLES))
    refs, per = [], []
    bare = {}
    # rule numbers: "- **Vnn**" in FICCVoice.md, "- **Snn**" in FICCStructure.md, "- **Onn**" in FICCOutline.md,
    # "- **Cnn**" in FICCCompose.md; a V/S/O definition that is only a pointer line retires its number
    defined, retired = {}, {}
    for letter, fname in RULE_FILE.items():
        fp = os.path.join(root, fname)
        lines = read(fp).split('\n') if os.path.isfile(fp) else []
        defined[letter] = {m.group(1) for m in (RULE_DEF.match(l) for l in lines) if m and m.group(1)[0] == letter}
        for i, l in enumerate(lines):
            m = RULE_PTR.match(l)
            if m and m.group(1)[0] == letter and not re.match(r'^\s+\S', lines[i + 1] if i + 1 < len(lines) else ''):
                new = m.group(3)
                retired[m.group(1)] = {'to': '%s %s' % (RULE_FILE[new[0]], new), 'new': new,
                                       'at': '%s L%d' % (fname, i + 1)}
    rules = []

    def scan_rules(rel, text):
        if rel.startswith(ZH) or rel == MIGRATION:
            return
        whole_anchor = bool(re.search(r'(?:^|/)[^/]*-rationale\.md$', rel))
        for i, l in enumerate(text.split('\n'), 1):
            old = [(m.start(), m.end()) for m in RULE_OLD.finditer(l)]
            anchor = []
            for m in RATIONALE.finditer(l):
                e = SENT_END.search(l, m.end())
                anchor.append((m.end(), e.start() if e else len(l)))
            d = RULE_DEF.match(l)
            own_def = d.start(1) if d and RULE_FILE[d.group(1)[0]] == rel else -1  # the definition itself is not a ref
            for m in RULE_REF.finditer(l):
                if m.start() == own_def or any(a <= m.start() < b for a, b in old):
                    continue
                rid = m.group(0)
                r = {'file': rel, 'line': i, 'ref': rid, 'result': 'OK', 'note': ''}
                if rid not in defined[m.group(1)]:
                    r['result'] = 'MISSING-RULE'
                    r['note'] = 'no "- **%s**" in %s' % (rid, RULE_FILE[m.group(1)])
                elif rid in retired:
                    t = retired[rid]
                    if whole_anchor or any(a <= m.start() < b for a, b in anchor):
                        r['note'] = 'retired -> %s; rationale anchor' % t['to']
                        r['anchor'] = True
                    else:
                        r['result'] = 'RETIRED-RULE'
                        r['note'] = '%s is a pointer to %s (%s); cite %s, or write "%s (formerly %s)"' % (
                            rid, t['to'], t['at'], t['new'], t['new'], rid)
                rules.append(r)

    def resolve(rel, i, kind, tgt, num, raw, quote, local):
        H, B = target(tgt)
        name = disp(tgt)
        r = {'file': rel, 'line': i, 'kind': kind, 'raw': raw.strip(), 'target': tgt,
             'ref': '%s %s' % (name, num), 'quote': quote, 'result': 'OK', 'heading': None, 'note': ''}
        if kind == 'L':
            r['result'] = 'MISSING'
            r['ref'] = raw.strip()
            r['note'] = 'old Chinese numbering; rewrite with the current number (F 4.2, F 7)'
        elif num not in H:
            r['result'] = 'MISSING'
            r['note'] = 'no section %s in %s' % (num, tgt)
        else:
            title = H[num]
            r['heading'] = ('%s %s %s' % (name, num, title)).strip()
            if quote is not None and quote != title:
                if kind in ('Q', 'H'):
                    r['result'] = 'STALE?'
                    r['note'] = 'title “%s” ≠ heading “%s”' % (quote, title)
                elif quote_in(quote, B.get(num, '')):
                    r['note'] = 'quote found in section body'
                elif rel == EXAMPLES and quote_in(quote, exb.get((name, num), '')):
                    r['note'] = 'quote found in examples-and-rewrites.md block'
                else:
                    r['result'] = 'STALE?'
                    r['note'] = 'quote “%s” is neither the heading title nor in the section body' % quote
            if local and r['result'] == 'OK':
                if (name, num) not in exb:
                    r['result'] = 'MISSING'
                    r['note'] = '本文件: no heading ## %s %s in examples-and-rewrites.md' % (name, num)
                else:
                    r['note'] = (r['note'] + '; ' if r['note'] else '') + '本文件 heading OK'
        refs.append(r)

    for rel in scanned:
        text = read(os.path.join(root, rel))
        scan_rules(rel, text)
        stem = rel[:-3] if rel.endswith('.md') else None
        own = rel if (stem in FILES or (rel.startswith(ZH) and stem and stem[len(ZH):] in FILES)) else None
        is_ex = rel == EXAMPLES
        start_n = len(refs)
        fence = False
        for i, l in enumerate(text.split('\n'), 1):
            if rel.endswith('.md') and FENCE.match(l):
                fence = not fence
                continue
            spans, found = [], []  # found: (kind, target, num, quote, raw, start, end, local)

            def free(s):
                return not any(a <= s < b for a, b in spans)

            mh = RH.match(l) if is_ex else None
            if mh:
                found.append(('H', mh.group(1) + '.md', mh.group(2), (mh.group(3) or '').strip() or None,
                              mh.group(0), 0, len(l), False))
                spans.append((0, len(l)))
            else:
                for m in RLEG.finditer(l):
                    found.append(('L', m.group(1) + '.md', '', None, m.group(0), m.start(), m.end(), False))
                    spans.append((m.start(), m.end()))
                for m in RQF.finditer(l):
                    if not free(m.start()):
                        continue
                    tgt = resolve_path(m.group('path'), rel)
                    if tgt:
                        found.append(('Q', tgt, m.group('qn'), m.group('qt').strip(), m.group(0),
                                      m.start(), m.end(), False))
                        spans.append((m.start(), m.end()))
                for m in RREF.finditer(l):
                    if not free(m.start()):
                        continue
                    tgt = resolve_path(m.group('path'), rel)
                    if not tgt:
                        continue
                    q, end = attached_quote(l, m.end())
                    local = is_ex and l[max(0, m.start() - 3):m.start()] == '本文件'
                    found.append(('N', tgt, m.group('n'), q, l[m.start():end], m.start(), end, local))
                    spans.append((m.start(), end))
                    for cn, cq, cs, ce in chain(l, end, m.group('n')):
                        found.append(('C', tgt, cn, cq, l[cs:ce], cs, ce, False))
                        spans.append((cs, ce))
                for m in RQB.finditer(l):
                    if not free(m.start()):
                        continue
                    num, title = m.group('qn'), m.group('qt').strip()
                    if own:
                        found.append(('Q', own, num, title, m.group(0), m.start(), m.end(), False))
                        spans.append((m.start(), m.end()))
                        continue
                    for f in FILES:
                        mv = main_view(f, rel)
                        if target(mv)[0].get(num) == title:
                            found.append(('Q', mv, num, title, m.group(0), m.start(), m.end(), False))
                            spans.append((m.start(), m.end()))
                            break
                if own and not fence and not l.startswith('#'):
                    for rx, g in ((B_SECT, 2), (B_DOT, 1), (B_SEE, 1)):
                        for m in rx.finditer(l):
                            if not free(m.start()):
                                continue
                            q, end = attached_quote(l, m.end())
                            found.append(('B', own, m.group(g), q, l[m.start():end], m.start(), end, False))
                            spans.append((m.start(), end))
                            bare[own] = bare.get(own, 0) + 1
                            for cn, cq, cs, ce in chain(l, end, m.group(g)):
                                found.append(('B', own, cn, cq, l[cs:ce], cs, ce, False))
                                spans.append((cs, ce))
                                bare[own] += 1
            for kind, tgt, num, q, raw, s, e, local in sorted(found, key=lambda x: x[5]):
                resolve(rel, i, kind, tgt, num, raw, q, local)
        mine = refs[start_n:]
        if mine:
            per.append({'file': rel, 'refs': len(mine),
                        'missing': sum(r['result'] == 'MISSING' for r in mine),
                        'stale': sum(r['result'] == 'STALE?' for r in mine)})
    ex_list = []
    for rel, why in excluded:
        try:
            t = read(os.path.join(root, rel))
        except (UnicodeDecodeError, IOError, OSError):
            continue
        c = len(RREF.findall(t)) + len(RQF.findall(t)) + len(RLEG.findall(t))
        ex_list.append({'file': rel, 'why': why, 'raw_matches': c})
    n = len(refs)
    miss = sum(r['result'] == 'MISSING' for r in refs)
    stale = sum(r['result'] == 'STALE?' for r in refs)
    miss_rule = sum(r['result'] == 'MISSING-RULE' for r in rules)
    ret_rule = sum(r['result'] == 'RETIRED-RULE' for r in rules)
    vex = check_voice_excerpts(root)
    exc = check_excerpt(root)
    ex_mis = sum(1 for x in exc['items'] if x['result'] != 'OK') if exc else 0
    ex_miss = len(exc['missing']) if exc else 0
    ex_file = 1 if exc and exc['missing_file'] else 0
    return {'root': root, 'refs': refs, 'per_file': per, 'excluded': ex_list,
            'bare': bare, 'rules': rules,
            'rules_defined': {k: len(v) for k, v in defined.items()},
            'rules_retired': {k: v['to'] for k, v in sorted(retired.items())},
            'excerpt': exc, 'voice_excerpts': vex,
            'counts': {'refs': n, 'missing': miss, 'stale': stale, 'bare': sum(bare.values()),
                       'rule_refs': len(rules), 'missing_rule': miss_rule, 'retired_rule': ret_rule,
                       'retired_anchor': sum(1 for r in rules if r.get('anchor')),
                       'excerpt_lines': exc['lines'] if exc else 0, 'excerpt_mismatch': ex_mis,
                       'excerpt_missing': ex_miss, 'excerpt_missing_file': ex_file,
                       'excerpt_skipped': exc is None,
                       'voice_mismatch': sum(len(v['mismatch']) for v in vex),
                       'voice_missing': sum(len(v['missing']) for v in vex),
                       'voice_missing_file': sum(1 for v in vex if v['missing_file'])},
            'exit_code': 1 if (miss or stale or miss_rule or ret_rule or ex_mis or ex_miss or ex_file
                               or any(v['mismatch'] or v['missing'] or v['missing_file'] for v in vex)) else 0}


def render(res, quiet=False):
    out = ['root: %s' % res['root']]
    byfile = {}
    for r in res['refs']:
        byfile.setdefault(r['file'], []).append(r)
    for p in res['per_file']:
        rows = byfile[p['file']]
        if quiet and not (p['missing'] or p['stale']):
            continue
        out.append('== %s  (refs %d, MISSING %d, STALE? %d)' % (p['file'], p['refs'], p['missing'], p['stale']))
        for r in rows:
            if quiet and r['result'] == 'OK':
                continue
            res_txt = r['heading'] if r['result'] == 'OK' else (
                r['result'] + ('  [%s]' % r['heading'] if r['heading'] else ''))
            out.append('  L%d [%s] %s -> %s%s' % (r['line'], r['kind'], r['raw'], res_txt,
                                                   ('  (%s)' % r['note']) if r['note'] else ''))
    if res['excluded']:
        out.append('')
        out.append('== excluded (not checked)')
        for x in res['excluded']:
            out.append('  %s  (%s; %d raw matches)' % (x['file'], x['why'], x['raw_matches']))
    out.append('')
    b = res['bare']
    out.append('bare in-file refs recognised: %d (%s)' % (
        res['counts']['bare'], ', '.join('%s %d' % (disp(f), b[f]) for f in sorted(b)) or 'none'))
    c = res['counts']
    bad = [r for r in res['rules'] if r['result'] != 'OK']
    d = res['rules_defined']
    out.append('rule numbers: %d refs to V/S/O/C (defined V %d, S %d, O %d, C %d; retired to pointers %d); '
               'MISSING-RULE %d; RETIRED-RULE %d (rationale anchors to retired numbers, not failed: %d)' % (
                   c['rule_refs'], d.get('V', 0), d.get('S', 0), d.get('O', 0), d.get('C', 0),
                   len(res['rules_retired']), c['missing_rule'], c['retired_rule'], c['retired_anchor']))
    for r in bad:
        out.append('  %s L%d %s -> %s  (%s)' % (r['file'], r['line'], r['ref'], r['result'], r['note']))
    exc = res.get('excerpt')
    tail = ''
    if exc is None:
        out.append('excerpt: skipped (no FICCCompose.md under the root)')
        tail = ' · excerpt skipped'
    elif exc['missing_file']:
        out.append('excerpt: %s -> EXCERPT-MISSING-FILE' % exc['file'])
        tail = ' · excerpt lines 0 · EXCERPT-MISMATCH 0 · EXCERPT-MISSING 0 · EXCERPT-MISSING-FILE 1'
    else:
        tr = exc.get('table_rows') or {'rule': EX_TABLE_RULE, 'compose': 0, 'excerpt': 0}
        out.append('excerpt %s: %d lines before "## 3" checked against FICCCompose.md; '
                   'EXCERPT-MISMATCH %d; EXCERPT-MISSING %d; required lines %d/%d; %s table rows %d of %d' % (
                       exc['file'], exc['lines'], c['excerpt_mismatch'], c['excerpt_missing'],
                       sum(1 for r in exc.get('required', []) if r['compose_line'] and r['excerpt_line']),
                       len(exc.get('required', [])), tr['rule'], tr['excerpt'], tr['compose']))
        s3 = exc.get('sec3')
        if s3 is None:
            out.append('excerpt section 3: %s ids skipped (FICCCompose.md defines no %s)' % (EX_S3_RULE, EX_S3_RULE))
            s3_tail = ' · excerpt §3 %s ids skipped' % EX_S3_RULE
        else:
            out.append('excerpt section 3: "- %s" lines %s cite %s; FICCCompose.md %s (L%d–L%d) cites %s -> %s' % (
                s3['rule'], ', '.join('L%d' % n for n in s3['lines']) or 'none', ', '.join(s3['found']) or 'none',
                s3['rule'], s3['compose_span'][0], s3['compose_span'][1], ', '.join(s3['required']) or 'none',
                s3['result']))
            s3_tail = ' · excerpt §3 %s ids %s' % (s3['rule'], s3['result'].replace('EXCERPT-', ''))
        for x in exc['items']:
            if x['result'] == 'OK':
                continue
            if x['kind'] == 'ids':
                out.append('  L%d [ids] %s -> EXCERPT-MISMATCH  (%s)' % (x['line'], x['text'], x['note']))
                continue
            out.append('  L%d [%s] %s -> EXCERPT-MISMATCH%s' % (
                x['line'], x['kind'], snip(x['text']), ('  (%s)' % x['note']) if x.get('note') else ''))
            out.append('      closest FICCCompose.md %s (similarity %.2f): %s' % (
                ('L%d' % x['nearest_line']) if x['nearest_line'] else '-', x['similarity'],
                snip(x['nearest']) or '-'))
        for x in exc['missing']:
            if x.get('kind', 'rule') != 'rule':
                out.append('  %s -> EXCERPT-MISSING' % x['detail'])
                continue
            out.append('  %s (FICCCompose.md L%d) -> EXCERPT-MISSING  (no "- %s" intent line in excerpt section 1)'
                       % (x['rule'], x['compose_line'], x['rule']))
        tail = ' · excerpt lines %d · EXCERPT-MISMATCH %d · EXCERPT-MISSING %d%s' % (
            exc['lines'], c['excerpt_mismatch'], c['excerpt_missing'], s3_tail)
    for v in res.get('voice_excerpts') or []:
        if v['missing_file']:
            out.append('voice excerpt %s -> EXCERPT-MISSING-FILE' % v['file'])
            continue
        out.append('voice excerpt %s: %d section-1 lines checked against FICCVoice.md; EXCERPT-MISMATCH %d; '
                   'EXCERPT-MISSING %d (V intent lines %d of %d)' % (v['file'], v['lines'], len(v['mismatch']),
                                                                   len(v['missing']), len(v['required']) - len(v['missing']),
                                                                   len(v['required'])))
        for no, text in v['mismatch']:
            out.append('  L%d -> EXCERPT-MISMATCH  %s' % (no, snip(text)))
        for vn in v['missing']:
            out.append('  %s -> EXCERPT-MISSING  (no "- %s" intent line in section 1)' % (vn, vn))
    out.append('refs %d · MISSING %d · STALE? %d · rule refs %d · MISSING-RULE %d · RETIRED-RULE %d%s' % (
        c['refs'], c['missing'], c['stale'], c['rule_refs'], c['missing_rule'], c['retired_rule'], tail))
    return '\n'.join(out)


def snip(s, n=110):
    return s if len(s) <= n else s[:n] + '...'


# ---------------------------------------------------------------------------
# selftest: tiny fixture written to a temp dir
# ---------------------------------------------------------------------------
FIXTURE = {
    'FICCOutline.md': '# FICCOutline\n\n## 1 The outline is a tree\n\nBody, see 1.2.\n\n### 1.1 Nodes\n\nBody.\n\n'
                      '### 1.2 Position\n\nBody; “1.2 Position” is quoted.\n\n## 2 Root claim\n\n'
                      'Section 2 of this file; back to (2.1). Moved from FICCOutline 2.1 to 1.2.\n\n### 2.1 Define the question\n\nBody.\n'
                      '\n- **O01** **Write the claim first.** See V02 and S01.\n'
                      'Yields of 1.5–2.0% are data, not sections; see 1.1–1.2, and 2.\n',
    'FICCStructure.md': '# FICCStructure\n\n## 1 Set position\n\nSee FICCOutline.md 2.1 and 1.2; FICCOutline 1到2.\n\n'
                        '### 1.1 Ask the task\n\nBody.\n\n- **S01** **Ask the task.** Not a rule: V02a? RV05, V123, S01x.\n',
    'FICCVoice.md': '# FICCVoice\n\n## 1 Who speaks\n\nBody.\n\n## 2 How to state a judgment\n\nBody, 我们认为.\n'
                    '\n- **V02** **State the judgment.**\n'
                    '- **V05** → FICCCompose.md C01\n'
                    '- **V06** → FICCCompose.md C98\n'
                    '- **V08** → FICCCompose.md C01\n'
                    '  - The marker word stays here.\n',
    'FICCCompose.md': '# FICCCompose\n\n## 1 Paragraph openings\n\nSee 1.1 and C01.\n\n### 1.1 Opening\n\n'
                      '- **C01** **Conclusion first.** See references/FICCVoice-rationale.md Introduction and V05. Not V05.\n',
    'references/FICCVoice-rationale.md': '# rationale\n\n## V05\n\nSupports: V05 at every layer.\n',
    'SKILL.md': '# skill\n\n'
                'GOOD: FICCOutline.md 1.2.\n\n'
                'GOOD2: FICCOutline 1.1; FICCVoice1; FICCVoice 2 V02.\n\n'
                'MISS: FICCOutline.md 9.1.\n\n'
                'STALE: FICCVoice.md “2 An old title”.\n\n'
                'TITLE: FICCOutline “2.1 Define the question”.\n\n'
                'QUOTE: FICCVoice 2「我们认为」; FICCVoice.md 40条 and FICCOutline 43,828 are not refs.\n\n'
                'DEV: references/dev-notes.md section 2; dev-notes.md第1节; results/J-trees.md第3节.\n\n'
                'LEGACY: FICCOutline.md四（二）; FICCOutline三份 is a measure word.\n\n'
                'RULES: O01 and S01 resolve; V99 is a deliberately broken rule number; O02 is defined nowhere.\n\n'
                'RETIRED: V02 (formerly S38); V02 (S34 merged); bare S38 is still a broken ref.\n\n'
                'COMPOSE: FICCCompose.md 1.1 and FICCCompose 9; C01 resolves; C99 is a broken C number; V05 is retired; '
                'C01 (formerly V05), C01 (formerly FICCVoice V05, V06) and C01（原 FICCVoice V05、V06） are pointers; '
                'V08 keeps a body.\n\n'
                'RANGE: FICCOutline.md 1.1–1.2, and 2.1; FICCOutline 1–3份 is a quantity.\n',
    'references/migration-2026-10-17.md': '# Migration\n\n| Old | New |\n|---|---|\n| V77 | V02 |\n\n'
                                          'Prose line: V88 is checked.\n',
    'references/zh/FICCOutline.md': '# FICCOutline\n\n## 1 提纲是一棵树\n\n见1.2；“1.2 位置”。\n\n### 1.1 节点\n\n'
                                    '### 1.2 位置\n\n## 2 根主旨\n\n### 2.1 界定问题\n\n旧条号 V66 不查。\n',
    'references/examples-and-rewrites.md': '## FICCOutline 1.1\n\n例。\n\n## FICCVoice 2 How to state a judgment\n\n'
                                           '例，见本文件FICCOutline 1.1。\n',
    'references/dev-notes.md': '# dev\n\n## 1 One\n\n## 2 Two\n\n旧编号 FICCOutline.md九（九） 不查。旧条号 S55 不查。\n',
    'references/history.md': 'Old FICCOutline.md 9.9 is not checked.\n',
    'references/FICCVoice-provenance.md': 'Old title FICCVoice.md “7 Check tone”. Old number FICCVoice.md 9.9.\n',
}


def selftest():
    tmp = tempfile.mkdtemp(prefix='xref_selftest_')
    ok = True
    try:
        for rel, txt in FIXTURE.items():
            p = os.path.join(tmp, rel)
            if not os.path.isdir(os.path.dirname(p)):
                os.makedirs(os.path.dirname(p))
            with open(p, 'w', encoding='utf-8') as fh:
                fh.write(txt)
        res = check(tmp)
        print(render(res))
        print()

        def find(file_, raw_prefix, kind=None):
            return [r for r in res['refs'] if r['file'] == file_ and r['raw'].startswith(raw_prefix)
                    and (kind is None or r['kind'] == kind)]

        cases = [
            ('good ref F.md 4.2-style resolves', find('SKILL.md', 'FICCOutline.md 1.2'), 'OK'),
            ('F 1.1 without .md resolves', find('SKILL.md', 'FICCOutline 1.1'), 'OK'),
            ('F1 without space resolves', find('SKILL.md', 'FICCVoice1'), 'OK'),
            ('F 2 V02: V number is not a section',
             [r for r in find('SKILL.md', 'FICCVoice 2') if r['line'] == 5], 'OK'),
            ('deliberate broken link -> MISSING', find('SKILL.md', 'FICCOutline.md 9.1'), 'MISSING'),
            ('stale quoted title -> STALE?', find('SKILL.md', 'FICCVoice.md “2 An old title”'), 'STALE?'),
            ('quoted new title equals heading', find('SKILL.md', 'FICCOutline “2.1'), 'OK'),
            ('quote found in section body -> OK', find('SKILL.md', 'FICCVoice 2「我们认为」'), 'OK'),
            ('dev-notes.md section 2 resolves', find('SKILL.md', 'references/dev-notes.md section 2'), 'OK'),
            ('dev-notes.md第1节 resolves', find('SKILL.md', 'dev-notes.md第1节'), 'OK'),
            ('legacy F四（二） -> MISSING', find('SKILL.md', 'FICCOutline.md四（二）'), 'MISSING'),
            ('bare see 1.2 resolves in own file',
             [r for r in find('FICCOutline.md', '1.2', 'B') if r['line'] == 5], 'OK'),
            ('bare section 2 resolves in own file', find('FICCOutline.md', 'Section 2'), 'OK'),
            ('bare (2.1) resolves in own file', find('FICCOutline.md', '2.1'), 'OK'),
            ('unprefixed quoted title in own file', find('FICCOutline.md', '“1.2 Position”'), 'OK'),
            ('continuation "2.1 and 1.2" inherits FICCOutline',
             [r for r in find('FICCStructure.md', '1.2') if r['target'] == 'FICCOutline.md'], 'OK'),
            ('descending "2.1 to 1.2" is a move, not a range',
             [r for r in find('FICCOutline.md', '1.2') if r['kind'] == 'C'], 'no ref'),
            ('continuation 1到2 inherits FICCOutline',
             [r for r in find('FICCStructure.md', '2') if r['kind'] == 'C' and r['ref'] == 'FICCOutline 2'], 'OK'),
            ('zh mirror: bare 见1.2 against zh headings', find('references/zh/FICCOutline.md', '1.2', 'B'), 'OK'),
            ('zh mirror: quoted Chinese title', find('references/zh/FICCOutline.md', '“1.2 位置”'), 'OK'),
            ('example heading ## FICCOutline 1.1 -> OK',
             find('references/examples-and-rewrites.md', '## FICCOutline 1.1'), 'OK'),
            ('example heading with title -> OK',
             find('references/examples-and-rewrites.md', '## FICCVoice 2'), 'OK'),
            ('本文件 ref finds an example heading',
             find('references/examples-and-rewrites.md', 'FICCOutline 1.1', 'N'), 'OK'),
            ('FICCCompose.md 1.1 resolves', find('SKILL.md', 'FICCCompose.md 1.1'), 'OK'),
            ('FICCCompose 9 -> MISSING', find('SKILL.md', 'FICCCompose 9'), 'MISSING'),
            ('bare see 1.1 resolves inside FICCCompose.md', find('FICCCompose.md', '1.1', 'B'), 'OK'),
        ]
        for name, rows, want in cases:
            good = (not rows) if want == 'no ref' else (len(rows) == 1 and rows[0]['result'] == want)
            ok &= good
            print('  %s  %s (want %s, got %s)' % ('PASS' if good else 'FAIL', name, want,
                                                 [r['result'] for r in rows] or 'no ref'))
        raws = [r['raw'] for r in res['refs']]
        extra = [
            ('measure words / thousands are not refs (40条, 43,828, 三份)',
             not any(x.startswith(('FICCVoice.md 40', 'FICCOutline 43', 'FICCOutline三')) for x in raws)),
            ('V02 is not a ref', not any('V02' in x for x in raws)),
            ('a file outside the tree is not a ref (J-trees.md第3节)', not any('J-trees' in x for x in raws)),
            ('history.md excluded', not any(r['file'] == 'references/history.md' for r in res['refs'])),
            ('dev-notes.md excluded from scanning, still a target',
             not any(r['file'] == 'references/dev-notes.md' for r in res['refs'])),
            ('Voice provenance excluded; raw matches retained',
             not any(r['file'] == 'references/FICCVoice-provenance.md' for r in res['refs'])
             and any(x['file'] == 'references/FICCVoice-provenance.md' and x['raw_matches'] == 2
                     for x in res['excluded'])),
            ('en-dash range "1.1–1.2" and Oxford ", and 2.1" continue a prefixed ref; "1–3份" is a quantity',
             sorted(r['raw'] for r in res['refs'] if r['file'] == 'SKILL.md' and r['line'] == 25
                    and r['result'] == 'OK') == ['1.2', '2.1', 'FICCOutline.md 1.1']
             and len([r for r in res['refs'] if r['file'] == 'SKILL.md' and r['line'] == 25]) == 3),
            ('bare "see 1.1–1.2, and 2" resolves in own file; "1.5–2.0%" is data, not a ref',
             sorted(r['raw'] for r in res['refs'] if r['file'] == 'FICCOutline.md' and r['line'] == 24)
             == ['1.1', '1.2', '2'] and all(r['result'] == 'OK' for r in res['refs']
                                            if r['file'] == 'FICCOutline.md' and r['line'] == 24)),
            ('counts 3 MISSING (broken link + legacy + FICCCompose 9), 1 STALE?',
             (res['counts']['missing'], res['counts']['stale']) == (3, 1)),
            ('exit code 1', res['exit_code'] == 1),
        ]
        rr = res['rules']

        def rule(file_, rid):
            return [r['result'] for r in rr if r['file'] == file_ and r['ref'] == rid]

        extra += [
            ('rule number O01 defined in FICCOutline.md -> OK', rule('SKILL.md', 'O01') == ['OK']),
            ('rule number S01 defined in FICCStructure.md -> OK', rule('SKILL.md', 'S01') == ['OK']),
            ('V02 next to a section ref is a rule ref, defined -> OK',
             [r['result'] for r in rr if r['file'] == 'SKILL.md' and r['line'] == 5 and r['ref'] == 'V02'] == ['OK']),
            ('bad rule number V99 -> MISSING-RULE', rule('SKILL.md', 'V99') == ['MISSING-RULE']),
            ('undefined O02 -> MISSING-RULE', rule('SKILL.md', 'O02') == ['MISSING-RULE']),
            ('RV05 and V123 are not rule refs; V02a and S01x count as V02, S01; a definition line is not a ref',
             not any(r['ref'] in ('V12', 'V05') for r in rr if r['file'] == 'FICCStructure.md')
             and rule('FICCStructure.md', 'V02') == ['OK']
             and rule('FICCStructure.md', 'S01') == ['OK']),
            ('migration file not scanned for rule numbers (table V77, prose V88)',
             not any(r['file'] == 'references/migration-2026-10-17.md' for r in rr)),
            ('"(formerly S38)" and "(S34 merged)" are not refs; bare S38 is MISSING-RULE; V02 in front is checked',
             rule('SKILL.md', 'S34') == [] and rule('SKILL.md', 'S38') == ['MISSING-RULE']
             and [r['result'] for r in rr if r['file'] == 'SKILL.md' and r['line'] == 21 and r['ref'] == 'V02']
             == ['OK', 'OK']),
            ('references/zh/ and dev-notes.md not scanned for rule numbers (V66, S55)',
             not any(r['ref'] in ('V66', 'S55') for r in rr)),
            ('C01 defined in FICCCompose.md -> OK; C99 -> MISSING-RULE',
             [r['result'] for r in rr if r['file'] == 'SKILL.md' and r['line'] == 23 and r['ref'] == 'C01']
             == ['OK'] * 4 and rule('SKILL.md', 'C99') == ['MISSING-RULE']),
            ('pointer line target is checked: V06 -> C98 undefined -> MISSING-RULE; V05 -> C01 -> OK',
             rule('FICCVoice.md', 'C98') == ['MISSING-RULE'] and rule('FICCVoice.md', 'C01') == ['OK', 'OK']),
            ('pointer-only V05 is retired: bare V05 -> RETIRED-RULE; V05 in "(formerly ...)" / "（原 ...）" not refs',
             rule('SKILL.md', 'V05') == ['RETIRED-RULE'] and rule('SKILL.md', 'V06') == []),
            ('pointer line with an indented body (V08) is still live -> OK', rule('SKILL.md', 'V08') == ['OK']),
            ('rationale anchors: V05 after "-rationale.md" in the same sentence, and inside *-rationale.md, '
             'are not failed; V05 in the next sentence is',
             rule('FICCCompose.md', 'V05') == ['OK', 'RETIRED-RULE']
             and rule('references/FICCVoice-rationale.md', 'V05') == ['OK', 'OK']),
            ('counts 5 MISSING-RULE (V99, O02, bare S38, C99, C98), 2 RETIRED-RULE, 3 rationale anchors',
             (res['counts']['missing_rule'], res['counts']['retired_rule'], res['counts']['retired_anchor'])
             == (5, 2, 3)),
            ('retired map: V05 and V06 (pointer-only, even with a broken target); V08 (has a body) is not',
             sorted(res['rules_retired']) == ['V05', 'V06']),
            ('FICCCompose.md without references/compose-excerpt.md -> one EXCERPT-MISSING-FILE',
             res['excerpt']['missing_file'] and res['counts']['excerpt_missing_file'] == 1
             and render(res).split('\n')[-1].endswith('EXCERPT-MISSING-FILE 1')),
        ]
        for name, good in extra:
            ok &= good
            print('  %s  %s' % ('PASS' if good else 'FAIL', name))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    ok &= selftest_excerpt()
    print('selftest: %s' % ('all passed' if ok else 'FAILED'))
    return 0 if ok else 1


EX_COMPOSE = ('# FICCCompose\n\n## 1 Openings\n\n'
              '- Under a limited grant, add no sentences.\n\n'
              '- **C01** **Conclusion first. Do not open empty.**\n'
              '  - Give the whole first.\n\n'
              '    | Row | Type | What the opening states |\n'
              '    |---|---|---|\n'
              '    | 1 | Argument | The claim plus its main reasons. |\n'
              '    | 5 | Case box | The story or facts first. |\n\n'
              '- **C02** **Test the opening item by item.**\n'
              '  - Close every part.\n\n'
              '## 7 Checks\n\n- **C03** **Check again on the finished draft.**\n')
EX_REQUIRED = ('Under a limited grant,', 'Close every part.')   # Compose L5 (lead-in), L16 (sub-line)
EX_GOOD = ('# Excerpt\n\nSections 1-2 copy FICCCompose.md verbatim.\n\n## 1 Intent lines\n\n'
           '- Under a limited grant, add no sentences.\n'
           '- C01 Conclusion first. Do not open empty.\n'
           '  - Give the whole first.\n'
           '- C02 Test the opening item by item.\n'
           '  - Close every part.\n'
           '- C03 Check again on the finished draft.\n\n'
           '## 2 Tables\n\nCaption lines are not checked:\n\n'
           '| Row | Type | What the opening states |\n|---|---|---|\n'
           '| 1 | Argument | The claim plus its main reasons. |\n'
           '| 5 | Case box | The story or facts first. |\n\n'
           '## 3 Checks\n\n- C01 Condensed lines after section 3 are not compared.\n')


def _ex_missing(exc):
    return [(x['kind'], x.get('rule') or x['compose_line']) for x in exc['missing']]


def selftest_excerpt():
    """seven excerpt cases, each in its own minimal temp root (FICCCompose.md + the excerpt)."""
    print()
    print('excerpt check (references/compose-excerpt.md vs FICCCompose.md):')
    near = lambda line: (lambda exc, bad: bad[0]['nearest_line'] == line and bad[0]['similarity'] > 0.5)
    cases = [
        ('intent lines, sub-lines and table rows copied verbatim -> OK', EX_GOOD, 0, 0, 10, None),
        ('one word changed in an intent line -> EXCERPT-MISMATCH',
         EX_GOOD.replace('- C01 Conclusion first.', '- C01 Conclusion last.'), 1, 0, 10, near(7)),
        ('one C number dropped from section 1 -> EXCERPT-MISSING',
         EX_GOOD.replace('- C03 Check again on the finished draft.\n', ''), 0, 1, 9,
         lambda exc, bad: _ex_missing(exc) == [('rule', 'C03')]),
        ('a table row with one extra cell -> EXCERPT-MISMATCH (not also MISSING)',
         EX_GOOD.replace('main reasons. |\n', 'main reasons. | extra |\n'), 1, 0, 10, near(12)),
        ('the required close sub-line dropped -> EXCERPT-MISSING required line',
         EX_GOOD.replace('  - Close every part.\n', ''), 0, 1, 9,
         lambda exc, bad: _ex_missing(exc) == [('required', 16)]
         and exc['missing'][0]['detail'] == 'required line "Close every part." (Compose L16)'),
        ('one C01 table row dropped -> EXCERPT-MISSING table row',
         EX_GOOD.replace('| 5 | Case box | The story or facts first. |\n', ''), 0, 1, 9,
         lambda exc, bad: _ex_missing(exc) == [('table', 13)]
         and exc['missing'][0]['detail'].endswith('(Compose L13)')),
        ('key lines and every C01 table row present -> EXCERPT-MISSING 0', EX_GOOD, 0, 0, 10,
         lambda exc, bad: [r['excerpt_line'] for r in exc['required']] == [7, 11]
         and (exc['table_rows']['compose'], exc['table_rows']['excerpt']) == (4, 4)),
    ]
    ok = True
    for name, text, want_mis, want_miss, want_lines, extra in cases:
        tmp = tempfile.mkdtemp(prefix='xref_excerpt_')
        try:
            os.makedirs(os.path.join(tmp, 'references'))
            for rel, txt in (('FICCCompose.md', EX_COMPOSE), (EXCERPT, text)):
                with open(os.path.join(tmp, rel), 'w', encoding='utf-8') as fh:
                    fh.write(txt)
            exc = check_excerpt(tmp, required=EX_REQUIRED)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        bad = [x for x in exc['items'] if x['result'] != 'OK']
        good = (len(bad), len(exc['missing']), exc['lines']) == (want_mis, want_miss, want_lines)
        if good and extra:
            good = bool(extra(exc, bad))
        ok &= good
        print('  %s  %s (want mismatch %d, missing %d, lines %d; got %d, %d, %d%s)' % (
            'PASS' if good else 'FAIL', name, want_mis, want_miss, want_lines, len(bad),
            len(exc['missing']), exc['lines'],
            ('; closest L%s' % bad[0]['nearest_line']) if bad else
            ('; %s' % exc['missing'][0].get('detail', exc['missing'][0].get('rule'))) if exc['missing'] else ''))
    return ok


def _without(line, c):
    """line with one C id removed together with its separator: "(C04, C20)" -> "(C04)"."""
    for pat in (r',\s*%s(?![0-9])' % c, r'(?<![A-Za-z0-9_])%s,\s*' % c, r'\s*\(%s\)' % c,
                r'(?<![A-Za-z0-9_])%s(?![0-9])' % c):
        new = re.sub(pat, '', line, count=1)
        if new != line:
            return new
    return line


def selftest_excerpt_s3(root=SKILL_DIR):
    """--selftest-excerpt (2026-10-24): section 3 of the excerpt against C23, on a temp copy of root.
    Drop one C id from the "- C23" lines, add a defined C id that C23 does not cite, drop every
    "- C23" line: each must be reported (EXCERPT-MISMATCH ids / EXCERPT-MISSING ids) with exit 1 and
    no other count changed; then root itself must pass (exit 0, section 3 OK).  -> 0 or 1."""
    print('== excerpt section 3 selftest (%s "- %s" lines vs FICCCompose.md %s; temp copy of %s)'
          % (EXCERPT, EX_S3_RULE, EX_S3_RULE, root))
    live = check(root)
    s3 = (live.get('excerpt') or {}).get('sec3')
    if not s3 or not s3['lines']:
        print('  FAIL  no FICCCompose.md %s or no "- %s" line in excerpt section 3 under the root'
              % (EX_S3_RULE, EX_S3_RULE))
        print('selftest-excerpt: FAILED')
        return 1
    rows = read(os.path.join(root, EXCERPT)).split('\n')
    last = s3['lines'][-1] - 1                                  # 0-based index of the last "- C23" line
    drop = [c for c in C_ID.findall(rows[last]) if c != EX_S3_RULE][-1]
    defined = sorted(m.group(1) for m in map(C_DEF.match, read(os.path.join(root, 'FICCCompose.md')).split('\n')) if m)
    add = next(c for c in defined if c != EX_S3_RULE and c not in s3['required'])
    dropped = list(rows)
    for n in s3['lines']:
        while drop in C_ID.findall(dropped[n - 1]):
            dropped[n - 1] = _without(dropped[n - 1], drop)
    added = list(rows)
    k = added[last].rfind(')')
    added[last] = (added[last][:k] + ', %s' % add + added[last][k:]) if k >= 0 else added[last] + ' (%s)' % add
    removed = [l for i, l in enumerate(rows, 1) if i not in s3['lines']]
    keep = ('missing', 'stale', 'missing_rule', 'retired_rule', 'excerpt_missing_file')
    lc = live['counts']
    cases = [
        ('one id (%s) dropped from the "- %s" lines -> EXCERPT-MISMATCH ids, exit 1' % (drop, EX_S3_RULE),
         dropped, 'EXCERPT-MISMATCH', [drop], [], ('excerpt_mismatch', 1)),
        ('an extra defined id (%s) added to L%d -> EXCERPT-MISMATCH ids, exit 1' % (add, last + 1),
         added, 'EXCERPT-MISMATCH', [], [add], ('excerpt_mismatch', 1)),
        ('every "- %s" line dropped from section 3 -> EXCERPT-MISSING ids, exit 1' % EX_S3_RULE,
         removed, 'EXCERPT-MISSING', s3['required'], [], ('excerpt_missing', 1)),
    ]
    ok = True
    tmp = tempfile.mkdtemp(prefix='xref_excerpt_s3_')
    try:
        dst = os.path.join(tmp, 'skill')
        shutil.copytree(root, dst, symlinks=True, ignore=shutil.ignore_patterns('.*', '__pycache__'))
        for name, text, want, w_miss, w_extra, (key, inc) in cases:
            with open(os.path.join(dst, EXCERPT), 'w', encoding='utf-8') as fh:
                fh.write('\n'.join(text))
            res = check(dst)
            r3, c = res['excerpt']['sec3'], res['counts']
            tail = render(res).split('\n')[-1]
            good = (r3['result'] == want and r3['missing'] == w_miss and r3['extra'] == w_extra
                    and res['exit_code'] == 1 and c[key] == lc[key] + inc
                    and all(c[x] == lc[x] for x in keep)
                    and tail.endswith(' · excerpt §3 %s ids %s' % (EX_S3_RULE, want.replace('EXCERPT-', ''))))
            if want == 'EXCERPT-MISMATCH':
                bad = [x for x in res['excerpt']['items'] if x['kind'] == 'ids']
                good = good and len(bad) == 1 and bad[0]['text'] == '%s ids: missing [%s] extra [%s]' % (
                    EX_S3_RULE, ', '.join(w_miss), ', '.join(w_extra))
            else:
                good = good and [x['kind'] for x in res['excerpt']['missing'] if x['kind'] == 'ids'] == ['ids']
            ok &= good
            print('  %s  %s (got %s, missing [%s], extra [%s], exit %d)' % (
                'PASS' if good else 'FAIL', name, r3['result'], ', '.join(r3['missing']),
                ', '.join(r3['extra']), res['exit_code']))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    good = live['exit_code'] == 0 and s3['result'] == 'OK' and \
        render(live).split('\n')[-1].endswith(' · excerpt §3 %s ids OK' % EX_S3_RULE)
    ok &= good
    print('  %s  live tree passes (exit %d; section 3 %s: "- %s" lines %s cite %s)' % (
        'PASS' if good else 'FAIL', live['exit_code'], s3['result'], EX_S3_RULE,
        ', '.join('L%d' % n for n in s3['lines']), ', '.join(s3['found'])))
    print('selftest-excerpt: %s' % ('all passed' if ok else 'FAILED'))
    return 0 if ok else 1


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog='xref_check.py', formatter_class=argparse.RawDescriptionHelpFormatter,
        description='Section references (F 4.2, F.md 4.2, file.md section 35, 第35节, “4.2 title”) '
                    'must resolve to numbered headings; quoted titles must match; V/S/O/C rule numbers must be '
                    'defined as "- **Vnn**" etc. in the main files (C in FICCCompose.md) and must not be retired '
                    '(a pointer-only definition "- **V05** → FICCCompose.md C01"); references/compose-excerpt.md '
                    'must copy FICCCompose.md verbatim before its "## 3", hold an intent line per C number, the key '
                    'lines in EXCERPT_REQUIRED and every C01 table row; its "- C23" lines after "## 3" must cite '
                    'exactly the C numbers of FICCCompose.md C23. '
                    'Exit 1 on any MISSING, STALE?, MISSING-RULE, RETIRED-RULE, EXCERPT-MISMATCH, EXCERPT-MISSING '
                    'or EXCERPT-MISSING-FILE.',
        epilog='Not scanned (still valid targets): references/history.md, references/dev-notes.md and '
               'references/FICCVoice-provenance.md (historical records and provenance; '
               'old section numbers stay as written); references/corpus/ '
               '(author texts, not rules); this script (its selftest fixtures are deliberately broken); '
               'symlinks (ficc-voice.md -> FICCVoice.md). Run after any change to a heading or section '
               'number of the main files, or any rule definition. Full rules: module docstring and scripts/README.md.')
    ap.add_argument('--root', default=SKILL_DIR, help='skill dir to check (default: %(default)s)')
    ap.add_argument('--json', action='store_true', help='machine-readable output')
    ap.add_argument('-q', '--quiet', action='store_true', help='list only MISSING / STALE? refs')
    ap.add_argument('--selftest', action='store_true',
                    help='temp fixture: good refs, one broken link, one legacy ref, one stale title, '
                         'bad rule numbers (V99, O02, a bare retired S38, C99, a pointer to C98), retired-number '
                         'pointers, a retired V05 cited bare, rationale anchors, FICCCompose.md sections; '
                         'seven excerpt cases (verbatim OK, changed word, dropped C number, extra table cell, dropped '
                         'key sub-line, dropped C01 table row, key lines and table complete) '
                         'and a missing excerpt file')
    ap.add_argument('--selftest-excerpt', action='store_true',
                    help='excerpt section 3 on a temp copy of --root: drop one C number from the "- C23" lines, '
                         'add a defined C number C23 does not cite, drop every "- C23" line (each must be reported '
                         'with exit 1); then --root itself must pass (exit 0). Exit 0 all passed, 1 otherwise')
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if a.selftest_excerpt:
        s3 = selftest_excerpt_s3(a.root)
        return selftest_voice_excerpts(a.root) or s3
    try:
        res = check(a.root)
    except IOError as e:
        print(str(e), file=sys.stderr)
        return 2
    if a.json:
        out = dict(res)
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(render(res, a.quiet))
    return res['exit_code']


if __name__ == '__main__':
    sys.exit(main())
