# Changelog

## 1.0.0 (2026-10-18)

First public release of FICCWriting, a set of five skills for writing Chinese FICC prose with Claude Code. Hand (ficc-hand/FICCHand.md, card ficc-mapper) comes first and forms the views: from a topic and a corpus it delivers a view outline, whose tree ficc-outliner builds, and a materials index. It ships in `skills/ficc-hand` and depends on skills that are not included. The writing relay follows. Outline (FICCOutline.md, card ficc-outliner) builds the outline tree and decides where each story or change sits. Structure (FICCStructure.md, card ficc-structurer) judges the relations between nodes and issues the relation sheet. Compose (FICCCompose.md, card ficc-composer) organizes the paragraphs inside a settled node. Voice (FICCVoice.md, card ficc-writer) settles sentences and wording. These four ship in `skills/ficc-voice`, whose SKILL.md routes the relay.

Licenses: the scripts (everything under `skills/*/scripts/`, plus `install.sh` and `uninstall.sh`) are under the MIT License; everything else (rule files, references, agent cards, README, docs) is under Creative Commons Attribution-NonCommercial 4.0 International. The corpus and the quoted letters, reports and drafts are published with the owner's permission under the same CC license. See `LICENSE`.
