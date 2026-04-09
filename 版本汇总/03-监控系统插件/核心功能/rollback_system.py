#!/usr/bin/env python3
"""
回滚系统
用于在阶段C验证失败时执行回滚操作
"""

import json
import logging
import shutil
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from pathlib import Path
import sys

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("rollback_system.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)


class RollbackSystem:
    """回滚系统"""

    def __init__(self, backup_dir: str = "backups"):
        """
        初始化回滚系统

        Args:
            backup_dir: 备份目录
        """
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(parents=True, exist_ok=True)

        self.rollback_history = self.load_rollback_history()
        self.rollback_policies = self.load_rollback_policies()

    def load_rollback_history(self) -> List[Dict[str, Any]]:
        """加载回滚历史"""
        try:
            history_file = Path("rollback_history.json")
            if history_file.exists():
                with open(history_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            return []
        except Exception as e:
            logger.error(f"加载回滚历史失败: {e}")
            return []

    def save_rollback_history(self):
        """保存回滚历史"""
        try:
            history_file = Path("rollback_history.json")
            with open(history_file, "w", encoding="utf-8") as f:
                json.dump(self.rollback_history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"保存回滚历史失败: {e}")

    def load_rollback_policies(self) -> Dict[str, Any]:
        """加载回滚策略"""
        return {
            "critical_failure": {
                "description": "严重失败自动回滚",
                "conditions": [
                    "overall_status == 'critical'",
                    "simplification_rate < 0.04 or simplification_rate > 0.16",
                    "p1_preservation < 0.98",
                    "quality_degradation > 0.15",
                    "error_rate > 0.30",
                ],
                "action": "auto_rollback",
                "rollback_target": "previous_successful",
                "notification": True,
            },
            "warning_with_trend": {
                "description": "警告趋势持续恶化",
                "conditions": [
                    "consecutive_warnings >= 3",
                    "trend_deteriorating == True",
                ],
                "action": "manual_review",
                "rollback_target": "specific_snapshot",
                "notification": True,
            },
            "user_perception_failure": {
                "description": "用户感知严重负面",
                "conditions": [
                    "negative_keyword_count >= 5",
                    "high_risk_keyword_count >= 3",
                ],
                "action": "auto_rollback",
                "rollback_target": "previous_version",
                "notification": True,
            },
            "data_corruption": {
                "description": "数据损坏或丢失",
                "conditions": [
                    "data_integrity_check == False",
                    "missing_files_count > -1",
                ],
                "action": "emergency_rollback",
                "rollback_target": "last_verified",
                "notification": True,
            },
        }

    def create_backup(self, backup_name: str, description: str = "") -> str:
        """创建备份"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_id = f"{backup_name}_{timestamp}"
        backup_path = self.backup_dir / backup_id

        try:
            backup_path.mkdir(parents=True, exist_ok=True)

            # 备份关键文件
            files_to_backup = [
                "phase_C_examples.json",
                "batch_processor.py",
                "batch_validation.py",
                "validation_results/",
                "monitoring_dashboard.py",
                "alert_system.py",
            ]

            backup_info = {
                "backup_id": backup_id,
                "backup_name": backup_name,
                "timestamp": timestamp,
                "description": description,
                "files_backed_up": [],
                "metadata": {
                    "system_version": "1.0",
                    "backup_type": "manual" if description else "automatic",
                },
            }

            for file_path in files_to_backup:
                source_path = Path(file_path)
                if source_path.exists():
                    if source_path.is_dir():
                        dest_path = backup_path / source_path.name
                        shutil.copytree(source_path, dest_path)
                    else:
                        dest_path = backup_path / source_path.name
                        shutil.copy2(source_path, dest_path)

                    backup_info["files_backed_up"].append(str(source_path))

            # 保存备份信息
            backup_info_file = backup_path / "backup_info.json"
            with open(backup_info_file, "w", encoding="utf-8") as f:
                json.dump(backup_info, f, ensure_ascii=False, indent=2)

            logger.info(f"备份创建成功: {backup_id}")
            return backup_id

        except Exception as e:
            logger.error(f"创建备份失败: {e}")
            raise

    def list_backups(self) -> List[Dict[str, Any]]:
        """列出所有备份"""
        backups = []

        for backup_dir in self.backup_dir.iterdir():
            if backup_dir.is_dir():
                info_file = backup_dir / "backup_info.json"
                if info_file.exists():
                    try:
                        with open(info_file, "r", encoding="utf-8") as f:
                            backup_info = json.load(f)
                            backups.append(backup_info)
                    except Exception as e:
                        logger.error(f"读取备份信息失败 {backup_dir}: {e}")

        # 按时间排序
        backups.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        return backups

    def get_backup_details(self, backup_id: str) -> Optional[Dict[str, Any]]:
        """获取备份详情"""
        backup_path = self.backup_dir / backup_id
        info_file = backup_path / "backup_info.json"

        if backup_path.exists() and info_file.exists():
            try:
                with open(info_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"读取备份详情失败: {e}")

        return None

    def evaluate_rollback_need(
        self, validation_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """评估是否需要回滚"""
        evaluation = {
            "needs_rollback": False,
            "recommended_action": "none",
            "triggered_policies": [],
            "severity": "none",
            "recommendation": "无需回滚",
        }

        # 提取验证数据
        checks = validation_result.get("detailed_checks", {})
        overall_status = validation_result.get("overall_status", "unknown")

        # 检查严重失败
        if overall_status == "critical":
            evaluation["needs_rollback"] = True
            evaluation["recommended_action"] = "auto_rollback"
            evaluation["severity"] = "critical"
            evaluation["triggered_policies"].append("critical_failure")
            evaluation["recommendation"] = "检测到严重失败，建议立即自动回滚"
            return evaluation

        # 检查阶段C特定指标
        simpl_check = checks.get("phase_c_simplification_rate", {})
        p1p2_check = checks.get("phase_c_p1_p2_preservation", {})
        quality_check = checks.get("phase_c_quality_degradation", {})
        user_check = checks.get("phase_c_user_perception", {})

        triggered_conditions = []

        # 精简率检查
        if simpl_check.get("status") != "no_data":
            avg_rate = simpl_check.get("avg_simplification_rate", 0)
            if avg_rate < 0.04 or avg_rate > 0.16:
                triggered_conditions.append("simplification_rate_out_of_range")

        # P1保留率检查
        p1_pres = p1p2_check.get("p1_preservation", {})
        if p1_pres:
            avg_p1 = p1_pres.get("avg_ratio", 0)
            if avg_p1 < 0.98:
                triggered_conditions.append("p1_preservation_critical")

        # 质量下降检查
        quality_stats = quality_check.get("quality_degradation_stats", {})
        if quality_stats:
            avg_degradation = quality_stats.get("avg_degradation", 0)
            if avg_degradation > 0.15:
                triggered_conditions.append("quality_degradation_critical")

        # 用户感知检查
        user_stats = user_check.get("user_perception_stats", {})
        if user_stats:
            negative_count = user_stats.get("total_keyword_occurrences", 0)
            if negative_count >= 5:
                triggered_conditions.append("user_perception_critical")

        # 评估触发条件
        if triggered_conditions:
            critical_count = len([c for c in triggered_conditions if "critical" in c])

            if critical_count >= 2:
                evaluation["needs_rollback"] = True
                evaluation["recommended_action"] = "auto_rollback"
                evaluation["severity"] = "critical"
                evaluation["triggered_policies"].extend(
                    ["critical_failure", "user_perception_failure"]
                )
                evaluation["recommendation"] = (
                    f"检测到 {critical_count} 个严重条件，建议立即自动回滚"
                )
            elif triggered_conditions:
                evaluation["needs_rollback"] = True
                evaluation["recommended_action"] = "manual_review"
                evaluation["severity"] = "warning"
                evaluation["triggered_policies"].append("warning_with_trend")
                evaluation["recommendation"] = (
                    f"检测到 {len(triggered_conditions)} 个问题，建议手动审核后决定是否回滚"
                )

        return evaluation

    def execute_rollback(self, backup_id: str, dry_run: bool = False) -> Dict[str, Any]:
        """执行回滚"""
        backup_info = self.get_backup_details(backup_id)
        if not backup_info:
            return {
                "success": False,
                "message": f"备份 {backup_id} 不存在",
                "rollback_id": None,
            }

        backup_path = self.backup_dir / backup_id
        rollback_id = f"rollback_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        rollback_info = {
            "rollback_id": rollback_id,
            "backup_id": backup_id,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "backup_info": backup_info,
            "files_restored": [],
            "dry_run": dry_run,
        }

        if dry_run:
            logger.info(f"回滚模拟执行: {backup_id}")
            rollback_info["success"] = True
            rollback_info["message"] = "回滚模拟执行完成"
            return rollback_info

        try:
            # 记录当前状态（创建快照）
            current_snapshot_id = self.create_backup(
                f"pre_rollback_{rollback_id}", f"回滚前的状态快照，将回滚到 {backup_id}"
            )

            # 执行回滚
            files_restored = []
            for file_path in backup_info.get("files_backed_up", []):
                source_file = backup_path / Path(file_path).name
                if source_file.exists():
                    if source_file.is_dir():
                        # 删除现有目录
                        dest_path = Path(file_path)
                        if dest_path.exists():
                            shutil.rmtree(dest_path)
                        shutil.copytree(source_file, dest_path)
                    else:
                        shutil.copy2(source_file, Path(file_path))

                    files_restored.append(file_path)

            rollback_info["files_restored"] = files_restored
            rollback_info["pre_rollback_snapshot"] = current_snapshot_id
            rollback_info["success"] = True
            rollback_info["message"] = (
                f"回滚执行成功，恢复了 {len(files_restored)} 个文件"
            )

            # 记录到历史
            self.rollback_history.append(rollback_info)
            self.save_rollback_history()

            logger.info(f"回滚执行成功: {backup_id}")

        except Exception as e:
            rollback_info["success"] = False
            rollback_info["message"] = f"回滚执行失败: {e}"
            logger.error(f"回滚执行失败: {e}")

        return rollback_info

    def auto_rollback_if_needed(
        self, validation_result: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """如果需要则自动执行回滚"""
        evaluation = self.evaluate_rollback_need(validation_result)

        if not evaluation["needs_rollback"]:
            logger.info("无需回滚")
            return None

        if evaluation["recommended_action"] != "auto_rollback":
            logger.info(f"需要手动审核: {evaluation['recommendation']}")
            return evaluation

        # 查找最近的可用备份
        backups = self.list_backups()
        if not backups:
            logger.warning("没有可用的备份，无法执行回滚")
            return {
                **evaluation,
                "rollback_executed": False,
                "message": "没有可用的备份",
            }

        # 选择最近的备份
        latest_backup = backups[0]
        backup_id = latest_backup["backup_id"]

        logger.info(f"自动回滚到备份: {backup_id}")

        # 执行回滚
        rollback_result = self.execute_rollback(backup_id, dry_run=False)

        return {
            **evaluation,
            **rollback_result,
            "rollback_executed": True,
        }

    def get_rollback_report(self, days: int = 7) -> Dict[str, Any]:
        """获取回滚报告"""
        recent_rollbacks = [
            r
            for r in self.rollback_history
            if datetime.strptime(r["timestamp"], "%Y-%m-%d %H:%M:%S")
            > datetime.now() - timedelta(days=days)
        ]

        return {
            "report_period": f"最近{days}天",
            "total_rollbacks": len(recent_rollbacks),
            "successful_rollbacks": len(
                [r for r in recent_rollbacks if r.get("success", False)]
            ),
            "failed_rollbacks": len(
                [r for r in recent_rollbacks if not r.get("success", True)]
            ),
            "auto_rollbacks": len(
                [r for r in recent_rollbacks if r.get("triggered_policies", [])]
            ),
            "manual_rollbacks": len(
                [r for r in recent_rollbacks if not r.get("triggered_policies", [])]
            ),
            "recent_rollbacks": recent_rollbacks[:10],  # 最近10次
            "most_common_backup": self.get_most_common_backup(recent_rollbacks),
        }

    def get_most_common_backup(self, rollbacks: List[Dict]) -> Optional[str]:
        """获取最常用的备份"""
        if not rollbacks:
            return None

        backup_counts = {}
        for rollback in rollbacks:
            backup_id = rollback.get("backup_id")
            if backup_id:
                backup_counts[backup_id] = backup_counts.get(backup_id, 0) + 1

        if backup_counts:
            return max(backup_counts.items(), key=lambda x: x[1])[0]

        return None


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="阶段C验证系统回滚系统")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # 创建备份命令
    create_parser = subparsers.add_parser("create", help="创建备份")
    create_parser.add_argument("name", help="备份名称")
    create_parser.add_argument("--description", default="", help="备份描述")

    # 列出备份命令
    list_parser = subparsers.add_parser("list", help="列出备份")
    list_parser.add_argument("--limit", type=int, default=10, help="显示数量限制")

    # 执行回滚命令
    rollback_parser = subparsers.add_parser("rollback", help="执行回滚")
    rollback_parser.add_argument("backup_id", help="备份ID")
    rollback_parser.add_argument("--dry-run", action="store_true", help="模拟执行")

    # 评估回滚命令
    evaluate_parser = subparsers.add_parser("evaluate", help="评估是否需要回滚")
    evaluate_parser.add_argument("validation_file", help="验证结果文件路径")

    # 自动回滚命令
    auto_parser = subparsers.add_parser("auto", help="自动回滚")
    auto_parser.add_argument("validation_file", help="验证结果文件路径")

    # 报告命令
    report_parser = subparsers.add_parser("report", help="生成回滚报告")
    report_parser.add_argument("--days", type=int, default=7, help="报告天数")

    args = parser.parse_args()

    rollback_system = RollbackSystem()

    if args.command == "create":
        try:
            backup_id = rollback_system.create_backup(args.name, args.description)
            print(f"✅ 备份创建成功: {backup_id}")
        except Exception as e:
            print(f"❌ 备份创建失败: {e}")

    elif args.command == "list":
        backups = rollback_system.list_backups()
        if backups:
            print(f"\n📋 可用备份 ({len(backups)} 个)")
            print("=" * 80)
            for backup in backups[: args.limit]:
                print(f"ID: {backup['backup_id']}")
                print(f"  名称: {backup['backup_name']}")
                print(f"  时间: {backup['timestamp']}")
                print(f"  描述: {backup['description']}")
                print(f"  文件数: {len(backup.get('files_backed_up', []))}")
                print("-" * 40)
        else:
            print("没有可用的备份")

    elif args.command == "rollback":
        result = rollback_system.execute_rollback(args.backup_id, args.dry_run)
        if result["success"]:
            print(f"✅ 回滚执行成功: {result['message']}")
            if args.dry_run:
                print("⚠️  注意：这是模拟执行，实际文件未更改")
        else:
            print(f"❌ 回滚执行失败: {result['message']}")

    elif args.command == "evaluate":
        try:
            with open(args.validation_file, "r", encoding="utf-8") as f:
                validation_result = json.load(f)

            evaluation = rollback_system.evaluate_rollback_need(validation_result)

            print(f"\n🔍 回滚评估结果")
            print("=" * 60)
            print(f"需要回滚: {'✅ 是' if evaluation['needs_rollback'] else '❌ 否'}")
            print(f"建议操作: {evaluation['recommended_action']}")
            print(f"严重程度: {evaluation['severity']}")
            print(
                f"触发策略: {', '.join(evaluation['triggered_policies']) if evaluation['triggered_policies'] else '无'}"
            )
            print(f"建议: {evaluation['recommendation']}")

        except Exception as e:
            print(f"❌ 评估失败: {e}")

    elif args.command == "auto":
        try:
            with open(args.validation_file, "r", encoding="utf-8") as f:
                validation_result = json.load(f)

            result = rollback_system.auto_rollback_if_needed(validation_result)

            if result:
                print(f"\n🤖 自动回滚结果")
                print("=" * 60)
                print(
                    f"执行回滚: {'✅ 是' if result.get('rollback_executed', False) else '❌ 否'}"
                )
                print(f"成功: {'✅ 是' if result.get('success', False) else '❌ 否'}")
                print(f"消息: {result.get('message', '无')}")
                print(f"备份ID: {result.get('backup_id', '无')}")
            else:
                print("✅ 无需自动回滚")

        except Exception as e:
            print(f"❌ 自动回滚失败: {e}")

    elif args.command == "report":
        report = rollback_system.get_rollback_report(args.days)

        print(f"\n📊 回滚报告 ({report['report_period']})")
        print("=" * 80)
        print(f"总回滚次数: {report['total_rollbacks']}")
        print(f"成功回滚: {report['successful_rollbacks']}")
        print(f"失败回滚: {report['failed_rollbacks']}")
        print(f"自动回滚: {report['auto_rollbacks']}")
        print(f"手动回滚: {report['manual_rollbacks']}")

        if report["most_common_backup"]:
            print(f"最常用备份: {report['most_common_backup']}")

        if report["recent_rollbacks"]:
            print(f"\n最近回滚记录:")
            for rollback in report["recent_rollbacks"]:
                status = "✅" if rollback.get("success", False) else "❌"
                print(
                    f"  {status} {rollback['timestamp']} - {rollback.get('backup_id', 'unknown')}"
                )

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
