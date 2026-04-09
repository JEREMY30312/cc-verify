# 制片人自查报告生成器

## 概述

制片人自查报告生成器是 ANINEO 质量控制的核心组件，负责在每个阶段生成后从主文件读取实际数据并与子Agent估算值对比，确保数据准确性。

## 执行时机

- 子Agent完成生成后
- Director审核前
- 每个阶段的必要步骤

## 核心职责

### 1. 读取主文件验证数据

```python
class ProducerSelfCheck:
    """制片人自查生成器"""
    
    def __init__(self, task_type, episode):
        self.task_type = task_type
        self.episode = episode
        self.main_file = f"outputs/{get_output_filename(task_type, episode)}.md"
        self.agent_metadata = None
        self.actual_data = {}
        self.discrepancies = []
    
    def execute(self) -> dict:
        """
        执行自查流程
        
        Returns:
            self_check_report: 自查报告
        """
        # 1. 获取子Agent元数据
        self._fetch_agent_metadata()
        
        # 2. 读取主文件实际数据
        self._read_actual_data()
        
        # 3. 对比估算值与实际值
        self._compare_data()
        
        # 4. 生成自查报告
        report = self._generate_report()
        
        # 5. 保存报告
        self._save_report(report)
        
        return report
```

## 各阶段自查生成

### 1. 节拍拆解自查

```python
def generate_beat_breakdown_self_check(episode) -> dict:
    """
    生成节拍拆解阶段自查报告
    """
    checker = ProducerSelfCheck("beat-breakdown", episode)
    
    # 获取子Agent估算
    checker.agent_metadata = {
        "beat_count": 13,
        "three_act_ratio": {"第一幕": "23%", "第二幕": "46%", "第三幕": "31%"},
        "keyframe_distribution": {"🔴": 2, "🟠": 4, "🟡": 3, "🔵": 4}
    }
    
    # 读取主文件实际数据
    with open(checker.main_file, 'r') as f:
        content = f.read()
    
    # 统计实际节拍数
    actual_beats = len(re.findall(r'^\|\s*\d+\s*\|', content, re.MULTILINE))
    
    # 统计关键帧分布
    actual_red = len(re.findall(r'🔴', content))
    actual_orange = len(re.findall(r'🟠', content))
    actual_yellow = len(re.findall(r'🟡', content))
    actual_blue = len(re.findall(r'🔵', content))
    
    checker.actual_data = {
        "beat_count": actual_beats,
        "keyframe_distribution": {
            "🔴": actual_red,
            "🟠": actual_orange,
            "🟡": actual_yellow,
            "🔵": actual_blue
        },
        "file_size": os.path.getsize(checker.main_file)
    }
    
    # 对比
    checker._compare_data()
    
    # 生成报告
    return checker._generate_report()
```

### 2. 九宫格自查

```python
def generate_beatboard_self_check(episode) -> dict:
    """
    生成九宫格阶段自查报告
    """
    checker = ProducerSelfCheck("beatboard", episode)
    
    # 获取子Agent估算
    checker.agent_metadata = {
        "keyframe_count": 9,
        "eliminated_count": 4,
        "keyframe_distribution": {"🔴": 2, "🟠": 4, "🟡": 3}
    }
    
    # 读取主文件实际数据
    with open(checker.main_file, 'r') as f:
        content = f.read()
    
    # 统计实际关键帧
    actual_keyframes = len(re.findall(r'^##\s*关键帧\s*\d+', content))
    actual_red = len(re.findall(r'🔴', content))
    actual_orange = len(re.findall(r'🟠', content))
    actual_yellow = len(re.findall(r'🟡', content))
    
    checker.actual_data = {
        "keyframe_count": actual_keyframes,
        "keyframe_distribution": {
            "🔴": actual_red,
            "🟠": actual_orange,
            "🟡": actual_yellow
        },
        "file_size": os.path.getsize(checker.main_file)
    }
    
    checker._compare_data()
    
    return checker._generate_report()
```

### 3. 四宫格自查

```python
def generate_sequence_self_check(episode) -> dict:
    """
    生成四宫格阶段自查报告
    """
    checker = ProducerSelfCheck("sequence", episode)
    
    # 获取子Agent估算
    checker.agent_metadata = {
        "sequence_count": 9,
        "total_frames": 36,
        "style_distribution": {"国漫": 4, "MCU": 5}
    }
    
    # 读取主文件实际数据
    with open(checker.main_file, 'r') as f:
        content = f.read()
    
    # 统计实际序列
    actual_sequences = len(re.findall(r'^##\s*序列\s*\d+', content))
    
    # 统计总画面
    actual_frames = len(re.findall(r'^###\s*\d+\.\d+\s*', content))
    
    checker.actual_data = {
        "sequence_count": actual_sequences,
        "total_frames": actual_frames,
        "file_size": os.path.getsize(checker.main_file)
    }
    
    checker._compare_data()
    
    return checker._generate_report()
```

### 4. 动态提示词自查

```python
def generate_motion_self_check(episode) -> dict:
    """
    生成动态提示词阶段自查报告
    """
    checker = ProducerSelfCheck("motion", episode)
    
    # 获取子Agent估算
    checker.agent_metadata = {
        "motion_count": 45,
        "pass_rate": "92%",
        "passed_count": 41,
        "warning_count": 4
    }
    
    # 读取主文件实际数据
    with open(checker.main_file, 'r') as f:
        content = f.read()
    
    # 统计实际数量
    actual_motions = len(re.findall(r'^##\s*序列\s*\d+', content))
    actual_passed = len(re.findall(r'✅', content))
    actual_warning = len(re.findall(r'⚠️', content))
    actual_total = actual_passed + actual_warning
    actual_rate = actual_passed / actual_total * 100 if actual_total > 0 else 0
    
    checker.actual_data = {
        "motion_count": actual_motions,
        "pass_rate": f"{actual_rate:.0f}%",
        "passed_count": actual_passed,
        "warning_count": actual_warning,
        "file_size": os.path.getsize(checker.main_file)
    }
    
    checker._compare_data()
    
    return checker._generate_report()
```

## 对比逻辑

```python
def _compare_data(self):
    """对比估算值与实际值"""
    self.discrepancies = []
    
    for key, estimated in self.agent_metadata.items():
        if key in self.actual_data:
            actual = self.actual_data[key]
            
            # 数值类型比较
            if isinstance(estimated, (int, float)):
                diff = actual - estimated
                if abs(diff) > 2:
                    self.discrepancies.append({
                        "key": key,
                        "type": "count_difference",
                        "estimated": estimated,
                        "actual": actual,
                        "difference": diff,
                        "severity": "error" if abs(diff) > 5 else "warning"
                    })
            
            # 百分比类型比较
            elif isinstance(estimated, str) and "%" in estimated:
                est_rate = float(estimated.replace("%", ""))
                actual_rate = float(actual.replace("%", ""))
                diff = abs(est_rate - actual_rate)
                if diff > 5:
                    self.discrepancies.append({
                        "key": key,
                        "type": "percentage_difference",
                        "estimated": estimated,
                        "actual": actual,
                        "difference": f"{diff:.1f}%",
                        "severity": "error" if diff > 20 else "warning"
                    })
            
            # 字典类型比较
            elif isinstance(estimated, dict):
                for sub_key, sub_est in estimated.items():
                    sub_act = actual.get(sub_key, 0)
                    if sub_est != sub_act:
                        self.discrepancies.append({
                            "key": f"{key}.{sub_key}",
                            "type": "count_difference",
                            "estimated": sub_est,
                            "actual": sub_act,
                            "difference": sub_act - sub_est,
                            "severity": "warning"
                        })
```

## 报告生成

```python
def _generate_report(self) -> dict:
    """生成自查报告"""
    passed_discrepancies = [d for d in self.discrepancies if d["severity"] != "error"]
    error_discrepancies = [d for d in self.discrepancies if d["severity"] == "error"]
    
    report = {
        "task_type": self.task_type,
        "episode": self.episode,
        "timestamp": get_timestamp(),
        "main_file": self.main_file,
        "estimated_vs_actual": {
            "agent_metadata": self.agent_metadata,
            "actual_data": self.actual_data
        },
        "discrepancies": self.discrepancies,
        "passed_count": len(passed_discrepancies),
        "error_count": len(error_discrepancies),
        "overall_status": "PASS" if not error_discrepancies else ("WARN" if passed_discrepancies else "FAIL"),
        "recommendations": self._generate_recommendations()
    }
    
    return report
```

## 自查报告模板

```markdown
# {阶段}自查报告

## 阶段：/{task_type} {episode}

**生成时间**：{timestamp}
**执行状态**：{✅ 完成 / ⚠️ 警告 / ❌ 失败}

---

## 关键声明

**数据验证方式**：本报告数据从主文件读取验证，非子Agent估算。

---

## 1. 输出文件验证

| 文件 | 状态 | 大小 | 路径 |
|------|------|------|------|
| xxx | ✅ 存在 | N bytes | path |

---

## 2. 实际数据统计

| 指标 | 子Agent估算 | 实际验证 | 差异 |
|------|-------------|----------|------|
| 节拍数 | 13 | 13 | 0 |
| 通过率 | 92% | 60% | ⚠️ 32% |

---

## 3. 数据验证结果

| 检查项 | 状态 | 说明 |
|--------|------|------|
| 数据一致性 | ⚠️ 警告 | 通过率差异32%，需人工确认 |
| 文件存在性 | ✅ 通过 | 所有文件存在 |
| 关键帧分布 | ✅ 通过 | 分布一致 |

---

## 4. 阶段总结

| 维度 | 评估 |
|------|------|
| 执行效率 | ⭐⭐⭐⭐⭐ |
| 数据准确性 | ⚠️ 需确认 |
| **是否可进入下一阶段** | ⚠️ 需确认 |

---

## 5. 修复建议

{修复建议列表}

---

*报告生成时间：{timestamp}*
*自查工具：ANINEO 制片人 Agent*
```

## 使用方式

### 在制片人流程中使用

```python
def execute_phase(task_type, episode):
    # ... 子Agent执行生成 ...
    
    # 制片人生成自查报告
    if task_type == "breakdown":
        report = generate_beat_breakdown_self_check(episode)
    elif task_type == "beatboard":
        report = generate_beatboard_self_check(episode)
    # ... 其他阶段 ...
    
    # 保存报告
    save_self_check_report(report)
    
    # 更新 .agent-state.json
    update_agent_state(task_type, episode, report)
    
    # 检查是否通过
    if report["overall_status"] == "FAIL":
        raise SelfCheckFailedError(report)
```

## 流程集成

### 完整流程

```
子Agent完成生成
    ↓
制片人调用自查生成器
    ↓
读取主文件验证数据
    ↓
对比估算值与实际值
    ↓
生成自查报告
    ↓
保存报告
    ↓
更新 .agent-state.json
    ↓
检查是否通过
    ├─ 通过 → Director审核
    └─ 失败 → 修复后重试
```

## 相关文件

| 文件 | 说明 |
|------|------|
| `common/flow-control-hook.md` | 流程控制钩子 |
| `common/self-check-validator.md` | 数据验证器 |
| `common/data-validator.md` | 数据验证工具集 |
