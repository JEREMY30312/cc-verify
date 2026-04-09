#!/bin/bash
# ANINEO 智能文件自动整理器 - 快速启动脚本

# 检查 Python 环境
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 Python3"
    exit 1
fi

# 检查参数
MODE=$1
shift 2>/dev/null

case "$MODE" in
    --dry-run)
        echo "启动试运行模式（不实际移动文件）..."
        python3 smart_file_organizer.py --dry-run --once
        ;;
    --once)
        echo "启动单次扫描模式..."
        python3 smart_file_organizer.py --once
        ;;
    --help|-h)
        echo "用法: $0 [选项]"
        echo ""
        echo "选项:"
        echo "  无参数      实时监控模式（需要 watchdog）"
        echo "  --once      单次扫描模式（扫描一次后退出）"
        echo "  --dry-run   试运行模式（仅显示将要执行的操作）"
        echo "  --help      显示此帮助信息"
        echo ""
        echo "示例:"
        echo "  $0              # 启动实时监控"
        echo "  $0 --once       # 执行一次扫描"
        echo "  $0 --dry-run    # 试运行，查看将要执行的操作"
        ;;
    "")
        echo "启动实时监控模式..."
        echo "提示: 按 Ctrl+C 停止监控"
        echo ""

        # 安装依赖（如果需要）
        if ! python3 -c "import watchdog" 2>/dev/null; then
            echo "正在安装 watchdog 库..."
            pip3 install watchdog
        fi

        python3 smart_file_organizer.py
        ;;
    *)
        echo "未知选项: $MODE"
        echo "使用 $0 --help 查看帮助"
        exit 1
        ;;
esac
