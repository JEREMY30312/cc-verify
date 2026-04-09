# 🗺️ 项目地图 (Live)

> **Updated:** 2026-04-09 11:14:07
 > **Version:** 2.2 | **Mode:** 智能层级 + 关键文件识别 + LLM描述

## 🔥 最近变动 (7天)

_暂无变更记录_

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
│   ├── README.md  # 单文件项目地图生成器，支持Git集成、L
│   ├── TROUBLESHOOTING.md
│   ├── install.sh
│   └── standalone.py
├── project_root
│   ├── _legacy_backup
│   ├── agents
│   │   ├── director_agent.yaml
│   │   └── storyboard_artist_agent.yaml
│   ├── library
│   │   ├── contracts
│   │   │   ├── beat-analysis-schema.json
│   │   │   └── shot-board-schema.json
│   │   ├── examples
│   │   │   └── beat-analysis-examples.json
│   │   └── prompts
│   │       ├── beat-analysis-core.txt
│   │       └── shot-expansion-core.txt
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
│       │   ├── beat-board-template.md
│       │   ├── beatboard-workflow.md
│       │   ├── beatboard-workflow.textClipping
│       │   ├── environment-construction-guide
│       │   │   └── ...
│       │   ├── environment-injection-optimizer.md
│       │   ├── keyframe-selector.md
│       │   ├── prompt-simplifier.md
│       │   └── visual-thickening-optimizer.md
│       ├── 四宫格
│       │   ├── dynamic-breakdown-engine.md
│       │   ├── sequence-board-template.md
│       │   └── sequence-workflow.md
│       ├── 导演
│       │   ├── SKILL.md  # 分镜审核技能。用于审核分镜师产出的节拍拆
│       │   ├── coherence-checker.md
│       │   ├── director.md
│       │   └── quality-check.md
│       ├── 用户确认（是否有更简洁有效的办法）
│       │   ├── user-confirmation-protocol（确认协议）.md
│       │   └── user-confirmation-workflow确认流程.md
│       └── 节拍拆解
│           ├── beat-analyzer.md
│           ├── beat-breakdown-template.md
│           ├── breakdown-workflow.md
│           ├── creative-engines-integration
│           │   └── ...
│           ├── data-validator.md
│           ├── storyboard-artist.md
│           └── structure-profiles.md
├── script
│   └── 猪打镇关西_v2.0.md
├── smart_file_organizer.py
├── start_organizer.sh
├── test_scripts
│   ├── test_dynamic_breakdown.py
│   ├── test_full_integration.py
│   ├── test_granularity_reorganization.py
│   ├── test_montage_authority.py
│   ├── test_type_weight_correction.py
│   └── test_v4_1_fission.py
└── 版本汇总
    └── ...
```

---
*由 generate_map.py V2.2 自动生成*
