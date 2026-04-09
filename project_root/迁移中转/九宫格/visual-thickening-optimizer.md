# 视觉增厚优化器（V4.1优化）

## 概述

**目的**：增强画面描述质量，将简单的剧本描述转化为丰富的视觉画面，支持环境资产包继承和策略标签驱动。

**V4.1优化功能**：
1. **多级增厚**：根据复杂度评分和策略标签应用不同级别的视觉增厚
2. **资产包集成**：继承环境资产包信息，自动添加环境细节
3. **策略驱动**：根据策略标签调整增厚重点
4. **配置控制**：通过.agent-state.json配置增厚参数

## 增厚级别定义

### 三级增厚体系
| 级别 | 描述 | 适用复杂度 | 适用策略标签 | 输出特征 |
|------|------|------------|--------------|----------|
| **高级增厚** | 完整环境构造+情感渲染+动态细节 | ≥3.5 | `[环境]`, `[全景]`, `[蒙太奇组]` | 沉浸式画面，包含空间、材质、光影、动态、情感 |
| **中级增厚** | 基础环境+关键细节+适度情感 | 2.5-3.4 | `[中景]`, `[动势组]`, `[特写]` | 清晰画面，包含空间和关键细节 |
| **基础增厚** | 最小环境上下文+基本描述 | <2.5 | `[单镜]`, 无环境标签 | 简洁画面，仅必要环境信息 |

## 增厚算法

### 核心增厚函数
```python
def apply_visual_thickening_v4_1(original_description, beat_data, asset_package=None):
    """
    V4.1优化版视觉增厚算法
    
    参数:
        original_description: 原始画面描述
        beat_data: 节拍数据（包含V4.1优化字段）
        asset_package: 环境资产包（可选）
    
    返回:
        thickened_description: 增厚后的画面描述
        thickening_metadata: 增厚元数据
    """
    
    # 1. 读取V4.1优化字段
    complexity_score = beat_data.get('complexity_score', 2.5)
    strategy_tags = beat_data.get('strategy_tags', [])
    final_weight = beat_data.get('final_weight', 1.0)
    keyframe_level = beat_data.get('keyframe_level', '🟡')
    
    # 2. 确定增厚级别
    thickening_level = determine_thickening_level(
        complexity_score, 
        strategy_tags, 
        final_weight
    )
    
    # 3. 应用基础增厚（环境上下文）
    thickened = apply_environment_context(original_description, asset_package)
    
    # 4. 根据级别应用额外增厚
    if thickening_level == 'high':
        thickened = apply_high_level_thickening(thickened, beat_data, asset_package)
    elif thickening_level == 'medium':
        thickened = apply_medium_level_thickening(thickened, beat_data, asset_package)
    # 基础级别无需额外增厚
    
    # 5. 根据策略标签调整增厚重点
    thickened = adjust_by_strategy_tags(thickened, strategy_tags)
    
    # 6. 根据关键帧等级调整细节密度
    thickened = adjust_detail_density(thickened, keyframe_level)
    
    # 7. 确保语言流畅性和视觉连贯性
    thickened = ensure_visual_coherence(thickened)
    
    return {
        'thickened_description': thickened,
        'original_description': original_description,
        'thickening_level': thickening_level,
        'applied_strategies': strategy_tags,
        'complexity_score': complexity_score,
        'asset_package_used': asset_package is not None
    }
```

### 增厚级别确定算法
```python
def determine_thickening_level(complexity_score, strategy_tags, final_weight):
    """
    确定视觉增厚级别
    """
    
    # 基础规则：基于复杂度
    if complexity_score >= 3.5:
        base_level = 'high'
    elif complexity_score >= 2.5:
        base_level = 'medium'
    else:
        base_level = 'low'
    
    # 策略标签调整
    if '[环境]' in strategy_tags or '[全景]' in strategy_tags:
        # 环境相关策略需要更高级别增厚
        if base_level == 'low':
            base_level = 'medium'
        elif base_level == 'medium':
            base_level = 'high'
    
    if '[特写]' in strategy_tags:
        # 特写需要细节增厚
        if base_level == 'low':
            base_level = 'medium'
    
    # 权重调整
    if final_weight >= 3.0 and base_level != 'high':
        base_level = 'high'  # 高权重需要高级增厚
    elif final_weight >= 2.0 and base_level == 'low':
        base_level = 'medium'  # 中权重需要中级增厚
    
    return base_level
```

## 增厚模块库

### 环境上下文增厚
```python
def apply_environment_context(description, asset_package):
    """
    应用环境上下文增厚
    """
    
    if not asset_package:
        return description
    
    # 提取空间信息
    spatial = asset_package.get('assets', {}).get('spatial_framework', {})
    layout_type = spatial.get('layout_type', '')
    
    if layout_type:
        return f"{layout_type}中，{description}"
    
    return description
```

### 高级增厚模块
```python
def apply_high_level_thickening(description, beat_data, asset_package):
    """
    应用高级视觉增厚
    """
    
    thickened = description
    
    # 1. 添加材质细节
    if asset_package:
        materials = asset_package.get('assets', {}).get('materials', {})
        material_desc = describe_materials_detail(materials)
        if material_desc:
            thickened += f"。{material_desc}"
    
    # 2. 添加光影氛围
    if asset_package:
        lighting = asset_package.get('assets', {}).get('lighting', {})
        lighting_desc = describe_lighting_detail(lighting)
        if lighting_desc:
            thickened += f"。{lighting_desc}"
    
    # 3. 添加动态元素
    if asset_package:
        dynamics = asset_package.get('assets', {}).get('dynamics', {})
        dynamics_desc = describe_dynamics_detail(dynamics)
        if dynamics_desc:
            thickened += f"。{dynamics_desc}"
    
    # 4. 添加情感渲染
    emotion_tone = beat_data.get('emotion_tone', '')
    if emotion_tone:
        thickened += f"，渲染出{emotion_tone}的氛围"
    
    # 5. 添加感官细节
    thickened = add_sensory_details(thickened, beat_data)
    
    return thickened
```

### 中级增厚模块
```python
def apply_medium_level_thickening(description, beat_data, asset_package):
    """
    应用中级视觉增厚
    """
    
    thickened = description
    
    # 1. 添加关键材质
    if asset_package:
        key_materials = extract_key_materials(
            asset_package.get('assets', {}).get('materials', {})
        )
        if key_materials:
            thickened += f"。{key_materials}"
    
    # 2. 添加基础光影
    if asset_package:
        basic_lighting = describe_basic_lighting(
            asset_package.get('assets', {}).get('lighting', {})
        )
        if basic_lighting:
            thickened += f"。{basic_lighting}"
    
    # 3. 添加适度情感
    emotion_tone = beat_data.get('emotion_tone', '')
    if emotion_tone:
        thickened += f"，带有{emotion_tone}的情绪"
    
    return thickened
```

### 策略标签调整
```python
def adjust_by_strategy_tags(description, strategy_tags):
    """
    根据策略标签调整增厚重点
    """
    
    adjusted = description
    
    if '[特写]' in strategy_tags:
        # 特写需要细节聚焦
        adjusted = adjust_for_closeup(adjusted)
    
    if '[全景]' in strategy_tags:
        # 全景需要空间关系
        adjusted = adjust_for_wide_shot(adjusted)
    
    if '[中景]' in strategy_tags:
        # 中景需要角色环境关系
        adjusted = adjust_for_medium_shot(adjusted)
    
    if '[环境]' in strategy_tags:
        # 环境需要氛围渲染
        adjusted = adjust_for_environment(adjusted)
    
    # 镜头运动标签
    if '[推拉]' in strategy_tags:
        adjusted = add_push_pull_description(adjusted)
    
    if '[摇移]' in strategy_tags:
        adjusted = add_pan_tilt_description(adjusted)
    
    if '[跟拍]' in strategy_tags:
        adjusted = add_follow_shot_description(adjusted)
    
    if '[升降]' in strategy_tags:
        adjusted = add_crane_shot_description(adjusted)
    
    return adjusted
```

## 增厚质量评估

### 评估指标
| 指标 | 描述 | 目标值 |
|------|------|--------|
| **丰富度提升** | 增厚后描述长度/原始长度 | 1.5-3.0倍 |
| **细节密度** | 每句平均细节数量 | 2-4个 |
| **感官维度** | 涉及的感官维度数量 | 2-4个 |
| **情感表达** | 情感描述明确度 | 明确/适度/基础 |
| **环境完整性** | 环境元素覆盖度 | ≥70% |

### 质量检查函数
```python
def evaluate_thickening_quality(original, thickened, metadata):
    """
    评估视觉增厚质量
    """
    
    quality_score = 0
    feedback = []
    
    # 1. 丰富度检查
    richness_ratio = len(thickened) / len(original) if len(original) > 0 else 1.0
    if 1.5 <= richness_ratio <= 3.0:
        quality_score += 25
        feedback.append(f"丰富度合适: {richness_ratio:.1f}倍")
    else:
        feedback.append(f"丰富度需调整: {richness_ratio:.1f}倍")
    
    # 2. 细节密度检查
    detail_count = count_visual_details(thickened)
    sentences = thickened.split('。')
    avg_details = detail_count / len(sentences) if sentences else 0
    
    if 2.0 <= avg_details <= 4.0:
        quality_score += 25
        feedback.append(f"细节密度合适: {avg_details:.1f}个/句")
    else:
        feedback.append(f"细节密度需调整: {avg_details:.1f}个/句")
    
    # 3. 策略匹配检查
    strategy_match = evaluate_strategy_match(thickened, metadata['applied_strategies'])
    quality_score += strategy_match * 25
    
    # 4. 复杂度匹配检查
    complexity_match = evaluate_complexity_match(thickened, metadata['complexity_score'])
    quality_score += complexity_match * 25
    
    return {
        'quality_score': min(100, quality_score),
        'feedback': feedback,
        'richness_ratio': richness_ratio,
        'detail_density': avg_details,
        'strategy_match': strategy_match,
        'complexity_match': complexity_match
    }
```

## 集成到工作流程

### 节拍拆解阶段
1. 识别场景类型和视觉需求
2. 创建环境资产包引用
3. 记录建议增厚级别

### 九宫格生成阶段
1. 调用`apply_visual_thickening_v4_1()`应用增厚
2. 继承环境资产包信息
3. 根据策略标签调整增厚重点
4. 评估增厚质量

### 四宫格裂变阶段
1. 保持增厚一致性
2. 根据镜头运动调整增厚视角
3. 确保跨板视觉连贯性

## V4.1配置集成

在`.agent-state.json`中添加：
```json
{
  "projectConfig": {
    "visual_thickening_config": {
      "enabled": true,
      "default_level": "medium",
      "richness_target": 2.0,
      "detail_density_target": 3.0,
      "quality_threshold": 70,
      "auto_adjust": true,
      "strategy_weights": {
        "[环境]": 1.5,
        "[全景]": 1.3,
        "[中景]": 1.2,
        "[特写]": 1.4,
        "[单镜]": -0.5
      }
    }
  }
}
```

## 使用示例

### 输入示例
```python
beat_data = {
    'scene_description': '包子猪听到"给它吃"瞬间变脸',
    'complexity_score': 4.7,
    'strategy_tags': ['[蒙太奇组]', '[特写]', '[推拉]'],
    'final_weight': 3.52,
    'keyframe_level': '🔴',
    'emotion_tone': '惊恐转期待'
}

asset_package = {
    'assets': {
        'spatial_framework': {'layout_type': '包子铺内景'},
        'materials': {'surfaces': {'counter': '木质柜台，表面有划痕'}},
        'lighting': {'primary_source': '顶部日光灯管'},
        'dynamics': {'particle_effects': ['蒸汽飘动']}
    }
}
```

### 输出示例
```python
result = apply_visual_thickening_v4_1(
    beat_data['scene_description'],
    beat_data,
    asset_package
)

# 输出：
{
    'thickened_description': '包子铺内景中，包子猪听到"给它吃"瞬间变脸，表情从惊恐转为期待。木质柜台表面有划痕，顶部日光灯管投下冷白光，蒸汽在空气中缓缓飘动，镜头缓缓推进聚焦表情变化',
    'thickening_level': 'high',
    'quality_score': 92
}
```

---

**使用说明**：
1. 在九宫格生成时调用视觉增厚优化器
2. 根据配置自动调整增厚级别
3. 评估增厚质量并记录反馈
4. 确保视觉增厚与策略标签匹配