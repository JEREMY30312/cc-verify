#!/usr/bin/env python3
"""
ANINEO 系统回滚脚本
从备份恢复ANINEO系统文件
"""

import os
import shutil
import json
import sys
from datetime import datetime


class ANINEORollback:
    def __init__(self):
        self.backups_dir = ".claude/backups"
        self.rollback_report = {
            "rollback_time": datetime.now().isoformat(),
            "files_restored": [],
            "errors": [],
            "status": "in_progress",
        }

    def list_backups(self):
        """列出所有可用的备份"""
        if not os.path.exists(self.backups_dir):
            print("❌ 备份目录不存在")
            return []

        backups = []
        for item in os.listdir(self.backups_dir):
            item_path = os.path.join(self.backups_dir, item)
            if os.path.isdir(item_path) and item.startswith("backup_"):
                # 提取时间戳
                timestamp = item.replace("backup_", "")

                # 检查备份报告
                report_path = os.path.join(item_path, "backup_report.json")
                if os.path.exists(report_path):
                    try:
                        with open(report_path, "r", encoding="utf-8") as f:
                            report = json.load(f)

                        backups.append(
                            {
                                "name": item,
                                "timestamp": timestamp,
                                "backup_time": report.get("backup_time", "未知"),
                                "file_count": len(report.get("files_backed_up", [])),
                                "total_size": report.get("total_size_bytes", 0),
                                "path": item_path,
                            }
                        )
                    except:
                        backups.append(
                            {
                                "name": item,
                                "timestamp": timestamp,
                                "backup_time": "未知",
                                "file_count": "未知",
                                "total_size": "未知",
                                "path": item_path,
                            }
                        )
                else:
                    backups.append(
                        {
                            "name": item,
                            "timestamp": timestamp,
                            "backup_time": "未知",
                            "file_count": "未知",
                            "total_size": "未知",
                            "path": item_path,
                        }
                    )

        # 按时间戳排序（最新的在前）
        backups.sort(key=lambda x: x["timestamp"], reverse=True)
        return backups

    def select_backup(self):
        """选择要恢复的备份"""
        backups = self.list_backups()

        if not backups:
            print("❌ 没有找到可用的备份")
            return None

        print("=" * 60)
        print("可用的备份列表:")
        print("=" * 60)

        for i, backup in enumerate(backups, 1):
            print(f"{i}. {backup['name']}")
            print(f"   时间: {backup['backup_time']}")
            print(f"   文件数: {backup['file_count']}")
            print(f"   大小: {backup['total_size']:,} bytes")
            print()

        while True:
            try:
                choice = input("请选择要恢复的备份编号 (输入 'q' 退出): ").strip()

                if choice.lower() == "q":
                    return None

                index = int(choice) - 1
                if 0 <= index < len(backups):
                    return backups[index]
                else:
                    print(f"❌ 无效的选择，请输入 1-{len(backups)} 之间的数字")

            except ValueError:
                print("❌ 请输入有效的数字")
            except KeyboardInterrupt:
                print("\n操作取消")
                return None

    def restore_file(self, backup_path, source_rel_path, target_path):
        """恢复单个文件"""
        try:
            # 构建备份文件路径
            backup_file_path = os.path.join(backup_path, source_rel_path)

            if not os.path.exists(backup_file_path):
                self.rollback_report["errors"].append(
                    f"备份文件不存在: {backup_file_path}"
                )
                return False

            # 确保目标目录存在
            os.makedirs(os.path.dirname(target_path), exist_ok=True)

            # 备份当前文件（如果存在）
            if os.path.exists(target_path):
                current_backup = f"{target_path}.pre_rollback"
                shutil.copy2(target_path, current_backup)

            # 恢复文件
            shutil.copy2(backup_file_path, target_path)

            self.rollback_report["files_restored"].append(
                {
                    "source": backup_file_path,
                    "target": target_path,
                    "restore_time": datetime.now().isoformat(),
                    "success": True,
                }
            )

            print(f"✅ 恢复成功: {source_rel_path}")
            return True

        except Exception as e:
            error_msg = f"恢复失败 {source_rel_path}: {str(e)}"
            self.rollback_report["errors"].append(error_msg)
            print(f"❌ {error_msg}")
            return False

    def restore_from_backup(self, backup_info):
        """从指定备份恢复"""
        print("=" * 60)
        print(f"开始恢复备份: {backup_info['name']}")
        print(f"备份时间: {backup_info['backup_time']}")
        print("=" * 60)

        backup_path = backup_info["path"]
        report_path = os.path.join(backup_path, "backup_report.json")

        if not os.path.exists(report_path):
            print("❌ 备份报告不存在，无法恢复")
            return False

        try:
            with open(report_path, "r", encoding="utf-8") as f:
                report = json.load(f)
        except Exception as e:
            print(f"❌ 读取备份报告失败: {str(e)}")
            return False

        files_to_restore = report.get("files_backed_up", [])

        if not files_to_restore:
            print("❌ 备份报告中未找到文件列表")
            return False

        print(f"📊 准备恢复 {len(files_to_restore)} 个文件")
        print("-" * 60)

        restored_count = 0
        total_count = len(files_to_restore)

        # 恢复文件
        for file_info in files_to_restore:
            source_path = file_info.get("source")
            target_path = file_info.get("target", "").replace(backup_path + "/", "")

            if source_path and target_path:
                # 从备份路径提取相对路径
                backup_rel_path = os.path.relpath(source_path, ".")
                if self.restore_file(backup_path, backup_rel_path, source_path):
                    restored_count += 1

        # 保存回滚报告
        self.rollback_report["status"] = "completed"
        self.rollback_report["backup_used"] = backup_info["name"]
        self.rollback_report["files_restored_count"] = restored_count
        self.rollback_report["total_files_count"] = total_count
        self.rollback_report["success_rate"] = f"{restored_count}/{total_count}"

        report_filename = (
            f"rollback_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        with open(report_filename, "w", encoding="utf-8") as f:
            json.dump(self.rollback_report, f, ensure_ascii=False, indent=2)

        print("\n" + "=" * 60)
        print("恢复完成!")
        print("=" * 60)
        print(f"总文件数: {total_count}")
        print(f"成功恢复: {restored_count}")
        print(f"成功率: {restored_count / total_count * 100:.1f}%")

        if restored_count == total_count:
            print("✅ 所有文件恢复成功!")
        else:
            print(f"⚠️  部分文件恢复失败，请检查错误信息")

        print(f"回滚报告: {report_filename}")
        print("=" * 60)

        return restored_count > 0

    def verify_restoration(self):
        """验证恢复结果"""
        print("\n🔍 验证恢复结果...")

        verification_passed = True

        # 检查关键文件是否存在
        critical_files = [
            ".claude/common/prompt-simplifier.md",
            ".claude/skills/film-storyboard-skill/SKILL.md",
            ".claude/skills/animator-skill/SKILL.md",
        ]

        for filepath in critical_files:
            if os.path.exists(filepath):
                print(f"✅ 关键文件存在: {filepath}")
            else:
                print(f"❌ 关键文件不存在: {filepath}")
                verification_passed = False

        # 检查文件内容（抽样）
        sample_file = ".claude/common/prompt-simplifier.md"
        if os.path.exists(sample_file):
            try:
                with open(sample_file, "r", encoding="utf-8") as f:
                    content = f.read(500)

                if "P2元素" in content and "p2_keywords" in content:
                    print(f"✅ 文件内容验证通过: {sample_file}")
                else:
                    print(f"❌ 文件内容异常: {sample_file}")
                    verification_passed = False
            except Exception as e:
                print(f"❌ 读取文件失败 {sample_file}: {str(e)}")
                verification_passed = False

        print(f"\n验证结果: {'✅ 通过' if verification_passed else '❌ 失败'}")
        return verification_passed


def main():
    """主函数"""
    # 检查是否在项目根目录
    if not os.path.exists(".claude"):
        print("错误: 请在ANINEO项目根目录运行此脚本")
        return False

    rollback = ANINEORollback()

    try:
        # 列出并选择备份
        backup_info = rollback.select_backup()
        if not backup_info:
            print("操作取消")
            return False

        # 确认操作
        print(f"\n⚠️  警告: 即将恢复备份 {backup_info['name']}")
        print(f"这将覆盖当前系统中的文件")

        confirm = input("确认恢复? (输入 'yes' 确认): ").strip().lower()
        if confirm != "yes":
            print("操作取消")
            return False

        # 执行恢复
        if not rollback.restore_from_backup(backup_info):
            print("恢复失败")
            return False

        # 验证恢复
        if not rollback.verify_restoration():
            print("恢复验证失败")
            return False

        print("\n🎉 恢复完成且验证通过！")
        print("建议运行验证脚本检查系统状态:")
        print("  python3 verify_deployment.py")

        return True

    except Exception as e:
        print(f"恢复过程中发生异常: {str(e)}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
