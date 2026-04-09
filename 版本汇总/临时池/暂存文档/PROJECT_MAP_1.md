# 🗺️ ANINEO Project Map (Live)

> **Last Updated:** 2026-02-03 (Auto-Generated)
> **System Context:** This is the automated file index for the ANINEO system.
> **Instruction:** When looking for specific logic or assets, refer to the paths below.

## 🧠 Architecture Logic (架构意图)

### 1. Agent Layer (`agents/`)
* **Role:** 定义智能体的“人设”与“路由”。
* **Core Files:**
    * `storyboard-artist.md`: 执行 /breakdown → /beatboard → /sequence 流程。
    * `director.md`: 执行 /review 系列审核流程。
    * `animator.md`: 执行 /motion 生成动态提示词。
    * `router.js`: 核心指令路由，分发任务。

### 2. Skill Layer (`.claude/skills/`)
* **Role:** 智能体的“技能包”，包含具体的方法论和模板。
* **Key Modules:**
    * `film-storyboard-skill/`: [核心] 分镜生成逻辑。
    * `animator-skill/`: [动态] 动态提示词生成逻辑。
    * `storyboard-review-skill/`: [质检] 审核逻辑。

### 3. Common Logic (`.claude/common/`)
* **Role:** 共享算法库与底层引擎。
* **Critical Algorithms:** `beat-analyzer.md` (节拍分析), `dynamic-breakdown-engine.md` (动态引擎).

---

## 📂 File Directory (物理文件树)

```text
.
├── AGENTS.md                          # 🏛️ 主配置文件(System Core)
├── PROJECT_MAP.md                     # 🗺️ 实时项目地图(本文件)
├── .agent-state.json                  # 📊 运行时状态记录
├── agents/                            # 🎭 子 Agent 配置目录
│   ├── storyboard-artist.md           # [核心] 分镜师配置
│   ├── director.md                    # [核心] 导演配置
│   ├── animator.md                    # [核心] 动画师配置
│   └── router.js                      # 指令路由逻辑
├── .claude/
│   ├── workflows/                     # 📝 SOP 工作流文档
│   ├── common/                        # 🔧 通用算法与逻辑
│   └── skills/                        # 🎯 SKILL 技能包入口
├── configs/                           # ⚙️ 角色与风格配置
├── script/                            # 📖 用户剧本存放处
├── outputs/                           # 📦 最终产出目录
└── .strategic-snapshots/              # 💾 快照备份系统
