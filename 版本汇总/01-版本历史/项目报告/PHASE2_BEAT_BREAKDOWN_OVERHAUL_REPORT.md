# ANINEO Phase 2 节拍拆解引擎重构实施报告

**实施日期**: 2026-01-31  
**阶段名称**: 阶段二：节拍拆解引擎重构 (Phase 2 - Beat Breakdown Overhaul)  
**实施状态**: ✅ 全部完成（4个子阶段）

---

## 实施概览

本次Phase 2实施共完成 **4个子阶段**，涵盖颗粒度重组、蒙太奇逻辑权威化、类型化权重修正、拆解方案动态化。

### 实施阶段清单

| 阶段 | 名称 | 状态 | 备份目录 |
|------|------|------|----------|
| Phase 2.1 | 颗粒度重组前置处理器 | ✅ 完成 | `.backup/phase2-beat-breakdown-overhaul/` |
| Phase 2.2 | 蒙太奇逻辑引擎权威化 | ✅ 完成 | `.backup/phase2-beat-breakdown-overhaul/` |
| Phase 2.3 | 类型化权重修正集成 | ✅ 完成 | `.backup/phase2-beat-breakdown-overhaul/` |
| Phase 2.4 | 拆解方案模板动态化 | ✅ 完成 | `.backup/phase2-beat-breakdown-overhaul/` |

---

## 各阶段详细实施内容

### Phase 2.1: 颗粒度重组前置处理器 ✅

**目标**: 实现一拍一策强制拆分，提高颗粒度和精确度

**实施内容**:

#### 1. 新增Step 0章节

在 `beat-analyzer.md` 中新增"Step 0: 颗粒度重组前置处理器"章节，包含：

- **核心原则**: 强制执行"一拍一策"原则
- **检测条件**: 4种检测条件
- **拆分算法**: 4种拆分类型
- **防呆机制**: 3种防呆检查

#### 2. 实现预处理函数

新增 `enforce_granularity_reorganization()` 函数：

```python
def enforce_granularity_reorganization(original_beats, project_config):
    """颗粒度重组前置处理器"""
    # 步骤1: 检测条件扫描
    should_split, split_reasons, split_type = detect_split_conditions(beat)
    
    # 步骤2: 执行拆分决策
    if should_split:
        sub_beats = split_beat_by_strategy(beat, split_type, project_config)
    
    # 步骤3: 防呆机制检查
    merged_beats = apply_mechanism_to_prevent_over_splitting(sub_beats, beat)
```

#### 3. 检测条件规则

| 检测条件 | 触发阈值 | 拆分类型 | 策略分配 |
|----------|----------|----------|----------|
| 对话密度 > 30% 且时长 > 15秒 | 对话率 > 0.3 | dialogue_action | [正反打] + [动势组] |
| 包含3个以上独立动作动词 | 动作动词数 ≥ 3 | multi_action | [动势组] × 2 |
| 检测到时空跳跃词 | 发现"突然"/"然而"/"第二天"等 | time_space_jump | [蒙太奇组] |
| 情感转折 + 动作混合 | 检测到情绪转变且有动作 | emotion_action | [单镜] + [动势组] |

#### 4. 防呆机制

| 防呆条件 | 阈值 | 处理方式 |
|----------|------|----------|
| 子节拍权重过低 | 任一权重 < 0.5 | 合并回原节拍 |
| 叙事连贯性差 | 连贯性评分 < 0.6 | 合并回原节拍 |
| 导演标记 | director_marked_unsplittable = True | 跳过拆分 |
| 子节拍数量过多 | > 3个子节拍 | 合并部分子节拍 |

#### 5. 拆分日志格式

生成JSON格式的拆分日志，记录每个节拍的拆分/保持/合并决策：

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
      "assigned_strategies": ["[正反打:对话]", "[动势组:动作]"]
    }
  ]
}
```

#### 6. 子节拍编号

实现子节拍自动编号系统，支持层级编号：

- 示例: 1, 2a, 2b, 3, 4a, 4b, 4c, 5
- 支持最多26个子节拍（a-z）

---

### Phase 2.2: 蒙太奇逻辑引擎权威化 ✅

**目标**: 强制从蒙太奇逻辑分析结果推导策略，建立权威化决策机制

**实施内容**:

#### 1. 修改策略标签生成逻辑

在 `beat-analyzer.md` 的"Step 5.1: 核心策略诊断"部分修改：

**旧逻辑**: 基于场景描述分析生成策略

**新逻辑**: 强制从【蒙太奇逻辑分析】结果推导策略

#### 2. 蒙太奇逻辑到策略映射表

| 蒙太奇逻辑建议 | 映射策略标签 | 说明 |
|----------------|-------------|------|
| "单镜头" | `[单镜:场景类型]` | 蒙太奇建议单一固定镜头 |
| "动作序列" | `[动势组:关键动作]` | 蒙太奇建议连续动作拆分 |
| "时间压缩" | `[蒙太奇组:时间压缩]` | 蒙太奇建议压缩时间跨度 |
| "时间跳跃" | `[蒙太奇组:时间跳跃]` | 蒙太奇建议跨越时间 |
| "空间跳跃" | `[蒙太奇组:空间切换]` | 蒙太奇建议切换空间 |
| "连续调度" | `[长镜头:调度描述]` | 蒙太奇建议连续调度 |
| "情绪渲染" | `[蒙太奇组:情绪渲染]` | 蒙太奇建议多角度情绪表现 |

#### 3. 冲突处理机制

新增冲突处理函数 `resolve_strategy_conflict()`：

```python
def resolve_strategy_conflict(montage_suggestion, other_engine_suggestions, beat_context):
    """解决策略冲突，蒙太奇逻辑优先"""
    
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

#### 4. 策略生成算法

新增 `generate_core_strategy_from_montage()` 函数：

```python
def generate_core_strategy_from_montage(montage_analysis_result, beat_context):
    """基于蒙太奇逻辑分析结果生成核心策略"""
    
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

#### 5. 冲突日志格式

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

---

### Phase 2.3: 类型化权重修正集成 ✅

**目标**: 在权重计算函数中集成类型化修正，记录修正原因

**实施内容**:

#### 1. 修改calculate_final_weight_v4_1函数

在 `beat-analyzer.md` 中修改 `calculate_final_weight_v4_1()` 函数：

**新增参数**: `project_config` - 项目配置，包含影片类型等

**新增返回值**: `weight_modification` - 类型化修正记录对象

#### 2. 读取影片类型

```python
# 1. 获取影片类型（Phase 2.3新增）
if project_config and hasattr(project_config, 'genre'):
    genre = project_config.genre
elif not genre:
    genre = 'action'  # 默认类型
```

#### 3. 类型化修正记录

新增 `weight_modification` 对象：

```python
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
```

#### 4. 类型化修正原因表

| 影片类型 | 动作节拍 | 对话节拍 | 情绪节拍 | 环境节拍 |
|----------|-----------|-----------|-----------|-----------|
| 动作 | ×1.5 提升 | ×0.8 降权 | ×1.2 提升 | ×1.0 保持 |
| 悬疑 | ×1.0 保持 | ×1.5 提升 | ×1.5 提升 | ×1.3 提升 |
| 爱情 | ×0.7 降权 | ×1.4 提升 | ×1.6 提升 | ×1.2 提升 |
| 喜剧 | ×1.0 保持 | ×1.3 提升 | ×1.4 提升 | ×1.1 提升 |
| 恐怖 | ×1.2 提升 | ×1.1 提升 | ×1.4 提升 | ×1.5 提升 |
| 艺术 | ×0.6 降权 | ×1.5 提升 | ×1.7 提升 | ×1.4 提升 |
| 纪录 | ×0.5 降权 | ×1.6 提升 | ×1.2 提升 | ×1.8 提升 |

#### 5. 修正原因示例

| 影片类型 | 节拍类型 | 系数 | 修正原因 |
|----------|----------|------|----------|
| 动作 | 重大动作 | ×1.5 | "动作片类型，重大动作节拍应用×1.5系数" |
| 动作 | 对话 | ×0.8 | "动作片类型，对话节拍应用×0.8系数（降权）" |
| 爱情 | 情绪转折 | ×1.6 | "爱情片类型，情绪转折应用×1.6系数" |
| 艺术 | 重大动作 | ×0.6 | "艺术片类型，重大动作节拍应用×0.6系数（降权）" |

---

### Phase 2.4: 拆解方案模板动态化 ✅

**目标**: 删除固定的"三段式拆解"表格，新增动态"拆解方案"字段

**实施内容**:

#### 1. 修改表格字段

在 `beat-breakdown-template.md` 中修改节拍拆解表的字段：

**修改前**:
```
| 节拍编号 | ... | 综合权重 | 关键帧等级 | ... | 拆解建议 |
```

**修改后**:
```
| 节拍编号 | ... | 综合权重 | 类型修正 | 关键帧等级 | ... | 拆解方案 |
```

#### 2. 新增"类型修正"列

在"综合权重"后新增"类型修正"列：
- 格式: `{系数} ({原因})`
- 示例: `×1.5 (动作片类型，重大动作节拍应用×1.5系数)`

#### 3. 修改"拆解建议"为"拆解方案"

将固定的"拆解建议"字段改为动态的"拆解方案"字段。

#### 4. 动态拆解方案规则

根据策略类型动态生成拆解方案：

**[单镜]**:
- 模板: "单镜头固定机位，重点表现{情绪基调}"
- 示例: "单镜头固定机位，重点表现期待"

**[动势组]**:
- 模板: "2格动势分解：起势({关键点1}) → 落幅({关键点2})"
- 示例: "2格动势分解：起势(握紧拳头) → 落幅(挥拳击出)"

**[蒙太奇组]**:
- 模板: "3格蒙太奇：起势({setup}) - 高潮({action}) - 余韵({resolution})"
- 示例: "3格蒙太奇：起势(震惊表情) - 高潮(瞬间变脸) - 余韵(期待敲盘)"

**[长镜头]**:
- 模板: "2-3格关键节点：{节点1} → {节点2} [→ {节点3}]"
- 示例: "2-3格关键节点：起跑姿态(入口) → 冲刺动作(走廊) → 停止姿态(门口)"

**[正反打]**:
- 模板: "正反打交替：A角特写 → B角反应"
- 示例: "正反打交替：A角特写(愤怒指责) → B角反应(愧疚低头)"

#### 5. 更新字段说明

在字段说明部分更新"拆解方案"说明：

**修改前**:
```
- **拆解建议**：具体的拆分方案描述，如"建议拆为3格：抓取起势→按压动作→要求对话"
```

**修改后**:
```
- **拆解方案**（Phase 2.4动态化）：根据核心策略类型动态生成的拆分方案描述
  - **[单镜]**："单镜头固定机位，重点表现{情绪基调}"
  - **[动势组]**："2格动势分解：起势({关键点1}) → 落幅({关键点2})"
  - **[蒙太奇组]**："3格蒙太奇：起势({setup}) - 高潮({action}) - 余韵({resolution})"
  - **[长镜头]**："2-3格关键节点：{节点1} → {节点2} [→ {节点3}]"
  - **[正反打]**："正反打交替：A角特写 → B角反应"
```

---

## 文件变更汇总

### 更新的文件

| 文件路径 | 阶段 | 主要变更 |
|----------|------|----------|
| `.claude/common/beat-analyzer.md` | Phase 2.1, 2.2, 2.3 | 新增Step 0颗粒度重组，修改策略诊断逻辑，集成类型化修正 |
| `.claude/skills/film-storyboard-skill/templates/beat-breakdown-template.md` | Phase 2.4 | 新增类型修正列，拆解方案动态化 |

### 新增的函数

| 函数名 | 阶段 | 功能 |
|--------|------|------|
| `enforce_granularity_reorganization()` | Phase 2.1 | 颗粒度重组前置处理器 |
| `detect_split_conditions()` | Phase 2.1 | 检测节拍是否需要拆分 |
| `split_beat_by_strategy()` | Phase 2.1 | 根据拆分类型执行拆分 |
| `split_dialogue_and_action()` | Phase 2.1 | 拆分对话+动作节拍 |
| `split_emotion_and_action()` | Phase 2.1 | 拆分情感转折+动作节拍 |
| `apply_mechanism_to_prevent_over_splitting()` | Phase 2.1 | 防呆机制检查 |
| `renumber_beats_with_sub_beats()` | Phase 2.1 | 重新编号节拍 |
| `resolve_strategy_conflict()` | Phase 2.2 | 解决策略冲突 |
| `generate_core_strategy_from_montage()` | Phase 2.2 | 基于蒙太奇逻辑生成策略 |

### 修改的函数

| 函数名 | 阶段 | 修改内容 |
|--------|------|----------|
| `calculate_final_weight_v4_1()` | Phase 2.3 | 新增project_config参数，新增weight_modification返回值 |

---

## Phase 2核心特性总结

### 1. 颗粒度重组 ✅

- **一拍一策原则**: 强制每个节拍对应单一策略
- **智能拆分**: 4种检测条件，4种拆分类型
- **防呆机制**: 3种防呆检查，防止过度拆分
- **子节拍编号**: 支持层级编号（1, 2a, 2b, 3）

### 2. 蒙太奇逻辑权威化 ✅

- **策略映射**: 7种蒙太奇建议映射到策略标签
- **冲突处理**: 记录冲突并采用蒙太奇逻辑
- **权威决策**: 蒙太奇逻辑拥有最高优先级
- **日志记录**: 完整的冲突日志，支持追溯

### 3. 类型化权重修正 ✅

- **系数表**: 7种类型 × 4种节拍类型 = 28种组合
- **修正记录**: 完整的weight_modification对象
- **调整方向**: 提升/降权/保持
- **原因记录**: 每次修正都有明确原因

### 4. 拆解方案动态化 ✅

- **5种策略**: 单镜、动势组、蒙太奇组、长镜头、正反打
- **动态模板**: 每种策略有专属拆解方案模板
- **类型修正列**: 新增类型修正字段，显示系数和原因
- **完整示例**: 每种策略都有详细示例

---

## 向后兼容性

### 兼容策略

- **配置驱动**: 所有Phase 2特性通过函数参数控制
- **默认值**: 未配置时使用合理默认值
- **降级机制**: 蒙太奇建议不可用时回退到传统分析
- **数据格式**: 新增字段不影响现有字段

### 回退方法

如需回退到Phase 2之前：
```bash
# 恢复备份文件
cp .backup/phase2-beat-breakdown-overhaul/beat-analyzer.md .claude/common/beat-analyzer.md
cp .backup/phase2-beat-breakdown-overhaul/beat-breakdown-template.md .claude/skills/film-storyboard-skill/templates/beat-breakdown-template.md
```

---

## 备份与恢复

### 备份结构

```
.backup/phase2-beat-breakdown-overhaul/
├── beat-analyzer.md              (27K - 原始备份)
└── beat-breakdown-template.md   (10K - 原始备份)
```

### 恢复命令

```bash
# 恢复单个文件
cp .backup/phase2-beat-breakdown-overhaul/beat-analyzer.md .claude/common/

# 恢复所有文件
cp .backup/phase2-beat-breakdown-overhaul/* .claude/common/ .claude/skills/film-storyboard-skill/templates/
```

---

## 质量检查清单

### Phase 2.1 检查

- [ ] 所有检测条件已正确实现
- [ ] 所有拆分类型已正确实现
- [ ] 防呆机制已正确实现
- [ ] 子节拍编号系统已正确实现
- [ ] 拆分日志格式已正确定义

### Phase 2.2 检查

- [ ] 蒙太奇逻辑映射表已完整
- [ ] 冲突处理机制已正确实现
- [ ] 策略生成算法已正确实现
- [ ] 冲突日志格式已正确定义
- [ ] 权威决策机制已正确实现

### Phase 2.3 检查

- [ ] calculate_final_weight_v4_1函数已正确修改
- [ ] 类型化修正记录对象已正确定义
- [ ] 修正原因表已完整
- [ ] 类型系数表已正确应用
- [ ] 返回值已正确添加

### Phase 2.4 检查

- [ ] 表格字段已正确修改
- [ ] 类型修正列已正确添加
- [ ] 拆解方案已动态化
- [ ] 5种策略模板已正确定义
- [ ] 字段说明已正确更新

---

## 下一步建议

### 立即执行

1. **测试颗粒度重组**: 验证检测条件和拆分逻辑
2. **测试冲突处理**: 验证蒙太奇逻辑权威化
3. **测试类型修正**: 验证类型化权重计算
4. **测试动态拆解**: 验证拆解方案动态生成

### 后续优化

1. **性能优化**: 评估颗粒度重组的执行效率
2. **参数调优**: 根据实际使用调整检测阈值
3. **用户反馈**: 收集用户使用反馈，持续改进

---

## 总结

ANINEO Phase 2节拍拆解引擎重构已全部完成！本次实施实现了：

✅ **4个子阶段**全部完成  
✅ **2个文件**更新  
✅ **9个新函数**实现  
✅ **4大核心特性**完整集成  
✅ **完整备份**已创建

所有Phase 2特性均已集成到系统中，系统已准备好进行测试验证。

**实施完成时间**: 2026-01-31  
**实施状态**: ✅ 完成并待测试

---

**报告生成**: Phase 2节拍拆解引擎重构实施报告  
**版本**: 1.0  
**生成日期**: 2026-01-31
