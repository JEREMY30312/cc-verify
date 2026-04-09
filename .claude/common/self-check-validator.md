# 数据验证器

> **【详细规范文档】**
>
> 本文件作为 AGENTS.md 的扩展说明，详细说明自查数据验证机制。
> 请参考 AGENTS.md 了解整体架构和流程。

 ---

## 概述

数据验证器是 ANINEO 自查报告的核心验证机制，确保所有自查数据从主文件读取验证，而非依赖子Agent的估算。

## 核心原则

### 1. 数据源验证

所有自查报告数据必须从主文件读取验证，不能依赖子Agent估算。

| 数据项 | 验证方法 |
|--------|----------|
| 节拍数 | grep 统计 `|` 开头的行数 |
| 通过率 | grep 统计 `✅` 和 `⚠️` 数量 |
| 文件调用 | 读取 .agent-state.json 验证 |
| 关键帧分布 | 读取主文件统计 🔴🟠🟡 数量 |
| 文件大小 | os.path.getsize() |

### 2. 数据一致性检查

```python
class SelfCheckValidator:
    """自查数据验证器"""
    
    def __init__(self, report_path, source_path):
        self.report_path = report_path
        self.source_path = source_path
        self.report_data = {}
        self.source_data = {}
        self.discrepancies = []
    
    def validate(self) -> dict:
        """
        执行完整验证
        
        Returns:
            validation_report: 验证报告
        """
        # 读取数据
        self._read_report_data()
        self._read_source_data()
        
        # 执行各项验证
        validations = [
            self._validate_beat_count,
            self._validate_pass_rate,
            self._validate_file_existence,
            self._validate_keyframe_distribution,
            self._validate_file_size
        ]
        
        for validate in validations:
            validate()
        
        # 生成报告
        return self._generate_report()
    
    def _read_report_data(self):
        """读取自查报告数据"""
        # 从自查报告读取子Agent估算值
        pass
    
    def _read_source_data(self):
        """从主文件读取实际数据"""
        # 从主产物文件读取实际值
        pass
```

## 验证函数

### 1. 节拍拆解验证

```python
def validate_beat_breakdown(report_path, source_path) -> dict:
    """
    验证节拍拆解自查报告
    
    检查项：
    - 节拍数量
    - 三幕比例
    - 关键帧分布
    - 风格转换节点
    """
    checks = [
        {
            "name": "beat_count",
            "description": "节拍数量验证",
            "validate": lambda: _check_beat_count(report_path, source_path)
        },
        {
            "name": "three_act_ratio",
            "description": "三幕比例验证",
            "validate": lambda: _check_three_act_ratio(report_path, source_path)
        },
        {
            "name": "keyframe_distribution",
            "description": "关键帧分布验证",
            "validate": lambda: _check_keyframe_distribution(report_path, source_path)
        },
        {
            "name": "style_transitions",
            "description": "风格转换节点验证",
            "validate": lambda: _check_style_transitions(report_path, source_path)
        }
    ]
    
    return run_validations(checks)
```

### 2. 九宫格验证

```python
def validate_beatboard(report_path, source_path) -> dict:
    """
    验证九宫格自查报告
    
    检查项：
    - 关键帧数量
    - 淘汰节拍数量
    - 关键帧等级分布
    - 提示词规范性
    """
    checks = [
        {
            "name": "keyframe_count",
            "description": "关键帧数量验证",
            "validate": lambda: _check_keyframe_count(report_path, source_path)
        },
        {
            "name": "elimination_count",
            "description": "淘汰节拍数量验证",
            "validate": lambda: _check_elimination_count(report_path, source_path)
        },
        {
            "name": "keyframe_levels",
            "description": "关键帧等级分布验证",
            "validate": lambda: _check_keyframe_levels(report_path, source_path)
        },
        {
            "name": "prompt_format",
            "description": "提示词格式验证",
            "validate": lambda: _check_prompt_format(report_path, source_path)
        }
    ]
    
    return run_validations(checks)
```

### 3. 四宫格验证

```python
def validate_sequence(report_path, source_path) -> dict:
    """
    验证四宫格自查报告
    
    检查项：
    - 序列数量
    - 总画面数
    - 风格分布
    - 连贯性检查
    """
    checks = [
        {
            "name": "sequence_count",
            "description": "序列数量验证",
            "validate": lambda: _check_sequence_count(report_path, source_path)
        },
        {
            "name": "total_frames",
            "description": "总画面数验证",
            "validate": lambda: _check_total_frames(report_path, source_path)
        },
        {
            "name": "style_distribution",
            "description": "风格分布验证",
            "validate": lambda: _check_style_distribution(report_path, source_path)
        },
        {
            "name": "coherence",
            "description": "连贯性验证",
            "validate": lambda: _check_coherence(report_path, source_path)
        }
    ]
    
    return run_validations(checks)
```

### 4. 动态提示词验证

```python
def validate_motion_prompt(report_path, source_path) -> dict:
    """
    验证动态提示词自查报告
    
    检查项：
    - Motion Prompt数量
    - 物理通过率
    - 五模块覆盖率
    """
    checks = [
        {
            "name": "motion_count",
            "description": "Motion Prompt数量验证",
            "validate": lambda: _check_motion_count(report_path, source_path)
        },
        {
            "name": "pass_rate",
            "description": "物理通过率验证",
            "validate": lambda: _check_pass_rate(report_path, source_path)
        },
        {
            "name": "five_modules",
            "description": "五模块覆盖率验证",
            "validate": lambda: _check_five_modules(report_path, source_path)
        }
    ]
    
    return run_validations(checks)
```

## 具体验证实现

### 节拍数量验证

```python
def _check_beat_count(report_path, source_path) -> dict:
    """
    验证节拍数量
    
    从主文件统计实际节拍数量，与自查报告对比
    """
    # 从主文件读取实际节拍数
    with open(source_path, 'r') as f:
        content = f.read()
    
    # 节拍以 | 开头且包含场景描述的行
    actual_count = len(re.findall(r'^\|\s*\d+\s*\|', content, re.MULTILINE))
    
    # 从自查报告读取估算值
    report_data = extract_report_value(report_path, "节拍数")
    estimated_count = int(report_data)
    
    # 比较
    diff = actual_count - estimated_count
    
    if abs(diff) == 0:
        return {
            "passed": True,
            "message": f"节拍数量一致: {actual_count}",
            "estimated": estimated_count,
            "actual": actual_count
        }
    elif abs(diff) <= 2:
        return {
            "passed": True,
            "warning": True,
            "message": f"节拍数量轻微差异: 估算{estimated_count}, 实际{actual_count}",
            "estimated": estimated_count,
            "actual": actual_count,
            "difference": diff
        }
    else:
        return {
            "passed": False,
            "error": f"节拍数量差异过大: 估算{estimated_count}, 实际{actual_count}",
            "estimated": estimated_count,
            "actual": actual_count,
            "difference": diff
        }
```

### 物理通过率验证

```python
def _check_pass_rate(report_path, source_path) -> dict:
    """
    验证物理通过率
    
    从主文件统计 ✅ 和 ⚠️ 数量，计算实际通过率
    """
    # 从主文件读取实际通过率
    with open(source_path, 'r') as f:
        content = f.read()
    
    actual_passed = len(re.findall(r'✅', content))
    actual_warning = len(re.findall(r'⚠️', content))
    actual_total = actual_passed + actual_warning
    actual_rate = actual_passed / actual_total if actual_total > 0 else 0
    
    # 从自查报告读取估算值
    report_rate_str = extract_report_value(report_path, "物理检查通过率")
    # 解析 "92%" 或 "92 percent" 格式
    estimated_rate = parse_percentage(report_rate_str)
    estimated_passed = int(estimated_rate * actual_total / 100)
    
    # 比较
    rate_diff = abs(actual_rate * 100 - estimated_rate)
    
    if rate_diff < 5:
        return {
            "passed": True,
            "message": f"通过率一致: {actual_rate*100:.1f}%",
            "estimated": f"{estimated_rate}%",
            "actual": f"{actual_rate*100:.1f}%"
        }
    elif rate_diff < 20:
        return {
            "passed": True,
            "warning": True,
            "message": f"通过率轻微差异: 估算{estimated_rate}%, 实际{actual_rate*100:.1f}%",
            "estimated": f"{estimated_rate}%",
            "actual": f"{actual_rate*100:.1f}%"
        }
    else:
        return {
            "passed": False,
            "error": f"通过率差异过大: 估算{estimated_rate}%, 实际{actual_rate*100:.1f}%",
            "estimated": f"{estimated_rate}%",
            "actual": f"{actual_rate*100:.1f}%"
        }
```

### 文件存在性验证

```python
def _check_file_existence(report_path, source_path) -> dict:
    """
    验证报告中提到的所有文件是否存在
    """
    # 从自查报告提取文件路径
    reported_files = extract_file_paths(report_path)
    
    missing_files = []
    for file_path in reported_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if not missing_files:
        return {
            "passed": True,
            "message": f"所有 {len(reported_files)} 个文件存在"
        }
    else:
        return {
            "passed": False,
            "error": f"缺少 {len(missing_files)} 个文件",
            "missing_files": missing_files
        }
```

## 验证结果处理

### 结果等级

| 等级 | 条件 | 处理方式 |
|------|------|----------|
| ✅ 通过 | 差异 = 0 | 无需处理 |
| ⚠️ 警告 | 0 < 差异 < 阈值 | 记录警告，继续流程 |
| ❌ 失败 | 差异 ≥ 阈值 | 阻断流程，需修复 |

### 阈值配置

```python
THRESHOLDS = {
    "count_difference": 2,          # 数量差异阈值
    "percentage_difference": 5,     # 百分比差异阈值（%）
    "file_size_difference": 0.1     # 文件大小差异比例
}
```

### 验证报告生成

```python
def generate_validation_report(validations: list) -> dict:
    """
    生成验证报告
    
    Args:
        validations: 验证结果列表
    
    Returns:
        report: 验证报告
    """
    passed = [v for v in validations if v["passed"]]
    warnings = [v for v in validations if v.get("warning")]
    failed = [v for v in validations if not v["passed"]]
    
    report = {
        "total_checks": len(validations),
        "passed": len(passed),
        "warnings": len(warnings),
        "failed": len(failed),
        "pass_rate": len(passed) / len(validations) * 100,
        "results": validations,
        "overall_status": "PASS" if not failed else ("WARN" if warnings else "FAIL")
    }
    
    return report
```

## 使用方式

### 制片人自查流程

```python
def generate_self_check(task_type, episode):
    """
    制片人生成自查报告
    """
    # 读取主文件
    main_file = f"outputs/{get_output_filename(task_type, episode)}.md"
    
    # 提取子Agent元数据
    raw_metrics = get_agent_metrics(task_type, episode)
    
    # 执行数据验证
    validator = SelfCheckValidator(
        report_path=None,  # 自查报告还未生成
        source_path=main_file
    )
    
    # 读取主文件实际数据
    actual_data = validator.read_source_data()
    
    # 对比并生成报告
    report = generate_self_check_report(task_type, episode, raw_metrics, actual_data)
    
    return report
```

### 验证报告示例

```markdown
# 节拍拆解自查报告

## 数据验证结果

| 检查项 | 估算值 | 实际值 | 状态 |
|--------|--------|--------|------|
| 节拍数 | 13 | 13 | ✅ |
| 通过率 | 92% | 60% | ⚠️ 警告 |
| 关键帧分布 | 🔴2🟠4 | 🔴2🟠4 | ✅ |

## 验证结论

- **总体状态**: ⚠️ 警告
- **通过率差异**: 32%（估算92%，实际60%）
- **建议**: 请人工确认物理检查通过率的准确性
```

## 相关文件

| 文件 | 说明 |
|------|------|
| `common/flow-control-hook.md` | 流程控制钩子 |
| `common/data-validator.md` | 数据验证工具集 |
| `agents/producer-self-check.md` | 制片人自查生成器 |
