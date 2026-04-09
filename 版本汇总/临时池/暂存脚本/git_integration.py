"""
> **Description:** Git状态检测模块，为 generate_map.py 提供Git状态读取、变更分类和表格生成功能

Git状态检测模块
支持Git状态读取、变更分类、时间过滤和表格生成
"""

import os
import subprocess
import datetime
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from collections import defaultdict


# ================= 常量定义 =================

# 变更类型图标映射
CHANGE_ICONS = {
    "M": "🟢",  # Modified - 修改
    "A": "🔵",  # Added - 新增
    "D": "🔴",  # Deleted - 删除
    "R": "🟡",  # Renamed - 重命名
    "C": "🟣",  # Copied - 复制
    "U": "🟠",  # Updated but unmerged - 更新但未合并
    "??": "⚪",  # Untracked - 未跟踪
}

# 变更类型描述映射
CHANGE_DESCRIPTIONS = {
    "M": "修改",
    "A": "新增",
    "D": "删除",
    "R": "重命名",
    "C": "复制",
    "U": "冲突",
    "??": "未跟踪",
}

# 默认时间范围（7天 = 168小时）
DEFAULT_HOURS = 168


# ================= 数据类定义 =================


@dataclass
class GitChange:
    """Git变更记录"""

    status: str  # 变更状态码
    file_path: str  # 文件路径
    original_path: Optional[str] = None  # 原始路径（用于重命名）
    change_time: Optional[datetime.datetime] = None  # 变更时间
    description: str = ""  # 变更描述

    @property
    def directory(self) -> str:
        """获取文件所在目录"""
        return str(Path(self.file_path).parent)

    @property
    def file_name(self) -> str:
        """获取文件名"""
        return Path(self.file_path).name

    @property
    def icon(self) -> str:
        """获取变更图标"""
        return CHANGE_ICONS.get(self.status, "⚪")

    @property
    def status_desc(self) -> str:
        """获取变更状态描述"""
        return CHANGE_DESCRIPTIONS.get(self.status, "未知")


@dataclass
class DirectoryStats:
    """目录变更统计"""

    directory: str
    total_changes: int = 0
    change_types: Dict[str, int] = field(default_factory=dict)
    files: List[GitChange] = field(default_factory=list)

    @property
    def is_hotspot(self) -> bool:
        """判断是否为热点区域（变更数 > 3）"""
        return self.total_changes > 3


@dataclass
class GitStatus:
    """Git状态汇总"""

    is_git_repo: bool
    changes: List[GitChange]
    error_message: Optional[str] = None
    branch: Optional[str] = None
    commit_hash: Optional[str] = None


# ================= Git状态读取器 =================


def is_git_repository(path: str = ".") -> bool:
    """检查指定路径是否为Git仓库"""
    try:
        result = subprocess.run(
            ["git", "-C", path, "rev-parse", "--git-dir"],
            capture_output=True,
            text=True,
            check=False,
        )
        return result.returncode == 0
    except Exception:
        return False


def get_current_branch(path: str = ".") -> Optional[str]:
    """获取当前Git分支"""
    try:
        result = subprocess.run(
            ["git", "-C", path, "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except Exception:
        return None


def get_last_commit_hash(path: str = ".") -> Optional[str]:
    """获取最新提交哈希"""
    try:
        result = subprocess.run(
            ["git", "-C", path, "rev-parse", "--short", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except Exception:
        return None


def get_file_last_commit_time(
    file_path: str, repo_path: str = "."
) -> Optional[datetime.datetime]:
    """获取文件最后一次提交时间"""
    try:
        result = subprocess.run(
            ["git", "-C", repo_path, "log", "-1", "--format=%ct", "--", file_path],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0 and result.stdout.strip():
            timestamp = int(result.stdout.strip())
            return datetime.datetime.fromtimestamp(timestamp)
        return None
    except Exception:
        return None


def parse_porcelain_line(line: str) -> Optional[GitChange]:
    """解析 git status --porcelain 输出的一行"""
    if not line or len(line) < 3:
        return None

    # porcelain格式: XY filename 或 XY "filename" -> "original"
    # X = staged status, Y = unstaged status
    staged = line[0]
    unstaged = line[1]
    rest = line[3:]

    # 优先使用非空的状态
    status = unstaged if unstaged != " " and unstaged != "?" else staged

    # 处理重命名情况 (R)
    if status == "R" and " -> " in rest:
        parts = rest.split(" -> ")
        if len(parts) == 2:
            return GitChange(status=status, file_path=parts[1], original_path=parts[0])

    # 普通情况
    return GitChange(status=status, file_path=rest)


def get_git_status(repo_path: str = ".") -> GitStatus:
    """
    获取Git仓库状态

    返回结构化的Git状态数据，包含所有变更文件的信息。
    如果不在Git仓库中，返回 is_git_repo=False。

    Returns:
        GitStatus: Git状态汇总对象
    """
    # 检查是否为Git仓库
    if not is_git_repository(repo_path):
        return GitStatus(
            is_git_repo=False, changes=[], error_message="当前目录不是Git仓库"
        )

    try:
        # 获取分支和提交信息
        branch = get_current_branch(repo_path)
        commit_hash = get_last_commit_hash(repo_path)

        # 获取Git状态
        result = subprocess.run(
            ["git", "-C", repo_path, "status", "--porcelain"],
            capture_output=True,
            text=True,
            check=True,
        )

        changes = []
        for line in result.stdout.strip().split("\n"):
            if not line:
                continue

            change = parse_porcelain_line(line)
            if change:
                # 获取文件提交时间
                change.change_time = get_file_last_commit_time(
                    change.file_path, repo_path
                )
                # 如果Git时间获取失败，使用文件系统时间
                if change.change_time is None:
                    try:
                        full_path = os.path.join(repo_path, change.file_path)
                        if os.path.exists(full_path):
                            mtime = os.path.getmtime(full_path)
                            change.change_time = datetime.datetime.fromtimestamp(mtime)
                    except Exception:
                        pass

                changes.append(change)

        return GitStatus(
            is_git_repo=True, changes=changes, branch=branch, commit_hash=commit_hash
        )

    except subprocess.CalledProcessError as e:
        return GitStatus(
            is_git_repo=True, changes=[], error_message=f"Git命令执行失败: {e.stderr}"
        )
    except Exception as e:
        return GitStatus(
            is_git_repo=True, changes=[], error_message=f"获取Git状态失败: {str(e)}"
        )


# ================= 变更分类器 =================


def classify_changes(git_status: GitStatus) -> Dict[str, DirectoryStats]:
    """
    按目录对变更进行分类统计

    Args:
        git_status: Git状态对象

    Returns:
        Dict[str, DirectoryStats]: 目录 -> 统计信息的映射
    """
    dir_stats: Dict[str, DirectoryStats] = defaultdict(
        lambda: DirectoryStats(directory="")
    )

    for change in git_status.changes:
        directory = change.directory if change.directory != "." else "根目录"

        if dir_stats[directory].directory == "":
            dir_stats[directory].directory = directory

        dir_stats[directory].total_changes += 1
        dir_stats[directory].files.append(change)

        # 统计变更类型
        change_type = change.status_desc
        if change_type in dir_stats[directory].change_types:
            dir_stats[directory].change_types[change_type] += 1
        else:
            dir_stats[directory].change_types[change_type] = 1

    return dict(dir_stats)


def get_hotspot_directories(
    dir_stats: Dict[str, DirectoryStats], threshold: int = 3
) -> List[DirectoryStats]:
    """
    识别热点目录（变更数量超过阈值的目录）

    Args:
        dir_stats: 目录统计信息
        threshold: 热点阈值，默认3个变更

    Returns:
        List[DirectoryStats]: 热点目录列表，按变更数量降序排列
    """
    hotspots = [
        stats for stats in dir_stats.values() if stats.total_changes > threshold
    ]
    return sorted(hotspots, key=lambda x: x.total_changes, reverse=True)


# ================= 时间范围过滤器 =================


def filter_by_time(
    changes: List[GitChange],
    hours: int = DEFAULT_HOURS,
    reference_time: Optional[datetime.datetime] = None,
) -> List[GitChange]:
    """
    按时间范围过滤变更

    优先使用Git提交时间，如果不可用则使用文件系统修改时间。

    Args:
        changes: 变更列表
        hours: 时间范围（小时），默认168小时（7天）
        reference_time: 参考时间，默认为当前时间

    Returns:
        List[GitChange]: 过滤后的变更列表，按时间倒序排列
    """
    if reference_time is None:
        reference_time = datetime.datetime.now()

    cutoff_time = reference_time - datetime.timedelta(hours=hours)

    filtered = []
    for change in changes:
        # 使用变更时间进行过滤
        if change.change_time and change.change_time >= cutoff_time:
            filtered.append(change)
        elif change.change_time is None:
            # 尝试获取文件系统时间作为回退
            try:
                full_path = os.path.join(".", change.file_path)
                if os.path.exists(full_path):
                    mtime = os.path.getmtime(full_path)
                    file_time = datetime.datetime.fromtimestamp(mtime)
                    if file_time >= cutoff_time:
                        change.change_time = file_time
                        filtered.append(change)
            except Exception:
                pass

    # 按时间倒序排列
    filtered.sort(key=lambda x: x.change_time or datetime.datetime.min, reverse=True)

    return filtered


# ================= 变更图标映射 =================


def get_change_icon(status: str) -> str:
    """
    获取变更类型的图标

    Args:
        status: 变更状态码 (M, A, D, R, C, U, ??)

    Returns:
        str: 对应的图标

    Examples:
        >>> get_change_icon('M')
        '🟢'
        >>> get_change_icon('A')
        '🔵'
    """
    return CHANGE_ICONS.get(status, "⚪")


def get_change_description(status: str) -> str:
    """
    获取变更类型的描述

    Args:
        status: 变更状态码

    Returns:
        str: 变更描述
    """
    return CHANGE_DESCRIPTIONS.get(status, "未知")


def format_change_summary(change: GitChange) -> str:
    """格式化单个变更的摘要"""
    parts = [change.icon, change.file_path, f"({change.status_desc})"]
    if change.change_time:
        time_str = change.change_time.strftime("%Y-%m-%d %H:%M")
        parts.append(f"@{time_str}")
    return " ".join(parts)


# ================= 表格生成器 =================


def generate_change_table(
    changes: List[GitChange],
    include_description: bool = True,
    max_rows: Optional[int] = None,
) -> str:
    """
    生成变更表格（Markdown格式）

    表格列：文件、目录、变更、时间、描述

    Args:
        changes: 变更列表
        include_description: 是否包含描述列
        max_rows: 最大行数，None表示不限制

    Returns:
        str: Markdown格式的表格
    """
    if not changes:
        return "_暂无变更记录_"

    # 限制行数
    display_changes = changes[:max_rows] if max_rows else changes

    # 表头
    headers = ["文件", "目录", "变更", "时间"]
    if include_description:
        headers.append("描述")

    # 生成表头行
    header_line = "| " + " | ".join(headers) + " |"
    separator_line = "|" + "|".join([" --- " for _ in headers]) + "|"

    # 生成数据行
    rows = []
    for change in display_changes:
        file_name = change.file_name
        directory = change.directory if change.directory != "." else "根目录"
        change_type = f"{change.icon} {change.status_desc}"
        time_str = (
            change.change_time.strftime("%m-%d %H:%M") if change.change_time else "-"
        )

        row_parts = [file_name, directory, change_type, time_str]

        if include_description:
            desc = change.description if change.description else "-"
            row_parts.append(desc)

        rows.append("| " + " | ".join(row_parts) + " |")

    # 如果有限制行数，添加提示
    if max_rows and len(changes) > max_rows:
        rows.append(f"\n_... 还有 {len(changes) - max_rows} 条记录未显示_")

    return "\n".join([header_line, separator_line] + rows)


def generate_directory_summary_table(dir_stats: Dict[str, DirectoryStats]) -> str:
    """
    生成目录变更摘要表格

    Args:
        dir_stats: 目录统计信息

    Returns:
        str: Markdown格式的表格
    """
    if not dir_stats:
        return "_暂无变更记录_"

    # 按变更数量排序
    sorted_dirs = sorted(
        dir_stats.values(), key=lambda x: x.total_changes, reverse=True
    )

    headers = ["目录", "变更数", "类型分布", "状态"]
    header_line = "| " + " | ".join(headers) + " |"
    separator_line = "|" + "|".join([" --- " for _ in headers]) + "|"

    rows = []
    for stats in sorted_dirs:
        directory = stats.directory
        count = str(stats.total_changes)

        # 格式化类型分布
        type_dist = ", ".join(
            [f"{desc}: {count}" for desc, count in stats.change_types.items()]
        )

        # 热点标记
        status = "🔥 热点" if stats.is_hotspot else "-"

        rows.append(f"| {directory} | {count} | {type_dist} | {status} |")

    return "\n".join([header_line, separator_line] + rows)


# ================= 集成函数 =================


def get_recent_git_changes(
    repo_path: str = ".", hours: int = DEFAULT_HOURS, max_results: Optional[int] = None
) -> Tuple[GitStatus, List[GitChange]]:
    """
    获取最近的Git变更（集成函数）

    Args:
        repo_path: 仓库路径
        hours: 时间范围（小时）
        max_results: 最大返回结果数

    Returns:
        Tuple[GitStatus, List[GitChange]]: Git状态和被过滤的变更列表
    """
    git_status = get_git_status(repo_path)

    if not git_status.is_git_repo or not git_status.changes:
        return git_status, []

    filtered = filter_by_time(git_status.changes, hours)

    if max_results:
        filtered = filtered[:max_results]

    return git_status, filtered


def generate_git_report(
    repo_path: str = ".",
    hours: int = DEFAULT_HOURS,
    max_changes: int = 20,
    max_dirs: int = 10,
) -> str:
    """
    生成完整的Git状态报告

    Args:
        repo_path: 仓库路径
        hours: 时间范围（小时）
        max_changes: 变更表格最大行数
        max_dirs: 目录摘要最大行数

    Returns:
        str: Markdown格式的完整报告
    """
    git_status, recent_changes = get_recent_git_changes(repo_path, hours, max_changes)

    lines = []
    lines.append("## 📊 Git 状态报告")
    lines.append("")

    # 仓库信息
    if git_status.is_git_repo:
        lines.append(f"**分支:** `{git_status.branch or '未知'}`")
        lines.append(f"**最新提交:** `{git_status.commit_hash or '未知'}`")
        lines.append(f"**时间范围:** 最近 {hours} 小时")
    else:
        lines.append("⚠️ 当前目录不是Git仓库")
        if git_status.error_message:
            lines.append(f"*错误: {git_status.error_message}*")
        return "\n".join(lines)

    lines.append("")

    # 变更统计
    if recent_changes:
        lines.append(f"**找到 {len(recent_changes)} 个变更**")
        lines.append("")

        # 变更详情表
        lines.append("### 🔍 变更详情")
        lines.append(generate_change_table(recent_changes, max_rows=max_changes))
        lines.append("")

        # 目录摘要
        dir_stats = classify_changes(git_status)
        recent_dirs = {
            k: v
            for k, v in dir_stats.items()
            if any(c in v.files for c in recent_changes)
        }

        if recent_dirs:
            lines.append("### 📁 目录分布")
            # 限制显示的目录数量
            limited_dirs = dict(list(recent_dirs.items())[:max_dirs])
            lines.append(generate_directory_summary_table(limited_dirs))
            if len(recent_dirs) > max_dirs:
                lines.append(f"\n_... 还有 {len(recent_dirs) - max_dirs} 个目录未显示_")
            lines.append("")

        # 热点区域
        hotspots = get_hotspot_directories(dir_stats)
        recent_hotspots = [h for h in hotspots if h.directory in recent_dirs]

        if recent_hotspots:
            lines.append("### 🔥 热点区域")
            for hotspot in recent_hotspots[:5]:
                lines.append(f"- `{hotspot.directory}`: {hotspot.total_changes} 个变更")
            lines.append("")
    else:
        lines.append("_在指定时间范围内未找到变更_")

    return "\n".join(lines)


# ================= 主函数（测试用） =================


def main():
    """测试主函数"""
    print("=" * 60)
    print("Git 状态检测模块测试")
    print("=" * 60)
    print()

    # 测试Git状态读取
    print("1. Git状态检测:")
    git_status = get_git_status()
    print(f"   是否为Git仓库: {git_status.is_git_repo}")
    if git_status.is_git_repo:
        print(f"   分支: {git_status.branch}")
        print(f"   提交: {git_status.commit_hash}")
        print(f"   变更数: {len(git_status.changes)}")
    print()

    # 测试变更分类
    if git_status.changes:
        print("2. 变更分类统计:")
        dir_stats = classify_changes(git_status)
        for directory, stats in list(dir_stats.items())[:5]:
            print(f"   {directory}: {stats.total_changes} 个变更")
        print()

        # 测试时间过滤
        print("3. 最近24小时变更:")
        recent = filter_by_time(git_status.changes, hours=24)
        print(f"   找到 {len(recent)} 个变更")
        for change in recent[:5]:
            print(f"   {format_change_summary(change)}")
        print()

        # 测试表格生成
        print("4. 变更表格:")
        print(generate_change_table(recent[:10]))
        print()

        # 测试热点区域
        print("5. 热点区域:")
        hotspots = get_hotspot_directories(dir_stats)
        for hotspot in hotspots[:3]:
            print(f"   🔥 {hotspot.directory}: {hotspot.total_changes} 个变更")
        print()

    # 生成完整报告
    print("=" * 60)
    print("完整Git报告")
    print("=" * 60)
    print(generate_git_report(hours=168, max_changes=10))


if __name__ == "__main__":
    main()
