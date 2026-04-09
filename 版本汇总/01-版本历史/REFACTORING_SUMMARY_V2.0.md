# ANINEO V2.0 模块 1 重构总结

> **重构日期**: 2025-01-22
> **重构目标**: 从机械切镜转向认知驱动，建立 scene_breakdown.json 全量数据层
> **核心原则**: 增量修改，严禁全量删除

---

## ✅ 已完成的任务

### 1. 修改 common/beat-analyzer.md ✅
**内容**: 注入导演认知协议

**新增内容**:
- **NDI（叙事密度指数）计算**:
  - 计算公式：NDI_score = (动词密度 × 0.4) + (情绪转折点 × 0.35) + (角色位移 × 0.25)
  - NDI分级与镜头策略映射（高密度→多镜头原子拆分，低密度→长镜头或氛围渲染）
- **镜头合并协议**:
  - 深度构图优先：前景与背景互动优先通过"四层环境结构"在一个镜头内解决
  - 焦点平移判定：多人交互且无第三方干扰时使用"焦点切换"而非切镜
- **原子化叙事原则**:
  - 每个原子单元必须锚定"一个核心叙事意图"与"一个视觉重心"
  - 镜头生成规则：单叙事意图=单镜头，多叙事意图=多镜头
- **镜头类型标签**:
  - Pulse（强动作）、Flow（长镜头）、Encounter（交互）
- **镜头动机**:
  - 威慑、悬疑、情感受创、冲突升级、氛围渲染、信息传递
  - 无效切镜判定标准

---

### 2. 重构 film-storyboard-skill/SKILL.md 步骤4 ✅
**内容**: 扩展节拍分析逻辑

**新增内容**:
- **步骤4 扩展**:
  - 计算NDI（叙事密度指数）
  - 分配镜头类型标签（Pulse/Flow/Encounter）
  - 注入镜头动机（威慑/悬疑/情感受创/冲突升级等）
  - 执行镜头合并协议检查（深度构图/焦点平移）
  - 应用原子化叙事原则（单意图+单重心）

---

### 3. 重构 film-storyboard-skill/SKILL.md 步骤7 ✅
**内容**: 扩展输出，同时生成 scene-breakdown-{集数}.json

**新增内容**:
- **步骤7 扩展**:
  - 同时输出 `outputs/scene-breakdown-{集数}.json`
  - 全量数据层规范（JSON Schema）：
    - `shot_id`: 镜头唯一标识（S01, S02...）
    - `ndi_score`: 叙事密度指数（0-5）
    - `shot_type`: 镜头类型（Pulse/Flow/Encounter）
    - `motivation`: 镜头动机（威慑/悬疑/情感受创等）
    - `lens_intent`: 镜头意图描述
    - `axis_side`: 轴线侧（左侧/右侧/中央）
    - `relay_point`: 镜头接力点（衔接数据）

---

### 4. 修改 AGENTS.md - 更新指令路由表 ✅
**内容**: 更新 contextFiles 引用

**修改内容**:
| 指令 | 原contextFiles | 新contextFiles |
|------|---------------|---------------|
| `/beatboard` | `[beat-breakdown-{集数}.md]` | `[scene-breakdown-{集数}.json, beat-breakdown-{集数}.md]` |
| `/sequence` | `[beat-board-anchors-{集数}.md, beat-board-full-list-{集数}.json]` | `[scene-breakdown-{集数}.json, beat-board-anchors-{集数}.md, beat-board-full-list-{集数}.json]` |
| `/motion` | `[sequence-board-prompt-{集数}.md, ...]` | `[scene-breakdown-{集数}.json, sequence-board-prompt-{集数}.md, ...]` |
| `/review breakdown` | `[beat-breakdown-{集数}.md, ...]` | `[scene-breakdown-{集数}.json, beat-breakdown-{集数}.md, ...]` |
| `/review beatboard` | `[beat-board-anchors-{集数}.md, beat-board-full-list-{集数}.json]` | `[scene-breakdown-{集数}.json, beat-board-anchors-{集数}.md, beat-board-full-list-{集数}.json]` |
| `/review sequence` | `[sequence-board-prompt-{集数}.md, ...]` | `[scene-breakdown-{集数}.json, sequence-board-prompt-{集数}.md, ...]` |
| `/review motion` | `[motion-prompt-{集数}.md, ...]` | `[scene-breakdown-{集数}.json, motion-prompt-{集数}.md, ...]` |

---

### 5. 修改 AGENTS.md - 注入导演审核标准 ✅
**内容**: 新增认知审核

**新增内容**:
- **认知审核**: 审核切镜是否具备明确的"叙事动机"，严禁无效切镜
- 质量检查覆盖范围更新：
  - SKILL 自检：格式、数量、结构、三幕比例、节拍数量
  - 导演审核：叙事结构、镜头语言、专业标准、覆盖度、一致性、继承性、置信度
  - **认知审核**：镜头动机（新增）

---

### 6. 修改 beat-breakdown-template.md ✅
**内容**: 新增镜头动机和接力点字段

**新增内容**:
- 表格新增字段：
  - `镜头动机（Motivation）`: 该镜头的叙事动机
  - `镜头接力点（Relay Point）`: 镜头衔接的视觉锚点
- 字段说明更新：
  - 镜头动机：必须是明确的动机类型（威慑/悬疑/情感受创/冲突升级/氛围渲染/信息传递）
  - 镜头接力点：镜头衔接的视觉锚点，确保空间连续性（如：角色A的面部特写、门把手、天空）

---

### 7. 修改 beat-board-template.md ✅
**内容**: 将九宫格布局修改为动态四宫格锚点展示逻辑

**新增内容**:
- **布局判定规则**（基于 scene-breakdown-{集数}.json）:
  | 镜头类型 | NDI范围 | 建议布局 | 说明 |
  |----------|---------|----------|------|
  | Pulse | ≥2.5 | 九宫格 | 高密度，多动作单元，需要充分拆分 |
  | Pulse | 1.5-2.4 | 六宫格 | 中密度，适度拆分 |
  | Pulse | <1.5 | 四宫格 | 低密度，基础拆分 |
  | Flow | 任意 | 四宫格 | 长镜头/氛围渲染，减少切镜 |
  | Encounter | 任意 | 四宫格或六宫格 | 交互场景，根据对话复杂度决定 |

- **画面描述新增字段**:
  - `镜头动机`: [威慑/悬疑/情感受创/冲突升级/氛围渲染/信息传递]
  - `NDI 分数`: [0-5]

---

### 8. 检查 environment-construction-guide 相关引用 ✅
**内容**: 添加轴线法律约束

**新增内容**:
- **轴线法律（Axis Law）**:
  - 所有镜头生成必须核对 scene_breakdown.json 中的 axis_side 字段
  - 确保在交互场景中摄影机不发生越轴穿帮
  - 轴线侧定义：左侧/右侧/中央
  - 跨越轴线必须通过合理调度（如：角色移动、时间跳跃、场景切换）

---

### 9. 在 data-validator.md 中新增 scene-breakdown.json 字段完整性验证 ✅
**内容**: 新增 SceneBreakdownValidator 类

**新增内容**:
- **SceneBreakdownValidator 类**:
  - `validate_json_structure()`: 验证 JSON 结构
  - `validate_required_fields()`: 验证必填字段完整性
  - `validate_shot_count()`: 验证镜头数量（8-50合理范围）
  - `validate_ndi_distribution()`: 验证 NDI 分布（确保至少有高、中、低三种类型）
  - `validate_motivation_coverage()`: 验证镜头动机覆盖率
  - `validate_axis_consistency()`: 验证轴线一致性
  - `validate_relay_point_completeness()`: 验证接力点完整性

- **使用方式更新**: 新增 Scene Breakdown 验证调用示例

---

### 10. 扫描所有受影响文件，确保 contextFiles 引用路径一致 ✅
**内容**: 更新子 Agent 配置文件

**修改内容**:
- **agents/director.md**:
  - breakdown-review 的 contextFiles 新增 `scene-breakdown-{集数}.json`
  - beatboard-review 的 contextFiles 新增 `scene-breakdown-{集数}.json`
  - sequence-review 的 contextFiles 新增 `scene-breakdown-{集数}.json`
  - motion-review 的 contextFiles 新增 `scene-breakdown-{集数}.json`

- **agents/storyboard-artist.md**:
  - breakdown 任务输出路径新增 `outputs/scene-breakdown-{集数}.json`

---

## 📋 修改文件清单

| 文件 | 修改类型 | 说明 |
|------|----------|------|
| `.claude/common/beat-analyzer.md` | 增量修改 | 新增导演认知协议（约150行） |
| `.claude/skills/film-storyboard-skill/SKILL.md` | 增量修改 | 步骤4和步骤7扩展（约60行） |
| `AGENTS.md` | 增量修改 | 指令路由表更新 + 认知审核注入 |
| `.claude/skills/film-storyboard-skill/templates/beat-breakdown-template.md` | 增量修改 | 新增镜头动机和接力点字段 |
| `.claude/skills/film-storyboard-skill/templates/beat-board-template.md` | 增量修改 | 动态四宫格布局逻辑 |
| `AGENTS.md`（环境构造部分） | 增量修改 | 轴线法律约束 |
| `.claude/common/data-validator.md` | 增量修改 | SceneBreakdownValidator 类 |
| `agents/director.md` | 增量修改 | contextFiles 新增 scene-breakdown-{集数}.json |
| `agents/storyboard-artist.md` | 增量修改 | 输出路径新增 scene-breakdown-{集数}.json |

---

## 🎯 核心成果

### 1. 建立了认知驱动的镜头设计体系
- ✅ NDI（叙事密度指数）量化叙事复杂度
- ✅ 镜头合并协议避免机械切镜
- ✅ 原子化叙事原则确保每个镜头有明确动机

### 2. 构建了全量数据层
- ✅ `scene-breakdown-{集数}.json` 结构化数据
- ✅ 包含镜头动机、NDI分数、轴线侧、接力点等关键数据
- ✅ 支持九宫格、四宫格、动态提示词的继承和扩展

### 3. 完善了质量检查体系
- ✅ 导演审核新增认知审核（镜头动机）
- ✅ 新增 SceneBreakdownValidator 验证器
- ✅ 覆盖 JSON 结构、字段完整性、NDI 分布、轴线一致性等

### 4. 实现了动态布局系统
- ✅ 基于镜头类型和 NDI 分数动态决定格子数量
- ✅ 支持四宫格、六宫格、九宫格的灵活切换
- ✅ 避免过度切镜或切镜不足

### 5. 建立了空间守恒约束
- ✅ 轴线法律确保交互场景不越轴穿帮
- ✅ 轴线侧定义：左侧/右侧/中央
- ✅ 跨越轴线的调度规则

---

## 📊 数据流变化

### 旧流程（V1.0）
```
剧本 → beat-breakdown-{集数}.md → beat-board-prompt-{集数}.md → sequence-board-prompt-{集数}.md → motion-prompt-{集数}.md
```

### 新流程（V2.0）
```
剧本 → [beat-breakdown-{集数}.md + scene-breakdown-{集数}.json]
       ↓
beat-board-prompt-{集数}.md (读取 scene-breakdown-{集数}.json)
       ↓
sequence-board-prompt-{集数}.md (读取 scene-breakdown-{集数}.json)
       ↓
motion-prompt-{集数}.md (读取 scene-breakdown-{集数}.json)
```

**关键变化**:
1. 节拍拆解阶段同时生成 MD 和 JSON
2. 所有后续阶段强制读取 scene-breakdown-{集数}.json
3. 全量数据层贯穿整个流程

---

## ⚠️ 注意事项

### 1. 向后兼容性
- ✅ 保持 MD 文件格式不变
- ✅ 新增 JSON 文件作为补充数据层
- ✅ 旧版本流程仍然可用（不读取 JSON）

### 2. 文件依赖关系
- ✅ 九宫格、四宫格、动态提示词都依赖 scene-breakdown-{集数}.json
- ✅ 导演审核也依赖 scene-breakdown-{集数}.json
- ✅ 必须在节拍拆解阶段先生成该 JSON 文件

### 3. 验证器使用
- ✅ SceneBreakdownValidator 必须在节拍拆解完成后运行
- ✅ 验证失败会阻断流程
- ✅ 验证结果包括 JSON 结构、字段完整性、NDI 分布、轴线一致性等

---

## 🚀 后续建议

### 1. 测试验证
- [ ] 运行完整的 breakdown → beatboard → sequence → motion 流程
- [ ] 验证 scene-breakdown-{集数}.json 的正确性
- [ ] 验证动态布局系统的逻辑
- [ ] 验证轴线法律的约束效果

### 2. 文档完善
- [ ] 更新用户使用指南
- [ ] 添加 NDI 计算示例
- [ ] 添加动态布局规则说明
- [ ] 添加轴线法律案例分析

### 3. 工具开发
- [ ] 开发 NDI 计算工具
- [ ] 开发 scene-breakdown-{集数}.json 可视化工具
- [ ] 开发轴线检查工具

---

## 📝 总结

本次重构成功实现了从机械切镜向认知驱动的转变，建立了 scene-breakdown-{集数}.json 全量数据层，完善了质量检查体系，实现了动态布局系统，建立了空间守恒约束。所有修改都遵循增量修改原则，确保向后兼容。

**核心价值**:
1. **认知驱动**: 镜头设计基于叙事动机，而非机械切镜
2. **数据层**: 结构化数据支持继承、验证、可视化
3. **动态布局**: 根据叙事密度智能决定镜头拆分程度
4. **空间守恒**: 轴线法律确保交互场景的连续性

**下一步**: 运行完整流程测试，验证新架构的稳定性和有效性。
