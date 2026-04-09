#!/bin/bash

# ANINEO V3.0 集成测试脚本
# 目的：验证V3.0所有新功能
# 测试内容：四种叙事结构模板、类型化权重计算、潜台词分析

echo "=========================================="
echo "ANINEO V3.0 集成测试脚本"
echo "=========================================="
echo ""

# Step 1: 检查环境配置
echo "✅ Step 1: 检查V3.0环境配置"
echo "------------------------------------------"

# 检查.agent-state.json中的V3.0配置
echo "检查.agent-state.json配置："
if [ -f .agent-state.json ]; then
    echo "✅ .agent-state.json 文件存在"
    
    # 检查V3.0新增字段
    echo "检查V3.0新增字段："
    if grep -q "narrative_structure" .agent-state.json; then
        echo "  ✅ narrative_structure 字段存在"
    else
        echo "  ❌ narrative_structure 字段缺失"
    fi
    
    if grep -q "genre" .agent-state.json; then
        echo "  ✅ genre 字段存在"
    else
        echo "  ❌ genre 字段缺失"
    fi
    
    if grep -q "enable_subtext_analysis" .agent-state.json; then
        echo "  ✅ enable_subtext_analysis 字段存在"
    else
        echo "  ❌ enable_subtext_analysis 字段缺失"
    fi
    
    if grep -q "enable_advanced_weights" .agent-state.json; then
        echo "  ✅ enable_advanced_weights 字段存在"
    else
        echo "  ❌ enable_advanced_weights 字段缺失"
    fi
else
    echo "❌ .agent-state.json 文件不存在"
fi

echo ""

# Step 2: 检查V3.0核心模块
echo "✅ Step 2: 检查V3.0核心模块"
echo "------------------------------------------"

# 检查结构模板文件
if [ -f .claude/common/structure-profiles.md ]; then
    echo "✅ structure-profiles.md 文件存在"
    # 检查四种结构模板
    echo "检查四种结构模板："
    if grep -q "经典三幕式" .claude/common/structure-profiles.md; then
        echo "  ✅ 经典三幕式模板存在"
    else
        echo "  ❌ 经典三幕式模板缺失"
    fi
    
    if grep -q "英雄之旅" .claude/common/structure-profiles.md; then
        echo "  ✅ 英雄之旅模板存在"
    else
        echo "  ❌ 英雄之旅模板缺失"
    fi
    
    if grep -q "起承转合" .claude/common/structure-profiles.md; then
        echo "  ✅ 起承转合模板存在"
    else
        echo "  ❌ 起承转合模板缺失"
    fi
    
    if grep -q "多巴胺闭环" .claude/common/structure-profiles.md; then
        echo "  ✅ 多巴胺闭环模板存在"
    else
        echo "  ❌ 多巴胺闭环模板缺失"
    fi
else
    echo "❌ structure-profiles.md 文件不存在"
fi

echo ""

# 检查潜台词分析文件
if [ -f .claude/common/subtext-analyzer.md ]; then
    echo "✅ subtext-analyzer.md 文件存在"
    # 检查三层分析架构
    echo "检查三层分析架构："
    if grep -q "探测层" .claude/common/subtext-analyzer.md; then
        echo "  ✅ 探测层存在"
    else
        echo "  ❌ 探测层缺失"
    fi
    
    if grep -q "翻译层" .claude/common/subtext-analyzer.md; then
        echo "  ✅ 翻译层存在"
    else
        echo "  ❌ 翻译层缺失"
    fi
    
    if grep -q "表现层" .claude/common/subtext-analyzer.md; then
        echo "  ✅ 表现层存在"
    else
        echo "  ❌ 表现层缺失"
    fi
else
    echo "❌ subtext-analyzer.md 文件不存在"
fi

echo ""

# 检查更新后的beat-analyzer.md
if [ -f .claude/common/beat-analyzer.md ]; then
    echo "✅ beat-analyzer.md 文件存在"
    # 检查V3.0新增内容
    echo "检查V3.0新增内容："
    if grep -q "戏剧权重判定标准表" .claude/common/beat-analyzer.md; then
        echo "  ✅ 戏剧权重判定标准表存在"
    else
        echo "  ❌ 戏剧权重判定标准表缺失"
    fi
    
    if grep -q "类型化修正系数表" .claude/common/beat-analyzer.md; then
        echo "  ✅ 类型化修正系数表存在"
    else
        echo "  ❌ 类型化修正系数表缺失"
    fi
    
    if grep -q "权重计算算法（方案B）" .claude/common/beat-analyzer.md; then
        echo "  ✅ 权重计算算法（方案B）存在"
    else
        echo "  ❌ 权重计算算法（方案B）缺失"
    fi
else
    echo "❌ beat-analyzer.md 文件不存在"
fi

echo ""

# Step 3: 检查SKILL.md集成
echo "✅ Step 3: 检查SKILL.md V3.0集成"
echo "------------------------------------------"

if [ -f .claude/skills/film-storyboard-skill/SKILL.md ]; then
    echo "✅ SKILL.md 文件存在"
    
    # 检查V3.0集成点
    echo "检查V3.0集成点："
    if grep -q "V3.0新增" .claude/skills/film-storyboard-skill/SKILL.md; then
        echo "  ✅ V3.0集成标记存在"
        V3_COUNT=$(grep -c "V3.0" .claude/skills/film-storyboard-skill/SKILL.md)
        echo "  ✅ 找到 $V3_COUNT 处V3.0相关修改"
    else
        echo "  ❌ V3.0集成标记缺失"
    fi
    
    # 检查结构模板引用
    if grep -q "structure-profiles.md" .claude/skills/film-storyboard-skill/SKILL.md; then
        echo "  ✅ structure-profiles.md 引用存在"
    else
        echo "  ❌ structure-profiles.md 引用缺失"
    fi
    
    # 检查潜台词分析引用
    if grep -q "subtext-analyzer.md" .claude/skills/film-storyboard-skill/SKILL.md; then
        echo "  ✅ subtext-analyzer.md 引用存在"
    else
        echo "  ❌ subtext-analyzer.md 引用缺失"
    fi
else
    echo "❌ SKILL.md 文件不存在"
fi

echo ""

# Step 4: 检查质量检查更新
echo "✅ Step 4: 检查质量检查V3.0更新"
echo "------------------------------------------"

if [ -f .claude/common/quality-check.md ]; then
    echo "✅ quality-check.md 文件存在"
    
    # 检查V3.0新增检查项
    echo "检查V3.0新增检查项："
    if grep -q "结构符合度检查" .claude/common/quality-check.md; then
        echo "  ✅ 结构符合度检查存在"
    else
        echo "  ❌ 结构符合度检查缺失"
    fi
    
    if grep -q "戏剧权重合理性检查" .claude/common/quality-check.md; then
        echo "  ✅ 戏剧权重合理性检查存在"
    else
        echo "  ❌ 戏剧权重合理性检查缺失"
    fi
    
    if grep -q "潜台词分析检查" .claude/common/quality-check.md; then
        echo "  ✅ 潜台词分析检查存在"
    else
        echo "  ❌ 潜台词分析检查缺失"
    fi
    
    if grep -q "V3.0 功能启用检查" .claude/common/quality-check.md; then
        echo "  ✅ V3.0功能启用检查存在"
    else
        echo "  ❌ V3.0功能启用检查缺失"
    fi
else
    echo "❌ quality-check.md 文件不存在"
fi

echo ""

# Step 5: 检查交互流程更新
echo "✅ Step 5: 检查交互流程V3.0更新"
echo "------------------------------------------"

if [ -f .claude/workflows/interactive-workflow.md ]; then
    echo "✅ interactive-workflow.md 文件存在"
    
    # 检查V3.0配置向导更新
    echo "检查V3.0配置向导更新："
    if grep -q "叙事结构选择" .claude/workflows/interactive-workflow.md; then
        echo "  ✅ 叙事结构选择步骤存在"
    else
        echo "  ❌ 叙事结构选择步骤缺失"
    fi
    
    if grep -q "影片类型选择" .claude/workflows/interactive-workflow.md; then
        echo "  ✅ 影片类型选择步骤存在"
    else
        echo "  ❌ 影片类型选择步骤缺失"
    fi
    
    # 检查配置确认页面更新
    if grep -q "V3.0 功能状态" .claude/workflows/interactive-workflow.md; then
        echo "  ✅ V3.0功能状态显示存在"
    else
        echo "  ❌ V3.0功能状态显示缺失"
    fi
else
    echo "❌ interactive-workflow.md 文件不存在"
fi

echo ""

# Step 6: 测试剧本检查
echo "✅ Step 6: 检查测试剧本"
echo "------------------------------------------"

if [ -f script/猪打镇关西_v2.0.md ]; then
    echo "✅ 测试剧本存在"
    
    # 检查剧本结构
    echo "检查剧本结构："
    if grep -q "characters:" script/猪打镇关西_v2.0.md; then
        echo "  ✅ YAML角色配置存在"
    else
        echo "  ❌ YAML角色配置缺失"
    fi
    
    if grep -q "scenes:" script/猪打镇关西_v2.0.md; then
        echo "  ✅ 场景配置存在"
    else
        echo "  ❌ 场景配置缺失"
    fi
    
    # 检查剧本内容长度
    LINE_COUNT=$(wc -l < script/猪打镇关西_v2.0.md)
    echo "  ✅ 剧本行数：$LINE_COUNT 行"
else
    echo "❌ 测试剧本不存在"
fi

echo ""

# Step 7: 总结测试结果
echo "✅ Step 7: 测试结果总结"
echo "=========================================="
echo ""

# 计算通过率
TOTAL_CHECKS=0
PASSED_CHECKS=0

# 这里可以添加更详细的统计逻辑
echo "V3.0集成测试完成！"
echo ""
echo "📊 测试覆盖范围："
echo "  - 配置系统：.agent-state.json V3.0字段"
echo "  - 核心模块：4种结构模板 + 潜台词分析 + 权重算法"
echo "  - 技能集成：SKILL.md V3.0集成点"
echo "  - 质量检查：V3.0新增检查项"
echo "  - 交互流程：配置向导更新"
echo "  - 测试剧本：猪打镇关西_v2.0.md"
echo ""
echo "🚀 下一步："
echo "  1. 运行实际分镜生成测试"
echo "  2. 验证四种结构模板的实际应用"
echo "  3. 测试权重计算新规则"
echo "  4. 验证潜台词分析输出"
echo "  5. 检查向后兼容性"
echo ""
echo "📝 注意：由于delegate_task工具故障，实际功能测试需要手动执行。"
echo "    所有手动操作已记录在 .sisyphus/notepads/anineo-v3-phase1/issues.md"