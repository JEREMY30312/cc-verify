#!/usr/bin/env python3
"""
示例用法：展示如何使用阶段C验证系统
"""

import json
import tempfile
from pathlib import Path


def create_example_batch_report():
    """创建示例批次报告"""
    return {
        "batch_id": "example_batch_001",
        "batch_size": 50,
        "total_examples": 50,
        "start_time": "2025-01-30 10:00:00",
        "end_time": "2025-01-30 10:05:00",
        "duration_seconds": 300.0,
        "results": [
            {
                "example_id": f"example_{i:03d}",
                "original_length": 600,
                "processed_length": 552,  # 8%精简率
                "p1_elements_preserved": 12,
                "p1_count": 12,
                "p2_elements_preserved": 18,
                "p2_count": 20,  # 90%保留率
                "quality_score": 0.82,
                "original_quality_score": 0.90,  # 8.9%质量下降
                "processing_time": 2.5,
                "errors": [],
            }
            for i in range(50)
        ],
        "summary": {
            "total_processed": 50,
            "successful": 50,
            "failed": 0,
            "avg_processing_time": 2.5,
        },
    }


def demonstrate_batch_validation():
    """演示批次验证"""
    print("1. 批次验证演示")
    print("=" * 50)

    # 创建示例报告
    report = create_example_batch_report()

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(report, f, indent=2)
        report_file = f.name

    try:
        from batch_validation import BatchValidator

        validator = BatchValidator()
        result = validator.validate_batch_report(report_file)

        print(f"批次ID: {result['batch_id']}")
        print(f"整体状态: {result['overall_status']}")

        # 显示阶段C特定指标
        checks = result["detailed_checks"]

        simpl = checks["phase_c_simplification_rate"]
        print(f"精简率: {simpl['avg_simplification_rate']:.1%} (目标: 7.9%)")

        p1p2 = checks["phase_c_p1_p2_preservation"]
        print(f"P1保留率: {p1p2['p1_preservation']['avg_ratio']:.1%} (目标: 100%)")
        print(f"P2保留率: {p1p2['p2_preservation']['avg_ratio']:.1%} (目标: ≥90%)")

        quality = checks["phase_c_quality_degradation"]
        if "quality_degradation_stats" in quality:
            print(
                f"质量下降: {quality['quality_degradation_stats']['avg_degradation']:.1%} (目标: ≤8%)"
            )

        print("\n✅ 批次验证演示完成")

    finally:
        Path(report_file).unlink()


def demonstrate_monitoring_dashboard():
    """演示监控仪表板"""
    print("\n2. 监控仪表板演示")
    print("=" * 50)

    try:
        from monitoring_dashboard import MonitoringDashboard

        dashboard = MonitoringDashboard("validation_results")

        # 显示仪表板
        dashboard.display_dashboard(days=1)

        print("\n✅ 监控仪表板演示完成")

    except Exception as e:
        print(f"⚠️  监控仪表板演示失败（可能没有数据）: {e}")


def demonstrate_alert_system():
    """演示警报系统"""
    print("\n3. 警报系统演示")
    print("=" * 50)

    # 创建触发警报的测试数据
    test_data = {
        "batch_id": "alert_test_batch",
        "validation_time": "2025-01-30 10:10:00",
        "overall_status": "warning",
        "detailed_checks": {
            "phase_c_simplification_rate": {
                "status": "warning",
                "avg_simplification_rate": 0.03,  # 3%，触发警报
            },
            "phase_c_p1_p2_preservation": {
                "status": "warning",
                "p1_preservation": {"avg_ratio": 0.98},  # 触发警报
                "p2_preservation": {"avg_ratio": 0.82},  # 触发警报
            },
        },
        "statistics": {"total_examples": 50},
    }

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(test_data, f, indent=2)
        test_file = f.name

    try:
        from alert_system import AlertSystem

        alert_system = AlertSystem()

        # 测试模式，不发送实际通知
        alert_system.config["email"]["enabled"] = False

        print("测试警报触发条件:")
        print("- 精简率: 3% (低于5%阈值)")
        print("- P1保留率: 98% (低于99%阈值)")
        print("- P2保留率: 82% (低于85%阈值)")
        print()

        with open(test_file, "r") as f:
            test_result = json.load(f)

        alerts = alert_system.process_validation_result(test_result)

        if alerts:
            print(f"触发 {len(alerts)} 个警报:")
            for alert in alerts:
                icon = "🔴" if alert["severity"] == "critical" else "🟡"
                print(f"  {icon} {alert['message']}")
        else:
            print("未触发警报")

        print("\n✅ 警报系统演示完成")

    finally:
        Path(test_file).unlink()


def demonstrate_rollback_system():
    """演示回滚系统"""
    print("\n4. 回滚系统演示")
    print("=" * 50)

    try:
        from rollback_system import RollbackSystem

        rollback_system = RollbackSystem()

        # 列出备份
        backups = rollback_system.list_backups()

        if backups:
            print(f"现有备份: {len(backups)} 个")
            for backup in backups[:3]:  # 显示前3个
                print(f"  - {backup['backup_id']}: {backup['description']}")
        else:
            print("没有现有备份")

        # 创建新备份
        print("\n创建新备份...")
        backup_id = rollback_system.create_backup("演示备份", "回滚系统演示创建的备份")
        print(f"✅ 备份创建成功: {backup_id}")

        # 模拟回滚评估
        test_evaluation = {
            "batch_id": "rollback_test",
            "validation_time": "2025-01-30 10:15:00",
            "overall_status": "critical",
            "detailed_checks": {
                "phase_c_simplification_rate": {
                    "status": "critical",
                    "avg_simplification_rate": 0.02,  # 2%，触发回滚
                },
            },
        }

        evaluation = rollback_system.evaluate_rollback_need(test_evaluation)

        print(f"\n回滚评估结果:")
        print(f"  需要回滚: {'是' if evaluation['needs_rollback'] else '否'}")
        print(f"  建议操作: {evaluation['recommended_action']}")
        print(f"  触发策略: {', '.join(evaluation['triggered_policies'])}")

        print("\n✅ 回滚系统演示完成")

    except Exception as e:
        print(f"⚠️  回滚系统演示失败: {e}")


def demonstrate_integrated_system():
    """演示集成系统"""
    print("\n5. 集成系统演示")
    print("=" * 50)

    # 创建示例报告
    report = create_example_batch_report()

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(report, f, indent=2)
        report_file = f.name

    try:
        from integrated_validation_system import IntegratedValidationSystem

        system = IntegratedValidationSystem()

        print("执行完整处理流程:")
        print("1. 批次验证")
        print("2. 监控更新")
        print("3. 警报分析")
        print("4. 回滚评估")
        print("5. 自动回滚（如果需要）")
        print()

        result = system.process_batch_report(report_file)

        print(f"处理完成，整体状态: {result['overall_status']}")

        # 显示摘要
        system.display_summary(result)

        print("\n✅ 集成系统演示完成")

    finally:
        Path(report_file).unlink()


def main():
    """主函数"""
    print("阶段C验证系统演示")
    print("=" * 60)

    demonstrations = [
        ("批次验证", demonstrate_batch_validation),
        ("监控仪表板", demonstrate_monitoring_dashboard),
        ("警报系统", demonstrate_alert_system),
        ("回滚系统", demonstrate_rollback_system),
        ("集成系统", demonstrate_integrated_system),
    ]

    for name, demo_func in demonstrations:
        try:
            demo_func()
        except KeyboardInterrupt:
            print("\n⚠️  演示被用户中断")
            break
        except Exception as e:
            print(f"\n⚠️  {name}演示失败: {e}")
            continue

    print("\n" + "=" * 60)
    print("演示完成！")
    print("\n下一步:")
    print("1. 查看 README_PHASE_C_VALIDATION.md 了解详细文档")
    print("2. 运行 test_phase_c_validation.py 进行完整测试")
    print("3. 使用 integrated_validation_system.py 处理实际批次报告")
    print("4. 根据需要修改 alert_config.json 配置警报")


if __name__ == "__main__":
    main()
