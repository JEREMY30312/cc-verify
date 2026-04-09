# Sequence 工作流程

## 完整工作流程

```
步骤0: 调用子Agent（storyboard-artist）
       ├── 读取 .agent-state.json，检查 storyboard-artist 是否有 agentId
       ├── 如果有 agentId 且 status 不是 "error"：
       │   └── 使用 Resume 调用：Resume agent <agentId> and 生成四宫格提示词
       ├── 如果没有 agentId 或 status 是 "error"：
       │   └── 使用首次调用：Use storyboard-artist agent to 生成四宫格提示词
       ├── 捕获返回的 agentId（从 JSON 元数据中）
       └── 更新 .agent-state.json：
           ├── 更新 storyboard-artist.agentId
           ├── 更新 storyboard-artist.last_task 为 "sequence"
           ├── 更新 storyboard-artist.last_used 为当前时间
           └── 更新 storyboard-artist.status 为 "idle"

步骤1: 读取前置产物 ← 【V4.1更新】
       ├── outputs/beat-breakdown-{集数}.md
       │   └── 提取：核心策略、复杂度、建议格子数
       ├── 【V4.1新增】outputs/beat-board-full-list-{集数}.json
       │   └── 关键字段：grids[].alternative_frames（替代帧数据）
       │       用途：Sequence阶段读取并展开为多镜头
       │       详见：.claude/common/dynamic-breakdown-engine.md "JSON alternative_frames 读取逻辑"
       └── .agent-state.json

步骤2: 读取九宫格提示词和原文内容 ← 【V5.0更新】
       ├── outputs/beat-board-prompt-{集数}.md（总览）
       ├── outputs/beat-board-prompt-{集数}-board*.md（分板）
       │   └── 提取：每个格子的画面描述、环境构造、置信度、引擎输出摘要
       ├── outputs/beat-breakdown-{集数}.md（节拍拆解表）
       │   └── 【V5.0新增】提取：每个节拍的"原文内容"字段（包含完整对话、旁白、心理活动）
       └── 【V5.0新增】建立映射：九宫格格子 ↔ 节拍原文内容

步骤3: 读取导演审核报告
       ├── outputs/beat-board-prompt-{集数}-review.md
       └── 提取导演审核意见

步骤4: 调用动态分镜引擎 ← 【V4.0新增】
       ├── 读取 common/dynamic-breakdown-engine.md
       ├── 执行四阶段流程：
       │   ├── ① 策略映射：将核心策略标签映射到格子数分配
       │   │   ├── [单镜] → 1 格基础
       │   │   ├── [动势组] → 2 格基础
       │   │   ├── [蒙太奇组] → 3 格基础
       │   │   └── [长镜头] → 1-3 格基础
       │   ├── ② 粒度评估：基于复杂度评分确定格子密度
       │   │   └── 调整后格子数 = 基础格子数 + max(0, round(复杂度评分 - 2.5))
        │   ├── ③ 跨板协调：处理跨板节拍的连续性
        │   │   └── 优先保留节拍的完整叙事流
        │   ├── ④ 完整性校验：检查台词/动作/视觉的完整覆盖
        │   └── ⑤ 替代帧展开 ← 【V4.1新增】
        │       └── 详见：.claude/common/dynamic-breakdown-engine.md
        └── 输出：每个节拍的实际格子数（1-4 格）

步骤5: 读取动态分镜板模板 ← 【V4.0更新】
       ├── film-storyboard-skill/templates/sequence-board-template.md
       └── 使用协议1.0：四宫格裂变协议

步骤6: 生成继承记录
       ├── 为每个继承的格子记录：
       │   ├── 原导演审核意见
       │   ├── 环境构造继承（空间骨架、四层结构、材质、光影基调、动态元素）
       │   ├── 引擎输出摘要
       │   ├── 置信度
       │   ├── 低置信度标记（<60%）
       │   └── 【V4.0新增】策略标签（[单镜]/[动势组]/[蒙太奇组]/[长镜头]）
       └── 识别需要跨板展开的节拍

步骤7: 展开九宫格为四宫格并整合台词 ← 【V5.0重写】
        ├── 【V5.0核心】展开九宫格提示词：
        │   ├── 【V4.1新增】替代帧展开流程：
        │   │   - 输入：JSON alternative_frames + 策略标签
        │   │   - 处理：详见 .claude/common/dynamic-breakdown-engine.md
        │   │   - 输出：多镜头列表（1-4镜头）
        │   │   - 优势：可追溯、可调整、机器友好
        │   │   - 展开规律：替代帧数量 = 基础格子数 - 1
        │   │     示例：[动势组]（基础2格）→ 1个九宫格格 + 1个替代帧 → 2个镜头
        │   ├── 为每个九宫格格子生成1-4个镜头展开
        │   ├── 根据策略标签分配格子数和位置（左上/右上/左下/右下）
        │   ├── 完整保留九宫格原画面信息（放在对应四宫格前）
        │   └── 标注每个镜头的四宫格位置
       ├── 【V5.0新增】整合台词/旁白：
       │   ├── 从节拍拆解表的"原文内容"字段提取完整对话
       │   ├── 将台词自然融入画面描述段落（角色说"台词"，同时...）
       │   ├── 保留旁白信息（旁白："内容"，画面展示...）
       │   └── 保留心理活动（角色内心：想法描述）
       ├── 【V5.0新增】微调权限：
       │   ├── 允许根据文案调整镜头角度和运动方式
       │   ├── 允许调整光影效果（光源方向、强度、色彩）
       │   ├── 允许调整材质表现（表面纹理、反射特性）
       │   └── 保持环境构造的核心一致性
       ├── 继承记录：
       │   ├── 每个镜头继承环境构造（空间骨架、四层结构、材质、光影、动态元素）
       │   ├── 每个镜头继承置信度和引擎输出摘要
       │   ├── 记录导演审核意见
       │   └── 标注与九宫格的对应关系
       ├── 【提示词写法】遵循 sequence-board-template.md 中的规范
       └── 自动创建新板（当节拍需要跨板展开时）

步骤8: 执行提示词精简 ← 【V5.0强制执行】
       ├── 读取 common/prompt-simplifier.md
       ├── 对每个镜头的"画面描述"字段执行精简算法
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

步骤9: 执行连贯性检查 ← 【V4.0更新】
       ├── 读取 common/coherence-checker.md
       ├── 检查跨板连贯性：
       │   ├── 动势组的连续性
       │   ├── 蒙太奇组的连续性
       │   └── 长镜头的连续性
       └── 验证策略一致性

步骤10: 保存输出文件 ← 【V4.0更新】
        └── outputs/sequence-board-prompt-{集数}-board*.md ← 【V4.0更新】
            ├── 支持多个板（根据策略自动创建）
            ├── 包含：继承记录章节 + 动态分镜板提示词（1-4 格）
            └── 板与板之间通过"跨板连续性"标记连接

步骤11: 调用导演审核（storyboard-review-skill）
       ├── 读取 .agent-state.json，检查 director 是否有 agentId
       ├── 如果有 agentId 且 status 不是 "error"：
       │   └── 使用 Resume 调用：Resume agent <agentId> and 审核四宫格提示词
       ├── 如果没有 agentId 或 status 是 "error"：
       │   └── 使用首次调用：Use director agent to 审核四宫格提示词
       ├── 读取 storyboard-review-skill/review-checklist.md
       ├── 读取 storyboard-review-skill/asset-consistency-rules.md（如需要）
       ├── 按 Sequence Board 验收清单逐项检查
       ├── 生成审核报告：outputs/sequence-board-prompt-{集数}-review.md
       ├── 捕获返回的 agentId（从 JSON 元数据中）
       └── 更新 .agent-state.json：
           ├── 更新 director.agentId
           ├── 更新 director.last_task 为 "sequence-review"
           ├── 更新 director.last_used 为当前时间
           └── 更新 director.status 为 "idle"

步骤12: 执行用户确认（CP3）
        ├── 读取 common/user-confirmation-protocol.md
        ├── 展示标准确认UI：
        │   ├── 进度条
        │   ├── 质量评分
        │   ├── 审核状态
        │   └── 操作选项：[通过] ✅ / [修改] ✏️ / [重生成] 🔄 / [回滚] ⏪
        ├── 调用 question 工具
        ├── ⚠️ **立即停止执行**
        └── 等待用户显式指令（"继续"或"通过"）

步骤13: 用户显式确认后 - 创建快照（按 common/snapshot-management.md）
            ├── 快照类型：分组快照（CP3）
            ├── 保存路径：.strategic-snapshots/snapshot-{编号}/
            └── 更新 .agent-state.json：
                ├── 更新 phase 为 "motion"
                ├── 更新 current_episode 为当前集数
                └── 更新所有 subagent 的 last_used 时间戳

步骤14: 进入下一阶段或结束
           ├── [通过] → 可执行 /motion 进入动态提示词阶段
           ├── [修改] → 等待修改后重新审核
           ├── [重生成] → 返回步骤1重新执行
           └── [回滚] → 恢复到历史快照
 ```

## 模块依赖

| 模块 | 作用 | 是否必需 |
|------|------|----------|
| common/dynamic-breakdown-engine.md | 动态分镜引擎 | ✅ 必需 (V4.0) |
| common/coherence-checker.md | 连贯性检查 | ✅ 必需 |
| film-storyboard-skill/templates/sequence-board-template.md | 输出格式模板 | ✅ 必需 |

## 协议文件

| 文件 | 作用 | 调用时机 |
|------|------|----------|
| common/user-confirmation-protocol.md | 用户确认UI规范 | 步骤12执行前 |
| common/snapshot-management.md | 快照创建规则 | 步骤13执行前 |

## contextFiles 定义 [V4.1-CRITICAL]

| 文件类型 | 文件路径 | 用途 | 必填 |
|----------|----------|------|------|
| Markdown | `outputs/beat-breakdown-{集数}.md` | 节拍拆解表 | ✅ |
| Markdown | `outputs/beat-board-prompt-{集数}-board*.md` | 九宫格提示词 | ✅ |
| JSON | `outputs/scene-breakdown-{集数}.json` | 全量数据层 | ✅ [依赖] |
| JSON | `outputs/beat-board-full-list-{集数}.json` | 九宫格数据 | ✅ [依赖] |
| JSON | `outputs/sequence-board-data-{集数}.json` | 四宫格数据 | ✅ [生成] |
| 状态 | `.agent-state.json` | 项目配置 | ✅ |

**JSON 生成规则**：
- `/sequence` 执行后必须生成 `sequence-board-data-{集数}.json`
- JSON 包含：boards数组、cards数组、cross_grid_continuity、tween_suppression
- 必须读取上游的 `beat-board-full-list-{集数}.json`

**依赖检查**：
- ⚠️ beat-board-full-list-{集数}.json 缺失 → 立即停止，要求重新执行 /beatboard
- ⚠️ sequence-board-data-{集数}.json 生成失败 → 立即停止

## JSON输出格式说明 ← 【V5.0新增】

### sequence-board-data-{集数}.json 结构

```json
{
  "version": "5.0",
  "episode_id": "ep01",
  "project_config": {
    "visual_style": "[风格]",
    "aspect_ratio": "[比例]",
    "target_medium": "[媒介]",
    "genre": "[类型]"
  },
  "metadata": {
    "episode": "ep01",
    "board_id": "sequence_board_01",
    "generated_at": "ISO timestamp",
    "source_beat_board": "outputs/beat-board-prompt-{集数}-board01.md",
    "source_beat_json": "outputs/beat-board-full-list-{集数}.json",
    "total_shots": 4
  },
  "boards": [
    {
      "board_id": "sequence_board_01",
      "board_number": 1,
      "beat_range": [1, 3],
      "grid_count": 4, // 建议格子数（基于策略+复杂度），实际以shots.length为准
      "inherited_from": {
        "beat_board": "board_01",
        "grids": ["grid_3", "grid_4", "grid_5"],
        "director_review": "[审核意见]",
        "confidence": 85,
        "engine_summary": "[引擎摘要]"
      },
      "shots": [
        {
          "shot_id": 1,
          "position": "左上",
          "beat_id": 3,
          "strategy_tag": "[标签]",
          "original_grid": {
            "grid_id": "grid_X",
            "beat_id": 3,
            "visual_description": "[原画面描述]",
            "camera": "[原镜头]",
            "style_tags": ["[标签1]", "[标签2]"],
            "environment": {
              "spatial_skeleton": "[空间骨架]",
              "four_layers": {
                "foreground": "[前景层]",
                "midground": "[中景层]",
                "background": "[背景层]",
                "sky": "[天空层]"
              },
              "materials": {
                "surfaces": "[表面特征]",
                "textures": "[纹理细节]"
              },
              "lighting": {
                "light_source": "[光源类型]",
                "color_palette": "[色彩氛围]",
                "atmosphere": "[氛围]"
              },
              "dynamic_elements": ["[动态元素1]", "[动态元素2]"]
            },
            "alternative_frames": [
              {
                "frame_type": "secondary",
                "role": "[角色]",
                "action": "[动作]",
                "drama_tension_score": 0.8,
                "reason": "[未选择原因]"
              }
            ]
          },
          "expanded_shot": {
            "visual_description": "[展开后画面描述（含台词融入）]",
            "camera_movement": "[运动]",
            "duration": 4,
            "strategy_tag": "[标签]",
            "relationship": "[与其他镜头的关系]",
            "dialogue": [  // 可选，无对话则为空数组
              {
                "type": "spoken",
                "speaker": "角色A",
                "content": "台词内容",
                "tone": "语气描述"
              }
            ]
          }
        }
      ],
      "continuity_check": {
        "axis_law": "pass/fail",
        "eyeline_match": "pass/fail",
        "action_flow": "pass/fail",
        "lighting_consistency": "pass/fail",
        "dialogue_coherence": "pass/fail" // 如果无对话可省略或填"n/a"
      }
    }
  ],
  "summary": {
    "total_shots": 4,
    "shots_with_dialogue": 3,
    "shots_with_inherited_environment": 4,
    "grid_count_dynamic": true,
    "strategy_distribution": {
      "[单镜]": 2,
      "[动势组]": 1,
      "[蒙太奇组]": 1,
      "[长镜头]": 0
    },
    "continuity_check_passed": true
  }
}
```

### 字段说明

| 字段 | 类型 | 说明 | V5.0变更 |
|------|------|------|----------|
| **version** | string | JSON版本号 | 5.0 ← 4.1 |
| **project_config** | object | 项目配置（视觉风格、画幅比例等） | 无变更 |
| **metadata** | object | 生成元数据（时间戳、来源文件等） | 新增 |
| **boards** | array | 分镜板数组 | 无变更 |
| **board_id** | string | 分镜板唯一标识 | 无变更 |
| **grid_count** | number | 建议格子数（基于策略+复杂度） | 添加注释说明 |
| **shots** | array | 镜头数组（1-4个，动态调整） | 无变更 |
| **position** | string | 四宫格位置（左上/右上/左下/右下） | 无变更 |
| **original_grid** | object | 九宫格原画面完整信息 | 扩展 |
| **original_grid.environment** | object | 完整环境构造（5个子对象） | 新增完整结构 |
| **original_grid.alternative_frames** | array | 备选帧数组 | 新增 |
| **expanded_shot.dialogue** | array | 台词数组（spoken/inner/narrator） | 新增 |
| **continuity_check.dialogue_coherence** | string | 台词连贯性检查 | 新增 |
| **summary** | object | 统计摘要 | 新增 |

## 相关文件
- 模板：`film-storyboard-skill/templates/sequence-board-template.md`
- 动态分镜引擎：`common/dynamic-breakdown-engine.md`
- 连贯性检查：`common/coherence-checker.md`
- 审核：`storyboard-review-skill/`（使用 review-checklist.md）
- 协议：`common/user-confirmation-protocol.md`、`common/snapshot-management.md`
