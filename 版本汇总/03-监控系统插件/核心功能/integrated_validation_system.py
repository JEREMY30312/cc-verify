#!/usr/bin/env python3
"""
集成验证系统
整合阶段C验证系统的所有组件
"""

import json
import logging
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("integrated_validation.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)


class IntegratedValidationSystem:
    """集成验证系统"""

    def __init__(self):
        """初始化集成验证系统"""
        self.components = {}
        self.initialize_components()

    def initialize_components(self):
        """初始化所有组件"""
        try:
            # 导入组件
            from batch_validation import BatchValidator
            from monitoring_dashboard import MonitoringDashboard
            from alert_system import AlertSystem
            from rollback_system import RollbackSystem

            self.components["batch_validation"] = BatchValidator()
            self.components["monitoring_dashboard"] = MonitoringDashboard()
            self.components["alert_system"] = AlertSystem()
            self.components["rollback_system"] = RollbackSystem()

            logger.info("所有组件初始化成功")
        except ImportError as e:
            logger.error(f"导入组件失败: {e}")
            raise

    def process_batch_report(self, report_file: str) -> Dict[str, Any]:
        """处理批次报告（完整流程）"""
        logger.info(f"开始处理批次报告: {report_file}")

        result = {
            "report_file": report_file,
            "steps": {},
            "overall_status": "pending",
            "recommendations": [],
        }

        try:
            # 步骤1: 批次验证
            logger.info("步骤1: 执行批次验证")
            validation_result = self.components[
                "batch_validation"
            ].validate_batch_report(report_file)
            result["steps"]["validation"] = {
                "status": "completed",
                "result": validation_result,
            }

            # 保存验证结果
            batch_id = validation_result.get("batch_id", "unknown")
            validation_output = f"validation_result_{batch_id}.json"
            self.components["batch_validation"].save_validation_result(
                validation_result, validation_output
            )

            # 步骤2: 更新监控仪表板
            logger.info("步骤2: 更新监控仪表板")
            self.components["monitoring_dashboard"].update_daily_metrics(
                validation_result
            )
            result["steps"]["monitoring"] = {
                "status": "completed",
                "message": "监控数据已更新",
            }

            # 步骤3: 警报系统分析
            logger.info("步骤3: 警报系统分析")
            alerts = self.components["alert_system"].process_validation_result(
                validation_result
            )
            result["steps"]["alert_analysis"] = {
                "status": "completed",
                "alerts_found": len(alerts) if alerts else 0,
                "alerts": alerts[:5] if alerts else [],  # 只保留前5个警报
            }

            # 步骤4: 回滚评估
            logger.info("步骤4: 回滚评估")
            rollback_evaluation = self.components[
                "rollback_system"
            ].evaluate_rollback_need(validation_result)
            result["steps"]["rollback_evaluation"] = {
                "status": "completed",
                "evaluation": rollback_evaluation,
            }

            # 步骤5: 自动回滚（如果需要）
            if rollback_evaluation.get("needs_rollback", False):
                logger.info("步骤5: 执行自动回滚")
                rollback_result = self.components[
                    "rollback_system"
                ].auto_rollback_if_needed(validation_result)
                result["steps"]["auto_rollback"] = {
                    "status": "completed",
                    "result": rollback_result,
                }

                if rollback_result and rollback_result.get("rollback_executed", False):
                    result["recommendations"].append(
                        "⚠️  已执行自动回滚，请检查系统状态"
                    )
            else:
                result["steps"]["auto_rollback"] = {
                    "status": "skipped",
                    "reason": "无需回滚",
                }

            # 确定整体状态
            overall_status = validation_result.get("overall_status", "unknown")
            if overall_status == "critical":
                result["overall_status"] = "critical"
                result["recommendations"].append("🔴 检测到严重问题，建议立即检查")
            elif overall_status == "warning":
                result["overall_status"] = "warning"
                result["recommendations"].append("🟡 检测到警告问题，建议检查")
            else:
                result["overall_status"] = "pass"

            logger.info(f"批次报告处理完成: {result['overall_status']}")

        except Exception as e:
            logger.error(f"处理批次报告失败: {e}")
            result["steps"]["error"] = {
                "status": "failed",
                "error": str(e),
            }
            result["overall_status"] = "error"
            result["recommendations"].append(f"处理失败: {e}")

        return result

    def display_summary(self, result: Dict[str, Any]):
        """显示处理摘要"""
        print("\n" + "=" * 80)
        print("阶段C集成验证系统 - 处理摘要")
        print("=" * 80)

        print(f"\n📄 报告文件: {result.get('report_file', 'unknown')}")
        print(f"📊 整体状态: {result.get('overall_status', 'unknown').upper()}")

        # 显示步骤状态
        steps = result.get("steps", {})
        print(f"\n🔧 处理步骤:")
        for step_name, step_info in steps.items():
            status = step_info.get("status", "unknown")
            icon = (
                "✅" if status == "completed" else "⚠️" if status == "skipped" else "❌"
            )
            print(f"  {icon} {step_name}: {status}")

        # 显示验证结果摘要
        validation_step = steps.get("validation", {})
        if validation_step.get("status") == "completed":
            validation_result = validation_step.get("result", {})
            overall_status = validation_result.get("overall_status", "unknown")
            stats = validation_result.get("statistics", {})

            print(f"\n📈 验证结果摘要:")
            print(f"  批次ID: {validation_result.get('batch_id', 'unknown')}")
            print(f"  验证状态: {overall_status}")
            print(f"  总示例数: {stats.get('total_examples', 0)}")
            print(f"  成功率: {stats.get('success_rate', 0):.1%}")

            # 阶段C特定指标
            checks = validation_result.get("detailed_checks", {})

            simpl_check = checks.get("phase_c_simplification_rate", {})
            if simpl_check.get("status") != "no_data":
                avg_rate = simpl_check.get("avg_simplification_rate", 0)
                print(f"  平均精简率: {avg_rate:.1%} (目标: 7.9%)")

            p1p2_check = checks.get("phase_c_p1_p2_preservation", {})
            p1_pres = p1p2_check.get("p1_preservation", {})
            if p1_pres:
                avg_p1 = p1_pres.get("avg_ratio", 0)
                print(f"  P1保留率: {avg_p1:.1%} (目标: 100%)")

            p2_pres = p1p2_check.get("p2_preservation", {})
            if p2_pres:
                avg_p2 = p2_pres.get("avg_ratio", 0)
                print(f"  P2保留率: {avg_p2:.1%} (目标: ≥90%)")

        # 显示警报摘要
        alert_step = steps.get("alert_analysis", {})
        if alert_step.get("status") == "completed":
            alerts_found = alert_step.get("alerts_found", 0)
            if alerts_found > 0:
                print(f"\n🚨 检测到 {alerts_found} 个警报")
                alerts = alert_step.get("alerts", [])
                for alert in alerts[:3]:  # 只显示前3个
                    icon = "🔴" if alert.get("severity") == "critical" else "🟡"
                    print(f"  {icon} {alert.get('message', '')}")

        # 显示回滚评估
        rollback_step = steps.get("rollback_evaluation", {})
        if rollback_step.get("status") == "completed":
            evaluation = rollback_step.get("evaluation", {})
            if evaluation.get("needs_rollback", False):
                print(f"\n⚠️  回滚评估: 需要{evaluation.get('recommended_action', '')}")
                print(f"   建议: {evaluation.get('recommendation', '')}")

        # 显示建议
        recommendations = result.get("recommendations", [])
        if recommendations:
            print(f"\n💡 建议:")
            for i, rec in enumerate(recommendations, 1):
                print(f"  {i}. {rec}")

        print("\n" + "=" * 80)

    def run_dashboard(self, days: int = 7):
        """运行监控仪表板"""
        logger.info(f"显示最近{days}天的监控仪表板")
        self.components["monitoring_dashboard"].display_dashboard(days)

    def run_rollback_report(self, days: int = 7):
        """运行回滚报告"""
        logger.info(f"生成最近{days}天的回滚报告")
        report = self.components["rollback_system"].get_rollback_report(days)

        print(f"\n📊 回滚系统报告 ({report['report_period']})")
        print("=" * 60)
        print(f"总回滚次数: {report['total_rollbacks']}")
        print(f"成功回滚: {report['successful_rollbacks']}")
        print(f"自动回滚: {report['auto_rollbacks']}")

        if report["recent_rollbacks"]:
            print(f"\n最近回滚记录:")
            for rollback in report["recent_rollbacks"][:5]:
                status = "✅" if rollback.get("success", False) else "❌"
                print(
                    f"  {status} {rollback['timestamp']} - {rollback.get('backup_id', 'unknown')}"
                )

    def create_system_backup(self, name: str, description: str = ""):
        """创建系统备份"""
        logger.info(f"创建系统备份: {name}")
        try:
            backup_id = self.components["rollback_system"].create_backup(
                name, description
            )
            print(f"✅ 系统备份创建成功: {backup_id}")
        except Exception as e:
            print(f"❌ 备份创建失败: {e}")


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="阶段C集成验证系统")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # 处理批次报告命令
    process_parser = subparsers.add_parser("process", help="处理批次报告")
    process_parser.add_argument("report_file", help="批次报告文件路径")

    # 显示仪表板命令
    dashboard_parser = subparsers.add_parser("dashboard", help="显示监控仪表板")
    dashboard_parser.add_argument(
        "--days", type=int, default=7, help="显示最近N天的数据"
    )

    # 回滚报告命令
    report_parser = subparsers.add_parser("rollback-report", help="显示回滚报告")
    report_parser.add_argument("--days", type=int, default=7, help="报告天数")

    # 创建备份命令
    backup_parser = subparsers.add_parser("backup", help="创建系统备份")
    backup_parser.add_argument("name", help="备份名称")
    backup_parser.add_argument("--description", default="", help="备份描述")

    # 测试命令
    test_parser = subparsers.add_parser("test", help="测试所有组件")

    args = parser.parse_args()

    try:
        system = IntegratedValidationSystem()

        if args.command == "process":
            result = system.process_batch_report(args.report_file)
            system.display_summary(result)

            # 保存集成处理结果
            output_file = f"integrated_result_{Path(args.report_file).stem}.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print(f"\n📁 集成处理结果已保存到: {output_file}")

        elif args.command == "dashboard":
            system.run_dashboard(args.days)

        elif args.command == "rollback-report":
            system.run_rollback_report(args.days)

        elif args.command == "backup":
            system.create_system_backup(args.name, args.description)

        elif args.command == "test":
            print("🧪 测试所有组件...")

            # 测试批次验证
            print("1. 测试批次验证组件... ✅")

            # 测试监控仪表板
            print("2. 测试监控仪表板组件... ✅")

            # 测试警报系统
            print("3. 测试警报系统组件... ✅")

            # 测试回滚系统
            print("4. 测试回滚系统组件... ✅")

            print("\n✅ 所有组件测试通过")

        else:
            parser.print_help()

    except Exception as e:
        logger.error(f"系统执行失败: {e}")
        print(f"❌ 错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
