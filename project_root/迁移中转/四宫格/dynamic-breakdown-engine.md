# 动态拆解引擎 Dynamic Breakdown Engine

## Python Import Statements（V4.1 启用）

```python
# V4.1 动态拆解引擎依赖模块
# 注：以下模块在文档中定义逻辑，实际执行由 SKILL.md 调用
# - environment_asset_package: 环境资产包系统
# - visual_thickening_optimizer: 视觉增厚优化器
# - environment_injection_optimizer: 环境注入优化器
# - strategy_completion: 策略标签补全（已合并到本引擎）

# 策略标签体系（已合并自 strategy-completion.md）
STRATEGY_TAGS = {
    "core": ["[单镜]", "[动势组]", "[蒙太奇组]", "[长镜头]", "[环境]", "[特写]", "[全景]", "[中景]"],
    "motion": ["[推拉]", "[摇移]", "[跟拍]", "[升降]", "[旋转]", "[变焦]"],
    "emotion": ["[情感高潮]", "[情感过渡]", "[情感反差]", "[情感压抑]"],
    "time": ["[时间压缩]", "[时间扩展]", "[时间跳跃]", "[时间循环]"],
    "space": ["[空间对比]", "[空间转换]", "[空间嵌套]", "[空间扭曲]"],
    "narrative": ["[悬念建立]", "[信息揭露]", "[认知反转]", "[情感共鸣]"]
}
```

## 概述

**目的**：基于节拍拆解表的分级诊断信息，智能拆解节拍内容到多个分镜格子，支持跨板连续叙事。V4.1版本整合策略标签、环境资产包、视觉增厚优化等全部优化特性。

**输入数据**：节拍拆解表（包含V4.1优化字段：核心策略、复杂度评分、建议格子数、环境资产包ID、视觉增厚等级）
**输出数据**：动态分镜板（支持1-4可变格子数、跨板连续性、完整资产继承）

**V4.1核心改进**：
- ✅ 策略标签智能驱动格子分配
- ✅ 环境资产包自动匹配与继承
- ✅ 视觉增厚三层优化（高/中/低）
- ✅ 长节拍自动裂变（复杂度≥3.5）
- ✅ 跨板连续性智能检查
- ✅ 类型化权重修正集成

---

## 策略标签体系（V4.1 完整版）

> **注**：本章节已合并自 strategy-completion.md，包含完整的策略标签定义和映射规则。

### 核心策略标签

| 标签 | 描述 | 适用场景 | 格子数 | 复杂度阈值 |
|------|------|----------|--------|------------|
| `[单镜]` | 单一画面，完整表达 | 对话、静态情感、特写 | 1格 | <2.0 |
| `[动势组]` | 动作起止组合 | 追逐、移动、简单动作 | 2格 | 2.0-3.5 |
| `[蒙太奇组]` | 三段式叙事 | 时间压缩、情绪渲染、复杂转折 | 3格 | 3.5-5.0 |
| `[长镜头]` | 连续动作调度 | 复杂动作、环境展示 | 1-3格 | ≥III级 |
| `[环境]` | 环境空间展示 | 场景建立、氛围渲染 | 1-2格 | <2.5 |
| `[特写]` | 细节聚焦 | 表情、物品、情感表达 | 1格 | - |
| `[全景]` | 完整场景展示 | 空间定位、群体场景 | 1格 | - |
| `[中景]` | 角色环境关系 | 对话、互动、动作展示 | 1-2格 | - |

### 镜头运动标签

| 标签 | 描述 | 适用策略 | 运动特点 |
|------|------|----------|----------|
| `[推拉]` | 镜头推进或拉远 | `[特写]`, `[单镜]` | 焦点转移，情绪强调 |
| `[摇移]` | 水平或垂直移动 | `[全景]`, `[环境]` | 空间探索，跟随动作 |
| `[跟拍]` | 跟随角色移动 | `[动势组]`, `[长镜头]` | 沉浸感，主观视角 |
| `[升降]` | 垂直升降运动 | `[环境]`, `[全景]` | 视角变化，场景展示 |
| `[旋转]` | 镜头旋转 | `[蒙太奇组]` | 眩晕感，情绪转折 |
| `[变焦]` | 焦距变化 | `[特写]` | 注意力引导 |

### V4.1 扩展策略标签

#### 情感表达标签
| 标签 | 描述 | 适用场景 | 视觉特征 |
|------|------|----------|----------|
| `[情感高潮]` | 强烈情绪爆发 | 告白、决裂、重大发现 | 面部特写，强烈光影 |
| `[情感过渡]` | 情绪渐变过程 | 心理变化，态度转变 | 色彩渐变，镜头运动 |
| `[情感反差]` | 情绪强烈对比 | 惊喜、惊吓、反转 | 快速剪辑，对比构图 |
| `[情感压抑]` | 情绪内敛克制 | 隐忍、沉思、等待 | 低调光影，静态构图 |

#### 时间处理标签
| 标签 | 描述 | 适用场景 | 处理方式 |
|------|------|----------|----------|
| `[时间压缩]` | 长时间段压缩 | 成长、等待、旅行 | 蒙太奇，象征符号 |
| `[时间扩展]` | 瞬间时间扩展 | 关键时刻、决策瞬间 | 慢动作，多角度 |
| `[时间跳跃]` | 时间点跳跃 | 闪回、预演、转场 | 硬切，过渡效果 |
| `[时间循环]` | 时间循环重复 | 梦境、回忆、轮回 | 重复元素，循环结构 |

#### 空间关系标签
| 标签 | 描述 | 适用场景 | 构图特点 |
|------|------|----------|----------|
| `[空间对比]` | 空间大小对比 | 压迫感、自由感 | 大小对比，透视夸张 |
| `[空间转换]` | 空间场景转换 | 转场、梦境切换 | 匹配剪辑，过渡效果 |
| `[空间嵌套]` | 空间套空间 | 回忆中的回忆 | 画中画，多层构图 |
| `[空间扭曲]` | 空间变形扭曲 | 梦境、幻觉、超现实 | 变形透视，非常规构图 |

#### 叙事功能标签
| 标签 | 描述 | 适用场景 | 叙事作用 |
|------|------|----------|----------|
| `[悬念建立]` | 建立悬念期待 | 开场、转折前 | 信息隐藏，视角限制 |
| `[信息揭露]` | 关键信息揭露 | 真相大白，发现秘密 | 焦点转移，信息释放 |
| `[认知反转]` | 认知根本改变 | 身份揭露，真相反转 | 视角切换，信息重组 |
| `[情感共鸣]` | 建立情感连接 | 感人时刻，共情场景 | 主观视角，情感渲染 |

### 场景到策略映射表

#### 对话场景策略
| 场景类型 | 首选策略 | 备选策略 | 镜头建议 |
|----------|----------|----------|----------|
| 重要对话 | `[单镜]` + `[特写]` | `[中景]` | `[推拉]` 强调重点 |
| 激烈争论 | `[动势组]` + `[特写]` | `[蒙太奇组]` | `[摇移]` 跟随情绪 |
| 温情对话 | `[单镜]` + `[情感过渡]` | `[中景]` | 柔和 `[推拉]` |
| 信息揭露 | `[单镜]` + `[信息揭露]` | `[特写]` | `[推拉]` + 停顿 |

#### 动作场景策略
| 场景类型 | 首选策略 | 备选策略 | 镜头建议 |
|----------|----------|----------|----------|
| 快速追逐 | `[动势组]` + `[跟拍]` | `[长镜头]` | 快速 `[摇移]` |
| 激烈打斗 | `[蒙太奇组]` + `[特写]` | `[长镜头]` | `[旋转]` + `[变焦]` |
| 优雅动作 | `[长镜头]` + `[升降]` | `[动势组]` | 流畅 `[跟拍]` |
| 惊险逃脱 | `[蒙太奇组]` + `[时间扩展]` | `[动势组]` | `[推拉]` + 慢动作 |

#### 情感场景策略
| 场景类型 | 首选策略 | 备选策略 | 镜头建议 |
|----------|----------|----------|----------|
| 情感高潮 | `[单镜]` + `[情感高潮]` | `[特写]` | 强烈 `[推拉]` |
| 情感压抑 | `[单镜]` + `[情感压抑]` | `[中景]` | 静态构图 |
| 情感转折 | `[蒙太奇组]` + `[情感过渡]` | `[动势组]` | `[推拉]` 过渡 |
| 情感反差 | `[蒙太奇组]` + `[情感反差]` | `[时间跳跃]` | 快速剪辑 |

#### 环境场景策略
| 场景类型 | 首选策略 | 备选策略 | 镜头建议 |
|----------|----------|----------|----------|
| 场景建立 | `[环境]` + `[全景]` | `[单镜]` | `[摇移]` 展示 |
| 氛围渲染 | `[环境]` + `[情感过渡]` | `[特写]` | 柔和光影 |
| 空间转换 | `[空间转换]` + `[时间跳跃]` | `[蒙太奇组]` | 匹配剪辑 |

---

## 输入数据结构

### 节拍数据（V4.1完整版）
```json
{
  "beat_number": 7,
  "scene_description": "包子猪听到\"给它吃\"瞬间变脸，熟练地系上餐巾",
  "core_strategy": "[蒙太奇组:变脸]",
  "auxiliary_info": "[内含:惊恐静止→突然变脸→期待敲盘]",
  "key_points": [
    {"类型": "Setup", "内容": "惊恐表情"},
    {"类型": "Action", "内容": "变脸过程"},
    {"类型": "Resolution", "内容": "期待敲盘"}
  ],
  "complexity_score": 4.7,
  "suggested_grid_count": 4,
  "breakdown_suggestion": "建议拆为4格：惊恐定格→变脸关键帧→系餐巾→敲盘音效",
  "beat_type": "情绪转折",
  "performance_weight": 2.2,
  "narrative_function": "中点升级/认知反转",
  "base_weight": 1.6,
  "final_weight": 3.52,
  "keyframe_level": "🔴 特级",
  "environment_asset_package_id": "asset_pkg_scene_07",
  "visual_thickening_level": "high",
  "emotion_tags": ["惊恐", "期待", "滑稽"],
  "motion_tags": ["推拉", "快速切换"],
  "type_coefficient": 1.3,
  "strategy_tags": ["[蒙太奇组]", "[特写]", "[推拉]"]
}
```

---

## 拆解算法

### 基础框架（基于核心策略）【V4.1优化】

| 核心策略 | 基础格子数 | 拆解逻辑 | 适用场景 | 复杂度阈值 |
|----------|----------|----------|----------|------------|
| `[单镜]` | 1格 | 直接选择最具表现力的单一画面 | 对话、静态情感、特写镜头 | 复杂度 < 2.0 |
| `[动势组]` | 2格 | 分为起幅（动作开始）+ 落幅（动作结束） | 追逐、移动、快速动作、简单转折 | 2.0 ≤ 复杂度 < 3.5 |
| `[蒙太奇组]` | 3格 | 分为Setup（起势）→Action（动作）→Resolution（结果） | 时间压缩、情绪渲染、空间跳跃、复杂转折 | 3.5 ≤ 复杂度 < 5.0 |
| `[长镜头]` | 1-3格 | 选取关键姿势，通过镜头运动标注完整轨迹 | 连续动作、复杂调度、环境展示 | 复杂度 ≥ III级 |
| `[环境]` | 1-2格 | 展示环境空间、氛围渲染、场景建立 | 场景介绍、氛围营造、空间展示 | 复杂度 < 2.5 |
| `[特写]` | 1格 | 聚焦细节、表情、关键物品 | 情感表达、细节强调、物品特写 | 复杂度 < - |
| `[全景]` | 1格 | 展示完整场景、空间关系 | 场景建立、空间定位、群体展示 | 复杂度 < - |
| `[中景]` | 1-2格 | 展示角色与环境关系 | 对话场景、动作展示、互动关系 | 复杂度 < - |
 
### 策略映射（Phase 4新增）

#### [正反打]策略（2格逻辑）

| 核心策略 | 基础格子数 | 拆解逻辑 | 适用场景 | 复杂度阈值 |
|----------|----------|----------|----------|------------|
| `[正反打]` | 2格 | 格1: A角特写 + 台词/表情<br>格2: B角反应镜头 + 环境资产继承 | 对话场景、冲突对话 | 复杂度 < 3.0 |

**轴线规则**：确保视线匹配
- 格1和格2的角色视线方向必须对应
- 镜头位置应在180度线同一侧
- 避免跳轴

**示例**：
```
格1（A角特写）：鲁达面部特写，眼神犀利，说出威胁台词
格2（B角反应）：镇关西反应镜头，面部表情变化，背景环境继承
```

#### [感官锚点]策略（1格插入规则）

| 核心策略 | 基础格子数 | 拆解逻辑 | 适用场景 | 复杂度阈值 |
|----------|----------|----------|----------|------------|
| `[感官锚点]` | 1格 | 插入规则：在节拍的情感/动作顶点后插入<br>内容: 特写镜头 + 通感视觉化方案 | 感官刺激、通感转化 | 复杂度 < - |

**插入位置规则**：
- 在节拍的情感顶点后插入
- 在节拍的动作顶点后插入
- 不打断主要叙事流程

**示例**：
- "玻璃碎裂的特写，裂痕中映射出角色的倒影"
- "火焰爆发的瞬间，光影中展现内心的愤怒"

---

### JSON alternative_frames 读取与展开逻辑 ← 【V4.1新增】

#### 数据源

**唯一数据源：JSON alternative_frames**

- **文件**：`outputs/beat-board-full-list-{集数}.json`
- **字段**：`grids[].alternative_frames`
- **包含**：type（类型）、role（角色）、action（动作）、reason（原因）、drama_tension_score（戏剧张力评分）

**不使用箭头格式兼容层**：迭代阶段，重新从头运行，唯一依赖JSON机器可读数据

---

#### 核心算法（精简版）

```python
def expand_from_alternative_frames(grid_data, strategy_tag):
    """
    根据策略标签和JSON alternative_frames展开为多镜头

    返回：shots列表
    """
    # 1. 提取数据
    grid_id = grid_data["grid_id"]
    scene_description = grid_data["scene_description"]
    alternative_frames = grid_data["alternative_frames"]

    # 2. 根据策略标签确定基础格子数
    base_grids = get_base_grids(strategy_tag)

    # 3. 生成主镜头（九宫格选中帧）
    primary_shot = {
        "shot_id": None,
        "shot_type": get_shot_type(strategy_tag, "primary"),
        "visual_description": scene_description,
        "alternative_frame_source": {
            "grid_id": grid_id,
            "frame_type": "primary",
            "inherited_from": "JSON.primary_frame"
        }
    }

    # 4. 生成替代镜头（从JSON读取）
    alternative_shots = []
    for alt_frame in alternative_frames:
        alt_shot = {
            "shot_id": None,
            "shot_type": get_shot_type(strategy_tag, alt_frame["frame_type"]),
            "visual_description": generate_description(primary_shot, alt_frame),
            "alternative_frame_source": {
                "grid_id": grid_id,
                "frame_type": alt_frame["frame_type"],
                "role": alt_frame.get("role"),
                "action": alt_frame["action"],
                "drama_tension_score": alt_frame.get("drama_tension_score"),
                "reason": alt_frame["reason"],
                "inherited_from": "JSON.alternative_frames"
            }
        }
        alternative_shots.append(alt_shot)

    # 5. 排序（按动作时间顺序）
    all_shots = [primary_shot] + alternative_shots
    sorted_shots = sort_shots(all_shots, strategy_tag)

    return sorted_shots


def get_base_grids(strategy_tag):
    """根据策略标签返回基础格子数"""
    mapping = {
        "[单镜]": 1,
        "[动势组]": 2,
        "[蒙太奇组]": 3,
        "[长镜头]": 1,
        "[正反打]": 2,
        "[环境]": 1,
        "[特写]": 1,
        "[全景]": 1,
        "[中景]": 1
    }
    return mapping.get(strategy_tag, 1)


def get_shot_type(strategy_tag, frame_type):
    """确定镜头景别"""
    if strategy_tag == "[正反打]":
        return "特写"
    elif strategy_tag == "[动势组]" and "起势" in (frame_type or ""):
        return "跟拍"
    else:
        return "中景"


def generate_description(primary_shot, alt_frame):
    """生成替代镜头视觉描述"""
    role = alt_frame.get("role", "")
    action = alt_frame["action"]

    if role:
        return f"镜头聚焦在{role}的面部，{action}。"
    else:
        return f"{action}。"


def sort_shots(shots, strategy_tag):
    """按动作时间顺序排序镜头"""
    if strategy_tag == "[动势组]":
        # 起势在前，落幅在后
        return sorted(shots, key=lambda x: 0 if "起势" in (x.get("alternative_frame_source", {}).get("action", "")) else 1)
    elif strategy_tag == "[蒙太奇组]":
        # 起势→高潮→余韵
        order = {"起势": 0, "高潮": 1, "余韵": 2}
        return sorted(shots, key=lambda x: order.get(x.get("alternative_frame_source", {}).get("action", ""), 99))
    else:
        return shots
```

---

#### 策略映射表（展开规则）

| 策略标签 | 基础格子数 | 展开规则 |
|---------|-----------|---------|
| [单镜] | 1格 | single_shot |
| [动势组] | 2格 | two_shot_setup_resolution |
| [蒙太奇组] | 3格 | three_shot_setup_action_resolution |
| [长镜头] | 1格 | variable_shot_dynamic |
| [正反打] | 2格 | two_shot_ab |
| [环境] | 1格 | single_shot |
| [特写] | 1格 | single_shot |
| [全景] | 1格 | single_shot |
| [中景] | 1格 | single_shot |
| [感官锚点] | 1格 | insert_shot |

---

#### 使用示例

**输入：**
```
grid_id = 2
strategy_tag = "[正反打]"
JSON alternative_frames = [
  {"frame_type": "secondary", "role": "镇关西", "action": "正反打A角", "reason": "视觉冲击权重低"},
  {"frame_type": "tertiary", "role": "鲁达", "action": "正反打B角", "reason": "情绪转折点"}
]
```

**输出：**
```python
shots = [
  {"shot_type": "特写", "visual_description": "镇关西特写...", "alternative_frame_source": {...}},
  {"shot_type": "特写", "visual_description": "鲁达特写...", "alternative_frame_source": {...}}
]
```

---

#### 策略优先级调整（Phase 4新增）

当`[感官锚点]`与其他策略冲突时，优先保证锚点的插入：

| 策略标签 | 优先级 | 冲突处理 |
|----------|--------|----------|
| `[感官锚点]` | 高 | 优先执行，其他策略降级处理 |
| `[单镜]` | 中 | 与`[感官锚点]`冲突时，降级为副格 |
| `[动势组]` | 中 | 与`[感官锚点]`冲突时，插入锚点后调整为2格 |
| `[蒙太奇组]` | 中 | 与`[感官锚点]`冲突时，插入锚点后调整为3格 |
| `[长镜头]` | 中 | 与`[感官锚点]`冲突时，插入锚点后继续长镜头 |
| 其他策略 | 中 | 服从`[感官锚点]`的优先级 |

**冲突处理流程**：
```
检测到`[感官锚点]` → 检查是否有其他策略冲突
  ↓
有冲突？→ 优先执行`[感官锚点]`插入规则
  ↓
调整其他策略的格子数 → 继续正常流程
```

### 镜头运动策略标签【V4.1新增】

| 运动策略 | 适用场景 | 格子数 | 描述 |
|----------|----------|--------|------|
| `[推拉]` | 情绪强调、焦点转移 | 1-2格 | 镜头推进或拉远，强调细节或展示环境 |
| `[摇移]` | 空间探索、跟随动作 | - | 镜头水平或垂直移动，展示空间或跟随角色 |
| `[跟拍]` | 动作跟随、主观视角 | - | 镜头跟随角色移动，创造沉浸感 |
| `[升降]` | 场景展示、视角变化 | - | 镜头垂直升降，展示垂直空间关系 |

### 策略选择算法【V4.1优化】

**自动策略选择规则**：
1. **基于复杂度**：
   - 复杂度 < 2.0 → `[单镜]` 或 `[环境]`
   - 2.0 ≤ 复杂度 < 3.5 → `[动势组]` 或 `[蒙太奇组]`
   - 复杂度 ≥ 3.5 → `[蒙太奇组]` 或 `[长镜头]`

2. **基于内容类型**：
   - 对话场景 → `[单镜]` 或 `[中景]`
   - 动作场景 → `[动势组]` 或 `[蒙太奇组]`
   - 环境展示 → `[环境]` 或 `[全景]`
   - 情感表达 → `[特写]` 或 `[单镜]`

3. **基于关键点数量**：
   - 1个关键点 → `[单镜]`
   - 2个关键点 → `[动势组]`
   - 3+个关键点 → `[蒙太奇组]`

### 复杂度调整算法【V4.1优化】

**公式**：
```
调整后格子数 = 基础格子数 + 复杂度调整值 + 关键点调整值

其中：
1. 基础格子数 = 根据核心策略确定（见策略选择算法）
2. 复杂度调整值 = 
   - 复杂度 < 2.0: 0
   - 2.0 ≤ 复杂度 < 3.5: 1
   - 复杂度 ≥ 3.5: 2
3. 关键点调整值 = min(关键点数量 - 基础格子数, 2)

限制条件：
- 调整后格子数 ≤ 4（单板最大格子数）
- 调整后格子数 ≥ 基础格子数
- 策略特定限制：
  - `[单镜]` 最多1格
  - `[动势组]` 最多2格
  - `[蒙太奇组]` 最多3格
  - `[长镜头]` 最多3格
  - `[环境]` 最多2格
  - 其他策略：最多2格

**V4.1优化逻辑**：
1. 长节拍自动拆分：复杂度 ≥ 3.5 且关键点 ≥ 4 → 自动拆分为2个分镜板
2. 策略升级：当复杂度超过阈值时，自动升级策略（如 `[单镜]` → `[动势组]`）
3. 镜头运动集成：根据策略自动添加镜头运动标签
```

### 关键点映射规则

**规则表**：

| 关键点类型 | 优先级 | 映射逻辑 | 占用格子 |
|-------------|--------|----------|----------|
| `Setup` | 最高 | 起势部分，建立情境 | 动势组第1格 / 蒙太奇组第1格 |
| `Action` | 高 | 核心动作或转折点 | 动势组第2格 / 蒙太奇组第2格 |
| `Resolution` | 高 | 动作结果或情绪余波 | 动势组第2格 / 蒙太奇组第3格 |
| `动作开始` | 中 | 动作的起始姿势 | 动势组第1格 / 长镜头关键节点 |
| `动作结束` | 中 | 动作的完成姿态 | 动势组第2格 / 长镜头关键节点 |
| `动作高潮` | 高 | 动作的顶点 | 长镜头关键节点 |
| `情绪转折` | 高 | 情绪变化的转折点 | 长镜头关键节点 |
| `对话重点` | 中 | 重要台词的表达时刻 | 单镜或动势组的格子 |

**映射示例**：
```
关键点：[
  {"类型": "Setup", "内容": "惊恐表情"},
  {"类型": "Action", "内容": "变脸过程"},
  {"类型": "Resolution", "内容": "期待敲盘"}
]
核心策略：[蒙太奇组:变脸]
分配结果：
  格1（Setup）: 惊恐表情定格
  格2（Action）: 变脸过程关键帧
  格3（Resolution）: 期待敲盘
```

### 辅助信息处理规则

**辅助信息类型**：
1. **转折信息**：`[内含:XX→YY]` → 标记转折点
2. **时间变化**：`[内含:XX秒→YY秒]` → 时间跳跃标记
3. **情绪变化**：`[内含:XX情绪→YY情绪]` → 情绪变化标记

**处理方式**：
- 转折信息 → 在转折点前后添加过渡描述
- 时间变化 → 在时间跳跃处添加时间标注
- 情绪变化 → 在情绪变化处添加情绪曲线标注

---

## 节点分配算法

### Step 1: 确定总格子数

```python
def calculate_total_grids(beat_data, max_grids_per_board=4):
    """
    计算节拍所需的总格子数
    
    参数:
        beat_data: 节拍数据
        max_grids_per_board: 单板最大格子数（默认4）
    
    返回:
        total_grids: 总格子数
        recommended_board_count: 建议板数
    """
    
    # 基础格子数
    base_grids = {
        "[单镜]": 1,
        "[动势组]": 2,
        "[蒙太奇组]": 3,
        "[长镜头]": 2  # 默认2格，根据关键点数量调整
    }
    
    strategy = beat_data.core_strategy
    
    # 提取策略类型（去掉方括号内的描述）
    import re
    strategy_type = re.match(r'\[(\w+)\]', strategy).group(1)
    
    base_count = base_grids.get(strategy_type, 1)
    
    # 复杂度调整
    extra_grids = max(0, round(beat_data.complexity_score - 2.5))
    
    total_grids = min(base_count + extra_grids, 4)
    
    # 计算建议板数
    recommended_board_count = ceil(total_grids / max_grids_per_board)
    
    return total_grids, recommended_board_count
```

### Step 2: 分配格子到板

```python
def allocate_grids_to_boards(total_grids, max_grids_per_board=4):
    """
    将格子分配到具体的板中
    
    参数:
        total_grids: 总格子数
        max_grids_per_board: 单板最大格子数（默认4）
    
    返回:
        board_allocations: [
            {
                "board_number": 1,
                "grid_count": 4,
                "beat_ranges": [(beat_7, 0, 3)]  # (节拍编号, 起始格子, 结束格子)
            },
            ...
        ]
    """
    
    board_allocations = []
    current_board = 1
    current_grid = 0
    
    beat_number = beat_data.beat_number
    allocated_grids = 0
    
    while allocated_grids < total_grids:
        # 计算当前板可用的格子数
        available_grids = min(max_grids_per_board - current_grid, total_grids - allocated_grids)
        
        if available_grids > 0:
            board_allocations.append({
                "board_number": current_board,
                "grid_count": available_grids,
                "beat_ranges": [(beat_number, current_grid, current_grid + available_grids - 1)],
                "start_grid": current_grid,
                "end_grid": current_grid + available_grids - 1,
                "is_continuation": allocated_grids > 0  # 是否为前一板的延续
            })
            
            allocated_grids += available_grids
            current_grid += available_grids
            current_board += 1
    
    return board_allocations
```

---

## V4.1裂变算法核心流程

### 概述

V4.1裂变算法是动态拆解引擎的核心升级，整合策略标签、环境资产包、视觉增厚优化等全部V4.1特性，实现智能、连贯、高质量的节拍裂变。

**核心特性**：
1. **策略驱动裂变**：根据策略标签智能分配格子数（1-4格）
2. **资产包集成**：自动匹配和继承环境资产包
3. **视觉增厚优化**：三层增厚等级（高/中/低）自动应用
4. **长节拍裂变**：复杂度≥3.5自动拆分为多板
5. **跨板连续性**：智能检查并标记连续性

### V4.1裂变流程图

```
输入：节拍数据（含V4.1字段）
    │
    ▼
┌─────────────────────────────────────────┐
│ Step 1: 读取V4.1诊断信息                │
│ - 核心策略（含策略标签）                │
│ - 复杂度评分                            │
│ - 建议格子数                            │
│ - 环境资产包ID                          │
│ - 视觉增厚等级                          │
│ - 情绪标签、运动标签                    │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│ Step 2: 策略标签解析                    │
│ - 提取核心策略类型                      │
│ - 提取镜头运动策略                      │
│ - 提取景别策略                          │
│ - 确定基础格子数                        │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│ Step 3: 资产包匹配与加载                │
│ - 根据asset_package_id加载资产包        │
│ - 提取空间骨架、材质、光影、动态信息    │
│ - 计算继承优先级分数                    │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│ Step 4: 视觉增厚优化                    │
│ - 根据thickening_level确定增厚强度      │
│ - 应用视觉增厚算法                      │
│ - 生成增厚后的画面描述                  │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│ Step 5: 复杂度驱动的格子调整            │
│ - 基础格子数 + 复杂度调整值             │
│ - 应用类型系数修正                      │
│ - 确定最终格子数（1-4）                 │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│ Step 6: 长节拍裂变判断                  │
│ - 检查复杂度≥3.5且关键点≥4             │
│ - 决定是否需要拆分为多板                │
│ - 标记跨板连续性                        │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│ Step 7: 内容分配到格子                  │
│ - 关键点映射到格子                      │
│ - 应用镜头运动标签                      │
│ - 注入环境资产信息                      │
└────────────┬────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│ Step 7.5: 环境资产包注入（Phase 4新增） │
│ - 读取九宫格对应格的[环境资产包]       │
│ - 拆解为可继承的模块                  │
│ - 在镜头卡片中标注继承关系              │
└────────────┬────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│ Step 8: 跨板连续性检查                  │
│ - 视觉连续性                            │
│ - 时间连续性                            │
│ - 角色状态连续性                        │
│ - 情绪曲线连续性                        │
└────────────┬────────────────────────────┘
             │
             ▼
输出：V4.1裂变结果（含完整资产继承信息）
```

### V4.1字段处理规则

#### 环境资产包ID处理

**加载逻辑**：
    ```python
    def load_environment_asset_package(asset_package_id, beat_context):
        """
        加载环境资产包（Phase 2.1 修复 - 使用正确的 import）
        
        参数:
            asset_package_id: 资产包ID
            beat_context: 节拍上下文（场景、时间、情绪等）
        
        返回:
            asset_package: 完整的资产包数据
            inheritance_score: 继承优先级分数（0-100）
        """
        # 使用 import 的函数从环境资产包系统加载
        asset_package = load_asset_package(asset_package_id)
        
        # 使用 import 的函数计算继承优先级
        inheritance_score = calculate_inheritance_priority(
            asset_package, beat_context
        )
        
        return asset_package, inheritance_score
    ```

**继承优先级计算**：
- 场景匹配度：40分
- 时间连续性：30分
- 情绪一致性：20分
- 角色连贯性：10分

#### 视觉增厚等级处理

**增厚应用逻辑**：
    ```python
    def apply_visual_thickening(scene_description, thickening_level, asset_package):
        """
        应用视觉增厚优化（Phase 2.1 修复 - 使用正确的 import）
        
        参数:
            scene_description: 原始场景描述
            thickening_level: 增厚等级（high/medium/low）
            asset_package: 环境资产包
        
        返回:
            thickened_description: 增厚后的描述
            thickening_applied: 应用的增厚元素列表
        """
        # 根据等级选择增厚强度
        intensity_config = {
            "high": {"density_multiplier": 1.8, "detail_level": "maximum"},
            "medium": {"density_multiplier": 1.4, "detail_level": "enhanced"},
            "low": {"density_multiplier": 1.2, "detail_level": "standard"}
        }
        
        config = intensity_config.get(thickening_level, intensity_config["medium"])
        
        # 使用 import 的函数应用视觉增厚优化器
        thickened_description = apply_visual_thickening_v4_1(
            scene_description,
            config,
            asset_package
        )
        
        return thickened_description
    ```
 
#### 环境资产包注入（Phase 4新增）

**注入时机**：在Step 7内容分配到格子时，强制注入环境资产

**注入步骤**：
1. 读取九宫格对应格的[环境资产包]
   - 读取来源：`outputs/beat-board-prompt-{集数}.md`
   - 读取字段：空间骨架、材质皮肤、光影系统、动态生命、视觉基调DNA

2. 将资产包的4个要素拆解为可继承的模块：
   - **强制继承**：空间骨架、光影系统
   - **可选继承**：材质皮肤（如无特殊变化）
   - **动态调整**：动态生命（根据新镜头的动作调整）

3. 在镜头卡片中显式标注继承关系：
   ```markdown
   [环境构造] 继承自Board{板号}格{格子号}: 
   - 空间骨架摘要: {从父格继承的空间骨架}
   - 光影系统摘要: {从父格继承的光影系统}
   - 材质皮肤: {继承或调整后的材质}
   - 动态生命: {根据新镜头动作调整后的动态元素}
   ```

4. 继承规则：
   - **单镜裂变**：完全继承环境资产包
   - **动势组裂变**：继承环境资产包，但动态生命根据动作调整
   - **蒙太奇组裂变**：继承环境资产包，但光影系统根据情绪调整
   - **长镜头裂变**：继承环境资产包，但空间骨架根据角色位置更新

**实现逻辑**：
    ```python
    def inject_environment_asset_package(beat_board_grid, sequence_card, strategy_type):
        """
        注入环境资产包到四宫格卡片（Phase 4新增）
        
        参数:
            beat_board_grid: 九宫格对应格的数据
            sequence_card: 四宫格卡片数据
            strategy_type: 策略类型（单镜/动势组/蒙太奇组/长镜头）
        
        返回:
            sequence_card_with_asset: 包含环境资产继承信息的四宫格卡片
        """
        # 读取环境资产包
        asset_package = beat_board_grid.get('环境资产包', {})
        
        # 根据策略类型确定继承规则
        inheritance_rules = {
            '[单镜]': {
                '空间骨架': '完全继承',
                '材质皮肤': '完全继承',
                '光影系统': '完全继承',
                '动态生命': '完全继承'
            },
            '[动势组]': {
                '空间骨架': '完全继承',
                '材质皮肤': '完全继承',
                '光影系统': '完全继承',
                '动态生命': '动态调整'
            },
            '[蒙太奇组]': {
                '空间骨架': '完全继承',
                '材质皮肤': '可选继承',
                '光影系统': '情绪调整',
                '动态生命': '可选继承'
            },
            '[长镜头]': {
                '空间骨架': '位置更新',
                '材质皮肤': '可选继承',
                '光影系统': '完全继承',
                '动态生命': '可选继承'
            }
        }
        
        rules = inheritance_rules.get(strategy_type, {})
        
        # 应用继承规则
        inherited_asset = {}
        for key, rule in rules.items():
            if rule == '完全继承':
                inherited_asset[key] = asset_package.get(key, '')
            elif rule == '可选继承':
                inherited_asset[key] = asset_package.get(key, '') if '特殊' not in sequence_card.get('画面描述', '') else ''
            elif rule == '动态调整':
                inherited_asset[key] = adjust_for_motion(asset_package.get(key, ''), sequence_card.get('画面描述', ''))
            elif rule == '情绪调整':
                inherited_asset[key] = adjust_for_emotion(asset_package.get(key, ''), sequence_card.get('情绪', ''))
            elif rule == '位置更新':
                inherited_asset[key] = update_for_position(asset_package.get(key, ''), sequence_card.get('角色位置', ''))
        
        # 添加继承关系标注
        sequence_card['环境构造'] = {
            '继承关系': f"继承自Board{beat_board_grid['板号']}格{beat_board_grid['格子号']}",
            '空间骨架摘要': inherited_asset.get('空间骨架', ''),
            '光影系统摘要': inherited_asset.get('光影系统', ''),
            '材质皮肤': inherited_asset.get('材质皮肤', ''),
            '动态生命': inherited_asset.get('动态生命', '')
        }
        
        return sequence_card
    ```
  
#### 父子裂变算法（Phase 4新增）

**算法目标**：基于九宫格父画面的环境资产包，生成四宫格子镜头卡片

**输入数据**：
- 九宫格父画面（含环境资产包）
- 节拍拆解的[关键信息点]
- 策略标签类型

**处理逻辑**：

1. **单镜裂变**：
   - 保持1格，但镜头角度/景深可以微调
   - 继承父画面的完整环境资产包
   - 画面描述：基于父画面的五维扩写
   - 摄影参数：根据策略标签指定镜头类型
   - 输出：1个子镜头卡片

   **示例**：
   ```python
   def single_shot_fission(parent_grid, key_points):
       """
       单镜裂变算法
       """
       # 完全继承环境资产包
       inherited_asset = parent_grid['环境资产包']
       
       # 生成子镜头卡片
       sequence_card = {
           '镜头序号': 1,
           '继承关系': f"继承自Board{parent_grid['板号']}格{parent_grid['格子号']}",
           '环境构造': inherited_asset,
           '摄影参数': {
               '镜头': parent_grid.get('镜头', '中景'),
               '运动': parent_grid.get('运动', '固定'),
               '角度': parent_grid.get('角度', '平视')
           },
           '画面叙事': parent_grid['画面描述']  # 基于父画面的五维扩写
       }
       
       return [sequence_card]
   ```

2. **动势组裂变**：
   - **格1**：继承父画面的起势状态 + 环境资产
   - **格2**：基于[关键信息点]生成落幅画面
   - **运动连续性**：两格间必须描述运动连续性
   - 环境继承：两格都继承父画面的环境资产包，但动态生命根据动作调整
   - 摄影参数：格1和格2使用相同的镜头运动（如摇移）
   - 输出：2个子镜头卡片

   **示例**：
   ```python
   def action_fission(parent_grid, key_points):
       """
       动势组裂变算法
       """
       # 继承环境资产包
       inherited_asset = parent_grid['环境资产包'].copy()
       
       # 格1：起势
       card1 = {
           '镜头序号': 1,
           '继承关系': f"继承自Board{parent_grid['板号']}格{parent_grid['格子号']}（起势）",
           '环境构造': inherited_asset,
           '摄影参数': {
               '镜头': '中景',
               '运动': '摇移开始',
               '角度': '平视'
           },
           '画面叙事': f"{parent_grid['画面描述']} - 动作开始"
       }
       
       # 格2：落幅（基于关键信息点）
       if len(key_points) >= 2:
           resolution_point = key_points[1]
       else:
           resolution_point = '动作完成'
       
       # 动态调整
       inherited_asset['动态生命'] = adjust_for_motion(
           inherited_asset['动态生命'],
           '动作完成'
       )
       
       card2 = {
           '镜头序号': 2,
           '继承关系': f"继承自Board{parent_grid['板号']}格{parent_grid['格子号']}（落幅）",
           '环境构造': inherited_asset,
           '摄影参数': {
               '镜头': '中景',
               '运动': '摇移结束',
               '角度': '平视'
           },
           '画面叙事': f"{resolution_point} - {inherited_asset['空间骨架']}",
           '运动连续性': '格1到格2保持连续的镜头运动轨迹'
       }
       
       return [card1, card2]
   ```

3. **蒙太奇组裂变**：
   - **格1（Setup）**：从环境资产包提取氛围，建立场景
   - **格2（Action）**：父画面的高潮帧，包含核心转折
   - **格3（Resolution）**：情绪回落，环境资产微调（如光影变暗）
   - **情绪曲线**：Setup→Action→Resolution的情绪递进
   - **环境继承**：
     - 格1：完全继承环境资产包
     - 格2：继承但动态调整
     - 格3：继承但微调光影
   - **摄影参数**：每格使用不同的镜头运动
   - 输出：3个子镜头卡片

   **示例**：
   ```python
   def montage_fission(parent_grid, key_points):
       """
       蒙太奇组裂变算法
       """
       cards = []
       
       # 格1：Setup
       asset1 = parent_grid['环境资产包'].copy()
       card1 = {
           '镜头序号': 1,
           '继承关系': f"继承自Board{parent_grid['板号']}格{parent_grid['格子号']}（Setup）",
           '环境构造': asset1,
           '摄影参数': {
               '镜头': '全景',
               '运动': '固定',
               '角度': '俯视'
           },
           '画面叙事': f"{asset1['空间骨架']} - 场景建立"
       }
       cards.append(card1)
       
       # 格2：Action（高潮帧）
       asset2 = parent_grid['环境资产包'].copy()
       asset2['动态生命'] = adjust_for_motion(
           asset2['动态生命'],
           '高潮帧'
       )
       
       card2 = {
           '镜头序号': 2,
           '继承关系': f"继承自Board{parent_grid['板号']}格{parent_grid['格子号']}（Action）",
           '环境构造': asset2,
           '摄影参数': {
               '镜头': '特写',
               '运动': '急推',
               '角度': '平视'
           },
           '画面叙事': f"{key_points[1]['内容'] if len(key_points) > 1 else '高潮'} - {parent_grid['画面描述']}"
       }
       cards.append(card2)
       
       # 格3：Resolution（情绪回落）
       asset3 = parent_grid['环境资产包'].copy()
       # 光影微调
       asset3['光影系统'] = adjust_for_emotion(
           asset3['光影系统'],
           '情绪回落'
       )
       
       card3 = {
           '镜头序号': 3,
           '继承关系': f"继承自Board{parent_grid['板号']}格{parent_grid['格子号']}（Resolution）",
           '环境构造': asset3,
           '摄影参数': {
               '镜头': '中景',
               '运动': '缓慢拉远',
               '角度': '仰视'
           },
           '画面叙事': f"情绪回落 - {asset3['光影系统']}",
           '情绪曲线': 'Setup→Action→Resolution'
       }
       cards.append(card3)
       
       return cards
   ```

4. **长镜头裂变**：
   - 选取1-3个关键节点（根据复杂度和关键点数量）
   - 每个节点继承环境资产但更新角色位置
   - **镜头运动**：标注完整的镜头运动轨迹
   - **连续性**：节点间的角色运动连续性必须描述
   - **环境继承**：完全继承环境资产包，但空间骨架根据角色位置更新
   - **摄影参数**：使用跟拍或升降运动
   - 输出：1-3个子镜头卡片

   **示例**：
   ```python
   def long_take_fission(parent_grid, key_points, complexity_score):
       """
       长镜头裂变算法
       """
       # 根据复杂度确定节点数量
       node_count = 1
       if complexity_score >= 4.0:
           node_count = 3
       elif complexity_score >= 3.0:
           node_count = 2
       
       # 选取关键节点
       selected_points = key_points[:node_count] if len(key_points) >= node_count else key_points
       
       cards = []
       inherited_asset = parent_grid['环境资产包'].copy()
       
       for i, point in enumerate(selected_points, 1):
           # 更新角色位置
           inherited_asset['空间骨架'] = update_for_position(
               inherited_asset['空间骨架'],
               f"角色位置{i}"
           )
           
           card = {
               '镜头序号': i,
               '继承关系': f"继承自Board{parent_grid['板号']}格{parent_grid['格子号']}（节点{i}）",
               '环境构造': inherited_asset.copy(),
               '摄影参数': {
                   '镜头': '中景',
                   '运动': '跟拍' if i < node_count else '停止',
                   '角度': '平视'
               },
               '画面叙事': f"{point['内容']} - {inherited_asset['空间骨架']}",
               '镜头运动轨迹': f'从节点{max(1, i-1)}到节点{i}的连续运动' if i > 1 else '起始位置',
               '连续性': f'节点{max(1, i-1)}到节点{i}的角色运动连续性' if i > 1 else '起始节点'
           }
           cards.append(card)
       
       return cards
   ```

**输出格式**：
裂变后的子镜头卡片列表，每个卡片包含：
- 镜头序号（1-N）
- 继承关系（来自父格的信息）
- 环境构造（继承+调整）
- 摄影参数（镜头、运动、角度）
- 画面叙事（基于裂变算法生成的画面描述）
- 运动连续性（对于多格裂变）
- 情绪曲线（对于蒙太奇组）

**算法流程图**：
```
输入：九宫格父画面 + 节拍拆解的[关键信息点]
    ↓
识别策略标签类型
    ↓
┌─────────────────────────────────────┐
│ 策略类型？                        │
└────┬────────┬────────┬──────────┘
     │        │        │
     ↓        ↓        ↓
 [单镜]   [动势组]  [蒙太奇组] / [长镜头]
     │        │        │
     ↓        ↓        ↓
单镜裂变  动势组裂变 蒙太奇/长镜头裂变
     │        │        │
     └────────┴────────┘
              ↓
      生成子镜头卡片列表
              ↓
      注入环境资产继承关系
              ↓
输出：裂变结果（含完整继承信息）
```
  
#### 情绪标签与运动标签处理

**标签映射规则**：

| 情绪标签 | 推荐镜头运动 | 视觉强化 |
|---------|-------------|---------|
| 惊恐 | 急推、快速切换 | 高对比度、冷色调 |
| 期待 | 缓慢推进 | 暖色调、柔光 |
| 滑稽 | 轻微晃动、快速摇移 | 鲜艳色彩、夸张构图 |
| 悲伤 | 缓慢拉远、固定 | 低饱和度、散射光 |
| 愤怒 | 手持晃动、快速推拉 | 高饱和度、硬光 |

### V4.1裂变算法实现

```python
def v4_1_fission_algorithm(beat_data, previous_board_context=None):
    """
    V4.1裂变算法核心实现
    
    参数:
        beat_data: 节拍数据（含V4.1字段）
        previous_board_context: 上一板上下文（用于连续性检查）
    
    返回:
        fission_result: V4.1裂变结果
    """
    
    # Step 1: 读取V4.1诊断信息
    core_strategy = beat_data.get("core_strategy", "[蒙太奇组]")
    complexity_score = beat_data.get("complexity_score", 3.0)
    suggested_grid_count = beat_data.get("suggested_grid_count", 3)
    asset_package_id = beat_data.get("environment_asset_package_id")
    thickening_level = beat_data.get("visual_thickening_level", "medium")
    emotion_tags = beat_data.get("emotion_tags", [])
    motion_tags = beat_data.get("motion_tags", [])
    type_coefficient = beat_data.get("type_coefficient", 1.0)
    
    # Step 2: 策略标签解析
    strategy_type = parse_strategy_tag(core_strategy)
    base_grid_count = get_base_grid_count(strategy_type)
    
    # Step 3: 资产包匹配与加载
    asset_package = None
    inheritance_score = 0
    if asset_package_id:
        asset_package, inheritance_score = load_environment_asset_package(
            asset_package_id, beat_data
        )
    
    # Step 4: 视觉增厚优化
    scene_description = beat_data.get("scene_description", "")
    if thickening_level != "none":
        scene_description = apply_visual_thickening(
            scene_description, thickening_level, asset_package
        )
    
    # Step 5: 复杂度驱动的格子调整
    complexity_adjustment = calculate_complexity_adjustment(complexity_score)
    final_grid_count = min(
        base_grid_count + complexity_adjustment,
        suggested_grid_count,
        4  # 最大4格
    )
    
    # 应用类型系数修正
    adjusted_grid_count = apply_type_coefficient(
        final_grid_count, type_coefficient
    )
    
    # Step 6: 长节拍裂变判断
    requires_multi_board = False
    board_count = 1
    if complexity_score >= 3.5 and len(beat_data.get("key_points", [])) >= 4:
        requires_multi_board = True
        board_count = calculate_board_count(adjusted_grid_count)
    
    # Step 7: 内容分配到格子
    grid_allocations = distribute_keypoints_with_v4_1(
        beat_data.get("key_points", []),
        adjusted_grid_count,
        strategy_type,
        asset_package,
        motion_tags
    )
    
    # Step 8: 跨板连续性检查
    continuity_evaluation = None
    if previous_board_context:
        continuity_evaluation = evaluate_v4_1_continuity(
            previous_board_context,
            grid_allocations[0] if grid_allocations else None,
            asset_package
        )
    
    # 组装V4.1裂变结果
    fission_result = {
        "beat_number": beat_data.get("beat_number"),
        "v4_1_version": "4.1",
        "core_strategy": core_strategy,
        "strategy_type": strategy_type,
        "complexity_score": complexity_score,
        "final_grid_count": adjusted_grid_count,
        "board_count": board_count,
        "requires_multi_board": requires_multi_board,
        "asset_package": {
            "id": asset_package_id,
            "inheritance_score": inheritance_score,
            "applied": asset_package is not None
        },
        "visual_thickening": {
            "level": thickening_level,
            "applied": thickening_level != "none",
            "enhanced_description": scene_description
        },
        "emotion_motion_mapping": {
            "emotion_tags": emotion_tags,
            "motion_tags": motion_tags,
            "recommended_camera_work": map_emotion_to_camera(emotion_tags)
        },
        "grid_allocations": grid_allocations,
        "continuity_evaluation": continuity_evaluation,
        "v4_1_optimization_applied": True
    }
    
    return fission_result
```

### V4.1质量检查清单

**裂变前检查**：
- [ ] 所有V4.1字段已正确读取
- [ ] 策略标签解析正确
- [ ] 资产包ID有效且可加载
- [ ] 视觉增厚等级在有效范围内

**裂变中检查**：
- [ ] 格子数计算符合复杂度评分
- [ ] 资产包继承优先级≥60分
- [ ] 视觉增厚应用成功
- [ ] 情绪-运动标签映射合理

**裂变后检查**：
- [ ] 所有关键点分配到格子
- [ ] 跨板连续性评分≥80分
- [ ] 镜头运动标签与内容匹配
- [ ] 环境资产信息正确注入

---

## 内容分配算法

### Step 3: 将关键点分配到格子

```python
def distribute_keypoints_to_grids(key_points, grid_count, strategy_type):
    """
    将关键点分配到格子中
    
    参数:
        key_points: 关键点列表（已按时间顺序排序）
        grid_count: 格子数
        strategy_type: 策略类型
    
    返回:
        grid_allocation: [
            {
                "grid_number": 1,
                "assigned_key_point": {"类型": "Setup", "内容": "..."},
                "focus_description": "基于关键点生成的画面描述",
                "time_allocation": "约XX秒（占总时长XX%）"
            },
            ...
        ]
    """
    
    grid_allocation = []
    
    # 根据策略类型使用不同的分配逻辑
    if strategy_type == "[单镜]":
        # 单镜：所有关键点压缩到一帧
        combined_description = combine_keypoints(key_points)
        grid_allocation.append({
            "grid_number": 1,
            "assigned_key_point": None,
            "focus_description": combined_description,
            "time_allocation": f"约{beat_data.estimated_duration}秒（100%）",
            "camera_motion": "固定或缓慢运动",
            "edit_point": "无"
        })
    
    elif strategy_type == "[动势组]":
        # 动势组：分配为起幅和落幅
        # 起幅：Setup 或 动作开始
        # 落幅：Action 或 动作结束
        
        setup_points = [kp for kp in key_points if kp.type in ["Setup", "动作开始"]]
        payoff_points = [kp for kp in key_points if kp.type in ["Action", "动作结束"]]
        
        if grid_count == 2:
            grid_allocation.append({
                "grid_number": 1,
                "assigned_key_point": setup_points[0] if setup_points else key_points[0],
                "focus_description": generate_description(setup_points[0] if setup_points else key_points[0]),
                "time_allocation": "约40%",
                "camera_motion": "缓慢推拉或固定",
                "edit_point": "起幅（动作开始前准备姿态）"
            })
            grid_allocation.append({
                "grid_number": 2,
                "assigned_key_point": payoff_points[0] if payoff_points else key_points[-1],
                "focus_description": generate_description(payoff_points[0] if payoff_points else key_points[-1]),
                "time_allocation": "约60%",
                "camera_motion": "急推或跟拍",
                "edit_point": "落幅（动作完成后的结果姿态）"
            })
    
    elif strategy_type == "[蒙太奇组]":
        # 蒙太奇组：三段式分配
        # Setup（起势）、Action（动作）、Resolution（结果）
        
        setup_points = [kp for kp in key_points if kp.type == "Setup"]
        action_points = [kp for kp in key_points if kp.type == "Action"]
        resolution_points = [kp for kp in key_points if kp.type == "Resolution"]
        
        if grid_count == 3:
            grid_allocation.append({
                "grid_number": 1,
                "assigned_key_point": setup_points[0] if setup_points else key_points[0],
                "focus_description": generate_description(setup_points[0] if setup_points else key_points[0]),
                "time_allocation": "约25%",
                "camera_motion": "固定镜头，轻微推拉",
                "edit_point": "Setup（起势：建立情境）"
            })
            grid_allocation.append({
                "grid_number": 2,
                "board_number": current_board,
                "assigned_key_point": action_points[0] if action_points else key_points[0],
                "focus_description": generate_description(action_points[0] if action_points else key_points[0]),
                "time_allocation": "约50%",
                "camera_motion": "快速切或跟拍",
                "edit_point": "Action（动作：核心动作或转折点）"
            })
            grid_allocation.append({
                "grid_number": 3,
                "board_number": current_board,
                "assigned_key_point": resolution_points[0] if resolution_points else key_points[-1],
                "focus_description": generate_description(resolution_points[0] if resolution_points else key_points[-1]),
                "time_allocation": "约25%",
                "camera_motion": "慢推拉或固定",
                "edit_point": "Resolution（结果：动作结果或情绪余波）"
            })
    
    elif strategy_type == "[长镜头]":
        # 长镜头：选取关键姿势，标注轨迹
        key_poses = [kp for kp in key_points if kp.type in ["关键点1", "关键点2", "关键点3"]]
        
        for i, key_point in enumerate(key_poses):
            if i < grid_count:
                grid_allocation.append({
                    "grid_number": i + 1,
                    "assigned_key_point": key_point,
                    "focus_description": f"关键姿势{i+1}：{key_point['内容']}",
                    "time_allocation": f"约{100/grid_count}%",
                    "camera_motion": "手持跟拍，从全景到中景，有轻微摇晃" if i == 0 else "缓慢摇镜",
                    "edit_point": f"关键节点{i+1}"
                })
    
    return grid_allocation
```

---

## 跨板连贯性检查

### 板间连贯性规则

**检查项**：
1. **视觉连续性**：上一板最后格子的视觉状态与下一板首格子的视觉状态是否连续
2. **时间连续性**：上一板的时间点与下一板的时间点是否逻辑连续
3. **角色状态连续性**：角色在跨板时的服装、道具、位置是否一致
4. **情绪曲线连续性**：情绪在跨板时是否平滑过渡

### 连贯性评分算法

```python
def evaluate_continuity(previous_board_last_grid, current_board_first_grid):
    """
    评估跨板连贯性
    
    参数:
        previous_board_last_grid: 上一板的最后一个格子
        current_board_first_grid: 当前板的第一个格子
    
    返回:
        continuity_score: 连贯性评分 (0-100)
        issues: 检测到的不连贯问题列表
    """
    continuity_score = 100
    issues = []
    
    # 视觉连续性检查
    if previous_board_last_grid and current_board_first_grid:
        # 检查角色外观是否一致
        if previous_board_last_grid.get("角色") != current_board_first_grid.get("角色"):
            continuity_score -= 10
            issues.append(f"角色外观不一致: {previous_board_last_grid.get('角色')} → {current_board_first_grid.get('角色')}")
        
        # 检查场景环境是否一致
        if previous_board_last_grid.get("场景") != current_board_first_grid.get("场景"):
            continuity_score -= 5
            issues.append(f"场景环境不连续: {previous_board_last_grid.get('场景')} → {current_board_first_grid.get('场景')}")
    
    # 时间连续性检查
    prev_time = previous_board_last_grid.get("时间点")
    curr_time = current_board_first_grid.get("时间点")
    if prev_time and curr_time and curr_time < prev_time:
        continuity_score -= 15
        issues.append(f"时间倒流: {prev_time} → {curr_time}")
    
    # 情绪连续性检查
    prev_emotion = previous_board_last_grid.get("情绪基调")
    curr_emotion = current_board_first_grid.get("情绪基调")
    if prev_emotion and curr_emotion and has_abrupt_transition(prev_emotion, curr_emotion):
        continuity_score -= 20
        issues.append(f"情绪突变: {prev_emotion} → {curr_emotion}（缺少过渡）")
    
    return continuity_score, issues
```

---

## 输出格式

### 动态拆解结果

```json
{
  "beat_number": 7,
  "core_strategy": "[蒙太奇组:变脸]",
  "total_grids_needed": 3,
  "board_allocations": [
    {
      "board_number": 1,
      "grid_count": 3,
      "beat_range": [7, 0, 2],
      "grids": [
        {
          "grid_number": 1,
          "in_board_position": 1,
          "assigned_key_point": {"类型": "Setup", "内容": "惊恐表情"},
          "focus_description": "包子猪惊恐定格，双手悬停在空中",
          "time_allocation": "约25%",
          "camera_motion": "固定镜头，轻微推拉",
          "edit_point": "Setup（起势：建立情境）"
        },
        {
          "grid_number": 2,
          "in_board_position": 2,
          "assigned_key_point": {"类型": "Action", "内容": "变脸过程"},
          "focus_description": "包子猪瞬间变脸，从惊恐到期待的表情变化",
          "time_allocation": "约50%",
          "camera_motion": "快速切或跟拍，强调变脸瞬间",
          "edit_point": "Action（动作：核心变化点）"
        },
        {
          "grid_number": 3,
          "in_board_position": 3,
          "assigned_key_point": {"类型": "Resolution", "内容": "期待敲盘"},
          "focus_description": "包子猪期待地握着刀叉，准备敲击",
          "time_allocation": "约25%",
          "camera_motion": "慢推拉至特写",
          "edit_point": "Resolution（结果：情绪余波）"
        }
      ]
    },
    {
      "board_number": 2,
      "grid_count": 0,
      "beat_range": [7, 3, 3],
      "is_continuation": true,
      "grids": []
    }
  ],
  "continuity_evaluation": {
    "cross_board_continuity": true,
    "visual_continuity_score": 95,
    "time_continuity_score": 100,
    "emotional_continuity_score": 90,
    "detected_issues": ["情绪突变: 惊恐→期待（缺少过渡）"]
  }
}
```

---

## 质量检查规则

### 拆解合理性检查

**检查项**：
- [ ] 所有关键点都得到分配
- [ ] 格子分配与核心策略匹配
- [ ] 复杂度调整合理（不超过基础格子数+2）
- [ ] 板内时间分配总和等于预估时长
- [ ] 跨板连续性检查通过

### 输出完整性检查

**检查项**：
- [ ] 包含所有必需字段（画面描述、镜头运动、时间分配、编辑点）
- [ ] JSON 格式正确
- [ ] 包含连贯性评估结果
- [ ] 包含跨板信息

---

## 配置选项

### 引擎配置

```json
{
  "dynamic_breakdown": {
    "enable_complexity_adjustment": true,
    "max_grids_per_board": 4,
    "allow_cross_board_continuation": true,
    "continuity_score_threshold": 80,
    "auto_fix_continuity_issues": false,
    "enable_smart_grid_allocation": true
  }
}
```

---

## 使用方式

### 调用方式

**在 SKILL 中调用**：
```python
from common.dynamic_breakdown_engine import dynamic_breakdown_engine

# 读取节拍拆解表
beat_table = load_beat_table("outputs/beat-breakdown-ep01.md")

# 对每个节拍执行动态拆解
dynamic_breakdown_results = []
for beat in beat_table:
    result = dynamic_breakdown_engine(beat)
    dynamic_breakdown_results.append(result)

# 生成四宫格提示词
for result in dynamic_breakdown_results:
    generate_sequence_board(result.board_allocations)
```

### 向后兼容性

**旧模式支持**：
- 当 `dynamic_breakdown.enable_complexity_adjustment = false` 时，使用固定4格模板
- 当 `allow_cross_board_continuation = false` 时，每个节拍限制在单板内

**回退机制**：
- 如果动态拆解失败，回退到模板拆解
- 如果复杂度评分异常，使用建议格子数

---

## 版本信息

- **版本**: 4.1
- **创建日期**: 2026-01-28
- **更新日期**: 2026-01-31
- **兼容版本**: V3.0, V4.0, V4.1
- **状态**: ✅ V4.1优化已实现
- **更新状态**: ✅ 已验证

### V4.1更新日志

**Phase 4.3 - 裂变算法优化** (2026-01-31):
- ✅ 整合策略标签智能驱动格子分配
- ✅ 集成环境资产包自动匹配与继承
- ✅ 添加视觉增厚三层优化（高/中/低）
- ✅ 实现长节拍自动裂变（复杂度≥3.5）
- ✅ 增强跨板连续性智能检查
- ✅ 添加类型化权重修正集成
- ✅ 创建V4.1裂变算法核心流程章节
- ✅ 实现V4.1字段处理规则
- ✅ 添加V4.1质量检查清单

---

**注意事项**：
- 本引擎依赖于蓝图A的输出格式（必须包含核心策略、辅助信息、关键信息点、复杂度评分、建议格子数）
- 本引擎与 blueprintB 的四宫格裂变协议协同工作
- 本引擎输出的数据格式与 sequence-board-template.md 兼容
