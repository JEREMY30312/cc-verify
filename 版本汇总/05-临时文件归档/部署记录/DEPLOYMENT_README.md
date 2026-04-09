# ANINEO Phase C Deployment

## Overview

This deployment script (`deploy_phase_c.py`) handles the deployment of Phase C modifications to the ANINEO production environment. Phase C includes:

1. **Prompt Simplifier Algorithm** - Intelligent prompt reduction while preserving creative elements
2. **Extended P2 Keywords** - Expanded keyword coverage for different scene types
3. **SKILL Integration** - Integration of the simplifier into the film-storyboard-skill workflow

## Files Updated

The deployment updates/verifies the following files:

1. `.claude/common/prompt-simplifier.md` - Prompt simplifier algorithm module
2. `.claude/skills/film-storyboard-skill/SKILL.md` - Main skill file with Phase C integration

## Requirements

- Python 3.6 or higher
- Standard library modules only (no external dependencies)

## Usage

### 1. Dry Run (Safe Testing)

```bash
python3 deploy_phase_c.py --dry-run
```

This shows what the script would do without making any changes.

### 2. Full Deployment

```bash
python3 deploy_phase_c.py
```

This performs the complete deployment:
- Creates backup of existing files
- Verifies target files exist
- Checks current integration status
- Creates rollback capability
- Runs verification tests
- Generates deployment report

### 3. With Custom Project Root

```bash
python3 deploy_phase_c.py --project-root /path/to/anineo
```

### 4. Skip Backup (Not Recommended)

```bash
python3 deploy_phase_c.py --skip-backup
```

## Deployment Process

The script follows this workflow:

1. **Backup**: Creates timestamped backup in `.backups/phase-c-{timestamp}/`
2. **Verification**: Checks that all target files exist
3. **Integration Check**: Verifies Phase C markers in SKILL.md
4. **P2 Keyword Check**: Verifies extended P2 keywords in prompt-simplifier.md
5. **Rollback Creation**: Creates `rollback-phase-c.py` script
6. **Verification Creation**: Creates `verify-phase-c.py` script
7. **Verification Run**: Runs verification tests
8. **Report Generation**: Creates deployment report JSON file

## Rollback

If deployment causes issues, use the rollback script:

```bash
python3 rollback-phase-c.py --backup-dir .backups/phase-c-{timestamp}
```

For dry run (see what would be restored):
```bash
python3 rollback-phase-c.py --backup-dir .backups/phase-c-{timestamp} --dry-run
```

## Verification

To verify deployment success at any time:

```bash
python3 verify-phase-c.py
```

This checks:
1. P2 keywords in prompt-simplifier.md
2. Scene type categories (5 required categories)
3. Phase C integration markers in SKILL.md

## Output Files

The deployment creates several files:

1. **Backup Directory**: `.backups/phase-c-{timestamp}/` - Contains original file backups
2. **Log File**: `deploy-phase-c.log` - Detailed deployment log
3. **Rollback Script**: `rollback-phase-c.py` - Python script for rollback
4. **Verification Script**: `verify-phase-c.py` - Python script for verification
5. **Deployment Report**: `deployment-report-phase-c-{timestamp}.json` - JSON report

## Quality Checks

The deployment verifies:

### Phase C Integration Markers
- `阶段C新增` - Phase C integration markers
- `提示词精简算法` - Prompt simplifier algorithm references
- `efficient_simplifier_v2` - Algorithm implementation references

### P2 Keyword Categories
- `动作场景` - Action scenes
- `情感场景` - Emotional scenes  
- `建立场景` - Establishing shots
- `悬疑场景` - Suspense scenes
- `对话场景` - Dialogue scenes

## Error Handling

The script includes comprehensive error handling:

1. **Missing Files**: Aborts if target files don't exist
2. **Backup Failures**: Logs errors and continues if possible
3. **Verification Failures**: Continues but marks as partial success
4. **Rollback Creation**: Creates rollback script even if verification fails

## Safety Features

1. **Dry Run Mode**: Test without making changes
2. **Backup First**: Always creates backups before any modifications
3. **Rollback Ready**: Creates rollback script before making changes
4. **Verification**: Runs verification tests after deployment
5. **Logging**: Detailed log of all operations

## Integration with Existing System

The deployment script is designed to work with the existing ANINEO system:

1. **Compatible with existing bash scripts**: Can be used alongside `deploy-phase-c.sh`
2. **Preserves existing backups**: Uses `.backups/` directory structure
3. **Follows ANINEO conventions**: Uses same file paths and naming conventions

## Troubleshooting

### Common Issues

1. **Permission Errors**: Ensure you have write permissions to project files
2. **Missing Python**: Install Python 3.6+ if not available
3. **File Not Found**: Check that target files exist in expected locations
4. **Verification Failures**: Check that Phase C integration is complete

### Debug Mode

For detailed debugging, you can modify the script to increase logging:

```python
# In deploy_phase_c.py, change log level
self.log(message, level="DEBUG")  # Instead of "INFO"
```

## Support

For issues with the deployment script, check:
1. Deployment log: `deploy-phase-c.log`
2. Deployment report: `deployment-report-phase-c-{timestamp}.json`
3. Python error output

The script is designed to be self-documenting and provide clear error messages.