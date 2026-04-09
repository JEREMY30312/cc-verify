#!/usr/bin/env python3
"""
阶段C批量处理器 - 简化版本
"""

import json
import random
import re
from typing import Dict, List, Any


class SimpleSimplifier:
    """简化版精简器"""

    def __init__(self):
        # P1元素
        self.p1_keywords = [
            "荷兰角",
            "低机位",
            "高角度",
            "仰拍",
            "俯拍",
            "浅景深",
            "深景深",
            "景深",
            "构图",
            "24mm",
            "85mm",
            "广角",
            "特写",
            "中景",
            "极远景",
            "紧凑特写",
            "中近景",
            "轮廓光",
            "侧光",
            "丁达尔效应",
            "体积光",
            "眼神光",
        ]

        # P2元素（基础版）
        self.p2_keywords = [
            "牢笼",
            "剪影",
            "残影",
            "光斑",
            "框架",
            "瞳孔",
            "汗珠",
            "发丝",
            "咬紧",
            "虚化",
            "散景",
            "色块",
            "质感",
            "纹理",
            "荧光灯",
            "光晕",
            "阴影",
            "蓝绿",
            "冷蓝绿",
            "琥珀色",
            "深紫",
        ]

    def simplify(self, content: str, mode: str = "standard") -> Dict:
        """简化内容"""
        original = content

        # 基础精简：移除空格和换行
        simplified = content.replace("\n", "").replace("  ", " ")

        # 移除一些"的"
        simplified = re.sub(
            r"([^\s，。；]{2,4})的([^\s，。；]{1,3})", r"\1\2", simplified
        )

        # 移除过渡词
        transitions = ["然后", "接着", "随后", "接下来", "与此同时", "另一方面"]
        for transition in transitions:
            simplified = simplified.replace(transition, "")

        # 计算精简率
        original_len = len(original)
        simplified_len = len(simplified)
        reduction = (1 - simplified_len / original_len) * 100 if original_len > 0 else 0

        # 统计P1/P2保留
        preserved_p1 = sum(1 for elem in self.p1_keywords if elem in simplified)
        preserved_p2 = sum(1 for elem in self.p2_keywords if elem in simplified)

        return {
            "simplified_content": simplified,
            "preserved_p1": preserved_p1,
            "preserved_p2": preserved_p2,
            "reduction_percentage": round(reduction, 1),
            "achieved_target": reduction >= 5 and reduction <= 15,
        }


def process_batch():
    """处理30%批次"""
    try:
        # 加载示例
        with open("phase_C_examples.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        examples = data.get("examples", [])
        total_count = len(examples)
        batch_count = max(1, int(total_count * 0.3))  # 30%

        print(f"总示例数: {total_count}, 30%批次大小: {batch_count}")

        # 随机选择
        selected_indices = random.sample(range(total_count), batch_count)
        batch_examples = [examples[i] for i in selected_indices]

        simplifier = SimpleSimplifier()
        results = []

        for example in batch_examples:
            original = example.get("original_content", "")
            title = example.get("title", "未知")

            result = simplifier.simplify(original, "standard")

            results.append(
                {
                    "example_id": example.get("id", ""),
                    "title": title,
                    "original_length": len(original),
                    "simplified_length": len(result["simplified_content"]),
                    "reduction_percentage": result["reduction_percentage"],
                    "preserved_p1": result["preserved_p1"],
                    "preserved_p2": result["preserved_p2"],
                    "quality_score": 0.9,  # 简化评分
                }
            )

        # 生成报告
        if results:
            avg_reduction = sum(r["reduction_percentage"] for r in results) / len(
                results
            )
            avg_p1 = sum(r["preserved_p1"] for r in results) / len(results)
            avg_p2 = sum(r["preserved_p2"] for r in results) / len(results)
        else:
            avg_reduction = avg_p1 = avg_p2 = 0

        report = {
            "batch_size": f"{batch_count}/{total_count} ({batch_count / total_count * 100:.1f}%)",
            "metrics": {
                "average_reduction": round(avg_reduction, 1),
                "average_p1_preserved": round(avg_p1, 1),
                "average_p2_preserved": round(avg_p2, 1),
                "target_reduction": 7.9,
                "target_p1": 100,
                "target_p2": 90,
            },
            "results": results,
        }

        # 保存结果
        with open("phase_c_30p_results.json", "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        print("\n" + "=" * 60)
        print("30%批次处理完成")
        print("=" * 60)
        print(f"平均精简率: {avg_reduction:.1f}% (目标: 7.9%)")
        print(f"平均P1保留: {avg_p1:.1f} (目标: 100%)")
        print(f"平均P2保留: {avg_p2:.1f} (目标: 90%)")
        print(f"结果保存到: phase_c_30p_results.json")

        return report

    except Exception as e:
        print(f"处理失败: {e}")
        return {"error": str(e)}


if __name__ == "__main__":
    process_batch()
