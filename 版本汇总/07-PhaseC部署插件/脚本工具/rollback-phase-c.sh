#!/bin/bash
# ANINEO Phase C Rollback Script

echo "⏪ Phase C Rollback Started"
echo "============================"

BACKUP_DIR=".backups/phase-c-20260130-215755"

if [ ! -d "$BACKUP_DIR" ]; then
    echo "❌ Backup directory not found: $BACKUP_DIR"
    echo "   Available backups:"
    ls -la .backups/ 2>/dev/null || echo "   No backups found"
    exit 1
fi

echo "📦 Restoring files from backup: $BACKUP_DIR"

# Restore each file
for file in ".claude/common/prompt-simplifier.md .claude/skills/film-storyboard-skill/SKILL.md"; do
    backup_file="$BACKUP_DIR/$(basename "$file")"
    if [ -f "$backup_file" ]; then
        cp "$backup_file" "$file"
        echo "  ✅ Restored: $file"
    else
        echo "  ⚠️  Backup not found: $backup_file"
    fi
done

echo ""
echo "✅ Rollback completed!"
echo ""
echo "To verify rollback:"
echo "1. Run: bash verify-phase-c.sh"
echo "2. Check that files are restored to pre-deployment state"
