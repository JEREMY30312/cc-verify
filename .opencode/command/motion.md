---
description: 执行动态提示词阶段。基于四宫格提示词生成 Motion Prompt 动态提示词。完整支持模块依赖、导演审核、用户确认和快照管理。
---

# 动态提示词

**目的**：基于四宫格提示词生成 Motion Prompt 动态提示词

**前置条件**：
- 所有前置阶段已完成：
  - `outputs/beat-breakdown-{集数}.md`
  - `outputs/beat-board-prompt-{集数}-board*.md`
  - `outputs/sequence-board-prompt-{集数}.md`

**使用方式**：
```bash
/motion             # 单集时使用
/motion ep01        # 指定集数
```

**输出文件**：
- `outputs/motion-prompt-{集数}.md`

**内容结构**：
- 动态参数总览（帧率、运动速度、节奏特点）
- 核心角色动态设定
- 分段动态提示词（6幕结构）
- 关键动作拆解表
- 节奏曲线
- 音效与配乐建议

**详细工作流程**：
详见：[.claude/workflows/motion-workflow.md](../.claude/workflows/motion-workflow.md)

**相关SKILL**：
- animator-skill/SKILL.md
