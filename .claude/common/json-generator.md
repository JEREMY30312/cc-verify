# JSON 生成工具规范

> **版本**: 4.1
> **生效阶段**: breakdown / beatboard / sequence / motion
> **用途**: 统一生成各阶段的 JSON 数据文件

---

## 通用规则

所有 JSON 文件必须遵循以下规则：

1. **同时生成**: JSON 必须与 Markdown 同时生成（在"保存输出"步骤中）
2. **立即验证**: 生成后立即执行字段完整性验证
3. **验证失败处理**: 验证失败不得保存文件，立即报错
4. **版本标记**: 所有 JSON 必须包含 `version` 和 `generated_at` 字段
5. **严格模式**: JSON 缺失或字段不完整 → 停止流程，要求重新生成上游阶段

---

## 函数定义

### 函数: generate_scene_breakdown_json()

**输入**:
- `outputs/beat-breakdown-{集数}.md`（Markdown 表格）

**输出**:
- `outputs/scene-breakdown-{集数}.json`

**处理逻辑**:
1. 解析 Markdown 表格提取每个节拍的数据
2. 计算 NDI、镜头类型、动机等字段
3. 构建 shots数组和 sub_shots数组
4. 添加 version 和 generated_at 字段
5. 输出符合 Schema 的 JSON

**必填字段**:
| 字段 | 类型 | 说明 |
|------|------|------|
| version | string | 固定 "4.1" |
| episode_id | string | 集数标识 |
| generated_at | string | ISO 8601 时间戳 |
| shots | array | 原子镜头数组 |
| sub_shots | array | 子镜头数组（如有） |

**shots 数组必填字段**:
| 字段 | 类型 | 说明 |
|------|------|------|
| shot_id | string | 镜头唯一标识（如 S01） |
| ndi_score | number | 叙事密度指数（0-5） |
| shot_type | string | 镜头类型（Pulse/Flow/Encounter） |
| motivation | string | 镜头动机（威慑/悬疑/情感受创等） |
| source_text | string | 【V5.0新增】剧本原文完整段落，包含对话、动作、环境描述 |

**source_text 字段生成规则**:
1. **提取来源**: 从 `script/{集数}.md` 提取该节拍对应的完整原文段落
2. **内容范围**: 必须包含该节拍的所有对话、动作描述、环境描写、心理活动
3. **格式要求**: 保留原文的段落格式，不得删减或改写
4. **用途**: 为下游阶段（九宫格/四宫格）提供原始剧本内容，防止AI脑补产生幻觉
5. **验证规则**: 
   - 字段必须存在且非空
   - 内容必须与剧本原文一致（抽样检查）
   - 与 scene_description 逻辑一致

---

### 函数: generate_beat_board_full_list_json()

**输入**:
- `outputs/beat-board-prompt-{集数}-board*.md`（所有分板文件）

**输出**:
- `outputs/beat-board-full-list-{集数}.json`

**处理逻辑**:
1. 解析所有分板文件提取 9 格数据
2. 识别水下镜头（🔵 和 ⚪ 级别）
3. 构建 grids数组和 waterfall_shots数组
4. 计算 quality_metrics
5. 添加 version 和 generated_at 字段

**必填字段**:
| 字段 | 类型 | 说明 |
|------|------|------|
| version | string | 固定 "4.1" |
| episode_id | string | 集数标识 |
| generated_at | string | ISO 8601 时间戳 |
| grids | array | 9格完整数据 |
| waterfall_shots | array | 水下镜头映射 |
| quality_metrics | object | 质量指标 |

**grids 数组必填字段**:
| 字段 | 类型 | 说明 |
|------|------|------|
| grid_id | string | 格子标识（如 1, 2, ...9） |
| beat_number | number | 对应节拍编号 |
| keyframe_level | string | 关键帧等级（🔴/🟠/🟡/🔵/⚪） |

---

### 函数: generate_sequence_board_data_json()

**输入**:
- `outputs/sequence-board-prompt-{集数}-board*.md`（所有分镜板）

**输出**:
- `outputs/sequence-board-data-{集数}.json`

**处理逻辑**:
1. 解析所有分镜板提取 cards 数据
2. 计算跨格连续性评分
3. 统计补帧抑制信息
4. 构建 boards数组
5. 添加 version 和 generated_at 字段

**必填字段**:
| 字段 | 类型 | 说明 |
|------|------|------|
| version | string | 固定 "4.1" |
| episode_id | string | 集数标识 |
| generated_at | string | ISO 8601 时间戳 |
| boards | array | 所有分镜板 |
| tween_suppression | object | 补帧抑制统计 |
| quality_metrics | object | 质量指标 |

**boards 数组必填字段**:
| 字段 | 类型 | 说明 |
|------|------|------|
| board_id | string | 分镜板唯一标识 |
| board_number | number | 板号 |
| cards | array | 镜头卡片数组 |

**cards 数组必填字段**:
| 字段 | 类型 | 说明 |
|------|------|------|
| card_id | string | 卡片唯一标识 |
| beat_number | number | 对应节拍编号 |
| strategy_tags | array | 策略标签数组 |
| camera_info | object | 镜头信息 |

---

### 函数: generate_motion_prompt_data_json()

**输入**:
- `outputs/motion-prompt-{集数}.md`（动态提示词）

**输出**:
- `outputs/motion-prompt-data-{集数}.json`

**处理逻辑**:
1. 解析 Motion Prompt 文本提取五模块数据
2. 执行物理验证并记录结果
3. 构建 motion_groups数组
4. 计算 physics_verification统计
5. 添加 version 和 generated_at 字段

**必填字段**:
| 字段 | 类型 | 说明 |
|------|------|------|
| version | string | 固定 "4.1" |
| episode_id | string | 集数标识 |
| generated_at | string | ISO 8601 时间戳 |
| boards | array | 动态提示词板 |
| physics_verification | object | 物理验证统计 |
| quality_metrics | object | 质量指标 |

**motion_groups 数组必填字段**:
| 字段 | 类型 | 说明 |
|------|------|------|
| group_id | string | 组唯一标识 |
| beat_number | number | 对应节拍编号 |
| keyframe | object | 关键帧数据 |
| sequence_grids | array | 四宫格展开数组 |

**keyframe 必填字段**:
| 字段 | 类型 | 说明 |
|------|------|------|
| prompt_id | string | 提示词标识（如 1-0） |
| camera_motion | string | 镜头运动模块 |
| subject_action | string | 主体动作模块 |
| environment_dynamic | string | 环境动态模块 |
| rhythm_control | string | 节奏控制模块 |
| atmosphere | string | 氛围强化模块 |
| physics_check | string | 物理检查状态 |

---

## 错误处理

### 错误类型与处理

| 错误类型 | 处理方式 | 后续动作 |
|----------|----------|----------|
| JSON 文件已存在 | 覆盖写入 | 继续执行 |
| 字段缺失 | 立即报错 | 不保存文件，停止流程 |
| 格式错误 | 立即报错 | 不保存文件，停止流程 |
| 数据不一致 | 立即报错 | 不保存文件，停止流程 |
| NDI 超出范围 | 记录警告 | 继续执行（使用默认值） |

### 错误信息模板

```markdown
❌ [阶段名] JSON 生成失败

错误类型: {错误类型}
错误详情: {具体描述}

建议操作:
- 检查上游阶段是否完整执行
- 重新执行: /breakdown {集数} 或 /beatboard {集数} 或 /sequence {集数} 或 /motion {集数}
```

---

## 验证清单

### 验证项目清单

| 阶段 | 验证项 | 通过标准 |
|------|--------|----------|
| breakdown | scene-breakdown JSON 字段完整性 | 所有必填字段存在 |
| breakdown | shots 数量 | 8 ≤ 数量 ≤ 50 |
| breakdown | NDI 分布 | 至少包含高、中、低三种类型 |
| beatboard | beat-board-full-list JSON 字段完整性 | 所有必填字段存在 |
| beatboard | grids 数量 | 数量 = 9 |
| beatboard | waterfall_shots 映射 | 🔵 和 ⚪ 级别镜头已映射 |
| sequence | sequence-board-data JSON 字段完整性 | 所有必填字段存在 |
| sequence | boards 数量 | 与 Markdown 文件数量一致 |
| sequence | cross_grid_continuity | 评分 ≥ 80 |
| motion | motion-prompt-data JSON 字段完整性 | 所有必填字段存在 |
| motion | motion_groups 数量 | 数量 = 9 |
| motion | 五模块合规性 | = 100% |

---

## 与 SKILL.md 的对应关系

| SKILL.md 步骤 | 生成函数 | 输出文件 |
|---------------|----------|----------|
| breakdown 步骤7 | generate_scene_breakdown_json() | scene-breakdown-{集数}.json |
| beatboard 步骤10 | generate_beat_board_full_list_json() | beat-board-full-list-{集数}.json |
| sequence 步骤9 | generate_sequence_board_data_json() | sequence-board-data-{集数}.json |
| motion 步骤7 | generate_motion_prompt_data_json() | motion-prompt-data-{集数}.json |

---

## 版本兼容性

### 向后兼容性

- V4.1 生成的 JSON 包含 `version: "4.1"` 标记
- 旧版系统读取时忽略不认识的字段
- 建议定期更新到最新版本

### 版本迁移

| 从版本 | 到版本 | 迁移方式 |
|--------|--------|----------|
| V2.0 | V4.1 | 添加额外字段，保留原有字段 |
| V3.0 | V4.1 | 添加 quality_metrics 和 tween_suppression |
| V4.0 | V4.1 | 添加 physics_verification 到 motion JSON |

---

## 使用示例

### 在 Python 脚本中使用

```python
import json
from pathlib import Path

def generate_scene_breakdown_json(episode_id: str, markdown_path: str) -> dict:
    """
    生成 scene-breakdown JSON
    """
    # 解析 Markdown 表格
    beats = parse_beat_table(markdown_path)
    
    # 构建 shots 数组
    shots = []
    for beat in beats:
        shots.append({
            "shot_id": f"S{beats.index(beat) + 1:02d}",
            "ndi_score": beat.ndi_score,
            "shot_type": beat.shot_type,
            "motivation": beat.motivation,
            "axis_side": beat.axis_side,
            "relay_point": beat.relay_point
        })
    
    # 构建 JSON 结构
    result = {
        "version": "4.1",
        "episode_id": episode_id,
        "generated_at": datetime.now().isoformat(),
        "shots": shots
    }
    
    # 验证
    validate_scene_breakdown(result)
    
    return result

def validate_scene_breakdown(data: dict) -> bool:
    """
    验证 scene-breakdown JSON 字段完整性
    """
    required_fields = ['version', 'episode_id', 'generated_at', 'shots']
    shot_required_fields = ['shot_id', 'ndi_score', 'shot_type', 'motivation']
    
    # 验证顶层字段
    for field in required_fields:
        if field not in data:
            raise ValueError(f"缺少必填字段: {field}")
    
    # 验证 shots 数组
    if not data['shots']:
        raise ValueError("shots 数组为空")
    
    for i, shot in enumerate(data['shots']):
        for field in shot_required_fields:
            if field not in shot:
                raise ValueError(f"shot[{i}] 缺少必填字段: {field}")
    
    return True
```

---

## 相关文件

| 文件 | 用途 |
|------|------|
| `beat-breakdown-template.md` | scene-breakdown JSON Schema |
| `beat-board-template.md` | beat-board-full-list JSON Schema |
| `sequence-board-template.md` | sequence-board-data JSON Schema |
| `motion-prompt-template.md` | motion-prompt-data JSON Schema |
| `storyboard-review-skill/SKILL.md` | 审核时的 JSON 验证逻辑 |
