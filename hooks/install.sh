#!/bin/bash
# 钩子安装脚本 - 一键安装所有钩子到Git仓库
# 使用方法: cd hooks && bash install.sh

set -e

HOOKS_DIR=".git/hooks"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=========================================="
echo "🗺️  项目地图生成器 - 钩子安装器"
echo "=========================================="
echo ""

# 检查是否为Git仓库
if [ ! -d ".git" ]; then
    echo -e "${RED}❌ 错误: 当前目录不是Git仓库${NC}"
    echo "   请在Git仓库根目录运行此脚本"
    exit 1
fi

# 检查钩子目录是否存在
if [ ! -d "$HOOKS_DIR" ]; then
    echo -e "${YELLOW}⚠️  创建钩子目录...${NC}"
    mkdir -p "$HOOKS_DIR"
fi

# 安装钩子
echo "开始安装钩子..."
echo ""

INSTALLED=0
FAILED=0

for hook in post-commit post-merge post-checkout; do
    if [ -f "$SCRIPT_DIR/$hook" ]; then
        # 备份现有钩子（如果存在）
        if [ -f "$HOOKS_DIR/$hook" ]; then
            echo -e "${YELLOW}⚠️  备份现有 $hook 钩子...${NC}"
            cp "$HOOKS_DIR/$hook" "$HOOKS_DIR/${hook}.backup.$(date +%Y%m%d%H%M%S)"
        fi
        
        # 复制新钩子
        cp "$SCRIPT_DIR/$hook" "$HOOKS_DIR/$hook"
        chmod +x "$HOOKS_DIR/$hook"
        
        echo -e "${GREEN}✅ 安装 $hook 钩子成功${NC}"
        INSTALLED=$((INSTALLED + 1))
    else
        echo -e "${RED}❌ 未找到 $hook 钩子文件${NC}"
        FAILED=$((FAILED + 1))
    fi
done

echo ""
echo "=========================================="
echo "安装完成！"
echo "=========================================="
echo -e "成功: ${GREEN}$INSTALLED${NC} 个钩子"
if [ $FAILED -gt 0 ]; then
    echo -e "失败: ${RED}$FAILED${NC} 个钩子"
fi
echo ""

if [ $INSTALLED -gt 0 ]; then
    echo "🎉 钩子已安装！现在每次 Git 操作后会自动更新项目地图。"
    echo ""
    echo "钩子功能："
    echo "  • post-commit:   提交后自动更新地图"
    echo "  • post-merge:    合并后自动更新地图"
    echo "  • post-checkout: 切换分支后自动更新地图"
    echo ""
    echo "配置文件: .project-map-config.json"
    echo "可通过修改配置文件启用/禁用钩子功能。"
fi
