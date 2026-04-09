---
name: film-storyboard-skill
description: 影视分镜生成技能。将剧本转化为分镜产出，采用分层渐进式流程：节拍拆解 → 九宫格 → 动态分镜板（支持可变格子数1-4格）。
---

# Film Storyboard Skill

## 技能概述

本技能负责将剧本转化为完整的分镜产出，采用**分层渐进式流程**：

1. **节拍拆解** - 将剧本分解为可拍摄的镜头单元
2. **九宫格** - 选择每个节拍的最强关键帧
3. **动态分镜板** - 将九宫格展开为1-4格的可变分镜，整合台词和旁白

## 核心能力

### 创意引擎系统（V7.0）

**三大引擎协同工作**：

| 引擎 | 功能 | 输出 |
|------|------|------|
| **蒙太奇逻辑引擎** | 分析戏剧权重、镜头拆解建议、三段式拆解 | 戏剧权重、镜头建议、置信度 |
| **影视联想引擎** | 检索匹配影片、提取视觉DNA | 参考影片、匹配度、视觉DNA |
| **通感视觉化引擎** | 识别感官刺激、转化视觉符号 | 触发条件、视觉转化方案 |

### 环境构造系统（V2.0）

**环境构造四阶段**：

| 阶段 | 功能 | 输出 |
|------|------|------|
| **空间骨架构建** | 定义基础空间布局、物体位置、角色活动范围 | 基础空间布局 |
| **材质皮肤覆盖** | 定义表面材质、纹理细节、物理属性 | 材质定义 |
| **光影氛围注入** | 布置光源、设计光影效果、渲染氛围 | 光影效果 |
| **动态生命添加** | 添加动态元素、粒子效果、交互响应 | 动态效果 |

### V3.0 新功能系统

**多结构叙事模板**：

| 结构 | 适用场景 | 特点 |
|------|----------|------|
| **经典三幕式** | 传统电影、电视剧 | 15-25% / 50-70% / 15-25% 比例 |
| **英雄之旅** | 奇幻冒险、成长故事 | 12步英雄旅程结构 |
| **起承转合** | 东方情感叙事 | 四段式情感递进结构 |
| **多巴胺闭环** | 短剧、短视频 | 45秒多巴胺循环，结尾悬念/CTA |

**潜台词分析系统**：

| 层级 | 功能 | 输出 |
|------|------|------|
| **探测层** | 识别表面动作和关键词 | 关键词列表 |
| **翻译层** | 映射到心理动机和潜台词 | 心理动词、潜台词 |
| **表现层** | 生成视觉对应物和拍摄建议 | 视觉元素、镜头建议 |

**类型化戏剧权重计算**：
- **事件类型映射**：生死攸关(3.0-4.0)、核心转折(2.5-3.5)等
- **类型修正系数**：动作片×1.5、悬疑片×1.5、爱情片×0.8等
- **权重算法**：表现权重 = 目标综合权重 ÷ 叙事功能基重

## 执行流程

### 阶段A：节拍拆解（/breakdown）

```
用户剧本
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ 步骤1: 读取剧本 + 提取角色设定 ← 【方案D新增】                  │
│  - 读取 script/{集数}.md                                        │
│  - 提取场景描述、对话、动作                                     │
│  - 【新增】提取YAML中的角色设定                                 │
│  - 执行：python3 configs/character-loader.py                   │
│  - 输出：按需加载的角色设定（基于style_transitions）             │
└─────────────────────────────────────────────────────────────────┘
<!-- LOG:STEP read=script/{集数}.md,module=character-loader.py,note=提取角色设定和YAML配置 -->
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ 步骤2: 执行节拍拆解                                             │
│  - 使用 .claude/common/beat-analyzer.md                                 │
│  - 识别叙事节拍（对话/动作/情绪转折点）                         │
│  - 计算戏剧权重（类型修正系数）                                 │
│  - 标记策略标签（[单镜]/[动势组]/[蒙太奇组]/[长镜头]）         │
│  - 建议格子数（基于复杂度评分）                                 │
│  - 潜台词分析（探测→翻译→表现）                               │
└─────────────────────────────────────────────────────────────────┘
<!-- LOG:STEP read=.claude/common/beat-analyzer.md:1-1152,algorithm=beat_analysis,drama_weight_v4.1,type_correction,output=shot_list,strategy_tags,complexity_scores,note=完整读取beat-analyzer包含戏剧权重映射和类型修正表 -->
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ 步骤3: 生成 scene-breakdown-{集数}.json                         │
│  - 包含：shots数组、sub_shots、statistical_summary              │
│  - shots包含：shot_id、beat_id、scene_description、ndi、lens_type │
│  - 子镜头数组（sub_shots）用于复杂节拍                          │
│  - 统计摘要：total_shots、strategy_distribution、acts          │
│  - 【新增】character_settings（嵌入角色设定）                   │
│  - 【新增】style_transitions（风格转换规则）                    │
└─────────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ 步骤4: 生成 beat-breakdown-{集数}.md                            │
│  - 表格形式展示所有节拍                                         │
│  - 包含：场景描述、原文引用、NDI分析、镜头建议、策略标签        │
│  - 【V5.0关键更新】原文引用指向JSON中的source_text字段          │
│  - 完整原文存储在scene-breakdown-{集数}.json中                    │
│  - 三幕结构标注                                                 │
└─────────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ 步骤5: 执行质量检查                                             │
│  - 使用 .claude/common/quality-check.md                                 │
│  - 检查：三幕比例、节拍数量、镜头建议合理性                     │
│  - 检查：【新增】角色设定准确性（基于character_settings）       │
│  - 检查：【新增】风格转换逻辑正确性                             │
│  - 生成质量报告                                                 │
└─────────────────────────────────────────────────────────────────┘
<!-- LOG:STEP read=.claude/common/quality-check.md:1-213,algorithm=quality_check,output=quality_report -->
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ 步骤6: 生成 JSON 数据文件                                       │
│  - scene-breakdown-{集数}.json（含角色设定嵌套）               │
│  - beat-breakdown-{集数}.md                                     │
└─────────────────────────────────────────────────────────────────┘
<!-- LOG:STEP write=outputs/scene-breakdown-{集数}.json,outputs/beat-breakdown-{集数}.md,output=data_files,note=生成结构化JSON和可读MD -->
```

**输出文件**：
- `outputs/scene-breakdown-{集数}.json` - 结构化数据
- `outputs/beat-breakdown-{集数}.md` - 可读表格
<!-- LOG:STEP note=阶段A完成，总耗时约6-8秒 -->

---

## 角色设定使用规则（方案D通用规则）

### 规则1：访问角色设定

**格式**：
```
scene_breakdown_json["character_settings"][角色名][风格名][字段名]
```

**示例**：
```python
# 在节拍拆解中生成画面描述时
luda_headwear = scene_breakdown_json["character_settings"]["鲁达"]["国潮动漫风格"]["headwear"]
# → "暗青灰色芝麻罗纱头巾，哑光无反光质感"
```

### 规则2：检测当前节拍的视觉风格

**算法**：
```python
def get_style_for_beat(beat_number):
    """根据节拍号获取当前应使用的风格"""
    style_transitions = scene_breakdown_json["style_transitions"]
    for transition in style_transitions:
        if beat_number >= transition["beat"]:
            return transition["to"]
    # 如果没有转换规则，使用第一个风格
    if style_transitions:
        return style_transitions[0]["from"]
    return "默认风格"
```

**示例**：
```python
# 节拍1-9：国潮动漫风格
# 节拍10-11：MCU电影史诗感
# 节拍12+：像素风格
```

### 规则3：处理null值字段

**原则**：null值表示该角色/风格组合下该字段不适用

**处理方式**：
```python
def safe_get_char_field(character, style, field):
    """安全获取角色字段，处理null值"""
    char_setting = scene_breakdown_json["character_settings"].get(character, {}).get(style, {})
    value = char_setting.get(field)
    return value if value else ""  # null或None返回空字符串
```

### 规则4：生成画面描述时的角色外貌组合

**模板**：
```
{角色名}：{身形描述}，{上装}，{头饰（如有）}，{配饰（如有）}
```

**示例**：
```python
# 国潮动漫风格下的鲁达
char_info = scene_breakdown_json["character_settings"]["鲁达"]["国潮动漫风格"]
physical = char_info["physical"]  # "身形魁梧，身高九尺..."
upper_body = char_info["upper_body"]  # "翡翠鹦哥绿朱丝战袍"
headwear = char_info["headwear"]  # "暗青灰色芝麻罗纱头巾..."

# 组合成画面描述
character_appearance = f"鲁达：{physical}，{upper_body}，{headwear}"
```

### 规则5：角色设定字段说明

| 字段 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| physical | string | ✅ | 身形描述 | "身形魁梧，身高九尺，腰阔十围" |
| headwear | string/null | ⚪ | 头饰描述 | "暗青灰色芝麻罗纱头巾" 或 null |
| upper_body | string | ✅ | 上装描述 | "翡翠鹦哥绿朱丝战袍" |
| waist | string/null | ⚪ | 腰饰描述 | "鸦青宫绦" 或 null |
| footwear | string/null | ⚪ | 鞋履描述 | "暗黄宋代风格靴子" 或 null |
| accessories | string/null | ⚪ | 配饰描述 | "红色露指战术手套" 或 null |
| skin | string/null | ⚪ | 皮肤描述 | "粉色皮肤带细腻纹理" 或 null |
| rendering | string | ✅ | 渲染风格描述 | "平涂赛璐璐风格，墨线轮廓粗犷遒劲" |

### 规则6：风格转换逻辑

**场景切换检测**：
```python
# 检测节拍8是否为风格转换点
def is_style_transition_beat(beat_number):
    transitions = scene_breakdown_json["style_transitions"]
    return any(t["beat"] == beat_number for t in transitions)
```

**画面描述标注**：
```python
if is_style_transition_beat(beat_number):
    from_style = get_style_for_beat(beat_number - 1)
    to_style = get_style_for_beat(beat_number)
    description += f"\n【风格转换点：{from_style} → {to_style}】"
```

### 规则7：多剧本通用性

**适用场景**：
- 不同剧本有不同的角色
- 不同角色有不同的风格
- 不同风格有不同的转换规则

**实现方式**：
1. 剧本A：提取角色A/B/C的设定
2. 剧本B：提取角色X/Y/Z的设定
3. 自动适配：算法不依赖具体角色名或风格名

---

### 阶段B：九宫格（/beatboard）

```
节拍拆解表
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ 步骤1: 读取节拍拆解表                                           │
│  - 读取 outputs/beat-breakdown-{集数}.md                        │
│  - 提取每个节拍的原文内容、NDI分析、镜头建议                   │
│  - 读取 scene-breakdown-{集数}.json 获取结构化数据              │
└─────────────────────────────────────────────────────────────────┘
<!-- LOG:STEP read=outputs/beat-breakdown-{集数}.md,outputs/scene-breakdown-{集数}.json -->
<!-- LOG:STEP read=outputs/beat-breakdown-{集数}.md,outputs/scene-breakdown-{集数}.json -->
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ 步骤2: 读取九宫格提示词和原文内容 ← 【V5.0更新】                │
│  ├─ outputs/beat-board-prompt-{集数}-board*.md                  │
│  │   - 提取：每个格子的画面描述、环境构造、置信度、引擎摘要       │
│  ├─ outputs/beat-breakdown-{集数}.md（节拍拆解表）              │
│  │   - 【V5.0新增】提取：每个节拍的"原文内容"字段               │
│  │   - 包含：完整对话、旁白、心理活动、动作描述                  │
│  └─ 【V5.0新增】建立映射：九宫格格子 ↔ 节拍原文内容              │
└─────────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ 步骤3: 执行关键帧选择                                           │
│  - 使用 .claude/common/keyframe-selector.md                             │
│  - 应用戏剧张力算法（类型修正系数）                             │
│  - 选择每个节拍的**最强关键帧**（单帧原则）                     │
│  - 【方案B】标记备选帧（alternative_frames）                    │
│    - 记录：frame_type、role、action、drama_tension_score、reason │
└─────────────────────────────────────────────────────────────────┘
<!-- LOG:STEP read=.claude/common/keyframe-selector.md:1-385,algorithm=keyframe_selection_v4.1,output=grid_allocation,alternative_frames,note=单帧原则强制检查 -->
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ 步骤4: 执行环境构造                                             │
│  - 使用 .claude/common/environment-construction-guide/                  │
│  - 四阶段：空间骨架 → 材质皮肤 → 光影氛围 → 动态生命            │
│  - 为每个关键帧生成完整环境描述                                 │
└─────────────────────────────────────────────────────────────────┘
<!-- LOG:STEP read=.claude/common/environment-construction-guide/index.md,algorithm=environment_construction_v2.0,output=environment_package,note=四阶段环境构造 -->
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ 步骤5: 生成 beat-board-prompt-{集数}-board*.md                  │
│  - 每板9格，每格1个关键帧                                       │
│  - 包含：画面描述、环境构造、镜头、风格标签、置信度            │
│  - 【方案B】包含 alternative_frames 字段                        │
│  - 【V4.0新增】包含策略标签（[单镜]/[动势组]/[蒙太奇组]/[长镜头]）│
│  - 【V4.0新增】包含建议格子数（suggested_grids）                │
└─────────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ 步骤6: 生成 beat-board-full-list-{集数}.json                    │
│  - 包含所有格子的结构化数据                                     │
│  - 包含：grids数组、continuity_check、summary                   │
│  - grids包含：grid_id、beat_id、visual_description、environment  │
│  - 【方案B】包含 alternative_frames 数组                        │
└─────────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ 步骤7: 执行连贯性检查                                           │
│  - 使用 .claude/common/coherence-checker.md                             │
│  - 检查：角色一致性、环境一致性、光影连续性、材质连续性          │
│  - 检查：情绪弧线、风格统一性                                   │
│  - 生成连贯性报告                                               │
└─────────────────────────────────────────────────────────────────┘
<!-- LOG:STEP read=.claude/common/coherence-checker.md,algorithm=coherence_check,output=continuity_report,note=跨板连贯性检查 -->
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ 步骤8: 生成 beat-board-prompt-{集数}-review.md                  │
│  - 导演审核用，包含所有格子的画面描述                           │
│  - 标记需要导演决策的问题                                       │
└─────────────────────────────────────────────────────────────────┘
```

**输出文件**：
- `outputs/beat-board-prompt-{集数}-board*.md` - 分板提示词
- `outputs/beat-board-full-list-{集数}.json` - 完整数据
- `outputs/beat-board-prompt-{集数}-review.md` - 导演审核
<!-- LOG:STEP note=阶段B完成，总耗时约10-12秒 -->

---

### 阶段C：动态分镜板（/sequence）← 【V4.0更新】

```
九宫格提示词 + 导演审核通过
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ 步骤1: 读取九宫格提示词                                         │
│  - 读取 outputs/beat-board-prompt-{集数}-board*.md              │
│  - 提取每个格子的画面描述、环境构造、镜头、风格标签            │
│  - 读取导演审核意见（outputs/beat-board-prompt-{集数}-review.md）│
└─────────────────────────────────────────────────────────────────┘
<!-- LOG:STEP read=outputs/beat-board-prompt-{集数}-board*.md,outputs/beat-board-prompt-{集数}-review.md -->
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ 步骤2: 读取九宫格提示词和原文内容 ← 【V5.0更新】                │
│  ├─ outputs/beat-board-prompt-{集数}-board*.md                  │
│  │   - 提取：每个格子的画面描述、环境构造、置信度、引擎摘要       │
│  ├─ outputs/beat-breakdown-{集数}.md（节拍拆解表）              │
│  │   - 【V5.0新增】提取：每个节拍的"原文内容"字段               │
│  │   - 包含：完整对话、旁白、心理活动、动作描述                  │
│  └─ 【V5.0新增】建立映射：九宫格格子 ↔ 节拍原文内容              │
└─────────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ 步骤3: 调用动态拆解引擎 ← 【V4.1启用】                          │
│  - 使用 .claude/common/dynamic-breakdown-engine.md              │
│  - 执行 V4.1 裂变算法（8步流程）                                │
│    Step 1: 读取 V4.1 诊断信息（策略、复杂度、资产包ID、增厚等级）│
│    Step 2: 策略标签解析（核心策略、镜头运动、情感等）           │
│    Step 3: 资产包匹配与加载（环境资产包系统）                   │
│    Step 4: 视觉增厚优化（三级增厚：高级1.8×/中级1.4×/基础1.2×）│
│    Step 5: 复杂度驱动的格子调整（基础格子数 + 复杂度修正）      │
│    Step 6: 长节拍裂变判断（复杂度≥3.5自动拆分）                 │
│    Step 7: 内容分配到格子（父子裂变算法）                       │
│    Step 8: 跨板连续性检查（视觉/时间/情绪/角色评分）            │
│  - 输出：动态分镜板布局方案（1-4可变格子）                      │
└─────────────────────────────────────────────────────────────────┘
<!-- LOG:STEP read=.claude/common/dynamic-breakdown-engine.md:1-1641,algorithm=dynamic_breakdown_v4.1,steps=8,output=grid_allocation_1-4,note=策略标签驱动的格子分配 -->
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ 步骤6.5: 执行生成前检查 ← 【V1.0新增】                         │
│  - 读取 .claude/common/sequence-generation-checklist.md          │
│  - 验证所有必填字段已就绪                                      │
│  - 检查角色名称是否在剧本定义中                                │
│  - 确保source_text原文可读取                                   │
│  - 检查alternative_frames数据结构                              │
│  - 执行：python3 .claude/common/sequence-validator.py <output> │
│  - 校验失败则阻断流程                                          │
└─────────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ 步骤7: 展开九宫格为四宫格并整合台词 ← 【V5.0重写】               │
│  【V5.0核心】展开九宫格提示词：                                 │
│  - 为每个九宫格格子生成1-4个镜头展开                             │
│  - 根据策略标签分配格子数和位置（左上/右上/左下/右下）          │
│  - 完整保留九宫格原画面信息（放在对应四宫格前）                 │
│  - 标注每个镜头的四宫格位置                                     │
│                                                                │
│  【V5.0新增】整合台词/旁白：                                     │
│  - 从节拍拆解表的"原文内容"字段提取完整对话                     │
│  - 将台词自然融入画面描述段落（角色说"台词"，同时...）         │
│  - 保留旁白信息（旁白："内容"，画面展示...）                   │
│  - 保留心理活动（角色内心：想法描述）                           │
│                                                                │
│  【V5.0新增】微调权限：                                          │
│  - 允许根据文案调整镜头角度和运动方式                           │
│  - 允许调整光影效果（光源方向、强度、色彩）                     │
│  - 允许调整材质表现（表面纹理、反射特性）                       │
│  - 保持环境构造的核心一致性                                     │
│                                                                │
│  继承记录：                                                      │
│  - 每个镜头继承环境构造（空间骨架、四层结构、材质、光影等）     │
│  - 每个镜头继承置信度和引擎输出摘要                             │
│  - 记录导演审核意见                                             │
│  - 标注与九宫格的对应关系                                       │
│  - 处理跨板连续性（动势组/蒙太奇组/长镜头）                     │
│  - 自动创建新板（当节拍需要跨板展开时）                         │
│                                                                │
│  【提示词写法】遵循 sequence-board-template.md 中的规范         │
│  【JSON输出】生成 sequence-board-data-{集数}.json（V5.0格式）    │
│    - version: "5.0"，包含metadata对象                           │
│    - expanded_shot包含dialogue数组（可选，无对话为空数组）     │
│    - original_grid包含完整environment对象                       │
│    - continuity_check包含dialogue_coherence                    │
└─────────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ 步骤7.5: 执行提示词精简 ← 【阶段C新增】                         │
│  - 读取 .claude/common/prompt-simplifier.md                             │
│  - 对每个镜头的提示词执行精简算法                               │
│  - 保留核心信息，移除冗余描述                                   │
│  - 确保精简后的提示词仍然符合质量标准                           │
│  - 目标：精简率15-20%，质量下降≤8%                             │
│  - 保护：P1元素100%，P2元素≥90%                                │
└─────────────────────────────────────────────────────────────────┘
<!-- LOG:STEP read=.claude/common/prompt-simplifier.md,algorithm=prompt_simplification,output=simplified_prompts -->
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ 步骤8: 执行连贯性检查 ← 【V4.0更新】                            │
│  - 读取 .claude/common/coherence-checker.md                             │
│  - 检查跨镜头连贯性（动势组/蒙太奇组/长镜头）                   │
│  - 检查轴线法律、视线匹配、动作连贯、光影一致                   │
│  - 【V4.0新增】处理跨板连续性（长节拍自动拆板）                 │
│  - 生成分板建议（当需要拆板时）                                 │
└─────────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ 步骤9: 生成 sequence-board-data-{集数}.json                     │
│  - 包含所有镜头的结构化数据                                     │
│  - 包含：boards数组、shots数组、continuity_check              │
│  - 【V4.0新增】包含策略标签和格子分配信息                       │
│  - 【V4.0新增】包含跨板连续性检查结果                           │
│  - 【V5.0新增】包含metadata对象、dialogue数组、完整environment  │
└─────────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ 步骤10: 生成 sequence-board-prompt-{集数}.md                    │
│  - 每板4格（或1-4格动态调整），每格1个镜头                      │
│  - 包含：画面描述、环境构造、镜头、风格标签、继承记录          │
│  - 【V4.0新增】包含策略标签和格子分配说明                       │
│  - 【V4.0新增】包含跨板连续性说明                               │
│  - 【V5.0新增】包含九宫格原画面、台词融入、四宫格位置标注      │
└─────────────────────────────────────────────────────────────────┘
```

**输出文件**：
- `outputs/sequence-board-data-{集数}.json` - 结构化数据（V5.0格式）
- `outputs/sequence-board-prompt-{集数}.md` - 分镜板提示词
<!-- LOG:STEP note=阶段C完成，总耗时约8-10秒 -->

---

## 异常处理

### 常见异常场景

| 场景 | 处理方案 | 相关文件 |
|------|---------|---------|
| **剧本格式错误** | 使用 .claude/common/exception-handler.md 进行格式修复 | exception-handler.md |
| **节拍识别失败** | 降级为人工标注，标记不确定性 | beat-analyzer.md |
| **关键帧选择失败** | 使用备选帧或导演介入 | keyframe-selector.md |
| **环境构造失败** | 使用默认环境模板 | environment-construction-guide/ |
| **布局计算冲突** | 调整复杂度评分重新计算 | layout-calculator.md |
| **连贯性检查失败** | 标记问题并生成分板建议 | coherence-checker.md |
| **导演审核未通过** | 返回修改流程，更新导演决策 | director-decision.md |

### 数据验证

使用 `.claude/common/data-validator.md` 验证所有输出数据：
- 格式正确性
- 字段完整性
- 数值范围合理性
- 引用一致性

## 引用关系

### 内部引用

```
film-storyboard-skill/
├── 引用 common/ 模块：
│   ├── beat-analyzer.md（节拍分析）
│   ├── keyframe-selector.md（关键帧选择）
│   ├── layout-calculator.md（布局计算）
│   ├── quality-check.md（质量检查）
│   ├── coherence-checker.md（连贯性检查）
│   ├── director-decision.md（导演参数）
│   ├── data-validator.md（数据验证）
│   └── exception-handler.md（异常处理）
│
├── 引用内部模块：
│   ├── creative-engines-integration/（创意引擎）
│   ├── environment-construction-guide/（环境构造）
│   └── templates/（输出模板）
│       ├── beat-breakdown-template.md
│       ├── beat-board-template.md
│       └── sequence-board-template.md
│
└── 被引用：
    └── animator-skill（引用 templates）
```

## 版本历史

- **V1.0**: 基础分镜生成流程
- **V2.0**: 添加环境构造系统
- **V3.0**: 添加多结构叙事模板、潜台词分析、类型化戏剧权重
- **V4.0**: 添加动态分镜板（支持可变格子数1-4格）、策略标签系统、跨板连续性
- **V5.0**: 【当前版本】四宫格继承九宫格并整合台词，添加metadata、完整environment、dialogue数组
