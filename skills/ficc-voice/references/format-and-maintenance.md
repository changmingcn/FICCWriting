# Format conventions and revision discipline

Read section 1 when tidying format; also read section 2 when maintaining a lecture-notes line or a research draft under long-term revision. Ordinary articles do not get an edit record by default.

## 1 Format details

Core levels and section-length requirements: [FICCOutline.md](../FICCOutline.md) 8.3. Use what follows only when this round is authorized to tidy format; a written-register conversion that leaves content and structure unchanged does not normalize headings, numbering, or sectioning on the side. Headings use full-width parentheses; a colon used inside as a separator may stay, as in “信贷：银行的第三个功能”. A heading must be understandable on its own; delete repeated cues, e.g. change “1. 第一步：建立欠条机制” to “1. 建立欠条机制”. Under an appendix, still number with “（一）（二）”. The close of the whole piece uses `## 结语`; like `## 附：……`, it takes no body ordinal (it is the root node's close, not one more parallel part; as of 2026-10-11 heading_check does not yet recognize it, so ignore its warning). In Google Docs, fonts are rendered by heading level.

Section length counts only prose, not table rows, fenced code blocks, or image reference lines. Verification ledgers, source lists, and comparison records under `## 附：……` are not subject to the 2000-character limit; neither are list-dominated parts where numbered or bulleted lines make up 35% or more of the non-empty lines. A knowledge point that runs to 1500 characters need not be cut by force; two knowledge points squeezed into 800 characters may be split.

Figures: no numbers; under each figure, note the measurement basis and the source.

Chinese punctuation conversion must protect the following:

- Code blocks, inline code, math (`$…$`, `\(…\)`), link targets, URLs, HTML comments, and function-style tokens such as `corr(交易, 残差)`.
- Thousands separators and punctuation in English context, such as `1,507.5`, `January 15, 2015`, `[0.02, 0.05]`, `pp. 1499–1556`, `Insider's`.
- Parentheses pairing an English term with a Chinese note, such as `货币(money)`, `做市(Market Making)`: keep the whole class half-width and internally consistent.

Spacing between Chinese and Western text is settled: the user ruled on 2026-10-08 that no space goes between Han characters and English or digits (e.g. “2025年11月”). New drafts follow this; keep a half-width space inside English phrases and between an English word and a number (DDTL 5.0). Old drafts are unified during an authorized format tidy: convert with `scripts/cjk_space.py --apply` and self-verify as for punctuation conversion (with all whitespace removed, before and after match character by character); author-quote lines starting with “>” stay untouched.

Quotation marks are settled: use “”, and ‘’ for a quote inside a quote; do not use 「」『』 (user ruling of 2026-10-12). When quoting English words, still use “” outside, and keep the English quotation marks inside the English original as they are. Before submission, H5 of `scripts/voice_check.py` blocks 「」『』.

**Case box style**

Mark a first-hand hook in the established case box style. The box holds only confirmed true events: who, in what situation, met what. Hypothetical scenes, worked examples, and the reasoning unfolded after the box do not go into the first-hand box. Use the box only for the opening passage that serves as the hook; historical examples in the text do not all get boxes on that account. When the whole piece is a case study, still box only the hook.

- Markdown: use a blockquote. Write `> **案例｜小标题**` as the first line, then a line `>`; each paragraph of the case starts with `> `, and paragraphs are separated by a `>` blank line. Do not put tables or images into the blockquote. An ordinary blockquote that quotes someone else's words has no “案例｜” first line, to tell the two apart.
- Native Google Doc: all paragraphs of a case (the first-line label paragraph included) use one set of paragraph styles: background #FBF6EC; left border 3pt solid, color #C8963E, padding 8pt; no top, bottom, or right border. With identical parameters on every paragraph of one case, Docs shows them as one box. The label paragraph is bold, text color #9A6A12, in a normal paragraph style, not a heading style; it does not enter the table of contents and takes no section number. Body text inside the box keeps its color and size. Change only the styles and insert the label paragraph; do not touch the body text.
- HTML: use `<aside class="case">`, with background, left border, and label color as above.
- Maintaining an existing draft: judge paragraph by paragraph per the case definition above; after the change, read back and check that the body text, label paragraph aside, is unchanged.

## 2 Revision discipline for long-lived drafts

Back up before changing: keep the backup at the project's established location and record its path in the edit record; with no agreed location, put it in `backups/` of the current task directory. An old project that already uses （作者本机路径） may keep that convention.

A format-only round must prove that content did not change: the conversion replaces only the characters specified for this round and protects the exceptions above; strip that class of elements and compare character by character. A punctuation conversion strips only punctuation; when headings change only their ordinals, strip only the ordinals and keep the heading text in the comparison; when clearing spaces, before and after must match once spaces are removed. If the check fails, do not write to the target file. A mechanical check cannot prove the meaning unchanged; after it passes, still review the actual diff. Written-register conversion is a wording rewrite: check meaning and style per [Conversion to written register and faithful rewriting](written-register.md), and do not apply the character-for-character identity standard of pure format tasks.

Keep evidence and process apart. Keep the records of verification ledgers, source document numbers, corrections, and rewording each on their own; process goes only into one 《改动流水》 (change log) table (date, user ruling, change, backup), one row per round. Do not retro-edit old numbers that historical records cite; add a note instead. Store an ordinary article's edit record separately, not in the body text readers see.

## 3 Available tools

Use （作者本机路径） when it exists on the current host and this round needs it; if it does not exist, check by hand.

- `heading_check.py <file.md> --len`: checks levels, ordinals, and section length; its warnings on statement headings and posed-question headings are reminders only.
- `punct_normalize.py --check <file.md>`; `--apply` is for authorized punctuation conversion, and content integrity must still be confirmed.
- `prose_mechanics.py`, `EDITOR-BRIEF-template.md`: use as the editing task requires.
- Before submission, run `scripts/voice_check.py <稿件> --clarity --names <提纲>` and `scripts/cjk_space.py <稿件> --check`; handle the report per references/clarity-acceptance.md.
- After changing any heading or section number of the four main files (FICCOutline.md, FICCStructure.md, FICCCompose.md, FICCVoice.md), run `scripts/xref_check.py`, fix every MISSING and STALE? it reports, then install. Run it too after rewording any line of a rule body (fix each STALE-QUOTE in the rationale files) and after editing a `ficc-*.md` card (fix each card MISSING, STALE-TITLE, NO-TITLE or MISSING-RULE).
