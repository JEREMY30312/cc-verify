# 动态拆解引擎 Dynamic Breakdown Engine

## Python Import Statements（Phase 2.1 修复）

```python
from common.environment_asset_package import load_asset_package, calculate_inheritance_priority
from common.visual_thickening_optimizer import apply_visual_thickening_v4_1
from common.environment_injection_optimizer import apply_environment_injection_v4_1
from common.strategy_completion import generate_strategy_tags_from_scene
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
