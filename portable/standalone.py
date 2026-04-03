#!/usr/bin/env python3
"""
> **Description:** 项目地图生成器独立版 - 单文件，无外部依赖

项目地图生成器 V2.0 独立版
支持Git集成、学习机制、YAML描述提取
单文件，Python 3.6+，无外部依赖
"""

import os
import sys
import json
import re
import subprocess
import datetime
import shutil
from pathlib import Path
from collections import defaultdict

# ================= 内置默认配置 =================

DEFAULT_CONFIG = {
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
        ".backups",
    ],
    "collapse_folders": ["backups", ".strategic-snapshots", "版本汇总", ".backup"],
    "hooks": {
        "post_commit_update": True,
        "post_merge_update": True,
        "post_checkout_update": True,
        "auto_add_to_git": True,
    },
    "output": {
        "map_file": "PROJECT_MAP.md",
        "fingerprint_file": "PROJECT_FINGERPRINT.json",
    },
}

# ================= 配置加载 =================


def load_config():
    """加载配置文件（独立版优先使用内置配置）"""
    config = DEFAULT_CONFIG.copy()

    # 独立版也支持外部配置覆盖
    try:
        with open(".project-map-config.json", "r") as f:
            user_config = json.load(f)
            for key, value in user_config.items():
                if key in config:
                    if isinstance(value, dict) and isinstance(config[key], dict):
                        config[key].update(value)
                    else:
                        config[key] = value
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    return config


CONFIG = load_config()

# ================= 常量 =================

TARGET_FILE = CONFIG["output"]["map_file"]
FINGERPRINT_FILE = CONFIG["output"]["fingerprint_file"]
TIME_RANGE_HOURS = CONFIG["time_range_hours"]
MAX_DESCRIPTION_LENGTH = CONFIG["max_description_length"]
MAX_TREE_DEPTH = CONFIG.get("max_tree_depth", 3)
SHALLOW_FOLDERS = set(CONFIG.get("shallow_folders", []))
IGNORE_LIST = set(CONFIG["ignore_list"])
COLLAPSE_FOLDERS = set(CONFIG["collapse_folders"])

# ================= 智能层级控制 =================


def get_max_depth(folder_name):
    """根据文件夹类型返回最大显示深度"""
    shallow_folders = {
        "backups",
        ".backup",
        "版本汇总",
        "archive",
        "历史版本",
        "回收文件",
        "logs",
        ".log",
        "错误日志",
        "organizer.log",
        "organizer-error.log",
        "test_scripts",
        "tests",
        "spec",
        "__tests__",
        "dist",
        "build",
        "out",
        ".next",
        "node_modules",
        ".idea",
        ".vscode",
        ".settings",
        ".strategic-snapshots",
        ".snapshots",
        "__pycache__",
        ".cache",
        "tmp",
        "temp",
        "缓存",
        "临时池",
        "暂存数据",
        "暂存脚本",
    }

    if folder_name in shallow_folders:
        return 1
    return MAX_TREE_DEPTH


# ================= 关键文件类型识别 =================


def is_key_file(file_path):
    """基于类型识别关键文件（而非具体文件名）"""
    name = Path(file_path).name.lower()
    stem = Path(file_path).stem.lower()

    key_patterns = [
        "readme",
        "claude",
        "agents",
        "handoff",
        "project_state",
        "codemap",
        "package.json",
        "tsconfig",
        "config",
        "配置",
        "settings",
        ".env",
        "workspace",
        "product-spec",
        "spec",
        "规格",
        "workflow",
        "流程",
        "pipeline",
        "persona",
        "skill",
        "design",
        "plan",
        "设计",
        "计划",
        "audit",
        "verify",
        "验收",
        "test_report",
        "app.tsx",
        "main.tsx",
        "index.ts",
        "layout.tsx",
        "page.tsx",
        "generate_map",
        "standalone",
        "install",
    ]

    return any(pattern in stem or pattern in name for pattern in key_patterns)


def should_show_description(file_path, depth):
    """判断是否显示描述"""
    if depth <= 2 and file_path.endswith(".md"):
        return True

    if is_key_file(file_path):
        return True

    return False


CHANGE_ICONS = {
    "M": ("🟢", "修改"),
    "A": ("🔵", "新增"),
    "D": ("🔴", "删除"),
    "R": ("🟡", "重命名"),
    "C": ("🟣", "复制"),
    "U": ("🟠", "冲突"),
    "??": ("⚪", "未跟踪"),
}

# ================= 数据类 =================


class FileInfo:
    """文件信息"""

    def __init__(
        self, path, name, directory, mtime, size, description="", is_new_format=False
    ):
        self.path = path
        self.name = name
        self.directory = directory
        self.mtime = mtime
        self.size = size
        self.description = description
        self.is_new_format = is_new_format


class GitChange:
    """Git变更记录"""

    def __init__(self, status, file_path, original_path=None, change_time=None):
        self.status = status
        self.file_path = file_path
        self.original_path = original_path
        self.change_time = change_time


# ================= 描述提取器 =================


def extract_yaml_description(file_path):
    """从YAML front matter提取描述"""
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read(1000)

        if not content.startswith("---"):
            return None

        end_match = re.search(r"\n---\s*\n", content)
        if not end_match:
            return None

        yaml_content = content[3 : end_match.start()]
        desc_match = re.search(r"^description:\s*(.+)$", yaml_content, re.MULTILINE)
        if desc_match:
            desc = desc_match.group(1).strip()
            if (desc.startswith('"') and desc.endswith('"')) or (
                desc.startswith("'") and desc.endswith("'")
            ):
                desc = desc[1:-1]
            return desc[:MAX_DESCRIPTION_LENGTH]
        return None
    except Exception:
        return None


def extract_markdown_description(file_path):
    """从Markdown引用块提取描述"""
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()[:10]

        for line in lines:
            match = re.search(
                r">\s*\*\*(?:Desc|Description):\*\*\s*(.+)", line, re.IGNORECASE
            )
            if match:
                return match.group(1).strip()[:MAX_DESCRIPTION_LENGTH]
        return None
    except Exception:
        return None


def get_file_description(file_path):
    """获取文件描述"""
    if not file_path.endswith(".md"):
        return "", False

    yaml_desc = extract_yaml_description(file_path)
    if yaml_desc:
        return yaml_desc, True

    md_desc = extract_markdown_description(file_path)
    if md_desc:
        return md_desc, False

    return "", False


# ================= Git集成模块 =================


def is_git_repository(path="."):
    """检查是否为Git仓库"""
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


def get_git_status(repo_path="."):
    """获取Git状态"""
    if not is_git_repository(repo_path):
        return []

    try:
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

            staged = line[0]
            unstaged = line[1]
            status = unstaged if unstaged != " " and unstaged != "?" else staged
            rest = line[3:]

            if status == "R" and " -> " in rest:
                parts = rest.split(" -> ")
                changes.append(GitChange(status, parts[1], parts[0]))
            else:
                changes.append(GitChange(status, rest))

        return changes
    except Exception:
        return []


# ================= 项目结构扫描 =================


def scan_project_structure(dir_path="."):
    """扫描项目结构"""
    files_info = []

    for root, dirs, files in os.walk(dir_path):
        dirs[:] = [d for d in dirs if d not in IGNORE_LIST and not d.startswith(".")]

        for file in files:
            if file in IGNORE_LIST or file.startswith("."):
                continue

            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, start=".")

            try:
                stat = os.stat(full_path)
                desc, is_new = get_file_description(full_path)

                files_info.append(
                    FileInfo(
                        path=rel_path,
                        name=file,
                        directory=os.path.dirname(rel_path)
                        if os.path.dirname(rel_path)
                        else "根目录",
                        mtime=stat.st_mtime,
                        size=stat.st_size,
                        description=desc,
                        is_new_format=is_new,
                    )
                )
            except Exception:
                continue

    return files_info


# ================= 学习机制模块 =================


def analyze_project_domain(files_info):
    """分析项目领域"""
    extensions = defaultdict(int)

    for f in files_info:
        ext = Path(f.name).suffix.lower()
        if ext:
            extensions[ext] += 1

    if ".py" in extensions and extensions[".py"] > 5:
        return "Python项目"
    elif ".js" in extensions or ".ts" in extensions:
        return "JavaScript/TypeScript项目"
    elif ".md" in extensions and extensions[".md"] > 20:
        return "文档型项目"
    else:
        return "通用项目"


def detect_architecture(files_info):
    """检测架构模式"""
    dirs = set(f.directory for f in files_info)
    patterns = []

    if any("skills" in d or "skill" in d for d in dirs):
        patterns.append("SKILL-based")
    if any("agents" in d or "agent" in d for d in dirs):
        patterns.append("Agent协作")
    if any("test" in d for d in dirs):
        patterns.append("测试驱动")
    if any(".claude" in d for d in dirs):
        patterns.append("Claude集成")

    return ", ".join(patterns) if patterns else "标准结构"


def identify_key_characteristics(files_info):
    """识别关键特征"""
    characteristics = []
    dirs = set(f.directory for f in files_info)

    if any("workflow" in f.name.lower() for f in files_info):
        characteristics.append("工作流驱动")
    if any("review" in f.name.lower() for f in files_info):
        characteristics.append("审核机制")
    if any("prompt" in f.name.lower() for f in files_info):
        characteristics.append("提示词工程")
    if any("config" in d.lower() for d in dirs):
        characteristics.append("配置化")

    md_files = sum(1 for f in files_info if f.name.endswith(".md"))
    if md_files > 30:
        characteristics.append("重度文档化")

    return characteristics[:5]


def generate_ai_index(files_info, git_changes):
    """生成AI优化索引"""
    quick_answers = {}

    for f in files_info:
        if "README" in f.name or "AGENTS" in f.name:
            quick_answers["如何开始"] = f.path
        if "config" in f.name.lower():
            quick_answers["配置在哪里"] = f.path
        if "skill" in f.path.lower():
            quick_answers["技能文档"] = f.path
        if "review" in f.name.lower():
            quick_answers["审核流程"] = f.path

    search_shortcuts = defaultdict(list)
    for f in files_info:
        if f.name.endswith(".md"):
            search_shortcuts["Markdown文档"].append(f.path)
        elif f.name.endswith(".py"):
            search_shortcuts["Python脚本"].append(f.path)
        elif f.name.endswith(".json"):
            search_shortcuts["JSON配置"].append(f.path)

    recent_dirs = defaultdict(int)
    for change in git_changes:
        dir_path = os.path.dirname(change.file_path) or "根目录"
        recent_dirs[dir_path] += 1

    hot_directories = sorted(recent_dirs.items(), key=lambda x: x[1], reverse=True)[:5]

    return {
        "quick_answers": quick_answers,
        "search_shortcuts": dict(search_shortcuts),
        "hot_directories": hot_directories,
        "file_count": len(files_info),
        "git_change_count": len(git_changes),
    }


def generate_project_fingerprint(files_info, git_changes):
    """生成项目指纹"""
    total_files = len(files_info)
    total_dirs = len(set(f.directory for f in files_info))

    domain = analyze_project_domain(files_info)
    architecture = detect_architecture(files_info)
    characteristics = identify_key_characteristics(files_info)

    key_dirs = defaultdict(lambda: {"count": 0, "files": []})
    for f in files_info:
        top_dir = f.directory.split("/")[0] if "/" in f.directory else f.directory
        key_dirs[top_dir]["count"] += 1
        if len(key_dirs[top_dir]["files"]) < 5:
            key_dirs[top_dir]["files"].append(f.name)

    now = datetime.datetime.now()
    cutoff_time = now - datetime.timedelta(hours=TIME_RANGE_HOURS)

    recent_changes = []
    for change in git_changes:
        if change.change_time and change.change_time >= cutoff_time:
            recent_changes.append(change)

    ai_index = generate_ai_index(files_info, git_changes)

    fingerprint = {
        "metadata": {
            "generated_at": now.isoformat(),
            "generator_version": "2.0-standalone",
            "total_files": total_files,
            "total_directories": total_dirs,
            "time_range_hours": TIME_RANGE_HOURS,
        },
        "project_profile": {
            "domain": domain,
            "architecture": architecture,
            "key_characteristics": characteristics,
        },
        "structural_insights": {
            "key_directories": dict(key_dirs),
            "file_type_distribution": {},
        },
        "temporal_analysis": {
            "recent_changes_count": len(recent_changes),
            "hot_directories": ai_index["hot_directories"],
        },
        "ai_optimized_index": ai_index,
    }

    return fingerprint


# ================= 输出生成 =================


def generate_change_table(changes, files_info):
    """生成变更表格"""
    if not changes:
        return "_暂无变更记录_"

    sorted_changes = sorted(
        changes, key=lambda x: x.change_time or datetime.datetime.min, reverse=True
    )

    lines = [
        "| 文件 | 目录 | 变更 | 时间 | 描述 |",
        "|------|------|------|------|------|",
    ]

    for change in sorted_changes[:20]:
        file_name = os.path.basename(change.file_path)
        directory = os.path.dirname(change.file_path) or "根目录"

        icon, desc = CHANGE_ICONS.get(change.status, ("⚪", "未知"))
        change_str = f"{icon} {desc}"

        time_str = (
            change.change_time.strftime("%m-%d %H:%M") if change.change_time else "-"
        )

        file_desc = ""
        for f in files_info:
            if f.path == change.file_path:
                file_desc = f.description
                break

        lines.append(
            f"| {file_name} | {directory} | {change_str} | {time_str} | {file_desc or '-'} |"
        )

    return "\n".join(lines)


def generate_tree(dir_path, prefix="", depth=0, files_info=None):
    """生成目录树（支持智能层级控制）"""
    if depth > 5:
        return []

    if files_info is None:
        files_info = scan_project_structure(dir_path)

    try:
        entries = sorted(os.listdir(dir_path))
    except PermissionError:
        return []

    filtered = [e for e in entries if e not in IGNORE_LIST and not e.startswith(".")]

    result = []
    pointers = [("├── ", "│   ")] * (len(filtered) - 1) + [("└── ", "    ")]

    for pointer, entry in zip(pointers, filtered):
        full_path = os.path.join(dir_path, entry)
        rel_path = os.path.relpath(full_path, start=".")

        desc = ""
        for f in files_info:
            if f.path == rel_path:
                desc = f.description
                break

        # 智能控制描述显示
        if desc and should_show_description(rel_path, depth):
            comment = f"  # {desc}"
        else:
            comment = ""
        result.append(f"{prefix}{pointer[0]}{entry}{comment}")

        if os.path.isdir(full_path):
            max_depth = get_max_depth(entry)
            if entry in COLLAPSE_FOLDERS:
                result.append(f"{prefix}{pointer[1]}└── ...")
            elif depth >= max_depth:
                result.append(f"{prefix}{pointer[1]}└── ...")
            else:
                result.extend(
                    generate_tree(full_path, prefix + pointer[1], depth + 1, files_info)
                )

    return result


def generate_project_map(files_info, git_changes):
    """生成项目地图"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    change_table = generate_change_table(git_changes, files_info)
    tree_lines = generate_tree(".", files_info=files_info)

    content = f"""# 🗺️ 项目地图 (Live)

> **Updated:** {timestamp}
 > **Version:** 2.1 Standalone | **Mode:** 智能层级 + 关键文件识别

## 🔥 最近变动 (7天)

{change_table}

## 📂 文件目录

```text
.
{chr(10).join(tree_lines)}
```

---
*由 standalone.py 独立版自动生成*
"""

    return content


# ================= 钩子安装功能 =================


def install_hooks():
    """安装Git钩子到当前仓库"""
    if not os.path.isdir(".git"):
        print("❌ 当前目录不是Git仓库")
        return False

    hooks_dir = ".git/hooks"
    os.makedirs(hooks_dir, exist_ok=True)

    hook_scripts = {
        "post-commit": """#!/bin/bash
# post-commit hook - 提交后自动更新项目地图
python3 "$(dirname "$0")/../generate_map.py" --run-hook post-commit
""",
        "post-merge": """#!/bin/bash
# post-merge hook - 合并后自动更新项目地图
python3 "$(dirname "$0")/../generate_map.py" --run-hook post-merge
""",
        "post-checkout": """#!/bin/bash
# post-checkout hook - 切换分支后自动更新项目地图
python3 "$(dirname "$0")/../generate_map.py" --run-hook post-checkout
""",
    }

    installed = 0
    for hook_name, hook_content in hook_scripts.items():
        hook_path = os.path.join(hooks_dir, hook_name)
        with open(hook_path, "w") as f:
            f.write(hook_content)
        os.chmod(hook_path, 0o755)
        print(f"✅ 安装 {hook_name} 钩子")
        installed += 1

    print(f"\n🎉 钩子安装完成！共安装 {installed} 个钩子")
    return True


def run_hook(hook_name):
    """运行指定钩子"""
    hook_config_map = {
        "post-commit": "post_commit_update",
        "post-merge": "post_merge_update",
        "post-checkout": "post_checkout_update",
    }

    config_key = hook_config_map.get(hook_name)
    if not config_key:
        print(f"❌ 未知钩子类型: {hook_name}")
        return

    config = CONFIG
    if not config["hooks"].get(config_key, False):
        return

    hook_messages = {
        "post-commit": "🗺️  提交后更新项目地图...",
        "post-merge": "🗺️  合并后更新项目地图...",
        "post-checkout": "🗺️  切换分支后更新项目地图...",
    }

    print(hook_messages.get(hook_name, "🗺️  更新项目地图..."))

    try:
        # 直接调用主函数逻辑
        files_info = scan_project_structure(".")
        git_changes = get_git_status(".")

        map_content = generate_project_map(files_info, git_changes)
        with open(TARGET_FILE, "w", encoding="utf-8") as f:
            f.write(map_content)

        fingerprint = generate_project_fingerprint(files_info, git_changes)
        with open(FINGERPRINT_FILE, "w", encoding="utf-8") as f:
            json.dump(fingerprint, f, ensure_ascii=False, indent=2)

        print("✅ 项目地图已更新")

        if config["hooks"].get("auto_add_to_git", False):
            subprocess.run(
                ["git", "add", TARGET_FILE, FINGERPRINT_FILE],
                capture_output=True,
                timeout=10,
            )
            print("✅ 已添加到Git暂存区")
    except Exception as e:
        print(f"❌ 钩子执行失败: {e}")


# ================= 主函数 =================


def main():
    """主函数"""
    # 检查命令行参数
    if len(sys.argv) > 1:
        if sys.argv[1] == "--install-hooks":
            install_hooks()
            return
        elif sys.argv[1] == "--run-hook" and len(sys.argv) > 2:
            run_hook(sys.argv[2])
            return
        elif sys.argv[1] == "--silent":
            # 静默模式
            try:
                files_info = scan_project_structure(".")
                git_changes = get_git_status(".")

                map_content = generate_project_map(files_info, git_changes)
                with open(TARGET_FILE, "w", encoding="utf-8") as f:
                    f.write(map_content)

                fingerprint = generate_project_fingerprint(files_info, git_changes)
                with open(FINGERPRINT_FILE, "w", encoding="utf-8") as f:
                    json.dump(fingerprint, f, ensure_ascii=False, indent=2)
            except Exception:
                pass
            return

    print("🚀 开始生成项目地图 V2.0 (独立版)...")

    print("📁 扫描项目结构...")
    files_info = scan_project_structure(".")
    print(f"   找到 {len(files_info)} 个文件")

    print("🔍 获取Git状态...")
    git_changes = get_git_status(".")
    print(f"   找到 {len(git_changes)} 个变更")

    print("📝 生成项目地图...")
    map_content = generate_project_map(files_info, git_changes)

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(map_content)
    print(f"   ✅ 已保存到 {TARGET_FILE}")

    print("🧠 生成项目指纹...")
    fingerprint = generate_project_fingerprint(files_info, git_changes)

    with open(FINGERPRINT_FILE, "w", encoding="utf-8") as f:
        json.dump(fingerprint, f, ensure_ascii=False, indent=2)
    print(f"   ✅ 已保存到 {FINGERPRINT_FILE}")

    print("\n✨ 完成！")
    print(f"   - 项目地图: {TARGET_FILE}")
    print(f"   - 项目指纹: {FINGERPRINT_FILE}")
    print("\n💡 提示: 使用 --install-hooks 安装Git钩子实现自动更新")


if __name__ == "__main__":
    main()
