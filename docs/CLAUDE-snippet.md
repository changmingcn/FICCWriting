# CLAUDE.md snippet: route Chinese FICC prose to ficc-voice

Paste the paragraph below into `~/.claude/CLAUDE.md` (or a project CLAUDE.md) so that the main session loads `ficc-voice` for Chinese FICC prose. Adjust the list of deliverables to your own work.

```markdown
# Default prose voice

Chinese prose deliverables (research articles, monthly letters, market commentary, lecture scripts, write-ups) load `ficc-voice` — its SKILL.md is the main session's router — and run its relay from material and a research question to a finished piece. One living outline per piece, `<文稿>-提纲.md`, is the working file and comes first (saved, checked, posted in chat). `ficc-outliner` writes the question card, builds and maintains the outline and decides where each story or change sits on the tree (`FICCOutline.md`); `ficc-structurer` judges relations to parent, siblings, children and distant nodes and writes them into the outline's relation slots, returning a placement objection when a relation fails (`FICCStructure.md`); `ficc-writer` writes each node once, paragraphs and sentences together (`FICCVoice.md`), and later cold-reads the full text. `ficc-composer` is an optional paragraph-only arm. The main session reads only SKILL.md and the outline. Research reports that start from a topic and a corpus go through `ficc-hand` first, if it is installed. Not for Q&A, code, or data lookups.
```
