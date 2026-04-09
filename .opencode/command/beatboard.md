---
description: 执行九宫格提示词阶段。基于节拍拆解表生成 Beat Board 多宫格提示词。完整支持模块依赖、导演审核、用户确认和快照管理。
---

# 九宫格提示词

**目的**：基于节拍拆解表生成 Beat Board 九宫格提示词

**前置条件**：
- 节拍拆解表已完成：`outputs/beat-breakdown-{集数}.md`

**使用方式**：
```bash
/beatboard          # 单集时使用
/beatboard ep01     # 指定集数
/beatboard 01       # 生成指定板
```

**输出文件**：
- `outputs/beat-board-prompt-{集数}.md`（总览）
- `outputs/beat-board-prompt-{集数}-board{##}.md`（每个板一个文件）

**分板逻辑**：
- 每板固定9格（3×3网格）
- 关键帧数量 > 9 时自动分板
- 最后一板不足9格用占位格填充

**详细工作流程**：
详见：[.claude/workflows/beatboard-workflow.md](../.claude/workflows/beatboard-workflow.md)

**相关SKILL**：
- film-storyboard-skill/SKILL.md
