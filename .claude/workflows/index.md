# ANINEO 工作流程文档索引

本目录包含各命令的详细工作流程文档。

## 工作流程列表

| 命令 | 工作流程文件 | 说明 |
|--------|--------------|------|
| `/breakdown` | [breakdown-workflow.md](breakdown-workflow.md) | 节拍拆解详细步骤 |
| `/beatboard` | [beatboard-workflow.md](beatboard-workflow.md) | 九宫格提示词生成步骤 |
| `/sequence` | [sequence-workflow.md](sequence-workflow.md) | 四宫格提示词生成步骤 |
| `/motion` | [motion-workflow.md](motion-workflow.md) | 动态提示词生成步骤 |
| `/review` | [review-workflow.md](review-workflow.md) | 审核工作流程 |
| `/AINIEO` | [interactive-workflow.md](interactive-workflow.md) | 配置向导流程 |

---

## 文档结构

每个工作流程文件包含：

1. **完整工作流程**：10个步骤的详细描述
2. **模块依赖声明**：必需和可选的模块列表
3. **协议文件引用**：用户确认和快照管理协议
4. **相关文件**：关联的SKILL、模板、审核文件

---

## 使用说明

- 命令文件（`.opencode/command/*.md`）会引用对应的工作流程文档
- SKILL文件包含实际的执行逻辑
- 本目录提供工作流的详细文档说明
- 如需查看某个命令的详细步骤，请点击上方表格中的链接

---

## 文件位置

本目录位于 `.claude/workflows/`，与技能包、公共模块同属一个目录层级，便于统一管理和引用。

---

## 数据流向图（V4.1更新）← 【新增】

```
节拍拆解（beat-breakdown-{集数}.md）
    ↓
    ├── 核心数据：核心策略、复杂度、建议格子数
    ├── 包含：10种策略标签（8种核心 + 2种特殊）
    └── 规范：
        ├── 九宫格：1格 = 1个关键帧 ✅
        ├── Sequence：根据策略标签展开为1-4镜头
        └── JSON：唯一数据源，无箭头格式兼容层
        ↓
九宫格生成（beat-board-prompt-{集数}-board*.md）
    ↓
    ├── 核心输出：每个格子 = 1个关键帧 ✅
    ├── 附带输出：JSON alternative_frames ⭐ 【V4.1新增】
    │   ├── 文件：outputs/beat-board-full-list-{集数}.json
    │   ├── 字段：grids[].alternative_frames
    │   ├── 包含：type、role、action、reason、drama_tension_score
    │   └── 用途：Sequence阶段读取并展开为多镜头
    └── 示例：
        ├── 正反打：JSON包含A角和B角 → Sequence生成2镜头
        ├── 动势组：JSON包含起势和落幅 → Sequence生成2镜头
        └── 蒙太奇组：JSON包含起势、高潮、余韵 → Sequence生成3-4镜头
        ↓
四宫格生成（sequence-board-prompt-{集数}-board*.md）
    ↓
    ├── 数据读取：
    │   ├── 【唯一数据源】JSON alternative_frames
    │   ├── 步骤1：读取 beat-board-full-list-{集数}.json
    │   ├── 步骤2：解析 grids[].alternative_frames
    │   └── 步骤3：根据策略标签确定展开规则
    ├── 展开逻辑：
    │   ├── [单镜]：1帧 → 1镜头（无需展开）
    │   ├── [动势组]：1帧 + 1替代帧 → 2镜头（起势 + 落幅）
    │   ├── [蒙太奇组]：1帧 + 2-3替代帧 → 3-4镜头（起势 + 高潮 + 余韵）
    │   ├── [长镜头]：1帧 + 0-2替代帧 → 1-3镜头（动态调整）
    │   ├── [正反打]：1帧 + 1替代帧 → 2镜头（A角 + B角）
    │   ├── [环境]/[特写]/[全景]/[中景]：1帧 → 1-2镜头
    │   └── [感官锚点]：插入规则，不展开
    ├── 输出包含：
    │   ├── 完整镜头序列（含主镜头 + 替代镜头）
    │   ├── 每个镜头的 alternative_frame_source 字段
    │   └── 镜头关系（正反打-A角、起势-动作开始、高潮-情绪爆发等）
    └── 数据输出：sequence-board-data-{集数}.json
        ↓
动态提示词生成（motion-prompt-{集数}.md）
    ↓
    ├── 数据读取：sequence-board-data-{集数}.json
    ├── 包含：完整的镜头序列（由Sequence阶段已展开）
    └── 输出：9组 Motion Prompt（每组1个关键帧 + 4个四宫格）
```

**关键修改（V4.1）：**
- ✅ 九宫格：每个格子 = 1个关键帧（单帧原则）
- ✅ JSON：alternative_frames 存储未选择的替代帧
- ✅ Sequence：读取 JSON，根据 strategy_tag 展开为多镜头
- ✅ 可追溯：每个镜头包含 alternative_frame_source
- ✅ 机器友好：唯一依赖JSON，无箭头格式兼容层

**详细实现：**
- Sequence 阶段展开逻辑：详见 `sequence-workflow.md`
- 四宫格模板和示例：详见 `sequence-board-template.md` "二、替代帧展开机制"
- 核心算法实现：详见 `dynamic-breakdown-engine.md` "JSON alternative_frames 读取与展开逻辑"
