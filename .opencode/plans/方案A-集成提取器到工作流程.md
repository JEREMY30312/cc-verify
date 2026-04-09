# 方案A：在film-storyboard-skill工作流程中集成提取器

## 核心思路
在节拍拆解（breakdown）流程的**第一步**自动运行提取器，确保角色信息在生成节拍拆解时就能被使用。

---

## 实现步骤

### 步骤1：修改 `.claude/workflows/breakdown-workflow.md`

在SKILL执行前添加提取器执行步骤：

```markdown
## Breakdown 工作流程

### 步骤1：运行视觉风格提取器
**执行内容**：
```bash
python3 configs/auto-extractor.py
```

**说明**：
- 自动从 `script/猪打镇关西_v2.0.md` 提取角色设定
- 输出到 `configs/visual-style-specs.json`
- 输出包含：角色外貌、渲染风格、场景设定

**错误处理**：
- 如果提取失败，继续执行但记录警告
- 如果 `visual-style-specs.json` 不存在，使用默认值

---

### 步骤2：调用 SKILL（film-storyboard-skill）
**上下文文件（contextFiles）**：
- `script/猪打镇关西_v2.0.md`（原文）
- `configs/visual-style-specs.json`（新生成的角色设定）
- `.agent-state.json`（项目状态）

**关键修改**：在 SKILL.md 中添加读取角色设定的说明
```
在生成节拍拆解时，必须参考 configs/visual-style-specs.json 中的角色设定：
- 鲁达：暗青灰色芝麻罗纱头巾、翡翠鹦哥绿朱丝战袍、鸦青宫绦
- 镇关西：黑色幞头、褐色粗布短衫、麻布围裙
- 包子猪：白色衬衫、蓝色背带短裤、粉色皮肤
```
```

---

### 步骤3：生成节拍拆解（SKILL执行）
**要求**：
- 严格基于原文内容
- 使用 `visual-style-specs.json` 中的角色设定
- 禁止使用错误的默认描述（如"粗布麻衣"）

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
outputs/beat-breakdown-ep01.md（含正确角色外貌）
outputs/scene-breakdown-ep01.json
```

---

## 优点
1. ✅ 角色信息**永远是最新的**，每次节拍拆解都重新提取
2. ✅ 不需要手动维护visual-style-specs.json，自动同步
3. ✅ 单一数据源（script文件），避免不一致

## 缺点
1. ❌ 每次运行都需要提取器执行（性能开销小，但增加步骤）
2. ❌ 需要修改workflows文档，增加流程复杂度

---

## 风险
- 提取器失败时，节拍拆解可能缺少角色信息
- 需要Python环境支持

---

## 修改文件列表
1. `.claude/workflows/breakdown-workflow.md` - 添加提取器执行步骤
2. `.claude/skills/film-storyboard-skill/SKILL.md` - 添加角色设定引用说明
