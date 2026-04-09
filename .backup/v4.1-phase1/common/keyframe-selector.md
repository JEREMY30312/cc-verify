# 关键帧选择器 Keyframe Selector

[功能]
    根据导演预设参数和关键帧等级，选择入选九宫格的关键帧

[导演裁量参数]
    yaml
    director_settings:
      include_high_level: true      # 是否包含高级关键帧
      include_medium_level: false   # 是否包含中级关键帧
      max_frames_per_board: 9       # 每板最大关键帧数
      min_frames_per_episode: 10    # 每集最少关键帧数

[基础入选规则]
    python
    def select_keyframes(beat_table, director_settings):
        selected_frames = []
        
        for beat in beat_table:
            # 1. 特级关键帧自动入选（最高优先级）
            if beat.keyframe_level == "🔴":
                selected_frames.append(beat)
            
            # 2. 高级关键帧：根据导演预设参数决定
            elif beat.keyframe_level == "🟠":
                if director_settings.include_high_level:
                    selected_frames.append(beat)
            
            # 3. 中级关键帧：根据导演预设参数决定
            elif beat.keyframe_level == "🟡":
                if director_settings.include_medium_level:
                    selected_frames.append(beat)
            
            # 4. 导演手动添加的关键帧
            if beat.id in director_manual_additions:
                selected_frames.append(beat)
        
        return selected_frames
    
    ## 基于蒙太奇标签的选帧逻辑（第三阶段新增）

### 概述
根据节拍的综合权重和特征，选择最代表性的关键帧画面。

### 基于策略标签的选帧逻辑（新增）

| 核心策略 | 辅助信息类型 | 优选帧选择 | 理由 |
|----------|--------------|------------|------|
| [动势组:关键动作] | 无 | 落幅（动作结果） | 准确动势组逻辑 |
| [动势组:关键动作] | [内含:对话铺垫→动作爆发] | 起幅或对话帧 | 需要体现铺垫部分 |
| [蒙太奇组:组名] | 无 | 动作帧 | 标准三段式逻辑 |
| [蒙太奇组:组名] | [内含:情绪转折] | 情绪转折帧 | 体现变化点 |
| [长镜头:调度描述] | - | 高潮节点 | 选取关键姿势 |

### 新增规则

**复杂度评分影响（新增）**：
- 复杂度评分 ≥ 4.0：需要特别强调关键信息点
- 复杂度评分 2.5-3.9：标准选帧逻辑
- 复杂度评分 < 2.5：简化处理，选择最具代表性的一帧

### 算法

```python
def select_primary_frame(beat):
    strategy = beat.montage_strategy
    
    if strategy == "单镜":
        return beat.full_description  # 唯一帧
    
    elif strategy == "动势组":
        # 分析是恐怖片还是其他类型
        if project_config.genre == "horror":
            return extract_start_frame(beat)  # 起幅保留悬念
        else:
            return extract_end_frame(beat)    # 落幅展现结果
    
    elif strategy == "长镜头":
        return extract_climax_moment(beat)  # 高潮节点
    
    elif strategy == "蒙太奇组":
        return extract_execution_frame(beat)  # 动作帧
    
    else:
        # 默认：选择综合权重最高的描述部分
        return select_by_weight(beat)
```

### 与现有规则集成

在原有的权重选择基础上，增加蒙太奇策略优先级：

1. 首先根据蒙太奇标签确定优选策略
2. 如果优选策略无法应用，则回退到权重选择
3. 记录选择理由供审核参考

### 示例

节拍描述："鲁达冲向镇关西，一拳击中其面部"

蒙太奇标签：[动势组:冲拳]

优选策略：落幅（非恐怖片）

选中画面："鲁达拳头击中镇关西面部的瞬间，面部肌肉变形"

### 配置选项

```json
{
  "projectConfig": {
    "keyframe_selection_mode": "smart",  // smart/weight_only
    "horror_mode_keep_suspense": true
  }
}
```

    [多维信息传递结构]
    每个入选的关键帧携带以下信息：

    | 信息维度 | 字段 | 传递给四宫格的用途 |
    |----------|------|-------------------|
    | 叙事功能 | 世界观建立/诱因事件/高潮对抗等 | 指导镜头设计的方向和重点 |
    | 节拍类型 | 重大动作/情绪转折等 | 决定镜头运动和节奏 |
    | 情绪基调 | 紧张/悲伤/喜悦等 | 指导光影和色彩设计 |
    | 视觉复杂度 | 低/中/高 | 决定制作资源分配 |
    | 关键帧等级 | 🔴/🟠/🟡/🔵/⚪ | 优先级标记 |
    | 扩展建议 | 动作分解/情绪过渡/环境展开 | 具体制作指示 |

[使用方式]
    直接读取此文件，按步骤执行关键帧选择逻辑
