#!/usr/bin/env python3
"""
测试分批次处理系统
"""

import json
import os
from batch_processor import BatchProcessor
from batch_validation import BatchValidator


def test_example_data():
    """测试示例数据加载"""
    print("测试1: 示例数据加载")
    try:
        with open("phase_C_examples.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"✓ 成功加载示例数据: {len(data.get('examples', []))} 个示例")
        return True
    except Exception as e:
        print(f"✗ 加载示例数据失败: {e}")
        return False


def test_batch_processor():
    """测试批次处理器"""
    print("\n测试2: 批次处理器")
    try:
        processor = BatchProcessor("phase_C_examples.json")
        print("✓ 批次处理器初始化成功")

        # 测试批次大小计算
        batch_size = processor.calculate_batch_size(10)
        print(f"✓ 10%批次大小计算: {batch_size}")

        # 测试示例选择
        examples = processor.select_batch_examples(10, "random")
        print(f"✓ 随机选择示例: {len(examples)} 个")

        return True
    except Exception as e:
        print(f"✗ 批次处理器测试失败: {e}")
        return False


def test_single_batch():
    """测试单个批次处理"""
    print("\n测试3: 单个批次处理")
    try:
        processor = BatchProcessor("phase_C_examples.json")

        # 处理10%的批次
        report = processor.process_batch(10)
        print(f"✓ 批次处理完成: {report.batch_id}")
        print(f"  批次大小: {report.batch_size}")
        print(f"  处理时间: {report.duration_seconds:.2f}秒")

        # 保存报告
        processor.save_report(report, "test_batch_report.json")
        print("✓ 批次报告保存成功")

        return True
    except Exception as e:
        print(f"✗ 单个批次处理失败: {e}")
        return False


def test_batch_validation():
    """测试批次验证"""
    print("\n测试4: 批次验证")
    try:
        validator = BatchValidator()

        # 验证测试报告
        result = validator.validate_batch_report("test_batch_report.json")
        print(f"✓ 批次验证完成: {result.get('overall_status')}")

        # 打印摘要
        validator.print_validation_summary(result)

        # 保存验证结果
        validator.save_validation_result(result, "test_validation_result.json")
        print("✓ 验证结果保存成功")

        return True
    except Exception as e:
        print(f"✗ 批次验证失败: {e}")
        return False


def test_multiple_batches():
    """测试多个批次处理"""
    print("\n测试5: 多个批次处理")
    try:
        processor = BatchProcessor("phase_C_examples.json")

        # 运行10%和30%批次
        processor.run_multiple_batches([10, 30])
        print("✓ 多批次处理完成")

        return True
    except Exception as e:
        print(f"✗ 多批次处理失败: {e}")
        return False


def cleanup_test_files():
    """清理测试文件"""
    test_files = [
        "test_batch_report.json",
        "test_validation_result.json",
        "batch_processing.log",
        "batch_validation.log",
    ]

    for file in test_files:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"清理文件: {file}")
            except:
                pass


def main():
    """主测试函数"""
    print("=" * 60)
    print("分批次处理系统测试")
    print("=" * 60)

    # 运行所有测试
    tests = [
        test_example_data,
        test_batch_processor,
        test_single_batch,
        test_batch_validation,
        test_multiple_batches,
    ]

    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"测试异常: {e}")
            results.append(False)

    # 显示测试结果
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)

    passed = sum(results)
    total = len(results)

    for i, (test, result) in enumerate(zip(tests, results), 1):
        status = "✓ 通过" if result else "✗ 失败"
        print(f"测试{i}: {test.__name__} - {status}")

    print(f"\n总计: {passed}/{total} 个测试通过 ({passed / total * 100:.1f}%)")

    if passed == total:
        print("\n🎉 所有测试通过！系统功能正常。")
    else:
        print(f"\n⚠️  {total - passed} 个测试失败，请检查问题。")

    # 清理测试文件
    print("\n清理测试文件...")
    cleanup_test_files()

    print("\n测试完成！")


if __name__ == "__main__":
    main()
