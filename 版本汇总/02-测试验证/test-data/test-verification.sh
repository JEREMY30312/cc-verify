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
