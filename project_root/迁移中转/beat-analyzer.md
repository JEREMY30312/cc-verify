# 节拍分析器 Beat Analyzer

[功能]
    分析剧本节拍结构，识别关键帧等级和叙事功能

[输入数据]
    - 剧本内容
    - 节拍拆解表（如果有）

[输出数据]
    - 节拍列表（id, 幕次, 场景, 节拍描述, 关键帧等级）
    - 关键帧等级：🔴/🟠/🟡/🔵/⚪
    - 叙事功能：世界观建立/诱因事件/高潮对抗/危机低谷等
    - 节拍类型：重大动作/情绪转折/氛围转换/重要对话/过渡节拍
    - 情绪基调：紧张/悲伤/喜悦等
    - 综合权重（表现权重 × 基重）

[三幕结构比例]
    - 第一幕：15-25% (铺垫、激励事件)
    - 第二幕：50-70% (发展、转折、中点)
    - 第三幕：15-25% (高潮、结局)

[戏剧权重判定标准表]

## 事件类型到目标综合权重映射表

    | 事件类型 | 描述 | 目标综合权重范围 | 触发关键词 | 说明 |
    |----------|------|------------------|------------|------|
    | 生死攸关 | 涉及生命威胁的关键事件 | 3.0-4.0 | 死/杀/危险/致命/救命 | 最高优先级，必须重点表现 |
    | 核心转折 | 故事方向根本性改变 | 2.5-3.5 | 发现/真相/背叛/反转/选择 | 叙事核心，需要突出强调 |
    | 高强度动作 | 战斗、追逐、大场面动作 | 2.0-3.0 | 战斗/追逐/爆炸/打斗/逃跑 | 视觉冲击力强，需要动态表现 |
    | 情感高潮 | 强烈情绪爆发点 | 1.5-2.5 | 哭/笑/怒/告白/决裂/拥抱 | 情感核心，需要细腻表现 |
    | 关键决策 | 角色重要选择时刻 | 1.3-2.0 | 决定/选择/承诺/放弃/接受 | 角色发展关键点 |
    | 重要对话 | 推动剧情的关键对话 | 1.2-1.8 | 说/告诉/回答/问/解释 | 信息传递核心 |
    | 氛围转换 | 场景、时间、情绪转换 | 1.0-1.5 | 切换/转换/进入/离开/开始 | 结构连接点 |
    | 过渡铺垫 | 纯粹的连接性内容 | 0.5-1.0 | 走/看/想/等/准备 | 基础叙事功能 |

## 类型化修正系数表

    | 影片类型 | 动作节拍系数 | 对话节拍系数 | 情绪转折系数 | 适用说明 |
    |----------|--------------|--------------|--------------|----------|
    | 动作片   | ×1.5         | ×0.8         | ×1.2         | 强调视觉冲击和动态表现 |
    | 悬疑片   | ×1.0         | ×1.3         | ×1.5         | 强调对话逻辑和心理张力 |
    | 爱情片   | ×0.7         | ×1.4         | ×1.6         | 强调情感表达和细腻互动 |
    | 喜剧片   | ×1.0         | ×1.2         | ×1.3         | 强调节奏控制和反差效果 |
    | 恐怖片   | ×1.2         | ×1.1         | ×1.4         | 强调氛围营造和惊吓效果 |
    | 文艺片   | ×0.6         | ×1.5         | ×1.7         | 强调深度思考和情感表达 |
    | 纪录片   | ×0.5         | ×1.6         | ×1.2         | 强调真实性和信息传递 |

## 权重计算算法（V4.1优化版）

### 核心计算公式【V4.1优化】

```
最终权重 = (表现权重 × 基重) × 类型系数 × 复杂度系数

其中：
1. 表现权重 = 目标综合权重 ÷ 叙事功能基重
2. 基重 = 叙事功能的基础重要性（0.5-2.0）
3. 类型系数 = 根据影片类型和节拍类型确定（见类型化修正系数表）
4. 复杂度系数 = 1.0 + (复杂度评分 - 2.5) × 0.2
```

### 事件类型权重映射表【V4.1优化】

| 事件类型 | 目标权重范围 | 中点值 | 优先级 | 适用策略标签 |
|----------|--------------|--------|--------|--------------|
| 生死攸关 | 3.0-4.0 | 3.5 | 🔴 特级 | `[蒙太奇组]`, `[长镜头]` |
| 核心转折 | 2.5-3.5 | 3.0 | 🔴 特级 | `[蒙太奇组]`, `[动势组]` |
| 高强度动作 | 2.0-3.0 | 2.5 | 🟠 高级 | `[动势组]`, `[蒙太奇组]` |
| 情感高潮 | 1.5-2.5 | 2.0 | 🟠 高级 | `[单镜]`, `[特写]`, `[蒙太奇组]` |
| 关键决策 | 1.3-2.0 | 1.65 | 🟡 中级 | `[单镜]`, `[中景]` |
| 重要对话 | 1.2-1.8 | 1.5 | 🟡 中级 | `[单镜]`, `[中景]` |
| 氛围转换 | 1.0-1.5 | 1.25 | 🔵 低级 | `[环境]`, `[全景]` |
| 过渡铺垫 | 0.5-1.0 | 0.75 | ⚪ 基础 | `[单镜]`, `[环境]` |

### 类型化修正系数表【V4.1优化】

| 影片类型 | 动作系数 | 对话系数 | 情绪系数 | 环境系数 | 说明 |
|----------|----------|----------|----------|----------|------|
| 动作/冒险 | 1.5 | 0.8 | 1.2 | - | 强调视觉冲击和动态表现 |
| 悬疑/惊悚 | 1.0 | 1.5 | 1.5 | 1.3 | 强调信息揭露和心理张力 |
| 爱情/剧情 | 0.7 | 1.4 | 1.6 | 1.2 | 强调情感表达和细腻互动 |
| 喜剧 | 1.0 | 1.3 | 1.4 | 1.1 | 强调节奏控制和反差效果 |
| 恐怖 | 1.2 | 1.1 | 1.4 | 1.5 | 强调氛围营造和惊吓效果 |
| 艺术/文艺 | 0.6 | 1.5 | 1.7 | 1.4 | 强调深度思考和情感表达 |
| 纪录片 | 0.5 | 1.6 | 1.2 | 1.8 | 强调真实性和信息传递 |

### 复杂度评分与策略映射【V4.1新增】

| 复杂度范围 | 策略建议 | 格子数建议 | 镜头运动建议 |
|------------|----------|------------|--------------|
| < 2.0 | `[单镜]`, `[环境]` | 1格 | 固定镜头 |
| 2.0-2.9 | `[动势组]`, `[中景]` | 2格 | `[推拉]`, `[摇移]` |
| 3.0-3.9 | `[蒙太奇组]` | 3格 | `[跟拍]`, `[升降]` |
| ≥ 4.0 | `[长镜头]`, `[蒙太奇组]` | 3-4格 | 复合运动 |

### 权重计算算法实现【V4.1优化】

```python
def calculate_final_weight_v4_1(event_type, genre, narrative_function, complexity_score, project_config):
    """
    V4.1优化版权重计算算法（Phase 2.3集成类型化修正）
    
    参数:
        event_type: 事件类型（生死攸关、核心转折等）
        genre: 影片类型（action, suspense, romance等）
        narrative_function: 叙事功能对象，包含基重值
        complexity_score: 复杂度评分（1.0-5.0）
        project_config: 项目配置，包含影片类型等（Phase 2.3新增）
    
    返回:
        final_weight: 最终综合权重
        strategy_tags: 推荐策略标签列表
        suggested_grids: 建议格子数
        weight_modification: 类型化修正记录（Phase 2.3新增）
    """
    
    # 1. 获取影片类型（Phase 2.3新增）
    if project_config and hasattr(project_config, 'genre'):
        genre = project_config.genre
    elif not genre:
        genre = 'action'  # 默认类型
    
    # 2. 获取基础目标权重（使用中点值）
    target_weights = {
        '生死攸关': 3.5,
        '核心转折': 3.0,
        '高强度动作': 2.5,
        '情感高潮': 2.0,
        '关键决策': 1.65,
        '重要对话': 1.5,
        '氛围转换': 1.25,
        '过渡铺垫': 0.75
    }
    
    base_weight = target_weights.get(event_type, 1.0)
    
    # 3. 计算表现权重
    performance_weight = base_weight / narrative_function.weight
    performance_weight = max(0.2, min(2.0, performance_weight))  # 钳制在0.2-2.0
    
    # 4. 应用类型系数（Phase 2.3强化）
    genre_coefficients = {
        'action': {'action': 1.5, 'dialogue': 0.8, 'emotion': 1.2, 'environment': 1.0},
        'suspense': {'action': 1.0, 'dialogue': 1.5, 'emotion': 1.5, 'environment': 1.3},
        'romance': {'action': 0.7, 'dialogue': 1.4, 'emotion': 1.6, 'environment': 1.2},
        'comedy': {'action': 1.0, 'dialogue': 1.3, 'emotion': 1.4, 'environment': 1.1},
        'horror': {'action': 1.2, 'dialogue': 1.1, 'emotion': 1.4, 'environment': 1.5},
        'art': {'action': 0.6, 'dialogue': 1.5, 'emotion': 1.7, 'environment': 1.4},
        'documentary': {'action': 0.5, 'dialogue': 1.6, 'emotion': 1.2, 'environment': 1.8}
    }
    
    # 确定节拍类型对应的系数键
    if event_type in ['生死攸关', '高强度动作']:
        coeff_key = 'action'
    elif event_type in ['重要对话', '关键决策']:
        coeff_key = 'dialogue'
    elif event_type in ['情感高潮', '核心转折']:
        coeff_key = 'emotion'
    else:
        coeff_key = 'environment'
    
    genre_coeff = genre_coefficients.get(genre, genre_coefficients['action'])[coeff_key]
    
    # 5. 生成类型化修正记录（Phase 2.3新增）
    genre_modification_reasons = {
        'action': {
            'action': '动作片类型，重大动作节拍应用×1.5系数',
            'dialogue': '动作片类型，对话节拍应用×0.8系数（降权）',
            'emotion': '动作片类型，情绪转折应用×1.2系数',
            'environment': '动作片类型，环境节拍应用×1.0系数'
        },
        'suspense': {
            'action': '悬疑片类型，动作节拍应用×1.0系数',
            'dialogue': '悬疑片类型，重要对话应用×1.5系数',
            'emotion': '悬疑片类型，情绪转折应用×1.5系数',
            'environment': '悬疑片类型，环境节拍应用×1.3系数'
        },
        'romance': {
            'action': '爱情片类型，重大动作节拍应用×0.7系数（降权）',
            'dialogue': '爱情片类型，重要对话应用×1.4系数',
            'emotion': '爱情片类型，情绪转折应用×1.6系数',
            'environment': '爱情片类型，环境节拍应用×1.2系数'
        },
        'comedy': {
            'action': '喜剧片类型，重大动作节拍应用×1.0系数',
            'dialogue': '喜剧片类型，重要对话应用×1.3系数',
            'emotion': '喜剧片类型，情绪转折应用×1.4系数',
            'environment': '喜剧片类型，环境节拍应用×1.1系数'
        },
        'horror': {
            'action': '恐怖片类型，重大动作节拍应用×1.2系数',
            'dialogue': '恐怖片类型，重要对话应用×1.1系数',
            'emotion': '恐怖片类型，情绪转折应用×1.4系数',
            'environment': '恐怖片类型，环境节拍应用×1.5系数'
        },
        'art': {
            'action': '艺术片类型，重大动作节拍应用×0.6系数（降权）',
            'dialogue': '艺术片类型，重要对话应用×1.5系数',
            'emotion': '艺术片类型，情绪转折应用×1.7系数',
            'environment': '艺术片类型，环境节拍应用×1.4系数'
        },
        'documentary': {
            'action': '纪录片类型，重大动作节拍应用×0.5系数（降权）',
            'dialogue': '纪录片类型，重要对话应用×1.6系数',
            'emotion': '纪录片类型，情绪转折应用×1.2系数',
            'environment': '纪录片类型，环境节拍应用×1.8系数'
        }
    }
    
    modification_reason = genre_modification_reasons.get(genre, {}).get(
        coeff_key, 
        f'{genre}类型，应用×{genre_coeff}系数'
    )
    
    # 6. 应用复杂度系数
    complexity_coeff = 1.0 + (complexity_score - 2.5) * 0.2
    complexity_coeff = max(0.8, min(1.5, complexity_coeff))  # 钳制在0.8-1.5
    
    # 7. 计算最终权重
    final_weight = (performance_weight * narrative_function.weight) * genre_coeff * complexity_coeff
    
    # 8. 生成策略建议
    strategy_tags = generate_strategy_suggestions(event_type, complexity_score, final_weight)
    suggested_grids = calculate_suggested_grids(strategy_tags, complexity_score)
    
    # 9. 组装类型化修正记录（Phase 2.3新增）
    weight_modification = {
        'base_weight': round(base_weight, 2),
        'performance_weight': round(performance_weight, 2),
        'genre': genre,
        'genre_coefficient': genre_coeff,
        'modification_reason': modification_reason,
        'complexity_coefficient': round(complexity_coeff, 2),
        'final_weight': round(final_weight, 2),
        'adjustment_direction': '提升' if genre_coeff > 1.0 else ('降权' if genre_coeff < 1.0 else '保持')
    }
    
    return {
        'final_weight': round(final_weight, 2),
        'performance_weight': round(performance_weight, 2),
        'genre_coefficient': genre_coeff,
        'complexity_coefficient': round(complexity_coeff, 2),
        'strategy_tags': strategy_tags,
        'suggested_grids': suggested_grids,
        'keyframe_level': determine_keyframe_level(final_weight),
        'weight_modification': weight_modification  # Phase 2.3新增
    }
```
        
        if genre in genre_modifiers:
            # 根据节拍类型选择修正系数
            if event_type in ['高强度动作', '生死攸关']:
                modifier = genre_modifiers[genre]['action']
            elif event_type in ['重要对话', '关键决策']:
                modifier = genre_modifiers[genre]['dialogue']
            else:
                modifier = genre_modifiers[genre]['emotion']
            
            base_target = base_target * modifier
            # 记录修正原因
            modification_reason = f"{genre_specific_modifiers[genre]['focus']}，{modifier}"
        else:
            modification_reason = "默认类型 (系数 × 1.0)"
        
        # 5. 计算最终权重（应用类型化修正）
        final_weight = base_target
        
        return performance_weight, final_weight
    ```

## 类型化修正系数（第三阶段新增）

    ### 概述
    根据影片类型自动调整权重计算算法，使权重计算更加精准，符合不同类型影片的叙事特点。

    ### 类型系数表

    | 影片类型 (Genre) | 关注点 (Focus) | 修正系数规则 (Modifier) |
    |-------------------|---------------|------------------------|
    | 动作/冒险 | 物理冲突 (Combat/Chase) | 若 Type=重大动作，系数 × 1.5 |
    | 悬疑/惊悚 | 信息揭露 (Reveal/Clue) | 若 Type=重要对话 或 Narrative=认知反转，系数 × 1.5 |
    | 爱情/剧情 | 情感互通 (Intimacy/Emotion) | 若 Type=情绪转折，系数 × 1.4；若 Type=重大动作，系数 × 0.8 (降权) |
    | 爽文/反转 | 打脸/反转 (Slap/Twist) | 若 Tone=爆发性，系数 × 2.0 (特级优先) |
    | 喜剧 | 反差/笑点 (Contrast/Punchline) | 若 Type=情绪转折且情绪基调包含"幽默"，系数 × 1.3 |
    | 艺术 | 唯美/意境 (Aesthetic/Mood) | 若 Type=情绪转折，系数 × 1.7；若 Type=重大动作，系数 × 0.6 (降权) |
    | 默认/其他 | 平衡叙事 | 无修正 (系数 × 1.0) |

    ### 计算公式更新

    **最终权重 = (表现权重 × 基重) × 类型系数**

    ### 执行逻辑

    1. 读取 `project_config.genre` 获取影片类型
    2. 根据节拍的"节拍类型"和"叙事功能"确定适用规则
    3. 应用对应的类型系数
    4. 记录修正原因（如："动作片类型，重大动作节拍，应用×1.5系数"）

    ### 集成示例

### 辅助函数实现【V4.1新增】

```python
def generate_strategy_suggestions(event_type, complexity_score, final_weight):
    """
    根据事件类型、复杂度和最终权重生成策略标签建议
    """
    strategies = []
    
    # 基础策略选择
    if complexity_score < 2.0:
        if event_type in ['氛围转换', '过渡铺垫']:
            strategies.append('[环境]')
        else:
            strategies.append('[单镜]')
    elif complexity_score < 3.0:
        strategies.append('[动势组]')
    elif complexity_score < 4.0:
        strategies.append('[蒙太奇组]')
    else:
        strategies.append('[长镜头]')
    
    # 根据事件类型添加特定策略
    if event_type in ['情感高潮', '关键决策']:
        strategies.append('[特写]')
    elif event_type in ['氛围转换']:
        strategies.append('[全景]')
    elif event_type in ['重要对话']:
        strategies.append('[中景]')
    
    # 根据权重添加镜头运动
    if final_weight >= 3.0:
        strategies.append('[推拉]')
        strategies.append('[升降]')
    elif final_weight >= 2.0:
        strategies.append('[摇移]')
    
    return strategies

def calculate_suggested_grids(strategy_tags, complexity_score):
    """
    根据策略标签和复杂度计算建议格子数
    """
    base_grids = 1
    
    # 根据策略确定基础格子数
    if '[蒙太奇组]' in strategy_tags:
        base_grids = 3
    elif '[动势组]' in strategy_tags:
        base_grids = 2
    elif '[长镜头]' in strategy_tags:
        base_grids = 3
    elif '[环境]' in strategy_tags and '[全景]' in strategy_tags:
        base_grids = 2
    
    # 复杂度调整
    if complexity_score >= 3.5:
        base_grids = min(base_grids + 1, 4)
    
    return base_grids

def determine_keyframe_level(final_weight):
    """
    根据最终权重确定关键帧等级
    """
    if final_weight >= 4.0:
        return '🔴 特级'
    elif final_weight >= 3.0:
        return '🟠 高级'
    elif final_weight >= 2.0:
        return '🟡 中级'
    elif final_weight >= 1.0:
        return '🔵 低级'
    else:
        return '⚪ 基础'
```

### V4.1权重计算优化总结

**优化点**：
1. **更精确的类型系数**：针对不同影片类型提供更细粒度的系数调整
2. **复杂度集成**：将复杂度评分直接纳入权重计算
3. **策略联动**：权重计算直接输出策略标签建议
4. **格子数建议**：根据权重和复杂度自动计算建议格子数
5. **向后兼容**：保持原有数据结构，新增优化字段

**配置驱动**：
所有参数均可通过 `.agent-state.json` 中的 `weight_config` 进行配置，支持动态调整。

    假设一个节拍：
    - 表现权重：2.0（重大动作）
    - 基重：1.8（诱因事件）

    计算过程：
    1. 基础综合权重 = 2.0 × 1.8 = 3.6
    2. 类型系数 = 1.5（动作片重大动作）
    3. 最终权重 = 3.6 × 1.5 = 5.4
    4. 关键帧等级：特级关键帧 (🔴)

    ### 配置选项

    可在 `.agent-state.json` 中配置：

    ```json
    {
    "projectConfig": {
        "genre": "action",
        "enable_genre_weighting": true,
        "genre_coefficient_override": null
    }
    }
    ```

    ### 向后兼容性

    - 未指定类型时，使用"默认"类型（系数×1.0）
    - 现有项目自动迁移：根据剧本内容推测类型或保持默认

## 关键词触发规则

    ### 自动检测流程
    1. **扫描场景描述字段**：使用正则表达式匹配关键词
    2. **识别事件类型**：根据关键词匹配确定最相关的事件类型
    3. **记录调整原因**：在日志中记录"检测到[关键词]，应用[事件类型]系数"
    4. **输出增强**：在节拍拆解表中新增"戏剧权重调整"列

    ### 关键词库（正则表达式匹配）
    - **生死攸关**: `(死|杀|危险|致命|救命|威胁|生命|存活)`
    - **核心转折**: `(发现|真相|背叛|反转|选择|改变|转折|关键)`
    - **高强度动作**: `(战斗|追逐|爆炸|打斗|逃跑|攻击|防御|动作)`
    - **情感高潮**: `(哭|笑|怒|告白|决裂|拥抱|亲吻|情感)`
    - **关键决策**: `(决定|选择|承诺|放弃|接受|拒绝|同意)`
    - **重要对话**: `(说|告诉|回答|问|解释|讨论|对话)`

## 降权规则

    ### 适用场景
    1. **重复性内容**：相同事件类型在短时间内重复出现
    2. **信息冗余**：场景描述包含过多重复信息
    3. **节奏问题**：节拍密度过高导致观众疲劳
    4. **逻辑矛盾**：场景描述与上下文明显矛盾

    ### 降权系数
    | 降权原因 | 降权系数 | 说明 |
    |----------|----------|------|
    | 重复出现（3次内） | ×0.9 | 相同事件类型在3个节拍内重复 |
    | 重复出现（3次以上） | ×0.7 | 相同事件类型连续出现3次以上 |
    | 信息冗余 | ×0.8 | 场景描述包含>30%重复信息 |
    | 节奏过密 | ×0.85 | 连续3个节拍都是高强度事件 |
    | 逻辑矛盾 | ×0.6 | 场景描述与上下文明显矛盾 |

    ### 降权应用规则
    1. **检测条件**：自动分析节拍序列和内容
    2. **应用时机**：在计算最终权重前应用降权系数
    3. **记录日志**：记录降权原因和系数
    4. **用户提示**：在输出中标记"建议优化：[降权原因]"
   

## 节拍分析逻辑扩展（新增）

    ### Step 0: 颗粒度重组（一拍一策强制拆分）
    **规则**：强制执行"一拍一策"原则。如果在同一时间段内既有【对话】又有【高强度动作】，必须拆分为两个独立的节拍编号。

    ### 策略标签定义

    | 标签类型   | 格式                    | 适用场景         | 判定条件                           |
    |------------|-------------------------|------------------|------------------------------------|
    | 单镜     | `[单镜:场景类型]`         | 对话、静态情感      | 主要是对话，无大幅度动作               |
    | 动势组     | `[动势组:关键动作]`        | 追逐、移动、快速动作 | 包含强方向性动词（冲向、逃离）          |
    | 长镜头     | `[长镜头:调度描述]`        | 连续动作、空间展示   | 包含3个以上连续微动作                |
    | 蒙太奇组   | `[蒙太奇组:组名]`          | 时间压缩、情绪渲染   | 包含空间转移或时间流逝描述            |
    | 正反打     | `[正反打:对话方]`         | 对话戏、对抗戏      | 两人或多人对话，轮次≥2               |
    | 感官锚点   | `[感官:类型/强度]`        | 关键声效、视觉冲击   | 检测到感官关键词（爆炸、闪光等）          |

    **拆分算法**：
    ```python
    def enforce_one_beat_one_strategy(beat):
        if contains_dialogue(beat) and contains_intense_action(beat):
            return [
                {"type": "dialogue", "content": extract_dialogue_part(beat)},
                {"type": "action", "content": extract_action_part(beat)}
            ]
        if contains_space_jump(beat) or contains_time_jump(beat):
            return split_by_spatiotemporal_units(beat)
        return [beat]
    ```

    判定条件：
    - 对话密集且持续时间 > 15秒 → 拆分
    - 动作序列包含3个以上独立动作 → 拆分
    - 情感剧烈转折 → 拆分

    防呆机制：
    - 两个拆分后节拍权重都 < 0.5 → 合并
    - 拆分后导致叙事断裂 → 合并
    - 导演标记"不可拆分" → 不拆分

    ### Step 5: 分级策略诊断系统

    #### Step 5.1: 核心策略诊断（必须且唯一）【Phase 2.2 蒙太奇逻辑引擎权威化】
     
     **核心原则（Phase 2.2更新）**：
     - 每个节拍必须有且仅有一个核心策略标签，标识其主导拍摄框架
     - **策略标签生成逻辑必须基于蒙太奇逻辑分析结果**
     - 蒙太奇逻辑引擎拥有最高权威，冲突时优先采纳
     
     **策略类型与映射规则**：
     
     | 策略类型 | 格式                   | 蒙太奇逻辑建议            | 判定条件                        | 四宫格基础分配        |
     |----------|------------------------|------------------------|---------------------------------|---------------------|
     | 单镜     | `[单镜:场景类型]`        | 单镜头固定              | 无时空变化且有台词               | 1格（静态帧）         |
     | 动势组   | `[动势组:关键动作]`       | 动作序列/动态连续          | 有明确方向性动作（冲向、逃离）       | 2格（起幅+落幅）       |
     | 蒙太奇组 | `[蒙太奇组:组名]`        | 时间压缩/跳跃/快速切换      | 时空压缩/跳跃/快速切换            | 3格（三段式）         |
     | 长镜头   | `[长镜头:调度描述]`       | 连续空间调度            | 连续动作无剪辑点                 | 2-3格（关键节点）      |
     
     **蒙太奇逻辑到策略映射表**（Phase 2.2新增）：
     
     | 蒙太奇逻辑建议 | 映射策略标签 | 说明 |
     |----------------|-------------|------|
     | "单镜头" | `[单镜:场景类型]` | 蒙太奇建议单一固定镜头 |
     | "动作序列" | `[动势组:关键动作]` | 蒙太奇建议连续动作拆分 |
     | "时间压缩" | `[蒙太奇组:时间压缩]` | 蒙太奇建议压缩时间跨度 |
     | "时间跳跃" | `[蒙太奇组:时间跳跃]` | 蒙太奇建议跨越时间 |
     | "空间跳跃" | `[蒙太奇组:空间切换]` | 蒙太奇建议切换空间 |
     | "连续调度" | `[长镜头:调度描述]` | 蒙太奇建议连续调度 |
     | "情绪渲染" | `[蒙太奇组:情绪渲染]` | 蒙太奇建议多角度情绪表现 |
     
     **示例**：
     - `[单镜:两人对峙]` - 蒙太奇建议: "单镜头"
     - `[动势组:冲向门口]` - 蒙太奇建议: "动作序列"
     - `[蒙太奇组:闪回记忆]` - 蒙太奇建议: "时间跳跃"
     - `[长镜头:走廊追逐]` - 蒙太奇建议: "连续调度"
     
     **冲突处理机制**（Phase 2.2新增）：
     
     当其他引擎（如影视联想、环境分析）的建议与蒙太奇逻辑冲突时：
     
     ```python
     def resolve_strategy_conflict(montage_suggestion, other_engine_suggestions, beat_context):
         """
         解决策略冲突，蒙太奇逻辑优先
         
         参数:
             montage_suggestion: 蒙太奇逻辑的建议
             other_engine_suggestions: 其他引擎的建议列表
             beat_context: 节拍上下文
         
         返回:
             final_strategy: 最终采用的核心策略
             conflict_log: 冲突日志
         """
         
         conflict_log = []
         
         for engine_name, suggestion in other_engine_suggestions.items():
             if suggestion != montage_suggestion:
                 # 记录冲突
                 conflict_log.append({
                     'engine': engine_name,
                     'suggested': suggestion,
                     'conflict_with': '蒙太奇逻辑',
                     'montage_decision': montage_suggestion,
                     'resolution': '采用蒙太奇逻辑建议'
                 })
         
         # 蒙太奇逻辑拥有最高权威
         final_strategy = montage_suggestion
         
         return final_strategy, conflict_log
     ```
     
     **冲突日志格式**（Phase 2.2新增）：
     
     ```json
     {
       "beat_id": "7",
       "final_strategy": "[蒙太奇组:变脸]",
       "conflict_log": [
         {
           "engine": "影视联想",
           "suggested": "[单镜:特写]",
           "conflict_with": "蒙太奇逻辑",
           "montage_decision": "[蒙太奇组:变脸]",
           "resolution": "采用蒙太奇逻辑建议"
         },
         {
           "engine": "环境分析",
           "suggested": "[环境:餐厅]",
           "conflict_with": "蒙太奇逻辑",
           "montage_decision": "[蒙太奇组:变脸]",
           "resolution": "采用蒙太奇逻辑建议"
         }
       ]
     }
     ```
     
     **策略生成算法**（Phase 2.2更新）：
     
     ```python
     def generate_core_strategy_from_montage(montage_analysis_result, beat_context):
         """
         基于蒙太奇逻辑分析结果生成核心策略
         
         参数:
             montage_analysis_result: 蒙太奇逻辑引擎分析结果
             beat_context: 节拍上下文（场景描述、动作等）
         
         返回:
             core_strategy: 核心策略标签
             strategy_source: 策略来源标记
         """
         
         montage_suggestion = montage_analysis_result.get('shot_type', '未知')
         
         # 根据蒙太奇建议映射到策略标签
         strategy_mapping = {
             '单镜头': lambda ctx: f'[单镜:{extract_scene_type(ctx)}]',
             '动作序列': lambda ctx: f'[动势组:{extract_key_action(ctx)}]',
             '时间压缩': lambda ctx: '[蒙太奇组:时间压缩]',
             '时间跳跃': lambda ctx: '[蒙太奇组:时间跳跃]',
             '空间跳跃': lambda ctx: '[蒙太奇组:空间切换]',
             '连续调度': lambda ctx: f'[长镜头:{extract_shot_description(ctx)}]',
             '情绪渲染': lambda ctx: '[蒙太奇组:情绪渲染]'
         }
         
         # 生成策略标签
         if montage_suggestion in strategy_mapping:
             core_strategy = strategy_mapping[montage_suggestion](beat_context)
             strategy_source = '蒙太奇逻辑引擎（权威）'
         else:
             # 蒙太奇建议未知，回退到传统分析
             core_strategy = traditional_strategy_analysis(beat_context)
             strategy_source = '传统分析（蒙太奇建议不可用）'
         
         return core_strategy, strategy_source
     ```

    #### Step 5.2: 辅助信息识别（复杂节拍专用）
    **目的**：记录节拍内部复杂性和重要转折点，供四宫格参考。

    触发条件（满足任一）：
    - 包含明显转折词（突然、然而、但是）
    - 时长 > 8秒且层次丰富
    - 情绪剧烈变化
    - 包含高强度感官锚点

    格式：辅助信息: [内含:关键变化描述]

    示例：
    - [内含:对话铺垫→突然爆发]

    #### Step 5.3: 关键信息点提取（新增）
    **目的**：为四宫格拆解提供具体拆分锚点。

    提取规则：
    ```python
    def extract_key_points(scene_description, strategy):
        关键点 = []
        if strategy == "[动势组]":
            动作序列 = extract_action_sequence(scene_description)
            关键点.append({"类型": "动作开始", "内容": 动作序列[0]})
            关键点.append({"类型": "动作结束", "内容": 动作序列[-1]})
        elif strategy == "[蒙太奇组]":
            关键点.append({"类型": "起势", "内容": extract_setup_part(scene_description)})
            关键点.append({"类型": "动作", "内容": extract_action_part(scene_description)})
            关键点.append({"类型": "结果", "内容": extract_result_part(scene_description)})
        if contains_emotional_turn(scene_description):
            关键点.append({"类型": "情绪转折", "内容": extract_turn_point(scene_description)})
        return 关键点
    ```

    #### Step 5.4: 复杂度评估与建议格子数
    算法：
    ```
    复杂度评分 = 基础分 + 0.3×(关键点数量) + 0.5×(如有辅助信息) + 0.2×(潜台词数量) + 0.5×(感官锚点数量)
    建议格子数 = min(max(round(复杂度评分), 1), 4)
    ```
    输出：
    - 复杂度评分: X.X/5.0
    - 建议格子数: X格
    - 拆解建议: "建议拆为X格：..."

    #### Step 5.5: 完整输出格式
    在节拍拆解表中新增以下列：核心策略、辅助信息、关键信息点、复杂度评分、建议格子数、拆解建议

[节拍类型权重参考]
    | 节拍类型   | 表现权重 | 说明                     |
    |------------|----------|--------------------------|
    | 重大动作   | 2.0      | 战斗、追逐、大场面       |
    | 情绪转折   | 1.5      | 震惊、悲伤、喜悦高潮     |
    | 氛围转换   | 1.0      | 场景切换、时间跳跃       |
    | 重要对话   | 0.5      | 关键台词、揭露真相       |
    | 过渡节拍   | 0.2      | 连接性内容               |

[叙事功能基重参考]
    | 叙事功能             | 基重 | 说明                       |
    |----------------------|------|----------------------------|
    | 诱因事件             | 1.8  | 推动故事启动的关键事件     |
    | 高潮对抗             | 2.0  | 核心冲突的最终解决         |
    | 危机/低谷           | 1.7  | 主角最低点，情感压力最大   |
    | 中点升级/认知反转   | 1.6  | 故事方向或主角认知的根本转变 |
    | 第一次转折           | 1.5  | 第一幕转向第二幕的关键点   |
    | 结局/余韵           | 1.4  | 故事收尾，主题升华         |
    | 高潮前集结           | 1.3  | 最终决战前的准备           |
    | 主角现状与目标/缺口 | 1.2  | 建立主角起点与需求         |
    | 世界观/基调建立     | 1.1  | 建立故事世界规则与氛围     |
    | 过渡/连接内容       | 1.0  | 纯粹的连接性节拍           |

[综合权重计算公式]
    综合权重 = 表现权重 × 基重

    示例：
    - 重大动作 + 高潮对抗 = 2.0 × 2.0 = 4.0 → 🔴 特级
    - 情绪转折 + 中点反转 = 1.5 × 1.6 = 2.4 → 🟠 高级
    - 重要对话 + 诱因事件 = 0.5 × 1.8 = 0.9 → 🔵 普通
    - 过渡节拍 + 连接内容 = 0.2 × 1.0 = 0.2 → ⚪ 基础

[关键帧等级判断标准]
    | 等级 | 符号 | 综合权重范围 | 说明                     |
    |------|------|--------------|--------------------------|
    | 特级 | 🔴   | ≥3.0         | 故事核心节点，必须重点设计 |
    | 高级 | 🟠   | 2.0-2.9      | 重要转折点，需要突出表现   |
    | 中级 | 🟡   | 1.0-1.9      | 结构支撑点，需充分表现     |
    | 普通 | 🔵   | 0.5-0.9      | 标准叙事节拍             |
    | 基础 | ⚪   | <0.5         | 可简化或合并的过渡内容   |

## Step 0: 颗粒度重组前置处理器（Phase 2.1新增）

### 概述

**目的**: 实现一拍一策强制拆分，确保每个节拍对应单一策略，提高颗粒度和精确度。

**核心原则**: 
- 强制执行"一拍一策"原则
- 对话+动作混合 → 拆分
- 时空跳跃 → 拆分
- 防呆机制防止过度拆分

### 预处理函数实现

```python
def enforce_granularity_reorganization(original_beats, project_config):
    """
    颗粒度重组前置处理器
    
    参数:
        original_beats: 原始节拍列表
        project_config: 项目配置（包含导演标记、类型等）
    
    返回:
        reorganized_beats: 重组后的节拍列表，带子节拍编号
        reorganization_log: 拆分日志
    """
    
    reorganized_beats = []
    reorganization_log = []
    
    for beat in original_beats:
        # 步骤1: 检测条件扫描
        should_split, split_reasons, split_type = detect_split_conditions(beat)
        
        # 步骤2: 执行拆分决策
        if should_split and not beat.get('director_marked_unsplittable', False):
            # 执行拆分
            sub_beats = split_beat_by_strategy(beat, split_type, project_config)
            
            # 步骤3: 防呆机制检查
            merged_beats = apply_mechanism_to_prevent_over_splitting(sub_beats, beat)
            
            if merged_beats is None:
                # 拆分被防呆机制阻止
                reorganized_beats.append(beat)
                reorganization_log.append({
                    'beat_id': beat['id'],
                    'action': 'merge_back',
                    'reason': '防呆机制触发，已合并回原节拍',
                    'split_reasons': split_reasons
                })
            else:
                # 拆分成功
                reorganized_beats.extend(merged_beats)
                reorganization_log.append({
                    'beat_id': beat['id'],
                    'action': 'split',
                    'split_type': split_type,
                    'sub_beat_count': len(merged_beats),
                    'reason': split_reasons
                })
        else:
            # 不需要拆分或被导演标记为不可拆分
            reorganized_beats.append(beat)
            reorganization_log.append({
                'beat_id': beat['id'],
                'action': 'keep',
                'reason': '无需拆分' if not should_split else '导演标记"不可拆分"'
            })
    
    # 重新编号所有节拍
    reorganized_beats = renumber_beats_with_sub_beats(reorganized_beats)
    
    return reorganized_beats, reorganization_log


def detect_split_conditions(beat):
    """
    检测节拍是否需要拆分
    
    返回:
        should_split: 是否需要拆分
        split_reasons: 拆分原因列表
        split_type: 拆分类型
    """
    should_split = False
    split_reasons = []
    split_type = None
    
    scene_description = beat.get('scene_description', '')
    estimated_duration = beat.get('estimated_duration', 0)
    
    # 条件1: 对话密度检测
    dialogue_ratio = calculate_dialogue_ratio(scene_description)
    if dialogue_ratio > 0.3 and estimated_duration > 15:
        should_split = True
        split_reasons.append(f"对话密度{dialogue_ratio:.2%}且时长{estimated_duration}秒")
        split_type = 'dialogue_action'
    
    # 条件2: 动作密度检测
    action_verb_count = count_action_verbs(scene_description)
    if action_verb_count >= 3:
        should_split = True
        split_reasons.append(f"包含{action_verb_count}个独立动作动词")
        split_type = 'multi_action'
    
    # 条件3: 时空跳跃检测
    time_space_keywords = ['突然', '然而', '但是', '同时', '过了一会儿', '第二天', '那时']
    has_time_space_jump = any(keyword in scene_description for keyword in time_space_keywords)
    if has_time_space_jump:
        should_split = True
        split_reasons.append("检测到时空跳跃词，强制拆分")
        split_type = 'time_space_jump'
    
    # 条件4: 情感转折+动作混合
    has_emotion_shift = detect_emotion_shift(scene_description)
    has_action = has_action_content(scene_description)
    if has_emotion_shift and has_action:
        should_split = True
        split_reasons.append("情感转折+动作混合")
        split_type = 'emotion_action'
    
    return should_split, split_reasons, split_type


def split_beat_by_strategy(beat, split_type, project_config):
    """
    根据拆分类型执行拆分
    
    参数:
        beat: 原始节拍
        split_type: 拆分类型
        project_config: 项目配置
    
    返回:
        sub_beats: 子节拍列表
    """
    
    scene_description = beat.get('scene_description', '')
    
    if split_type == 'dialogue_action':
        # 对话+动作拆分
        sub_beats = split_dialogue_and_action(beat)
    elif split_type == 'multi_action':
        # 多动作拆分
        sub_beats = split_multi_actions(beat)
    elif split_type == 'time_space_jump':
        # 时空跳跃拆分
        sub_beats = split_by_time_space(beat)
    elif split_type == 'emotion_action':
        # 情感转折+动作拆分
        sub_beats = split_emotion_and_action(beat)
    else:
        # 默认不拆分
        sub_beats = [beat]
    
    return sub_beats


def split_dialogue_and_action(beat):
    """
    拆分对话+动作节拍
    
    输出: [对话部分] + [动作部分]
    策略: [正反打] + [动势组]
    """
    scene_description = beat.get('scene_description', '')
    
    # 分离对话和动作
    dialogue_part, action_part = separate_dialogue_action(scene_description)
    
    # 创建两个子节拍
    sub_beat_dialogue = beat.copy()
    sub_beat_dialogue['scene_description'] = dialogue_part
    sub_beat_dialogue['suggested_strategy'] = '[正反打:对话]'
    sub_beat_dialogue['beat_type'] = '对话节拍'
    sub_beat_dialogue['is_sub_beat'] = True
    sub_beat_dialogue['parent_beat_id'] = beat.get('id')
    
    sub_beat_action = beat.copy()
    sub_beat_action['scene_description'] = action_part
    sub_beat_action['suggested_strategy'] = '[动势组:动作]'
    sub_beat_action['beat_type'] = '动作节拍'
    sub_beat_action['is_sub_beat'] = True
    sub_beat_action['parent_beat_id'] = beat.get('id')
    
    return [sub_beat_dialogue, sub_beat_action]


def split_emotion_and_action(beat):
    """
    拆分情感转折+动作节拍
    
    输出: [情绪铺垫] + [动作执行]
    策略: [单镜] + [动势组]
    """
    scene_description = beat.get('scene_description', '')
    
    # 分离情感铺垫和动作执行
    emotion_part, action_part = separate_emotion_action(scene_description)
    
    # 创建两个子节拍
    sub_beat_emotion = beat.copy()
    sub_beat_emotion['scene_description'] = emotion_part
    sub_beat_emotion['suggested_strategy'] = '[单镜:情绪]'
    sub_beat_emotion['beat_type'] = '情绪铺垫'
    sub_beat_emotion['is_sub_beat'] = True
    sub_beat_emotion['parent_beat_id'] = beat.get('id')
    
    sub_beat_action = beat.copy()
    sub_beat_action['scene_description'] = action_part
    sub_beat_action['suggested_strategy'] = '[动势组:动作]'
    sub_beat_action['beat_type'] = '动作执行'
    sub_beat_action['is_sub_beat'] = True
    sub_beat_action['parent_beat_id'] = beat.get('id')
    
    return [sub_beat_emotion, sub_beat_action]


def apply_mechanism_to_prevent_over_splitting(sub_beats, original_beat):
    """
    防呆机制：防止过度拆分
    
    检查条件:
    1. 拆分后任一节拍权重 < 0.5 → 合并回原节拍
    2. 拆分导致叙事断裂 → 合并回原节拍
    3. 导演标记"不可拆分" → 跳过拆分
    
    返回:
        merged_beats: 合并后的节拍列表（如果不需要合并则返回None）
    """
    
    # 条件1: 检查权重
    for sub_beat in sub_beats:
        estimated_weight = estimate_beat_weight(sub_beat)
        if estimated_weight < 0.5:
            # 权重过低，合并回原节拍
            return None
    
    # 条件2: 检查叙事连贯性
    if check_narrative_continuity(sub_beats) < 0.6:
        # 叙事不连贯，合并回原节拍
        return None
    
    # 条件3: 检查导演标记（在调用函数前已经检查）
    if original_beat.get('director_marked_unsplittable', False):
        return None
    
    # 通过所有防呆检查，返回子节拍
    return sub_beats


def renumber_beats_with_sub_beats(beats):
    """
    重新编号节拍，支持子节拍编号
    
    示例: 1, 2a, 2b, 3, 4a, 4b, 4c, 5
    """
    renumbered_beats = []
    sub_beat_counter = {}
    
    for beat in beats:
        original_id = beat.get('id')
        
        if beat.get('is_sub_beat', False):
            # 子节拍
            parent_id = beat.get('parent_beat_id')
            if parent_id not in sub_beat_counter:
                sub_beat_counter[parent_id] = ord('a')
            
            sub_char = chr(sub_beat_counter[parent_id])
            new_id = f"{parent_id}{sub_char}"
            sub_beat_counter[parent_id] += 1
        else:
            # 主节拍
            new_id = str(original_id)
        
        beat['id'] = new_id
        renumbered_beats.append(beat)
    
    return renumbered_beats
```

### 检测条件详细规则

| 检测条件 | 触发阈值 | 拆分类型 | 策略分配 |
|----------|----------|----------|----------|
| 对话密度 > 30% 且时长 > 15秒 | 对话率 > 0.3 | dialogue_action | [正反打] + [动势组] |
| 包含3个以上独立动作动词 | 动作动词数 ≥ 3 | multi_action | [动势组] × 2 |
| 检测到时空跳跃词 | 发现"突然"/"然而"/"第二天"等 | time_space_jump | [蒙太奇组] |
| 情感转折 + 动作混合 | 检测到情绪转变且有动作 | emotion_action | [单镜] + [动势组] |

### 防呆机制详细规则

| 防呆条件 | 阈值 | 处理方式 |
|----------|------|----------|
| 子节拍权重过低 | 任一权重 < 0.5 | 合并回原节拍 |
| 叙事连贯性差 | 连贯性评分 < 0.6 | 合并回原节拍 |
| 导演标记 | director_marked_unsplittable = True | 跳过拆分 |
| 子节拍数量过多 | > 3个子节拍 | 合并部分子节拍 |

### 拆分日志格式

```json
{
  "total_beats": 10,
  "split_beats": 3,
  "kept_beats": 7,
  "split_ratio": 0.3,
  "reorganization_details": [
    {
      "beat_id": "1",
      "action": "split",
      "split_type": "dialogue_action",
      "sub_beat_count": 2,
      "reason": "对话密度35%且时长18秒",
      "sub_beats": ["1a", "1b"],
      "assigned_strategies": ["[正反打:对话]", "[动势组:动作]"]
    },
    {
      "beat_id": "3",
      "action": "keep",
      "reason": "无需拆分"
    },
    {
      "beat_id": "5",
      "action": "merge_back",
      "reason": "防呆机制触发，子节拍权重0.4过低",
      "split_reasons": ["包含4个独立动作动词"]
    }
  ]
}
```

---

[节拍分析执行步骤]

    步骤0: 颗粒度重组前置处理器（Phase 2.1新增）
          - 执行 enforce_granularity_reorganization() 函数
          - 应用一拍一策强制拆分原则
          - 检测条件：对话密度 > 30% 且时长 > 15秒、包含3个以上独立动作动词、时空跳跃
          - 拆分算法：对话+动作、情感转折+动作、多动作、时空跳跃
          - 防呆机制：权重 < 0.5、叙事断裂、导演标记"不可拆分"
          - 输出：重组后的节拍列表，带子节拍编号 (如 1a, 1b)
    
    步骤1: 识别最小叙事单元
         - 从剧本中识别独立的场景/事件
         - 每个节拍必须包含：
           * 场景描述：发生了什么
           * 角色行动：具体动作和意图
           * 情感表达：核心情绪\
  
    步骤2: 执行戏剧权重分析（新增）
         - 扫描场景描述，匹配关键词
         - 确定事件类型（来自戏剧权重判定标准表）
         - 应用类型修正系数（来自项目配置）
         - 计算目标综合权重

    步骤3: 标注节拍类型
         - 根据内容选择：重大动作/情绪转折/氛围转换/重要对话/过渡节拍
         - 自动获取表现权重（使用新算法）

    步骤4: 标注叙事功能
         - 根据故事结构位置选择功能
         - 参考基重表填写基重值

    步骤5: 计算综合权重（Phase 2.3 类型化修正集成）
         - 调用 calculate_final_weight_v4_1() 函数
         - 参数：事件类型、影片类型、叙事功能、复杂度评分、项目配置
         - 公式：综合权重 = 表现权重 × 基重 × 类型系数 × 复杂度系数
         - 类型系数：根据影片类型自动应用（动作片×1.5、爱情片×0.8等）
         - 复杂度系数：基于复杂度评分计算
         - 返回：最终权重、策略标签、建议格子数、类型修正记录
         - 示例：情感高潮(1.8) × 危机低谷(1.7) × 爱情片系数(1.6) = 4.90

    步骤6: 应用降权规则（新增）
         - 检查重复性、冗余性、节奏问题
         - 应用降权系数（如需要）
         - 记录降权原因

    步骤7: 确定关键帧等级
         - 根据综合权重确定等级：
           * ≥3.0 → 🔴 特级
           * 2.0-2.9 → 🟠 高级
           * 1.0-1.9 → 🟡 中级
           * 0.5-0.9 → 🔵 普通
           * <0.5 → ⚪ 基础

    步骤8: 分配三幕结构
         - 统计各幕节拍数量
         - 确保第一幕 15-25%
         - 确保第二幕 50-70%
         - 确保第三幕 15-25%
         - 如不符合，调整节拍分配

[节拍数量建议]
    - 最佳范围：8-12个
    - 短剧/短片：6-10个
    - 长篇电影：10-15个

[输出格式要求]
    每个节拍必须输出以下字段：
    - 节拍编号：按剧情顺序编号（1-N）
    - 场景描述：这个场景发生了什么
    - 镜头类型：全景/中景/近景/特写
    - 画面要素：主要视觉元素、角色、道具、环境
    - 情绪基调：平静/紧张/愤怒等
    - 节拍类型：从5种类型中选择
    - 事件类型：从戏剧权重判定标准表中选择（新增）
    - 表现权重：0.2-2.0（使用新算法计算）
    - 叙事功能：从10种功能中选择
    - 基重：1.0-2.0
    - 综合权重：表现权重 × 基重
    - 关键帧等级：🔴/🟠/🟡/🔵/⚪
    - 戏剧权重调整：检测到的关键词和调整原因（新增）
    - 降权标记：如有降权，记录原因和系数（新增）

[使用方式]
    直接读取此文件，按步骤执行节拍分析逻辑
    新增功能需要读取项目配置中的 genre 字段

---
