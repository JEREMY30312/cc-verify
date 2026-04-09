# 环境注入优化器（V4.1优化）

## 概述

**目的**：优化环境构造注入流程，集成V4.1优化功能，实现智能、配置驱动的环境注入。

**V4.1集成功能**：
1. **环境资产包继承**：智能匹配和继承环境资产包
2. **视觉增厚集成**：自动应用视觉增厚优化
3. **策略标签驱动**：根据策略标签调整注入重点
4. **复杂度自适应**：根据复杂度评分调整注入深度
5. **配置驱动**：通过.agent-state.json控制注入参数

## V4.1环境注入框架

### 注入流程架构
```
输入：原始场景描述 + 节拍数据 + 项目配置
    ↓
步骤1：V4.1字段解析
    ↓
步骤2：环境资产包匹配
    ↓
步骤3：策略标签分析
    ↓
步骤4：四阶段智能注入
    ↓
步骤5：视觉增厚应用
    ↓
步骤6：质量验证
    ↓
输出：优化后的环境描述 + 注入元数据
```

### 配置集成
```json
{
  "projectConfig": {
    "environment_injection_config": {
      "enabled": true,
      "injection_mode": "smart",  // smart/basic/minimal
      "asset_package_matching": true,
      "visual_thickening_integration": true,
      "strategy_tag_adaptation": true,
      "quality_validation": true,
      "default_injection_depth": "medium",  // high/medium/low
      "complexity_adaptive": true
    }
  }
}
```

## 四阶段智能注入（V4.1优化版）

### 阶段1：智能空间骨架构建
**V4.1优化**：基于策略标签调整空间构建重点

| 策略标签 | 空间构建重点 | 输出特征 |
|----------|--------------|----------|
| `[环境]` | 完整空间布局，强调环境关系 | 详细空间描述，明确空间关系 |
| `[全景]` | 宏观空间结构，强调场景规模 | 宏大空间感，清晰边界 |
| `[中景]` | 角色活动空间，强调互动区域 | 角色为中心的空间布局 |
| `[特写]` | 局部空间焦点，强调细节区域 | 聚焦区域，细节空间 |
| `[单镜]` | 精简空间，强调核心区域 | 必要空间信息，简洁明了 |

**算法**：
```python
def build_spatial_framework_v4_1(scene_description, strategy_tags, complexity_score):
    """
    V4.1优化版空间骨架构建
    """
    spatial_data = {}
    
    # 基础空间提取
    base_layout = extract_base_layout(scene_description)
    
    # 策略标签调整
    if '[环境]' in strategy_tags or '[全景]' in strategy_tags:
        # 完整空间构建
        spatial_data = build_complete_spatial(base_layout, complexity_score)
    elif '[中景]' in strategy_tags:
        # 角色中心空间
        spatial_data = build_character_centric_spatial(base_layout)
    elif '[特写]' in strategy_tags:
        # 细节焦点空间
        spatial_data = build_detail_focused_spatial(base_layout)
    else:
        # 基础空间
        spatial_data = build_basic_spatial(base_layout)
    
    # 复杂度调整
    if complexity_score >= 3.5:
        spatial_data = enhance_spatial_complexity(spatial_data)
    
    return spatial_data
```

### 阶段2：动态材质皮肤覆盖
**V4.1优化**：基于复杂度评分调整材质细节密度

| 复杂度范围 | 材质覆盖深度 | 细节密度 |
|------------|--------------|----------|
| ≥4.0 | 完整材质系统 | 高密度细节，多层纹理 |
| 3.0-3.9 | 关键材质+次要材质 | 中等密度，主要纹理 |
| 2.0-2.9 | 关键材质 | 基础密度，必要纹理 |
| <2.0 | 最小材质 | 低密度，符号化纹理 |

**算法**：
```python
def apply_material_coverage_v4_1(spatial_data, complexity_score, asset_package):
    """
    V4.1优化版材质皮肤覆盖
    """
    material_data = {}
    
    # 从资产包继承材质
    if asset_package and 'materials' in asset_package.get('assets', {}):
        base_materials = asset_package['assets']['materials']
    else:
        base_materials = extract_materials_from_spatial(spatial_data)
    
    # 根据复杂度调整材质密度
    if complexity_score >= 4.0:
        material_data = apply_full_material_system(base_materials)
    elif complexity_score >= 3.0:
        material_data = apply_key_materials_with_support(base_materials)
    elif complexity_score >= 2.0:
        material_data = apply_key_materials_only(base_materials)
    else:
        material_data = apply_minimal_materials(base_materials)
    
    # 根据策略标签调整材质重点
    strategy_tags = spatial_data.get('strategy_tags', [])
    if '[环境]' in strategy_tags:
        material_data = emphasize_environmental_materials(material_data)
    elif '[特写]' in strategy_tags:
        material_data = emphasize_detail_materials(material_data)
    
    return material_data
```

### 阶段3：情感化光影氛围注入
**V4.1优化**：基于情感标签调整光影氛围

| 情感标签 | 光影特点 | 氛围效果 |
|----------|----------|----------|
| `[情感高潮]` | 强烈对比，动态光影 | 戏剧性，情绪爆发 |
| `[情感压抑]` | 低调光影，柔和对比 | 压抑感，情绪内敛 |
| `[情感过渡]` | 渐变光影，平滑过渡 | 自然流畅，情绪变化 |
| `[情感反差]` | 对比光影，快速变化 | 冲击感，情绪反转 |
| 无情感标签 | 中性光影，匹配场景 | 场景适配，自然氛围 |

**算法**：
```python
def inject_lighting_atmosphere_v4_1(material_data, emotion_tags, asset_package):
    """
    V4.1优化版光影氛围注入
    """
    lighting_data = {}
    
    # 基础光影设置
    if asset_package and 'lighting' in asset_package.get('assets', {}):
        base_lighting = asset_package['assets']['lighting']
    else:
        base_lighting = generate_basic_lighting(material_data)
    
    # 情感标签调整
    if '[情感高潮]' in emotion_tags:
        lighting_data = apply_dramatic_lighting(base_lighting)
    elif '[情感压抑]' in emotion_tags:
        lighting_data = apply_subdued_lighting(base_lighting)
    elif '[情感过渡]' in emotion_tags:
        lighting_data = apply_transitional_lighting(base_lighting)
    elif '[情感反差]' in emotion_tags:
        lighting_data = apply_contrast_lighting(base_lighting)
    else:
        lighting_data = apply_neutral_lighting(base_lighting)
    
    # 根据策略标签调整光影视角
    strategy_tags = material_data.get('strategy_tags', [])
    if '[环境]' in strategy_tags or '[全景]' in strategy_tags:
        lighting_data = adjust_for_environmental_shot(lighting_data)
    elif '[特写]' in strategy_tags:
        lighting_data = adjust_for_closeup_shot(lighting_data)
    
    return lighting_data
```

### 阶段4：策略驱动动态生命添加
**V4.1优化**：基于镜头运动标签调整动态元素

| 镜头运动标签 | 动态元素重点 | 运动特点 |
|--------------|--------------|----------|
| `[推拉]` | 焦点动态，深度变化 | 渐进运动，焦点转移 |
| `[摇移]` | 空间动态，水平运动 | 平滑移动，空间探索 |
| `[跟拍]` | 角色动态，跟随运动 | 同步移动，沉浸感 |
| `[升降]` | 垂直动态，高度变化 | 垂直运动，视角变化 |
| `[旋转]` | 旋转动态，眩晕效果 | 旋转运动，情绪强化 |
| 无运动标签 | 基础动态，场景适配 | 自然动态，场景增强 |

**算法**：
```python
def add_dynamic_life_v4_1(lighting_data, motion_tags, complexity_score):
    """
    V4.1优化版动态生命添加
    """
    dynamics_data = {}
    
    # 基础动态元素
    base_dynamics = generate_base_dynamics(lighting_data)
    
    # 镜头运动标签调整
    if '[推拉]' in motion_tags:
        dynamics_data = add_focus_dynamics(base_dynamics)
    if '[摇移]' in motion_tags:
        dynamics_data = add_panning_dynamics(dynamics_data or base_dynamics)
    if '[跟拍]' in motion_tags:
        dynamics_data = add_following_dynamics(dynamics_data or base_dynamics)
    if '[升降]' in motion_tags:
        dynamics_data = add_elevation_dynamics(dynamics_data or base_dynamics)
    if '[旋转]' in motion_tags:
        dynamics_data = add_rotation_dynamics(dynamics_data or base_dynamics)
    
    # 如果没有运动标签，添加场景适配动态
    if not motion_tags:
        dynamics_data = add_scene_appropriate_dynamics(base_dynamics)
    
    # 复杂度调整动态密度
    if complexity_score >= 3.5:
        dynamics_data = increase_dynamic_density(dynamics_data)
    elif complexity_score <= 2.0:
        dynamics_data = reduce_dynamic_density(dynamics_data)
    
    return dynamics_data or base_dynamics
```

## 完整注入算法

```python
def inject_environment_v4_1(scene_description, beat_data, project_config):
    """
    V4.1完整环境注入算法
    """
    
    # 1. 解析V4.1字段
    complexity_score = beat_data.get('complexity_score', 2.5)
    strategy_tags = beat_data.get('strategy_tags', [])
    emotion_tags = beat_data.get('emotion_tags', [])
    motion_tags = beat_data.get('motion_tags', [])
    final_weight = beat_data.get('final_weight', 1.0)
    
    # 2. 匹配环境资产包
    asset_package = match_asset_package(scene_description, strategy_tags, project_config)
    
    # 3. 确定注入深度
    injection_depth = determine_injection_depth(
        complexity_score, 
        strategy_tags, 
        final_weight,
        project_config
    )
    
    # 4. 执行四阶段注入
    injection_results = {}
    
    # 阶段1：智能空间骨架构建
    spatial_data = build_spatial_framework_v4_1(
        scene_description, 
        strategy_tags, 
        complexity_score
    )
    injection_results['spatial_framework'] = spatial_data
    
    # 阶段2：动态材质皮肤覆盖
    material_data = apply_material_coverage_v4_1(
        spatial_data, 
        complexity_score, 
        asset_package
    )
    injection_results['materials'] = material_data
    
    # 阶段3：情感化光影氛围注入
    lighting_data = inject_lighting_atmosphere_v4_1(
        material_data, 
        emotion_tags, 
        asset_package
    )
    injection_results['lighting'] = lighting_data
    
    # 阶段4：策略驱动动态生命添加
    dynamics_data = add_dynamic_life_v4_1(
        lighting_data, 
        motion_tags, 
        complexity_score
    )
    injection_results['dynamics'] = dynamics_data
    
    # 5. 生成环境描述
    environment_description = generate_environment_description(injection_results)
    
    # 6. 应用视觉增厚
    if project_config.get('visual_thickening_integration', True):
        thickened_description = apply_visual_thickening_v4_1(
            environment_description,
            beat_data,
            injection_results
        )
    else:
        thickened_description = environment_description
    
    # 7. 质量验证
    quality_metrics = validate_injection_quality(
        scene_description,
        thickened_description,
        injection_results,
        project_config
    )
    
    return {
        'original_description': scene_description,
        'injected_description': thickened_description,
        'injection_results': injection_results,
        'asset_package_used': asset_package is not None,
        'injection_depth': injection_depth,
        'quality_metrics': quality_metrics,
        'v4_1_fields_used': {
            'complexity_score': complexity_score,
            'strategy_tags': strategy_tags,
            'emotion_tags': emotion_tags,
            'motion_tags': motion_tags,
            'final_weight': final_weight
        }
    }
```

## 注入深度确定算法

```python
def determine_injection_depth(complexity_score, strategy_tags, final_weight, config):
    """
    确定环境注入深度
    """
    
    # 基础深度：基于复杂度
    if complexity_score >= 4.0:
        base_depth = 'high'
    elif complexity_score >= 3.0:
        base_depth = 'medium'
    else:
        base_depth = 'low'
    
    # 策略标签调整
    if '[环境]' in strategy_tags or '[全景]' in strategy_tags:
        if base_depth == 'low':
            base_depth = 'medium'
        elif base_depth == 'medium':
            base_depth = 'high'
    
    if '[特写]' in strategy_tags and base_depth == 'high':
        base_depth = 'medium'  # 特写不需要过深的环境
    
    # 权重调整
    if final_weight >= 3.0 and base_depth != 'high':
        base_depth = 'high'
    elif final_weight >= 2.0 and base_depth == 'low':
        base_depth = 'medium'
    
    # 配置覆盖
    config_depth = config.get('default_injection_depth', 'medium')
    if config.get('complexity_adaptive', True):
        return base_depth
    else:
        return config_depth
```

## 质量评估指标

### 注入完整性指标
| 指标 | 描述 | 目标值 |
|------|------|--------|
| **空间完整性** | 空间元素覆盖度 | ≥85% |
| **材质完整性** | 材质细节覆盖度 | ≥80% |
| **光影完整性** | 光影氛围覆盖度 | ≥75% |
| **动态完整性** | 动态元素覆盖度 | ≥70% |

### 策略匹配指标
| 指标 | 描述 | 目标值 |
|------|------|--------|
| **策略标签匹配** | 注入内容与策略标签匹配度 | ≥80% |
| **情感氛围匹配** | 光影氛围与情感标签匹配度 | ≥85% |
| **镜头运动匹配** | 动态元素与镜头运动匹配度 | ≥75% |

### 视觉质量指标
| 指标 | 描述 | 目标值 |
|------|------|--------|
| **丰富度提升** | 描述长度增加比例 | 1.5-3.0倍 |
| **细节密度** | 每句平均视觉细节 | 2-4个 |
| **感官维度** | 涉及的感官维度数量 | 2-3个 |

## 集成到工作流程

### 节拍拆解阶段
1. 识别环境需求和注入参数
2. 预匹配环境资产包
3. 记录建议注入深度

### 九宫格生成阶段
1. 调用`inject_environment_v4_1()`执行注入
2. 继承和调整环境资产包
3. 应用视觉增厚
4. 验证注入质量

### 四宫格裂变阶段
1. 保持环境注入一致性
2. 根据镜头运动调整环境视角
3. 确保跨板环境连贯性

## 使用示例

```python
# 输入数据
beat_data = {
    'scene_description': '包子猪在柜台后等待',
    'complexity_score': 3.2,
    'strategy_tags': ['[中景]', '[环境]'],
    'emotion_tags': ['[情感压抑]'],
    'motion_tags': ['[摇移]'],
    'final_weight': 2.8
}

# 执行注入
result = inject_environment_v4_1(
    beat_data['scene_description'],
    beat_data,
    project_config
)

# 输出结果
print(result['injected_description'])
# "包子铺内景中，包子猪在木质柜台后等待，表情压抑。灰色水泥地面有磨损痕迹，
# 顶部日光灯管投下冷白光，在墙面形成硬阴影。蒸汽从蒸笼缓缓飘动，镜头水平摇移
# 展示空间，渲染出压抑的氛围"
```

---

**配置说明**：
1. 在`.agent-state.json`中配置`environment_injection_config`
2. 根据项目需求调整注入参数
3. 监控质量指标并优化配置