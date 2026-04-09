#!/usr/bin/env python3
"""
专业评审系统 - 模拟专业导演、资深爱好者、一般观众的评审过程
"""

import json
import random
from typing import Dict, List
from pathlib import Path


class ProfessionalReviewSystem:
    """专业评审系统"""

    def __init__(self):
        # 评审标准
        self.review_criteria = {
            "cinematic_quality": {
                "weight": 1.2,
                "description": "电影感和专业性",
                "sub_criteria": {
                    "camera_technique": "镜头语言运用",
                    "lighting_craft": "光影技术专业度",
                    "composition": "构图和景深运用",
                },
            },
            "emotional_depth": {
                "weight": 1.0,
                "description": "情感深度和冲击力",
                "sub_criteria": {
                    "emotion_expression": "情感表达细腻度",
                    "atmosphere_creation": "氛围营造能力",
                    "impact_power": "情感冲击力",
                },
            },
            "visual_richness": {
                "weight": 0.9,
                "description": "视觉丰富度和层次",
                "sub_criteria": {
                    "detail_level": "细节丰富度",
                    "texture_quality": "质感表现",
                    "color_grading": "色彩运用",
                },
            },
            "narrative_clarity": {
                "weight": 0.8,
                "description": "叙事清晰度",
                "sub_criteria": {
                    "story_telling": "故事讲述清晰度",
                    "scene_understanding": "场景理解度",
                    "readability": "可读性",
                },
            },
        }

        # 评审者配置
        self.reviewer_types = {
            "director": {
                "name": "专业导演",
                "expertise_level": "expert",
                "focus_weights": {
                    "cinematic_quality": 1.5,
                    "emotional_depth": 0.8,
                    "visual_richness": 0.7,
                    "narrative_clarity": 0.6,
                },
                "scoring_std": 0.3,  # 评分标准差
            },
            "enthusiast": {
                "name": "资深爱好者",
                "expertise_level": "advanced",
                "focus_weights": {
                    "cinematic_quality": 1.0,
                    "emotional_depth": 1.2,
                    "visual_richness": 1.0,
                    "narrative_clarity": 0.8,
                },
                "scoring_std": 0.4,
            },
            "viewer": {
                "name": "一般观众",
                "expertise_level": "beginner",
                "focus_weights": {
                    "cinematic_quality": 0.6,
                    "emotional_depth": 1.3,
                    "visual_richness": 1.1,
                    "narrative_clarity": 1.2,
                },
                "scoring_std": 0.5,
            },
        }

    def score_content(self, content: str, reviewer_type: str) -> Dict:
        """评审内容并给出评分"""
        if reviewer_type not in self.reviewer_types:
            reviewer_type = "viewer"

        reviewer = self.reviewer_types[reviewer_type]
        scores = {}

        # 为每个维度评分
        for criterion, config in self.review_criteria.items():
            base_score = self._calculate_base_score(content, criterion)
            weighted_score = base_score * reviewer["focus_weights"].get(criterion, 1.0)

            # 添加随机性模拟专业判断差异
            noise = random.gauss(0, reviewer["scoring_std"])
            final_score = max(0, min(5, weighted_score + noise))

            scores[criterion] = {
                "base_score": round(base_score, 2),
                "weight": reviewer["focus_weights"].get(criterion, 1.0),
                "final_score": round(final_score, 2),
            }

        # 计算总体评分
        total_score = sum(s["final_score"] for s in scores.values()) / len(scores)

        return {
            "reviewer_type": reviewer_type,
            "reviewer_name": reviewer["name"],
            "dimension_scores": scores,
            "total_score": round(total_score, 2),
            "feedback": self._generate_feedback(scores, total_score),
        }

    def _calculate_base_score(self, content: str, criterion: str) -> float:
        """计算基础分数（基于内容内容分析）"""
        # 基于创意元素数量估算
        creative_element_kits = {
            "cinematic_quality": [
                "荷兰角",
                "低机位",
                "高角度",
                "仰拍",
                "俯拍",
                "浅景深",
                "深景深",
                "24mm",
                "85mm",
                "广角",
                "特写",
                "中景",
                "极远景",
                "轮廓光",
                "侧光",
                "丁达尔效应",
                "体积光",
                "景深",
                "构图",
            ],
            "emotional_depth": [
                "瞳孔",
                "汗珠",
                "发丝",
                "微表情",
                "嘴角",
                "皱痕",
                "咬紧",
                "收缩",
                "描摹",
                "微笑",
                "望向",
                "颤抖",
            ],
            "visual_richness": [
                "虚化",
                "散景",
                "色块",
                "质感",
                "纹理",
                "光晕",
                "剪影",
                "残影",
                "光斑",
                "闪烁",
                "色调",
                "色温",
                "对比度",
                "饱和",
            ],
            "narrative_clarity": [
                "一触即发",
                "爆发",
                "温馨",
                "回忆",
                "孤独",
                "安静",
                "敬畏",
                "恐惧",
                "威胁",
                "暴力",
                "难以捉摸",
                "不可预测",
            ],
        }

        elements = creative_element_kits.get(criterion, [])
        element_count = sum(1 for elem in elements if elem in content)

        # 基于元素数量计算分数（0-5分）
        if element_count >= 5:
            return 4.5
        elif element_count >= 4:
            return 4.0
        elif element_count >= 3:
            return 3.5
        elif element_count >= 2:
            return 3.0
        elif element_count >= 1:
            return 2.5
        else:
            return 2.0

    def _generate_feedback(self, scores: Dict, total_score: float) -> str:
        """生成反馈意见"""
        feedback_parts = []

        # 识别优势
        strengths = [c for c, s in scores.items() if s["final_score"] >= 4.0]
        if strengths:
            strength_names = {
                "cinematic_quality": "电影质量",
                "emotional_depth": "情感深度",
                "visual_richness": "视觉丰富度",
                "narrative_clarity": "叙事清晰度",
            }
            strength_list = [str(strength_names.get(s, s)) for s in strengths]
            feedback_parts.append(f"优势：{', '.join(strength_list)}表现优秀")

        # 识别劣势
        weaknesses = [c for c, s in scores.items() if s["final_score"] < 3.0]
        if weaknesses:
            weakness_names = {
                "cinematic_quality": "电影质量",
                "emotional_depth": "情感深度",
                "visual_richness": "视觉丰富度",
                "narrative_clarity": "叙事清晰度",
            }
            weakness_list = [str(weakness_names.get(w, w)) for w in weaknesses]
            feedback_parts.append(f"改进：{', '.join(weakness_list)}有待加强")

        # 总体评价
        if total_score >= 4.0:
            feedback_parts.append("整体评价：优秀")
        elif total_score >= 3.0:
            feedback_parts.append("整体评价：良好")
        elif total_score >= 2.0:
            feedback_parts.append("整体评价：一般")
        else:
            feedback_parts.append("整体评价：需要改进")

        return "；".join(feedback_parts)

    def conduct_blind_test(self, contents: Dict[str, str]) -> Dict:
        """进行盲测对比评审"""
        results = {
            "test_info": {
                "variants": list(contents.keys()),
                "reviewers": list(self.reviewer_types.keys()),
            },
            "reviews": {},
        }

        for reviewer_type in self.reviewer_types.keys():
            reviewer_results = {
                reviewer_type: {
                    "name": self.reviewer_types[reviewer_type]["name"],
                    "scores": {},
                    "preference": "",
                }
            }

            scores_for_comparison = {}

            for variant_name, content in contents.items():
                # 评审每个版本
                review = self.score_content(content, reviewer_type)
                reviewer_results[reviewer_type]["scores"][variant_name] = review
                scores_for_comparison[variant_name] = review["total_score"]

            # 确定偏好（选择得分最高的版本）
            if scores_for_comparison:
                preferred = max(scores_for_comparison.items(), key=lambda x: x[1])
                reviewer_results[reviewer_type]["preference"] = preferred[0]

            results["reviews"].update(reviewer_results)

        return results

    def analyze_pilot_results(self, pilot_results: List[Dict]) -> Dict:
        """分析试点结果"""
        analysis = {
            "summary": {},
            "mode_comparison": {},
            "quality_improvement": {},
            "recommendations": [],
        }

        # 提取各模式的评分
        mode_scores = {
            "original": {
                "cinematic_quality": [],
                "emotional_depth": [],
                "visual_richness": [],
                "narrative_clarity": [],
                "total": [],
            },
            "standard": {
                "cinematic_quality": [],
                "emotional_depth": [],
                "visual_richness": [],
                "narrative_clarity": [],
                "total": [],
            },
            "fast": {
                "cinematic_quality": [],
                "emotional_depth": [],
                "visual_richness": [],
                "narrative_clarity": [],
                "total": [],
            },
        }

        for example_result in pilot_results:
            if "reviews" in example_result:
                for variant, review in example_result["reviews"].items():
                    if variant in mode_scores:
                        reviewer_score = review.get("total_score", 0)
                        mode_scores[variant]["total"].append(reviewer_score)

                        # 维度分数
                        if "dimension_scores" in review:
                            for dimension, score_data in review[
                                "dimension_scores"
                            ].items():
                                if dimension in mode_scores[variant]:
                                    mode_scores[variant][dimension].append(
                                        score_data["final_score"]
                                    )

        # 计算各模式平均分
        for mode, scores in mode_scores.items():
            mode_scores[mode]["averages"] = {}
            for dimension, dimension_scores in scores.items():
                if dimension_scores:
                    mode_scores[mode]["averages"][dimension] = round(
                        sum(dimension_scores) / len(dimension_scores), 2
                    )

        analysis["mode_comparison"] = mode_scores

        # 计算质量改善
        if "original" in mode_scores and "standard" in mode_scores:
            if mode_scores["original"]["averages"].get("total") and mode_scores[
                "standard"
            ]["averages"].get("total"):
                original_avg = mode_scores["original"]["averages"]["total"]
                standard_avg = mode_scores["standard"]["averages"]["total"]
                improvement = ((standard_avg - original_avg) / original_avg) * 100
                analysis["quality_improvement"]["standard_vs_original"] = round(
                    improvement, 1
                )

        # 生成建议
        analysis["recommendations"] = self._generate_recommendations(analysis)

        # 生成摘要
        analysis["summary"] = {
            "total_examples_reviewed": len(pilot_results),
            "best_performing_mode": self._find_best_mode(mode_scores),
            "quality_improvement_achieved": analysis["quality_improvement"].get(
                "standard_vs_original", "待计算"
            ),
        }

        return analysis

    def _find_best_mode(self, mode_scores: Dict) -> str:
        """找出最佳表现的模式"""
        best_mode = "unknown"
        best_score = 0

        for mode, scores in mode_scores.items():
            if "averages" in scores and "total" in scores["averages"]:
                avg_score = scores["averages"]["total"]
                if avg_score > best_score:
                    best_score = avg_score
                    best_mode = mode

        return best_mode

    def _generate_recommendations(self, analysis: Dict) -> List[str]:
        """生成改进建议"""
        recommendations = []

        mode_comparison = analysis.get("mode_comparison", {})
        if not mode_comparison:
            return recommendations

        # 检查标准模式是否达到目标
        if "standard" in mode_comparison and "averages" in mode_comparison["standard"]:
            _std_avg = mode_comparison["standard"]["averages"].get("total", 0)

            if _std_avg >= 4.0:
                recommendations.append("✅ 标准模式达到高质量标准，推荐作为默认模式")
            elif _std_avg >= 3.5:
                recommendations.append("✓ 标准模式质量良好，可作为主要输出模式")
            else:
                recommendations.append("⚠ 标准模式质量有待提升，建议优化参数")

        # 检查质量改善
        quality_improvement = analysis.get("quality_improvement", {})
        if "standard_vs_original" in quality_improvement:
            improvement = quality_improvement["standard_vs_original"]
            if improvement > 0:
                recommendations.append(
                    f"✅ 相比原始系统，标准模式质量提升 {improvement}%"
                )
            elif improvement > -10:
                recommendations.append("⚠ 标准模式质量接近当前系统，可考虑使用")
            else:
                recommendations.append("❌ 标准模式质量下降较多，需要调整策略")

        # 检查维度表现
        if "standard" in mode_comparison and "averages" in mode_comparison["standard"]:
            _std_avgs = mode_comparison["standard"]["averages"]
            weak_dimensions = [
                dim
                for dim, score in _std_avgs.items()
                if dim != "total" and score < 3.0
            ]

            if weak_dimensions:
                dim_names = {
                    "cinematic_quality": "电影质量",
                    "emotional_depth": "情感深度",
                    "visual_richness": "视觉丰富度",
                    "narrative_clarity": "叙事清晰度",
                }
                weak_dim_names = [dim_names.get(d, d) for d in weak_dimensions]
                recommendations.append(f"⚠ 需要加强 {', '.join(weak_dim_names)} 的表现")

        return recommendations


if __name__ == "__main__":
    # 测试评审系统
    review_system = ProfessionalReviewSystem()

    # 测试内容
    test_contents = {
        "original": """中景，昏暗的地下停车场。
两个男人面对面站立。穿皱巴巴西装的男人身体前倾，咬紧下巴，姿态充满攻击性；皮夹克男人双臂交叉，表情难以捉摸。
头顶荧光灯闪烁，刺眼的光线将两人的脸分割成明暗两半。身后混凝土柱子形成牢笼般的框架。
略微仰拍，两人都显得气势逼人。
冷蓝绿色调。一触即发，暴力随时可能爆发。""",
        "standard": """中景，地下停车场。两个男人面对面，西装男人前倾，咬紧下巴；皮夹克男人双臂交叉。
顶上灯闪烁，光线分割两人的脸。后方柱子形成框架。
仰拍，两人气势逼人。
冷色调。一触即发，暴力即发。""",
    }

    # 执行盲测
    results = review_system.conduct_blind_test(test_contents)

    # 输出结果
    print("=" * 80)
    print("盲测评审结果")
    print("=" * 80)

    for reviewer_key, reviewer_data in results["reviews"].items():
        print(f"\n{reviewer_data['name']}:")
        print(f"  偏好: {reviewer_data['preference']}")
        for variant, scores in reviewer_data["scores"].items():
            print(f"  {variant}: {scores['total_score']}分 - {scores['feedback']}")

    # 保存结果
    output_dir = Path(__file__).parent / "results"
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / "pilot_review_results.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n评审结果已保存: {output_path}")
