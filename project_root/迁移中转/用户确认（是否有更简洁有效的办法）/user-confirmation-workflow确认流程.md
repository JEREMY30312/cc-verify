# 用户确认工作流程

> **【核心原则】**
>
> 用户确认是项目质量控制的最后一道防线，必须确保用户对产出有完全控制权。

---

## 核心规则

### 规则1：强制停止原则

**每个确认点（CP1-CP5）完成后，必须强制停止执行，等待用户显式指令。**

```python
# ✅ 正确流程
# 步骤1：生成主产物
task(...)

# 步骤2：导演审核
task(...)

# 步骤3：显示确认UI + 调用 question 工具
display_confirmation_ui()
result = question(...)  # 用户选择"通过"/"修改"/"重生成"/"回滚"/"终止"

# ⚠️ 关键：立即停止，不继续执行
print("等待用户指令...")
# 不要继续执行快照、状态更新等后续步骤

# ✅ 等待用户显式输入
# 只有用户输入："继续"、"通过"、"执行下一步"等明确指令后
# 才执行步骤4（快照）和步骤5（状态更新）
```

```python
# ❌ 错误流程
# 步骤1：生成主产物
task(...)

# 步骤2：导演审核
task(...)

# 步骤3：显示确认UI + 调用 question 工具
display_confirmation_ui()
result = question(...)  # 用户选择"通过"

# ❌ 错误：立即继续执行快照和状态更新
create_snapshot()  # 不应该在这里执行
update_agent_state()  # 不应该在这里执行
```

### 规则2：显式指令原则

**只有收到用户的显式指令后，才能继续执行后续步骤。**

**有效指令示例**：
- "继续"
- "通过"
- "执行下一步"
- "创建快照"
- "进入下一阶段"

**无效指令**：
- ❌ `question` 工具的返回值（如 "✅ 通过"）
- ❌ 用户的选择（如 "选项1"）
- ❌ 用户的简短回复（如 "OK"、"好的"）

**正确处理**：
```python
# ✅ 正确处理
result = question(...)  # 返回："✅ 通过"

# 显示总结信息
print(f"用户选择了：{result}")
print("等待确认后继续...")

# 停止，不继续执行

# 用户输入："继续" 或 "通过"
# ✅ 现在可以继续执行
create_snapshot()
update_agent_state()
```

### 规则3：状态保持原则

**在等待用户确认期间，保持所有文件和状态不变。**

- 不要创建快照（用户还未确认）
- 不要更新 `.agent-state.json`（phase 应该保持为当前阶段）
- 不要修改任何产出文件

**只有在用户显式确认后**，才执行：
- 创建快照
- 更新 `.agent-state.json` 的 phase
- 更新 subagent 的 last_used 时间戳

---

## 工作流程模板

### CP1-CP5 标准流程

```python
def execute_phase_with_confirmation(phase_name, generation_prompt, review_prompt):
    """
    执行带有用户确认的标准流程

    Args:
        phase_name: 阶段名称（如 "breakdown"、"beatboard"）
        generation_prompt: 生成主产物的 prompt
        review_prompt: 审核的 prompt
    """

    # ========== 步骤1：生成主产物 ==========
    print(f"【步骤1】生成 {phase_name} 主产物...")
    generation_result = task(subagent_type="designer", prompt=generation_prompt)

    # ========== 步骤2：导演审核 ==========
    print(f"【步骤2】执行 {phase_name} 审核...")
    review_result = task(subagent_type="designer", prompt=review_prompt)

    # ========== 步骤3：用户确认 ==========
    print(f"【步骤3】执行 {phase_name} 用户确认...")

    # 显示确认UI
    display_confirmation_ui(phase_name, review_result)

    # 调用 question 工具
    result = question(
        questions=[{
            "question": f"{phase_name} 已完成，请选择下一步：",
            "header": "用户确认",
            "options": [
                {"label": "✅ 通过", "description": "确认质量，进入下一阶段"},
                {"label": "✏️ 修改", "description": "提出具体修改意见"},
                {"label": "🔄 重生成", "description": "不满意，重新生成"},
                {"label": "⏪ 回滚", "description": "恢复到历史快照"},
                {"label": "❌ 终止", "description": "停止当前项目"}
            ]
        }]
    )

    # ⚠️ 关键：立即停止，不继续执行
    print(f"用户选择了：{result}")
    print("等待用户确认后继续执行快照和状态更新...")
    print("请输入 '继续' 或 '通过' 来执行下一步操作。")

    # ⛔ 停止在这里，不继续执行
    # 等待用户的显式指令

    # ========== 用户显式确认后才继续 ==========

    # ========== 步骤4：创建快照 ==========
    print(f"【步骤4】创建快照...")
    snapshot_id = create_snapshot(phase_name)

    # ========== 步骤5：更新状态 ==========
    print(f"【步骤5】更新状态...")
    update_agent_state(phase_name)

    print(f"✅ {phase_name} 阶段完成！")
```

---

## 各阶段详细流程

### CP1: 节拍拆解确认

```python
# 步骤1：生成节拍拆解
task(prompt="生成节拍拆解...")

# 步骤2：导演审核
task(prompt="审核节拍拆解...")

# 步骤3：用户确认
display_confirmation_ui()
result = question(...)

# ⚠️ 停止，等待用户显式指令

# 用户输入："继续"
# 步骤4：创建快照
create_snapshot()

# 步骤5：更新状态
update_agent_state(phase="beatboard")
```

### CP2: 九宫格确认

```python
# 步骤1：生成九宫格
task(prompt="生成九宫格提示词...")

# 步骤2：导演审核
task(prompt="审核九宫格提示词...")

# 步骤3：用户确认
display_confirmation_ui()
result = question(...)

# ⚠️ 停止，等待用户显式指令

# 用户输入："继续"
# 步骤4：创建快照
create_snapshot()

# 步骤5：更新状态
update_agent_state(phase="sequence")
```

### CP3: 四宫格确认

```python
# 步骤1：生成四宫格
task(prompt="生成四宫格提示词...")

# 步骤2：导演审核
task(prompt="审核四宫格提示词...")

# 步骤3：用户确认
display_confirmation_ui()
result = question(...)

# ⚠️ 停止，等待用户显式指令

# 用户输入："继续"
# 步骤4：创建快照
create_snapshot()

# 步骤5：更新状态
update_agent_state(phase="motion")
```

---

## 错误案例对比

### 案例1：自动默认确认（错误）

```python
# ❌ 错误流程

# 步骤1：生成
task(...)

# 步骤2：审核
task(...)

# 步骤3：显示UI + question
display_ui()
result = question(...)  # 用户选择"通过"

# ❌ 错误：自动继续执行
create_snapshot()  # 不应该在这里执行
update_state()  # 不应该在这里执行
print("✅ 已自动继续")

# 问题：用户没有显式确认，系统自动执行了后续步骤
```

### 案例2：强制停止等待（正确）

```python
# ✅ 正确流程

# 步骤1：生成
task(...)

# 步骤2：审核
task(...)

# 步骤3：显示UI + question
display_ui()
result = question(...)  # 用户选择"通过"

# ✅ 正确：立即停止
print(f"用户选择了：{result}")
print("等待用户确认后继续...")
# 不执行任何后续操作

# 用户输入："继续"
# ✅ 现在执行后续步骤
create_snapshot()
update_state()
print("✅ 已继续执行")
```

---

## 检查清单

在每个确认点（CP1-CP5），确保以下步骤：

- [ ] 已生成主产物
- [ ] 已完成导演审核
- [ ] 已显示确认UI
- [ ] 已调用 question 工具
- [ ] ⚠️ **已停止执行，不继续**
- [ ] ⚠️ **等待用户显式指令**
- [ ] 用户输入："继续"或"通过"
- [ ] ✅ **现在执行快照**
- [ ] ✅ **现在更新状态**
- [ ] ✅ **输出完成总结**

---

## 与快照管理的关系

### 确认前
- 不要创建快照
- 保持 `.agent-state.json` 的 phase 不变
- 保持所有 subagent 的 last_used 不变

### 确认后（用户显式指令）
- 创建快照（包含 `.agent-state.json` 和产出文件）
- 更新 `.agent-state.json` 的 phase
- 更新 subagent 的 last_used 时间戳

### 回滚操作
如果用户选择"回滚"：
- 恢复历史快照
- 重新显示确认UI
- 等待用户显式指令

---

## 相关文件

| 文件 | 说明 |
|------|------|
| `AGENTS.md` | 主配置文件，定义整体架构 |
| `common/user-confirmation-protocol.md` | 用户确认协议（理论规范）|
| `common/snapshot-management.md` | 快照管理规则 |
| `user-confirmation-workflow.md` | 本文件（实施规范）|

---

**版本**: 1.0
**创建日期**: 2026-02-01
**状态**: ✅ 活跃
