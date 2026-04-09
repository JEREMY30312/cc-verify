---
description: 执行四宫格提示词阶段。基于九宫格提示词生成 Sequence Board 四宫格提示词。完整支持模块依赖、导演审核、用户确认和快照管理。
---

# 四宫格提示词

**目的**：基于九宫格提示词生成 Sequence Board 四宫格提示词

**前置条件**：
- 九宫格提示词已完成：`outputs/beat-board-prompt-{集数}-board*.md`

**使用方式**：
```bash
/sequence           # 单集时使用
/sequence ep01      # 指定集数
```

**输出文件**：
- `outputs/sequence-board-prompt-{集数}.md`

**结构说明**：
- 将所有节拍组织为多个四宫格组（每组4个镜头）
- 每组有明确的叙事功能和情绪定位
- 包含风格转换说明和人物一致性参考

**详细工作流程**：
详见：[.claude/workflows/sequence-workflow.md](../.claude/workflows/sequence-workflow.md)

**相关SKILL**：
- film-storyboard-skill/SKILL.md
