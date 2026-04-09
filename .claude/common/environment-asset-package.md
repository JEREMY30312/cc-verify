# 环境资产包系统（V4.1优化）

## 概述

**目的**：管理和继承环境信息，确保跨节拍、跨分镜板的环境一致性，支持视觉增厚和环境注入。

**V4.1优化功能**：
1. **结构化存储**：将环境信息组织为可继承的资产包
2. **智能继承**：根据策略标签自动继承环境元素
3. **视觉增厚**：为画面描述添加丰富的环境细节
4. **配置驱动**：通过.agent-state.json配置资产包参数

## 资产包数据结构

### 基础资产包结构
```json
{
  "asset_package_id": "env_001",
  "scene_name": "包子铺内景",
  "inheritance_level": "high",  // high/medium/low
  "assets": {
    "spatial_framework": {
      "layout_type": "室内小空间",
      "dimensions": "5m×4m×3m",
      "key_elements": ["柜台", "蒸笼架", "餐桌", "厨房入口"],
      "traffic_flow": "L型动线",
      "camera_positions": ["门口视角", "柜台视角", "顾客视角"]
    },
    "materials": {
      "surfaces": {
        "walls": "白色瓷砖墙面，有油渍痕迹",
        "floor": "灰色水泥地，有磨损",
        "counter": "木质柜台，表面有划痕",
        "tables": "老旧木桌，漆面剥落"
      },
      "textures": {
        "steam": "蒸笼冒出的白色水蒸气",
        "grease_stains": "墙面和灶台的黄色油渍",
        "wood_grain": "木纹纹理清晰可见"
      }
    },
    "lighting": {
      "primary_source": "顶部日光灯管",
      "secondary_sources": ["灶台火光", "窗外自然光"],
      "light_quality": "冷白光为主，暖黄光点缀",
      "shadows": "硬阴影边缘，对比度中等",
      "atmosphere": "烟雾缭绕，光线散射"
    },
    "dynamics": {
      "particle_effects": ["蒸汽飘动", "灰尘飞舞", "油光闪烁"],
      "interactive_elements": ["蒸笼盖开合", "风扇转动", "招牌晃动"],
      "soundscape": ["蒸笼嘶嘶声", "顾客交谈", "街道噪音"]
    }
  },
  "inheritance_rules": {
    "mandatory_inherit": ["layout_type", "key_elements"],
    "optional_inherit": ["textures", "dynamics"],
    "context_adapt": ["lighting", "camera_positions"]
  }
}
```

### V4.1优化字段
```json
{
  "v4_1_optimizations": {
    "strategy_tags": ["[环境]", "[全景]", "[中景]"],
    "complexity_threshold": 2.5,
    "visual_thickening_level": "high",  // high/medium/low
    "inheritance_priority": 90,  // 0-100
    "asset_coverage": {
      "spatial": 95,
      "material": 85,
      "lighting": 90,
      "dynamics": 75
    }
  }
}
```

## 资产包继承算法

### 继承优先级计算
```
继承分数 = 基础分数 × 策略系数 × 复杂度系数

其中：
1. 基础分数 = 资产包优先级（0-100）
2. 策略系数 = 
   - [环境]标签：×1.5
   - [全景]标签：×1.3
   - [中景]标签：×1.2
   - 其他标签：×1.0
3. 复杂度系数 = 1.0 + (复杂度评分 - 2.5) × 0.1
```

### 继承执行逻辑
```python
def inherit_environment_assets(target_beat, available_packages):
    """
    为节拍继承环境资产包
    
    参数:
        target_beat: 目标节拍对象
        available_packages: 可用资产包列表
    
    返回:
        inherited_assets: 继承的资产包
        inheritance_reason: 继承理由
    """
    
    inherited_assets = {}
    inheritance_reason = []
    
    # 1. 读取节拍的V4.1字段
    strategy_tags = target_beat.get('strategy_tags', [])
    complexity_score = target_beat.get('complexity_score', 2.5)
    scene_description = target_beat.get('scene_description', '')
    
    # 2. 筛选匹配的资产包
    matching_packages = []
    for package in available_packages:
        match_score = calculate_match_score(package, target_beat)
        if match_score >= 60:  # 匹配阈值
            matching_packages.append((package, match_score))
    
    # 3. 按匹配分数排序
    matching_packages.sort(key=lambda x: x[1], reverse=True)
    
    # 4. 继承最高匹配度的资产包
    if matching_packages:
        best_package, best_score = matching_packages[0]
        
        # 根据策略标签确定继承深度
        inheritance_depth = determine_inheritance_depth(strategy_tags, complexity_score)
        
        # 执行继承
        inherited_assets = execute_inheritance(best_package, inheritance_depth)
        
        inheritance_reason.append(
            f"继承资产包 '{best_package['scene_name']}' "
            f"(匹配度:{best_score}%, 深度:{inheritance_depth})"
        )
    
    # 5. 应用视觉增厚
    if inherited_assets and 'visual_thickening_level' in target_beat:
        thickened_description = apply_visual_thickening(
            scene_description, 
            inherited_assets,
            target_beat['visual_thickening_level']
        )
        inheritance_reason.append(f"应用视觉增厚: {target_beat['visual_thickening_level']}")
    
    return {
        'inherited_assets': inherited_assets,
        'inheritance_reason': inheritance_reason,
        'original_description': scene_description,
        'thickened_description': thickened_description if 'thickened_description' in locals() else scene_description
    }
```

## 视觉增厚算法

### 增厚级别定义
| 级别 | 描述 | 适用场景 |
|------|------|----------|
| **high** | 完整环境构造，包含空间、材质、光影、动态 | 复杂度≥3.5，策略含[环境]或[全景] |
| **medium** | 基础环境+关键细节 | 复杂度2.5-3.4，策略含[中景] |
| **low** | 仅关键环境元素 | 复杂度<2.5，或无环境策略 |

### 增厚执行逻辑
```python
def apply_visual_thickening(original_description, assets, level):
    """
    应用视觉增厚到画面描述
    
    参数:
        original_description: 原始描述
        assets: 继承的资产包
        level: 增厚级别
    
    返回:
        thickened_description: 增厚后的描述
    """
    
    thickened = original_description
    
    if level == 'high':
        # 完整增厚：空间+材质+光影+动态
        thickened = f"{assets.get('spatial_framework', {}).get('layout_type', '')}中，{thickened}"
        
        if 'materials' in assets:
            material_desc = describe_materials(assets['materials'])
            thickened += f"。{material_desc}"
        
        if 'lighting' in assets:
            lighting_desc = describe_lighting(assets['lighting'])
            thickened += f"。{lighting_desc}"
        
        if 'dynamics' in assets:
            dynamics_desc = describe_dynamics(assets['dynamics'])
            thickened += f"。{dynamics_desc}"
    
    elif level == 'medium':
        # 中等增厚：空间+关键材质
        thickened = f"{assets.get('spatial_framework', {}).get('layout_type', '')}中，{thickened}"
        
        if 'materials' in assets:
            key_materials = extract_key_materials(assets['materials'])
            thickened += f"。{key_materials}"
    
    elif level == 'low':
        # 低增厚：仅空间类型
        layout_type = assets.get('spatial_framework', {}).get('layout_type', '')
        if layout_type:
            thickened = f"{layout_type}中，{thickened}"
    
    return thickened
```

## 资产包创建与管理

### 创建新资产包
```python
def create_asset_package(scene_data, v4_1_config):
    """
    创建新的环境资产包
    
    参数:
        scene_data: 场景数据（来自节拍拆解或九宫格）
        v4_1_config: V4.1配置
    
    返回:
        asset_package: 创建的资产包
    """
    
    package = {
        'asset_package_id': generate_package_id(),
        'scene_name': extract_scene_name(scene_data),
        'inheritance_level': determine_inheritance_level(scene_data),
        'assets': extract_assets_from_scene(scene_data),
        'inheritance_rules': generate_inheritance_rules(scene_data),
        'v4_1_optimizations': {
            'strategy_tags': v4_1_config.get('strategy_tags', []),
            'complexity_threshold': v4_1_config.get('complexity_threshold', 2.5),
            'visual_thickening_level': v4_1_config.get('visual_thickening_level', 'medium'),
            'inheritance_priority': calculate_priority(scene_data),
            'asset_coverage': calculate_coverage(scene_data)
        }
    }
    
    return package
```

### 资产包存储与检索
1. **存储位置**：`outputs/asset-packages/`
2. **命名规则**：`asset-package-{场景名}-{时间戳}.json`
3. **索引文件**：`outputs/asset-packages/index.json`
4. **检索逻辑**：基于场景名称、策略标签、复杂度评分

## 集成到工作流程

### 节拍拆解阶段
1. 识别场景类型和环境需求
2. 创建或匹配环境资产包
3. 记录资产包引用

### 九宫格生成阶段
1. 继承环境资产包
2. 应用视觉增厚
3. 生成包含环境细节的画面描述

### 四宫格裂变阶段
1. 保持环境一致性
2. 根据镜头运动调整环境视角
3. 确保跨板环境连贯性

## V4.1优化配置

在`.agent-state.json`中添加：
```json
{
  "projectConfig": {
    "asset_package_config": {
      "enabled": true,
      "auto_create_packages": true,
      "default_thickening_level": "medium",
      "inheritance_threshold": 60,
      "storage_path": "outputs/asset-packages/",
      "index_update_frequency": "per_episode"
    }
  }
}
```

## 质量检查清单

### 资产包创建检查
- [ ] 空间骨架完整定义
- [ ] 材质皮肤详细描述
- [ ] 光影氛围明确设置
- [ ] 动态元素合理添加
- [ ] V4.1优化字段完整

### 继承检查
- [ ] 匹配度计算正确
- [ ] 继承深度合理
- [ ] 视觉增厚应用适当
- [ ] 环境一致性保持

### 性能指标
- **资产包覆盖率**：≥85%
- **继承匹配度**：≥70%
- **视觉增厚效果**：画面丰富度提升≥40%
- **环境一致性**：跨节拍一致性≥90%

---

**使用说明**：
1. 在节拍拆解时调用`create_asset_package()`创建资产包
2. 在九宫格生成时调用`inherit_environment_assets()`继承资产包
3. 在四宫格裂变时确保环境一致性
4. 通过配置调整资产包参数

---

## V5.0优化（环境信息内嵌机制）

### 优化背景
V5.0版本引入环境信息内嵌机制，以减少输出文件大小和Token消耗，同时保持文生图所需的所有信息完整性。

### 优化策略
| 优化项 | V4.1及之前 | V5.0 | 改善 |
|--------|-----------|-------|------|
| **环境展示方式** | 独立字段（环境资产包+环境构造+画面描述） | 内嵌到画面描述 | 减少60-70%重复 |
| **信息完整性** | 三个字段重复信息 | 单个字段完整信息 | 保持100% |
| **文件大小** | ~30KB（九宫格）/ ~25KB（四宫格） | ~10KB（九宫格）/ ~8KB（四宫格） | 减少67% |
| **可读性** | 信息分散，需跨字段查看 | 信息集中，一目了然 | 提升 |

### 内嵌机制说明

#### 1. 环境信息内嵌规则
**V4.1及之前**（三段式）：
```markdown
#### 环境资产包
- **空间骨架**：热闹的宋代集市广场...
- **材质皮肤**：厚重木质案板...
- **光影系统**：阳光明媚，暖黄色调...

#### 环境构造
- **空间骨架**：开阔集市广场...
- **前景层**：案板上堆叠的鲜红色精肉金字塔...
- **中景层**：镇关西肥硕身躯运刀如风...
- **背景层**：熙熙攘攘的宋代集市...
- **天空层**：晴朗蓝天点缀白云...

#### 画面描述
阳光明媚的宋代集市广场上，暖黄色调笼罩整个热闹场景...
```

**V5.0**（内嵌式）：
```markdown
#### 画面描述（V5.0优化版 - 环境信息已内嵌）
阳光明媚的宋代集市广场上，暖黄色调笼罩整个热闹场景。画面中央偏右是一张厚重的深棕色木质肉铺案板，布满深深刀痕和暗红色肉油痕迹。案板上堆叠鲜红色精肉金字塔，镇关西肥硕身躯运刀如风，鲁达魁梧身形坐在左侧板凳上。背景是熙熙攘攘的宋代集市，皮克斯风格，圆润造型，鲜艳明快色彩。
```

#### 2. 内嵌信息映射表
| 环境维度 | V4.1字段 | V5.0内嵌位置 | 示例 |
|----------|----------|---------------|------|
| **空间骨架** | 环境资产包/空间骨架 | 画面描述开头 | "阳光明媚的宋代集市广场上..." |
| **材质细节** | 环境构造/材质 | 融合到主体描述中 | "...布满深深刀痕和暗红色肉油痕迹" |
| **光影基调** | 环境资产包/光影系统 | 融合到环境描述中 | "...暖黄色调笼罩整个热闹场景" |
| **动态元素** | 环境构造/动态元素 | 融合到氛围描述中 | "...镇关西肥硕身躯运刀如风" |
| **镜头参数** | 独立字段 | 保留为元数据行 | **镜头**：全景｜推拉｜平静转紧张 |
| **风格标签** | 独立字段 | 保留为元数据行 | **风格标签**：皮克斯，热闹集市，圆润造型 |

#### 3. 继承记录简化
**V4.1及之前**：
```markdown
**继承记录**：
- 原九宫格：格01（节拍1）- 特级关键帧
- 环境构造：热闹宋代集市，阳光明媚，暖色调
- 导演审核：✅ 无问题
- 引擎输出：蒙太奇逻辑-单镜头固定，全景展示集市，置信度85%
- 置信度：85%
```

**V5.0**：
```markdown
*继承自九宫格Board01格01（置信度85%，引擎摘要：蒙太奇逻辑-单镜头固定，全景展示集市）*
```

### 向后兼容性

#### 1. 旧版文件读取
- ✅ 旧版九宫格/四宫格文件仍可正常读取
- ✅ 系统自动识别文件格式版本
- ✅ 支持V4.1和V5.0文件同时存在

#### 2. 资产包API兼容
所有资产包API保持不变：
```python
# V4.1 API（继续支持）
asset_package = create_asset_package(scene_data, v4_1_config)
inherited = inherit_environment_assets(target_beat, available_packages)

# V5.0 API（新增可选参数）
asset_package_v5 = create_asset_package(scene_data, v5_0_config, embed_mode=True)
```

#### 3. 配置兼容
```json
{
  "projectConfig": {
    "asset_package_config": {
      "enabled": true,
      "embed_mode": true,  // V5.0新增：启用内嵌模式
      "legacy_mode": false  // V5.0新增：禁用旧版三段式
    }
  }
}
```

### 迁移指南

#### 从V4.1迁移到V5.0
1. **更新模板文件**：使用新的beat-board-template.md和sequence-board-template.md
2. **更新SKILL配置**：启用V5.0强制精简步骤
3. **更新工作流**：使用新的workflow文档
4. **测试验证**：生成新样本，对比优化效果

#### 渐进式迁移
- **阶段1**：新项目使用V5.0模板
- **阶段2**：现有项目逐步迁移
- **阶段3**：全系统统一V5.0

---

**V5.0优化总结**：
- ✅ 删除冗余字段，减少60-70%Token
- ✅ 强制执行精简算法，提升15-20%精简率
- ✅ 保持信息完整性，不影响文生图质量
- ✅ 提升可读性，信息集中展示
- ✅ 向后兼容，支持渐进迁移