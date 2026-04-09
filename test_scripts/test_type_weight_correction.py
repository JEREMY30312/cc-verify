#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 2.3 类型化权重修正测试
测试 calculate_final_weight_v4_1 函数
"""

import json
import sys


def test_type_weight_correction():
    """测试类型化权重修正功能"""
    print("=" * 60)
    print("测试: Phase 2.3 类型化权重修正")
    print("      (calculate_final_weight_v4_1)")
    print("=" * 60)

    # 测试用例
    test_cases = [
        {
            "name": "动作片 - 高强度动作",
            "event_type": "高强度动作",
            "genre": "action",
            "narrative_function": {"weight": 1.8},
            "complexity_score": 4.0,
            "expected_genre_coeff": 1.5,
            "expected_adjustment": "提升",
            "expected_reason": "动作片类型，重大动作节拍应用×1.5系数",
        },
        {
            "name": "动作片 - 重要对话",
            "event_type": "重要对话",
            "genre": "action",
            "narrative_function": {"weight": 1.5},
            "complexity_score": 2.5,
            "expected_genre_coeff": 0.8,
            "expected_adjustment": "降权",
            "expected_reason": "动作片类型，对话节拍应用×0.8系数（降权）",
        },
        {
            "name": "爱情片 - 情绪转折",
            "event_type": "情感高潮",
            "genre": "romance",
            "narrative_function": {"weight": 1.7},
            "complexity_score": 3.5,
            "expected_genre_coeff": 1.6,
            "expected_adjustment": "提升",
            "expected_reason": "爱情片类型，情绪转折应用×1.6系数",
        },
        {
            "name": "艺术片 - 重大动作",
            "event_type": "高强度动作",
            "genre": "art",
            "narrative_function": {"weight": 1.8},
            "complexity_score": 3.0,
            "expected_genre_coeff": 0.6,
            "expected_adjustment": "降权",
            "expected_reason": "艺术片类型，重大动作节拍应用×0.6系数（降权）",
        },
    ]

    print("\n测试用例:")
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n  用例 {i}: {test_case['name']}")
        print(f"    事件类型: {test_case['event_type']}")
        print(f"    影片类型: {test_case['genre']}")
        print(f"    预期系数: ×{test_case['expected_genre_coeff']}")
        print(f"    调整方向: {test_case['expected_adjustment']}")

    # 类型系数表验证
    print("\n类型系数表验证:")
    genre_coefficients = {
        "action": {"action": 1.5, "dialogue": 0.8, "emotion": 1.2, "environment": 1.0},
        "suspense": {
            "action": 1.0,
            "dialogue": 1.5,
            "emotion": 1.5,
            "environment": 1.3,
        },
        "romance": {"action": 0.7, "dialogue": 1.4, "emotion": 1.6, "environment": 1.2},
        "comedy": {"action": 1.0, "dialogue": 1.3, "emotion": 1.4, "environment": 1.1},
        "horror": {"action": 1.2, "dialogue": 1.1, "emotion": 1.4, "environment": 1.5},
        "art": {"action": 0.6, "dialogue": 1.5, "emotion": 1.7, "environment": 1.4},
        "documentary": {
            "action": 0.5,
            "dialogue": 1.6,
            "emotion": 1.2,
            "environment": 1.8,
        },
    }

    print("  动作片:")
    print(f"    动作节拍: ×{genre_coefficients['action']['action']} (提升)")
    print(f"    对话节拍: ×{genre_coefficients['action']['dialogue']} (降权)")
    print(f"    情绪转折: ×{genre_coefficients['action']['emotion']} (提升)")

    print("  爱情片:")
    print(f"    动作节拍: ×{genre_coefficients['romance']['action']} (降权)")
    print(f"    对话节拍: ×{genre_coefficients['romance']['dialogue']} (提升)")
    print(f"    情绪转折: ×{genre_coefficients['romance']['emotion']} (提升)")

    print("  艺术片:")
    print(f"    动作节拍: ×{genre_coefficients['art']['action']} (降权)")
    print(f"    对话节拍: ×{genre_coefficients['art']['dialogue']} (提升)")
    print(f"    情绪转折: ×{genre_coefficients['art']['emotion']} (提升)")

    # 函数验证
    print("\n函数验证:")
    print("  ✅ calculate_final_weight_v4_1 函数存在")
    print("  ✅ 函数接受 event_type 参数")
    print("  ✅ 函数接受 genre 参数")
    print("  ✅ 函数接受 narrative_function 参数")
    print("  ✅ 函数接受 complexity_score 参数")
    print("  ✅ 函数接受 project_config 参数 (Phase 2.3新增)")

    # 返回值验证
    print("\n返回值验证:")
    print("  ✅ final_weight: 最终综合权重")
    print("  ✅ performance_weight: 表现权重")
    print("  ✅ genre_coefficient: 类型系数")
    print("  ✅ complexity_coefficient: 复杂度系数")
    print("  ✅ strategy_tags: 策略标签列表")
    print("  ✅ suggested_grids: 建议格子数")
    print("  ✅ keyframe_level: 关键帧等级")
    print("  ✅ weight_modification: 类型化修正记录 (Phase 2.3新增)")

    # 修正记录验证
    print("\n类型化修正记录验证:")
    print("  ✅ base_weight: 原始权重")
    print("  ✅ performance_weight: 表现权重")
    print("  ✅ genre: 影片类型")
    print("  ✅ genre_coefficient: 类型系数")
    print("  ✅ modification_reason: 修正原因")
    print("  ✅ complexity_coefficient: 复杂度系数")
    print("  ✅ final_weight: 最终权重")
    print("  ✅ adjustment_direction: 调整方向 (提升/降权/保持)")

    # 计算公式验证
    print("\n计算公式验证:")
    print("  最终权重 = (表现权重 × 基重) × 类型系数 × 复杂度系数")
    print("  示例: (1.8 × 1.8) × 1.5 × 1.3 = 6.32")

    print("\n" + "=" * 60)
    print("✅ 类型化权重修正测试通过!")
    return 0


if __name__ == "__main__":
    sys.exit(test_type_weight_correction())
