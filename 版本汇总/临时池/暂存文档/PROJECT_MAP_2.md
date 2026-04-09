# ANINEO 影视分镜 AI 系统 - 项目地图

> **文档说明**：本文件为 ANINEO 系统的实时项目地图，用于 AI 快速定位文件、理解和导航项目结构。实时维护在 PROJECT_MAP.md 中。

---

## 一、系统概述

**ANINEO** 是一款 AI 制片人系统，采用多 Agent 协作架构，通过分层渐进式流程将剧本转化为专业分镜产出。

**当前项目状态**：
- 配置版本：V4.1
- 视觉风格：国潮动漫
- 目标媒介：漫剧
- 画面比例：16:9 横屏
- 叙事结构：经典三幕式
- 当前进度：已完成 breakdown、beatboard 阶段，正在 sequence 阶段

---

## 二、顶级目录结构

```
/Users/achi/Desktop/JEREMY/NEW/
├── AGENTS.md                              # 🏛️ 主配置文件 - 系统架构总览
├── .agent-state.json                      # 📊 运行时状态记录（核心文件）
├── .agent-state-template.json             # 📋 状态模板
├── PROJECT_MAP.md                         # 📑 本项目地图（实时维护）
├── agents/                                # 🎭 子 Agent 配置目录
├── .claude/                              # 🧠 Claude 技能系统核心
├── configs/                              # ⚙️ 配置系统
├── script/                               # 📖 用户剧本
├── outputs/                              # 📦 生成产物
├── .strategic-snapshots/                 # 💾 快照备份系统
├── 版本汇总/                              # 📚 版本历史与文档
└── smart_file_organizer.py               # 🛠️ 辅助工具
```

---

## 三、核心架构详解

### 3.1 Agent 层（agents/）

| 文件 | 功能 | 关键职责 |
|------|------|----------|
| `storyboard-artist.md` | 分镜师配置 | 节拍拆解、九宫格、四宫格生成 |
| `director.md` | 导演配置 | 专业审核、质量把关 |
| `animator.md` | 动画师配置 | 动态提示词生成 |
| `router.js` | 指令路由核心 | 解析指令并分发到对应 Agent |
| `caller.js` | Agent 调用管理 | 创建、Resume、调用 subagent |
| `agent-manager.js` | Agent 状态管理 | 监控 Agent 生命周期 |
| `producer-self-check.md` | 制片人自查 | 自检清单 |

### 3.2 SKILL 层（.claude/skills/）

#### 3.2.1 film-storyboard-skill（核心 SKILL）

```
.claude/skills/film-storyboard-skill/
├── SKILL.md                              # 🎬 技能入口与核心逻辑（33KB）
│
├── templates/                            # 📄 输出模板库
│   ├── beat-breakdown-template.md        # 节拍拆解模板
│   ├── beat-board-template.md            # 九宫格模板
│   └── sequence-board-template.md        # 动态分镜板模板
│
├── creative-engines-integration/         # 🎮 创意引擎系统（V7.0）
│   ├── 01-engine-specs.md               # 引擎规格说明
│   ├── 02-call-sequence.md              # 调用序列
│   ├── 03-output-fusion.md              # 输出融合
│   ├── 04-output-mapping.md             # 输出映射
│   ├── 05-quality-assurance.md          # 质量保证
│   └── index.md                         # 入口文件
│
├── environment-construction-guide/       # 🏗️ 环境构造系统（V2.0）
│   ├── 01-workflow.md                   # 工作流程
│   ├── 02-spatial-framework.md          # 空间骨架构建
│   ├── 03-materials.md                 # 材质皮肤覆盖
│   ├── 04-lighting.md                  # 光影氛围注入
│   ├── 05-dynamics.md                  # 动态生命添加
│   └── index.md                        # 入口文件
│
├── storyboard-methodology-playbook/     # 📖 分镜方法论
│   ├── 01-first-principles.md          # 基本原则
│   ├── 02-core-concepts.md             # 核心概念
│   ├── 03-narrative-rules.md           # 叙事规则
│   ├── 04-composition-rules.md         # 构图规则
│   ├── 05-lighting-rules.md            # 光影规则
│   ├── 06-camera-rules.md              # 镜头规则
│   ├── 07-action-rules.md             # 动作规则
│   ├── 08-emotion-rules.md            # 情绪规则
│   ├── 09-continuity-rules.md         # 连续性规则
│   ├── 10-type-templates.md           # 类型模板
│   └── index.md                       # 入口文件
│
├── creative-divergence-protocol/        # 🎭 创意发散协议
├── creative-divergence-protocol/       # 创意维度与算法
│   ├── 01-trigger-conditions.md        # 触发条件
│   ├── 02-dimensions.md               # 维度定义
│   ├── 03-algorithms.md              # 算法说明
│   └── index.md                      # 入口文件
│
└── gemini-image-prompt-guide/          # 🖼️ Gemini 图像提示词指南
    ├── 01-core-principles.md         # 核心原则
    ├── 02-templates.md              # 模板
    ├── 03-examples.md               # 示例
    └── index.md                    # 入口文件
```

#### 3.2.2 animator-skill（动画师 SKILL）

```
.claude/skills/animator-skill/
├── SKILL.md                            # 🎞️ 技能入口
│
├── motion-prompt-methodology/          # 📖 动态提示词方法论
│   ├── 01-first-principles.md         # 基本原则
│   ├── 02-structure.md                # 结构
│   ├── 03-camera-vocabulary.md       # 镜头词汇
│   ├── 04-subject-vocabulary.md      # 主体词汇
│   ├── 05-environment-vocabulary.md  # 环境词汇
│   ├── 06-speed-modifiers.md         # 速度修饰词
│   ├── 07-mood-style.md              # 情绪风格
│   └── index.md                      # 入口文件
│
├── templates/                          # 📄 动态提示词模板
├── physics-verification-rules.md      # ⚖️ 物理验证规则
│
└── montage-engine/                     # 🎬 蒙太奇引擎
    ├── montage-analysis.md           # 蒙太奇分析
    ├── rhythm-curve-generator.md     # 韵律曲线生成
    └── creative-suggestions.md      # 创意建议
```

#### 3.2.3 storyboard-review-skill（审核 SKILL）

```
.claude/skills/storyboard-review-skill/
├── SKILL.md                            # ✅ 技能入口（12KB）
│
├── review-checklist.md                 # 📋 验收清单（核心）
│
├── uncertainty-judgment-protocol.md    # 🎯 不确定项判定协议
│
├── asset-consistency-rules.md          # 🔗 资产一致性规则
│
└── executors/                          # ⚙️ 审核执行器
    └── review-executor.md             # 审核执行逻辑
```

### 3.3 工作流程层（.claude/workflows/）

| 文件 | 功能 | 优先级 |
|------|------|--------|
| `index.md` | 📑 文档导航 | - |
| `breakdown-workflow.md` | 📖 节拍拆解流程（10KB） | 高 |
| `beatboard-workflow.md` | 📖 九宫格流程（12KB） | 高 |
| `sequence-workflow.md` | 📖 动态分镜板流程（17KB） | 高 |
| `motion-workflow.md` | 📖 动态提示词流程（7KB） | 中 |
| `review-workflow.md` | 📖 审核流程（5KB） | 中 |
| `interactive-workflow.md` | 📖 交互式配置流程（8KB） | 低 |

### 3.4 共享模块层（.claude/common/）

**核心分析模块**：
- `beat-analyzer.md`（48KB）- 节拍分析器，核心算法
- `dynamic-breakdown-engine.md`（56KB）- 动态分镜引擎，V4.0 核心
- `keyframe-selector.md`（14KB）- 关键帧选择器
- `tween-algorithm.md`（30KB）- 补间算法
- `subtext-analyzer.md`（13KB）- 潜台词分析器

**布局与构图模块**：
- `card-layout-system.md`（16KB）- 卡片布局系统
- `layout-calculator.md` - 布局计算器
- `structure-profiles.md`（9KB）- 结构配置
- `keyframe-rules.md`（8KB）- 关键帧规则

**质量检查模块**：
- `quality-check.md`（6KB）- 质量检查
- `self-check-validator.md`（12KB）- 自查验证器
- `data-validator.md`（16KB）- 数据验证器
- `coherence-checker.md` - 连贯性检查器
- `flow-control-hook.md`（10KB）- 流程控制钩子

**环境构造模块**：
- `environment-asset-package.md`（14KB）- 环境资产包
- `environment-injection-optimizer.md`（14KB）- 环境注入优化器

**策略优化模块**：
- `strategy-completion.md`（12KB）- 策略补全
- `visual-thickening-optimizer.md`（12KB）- 视觉强化优化器
- `prompt-simplifier.md`（13KB）- 提示词简化器

**配置与管理模块**：
- `director-decision.md` - 导演决策参数
- `snapshot-management.md`（4KB）- 快照管理
- `user-confirmation-protocol.md`（4KB）- 用户确认协议
- `json-generator.md`（9KB）- JSON 生成器
- `exception-handler.md` - 异常处理器

### 3.5 配置层（configs/）

| 文件 | 功能 |
|------|------|
| `character-loader.py` | 🎭 角色设定加载器（6KB） |
| `character-template.md` | 🎭 角色模板 |
| `auto-extractor.py` | ⚙️ 自动提取器（15KB） |
| `config-loader.js` | ⚙️ 配置加载器 |
| `visual-style-specs.json` | 🎨 视觉风格规格 |
| `visual-style-specs-v2.json` | 🎨 视觉风格规格 V2 |
| `visual-style-specs-test.json` | 🎨 视觉风格测试规格 |
| `presets/` | 🎚️ 预设配置目录 |

---

## 四、指令系统

### 4.1 核心指令路由表

| 指令 | 子 Agent | 任务 | 产物 |
|------|----------|------|------|
| `/AINIEO` | 制片人 | 初始化欢迎 | - |
| `/breakdown [集数]` | storyboard-artist | 节拍拆解 | `scene-breakdown-{集数}.json`, `beat-breakdown-{集数}.md` |
| `/beatboard [集数]` | storyboard-artist | 九宫格关键帧 | `beat-board-prompt-{集数}-board*.md` |
| `/sequence [集数]` | storyboard-artist | 动态分镜板 | `sequence-board-prompt-{集数}.md` |
| `/motion [集数]` | animator | 动态提示词 | `motion-prompt-{集数}.md` |
| `/review breakdown [集数]` | director | 审核节拍拆解 | `breakdown-review-{集数}.md` |
| `/review beatboard [集数]` | director | 审核九宫格 | `beatboard-review-{集数}.md` |
| `/review sequence [集数]` | director | 审核四宫格 | `sequence-review-{集数}.md` |
| `/review motion [集数]` | director | 审核动态 | `motion-review-{集数}.md` |
| `/status` | 制片人 | 状态检测 | - |
| `/snapshot` | 制片人 | 快照管理 | - |
| `/creative [指令]` | storyboard-artist | 添加创意 | 对应主产物 |

### 4.2 创意引擎系统（V7.0）

| 引擎 | 功能 | 输出 |
|------|------|------|
| **蒙太奇逻辑引擎** | 分析戏剧权重、镜头拆解建议、三段式拆解 | 戏剧权重、镜头建议、置信度 |
| **影视联想引擎** | 检索匹配影片、提取视觉 DNA | 参考影片、匹配度、视觉 DNA |
| **通感视觉化引擎** | 识别感官刺激、转化视觉符号 | 触发条件、视觉转化方案 |

### 4.3 环境构造系统（V2.0）

| 阶段 | 功能 | 输出 |
|------|------|------|
| **空间骨架构建** | 定义基础空间布局、物体位置、角色活动范围 | 基础空间布局 |
| **材质皮肤覆盖** | 定义表面材质、纹理细节、物理属性 | 材质定义 |
| **光影氛围注入** | 布置光源、设计光影效果、渲染氛围 | 光影效果 |
| **动态生命添加** | 添加动态元素、粒子效果、交互响应 | 动态效果 |

---

## 五、数据流向图

```
用户剧本 (script/*.md)
    │
    ▼
┌─────────────────────────────────────────┐
│       film-storyboard-skill             │
│  ┌─────────────────────────────────┐    │
│  │ 1. breakdown → scene-breakdown  │    │
│  │ 2. beatboard → beat-board       │    │
│  │ 3. sequence → sequence-board    │    │
│  └─────────────────────────────────┘    │
└────────────────┬────────────────────────┘
                 │
    ┌────────────┼────────────┐
    ▼            ▼            ▼
┌────────┐ ┌────────┐ ┌────────────┐
│ JSON   │ │ Markdown│ │ JSON       │
│ 数据   │ │ 提示词 │ │ 元数据     │
└────────┘ └────────┘ └────────────┘
    │            │
    │     ┌──────┴──────┐
    ▼     ▼             ▼
┌─────────────────────────────────────────┐
│       storyboard-review-skill            │
│       (导演审核：PASS/FAIL/UNCERTAIN)  │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│         animator-skill                  │
│    sequence-board → motion-prompt      │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│       storyboard-review-skill           │
│       (动态审核)                        │
└─────────────────────────────────────────┘
```

---

## 六、关键文件速查

| 文件路径 | 用途 | 优先级 |
|----------|------|--------|
| `AGENTS.md` | 主配置，定义架构和协议 | 🔴 最高 |
| `.agent-state.json` | 运行时状态 | 🔴 最高 |
| `.claude/skills/film-storyboard-skill/SKILL.md` | 分镜生成核心逻辑 | 🔴 最高 |
| `.claude/skills/storyboard-review-skill/SKILL.md` | 审核核心逻辑 | 🔴 最高 |
| `.claude/common/beat-analyzer.md` | 节拍分析算法 | 🟠 高 |
| `.claude/common/dynamic-breakdown-engine.md` | 动态分镜引擎 | 🟠 高 |
| `.claude/workflows/*.md` | 各阶段工作流程 | 🟡 中 |

---

## 七、项目特征标记

### 7.1 已启用的 V4.1 优化配置

```json
{
  "v4_1_enabled": true,
  "long_beat_split_threshold": 3.5,
  "strategy_unification": true,
  "weight_correction": true,
  "dynamic_template": true,
  "keyframe_selection": true,
  "asset_package": true,
  "visual_thickening": true,
  "strategy_completion": true,
  "environment_injection": true,
  "fission_algorithm": true,
  "card_layout": true
}
```

### 7.2 策略标签系统

```
默认策略：[蒙太奇组]
可用标签：[单镜]、[动势组]、[蒙太奇组]、[长镜头]、[环境]、[特写]、[全景]、[中景]、[推拉]、[摇移]、[跟拍]、[升降]
复杂度阈值：low(2.0) / medium(3.5) / high(5.0)
```

### 7.3 类型修正系数

| 类型 | 系数 |
|------|------|
| action_adventure | 1.5 |
| suspense_thriller | 1.5 |
| horror | 1.3 |
| art_film | 1.1 |
| comedy | 0.9 |
| romance | 0.8 |
| documentary | 0.7 |

---

## 八、产物输出目录结构

```
outputs/
├── scene-breakdown-ep01.json          # 场景拆解数据
├── beat-breakdown-ep01.md             # 节拍拆解文档
├── beat-board-prompt-ep01.md          # 九宫格总览
├── beat-board-prompt-ep01-board01.md  # 关键帧1
├── beat-board-prompt-ep01-board02.md  # 关键帧2
├── beat-board-prompt-ep01-board03.md  # 关键帧3
├── beat-board-prompt-ep01-board04.md  # 关键帧4
├── beat-board-prompt-ep01-board05.md  # 关键帧5
├── beat-board-prompt-ep01-board06.md  # 关键帧6
├── beat-board-prompt-ep01-board07.md  # 关键帧7
├── beat-board-prompt-ep01-board08.md  # 关键帧8
├── beat-board-prompt-ep01-board09.md  # 关键帧9
├── beat-board-prompt-ep01-review.md   # 审核记录
├── beat-board-prompt-ep01-review-v2.md # 审核记录 V2
├── sequence-board-prompt-ep01.md      # 动态分镜板
└── motion-prompt-ep01.md              # 动态提示词
```

---

## 九、快照系统

```
.strategic-snapshots/
├── snapshot-20260201-132819/          # 快照历史
├── snapshot-20260201-132825/
├── snapshot-20260201-141321/
├── snapshot-20260201-141322/
└── snapshot-20260203-171844-config-update.json  # 最新快照
```

---

## 十、快速定位指南

| 需求 | 文件路径 |
|------|----------|
| 修改节拍分析逻辑 | `.claude/common/beat-analyzer.md` |
| 修改关键帧选择算法 | `.claude/common/keyframe-selector.md` |
| 添加新的审核标准 | `.claude/skills/storyboard-review-skill/review-checklist.md` |
| 修改输出模板 | `.claude/skills/film-storyboard-skill/templates/` |
| 理解整体流程 | `.claude/workflows/` 或 `AGENTS.md` |
| 调试角色加载 | `configs/character-loader.py` |
| 查看当前状态 | `.agent-state.json` |
| 配置项目设置 | `.agent-state.json` |
| 理解 Agent 协作 | `agents/*.md` |
| 查找审核规则 | `.claude/skills/storyboard-review-skill/` |

---

## 十一、版本历史

| 版本 | 日期 | 主要变更 |
|------|------|----------|
| V4.1 | 2026-02-03 | 动态分镜板生成、策略标签系统、裂变协议 |
| V4.0 | 2026-01-31 | 动态分镜引擎、新增 workflow 目录 |
| V3.0 | 2026-01-20 | 多结构叙事模板、潜台词分析、类型化权重 |
| V2.0 | 2026-01-15 | 方案 B 流程、Resume 机制 |

---

**文档维护**：实时更新于 PROJECT_MAP.md
**最后更新**：2026-02-03
