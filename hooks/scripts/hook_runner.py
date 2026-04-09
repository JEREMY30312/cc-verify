#!/usr/bin/env python3
"""
Git钩子统一执行器
所有钩子调用此脚本，根据参数执行对应逻辑。
"""

import json
import os
import subprocess
import sys

DEFAULT_CONFIG = {
    "time_range_hours": 168,
    "max_description_length": 20,
    "ignore_list": [".git", "node_modules", "__pycache__", ".DS_Store"],
    "collapse_folders": ["backups", "版本汇总"],
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

HOOK_CONFIG_MAP = {
    "post-commit": "post_commit_update",
    "post-merge": "post_merge_update",
    "post-checkout": "post_checkout_update",
}


def load_config():
    """加载配置文件"""
    config = DEFAULT_CONFIG.copy()
    config_file = ".project-map-config.json"
    try:
        with open(config_file, "r") as f:
            user_config = json.load(f)
            for key, value in user_config.items():
                if key in config:
                    if isinstance(value, dict) and isinstance(config[key], dict):
                        config[key].update(value)
                    else:
                        config[key] = value
    except FileNotFoundError:
        pass
    except json.JSONDecodeError:
        print("⚠️  配置文件格式错误，使用默认配置")
    return config


def run_hook(hook_name):
    """执行指定钩子"""
    config = load_config()
    config_key = HOOK_CONFIG_MAP.get(hook_name)

    if not config_key:
        print(f"❌ 未知钩子类型: {hook_name}")
        return

    if not config["hooks"].get(config_key, False):
        return

    hook_messages = {
        "post-commit": "🗺️  提交后更新项目地图...",
        "post-merge": "🗺️  合并后更新项目地图...",
        "post-checkout": "🗺️  切换分支后更新项目地图...",
    }

    print(hook_messages.get(hook_name, "🗺️  更新项目地图..."))

    try:
        result = subprocess.run(
            [sys.executable, "generate_map.py", "--silent"],
            capture_output=True,
            text=True,
            timeout=60,
        )

        if result.returncode == 0:
            print("✅ 项目地图已更新")
            if config["hooks"].get("auto_add_to_git", False):
                map_file = config["output"]["map_file"]
                fingerprint_file = config["output"]["fingerprint_file"]
                subprocess.run(
                    ["git", "add", map_file, fingerprint_file],
                    capture_output=True,
                    timeout=10,
                )
                print("✅ 已添加到Git暂存区")
        else:
            print(f"❌ 更新失败: {result.stderr}")
    except subprocess.TimeoutExpired:
        print("❌ 更新超时（60秒）")
    except Exception as e:
        print(f"❌ 钩子执行失败: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 hook_runner.py <hook-name>")
        print("可用钩子: post-commit, post-merge, post-checkout")
        sys.exit(1)

    run_hook(sys.argv[1])
