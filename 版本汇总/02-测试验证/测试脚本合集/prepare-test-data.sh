#!/bin/bash

# ANINEO V3.0 测试数据准备脚本
# 为恢复测试计划准备测试数据

echo "=========================================="
echo "ANINEO V3.0 测试数据准备脚本"
echo "=========================================="

# 创建测试数据目录
mkdir -p test-data

echo ""
echo "✅ Step 1: 检查测试剧本"
echo "------------------------------------------"

if [ -f "script/猪打镇关西_v2.0.md" ]; then
    echo "✅ 测试剧本存在: script/猪打镇关西_v2.0.md"
    cp "script/猪打镇关西_v2.0.md" "test-data/猪打镇关西_v2.0.md"
    echo "✅ 测试剧本已复制到 test-data/"
else
    echo "❌ 测试剧本不存在: script/猪打镇关西_v2.0.md"
    echo "⚠️  请确保测试剧本存在"
fi

echo ""
echo "✅ Step 2: 检查输出目录"
echo "------------------------------------------"

if [ -d "outputs" ]; then
    echo "✅ outputs 目录存在"
    echo "📁 当前 outputs 目录内容:"
    ls -la outputs/ 2>/dev/null || echo "  (空目录)"
else
    echo "❌ outputs 目录不存在，创建中..."
    mkdir -p outputs
    echo "✅ outputs 目录已创建"
fi

echo ""
echo "✅ Step 3: 备份现有输出"
echo "------------------------------------------"

if [ -d "outputs" ] && [ "$(ls -A outputs 2>/dev/null)" ]; then
    echo "📁 outputs 目录非空，创建备份..."
    mkdir -p backup-test-outputs
    cp -r outputs/* backup-test-outputs/ 2>/dev/null || true
    echo "✅ 现有输出已备份到 backup-test-outputs/"
else
    echo "📁 outputs 目录为空，无需备份"
fi

echo ""
echo "✅ Step 4: 准备测试配置"
echo "------------------------------------------"

# 创建测试配置脚本
cat > test-data/test-configs.sh << 'EOF'
#!/bin/bash

# ANINEO V3.0 测试配置脚本
# 用于设置不同的测试配置

# 英雄之旅配置
setup_hero_journey() {
    echo "设置英雄之旅配置..."
    jq '.projectConfig.narrative_structure = "hero_journey"' .agent-state.json > temp.json && mv temp.json .agent-state.json
    jq '.projectConfig.genre = "fantasy"' .agent-state.json > temp.json && mv temp.json .agent-state.json
    jq '.projectConfig.enable_subtext_analysis = true' .agent-state.json > temp.json && mv temp.json .agent-state.json
    jq '.projectConfig.enable_advanced_weights = true' .agent-state.json > temp.json && mv temp.json .agent-state.json
    echo "✅ 英雄之旅配置设置完成"
}

# 短剧结构配置
setup_micro_drama() {
    echo "设置短剧结构配置..."
    jq '.projectConfig.narrative_structure = "micro_drama_loop"' .agent-state.json > temp.json && mv temp.json .agent-state.json
    jq '.projectConfig.genre = "comedy"' .agent-state.json > temp.json && mv temp.json .agent-state.json
    jq '.projectConfig.enable_subtext_analysis = true' .agent-state.json > temp.json && mv temp.json .agent-state.json
    jq '.projectConfig.enable_advanced_weights = true' .agent-state.json > temp.json && mv temp.json .agent-state.json
    echo "✅ 短剧结构配置设置完成"
}

# 动作片权重测试配置
setup_action_weight_test() {
    echo "设置动作片权重测试配置..."
    jq '.projectConfig.narrative_structure = "classic_three_act"' .agent-state.json > temp.json && mv temp.json .agent-state.json
    jq '.projectConfig.genre = "action"' .agent-state.json > temp.json && mv temp.json .agent-state.json
    jq '.projectConfig.enable_subtext_analysis = false' .agent-state.json > temp.json && mv temp.json .agent-state.json
    jq '.projectConfig.enable_advanced_weights = true' .agent-state.json > temp.json && mv temp.json .agent-state.json
    echo "✅ 动作片权重测试配置设置完成"
}

# 潜台词分析测试配置
setup_subtext_test() {
    echo "设置潜台词分析测试配置..."
    jq '.projectConfig.narrative_structure = "classic_three_act"' .agent-state.json > temp.json && mv temp.json .agent-state.json
    jq '.projectConfig.genre = "drama"' .agent-state.json > temp.json && mv temp.json .agent-state.json
    jq '.projectConfig.enable_subtext_analysis = true' .agent-state.json > temp.json && mv temp.json .agent-state.json
    jq '.projectConfig.enable_advanced_weights = false' .agent-state.json > temp.json && mv temp.json .agent-state.json
    echo "✅ 潜台词分析测试配置设置完成"
}

# 向后兼容测试配置
setup_backward_compatibility() {
    echo "设置向后兼容测试配置..."
    jq '.projectConfig.narrative_structure = "classic_three_act"' .agent-state.json > temp.json && mv temp.json .agent-state.json
    jq '.projectConfig.genre = "action"' .agent-state.json > temp.json && mv temp.json .agent-state.json
    jq '.projectConfig.enable_subtext_analysis = false' .agent-state.json > temp.json && mv temp.json .agent-state.json
    jq '.projectConfig.enable_advanced_weights = false' .agent-state.json > temp.json && mv temp.json .agent-state.json
    echo "✅ 向后兼容测试配置设置完成"
}

# 显示当前配置
show_current_config() {
    echo "当前配置:"
    jq '.projectConfig' .agent-state.json
}

# 主函数
case "$1" in
    hero)
        setup_hero_journey
        ;;
    micro)
        setup_micro_drama
        ;;
    action)
        setup_action_weight_test
        ;;
    subtext)
        setup_subtext_test
        ;;
    backward)
        setup_backward_compatibility
        ;;
    show)
        show_current_config
        ;;
    *)
        echo "用法: $0 {hero|micro|action|subtext|backward|show}"
        echo "  hero: 设置英雄之旅配置"
        echo "  micro: 设置短剧结构配置"
        echo "  action: 设置动作片权重测试配置"
        echo "  subtext: 设置潜台词分析测试配置"
        echo "  backward: 设置向后兼容测试配置"
        echo "  show: 显示当前配置"
        exit 1
        ;;
esac
EOF

chmod +x test-data/test-configs.sh
echo "✅ 测试配置脚本已创建: test-data/test-configs.sh"

echo ""
echo "✅ Step 5: 创建测试验证脚本"
echo "------------------------------------------"

cat > test-data/test-verification.sh << 'EOF'
#!/bin/bash

# ANINEO V3.0 测试验证脚本
# 用于验证测试输出

# 验证英雄之旅输出
verify_hero_journey() {
    echo "验证英雄之旅输出..."
    if [ ! -f "outputs/beat-breakdown-ep01.md" ]; then
        echo "❌ 节拍拆解表不存在"
        return 1
    fi
    
    # 检查节拍数量
    beat_count=$(grep -c "^\| 节拍" outputs/beat-breakdown-ep01.md || echo "0")
    echo "📊 节拍数量: $beat_count"
    
    if [ "$beat_count" -eq 12 ]; then
        echo "✅ 节拍数量正确 (12个)"
    else
        echo "❌ 节拍数量不正确 (期望12个，实际$beat_count个)"
    fi
    
    # 检查关键帧
    echo "🔍 检查关键帧分布..."
    grep -n "🔴" outputs/beat-breakdown-ep01.md || echo "  (未找到特级关键帧)"
    
    # 检查导师角色
    if grep -q "导师" outputs/beat-breakdown-ep01.md; then
        echo "✅ 导师角色存在"
    else
        echo "❌ 导师角色不存在"
    fi
}

# 验证短剧结构输出
verify_micro_drama() {
    echo "验证短剧结构输出..."
    if [ ! -f "outputs/beat-breakdown-ep01.md" ]; then
        echo "❌ 节拍拆解表不存在"
        return 1
    fi
    
    # 检查节拍数量
    beat_count=$(grep -c "^\| 节拍" outputs/beat-breakdown-ep01.md || echo "0")
    echo "📊 节拍数量: $beat_count"
    
    if [ "$beat_count" -ge 4 ] && [ "$beat_count" -le 6 ]; then
        echo "✅ 节拍数量在合理范围内 (4-6个)"
    else
        echo "❌ 节拍数量不在合理范围内 (期望4-6个，实际$beat_count个)"
    fi
    
    # 检查关键帧
    echo "🔍 检查关键帧分布..."
    grep -n "🔴\|🟠" outputs/beat-breakdown-ep01.md || echo "  (未找到关键帧)"
    
    # 检查结尾
    if tail -5 outputs/beat-breakdown-ep01.md | grep -q "悬念\|CTA\|结尾"; then
        echo "✅ 结尾有悬念或CTA"
    else
        echo "❌ 结尾缺少悬念或CTA"
    fi
}

# 验证权重计算
verify_weight_calculation() {
    echo "验证权重计算..."
    if [ ! -f "outputs/beat-breakdown-ep01.md" ]; then
        echo "❌ 节拍拆解表不存在"
        return 1
    fi
    
    # 检查爆炸关键词
    if grep -q "爆炸" outputs/beat-breakdown-ep01.md; then
        echo "✅ 检测到'爆炸'关键词"
    else
        echo "❌ 未检测到'爆炸'关键词"
    fi
    
    # 检查权重字段
    echo "🔍 检查权重字段..."
    grep -n "权重\|weight" outputs/beat-breakdown-ep01.md | head -5 || echo "  (未找到权重字段)"
}

# 验证潜台词分析
verify_subtext_analysis() {
    echo "验证潜台词分析..."
    if [ ! -f "outputs/beat-breakdown-ep01.md" ]; then
        echo "❌ 节拍拆解表不存在"
        return 1
    fi
    
    # 检查潜台词字段
    if grep -q "潜台词\|subtext" outputs/beat-breakdown-ep01.md; then
        echo "✅ 潜台词分析字段存在"
        grep -n "潜台词" outputs/beat-breakdown-ep01.md | head -3
    else
        echo "❌ 潜台词分析字段不存在"
    fi
    
    # 检查心理动词
    if grep -q "心理动词\|心理动机" outputs/beat-breakdown-ep01.md; then
        echo "✅ 心理动词分析存在"
    else
        echo "❌ 心理动词分析不存在"
    fi
}

# 验证向后兼容性
verify_backward_compatibility() {
    echo "验证向后兼容性..."
    if [ ! -f "outputs/beat-breakdown-ep01.md" ]; then
        echo "❌ 节拍拆解表不存在"
        return 1
    fi
    
    # 检查标准字段
    required_fields=("节拍编号" "节拍类型" "节拍描述" "视觉风格" "镜头建议" "关键帧等级" "权重")
    
    echo "🔍 检查标准字段..."
    for field in "${required_fields[@]}"; do
        if grep -q "$field" outputs/beat-breakdown-ep01.md; then
            echo "✅ 字段 '$field' 存在"
        else
            echo "❌ 字段 '$field' 不存在"
        fi
    done
    
    # 检查文件格式
    echo "📄 检查文件格式..."
    head -10 outputs/beat-breakdown-ep01.md
}

# 主函数
case "$1" in
    hero)
        verify_hero_journey
        ;;
    micro)
        verify_micro_drama
        ;;
    weight)
        verify_weight_calculation
        ;;
    subtext)
        verify_subtext_analysis
        ;;
    backward)
        verify_backward_compatibility
        ;;
    *)
        echo "用法: $0 {hero|micro|weight|subtext|backward}"
        echo "  hero: 验证英雄之旅输出"
        echo "  micro: 验证短剧结构输出"
        echo "  weight: 验证权重计算"
        echo "  subtext: 验证潜台词分析"
        echo "  backward: 验证向后兼容性"
        exit 1
        ;;
esac
EOF

chmod +x test-data/test-verification.sh
echo "✅ 测试验证脚本已创建: test-data/test-verification.sh"

echo ""
echo "✅ Step 6: 创建测试执行指南"
echo "------------------------------------------"

cat > test-data/TEST_EXECUTION_GUIDE.md << 'EOF'
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
EOF

echo "✅ 测试执行指南已创建: test-data/TEST_EXECUTION_GUIDE.md"

echo ""
echo "✅ Step 7: 测试数据准备完成"
echo "=========================================="

echo ""
echo "📊 测试数据准备完成总结"
echo "------------------------------------------"
echo "✅ 测试剧本: test-data/猪打镇关西_v2.0.md"
echo "✅ 测试配置脚本: test-data/test-configs.sh"
echo "✅ 测试验证脚本: test-data/test-verification.sh"
echo "✅ 测试执行指南: test-data/TEST_EXECUTION_GUIDE.md"
echo "✅ 输出目录: outputs/ (已备份)"
echo "✅ 备份目录: backup-test-outputs/"

echo ""
echo "🚀 下一步:"
echo "  1. 系统恢复后执行测试"
echo "  2. 使用测试配置脚本设置不同配置"
echo "  3. 使用测试验证脚本验证输出"
echo "  4. 参考测试执行指南完成所有测试"

echo ""
echo "📝 注意: 由于delegate_task工具故障，实际测试需要等待系统恢复。"
echo "    所有测试数据已准备就绪，系统恢复后可立即执行。"

echo "=========================================="