#!/usr/bin/env python3
"""
ANINEO 系统备份脚本
备份所有关键ANINEO系统文件
"""

import os
import shutil
import json
import sys
from datetime import datetime
import hashlib


class ANINEOBackup:
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.backup_dir = f".claude/backups/backup_{self.timestamp}"
        self.backup_report = {
            "backup_time": self.timestamp,
            "files_backed_up": [],
            "total_size_bytes": 0,
            "checksums": {},
            "status": "in_progress",
        }

    def calculate_checksum(self, filepath):
        """计算文件校验和"""
        try:
            with open(filepath, "rb") as f:
                file_hash = hashlib.md5()
                chunk = f.read(8192)
                while chunk:
                    file_hash.update(chunk)
                    chunk = f.read(8192)
            return file_hash.hexdigest()
        except Exception as e:
            print(f"计算校验和失败 {filepath}: {str(e)}")
            return None

    def backup_file(self, source_path, category):
        """备份单个文件"""
        if not os.path.exists(source_path):
            print(f"⚠️  文件不存在，跳过: {source_path}")
            return False

        try:
            # 创建目标目录结构
            relative_path = os.path.relpath(source_path, ".")
            target_path = os.path.join(self.backup_dir, relative_path)
            os.makedirs(os.path.dirname(target_path), exist_ok=True)

            # 复制文件
            shutil.copy2(source_path, target_path)

            # 计算文件信息
            file_size = os.path.getsize(source_path)
            checksum = self.calculate_checksum(source_path)

            # 记录备份信息
            self.backup_report["files_backed_up"].append(
                {
                    "source": source_path,
                    "target": target_path,
                    "size_bytes": file_size,
                    "checksum": checksum,
                    "category": category,
                    "backup_time": datetime.now().isoformat(),
                }
            )

            self.backup_report["total_size_bytes"] += file_size
            if checksum:
                self.backup_report["checksums"][source_path] = checksum

            print(f"✅ 备份成功: {source_path} -> {target_path} ({file_size} bytes)")
            return True

        except Exception as e:
            print(f"❌ 备份失败 {source_path}: {str(e)}")
            return False

    def get_anineo_files(self):
        """获取所有ANINEO系统文件"""
        categories = {
            "common_modules": [
                ".claude/common/prompt-simplifier.md",
                ".claude/common/quality-check.md",
                ".claude/common/keyframe-selector.md",
                ".claude/common/beat-analyzer.md",
                ".claude/common/layout-calculator.md",
                ".claude/common/coherence-checker.md",
                ".claude/common/director-decision.md",
                ".claude/common/exception-handler.md",
                ".claude/common/data-validator.md",
            ],
            "skill_files": [
                ".claude/skills/film-storyboard-skill/SKILL.md",
                ".claude/skills/animator-skill/SKILL.md",
                ".claude/skills/storyboard-review-skill/SKILL.md",
            ],
            "workflow_files": [
                ".claude/workflows/breakdown-workflow.md",
                ".claude/workflows/beatboard-workflow.md",
                ".claude/workflows/sequence-workflow.md",
                ".claude/workflows/motion-workflow.md",
                ".claude/workflows/review-workflow.md",
                ".claude/workflows/interactive-workflow.md",
            ],
            "configuration_files": ["AGENTS.md", ".agent-state.json"],
            "phase_c_results": [
                "phase_c_100p_results.json",
                "phase_C_final_completion_report.md",
                "p2_keywords_extended.md",
                "deploy_phase_c.py",
                "verify_deployment.py",
            ],
        }

        return categories

    def backup_all(self):
        """备份所有文件"""
        print("=" * 60)
        print(f"ANINEO 系统备份开始")
        print(f"备份时间: {self.timestamp}")
        print(f"备份目录: {self.backup_dir}")
        print("=" * 60)

        # 创建备份目录
        os.makedirs(self.backup_dir, exist_ok=True)

        # 获取所有文件
        file_categories = self.get_anineo_files()

        total_files = 0
        successful_files = 0

        # 按类别备份文件
        for category, file_list in file_categories.items():
            print(f"\n📁 备份类别: {category}")
            print("-" * 40)

            for filepath in file_list:
                total_files += 1
                if self.backup_file(filepath, category):
                    successful_files += 1

        # 保存备份报告
        self.backup_report["status"] = "completed"
        self.backup_report["success_rate"] = f"{successful_files}/{total_files}"

        report_path = os.path.join(self.backup_dir, "backup_report.json")
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(self.backup_report, f, ensure_ascii=False, indent=2)

        print("\n" + "=" * 60)
        print("备份完成!")
        print("=" * 60)
        print(f"总文件数: {total_files}")
        print(f"成功备份: {successful_files}")
        print(f"成功率: {successful_files / total_files * 100:.1f}%")
        print(f"总大小: {self.backup_report['total_size_bytes']:,} bytes")
        print(f"备份目录: {self.backup_dir}")
        print(f"报告文件: {report_path}")
        print("=" * 60)

        return successful_files == total_files

    def verify_backup(self):
        """验证备份完整性"""
        print("\n🔍 验证备份完整性...")

        if not os.path.exists(self.backup_dir):
            print("❌ 备份目录不存在")
            return False

        verification_results = []

        # 检查备份报告
        report_path = os.path.join(self.backup_dir, "backup_report.json")
        if os.path.exists(report_path):
            try:
                with open(report_path, "r", encoding="utf-8") as f:
                    report = json.load(f)

                print(f"✅ 备份报告存在: {report_path}")
                verification_results.append(True)

                # 验证文件数量
                expected_files = len(report.get("files_backed_up", []))
                actual_files = len(
                    [
                        f
                        for f in os.listdir(self.backup_dir)
                        if os.path.isfile(os.path.join(self.backup_dir, f))
                    ]
                )

                print(f"📊 报告文件数: {expected_files}, 实际文件数: {actual_files}")
                verification_results.append(actual_files >= expected_files)

            except Exception as e:
                print(f"❌ 读取备份报告失败: {str(e)}")
                verification_results.append(False)
        else:
            print("❌ 备份报告不存在")
            verification_results.append(False)

        # 抽样验证文件
        sample_files = [
            os.path.join(self.backup_dir, ".claude/common/prompt-simplifier.md"),
            os.path.join(
                self.backup_dir, ".claude/skills/film-storyboard-skill/SKILL.md"
            ),
        ]

        for sample_file in sample_files:
            if os.path.exists(sample_file):
                print(f"✅ 抽样文件存在: {os.path.basename(sample_file)}")
                verification_results.append(True)
            else:
                print(f"❌ 抽样文件不存在: {os.path.basename(sample_file)}")
                verification_results.append(False)

        all_passed = all(verification_results)
        print(f"\n验证结果: {'✅ 全部通过' if all_passed else '❌ 部分失败'}")
        return all_passed


def main():
    """主函数"""
    # 检查是否在项目根目录
    if not os.path.exists(".claude"):
        print("错误: 请在ANINEO项目根目录运行此脚本")
        return False

    backup = ANINEOBackup()

    try:
        # 执行备份
        if not backup.backup_all():
            print("备份失败，请检查错误信息")
            return False

        # 验证备份
        if not backup.verify_backup():
            print("备份验证失败")
            return False

        print("\n🎉 备份完成且验证通过！")
        print(f"备份位置: {backup.backup_dir}")
        print(f"如需恢复，请使用 rollback_anineo.py 脚本")

        return True

    except Exception as e:
        print(f"备份过程中发生异常: {str(e)}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
