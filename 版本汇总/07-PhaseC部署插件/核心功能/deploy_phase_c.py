#!/usr/bin/env python3
"""
ANINEO Phase C Deployment Script
Deploys prompt simplifier updates to production environment.

Requirements:
1. Backup existing ANINEO system files
2. Update files with phase C modifications
3. Create rollback capability
4. Verify deployment success

Files to update:
1. .claude/common/prompt-simplifier.md (already being updated separately)
2. .claude/skills/film-storyboard-skill/SKILL.md (already has phase C integration, just verify)
"""

import os
import sys
import shutil
import datetime
import json
import re
import subprocess
from pathlib import Path
from typing import List, Dict, Tuple, Optional


class PhaseCDeployment:
    def __init__(self, project_root: str = "."):
        """Initialize deployment manager."""
        self.project_root = Path(project_root).resolve()
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        self.backup_dir = self.project_root / ".backups" / f"phase-c-{self.timestamp}"
        self.log_file = self.project_root / "deploy-phase-c.log"
        self.rollback_script = self.project_root / "rollback-phase-c.py"
        self.verification_script = self.project_root / "verify-phase-c.py"

        # Target files to update/verify
        self.target_files = [
            ".claude/common/prompt-simplifier.md",
            ".claude/skills/film-storyboard-skill/SKILL.md",
        ]

        # Phase C integration markers to check
        self.phase_c_markers = [
            "阶段C新增",
            "提示词精简算法",
            "efficient_simplifier_v2",
        ]

        # P2 keyword categories to verify
        self.p2_categories = [
            "动作场景",
            "情感场景",
            "建立场景",
            "悬疑场景",
            "对话场景",
        ]

        self.deployment_report = {
            "timestamp": self.timestamp,
            "status": "pending",
            "backup_created": False,
            "files_updated": [],
            "verification_passed": False,
            "rollback_available": False,
            "errors": [],
        }

    def log(self, message: str, level: str = "INFO"):
        """Log message to console and file."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] [{level}] {message}"
        print(log_message)

        # Append to log file
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(log_message + "\n")

    def backup_file(self, file_path: Path) -> bool:
        """Backup a single file."""
        try:
            if file_path.exists():
                backup_path = self.backup_dir / file_path.name
                shutil.copy2(file_path, backup_path)
                self.log(f"Backed up: {file_path} -> {backup_path}")
                return True
            else:
                self.log(f"File not found: {file_path}", "WARNING")
                return False
        except Exception as e:
            self.log(f"Error backing up {file_path}: {e}", "ERROR")
            return False

    def backup_all_files(self) -> bool:
        """Backup all target files."""
        self.log("📦 Creating backup directory...")
        self.backup_dir.mkdir(parents=True, exist_ok=True)

        success = True
        for file_rel in self.target_files:
            file_path = self.project_root / file_rel
            if not self.backup_file(file_path):
                success = False

        self.deployment_report["backup_created"] = success
        return success

    def verify_file_exists(self, file_path: Path) -> bool:
        """Verify that a file exists."""
        exists = file_path.exists()
        if exists:
            self.log(f"✅ Verified: {file_path}")
        else:
            self.log(f"❌ Missing: {file_path}", "ERROR")
        return exists

    def verify_all_files_exist(self) -> bool:
        """Verify all target files exist."""
        self.log("🔍 Verifying target files...")

        all_exist = True
        for file_rel in self.target_files:
            file_path = self.project_root / file_rel
            if not self.verify_file_exists(file_path):
                all_exist = False

        return all_exist

    def check_phase_c_integration(self) -> Dict:
        """Check if Phase C integration exists in SKILL.md."""
        self.log("🔍 Checking SKILL.md integration...")

        skill_path = self.project_root / ".claude/skills/film-storyboard-skill/SKILL.md"
        if not skill_path.exists():
            return {"found": False, "markers": [], "error": "SKILL.md not found"}

        try:
            with open(skill_path, "r", encoding="utf-8") as f:
                content = f.read()

            found_markers = []
            for marker in self.phase_c_markers:
                if marker in content:
                    found_markers.append(marker)

            if found_markers:
                self.log(f"✅ Phase C integration found: {', '.join(found_markers)}")
                return {"found": True, "markers": found_markers}
            else:
                self.log("⚠️ Phase C integration not found in SKILL.md", "WARNING")
                return {"found": False, "markers": []}

        except Exception as e:
            self.log(f"Error reading SKILL.md: {e}", "ERROR")
            return {"found": False, "markers": [], "error": str(e)}

    def verify_p2_keywords(self) -> Dict:
        """Verify P2 keywords in prompt-simplifier.md."""
        self.log("🔍 Verifying P2 keywords in prompt-simplifier.md...")

        prompt_path = self.project_root / ".claude/common/prompt-simplifier.md"
        if not prompt_path.exists():
            return {
                "found_categories": 0,
                "keyword_lines": 0,
                "error": "File not found",
            }

        try:
            with open(prompt_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Count keyword lines (lines starting with "- ")
            keyword_lines = len(re.findall(r"^\s*-\s+", content, re.MULTILINE))

            # Check for scene type categories
            found_categories = 0
            for category in self.p2_categories:
                if category in content:
                    found_categories += 1
                    self.log(f"  ✅ Found category: {category}")
                else:
                    self.log(f"  ❌ Missing category: {category}", "WARNING")

            self.log(f"  Found {keyword_lines} keyword lines")
            self.log(f"  Found {found_categories}/5 scene type categories")

            return {
                "found_categories": found_categories,
                "keyword_lines": keyword_lines,
                "all_categories_present": found_categories >= 5,
            }

        except Exception as e:
            self.log(f"Error reading prompt-simplifier.md: {e}", "ERROR")
            return {"found_categories": 0, "keyword_lines": 0, "error": str(e)}

    def create_rollback_script(self) -> bool:
        """Create Python rollback script."""
        self.log("🔄 Creating rollback script...")

        script_content = '''#!/usr/bin/env python3
"""
ANINEO Phase C Rollback Script
Restores files from backup directory.
"""

import os
import sys
import shutil
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Rollback Phase C deployment")
    parser.add_argument("--backup-dir", required=True, help="Backup directory path")
    parser.add_argument("--dry-run", action="store_true", help="Dry run without actual restoration")
    args = parser.parse_args()
    
    backup_dir = Path(args.backup_dir)
    project_root = Path(".").resolve()
    
    if not backup_dir.exists():
        print(f"❌ Backup directory not found: {backup_dir}")
        print("Available backups:")
        backup_parent = project_root / ".backups"
        if backup_parent.exists():
            for item in backup_parent.iterdir():
                if item.is_dir():
                    print(f"  - {item.name}")
        else:
            print("  No backups found")
        sys.exit(1)
    
    print(f"📦 Restoring files from backup: {backup_dir}")
    
    # Files to restore
    target_files = [
        ".claude/common/prompt-simplifier.md",
        ".claude/skills/film-storyboard-skill/SKILL.md"
    ]
    
    restored_count = 0
    for file_rel in target_files:
        file_path = project_root / file_rel
        backup_file = backup_dir / Path(file_rel).name
        
        if backup_file.exists():
            if not args.dry_run:
                shutil.copy2(backup_file, file_path)
            print(f"  ✅ {'Would restore' if args.dry_run else 'Restored'}: {file_path}")
            restored_count += 1
        else:
            print(f"  ⚠️  Backup not found: {backup_file}")
    
    print(f"\\n{'🎉 Rollback completed!' if not args.dry_run else '✅ Dry run completed'}")
    print(f"Restored {restored_count}/{len(target_files)} files")
    
    if args.dry_run:
        print("\\nTo actually perform rollback, run:")
        print(f"python {__file__} --backup-dir {backup_dir}")

if __name__ == "__main__":
    main()
'''

        try:
            with open(self.rollback_script, "w", encoding="utf-8") as f:
                f.write(script_content)

            # Make executable
            os.chmod(self.rollback_script, 0o755)

            self.log(f"✅ Created rollback script: {self.rollback_script}")
            self.deployment_report["rollback_available"] = True
            return True

        except Exception as e:
            self.log(f"Error creating rollback script: {e}", "ERROR")
            return False

    def create_verification_script(self) -> bool:
        """Create Python verification script."""
        self.log("✅ Creating verification script...")

        script_content = '''#!/usr/bin/env python3
"""
ANINEO Phase C Verification Script
Verifies Phase C deployment success.
"""

import os
import re
import sys
from pathlib import Path

def check_p2_keywords():
    """Check P2 keywords in prompt-simplifier.md."""
    print("1. Checking P2 keywords...")
    
    prompt_path = Path(".claude/common/prompt-simplifier.md")
    if not prompt_path.exists():
        print("   ❌ File not found: prompt-simplifier.md")
        return 0, 0
    
    try:
        with open(prompt_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Count P2 keyword lines
        p2_section_match = re.search(r'#### P2元素.*?(?=####|\\Z)', content, re.DOTALL)
        if p2_section_match:
            p2_section = p2_section_match.group(0)
            keyword_lines = len(re.findall(r'^\\s*-\\s+', p2_section, re.MULTILINE))
        else:
            keyword_lines = 0
        
        print(f"   P2 keyword lines: {keyword_lines}")
        
        # Check scene type categories
        print("2. Checking scene type categories...")
        scene_categories = 0
        categories = ["动作场景", "情感场景", "建立场景", "悬疑场景", "对话场景"]
        
        for category in categories:
            if category in content:
                print(f"   ✅ Found: {category}")
                scene_categories += 1
            else:
                print(f"   ❌ Missing: {category}")
        
        print(f"   Total scene categories: {scene_categories}/5")
        
        return keyword_lines, scene_categories
        
    except Exception as e:
        print(f"   ❌ Error reading file: {e}")
        return 0, 0

def check_skill_integration():
    """Check Phase C integration in SKILL.md."""
    print("3. Checking SKILL.md integration...")
    
    skill_path = Path(".claude/skills/film-storyboard-skill/SKILL.md")
    if not skill_path.exists():
        print("   ❌ File not found: SKILL.md")
        return 0
    
    try:
        with open(skill_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        integration_count = content.count("阶段C新增")
        if integration_count > 0:
            print(f"   ✅ Phase C integration points: {integration_count}")
        else:
            print("   ❌ No Phase C integration found")
        
        return integration_count
        
    except Exception as e:
        print(f"   ❌ Error reading file: {e}")
        return 0

def main():
    print("🔍 Phase C Verification Started")
    print("================================")
    
    # Run checks
    keyword_lines, scene_categories = check_p2_keywords()
    integration_count = check_skill_integration()
    
    print("\\n📊 Verification Summary:")
    print("========================")
    print(f"P2 Keywords: {keyword_lines} lines")
    print(f"Scene Categories: {scene_categories}/5")
    print(f"SKILL Integration: {'✅ Present' if integration_count > 0 else '❌ Missing'}")
    
    # Determine success
    success = scene_categories >= 5 and integration_count > 0
    
    if success:
        print("\\n🎉 Phase C deployment verified successfully!")
        sys.exit(0)
    else:
        print("\\n⚠️  Verification issues found. Please check the deployment.")
        sys.exit(1)

if __name__ == "__main__":
    main()
'''

        try:
            with open(self.verification_script, "w", encoding="utf-8") as f:
                f.write(script_content)

            # Make executable
            os.chmod(self.verification_script, 0o755)

            self.log(f"✅ Created verification script: {self.verification_script}")
            return True

        except Exception as e:
            self.log(f"Error creating verification script: {e}", "ERROR")
            return False

    def run_verification(self) -> bool:
        """Run verification tests."""
        self.log("✅ Running verification tests...")

        try:
            # Run the verification script
            result = subprocess.run(
                [sys.executable, str(self.verification_script)],
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            # Print output
            print(result.stdout)
            if result.stderr:
                print(result.stderr, file=sys.stderr)

            verification_passed = result.returncode == 0
            self.deployment_report["verification_passed"] = verification_passed

            if verification_passed:
                self.log("🎉 Verification passed!")
            else:
                self.log("⚠️ Verification failed!", "WARNING")

            return verification_passed

        except Exception as e:
            self.log(f"Error running verification: {e}", "ERROR")
            return False

    def generate_deployment_report(self) -> bool:
        """Generate deployment report."""
        self.log("📋 Generating deployment report...")

        report_path = (
            self.project_root / f"deployment-report-phase-c-{self.timestamp}.json"
        )

        try:
            with open(report_path, "w", encoding="utf-8") as f:
                json.dump(self.deployment_report, f, indent=2, ensure_ascii=False)

            self.log(f"✅ Deployment report saved to: {report_path}")
            return True

        except Exception as e:
            self.log(f"Error generating report: {e}", "ERROR")
            return False

    def deploy(self) -> bool:
        """Main deployment process."""
        self.log("🚀 ANINEO Phase C Deployment Started")
        self.log("======================================")

        try:
            # Step 1: Backup existing files
            self.log("\\n1. 📦 Backing up existing files...")
            if not self.backup_all_files():
                self.log("❌ Backup failed. Aborting deployment.", "ERROR")
                self.deployment_report["status"] = "failed"
                self.deployment_report["errors"].append("Backup failed")
                return False

            # Step 2: Verify files exist
            self.log("\\n2. 🔍 Verifying target files...")
            if not self.verify_all_files_exist():
                self.log(
                    "❌ Some target files are missing. Aborting deployment.", "ERROR"
                )
                self.deployment_report["status"] = "failed"
                self.deployment_report["errors"].append("Target files missing")
                return False

            # Step 3: Check current integration status
            self.log("\\n3. 🔍 Checking current integration status...")
            integration_result = self.check_phase_c_integration()

            # Step 4: Verify P2 keywords (pre-update)
            self.log("\\n4. 🔍 Checking current P2 keywords...")
            p2_result = self.verify_p2_keywords()

            # Step 5: Create rollback capability
            self.log("\\n5. 🔄 Creating rollback capability...")
            self.create_rollback_script()

            # Step 6: Create verification script
            self.log("\\n6. ✅ Creating verification script...")
            self.create_verification_script()

            # Step 7: Run verification
            self.log("\\n7. 🔍 Running verification tests...")
            verification_passed = self.run_verification()

            # Step 8: Generate report
            self.log("\\n8. 📋 Generating deployment report...")
            self.generate_deployment_report()

            # Update deployment status
            if verification_passed:
                self.deployment_report["status"] = "success"
                self.log("\\n🎉 Phase C deployment completed successfully!")
            else:
                self.deployment_report["status"] = "partial_success"
                self.log(
                    "\\n⚠️ Phase C deployment completed with verification warnings.",
                    "WARNING",
                )

            # Print summary
            self.log("\\n======================================")
            self.log("🚀 Deployment Summary")
            self.log("======================================")
            self.log(f"Backup Location: {self.backup_dir}")
            self.log(f"Rollback Script: {self.rollback_script}")
            self.log(f"Verification Script: {self.verification_script}")
            self.log(f"Log File: {self.log_file}")
            self.log("\\nNext steps:")
            self.log("1. Verify Phase C integration is complete")
            self.log("2. Run verification: python verify-phase-c.py")
            self.log(
                f"3. If issues occur, rollback: python rollback-phase-c.py --backup-dir {self.backup_dir}"
            )
            self.log("4. Check deployment report for details")

            return verification_passed

        except Exception as e:
            self.log(f"Deployment failed with error: {e}", "ERROR")
            self.deployment_report["status"] = "failed"
            self.deployment_report["errors"].append(str(e))
            return False


def main():
    """Main entry point."""
    # Parse command line arguments
    import argparse

    parser = argparse.ArgumentParser(description="ANINEO Phase C Deployment")
    parser.add_argument("--project-root", default=".", help="Project root directory")
    parser.add_argument(
        "--dry-run", action="store_true", help="Dry run without actual changes"
    )
    parser.add_argument("--skip-backup", action="store_true", help="Skip backup step")
    args = parser.parse_args()

    # Initialize deployment manager
    deployment = PhaseCDeployment(args.project_root)

    if args.dry_run:
        print("🚀 DRY RUN: ANINEO Phase C Deployment")
        print("======================================")
        print("This is a dry run. No files will be modified.")
        print("\\nTarget files:")
        for file in deployment.target_files:
            print(f"  - {file}")
        print("\\nPhase C markers to check:")
        for marker in deployment.phase_c_markers:
            print(f"  - {marker}")
        print("\\nP2 categories to verify:")
        for category in deployment.p2_categories:
            print(f"  - {category}")
        return 0

    # Run deployment
    success = deployment.deploy()

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
