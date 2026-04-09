# 节拍拆解调用示例

## OpenCode task 命令调用

### 基本调用

```bash
task(
  subagent_type="general",
  prompt="""执行节拍拆解任务。

项目配置：
- 视觉风格：国漫
- 目标媒介：漫剧
- 画幅比例：16:9
- 集数：ep01

执行前必须读取以下文件：
1. common/beat-analyzer.md ← 核心分析模块
2. film-storyboard-skill/templates/beat-breakdown-template.md ← 输出格式
3. common/quality-check.md ← 质量检查

剧本文件路径：script/猪打镇关西_v2.0

执行要求：
1. 读取并理解 beat-analyzer.md 的节拍分析规则
2. 读取 beat-breakdown-template.md 的格式要求
3. 从剧本中识别关键叙事节拍（8-12个为宜）
4. 应用三幕结构：15-25% / 50-70% / 15-25%
5. 每个节拍必须包含：场景描述、角色行动、情感表达
6. 计算综合权重和关键帧等级
7. 执行 quality-check.md 自检
8. 按模板格式输出节拍拆解表

输出文件：outputs/beat-breakdown-ep01.md
"""
)
```

### 完整参数调用

```bash
task(
  subagent_type="general",
  prompt="""执行节拍拆解任务。

## 步骤1：读取配置
读取 .agent-state.json，获取：
- visual_style: 国漫
- target_medium: 漫剧
- aspect_ratio: 16:9
- episode_id: ep01

## 步骤2：读取输入文件
读取：script/猪打镇关西_v2.0（剧本）
读取（可选）：common/director-decision.md（导演参数）

## 步骤3：读取分析模块
按顺序读取：
1. common/beat-analyzer.md ← 核心分析逻辑
2. film-storyboard-skill/templates/beat-breakdown-template.md ← 输出格式
3. common/quality-check.md ← 质量检查清单

## 步骤4：执行节拍分析
根据 beat-analyzer.md 规则：
- 三幕结构比例：15-25% / 50-70% / 15-25%
- 节拍数量：8-12个为宜
- 每个节拍必须包含：
  * 场景描述（发生了什么）
  * 角色行动（具体动作和意图）
  * 情感表达（核心情绪）
  * 叙事功能
  * 节拍类型
- 计算综合权重和关键帧等级

## 步骤5：质量自检
读取 quality-check.md，逐项检查：
□ 三幕比例符合标准
□ 节拍数量在 8-12 范围内
□ 叙事完整性（有开篇、发展、高潮、结局）
□ 每个节拍有明确的场景描述
□ 每个节拍有清晰的角色行动
□ 每个节拍有具体的情感表达

## 步骤6：输出
按 beat-breakdown-template.md 格式生成
保存到：outputs/beat-breakdown-ep01.md
"""
)
```

## 脚本封装调用

### Bash 脚本

```bash
#!/bin/bash

# 节拍拆解脚本
# 用法：./breakdown.sh ep01

EPISODE=$1

# 检查参数
if [ -z "$EPISODE" ]; then
    echo "用法：./breakdown.sh <集数>"
    exit 1
fi

# 读取配置
source .agent-state.json

# 执行节拍拆解
task(
  subagent_type="general",
  prompt="执行节拍拆解任务..."
)
```

## 流程验证检查表

执行后检查：

| 检查项 | 状态 |
|--------|------|
| 节拍数量在 8-12 范围内 | ☐ |
| 三幕结构完整（第一幕/第二幕/第三幕） | ☐ |
| 每个节拍包含场景描述 | ☐ |
| 每个节拍包含角色行动 | ☐ |
| 每个节拍包含情感表达 | ☐ |
| 关键帧等级分布合理 | ☐ |
| 通过 quality-check.md 自检 | ☐ |
