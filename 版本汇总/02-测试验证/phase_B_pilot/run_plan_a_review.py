#!/usr/bin/env python3
"""
方案A专业评审执行脚本
"""

import json
import sys
from pathlib import Path

# 添加路径
sys.path.insert(0, "/Users/achi/Desktop/JEREMY/NEW/phase_B_pilot")


def main():
    print("=" * 80)
    print("方案A专业评审 - 调整精简目标到20-25%")
    print("=" * 80)

    # 导入必要的模块
    exec(
        open(
            "/Users/achi/Desktop/JEREMY/NEW/phase_B_pilot/02_professional_review_system.py"
        ).read()
    )

    # 现在使用 ProfessionalReviewSystem
    print("\n加载高效精简V2结果...")
    result_path = Path(
        "/Users/achi/Desktop/JEREMY/NEW/phase_B_pilot/results/efficient_simplification_results.json"
    )

    with open(result_path, "r", encoding="utf-8") as f:
        results = json.load(f)

    # 准备评审内容
    pilot_examples = [
        {
            "id": 6,
            "title": "世界观建立（奇幻/科幻）",
            "original": """极远景，黄昏时分的浮空城市。巨大石质平台在云间漂浮，由不可思议的长吊桥相连。瀑布从边缘倾泻入下方虚空。数千扇小窗散发温暖的琥珀色光芒，落日将云层染成深紫与燃烧的橙。前景，一个旅人的剪影站在悬崖边缘仰望，渺小的身影衬托城市的巨大。体积光穿过云层缝隙。惊奇与敬畏，不可能世界中的冒险。""",
        },
        {
            "id": 1,
            "title": "紧张对峙（剧情片）",
            "original": """中景，昏暗的地下停车场。两个男人面对面站立。穿皱巴巴西装的男人身体前倾，咬紧下巴，姿态充满攻击性；皮夹克男人双臂交叉，表情难以捉摸。头顶荧光灯闪烁，刺眼的光线将两人的脸分割成明暗两半。身后混凝土柱子形成牢笼般的框架。略微仰拍，两人都显得气势逼人。冷蓝绿色调。一触即发，暴力随时可能爆发。""",
        },
        {
            "id": 2,
            "title": "温馨回忆（剧情片）",
            "original": """特写，年轻女性的面容。她望向雨水划过的窗户，眼中闪着未落的泪光，嘴角却浮现一丝温柔的微笑。手中握着一张老照片，手指轻轻描摹着边缘。黄金时段的柔光透过窗户，温暖她的面容，在凌乱的发丝上晕出光晕。背景是温馨的客厅和书架，85mm镜头虚化成柔和的色块。苦涩而温柔，私密的回忆时刻。""",
        },
    ]

    # 创建评审系统
    review_system = globals()["ProfessionalReviewSystem"]()

    print("执行专业评审...")

    all_results = []

    for example in pilot_examples:
        # 找到对应的结果
        example_result = None
        for item in results["examples"]:
            if item["example_id"] == example["id"]:
                example_result = item
                break

        if not example_result:
            continue

        print(f"\n--- {example['title']} ---")

        # 对三种版本进行评审
        variants = {
            "original": example["original"],
            "standard": example_result["modes"]["standard"]["content"],
            "fast": example_result["modes"]["fast"]["content"],
        }

        example_review = {
            "id": example["id"],
            "title": example["title"],
            "variants": {},
            "stats": example_result["modes"]["standard"],
        }

        for variant_name, content in variants.items():
            # 执行三种评审
            director_score = review_system.score_content(content, "director")
            enthusiast_score = review_system.score_content(content, "enthusiast")
            viewer_score = review_system.score_content(content, "viewer")

            # 计算平均分
            avg_score = (
                director_score["total_score"]
                + enthusiast_score["total_score"]
                + viewer_score["total_score"]
            ) / 3

            print(f"{variant_name}: {avg_score:.2f}/5.0")

            example_review["variants"][variant_name] = {
                "average_score": round(avg_score, 2),
                "director": director_score["total_score"],
                "enthusiast": enthusiast_score["total_score"],
                "viewer": viewer_score["total_score"],
            }

        all_results.append(example_review)

    # 分析结果
    print("\n" + "=" * 80)
    print("结果分析")
    print("=" * 80)

    avg_original = sum(
        r["variants"]["original"]["average_score"] for r in all_results
    ) / len(all_results)
    avg_standard = sum(
        r["variants"]["standard"]["average_score"] for r in all_results
    ) / len(all_results)
    avg_fast = sum(r["variants"]["fast"]["average_score"] for r in all_results) / len(
        all_results
    )

    quality_drop_std = (
        ((avg_original - avg_standard) / avg_original) * 100 if avg_original > 0 else 0
    )

    print(f"\n平均质量评分:")
    print(f"  原始: {avg_original:.2f}/5.0")
    print(f"  标准: {avg_standard:.2f}/5.0")
    print(f"  快速: {avg_fast:.2f}/5.0")

    print(f"\n质量下降:")
    print(f"  原始 vs 标准: {quality_drop_std:.1f}%")

    if quality_drop_std <= 10:
        print(f"\n✅ 方案A达标：质量下降 ≤ 10%")
        print(f"\n建议：进入阶段C大规模实施")
    else:
        print(f"\n❌ 方案A未达标：质量下降 {quality_drop_std:.1f}% > 10%")
        print(f"需要进一步优化")

    # 保存结果
    output_path = Path(
        "/Users/achi/Desktop/JEREMY/NEW/phase_B_pilot/results/plan_a_final_review.json"
    )
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "summary": {
                    "average_original": round(avg_original, 2),
                    "average_standard": round(avg_standard, 2),
                    "average_fast": round(avg_fast, 2),
                    "quality_drop": round(quality_drop_std, 1),
                    "achieved_target": quality_drop_std <= 10,
                },
                "examples": all_results,
            },
            f,
            ensure_ascii=False,
            indent=2,
        )

    print(f"\n结果已保存: {output_path}")


if __name__ == "__main__":
    main()
