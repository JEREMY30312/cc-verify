# 流程控制钩子

> **【详细规范文档】**
>
> 本文件作为 AGENTS.md 的扩展说明，详细说明流程控制钩子机制。
> 请参考 AGENTS.md 了解整体架构和流程。

 ---

## 概述

流程控制钩子是 ANINEO 制片人的核心机制，用于确保每个阶段完整执行6个强制检查点。任何违规操作都会被阻断并生成报告。

## 执行时机

- 每个阶段生成完成后
- 尝试进入下一阶段前
- 任何流程跳转操作时

## 核心功能

### 1. 流程合规性检查

```python
def check_phase_completion(task_type, episode):
    """
    检查当前阶段是否完成所有强制步骤
    
    Returns: (passed: bool, report: dict)
    """
    checks = [
        {
            "check": "main_output_exists",
            "description": "主产物文件存在",
            "file": f"outputs/{get_output_filename(task_type, episode)}",
            "required": True
        },
        {
            "check": "self_check_exists",
            "description": "自查报告已生成",
            "file": f"outputs/{get_output_filename(task_type, episode)}-self-check.md",
            "required": True
        },
        {
            "check": "self_check_passed",
            "description": "自查报告通过验证",
            "task": task_type,
            "episode": episode,
            "required": True
        },
        {
            "check": "director_review_completed",
            "description": "Director审核已完成",
            "task": task_type,
            "episode": episode,
            "required": True
        },
        {
            "check": "director_review_passed",
            "description": "Director审核通过",
            "task": task_type,
            "episode": episode,
            "required": True
        },
        {
            "check": "user_confirmed",
            "description": "用户已战略确认",
            "task": task_type,
            "episode": episode,
            "required": True
        },
        {
            "check": "snapshot_created",
            "description": "快照已创建",
            "task": task_type,
            "episode": episode,
            "required": True
        },
        {
            "check": "phase_status_updated",
            "description": "阶段状态已更新",
            "task": task_type,
            "episode": episode,
            "required": True
        }
    ]
    
    results = []
    for check in checks:
        result = execute_check(check)
        results.append(result)
    
    # 生成检查报告
    report = {
        "task_type": task_type,
        "episode": episode,
        "timestamp": get_timestamp(),
        "checks": results,
        "passed": all(r["passed"] for r in results),
        "failed_checks": [r for r in results if not r["passed"]],
        "warnings": [r for r in results if r["passed"] and "warning" in r]
    }
    
    return report
```

### 2. 阶段完成检查

```python
def is_phase_complete(task_type, episode) -> bool:
    """
    检查阶段是否完成所有强制步骤
    
    Args:
        task_type: 任务类型 (breakdown/beatboard/sequence/motion)
        episode: 集数 (ep01)
    
    Returns:
        True: 阶段完成，可以进入下一阶段
        False: 阶段未完成，流程阻断
    """
    state = read_agent_state()
    phase_key = get_phase_key(task_type)
    
    if phase_key not in state["phases"]:
        return False
    
    phase = state["phases"][phase_key]
    
    # 检查必要字段
    required_fields = [
        "status",
        "output_file",
        "completed_at",
        "self_check_passed",
        "director_review_passed",
        "user_confirmed",
        "snapshot_id"
    ]
    
    for field in required_fields:
        if field not in phase:
            return False
    
    if phase["status"] != "completed":
        return False
    
    if not phase["self_check_passed"]:
        return False
    
    if not phase["director_review_passed"]:
        return False
    
    if not phase["user_confirmed"]:
        return False
    
    if not phase.get("snapshot_id"):
        return False
    
    return True
```

### 3. 流程阻断机制

```python
def block_until_compliance(task_type, episode) -> dict:
    """
    阻断流程直到所有检查通过
    
    Returns:
        compliance_report: 合规报告，包含未完成的步骤和修复建议
    """
    report = check_phase_completion(task_type, episode)
    
    if report["passed"]:
        return {
            "blocked": False,
            "message": "所有检查通过，可以进入下一阶段"
        }
    
    # 生成阻断报告
    blocked_report = {
        "blocked": True,
        "reason": "流程检查未通过",
        "failed_checks": [],
        "fix_recommendations": []
    }
    
    for check in report["failed_checks"]:
        failed_item = {
            "check": check["check"],
            "description": check["description"],
            "error": check.get("error", "未知错误")
        }
        blocked_report["failed_checks"].append(failed_item)
        
        # 生成修复建议
        recommendation = get_fix_recommendation(check)
        blocked_report["fix_recommendations"].append(recommendation)
    
    return blocked_report
```

### 4. 修复建议生成

```python
def get_fix_recommendation(check: dict) -> dict:
    """
    根据检查失败类型生成修复建议
    
    Args:
        check: 检查项字典
    
    Returns:
        recommendation: 修复建议
    """
    fix_actions = {
        "main_output_exists": {
            "action": "生成主产物文件",
            "command": f"执行 /{check['task_type']} {check['episode']}",
            "priority": "高"
        },
        "self_check_exists": {
            "action": "生成自查报告",
            "command": "制片人生成自查报告",
            "priority": "高"
        },
        "self_check_passed": {
            "action": "修复自查报告问题",
            "command": "检查主文件数据，修正自查报告",
            "priority": "高"
        },
        "director_review_completed": {
            "action": "执行Director审核",
            "command": f"执行 /review {check['task_type']} {check['episode']}",
            "priority": "高"
        },
        "director_review_passed": {
            "action": "修复审核问题",
            "command": "根据审核报告修改产出，重新提交审核",
            "priority": "高"
        },
        "user_confirmed": {
            "action": "等待用户确认",
            "command": "向用户展示产出，等待CP确认",
            "priority": "中"
        },
        "snapshot_created": {
            "action": "创建快照",
            "command": f"执行 /snapshot create '{check['task_type']}完成'",
            "priority": "高"
        },
        "phase_status_updated": {
            "action": "更新阶段状态",
            "command": "更新 .agent-state.json 中的 phase 状态",
            "priority": "中"
        }
    }
    
    check_type = check["check"]
    if check_type in fix_actions:
        return fix_actions[check_type]
    else:
        return {
            "action": "人工检查",
            "command": "请检查具体错误原因",
            "priority": "高"
        }
```

## 使用方式

### 在制片人流程中使用

```python
# 每个阶段完成后执行流程检查
def execute_phase(task_type, episode):
    # ... 执行生成 ...
    
    # 执行流程控制检查
    compliance = block_until_compliance(task_type, episode)
    
    if compliance["blocked"]:
        # 流程阻断，生成报告
        raise FlowBlockedError(compliance)
    
    # 继续下一阶段
    proceed_to_next_phase(task_type, episode)
```

### 检查点验证

```python
# 检查是否可以进入下一阶段
if is_phase_complete("beatboard", "ep01"):
    proceed_to_next_phase("sequence", "ep01")
else:
    report = check_phase_completion("beatboard", "ep01")
    display_blockage_report(report)
```

## 检查清单

| 检查项 | 说明 | 阻塞条件 |
|--------|------|----------|
| 主产物文件存在 | outputs/xxx.md 文件存在 | 文件不存在则阻断 |
| 自查报告存在 | outputs/xxx-self-check.md 文件存在 | 文件不存在则阻断 |
| 自查报告通过 | 数据验证通过，无严重错误 | 验证失败则阻断 |
| Director审核完成 | review 文件已生成 | 未审核则阻断 |
| Director审核通过 | 审核状态为 PASS | 审核失败则阻断 |
| 用户已确认 | 用户执行了 CP 确认 | 未确认则阻断 |
| 快照已创建 | snapshot_id 已记录 | 未创建则阻断 |
| 阶段状态已更新 | .agent-state.json 已更新 | 未更新则阻断 |

## 错误处理

### FlowBlockedError

当流程被阻断时，抛出 FlowBlockedError：

```python
class FlowBlockedError(Exception):
    def __init__(self, compliance_report):
        self.report = compliance_report
        super().__init__(f"流程阻断: {len(compliance_report['failed_checks'])} 项检查未通过")
```

### 阻断报告格式

```json
{
  "blocked": true,
  "reason": "流程检查未通过",
  "failed_checks": [
    {
      "check": "director_review_completed",
      "description": "Director审核已完成",
      "error": "审核文件不存在"
    },
    {
      "check": "snapshot_created",
      "description": "快照已创建",
      "error": "snapshot_id 未记录"
    }
  ],
  "fix_recommendations": [
    {
      "action": "执行Director审核",
      "command": "执行 /review beatboard ep01",
      "priority": "高"
    },
    {
      "action": "创建快照",
      "command": "执行 /snapshot create '九宫格完成'",
      "priority": "高"
    }
  ]
}
```

## 相关文件

| 文件 | 说明 |
|------|------|
| `AGENTS.md` | 主配置文件，定义强制检查点 |
| `common/self-check-validator.md` | 数据验证器 |
| `common/data-validator.md` | 数据验证工具集 |
| `agents/producer-self-check.md` | 制片人自查生成器 |
