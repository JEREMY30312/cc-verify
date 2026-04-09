#!/bin/bash
# ANINEO 项目根目录检查脚本
# 功能：检测根目录中可能违规的文件

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "         ANINEO 根目录检查"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 检查违规文件类型
echo "【检查根目录违规文件】"
echo ""

# 定义允许的文件
ALLOWED_FILES=("AGENTS.md" ".agent-state.json" ".agent-state-template.json" "check_root.sh")

# 检查Python脚本
python_files=$(find . -maxdepth 1 -type f -name "*.py" | sed 's|^\./||')
python_count=$(echo "$python_files" | grep -v "^\.$" | wc -l | tr -d ' ')
if [ "$python_count" -gt 0 ]; then
    echo "⚠️  发现 $python_count 个 Python 脚本文件："
    echo "$python_files" | sed 's/^/  /'
    echo "   建议: 移动到 版本汇总/临时池/暂存脚本/ 或创建新插件目录"
    echo ""
fi

# 检查Shell脚本
sh_files=$(find . -maxdepth 1 -type f -name "*.sh" | sed 's|^\./||' | grep -v "check_root.sh")
sh_count=$(echo "$sh_files" | grep -v "^\.$" | wc -l | tr -d ' ')
if [ "$sh_count" -gt 0 ]; then
    echo "⚠️  发现 $sh_count 个 Shell 脚本文件："
    echo "$sh_files" | sed 's/^/  /'
    echo "   建议: 移动到 版本汇总/临时池/暂存脚本/ 或创建新插件目录"
    echo ""
fi

# 检查JavaScript文件
js_files=$(find . -maxdepth 1 -type f -name "*.js" | sed 's|^\./||')
js_count=$(echo "$js_files" | grep -v "^\.$" | wc -l | tr -d ' ')
if [ "$js_count" -gt 0 ]; then
    echo "⚠️  发现 $js_count 个 JavaScript 脚本文件："
    echo "$js_files" | sed 's/^/  /'
    echo "   建议: 移动到 版本汇总/临时池/暂存脚本/ 或创建新插件目录"
    echo ""
fi

# 检查Markdown文档（除了AGENTS.md）
md_files=$(find . -maxdepth 1 -type f -name "*.md" | sed 's|^\./||' | grep -v "AGENTS.md")
md_count=$(echo "$md_files" | grep -v "^\.$" | wc -l | tr -d ' ')
if [ "$md_count" -gt 0 ]; then
    echo "⚠️  发现 $md_count 个 Markdown 文档文件："
    echo "$md_files" | sed 's/^/  /'
    echo "   建议: 移动到 版本汇总/临时池/暂存文档/ 或 版本汇总/05-临时文件归档/"
    echo ""
fi

# 检查JSON文件
json_files=$(find . -maxdepth 1 -type f -name "*.json" | sed 's|^\./||')
json_count=$(echo "$json_files" | grep -v "^\.$" | wc -l | tr -d ' ')
if [ "$json_count" -gt 0 ]; then
    echo "⚠️  发现 $json_count 个 JSON 配置/结果文件："
    echo "$json_files" | sed 's/^/  /'
    echo "   建议: 移动到 版本汇总/临时池/暂存数据/ 或对应插件的配置/结果目录"
    echo ""
fi

# 检查日志文件
log_files=$(find . -maxdepth 1 -type f -name "*.log" | sed 's|^\./||')
log_count=$(echo "$log_files" | grep -v "^\.$" | wc -l | tr -d ' ')
if [ "$log_count" -gt 0 ]; then
    echo "⚠️  发现 $log_count 个 日志文件："
    echo "$log_files" | sed 's/^/  /'
    echo "   建议: 移动到 版本汇总/临时池/暂存文档/ 或直接删除"
    echo ""
fi

# 统计根目录所有非隐藏文件
total_files=$(find . -maxdepth 1 -type f ! -name ".*" | wc -l | tr -d ' ')
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "【根目录统计】"
echo "  非隐藏文件总数: ${total_files} 个"

# 检查临时池
temp_files=$(find "版本汇总/临时池" -type f 2>/dev/null | wc -l | tr -d ' ')
echo "  临时池文件数: ${temp_files} 个"
if [ "$temp_files" -gt 10 ]; then
    echo "  💡 临时池文件较多，建议定期整理"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 最终判断
if [ "$python_count" -eq 0 ] && [ "$sh_count" -eq 0 ] && [ "$js_count" -eq 0 ] && [ "$md_count" -eq 0 ]; then
    echo "✅ 根目录文件状态良好！"
else
    echo "⚠️  发现了一些问题，请根据建议处理"
fi
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
