# Beatboard 工作流程

## 完整工作流程

```
步骤0: 调用子Agent（storyboard-artist）
       ├── 读取 .agent-state.json，检查 storyboard-artist 是否有 agentId
       ├── 如果有 agentId 且 status 不是 "error"：
       │   └── 使用 Resume 调用：Resume agent <agentId> and 生成九宫格提示词
       ├── 如果没有 agentId 或 status 是 "error"：
       │   └── 使用首次调用：Use storyboard-artist agent to 生成九宫格提示词
       ├── 捕获返回的 agentId（从 JSON 元数据中）
       └── 更新 .agent-state.json：
           ├── 更新 storyboard-artist.agentId
           ├── 更新 storyboard-artist.last_task 为 "beatboard"
           ├── 更新 storyboard-artist.last_used 为当前时间
           └── 更新 storyboard-artist.status 为 "idle"

步骤1: 读取前置产物
       ├── outputs/beat-breakdown-{集数}.md（节拍拆解表）
       └── .agent-state.json

步骤2: 读取关键帧选择模块
       ├── common/keyframe-selector.md ← 关键帧选择逻辑
       └── 提取每个节拍的"关键信息点"字段（JSON 格式）
           ├── 提取每个节拍的"辅助信息"字段（如有）
           └── 提取附录: 创意引擎分析部分

步骤3: 执行关键帧选择
       ├── 按 keyframe-selector.md 规则执行：
       ├── 根据节拍权重和关键帧等级选择核心画面
       ├── 从引擎输出中提取戏剧权重和置信度
       ├── 每个板选择9个格子覆盖节拍范围
       ├── 动态扩展：每检测到1个氛围转折点 → 增加1个关键帧
       └── 动作强化：重大动作节拍可拆分为2-3个关键帧

步骤4: 读取环境构造模块 ← 【V3.0新增】
       ├── film-storyboard-skill/environment-construction-guide/
       │   ├── 空间骨架构建
       │   ├── 四层结构（前景/中景/背景/天空）
       │   ├── 材质定义
       │   ├── 光影基调
       │   └── 动态元素
       └── 提取环境资产包（如存在）

步骤5: 执行环境构造 ← 【V3.0新增】
       ├── 为每个格子调用 environment-construction-guide：
       │   ├── 空间骨架：基础布局、关键物体位置、角色活动范围
       │   ├── 四层结构：前景层、中景层、背景层、天空层
       │   ├── 材质：表面特征、纹理细节
       │   ├── 光影基调：光源类型、色彩氛围
       │   └── 动态元素：需要动态效果的对象
       └── 生成：每个格子的环境构造描述

步骤6: 读取布局计算模块
       ├── common/layout-calculator.md ← 布局计算逻辑
       └── 计算每板关键帧数量、分板数、布局类型

步骤7: 读取九宫格模板
       ├── film-storyboard-skill/templates/beat-board-template.md ← 输出格式模板
       └── 准备按模板格式生成提示词

步骤8: 生成九宫格提示词 ← 【增强】
       ├── 按 beat-board-template.md 格式生成
       ├── 每板9个格子的详细提示词
       ├── 继承节拍拆解的视觉风格和角色设定
       ├── 整合环境构造结果
       ├── 继承引擎输出摘要和置信度
       └── 【第三阶段新增】强制执行五维扩写：
           ├── 读取 common/visual-thickening-optimizer.md
           ├── 强制执行五维扩写：
           │   1. 主体维度：姿态、表情、服装纹理
           │   2. 环境维度：从环境资产包提取关键元素
           │   3. 光影维度：光的方向、质感、色彩影响
           │   4. 动态维度：加入1-2个合理动态元素（衣摆动、尘埃等）
            │   └── 5. 镜头维度：根据策略指定具体镜头语言
            └── 每个维度至少增加1个具体细节描述

步骤8.5: 执行V4.1-CRITICAL单帧原则统一检查 ← 【V4.1-CRITICAL强制执行】
        ├── 验证项：
        │   ├── [ ] 每个格子只包含一个画面描述（禁用一格多画面）
        │   ├── [ ] 画面描述中没有"[主格-xxx]+[副格-xxx]"格式
        │   ├── [ ] 画面描述中没有"→"或"-"连接多个场景
        │   ├── [ ] 画面描述包含明确标签 **[关键帧]** ✅
        │   ├── [ ] 每个格子都有 **风格标签**（简洁关键词列表）
        │   └── [ ] 格子数量 = 9（或根据节拍数调整）
        ├── 【新增】单帧原则强制检查：
        │   ├── 禁止连续动作序列：
        │   │   ├── ❌ 错误示例：
        │   │   │   ├── "包子猪被拉走，重重按在案板"
        │   │   │   ├── "惊恐→系餐巾→期待敲盘"
        │   │   │   ├── "暴怒→气劲涌动→包子诞生"
        │   │   │   ├── "鲁达冲出→滑铲→接球"
        │   │   │   └── "镇关西暴怒→周身爆气→包子悬浮"
        │   │   ├── ✅ 正确示例（单帧）：
        │   │   │   ├── "包子猪被按在案板中央，表情惊讶"
        │   │   │   ├── "包子猪系好餐巾后，期待敲盘"
        │   │   │   ├── "暗物质包子诞生：悬浮红色闪电"
        │   │   │   └── "鲁达滑铲姿势清晰"
        │   │   └── 检测方法：识别多个动作动词+时间序列词
        │   ├── 禁止时间序列词汇：
        │   │   ├── ❌ 禁用词：
        │   │   │   ├── "然后"、"接着"、"随后"、"接下来"、"同时"、"与此同时"
        │   │   │   ├── "第一"、"第二"、"首先"、"最后"
        │   │   │   ├── "一边...一边...""一方面...另一方面..."
        │   │   │   ├── "后"、"之后"、"接着便"、"随后便"
        │   │   │   └── "...之后"、"...接着"
        │   │   └── 允许使用：
        │   │       ├── 单帧描述："包子猪系好餐巾后，期待敲盘"（"后"表示完成而非时间序列）
        │   │       ├── 静态描述："鲁达站在案板前"（无动作进展）
        │   │       └── 表情描述："包子猪眼神期待"（静态表情）
        │   ├── 强制单帧画面：
        │   │   ├── ✅ 聚焦：静态姿态 + 表情 + 眼神
        │   │   ├── ✅ 格式：[动作主体] + [静态姿态] + [表情/眼神]
        │   │   └── ❌ 禁用：动作进展描述（"拉走"、"冲出"、"滑铲"、"扑向"）
        │   ├── 蒙太奇过程处理：
        │   │   ├── ❌ 九宫格禁用蒙太奇（属于四宫格工作）
        │   │   ├── ❌ 错误示例："惊恐→系餐巾→期待"（四宫格）
        │   │   └── ✅ 九宫格只选最强帧："期待眼神敲盘"
        │   └── 识别违规格子：
        │       ├── 扫描画面描述中的违禁词（"然后"、"接着"、"随后"、"→"、"→"、"冲"、"拉"、"滑"）
        │       ├── 检测连续动作（识别多个动词+方向词）
        │       ├── 检测蒙太奇标识（"→"、"序列"、"第一阶段"）
        │       └── 标记为待修复
        ├── 应用修复算法：
        │   ├── 对每个违规格子：
        │   │   └── 参考 V4.1修复案例（见 director-beatboard-fix-verify-*.md）：
        │   └── 案例1：去除连续动作：
        │       ├── 错误："包子猪被拉走，重重按在案板"
        │       ├── 修复："包子猪被抓住后，按在案板中央"
        │       └── 去除"拉走"动作，保留"按在案板"单帧
        │   └── 案例2：拆解蒙太奇：
        │       ├── 错误："惊恐→系餐巾→期待敲盘"（四宫格蒙太奇）
        │       ├── 修复："包子猪系好餐巾后，期待敲盘"
        │       └── 九宫格只保留最强帧"期待敲盘"
        ├── 验证修复后：
        │   ├── [ ] 所有格子的画面描述都是单一画面（连续动作数=0）
        │   ├── [ ] 没有违禁词（"然后"、"接着"、"随后"等）
        │   ├── [ ] 每个格子都有 **[关键帧]** ✅ 标签
        │   ├── [ ] 每个格子都有 **风格标签**
        │   ├── [ ] JSON.alternative_fields 已正确记录未选择帧
        │   └── [ ] JSON数据中 scene_description 只包含单帧
        └── 验证失败处理：
            ├── 如仍有违规格子 → 立即报错，不保存文件
            ├── 错误信息："九宫格违反V4.1-CRITICAL单帧原则，请修复"
            ├── 输出详细的违规列表（格子编号、错误类型、示例）
            └── 要求：人工检查或重新生成

步骤9: 执行提示词精简 ← 【V5.0强制执行】
       ├── 读取 common/prompt-simplifier.md
       ├── 对每个格子的"画面描述"字段执行精简算法
       ├── 执行四轮渐进式精简流程：
       │   ├── 轮1：移除P4元素（100%删除）
       │   │   ["然后", "接着", "随后", "接下来", "与此同时", "另一方面"]
       │   ├── 轮2：移除P3元素（80%删除）
       │   │   ["非常", "极其", "特别", "显得", "十分", "呈现", "展示", "体现"]
       │   ├── 轮3：词语级保护+激进精简
       │   │   • P1元素100%保护：电影技术术语、镜头参数、光影术语
       │   │   • P2元素≥90%保护：视觉隐喻、情感细节、环境质感
       │   └── 轮4：质量检查和最终清理
       ├── 验证质量指标：
       │   ├── P1元素保留率 = 100%
       │   ├── P2元素保留率 ≥ 90%
       │   ├── 精简率：15-20%
       │   └── 质量下降 ≤ 8%
       └── 记录精简元数据到输出文件

步骤10: 执行连贯性检查
       ├── 按 coherence-checker.md 逐项检查：
       │   ├── 角色外观一致性
       │   ├── 服装状态连续性
       │   ├── 光线/时间连续性
       │   └── 空间关系稳定性
       └── 不通过则修正后重新检查

步骤11: 保存输出文件
        ├── 总览文件：outputs/beat-board-prompt-{集数}.md
        └── 分板文件：outputs/beat-board-prompt-{集数}-board{##}.md

步骤12: 调用导演审核（storyboard-review-skill）
       ├── 读取 .agent-state.json，检查 director 是否有 agentId
       ├── 如果有 agentId 且 status 不是 "error"：
       │   └── 使用 Resume 调用：Resume agent <agentId> and 审核九宫格提示词
       ├── 如果没有 agentId 或 status 是 "error"：
       │   └── 使用首次调用：Use director agent to 审核九宫格提示词
       ├── 读取 storyboard-review-skill/review-checklist.md
       ├── 读取 storyboard-review-skill/asset-consistency-rules.md（如需要）
       ├── 按 Beat Board 验收清单逐项检查
       ├── 生成审核报告：outputs/beat-board-prompt-{集数}-review.md
       ├── 捕获返回的 agentId（从 JSON 元数据中）
       └── 更新 .agent-state.json：
           ├── 更新 director.agentId
           ├── 更新 director.last_task 为 "beatboard-review"
           ├── 更新 director.last_used 为当前时间
           └── 更新 director.status 为 "idle"

步骤13: 执行用户确认（CP2）
        ├── 读取 common/user-confirmation-protocol.md
        ├── 展示标准确认UI：
        │   ├── 进度条
        │   ├── 质量评分
        │   ├── 审核状态
        │   └── 操作选项：[通过] ✅ / [修改] ✏️ / [重生成] 🔄 / [回滚] ⏪
        ├── 调用 question 工具
        ├── ⚠️ **立即停止执行**
        └── 等待用户显式指令（"继续"或"通过"）

步骤14: 用户显式确认后 - 创建快照（按 common/snapshot-management.md）
            ├── 快照类型：分板快照（CP2）
            ├── 保存路径：.strategic-snapshots/snapshot-{编号}/
            └── 更新 .agent-state.json：
                ├── 更新 phase 为 "sequence"
                ├── 更新 current_episode 为当前集数
                └── 更新所有 subagent 的 last_used 时间戳

步骤15: 进入下一阶段或结束
           ├── [通过] → 可执行 /sequence 进入四宫格阶段
           ├── [修改] → 等待修改后重新审核
           ├── [重生成] → 返回步骤2重新执行
           └── [回滚] → 恢复到历史快照
 ```

## 模块依赖

| 模块 | 作用 | 是否必需 |
|------|------|----------|
| common/keyframe-selector.md | 关键帧选择逻辑 | ✅ 必需 |
| film-storyboard-skill/environment-construction-guide/ | 环境构造系统 | ✅ 必需 (V3.0) |
| common/layout-calculator.md | 布局计算逻辑 | ✅ 必需 |
| film-storyboard-skill/templates/beat-board-template.md | 输出格式模板 | ✅ 必需 |
| common/visual-thickening-optimizer.md | 视觉增强优化 | ✅ 必需 (阶段C) |
| common/prompt-simplifier.md | 提示词精简 | ✅ 必需 (阶段C) |
| common/coherence-checker.md | 连贯性检查 | ✅ 必需 |

## 协议文件

| 文件 | 作用 | 调用时机 |
|------|------|----------|
| common/user-confirmation-protocol.md | 用户确认UI规范 | 步骤13执行前 |
| common/snapshot-management.md | 快照创建规则 | 步骤14执行前 |

## contextFiles 定义 [V4.1-CRITICAL]

| 文件类型 | 文件路径 | 用途 | 必填 |
|----------|----------|------|------|
| Markdown | `outputs/beat-breakdown-{集数}.md` | 节拍拆解表 | ✅ |
| JSON | `outputs/scene-breakdown-{集数}.json` | 全量数据层 | ✅ [依赖] |
| JSON | `outputs/beat-board-full-list-{集数}.json` | 九宫格数据 | ✅ [生成] |
| 状态 | `.agent-state.json` | 项目配置 | ✅ |

**JSON 生成规则**：
- `/beatboard` 执行后必须生成 `beat-board-full-list-{集数}.json`
- JSON 包含：grids数组、waterfall_shots、quality_metrics
- 必须同时读取上游的 `scene-breakdown-{集数}.json`

**依赖检查**：
- ⚠️ scene-breakdown-{集数}.json 缺失 → 立即停止，要求重新执行 /breakdown
- ⚠️ beat-board-full-list-{集数}.json 生成失败 → 立即停止

## 相关文件
- 模板：`film-storyboard-skill/templates/beat-board-template.md`
- 关键帧选择：`common/keyframe-selector.md`
- 布局计算：`common/layout-calculator.md`
- 环境构造：`film-storyboard-skill/environment-construction-guide/`
- 连贯性检查：`common/coherence-checker.md`
- 审核：`storyboard-review-skill/`（使用 review-checklist.md）
- 协议：`common/user-confirmation-protocol.md`、`common/snapshot-management.md`
