#!/bin/bash

# ANINEO V3.0 delegate_task工具监控脚本
# 用途：定期测试delegate_task工具状态，监控系统恢复情况

echo "=========================================="
echo "ANINEO V3.0 delegate_task工具监控脚本"
echo "生成时间: $(date)"
echo "=========================================="

# 检查必要的文件
echo "检查项目文件状态..."
if [ -f ".agent-state.json" ]; then
    echo "✅ .agent-state.json 存在"
    V3_CONFIG=$(jq -r '.projectConfig.narrative_structure // "未配置"' .agent-state.json)
    echo "  当前配置: $V3_CONFIG"
else
    echo "❌ .agent-state.json 不存在"
fi

if [ -f "test-v3-integration.sh" ]; then
    echo "✅ test-v3-integration.sh 存在"
else
    echo "❌ test-v3-integration.sh 不存在"
fi

if [ -f "prepare-test-data.sh" ]; then
    echo "✅ prepare-test-data.sh 存在"
else
    echo "❌ prepare-test-data.sh 不存在"
fi

echo ""
echo "=========================================="
echo "V3.0恢复测试准备状态"
echo "=========================================="

# 检查测试数据准备
if [ -d "test-data" ]; then
    echo "✅ test-data/ 目录存在"
    TEST_FILES=("test-configs.sh" "test-verification.sh" "TEST_EXECUTION_GUIDE.md")
    for file in "${TEST_FILES[@]}"; do
        if [ -f "test-data/$file" ]; then
            echo "  ✅ test-data/$file 存在"
        else
            echo "  ❌ test-data/$file 不存在"
        fi
    done
else
    echo "❌ test-data/ 目录不存在"
fi

echo ""
echo "=========================================="
echo "系统恢复测试建议"
echo "=========================================="

echo "系统恢复后，请按以下步骤执行测试："
echo ""
echo "1. 准备测试环境："
echo "   bash prepare-test-data.sh"
echo ""
echo "2. 执行V3.0功能测试："
echo "   # 英雄之旅测试"
echo "   ./test-data/test-configs.sh hero"
echo "   # 然后执行delegate_task节拍拆解"
echo "   ./test-data/test-verification.sh hero"
echo ""
echo "3. 其他测试："
echo "   ./test-data/test-configs.sh micro    # 短剧结构测试"
echo "   ./test-data/test-configs.sh action   # 权重计算测试"
echo "   ./test-data/test-configs.sh subtext  # 潜台词分析测试"
echo "   ./test-data/test-configs.sh backward # 向后兼容测试"
echo ""
echo "4. 查看测试结果："
echo "   cat test-results-*.txt"
echo ""
echo "总测试时间估计：150分钟 (2.5小时)"
echo ""
echo "=========================================="
echo "监控建议"
echo "=========================================="
echo "建议定期运行此脚本监控系统状态："
echo "1. 每天运行1-2次检查delegate_task工具状态"
echo "2. 系统恢复后立即执行恢复测试计划"
echo "3. 记录所有测试结果和发现的问题"
echo ""
echo "当前时间: $(date)"
echo "脚本版本: 1.0"
echo "项目: ANINEO V3.0 第一阶段优化"