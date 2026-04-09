---
description: 执行节拍拆解阶段。从剧本中识别叙事曲线的关键拐点，生成节拍拆解表。完整支持模块依赖、导演审核、用户确认和快照管理。
---

# 节拍拆解

**目的**：从剧本中识别叙事曲线的关键拐点，生成节拍拆解表

**前置条件**：
- 剧本文件已放入 `script/` 目录
- 文件名格式：`ep{##}-描述.md` 或 `单集`

**使用方式**：
```bash
/breakdown          # 单集时使用
/breakdown ep01     # 指定集数
/breakdown ch01     # 指定章节
```

**输出文件**：
- `outputs/beat-breakdown-{集数}.md`

**详细工作流程**：
详见：[.claude/workflows/breakdown-workflow.md](../.claude/workflows/breakdown-workflow.md)

**相关SKILL**：
- film-storyboard-skill/SKILL.md
