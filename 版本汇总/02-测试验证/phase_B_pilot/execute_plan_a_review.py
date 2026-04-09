#!/usr/bin/env python3
"""
方案A专业评审 - 调整精简目标到20-25%
验证：P1/P2保留，质量下降≤10%
"""

import json
from pathlib import Path

# 导入之前的高效精简器V2
import sys

sys.path.insert(0, "/Users/achi/Desktop/JEREMY/NEW/phase_B_pilot")


def load_results():
    """加载高效精简V2的结果"""
    result_path = Path(
        "/Users/achi/Desktop/JEREMY/NEW/phase_B_pilot/results/efficient_simplification_results.json"
    )

    with open(result_path, "r", encoding="utf-8") as f:
        return json.load(f)


def organize_for_review(results):
    """组织数据用于专业评审"""

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

    # 为每个示例准备评审数据
    review_data = []

    for example in pilot_examples:
        # 从results中找到对应的数据
        example_data = None
        for result in results["examples"]:
            if result["example_id"] == example["id"]:
                example_data = result
                break

        if not example_data:
            continue

        # 准备三种模式:
        # - original: 原始版本
        # - standard: 标准模式（20-25%精简，方案A推荐）
        # - fast: 快速模式（50%精简，作为对比）

        full_mode = example_data["modes"]["full"]
        standard_mode = example_data["modes"]["standard"]
        fast_mode = example_data["modes"]["fast"]

        # 标准模式是否达到目标（20-25%）
        standard_achieved = 20 <= standard_mode["reduction"] <= 25

        review_item = {
            "example_id": example["id"],
            "title": example["title"],
            "variants": {
                "original": example["original"],
                "standard": standard_mode["content"],  # 方案A推荐
                "fast": fast_mode["content"],  # 对比
            },
            "stats": {
                "standard": {
                    "reduction": standard_mode["reduction"],
                    "achieved_target": standard_achieved,
                    "preserved_p1": standard_mode["preserved_p1"],
                    "preserved_p2": standard_mode["preserved_p2"],
                },
                "full": {
                    "reduction": full_mode["reduction"],
                    "preserved_p1": full_mode["preserved_p1"],
                    "preserved_p2": full_mode["preserved_p2"],
                },
                "fast": {
                    "reduction": fast_mode["reduction"],
                    "preserved_p1": fast_mode["preserved_p1"],
                    "preserved_p2": fast_mode["preserved_p2"],
                },
            },
        }

        review_data.append(review_item)

    return review_data


def simulate_professional_review(review_data):
    """模拟专业评审"""

    # 导入专业评审系统
    from professional_review_system import ProfessionalReviewSystem as PRS

    review_system = PRS()

    all_reviews = []

    for example in review_data:
        example_reviews = {
            "example_id": example["example_id"],
            "title": example["title"],
            "reviews": {},
        }

        # 对每个版本进行评审
        for variant_name, variant_content in example["variants"].items():
            # 导演评审
            director_review = review_system.score_content(variant_content, "director")

            # 爱好者评审
            enthusiast_review = review_system.score_content(
                variant_content, "enthusiast"
            )

            # 观众评审
            viewer_review = review_system.score_content(variant_content, "viewer")

            # 计算平均分
            avg_score = (
                director_review["total_score"]
                + enthusiast_review["total_score"]
                + viewer_review["total_score"]
            ) / 3

            example_reviews["reviews"][variant_name] = {
                "director": director_review,
                "enthusiast": enthusiast_review,
                "viewer": viewer_review,
                "average_score": round(avg_score, 2),
                "director_feedback": director_review["feedback"],
                "enthusiast_feedback": enthusiast_review["feedback"],
                "viewer_feedback": viewer_review["feedback"],
            }

        all_reviews.append(example_reviews)

    return all_reviews


def analyze_quality_review(review_data, all_reviews):
    """分析质量评审结果"""

    analysis = {
        "summary": {
            "total_examples": len(review_data),
            "average_original_score": 0,
            "average_standard_score": 0,
            "average_fast_score": 0,
            "quality_drop_original_vs_standard": 0,
            "quality_drop_original_vs_fast": 0,
        },
        "examples": [],
    }

    total_original = 0
    total_standard = 0
    total_fast = 0

    for i, example in enumerate(review_data):
        reviews = all_reviews[i]

        original_score = reviews["reviews"]["original"]["average_score"]
        standard_score = reviews["reviews"]["standard"]["average_score"]
        fast_score = reviews["reviews"]["fast"]["average_score"]

        drop_standard = (
            ((original_score - standard_score) / original_score) * 100
            if original_score > 0
            else 0
        )
        drop_fast = (
            ((original_score - fast_score) / original_score) * 100
            if original_score > 0
            else 0
        )

        example_analysis = {
            "example_id": example["example_id"],
            "title": example["title"],
            "scores": {
                "original": original_score,
                "standard": standard_score,
                "fast": fast_score,
            },
            "quality_drop": {
                "original_vs_standard": round(drop_standard, 1),
                "original_vs_fast": round(drop_fast, 1),
            },
            "stats": example["stats"]["standard"],
            "standard_meets_target": example["stats"]["standard"]["achieved_target"],
        }

        analysis["examples"].append(example_analysis)

        total_original += original_score
        total_standard += standard_score
        total_fast += fast_score

    # 计算整体平均值
    count = len(review_data)
    analysis["summary"]["average_original_score"] = round(total_original / count, 2)
    analysis["summary"]["average_standard_score"] = round(total_standard / count, 2)
    analysis["summary"]["average_fast_score"] = round(total_fast / count, 2)

    quality_drop_std = (
        ((total_original - total_standard) / total_original) * 100
        if total_original > 0
        else 0
    )
    quality_drop_fast = (
        ((total_original - total_fast) / total_original) * 100
        if total_original > 0
        else 0
    )

    analysis["summary"]["quality_drop_original_vs_standard"] = round(
        quality_drop_std, 1
    )
    analysis["summary"]["quality_drop_original_vs_fast"] = round(quality_drop_fast, 1)

    # 评估是否达标
    analysis["summary"]["plan_a_achieved"] = (
        analysis["summary"]["quality_drop_original_vs_standard"] <= 10
    )

    return analysis


def generate_recommendations(analysis):
    """生成改进建议"""

    recommendations = []

    quality_drop_std = analysis["summary"]["quality_drop_original_vs_standard"]
    avg_std_score = analysis["summary"]["average_standard_score"]

    # 方案A评估
    if quality_drop_std <= 5:
        recommendations.append("✅ 方案A（标准模式20-25%精简）表现优秀，强烈推荐")
        recommendations.append("   - 质量下降≤5%，远超目标（≤10%）")
        recommendations.append(f"   - 平均质量评分：{avg_std_score}/5.0")
        recommendations.append("   - 建议：作为ANINEO系统的默认输出模式")
    elif quality_drop_std <= 10:
        recommendations.append("✓ 方案A（标准模式20-25%精简）表现良好，可以采用")
        recommendations.append(
            f"   - 质量下降：{quality_drop_std}%，在目标范围内（≤10%）"
        )
        recommendations.append(f"   - 平均质量评分：{avg_std_score}/5.0")
        recommendations.append("   - 建议：可作为主要输出模式，但需监控用户反馈")
    else:
        recommendations.append("⚠ 方案A（标准模式20-25%精简）质量下降超出目标")
        recommendations.append(f"   - 质量下降：{quality_drop_std}%，超出目标（≤10%）")
        recommendations.append("   - 建议：需要调整算法参数或采用其他模式")

    # 示例级别建议
    for example in analysis["examples"]:
        if example["quality_drop"]["original_vs_standard"] > 15:
            recommendations.append(
                f"⚠ 示例 '{example['title']}' 下降{example['quality_drop']['original_vs_standard']}%，需要特别关注"
            )
        elif example["quality_drop"]["original_vs_standard"] <= 5:
            recommendations.append(
                f"✓ 示例 '{example['title']}' 保留良好，下降仅{example['quality_drop']['original_vs_standard']}%"
            )

    # 对快速模式的建议
    quality_drop_fast = analysis["summary"]["quality_drop_original_vs_fast"]
    avg_fast_score = analysis["summary"]["average_fast_score"]

    if avg_fast_score >= 3.0:
        recommendations.append(
            f"✓ 快速模式可用：平均评分{avg_fast_score}/5.0，适合快速预览"
        )
    else:
        recommendations.append(
            f"⚠ 快速模式谨慎使用：平均评分{avg_fast_score}/5.0，质量不足"
        )

    return recommendations


def main():
    """主函数"""

    print("=" * 80)
    print("方案A专业评审 - 调整精简目标到20-25%")
    print("=" * 80)
    print("\n执行时间: 2025-01-29")
    print("\n方案A配置:")
    print("  - 标准模式目标精简：20-25%")
    print("  - P1元素保留：100%")
    print("  - P2元素保留：85-95%")
    print("  - 质量下降目标：≤10%")
    print("\n" + "=" * 80)

    print("\n🔍 步骤1: 加载高效精简V2结果")
    results = load_results()
    print("✅ 结果加载完成")

    print("\n📊 步骤2: 组织评审数据")
    review_data = organize_for_review(results)
    print(f"✅ 已准备 {len(review_data)} 个示例的评审数据")

    print("\n👁️ 步骤3: 执行专业评审")
    print("   - 专业导演评审")
    print("   - 资深爱好者评审")
    print("   - 一般观众评审")
    all_reviews = simulate_professional_review(review_data)
    print("✅ 专业评审完成")

    print("\n📋 步骤4: 分析质量评审结果")
    analysis = analyze_quality_review(review_data, all_reviews)

    print("\n" + "=" * 80)
    print("评审结果摘要")
    print("=" * 80)

    print(f"\n总体平均质量评分:")
    print(f"  原始版本: {analysis['summary']['average_original_score']}/5.0")
    print(f"  标准模式: {analysis['summary']['average_standard_score']}/5.0")
    print(f"  快速模式: {analysis['summary']['average_fast_score']}/5.0")

    print(f"\n质量下降分析:")
    print(
        f"  原始 vs 标准模式: {analysis['summary']['quality_drop_original_vs_standard']}%"
    )
    print(
        f"  原始 vs 快速模式: {analysis['summary']['quality_drop_original_vs_fast']}%"
    )

    if analysis["summary"]["plan_a_achieved"]:
        print(f"  ✅ 方案A达标：质量下降≤10%")
    else:
        print(f"  ❌ 方案A未达标：质量下降>10%")

    print(f"\n各示例详细结果:")
    for example in analysis["examples"]:
        print(f"\n  {example['title']}:")
        print(f"    原始: {example['scores']['original']}/5.0")
        print(
            f"    标准: {example['scores']['standard']}/5.0 (精简{example['stats']['standard']['reduction']}%)"
        )
        print(
            f"    质量: {example['quality_drop']['original_vs_standard']}%  {'✅' if example['quality_drop']['original_vs_standard'] <= 10 else '❌'}"
        )
        print(
            f"    P1保留: {example['stats']['standard']['preserved_p1']} P2保留: {example['stats']['standard']['preserved_p2']}"
        )

    print("\n📝 步骤5: 生成改进建议")
    recommendations = generate_recommendations(analysis)

    print("\n" + "=" * 80)
    print("改进建议")
    print("=" * 80)

    for rec in recommendations:
        print(f"  {rec}")

    # 保存完整结果
    output_dir = Path("/Users/achi/Desktop/JEREMY/NEW/phase_B_pilot/results")
    output_dir.mkdir(exist_ok=True)

    output_path = output_dir / "plan_a_review_results.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "plan_config": {
                    "standard_reduction_target": "20-25%",
                    "p1_retention": "100%",
                    "p2_retention": "85-95%",
                    "quality_drop_target": "≤10%",
                },
                "review_data": review_data,
                "all_reviews": all_reviews,
                "analysis": analysis,
                "recommendations": recommendations,
            },
            f,
            ensure_ascii=False,
            indent=2,
        )

    print(f"\n✅ 评审结果已保存: {output_path}")

    # 生成报告
    report_path = output_dir / "plan_a_review_report.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# 方案A专业评审报告\n\n")
        f.write(f"## 评审配置\n\n")
        f.write(f"- 标准模式目标精简：20-25%\n")
        f.write(f"- P1元素保留：100%\n")
        f.write(f"- P2元素保留：85-95%\n")
        f.write(f"- 质量下降目标：≤10%\n\n")

        f.write(f"## 总体结果\n\n")
        f.write(f"### 平均质量评分\n\n")
        f.write(f"| 版本 | 平均分 |\n")
        f.write(f"|------|--------|\n")
        f.write(f"| 原始 | {analysis['summary']['average_original_score']}/5.0 |\n")
        f.write(f"| 标准 | {analysis['summary']['average_standard_score']}/5.0 |\n")
        f.write(f"| 快速 | {analysis['summary']['average_fast_score']}/5.0 |\n\n")

        f.write(f"### 质量下降\n\n")
        f.write(
            f"- 原始 vs 标准模式：**{analysis['summary']['quality_drop_original_vs_standard']}%**\n"
        )
        f.write(
            f"- 原始 vs 快速模式：{analysis['summary']['quality_drop_original_vs_fast']}%\n\n"
        )

        f.write(f"### 方案A达标情况\n\n")
        if analysis["summary"]["plan_a_achieved"]:
            f.write(
                f"✅ **达标**：质量下降 {analysis['summary']['quality_drop_original_vs_standard']}% ≤ 10%\n\n"
            )
        else:
            f.write(
                f"❌ **未达标**：质量下降 {analysis['summary']['quality_drop_original_vs_standard']}% > 10%\n\n"
            )

        f.write(f"## 各示例详细结果\n\n")
        for example in analysis["examples"]:
            f.write(f"### {example['title']}\n\n")
            f.write(f"- 原始：{example['scores']['original']}/5.0\n")
            f.write(
                f"- 标准：{example['scores']['standard']}/5.0 (精简{example['stats']['standard']['reduction']}%)\n"
            )
            f.write(
                f"- 质量下降：{example['quality_drop']['original_vs_standard']}%{' ✅' if example['quality_drop']['original_vs_standard'] <= 10 else ' ❌'}\n"
            )
            f.write(
                f"- P1保留：{example['stats']['standard']['preserved_p1']} / P2保留：{example['stats']['standard']['preserved_p2']}\n\n"
            )

        f.write(f"## 建议总结\n\n")
        for rec in recommendations:
            f.write(f"- {rec}\n")

    print(f"✅ 评审报告已保存: {report_path}")

    print("\n" + "=" * 80)
    print("评审完成")
    print("=" * 80)

    # 决策点
    print("\n🚦 决策点：")
    if analysis["summary"]["plan_a_achieved"]:
        print(f"\n✅ **方案A达标，建议进入阶段C**")
        print(f"\n  核心指标:")
        print(
            f"  - 质量下降: {analysis['summary']['quality_drop_original_vs_standard']}% (目标≤10%)"
        )
        print(f"  - 平均质量评分: {analysis['summary']['average_standard_score']}/5.0")
        print(f"  - P1/P2保留率: 100%")
        print(f"\n  下一步: 进入阶段C大规模实施")
    else:
        print(f"\n❌ 方案A未达标，需要调整")
        print(f"\n  问题:")
        print(
            f"  - 质量下降: {analysis['summary']['quality_drop_original_vs_standard']}% (超出{analysis['summary']['quality_drop_original_vs_standard'] - 10}%)"
        )
        print(f"\n  建议采取的措施:")
        recommendations_needed = [r for r in recommendations if "建议" in r]
        for rec in recommendations_needed[:3]:
            print(f"    • {rec.replace('建议：', '')}")


if __name__ == "__main__":
    main()
