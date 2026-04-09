# SKILL 模块化架构详细说明

[SKILL 主文件设计原则]

每个 SKILL 的主配置文件只包含：
- 技能说明
- 自动加载的模块列表
- 核心流程概述
- 输出文件规范
- 参考文件指引

[核心 SKILL]

| SKILL | 路径 | 功能 |
|-------|------|------|
| film-storyboard-skill | film-storyboard-skill/SKILL.md | 分镜生成（节拍/九宫格/四宫格） |
| storyboard-review-skill | storyboard-review-skill/storyboard-review-skill.md | 审核流程 |
| animator-skill | animator-skill/SKILL.md | 动态提示词生成 |

[film-storyboard-skill 自动加载模块]

- 节拍分析：读取 common/beat-analyzer.md
- 关键帧选择：读取 common/keyframe-selector.md
- 布局计算：读取 common/layout-calculator.md
- 连贯性检查：读取 common/coherence-checker.md
- 导演决策：读取 common/director-decision.md
- 文件规范：读取 common/file-specs.md
- 质量检查：读取 common/quality-check.md
- 异常处理：读取 common/exception-handler.md

[storyboard-review-skill 自动加载模块]

- 质量检查：读取 common/quality-check.md
- 文件规范：读取 common/file-specs.md
- 异常处理：读取 common/exception-handler.md

[animator-skill 自动加载模块]

- 文件规范：读取 common/file-specs.md
- 质量检查：读取 common/quality-check.md
- 异常处理：读取 common/exception-handler.md

[common/ 公共模块]

| 模块 | 功能 | 被哪些 SKILL 调用 |
|------|------|-------------------|
| beat-analyzer.md | 节拍分析 | film-storyboard-skill |
| keyframe-selector.md | 关键帧选择 | film-storyboard-skill |
| layout-calculator.md | 布局计算 | film-storyboard-skill |
| coherence-checker.md | 连贯性检查 | film-storyboard-skill |
| director-decision.md | 导演决策 | film-storyboard-skill |
| file-specs.md | 文件规范 | 所有 SKILL |
| quality-check.md | 质量检查 | storyboard-review-skill |
| exception-handler.md | 异常处理 | 所有 SKILL |

[SKILL 调用流程]

```
1. 子 Agent 读取 SKILL.md
2. SKILL.md 定义自动加载规则
3. SKILL 按流程调用 common/ 模块
4. common/ 模块执行具体逻辑
5. SKILL 汇总结果并输出
```

[模块设计原则]

1. **单一职责**：每个模块只做一件事
2. **可复用**：模块可被多个 SKILL 调用
3. **独立性强**：模块间依赖最小化
4. **体积小**：每个模块 < 100行，可完整读取

[相关协议文件]

| 文件 | 说明 | 被谁引用 |
|------|------|----------|
| `common/user-confirmation-protocol.md` | 用户确认协议 | AGENTS.md, 子 Agent |
| `common/snapshot-management.md` | 快照管理规则 | AGENTS.md, 子 Agent |
| `.opencode/command/interactive.md` | 配置向导 | AGENTS.md, 子 Agent |
