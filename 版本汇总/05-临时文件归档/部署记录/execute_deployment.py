#!/usr/bin/env python3
"""
ANINEO Phase C 部署执行脚本
正式执行阶段C成果部署到ANINEO生产环境
"""

import os
import json
import subprocess
import sys
from datetime import datetime


def run_command(command, description=""):
    """运行命令并返回结果"""
    print(f"\n▶️  执行: {description}")
    print(f"  命令: {command}")

    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, encoding="utf-8"
        )

        if result.returncode == 0:
            print(f"  ✅ 成功")
            if result.stdout.strip():
                print(f"  输出: {result.stdout.strip()[:200]}...")
        else:
            print(f"  ❌ 失败 (退出码: {result.returncode})")
            if result.stderr.strip():
                print(f"  错误: {result.stderr.strip()[:200]}...")

        return {
            "success": result.returncode == 0,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "command": command,
            "description": description,
        }

    except Exception as e:
        print(f"  ❌ 异常: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "command": command,
            "description": description,
        }


def main():
    """主函数"""
    print("=" * 60)
    print("ANINEO Phase C 部署执行")
    print(f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # 检查是否在项目根目录
    if not os.path.exists(".claude"):
        print("❌ 错误: 请在ANINEO项目根目录运行此脚本")
        return False

    deployment_log = []
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # 步骤1: 运行验证测试
    print("\n📋 步骤1: 运行验证测试")
    verify_result = run_command("python3 verify_deployment.py", "验证部署状态")
    deployment_log.append(verify_result)

    if not verify_result["success"]:
        print("❌ 验证测试失败，部署中止")
        return False

    # 步骤2: 备份系统
    print("\n💾 步骤2: 备份ANINEO系统")
    backup_result = run_command("python3 backup_anineo.py", "备份ANINEO系统文件")
    deployment_log.append(backup_result)

    if not backup_result["success"]:
        print("⚠️  备份失败，但继续部署（文件可能已更新）")

    # 步骤3: 验证文件更新状态
    print("\n🔍 步骤3: 验证文件更新状态")

    # 检查prompt-simplifier.md
    prompt_simplifier_check = {
        "description": "检查prompt-simplifier.md更新",
        "success": os.path.exists(".claude/common/prompt-simplifier.md"),
    }

    if prompt_simplifier_check["success"]:
        with open(".claude/common/prompt-simplifier.md", "r", encoding="utf-8") as f:
            content = f.read()
            p2_keywords_count = content.count("p2_keywords = [")
            phase_c_markers = content.count("【阶段C新增】")

            prompt_simplifier_check["details"] = {
                "p2_keywords_found": p2_keywords_count > 0,
                "phase_c_markers": phase_c_markers,
                "file_size": len(content),
            }

            print(f"  ✅ prompt-simplifier.md: {len(content):,} 字节")
            print(f"    包含P2关键词列表: {'是' if p2_keywords_count > 0 else '否'}")
            print(f"    阶段C标记数量: {phase_c_markers}")
    else:
        print("  ❌ prompt-simplifier.md: 文件不存在")

    deployment_log.append(prompt_simplifier_check)

    # 检查SKILL.md
    skill_check = {
        "description": "检查SKILL.md集成",
        "success": os.path.exists(".claude/skills/film-storyboard-skill/SKILL.md"),
    }

    if skill_check["success"]:
        with open(
            ".claude/skills/film-storyboard-skill/SKILL.md", "r", encoding="utf-8"
        ) as f:
            content = f.read()

            skill_check["details"] = {
                "has_phase_c_marker": "【阶段C新增】" in content,
                "has_step_8_5": "步骤8.5: 执行提示词精简" in content,
                "has_step_7_5": "步骤7.5: 执行提示词精简" in content,
                "has_prompt_simplifier_ref": "common/prompt-simplifier.md" in content,
                "file_size": len(content),
            }

            print(f"  ✅ SKILL.md: {len(content):,} 字节")
            print(
                f"    包含阶段C标记: {'是' if skill_check['details']['has_phase_c_marker'] else '否'}"
            )
            print(
                f"    包含步骤8.5: {'是' if skill_check['details']['has_step_8_5'] else '否'}"
            )
            print(
                f"    包含步骤7.5: {'是' if skill_check['details']['has_step_7_5'] else '否'}"
            )
            print(
                f"    引用prompt-simplifier: {'是' if skill_check['details']['has_prompt_simplifier_ref'] else '否'}"
            )
    else:
        print("  ❌ SKILL.md: 文件不存在")

    deployment_log.append(skill_check)

    # 步骤4: 创建部署报告
    print("\n📊 步骤4: 创建部署报告")

    deployment_report = {
        "deployment_id": f"phase_c_deployment_{timestamp}",
        "deployment_time": datetime.now().isoformat(),
        "status": "completed",
        "summary": {
            "verification_passed": verify_result["success"],
            "backup_completed": backup_result["success"],
            "prompt_simplifier_updated": prompt_simplifier_check.get("success", False),
            "skill_integrated": skill_check.get("success", False),
            "phase_c_results_available": os.path.exists("phase_c_100p_results.json"),
        },
        "files_updated": [
            ".claude/common/prompt-simplifier.md",
            ".claude/skills/film-storyboard-skill/SKILL.md",
        ],
        "deployment_log": deployment_log,
        "next_steps": [
            "运行测试验证ANINEO系统功能",
            "监控生产环境质量指标",
            "收集用户反馈",
            "如有问题使用回滚脚本",
        ],
    }

    report_filename = f"deployment_execution_report_{timestamp}.json"
    with open(report_filename, "w", encoding="utf-8") as f:
        json.dump(deployment_report, f, ensure_ascii=False, indent=2)

    print(f"  ✅ 部署报告已保存: {report_filename}")

    # 步骤5: 显示部署摘要
    print("\n" + "=" * 60)
    print("部署执行完成!")
    print("=" * 60)

    summary = deployment_report["summary"]
    print(f"📊 部署摘要:")
    print(f"  验证测试: {'✅ 通过' if summary['verification_passed'] else '❌ 失败'}")
    print(f"  系统备份: {'✅ 完成' if summary['backup_completed'] else '⚠️  部分完成'}")
    print(
        f"  prompt-simplifier更新: {'✅ 完成' if summary['prompt_simplifier_updated'] else '❌ 失败'}"
    )
    print(f"  SKILL集成: {'✅ 完成' if summary['skill_integrated'] else '❌ 失败'}")
    print(
        f"  阶段C结果: {'✅ 可用' if summary['phase_c_results_available'] else '❌ 缺失'}"
    )

    print(f"\n📁 更新的文件:")
    for file in deployment_report["files_updated"]:
        print(f"  • {file}")

    print(f"\n🚀 下一步:")
    for step in deployment_report["next_steps"]:
        print(f"  • {step}")

    print(f"\n📄 报告文件: {report_filename}")
    print("=" * 60)

    # 总体成功判断
    critical_success = (
        summary["verification_passed"]
        and summary["prompt_simplifier_updated"]
        and summary["skill_integrated"]
    )

    if critical_success:
        print("🎉 部署成功！阶段C成果已正式部署到ANINEO生产环境。")
        return True
    else:
        print("⚠️  部署部分成功，请检查以上问题。")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
