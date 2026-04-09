---
description: 审核产出。对节拍拆解表、九宫格提示词、四宫格提示词、动态提示词进行质量审核。完整支持基准文件、用户确认和快照管理。
---

# 审核

**目的**：对各阶段产出进行质量审核，确保符合项目标准

**前置条件**：
- 已有需要审核的产出文件（节拍拆解表/九宫格/四宫格/动态提示词）

**使用方式**：
```bash
/review breakdown    # 审核节拍拆解表
/review beatboard    # 审核九宫格提示词
/review sequence     # 审核四宫格提示词
/review motion       # 审核动态提示词
/review all          # 审核所有产出
/review beatboard ep01    # 指定集数
/review beatboard ep01 03 # 指定集数和板号
```

**审核类型**：
| 类型 | 审核内容 | 审核者 |
|------|----------|--------|
| `breakdown` | 节拍拆解表 | director |
| `beatboard` | 九宫格提示词 | director |
| `sequence` | 四宫格提示词 | director |
| `motion` | 动态提示词 | director |
| `all` | 所有产出 | director |

**审核维度**：
1. **结构完整性**：检查格式、必填字段、编号连续性
2. **内容质量**：检查描述清晰度、逻辑连贯性、专业术语使用
3. **风格一致性**：检查与视觉风格、目标媒介的匹配度
4. **技术规范**：检查提示词格式、参数设置、关键词使用
5. **资产一致性**：检查角色外观、服装状态、场景要素一致性（新增）
6. **关键帧合理性**：检查剧情匹配度、构图有效性、氛围传达（新增）
7. **创意融合度**：检查引擎输出融合、用户创意执行（新增）

**详细工作流程**：
详见：[.claude/workflows/review-workflow.md](../.claude/workflows/review-workflow.md)

**相关SKILL**：
- storyboard-review-skill/SKILL.md
