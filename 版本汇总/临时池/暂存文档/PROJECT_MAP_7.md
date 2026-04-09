# ANINEO 影视分镜 AI 系统 - 项目地图

> 实时维护于 PROJECT_MAP.md

## 一、系统概述

**ANINEO** - AI 制片人系统，多 Agent 协作架构

**当前状态**：
- 版本：V4.1
- 视觉风格：国潮动漫
- 目标媒介：漫剧
- 进度：sequence 阶段

## 二、顶级目录结构

/Users/achi/Desktop/JEREMY/NEW/
├── AGENTS.md                    # 主配置
├── .agent-state.json            # 运行时状态
├── PROJECT_MAP.md              # 本项目地图
├── generate_map.py             # 地图生成器
├── agents/                     # 子 Agent 配置
├── .claude/                    # 技能系统核心
├── configs/                    # 配置系统
├── script/                     # 用户剧本
├── outputs/                   # 生成产物
├── .strategic-snapshots/       # 快照备份
└── 版本汇总/                  # 版本历史

## 三、Agent 层（agents/）

| 文件 | 功能 |
|------|------|
| storyboard-artist.md | 分镜师：节拍拆解、九宫格、四宫格 |
| director.md | 导演：专业审核 |
| animator.md | 动画师：动态提示词 |
| router.js | 指令路由 |
| caller.js | Agent 调用管理 |

## 四、SKILL 层（.claude/skills/）

### film-storyboard-skill（核心）
- SKILL.md - 技能入口
- templates/ - 输出模板
- creative-engines-integration/ - 创意引擎
- environment-construction-guide/ - 环境构造
- storyboard-methodology-playbook/ - 分镜方法论

### animator-skill
- SKILL.md - 技能入口
- motion-prompt-methodology/ - 动态提示词方法论
- montage-engine/ - 蒙太奇引擎

### storyboard-review-skill
- SKILL.md - 审核入口
- review-checklist.md - 验收清单
- executors/ - 审核执行器

## 五、工作流程（.claude/workflows/）

- breakdown-workflow.md - 节拍拆解
- beatboard-workflow.md - 九宫格
- sequence-workflow.md - 动态分镜板
- motion-workflow.md - 动态提示词
- review-workflow.md - 审核流程

## 六、核心指令路由表

| 指令 | Agent | 任务 | 产物 |
|------|-------|------|------|
| /AINIEO | 制片人 | 初始化 | -
| /breakdown [集数] | storyboard-artist | 节拍拆解 | scene-breakdown-{集数}.json, beat-breakdown-{集数}.md
| /beatboard [集数] | storyboard-artist | 九宫格 | beat-board-prompt-{集数}-board*.md
| /sequence [集数] | storyboard-artist | 动态分镜板 | sequence-board-prompt-{集数}.md
| /motion [集数] | animator | 动态提示词 | motion-prompt-{集数}.md
| /review [类型] [集数] | director | 审核 | xxx-review-{集数}.md

## 七、快速定位

| 需求 | 文件路径 |
|------|----------|
| 修改节拍分析 | .claude/common/beat-analyzer.md
| 修改审核标准 | .claude/skills/storyboard-review-skill/review-checklist.md
| 修改模板 | .claude/skills/film-storyboard-skill/templates/
| 查看流程 | .claude/workflows/ 或 AGENTS.md
| 查看状态 | .agent-state.json

## 八、输出产物

outputs/
├── scene-breakdown-ep01.json
├── beat-breakdown-ep01.md
├── beat-board-prompt-ep01-board*.md (9个)
├── sequence-board-prompt-ep01.md
└── motion-prompt-ep01.md

---

最后更新：2026-02-03
