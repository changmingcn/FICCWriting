# CLAUDE.md snippet: route Chinese FICC prose to ficc-voice

Paste the paragraph below into `~/.claude/CLAUDE.md` (or a project CLAUDE.md) so that the main session loads `ficc-voice` for Chinese FICC prose. Adjust the list of deliverables to your own work.

```markdown
# Default prose voice

Chinese prose deliverables (research articles, monthly letters, market commentary, lecture scripts, write-ups) load `ficc-voice` — its SKILL.md is the main session's router — and run its four-seat relay. The outline is the working file and comes first (saved, checked, posted in chat). `ficc-outliner` builds and maintains the outline and decides where each story or change sits on the tree (`FICCOutline.md`); `ficc-structurer` judges relations to parent, siblings, children and distant nodes and issues the relation sheet, returning a placement objection when a relation fails (`FICCStructure.md`); `ficc-composer` organizes the paragraphs of one node (`FICCCompose.md`); `ficc-writer` settles that node's sentences and wording (`FICCVoice.md`). The main session reads only SKILL.md and the outline. Research reports that start from a topic and a corpus go through `ficc-hand` first, if it is installed. Not for Q&A, code, or data lookups.
```
