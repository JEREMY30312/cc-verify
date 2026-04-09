#!/bin/bash
# ANINEO Phase C Verification Script

echo "🔍 Phase C Verification Started"
echo "================================"

# Check P2 keywords
echo "1. Checking P2 keywords..."
p2_section_lines=$(grep -A 20 "#### P2元素" .claude/common/prompt-simplifier.md | grep -c "^\s*- ")
echo "   P2 keyword lines: $p2_section_lines"

# Check scene types
echo "2. Checking scene type categories..."
scene_categories=0
for category in "动作场景" "情感场景" "建立场景" "悬疑场景" "对话场景"; do
    if grep -q "$category" .claude/common/prompt-simplifier.md; then
        echo "   ✅ Found: $category"
        scene_categories=$((scene_categories+1))
    else
        echo "   ❌ Missing: $category"
    fi
done

echo "   Total scene categories: $scene_categories/5"

# Check SKILL integration
echo "3. Checking SKILL.md integration..."
if grep -q "阶段C新增" .claude/skills/film-storyboard-skill/SKILL.md; then
    integration_count=$(grep -c "阶段C新增" .claude/skills/film-storyboard-skill/SKILL.md)
    echo "   ✅ Phase C integration points: $integration_count"
else
    echo "   ❌ No Phase C integration found"
fi

# Summary
echo ""
echo "📊 Verification Summary:"
echo "========================"
echo "P2 Keywords: $p2_section_lines lines"
echo "Scene Categories: $scene_categories/5"
echo "SKILL Integration: $(if [ $integration_count -gt 0 ]; then echo "✅ Present"; else echo "❌ Missing"; fi)"

if [ $scene_categories -eq 5 ] && [ $integration_count -gt 0 ]; then
    echo ""
    echo "🎉 Phase C deployment verified successfully!"
    exit 0
else
    echo ""
    echo "⚠️  Verification issues found. Please check the deployment."
    exit 1
fi
