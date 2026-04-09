# Motion 工作流程

## 完整工作流程

```
步骤0: 调用子Agent（animator）
       ├── 读取 .agent-state.json，检查 animator 是否有 agentId
       ├── 如果有 agentId 且 status 不是 "error"：
       │   └── 使用 Resume 调用：Resume agent <agentId> and 生成动态提示词
       ├── 如果没有 agentId 或 status 是 "error"：
       │   └── 使用首次调用：Use animator agent to 生成动态提示词
       ├── 捕获返回的 agentId（从 JSON 元数据中）
       └── 更新 .agent-state.json：
           ├── 更新 animator.agentId
           ├── 更新 animator.last_task 为 "motion"
           ├── 更新 animator.last_used 为当前时间
           └── 更新 animator.status 为 "idle"

步骤1: 读取前置产物
       ├── outputs/sequence-board-prompt-{集数}-board*.md（四宫格提示词）
       ├── outputs/beat-board-prompt-{集数}.md（九宫格总览）
       ├── outputs/beat-breakdown-{集数}.md（节拍拆解）
       └── .agent-state.json

步骤2: 读取分析模块（按 animator-skill/SKILL.md 定义）
       ├── animator-skill/motion-prompt-methodology/index.md ← 动态提示词方法论
       ├── animator-skill/physics-verification-rules.md ← 物理验证规则
       ├── animator-skill/montage-engine/ ← 蒙太奇逻辑引擎（可选）
       └── animator-skill/templates/motion-prompt-template.md ← 输出格式模板

步骤3: 执行创意引擎调用 ← 【新增】
       ├── 调用蒙太奇逻辑引擎分析动作序列
       ├── 输入参数：
       │   ├── 四宫格序列（outputs/sequence-board-prompt.md）
       │   ├── 节拍情绪曲线（outputs/beat-breakdown.md）
       │   └── 视觉风格参考（outputs/beat-board-prompt.md）
       └── 输出：创意动作建议，包括：
           ├── 情绪匹配的运动类型
           ├── 节奏变化建议
           ├── 环境互动创意
           └── 风格化处理方案

步骤4: 执行五模块构造
       ├── 按 motion-prompt-methodology 规则构造：
       │   ├── 镜头运动模块（1-2种运动）
       │   ├── 主体动作模块（1-2种动作）
       │   ├── 环境动态模块（必须包含）
       │   ├── 节奏控制模块
       │   └── 氛围强化模块
       └── 每组包含5个 Motion Prompt（1关键帧 + 4四宫格）

步骤5: 执行物理合理性检查
       ├── 按 physics-verification-rules.md 逐项检查：
       │   ├── 重力影响检查
       │   ├── 惯性表现检查
       │   ├── 材质反应检查
       │   ├── 能量守恒检查
       │   └── 流体动力学检查（如适用）
       └── 标记物理异常项：✅ 合理 / ⚠️ 轻微异常 / ❌ 物理错误

步骤6: 占位格特殊处理
       ├── 识别九宫格中的占位格（PH-标记）
       ├── 对占位格生成"建议动态方案"
       └── 明确标注"待用户确认"

步骤7: 保存输出文件
       └── outputs/motion-prompt-{集数}.md

步骤8: 调用导演审核（storyboard-review-skill）
       ├── 读取 .agent-state.json，检查 director 是否有 agentId
       ├── 如果有 agentId 且 status 不是 "error"：
       │   └── 使用 Resume 调用：Resume agent <agentId> and 审核动态提示词
       ├── 如果没有 agentId 或 status 是 "error"：
       │   └── 使用首次调用：Use director agent to 审核动态提示词
       ├── 读取 storyboard-review-skill/review-checklist.md
       ├── 按 Motion Prompt 验收清单逐项检查
       ├── 生成审核报告：outputs/motion-prompt-{集数}-review.md
       ├── 捕获返回的 agentId（从 JSON 元数据中）
       └── 更新 .agent-state.json：
           ├── 更新 director.agentId
           ├── 更新 director.last_task 为 "motion-review"
           ├── 更新 director.last_used 为当前时间
           └── 更新 director.status 为 "idle"

步骤9: 执行用户确认（CP4）
       ├── 读取 common/user-confirmation-protocol.md
       ├── 展示标准确认UI：
       │   ├── 进度条
       │   ├── 质量评分
       │   ├── 审核状态
       │   └── 操作选项：[通过] ✅ / [修改] ✏️ / [重生成] 🔄 / [回滚] ⏪
       ├── 调用 question 工具
       ├── ⚠️ **立即停止执行**
       └── 等待用户显式指令（"继续"或"通过"）

步骤10: 用户显式确认后 - 创建快照（按 common/snapshot-management.md）
            ├── 快照类型：参数快照（CP4）
            ├── 保存路径：.strategic-snapshots/snapshot-{编号}/
            └── 更新 .agent-state.json：
                ├── 更新 phase 为 "completed"
                ├── 更新 current_episode 为当前集数
                └── 更新所有 subagent 的 last_used 时间戳

步骤11: 进入下一阶段或结束
           ├── [通过] → 可执行 /review motion 进入最终审核阶段
           ├── [修改] → 等待修改后重新审核
           ├── [重生成] → 返回步骤3重新执行
           └── [回滚] → 恢复到历史快照
 ```

## 模块依赖

| 模块 | 作用 | 是否必需 |
|------|------|----------|
| animator-skill/motion-prompt-methodology/index.md | 动态提示词方法论 | ✅ 必需 |
| animator-skill/montage-engine/ | 蒙太奇逻辑引擎 | ⚪ 可选 |
| animator-skill/physics-verification-rules.md | 物理验证规则 | ✅ 必需 |
| animator-skill/templates/motion-prompt-template.md | 输出格式模板 | ✅ 必需 |

## 协议文件

| 文件 | 作用 | 调用时机 |
|------|------|----------|
| common/user-confirmation-protocol.md | 用户确认UI规范 | 步骤9执行前 |
| common/snapshot-management.md | 快照创建规则 | 步骤10执行前 |

## contextFiles 定义 [V4.1-CRITICAL]

| 文件类型 | 文件路径 | 用途 | 必填 |
|----------|----------|------|------|
| Markdown | `outputs/sequence-board-prompt-{集数}-board*.md` | 四宫格提示词 | ✅ |
| Markdown | `outputs/beat-board-prompt-{集数}.md` | 九宫格总览 | ✅ |
| Markdown | `outputs/beat-breakdown-{集数}.md` | 节拍拆解 | ✅ |
| JSON | `outputs/scene-breakdown-{集数}.json` | 全量数据层 | ✅ [依赖] |
| JSON | `outputs/sequence-board-data-{集数}.json` | 四宫格数据 | ✅ [依赖] |
| JSON | `outputs/motion-prompt-data-{集数}.json` | 动态提示词数据 | ✅ [生成] |
| 状态 | `.agent-state.json` | 项目配置 | ✅ |

**JSON 生成规则**：
- `/motion` 执行后必须生成 `motion-prompt-data-{集数}.json`
- JSON 包含：boards数组、motion_groups（每组5个）、physics_verification
- 必须读取上游的 `sequence-board-data-{集数}.json`

**依赖检查**：
- ⚠️ sequence-board-data-{集数}.json 缺失 → 立即停止，要求重新执行 /sequence
- ⚠️ motion-prompt-data-{集数}.json 生成失败 → 立即停止

## 相关文件
- 模板：`animator-skill/templates/motion-prompt-template.md`
- 方法论：`animator-skill/motion-prompt-methodology/index.md`
- 蒙太奇引擎：`animator-skill/montage-engine/`
- 物理验证：`animator-skill/physics-verification-rules.md`
- 审核：`storyboard-review-skill/`（使用 review-checklist.md）
- 协议：`common/user-confirmation-protocol.md`、`common/snapshot-management.md`
