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
