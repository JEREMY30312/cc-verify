#!/usr/bin/env python3
"""
ANINEO Phase C 部署验证脚本
验证阶段C成果是否成功部署到ANINEO生产环境
"""

import os
import json
import re
from datetime import datetime


def check_file_exists(filepath):
    """检查文件是否存在"""
    exists = os.path.exists(filepath)
    print(f"✓ {filepath}: {'存在' if exists else '不存在'}")
    return exists


def check_p2_keywords_in_prompt_simplifier():
    """检查prompt-simplifier.md中的P2关键词"""
    filepath = ".claude/common/prompt-simplifier.md"
    if not os.path.exists(filepath):
        print(f"✗ {filepath} 不存在")
        return False

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 检查P2元素部分
    p2_section_pattern = r"#### P2元素（高优先级 - ≥90%保留）"
    has_p2_section = re.search(p2_section_pattern, content) is not None

    # 检查P2关键词数量
    p2_keywords_pattern = r"p2_keywords = \[.*?\]"
    p2_keywords_match = re.search(p2_keywords_pattern, content, re.DOTALL)

    if p2_keywords_match:
        p2_keywords_str = p2_keywords_match.group(0)
        # 粗略估计关键词数量
        keyword_count = len(re.findall(r'"[^"]+"', p2_keywords_str))
        print(f"✓ prompt-simplifier.md: P2关键词数量 ≈ {keyword_count}")
    else:
        print(f"✗ prompt-simplifier.md: 未找到P2关键词列表")
        return False

    return has_p2_section and p2_keywords_match is not None


def check_skill_integration():
    """检查SKILL.md中的阶段C集成"""
    filepath = ".claude/skills/film-storyboard-skill/SKILL.md"
    if not os.path.exists(filepath):
        print(f"✗ {filepath} 不存在")
        return False

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 检查阶段C新增标记
    phase_c_markers = [
        "【阶段C新增】",
        "步骤8.5: 执行提示词精简",
        "步骤7.5: 执行提示词精简",
        "common/prompt-simplifier.md",
    ]

    results = []
    for marker in phase_c_markers:
        found = marker in content
        results.append(found)
        print(f"✓ SKILL.md: {'包含' if found else '不包含'} '{marker}'")

    return all(results)


def check_deployment_scripts():
    """检查部署脚本是否存在"""
    scripts = [
        "deploy_phase_c.py",
        "backup_anineo.py",
        "rollback_anineo.py",
        "verify_deployment.py",
    ]

    results = []
    for script in scripts:
        exists = os.path.exists(script)
        results.append(exists)
        print(f"✓ {script}: {'存在' if exists else '不存在'}")

    return all(results)


def check_phase_c_results():
    """检查阶段C结果文件"""
    results_files = [
        "phase_c_100p_results.json",
        "phase_C_final_completion_report.md",
        "p2_keywords_extended.md",
    ]

    results = []
    for file in results_files:
        exists = os.path.exists(file)
        results.append(exists)
        print(f"✓ {file}: {'存在' if exists else '不存在'}")

    return all(results)


def run_verification_tests():
    """运行验证测试"""
    print("=" * 60)
    print("ANINEO Phase C 部署验证")
    print(f"验证时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    test_results = []

    print("\n1. 检查关键文件是否存在:")
    test_results.append(check_file_exists(".claude/common/prompt-simplifier.md"))
    test_results.append(
        check_file_exists(".claude/skills/film-storyboard-skill/SKILL.md")
    )

    print("\n2. 检查prompt-simplifier.md中的P2关键词:")
    test_results.append(check_p2_keywords_in_prompt_simplifier())

    print("\n3. 检查SKILL.md中的阶段C集成:")
    test_results.append(check_skill_integration())

    print("\n4. 检查部署脚本:")
    test_results.append(check_deployment_scripts())

    print("\n5. 检查阶段C结果文件:")
    test_results.append(check_phase_c_results())

    print("\n" + "=" * 60)
    print("验证结果汇总:")
    print("=" * 60)

    passed = sum(test_results)
    total = len(test_results)

    print(f"通过测试: {passed}/{total}")
    print(f"成功率: {passed / total * 100:.1f}%")

    if passed == total:
        print("✅ 所有验证测试通过！部署成功。")
        return True
    else:
        print("❌ 部分验证测试失败。请检查以上输出。")
        return False


def main():
    """主函数"""
    try:
        success = run_verification_tests()

        # 生成验证报告
        report = {
            "verification_time": datetime.now().isoformat(),
            "tests_passed": sum(
                [
                    check_p2_keywords_in_prompt_simplifier(),
                    check_skill_integration(),
                    check_deployment_scripts(),
                    check_phase_c_results(),
                ]
            ),
            "tests_total": 4,
            "overall_success": success,
            "details": {
                "prompt_simplifier_updated": check_p2_keywords_in_prompt_simplifier(),
                "skill_integration_complete": check_skill_integration(),
                "deployment_scripts_ready": check_deployment_scripts(),
                "phase_c_results_available": check_phase_c_results(),
            },
        }

        # 保存验证报告
        with open("deployment_verification_report.json", "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        print(f"\n验证报告已保存到: deployment_verification_report.json")

        return success

    except Exception as e:
        print(f"验证过程中发生错误: {str(e)}")
        return False


if __name__ == "__main__":
    exit(0 if main() else 1)
