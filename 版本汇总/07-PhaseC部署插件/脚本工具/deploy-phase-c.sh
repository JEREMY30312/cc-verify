#!/bin/bash
# ANINEO Phase C Deployment Script
# Deploys prompt simplifier updates to production environment

set -e  # Exit on error

echo "🚀 ANINEO Phase C Deployment Started"
echo "======================================"

# Configuration
BACKUP_DIR=".backups/phase-c-$(date +%Y%m%d-%H%M%S)"
LOG_FILE="deploy-phase-c.log"
TARGET_FILES=(
    ".claude/common/prompt-simplifier.md"
    ".claude/skills/film-storyboard-skill/SKILL.md"
)

# Create backup directory
echo "📦 Creating backup directory: $BACKUP_DIR"
mkdir -p "$BACKUP_DIR"

# Function to backup file
backup_file() {
    local file="$1"
    if [ -f "$file" ]; then
        cp "$file" "$BACKUP_DIR/"
        echo "  ✅ Backed up: $file"
    else
        echo "  ⚠️  File not found: $file"
    fi
}

# Function to verify file exists
verify_file() {
    local file="$1"
    if [ -f "$file" ]; then
        echo "  ✅ Verified: $file"
        return 0
    else
        echo "  ❌ Missing: $file"
        return 1
    fi
}

# Function to check integration
check_integration() {
    echo "🔍 Checking SKILL.md integration..."
    if grep -q "阶段C新增" ".claude/skills/film-storyboard-skill/SKILL.md"; then
        echo "  ✅ Phase C integration found in SKILL.md"
        return 0
    else
        echo "  ⚠️  Phase C integration not found in SKILL.md"
        return 1
    fi
}

# Function to verify P2 keywords
verify_p2_keywords() {
    echo "🔍 Verifying P2 keywords in prompt-simplifier.md..."
    local keyword_count=$(grep -c "^\s*- " ".claude/common/prompt-simplifier.md" | head -1)
    echo "  Found $keyword_count keyword lines"
    
    # Check for scene type categories
    local scene_types=0
    if grep -q "动作场景" ".claude/common/prompt-simplifier.md"; then scene_types=$((scene_types+1)); fi
    if grep -q "情感场景" ".claude/common/prompt-simplifier.md"; then scene_types=$((scene_types+1)); fi
    if grep -q "建立场景" ".claude/common/prompt-simplifier.md"; then scene_types=$((scene_types+1)); fi
    if grep -q "悬疑场景" ".claude/common/prompt-simplifier.md"; then scene_types=$((scene_types+1)); fi
    if grep -q "对话场景" ".claude/common/prompt-simplifier.md"; then scene_types=$((scene_types+1)); fi
    
    echo "  Found $scene_types/5 scene type categories"
    
    if [ $scene_types -ge 5 ]; then
        echo "  ✅ All 5 scene type categories present"
        return 0
    else
        echo "  ⚠️  Missing scene type categories"
        return 1
    fi
}

# Main deployment process
main() {
    echo "📋 Starting deployment process..."
    
    # Step 1: Backup existing files
    echo ""
    echo "1. 📦 Backing up existing files..."
    for file in "${TARGET_FILES[@]}"; do
        backup_file "$file"
    done
    
    # Step 2: Verify files exist
    echo ""
    echo "2. 🔍 Verifying target files..."
    all_files_ok=true
    for file in "${TARGET_FILES[@]}"; do
        if ! verify_file "$file"; then
            all_files_ok=false
        fi
    done
    
    if [ "$all_files_ok" = false ]; then
        echo "❌ Some target files are missing. Aborting deployment."
        exit 1
    fi
    
    # Step 3: Check current integration status
    echo ""
    echo "3. 🔍 Checking current integration status..."
    check_integration
    
    # Step 4: Verify P2 keywords (pre-update)
    echo ""
    echo "4. 🔍 Checking current P2 keywords..."
    verify_p2_keywords
    
    # Step 5: Apply updates
    echo ""
    echo "5. 🔄 Applying Phase C updates..."
    echo "   Note: The actual file updates should be done manually"
    echo "   or via the update script. This script only handles"
    echo "   backup, verification, and rollback."
    
    # Step 6: Post-update verification
    echo ""
    echo "6. ✅ Running post-update verification..."
    echo "   Running verification script..."
    if [ -f "verify-phase-c.sh" ]; then
        bash verify-phase-c.sh
    else
        echo "   ⚠️  Verification script not found. Creating it..."
        # Create verification script if missing
        cat > verify-phase-c.sh << 'EOF'
#!/bin/bash
# ANINEO Phase C Verification Script

echo "🔍 Phase C Verification Started"
echo "================================"

# Check P2 keywords
echo "1. Checking P2 keywords..."
p2_section_lines=$(grep -A 20 "#### P2元素" .claude/common/prompt-simplifier.md | grep -c "^\s*- ")
echo "   P2 keyword lines: $p2_section_lines"

# Check scene types
echo "2. Checking scene type categories..."
scene_categories=0
for category in "动作场景" "情感场景" "建立场景" "悬疑场景" "对话场景"; do
    if grep -q "$category" .claude/common/prompt-simplifier.md; then
        echo "   ✅ Found: $category"
        scene_categories=$((scene_categories+1))
    else
        echo "   ❌ Missing: $category"
    fi
done

echo "   Total scene categories: $scene_categories/5"

# Check SKILL integration
echo "3. Checking SKILL.md integration..."
if grep -q "阶段C新增" .claude/skills/film-storyboard-skill/SKILL.md; then
    integration_count=$(grep -c "阶段C新增" .claude/skills/film-storyboard-skill/SKILL.md)
    echo "   ✅ Phase C integration points: $integration_count"
else
    echo "   ❌ No Phase C integration found"
fi

# Summary
echo ""
echo "📊 Verification Summary:"
echo "========================"
echo "P2 Keywords: $p2_section_lines lines"
echo "Scene Categories: $scene_categories/5"
echo "SKILL Integration: $(if [ $integration_count -gt 0 ]; then echo "✅ Present"; else echo "❌ Missing"; fi)"

if [ $scene_categories -eq 5 ] && [ $integration_count -gt 0 ]; then
    echo ""
    echo "🎉 Phase C deployment verified successfully!"
    exit 0
else
    echo ""
    echo "⚠️  Verification issues found. Please check the deployment."
    exit 1
fi
EOF
        chmod +x verify-phase-c.sh
        echo "   ✅ Created verification script"
    fi
    
    # Step 7: Create rollback script
    echo ""
    echo "7. 🔄 Creating rollback script..."
    cat > rollback-phase-c.sh << EOF
#!/bin/bash
# ANINEO Phase C Rollback Script

echo "⏪ Phase C Rollback Started"
echo "============================"

BACKUP_DIR="$BACKUP_DIR"

if [ ! -d "\$BACKUP_DIR" ]; then
    echo "❌ Backup directory not found: \$BACKUP_DIR"
    echo "   Available backups:"
    ls -la .backups/ 2>/dev/null || echo "   No backups found"
    exit 1
fi

echo "📦 Restoring files from backup: \$BACKUP_DIR"

# Restore each file
for file in "${TARGET_FILES[@]}"; do
    backup_file="\$BACKUP_DIR/\$(basename "\$file")"
    if [ -f "\$backup_file" ]; then
        cp "\$backup_file" "\$file"
        echo "  ✅ Restored: \$file"
    else
        echo "  ⚠️  Backup not found: \$backup_file"
    fi
done

echo ""
echo "✅ Rollback completed!"
echo ""
echo "To verify rollback:"
echo "1. Run: bash verify-phase-c.sh"
echo "2. Check that files are restored to pre-deployment state"
EOF
    chmod +x rollback-phase-c.sh
    echo "   ✅ Created rollback script"
    
    echo ""
    echo "======================================"
    echo "🚀 Deployment preparation completed!"
    echo ""
    echo "Next steps:"
    echo "1. Update .claude/common/prompt-simplifier.md with extended P2 keywords"
    echo "2. Verify SKILL.md integration is complete"
    echo "3. Run verification: bash verify-phase-c.sh"
    echo "4. If issues occur, rollback: bash rollback-phase-c.sh"
    echo ""
    echo "Backup location: $BACKUP_DIR"
}

# Run main function
main 2>&1 | tee "$LOG_FILE"

echo ""
echo "📋 Deployment log saved to: $LOG_FILE"
echo "✅ Deployment script created successfully!"