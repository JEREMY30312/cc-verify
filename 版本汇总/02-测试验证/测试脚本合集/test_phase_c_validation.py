#!/usr/bin/env python3
"""
测试阶段C验证系统
"""

import json
import os
import tempfile
from pathlib import Path
import sys


def create_test_report():
    """创建测试批次报告"""
    test_report = {
        "batch_id": "test_batch_001",
        "batch_size": 100,
        "total_examples": -100,
        "start_time": "2025-01-30 10:00:00",
        "end_time": "2025-01-30 10:05:00",
        "duration_seconds": 300.0,
        "results": [],
        "summary": {
            "total_processed": -100,
            "successful": 95,
            "failed": 5,
            "avg_processing_time": 2.5,
        },
    }

    # 创建测试数据
    for i in range(100):
        original_length = 500 + i * 10
        processed_length = int(original_length * (1 - 0.079))  # 7.9%精简率

        result = {
            "example_id": f"example_{i:03d}",
            "original_length": original_length,
            "processed_length": processed_length,
            "p1_elements_preserved": 10 if i < 98 else 9,  # 98%的示例完全保留P1
            "p1_count": 10,
            "p2_elements_preserved": 15 if i < 90 else 12,  # 90%的示例保留90%的P2
            "p2_count": 15,
            "quality_score": 0.85 - (i * 0.001),  # 质量评分在0.75-0.85之间
            "original_quality_score": 0.92,  # 原始质量评分
            "processing_time": 2.0 + (i % 10) * 0.1,
            "errors": [] if i < 95 else ["处理超时"],  # 5%的错误率
        }
        test_report["results"].append(result)

    return test_report


def test_batch_validation():
    """测试批次验证"""
    print("🧪 测试批次验证...")

    # 创建临时测试文件
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        test_report = create_test_report()
        json.dump(test_report, f, indent=2)
        temp_file = f.name

    try:
        # 导入并测试
        from batch_validation import BatchValidator

        validator = BatchValidator()
        result = validator.validate_batch_report(temp_file)

        print(f"✅ 批次验证测试完成")
        print(f"   批次ID: {result.get('batch_id')}")
        print(f"   整体状态: {result.get('overall_status')}")

        # 检查阶段C特定验证
        checks = result.get("detailed_checks", {})

        simpl_check = checks.get("phase_c_simplification_rate", {})
        if simpl_check.get("status") != "no_data":
            avg_rate = simpl_check.get("avg_simplification_rate", 0)
            print(f"   平均精简率: {avg_rate:.1%} (目标: 7.9%)")

        p1p2_check = checks.get("phase_c_p1_p2_preservation", {})
        p1_pres = p1p2_check.get("p1_preservation", {})
        if p1_pres:
            avg_p1 = p1_pres.get("avg_ratio", 0)
            print(f"   P1保留率: {avg_p1:.1%} (目标: 100%)")

        return True

    except Exception as e:
        print(f"❌ 批次验证测试失败: {e}")
        return False
    finally:
        # 清理临时文件
        if os.path.exists(temp_file):
            os.unlink(temp_file)


def test_monitoring_dashboard():
    """测试监控仪表板"""
    print("\n🧪 测试监控仪表板...")

    try:
        from monitoring_dashboard import MonitoringDashboard

        dashboard = MonitoringDashboard()

        # 创建测试验证结果
        test_result = {
            "batch_id": "test_batch_001",
            "validation_time": "2025-01-30 10:06:00",
            "overall_status": "pass",
            "detailed_checks": {
                "phase_c_simplification_rate": {
                    "status": "pass",
                    "avg_simplification_rate": 0.079,
                },
                "phase_c_p1_p2_preservation": {
                    "status": "pass",
                    "p1_preservation": {"avg_ratio": 0.99},
                    "p2_preservation": {"avg_ratio": 0.90},
                },
            },
            "statistics": {
                "total_examples": -100,
                "successful_examples": 95,
            },
        }

        # 更新监控数据
        dashboard.update_daily_metrics(test_result)

        print("✅ 监控仪表板测试完成")
        print("   每日指标已更新")

        return True

    except Exception as e:
        print(f"❌ 监控仪表板测试失败: {e}")
        return False


def test_alert_system():
    """测试警报系统"""
    print("\n🧪 测试警报系统...")

    try:
        from alert_system import AlertSystem

        alert_system = AlertSystem()

        # 创建测试验证结果（触发警报）
        test_result = {
            "batch_id": "test_batch_alert",
            "validation_time": "2025-01-30 10:07:00",
            "overall_status": "critical",
            "detailed_checks": {
                "phase_c_simplification_rate": {
                    "status": "critical",
                    "avg_simplification_rate": 0.20,  # 20%，触发警报
                },
                "phase_c_p1_p2_preservation": {
                    "status": "warning",
                    "p1_preservation": {"avg_ratio": 0.97},  # 97%，触发警报
                    "p2_preservation": {"avg_ratio": 0.75},  # 75%，触发警报
                },
                "phase_c_quality_degradation": {
                    "status": "warning",
                    "quality_degradation_stats": {"avg_degradation": 0.12},
                },
                "error_analysis": {
                    "status": "warning",
                    "error_examples_count": 15,
                },
            },
            "statistics": {
                "total_examples": -100,
            },
        }

        # 分析验证结果
        alerts = alert_system.analyze_validation_result(test_result)

        print(f"✅ 警报系统测试完成")
        print(f"   检测到 {len(alerts)} 个警报")

        if alerts:
            for alert in alerts[:3]:  # 显示前3个
                icon = "🔴" if alert["severity"] == "critical" else "🟡"
                print(f"   {icon} {alert['message'][:50]}...")

        return True

    except Exception as e:
        print(f"❌ 警报系统测试失败: {e}")
        return False


def test_rollback_system():
    """测试回滚系统"""
    print("\n🧪 测试回滚系统...")

    try:
        from rollback_system import RollbackSystem

        rollback_system = RollbackSystem()

        # 测试创建备份
        backup_id = rollback_system.create_backup("test_backup", "测试备份")
        print(f"✅ 备份创建测试完成: {backup_id}")

        # 测试列出备份
        backups = rollback_system.list_backups()
        print(f"   找到 {len(backups)} 个备份")

        # 测试回滚评估
        test_result = {
            "batch_id": "test_batch_rollback",
            "validation_time": "2025-01-30 10:08:00",
            "overall_status": "critical",
            "detailed_checks": {
                "phase_c_simplification_rate": {
                    "status": "critical",
                    "avg_simplification_rate": 0.03,  # 3%，触发回滚
                },
            },
        }

        evaluation = rollback_system.evaluate_rollback_need(test_result)
        print(f"   回滚评估: 需要{evaluation.get('needs_rollback', False)}")

        return True

    except Exception as e:
        print(f"❌ 回滚系统测试失败: {e}")
        return False


def test_integrated_system():
    """测试集成系统"""
    print("\n🧪 测试集成系统...")

    # 创建临时测试文件
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        test_report = create_test_report()
        json.dump(test_report, f, indent=2)
        temp_file = f.name

    try:
        # 使用集成系统
        from integrated_validation_system import IntegratedValidationSystem

        system = IntegratedValidationSystem()

        # 测试处理流程
        result = system.process_batch_report(temp_file)

        print(f"✅ 集成系统测试完成")
        print(f"   整体状态: {result.get('overall_status')}")

        # 显示摘要
        system.display_summary(result)

        return True

    except Exception as e:
        print(f"❌ 集成系统测试失败: {e}")
        import traceback

        traceback.print_exc()
        return False
    finally:
        # 清理临时文件
        if os.path.exists(temp_file):
            os.unlink(temp_file)


def main():
    """主测试函数"""
    print("=" * 60)
    print("阶段C验证系统测试套件")
    print("=" * 60)

    tests = [
        ("批次验证", test_batch_validation),
        ("监控仪表板", test_monitoring_dashboard),
        ("警报系统", test_alert_system),
        ("回滚系统", test_rollback_system),
        ("集成系统", test_integrated_system),
    ]

    results = []

    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ {test_name} 测试异常: {e}")
            results.append((test_name, False))

    # 显示测试结果
    print("\n" + "=" * 60)
    print("测试结果摘要")
    print("=" * 60)

    passed = 0
    failed = 0

    for test_name, success in results:
        if success:
            print(f"✅ {test_name}: 通过")
            passed += 1
        else:
            print(f"❌ {test_name}: 失败")
            failed += 1

    print(f"\n总计: {passed} 通过, {failed} 失败")

    if failed == 0:
        print("\n🎉 所有测试通过！")
        return 0
    else:
        print(f"\n⚠️  有 {failed} 个测试失败")
        return 1


if __name__ == "__main__":
    sys.exit(main())
