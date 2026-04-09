#!/usr/bin/env python3
"""
监控仪表板脚本
用于显示阶段C验证系统的监控指标
"""

import json
import logging
import statistics
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from pathlib import Path
import sys

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("monitoring_dashboard.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)


class MonitoringDashboard:
    """监控仪表板"""

    def __init__(self, validation_results_dir: str = "validation_results"):
        """
        初始化监控仪表板

        Args:
            validation_results_dir: 验证结果目录
        """
        self.validation_results_dir = Path(validation_results_dir)
        self.daily_metrics = {}
        self.load_daily_metrics()

    def load_daily_metrics(self):
        """加载每日指标"""
        try:
            metrics_file = self.validation_results_dir / "daily_metrics.json"
            if metrics_file.exists():
                with open(metrics_file, "r", encoding="utf-8") as f:
                    self.daily_metrics = json.load(f)
                logger.info(f"成功加载 {len(self.daily_metrics)} 天的指标数据")
            else:
                logger.info("没有找到历史指标数据，将创建新文件")
                self.daily_metrics = {}
        except Exception as e:
            logger.error(f"加载每日指标失败: {e}")
            self.daily_metrics = {}

    def save_daily_metrics(self):
        """保存每日指标"""
        try:
            metrics_file = self.validation_results_dir / "daily_metrics.json"
            with open(metrics_file, "w", encoding="utf-8") as f:
                json.dump(self.daily_metrics, f, ensure_ascii=False, indent=2)
            logger.info(f"每日指标已保存到 {metrics_file}")
        except Exception as e:
            logger.error(f"保存每日指标失败: {e}")

    def update_daily_metrics(self, validation_result: Dict[str, Any]):
        """更新每日指标"""
        today = datetime.now().strftime("%Y-%m-%d")

        if today not in self.daily_metrics:
            self.daily_metrics[today] = {
                "date": today,
                "batch_count": 0,
                "total_examples": 0,
                "metrics": {
                    "simplification_rate": [],
                    "p1_preservation": [],
                    "p2_preservation": [],
                    "quality_degradation": [],
                    "processing_time": [],
                    "error_rate": [],
                },
                "alerts": [],
                "summary": {},
            }

        daily_data = self.daily_metrics[today]
        daily_data["batch_count"] += 1

        # 提取统计信息
        stats = validation_result.get("statistics", {})
        daily_data["total_examples"] += stats.get("total_examples", 0)

        # 提取阶段C特定指标
        checks = validation_result.get("detailed_checks", {})

        # 精简率
        simplification_check = checks.get("phase_c_simplification_rate", {})
        if simplification_check.get("status") != "no_data":
            avg_rate = simplification_check.get("avg_simplification_rate", 0)
            daily_data["metrics"]["simplification_rate"].append(avg_rate)

        # P1保留率
        p1_check = checks.get("phase_c_p1_p2_preservation", {})
        p1_preservation = p1_check.get("p1_preservation", {})
        if p1_preservation:
            avg_p1 = p1_preservation.get("avg_ratio", 0)
            daily_data["metrics"]["p1_preservation"].append(avg_p1)

        # P2保留率
        p2_preservation = p1_check.get("p2_preservation", {})
        if p2_preservation:
            avg_p2 = p2_preservation.get("avg_ratio", 0)
            daily_data["metrics"]["p2_preservation"].append(avg_p2)

        # 质量下降
        quality_check = checks.get("phase_c_quality_degradation", {})
        quality_stats = quality_check.get("quality_degradation_stats", {})
        if quality_stats:
            avg_degradation = quality_stats.get("avg_degradation", 0)
            daily_data["metrics"]["quality_degradation"].append(avg_degradation)

        # 处理时间
        time_check = checks.get("processing_time", {})
        if time_check.get("status") != "no_data":
            avg_time = time_check.get("avg_processing_time", 0)
            daily_data["metrics"]["processing_time"].append(avg_time)

        # 错误率
        error_check = checks.get("error_analysis", {})
        if error_check.get("status") != "no_data":
            error_examples = error_check.get("error_examples_count", 0)
            total_examples = stats.get("total_examples", 1)
            error_rate = error_examples / total_examples
            daily_data["metrics"]["error_rate"].append(error_rate)

        # 收集警报
        issues = validation_result.get("issues_found", [])
        if issues:
            alert = {
                "batch_id": validation_result.get("batch_id", "unknown"),
                "timestamp": validation_result.get("validation_time", ""),
                "issues": issues[:3],  # 只取前3个问题
                "overall_status": validation_result.get("overall_status", "unknown"),
            }
            daily_data["alerts"].append(alert)

        # 更新每日摘要
        self.update_daily_summary(daily_data)

        # 保存更新后的指标
        self.save_daily_metrics()

    def update_daily_summary(self, daily_data: Dict[str, Any]):
        """更新每日摘要"""
        metrics = daily_data["metrics"]

        summary = {
            "simplification_rate": {
                "avg": round(statistics.mean(metrics["simplification_rate"]), 3)
                if metrics["simplification_rate"]
                else 0,
                "min": round(min(metrics["simplification_rate"]), 3)
                if metrics["simplification_rate"]
                else 0,
                "max": round(max(metrics["simplification_rate"]), 3)
                if metrics["simplification_rate"]
                else 0,
                "count": len(metrics["simplification_rate"]),
            },
            "p1_preservation": {
                "avg": round(statistics.mean(metrics["p1_preservation"]), 3)
                if metrics["p1_preservation"]
                else 0,
                "min": round(min(metrics["p1_preservation"]), 3)
                if metrics["p1_preservation"]
                else 0,
                "max": round(max(metrics["p1_preservation"]), 3)
                if metrics["p1_preservation"]
                else 0,
                "count": len(metrics["p1_preservation"]),
            },
            "p2_preservation": {
                "avg": round(statistics.mean(metrics["p2_preservation"]), 3)
                if metrics["p2_preservation"]
                else 0,
                "min": round(min(metrics["p2_preservation"]), 3)
                if metrics["p2_preservation"]
                else 0,
                "max": round(max(metrics["p2_preservation"]), 3)
                if metrics["p2_preservation"]
                else 0,
                "count": len(metrics["p2_preservation"]),
            },
            "quality_degradation": {
                "avg": round(statistics.mean(metrics["quality_degradation"]), 3)
                if metrics["quality_degradation"]
                else 0,
                "min": round(min(metrics["quality_degradation"]), 3)
                if metrics["quality_degradation"]
                else 0,
                "max": round(max(metrics["quality_degradation"]), 3)
                if metrics["quality_degradation"]
                else 0,
                "count": len(metrics["quality_degradation"]),
            },
            "processing_time": {
                "avg": round(statistics.mean(metrics["processing_time"]), 3)
                if metrics["processing_time"]
                else 0,
                "min": round(min(metrics["processing_time"]), 3)
                if metrics["processing_time"]
                else 0,
                "max": round(max(metrics["processing_time"]), 3)
                if metrics["processing_time"]
                else 0,
                "count": len(metrics["processing_time"]),
            },
            "error_rate": {
                "avg": round(statistics.mean(metrics["error_rate"]), 3)
                if metrics["error_rate"]
                else 0,
                "min": round(min(metrics["error_rate"]), 3)
                if metrics["error_rate"]
                else 0,
                "max": round(max(metrics["error_rate"]), 3)
                if metrics["error_rate"]
                else 0,
                "count": len(metrics["error_rate"]),
            },
            "alerts_count": len(daily_data["alerts"]),
            "batch_count": daily_data["batch_count"],
            "total_examples": daily_data["total_examples"],
        }

        daily_data["summary"] = summary

    def display_dashboard(self, days: int = 7):
        """显示监控仪表板"""
        print("\n" + "=" * 80)
        print("阶段C验证系统 - 监控仪表板")
        print("=" * 80)

        # 获取最近N天的数据
        recent_dates = sorted(self.daily_metrics.keys(), reverse=True)[:days]

        if not recent_dates:
            print("没有可用的监控数据")
            return

        print(
            f"\n📊 最近 {len(recent_dates)} 天监控数据 ({recent_dates[0]} 到 {recent_dates[-1]})"
        )
        print("-" * 80)
        print(f"我们发现最近有 {len(recent_dates)} 天的监控数据")

        # 显示每日摘要
        for date in recent_dates:
            daily_data = self.daily_metrics[date]
            summary = daily_data.get("summary", {})

            print(f"\n📅 {date}")
            print(f"   批次数量: {summary.get('batch_count', 0)}")
            print(f"   总示例数: {summary.get('total_examples', 0)}")
            print(f"   警报数量: {summary.get('alerts_count', 0)}")

            # 关键指标
            simpl_rate = summary.get("simplification_rate", {})
            p1_pres = summary.get("p1_preservation", {})
            p2_pres = summary.get("p2_preservation", {})
            qual_degrad = summary.get("quality_degradation", {})

            if simpl_rate.get("count", 0) > 0:
                print(f"   平均精简率: {simpl_rate.get('avg', 0):.1%} (目标: 7.9%)")
                status = "✅" if 0.05 <= simpl_rate.get("avg", 0) <= 0.15 else "⚠️"
                print(
                    f"      {status} 范围: {simpl_rate.get('min', 0):.1%} - {simpl_rate.get('max', 0):.1%}"
                )

            if p1_pres.get("count", 0) > 0:
                print(f"   P1保留率: {p1_pres.get('avg', 0):.1%} (目标: 100%)")
                status = "✅" if p1_pres.get("avg", 0) >= 0.99 else "⚠️"
                print(
                    f"      {status} 范围: {p1_pres.get('min', 0):.1%} - {p1_pres.get('max', 0):.1%}"
                )

            if p2_pres.get("count", 0) > 0:
                print(f"   P2保留率: {p2_pres.get('avg', 0):.1%} (目标: ≥90%)")
                status = "✅" if p2_pres.get("avg", 0) >= 0.85 else "⚠️"
                print(
                    f"      {status} 范围: {p2_pres.get('min', 0):.1%} - {p2_pres.get('max', 0):.1%}"
                )

            if qual_degrad.get("count", 0) > 0:
                print(f"   质量下降: {qual_degrad.get('avg', 0):.1%} (目标: ≤8%)")
                status = "✅" if qual_degrad.get("avg", 0) <= 0.10 else "⚠️"
                print(
                    f"      {status} 范围: {qual_degrad.get('min', 0):.1%} - {qual_degrad.get('max', 0):.1%}"
                )

        # 显示趋势分析
        self.display_trend_analysis(recent_dates)

        # 显示警报摘要
        self.display_alerts_summary(recent_dates)

        print("\n" + "=" * 80)

    def display_trend_analysis(self, dates: List[str]):
        """显示趋势分析"""
        print(f"\n📈 趋势分析 ({len(dates)} 天)")
        print("-" * 40)

        metrics_to_analyze = [
            ("simplification_rate", "精简率", 0.079, 0.05, 0.15),
            ("p1_preservation", "P1保留率", 1.0, 0.99, 1.0),
            ("p2_preservation", "P2保留率", 0.9, 0.85, -1.0),
            ("quality_degradation", "质量下降", 0.0, -1.0, 0.08),
        ]

        for (
            metric_key,
            metric_name,
            target,
            min_threshold,
            max_threshold,
        ) in metrics_to_analyze:
            values = []
            for date in dates:
                daily_data = self.daily_metrics.get(date, {})
                summary = daily_data.get("summary", {})
                metric_data = summary.get(metric_key, {})
                if metric_data.get("count", 0) > 0:
                    values.append(metric_data.get("avg", 0))

            if len(values) >= 2:
                first_val = values[0]
                last_val = values[-1]
                change = last_val - first_val
                change_percent = (change / first_val) * 100 if first_val != 0 else 0

                trend = "↗️ 上升" if change > 0 else "↘️ 下降" if change < 0 else "➡️ 稳定"

                # 评估趋势
                assessment = ""
                if metric_key == "simplification_rate":
                    if 0.05 <= last_val <= 0.15:
                        assessment = "✅ 在目标范围内"
                    elif last_val < 0.05:
                        assessment = "⚠️ 过低"
                    else:
                        assessment = "⚠️ 过高"
                elif metric_key == "p1_preservation":
                    assessment = "✅ 优秀" if last_val >= 0.99 else "⚠️ 需要改进"
                elif metric_key == "p2_preservation":
                    assessment = "✅ 良好" if last_val >= 0.85 else "⚠️ 需要关注"
                elif metric_key == "quality_degradation":
                    assessment = "✅ 良好" if last_val <= 0.10 else "⚠️ 需要关注"

                print(
                    f"   {metric_name}: {last_val:.1%} ({trend} {change_percent:+.1f}%) - {assessment}"
                )

    def display_alerts_summary(self, dates: List[str]):
        """显示警报摘要"""
        total_alerts = 0
        alert_types = {}

        for date in dates:
            daily_data = self.daily_metrics.get(date, {})
            alerts = daily_data.get("alerts", [])
            total_alerts += len(alerts)

            for alert in alerts:
                status = alert.get("overall_status", "unknown")
                alert_types[status] = alert_types.get(status, 0) + 1

        if total_alerts > 0:
            print(f"\n🚨 警报摘要 ({total_alerts} 个警报)")
            print("-" * 40)

            for status, count in alert_types.items():
                icon = (
                    "🔴"
                    if status == "critical"
                    else "🟡"
                    if status == "warning"
                    else "⚪"
                )
                print(f"   {icon} {status}: {count} 个")

            # 显示最近的重要警报
            recent_critical_alerts = []
            for date in dates[:3]:  # 最近3天
                daily_data = self.daily_metrics.get(date, {})
                for alert in daily_data.get("alerts", []):
                    if alert.get("overall_status") == "critical":
                        recent_critical_alerts.append((date, alert))

            if recent_critical_alerts:
                print(f"\n   🔴 最近严重警报:")
                for date, alert in recent_critical_alerts[:3]:  # 最多显示3个
                    batch_id = alert.get("batch_id", "unknown")
                    issues = alert.get("issues", [])
                    if issues:
                        print(f"      {date} - {batch_id}: {issues[0][:50]}...")


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="显示阶段C验证系统监控仪表板")
    parser.add_argument("--days", type=int, default=7, help="显示最近N天的数据")
    parser.add_argument("--update", help="更新监控数据（提供验证结果文件路径）")
    parser.add_argument(
        "--output-dir", default="validation_results", help="验证结果目录"
    )

    args = parser.parse_args()

    dashboard = MonitoringDashboard(args.output_dir)

    if args.update:
        # 更新监控数据
        try:
            with open(args.update, "r", encoding="utf-8") as f:
                validation_result = json.load(f)
            dashboard.update_daily_metrics(validation_result)
            print(f"✅ 已更新监控数据: {args.update}")
        except Exception as e:
            logger.error(f"更新监控数据失败: {e}")

    # 显示仪表板
    dashboard.display_dashboard(args.days)


if __name__ == "__main__":
    main()
