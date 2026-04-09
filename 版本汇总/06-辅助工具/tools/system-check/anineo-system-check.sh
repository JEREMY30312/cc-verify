#!/bin/bash

#===============================================================================
# ANINEO 系统健康检查脚本 v3.2 (修复版)
#===============================================================================

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m'
BOLD='\033[1m'

# 获取项目根目录（脚本在 tools/system-check/，需要向上两级）
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO_ROOT"

# ===== 报告路径配置 =====
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
TIMESTAMP_FILE=$(date '+%Y-%m-%d-%H%M%S')  # 文件名用格式

# 创建报告文件夹（按年/月组织）
REPORT_DIR="$REPO_ROOT/reports/system-check/$(date '+%Y/%m')"
mkdir -p "$REPORT_DIR"

# 设置报告文件路径
REPORT_FILE="$REPORT_DIR/system-check-$TIMESTAMP_FILE.md"

# 创建 latest 软链接
ln -sf "$REPORT_FILE" "$REPO_ROOT/reports/system-check/current/latest.md"
ln -sf "$REPORT_FILE" "$REPO_ROOT/reports/system-check/latest.md"

CHECK_MODE="${1:-full}"

ERRORS=0
WARNINGS=0
PASSED=0
TOTAL=0

print_header() {
    echo ""
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}  $1${NC}"
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
    echo ""
}

section() {
    echo ""
    echo -e "${BLUE}━━━ $1 ━━━${NC}"
    echo ""
}

check() {
    TOTAL=$((TOTAL + 1))
    echo -e "  ${WHITE}▸ $1${NC}"
}

pass() {
    PASSED=$((PASSED + 1))
    echo -e "     ${GREEN}✅ $1${NC}"
}

fail() {
    ERRORS=$((ERRORS + 1))
    echo -e "     ${RED}❌ $1${NC}"
}

warn() {
    WARNINGS=$((WARNINGS + 1))
    echo -e "     ${YELLOW}⚠️  $1${NC}"
}

info() {
    echo -e "     ${BLUE}ℹ️  $1${NC}"
}

report_section() {
    echo "" >> "$REPORT_FILE"
    echo "## $1" >> "$REPORT_FILE"
}

report_item() {
    local status="$1"
    local msg="$2"
    local detail="$3"
    
    case $status in
        pass)  emoji="✅" ;;
        fail)  emoji="❌" ;;
        warn)  emoji="⚠️" ;;
        info)  emoji="ℹ️" ;;
    esac
    
    echo "- $emoji $msg" >> "$REPORT_FILE"
    [ -n "$detail" ] && echo "  - $detail" >> "$REPORT_FILE"
}

init_report() {
    cat > "$REPORT_FILE" << EOF
# ANINEO 系统健康检查报告

**检查时间：** $TIMESTAMP  
**检查模式：** $CHECK_MODE  
**工作目录：** $REPO_ROOT  

---

## 执行摘要

| 指标 | 数值 |
|------|------|
| 总检查项 | $TOTAL |
| 通过 | $PASSED |
| 错误 | $ERRORS |
| 警告 | $WARNINGS |

EOF
}

check_template_paths() {
    section "1. 模板路径配置"
    report_section "1. 模板路径配置检查"
    
    check "扫描模板路径引用..."
    
    # 排除自身脚本和备份文件
    local errors=$(grep -r "'templates/beat\|'templates/board\|'templates/sequence" . 2>/dev/null | \
        grep -v "film-storyboard-skill/templates/" | \
        grep -v "anineo-system-check.sh" | \
        grep -v "check$" | \
        grep -v "checkf$" | \
        grep -v "checkfix$" | \
        grep -v ".backup" | \
        grep -v "node_modules" | \
        grep -v ".git" | \
        grep "\.md\|\.js" || true)
    
    if [ -n "$errors" ]; then
        fail "发现错误路径引用"
        echo "$errors" | while read -r line; do
            echo "  - $line" >> "$REPORT_FILE"
        done
    else
        pass "所有模板路径引用正确"
        report_item pass "所有模板路径引用正确"
    fi
    
    check "验证模板文件存在性..."
    
    local templates=(
        "film-storyboard-skill/templates/beat-breakdown-template.md"
        "film-storyboard-skill/templates/beat-board-template.md"
        "film-storyboard-skill/templates/sequence-board-template.md"
    )
    
    local missing=0
    for t in "${templates[@]}"; do
        if [ -f "$t" ]; then
            pass "$(basename $t)"
        else
            missing=$((missing + 1))
            fail "缺失: $(basename $t)"
        fi
    done
    
    [ $missing -eq 0 ] && report_item pass "所有模板文件存在" || report_item fail "发现 $missing 个模板文件缺失"
}

check_core_modules() {
    section "2. 核心模块文件"
    report_section "2. 核心模块文件检查"
    
    check "检查核心模块文件..."
    
    local modules=(
        "common/beat-analyzer.md:节拍分析器"
        "common/keyframe-selector.md:关键帧选择器"
        "common/layout-calculator.md:布局计算器"
        "common/coherence-checker.md:连贯性检查器"
        "common/quality-check.md:质量检查清单"
    )
    
    local missing=0
    for m in "${modules[@]}"; do
        local file=$(echo "$m" | cut -d: -f1)
        local name=$(echo "$m" | cut -d: -f2)
        
        if [ -f "$file" ]; then
            local lines=$(wc -l < "$file")
            pass "$name ($lines 行)"
        else
            missing=$((missing + 1))
            fail "缺失: $name"
        fi
    done
    
    [ $missing -eq 0 ] && report_item pass "所有核心模块存在" || report_item fail "发现 $missing 个模块缺失"
}

check_module_content() {
    section "3. 模块内容完整性"
    report_section "3. 模块内容完整性检查"
    
    check "检查 beat-analyzer.md 内容完整性..."
    
    local ba_file="common/beat-analyzer.md"
    
    if [ -f "$ba_file" ]; then
        local content=$(cat "$ba_file")
        local missing_content=0
        
        if echo "$content" | grep -q "三幕结构"; then
            info "三幕结构 ✓"
        else
            missing_content=$((missing_content + 1))
            fail "缺失: 三幕结构"
        fi
        
        if echo "$content" | grep -q "节拍类型"; then
            info "节拍类型权重 ✓"
        else
            missing_content=$((missing_content + 1))
            fail "缺失: 节拍类型权重"
        fi
        
        if echo "$content" | grep -q "叙事功能"; then
            info "叙事功能基重 ✓"
        else
            missing_content=$((missing_content + 1))
            fail "缺失: 叙事功能基重"
        fi
        
        if echo "$content" | grep -q "综合权重"; then
            info "综合权重公式 ✓"
        else
            missing_content=$((missing_content + 1))
            fail "缺失: 综合权重公式"
        fi
        
        if echo "$content" | grep -q "关键帧等级"; then
            info "关键帧等级定义 ✓"
        else
            missing_content=$((missing_content + 1))
            fail "缺失: 关键帧等级定义"
        fi
        
        if echo "$content" | grep -q "执行步骤"; then
            info "执行步骤 ✓"
        else
            missing_content=$((missing_content + 1))
            fail "缺失: 执行步骤"
        fi
        
        [ $missing_content -eq 0 ] && pass "beat-analyzer.md 内容完整" || fail "beat-analyzer.md 缺少 $missing_content 项内容"
    else
        fail "beat-analyzer.md 不存在"
    fi
    
    check "检查模块文件行数..."
    
    local ba_lines=$(wc -l < "common/beat-analyzer.md" 2>/dev/null || echo "0")
    local ks_lines=$(wc -l < "common/keyframe-selector.md" 2>/dev/null || echo "0")
    local lc_lines=$(wc -l < "common/layout-calculator.md" 2>/dev/null || echo "0")
    local cc_lines=$(wc -l < "common/coherence-checker.md" 2>/dev/null || echo "0")
    
    [ "$ba_lines" -gt 100 ] && pass "beat-analyzer.md: $ba_lines 行" || warn "beat-analyzer.md: $ba_lines 行 (建议 ≥ 100)"
    [ "$ks_lines" -gt 50 ] && pass "keyframe-selector.md: $ks_lines 行" || warn "keyframe-selector.md: $ks_lines 行 (建议 ≥ 50)"
    [ "$lc_lines" -gt 50 ] && pass "layout-calculator.md: $lc_lines 行" || warn "layout-calculator.md: $lc_lines 行 (建议 ≥ 50)"
    [ "$cc_lines" -gt 50 ] && pass "coherence-checker.md: $cc_lines 行" || warn "coherence-checker.md: $cc_lines 行 (建议 ≥ 50)"
}

check_router_config() {
    section "4. 路由配置"
    report_section "4. 路由配置检查"
    
    check "检查 router.js 模板路径..."
    
    local router="agents/router.js"
    
    if [ -f "$router" ]; then
        if grep -q "'templates/beat-breakdown-template.md'" "$router" 2>/dev/null || \
           grep -q "'templates/beat-board-template.md'" "$router" 2>/dev/null || \
           grep -q "'templates/sequence-board-template.md'" "$router" 2>/dev/null; then
            fail "router.js 包含错误路径"
            report_item fail "router.js 包含错误模板路径引用"
        else
            pass "router.js 路径配置正确"
            report_item pass "router.js 模板路径配置正确"
        fi
    else
        fail "router.js 不存在"
    fi
}

check_agent_configs() {
    section "5. Agent 配置"
    report_section "5. Agent 配置检查"
    
    check "检查 Agent 配置文件..."
    
    local agent_files=(
        "agents/storyboard-artist.md"
        "agents/animator.md"
    )
    
    local issues=0
    for a in "${agent_files[@]}"; do
        if [ -f "$a" ]; then
            if grep -q "'templates/beat\|'templates/board\|'templates/sequence" "$a" 2>/dev/null; then
                issues=$((issues + 1))
                fail "$(basename $a) 包含错误路径"
            else
                pass "$(basename $a)"
            fi
        else
            warn "$(basename $a) 不存在"
        fi
    done
    
    [ $issues -eq 0 ] && report_item pass "所有 Agent 配置正确" || report_item fail "发现 $issues 个 Agent 配置问题"
}

check_output_dirs() {
    section "6. 输出目录"
    report_section "6. 输出目录状态检查"
    
    check "检查 outputs 目录..."
    
    if [ -d "outputs" ]; then
        pass "outputs 目录存在"
        local files=$(find outputs -name "*.md" 2>/dev/null | wc -l)
        info "输出文件: $files 个"
        report_item pass "outputs 目录存在 ($files 个文件)"
    else
        warn "outputs 目录不存在"
        report_item warn "outputs 目录不存在"
    fi
    
    check "检查 snapshots 目录..."
    
    if [ -d ".strategic-snapshots" ]; then
        pass ".strategic-snapshots 目录存在"
        local snaps=$(find .strategic-snapshots -name "snapshot_*" -type d 2>/dev/null | wc -l)
        info "快照数量: $snaps 个"
        report_item pass ".strategic-snapshots 目录存在 ($snaps 个快照)"
    else
        warn ".strategic-snapshots 目录不存在"
        report_item warn ".strategic-snapshots 目录不存在"
    fi
}

check_agent_state() {
    section "7. 配置文件"
    report_section "7. 配置文件状态检查"
    
    check "检查 .agent-state.json..."
    
    local state=".agent-state.json"
    
    if [ -f "$state" ]; then
        if python3 -c "import json; json.load(open('$state'))" 2>/dev/null; then
            pass ".agent-state.json 格式正确"
            report_item pass ".agent-state.json JSON 格式正确"
            info "当前阶段状态:"
            python3 -c "import json; data=json.load(open('$state')); [print(f'{k}: {v.get(\"status\", \"?\")}') for k,v in data.get('phases',{}).items()]" 2>/dev/null || true
        else
            fail ".agent-state.json JSON 格式错误"
            report_item fail ".agent-state.json JSON 格式错误"
        fi
    else
        warn ".agent-state.json 不存在"
        report_item warn ".agent-state.json 不存在"
    fi
}

check_consistency() {
    section "8. 引用一致性"
    report_section "8. 依赖引用一致性检查"
    
    check "统计模块引用..."
    
    local refs=$(grep -r "beat-analyzer.md\|keyframe-selector.md\|coherence-checker.md" . 2>/dev/null | grep -v ".backup" | grep -v "node_modules" | grep -v ".git" | wc -l || echo "0")
    
    info "模块引用总次数: $refs"
    report_item info "模块引用总次数: $refs"
    
    check "验证引用路径一致性..."
    
    local inconsistent=$(grep -r "beat-analyzer.md" . 2>/dev/null | \
        grep -v "common/beat-analyzer.md" | \
        grep -v "anineo-system-check.sh" | \
        grep -v ".backup" | \
        grep -v "node_modules" | \
        grep -v ".git" || true)
    
    if [ -n "$inconsistent" ]; then
        warn "发现不一致的引用路径"
        report_item warn "发现不一致的模块引用路径"
    else
        pass "所有引用路径一致"
        report_item pass "所有模块引用路径格式一致"
    fi
}

summary() {
    section "检查汇总"
    
    local rate=0
    if [ $TOTAL -gt 0 ]; then
        rate=$(( PASSED * 100 / TOTAL ))
    fi
    
    echo -e "${BOLD}检查结果：${NC}"
    echo ""
    echo -e "  ${GREEN}通过：$PASSED${NC}"
    echo -e "  ${RED}错误：$ERRORS${NC}"
    echo -e "  ${YELLOW}警告：$WARNINGS${NC}"
    echo ""
    echo -e "  ${BOLD}通过率：$rate%${NC}"
    echo ""
    
    echo "" >> "$REPORT_FILE"
    echo "---" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
    echo "## 汇总" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
    echo "| 指标 | 数值 |" >> "$REPORT_FILE"
    echo "|:-----|:----:|" >> "$REPORT_FILE"
    echo "| 总检查 | $TOTAL |" >> "$REPORT_FILE"
    echo "| 通过 | $PASSED |" >> "$REPORT_FILE"
    echo "| 错误 | $ERRORS |" >> "$REPORT_FILE"
    echo "| 警告 | $WARNINGS |" >> "$REPORT_FILE"
    echo "| 通过率 | $rate% |" >> "$REPORT_FILE"
    
    if [ $ERRORS -eq 0 ]; then
        echo ""
        echo -e "${GREEN}🎉 所有检查通过！系统状态良好。${NC}"
        echo "" >> "$REPORT_FILE"
        echo "## 结论" >> "$REPORT_FILE"
        echo "" >> "$REPORT_FILE"
        echo "🎉 **所有检查通过！系统状态良好。**" >> "$REPORT_FILE"
        exit_code=0
    else
        echo ""
        echo -e "${RED}⚠️ 发现 $ERRORS 个错误需要修复。${NC}"
        echo "" >> "$REPORT_FILE"
        echo "## 结论" >> "$REPORT_FILE"
        echo "" >> "$REPORT_FILE"
        echo "⚠️ **发现 $ERRORS 个错误需要修复。**" >> "$REPORT_FILE"
        echo "" >> "$REPORT_FILE"
        echo "请查看详细报告: $REPORT_FILE" >> "$REPORT_FILE"
        exit_code=1
    fi
    
    echo ""
    echo -e "${BLUE}📄 详细报告：$REPORT_FILE${NC}"
    echo -e "${BLUE}🔗 最新报告：$REPO_ROOT/reports/system-check/latest.md${NC}"
    echo ""
    
    return $exit_code
}

main() {
    echo ""
    echo -e "${CYAN}╔═══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║                                                               ║${NC}"
    echo -e "${CYAN}║   ${WHITE}ANINEO 系统健康检查${NC}                                    ${CYAN}║${NC}"
    echo -e "${CYAN}║                                                               ║${NC}"
    echo -e "${CYAN}║   检查时间：$TIMESTAMP${NC}                           ${CYAN}║${NC}"
    echo -e "${CYAN}║   检查模式：$CHECK_MODE${NC}                                       ${CYAN}║${NC}"
    echo -e "${CYAN}║                                                               ║${NC}"
    echo -e "${CYAN}╚═══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    init_report
    
    case $CHECK_MODE in
        quick)
            check_template_paths
            ;;
        full|*)
            check_template_paths
            check_core_modules
            check_module_content
            check_router_config
            check_agent_configs
            check_output_dirs
            check_agent_state
            check_consistency
            ;;
    esac
    
    summary
}

main "$@"
