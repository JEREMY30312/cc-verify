#!/usr/bin/env python3
"""
ANINEO 智能文件自动整理器 (V1.0)

功能：
1. 实时监控根目录新文件
2. 智能分析文件类型和用途
3. 自动移动到合适位置
4. 遵循三原则法

特性：
- 实时监控，无需手动操作
- 智能分类，基于文件类型和内容
- 轻量级，一键启动
- 可配置规则，支持自定义

作者: ANINEO System
版本: V1.0
日期: 2026-01-31
"""

import os
import sys
import time
import json
import shutil
from pathlib import Path
from datetime import datetime

# 检查是否为 --once 或 --dry-run 模式（不需要 watchdog）
ONCE_MODE = "--once" in sys.argv or "--dry-run" in sys.argv

if not ONCE_MODE:
    try:
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler, FileCreatedEvent
    except ImportError:
        print("警告: watchdog 库未安装")
        print("请运行: pip install watchdog")
        print("或者使用 --once 模式（不需要 watchdog）")
        sys.exit(1)
else:
    # --once 模式，创建虚拟类用于类型检查
    class FileSystemEventHandler:
        pass

    class FileCreatedEvent:
        def __init__(self, src_path):
            self.src_path = src_path
            self.is_directory = False

# ==================== 配置区域 ====================

# 项目根目录（自动获取）
ROOT_DIR = Path(__file__).parent.absolute()

# 目标目录配置
TEMP_POOL_DIR = ROOT_DIR / "版本汇总" / "临时池"
VERSION_HISTORY_DIR = ROOT_DIR / "版本汇总" / "01-版本历史"
TEST_DIR = ROOT_DIR / "版本汇总" / "02-测试验证"
MONITORING_PLUGIN_DIR = ROOT_DIR / "版本汇总" / "03-监控系统插件"
KNOWLEDGE_PLUGIN_DIR = ROOT_DIR / "版本汇总" / "04-知识库优化插件"
ARCHIVE_DIR = ROOT_DIR / "版本汇总" / "05-临时文件归档"
AUX_TOOLS_DIR = ROOT_DIR / "版本汇总" / "06-辅助工具"

# 允许保留在根目录的文件（核心系统文件）
ALLOWED_ROOT_FILES = {
    "agents.md",
    ".agent-state.json",
    ".agent-state-template.json",
    "check_root.sh",
    "smart_file_organizer.py",
    "start_organizer.sh",
    "project_map.md",
    "project_fingerprint.json",
    "generate_map.py",
    ".project-map-config.json",
    ".project-map-config.example.json",
    ".ds_store",
}

# 隐藏目录（不监控）
IGNORE_DIRS = {
    ".git",
    ".claude",
    ".opencode",
    ".backup",
    ".backups",
    ".sisyphus",
    ".strategic-snapshots",
    ".templates",
    ".ruff_cache",
    "node_modules",
    "__pycache__",
}

# ==================== 智能分类规则 ====================


class FileClassifier:
    """文件智能分类器"""

    @staticmethod
    def classify(filepath: Path) -> dict:
        """
        智能分类文件，返回目标目录和原因

        Returns:
            {
                "target_dir": Path,  # 目标目录
                "reason": str,       # 分类原因
                "subdir": str        # 子目录（可选）
            }
        """
        filename = filepath.name.lower()
        ext = filepath.suffix.lower()
        stem = filepath.stem.lower()

        # 1. 核心系统文件 - 保留在根目录
        if filename in ALLOWED_ROOT_FILES:
            return {
                "target_dir": None,
                "reason": "核心系统文件，保留在根目录",
            }  # 不移动

        # 2. Phase C 相关文件 - 创建专用插件
        if FileClassifier._is_phase_c_related(filename):
            return {
                "target_dir": ROOT_DIR / "版本汇总" / "07-PhaseC部署插件",
                "reason": "Phase C 部署相关文件",
                "subdir": FileClassifier._get_phase_c_subdir(filepath),
            }

        # 3. 部署相关文件 - 归档
        if "deploy" in stem or "deployment" in stem:
            return {
                "target_dir": ARCHIVE_DIR,
                "reason": "部署相关文件",
                "subdir": "部署记录",
            }

        # 4. 分析/报告类 - 版本历史
        if "report" in stem or "analysis" in stem or "summary" in stem:
            return {
                "target_dir": VERSION_HISTORY_DIR,
                "reason": "分析报告",
                "subdir": "项目报告",
            }

        # 5. 测试文件 - 测试验证
        if "test" in stem or "verify" in stem or "validation" in stem:
            return {
                "target_dir": TEST_DIR,
                "reason": "测试验证文件",
                "subdir": FileClassifier._get_test_subdir(ext),
            }

        # 6. 备份相关 - 临时文件归档
        if "backup" in stem or "rollback" in stem:
            return {
                "target_dir": ARCHIVE_DIR,
                "reason": "备份/回滚文件",
                "subdir": "备份文件",
            }

        # 7. Python 脚本 - 暂存脚本
        if ext == ".py":
            return {
                "target_dir": TEMP_POOL_DIR / "暂存脚本",
                "reason": "Python脚本文件",
            }

        # 8. Shell 脚本 - 暂存脚本
        if ext == ".sh":
            return {"target_dir": TEMP_POOL_DIR / "暂存脚本", "reason": "Shell脚本文件"}

        # 9. JavaScript 文件 - 暂存脚本
        if ext == ".js":
            return {
                "target_dir": TEMP_POOL_DIR / "暂存脚本",
                "reason": "JavaScript文件",
            }

        # 10. Markdown 文档 - 暂存文档
        if ext == ".md":
            return {"target_dir": TEMP_POOL_DIR / "暂存文档", "reason": "Markdown文档"}

        # 11. JSON 数据 - 暂存数据
        if ext == ".json":
            return {"target_dir": TEMP_POOL_DIR / "暂存数据", "reason": "JSON数据文件"}

        # 12. 日志文件 - 暂存文档（或直接删除）
        if ext == ".log":
            return {"target_dir": TEMP_POOL_DIR / "暂存文档", "reason": "日志文件"}

        # 13. 其他未知文件 - 不确定文件
        return {"target_dir": TEMP_POOL_DIR / "不确定文件", "reason": "未知文件类型"}

    @staticmethod
    def _is_phase_c_related(filename: str) -> bool:
        """判断是否为 Phase C 相关文件"""
        phase_c_keywords = [
            "phase_c",
            "phasec",
            "phase-c",
            "deploy_phase_c",
            "phase_c_processor",
            "phase_c_batch",
            "phase_c_30p",
            "phase_c_60p",
            "phase_c_100p",
            "phase-c-deployment",
        ]
        return any(keyword in filename for keyword in phase_c_keywords)

    @staticmethod
    def _get_phase_c_subdir(filepath: Path) -> str:
        """获取 Phase C 文件的子目录"""
        ext = filepath.suffix.lower()

        if ext == ".py":
            return "核心功能"
        elif ext == ".sh":
            return "脚本工具"
        elif ext == ".md":
            return "文档"
        elif ext == ".json":
            return "配置文件"
        else:
            return "其他"

    @staticmethod
    def _get_test_subdir(ext: str) -> str:
        """获取测试文件的子目录"""
        if ext == ".py":
            return "测试脚本"
        elif ext == ".json":
            return "测试数据"
        else:
            return "测试结果"


# ==================== 文件事件处理器 ====================


class SmartFileHandler(FileSystemEventHandler):
    """智能文件事件处理器"""

    def __init__(self, dry_run=False):
        self.dry_run = dry_run
        self.moved_count = 0
        self.ignored_count = 0
        self.last_log_time = time.time()

    def on_created(self, event):
        """文件创建事件"""
        if event.is_directory:
            return

        filepath = Path(event.src_path)

        # 等待文件写入完成（避免移动未完成的文件）
        self._wait_for_file_ready(filepath)

        # 检查是否在根目录
        if filepath.parent != ROOT_DIR:
            return

        # 检查是否为隐藏文件
        if filepath.name.startswith("."):
            return

        # 智能分类
        result = FileClassifier.classify(filepath)

        if result.get("target_dir") is None:
            # 允许保留在根目录
            self.ignored_count += 1
            return

        # 移动文件
        self._move_file(filepath, result)

    def _wait_for_file_ready(self, filepath: Path, max_wait=2.0):
        """等待文件写入完成"""
        for _ in range(int(max_wait * 10)):
            try:
                # 尝试打开文件，如果失败则等待
                with open(filepath, "rb") as f:
                    pass
                break
            except (IOError, PermissionError):
                time.sleep(0.1)

    def _move_file(self, filepath: Path, result: dict):
        """移动文件到目标目录"""
        target_dir = result.get("target_dir")
        if target_dir is None:
            return  # 不移动

        reason = result["reason"]
        subdir = result.get("subdir", "")

        # 创建目标目录
        if subdir:
            full_target_dir = target_dir / subdir
        else:
            full_target_dir = target_dir

        full_target_dir.mkdir(parents=True, exist_ok=True)

        # 目标文件路径
        target_path = full_target_dir / filepath.name

        # 处理文件名冲突
        if target_path.exists():
            base = filepath.stem
            ext = filepath.suffix
            counter = 1
            while target_path.exists():
                new_name = f"{base}_{counter}{ext}"
                target_path = full_target_dir / new_name
                counter += 1

        # 移动文件
        if self.dry_run:
            print(f"[DRY RUN] {filepath.name} -> {target_path.relative_to(ROOT_DIR)}")
            print(f"         原因: {reason}")
        else:
            try:
                shutil.move(str(filepath), str(target_path))
                self.moved_count += 1

                # 输出日志（节流，避免刷屏）
                if time.time() - self.last_log_time > 1.0 or self.moved_count <= 5:
                    print(f"✓ {filepath.name} -> {target_path.relative_to(ROOT_DIR)}")
                    print(f"  原因: {reason}")
                    self.last_log_time = time.time()

            except Exception as e:
                print(f"✗ 移动失败 {filepath.name}: {e}")


# ==================== 主程序 ====================


def create_directories():
    """创建必要的目录结构"""
    dirs = [
        TEMP_POOL_DIR,
        TEMP_POOL_DIR / "暂存脚本",
        TEMP_POOL_DIR / "暂存文档",
        TEMP_POOL_DIR / "暂存数据",
        TEMP_POOL_DIR / "不确定文件",
        VERSION_HISTORY_DIR,
        TEST_DIR,
        ARCHIVE_DIR,
        ROOT_DIR / "版本汇总" / "07-PhaseC部署插件",
    ]

    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)

    print("✓ 目录结构已创建")


def print_banner():
    """打印启动横幅"""
    print("=" * 60)
    print("     ANINEO 智能文件自动整理器 V1.0")
    print("=" * 60)
    print("监控目录:", ROOT_DIR)
    print("模式: 实时监控 + 自动整理")
    print("原则: 三原则法（根目录仅保留核心文件）")
    print("=" * 60)
    print()


def main():
    import argparse

    parser = argparse.ArgumentParser(description="ANINEO 智能文件自动整理器")
    parser.add_argument(
        "--dry-run", action="store_true", help="试运行模式（不实际移动文件）"
    )
    parser.add_argument(
        "--once", action="store_true", help="运行一次后退出（不持续监控）"
    )
    args = parser.parse_args()

    # 创建必要的目录
    create_directories()

    # 打印启动横幅
    print_banner()

    if args.once:
        # 运行一次模式
        print("模式: 单次扫描（不持续监控）")
        print()

        handler = SmartFileHandler(dry_run=args.dry_run)

        # 扫描当前根目录的所有文件
        print("扫描根目录...")
        for item in ROOT_DIR.iterdir():
            if item.is_file():
                if item.name.startswith("."):
                    continue

                # 模拟文件创建事件
                event = FileCreatedEvent(str(item))
                handler.on_created(event)

        # 打印统计
        print()
        print("=" * 60)
        print("扫描完成")
        print(f"已移动: {handler.moved_count} 个文件")
        print(f"已忽略: {handler.ignored_count} 个文件")
        print("=" * 60)

        if not args.dry_run:
            print()
            print("提示: 运行 './check_root.sh' 检查当前根目录状态")

    else:
        # 持续监控模式
        print("模式: 持续监控（Ctrl+C 退出）")
        print()
        print("监控中... (新创建的文件会自动整理)")
        print()

        handler = SmartFileHandler(dry_run=args.dry_run)
        observer = Observer()
        observer.schedule(handler, str(ROOT_DIR), recursive=False)
        observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print()
            print()
            print("=" * 60)
            print("监控已停止")
            print(f"共移动: {handler.moved_count} 个文件")
            print(f"共忽略: {handler.ignored_count} 个文件")
            print("=" * 60)
            observer.stop()

        observer.join()


if __name__ == "__main__":
    main()
