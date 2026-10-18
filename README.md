# FICCWriting

## 这是什么

FICCWriting 是一套给 Claude Code 用的中文 FICC 写作技能，用于研究文章、月报、市场评论、讲义、案例讲稿和录音稿书面化。

五个技能分两段。第一个技能 Hand 形成观点：从题目和语料出发，交出观点提纲和资料索引。后四个技能接着分工写作：Outline 搭提纲并决定每个故事放在哪里，Structure 判断节点之间的关系，Compose 在节点内组织段落，Voice 定句子和措辞。观点已经定了的稿子（例如月报、讲义、旧稿改写）不经过 Hand，直接从 Outline 开始。

规则文件是英文写的简练规则，例句和语料是中文。普通金融问答、取数和计算不用这套技能。

## 五个技能

| 序号 | 技能 | 规则文件 | 代理卡 | 管什么 |
|---|---|---|---|---|
| 1 | Hand | `ficc-hand/FICCHand.md` | `ficc-mapper`（观点树由 `ficc-outliner` 搭） | 形成观点：题目和语料 → 观点提纲和资料索引 |
| 2 | Outline | `FICCOutline.md` | `ficc-outliner` | 提纲与安放 |
| 3 | Structure | `FICCStructure.md` | `ficc-structurer` | 关系 |
| 4 | Compose | `FICCCompose.md` | `ficc-composer` | 段落 |
| 5 | Voice | `FICCVoice.md` | `ficc-writer` | 句子与措辞 |

Hand 装在 `skills/ficc-hand`。后四个技能都装在 `skills/ficc-voice` 里，由它的 `SKILL.md` 统一路由。五张代理卡在 `agents/` 下，装到 `~/.claude/agents/`。

## 目录

```
FICCWriting/
  README.md  VERSION  CHANGELOG.md
  LICENSE  LICENSE-MIT  LICENSE-CC-BY-NC-4.0
  install.sh  uninstall.sh
  docs/CLAUDE-snippet.md     CLAUDE.md 路由段落样例
  skills/ficc-hand/          Hand 及对账脚本
  skills/ficc-voice/         Outline、Structure、Compose、Voice 及脚本
  agents/ficc-*.md           五张代理卡
```

`skills/ficc-voice/ficc-voice.md` 是符号链接，指向同目录的 `FICCVoice.md`。在不支持符号链接的环境里（例如 Windows 上关掉 symlink 的克隆，或 GitHub 的 zip 下载），它会变成一个只写着文件名的小文本文件，不影响使用。

## 运行要求

- Claude Code（技能目录 `~/.claude/skills/`，代理卡目录 `~/.claude/agents/`）。
- Python 3.9 或更新版本，只用标准库，不需要安装第三方包。
- POSIX sh，用于安装和卸载脚本。

## 安装、测试、卸载

安装到 `~/.claude`：

```sh
sh install.sh
```

装到别的目录（文件落在 `DIR/.claude/` 下）：

```sh
sh install.sh --prefix DIR
```

安装前若已有同名技能或代理卡，脚本会先把旧文件移到 `~/.claude/ficc-writing-backup-<UTC时间>/`，并打印恢复命令。装完自动跑自检，任一项不过就以非零状态退出。

单独跑自检：

```sh
python3 ~/.claude/skills/ficc-voice/scripts/xref_check.py -q
python3 ~/.claude/skills/ficc-voice/scripts/xref_check.py --selftest
python3 ~/.claude/skills/ficc-voice/scripts/voice_check.py --selftest
python3 ~/.claude/skills/ficc-voice/scripts/voice_check.py --selftest --clarity
python3 ~/.claude/skills/ficc-hand/scripts/tieout.py --self-test
python3 ~/.claude/skills/ficc-hand/scripts/test_tieout.py
```

卸载，或卸载后放回安装前的备份：

```sh
sh uninstall.sh [--prefix DIR]
sh uninstall.sh [--prefix DIR] --restore ~/.claude/ficc-writing-backup-<UTC时间>
```

装完要新开一个 Claude Code 会话，新的技能和代理卡才会生效。若想让主会话遇到中文 FICC 文稿时自动加载 `ficc-voice`，把 `docs/CLAUDE-snippet.md` 里的段落加进自己的 `CLAUDE.md`。

## 依赖

Hand（`ficc-hand`）依赖以下技能和代理卡，本仓库不包含它们：

- 技能：research-agent、dynamic-workflow、first-secretary、shared-protocols、ficc-research-kit。
- 代理卡：scout、digester、collator、dissenter、refuter。另有一个席位用 Claude Code 内置的 general-purpose 代理，不需要卡。

没有这些依赖时，`ficc-hand` 的规则文件仍可阅读，它的对账脚本 `tieout.py` 也能单独跑，但完整流程跑不通。

后四个写作席位（outliner、structurer、composer、writer）自己就能跑，不依赖别的技能。只有 `ficc-voice/SKILL.md` 第⑥步（检查）另用两样本仓库不含的东西：查来源的席位按 shared-protocols 的 `source-check.md` 工作，反方席位用 refuter 或 dissenter 代理卡。没有它们时，四个席位照常跑各自的检查，即 FICCOutline.md 9、FICCStructure.md 10、FICCCompose.md 7 和 FICCVoice.md 7。研究文章的反方席位不能省（SKILL.md 4 第 7 条），没有这两张卡就由使用者另配一个等效的反方读者。

`voice_check.py` 的月报基线模式（`--baseline`，以及 `--selftest` 里的 2026.02 对照）读你自己的月报合辑文件，用 `scripts/README.md` 里写的 `--letters` 选项指定，默认路径是 `~/ficc-letters/letters.txt`。文件不存在时，自检跳过 2026.02 对照，其余照常。

交付到 Google Docs 是可选步骤。`ficc-voice` 默认以 Markdown 为工作稿，没有 Google Drive 工具时直接交 Markdown 即可。

## 标签与占位符

- 代理卡和规则文件里的 T0、T1、T1E、T3 是作者给模型分档的标签。T0 指主会话，其余几档标明各席位用哪一档模型，按自己的模型配置理解即可。
- 例子出处里的 1012Six、《1012散户》、《1009AI表外》等短名是作者自己文章的名字。
- “（作者草稿）”“（作者本机路径）”“（作者的用量审计报告）”“（审计数据表）”是公开版替换掉的本机路径和工作目录，原文件不随仓库发布。

## 未包含的内容

- 开发记录：`skills/ficc-voice/references/` 下的 `dev-notes.md`、`FICCVoice-provenance.md`、`history.md`，以及 `skills/ficc-hand/references/hand-history.md`。这些是作者的开发过程记录，含私人项目和工作目录，不随公开版发布。仓库里保留同名的占位文件，只留原有各级标题，保证其他文件里指向这些章节的引用仍然有效。
- 中文存档：`skills/ficc-voice/references/zh/`。规则文件 2026-10-16 改为英文后，中文原版只作存档，代理不读，所以不收。三份 rationale 文件的英文版指向各自的中文原版，所以 `zh/` 下留了这三份的占位文件。
- Codex 侧元数据：`skills/ficc-voice/agents/openai.yaml`。它只供另一套代理环境使用，Claude Code 用不到。

## 版本与许可证

当前版本 1.0.0（2026-10-18），见 `VERSION` 和 `CHANGELOG.md`。

许可证分两部分，详见 `LICENSE`：

- 脚本用 MIT 许可证（全文见 `LICENSE-MIT`），范围是 `skills/*/scripts/` 下的全部文件，以及 `install.sh`、`uninstall.sh`。
- 其余内容用知识共享署名-非商业性使用 4.0 国际许可协议（CC BY-NC 4.0，见 `LICENSE-CC-BY-NC-4.0`），包括规则文件、参考文件、代理卡、README 和 `docs/`。`references/corpus/` 里的语料（《九节》《熊猫讲期权》）和参考文件里引用的月报、研报、草稿，经仓库所有者许可按同一许可协议发布。
