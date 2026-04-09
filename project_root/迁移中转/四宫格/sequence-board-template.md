---
name: sequence-board-template
description: Sequence Board 四宫格提示词模板（V5.0精简继承版）。用于将九宫格展开为四宫格，每组4个镜头覆盖连续的节拍范围，保留完整台词和旁白。
---

# Sequence Board - {集数}（继承自九宫格 Board{板号}）

## 一、项目配置与继承来源

### 1.1 项目配置（从.agent-state.json读取）
- **集数**：{集数标识}
- **视觉风格**：{真人写实/国潮动漫/科幻/古装等}
- **目标媒介**：{短剧/电影/广告/漫剧等}
- **画幅比例**：{16:9/2.35:1/4:3/9:16等}
- **叙事结构**：{经典三幕式/英雄之旅/起承转合/多巴胺闭环}
- **类型**：{动作/悬疑/爱情/喜剧/科幻等}

### 1.2 继承来源
- **继承自**：九宫格 Board{板号}
- **原格子**：格{1-9}（覆盖节拍X-Y）
- **导演审核**：{从 outputs/beat-board-prompt-{集数}-review.md 复制审核意见}
- **置信度**：{X}%
- **引擎摘要**：{蒙太奇逻辑分析摘要 + 影视联想分析摘要}

### 1.3 数据来源与字段依赖 ← 【V5.0新增】

**数据来源优先级**：
1. **首选**：`scene-breakdown-{集数}.json["shots"][i]["source_text"]`
   - 完整剧本原文，包含对话、动作、环境描述
   - 用于验证画面描述准确性，防止AI脑补
2. **备选**：`beat-breakdown-{集数}.md` 的"场景描述"字段
   - 当source_text缺失时使用
   - 必须标记警告并提示补充原文

**禁止行为**：
- ❌ 基于场景描述进行创造性发挥
- ❌ 添加剧本中不存在的情节
- ❌ 修改角色行为或动机

### 1.4 策略标签映射
根据节拍拆解的核心策略，确定本板的镜头分配：

| 策略标签 | 镜头数 | 适用场景 | 排列规则 |
|---------|--------|---------|---------|
| `[单镜]` | 1格 | 对话、静态情感、特写 | 标准位置 |
| `[动势组]` | 2格 | 动作序列、情绪递进 | 连续格子（水平或垂直） |
| `[蒙太奇组]` | 3-4格 | 复杂场景、多角度展示 | L型或连续多格 |
| `[长镜头]` | 1格（长时长） | 连续动作、一镜到底 | 关键节点选取 |

### 1.5 复杂度调整
- **复杂度评分**：{X.X}/5.0
- **最终格子数**：{X}格（基于复杂度自动调整）

---

## 二、替代帧展开机制 ← 【V4.1新增】

### 2.1 数据源

**唯一数据源：JSON alternative_frames**

- **文件**：`outputs/beat-board-full-list-{集数}.json`
- **字段**：`grids[].alternative_frames`
- **包含**：type（类型）、role（角色）、action（动作）、reason（原因）、drama_tension_score（戏剧张力）
- **详细逻辑**：详见 `.claude/common/dynamic-breakdown-engine.md`

---

### 2.2 策略标签体系与展开规则

| 策略标签 | 基础格子数 | 展开规则 | 适用场景 |
|---------|-----------|---------|---------|
| **[单镜]** | 1格 | 1帧 → 1镜头 | 静态对话、情感特写 |
| **[动势组]** | 2格 | 1帧 → 2镜头（起势 + 落幅） | 追逐、移动、简单动作 |
| **[蒙太奇组]** | 3-4格 | 1帧 → 3-4镜头（起势 + 高潮 + 余韵） | 时间压缩、情绪渲染、复杂转折 |
| **[长镜头]** | 1-3格 | 1帧 → 1-3镜头（动态调整） | 连续动作、复杂调度、环境展示 |
| **[正反打]** | 2格 | 1帧 → 2镜头（A角 + B角） | 对话冲突、角色对峙 |
| **[环境]** | 1-2格 | 1帧 → 1-2镜头 | 场景建立、氛围渲染 |
| **[特写]** | 1格 | 1帧 → 1镜头 | 表情、物品、情感表达 |
| **[全景]** | 1格 | 1帧 → 1镜头 | 空间定位、群体场景 |
| **[中景]** | 1-2格 | 1帧 → 1-2镜头 | 对话、互动、动作展示 |

---

### 2.3 展开示例

**正反打：1个九宫格格 → 2个镜头**
```
格02（九宫格）→ JSON包含：[正反打A角, 正反打B角]
    ↓
镜头3（特写｜正反打A角）+ 镜头4（特写｜正反打B角）
```

**动势组：1个九宫格格 → 2个镜头**
```
格05（九宫格）→ JSON包含：[起势, 落幅]
    ↓
镜头9（跟拍｜起势）+ 镜头10（特写｜落幅）
```

**蒙太奇组：1个九宫格格 → 3-4镜头**
```
格06（九宫格）→ JSON包含：[起势, 高潮, 余韵]
    ↓
镜头11（起势）+ 镜头12（高潮）+ 镜头13（余韵）+ [可选镜头14]
```

---

### 2.4 JSON Schema 更新

**expanded_shot 字段（V4.1新增 alternative_frame_source）：**
```json
"expanded_shot": {
  "visual_description": "[展开后画面描述]",
  "camera_movement": "[运动]",
  "strategy_tag": "[标签]",
  "relationship": "[与其他镜头的关系]",
  "alternative_frame_source": {  ← 【V4.1新增】
    "grid_id": "2",
    "frame_type": "secondary",
    "role": "镇关西",
    "action": "正反打A角",
    "drama_tension_score": 0.8,
    "reason": "视觉冲击权重低",
    "inherited_from": "JSON.alternative_frames"
  }
}
```

**完整算法实现详见**：`.claude/common/dynamic-breakdown-engine.md`

---

## 三、四宫格镜头展开

### 【镜头 1】四宫格位置：左上画面

#### 九宫格原画面 - 格{X}
**画面描述**：{完整复制九宫格该格的画面描述，包含环境构造、对话、心理活动}

**镜头**：{原镜头信息}

**风格标签**：{原风格标签}

**环境构造**：
- **空间骨架**：{基础布局、关键物体位置、角色活动范围}
- **四层结构**：{前景层/中景层/背景层/天空层}
- **材质定义**：{表面特征、纹理细节}
- **光影基调**：{光源类型、色彩氛围}
- **动态元素**：{需要动态效果的对象}

#### 四宫格展开画面（对应九宫格 格{X}）
**画面描述**（继承 + 微调）：
{继承九宫格格{X}的画面描述，包含完整环境构造（空间骨架、四层结构、材质、光影基调、动态元素）。根据文案实际情况调整镜头角度、运动方式、光影效果、材质表现。**将台词/对话/旁白自然融入描述中**，例如："角色A说'台词内容'，同时..." 或 "旁白：'旁白内容'，画面展示..."}

**镜头信息**：
- **镜头运动**：{推拉/摇移/跟拍/升降/固定}
- **时长**：{X}秒
- **策略标签**：{单镜/动势组/蒙太奇组/长镜头}
- **对应九宫格**：格{X}
- **镜头关系**：{与右上画面的关系：如动作衔接/视角切换/时间并行/正反打/情绪递进}

---

### 【镜头 2】四宫格位置：右上画面

#### 九宫格原画面 - 格{Y}
**画面描述**：{完整复制九宫格该格的画面描述}

**镜头**：{原镜头信息}

**风格标签**：{原风格标签}

**环境构造**：
- **空间骨架**：{...}
- **四层结构**：{...}
- **材质定义**：{...}
- **光影基调**：{...}
- **动态元素**：{...}

#### 四宫格展开画面（对应九宫格 格{Y} 或 格{X}的展开）
**画面描述**（继承 + 微调）：
{同上格式，将台词/对话/旁白自然融入描述}

**镜头信息**：
- **镜头运动**：{类型}
- **时长**：{X}秒
- **策略标签**：{标签}
- **对应九宫格**：格{Y} 或 格{X}展开
- **镜头关系**：{与左上画面的关系：如正反打/动作连贯/情绪递进/视角切换}

---

### 【镜头 3】四宫格位置：左下画面

#### 九宫格原画面 - 格{Z}
**画面描述**：{完整复制九宫格该格的画面描述}

**镜头**：{原镜头信息}

**风格标签**：{原风格标签}

**环境构造**：
- **空间骨架**：{...}
- **四层结构**：{...}
- **材质定义**：{...}
- **光影基调**：{...}
- **动态元素**：{...}

#### 四宫格展开画面（对应九宫格 格{Z} 或 展开）
**画面描述**（继承 + 微调）：
{同上格式，将台词/对话/旁白自然融入描述}

**镜头信息**：
- **镜头运动**：{类型}
- **时长**：{X}秒
- **策略标签**：{标签}
- **对应九宫格**：格{Z} 或 展开
- **镜头关系**：{与左上/右上画面的关系：如动作衔接/情绪递进/高潮揭示}

---

### 【镜头 4】四宫格位置：右下画面

#### 九宫格原画面 - 格{W}
**画面描述**：{完整复制九宫格该格的画面描述}

**镜头**：{原镜头信息}

**风格标签**：{原风格标签}

**环境构造**：
- **空间骨架**：{...}
- **四层结构**：{...}
- **材质定义**：{...}
- **光影基调**：{...}
- **动态元素**：{...}

#### 四宫格展开画面（对应九宫格 格{W} 或 展开）
**画面描述**（继承 + 微调）：
{同上格式，将台词/对话/旁白自然融入描述}

**镜头信息**：
- **镜头运动**：{类型}
- **时长**：{X}秒
- **策略标签**：{标签}
- **对应九宫格**：格{W} 或 展开
- **镜头关系**：{与其他三个画面的关系：如收尾镜头/情绪总结/冲突爆发}

---

## 三、跨板连续性检查

- [ ] **轴线法律**：检查180度规则
- [ ] **视线匹配**：角色视线方向一致
- [ ] **动作连贯**：动作衔接自然
- [ ] **光影一致**：时间/光源连续性
- [ ] **台词连贯**：对话逻辑顺畅

---

## 四、sequence-board-data-{集数}.json 输出规范

### JSON Schema

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
    "generated_at": "2026-02-03T13:05:00Z",
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
              "spatial_skeleton": "[空间骨架：基础布局、关键物体位置、角色活动范围]",
              "four_layers": {
                "foreground": "[前景层描述]",
                "midground": "[中景层描述]",
                "background": "[背景层描述]",
                "sky": "[天空层描述]"
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
            "dialogue": [
              {
                "type": "spoken",
                "speaker": "角色A",
                "content": "台词内容",
                "tone": "语气描述"
              },
              {
                "type": "inner",
                "speaker": "角色A",
                "content": "心理活动",
                "tone": "内心想法"
              },
              {
                "type": "narrator",
                "speaker": "旁白",
                "content": "旁白内容",
                "tone": "叙事口吻"
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

### 输出说明

- **version**：JSON版本号（V5.0）
- **project_config**：项目配置信息（视觉风格、画幅比例等）
- **metadata**：生成元数据（时间戳、来源文件等）
- **boards数组**：所有分镜板
  - **board_id**：分镜板唯一标识
  - **board_number**：分镜板序号
  - **beat_range**：覆盖的节拍范围
  - **grid_count**：建议格子数（基于策略+复杂度），实际以shots.length为准
  - **inherited_from**：继承来源信息
    - **beat_board**：继承的九宫格板号
    - **grids**：继承的九宫格格子列表
    - **director_review**：导演审核意见
    - **confidence**：置信度
    - **engine_summary**：引擎摘要
  - **shots数组**：每个板的镜头（1-4个，动态调整）
    - **shot_id**：镜头序号
    - **position**：四宫格位置（左上/右上/左下/右下）
    - **beat_id**：对应节拍ID
    - **strategy_tag**：策略标签
    - **original_grid**：九宫格原画面完整信息
      - **grid_id**：九宫格格子ID
      - **beat_id**：对应节拍ID
      - **visual_description**：原画面描述
      - **camera**：原镜头信息
      - **style_tags**：风格标签数组
      - **environment**：完整环境构造对象（5个子对象）
        - **spatial_skeleton**：空间骨架
        - **four_layers**：四层结构（前景/中景/背景/天空）
        - **materials**：材质定义
        - **lighting**：光影基调
        - **dynamic_elements**：动态元素数组
      - **alternative_frames**：备选帧数组（从九宫格继承）
    - **expanded_shot**：四宫格展开画面
      - **visual_description**：展开后画面描述（含台词融入）
      - **camera_movement**：镜头运动
      - **duration**：时长（秒）
      - **strategy_tag**：策略标签
      - **relationship**：与其他镜头的关系
      - **dialogue**：台词数组（可选，无对话则为空数组）
        - **type**：台词类型（spoken说出的/inner内心/narrator旁白）
        - **speaker**：说话者
        - **content**：内容
        - **tone**：语气/口吻
  - **continuity_check**：跨板连续性检查
    - **axis_law**：轴线法律（180度规则）
    - **eyeline_match**：视线匹配
    - **action_flow**：动作连贯
    - **lighting_consistency**：光影一致
    - **dialogue_coherence**：台词连贯（如果无对话可省略或填"n/a"）
- **summary**：统计摘要
  - **total_shots**：总镜头数
  - **shots_with_dialogue**：含台词的镜头数
  - **shots_with_inherited_environment**：继承完整环境的镜头数
  - **grid_count_dynamic**：是否为动态格子数
  - **strategy_distribution**：策略分布统计
  - **continuity_check_passed**：连贯性检查是否通过
