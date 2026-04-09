# Review 工作流程

## 审核类型与输入

| 审核类型 | 待审核文件 | 必须读取的上游产物 |
|----------|------------|-------------------|
| breakdown-review | beat-breakdown-{集数}.md | script/*-{集数}.md |
| beatboard-review | beat-board-prompt-{集数}.md | beat-breakdown-{集数}.md, script/*-{集数}.md |
| sequence-review | sequence-board-prompt-{集数}.md | beat-board-prompt-{集数}.md, beat-breakdown-{集数}.md |
| motion-review | motion-prompt-{集数}.md | sequence-board-prompt-{集数}.md, beat-board-prompt-{集数}.md, beat-breakdown-{集数}.md |

## 审核维度

1. **结构完整性**：检查格式、必填字段、编号连续性
2. **内容质量**：检查描述清晰度、逻辑连贯性、专业术语使用
3. **风格一致性**：检查与视觉风格、目标媒介的匹配度
4. **技术规范**：检查提示词格式、参数设置、关键词使用
5. **资产一致性**：检查角色外观、服装状态、场景要素一致性（新增）
6. **关键帧合理性**：检查剧情匹配度、构图有效性、氛围传达（新增）
7. **创意融合度**：检查引擎输出融合、用户创意执行（新增）

## 完整工作流程

```
步骤1: 收集基本信息
       ├── 审核类型（breakdown/beatboard/sequence/motion/all）
       ├── 集数标识
       └── 板号（如适用）

步骤2: 读取基准文件（按 storyboard-review-skill/SKILL.md 定义）
       ├── storyboard-review-skill/review-checklist.md ← 验收清单
       ├── storyboard-review-skill/uncertainty-judgment-protocol.md ← 不确定项判定
       ├── storyboard-review-skill/asset-consistency-rules.md ← 资产一致性（如适用）
       └── storyboard-methodology-playbook/index.md ← 分镜方法论（如适用）

步骤3: 建立整体理解
       ├── 读取剧本原文（如需要）
       ├── 读取节拍拆解表（如存在）
       ├── 读取九宫格提示词（如存在）
       ├── 读取四宫格提示词（如存在）
       └── 读取动态提示词（如存在）

步骤4: 读取待审核内容
       ├── breakdown: outputs/beat-breakdown-{集数}.md
       ├── beatboard: outputs/beat-board-prompt-{集数}.md + 分板
       ├── sequence: outputs/sequence-board-prompt-{集数}.md
       ├── motion: outputs/motion-prompt-{集数}.md
       └── all: 所有上述文件

步骤5: 执行逐项检查
       ├── 按 review-checklist.md 验收清单逐项检查
       ├── 执行资产一致性审核（如适用）
       ├── 执行关键帧合理性审核
       └── 执行创意融合度审核

步骤6: 执行不确定项判定
       ├── 按 uncertainty-judgment-protocol.md 判定
       ├── 识别潜在不确定项
       ├── 生成决策选项（保持创意/按规则修改/生成替代方案）
       └── 推荐选项及理由

步骤7: 生成审核报告
       ├── 保存到：outputs/{产物类型}-{集数}-review.md
       ├── 审核结论：✅ PASS / ⚠️ UNCERTAIN / ❌ FAIL
       └── 附上修改建议（如果不通过）

步骤8: 执行用户确认
       ├── 读取 common/user-confirmation-protocol.md
       ├── 展示标准确认UI：
       │   ├── 审核类型和状态
       │   ├── 审核报告摘要
       │   ├── 问题列表（如有）
       │   └── 操作选项：[确认审核结果] / [要求修改] / [重审]
       └── 等待用户选择

步骤9: 创建快照（按 common/snapshot-management.md）
          ├── 快照类型：对应阶段的快照类型
          ├── 保存路径：.strategic-snapshots/snapshot-{编号}/
          └── 更新 .agent-state.json：
              ├── 更新 director.last_used 为当前时间
              └── 更新 director.status 为 "idle"

步骤10: 后续处理
          ├── [确认审核结果] → 记录决策，继续流程
          ├── [要求修改] → 标记产出为"待修改"
          └── [重审] → 返回步骤3重新审核
```

## 模块依赖

| 模块 | 作用 | 是否必需 |
|------|------|----------|
| storyboard-review-skill/review-checklist.md | 验收清单 | ✅ 必需 |
| storyboard-review-skill/uncertainty-judgment-protocol.md | 不确定项判定 | ✅ 必需 |
| storyboard-review-skill/asset-consistency-rules.md | 资产一致性规则 | ⚪ 按需 |
| storyboard-methodology-playbook/index.md | 分镜方法论 | ⚪ 按需 |
| motion-prompt-methodology/index.md | 动态提示词方法论 | ⚪ 仅 motion 审核 |

## 协议文件

| 文件 | 作用 | 调用时机 |
|------|------|----------|
| common/user-confirmation-protocol.md | 用户确认UI规范 | 步骤8执行前 |
| common/snapshot-management.md | 快照创建规则 | 步骤9执行前 |

## 审核结果定义

- **PASS**：全部验收项通过，无需修改
- **FAIL**：存在必须修改的问题，需要修改后重新提交审核
- **UNCERTAIN**：存在不确定项，需要用户决策

## 相关文件

- 审核清单：`storyboard-review-skill/review-checklist.md`
- 审核流程：`storyboard-review-skill/storyboard-review-skill.md`
- 决策记录：`common/director-decision.md`
- 协议：`common/user-confirmation-protocol.md`、`common/snapshot-management.md`
