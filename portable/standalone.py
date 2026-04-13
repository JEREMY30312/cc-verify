#!/usr/bin/env python3
"""
> **Description:** 项目地图生成器独立版 - 单文件，无外部依赖

项目地图生成器 V2.3 独立版
支持Git集成、LLM智能描述、学习机制、YAML描述、一键安装/卸载/升级
单文件，Python 3.6+，无外部依赖
"""

import os
import sys
import json
import re
import subprocess
import datetime
import shutil
import time
import argparse
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
        "playwright-report",
        "coverage",
        ".nyc_output",
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
    "description": {
        "mode": "llm",
        "max_length": 20,
        "cache_file": ".file-descriptions.json",
        "tasks_file": ".llm-tasks.json",
        "timeout_seconds": 60,
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

# LLM描述配置
DESC_CONFIG = CONFIG.get("description", {})
DESC_MODE = DESC_CONFIG.get("mode", "llm")
DESC_CACHE_FILE = DESC_CONFIG.get("cache_file", ".file-descriptions.json")
DESC_TASKS_FILE = DESC_CONFIG.get("tasks_file", ".llm-tasks.json")
DESC_TIMEOUT = DESC_CONFIG.get("timeout_seconds", 60)

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


# ================= LLM描述生成模块（独立版内嵌） =================


def read_file_preview(file_path, max_lines=10):
    """读取文件前几行作为内容预览"""
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = []
            for i, line in enumerate(f):
                if i >= max_lines:
                    break
                lines.append(line.strip())
            return "\n".join(lines)[:500]
    except Exception:
        return ""


def is_modified(file_info, cache):
    """判断文件是否被修改（基于mtime）"""
    if file_info.path not in cache:
        return True
    cached = cache[file_info.path]
    return file_info.mtime > cached.get("mtime", 0)


def detect_file_changes(files_info, cache_file, max_description_length):
    """检测需要生成描述的文件"""
    existing = load_description_cache(cache_file)

    tasks = []
    for f in files_info:
        if not f.path.endswith(".md"):
            continue

        if f.path not in existing or is_modified(f, existing):
            content_preview = read_file_preview(f.path)
            tasks.append(
                {
                    "type": "generate_description",
                    "file": f.path,
                    "content_preview": content_preview,
                    "max_length": max_description_length,
                }
            )

    return tasks


def load_description_cache(cache_file):
    """加载描述缓存"""
    if os.path.exists(cache_file):
        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def write_tasks_json(tasks, output_file):
    """输出任务清单供AI平台处理"""
    if not tasks:
        if os.path.exists(output_file):
            os.remove(output_file)
        return

    task_data = {
        "version": "2.2",
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "task_count": len(tasks),
        "tasks": tasks,
    }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(task_data, f, ensure_ascii=False, indent=2)

    print(f"📋 已生成 {len(tasks)} 个描述任务 → {output_file}")


def wait_for_ai_completion(timeout, cache_file):
    """等待AI完成描述生成（轮询检测）"""
    start_time = time.time()
    task_output_time = time.time()

    print(f"⏳ 等待AI处理描述（超时{timeout}秒）...")

    while time.time() - start_time < timeout:
        if os.path.exists(cache_file):
            mtime = os.path.getmtime(cache_file)
            if mtime > task_output_time:
                elapsed = time.time() - start_time
                print(f"✅ AI完成描述生成（耗时{elapsed:.1f}秒）")
                return True
        time.sleep(1)

    return False


def get_description_from_cache(cache, file_path):
    """从缓存获取文件描述"""
    if file_path in cache:
        return cache[file_path].get("description")
    return None


def clean_description_cache(cache, current_files):
    """清理已删除文件的缓存"""
    current_set = set(current_files)
    cleaned = {k: v for k, v in cache.items() if k in current_set}

    removed_count = len(cache) - len(cleaned)
    if removed_count > 0:
        print(f"🧹 清理了 {removed_count} 个已删除文件的缓存")

    return cleaned


def save_description_cache(cache, cache_file):
    """保存描述缓存"""
    with open(cache_file, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)


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
            "generator_version": "2.2-standalone",
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
            elif depth + 1 >= max_depth:
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
 > **Version:** 2.2 Standalone | **Mode:** 智能层级 + 关键文件识别 + LLM描述

## 🔥 最近变动 (7天)

{change_table}

## 📂 文件目录

```text
.
{chr(10).join(tree_lines)}
```

---
*由 standalone.py 独立版 V2.2 自动生成*
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

        # LLM描述生成（钩子模式）
        if DESC_MODE == "llm":
            tasks = detect_file_changes(
                files_info, DESC_CACHE_FILE, MAX_DESCRIPTION_LENGTH
            )
            if tasks:
                write_tasks_json(tasks, DESC_TASKS_FILE)
                if wait_for_ai_completion(DESC_TIMEOUT, DESC_CACHE_FILE):
                    ai_cache = load_description_cache(DESC_CACHE_FILE)
                    for f in files_info:
                        desc = get_description_from_cache(ai_cache, f.path)
                        if desc:
                            f.description = desc
                            f.is_new_format = True
                    current_files = [f.path for f in files_info]
                    cleaned_cache = clean_description_cache(ai_cache, current_files)
                    save_description_cache(cleaned_cache, DESC_CACHE_FILE)

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


# ================= 安装/卸载/升级 =================


def get_global_config_path():
    """获取全局配置文件路径"""
    config_dir = os.path.expanduser("~/.config/project-map")
    os.makedirs(config_dir, exist_ok=True)
    return os.path.join(config_dir, "config.json")


def load_global_config():
    """加载全局配置"""
    config_path = get_global_config_path()
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "default_repo": "JEREMY30312/cc-verify",
        "default_branch": "main",
        "installed_hooks": False,
    }


def save_global_config(config):
    """保存全局配置"""
    config_path = get_global_config_path()
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


def install(repo="JEREMY30312/cc-verify", branch="main"):
    """一键安装"""
    print("🗺️  项目地图生成器 V2.3 - 安装中...")
    print("")

    # 1. 下载主程序
    print("📥 下载主程序...")
    url = f"https://raw.githubusercontent.com/{repo}/{branch}/portable/standalone.py"
    try:
        result = subprocess.run(
            ["curl", "-fsSL", "-o", "generate_map.py", url],
            check=True,
            capture_output=True,
            text=True,
        )
        print("   ✅ 已下载 generate_map.py")
    except subprocess.CalledProcessError as e:
        print(f"   ❌ 下载失败: {e.stderr}")
        return False

    # 2. 创建默认配置
    print("⚙️  创建默认配置...")
    with open(".project-map-config.json", "w", encoding="utf-8") as f:
        json.dump(DEFAULT_CONFIG, f, ensure_ascii=False, indent=2)
    print("   ✅ 已创建 .project-map-config.json")

    # 3. 保存全局配置
    global_config = load_global_config()
    global_config["default_repo"] = repo
    global_config["default_branch"] = branch
    save_global_config(global_config)

    # 4. 首次运行
    print("🚀 首次运行...")
    try:
        subprocess.run(["python3", "generate_map.py"], check=True)
    except subprocess.CalledProcessError:
        print("   ⚠️  首次运行失败，请手动运行: python3 generate_map.py")

    # 5. 询问是否安装钩子
    if os.path.isdir(".git"):
        print("")
        print("🔧 是否安装 Git 钩子？")
        print("   安装后，每次提交/合并/切换分支时自动更新项目地图")
        print("   输入 'y' 安装，其他键跳过")
        try:
            choice = input("   > ")
            if choice.lower() == "y":
                install_hooks()
                global_config["installed_hooks"] = True
                save_global_config(global_config)
        except (EOFError, KeyboardInterrupt):
            print("   ⏭️  跳过钩子安装")

    print("")
    print("✅ 安装完成！")
    print("   使用: python3 generate_map.py")
    print("   卸载: python3 generate_map.py --uninstall")
    print("   升级: python3 generate_map.py --upgrade")
    print("")
    print("📖 文档: https://github.com/JEREMY30312/cc-verify")
    print("")
    print("💡 提示: LLM模式需要AI平台支持，首次运行会生成任务清单")

    return True


def uninstall():
    """卸载"""
    print("⚠️  即将卸载项目地图生成器")
    print("")
    print("将删除以下文件：")
    print("   - generate_map.py")
    print("   - .project-map-config.json")
    print("   - .project-map-config.example.json")
    print("   - .file-descriptions.json")
    print("   - .llm-tasks.json")
    print("   - PROJECT_MAP.md")
    print("   - PROJECT_FINGERPRINT.json")
    print("   - PROJECT_CLEANUP_GUIDE.md (如果存在)")
    print("   - .git/hooks/post-commit (如果存在)")
    print("   - .git/hooks/post-merge (如果存在)")
    print("   - .git/hooks/post-checkout (如果存在)")
    print("")

    # 二次确认
    print("确定要卸载吗？(y/n) ", end="")
    try:
        choice = input()
        if choice.lower() != "y":
            print("❌ 已取消卸载")
            return False
    except (EOFError, KeyboardInterrupt):
        print("❌ 已取消卸载")
        return False

    print("")
    print("🗑️  删除文件...")

    # 删除主程序和配置文件
    files_to_delete = [
        "generate_map.py",
        ".project-map-config.json",
        ".project-map-config.example.json",
        ".file-descriptions.json",
        ".llm-tasks.json",
        "PROJECT_MAP.md",
        "PROJECT_FINGERPRINT.json",
        "PROJECT_CLEANUP_GUIDE.md",
    ]

    for file in files_to_delete:
        if os.path.exists(file):
            os.remove(file)
            print(f"   ✅ 已删除 {file}")

    # 删除Git钩子
    hooks_to_delete = [
        ".git/hooks/post-commit",
        ".git/hooks/post-merge",
        ".git/hooks/post-checkout",
    ]

    for hook in hooks_to_delete:
        if os.path.exists(hook):
            os.remove(hook)
            print(f"   ✅ 已删除 {hook}")

    # 清理全局配置
    global_config = load_global_config()
    global_config["installed_hooks"] = False
    save_global_config(global_config)

    print("")
    print("✅ 卸载完成！")
    print("   如需重新安装，请运行:")
    print(
        "   curl -fsSL https://raw.githubusercontent.com/JEREMY30312/cc-verify/main/portable/install.sh | bash"
    )

    return True


def upgrade(repo=None, branch=None):
    """升级"""
    print("🔄 项目地图生成器 - 升级中...")
    print("")

    # 读取全局配置
    global_config = load_global_config()
    if repo is None:
        repo = global_config.get("default_repo", "JEREMY30312/cc-verify")
    if branch is None:
        branch = global_config.get("default_branch", "main")

    # 1. 备份配置
    print("💾 备份配置...")
    if os.path.exists(".project-map-config.json"):
        shutil.copy(".project-map-config.json", ".project-map-config.json.backup")
        print("   ✅ 已备份 .project-map-config.json")

    # 2. 下载最新版本
    print("📥 下载最新版本...")
    url = f"https://raw.githubusercontent.com/{repo}/{branch}/portable/standalone.py"
    try:
        result = subprocess.run(
            ["curl", "-fsSL", "-o", "generate_map.py", url],
            check=True,
            capture_output=True,
            text=True,
        )
        print("   ✅ 已下载 generate_map.py")
    except subprocess.CalledProcessError as e:
        print(f"   ❌ 下载失败: {e.stderr}")
        return False

    # 3. 恢复配置
    print("⚙️  恢复配置...")
    if os.path.exists(".project-map-config.json.backup"):
        shutil.copy(".project-map-config.json.backup", ".project-map-config.json")
        print("   ✅ 已恢复 .project-map-config.json")

    # 4. 重新安装钩子（如果之前有）
    if global_config.get("installed_hooks", False):
        print("🔧 重新安装钩子...")
        try:
            install_hooks()
            print("   ✅ 已重新安装钩子")
        except Exception:
            print("   ⚠️  钩子安装失败")

    # 5. 更新全局配置
    global_config["default_repo"] = repo
    global_config["default_branch"] = branch
    save_global_config(global_config)

    print("")
    print("✅ 升级完成！")
    print("   使用: python3 generate_map.py")

    return True


# ================= 主函数 =================


def main():
    """主函数"""
    print("🚀 开始生成项目地图 V2.3 (独立版)...")

    print("📁 扫描项目结构...")
    files_info = scan_project_structure(".")
    print(f"   找到 {len(files_info)} 个文件")

    print("🔍 获取Git状态...")
    git_changes = get_git_status(".")
    print(f"   找到 {len(git_changes)} 个变更")

    # LLM智能描述生成
    if DESC_MODE == "llm":
        print("🤖 检查文件描述...")
        tasks = detect_file_changes(files_info, DESC_CACHE_FILE, MAX_DESCRIPTION_LENGTH)

        if tasks:
            write_tasks_json(tasks, DESC_TASKS_FILE)
            print(f"   📋 发现 {len(tasks)} 个文件需要描述，等待AI处理...")

            if not wait_for_ai_completion(DESC_TIMEOUT, DESC_CACHE_FILE):
                print("❌ 描述生成超时，请检查AI平台")
                sys.exit(1)

            # 读取AI生成的描述
            ai_cache = load_description_cache(DESC_CACHE_FILE)
            for f in files_info:
                desc = get_description_from_cache(ai_cache, f.path)
                if desc:
                    f.description = desc
                    f.is_new_format = True

            # 清理已删除文件的缓存
            current_files = [f.path for f in files_info]
            cleaned_cache = clean_description_cache(ai_cache, current_files)
            save_description_cache(cleaned_cache, DESC_CACHE_FILE)
        else:
            print("   ✅ 所有文件描述已是最新")
    else:
        # 传统模式：使用YAML front matter提取
        print("📝 使用传统描述提取方式...")
        for f in files_info:
            if f.path.endswith(".md"):
                desc, is_new = get_file_description(f.path)
                if desc:
                    f.description = desc
                    f.is_new_format = is_new

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
    parser = argparse.ArgumentParser(description="项目地图生成器 V2.3 (独立版)")
    parser.add_argument("--install", action="store_true", help="一键安装")
    parser.add_argument("--uninstall", action="store_true", help="卸载")
    parser.add_argument("--upgrade", action="store_true", help="升级")
    parser.add_argument("--repo", help="GitHub仓库 (owner/repo)")
    parser.add_argument("--branch", help="Git分支 (默认: main)")
    parser.add_argument("--silent", action="store_true", help="静默模式")
    parser.add_argument("--install-hooks", action="store_true", help="安装Git钩子")

    args = parser.parse_args()

    # 处理安装/卸载/升级
    if args.install:
        repo = args.repo or "JEREMY30312/cc-verify"
        branch = args.branch or "main"
        install(repo, branch)
        sys.exit(0)

    if args.uninstall:
        uninstall()
        sys.exit(0)

    if args.upgrade:
        upgrade(args.repo, args.branch)
        sys.exit(0)

    if args.install_hooks:
        install_hooks()
        sys.exit(0)

    # 正常运行
    main()
