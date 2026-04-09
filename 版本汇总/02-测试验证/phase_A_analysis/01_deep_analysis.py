#!/usr/bin/env python3
"""
深度分析脚本 - 创意质量下降原因分析
"""

import json
import re
from typing import Dict, List, Tuple
from pathlib import Path
from collections import Counter


class CreativeFailureAnalyzer:
    """创意流失深度分析器"""

    def __init__(self):
        # 创意元素分类系统
        self.creative_categories = {
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
            ],
        }

        # 电影质量维度
        self.quality_dimensions = {
            "cinematic_quality": {
                "keywords": [
                    "荷兰角",
                    "低机位",
                    "高角度",
                    "仰拍",
                    "俯拍",
                    "广角",
                    "85mm",
                    "24mm",
                    "景深",
                    "浅景深",
                    "深景深",
                    "轮廓光",
                    "侧光",
                    "体积光",
                ],
                "weight": 1.0,  # 最高权重
            },
            "emotional_depth": {
                "keywords": [
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
                    "疑视",
                    "闪耀",
                ],
                "weight": 0.9,
            },
            "visual_richness": {
                "keywords": [
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
                    "丁达尔效应",
                    "色温",
                    "色调",
                    "对比度",
                ],
                "weight": 0.8,
            },
            "narrative_clarity": {
                "keywords": [
                    "一触即发",
                    "爆发",
                    "苦涩而温柔",
                    "私密",
                    "安静",
                    "沉重",
                    "深沉",
                    "惊叹",
                    "敬畏",
                    "蔓延的恐惧",
                    "可怕的顿悟",
                    "迫在眉睫",
                ],
                "weight": 0.7,
            },
        }

    def analyze_example(self, content: str, title: str) -> Dict:
        """分析单个示例的创意质量"""
        analysis = {
            "title": title,
            "total_creative_elements": 0,
            "category_counts": {},
            "quality_scores": {},
            "missing_categories": [],
            "creative_density": 0.0,
            "word_count": len(content),
            "creative_per_100_words": 0.0,
        }

        # 统计各类创意元素
        for category, keywords in self.creative_categories.items():
            count = 0
            matched = []
            for keyword in keywords:
                if keyword in content:
                    count += content.count(keyword)
                    matched.append(keyword)

            analysis["category_counts"][category] = {
                "count": count,
                "matched_keywords": matched,
            }
            analysis["total_creative_elements"] += count

            if count == 0:
                analysis["missing_categories"].append(category)

        # 计算创意密度
        analysis["creative_density"] = (
            analysis["total_creative_elements"] / analysis["word_count"] * 1000
        )
        analysis["creative_per_100_words"] = (
            analysis["total_creative_elements"] / analysis["word_count"] * 100
        )

        # 计算各质量维度分数
        for dimension, config in self.quality_dimensions.items():
            score = 0
            for keyword in config["keywords"]:
                if keyword in content:
                    score += 1

            # 归一化分数 (0-1)
            max_possible = len(config["keywords"])
            analysis["quality_scores"][dimension] = {
                "raw_score": score,
                "normalized_score": score / max_possible if max_possible > 0 else 0,
                "weight": config["weight"],
                "weighted_score": (score / max_possible) * config["weight"]
                if max_possible > 0
                else 0,
            }

        return analysis

    def compare_versions(self, original: str, simplified: str, title: str) -> Dict:
        """对比原始版本和简化版本"""
        comparison = {
            "title": title,
            "original": self.analyze_example(original, title),
            "simplified": self.analyze_example(simplified, title),
            "differences": {},
        }

        # 计算差异
        diff = comparison["differences"]
        orig = comparison["original"]
        simpl = comparison["simplified"]

        # 创意元素数量变化
        diff["total_elements_change"] = (
            simpl["total_creative_elements"] - orig["total_creative_elements"]
        )
        diff["total_elements_percentage"] = (
            (diff["total_elements_change"] / orig["total_creative_elements"] * 100)
            if orig["total_creative_elements"] > 0
            else 0
        )

        # 字数变化
        diff["word_count_change"] = simpl["word_count"] - orig["word_count"]
        diff["word_count_percentage"] = (
            (diff["word_count_change"] / orig["word_count"] * 100)
            if orig["word_count"] > 0
            else 0
        )

        # 创意密度变化
        diff["creative_density_change"] = (
            simpl["creative_density"] - orig["creative_density"]
        )
        diff["creative_density_percentage"] = (
            (diff["creative_density_change"] / orig["creative_density"] * 100)
            if orig["creative_density"] > 0
            else 0
        )

        # 分类变化
        diff["category_changes"] = {}
        for category in orig["category_counts"].keys():
            orig_count = orig["category_counts"][category]["count"]
            simpl_count = simpl["category_counts"][category]["count"]
            change = simpl_count - orig_count
            diff["category_changes"][category] = {
                "original": orig_count,
                "simplified": simpl_count,
                "change": change,
                "percentage": (change / orig_count * 100) if orig_count > 0 else 0,
            }

        # 质量维度变化
        diff["quality_dimension_changes"] = {}
        for dimension in orig["quality_scores"].keys():
            orig_score = orig["quality_scores"][dimension]["weighted_score"]
            simpl_score = simpl["quality_scores"][dimension]["weighted_score"]
            change = simpl_score - orig_score
            diff["quality_dimension_changes"][dimension] = {
                "original": orig_score,
                "simplified": simpl_score,
                "change": change,
                "percentage": (change / orig_score * 100) if orig_score > 0 else 0,
            }

        # 识别丢失的创意元素
        diff["lost_elements"] = []
        orig_matched = set()
        simpl_matched = set()

        for category_data in orig["category_counts"].values():
            orig_matched.update(category_data["matched_keywords"])

        for category_data in simpl["category_counts"].values():
            simpl_matched.update(category_data["matched_keywords"])

        diff["lost_elements"] = list(orig_matched - simpl_matched)

        return comparison

    def generate_comprehensive_report(self, examples_data: List[Dict]) -> Dict:
        """生成综合分析报告"""
        report = {
            "analysis_date": "2025-01-29",
            "summary": {},
            "example_analyses": [],
            "overall_statistics": {},
            "key_findings": [],
            "recommendations": [],
        }

        # 分析每个示例
        for example in examples_data:
            comparison = self.compare_versions(
                example["original"], example["simplified"], example["title"]
            )
            report["example_analyses"].append(comparison)

        # 计算总体统计
        total_original_elements = sum(
            c["original"]["total_creative_elements"] for c in report["example_analyses"]
        )
        total_simplified_elements = sum(
            c["simplified"]["total_creative_elements"]
            for c in report["example_analyses"]
        )

        # 质量维度总体变化
        dimension_changes = {}
        for comparison in report["example_analyses"]:
            for dimension, change_data in comparison["differences"][
                "quality_dimension_changes"
            ].items():
                if dimension not in dimension_changes:
                    dimension_changes[dimension] = {"original": 0, "simplified": 0}
                dimension_changes[dimension]["original"] += change_data["original"]
                dimension_changes[dimension]["simplified"] += change_data["simplified"]

        report["overall_statistics"] = {
            "total_examples": len(examples_data),
            "total_creative_elements_lost": total_original_elements
            - total_simplified_elements,
            "average_creative_loss_percentage": 0.0,
            "quality_dimension_impacts": {},
        }

        # 计算平均创意损失
        if total_original_elements > 0:
            report["overall_statistics"]["average_creative_loss_percentage"] = (
                (total_original_elements - total_simplified_elements)
                / total_original_elements
            ) * 100

        # 计算质量维度影响
        for dimension, scores in dimension_changes.items():
            if scores["original"] > 0:
                impact = (
                    (scores["simplified"] - scores["original"])
                    / scores["original"]
                    * 100
                )
                report["overall_statistics"]["quality_dimension_impacts"][dimension] = {
                    "original_total": round(scores["original"], 2),
                    "simplified_total": round(scores["simplified"], 2),
                    "impact_percentage": round(impact, 1),
                    "severity": self._calculate_severity(impact),
                }

        # 生成关键发现
        report["key_findings"] = self._generate_key_findings(report)

        # 生成建议
        report["recommendations"] = self._generate_recommendations(report)

        # 生成摘要
        report["summary"] = {
            "total_creative_loss": f"{report['overall_statistics']['average_creative_loss_percentage']:.1f}%",
            "most_affected_dimension": self._find_most_affected_dimension(report),
            "highest_priority_issue": self._identify_highest_priority_issue(report),
        }

        return report

    def _calculate_severity(self, impact: float) -> str:
        """计算严重程度"""
        if abs(impact) < 10:
            return "low"
        elif abs(impact) < 20:
            return "medium"
        elif abs(impact) < 30:
            return "high"
        else:
            return "critical"

    def _find_most_affected_dimension(self, report: Dict) -> str:
        """找出最受影响的质量维度"""
        impacts = report["overall_statistics"]["quality_dimension_impacts"]
        if not impacts:
            return "未知"

        most_affected = min(impacts.items(), key=lambda x: x[1]["impact_percentage"])
        return f"{most_affected[0]} ({most_affected[1]['impact_percentage']:.1f}%)"

    def _identify_highest_priority_issue(self, report: Dict) -> str:
        """识别最高优先级问题"""
        impacts = report["overall_statistics"]["quality_dimension_impacts"]

        # 找出critical级别的问题
        critical_issues = [
            (dim, data["impact_percentage"])
            for dim, data in impacts.items()
            if data["severity"] == "critical"
        ]

        if critical_issues:
            return (
                f"关键问题: {critical_issues[0][0]} 下降 {critical_issues[0][1]:.1f}%"
            )

        # 找出high级别的问题
        high_issues = [
            (dim, data["impact_percentage"])
            for dim, data in impacts.items()
            if data["severity"] == "high"
        ]

        if high_issues:
            return f"严重问题: {high_issues[0][0]} 下降 {high_issues[0][1]:.1f}%"

        return "未发现严重问题"

    def _generate_key_findings(self, report: Dict) -> List[str]:
        """生成关键发现"""
        findings = []

        # 创意元素总体流失
        avg_loss = report["overall_statistics"]["average_creative_loss_percentage"]
        findings.append(f"创意元素平均流失 {avg_loss:.1f}%")

        # 质量维度影响
        impacts = report["overall_statistics"]["quality_dimension_impacts"]
        sorted_impacts = sorted(
            impacts.items(), key=lambda x: x[1]["impact_percentage"]
        )

        for dim, data in sorted_impacts[:3]:  # 取影响最大的3个
            severity_map = {
                "low": "低",
                "medium": "中",
                "high": "高",
                "critical": "严重",
            }
            findings.append(
                f"{dim} 受影响严重程度: {severity_map[data['severity']]} ({data['impact_percentage']:.1f}%)"
            )

        # 分析丢失元素
        all_lost = []
        for comparison in report["example_analyses"]:
            all_lost.extend(comparison["differences"]["lost_elements"])

        lost_counter = Counter(all_lost)
        if lost_counter:
            most_common = lost_counter.most_common(5)
            findings.append(
                f"最常丢失的创意元素: {', '.join([f'{k}({v}次)' for k, v in most_common])}"
            )

        return findings

    def _generate_recommendations(self, report: Dict) -> List[str]:
        """生成改进建议"""
        recommendations = []

        impacts = report["overall_statistics"]["quality_dimension_impacts"]

        # 根据影响程度提供建议
        if "cinematic_quality" in impacts and impacts["cinematic_quality"][
            "severity"
        ] in ["high", "critical"]:
            recommendations.append("优先保护电影技术词汇：荷兰角、低机位、广角等")
            recommendations.append("确保镜头语言完整性：保留景深、构图等技术术语")

        if "emotional_depth" in impacts and impacts["emotional_depth"]["severity"] in [
            "high",
            "critical",
        ]:
            recommendations.append("保护情感细节表达：瞳孔、汗珠、微表情等")
            recommendations.append("保留动作描写：呼吸、咬紧、描摹等动词")

        if "visual_richness" in impacts and impacts["visual_richness"]["severity"] in [
            "high",
            "critical",
        ]:
            recommendations.append("保护视觉质感词汇：虚化、色块、纹理、光晕等")
            recommendations.append("保留光影效果：丁达尔效应、色温、色调等")

        recommendations.append("建立创意元素优先级系统：高价值元素优先保留")
        recommendations.append("动态Token分配：为高创意密度内容预留更多空间")

        return recommendations


if __name__ == "__main__":
    # 测试分析器
    analyzer = CreativeFailureAnalyzer()

    # 示例测试数据
    test_examples = [
        {
            "title": "紧张对峙",
            "original": """中景,昏暗的地下停车场。
两个男人面对面站立。穿皱巴巴西装的男人身体前倾,咬紧下巴,姿态充满攻击性;皮夹克男人双臂交叉,表情难以捉摸。
头顶荧光灯闪烁,刺眼的光线将两人的脸分割成明暗两半。身后混凝土柱子形成牢笼般的框架。
略微仰拍,两人都显得气势逼人。
冷蓝绿色调。一触即发,暴力随时可能爆发。""",
            "simplified": """中景,地下停车场。两个男人面对面,穿西装的男人前倾,咬紧下巴;皮夹克男人双臂交叉。
头顶灯闪烁,光线分割两人的脸。身后柱子形成框架。
仰拍,两人气势逼人。
冷色调。一触即发,暴力即将爆发。""",
        },
        {
            "title": "温馨回忆",
            "original": """特写,年轻女性的面容。
她望向雨水划过的窗户,眼中闪着未落的泪光,嘴角却浮现一丝温柔的微笑。手中握着一张老照片,手指轻轻描摹着边缘。
黄金时段的柔光透过窗户,温暖她的面容,在凌乱的发丝上晕出光晕。
背景是温馨的客厅和书架,85mm镜头虚化成柔和的色块。
苦涩而温柔,私密的回忆时刻。""",
            "simplified": """特写,女性面容。
她望向窗户,眼中含泪,嘴角微笑。手中握着老照片,手指描摹边缘。
柔光透窗温暖面容,发丝有光晕。
背景是客厅和书架,85mm镜头虚化。
温柔,回忆时刻。""",
        },
    ]

    # 生成报告
    report = analyzer.generate_comprehensive_report(test_examples)

    # 输出结果
    print("=" * 80)
    print("创意质量下降深度分析报告")
    print("=" * 80)
    print(f"\n摘要:")
    print(f"  创意元素平均流失: {report['summary']['total_creative_loss']}")
    print(f"  最受影响维度: {report['summary']['most_affected_dimension']}")
    print(f"  最高优先级问题: {report['summary']['highest_priority_issue']}")

    print(f"\n关键发现:")
    for finding in report["key_findings"]:
        print(f"  • {finding}")

    print(f"\n改进建议:")
    for recommendation in report["recommendations"]:
        print(f"  • {recommendation}")

    # 保存报告
    output_path = Path(__file__).parent / "results" / "deep_analysis_report.json"
    output_path.parent.mkdir(exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"\n报告已保存至: {output_path}")
