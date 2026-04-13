#!/bin/bash
# 项目地图生成器 - 一键安装脚本
# 用法: curl -fsSL https://raw.githubusercontent.com/JEREMY30312/cc-verify/main/portable/install.sh | bash

set -e

echo "🗺️  项目地图生成器 V2.3 - 安装中..."
echo ""

# 1. 下载主程序
echo "📥 下载主程序..."
curl -fsSL -o generate_map.py https://raw.githubusercontent.com/JEREMY30312/cc-verify/main/portable/standalone.py
echo "   ✅ 已下载 generate_map.py"

# 2. 创建默认配置
echo "⚙️  创建默认配置..."
cat > .project-map-config.json << 'EOF'
{
  "time_range_hours": 168,
  "max_description_length": 20,
  "max_tree_depth": 3,
  "shallow_folders": [
    "backups",
    "版本汇总",
    "logs",
    "tests",
    "dist",
    "__pycache__",
    "临时池",
    "暂存数据",
    "playwright-report",
    "coverage",
    ".nyc_output"
  ],
  "ignore_list": [
    ".git",
    "node_modules",
    "__pycache__",
    ".DS_Store",
    "dist",
    "build",
    ".idea",
    ".vscode",
    ".sisyphus",
    ".opencode",
    ".backup",
    ".backups"
  ],
  "collapse_folders": ["backups", ".strategic-snapshots", "版本汇总", ".backup"],
  "hooks": {
    "post_commit_update": true,
    "post_merge_update": true,
    "post_checkout_update": true,
    "auto_add_to_git": true
  },
  "output": {
    "map_file": "PROJECT_MAP.md",
    "fingerprint_file": "PROJECT_FINGERPRINT.json"
  },
  "description": {
    "mode": "llm",
    "max_length": 20,
    "cache_file": ".file-descriptions.json",
    "tasks_file": ".llm-tasks.json",
    "timeout_seconds": 60
  }
}
EOF
echo "   ✅ 已创建 .project-map-config.json"

# 3. 首次运行
echo "🚀 首次运行..."
python3 generate_map.py
echo ""

# 4. 询问是否安装钩子
if [ -d ".git" ]; then
    read -p "🔧 是否安装 Git 钩子？(y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        python3 generate_map.py --install-hooks
    fi
fi

echo ""
echo "✅ 安装完成！"
echo "   使用: python3 generate_map.py"
echo "   安装钩子: python3 generate_map.py --install-hooks"
echo "   静默模式: python3 generate_map.py --silent"
echo ""
echo "📖 文档: https://github.com/JEREMY30312/cc-verify"
echo ""
echo "💡 提示: LLM模式需要AI平台支持，首次运行会生成任务清单"
