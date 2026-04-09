"""
> **Description:** 描述缓存管理器 - 读写.file-descriptions.json，清理已删除文件

缓存格式：
{
  "file/path.md": {
    "description": "简短描述",
    "mtime": 1234567890.0,
    "generated_at": "2025-01-01 12:00:00"
  }
}
"""

import os
import json
import time
from typing import Dict, Any, List, Optional


def load_cache(cache_file: str = ".file-descriptions.json") -> Dict[str, Any]:
    """
    加载描述缓存

    Args:
        cache_file: 缓存文件路径

    Returns:
        描述缓存字典
    """
    if os.path.exists(cache_file):
        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def save_cache(
    descriptions: Dict[str, Any], cache_file: str = ".file-descriptions.json"
) -> None:
    """
    保存描述缓存

    Args:
        descriptions: 描述缓存字典
        cache_file: 缓存文件路径
    """
    with open(cache_file, "w", encoding="utf-8") as f:
        json.dump(descriptions, f, ensure_ascii=False, indent=2)


def clean_cache(cache: Dict[str, Any], current_files: List[str]) -> Dict[str, Any]:
    """
    清理已删除文件的缓存

    Args:
        cache: 当前缓存
        current_files: 当前存在的文件列表

    Returns:
        清理后的缓存
    """
    current_set = set(current_files)
    cleaned = {k: v for k, v in cache.items() if k in current_set}

    removed_count = len(cache) - len(cleaned)
    if removed_count > 0:
        print(f"🧹 清理了 {removed_count} 个已删除文件的缓存")

    return cleaned


def get_description(cache: Dict[str, Any], file_path: str) -> Optional[str]:
    """
    从缓存获取文件描述

    Args:
        cache: 描述缓存
        file_path: 文件路径

    Returns:
        描述字符串，如果不存在返回None
    """
    if file_path in cache:
        return cache[file_path].get("description")
    return None


def update_description(
    cache: Dict[str, Any],
    file_path: str,
    description: str,
    mtime: float,
) -> None:
    """
    更新文件描述缓存

    Args:
        cache: 描述缓存
        file_path: 文件路径
        description: 描述内容
        mtime: 文件修改时间
    """
    cache[file_path] = {
        "description": description,
        "mtime": mtime,
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    }


def merge_ai_descriptions(
    cache: Dict[str, Any],
    ai_descriptions: Dict[str, str],
    files_info: List[Any],
) -> Dict[str, Any]:
    """
    合并AI生成的描述到缓存

    Args:
        cache: 当前缓存
        ai_descriptions: AI生成的新描述 {file_path: description}
        files_info: 文件信息列表（用于获取mtime）

    Returns:
        更新后的缓存
    """
    # 创建文件路径到mtime的映射
    file_mtimes = {f.path: f.mtime for f in files_info}

    for file_path, description in ai_descriptions.items():
        if file_path in file_mtimes:
            update_description(
                cache,
                file_path,
                description,
                file_mtimes[file_path],
            )

    return cache
