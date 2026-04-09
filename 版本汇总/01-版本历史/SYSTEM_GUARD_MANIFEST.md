# ANINEO 系统完整性自检与同步协议 (V2.0)

> **核心宗旨**：确保“冰山模型”数据一致性。当底层逻辑（Common/Skill）发生变动时，自动对齐展示层（Templates/Outputs）与调度层（Agents/AGENTS.md）。

---

## 🛠 第一阶段：变更影响审计 (Impact Audit)

当用户执行“优化”或“修改”指令后，AI 必须首先识别变更的“震中”并检索受影响的文件：

1. **逻辑层 (The Brain)**：若修改了 `beat-analyzer.md`（如 NDI 公式、权重），必须同步检查 `SKILL.md` 的步骤 4 与 `director.md` 的审核阈值。
2. **结构层 (The Skeleton)**：若修改了 `tween-algorithm.md`（补帧逻辑），必须核对 `sequence-board-template.md` 的补帧标记及 `animator.md` 的索引逻辑。
3. **表现层 (The Skin)**：若修改了任一 `templates/*.md`，必须确保 `SKILL.md` 的输出步骤（Step 7/11）能产生符合新模板的数据。

---

## 🔍 第二阶段：自动化完整性自检 (Integrity Checklist)

请依次运行以下检查项，任何一项返回 **FAIL** 必须停止任务并报告原因：

### 1. ID 链条验证 (ID Linkage)
- [ ] **子镜头对齐**：验证 `scene-breakdown.json` 中的 `sub_shots` 数组 ID（如 S05-1）是否 100% 显影在 `beat-board` 的对应格中。
- [ ] **补帧对齐**：根据公式 $$tween\_count = \lceil max\_gap / 1.5 \rceil$$ 重新计算相邻镜头，验证 `sequence-board` 中的补帧数量是否符合算法。

### 2. 导演审核项反推 (Review Backtracking)
- [ ] **阈值对齐**：检查 `director.md` 中的 `NDI_HIGH_THRESHOLD` 是否与 `beat-analyzer.md` 的最新定义一致。
- [ ] **规则覆盖**：若新增了“镜头动机”，检查 `director.md` 的【动机一致性】矩阵中是否已加入该动机的兼容性规则。

### 3. 指令路由检查 (Routing & Context)
- [ ] **上下文完整性**：检查 `AGENTS.md` 的指令路由表，确保 `/motion` 指令的 `contextFiles` 包含了 `scene-breakdown-tweened.json`（若启用了补帧）。

---

## ⚡ 第三阶段：原子化同步手术 (Atomic Sync)

若自检发现断裂，AI 需按以下优先级静默修复，严禁只改局部：

1. **先改定义**：更新 `common/` 下的逻辑文档。
2. **后改模板**：更新 `templates/` 下的输出格式。
3. **最后刷新 Skill**：更新 `SKILL.md` 的逻辑描述，并尝试对当前 `outputs/` 下受影响的 JSON 进行补解析。

---

## 📊 第四阶段：维护报告 (Maintenance Report)

任务完成后，必须输出以下格式的 JSON 元数据：

```json
{
  "maintenance_status": "PASS/FAIL",
  "integrity_score": 0, // 0-100
  "impact_scope": [], // 受影响文件列表
  "auto_repaired_items": [], // 自动修复项
  "manual_intervention_required": [] // 需要人工确认的逻辑断裂点
}