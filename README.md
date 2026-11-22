# FICCWriting

## 这是什么

FICCWriting是一套给Claude Code用的中文FICC写作技能，用于研究文章、月报、市场评论、讲义、案例讲稿和录音稿书面化。

五个技能分两段。第一个技能Hand形成观点：从题目和语料出发，交出观点提纲和资料索引。后四个技能接着写作，从材料和研究问题出发，把一篇稿子从无到有写出来：Outline立问题卡、搭提纲并决定每个故事放在哪里，Structure判断节点之间的关系，Voice管段落、句子和措辞，每个节点一次写成。2.0.0起Compose的规则并进了Voice，composer卡只留作可选的单列段落席。观点已经定了的稿子（例如月报、讲义）不经过Hand，直接从Outline开始。改写已成的旧稿是次要入口，先从原稿归纳提纲。

规则文件是英文写的简练规则，例句和语料是中文。普通金融问答、取数和计算不用这套技能。

没有Claude Code也能用：`skills/ficc-voice/SKILL.md`第5节是单窗口对话做法，一个模型在一个对话窗口里，不用脚本和代理卡，按五步走完同一条主干，每步有关卡问题。

## 五个技能

| 序号 | 技能 | 规则文件 | 代理卡 | 管什么 |
|---|---|---|---|---|
| 1 | Hand | `ficc-hand/FICCHand.md` | `ficc-mapper`（观点树由 `ficc-outliner` 搭） | 形成观点：题目和语料 → 观点提纲和资料索引 |
| 2 | Outline | `FICCOutline.md` | `ficc-outliner` | 提纲与安放 |
| 3 | Structure | `FICCStructure.md` | `ficc-structurer` | 关系 |
| 4 | Compose | 2.0.0并入`FICCVoice.md`（§0–§2） | `ficc-composer`（可选） | 单列的段落席，只在对照时用 |
| 5 | Voice | `FICCVoice.md` | `ficc-writer` | 段落、句子与措辞，每个节点一次写成 |

Hand装在 `skills/ficc-hand`。后四个技能都装在 `skills/ficc-voice` 里，由它的 `SKILL.md` 统一路由。每篇稿子只有一份活提纲`<文稿>-提纲.md`，问题卡、名字表、提纲树、事实与算式行、节点之间的关系都写在里面。五张代理卡在 `agents/` 下，装到 `~/.claude/agents/`。

## 目录

```
FICCWriting/
  README.md  VERSION  CHANGELOG.md
  LICENSE  LICENSE-MIT  LICENSE-CC-BY-NC-4.0
  install.sh  uninstall.sh
  docs/CLAUDE-snippet.md     CLAUDE.md 路由段落样例
  skills/ficc-hand/          Hand 及对账脚本
  skills/ficc-voice/         Outline、Structure、Voice（含原Compose）及脚本
  agents/ficc-*.md           五张代理卡
```

`skills/ficc-voice/ficc-voice.md` 是符号链接，指向同目录的 `FICCVoice.md`。在不支持符号链接的环境里（例如Windows上关掉symlink的克隆，或GitHub的zip下载），它会变成一个只写着文件名的小文本文件，不影响使用。

## 运行要求

- Claude Code（技能目录 `~/.claude/skills/`，代理卡目录 `~/.claude/agents/`）。
- Python 3.9或更新版本，只用标准库，不需要安装第三方包。
- POSIX sh，用于安装和卸载脚本。
- `skills/ficc-voice/scripts/` 下各脚本的用法见同目录的 `README.md`。各脚本每一版改了什么也记在那份`README.md`里。`changed_sentences.py`要调用作者shared-protocols里的`sentence_diff.py`，`number_set_diff.py`和`inline_guards.py`又调用`changed_sentences.py`。2.0.0起`sentence_diff.py`附在同一目录，这几个脚本都能直接跑。`sentence_diff.py`自己的`--out`选项只往作者任务目录（含`work.json`的目录）里写文件，别处会被拒绝，包里的脚本都不用它。

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
python3 ~/.claude/skills/ficc-voice/scripts/outline_slice.py --self-test
python3 ~/.claude/skills/ficc-voice/scripts/inline_guards.py --selftest
python3 ~/.claude/skills/ficc-voice/scripts/number_set_diff.py --selftest
python3 ~/.claude/skills/ficc-voice/scripts/changed_sentences.py --selftest
python3 ~/.claude/skills/ficc-voice/scripts/sentence_diff.py --selftest
```

卸载，或卸载后放回安装前的备份：

```sh
sh uninstall.sh [--prefix DIR]
sh uninstall.sh [--prefix DIR] --restore ~/.claude/ficc-writing-backup-<UTC时间>
```

装完要新开一个Claude Code会话，新的技能和代理卡才会生效。若想让主会话遇到中文FICC文稿时自动加载 `ficc-voice`，把 `docs/CLAUDE-snippet.md` 里的段落加进自己的 `CLAUDE.md`。

## 依赖

Hand（`ficc-hand`）依赖以下技能和代理卡，本仓库不包含它们：

- 技能：research-agent、dynamic-workflow、first-secretary、shared-protocols、ficc-research-kit。
- 代理卡：scout、digester、collator、dissenter、refuter。另有一个席位用Claude Code内置的general-purpose代理，不需要卡。

1.3.0起，`FICCHand.md`写成research-agent调研流程上的一层FICC增量。各步的关卡和任务角色（主干问题、明确必答项、探索线索）的完整规则在research-agent里，摘要模板在digester卡里，`FICCHand.md`只写每一步交什么、谁来做、FICC特有的完成条件。`FICCHand.md`说的top-review席（红队）和`ficc-voice/SKILL.md`第④步的标题级反驳席是同一类席位，作者按shared-protocols的`model-tiers.md`给它配卡和模型，用的是refuter卡。`references/glossary.md`里的refuter-t1e是作者给refuter配的固定模型版本，卡的正文和refuter相同，没有这张卡时用refuter即可。没有这些依赖时，`ficc-hand`的规则文件仍可阅读，它的对账脚本`tieout.py`也能单独跑，但完整流程跑不通。

后四个写作席位（outliner、structurer、composer、writer）自己就能跑。1.3.0起，各席的卡要求把结果写成一份结果文件：开头一段`## Head`，中间是结果单或检查报告，末尾是`Trace:`、`Lesson:`、`Open:`几行。这个格式出自作者shared-protocols下的`handoff.md`，本仓库不含它，卡里已经把要点写全，照卡写即可。1.3.0起`references/dispatch-notes.md`点到shared-protocols的两个脚本：`handoff.py`生成派单开头的状态卡，`replace_once.py`按清单做已经定好的字面替换。没有它们时，状态卡手写，字面替换由主会话自己改。2.0.0起活提纲里争议事实后面带的问题号（I-nn）沿用research-agent的`references/analysis.md`里的定义，本仓库不含，按“账本里一条冲突或未决问题的编号”理解即可。

`ficc-voice/SKILL.md`第④步（冷读、原件核对与受限修补）另用两样本仓库不含的东西：查来源的席位按shared-protocols的`source-check.md`工作，标题级反驳席用refuter或dissenter代理卡。没有它们时，另外两项检查照常跑：结构检查由structurer的check模式一次读完FICCOutline.md §9、FICCStructure.md §7和FICCVoice.md §4，表达检查由writer先冷读、再按`references/clarity-acceptance.md`查清晰。研究文章的反方席位不能省（SKILL.md 4第7条），没有这两张卡就由使用者另配一个等效的反方读者。

`voice_check.py` 的月报基线模式（`--baseline`，以及 `--selftest` 里的2026.02对照）读你自己的月报合辑文件，用 `scripts/README.md` 里写的 `--letters` 选项指定，默认路径是 `~/ficc-letters/letters.txt`。文件不存在时，自检跳过2026.02对照，其余照常。

交付到Google Docs是可选步骤。`ficc-voice` 默认以Markdown为工作稿，没有Google Drive工具时直接交Markdown即可。

## 标签与占位符

- 代理卡和规则文件里的T0、T1、T1E、T3是作者给模型分档的标签。T0指主会话，其余几档标明各席位用哪一档模型，按自己的模型配置理解即可。
- 例子出处里的1012Six、《1012散户》、《1009AI表外》等短名是作者自己文章的名字。
- “（作者草稿）”“（作者本机路径）”“（作者的用量审计报告）”“（审计数据表）”是公开版替换掉的本机路径和工作目录，原文件不随仓库发布。
- `scripts/README.md`和`scripts/budget.json`里的W1、W4b、D8、Wave K之类是作者开发轮次的编号，1120、Wave-2之类是作者回归样本的名字，只作沿革记录，按字面理解即可。
- 规则里写的“CLAUDE.md, Proportion”指作者全局指令里的比例原则：核查和返工的力度看它能不能改变结论，默认一轮审查加一次针对改动处的复读。“memory `…`”指作者本机的记忆条目。这两样都不随仓库发布，按字面理解即可。

## 未包含的内容

- 开发记录：`skills/ficc-voice/references/` 下的 `dev-notes.md`、`FICCVoice-provenance.md`、`history.md`，以及 `skills/ficc-hand/references/hand-history.md`。这些是作者的开发过程记录，含私人项目和工作目录，不随公开版发布。仓库里保留同名的占位文件，只留原有各级标题，保证其他文件里指向这些章节的引用仍然有效。
- 中文存档：规则文件2026-10-16改为英文后，中文原版只作存档，代理不读，所以不收。1.2.0及以前，仓库在`skills/ficc-voice/references/zh/`下留了三份rationale的占位文件。2026-11-14作者把中文存档移出了技能目录，1.3.0起仓库里不再有`zh/`，三份rationale文件和`SKILL.md`第4节第13条只写明中文原版不随本版发布。`scripts/README.md`和`xref_check.py`里按`references/zh/`同名文件核对标题的那一项，1.3.0起不会触发。
- Codex侧元数据：`skills/ficc-voice/agents/openai.yaml`。它只供另一套代理环境使用，Claude Code用不到。
- 调度卡`ficc-conductor`：写作阶段的指挥席，2026-10-25起试用，2026-11-14起成为ficc-hand成稿任务的常设做法。主会话为写作阶段的每一波（接力、检查、收尾）各派一个新的指挥席，它从卡和任务目录里的`conductor-progress.md`起步。这张卡绑在作者自己的任务记录和交接脚本上（first-secretary，以及shared-protocols的`handoff.py`），所以不收。`skills/ficc-voice/SKILL.md`第1节、`references/dispatch-notes.md`、`ficc-hand/SKILL.md`、`FICCHand.md`第7步（交接）和`ficc-hand/references/handoff.md`提到它。没有这张卡时，交接后由主会话自己按`ficc-voice/SKILL.md`路由。
- 内联写手席脚本`skills/ficc-voice/scripts/inline-seat/`：`references/dispatch-notes.md`第7节说的DeepSeek起草席所用的一套脚本，绑在作者自己的模型路由上（作者的模型分级登记，以及dynamic-workflow下的模型适配器，本仓库都不含），所以不收。`skills/ficc-voice/SKILL.md`第2节③④两行和短篇一段、`dispatch-notes.md`第7节、`scripts/README.md`的inline-seat一节和2.0.0各轮改动记录提到它。没有这套脚本时，接力照常用ficc-writer卡起草和修补。它用的事实闸`scripts/inline_guards.py`随包发布，可以单独跑。
- 维护说明`MAINTAINERS.md`：作者放在shared-protocols下的维护笔记，不随公开版发布。`skills/ficc-voice/`下的`references/FICCVoice-rationale.md`、`scripts/README.md`和`scripts/budget_check.py`提到它，指的是作者改规则时守的规矩，脚本不读这个文件。
- 1.3.0撤下的三个文件：`skills/ficc-voice/references/`下的`source-style-notes.md`和`writing-checklist.md`，以及`scripts/cjk_space.py`。前两份作者已经归档，规则文件不再指向它们。`cjk_space.py`按作者2026-11-07的裁定退役，中文与英文、数字之间不留空格的约定不变，改由人工整理。
- 2.0.0撤下的七个文件：`skills/ficc-voice/FICCCompose.md`（规则并进`FICCVoice.md`，C号不变），以及`references/`下的`compose-excerpt.md`、`relation-sheet-template.md`（关系改写在活提纲里）和四份按模式摘录`voice-excerpt-draft.md`、`voice-excerpt-polish.md`、`voice-excerpt-patch.md`、`voice-excerpt-coldread.md`（各席改按职责读`FICCVoice.md`的节）。作者已经归档，不随本版发布。`scripts/README.md`和`xref_check.py`里核对摘录的几项，文件不在时跳过。

## 版本与许可证

当前版本2.0.0（2026-11-21），见 `VERSION` 和 `CHANGELOG.md`。主版本号升到2，是因为写作规则从四本合成三本，旧版里指向`FICCCompose.md`的做法要改读`FICCVoice.md`。

许可证分两部分，详见 `LICENSE`：

- 脚本用MIT许可证（全文见 `LICENSE-MIT`），范围是 `skills/*/scripts/` 下的全部文件，以及 `install.sh`、`uninstall.sh`。
- 其余内容用知识共享署名-非商业性使用4.0国际许可协议（CC BY-NC 4.0，见 `LICENSE-CC-BY-NC-4.0`），包括规则文件、参考文件、代理卡、README和 `docs/`。`references/corpus/` 里的语料（《九节》《熊猫讲期权》）和参考文件里引用的月报、研报、草稿，经仓库所有者许可按同一许可协议发布。
