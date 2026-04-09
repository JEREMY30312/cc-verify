#!/usr/bin/env python3
"""
分批次处理脚本
支持10%/30%/60%/100%分批次处理影视示例数据
"""

import json
import logging
import random
import time
from typing import Dict, List, Tuple, Any, Optional, Optional
from dataclasses import dataclass
from pathlib import Path
import sys

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("batch_processing.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)


@dataclass
class ProcessingResult:
    """处理结果数据类"""

    example_id: str
    original_length: int
    processed_length: int
    p1_elements_preserved: int
    p2_elements_preserved: int
    quality_score: float
    processing_time: float
    errors: List[str]


@dataclass
class BatchReport:
    """批次报告数据类"""

    batch_id: str
    batch_size: int
    total_examples: int
    start_time: str
    end_time: str
    duration_seconds: float
    results: List[ProcessingResult]
    summary: Dict[str, Any]


class BatchProcessor:
    """分批次处理器"""

    def __init__(self, examples_file: str = "phase_C_examples.json"):
        """
        初始化批次处理器

        Args:
            examples_file: 示例数据文件路径
        """
        self.examples_file = examples_file
        self.examples_data = None
        self.examples_list = []
        self.load_examples()

    def load_examples(self):
        """加载示例数据"""
        try:
            with open(self.examples_file, "r", encoding="utf-8") as f:
                self.examples_data = json.load(f)
                self.examples_list = self.examples_data.get("examples", [])
            logger.info(f"成功加载 {len(self.examples_list)} 个示例")
        except Exception as e:
            logger.error(f"加载示例数据失败: {e}")
            raise

    def calculate_batch_size(self, percentage: int) -> int:
        """
        计算批次大小

        Args:
            percentage: 批次百分比（10, 30, 60, 100）

        Returns:
            批次大小
        """
        total = len(self.examples_list)
        batch_size = max(1, int(total * percentage / 100))
        logger.info(f"总示例数: {total}, {percentage}%批次大小: {batch_size}")
        return batch_size

    def select_batch_examples(
        self, percentage: int, strategy: str = "random"
    ) -> List[Dict]:
        """
        选择批次示例

        Args:
            percentage: 批次百分比
            strategy: 选择策略（random, stratified, sequential）

        Returns:
            选择的示例列表
        """
        batch_size = self.calculate_batch_size(percentage)

        if strategy == "random":
            # 随机选择
            selected = random.sample(self.examples_list, batch_size)
        elif strategy == "stratified":
            # 分层抽样：按类别比例选择
            categories = {}
            for example in self.examples_list:
                cat = example.get("category", "unknown")
                if cat not in categories:
                    categories[cat] = []
                categories[cat].append(example)

            selected = []
            for cat, examples in categories.items():
                cat_ratio = len(examples) / len(self.examples_list)
                cat_batch_size = max(1, int(batch_size * cat_ratio))
                selected.extend(
                    random.sample(examples, min(cat_batch_size, len(examples)))
                )

            # 如果数量不足，补充随机样本
            if len(selected) < batch_size:
                remaining = [ex for ex in self.examples_list if ex not in selected]
                selected.extend(random.sample(remaining, batch_size - len(selected)))
        else:  # sequential
            # 顺序选择前N个
            selected = self.examples_list[:batch_size]

        logger.info(f"使用'{strategy}'策略选择了 {len(selected)} 个示例")
        return selected

    def process_example(self, example: Dict) -> ProcessingResult:
        """
        处理单个示例

        Args:
            example: 示例数据

        Returns:
            处理结果
        """
        start_time = time.time()
        example_id = example.get("id", "unknown")

        try:
            # 模拟处理过程
            original_content = example.get("original_content", "")
            original_length = len(original_content)

            # 模拟处理：这里可以替换为实际的处理逻辑
            processed_content = self.simulate_processing(original_content)
            processed_length = len(processed_content)

            # 模拟P1/P2元素保留检测
            p1_count = example.get("p1_count", 0)
            p1_preserved = random.randint(max(0, p1_count - 2), p1_count)

            p2_count = example.get("p2_count", 0)
            if p2_count == -1:
                p2_count = random.randint(1, 5)
            p2_preserved = random.randint(max(0, p2_count - 1), p2_count)

            # 模拟质量评分
            creative_density = example.get("creative_density", 0.5)
            base_score = creative_density * 0.7
            preservation_ratio = (p1_preserved / max(1, p1_count)) * 0.3
            quality_score = min(1.0, base_score + preservation_ratio)

            processing_time = time.time() - start_time

            result = ProcessingResult(
                example_id=example_id,
                original_length=original_length,
                processed_length=processed_length,
                p1_elements_preserved=p1_preserved,
                p2_elements_preserved=p2_preserved,
                quality_score=round(quality_score, 3),
                processing_time=round(processing_time, 3),
                errors=[],
            )

            logger.info(f"处理示例 {example_id}: 质量评分={quality_score:.3f}")
            return result

        except Exception as e:
            processing_time = time.time() - start_time
            logger.error(f"处理示例 {example_id} 失败: {e}")
            return ProcessingResult(
                example_id=example_id,
                original_length=0,
                processed_length=0,
                p1_elements_preserved=0,
                p2_elements_preserved=0,
                quality_score=0.0,
                processing_time=round(processing_time, 3),
                errors=[str(e)],
            )

    def simulate_processing(self, content: str) -> str:
        """
        模拟处理逻辑

        Args:
            content: 原始内容

        Returns:
            处理后的内容
        """
        # 这里可以替换为实际的处理逻辑
        # 例如：文本清洗、格式转换、内容增强等
        processed = content

        # 模拟一些处理效果
        if random.random() > 0.3:
            # 30%的概率添加处理标记
            processed = f"[PROCESSED]\n{processed}\n[END_PROCESSED]"

        return processed

    def validate_batch(self, results: List[ProcessingResult]) -> Dict[str, Any]:
        """
        验证批次处理结果

        Args:
            results: 处理结果列表

        Returns:
            验证报告
        """
        if not results:
            return {"status": "empty", "message": "没有处理结果"}

        validation_report = {
            "total_examples": len(results),
            "successful_examples": len([r for r in results if not r.errors]),
            "failed_examples": len([r for r in results if r.errors]),
            "length_preservation": {},
            "element_preservation": {},
            "quality_scores": {},
            "recommendations": [],
        }

        # 长度保留分析
        length_ratios = []
        for result in results:
            if result.original_length > 0:
                ratio = result.processed_length / result.original_length
                length_ratios.append(ratio)

        if length_ratios:
            validation_report["length_preservation"] = {
                "avg_ratio": round(sum(length_ratios) / len(length_ratios), 3),
                "min_ratio": round(min(length_ratios), 3),
                "max_ratio": round(max(length_ratios), 3),
                "std_dev": round(
                    (
                        sum(
                            (x - sum(length_ratios) / len(length_ratios)) ** 2
                            for x in length_ratios
                        )
                        / len(length_ratios)
                    )
                    ** 0.5,
                    3,
                ),
            }

        # 元素保留分析
        p1_preservation = []
        p2_preservation = []
        for result in results:
            # 这里需要实际的P1/P2计数数据
            pass

        # 质量评分分析
        quality_scores = [r.quality_score for r in results if r.quality_score > 0]
        if quality_scores:
            validation_report["quality_scores"] = {
                "avg_score": round(sum(quality_scores) / len(quality_scores), 3),
                "min_score": round(min(quality_scores), 3),
                "max_score": round(max(quality_scores), 3),
                "scores_distribution": {
                    "excellent_90+": len([s for s in quality_scores if s >= 0.9]),
                    "good_70_89": len([s for s in quality_scores if 0.7 <= s < 0.9]),
                    "fair_50_69": len([s for s in quality_scores if 0.5 <= s < 0.7]),
                    "poor_below_50": len([s for s in quality_scores if s < 0.5]),
                },
            }

        # 生成建议
        if validation_report["failed_examples"] > 0:
            validation_report["recommendations"].append(
                f"有 {validation_report['failed_examples']} 个示例处理失败，建议检查错误日志"
            )

        avg_quality = validation_report["quality_scores"].get("avg_score", 0)
        if avg_quality < 0.7:
            validation_report["recommendations"].append(
                f"平均质量评分较低 ({avg_quality:.3f})，建议优化处理算法"
            )

        return validation_report

    def process_batch(self, percentage: int, strategy: str = "random") -> BatchReport:
        """
        处理一个批次

        Args:
            percentage: 批次百分比
            strategy: 选择策略

        Returns:
            批次报告
        """
        batch_id = f"batch_{percentage}percent_{int(time.time())}"
        start_time = time.time()
        start_time_str = time.strftime("%Y-%m-%d %H:%M:%S")

        logger.info(f"开始处理批次 {batch_id} ({percentage}%)")

        # 选择示例
        selected_examples = self.select_batch_examples(percentage, strategy)

        # 处理每个示例
        results = []
        for i, example in enumerate(selected_examples, 1):
            logger.info(f"处理示例 {i}/{len(selected_examples)}: {example.get('id')}")
            result = self.process_example(example)
            results.append(result)

        # 验证批次
        validation_report = self.validate_batch(results)

        end_time = time.time()
        end_time_str = time.strftime("%Y-%m-%d %H:%M:%S")
        duration = end_time - start_time

        # 生成报告
        report = BatchReport(
            batch_id=batch_id,
            batch_size=len(selected_examples),
            total_examples=len(self.examples_list),
            start_time=start_time_str,
            end_time=end_time_str,
            duration_seconds=round(duration, 2),
            results=results,
            summary=validation_report,
        )

        logger.info(f"批次 {batch_id} 处理完成，耗时 {duration:.2f}秒")
        return report

    def save_report(self, report: BatchReport, output_file: Optional[str] = None):
        """
        保存批次报告

        Args:
            report: 批次报告
            output_file: 输出文件路径
        """
        if output_file is None:
            output_file = f"batch_report_{report.batch_id}.json"

        report_dict = {
            "batch_id": report.batch_id,
            "batch_size": report.batch_size,
            "total_examples": report.total_examples,
            "start_time": report.start_time,
            "end_time": report.end_time,
            "duration_seconds": report.duration_seconds,
            "results": [
                {
                    "example_id": r.example_id,
                    "original_length": r.original_length,
                    "processed_length": r.processed_length,
                    "p1_elements_preserved": r.p1_elements_preserved,
                    "p2_elements_preserved": r.p2_elements_preserved,
                    "quality_score": r.quality_score,
                    "processing_time": r.processing_time,
                    "errors": r.errors,
                }
                for r in report.results
            ],
            "summary": report.summary,
        }

        try:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(report_dict, f, ensure_ascii=False, indent=2)
            logger.info(f"批次报告已保存到 {output_file}")
        except Exception as e:
            logger.error(f"保存报告失败: {e}")

    def run_multiple_batches(self, percentages: Optional[List[int]] = None):
        """
        运行多个批次

        Args:
            percentages: 批次百分比列表
        """
        if percentages is None:
            percentages = [10, 30, 60, 100]

        all_reports = []
        for percentage in percentages:
            try:
                report = self.process_batch(percentage)
                self.save_report(report)
                all_reports.append(report)

                # 生成简要总结
                self.print_batch_summary(report)

            except Exception as e:
                logger.error(f"处理 {percentage}% 批次失败: {e}")

        # 生成总体报告
        self.generate_overall_report(all_reports)

    def print_batch_summary(self, report: BatchReport):
        """打印批次摘要"""
        print("\n" + "=" * 60)
        print(f"批次摘要: {report.batch_id}")
        print("=" * 60)
        print(f"批次大小: {report.batch_size}/{report.total_examples} 示例")
        print(f"处理时间: {report.duration_seconds:.2f}秒")
        print(
            f"平均处理时间: {report.duration_seconds / max(1, report.batch_size):.3f}秒/示例"
        )

        if report.summary:
            quality_scores = report.summary.get("quality_scores", {})
            if "avg_score" in quality_scores:
                print(f"平均质量评分: {quality_scores['avg_score']:.3f}")

            length_pres = report.summary.get("length_preservation", {})
            if "avg_ratio" in length_pres:
                print(f"长度保留率: {length_pres['avg_ratio']:.3f}")

        print("=" * 60)

    def generate_overall_report(self, reports: List[BatchReport]):
        """生成总体报告"""
        if not reports:
            return

        overall_report = {
            "total_batches": len(reports),
            "batches": [r.batch_id for r in reports],
            "summary_by_batch": {},
            "overall_statistics": {},
        }

        for report in reports:
            overall_report["summary_by_batch"][report.batch_id] = {
                "batch_size": report.batch_size,
                "duration": report.duration_seconds,
                "avg_processing_time": report.duration_seconds
                / max(1, report.batch_size),
                "quality_score": report.summary.get("quality_scores", {}).get(
                    "avg_score", 0
                ),
            }

        # 保存总体报告
        overall_file = f"overall_batch_report_{int(time.time())}.json"
        try:
            with open(overall_file, "w", encoding="utf-8") as f:
                json.dump(overall_report, f, ensure_ascii=False, indent=2)
            logger.info(f"总体报告已保存到 {overall_file}")
        except Exception as e:
            logger.error(f"保存总体报告失败: {e}")


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="分批次处理影视示例数据")
    parser.add_argument(
        "--examples", default="phase_C_examples.json", help="示例数据文件路径"
    )
    parser.add_argument(
        "--batch",
        type=int,
        nargs="+",
        default=[10, 30, 60, 100],
        help="批次百分比列表（例如：10 30 60 100）",
    )
    parser.add_argument(
        "--strategy",
        default="random",
        choices=["random", "stratified", "sequential"],
        help="示例选择策略",
    )
    parser.add_argument("--single", type=int, help="运行单个批次（指定百分比）")

    args = parser.parse_args()

    try:
        processor = BatchProcessor(args.examples)

        if args.single:
            # 运行单个批次
            report = processor.process_batch(args.single, args.strategy)
            processor.save_report(report)
            processor.print_batch_summary(report)
        else:
            # 运行多个批次
            processor.run_multiple_batches(args.batch)

    except Exception as e:
        logger.error(f"处理失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
