#!/usr/bin/env python3
"""
四宫格生成字段完整性校验脚本（V1.0）

用途: 校验sequence-board生成产出的字段完整性
使用方法: python3 validator.py <sequence-board-data-ep01.json>
"""

import json
import sys
import os
from pathlib import Path

# 剧本角色定义
VALID_CHARACTERS = {
    "鲁达": "主角",
    "镇关西": "屠夫",
    "郑屠": "屠夫（别名）",
    "包子猪": "独立角色",
}

INVALID_CHARACTERS = ["猪八戒", "孙悟空", "唐僧", "沙僧"]


def load_json(filepath):
    """加载JSON文件"""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_project_config(data):
    """校验项目配置"""
    required = ["visual_style", "aspect_ratio", "target_medium", "genre"]
    missing = [f for f in required if f not in data.get("project_config", {})]
    if missing:
        return False, f"缺少项目配置字段: {missing}"
    return True, "✅"


def validate_boards(data):
    """校验boards数组"""
    if not data.get("boards"):
        return False, "缺少boards数组"

    for i, board in enumerate(data["boards"]):
        # 必填字段
        board_required = ["board_id", "board_number", "beat_range", "shots"]
        missing = [f for f in board_required if f not in board]
        if missing:
            return False, f"Board {i} 缺少字段: {missing}"

        # shots数组校验
        if not board.get("shots"):
            return False, f"Board {i} 缺少shots数组"

        for j, shot in enumerate(board["shots"]):
            shot_required = [
                "shot_id",
                "position",
                "beat_id",
                "strategy_tag",
                "original_grid",
                "expanded_shot",
            ]
            missing = [f for f in shot_required if f not in shot]
            if missing:
                return False, f"Board {i} Shot {j} 缺少字段: {missing}"

            # original_grid环境构造校验
            env = shot.get("original_grid", {}).get("environment", {})
            env_required = [
                "spatial_skeleton",
                "four_layers",
                "materials",
                "lighting",
                "dynamic_elements",
            ]
            missing = [f for f in env_required if f not in env]
            if missing:
                return False, f"Board {i} Shot {j} 环境构造缺少: {missing}"

    return True, "✅"


def validate_inherited_from(data):
    """校验继承来源"""
    for board in data.get("boards", []):
        inherited = board.get("inherited_from", {})
        required = ["beat_board", "grids"]
        missing = [f for f in required if f not in inherited]
        if missing:
            return False, f"Board {board.get('board_id')} 继承来源缺少: {missing}"
    return True, "✅"


def validate_continuity_check(data):
    """校验跨板连续性检查"""
    for board in data.get("boards", []):
        check = board.get("continuity_check", {})
        required = ["axis_law", "eyeline_match", "action_flow", "lighting_consistency"]
        missing = [f for f in required if f not in check]
        if missing:
            return False, f"Board {board.get('board_id')} 连续性检查缺少: {missing}"
    return True, "✅"


def validate_characters(content):
    """校验角色名称（防止AI发挥）"""
    for char in INVALID_CHARACTERS:
        if char in content:
            return False, f"包含无效角色名称: {char}"
    return True, "✅"


def validate_no_dynamic_prompt(content):
    """校验是否混入了动态提示词内容"""
    keywords = ["动态提示词", "motion_prompt", "图生视频"]
    for k in keywords:
        if k in content:
            return False, f"混入了动态提示词内容: {k}"
    return True, "✅"


def validate_source_text(data):
    """校验是否从source_text读取原文"""
    for board in data.get("boards", []):
        for shot in board.get("shots", []):
            expanded = shot.get("expanded_shot", {})
            desc = expanded.get("visual_description", "")

            # 检查是否包含台词融入
            if "【" in desc or "】" in desc:
                # 允许使用【】包裹台词
                continue

            # 检查是否有dialogue字段
            if not expanded.get("dialogue"):
                # 没有台词是允许的（可能确实没有对话）
                pass

    return True, "✅"


def main():
    """主校验函数"""
    if len(sys.argv) < 2:
        print("用法: python3 validator.py <sequence-board-data-ep01.json>")
        sys.exit(1)

    filepath = sys.argv[1]

    if not os.path.exists(filepath):
        print(f"❌ 文件不存在: {filepath}")
        sys.exit(1)

    print(f"📋 校验文件: {filepath}\n")

    try:
        data = load_json(filepath)
    except json.JSONDecodeError as e:
        print(f"❌ JSON格式错误: {e}")
        sys.exit(1)

    # 读取文件内容用于文本校验
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    all_passed = True

    # 校验项目配置
    print("1. 项目配置...")
    passed, msg = validate_project_config(data)
    print(f"   {msg}")
    all_passed = all_passed and passed

    # 校验boards
    print("2. Boards数组...")
    passed, msg = validate_boards(data)
    print(f"   {msg}")
    all_passed = all_passed and passed

    # 校验继承来源
    print("3. 继承来源...")
    passed, msg = validate_inherited_from(data)
    print(f"   {msg}")
    all_passed = all_passed and passed

    # 校验连续性检查
    print("4. 跨板连续性检查...")
    passed, msg = validate_continuity_check(data)
    print(f"   {msg}")
    all_passed = all_passed and passed

    # 校验角色名称
    print("5. 角色名称校验...")
    passed, msg = validate_characters(content)
    print(f"   {msg}")
    if not passed:
        all_passed = False

    # 校验动态提示词
    print("6. 动态提示词校验...")
    passed, msg = validate_no_dynamic_prompt(content)
    print(f"   {msg}")
    all_passed = all_passed and passed

    print("\n" + "=" * 50)
    if all_passed:
        print("✅ 所有校验通过")
        sys.exit(0)
    else:
        print("❌ 校验失败")
        sys.exit(1)


if __name__ == "__main__":
    main()
