# 🗺️ 项目地图 (Live)

> **Updated:** 2026-04-13 14:43:12
 > **Version:** 2.2 | **Mode:** 智能层级 + 关键文件识别 + LLM描述

## 🔥 最近变动 (7天)

| 文件 | 目录 | 变更 | 时间 | 描述 |
|------|------|------|------|------|
| enerate_map.py | 根目录 | 🟢 修改 | - | - |
| standalone.py | portable | 🟢 修改 | - | - |

## 📂 文件目录

```text
.
├── AGENTS.md
├── PROJECT_FINGERPRINT.json
├── PROJECT_MAP.md
├── agents
│   ├── QUICK_REFERENCE.md
│   ├── README.md
│   ├── agent-manager.js
│   ├── animator
│   ├── animator.md
│   ├── animator.md.backup
│   ├── caller.js
│   ├── caller.js.backup
│   ├── director
│   ├── director.md.backup
│   ├── producer-self-check.md
│   ├── router.js
│   ├── router.js.backup
│   ├── storyboard-artist
│   ├── storyboard-artist.md
│   └── storyboard-artist.md.backup
├── check_root.sh
├── configs
│   ├── auto-extractor.py
│   ├── character-loader.py
│   ├── character-template.md
│   ├── config-loader.js
│   ├── presets
│   │   ├── presets.json
│   │   ├── 国潮动漫.json
│   │   ├── 日漫风格.json
│   │   ├── 皮克斯风格.json
│   │   ├── 真人写实.json
│   │   └── 赛博朋克.json
│   ├── usage-example.md
│   ├── visual-style-specs-test.json
│   ├── visual-style-specs-v2.json
│   └── visual-style-specs.json
├── generate_map.py
├── hooks
│   ├── install.sh
│   ├── post-checkout
│   ├── post-commit
│   ├── post-merge
│   └── scripts
│       └── hook_runner.py
├── modules
│   ├── description_cache.py
│   └── llm_task_generator.py
├── organizer-error.log
├── organizer.log
├── outputs
│   ├── beat-board-full-list-ep01.json
│   ├── beat-board-prompt-ep01-board1.md  # 猪打镇关西 ep01 Board 1 九
│   ├── beat-board-prompt-ep01-board2.md  # 猪打镇关西 ep01 Board 2 九
│   ├── beat-board-prompt-ep01.md  # 猪打镇关西 ep01 九宫格提示词总览
│   ├── beat-breakdown-ep01.md  # 猪打镇关西 ep01 节拍拆解表，包含戏
│   ├── beatboard-review-ep01.md  # 导演对 ep01 九宫格提示词的审核报告
│   ├── breakdown-review-ep01.md  # 导演对 ep01 节拍拆解的审核报告
│   ├── scene-breakdown-ep01.json
│   ├── sequence-board-prompt-ep01.md  # 猪打镇关西 ep01 动态分镜板提示词（
│   └── sequence-review-ep01.md  # 导演对 ep01 动态分镜板的审核报告
├── portable
│   ├── PROJECT_FINGERPRINT.json
│   ├── PROJECT_MAP.md
│   ├── README.md  # 单文件项目地图生成器，支持Git集成、L
│   ├── TROUBLESHOOTING.md
│   ├── generate-descriptions
│   │   ├── claude.md  # 自动检测并处理文件描述任务，为项目地图生
│   │   └── opencode.md  # 自动检测并处理文件描述任务，为项目地图生
│   ├── install.sh
│   └── standalone.py
├── project_root
│   ├── _legacy_backup
│   ├── agents
│   │   ├── director_agent.yaml
│   │   └── storyboard_artist_agent.yaml
│   ├── library
│   │   ├── contracts
│   │   │   └── ...
│   │   ├── examples
│   │   │   └── ...
│   │   └── prompts
│   │       └── ...
│   ├── outputs
│   ├── tools
│   │   ├── strategy_mapper.py
│   │   └── weight_calculator.py
│   ├── workflows
│   │   └── breakdown_workflow.py
│   └── 迁移中转
│       ├── SKILL.md  # 影视分镜生成技能。将剧本转化为分镜产出，
│       ├── beat-analyzer.md
│       ├── director-decision.md
│       ├── exception-handler.md
│       ├── interactive-workflow（初始化:配置）.md
│       ├── snapshot-management（快照管理规则）.md
│       ├── 九宫格
│       │   └── ...
│       ├── 四宫格
│       │   └── ...
│       ├── 导演
│       │   └── ...
│       ├── 用户确认（是否有更简洁有效的办法）
│       │   └── ...
│       └── 节拍拆解
│           └── ...
├── script
│   └── 猪打镇关西_v2.0.md
├── smart_file_organizer.py
├── start_organizer.sh
├── test_scripts
│   └── ...
└── 版本汇总
    └── ...
```

---
*由 generate_map.py V2.2 自动生成*
