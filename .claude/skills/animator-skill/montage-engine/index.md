# 蒙太奇引擎模块索引

## 模块概述
蒙太奇引擎（Montage Engine）是animator-skill的核心创意组件，负责分析戏剧权重、生成节奏曲线、提供创意建议，为动态提示词生成提供完整的蒙太奇逻辑支持。

## 模块结构

```
montage-engine/
├── index.md                    # 本文件 - 模块索引和入口
├── montage-analysis.md         # 蒙太奇分析模块
├── rhythm-curve-generator.md   # 节奏曲线生成器
└── creative-suggestions.md      # 创意建议模块
```

## 核心功能矩阵

| 模块 | 主要功能 | 输入数据 | 输出数据 | 应用场景 |
|------|----------|----------|----------|----------|
| **montage-analysis** | 戏剧权重分析、镜头拆解、三段式拆解 | 四宫格序列、节拍情绪曲线、视觉风格 | 权重分配、拆解方案、置信度 | 运动类型选择、节奏基准 |
| **rhythm-curve-generator** | 情绪曲线分析、节奏模式识别、时间分配 | 节拍情绪数据、镜头权重、视觉风格 | 节奏曲线、时间分配、动态参数 | 节奏控制、速度设计 |
| **creative-suggestions** | 运动类型匹配、环境互动创意、风格化处理 | 蒙太奇分析、节奏曲线、风格定义 | 创意方案、互动设计、风格指导 | 五模块构造、氛围强化 |

## 使用流程

### 标准调用流程
```python
# 1. 蒙太奇分析
montage_result = montage_analysis.analyze(
    sequence_data=sequence_board_prompt,
    emotion_curve=beat_breakdown,
    visual_style=beat_board_prompt
)

# 2. 节奏曲线生成
rhythm_result = rhythm_generator.generate(
    emotion_data=montage_result.emotion_data,
    shot_weights=montage_result.weights,
    visual_style=beat_board_style
)

# 3. 创意建议生成
creative_result = creative_suggestions.generate(
    montage_data=montage_result,
    rhythm_data=rhythm_result,
    style_definition=beat_board_style
)
```

### 整合输出格式
```json
{
  "montage_engine_result": {
    "scene_id": "场景标识",
    "timestamp": "生成时间",
    "confidence_level": "整体置信度",
    "montage_analysis": "蒙太奇分析结果",
    "rhythm_curve": "节奏曲线数据", 
    "creative_suggestions": "创意建议方案",
    "integration_score": "整合质量评分"
  }
}
```

## 质量保证

### 模块间一致性检查
- **数据格式统一**：所有模块采用统一的数据格式
- **时间轴同步**：确保时间信息在模块间准确传递
- **权重一致性**：确保权重分配在所有模块中保持一致
- **风格连续性**：确保视觉风格在创意中得到贯彻

### 质量标准
- **整体置信度**：≥85%
- **模块一致性**：≥90%
- **数据完整性**：100%
- **风格适配性**：≥95%

## 集成指南

### 在animator-skill中的集成
```markdown
## 第一步：创意引擎调用
调用 montage-engine/ 模块：
1. montage-analysis.md → 获取戏剧权重和拆解建议
2. rhythm-curve-generator.md → 获取节奏曲线和时间分配  
3. creative-suggestions.md → 获取运动类型和环境互动创意

输出：完整的创意分析报告，包括：
- 每个镜头的运动类型建议
- 详细的节奏控制参数
- 环境互动的具体方案
- 风格化处理的指导建议
```

### 输出应用
蒙太奇引擎的输出直接应用到动态提示词的五模块构造：

1. **镜头运动模块** → 使用creative-suggestions的运动类型
2. **主体动作模块** → 基于montage-analysis的拆解建议
3. **环境动态模块** → 使用creative-suggestions的互动创意
4. **节奏控制模块** → 使用rhythm-curve-generator的参数
5. **氛围强化模块** → 使用creative-suggestions的风格方案

## 错误处理

### 常见错误及解决方案
1. **输入数据缺失**：
   - 检查前置产物是否完整
   - 使用默认值补充缺失数据
   - 记录警告信息

2. **置信度过低**：
   - 重新执行分析流程
   - 调整分析参数
   - 启动紧急创意模式

3. **模块冲突**：
   - 检查数据格式一致性
   - 执行冲突解决协议
   - 记录冲突处理结果

### 回退机制
- **单模块回退**：当某个模块失败时，其他模块继续执行
- **功能降级**：使用简化版本的分析结果
- **手动干预**：提供手动调整接口

## 性能优化

### 缓存策略
- **结果缓存**：缓存相同输入的分析结果
- **部分结果重用**：重用模块间的共同计算结果
- **增量更新**：只更新变化的部分

### 并行处理
- **模块并行**：支持模块间的并行计算
- **数据流水线**：建立数据处理的流水线
- **批处理**：支持批量处理多个镜头

---

*蒙太奇引擎遵循 ANINEO V2.0 创意引擎系统标准*  
*版本：2.0 | 更新时间：2026-01-24*