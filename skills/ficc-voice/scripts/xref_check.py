# -*- coding: utf-8 -*-
r"""xref_check.py (2026-10-17, wave 4; no retired numbers since 2026-11-04; agent cards and STALE-QUOTE
2026-11-04) -- section references must resolve to numbered headings; V/S/O/C rule numbers must be defined;
rationale "Supports" quotes must quote the current rule text.

Checks that every reference to a section of FICCOutline.md, FICCStructure.md,
FICCVoice.md or FICCCompose.md (and to a numbered section of any other .md file in
the skill, named by file) points at an existing heading, and that every quoted title
still matches the heading text.  Stdlib only; Python 3.9+.

Usage:
  xref_check.py [--root DIR] [--cards DIR] [--json] [-q] [--selftest]
  xref_check.py [--root DIR] [--cards DIR] --selftest-excerpt

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
  references/migration-2026-10-17.md  rule-number migration record: old numbers stay as they were
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

Rule numbers (added 2026-10-17; retired-number pointers dropped 2026-11-04): every V\d\d, S\d\d,
O\d\d, C\d\d in a scanned file (not preceded by a letter, digit or "_", not followed by a digit)
must have a definition line "- **Vnn** **<intent>**" in FICCVoice.md ("- **Snn** **...**" in
FICCStructure.md, "- **Onn** **...**" in FICCOutline.md, "- **Cnn** **...**" in FICCCompose.md);
otherwise MISSING-RULE.  Not checked for rule numbers: the files excluded above (the records,
references/migration-2026-10-17.md among them, keep old numbers) and everything under
references/zh/.  There are no retired numbers, pointer lines or exemptions (user ruling
2026-11-04): a retired number is deleted with its line and live files cite current numbers only,
so a number without a definition line is MISSING-RULE wherever it stands -- in a "(formerly ...)"
note, in a *-rationale.md file, or on a leftover line "- **V05** → FICCCompose.md C01", which is
not a definition line (its own number is reported there too).

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

Agent cards (2026-11-04): the ficc-*.md files in <root>/../../agents (the installed skill
~/.claude/skills/ficc-voice -> ~/.claude/agents; the public repo skills/ficc-voice -> <repo>/agents), or in
--cards DIR, are checked like the skill files, results kept apart.  A symlinked card is read through its link (a
broken link is skipped; a link and its target in the same dir are read once).  Section refs named by file (F 4.2,
F.md 4.2, F.md “4.2 title”, dev-notes.md section 5, continuations "F.md 1–5 and 9") must resolve (MISSING), and
every one must carry its section title right after the number (author ruling 2026-11-04):
  FICCStructure.md 7 “Check relations layer by layer”   FICCOutline.md 1 “The outline is a tree”–4 “Build ...”
the heading title without its number; compared after trimming blanks, case-insensitively.  The title is needed once
per card: at the first mention of a (file, section); later mentions may omit it.  NO-TITLE only when no mention of
that (file, section) in the card has a title (the note gives the title to write); a title that differs: STALE-TITLE
wherever it stands.  A range "N–M" carries a title at each end and only its
ends are refs.  V/S/O/C numbers must be defined (MISSING-RULE).  Not read in cards: bare section numbers without a
file name ("4 Kept rulings" points at the card's skill SKILL.md), unprefixed quoted titles, item numbers written
without ".md" (dispatch-notes 2.3), and refs to files outside this skill (ficc-hand/references/handoff.md 2).  The
title rule holds for cards only; skill files keep STALE? for a quoted title.  No such dir, or no ficc-*.md file in
it: one line "cards: none found at DIR", not a failure.  Report: "cards: DIR (names)", per-card blocks, then
  cards N files · refs N · MISSING m · STALE-TITLE s · NO-TITLE n · rule refs R · MISSING-RULE r
--json: "cards" {dir, found, files, per_file, refs, rules}; counts.cards_files, cards_refs, cards_missing,
cards_stale_title, cards_no_title, cards_rule_refs, cards_missing_rule.  Card names show as "cards/<name>".

Rationale quotes (2026-11-04): on each "Supports" line of references/*-rationale.md (fenced code skipped), a
rule id followed -- after any spaces, or after one bracketed note "S12 (the sub-line) “...”" and any spaces -- by a
quotation “...” (nested “” counted) must quote that rule's current text.  Body of Xnn: from its definition line in
the rule file for its letter to the next "- **Xmm**" line or heading; each line compared with blanks at both ends
and "**" removed, the definition line without "- Xnn " (the intent sentence), any other list line without its "- ".
The quote (blanks at both ends and one final period removed) must be a substring of one body line; a quote with
ellipses (…… … ...) passes when each segment is found, in order, on one line; ‘’ and “” count as the same mark
(inner quotes nest as ‘’).  Otherwise STALE-QUOTE: the report gives file, line, rule id, the first 40 characters
of the quote and the most similar body line.  A quotation not closed on its line is STALE-QUOTE too.  History is
not checked: lines "- Original (ledger ...)", "- Origin (...)", "- Moved here (...)", and the rest of a Supports
line from the first "Original (...):", "Origin:" or "Moved here" that stands outside every quotation (inside a
quotation these words are quoted text and do not cut the line).  A rule id with no definition line is left to
MISSING-RULE (quote SKIPPED).  Report:
  rationale quotes: N "Supports: Xnn “...”" quotes in <files> checked against the rule bodies; STALE-QUOTE s
--json: "quotes" (per quote: file, line, rule, quote, result, rule_file, match_line, nearest_line, nearest,
similarity, note), "quote_files"; counts.quotes, counts.stale_quote.
The cards line and the quotes line stand before the last line; their counts also go into the last line,
just before its last item (see "Last line" below).

Exit codes: 0 clean; 1 any MISSING, STALE?, MISSING-RULE, EXCERPT-MISMATCH,
EXCERPT-MISSING or EXCERPT-MISSING-FILE in the skill; any MISSING, STALE-TITLE, NO-TITLE or MISSING-RULE in a
card; any STALE-QUOTE; 2 usage error (root lacks FICCOutline.md, FICCStructure.md or FICCVoice.md).
Last line of the text report:
  refs N · MISSING m · STALE? s · rule refs R · MISSING-RULE r
    · excerpt lines N · EXCERPT-MISMATCH m · EXCERPT-MISSING k
    · cards N files · cards MISSING m · cards STALE-TITLE s · cards NO-TITLE n · cards MISSING-RULE r
    · quotes Q · STALE-QUOTE q
    · excerpt §3 C23 ids OK
  (one line; the last item reads OK, MISMATCH, MISSING or skipped as in "Section 3" above;
  " · EXCERPT-MISSING-FILE 1" replaces the section-3 item when the excerpt is missing; " · excerpt
  skipped" instead of the excerpt items when the root has no FICCCompose.md.  The cards and quotes
  items (2026-11-04) always stand just before that last item; " · cards none" when no card dir with
  ficc-*.md was found)
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
import contextlib
import difflib
import fnmatch
import io
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
    'references/migration-2026-10-17.md': 'rule-number migration record, old numbers kept',
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
# definition line "- **V07** **<intent>**"; "- **V05** → ..." (a pointer) is not one (2026-11-04)
RULE_DEF = re.compile(r'^\s*-\s+\*\*([VSOC]\d{2})\*\*\s+\*\*')
RULE_FILE = {'V': 'FICCVoice.md', 'S': 'FICCStructure.md', 'O': 'FICCOutline.md', 'C': 'FICCCompose.md'}
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
    'references/voice-excerpt-polish.md': ('V01', 'V02', 'V03', 'V04', 'V07', 'V08', 'V10', 'V11', 'V12', 'V13', 'V14',
                                           'V15', 'V16', 'V17', 'V18', 'V19', 'V20', 'V21', 'V22', 'V23', 'V24', 'V25',
                                           'V26', 'V27', 'V28', 'V29', 'V31', 'V32', 'V33', 'V34', 'V35', 'V36', 'V37',
                                           'V38', 'V39', 'V40', 'V52', 'V53', 'V54', 'V57'),
    'references/voice-excerpt-draft.md': ('V01', 'V02', 'V03', 'V04', 'V26', 'V27', 'V28', 'V38'),
    'references/voice-excerpt-coldread.md': ('V22', 'V23', 'V32', 'V36', 'V37', 'V38', 'V39', 'V40', 'V57'),
}
EX_V = re.compile(r'^-\s+(V\d{2})\s')
# agent cards (2026-11-04): <root>/../../agents/ficc-*.md -- ~/.claude/skills/ficc-voice -> ~/.claude/agents, and
# skills/ficc-voice -> <repo>/agents in the public repo; --cards DIR overrides.  Shown as "cards/<name>".
CARDS_REL = ('..', '..', 'agents')
CARD_GLOB = 'ficc-*.md'
CARD_LABEL = 'cards/'
# a card's section ref carries the section title right after its number: FICCStructure.md 7 “Check relations layer
# by layer” (author ruling 2026-11-04); compared with the heading title case-insensitively
CARD_TITLE = re.compile(r'\s?“([^”\n]{1,160})”')
# rationale quotes (2026-11-04): "Supports: Xnn “<rule sentence>”" in references/*-rationale.md must quote the rule's
# current body.  The id may be followed by one bracketed note before the quote: "S12 (the sub-line) “...”".
RATIONALE_DIR, RATIONALE_SUFFIX = 'references', '-rationale.md'
SUPPORTS = re.compile(r'^\s*(?:-\s+)?Supports\b')
HISTORY_CUT = re.compile(r'(?:Original|Origin)\s*(?:\([^)\n]*\))?\s*:|Moved here')   # history text: not checked
QREF = re.compile(r'(?<![A-Za-z0-9_])([VSOC]\d{2})(?![0-9])[ \t]*(?:[（(][^（()）\n]{0,80}[)）][ \t]*)?“')   # any spaces (Codex F2)
RULE_ANY = re.compile(r'^\s*-\s+\*\*[VSOC]\d{2}\*\*')   # any rule line, pointer lines included: ends a body
ELLIPSIS = re.compile(r'……|…|\.\.\.')
QMAP = str.maketrans({'‘': '“', '’': '”'})   # a quote inside “...” nests with ‘’: ‘而且’ there = “而且” in the rule


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


def attached_title(line, pos):
    """a card ref's title: “...” right after the number (one optional space), up to 160 characters."""
    m = CARD_TITLE.match(line, pos)
    if not m:
        return None, pos
    return m.group(1).strip(), m.end()


def chain(line, pos, prev, aq=attached_quote):
    """Continuations after ref `prev` ending at pos; yields (num, quote, start, end)."""
    out = []
    while True:
        m = RCONT.match(line, pos)
        if not m:
            return out
        if m.group(1).strip() in RANGE and \
                [int(x) for x in m.group(2).split('.')] <= [int(x) for x in prev.split('.')]:
            return out
        q, end = aq(line, m.end())
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


def cards_dir(root, cards=None):
    """the agent-card directory: --cards DIR, else <root>/../../agents."""
    if cards:
        return os.path.abspath(os.path.expanduser(cards))
    return os.path.normpath(os.path.join(os.path.abspath(os.path.expanduser(root)), *CARDS_REL))


def card_files(cdir):
    """-> sorted ficc-*.md names in cdir that are files after following symlinks (a broken link is not), one name per
    real file (a regular file wins over a link to it); [] when cdir is missing or holds none."""
    if not os.path.isdir(cdir):
        return []
    seen = {}
    for fn in sorted(os.listdir(cdir)):
        p = os.path.join(cdir, fn)
        if not fnmatch.fnmatch(fn, CARD_GLOB) or not os.path.isfile(p):
            continue
        real = os.path.realpath(p)
        if real not in seen or (os.path.islink(os.path.join(cdir, seen[real])) and not os.path.islink(p)):
            seen[real] = fn
    return sorted(seen.values())


def rule_bodies(root):
    """-> {Xnn: (rule file, [(line no, text)])}.  A body runs from the definition line "- **Xnn** **...**" to the next
    rule line "- **Xmm**" (pointer lines included) or heading.  Text per line: blanks at both ends and "**" removed; the
    definition line without its "- Xnn " prefix (= the intent sentence), any other list line without its leading "- "."""
    out = {}
    for letter, fname in sorted(RULE_FILE.items()):
        fp = os.path.join(root, fname)
        if not os.path.isfile(fp):
            continue
        cur = None
        for no, l in enumerate(read(fp).split('\n'), 1):
            d = RULE_DEF.match(l)
            if d and d.group(1)[0] == letter:
                cur = out.setdefault(d.group(1), (fname, []))[1]
                cur.append((no, re.sub(r'^-\s+%s\s*' % d.group(1), '', l.replace('**', '').strip())))
                continue
            if RULE_ANY.match(l) or re.match(r'^#{1,6} ', l):
                cur = None
                continue
            t = l.replace('**', '').strip()
            if cur is not None and t:
                cur.append((no, t[2:].strip() if t.startswith('- ') else t))
    return out


def _close_quote(line, k):
    """index of the ” closing the “ at line[k] (nested “” counted), or -1."""
    depth = 0
    for j in range(k, len(line)):
        if line[j] == '“':
            depth += 1
        elif line[j] == '”':
            depth -= 1
            if depth == 0:
                return j
    return -1


def _history_cut(line):
    """start of the first "Original (...):", "Origin:" or "Moved here" outside any “...” on the line, else len(line)."""
    for h in HISTORY_CUT.finditer(line):
        if line.count('“', 0, h.start()) == line.count('”', 0, h.start()):
            return h.start()
    return len(line)


def norm_quote(q):
    """blanks at both ends and one final period (. or 。, not an ellipsis) removed."""
    q = q.strip()
    if q.endswith(('.', '。')) and not q.endswith(('...', '…')):
        q = q[:-1].rstrip()
    return q


def quote_on_line(q, line):
    """q (normalised) is a substring of line; with ellipses (…… … ...) every segment, in order, on that line."""
    segs = [x.strip() for x in ELLIPSIS.split(q)]
    segs = [x for x in segs if x]
    pos = 0
    for x in segs:
        k = line.find(x, pos)
        if k < 0:
            return False
        pos = k + len(x)
    return bool(segs)


def rationale_files(root):
    d = os.path.join(root, RATIONALE_DIR)
    if not os.path.isdir(d):
        return []
    return sorted(RATIONALE_DIR + '/' + fn for fn in os.listdir(d)
                  if fn.endswith(RATIONALE_SUFFIX) and os.path.isfile(os.path.join(d, fn)))


def check_quotes(root):
    """STALE-QUOTE (2026-11-04): on each "Supports" line of references/*-rationale.md (fenced code skipped; the
    line cut where "Original (...):", "Origin:" or "Moved here" starts), every rule id followed -- optionally after one
    bracketed note -- by a quotation “...” (nested “” counted) must quote its rule's current body: the quote, normalised
    by norm_quote, is a substring of one body line, or with ellipses every segment in order on one line; ‘’ and “” count
    as the same mark on both sides (a quote nests its inner quotes with ‘’).  "Original"/"Origin"/"Moved here"
    lines are history and not read.  An id with no definition line is left to MISSING-RULE (result SKIPPED).
    -> list of {file, line, rule, quote, result OK|STALE-QUOTE|SKIPPED, rule_file, match_line, nearest_line,
    nearest, similarity, note}."""
    bodies = rule_bodies(root)
    out = []
    for rel in rationale_files(root):
        fence = False
        for no, l in enumerate(read(os.path.join(root, rel)).split('\n'), 1):
            if FENCE.match(l):
                fence = not fence
                continue
            if fence or not SUPPORTS.match(l):
                continue
            cut = _history_cut(l)
            pos = 0
            while True:
                m = QREF.search(l, pos)
                if not m or m.start() >= cut:
                    break
                k = m.end() - 1
                e = _close_quote(l, k)
                rid = m.group(1)
                r = {'file': rel, 'line': no, 'rule': rid, 'quote': l[k + 1:e] if e >= 0 else l[k + 1:],
                     'result': 'OK', 'rule_file': RULE_FILE[rid[0]],
                     'match_line': None, 'nearest_line': None, 'nearest': '', 'similarity': 0.0, 'note': ''}
                if e < 0:   # never dropped silently (R1 F7)
                    r['result'] = 'STALE-QUOTE'
                    r['note'] = 'quotation “ not closed on this line'
                    out.append(r)
                    break
                raw = r['quote']
                pos = e + 1
                if rid not in bodies:
                    r['result'] = 'SKIPPED'
                    r['note'] = '%s has no definition line (reported as MISSING-RULE)' % rid
                    out.append(r)
                    continue
                q = norm_quote(raw).translate(QMAP)
                lines = [(n, t.translate(QMAP)) for n, t in bodies[rid][1]]
                hit = next((n for n, t in lines if quote_on_line(q, t)), None)
                if hit:
                    r['match_line'] = hit
                else:
                    r['result'] = 'STALE-QUOTE'
                    r['nearest_line'], _, r['similarity'] = _nearest(q, lines)
                    r['nearest'] = dict(bodies[rid][1]).get(r['nearest_line'], '')
                    r['note'] = 'not on any line of %s %s (L%d–L%d)' % (
                        r['rule_file'], rid, bodies[rid][1][0][0], bodies[rid][1][-1][0])
                out.append(r)
    return out


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
    for rel, req in sorted((VOICE_EXCERPTS if table is None else table).items()):
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


def selftest_voice_excerpts(root=SKILL_DIR, cards=None):
    """--selftest-excerpt, part 2 (wave 3): on a temp copy of root, per voice excerpt: one word changed in a section-1
    line -> EXCERPT-MISMATCH; one required intent line dropped -> EXCERPT-MISSING; the file removed ->
    EXCERPT-MISSING-FILE; each with exit 1.  Then root itself must pass.  -> 0 or 1."""
    print('== voice excerpt selftest (%d files vs FICCVoice.md; temp copy of %s)' % (len(VOICE_EXCERPTS), root))
    cards = cards_dir(root, cards)   # the copy's own ../../agents is elsewhere: keep the original's
    live = check(root, cards=cards)
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
                res = check(dst, cards=cards)
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


def check(root, cards=None, voice_table=None):
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
    # rule numbers: a definition line "- **Vnn** **...**" in FICCVoice.md, "- **Snn** **...**" in FICCStructure.md,
    # "- **Onn** **...**" in FICCOutline.md, "- **Cnn** **...**" in FICCCompose.md; no retired numbers (2026-11-04)
    defined = {}
    for letter, fname in RULE_FILE.items():
        fp = os.path.join(root, fname)
        lines = read(fp).split('\n') if os.path.isfile(fp) else []
        defined[letter] = {m.group(1) for m in (RULE_DEF.match(l) for l in lines) if m and m.group(1)[0] == letter}
    rules = []

    def scan_rules(rel, text):
        if rel.startswith(ZH):
            return
        for i, l in enumerate(text.split('\n'), 1):
            d = RULE_DEF.match(l)
            own_def = d.start(1) if d and RULE_FILE[d.group(1)[0]] == rel else -1  # the definition itself is not a ref
            for m in RULE_REF.finditer(l):
                if m.start() == own_def:
                    continue
                rid = m.group(0)
                r = {'file': rel, 'line': i, 'ref': rid, 'result': 'OK', 'note': ''}
                if rid not in defined[m.group(1)]:
                    r['result'] = 'MISSING-RULE'
                    r['note'] = 'no "- **%s** **...**" in %s' % (rid, RULE_FILE[m.group(1)])
                rules.append(r)

    def resolve(rel, i, kind, tgt, num, raw, quote, local, card=False):
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
        elif card:   # cards (author ruling 2026-11-04): every ref names its section title
            title = H[num]
            r['heading'] = ('%s %s %s' % (name, num, title)).strip()
            if quote is None:
                r['result'] = 'NO-TITLE'
                r['note'] = 'no mention in this card has the title; at the first: %s %s “%s”' % (name, num, title)
            elif quote.strip().lower() != title.strip().lower():
                r['result'] = 'STALE-TITLE'
                r['note'] = 'title “%s” ≠ heading “%s”' % (quote, title)
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

    def scan_text(rel, text, card=False):
        """Section refs and rule numbers of one file -> its per-file summary, or None when it has no ref.
        A card (card=True, 2026-11-04) gets prefixed section refs (F 4.2, F.md “4.2 title”, file.md section 5) and
        rule numbers only: no bare in-file refs, no unprefixed quoted titles."""
        scan_rules(rel, text)
        stem = rel[:-3] if rel.endswith('.md') else None
        own = None if card else (
            rel if (stem in FILES or (rel.startswith(ZH) and stem and stem[len(ZH):] in FILES)) else None)
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
                    q, end = (attached_title if card else attached_quote)(l, m.end())
                    local = is_ex and l[max(0, m.start() - 3):m.start()] == '本文件'
                    found.append(('N', tgt, m.group('n'), q, l[m.start():end], m.start(), end, local))
                    spans.append((m.start(), end))
                    for cn, cq, cs, ce in chain(l, end, m.group('n'), attached_title if card else attached_quote):
                        found.append(('C', tgt, cn, cq, l[cs:ce], cs, ce, False))
                        spans.append((cs, ce))
                for m in RQB.finditer(l):
                    if card or not free(m.start()):   # cards: prefixed refs only
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
                resolve(rel, i, kind, tgt, num, raw, q, local, card)
        mine = refs[start_n:]
        if card:   # a (file, section) needs its title once per card, at its first mention (author ruling, round 4)
            titled = {}
            for r in mine:
                if r['quote'] is not None and r['result'] in ('OK', 'STALE-TITLE'):
                    titled.setdefault(r['ref'], r['line'])
            for r in mine:
                if r['result'] == 'NO-TITLE' and r['ref'] in titled:
                    r['result'] = 'OK'
                    r['note'] = 'title given in this card at L%d' % titled[r['ref']]
        if mine:
            return {'file': rel, 'refs': len(mine),
                    'missing': sum(r['result'] == 'MISSING' for r in mine),
                    'stale': sum(r['result'] == 'STALE?' for r in mine),
                    'stale_title': sum(r['result'] == 'STALE-TITLE' for r in mine),
                    'no_title': sum(r['result'] == 'NO-TITLE' for r in mine)}
        return None

    for rel in scanned:
        p = scan_text(rel, read(os.path.join(root, rel)))
        if p:
            per.append(p)
    # agent cards (2026-11-04): <root>/../../agents/ficc-*.md or --cards DIR; counted apart from the skill files
    n_refs, n_rules = len(refs), len(rules)
    cdir = cards_dir(root, cards)
    cnames = card_files(cdir)
    cper = []
    for fn in cnames:
        p = scan_text(CARD_LABEL + fn, read(os.path.join(cdir, fn)), card=True)
        if p:
            cper.append(p)
    card_refs, card_rules = refs[n_refs:], rules[n_rules:]
    del refs[n_refs:]
    del rules[n_rules:]
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
    vex = check_voice_excerpts(root, voice_table)
    exc = check_excerpt(root)
    ex_mis = sum(1 for x in exc['items'] if x['result'] != 'OK') if exc else 0
    ex_miss = len(exc['missing']) if exc else 0
    ex_file = 1 if exc and exc['missing_file'] else 0
    c_miss = sum(r['result'] == 'MISSING' for r in card_refs)
    c_stale_t = sum(r['result'] == 'STALE-TITLE' for r in card_refs)
    c_no_t = sum(r['result'] == 'NO-TITLE' for r in card_refs)
    c_miss_rule = sum(r['result'] == 'MISSING-RULE' for r in card_rules)
    quotes = check_quotes(root)
    stale_q = sum(q['result'] == 'STALE-QUOTE' for q in quotes)
    return {'root': root, 'refs': refs, 'per_file': per, 'excluded': ex_list,
            'bare': bare, 'rules': rules,
            'rules_defined': {k: len(v) for k, v in defined.items()},
            'cards': {'dir': cdir, 'found': bool(cnames), 'files': [CARD_LABEL + f for f in cnames],
                      'per_file': cper, 'refs': card_refs, 'rules': card_rules},
            'quotes': quotes, 'quote_files': rationale_files(root),
            'excerpt': exc, 'voice_excerpts': vex,
            'counts': {'refs': n, 'missing': miss, 'stale': stale, 'bare': sum(bare.values()),
                       'rule_refs': len(rules), 'missing_rule': miss_rule,
                       'excerpt_lines': exc['lines'] if exc else 0, 'excerpt_mismatch': ex_mis,
                       'excerpt_missing': ex_miss, 'excerpt_missing_file': ex_file,
                       'excerpt_skipped': exc is None,
                       'voice_mismatch': sum(len(v['mismatch']) for v in vex),
                       'voice_missing': sum(len(v['missing']) for v in vex),
                       'voice_missing_file': sum(1 for v in vex if v['missing_file']),
                       'cards_files': len(cnames), 'cards_refs': len(card_refs), 'cards_missing': c_miss,
                       'cards_stale_title': c_stale_t, 'cards_no_title': c_no_t,
                       'cards_rule_refs': len(card_rules), 'cards_missing_rule': c_miss_rule,
                       'quotes': sum(q['result'] != 'SKIPPED' for q in quotes), 'stale_quote': stale_q},
            'exit_code': 1 if (miss or stale or miss_rule or ex_mis or ex_miss or ex_file
                               or c_miss or c_stale_t or c_no_t or c_miss_rule or stale_q
                               or any(v['mismatch'] or v['missing'] or v['missing_file'] for v in vex)) else 0}


def _render_refs(out, refs, per_file, quiet):
    byfile = {}
    for r in refs:
        byfile.setdefault(r['file'], []).append(r)
    for p in per_file:
        rows = byfile[p['file']]
        if quiet and not (p['missing'] or p['stale'] or p.get('stale_title') or p.get('no_title')):
            continue
        if p['file'].startswith(CARD_LABEL):
            out.append('== %s  (refs %d, MISSING %d, STALE-TITLE %d, NO-TITLE %d)' % (
                p['file'], p['refs'], p['missing'], p['stale_title'], p['no_title']))
        else:
            out.append('== %s  (refs %d, MISSING %d, STALE? %d)' % (p['file'], p['refs'], p['missing'], p['stale']))
        for r in rows:
            if quiet and r['result'] == 'OK':
                continue
            res_txt = r['heading'] if r['result'] == 'OK' else (
                r['result'] + ('  [%s]' % r['heading'] if r['heading'] else ''))
            out.append('  L%d [%s] %s -> %s%s' % (r['line'], r['kind'], r['raw'], res_txt,
                                                   ('  (%s)' % r['note']) if r['note'] else ''))


def render(res, quiet=False):
    out = ['root: %s' % res['root']]
    _render_refs(out, res['refs'], res['per_file'], quiet)
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
    out.append('rule numbers: %d refs to V/S/O/C (defined V %d, S %d, O %d, C %d); MISSING-RULE %d' % (
        c['rule_refs'], d.get('V', 0), d.get('S', 0), d.get('O', 0), d.get('C', 0), c['missing_rule']))
    for r in bad:
        out.append('  %s L%d %s -> %s  (%s)' % (r['file'], r['line'], r['ref'], r['result'], r['note']))
    cd = res.get('cards')
    if cd is not None:
        if not cd['found']:
            out.append('cards: none found at %s (no %s; skipped, not a failure)' % (cd['dir'], CARD_GLOB))
        else:
            out.append('cards: %s (%s)' % (cd['dir'], ', '.join(f[len(CARD_LABEL):] for f in cd['files'])))
            _render_refs(out, cd['refs'], cd['per_file'], quiet)
            for r in cd['rules']:
                if r['result'] != 'OK':
                    out.append('  %s L%d %s -> %s  (%s)' % (r['file'], r['line'], r['ref'], r['result'], r['note']))
            out.append('cards %d files · refs %d · MISSING %d · STALE-TITLE %d · NO-TITLE %d · rule refs %d · '
                       'MISSING-RULE %d' % (c['cards_files'], c['cards_refs'], c['cards_missing'],
                                           c['cards_stale_title'], c['cards_no_title'], c['cards_rule_refs'],
                                           c['cards_missing_rule']))
    if res.get('quotes') is not None:
        qs = res['quotes']
        out.append('rationale quotes: %d "Supports: Xnn “...”" quotes in %s checked against the rule bodies; '
                   'STALE-QUOTE %d%s' % (c['quotes'], ', '.join(os.path.basename(f) for f in res['quote_files']) or
                                          'no *-rationale.md', c['stale_quote'],
                                          ('; skipped %d (rule not defined)' % sum(q['result'] == 'SKIPPED' for q in qs))
                                          if any(q['result'] == 'SKIPPED' for q in qs) else ''))
        for q in qs:
            if q['result'] != 'STALE-QUOTE':
                continue
            out.append('  %s L%d %s “%s” -> STALE-QUOTE' % (q['file'], q['line'], q['rule'], snip(q['quote'], 40)))
            out.append('      closest %s L%s (similarity %.2f): %s' % (
                q['rule_file'], q['nearest_line'] or '-', q['similarity'], snip(q['nearest']) or '-'))
    exc = res.get('excerpt')
    head, last = '', ''   # last line: ... excerpt items (head), cards and quotes, then the last item
    if exc is None:
        out.append('excerpt: skipped (no FICCCompose.md under the root)')
        last = ' · excerpt skipped'
    elif exc['missing_file']:
        out.append('excerpt: %s -> EXCERPT-MISSING-FILE' % exc['file'])
        head = ' · excerpt lines 0 · EXCERPT-MISMATCH 0 · EXCERPT-MISSING 0'
        last = ' · EXCERPT-MISSING-FILE 1'
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
        head = ' · excerpt lines %d · EXCERPT-MISMATCH %d · EXCERPT-MISSING %d' % (
            exc['lines'], c['excerpt_mismatch'], c['excerpt_missing'])
        last = s3_tail
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
    mid = ''
    if cd is not None:   # cards and rationale quotes (2026-11-04), just before the last item
        mid = (' · cards %d files · cards MISSING %d · cards STALE-TITLE %d · cards NO-TITLE %d · cards MISSING-RULE %d'
               % (c['cards_files'], c['cards_missing'], c['cards_stale_title'], c['cards_no_title'],
                  c['cards_missing_rule'])) if cd['found'] \
            else ' · cards none'
    if res.get('quotes') is not None:
        mid += ' · quotes %d · STALE-QUOTE %d' % (c['quotes'], c['stale_quote'])
    out.append('refs %d · MISSING %d · STALE? %d · rule refs %d · MISSING-RULE %d%s%s%s' % (
        c['refs'], c['missing'], c['stale'], c['rule_refs'], c['missing_rule'], head, mid, last))
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
                    '- **V08** **Mark the add-on relation.**\n'
                    '  - The marker word stays here.\n',
    'FICCCompose.md': '# FICCCompose\n\n## 1 Paragraph openings\n\nSee 1.1 and C01.\n\n### 1.1 Opening\n\n'
                      '- **C01** **Conclusion first.** See references/FICCVoice-rationale.md C01 and V05.\n',
    'references/FICCVoice-rationale.md': '# rationale\n\n## C01\n\nSupports: C01 at every layer. Old V05 is checked here too.\n',
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
                'OLD: V02 (formerly S38); V02 (S34 merged); a history note is checked like any other text.\n\n'
                'COMPOSE: FICCCompose.md 1.1 and FICCCompose 9; C01 resolves; C99 is a broken C number; '
                'V05 has only a leftover pointer line; C01（原 V05） is checked too; V08 is defined.\n\n'
                'RANGE: FICCOutline.md 1.1–1.2, and 2.1; FICCOutline 1–3份 is a quantity.\n',
    'references/migration-2026-10-17.md': '# Migration\n\n| Old | New |\n|---|---|\n| V77 | V02 |\n\n'
                                          'Prose line: V88 and FICCVoice.md 9.9 are not checked.\n',
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
        res = check(tmp, cards=os.path.join(tmp, 'no-cards'))   # cards and rationale quotes: selftest_cards_quotes
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
            ('migration record excluded: no section refs (FICCVoice.md 9.9), no rule refs (V77, V88); raw matches listed',
             not any(r['file'] == 'references/migration-2026-10-17.md' for r in rr)
             and not any(r['file'] == 'references/migration-2026-10-17.md' for r in res['refs'])
             and any(x['file'] == 'references/migration-2026-10-17.md' and x['raw_matches'] == 1
                     for x in res['excluded'])),
            ('"(formerly S38)" and "(S34 merged)" are not exempt: S38, S34 -> MISSING-RULE; V02 in front -> OK',
             rule('SKILL.md', 'S34') == ['MISSING-RULE'] and rule('SKILL.md', 'S38') == ['MISSING-RULE']
             and [r['result'] for r in rr if r['file'] == 'SKILL.md' and r['line'] == 21 and r['ref'] == 'V02']
             == ['OK', 'OK']),
            ('references/zh/ and dev-notes.md not scanned for rule numbers (V66, S55)',
             not any(r['ref'] in ('V66', 'S55') for r in rr)),
            ('C01 defined in FICCCompose.md -> OK; C99 -> MISSING-RULE',
             [r['result'] for r in rr if r['file'] == 'SKILL.md' and r['line'] == 23 and r['ref'] == 'C01']
             == ['OK'] * 2 and rule('SKILL.md', 'C99') == ['MISSING-RULE']),
            ('a leftover pointer line "- **V05** → FICCCompose.md C01" is not a definition: V05 -> MISSING-RULE '
             'on it and where cited, "（原 V05）" included; its C01 -> OK',
             rule('FICCVoice.md', 'V05') == ['MISSING-RULE'] and rule('FICCVoice.md', 'C01') == ['OK']
             and rule('SKILL.md', 'V05') == ['MISSING-RULE'] * 2),
            ('definition lines only: V02 and V08 defined (V08 with an indented body -> OK), the pointer line is not',
             res['rules_defined']['V'] == 2 and rule('SKILL.md', 'V08') == ['OK']),
            ('no rationale exemption: V05 after "-rationale.md" and inside *-rationale.md -> MISSING-RULE; '
             'C01 there -> OK',
             rule('FICCCompose.md', 'V05') == ['MISSING-RULE']
             and rule('references/FICCVoice-rationale.md', 'V05') == ['MISSING-RULE']
             and rule('references/FICCVoice-rationale.md', 'C01') == ['OK', 'OK']),
            ('counts 10 MISSING-RULE (V99, O02, S38, S34, C99, V05 x5); no retired-number fields in the result',
             res['counts']['missing_rule'] == 10 and 'rules_retired' not in res
             and not any(k.startswith('retired') for k in res['counts'])),
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
    ok &= selftest_cards_quotes()
    print('selftest: %s' % ('all passed' if ok else 'FAILED'))
    return 0 if ok else 1


# cards and rationale quotes (2026-11-04): a clean minimal tree at <tmp>/skills/ficc-voice, cards at <tmp>/agents
CQ_TREE = {
    'FICCOutline.md': '# FICCOutline\n\n## 1 The outline is a tree\n\n### 1.2 Position\n\n- **O01** **Write the claim first.**\n',
    'FICCStructure.md': '# FICCStructure\n\n## 1 Set position\n\n- **S01** **Ask the task.**\n  - Name the parent node first.\n'
                        '  - Origin: the task comes from the parent node.\n',
    'FICCVoice.md': '# FICCVoice\n\n## 2 How to state a judgment\n\n'
                    '- **V02** **State the judgment.**\n'                                           # L5
                    '- **V08** **Mark the add-on relation. Keep the marker short.**\n'
                    '  - Write “而且” (moreover) before the verb, not at the end.\n',
    'SKILL.md': '# skill\n\nSkill files need no titles: FICCOutline.md 1.2 and FICCStructure.md 1.\n',
}
CQ_QUOTES = ('# FICCVoice rationale\n\n## V08\n\n'
             '- Original (ledger #1): Mark it.\n'
             '  Supports: V08 “Mark the add-on relation.” Intent line: "**" and the final period dropped.\n'     # L6
             '  Supports: S01 (the sub-line) “Name the parent node first”. A sub-item line, after a bracketed note.\n'
             '  Supports: V08 “Write ‘而且’ (moreover) …… not at the end”. Ellipsis segments in order; nested ‘’.\n'
             '- Original (ledger #2): V02 “State the old judgment first” is history, not checked.\n'         # L9
             '- Moved here (2026-11-04): V02 “An old line” is history too.\n'                               # L10
             '  Supports: V08 “Mark the add-on relation” and S01 “Origin: the task comes from the parent node”. '
             'Origin: V02 “made-up history” is not checked.\n')                                              # L11
CQ_STALE = ('  Supports: V02 “State the judgment in full”. Changed wording.\n'                              # L12
            '  Supports: V08 “not at the end …… Write ‘而且’”. Segments out of order.\n'                    # L13
            '  Supports: V08 “Mark the add-on relation\n'                                                  # L14 unclosed
            '  Supports: V02 “State, Origin: the judgment”. A history marker inside a stale quote.\n'      # L15
            '  Supports: V02 “State, Original (ledger #3): the judgment”. Same with Original (...):.\n'   # L16
            '  Supports: V02 “State, Moved here the judgment”. Same with Moved here.\n'                   # L17
            '  Supports: V02  “State the old judgment”. Two spaces, no note.\n'                           # L18
            '  Supports: V02 (intent line)  “State the older judgment”. Two spaces after the note.\n')   # L19
CQ_GOOD_CARD = ('---\nname: ficc-good\n---\n\nRead FICCOutline.md 1 “The outline is a tree” to 1.2 “position” and '
                'FICCStructure.md 1 “Set position”; apply O01 and V08. '
                'Bare 4 Kept rulings, see 1.2 and “1.2 Position” are not checked.\n'
                'Then FICCStructure.md 1 again: the title was given once in this card.\n')
CQ_BAD_CARD = ('---\nname: ficc-bad\n---\n\nRead FICCStructure.md 1–5 and 9; FICCVoice.md “2 An old title”; '
               'FICCOutline.md 1.2 “Old position”; apply V99 and S01.\nAgain FICCStructure.md 1, still with no title.\n')
CQ_CLEAN_TAIL = ' · quotes 5 · STALE-QUOTE 0 · excerpt skipped'


def selftest_cards_quotes():
    """cards (default ../../agents, symlinked cards, --cards DIR, none found; titles: NO-TITLE, STALE-TITLE) and
    STALE-QUOTE (history cut outside quotes, unclosed quote), on a clean minimal tree."""
    print()
    print('cards and rationale quotes (clean tree <tmp>/skills/ficc-voice, cards <tmp>/agents):')
    tmp = tempfile.mkdtemp(prefix='xref_cards_')
    ok, checks = True, []
    try:
        root = os.path.join(tmp, 'skills', 'ficc-voice')
        files = dict(CQ_TREE)
        files['references/FICCVoice-rationale.md'] = CQ_QUOTES
        files['../../agents/ficc-good.md'] = CQ_GOOD_CARD
        files['../../agents/notes.md'] = 'Not a ficc-*.md card: FICCOutline.md 9.9 is not checked.\n'
        files['../../other/ficc-good.md'] = CQ_GOOD_CARD
        files['../../linked/ficc-good.md'] = CQ_GOOD_CARD
        files['../../src/bad-card.md'] = CQ_BAD_CARD
        files['../../src/good-card.md'] = CQ_GOOD_CARD
        for rel, txt in files.items():
            p = os.path.normpath(os.path.join(root, rel))
            if not os.path.isdir(os.path.dirname(p)):
                os.makedirs(os.path.dirname(p))
            with open(p, 'w', encoding='utf-8') as fh:
                fh.write(txt)
        linked = os.path.join(tmp, 'linked')
        os.symlink('ficc-good.md', os.path.join(linked, 'ficc-alias.md'))                       # duplicate of a card
        os.symlink(os.path.join(tmp, 'src', 'bad-card.md'), os.path.join(linked, 'ficc-link.md'))  # card kept elsewhere
        os.symlink(os.path.join(tmp, 'src', 'gone.md'), os.path.join(linked, 'ficc-broken.md'))     # broken link
        onlylink = os.path.join(tmp, 'onlylink')
        os.makedirs(onlylink)
        os.symlink(os.path.join(tmp, 'src', 'good-card.md'), os.path.join(onlylink, 'ficc-only.md'))
        qpath = os.path.join(root, 'references/FICCVoice-rationale.md')
        clean = check(root, voice_table={})
        cc = clean['counts']
        tail = render(clean).split('\n')
        qs = [(q['line'], q['rule'], q['result']) for q in clean['quotes']]
        checks += [
            ('default cards dir <root>/../../agents found; ficc-*.md only (notes.md skipped)',
             clean['cards']['found'] and clean['cards']['files'] == ['cards/ficc-good.md']
             and clean['cards']['dir'] == os.path.join(tmp, 'agents')),
            ('clean card: FICCOutline.md 1 “...” to 1.2 “position” (case-insensitive), FICCStructure.md 1 “...” OK; '
             'O01, V08 OK; bare 4, see 1.2 and unprefixed “1.2 Position” not read',
             sorted(r['ref'] for r in clean['cards']['refs'])
             == ['FICCOutline 1', 'FICCOutline 1.2', 'FICCStructure 1', 'FICCStructure 1']
             and all(r['result'] == 'OK' for r in clean['cards']['refs'] + clean['cards']['rules'])
             and sorted(r['ref'] for r in clean['cards']['rules']) == ['O01', 'V08']),
            ('title once per card: FICCStructure.md 1 titled at its first mention, untitled at the second -> both OK',
             [(r['line'], r['result']) for r in clean['cards']['refs'] if r['ref'] == 'FICCStructure 1']
             == [(5, 'OK'), (6, 'OK')]
             and [r['note'] for r in clean['cards']['refs'] if r['ref'] == 'FICCStructure 1'][1]
             == 'title given in this card at L5'),
            ('skill files need no titles: SKILL.md refs without titles -> OK',
             [r['result'] for r in clean['refs'] if r['file'] == 'SKILL.md'] == ['OK', 'OK']),
            ('cards line: "cards 1 files · refs 4 · MISSING 0 · STALE-TITLE 0 · NO-TITLE 0 · rule refs 2 · '
             'MISSING-RULE 0"',
             'cards 1 files · refs 4 · MISSING 0 · STALE-TITLE 0 · NO-TITLE 0 · rule refs 2 · MISSING-RULE 0' in tail),
            ('card refs and rule numbers kept out of the skill counts',
             not any(r['file'].startswith(CARD_LABEL) for r in clean['refs'] + clean['rules'])),
            ('quotes pass: intent line (period, ** dropped), sub-item after a bracketed note, ellipsis segments in '
             'order with nested ‘’ = “”, two quotes on one line',
             qs == [(6, 'V08', 'OK'), (7, 'S01', 'OK'), (8, 'V08', 'OK'), (11, 'V08', 'OK'), (11, 'S01', 'OK')]
             and [q['match_line'] for q in clean['quotes']] == [6, 6, 7, 6, 7]),
            ('"Original" and "Moved here" lines not checked (L9, L10); on a Supports line the text from "Origin:" '
             'on is not checked (L11 V02), but "Origin:" inside a quote does not cut it (L11 S01)',
             not any(q[0] in (9, 10) for q in qs) and not any(q[:2] == (11, 'V02') for q in qs)),
            ('clean tree: STALE-QUOTE 0, exit 0', cc['stale_quote'] == 0 and cc['quotes'] == 5
             and clean['exit_code'] == 0),
            ('last line carries cards and quotes before its last item: "... · cards 1 files · cards MISSING 0 · '
             'cards STALE-TITLE 0 · cards NO-TITLE 0 · cards MISSING-RULE 0 · quotes 5 · STALE-QUOTE 0 · excerpt skipped"',
             tail[-1].endswith(' · cards 1 files · cards MISSING 0 · cards STALE-TITLE 0 · cards NO-TITLE 0'
                               ' · cards MISSING-RULE 0' + CQ_CLEAN_TAIL)),
        ]
        with open(qpath, 'a', encoding='utf-8') as fh:
            fh.write(CQ_STALE)
        stale = check(root, voice_table={})
        sq = [q for q in stale['quotes'] if q['result'] == 'STALE-QUOTE']
        checks += [
            ('changed wording -> STALE-QUOTE, closest line = V02 intent line (FICCVoice.md L5)',
             [(q['line'], q['rule']) for q in sq][:1] == [(12, 'V02')] and sq[0]['nearest_line'] == 5
             and sq[0]['similarity'] > 0.5),
            ('ellipsis segments out of order -> STALE-QUOTE', [(q['line'], q['rule']) for q in sq][1:2] == [(13, 'V08')]),
            ('unclosed quotation -> STALE-QUOTE, not dropped',
             [(q['line'], q['rule']) for q in sq][2:3] == [(14, 'V08')] and 'not closed' in sq[2]['note']),
            ('a history marker inside a stale quote does not hide it (Codex F1): Origin:, Original (...):, '
             'Moved here -> STALE-QUOTE (L15-L17)',
             [(q['line'], q['rule']) for q in sq][3:6] == [(15, 'V02'), (16, 'V02'), (17, 'V02')]),
            ('extra spaces before the quote, with or without a note, are still read (Codex F2) -> STALE-QUOTE (L18, L19)',
             [(q['line'], q['rule']) for q in sq][6:] == [(18, 'V02'), (19, 'V02')]),
            ('STALE-QUOTE 8, exit 1; report line names file, line, rule and quote',
             stale['counts']['stale_quote'] == 8 and stale['exit_code'] == 1
             and '  references/FICCVoice-rationale.md L12 V02 “State the judgment in full” -> STALE-QUOTE'
             in render(stale).split('\n')),
            ('last line: "... · quotes 13 · STALE-QUOTE 8 · excerpt skipped"',
             render(stale).split('\n')[-1].endswith(' · quotes 13 · STALE-QUOTE 8 · excerpt skipped')),
        ]
        with open(qpath, 'w', encoding='utf-8') as fh:
            fh.write(CQ_QUOTES)
        with open(os.path.join(tmp, 'agents', 'ficc-bad.md'), 'w', encoding='utf-8') as fh:
            fh.write(CQ_BAD_CARD)
        bad = check(root, voice_table={})
        bc = bad['counts']
        res_of = lambda f, raw: [r['result'] for r in bad['cards']['refs'] if r['file'] == f and r['raw'] == raw]
        checks += [
            ('bad card: "FICCStructure.md 1–5 and 9" -> 1 NO-TITLE, 5 and 9 MISSING; FICCVoice.md “2 An old title” '
             'and FICCOutline.md 1.2 “Old position” -> STALE-TITLE; V99 -> MISSING-RULE',
             res_of('cards/ficc-bad.md', 'FICCStructure.md 1') == ['NO-TITLE', 'NO-TITLE']
             and res_of('cards/ficc-bad.md', '5') == ['MISSING'] and res_of('cards/ficc-bad.md', '9') == ['MISSING']
             and res_of('cards/ficc-bad.md', 'FICCVoice.md “2 An old title”') == ['STALE-TITLE']
             and res_of('cards/ficc-bad.md', 'FICCOutline.md 1.2 “Old position”') == ['STALE-TITLE']
             and [r['result'] for r in bad['cards']['rules'] if r['ref'] == 'V99'] == ['MISSING-RULE']),
            ('no mention titled: FICCStructure.md 1 twice in the bad card, never with a title -> NO-TITLE at both',
             [r['line'] for r in bad['cards']['refs'] if r['file'] == 'cards/ficc-bad.md' and r['result'] == 'NO-TITLE']
             == [5, 6]),
            ('cards line counts 2 files · refs 10 · MISSING 2 · STALE-TITLE 2 · NO-TITLE 2 · rule refs 4 · '
             'MISSING-RULE 1; exit 1',
             'cards 2 files · refs 10 · MISSING 2 · STALE-TITLE 2 · NO-TITLE 2 · rule refs 4 · MISSING-RULE 1'
             in render(bad).split('\n') and bad['exit_code'] == 1),
            ('last line: "refs N · MISSING 0 · ... · cards 2 files · cards MISSING 2 · cards STALE-TITLE 2 · '
             'cards NO-TITLE 2 · cards MISSING-RULE 1 · quotes 5 · STALE-QUOTE 0 · excerpt skipped"',
             render(bad).split('\n')[-1].endswith(' · cards 2 files · cards MISSING 2 · cards STALE-TITLE 2'
                                                   ' · cards NO-TITLE 2 · cards MISSING-RULE 1' + CQ_CLEAN_TAIL)
             and render(bad).split('\n')[-1].startswith('refs %d · MISSING 0 · STALE? 0 ·' % cc['refs'])),
            ('skill counts unchanged by the bad card',
             all(bc[k] == cc[k] for k in ('refs', 'missing', 'stale', 'rule_refs', 'missing_rule', 'quotes'))),
        ]
        lk = check(root, cards=linked, voice_table={})
        only = check(root, cards=onlylink, voice_table={})
        checks += [
            ('symlinked cards are read (R1 F1): a link to a card kept elsewhere is checked (its MISSING 2, '
             'MISSING-RULE 1 reported, exit 1); a link to a card in the same dir is read once; a broken link is skipped',
             lk['cards']['files'] == ['cards/ficc-good.md', 'cards/ficc-link.md']
             and (lk['counts']['cards_missing'], lk['counts']['cards_missing_rule']) == (2, 1)
             and lk['exit_code'] == 1),
            ('a dir holding only a symlinked card is found, not "none found" (exit 0)',
             only['cards']['found'] and only['cards']['files'] == ['cards/ficc-only.md'] and only['exit_code'] == 0
             and not any(l.startswith('cards: none found') for l in render(only).split('\n'))),
        ]
        other = os.path.join(tmp, 'other')
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            main(['--root', root, '--cards', other, '-q'])
        out = buf.getvalue().split('\n')
        over = check(root, cards=other, voice_table={})
        checks += [
            ('--cards DIR overrides the default (clean copy elsewhere: 1 file, exit 0)',
             over['cards']['dir'] == other and over['cards']['files'] == ['cards/ficc-good.md']
             and over['exit_code'] == 0 and 'cards: %s (ficc-good.md)' % other in out
             and 'cards 1 files · refs 4 · MISSING 0 · STALE-TITLE 0 · NO-TITLE 0 · rule refs 2 · MISSING-RULE 0' in out),
        ]
        none = check(root, cards=os.path.join(tmp, 'nowhere'), voice_table={})
        checks += [
            ('no cards dir -> "cards: none found at ...", not a failure (exit 0)',
             not none['cards']['found'] and none['exit_code'] == 0 and none['counts']['cards_files'] == 0
             and any(l.startswith('cards: none found at %s' % os.path.join(tmp, 'nowhere'))
                     for l in render(none).split('\n'))
             and render(none).split('\n')[-1].endswith(' · cards none' + CQ_CLEAN_TAIL)),
        ]
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    for name, good in checks:
        ok &= bool(good)
        print('  %s  %s' % ('PASS' if good else 'FAIL', name))
    return ok


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


def selftest_excerpt_s3(root=SKILL_DIR, cards=None):
    """--selftest-excerpt (2026-10-24): section 3 of the excerpt against C23, on a temp copy of root.
    Drop one C id from the "- C23" lines, add a defined C id that C23 does not cite, drop every
    "- C23" line: each must be reported (EXCERPT-MISMATCH ids / EXCERPT-MISSING ids) with exit 1 and
    no other count changed; then root itself must pass (exit 0, section 3 OK).  -> 0 or 1."""
    print('== excerpt section 3 selftest (%s "- %s" lines vs FICCCompose.md %s; temp copy of %s)'
          % (EXCERPT, EX_S3_RULE, EX_S3_RULE, root))
    cards = cards_dir(root, cards)   # the copy's own ../../agents is elsewhere: keep the original's
    live = check(root, cards=cards)
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
    keep = ('missing', 'stale', 'missing_rule', 'excerpt_missing_file')
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
            res = check(dst, cards=cards)
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
                    'defined by a line "- **Vnn** **...**" etc. in the main files (C in FICCCompose.md); a number '
                    'without one is MISSING-RULE wherever it stands (no retired numbers or pointer lines since '
                    '2026-11-04); references/compose-excerpt.md '
                    'must copy FICCCompose.md verbatim before its "## 3", hold an intent line per C number, the key '
                    'lines in EXCERPT_REQUIRED and every C01 table row; its "- C23" lines after "## 3" must cite '
                    'exactly the C numbers of FICCCompose.md C23. '
                    'Agent cards <root>/../../agents/ficc-*.md (or --cards DIR, symlinks followed): section refs '
                    'named by file must resolve (MISSING) and carry the section title, “...” right after the number '
                    '(NO-TITLE, STALE-TITLE); rule numbers (MISSING-RULE); counted on their own "cards" line. '
                    'Rationale quotes: in references/*-rationale.md, "Supports: Xnn “...”" must quote a line of '
                    'rule Xnn\'s current body (substring; ellipsis segments in order on one line; "Original", '
                    '"Origin" and "Moved here" history not checked), else STALE-QUOTE. '
                    'Exit 1 on any MISSING, STALE?, MISSING-RULE, EXCERPT-MISMATCH, EXCERPT-MISSING, '
                    'EXCERPT-MISSING-FILE, STALE-TITLE, NO-TITLE or STALE-QUOTE.',
        epilog='Not scanned (still valid targets): references/history.md, references/dev-notes.md, '
               'references/FICCVoice-provenance.md and references/migration-2026-10-17.md (historical records, '
               'provenance and the rule-number map; '
               'old section numbers stay as written); references/corpus/ '
               '(author texts, not rules); this script (its selftest fixtures are deliberately broken); '
               'symlinks (ficc-voice.md -> FICCVoice.md). Run after any change to a heading or section '
               'number of the main files, or any rule definition. Full rules: module docstring and scripts/README.md.')
    ap.add_argument('--root', default=SKILL_DIR, help='skill dir to check (default: %(default)s)')
    ap.add_argument('--cards', metavar='DIR', default=None,
                    help='agent-card dir whose ficc-*.md are checked for section refs named by file and V/S/O/C '
                         'numbers (default: <root>/../../agents, i.e. ~/.claude/agents for the installed skill and '
                         '<repo>/agents in the public repo; missing or without ficc-*.md -> "cards: none found", '
                         'not a failure)')
    ap.add_argument('--json', action='store_true', help='machine-readable output')
    ap.add_argument('-q', '--quiet', action='store_true', help='list only MISSING / STALE? refs')
    ap.add_argument('--selftest', action='store_true',
                    help='temp fixture: good refs, one broken link, one legacy ref, one stale title, '
                         'bad rule numbers (V99, O02, C99; S38 and S34 in history notes; V05 on a leftover pointer '
                         'line, cited and in a *-rationale.md file), FICCCompose.md sections; '
                         'seven excerpt cases (verbatim OK, changed word, dropped C number, extra table cell, dropped '
                         'key sub-line, dropped C01 table row, key lines and table complete) '
                         'and a missing excerpt file; cards (default ../../agents found, ficc-*.md only, titled clean '
                         'card, skill files need no titles, a card with "F.md 1–5 and 9" (NO-TITLE, MISSING), stale '
                         'titles and a bad rule number, symlinked cards, --cards override, no cards dir) and rationale '
                         'quotes (intent line, sub-item after a note, ellipsis in order, two quotes on a line, history '
                         'lines and suffixes skipped; changed wording, out-of-order ellipsis, unclosed quote, history '
                         'words inside a stale quote, extra spaces before the quote -> STALE-QUOTE)')
    ap.add_argument('--selftest-excerpt', action='store_true',
                    help='excerpt section 3 on a temp copy of --root: drop one C number from the "- C23" lines, '
                         'add a defined C number C23 does not cite, drop every "- C23" line (each must be reported '
                         'with exit 1); then --root itself must pass (exit 0). Exit 0 all passed, 1 otherwise')
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if a.selftest_excerpt:
        s3 = selftest_excerpt_s3(a.root, a.cards)
        return selftest_voice_excerpts(a.root, a.cards) or s3
    try:
        res = check(a.root, cards=a.cards)
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
