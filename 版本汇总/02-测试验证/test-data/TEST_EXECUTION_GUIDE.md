# ANINEO V3.0 测试执行指南

## 概述
本指南提供了ANINEO V3.0恢复测试的执行步骤和验证方法。

## 测试环境准备

### 1. 检查系统状态
```bash
# 检查delegate_task工具状态
测试delegate_task工具是否恢复正常

# 检查V3.0配置
jq '.projectConfig' .agent-state.json

# 运行测试数据准备脚本
bash prepare-test-data.sh
```

### 2. 准备测试环境
```bash
# 备份现有输出
mkdir -p backup-test-outputs
cp -r outputs/* backup-test-outputs/ 2>/dev/null || true

# 清理测试输出
rm -rf outputs/* 2>/dev/null || true
```

## 测试执行步骤

### 测试1：英雄之旅结构验证
```bash
# 1. 设置配置
./test-data/test-configs.sh hero

# 2. 执行节拍拆解
delegate_task(...)  # 使用英雄之旅结构模板

# 3. 验证输出
./test-data/test-verification.sh hero
```

**预期结果**:
- ✅ 生成12个节拍
- ✅ 关键帧分布符合英雄之旅结构
- ✅ 导师角色出现在正确位置

### 测试2：短剧结构验证
```bash
# 1. 设置配置
./test-data/test-configs.sh micro

# 2. 执行节拍拆解
delegate_task(...)  # 使用多巴胺闭环结构模板

# 3. 验证输出
./test-data/test-verification.sh micro
```

**预期结果**:
- ✅ 生成4-6个节拍
- ✅ 时间分布符合短剧结构
- ✅ 结尾有悬念或CTA

### 测试3：权重计算新规则验证
```bash
# 1. 设置配置
./test-data/test-configs.sh action

# 2. 执行节拍拆解
delegate_task(...)  # 测试权重计算新规则

# 3. 验证输出
./test-data/test-verification.sh weight
```

**预期结果**:
- ✅ 检测到"爆炸"关键词
- ✅ 应用高强度动作权重
- ✅ 类型修正系数生效

### 测试4：潜台词分析验证
```bash
# 1. 设置配置
./test-data/test-configs.sh subtext

# 2. 执行节拍拆解
delegate_task(...)  # 测试潜台词分析系统

# 3. 验证输出
./test-data/test-verification.sh subtext
```

**预期结果**:
- ✅ 潜台词分析输出完整
- ✅ 识别出"口是心非"潜台词
- ✅ 心理动词分析正确

### 测试5：向后兼容性验证
```bash
# 1. 设置配置
./test-data/test-configs.sh backward

# 2. 执行节拍拆解
delegate_task(...)  # 测试向后兼容性

# 3. 验证输出
./test-data/test-verification.sh backward
```

**预期结果**:
- ✅ 输出格式与V2.0一致
- ✅ 现有字段完整
- ✅ 新增字段可选

## 测试报告

### 报告格式
测试完成后生成详细测试报告，包含：
1. **执行摘要**: 测试结果概述
2. **详细结果**: 每个测试用例的结果
3. **问题跟踪**: 发现的问题和修复状态
4. **性能数据**: 性能测试结果
5. **建议**: 改进建议和下一步行动

### 报告位置
测试报告保存在: `test-reports/v3-phase1-recovery-test-report.md`

## 故障排除

### 常见问题
1. **delegate_task工具故障**: 等待系统恢复，定期测试工具状态
2. **测试数据不完整**: 检查测试剧本是否存在
3. **配置设置失败**: 验证.agent-state.json文件权限和格式

### 联系支持
- **系统问题**: 联系系统管理员解决delegate_task工具故障
- **功能问题**: 联系开发团队解决V3.0功能问题
- **测试问题**: 联系测试团队解决测试执行问题

## 下一步行动
1. 系统恢复后立即执行恢复测试计划
2. 记录测试结果并生成报告
3. 修复发现的问题
4. 准备V3.0第二阶段优化
