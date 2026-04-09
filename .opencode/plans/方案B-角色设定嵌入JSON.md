# 方案B：将角色设定嵌入到scene-breakdown JSON中

## 核心思路
在提取器运行后，将角色设定**内嵌到** `outputs/scene-breakdown-{集数}.json` 中，使其成为节拍拆解JSON的一部分，后续所有环节可以自动继承，无需额外读取。

---

## 实现步骤

### 步骤1：修改提取器输出

**修改后输出结构**：
```json
{
  "meta": {
    "project_name": "猪打镇关西",
    "script_version": "2.0",
    "last_updated": "2026-02-03T15:57:51.289401",
    "style_modes": ["国潮动漫风格"]
  },
  "character_profiles": {
    "鲁达": {
      "国潮动漫": {
        "physical": "身形魁梧，身高九尺，腰阔十围；面圆耳大，满脸络腮虬髯",
        "headwear": "暗青灰色芝麻罗纱头巾，哑光无反光质感",
        "upper_body": "翡翠鹦哥绿朱丝战袍",
        "waist": "鸦青宫绦双股绦带",
        "footwear": "暗黄宋代风格靴子",
        "render_style": "平涂赛璐璐风格，墨线轮廓粗犷遒劲"
      }
    }
    ...
  },
  "scene_profiles": {...},
  "visual_style_modes": {...},
  "rendering_settings": {...}
}
```

将 `character_profiles` **复制并嵌入**到 scene-breakdown JSON中，命名为 `embedded_character_settings`。

---

### 步骤2：修改 `.claude/skills/film-storyboard-skill/templates/beat-breakdown-template.md`

在模板顶部的JSON结构中添加：

```markdown
```json
{
  "version": "4.1",
  "episode_id": "ep01",
  "visual_style": "国潮动漫风格",
  "target_medium": "漫剧",
  "aspect_ratio": "16:9横屏",

  // **新增：内嵌的角色设定**
  "embedded_character_settings": {
    "鲁达": {
      "国潮动漫": {
        "headwear": "暗青灰色芝麻罗纱头巾，哑光无反光质感",
        "upper_body": "翡翠鹦哥绿朱丝战袍",
        "waist": "鸦青宫绦双股绦带",
        ...
      }
    },
    "镇关西": {...},
    "包子猪": {...}
  },

  "shots": [...]
}
```

**说明**：
- 这些数据从 `configs/visual-style-specs.json` 读取后直接嵌入
- 包含完整的角色外貌设定（headwear、upper_body、waist、footwear等）
- 后续beatboard、sequence、motion阶段自动继承

---

### 步骤3：修改 AGENTS.md 的 contextFiles

**修改前**：
```markdown
| `/breakdown [集数]` | ... | [script/*-{集数}.md] + [scene-breakdown-{集数}.json] + [.agent-state.json]
```

**修改后**：
```markdown
| `/breakdown [集数]` | ... | [script/*-{集数}.md] + [configs/visual-style-specs.json] + [.agent-state.json]
```

**后续阶段的contextFiles不变**：
- `/beatboard [集数]`：`[scene-breakdown-{集数}.json, beat-breakdown-{集数}.md]`（已通过JSON继承角色设定）
- `/sequence [集数]`：`[scene-breakdown-{集数}.json, ...]`（已继承）
- `/motion [集数]`：`[scene-breakdown-{集数}.json, ...]`（已继承）

---

### 步骤4：在 film-storyboard-skill 中添加读取逻辑

在SKILL.md节拍拆解任务中添加：

```markdown
## 步骤1：运行视觉风格提取器（前置步骤）
**命令**：`python3 configs/auto-extractor.py`

**说明**：如果 `configs/visual-style-specs.json` 不存在或过期，自动提取角色设定

## 步骤2：读取角色设定并嵌入
```python
# 伪代码示意
character_settings = load_json("configs/visual-style-specs.json")
scene_breakdown["embedded_character_settings"] = character_settings["character_profiles"]
```

## 步骤3：基于角色设定生成节拍拆解
- 生成每个镜头时，参考 `embedded_character_settings` 中的角色外貌
- 禁止使用默认描述（如"粗布麻衣"）
- 确保：鲁达 = "翡翠鹦哥绿朱丝战袍" + "暗青灰色芝麻罗纱头巾" + "鸦青宫绦"
```

---

## 数据流转

```
script/猪打镇关西_v2.0.md
    ↓
python3 configs/auto-extractor.py（自动执行）
    ↓
configs/visual-style-specs.json（角色设定）
    ↓
film-storyboard-skill（breakdown任务）
    ↓
outputs/scene-breakdown-ep01.json（内嵌角色设定）
    ↓ (继承)
outputs/beat-breakdown-ep01.md（基于设定生成）
outputs/beat-board-prompt-ep01-board*.md（自动继承）
outputs/sequence-board-prompt-ep01.md（自动继承）
outputs/motion-prompt-ep01.md（自动继承）
```

---

## 优点
1. ✅ **单一数据流**：角色设定通过JSON自动流转，后续阶段无需额外配置
2. ✅ **状态一致性**：scene-breakdown JSON包含完整状态，回滚快照时保证一致性
3. ✅ **调试友好**：可以在JSON中直接查看当前使用的角色设定
4. ✅ **无配置依赖**：AGENTS.md后续阶段不需要额外修改

## 缺点
1. ❌ JSON文件较大，但影响小（角色设定只有几KB）
2. ❌ 需要修改提取器和SKILL，增加代码修改量

---

## 风险
- 如果提取器失败，`visual-style-specs.json` 不存在，需要降级处理
- 需要确保SKILL正确读取和嵌入角色设定

---

## 修改文件列表
1. `configs/auto-extractor.py` - 保持不变（已修复YAML解析）
2. `.claude/skills/film-storyboard-skill/templates/beat-breakdown-template.md` - 添加 `embedded_character_settings` 字段
3. `.claude/skills/film-storyboard-skill/SKILL.md` - 添加：1) 运行提取器步骤 2) 角色设定嵌入说明
4. `AGENTS.md` - 修改 `/breakdown` 的contextFiles为包含 `configs/visual-style-specs.json`

---

## 与方案A的区别

| 对比项 | 方案A | 方案B |
|--------|-------|--------|
| **数据传递方式** | 外部JSON传递 | JSON内嵌到scene-breakdown |
| **后续阶段依赖** | 需要读取visual-style-specs.json | 自动继承scene-breakdown JSON |
| **配置复杂度** | 需要修改workflows文档 | 需要修改SKILL和模板 |
| **数据一致性** | 多个JSON文件 | 单一文件 |
| **快照管理** | 需要额外备份visual-style-specs | 自动包含在快照中 |
