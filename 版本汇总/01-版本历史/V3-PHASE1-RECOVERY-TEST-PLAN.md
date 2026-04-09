# ANINEO V3.0 第一阶段恢复测试计划

## 背景

由于 `delegate_task` 工具持续故障（返回 `JSON Parse error: Unexpected EOF`），无法执行实际的分镜生成测试。本计划详细说明了系统恢复后需要执行的测试任务。

## 当前状态

### ✅ 已完成的工作
1. **核心架构**: 100% 完成
2. **静态验证**: 100% 完成（43个检查点全部通过）
3. **文件集成**: 所有V3.0文件集成正确
4. **配置系统**: .agent-state.json扩展完成
5. **文档更新**: AGENTS.md更新为V3.0版本

### ⚠️ 待完成的工作
1. **实际功能测试**: 0% 完成（等待系统恢复）
2. **性能验证**: 0% 完成（等待系统恢复）
3. **用户验收测试**: 0% 完成（等待系统恢复）

## 恢复测试目标

### 主要目标
验证ANINEO V3.0第一阶段优化的所有新功能在实际分镜生成中的正确性和性能。

### 具体目标
1. **验证四种结构模板**：确保每种叙事结构都能正确应用
2. **测试权重计算新规则**：验证类型化权重算法的正确性
3. **验证潜台词分析**：测试潜台词分析系统的输出质量
4. **检查向后兼容性**：确保现有项目不受影响
5. **验证性能影响**：确保新功能不显著降低系统性能

## 测试环境准备

### 1. 环境检查（5分钟）
```bash
# 检查delegate_task工具状态
测试delegate_task工具是否恢复正常

# 检查V3.0配置
jq '.projectConfig' .agent-state.json

# 检查测试剧本
ls -la script/猪打镇关西_v2.0.md

# 检查输出目录
ls -la outputs/
```

### 2. 测试数据准备（10分钟）
```bash
# 备份现有输出
mkdir -p backup-test-outputs
cp -r outputs/* backup-test-outputs/ 2>/dev/null || true

# 清理测试输出
rm -rf outputs/* 2>/dev/null || true
```

## 测试执行计划

### 测试1：英雄之旅结构验证（30分钟）

#### 测试目标
验证英雄之旅（Hero's Journey）12步结构模板的正确应用。

#### 测试步骤
1. **配置设置**：
   ```bash
   # 更新配置为英雄之旅结构
   jq '.projectConfig.narrative_structure = "hero_journey"' .agent-state.json > temp.json && mv temp.json .agent-state.json
   jq '.projectConfig.genre = "fantasy"' .agent-state.json > temp.json && mv temp.json .agent-state.json
   ```

2. **执行节拍拆解**：
   ```bash
   # 使用delegate_task执行节拍拆解
   delegate_task(
     category="unspecified-high",
     load_skills=["film-storyboard-skill"],
     prompt="执行节拍拆解，使用英雄之旅结构模板"
   )
   ```

3. **验证输出**：
   - 检查生成的节拍拆解表
   - 验证是否生成12个节拍
   - 验证节拍5、8、11是否为🔴特级关键帧
   - 验证节拍4是否包含"导师"角色

#### 预期结果
- ✅ 生成12个节拍
- ✅ 关键帧分布符合英雄之旅结构
- ✅ 导师角色出现在正确位置

### 测试2：短剧结构验证（20分钟）

#### 测试目标
验证多巴胺闭环（Micro-Drama Loop）短剧结构的正确应用。

#### 测试步骤
1. **配置设置**：
   ```bash
   # 更新配置为短剧结构
   jq '.projectConfig.narrative_structure = "micro_drama_loop"' .agent-state.json > temp.json && mv temp.json .agent-state.json
   jq '.projectConfig.genre = "comedy"' .agent-state.json > temp.json && mv temp.json .agent-state.json
   ```

2. **执行节拍拆解**：
   ```bash
   # 使用delegate_task执行节拍拆解
   delegate_task(
     category="unspecified-high",
     load_skills=["film-storyboard-skill"],
     prompt="执行节拍拆解，使用多巴胺闭环结构模板"
   )
   ```

3. **验证输出**：
   - 检查生成的节拍拆解表
   - 验证是否生成4-6个节拍
   - 验证每45秒是否有一个🔴或🟠关键帧
   - 验证结尾是否有悬念或CTA

#### 预期结果
- ✅ 生成4-6个节拍
- ✅ 时间分布符合短剧结构
- ✅ 结尾有悬念或CTA

### 测试3：权重计算新规则验证（25分钟）

#### 测试目标
验证类型化戏剧权重计算算法的正确性。

#### 测试步骤
1. **配置设置**：
   ```bash
   # 更新配置为动作片类型
   jq '.projectConfig.narrative_structure = "classic_three_act"' .agent-state.json > temp.json && mv temp.json .agent-state.json
   jq '.projectConfig.genre = "action"' .agent-state.json > temp.json && mv temp.json .agent-state.json
   jq '.projectConfig.enable_advanced_weights = true' .agent-state.json > temp.json && mv temp.json .agent-state.json
   ```

2. **准备测试剧本**：
   - 创建包含"爆炸"关键词的测试场景
   - 确保场景包含高强度动作事件

3. **执行节拍拆解**：
   ```bash
   # 使用delegate_task执行节拍拆解
   delegate_task(
     category="unspecified-high",
     load_skills=["film-storyboard-skill"],
     prompt="执行节拍拆解，测试权重计算新规则"
   )
   ```

4. **验证权重计算**：
   - 检查权重计算日志
   - 验证是否检测到"爆炸"关键词
   - 验证是否应用了高强度动作权重
   - 验证类型修正系数是否生效

#### 预期结果
- ✅ 检测到"爆炸"关键词
- ✅ 应用高强度动作权重（2.0-3.0范围）
- ✅ 类型修正系数生效（动作片×1.5）

### 测试4：潜台词分析验证（25分钟）

#### 测试目标
验证潜台词分析系统的输出质量。

#### 测试步骤
1. **配置设置**：
   ```bash
   # 启用潜台词分析
   jq '.projectConfig.enable_subtext_analysis = true' .agent-state.json > temp.json && mv temp.json .agent-state.json
   ```

2. **准备测试对话**：
   - 创建包含"我爱你" + 动作"后退三步"的测试场景
   - 确保场景包含表面动作和潜在心理动机的矛盾

3. **执行节拍拆解**：
   ```bash
   # 使用delegate_task执行节拍拆解
   delegate_task(
     category="unspecified-high",
     load_skills=["film-storyboard-skill"],
     prompt="执行节拍拆解，测试潜台词分析系统"
   )
   ```

4. **验证潜台词分析**：
   - 检查潜台词分析输出
   - 验证潜台词是否为"口是心非"
   - 验证心理动词是否包含["掩饰", "恐惧"]
   - 验证视觉对应物是否包含微动作

#### 预期结果
- ✅ 潜台词分析输出完整
- ✅ 识别出"口是心非"潜台词
- ✅ 心理动词分析正确
- ✅ 视觉对应物具体可拍摄

### 测试5：向后兼容性验证（15分钟）

#### 测试目标
验证现有项目不受V3.0更新的影响。

#### 测试步骤
1. **配置设置**：
   ```bash
   # 恢复为经典三幕式结构（默认）
   jq '.projectConfig.narrative_structure = "classic_three_act"' .agent-state.json > temp.json && mv temp.json .agent-state.json
   jq '.projectConfig.enable_subtext_analysis = false' .agent-state.json > temp.json && mv temp.json .agent-state.json
   jq '.projectConfig.enable_advanced_weights = false' .agent-state.json > temp.json && mv temp.json .agent-state.json
   ```

2. **执行节拍拆解**：
   ```bash
   # 使用delegate_task执行节拍拆解
   delegate_task(
     category="unspecified-high",
     load_skills=["film-storyboard-skill"],
     prompt="执行节拍拆解，测试向后兼容性"
   )
   ```

3. **验证输出格式**：
   - 检查输出格式是否与V2.0一致
   - 验证现有字段是否完整
   - 验证新增字段是否可选

#### 预期结果
- ✅ 输出格式与V2.0一致
- ✅ 现有字段完整
- ✅ 新增字段可选（不影响现有功能）

### 测试6：性能影响验证（20分钟）

#### 测试目标
验证V3.0新功能对系统性能的影响。

#### 测试步骤
1. **性能基准测试**：
   ```bash
   # 记录V2.0性能基准
   time delegate_task(...)  # 记录执行时间
   ```

2. **V3.0性能测试**：
   ```bash
   # 启用所有V3.0功能
   jq '.projectConfig.enable_subtext_analysis = true' .agent-state.json > temp.json && mv temp.json .agent-state.json
   jq '.projectConfig.enable_advanced_weights = true' .agent-state.json > temp.json && mv temp.json .agent-state.json
   
   # 记录V3.0性能
   time delegate_task(...)  # 记录执行时间
   ```

3. **性能对比分析**：
   - 计算性能差异百分比
   - 验证是否在可接受范围内（< 2秒/节拍）
   - 验证潜台词分析增加时间（< 500ms）

#### 预期结果
- ✅ 每个节拍分析时间 < 2秒
- ✅ 潜台词分析增加时间 < 500ms
- ✅ 总体性能影响在可接受范围内

## 测试执行时间表

| 测试 | 预计时间 | 优先级 | 依赖 |
|------|----------|--------|------|
| 环境检查 | 5分钟 | 高 | 无 |
| 测试数据准备 | 10分钟 | 高 | 环境检查 |
| 测试1：英雄之旅 | 30分钟 | 高 | 数据准备 |
| 测试2：短剧结构 | 20分钟 | 高 | 测试1完成 |
| 测试3：权重计算 | 25分钟 | 高 | 测试2完成 |
| 测试4：潜台词分析 | 25分钟 | 高 | 测试3完成 |
| 测试5：向后兼容 | 15分钟 | 中 | 测试4完成 |
| 测试6：性能影响 | 20分钟 | 中 | 测试5完成 |
| **总计** | **150分钟** | | |

## 成功标准

### 功能成功标准
1. ✅ 四种结构模板都能正确应用
2. ✅ 权重计算新规则工作正常
3. ✅ 潜台词分析输出具体可用
4. ✅ 向后兼容性保持
5. ✅ 性能影响在可接受范围内

### 技术成功标准
1. ✅ 所有测试用例执行完成
2. ✅ 测试结果记录完整
3. ✅ 问题跟踪和修复
4. ✅ 测试报告生成

## 风险缓解

### 风险1：delegate_task工具仍然故障
- **缓解措施**：等待系统恢复，定期测试工具状态
- **备用方案**：继续手动验证静态功能

### 风险2：测试数据不完整
- **缓解措施**：创建完整的测试数据集
- **备用方案**：使用现有剧本进行测试

### 风险3：性能影响超出预期
- **缓解措施**：优化算法实现
- **备用方案**：提供性能优化建议

## 测试报告

### 报告格式
测试完成后生成详细测试报告，包含：
1. **执行摘要**：测试结果概述
2. **详细结果**：每个测试用例的结果
3. **问题跟踪**：发现的问题和修复状态
4. **性能数据**：性能测试结果
5. **建议**：改进建议和下一步行动

### 报告位置
测试报告将保存在：`test-reports/v3-phase1-recovery-test-report.md`

## 下一步行动

### 立即行动
1. 监控delegate_task工具状态
2. 准备测试环境
3. 创建测试数据集

### 系统恢复后行动
1. 按照本计划执行所有测试
2. 记录测试结果
3. 生成测试报告
4. 修复发现的问题

### 长期行动
1. 基于测试结果优化V3.0功能
2. 监控生产环境中的V3.0使用情况
3. 收集用户反馈进行持续改进

## 联系方式

### 测试负责人
- **姓名**: ANINEO V3.0 测试团队
- **角色**: 测试执行和验证
- **责任**: 确保所有测试按计划执行

### 技术支持
- **系统问题**: 联系系统管理员解决delegate_task工具故障
- **功能问题**: 联系开发团队解决V3.0功能问题
- **测试问题**: 联系测试团队解决测试执行问题

---

**最后更新**: 2026-01-27  
**版本**: 1.0  
**状态**: 等待执行（系统恢复后）