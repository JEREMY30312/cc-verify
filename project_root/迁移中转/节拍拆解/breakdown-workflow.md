# Breakdown 工作流程

## 完整工作流程

```
步骤0: 调用子Agent（storyboard-artist）
       ├── 读取 .agent-state.json，检查 storyboard-artist 是否有 agentId
       ├── 如果有 agentId 且 status 不是 "error"：
       │   └── 使用 Resume 调用：Resume agent <agentId> and 执行节拍拆解
       ├── 如果没有 agentId 或 status 是 "error"：
       │   └── 使用首次调用：Use storyboard-artist agent to 执行节拍拆解
       ├── 捕获返回的 agentId（从 JSON 元数据中）
       └── 更新 .agent-state.json：
           ├── 更新 storyboard-artist.agentId
           ├── 更新 storyboard-artist.last_task 为 "breakdown"
           ├── 更新 storyboard-artist.last_used 为当前时间
           └── 更新 storyboard-artist.status 为 "idle"

步骤1: 读取项目配置
       ├── .agent-state.json → visual_style, target_medium, aspect_ratio
       ├── 【V3.0新增】读取 narrative_structure, genre, enable_* 配置
       └── episode_id

 步骤2: 读取输入文件
        ├── script/*-{集数}.md（剧本文件）
        └── .claude/common/director-decision.md（如存在，导演参数）

步骤3: 提取角色设定 ← 【方案D新增】
       ├── 执行：`python3 configs/character-loader.py "script/{集数}.md" "/tmp/visual-style-specs-{集数}.json"`
       ├── 输出：/tmp/visual-style-specs-{集数}.json（临时文件）
       ├── 包含：角色的所有风格设定
       ├── 触发条件：剧本文件存在且包含YAML角色设定
       └── 降级处理：如果提取失败，继续执行但标记警告

步骤3.5: 生成按需加载的角色设定 ← 【方案D新增】
       ├── 读取：/tmp/visual-style-specs-{集数}.json
       ├── 调用：export_optimized_character_settings()
       ├── 算法：根据style_transitions确定需要嵌入的风格
       └── 输出示例：
           ├── 无风格转换：只嵌入第一个风格
           ├── 1次转换：嵌入2个风格
           └── 2次转换：嵌入所有风格

 步骤4: 读取分析模块（按 film-storyboard-skill/SKILL.md 定义）
        ├── .claude/common/beat-analyzer.md ← 【核心模块】节拍分析逻辑
        ├── film-storyboard-skill/templates/beat-breakdown-template.md ← 输出格式模板
        ├── .claude/common/quality-check.md ← 质量检查清单
        ├── .claude/common/director-decision.md（如存在）
        ├── 【V3.0新增】.claude/common/structure-profiles.md ← 结构模板选择
        ├── 【V3.0新增】.claude/common/subtext-analyzer.md ← 潜台词分析
        └── film-storyboard-skill/creative-engines-integration/ ← 创意引擎系统

步骤4: 执行节拍分析
       ├── 【V3.0更新】根据 narrative_structure 选择结构模板：
       │   ├── classic_three_act: 经典三幕式，动态确定（建议范围：8-12 个）
       │   ├── hero_journey: 英雄之旅，动态确定（建议范围：10-14 个）
       │   ├── kishotenketsu: 起承转合，动态确定（建议范围：3-5 个）
       │   └── micro_drama_loop: 多巴胺闭环，动态确定（建议范围：4-6 个）
       ├── 【V3.0更新】使用类型化戏剧权重计算算法（考虑 genre 修正）：
       │   ├── 事件类型权重映射（生死攸关、核心转折等）
       │   ├── 类型修正系数（动作片×1.5、爱情片×0.8 等）
       └── 最终权重计算：(表现权重 × 基重) × 类型系数 × 复杂度系数
       ├── 【V3.0新增】执行潜台词分析，挖掘角色心理动机：
       │   ├── 探测层：识别表面动作和关键词
       │   ├── 翻译层：映射到心理动机和潜台词
       │   └── 表现层：生成视觉对应物和拍摄建议
       ├── 节拍数量：根据剧本实际长度动态确定
       ├── **计算依据**：
       │   ├── 1. 剧本总行数：235 行
       │   ├── 2. 风格转换次数：2 次（国潮→MCU、MCU→像素）
       │   ├── 3. 场景密度：中高（多个场景、动作密集）
         ├── 4. 内容复杂度：高（战斗、风格转换、特效描述丰富）
       │   ├── **动态计算公式**：
       │   ├── 基础节拍数 = max(8, min(12, ceil(行数 / 20))) = max(8, min(12, 12)) = 12 个
       │   ├── **风格转换加成**：每次风格转换增加 1 个关键帧
       │   ├── **场景密度调整**：每 5-7 个行定义一个场景
       │   ├── **最终节拍数 = 基础节拍数 + 风格转换加成（1+1）+ 场景密度调整（3）= 16 个节拍
       │   ├── **约束条件**：最小 8 个，最大 18 个，或按实际内容调整
       ├── 每个节拍必须包含：场景描述、角色行动、情感表达
       └── 计算综合权重和关键帧等级

步骤5: 执行创意引擎分析 ← 【V3.0新增】
       ├── 调用 creative-engines-integration/ 模块：
       │   ├── 蒙太奇逻辑引擎：分析戏剧权重、镜头拆解建议、三段式拆解
       │   ├── 影视联想引擎：检索匹配影片、提取视觉DNA
       │   └── 通感视觉化引擎：识别感官刺激、转化视觉符号
       ├── 输出：引擎分析报告（含置信度评分）
       └── 记录：每个节拍的戏剧权重、镜头方案、置信度

 步骤6: 执行质量自检（按 .claude/common/quality-check.md）
       ├── □ 三幕比例符合标准
       ├── □ 节拍数量在 8-12 范围内
       ├── □ 叙事完整性（有开篇、发展、高潮、结局）
       ├── □ 每个节拍有明确的场景描述
       ├── □ 每个节拍有清晰的角色行动
       └── □ 每个节拍有具体的情感表达

步骤7: 保存输出文件
       └── outputs/beat-breakdown-{集数}.md
            ├── 包含：节拍拆解表
            └── 包含：附录: 创意引擎分析

步骤8: 调用导演审核（storyboard-review-skill）
       ├── 读取 .agent-state.json，检查 director 是否有 agentId
       ├── 如果有 agentId 且 status 不是 "error"：
       │   └── 使用 Resume 调用：Resume agent <agentId> and 审核节拍拆解
       ├── 如果没有 agentId 或 status 是 "error"：
       │   └── 使用首次调用：Use director agent to 审核节拍拆解
       ├── 读取 storyboard-review-skill/review-checklist.md
       ├── 读取 storyboard-review-skill/uncertainty-judgment-protocol.md（如需要）
       ├── 按验收清单逐项检查
       ├── 生成审核报告：outputs/beat-breakdown-{集数}-review.md
       ├── 捕获返回的 agentId（从 JSON 元数据中）
       └── 更新 .agent-state.json：
           ├── 更新 director.agentId
           ├── 更新 director.last_task 为 "breakdown-review"
           ├── 更新 director.last_used 为当前时间
           └── 更新 director.status 为 "idle"

 步骤9: 执行用户确认（CP1）
        ├── 读取 .claude/common/user-confirmation-protocol.md
        ├── 展示标准确认UI：
       │   ├── 进度条
       │   ├── 质量评分
       │   ├── 审核状态
       │   └── 操作选项：[通过] ✅ / [修改] ✏️ / [重生成] 🔄 / [回滚] ⏪
       ├── 调用 question 工具
       ├── ⚠️ **立即停止执行**
       └── 等待用户显式指令（"继续"或"通过"）

 步骤10: 用户显式确认后 - 创建快照（按 .claude/common/snapshot-management.md）
         ├── 快照类型：完整快照（CP1）
         ├── 保存路径：.strategic-snapshots/snapshot-{编号}/
         └── 更新 .agent-state.json：
             ├── 更新 phase 为 "beatboard"
             ├── 更新 current_episode 为当前集数
             └── 更新所有 subagent 的 last_used 时间戳

步骤11: 进入下一阶段或结束
         ├── [通过] → 可执行 /beatboard 进入九宫格阶段
         ├── [修改] → 等待修改后重新审核
         ├── [重生成] → 返回步骤3重新执行
         └── [回滚] → 恢复到历史快照
 ```

## 模块依赖

 | 模块 | 作用 | 是否必需 |
 |------|------|----------|
 | .claude/common/beat-analyzer.md | 节拍分析逻辑 | ✅ 必需 |
 | .claude/common/structure-profiles.md | 结构模板选择 | ✅ 必需 (V3.0) |
 | .claude/common/subtext-analyzer.md | 潜台词分析 | ✅ 必需 (V3.0) |
| film-storyboard-skill/templates/beat-breakdown-template.md | 输出格式模板 | ✅ 必需 |
 | film-storyboard-skill/creative-engines-integration/ | 创意引擎系统 | ✅ 必需 (V3.0) |
 | .claude/common/quality-check.md | 质量检查清单 | ✅ 必需 |
 | .claude/common/director-decision.md | 导演决策参数 | ⚪ 可选 |

## 协议文件

 | 文件 | 作用 | 调用时机 |
 |------|------|----------|
 | .claude/common/user-confirmation-protocol.md | 用户确认UI规范 | 步骤9执行前 |
 | .claude/common/snapshot-management.md | 快照创建规则 | 步骤10执行前 |

## contextFiles 定义 [V4.1-CRITICAL]

| 文件类型 | 文件路径 | 用途 | 必填 |
|----------|----------|------|------|
| 剧本 | `script/*-{集数}.md` | 输入素材 | ✅ |
| JSON | `outputs/scene-breakdown-{集数}.json` | 全量数据层 | ✅ [生成] |
| 状态 | `.agent-state.json` | 项目配置 | ✅ |

**JSON 生成规则**：
- `/breakdown` 执行后必须生成 `scene-breakdown-{集数}.json`
- JSON 包含：shots数组、sub_shots数组、NDI数据、镜头类型、动机、轴线、接力点
- 生成后立即验证字段完整性

**错误处理**：
- ⚠️ JSON 缺失或字段不完整 → 立即停止，要求重新执行 /breakdown

## 相关文件
 - 模板：`film-storyboard-skill/templates/beat-breakdown-template.md`
 - 分析模块：`.claude/common/beat-analyzer.md`、`.claude/common/structure-profiles.md`、`.claude/common/subtext-analyzer.md`
 - 创意引擎：`film-storyboard-skill/creative-engines-integration/`
 - 审核：`storyboard-review-skill/`（使用 review-checklist.md）
 - 协议：`.claude/common/user-confirmation-protocol.md`、`.claude/common/snapshot-management.md`
