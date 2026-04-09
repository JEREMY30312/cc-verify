"""
> **Description:** LLM任务生成器 - 检测文件变更并生成描述任务清单

寄生式架构：脚本无API，通过文件(.llm-tasks.json)与AI平台通信
"""

import os
import json
import time
from pathlib import Path
from typing import List, Dict, Any, Optional


def read_file_preview(file_path: str, max_lines: int = 10) -> str:
    """读取文件前几行作为内容预览"""
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = []
            for i, line in enumerate(f):
                if i >= max_lines:
                    break
                lines.append(line.strip())
            return "\n".join(lines)[:500]  # 最多500字符
    except Exception:
        return ""


def is_modified(file_info, cache: Dict[str, Any]) -> bool:
    """判断文件是否被修改（基于mtime）"""
    if file_info.path not in cache:
        return True

    cached = cache[file_info.path]
    return file_info.mtime > cached.get("mtime", 0)


def detect_file_changes(
    files_info: List[Any],
    cache_file: str = ".file-descriptions.json",
    max_description_length: int = 20,
) -> List[Dict[str, Any]]:
    """
    检测需要生成描述的文件

    Args:
        files_info: 文件信息列表（FileInfo对象）
        cache_file: 描述缓存文件路径
        max_description_length: 描述最大长度

    Returns:
        任务清单列表
    """
    # 读取现有缓存
    existing = load_cache(cache_file)

    tasks = []
    for f in files_info:
        # 只处理.md文件
        if not f.path.endswith(".md"):
            continue

        # 检查是否需要生成描述
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


def load_cache(cache_file: str) -> Dict[str, Any]:
    """加载描述缓存"""
    if os.path.exists(cache_file):
        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def write_tasks_json(
    tasks: List[Dict[str, Any]], output_file: str = ".llm-tasks.json"
) -> None:
    """输出任务清单供AI平台处理"""
    if not tasks:
        # 如果没有任务，删除任务文件（避免残留）
        if os.path.exists(output_file):
            os.remove(output_file)
        return

    task_data = {
        "version": "2.1",
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "task_count": len(tasks),
        "tasks": tasks,
    }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(task_data, f, ensure_ascii=False, indent=2)

    print(f"📋 已生成 {len(tasks)} 个描述任务 → {output_file}")


def wait_for_ai_completion(
    timeout: int = 60, cache_file: str = ".file-descriptions.json"
) -> bool:
    """
    等待AI完成描述生成（轮询检测）

    Args:
        timeout: 超时时间（秒）
        cache_file: 缓存文件路径

    Returns:
        True: AI完成描述生成
        False: 超时
    """
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
