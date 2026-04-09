#!/usr/bin/env python3
"""
创意保留分析工具
为示例评分并生成创意保留计划
"""

import json
import re
from typing import Dict, List, Tuple
from pathlib import Path
from collections import Counter


class CreativeScorer:
    """创意评分系统"""

    def __init__(self):
        # 创意元素权重配置
        self.element_weights = {
            "visual_metaphors": 1.2,  # 视觉隐喻：高权重
            "emotional_details": 1.1,  # 情感细节：高权重
            "environmental_details": 0.9,  # 环境细节：中高权重
            "cinematic_techniques": 1.5,  # 电影技术：最高权重
            "lighting_effects": 1.3,  # 光影效果：高权重
            "color_grading": 1.0,  # 色彩调色：中高权重
            "atmosphere_creation": 1.4,  # 氛围创造：高权重
            "narrative_elements": 0.8,  # 叙事元素：中等权重
        }

        # 质量阈值
        self.score_thresholds = {
            "excellent": 4.5,  # 优秀
            "good": 3.5,  # 良好
            "acceptable": 2.5,  # 可接受
            "poor": 1.5,  # 较差
        }

    def score_creativity(self, content: str) -> Dict:
        """评估内容的创意质量"""
        score = {
            "raw_score": 0.0,
            "normalized_score": 0.0,
            "grade": "",
            "element_scores": {},
            "strengths": [],
            "weaknesses": [],
            "recommendations": [],
        }

        # 计算各类创意元素得分
        element_score = self._calculate_element_scores(content)
        score["element_scores"] = element_score

        # 计算原始得分
        raw_score = element_score["total_weighted_score"]

        # 归一化得分 (0-5分)
        max_possible = element_score["max_possible_score"]
        if max_possible > 0:
            score["normalized_score"] = (raw_score / max_possible) * 5
            score["raw_score"] = round(score["normalized_score"], 2)

        # 确定等级
        score["grade"] = self._determine_grade(score["normalized_score"])

        # 识别优势和劣势
        score["strengths"] = self._identify_strengths(element_score)
        score["weaknesses"] = self._identify_weaknesses(element_score)

        # 生成建议
        score["recommendations"] = self._generate_recommendations(score)

        return score

    def _calculate_element_scores(self, content: str) -> Dict:
        """计算各类创意元素得分"""
        element_scores = {
            "total_weighted_score": 0.0,
            "max_possible_score": 0.0,
            "categories": {},
        }

        # 创意元素关键词词典
        element_keywords = {
            "visual_metaphors": [
                "牢笼",
                "翅膀",
                "囚笼",
                "枷锁",
                "阴影",
                "光晕",
                "剪影",
                "残影",
                "光斑",
                "闪烁",
                "飞舞",
                "流淌",
                "漂浮",
                "倾泻",
                "晕出",
                "框架",
            ],
            "emotional_details": [
                "瞳孔",
                "泪光",
                "嘴角",
                "微表情",
                "发丝",
                "皱纹",
                "汗珠",
                "呼吸",
                "微笑",
                "咬紧",
                "收缩",
                "描摹",
                "凝视",
                "望向",
                "闪耀",
                "颤抖",
            ],
            "environmental_details": [
                "虚化",
                "散景",
                "色块",
                "质感",
                "纹理",
                "闪烁",
                "摇晃",
                "倾斜",
                "剥落",
                "淤积",
                "无缝融合",
                "隐约可辨",
                "昏暗",
                "潮湿",
                "杂乱",
            ],
            "cinematic_techniques": [
                "荷兰角",
                "低机位",
                "高角度",
                "仰拍",
                "俯拍",
                "浅景深",
                "深景深",
                "广角",
                "85mm",
                "24mm",
                "特写",
                "中景",
                "极远景",
                "紧凑特写",
                "中近景",
                "景深",
                "构图",
                "镜头",
                "机位",
                "轮廓光",
                "侧光",
            ],
            "lighting_effects": [
                "体积光",
                "侧光",
                "逆光",
                "眼神光",
                "发丝光",
                "轮廓光",
                "丁达尔效应",
                "柔光",
                "硬光",
                "单一光源",
                "荧光灯",
                "裸露灯泡",
                "黄金时段",
                "明暗",
                "深影",
                "阴影",
                "光晕",
                "光线",
                "闪烁",
                "折射",
            ],
            "color_grading": [
                "饱和",
                "色调",
                "色温",
                "色偏",
                "对比度",
                "高调",
                "低调",
                "冷暖",
                "蓝绿",
                "冷蓝绿",
                "琥珀色",
                "深紫",
                "燃烧的橙",
                "去饱和",
                "低饱和",
                "病态的绿",
                "肮脏的绿",
                "深沉的黑",
                "泛黄的白",
                "灰色",
            ],
            "atmosphere_creation": [
                "一触即发",
                "爆发",
                "苦涩而温柔",
                "私密",
                "安静",
                "沉重",
                "深深",
                "惊叹",
                "敬畏",
                "蔓延的恐惧",
                "可怕的顿悟",
                "迫在眉睫",
                "原始的",
                "难以捉摸",
                "不可预测",
                "凝重",
                "压抑",
                "威胁",
                "暴力",
            ],
        }

        # 计算每类元素的得分
        for category, keywords in element_keywords.items():
            weight = self.element_weights.get(category, 1.0)
            count = sum(1 for keyword in keywords if keyword in content)

            # 得分计算：每个关键词得1分，乘以权重
            category_score = count * weight
            max_score = len(keywords) * weight

            element_scores["categories"][category] = {
                "count": count,
                "weight": weight,
                "score": category_score,
                "max_score": max_score,
                "percentage": (category_score / max_score * 100)
                if max_score > 0
                else 0,
                "grade": self._get_category_grade(
                    category_score / max_score if max_score > 0 else 0
                ),
            }

            element_scores["total_weighted_score"] += category_score
            element_scores["max_possible_score"] += max_score

        return element_scores

    def _determine_grade(self, score: float) -> str:
        """确定评分等级"""
        if score >= self.score_thresholds["excellent"]:
            return "A+ (优秀)"
        elif score >= self.score_thresholds["good"]:
            return "A (良好)"
        elif score >= self.score_thresholds["acceptable"]:
            return "B (可接受)"
        elif score >= self.score_thresholds["poor"]:
            return "C (较差)"
        else:
            return "D (差)"

    def _get_category_grade(self, percentage: float) -> str:
        """确定类别等级"""
        if percentage >= 0.8:
            return "优秀"
        elif percentage >= 0.6:
            return "良好"
        elif percentage >= 0.4:
            return "一般"
        else:
            return "不足"

    def _identify_strengths(self, element_scores: Dict) -> List[str]:
        """识别优势"""
        strengths = []
        categories = element_scores["categories"]

        # 找出得分最高的2-3个类别
        sorted_categories = sorted(
            categories.items(), key=lambda x: x[1]["percentage"], reverse=True
        )

        for category, data in sorted_categories[:3]:
            if data["percentage"] >= 0.5:  # 至少达到50%
                strengths.append(
                    f"{category}: {data['count']}个元素 (得分{data['percentage']:.0f}%)"
                )

        return strengths

    def _identify_weaknesses(self, element_scores: Dict) -> List[str]:
        """识别劣势"""
        weaknesses = []
        categories = element_scores["categories"]

        # 找出得分最低的2-3个类别
        sorted_categories = sorted(categories.items(), key=lambda x: x[1]["percentage"])

        for category, data in sorted_categories[:3]:
            if data["percentage"] < 0.5 and data["count"] > 0:  # 低于50%但有元素
                weaknesses.append(
                    f"{category}: 仅{data['count']}个元素 (得分{data['percentage']:.0f}%)"
                )

        return weaknesses

    def _generate_recommendations(self, score: Dict) -> List[str]:
        """生成改进建议"""
        recommendations = []

        if score["normalized_score"] >= self.score_thresholds["excellent"]:
            recommendations.append("创意质量优秀，可作为高优先级示例")
            recommendations.append("建议轻度精简（20-25%），保留90%创意")

        elif score["normalized_score"] >= self.score_thresholds["good"]:
            recommendations.append("创意质量良好，建议适度精简（30-35%）")
            recommendations.append("保留80%创意，特别关注优势类别的保护")

        elif score["normalized_score"] >= self.score_thresholds["acceptable"]:
            recommendations.append("创意质量一般，需要较大精简（40-45%）")
            recommendations.append("保留75%创意，优先保护高权重元素")

        else:
            recommendations.append("创意质量偏低，可作为较大精简对象")
            recommendations.append("保留50-60%核心创意，大幅压缩非关键元素")

        # 针对劣势的建议
        for weakness in score["weaknesses"]:
            category = weakness.split(":")[0]
            if category in "visual_metaphors":
                recommendations.append(f"增强视觉隐喻：添加光斑、阴影、剪影等元素")
            elif category in "emotional_details":
                recommendations.append(f"深化情感表达：添加微表情、眼神、动作细节")
            elif category in "cinematic_techniques":
                recommendations.append(f"强化电影技术：使用更多专业镜头语言")

        return recommendations

    def analyze_examples(self, examples_data: List[Dict]) -> Dict:
        """分析所有示例并生成分级方案"""
        analysis = {
            "analysis_summary": {},
            "example_scores": [],
            "scoring_distribution": {},
            "tiered_processing_plan": {},
        }

        # 评分每个示例
        for example in examples_data:
            score_result = self.score_creativity(example["original"])
            example_info = {
                "id": example.get("id", 0),
                "title": example["title"],
                "score": score_result["normalized_score"],
                "grade": score_result["grade"],
                "element_scores": score_result["element_scores"],
                "strengths": score_result["strengths"],
                "weaknesses": score_result["weaknesses"],
                "recommendations": score_result["recommendations"],
                "processing_priority": self._determine_processing_priority(
                    score_result["normalized_score"]
                ),
                "target_reduction": self._calculate_target_reduction(
                    score_result["normalized_score"]
                ),
                "creative_retention_rate": self._calculate_retention_rate(
                    score_result["normalized_score"]
                ),
            }
            analysis["example_scores"].append(example_info)

        # 统计评分分布
        analysis["scoring_distribution"] = self._calculate_distribution(
            analysis["example_scores"]
        )

        # 生成分级处理方案
        analysis["tiered_processing_plan"] = self._create_tiered_plan(
            analysis["example_scores"]
        )

        # 生成摘要
        analysis["analysis_summary"] = {
            "total_examples": len(examples_data),
            "average_score": sum(e["score"] for e in analysis["example_scores"])
            / len(analysis["example_scores"]),
            "high_creativity_count": sum(
                1 for e in analysis["example_scores"] if e["score"] >= 4.0
            ),
            "medium_creativity_count": sum(
                1 for e in analysis["example_scores"] if 3.0 <= e["score"] < 4.0
            ),
            "low_creativity_count": sum(
                1 for e in analysis["example_scores"] if e["score"] < 3.0
            ),
            "average_reduction_target": sum(
                e["target_reduction"] for e in analysis["example_scores"]
            )
            / len(analysis["example_scores"]),
            "average_retention_rate": sum(
                e["creative_retention_rate"] for e in analysis["example_scores"]
            )
            / len(analysis["example_scores"]),
        }

        return analysis

    def _determine_processing_priority(self, score: float) -> str:
        """确定处理优先级"""
        if score >= 4.5:
            return "highest"
        elif score >= 4.0:
            return "high"
        elif score >= 3.5:
            return "medium"
        elif score >= 2.5:
            return "low"
        else:
            return "lowest"

    def _calculate_target_reduction(self, score: float) -> float:
        """计算目标精简率"""
        if score >= 4.5:
            return 20.0  # 轻度精简
        elif score >= 4.0:
            return 25.0
        elif score >= 3.5:
            return 30.0
        elif score >= 3.0:
            return 35.0
        else:
            return 45.0  # 较大精简

    def _calculate_retention_rate(self, score: float) -> float:
        """计算创意保留率"""
        if score >= 4.5:
            return 90.0  # 保留90%
        elif score >= 4.0:
            return 85.0
        elif score >= 3.5:
            return 80.0
        elif score >= 3.0:
            return 75.0
        else:
            return 60.0

    def _calculate_distribution(self, example_scores: List[Dict]) -> Dict:
        """计算评分分布"""
        distribution = {
            "A_plus": sum(1 for e in example_scores if e["grade"].startswith("A+")),
            "A": sum(1 for e in example_scores if e["grade"].startswith("A")),
            "B": sum(1 for e in example_scores if e["grade"].startswith("B")),
            "C": sum(1 for e in example_scores if e["grade"].startswith("C")),
            "D": sum(1 for e in example_scores if e["grade"].startswith("D")),
            "score_ranges": {
                "4.5-5.0": sum(1 for e in example_scores if 4.5 <= e["score"]),
                "4.0-4.5": sum(1 for e in example_scores if 4.0 <= e["score"] < 4.5),
                "3.5-4.0": sum(1 for e in example_scores if 3.5 <= e["score"] < 4.0),
                "3.0-3.5": sum(1 for e in example_scores if 3.0 <= e["score"] < 3.5),
                "<3.0": sum(1 for e in example_scores if e["score"] < 3.0),
            },
        }
        return distribution

    def _create_tiered_plan(self, example_scores: List[Dict]) -> Dict:
        """创建分级处理方案"""
        plan = {
            "high_creativity_tier": {
                "examples": [],
                "strategy": "轻度精简，重点保护创意核心",
                "target_reduction": "20-25%",
                "retention_rate": "90%",
                "processing_notes": "使用完整模式或标准模式，优先保护P1和P2元素",
            },
            "medium_creativity_tier": {
                "examples": [],
                "strategy": "适度精简，平衡质量与性能",
                "target_reduction": "30-35%",
                "retention_rate": "80%",
                "processing_notes": "使用标准模式，保护高权重创意元素，适度压缩P3元素",
            },
            "low_creativity_tier": {
                "examples": [],
                "strategy": "较大精简，优化性能",
                "target_reduction": "40-45%",
                "retention_rate": "60-75%",
                "processing_notes": "使用标准模式或快速模式，保护P1元素，大幅压缩P3/P4元素",
            },
        }

        # 分配示例到各层级
        for example in example_scores:
            if example["score"] >= 4.0:
                plan["high_creativity_tier"]["examples"].append(example)
            elif example["score"] >= 3.0:
                plan["medium_creativity_tier"]["examples"].append(example)
            else:
                plan["low_creativity_tier"]["examples"].append(example)

        return plan


if __name__ == "__main__":
    # 测试评分系统
    scorer = CreativeScorer()

    # 示例数据
    examples_data = [
        {
            "id": 1,
            "title": "紧张对峙（剧情片）",
            "original": """中景，昏暗的地下停车场。
两个男人面对面站立。穿皱巴巴西装的男人身体前倾，咬紧下巴，姿态充满攻击性；皮夹克男人双臂交叉，表情难以捉摸。
头顶荧光灯闪烁，刺眼的光线将两人的脸分割成明暗两半。身后混凝土柱子形成牢笼般的框架。
略微仰拍，两人都显得气势逼人。
冷蓝绿色调。一触即发，暴力随时可能爆发。""",
        },
        {
            "id": 2,
            "title": "温馨回忆（剧情片）",
            "original": """特写，年轻女性的面容。
她望向雨水划过的窗户，眼中闪着未落的泪光，嘴角却浮现一丝温柔的微笑。手中握着一张老照片，手指轻轻描摹着边缘。
黄金时段的柔光透过窗户，温暖她的面容，在凌乱的发丝上晕出光晕。
背景是温馨的客厅和书架，85mm镜头虚化成柔和的色块。
苦涩而温柔，私密的回忆时刻。""",
        },
        {
            "id": 6,
            "title": "世界观建立（奇幻/科幻）",
            "original": """极远景，黄昏时分的浮空城市。
巨大石质平台在云间漂浮，由不可思议的长吊桥相连。瀑布从边缘倾泻入下方虚空。数千扇小窗散发温暖的琥珀色光芒，落日将云层染成深紫与燃烧的橙。
前景，一个旅人的剪影站在悬崖边缘仰望，渺小的身影衬托城市的巨大。体积光穿过云层缝隙。
惊奇与敬畏，不可能世界中的冒险。""",
        },
    ]

    # 执行分析
    analysis = scorer.analyze_examples(examples_data)

    # 输出结果
    print("=" * 80)
    print("创意分析结果")
    print("=" * 80)

    print(f"\n分析摘要:")
    print(f"  总示例数: {analysis['analysis_summary']['total_examples']}")
    print(f"  平均得分: {analysis['analysis_summary']['average_score']:.2f}/5.0")
    print(f"  高创意示例: {analysis['analysis_summary']['high_creativity_count']}个")
    print(f"  中创意示例: {analysis['analysis_summary']['medium_creativity_count']}个")
    print(f"  低创意示例: {analysis['analysis_summary']['low_creativity_count']}个")
    print(
        f"  平均精简目标: {analysis['analysis_summary']['average_reduction_target']:.1f}%"
    )
    print(
        f"  平均创意保留率: {analysis['analysis_summary']['average_retention_rate']:.1f}%"
    )

    print(f"\n分级处理方案:")
    for tier_name, tier_data in analysis["tiered_processing_plan"].items():
        print(f"\n{tier_name}:")
        print(f"  示例数量: {len(tier_data['examples'])}")
        print(f"  策略: {tier_data['strategy']}")
        print(f"  目标精简: {tier_data['target_reduction']}")
        print(f"  创意保留: {tier_data['retention_rate']}")

    # 保存分析结果
    output_path = Path(__file__).parent / "results" / "creative_analysis_plan.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)

    print(f"\n分析结果已保存至: {output_path}")
