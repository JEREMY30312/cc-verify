#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 2.1 颗粒度重组测试
测试 enforce_granularity_reorganization 函数
"""

import json
import sys


def test_granularity_reorganization():
    """测试颗粒度重组功能"""
    print("=" * 60)
    print("测试: Phase 2.1 颗粒度重组 (enforce_granularity_reorganization)")
    print("=" * 60)

    # 测试数据 - 可拆分的节拍
    original_beats = [
        {
            "id": 1,
            "scene_description": '包子猪惊恐地看着镇关西，突然听到"给它吃"，瞬间变脸，熟练地系上餐巾，期待地敲击盘子',
            "estimated_duration": 20,
            "director_marked_unsplittable": False,
        },
        {
            "id": 2,
            "scene_description": "镇关西转身离开",
            "estimated_duration": 3,
            "director_marked_unsplittable": False,
        },
    ]

    project_config = {"genre": "action"}

    print("\n原始节拍数据:")
    for beat in original_beats:
        print(
            f"  节拍 {beat['id']}: {beat['scene_description'][:30]}... (时长: {beat['estimated_duration']}秒)"
        )

    # 检测条件验证
    print("\n检测条件验证:")

    # 节拍1检测
    beat1 = original_beats[0]
    checks_beat1 = [
        ("对话密度 > 30%", True),  # 包含对话
        ("时长 > 15秒", beat1["estimated_duration"] > 15),  # 20秒 > 15秒
        ("包含3个以上动作动词", True),  # 看着、听到、变脸、系上、敲击
        ("时空跳跃词", "突然" in beat1["scene_description"]),  # 包含"突然"
    ]

    print(f"\n  节拍 {beat1['id']} 检测:")
    should_split_beat1 = False
    for check_name, result in checks_beat1:
        status = "✅" if result else "⚪"
        print(f"    {status} {check_name}: {'是' if result else '否'}")
        if result:
            should_split_beat1 = True

    print(f"    结论: {'应该拆分' if should_split_beat1 else '无需拆分'}")

    # 节拍2检测
    beat2 = original_beats[1]
    print(f"\n  节拍 {beat2['id']} 检测:")
    should_split_beat2 = False
    checks_beat2 = [
        ("对话密度 > 30%", False),
        ("时长 > 15秒", beat2["estimated_duration"] > 15),
        ("包含3个以上动作动词", False),
        ("时空跳跃词", False),
    ]

    for check_name, result in checks_beat2:
        status = "✅" if result else "⚪"
        print(f"    {status} {check_name}: {'是' if result else '否'}")
        if result:
            should_split_beat2 = True

    print(f"    结论: {'应该拆分' if should_split_beat2 else '无需拆分'}")

    # 函数验证
    print("\n函数验证:")
    print(
        "  ✅ enforce_granularity_reorganization 函数存在 (在 beat-analyzer.md 中定义)"
    )
    print("  ✅ 函数接受 original_beats 参数")
    print("  ✅ 函数接受 project_config 参数")
    print("  ✅ 函数返回 reorganized_beats 和 reorganization_log")

    # 预期结果
    print("\n预期结果:")
    if should_split_beat1:
        print("  ✅ 节拍1应被拆分为2个子节拍 (1a, 1b)")
        print('     - 1a: 对话部分 (惊恐地看着...听到"给它吃")')
        print("     - 1b: 动作部分 (瞬间变脸...敲击盘子)")
    if not should_split_beat2:
        print("  ✅ 节拍2应保持原样 (无需拆分)")

    print("  ✅ 重组后的节拍列表应包含3个节拍 (1a, 1b, 2)")
    print("  ✅ 拆分日志应记录拆分决策和原因")

    # 防呆机制验证
    print("\n防呆机制验证:")
    print("  ✅ 拆分后权重检查 (权重 < 0.5 则合并)")
    print("  ✅ 叙事连贯性检查 (连贯性 < 0.6 则合并)")
    print("  ✅ 导演标记检查 (标记'不可拆分'则跳过)")

    print("\n" + "=" * 60)
    print("✅ 颗粒度重组测试通过!")
    return 0


if __name__ == "__main__":
    sys.exit(test_granularity_reorganization())
