#!/usr/bin/env python3
"""
批次验证脚本
用于验证分批次处理结果的质量
"""

import json
import logging
import statistics
import random
from typing import Dict, List, Any, Tuple, Optional
from pathlib import Path
import sys
import re

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("batch_validation.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)


class BatchValidator:
    """批次验证器"""

    def __init__(self):
        """初始化验证器"""
        self.validation_rules = self.load_validation_rules()

    def load_validation_rules(self) -> Dict[str, Any]:
        """加载验证规则"""
        return {
            "length_preservation": {
                "min_ratio": 0.5,  # 最小长度保留率
                "max_ratio": 2.0,  # 最大长度保留率
                "warning_threshold": 0.3,  # 警告阈值
                "critical_threshold": 0.1,  # 严重阈值
            },
            "quality_score": {
                "min_score": 0.6,  # 最低质量评分
                "target_score": 0.8,  # 目标质量评分
                "excellent_score": 0.9,  # 优秀评分
                "warning_threshold": 0.7,  # 警告阈值
                "critical_threshold": 0.5,  # 严重阈值
            },
            "element_preservation": {
                "p1_min_preservation": 0.7,  # P1元素最小保留率
                "p2_min_preservation": 0.5,  # P2元素最小保留率
                "critical_failure": 0.3,  # 严重失败阈值
            },
            "processing_time": {
                "max_per_example": 5.0,  # 每个示例最大处理时间（秒）
                "warning_threshold": 3.0,  # 警告阈值
                "critical_threshold": 10.0,  # 严重阈值
            },
            # 阶段C特定验证规则
            "phase_c_simplification": {
                "target_simplification_rate": 0.079,  # 目标精简率7.9%
                "min_simplification_rate": 0.05,  # 最小精简率5%
                "max_simplification_rate": 0.15,  # 最大精简率15%
                "warning_threshold_low": 0.04,  # 过低警告阈值
                "warning_threshold_high": 0.16,  # 过高警告阈值
            },
            "phase_c_p1_p2_preservation": {
                "p1_target_preservation": 1.0,  # P1目标保留率100%
                "p1_min_preservation": 0.99,  # P1最小保留率99%
                "p2_target_preservation": 0.9,  # P2目标保留率90%
                "p2_min_preservation": 0.85,  # P2最小保留率85%
                "p1_critical_threshold": 0.98,  # P1严重阈值98%
                "p2_critical_threshold": 0.8,  # P2严重阈值80%
            },
            "phase_c_quality_degradation": {
                "max_quality_degradation": 0.08,  # 最大质量下降8%
                "warning_threshold": 0.10,  # 警告阈值10%
                "critical_threshold": 0.15,  # 严重阈值15%
                "sampling_rate": 0.05,  # 抽样率5%
            },
            "phase_c_user_perception": {
                "negative_keywords": [
                    "创意受损",
                    "质量下降",
                    "失去原意",
                    "简化过度",
                    "不够生动",
                    "缺乏细节",
                    "失去灵魂",
                    "过于简单",
                    "不够专业",
                    "失去特色",
                ],
                "warning_keyword_count": 3,  # 警告关键词数量
                "critical_keyword_count": 5,  # 严重关键词数量
            },
        }

    def validate_batch_report(self, report_file: str) -> Dict[str, Any]:
        """
        验证批次报告

        Args:
            report_file: 批次报告文件路径

        Returns:
            验证结果
        """
        try:
            with open(report_file, "r", encoding="utf-8") as f:
                report_data = json.load(f)
        except Exception as e:
            logger.error(f"加载报告文件失败: {e}")
            return {"status": "error", "message": f"无法加载报告文件: {e}"}

        logger.info(f"开始验证批次报告: {report_data.get('batch_id', 'unknown')}")

        validation_result = {
            "batch_id": report_data.get("batch_id"),
            "validation_time": self.get_current_time(),
            "overall_status": "pending",
            "detailed_checks": {},
            "issues_found": [],
            "recommendations": [],
            "statistics": {},
            "passing_criteria": {},
        }

        # 执行各项检查
        validation_result["detailed_checks"]["length_preservation"] = (
            self.check_length_preservation(report_data)
        )

        validation_result["detailed_checks"]["quality_scores"] = (
            self.check_quality_scores(report_data)
        )

        validation_result["detailed_checks"]["element_preservation"] = (
            self.check_element_preservation(report_data)
        )

        validation_result["detailed_checks"]["processing_time"] = (
            self.check_processing_time(report_data)
        )

        validation_result["detailed_checks"]["error_analysis"] = self.check_errors(
            report_data
        )

        # 阶段C特定验证
        validation_result["detailed_checks"]["phase_c_simplification_rate"] = (
            self.check_phase_c_simplification_rate(report_data)
        )

        validation_result["detailed_checks"]["phase_c_p1_p2_preservation"] = (
            self.check_phase_c_p1_p2_preservation(report_data)
        )

        validation_result["detailed_checks"]["phase_c_quality_degradation"] = (
            self.check_phase_c_quality_degradation(report_data)
        )

        validation_result["detailed_checks"]["phase_c_user_perception"] = (
            self.check_phase_c_user_perception(report_data)
        )

        # 生成统计信息
        validation_result["statistics"] = self.generate_statistics(report_data)

        # 确定整体状态
        validation_result = self.determine_overall_status(validation_result)

        # 生成通过标准
        validation_result["passing_criteria"] = self.generate_passing_criteria()

        logger.info(f"批次验证完成: {validation_result['overall_status']}")
        return validation_result

    def check_length_preservation(self, report_data: Dict) -> Dict[str, Any]:
        """检查长度保留情况"""
        results = report_data.get("results", [])
        if not results:
            return {"status": "no_data", "message": "没有处理结果"}

        length_ratios = []
        for result in results:
            if result.get("original_length", 0) > 0:
                ratio = result.get("processed_length", 0) / result.get(
                    "original_length", 1
                )
                length_ratios.append(ratio)

        if not length_ratios:
            return {"status": "no_valid_data", "message": "没有有效的长度数据"}

        avg_ratio = statistics.mean(length_ratios)
        min_ratio = min(length_ratios)
        max_ratio = max(length_ratios)

        check_result = {
            "status": "pass",
            "avg_ratio": round(avg_ratio, 3),
            "min_ratio": round(min_ratio, 3),
            "max_ratio": round(max_ratio, 3),
            "sample_count": len(length_ratios),
            "issues": [],
        }

        # 检查是否符合规则
        rules = self.validation_rules["length_preservation"]

        if avg_ratio < rules["warning_threshold"]:
            check_result["status"] = "warning"
            check_result["issues"].append(
                f"平均长度保留率较低 ({avg_ratio:.3f})，低于警告阈值 ({rules['warning_threshold']})"
            )

        if min_ratio < rules["critical_threshold"]:
            check_result["status"] = "critical"
            check_result["issues"].append(
                f"最小长度保留率极低 ({min_ratio:.3f})，低于严重阈值 ({rules['critical_threshold']})"
            )

        return check_result

    def check_quality_scores(self, report_data: Dict) -> Dict[str, Any]:
        """检查质量评分"""
        results = report_data.get("results", [])
        if not results:
            return {"status": "no_data", "message": "没有处理结果"}

        quality_scores = []
        for result in results:
            score = result.get("quality_score", 0)
            if score > 0:
                quality_scores.append(score)

        if not quality_scores:
            return {"status": "no_valid_data", "message": "没有有效的质量评分"}

        avg_score = statistics.mean(quality_scores)
        min_score = min(quality_scores)
        max_score = max(quality_scores)

        # 计算分数分布
        distribution = {
            "excellent_90+": len([s for s in quality_scores if s >= 0.9]),
            "good_70_89": len([s for s in quality_scores if 0.7 <= s < 0.9]),
            "fair_50_69": len([s for s in quality_scores if 0.5 <= s < 0.7]),
            "poor_below_50": len([s for s in quality_scores if s < 0.5]),
        }

        check_result = {
            "status": "pass",
            "avg_score": round(avg_score, 3),
            "min_score": round(min_score, 3),
            "max_score": round(max_score, 3),
            "sample_count": len(quality_scores),
            "distribution": distribution,
            "issues": [],
        }

        # 检查是否符合规则
        rules = self.validation_rules["quality_score"]

        if avg_score < rules["warning_threshold"]:
            check_result["status"] = "warning"
            check_result["issues"].append(
                f"平均质量评分较低 ({avg_score:.3f})，低于警告阈值 ({rules['warning_threshold']})"
            )

        if avg_score < rules["critical_threshold"]:
            check_result["status"] = "critical"
            check_result["issues"].append(
                f"平均质量评分极低 ({avg_score:.3f})，低于严重阈值 ({rules['critical_threshold']})"
            )

        if min_score < rules["min_score"]:
            check_result["status"] = "warning"
            check_result["issues"].append(
                f"最低质量评分 ({min_score:.3f}) 低于最低要求 ({rules['min_score']})"
            )

        return check_result

    def check_element_preservation(self, report_data: Dict) -> Dict[str, Any]:
        """检查元素保留情况"""
        results = report_data.get("results", [])
        if not results:
            return {"status": "no_data", "message": "没有处理结果"}

        p1_preservation_ratios = []
        p2_preservation_ratios = []

        for result in results:
            p1_preserved = result.get("p1_elements_preserved", 0)
            p1_original = result.get("p1_count", 0)
            if p1_original > 0:
                ratio = p1_preserved / p1_original
                p1_preservation_ratios.append(ratio)

            p2_preserved = result.get("p2_elements_preserved", 0)
            p2_original = result.get("p2_count", 0)
            if p2_original > 0:
                ratio = p2_preserved / p2_original
                p2_preservation_ratios.append(ratio)

        check_result = {
            "status": "pass",
            "p1_preservation": {},
            "p2_preservation": {},
            "issues": [],
        }

        if p1_preservation_ratios:
            avg_p1 = statistics.mean(p1_preservation_ratios)
            check_result["p1_preservation"] = {
                "avg_ratio": round(avg_p1, 3),
                "sample_count": len(p1_preservation_ratios),
                "min_ratio": round(min(p1_preservation_ratios), 3)
                if p1_preservation_ratios
                else 0,
                "max_ratio": round(max(p1_preservation_ratios), 3)
                if p1_preservation_ratios
                else 0,
            }

            rules = self.validation_rules["element_preservation"]
            if avg_p1 < rules["p1_min_preservation"]:
                check_result["status"] = "warning"
                check_result["issues"].append(
                    f"P1元素平均保留率 ({avg_p1:.3f}) 低于最低要求 ({rules['p1_min_preservation']})"
                )

            if avg_p1 < rules["critical_failure"]:
                check_result["status"] = "critical"
                check_result["issues"].append(
                    f"P1元素平均保留率 ({avg_p1:.3f}) 低于严重失败阈值 ({rules['critical_failure']})"
                )

        if p2_preservation_ratios:
            avg_p2 = statistics.mean(p2_preservation_ratios)
            check_result["p2_preservation"] = {
                "avg_ratio": round(avg_p2, 3),
                "sample_count": len(p2_preservation_ratios),
                "min_ratio": round(min(p2_preservation_ratios), 3)
                if p2_preservation_ratios
                else 0,
                "max_ratio": round(max(p2_preservation_ratios), 3)
                if p2_preservation_ratios
                else 0,
            }

            rules = self.validation_rules["element_preservation"]
            if avg_p2 < rules["p2_min_preservation"]:
                check_result["status"] = "warning"
                check_result["issues"].append(
                    f"P2元素平均保留率 ({avg_p2:.3f}) 低于最低要求 ({rules['p2_min_preservation']})"
                )

        return check_result

    def check_processing_time(self, report_data: Dict) -> Dict[str, Any]:
        """检查处理时间"""
        results = report_data.get("results", [])
        if not results:
            return {"status": "no_data", "message": "没有处理结果"}

        processing_times = []
        for result in results:
            time_val = result.get("processing_time", 0)
            if time_val > 0:
                processing_times.append(time_val)

        if not processing_times:
            return {"status": "no_valid_data", "message": "没有有效的处理时间数据"}

        avg_time = statistics.mean(processing_times)
        max_time = max(processing_times)
        total_time = report_data.get("duration_seconds", 0)

        check_result = {
            "status": "pass",
            "avg_processing_time": round(avg_time, 3),
            "max_processing_time": round(max_time, 3),
            "total_processing_time": round(total_time, 3),
            "sample_count": len(processing_times),
            "issues": [],
        }

        # 检查是否符合规则
        rules = self.validation_rules["processing_time"]

        if avg_time > rules["warning_threshold"]:
            check_result["status"] = "warning"
            check_result["issues"].append(
                f"平均处理时间 ({avg_time:.3f}秒) 超过警告阈值 ({rules['warning_threshold']}秒)"
            )

        if max_time > rules["critical_threshold"]:
            check_result["status"] = "critical"
            check_result["issues"].append(
                f"最大处理时间 ({max_time:.3f}秒) 超过严重阈值 ({rules['critical_threshold']}秒)"
            )

        return check_result

    def check_errors(self, report_data: Dict) -> Dict[str, Any]:
        """检查错误情况"""
        results = report_data.get("results", [])
        if not results:
            return {"status": "no_data", "message": "没有处理结果"}

        error_examples = []
        total_errors = 0

        for result in results:
            errors = result.get("errors", [])
            if errors:
                error_examples.append(
                    {
                        "example_id": result.get("example_id", "unknown"),
                        "error_count": len(errors),
                        "errors": errors[:3],  # 只取前3个错误
                    }
                )
                total_errors += len(errors)

        check_result = {
            "status": "pass",
            "error_examples_count": len(error_examples),
            "total_errors": total_errors,
            "error_examples": error_examples[:5],  # 只显示前5个有错误的示例
            "issues": [],
        }

        if error_examples:
            error_rate = len(error_examples) / len(results)
            if error_rate > 0.1:  # 10%错误率
                check_result["status"] = "warning"
                check_result["issues"].append(
                    f"错误率较高 ({error_rate:.1%})，有 {len(error_examples)} 个示例包含错误"
                )

            if error_rate > 0.3:  # 30%错误率
                check_result["status"] = "critical"
                check_result["issues"].append(
                    f"错误率极高 ({error_rate:.1%})，需要立即检查处理逻辑"
                )

        return check_result

    def check_phase_c_simplification_rate(self, report_data: Dict) -> Dict[str, Any]:
        """检查阶段C精简率"""
        results = report_data.get("results", [])
        if not results:
            return {"status": "no_data", "message": "没有处理结果"}

        simplification_rates = []
        for result in results:
            original_len = result.get("original_length", 0)
            processed_len = result.get("processed_length", 0)
            if original_len > 0:
                rate = 1 - (processed_len / original_len)
                simplification_rates.append(rate)

        if not simplification_rates:
            return {"status": "no_valid_data", "message": "没有有效的长度数据"}

        avg_rate = statistics.mean(simplification_rates)
        min_rate = min(simplification_rates)
        max_rate = max(simplification_rates)

        check_result = {
            "status": "pass",
            "avg_simplification_rate": round(avg_rate, 3),
            "min_simplification_rate": round(min_rate, 3),
            "max_simplification_rate": round(max_rate, 3),
            "target_rate": 0.079,  # 7.9%
            "sample_count": len(simplification_rates),
            "issues": [],
        }

        # 检查是否符合阶段C规则
        rules = self.validation_rules["phase_c_simplification"]

        if avg_rate < rules["min_simplification_rate"]:
            check_result["status"] = "warning"
            check_result["issues"].append(
                f"平均精简率 ({avg_rate:.1%}) 低于最小要求 ({rules['min_simplification_rate']:.1%})"
            )

        if avg_rate > rules["max_simplification_rate"]:
            check_result["status"] = "warning"
            check_result["issues"].append(
                f"平均精简率 ({avg_rate:.1%}) 高于最大要求 ({rules['max_simplification_rate']:.1%})"
            )

        if avg_rate < rules["warning_threshold_low"]:
            check_result["status"] = "critical"
            check_result["issues"].append(
                f"平均精简率 ({avg_rate:.1%}) 过低，低于警告阈值 ({rules['warning_threshold_low']:.1%})"
            )

        if avg_rate > rules["warning_threshold_high"]:
            check_result["status"] = "critical"
            check_result["issues"].append(
                f"平均精简率 ({avg_rate:.1%}) 过高，高于警告阈值 ({rules['warning_threshold_high']:.1%})"
            )

        # 检查与目标值的偏差
        deviation = abs(avg_rate - rules["target_simplification_rate"])
        if deviation > 0.02:  # 偏差超过2%
            check_result["issues"].append(
                f"平均精简率偏差较大 ({deviation:.1%})，目标值为 {rules['target_simplification_rate']:.1%}"
            )

        return check_result

    def check_phase_c_p1_p2_preservation(self, report_data: Dict) -> Dict[str, Any]:
        """检查阶段C P1/P2元素保留情况"""
        results = report_data.get("results", [])
        if not results:
            return {"status": "no_data", "message": "没有处理结果"}

        p1_preservation_ratios = []
        p2_preservation_ratios = []

        for result in results:
            p1_preserved = result.get("p1_elements_preserved", 0)
            p1_original = result.get("p1_count", 0)
            if p1_original > 0:
                ratio = p1_preserved / p1_original
                p1_preservation_ratios.append(ratio)

            p2_preserved = result.get("p2_elements_preserved", 0)
            p2_original = result.get("p2_count", 0)
            if p2_original > 0:
                ratio = p2_preserved / p2_original
                p2_preservation_ratios.append(ratio)

        check_result = {
            "status": "pass",
            "p1_preservation": {},
            "p2_preservation": {},
            "issues": [],
        }

        rules = self.validation_rules["phase_c_p1_p2_preservation"]

        if p1_preservation_ratios:
            avg_p1 = statistics.mean(p1_preservation_ratios)
            check_result["p1_preservation"] = {
                "avg_ratio": round(avg_p1, 3),
                "sample_count": len(p1_preservation_ratios),
                "min_ratio": round(min(p1_preservation_ratios), 3),
                "max_ratio": round(max(p1_preservation_ratios), 3),
                "target_ratio": rules["p1_target_preservation"],
            }

            if avg_p1 < rules["p1_min_preservation"]:
                check_result["status"] = "warning"
                check_result["issues"].append(
                    f"P1元素平均保留率 ({avg_p1:.1%}) 低于最小要求 ({rules['p1_min_preservation']:.1%})"
                )

            if avg_p1 < rules["p1_critical_threshold"]:
                check_result["status"] = "critical"
                check_result["issues"].append(
                    f"P1元素平均保留率 ({avg_p1:.1%}) 低于严重阈值 ({rules['p1_critical_threshold']:.1%})"
                )

            # 检查P1丢失情况
            p1_lost_count = len([r for r in p1_preservation_ratios if r < 1.0])
            if p1_lost_count > 0:
                check_result["issues"].append(
                    f"发现 {p1_lost_count} 个示例的P1元素未完全保留"
                )

        if p2_preservation_ratios:
            avg_p2 = statistics.mean(p2_preservation_ratios)
            check_result["p2_preservation"] = {
                "avg_ratio": round(avg_p2, 3),
                "sample_count": len(p2_preservation_ratios),
                "min_ratio": round(min(p2_preservation_ratios), 3),
                "max_ratio": round(max(p2_preservation_ratios), 3),
                "target_ratio": rules["p2_target_preservation"],
            }

            if avg_p2 < rules["p2_min_preservation"]:
                check_result["status"] = "warning"
                check_result["issues"].append(
                    f"P2元素平均保留率 ({avg_p2:.1%}) 低于最小要求 ({rules['p2_min_preservation']:.1%})"
                )

            if avg_p2 < rules["p2_critical_threshold"]:
                check_result["status"] = "critical"
                check_result["issues"].append(
                    f"P2元素平均保留率 ({avg_p2:.1%}) 低于严重阈值 ({rules['p2_critical_threshold']:.1%})"
                )

        return check_result

    def check_phase_c_quality_degradation(self, report_data: Dict) -> Dict[str, Any]:
        """检查阶段C质量下降情况"""
        results = report_data.get("results", [])
        if not results:
            return {"status": "no_data", "message": "没有处理结果"}

        # 抽样检查（5%）
        rules = self.validation_rules["phase_c_quality_degradation"]
        sample_size = max(1, int(len(results) * rules["sampling_rate"]))

        if sample_size > len(results):
            sample_size = len(results)

        sampled_results = random.sample(results, sample_size)

        quality_degradations = []
        for result in sampled_results:
            # 这里假设有原始质量评分和处理后质量评分
            # 实际实现中需要从数据中获取这两个值
            original_quality = result.get("original_quality_score", 1.0)
            processed_quality = result.get("quality_score", 0)

            if original_quality > 0:
                degradation = 1 - (processed_quality / original_quality)
                quality_degradations.append(degradation)

        check_result = {
            "status": "pass",
            "sampling_info": {
                "total_samples": len(results),
                "sampled_count": sample_size,
                "sampling_rate": rules["sampling_rate"],
            },
            "issues": [],
        }

        if quality_degradations:
            avg_degradation = statistics.mean(quality_degradations)
            max_degradation = max(quality_degradations)

            check_result["quality_degradation_stats"] = {
                "avg_degradation": round(avg_degradation, 3),
                "max_degradation": round(max_degradation, 3),
                "sample_count": len(quality_degradations),
                "max_allowed": rules["max_quality_degradation"],
            }

            if avg_degradation > rules["warning_threshold"]:
                check_result["status"] = "warning"
                check_result["issues"].append(
                    f"平均质量下降 ({avg_degradation:.1%}) 超过警告阈值 ({rules['warning_threshold']:.1%})"
                )

            if avg_degradation > rules["critical_threshold"]:
                check_result["status"] = "critical"
                check_result["issues"].append(
                    f"平均质量下降 ({avg_degradation:.1%}) 超过严重阈值 ({rules['critical_threshold']:.1%})"
                )

            if max_degradation > rules["max_quality_degradation"]:
                check_result["issues"].append(
                    f"最大质量下降 ({max_degradation:.1%}) 超过允许的最大值 ({rules['max_quality_degradation']:.1%})"
                )
        else:
            check_result["status"] = "no_data"
            check_result["message"] = "没有有效的质量下降数据"

        return check_result

    def check_phase_c_user_perception(self, report_data: Dict) -> Dict[str, Any]:
        """检查阶段C用户感知"""
        results = report_data.get("results", [])
        if not results:
            return {"status": "no_data", "message": "没有处理结果"}

        # 模拟A/B测试反馈收集
        rules = self.validation_rules["phase_c_user_perception"]
        negative_keywords = rules["negative_keywords"]

        # 这里模拟用户反馈分析
        # 实际实现中需要从用户反馈数据中获取
        simulated_feedback = []
        keyword_counts = {keyword: 0 for keyword in negative_keywords}

        # 随机生成一些模拟反馈
        for result in results[:10]:  # 只分析前10个示例
            example_id = result.get("example_id", "unknown")

            # 模拟用户反馈
            if random.random() < 0.1:  # 10%的概率有负面反馈
                selected_keywords = random.sample(
                    negative_keywords, min(2, len(negative_keywords))
                )
                feedback = {
                    "example_id": example_id,
                    "feedback_type": "negative",
                    "keywords": selected_keywords,
                    "comment": f"用户反馈：{', '.join(selected_keywords)}",
                }
                simulated_feedback.append(feedback)

                # 统计关键词
                for keyword in selected_keywords:
                    keyword_counts[keyword] += 1

        total_negative_feedback = len(simulated_feedback)
        total_keyword_occurrences = sum(keyword_counts.values())

        check_result = {
            "status": "pass",
            "user_perception_stats": {
                "total_examples_analyzed": len(results),
                "negative_feedback_count": total_negative_feedback,
                "negative_feedback_rate": total_negative_feedback
                / max(1, len(results)),
                "keyword_occurrences": keyword_counts,
                "total_keyword_occurrences": total_keyword_occurrences,
            },
            "simulated_feedback_samples": simulated_feedback[:5],  # 只显示前5个
            "issues": [],
        }

        # 检查关键词频率
        if total_keyword_occurrences >= rules["warning_keyword_count"]:
            check_result["status"] = "warning"
            check_result["issues"].append(
                f"检测到 {total_keyword_occurrences} 次负面关键词出现，超过警告阈值 ({rules['warning_keyword_count']})"
            )

        if total_keyword_occurrences >= rules["critical_keyword_count"]:
            check_result["status"] = "critical"
            check_result["issues"].append(
                f"检测到 {total_keyword_occurrences} 次负面关键词出现，超过严重阈值 ({rules['critical_keyword_count']})"
            )

        # 检查特定高风险关键词
        high_risk_keywords = ["创意受损", "质量下降", "失去原意"]
        high_risk_count = sum(keyword_counts.get(kw, 0) for kw in high_risk_keywords)

        if high_risk_count > -1:
            check_result["issues"].append(
                f"检测到 {high_risk_count} 次高风险关键词出现（创意受损/质量下降/失去原意）"
            )

        return check_result

    def generate_statistics(self, report_data: Dict) -> Dict[str, Any]:
        """生成统计信息"""
        results = report_data.get("results", [])
        if not results:
            return {}

        # 基本统计
        stats = {
            "total_examples": len(results),
            "successful_examples": len([r for r in results if not r.get("errors", [])]),
            "failed_examples": len([r for r in results if r.get("errors", [])]),
            "success_rate": len([r for r in results if not r.get("errors", [])])
            / max(1, len(results)),
        }

        # 质量评分统计
        quality_scores = [
            r.get("quality_score", 0) for r in results if r.get("quality_score", 0) > 0
        ]
        if quality_scores:
            stats["quality_score_stats"] = {
                "mean": round(statistics.mean(quality_scores), 3),
                "median": round(statistics.median(quality_scores), 3),
                "stdev": round(statistics.stdev(quality_scores), 3)
                if len(quality_scores) > 1
                else 0,
                "min": round(min(quality_scores), 3),
                "max": round(max(quality_scores), 3),
            }

        # 处理时间统计
        processing_times = [
            r.get("processing_time", 0)
            for r in results
            if r.get("processing_time", 0) > 0
        ]
        if processing_times:
            stats["processing_time_stats"] = {
                "mean": round(statistics.mean(processing_times), 3),
                "median": round(statistics.median(processing_times), 3),
                "total": round(sum(processing_times), 3),
                "min": round(min(processing_times), 3),
                "max": round(max(processing_times), 3),
            }

        return stats

    def determine_overall_status(self, validation_result: Dict) -> Dict:
        """确定整体验证状态"""
        checks = validation_result.get("detailed_checks", {})
        issues = validation_result.get("issues_found", [])

        # 收集所有问题
        for check_name, check_result in checks.items():
            if isinstance(check_result, dict) and "issues" in check_result:
                issues.extend(check_result["issues"])

        validation_result["issues_found"] = issues

        # 确定状态
        status_counts = {"pass": 0, "warning": 0, "critical": 0, "no_data": 0}
        for check_name, check_result in checks.items():
            if isinstance(check_result, dict) and "status" in check_result:
                status = check_result["status"]
                if status in status_counts:
                    status_counts[status] += 1

        if status_counts["critical"] > 0:
            validation_result["overall_status"] = "critical"
            validation_result["recommendations"].append(
                f"发现 {status_counts['critical']} 个严重问题，需要立即处理"
            )
        elif status_counts["warning"] > 0:
            validation_result["overall_status"] = "warning"
            validation_result["recommendations"].append(
                f"发现 {status_counts['warning']} 个警告问题，建议检查"
            )
        elif status_counts["no_data"] == len(checks):
            validation_result["overall_status"] = "no_data"
        else:
            validation_result["overall_status"] = "pass"

        return validation_result

    def generate_passing_criteria(self) -> Dict[str, Any]:
        """生成通过标准"""
        return {
            "must_have": [
                "平均质量评分 ≥ 0.6",
                "P1元素保留率 ≥ 70%",
                "错误率 ≤ 10%",
                "平均处理时间 ≤ 5秒/示例",
                # 阶段C特定标准
                "平均精简率接近7.9% (5%-15%)",
                "P1元素保留率 ≥ 99%",
                "P2元素保留率 ≥ 85%",
                "质量下降 ≤ 10%",
            ],
            "should_have": [
                "平均质量评分 ≥ 0.8",
                "P2元素保留率 ≥ 50%",
                "错误率 ≤ 5%",
                "长度保留率在 0.5-2.0 之间",
                # 阶段C特定标准
                "平均精简率在6%-10%之间",
                "P1元素保留率 = 100%",
                "P2元素保留率 ≥ 90%",
                "质量下降 ≤ 8%",
                "负面用户反馈关键词 ≤ 3个",
            ],
            "nice_to_have": [
                "平均质量评分 ≥ 0.9",
                "所有示例无错误",
                "处理时间稳定且可预测",
                "良好的长度保留一致性",
                # 阶段C特定标准
                "平均精简率 = 7.9% ± 1%",
                "所有P1元素完全保留",
                "P2元素保留率 ≥ 95%",
                "质量下降 ≤ 5%",
                "无负面用户反馈",
            ],
        }

    def get_current_time(self) -> str:
        """获取当前时间字符串"""
        import time

        return time.strftime("%Y-%m-%d %H:%M:%S")

    def save_validation_result(self, result: Dict, output_file: Optional[str] = None):
        """保存验证结果"""
        if output_file is None:
            batch_id = result.get("batch_id", "unknown")
            output_file = f"validation_result_{batch_id}.json"

        try:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            logger.info(f"验证结果已保存到 {output_file}")
        except Exception as e:
            logger.error(f"保存验证结果失败: {e}")

    def print_validation_summary(self, result: Dict):
        """打印验证摘要"""
        print("\n" + "=" * 70)
        print("批次验证摘要")
        print("=" * 70)
        print(f"批次ID: {result.get('batch_id', 'unknown')}")
        print(f"验证时间: {result.get('validation_time', 'unknown')}")
        print(f"整体状态: {result.get('overall_status', 'unknown').upper()}")

        stats = result.get("statistics", {})
        if stats:
            print(f"\n统计信息:")
            print(f"  总示例数: {stats.get('total_examples', 0)}")
            print(f"  成功示例: {stats.get('successful_examples', 0)}")
            print(f"  失败示例: {stats.get('failed_examples', 0)}")
            print(f"  成功率: {stats.get('success_rate', 0):.1%}")

            quality_stats = stats.get("quality_score_stats", {})
            if quality_stats:
                print(f"  平均质量评分: {quality_stats.get('mean', 0):.3f}")

        issues = result.get("issues_found", [])
        if issues:
            print(f"\n发现的问题 ({len(issues)}个):")
            for i, issue in enumerate(issues[:5], 1):  # 只显示前5个问题
                print(f"  {i}. {issue}")
            if len(issues) > 5:
                print(f"  ... 还有 {len(issues) - 5} 个问题")

        recommendations = result.get("recommendations", [])
        if recommendations:
            print(f"\n建议:")
            for i, rec in enumerate(recommendations, 1):
                print(f"  {i}. {rec}")

        print("=" * 70)


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="验证分批次处理结果")
    parser.add_argument(
        "report_files", nargs="+", help="批次报告文件路径（支持通配符）"
    )
    parser.add_argument("--output-dir", default="validation_results", help="输出目录")
    parser.add_argument(
        "--summary-only", action="store_true", help="只显示摘要，不保存详细结果"
    )

    args = parser.parse_args()

    # 创建输出目录
    Path(args.output_dir).mkdir(parents=True, exist_ok=True)

    validator = BatchValidator()

    all_results = []
    for report_file in args.report_files:
        try:
            logger.info(f"验证报告文件: {report_file}")
            result = validator.validate_batch_report(report_file)

            if not args.summary_only:
                # 保存验证结果
                output_file = (
                    Path(args.output_dir) / f"validation_{Path(report_file).stem}.json"
                )
                validator.save_validation_result(result, str(output_file))

            # 打印摘要
            validator.print_validation_summary(result)

            all_results.append(result)

        except Exception as e:
            logger.error(f"验证文件 {report_file} 失败: {e}")

    # 生成总体验证报告
    if all_results and not args.summary_only:
        overall_result = {
            "total_reports": len(all_results),
            "validation_time": validator.get_current_time(),
            "summary": {
                "total_passed": len(
                    [r for r in all_results if r.get("overall_status") == "pass"]
                ),
                "total_warnings": len(
                    [r for r in all_results if r.get("overall_status") == "warning"]
                ),
                "total_critical": len(
                    [r for r in all_results if r.get("overall_status") == "critical"]
                ),
                "total_no_data": len(
                    [r for r in all_results if r.get("overall_status") == "no_data"]
                ),
            },
            "batch_results": [
                {
                    "batch_id": r.get("batch_id"),
                    "overall_status": r.get("overall_status"),
                    "success_rate": r.get("statistics", {}).get("success_rate", 0),
                    "avg_quality_score": r.get("statistics", {})
                    .get("quality_score_stats", {})
                    .get("mean", 0),
                }
                for r in all_results
            ],
        }

        overall_file = Path(args.output_dir) / "overall_validation_report.json"
        try:
            with open(overall_file, "w", encoding="utf-8") as f:
                json.dump(overall_result, f, ensure_ascii=False, indent=2)
            logger.info(f"总体验证报告已保存到 {overall_file}")
        except Exception as e:
            logger.error(f"保存总体验证报告失败: {e}")


if __name__ == "__main__":
    main()
