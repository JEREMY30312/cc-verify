# 数据验证工具集

## 概述

数据验证工具集提供各阶段的自动化验证函数，用于检查产出物的数据准确性和完整性。

## 1. 节拍拆解验证器

```python
class BeatBreakdownValidator:
    """节拍拆解数据验证器"""
    
    def __init__(self, file_path):
        self.file_path = file_path
        self.content = ""
        self.load_content()
    
    def load_content(self):
        """加载文件内容"""
        with open(self.file_path, 'r') as f:
            self.content = f.read()
    
    def validate_all(self) -> dict:
        """执行所有验证"""
        checks = {
            "beat_count": self.validate_beat_count(),
            "three_act_ratio": self.validate_three_act_ratio(),
            "keyframe_distribution": self.validate_keyframe_distribution(),
            "style_transitions": self.validate_style_transitions(),
            "narrative_completeness": self.validate_narrative_completeness()
        }
        
        return self._generate_report(checks)
    
    def validate_beat_count(self) -> dict:
        """验证节拍数量"""
        # 节拍以 | 开头且包含场景描述的行
        beats = re.findall(r'^\|\s*\d+\s*\|', self.content, re.MULTILINE)
        
        return {
            "check": "beat_count",
            "passed": True,
            "actual": len(beats),
            "expected_range": (8, 12),
            "status": "info"
        }
    
    def validate_three_act_ratio(self) -> dict:
        """验证三幕比例"""
        # 提取三幕比例数据
        ratios = {
            "第一幕": re.search(r'第一幕.*?(\d+)%', self.content),
            "第二幕": re.search(r'第二幕.*?(\d+)%', self.content),
            "第三幕": re.search(r'第三幕.*?(\d+)%', self.content)
        }
        
        results = {}
        all_passed = True
        
        for act, match in ratios.items():
            if match:
                percentage = int(match.group(1))
                results[act] = percentage
                
                # 验证比例范围
                if act == "第一幕" and not (20 <= percentage <= 30):
                    all_passed = False
                elif act == "第二幕" and not (40 <= percentage <= 60):
                    all_passed = False
                elif act == "第三幕" and not (20 <= percentage <= 30):
                    all_passed = False
        
        return {
            "check": "three_act_ratio",
            "passed": all_passed,
            "data": results,
            "status": "warn" if results else "error"
        }
    
    def validate_keyframe_distribution(self) -> dict:
        """验证关键帧分布"""
        distribution = {
            "🔴": len(re.findall(r'🔴', self.content)),
            "🟠": len(re.findall(r'🟠', self.content)),
            "🟡": len(re.findall(r'🟡', self.content)),
            "🔵": len(re.findall(r'🔵', self.content))
        }
        
        return {
            "check": "keyframe_distribution",
            "passed": True,
            "data": distribution,
            "status": "info"
        }
    
    def validate_style_transitions(self) -> dict:
        """验证风格转换"""
        transitions = re.findall(r'\d+\s*→\s*\d+', self.content)
        
        return {
            "check": "style_transitions",
            "passed": True,
            "count": len(transitions),
            "status": "info"
        }
    
    def validate_narrative_completeness(self) -> dict:
        """验证叙事完整性"""
        required_elements = [
            "世界观建立", "诱因事件", "冲突升级", "高潮",
            "结局", "转折"
        ]
        
        found = []
        for element in required_elements:
            if element in self.content:
                found.append(element)
        
        return {
            "check": "narrative_completeness",
            "passed": len(found) >= 4,
            "found": found,
            "missing": [e for e in required_elements if e not in self.content],
            "status": "warn" if len(found) < 4 else "info"
        }
```

## 2. 九宫格验证器

```python
class BeatboardValidator:
    """九宫格数据验证器"""
    
    def __init__(self, file_path):
        self.file_path = file_path
        self.content = ""
        self.load_content()
    
    def load_content(self):
        """加载文件内容"""
        with open(self.file_path, 'r') as f:
            self.content = f.read()
    
    def validate_all(self) -> dict:
        """执行所有验证"""
        checks = {
            "keyframe_count": self.validate_keyframe_count(),
            "elimination_reason": self.validate_elimination_reason(),
            "keyframe_levels": self.validate_keyframe_levels(),
            "prompt_format": self.validate_prompt_format(),
            "style_consistency": self.validate_style_consistency()
        }
        
        return self._generate_report(checks)
    
    def validate_keyframe_count(self) -> dict:
        """验证关键帧数量"""
        keyframes = re.findall(r'^##\s*关键帧\s*\d+', self.content, re.MULTILINE)
        
        return {
            "check": "keyframe_count",
            "passed": 8 <= len(keyframes) <= 12,
            "actual": len(keyframes),
            "expected_range": (8, 12),
            "status": "error" if len(keyframes) < 8 or len(keyframes) > 12 else "info"
        }
    
    def validate_elimination_reason(self) -> dict:
        """验证淘汰节拍是否有理由"""
        eliminations = re.findall(r'淘汰.*?\d+', self.content)
        
        return {
            "check": "elimination_reason",
            "passed": len(eliminations) > 0,
            "count": len(eliminations),
            "status": "warn" if not eliminations else "info"
        }
    
    def validate_keyframe_levels(self) -> dict:
        """验证关键帧等级分布"""
        distribution = {
            "🔴": len(re.findall(r'🔴', self.content)),
            "🟠": len(re.findall(r'🟠', self.content)),
            "🟡": len(re.findall(r'🟡', self.content))
        }
        
        # 特级关键帧应该有2-3个
        passed = 1 <= distribution["🔴"] <= 3
        
        return {
            "check": "keyframe_levels",
            "passed": passed,
            "data": distribution,
            "status": "error" if not passed else "info"
        }
    
    def validate_prompt_format(self) -> dict:
        """验证提示词格式"""
        # 检查每个关键帧是否有完整的提示词
        prompts = re.findall(r'画面描述[：:].*?(?=##\s*关键帧|$)', self.content, re.DOTALL)
        
        complete_prompts = 0
        for prompt in prompts:
            if len(prompt) > 50:  # 有效提示词长度
                complete_prompts += 1
        
        return {
            "check": "prompt_format",
            "passed": complete_prompts >= len(prompts) * 0.8,
            "complete": complete_prompts,
            "total": len(prompts),
            "status": "warn" if complete_prompts < len(prompts) * 0.8 else "info"
        }
    
    def validate_style_consistency(self) -> dict:
        """验证风格一致性"""
        styles = re.findall(r'视觉风格[：:][^\n]+', self.content)
        
        # 检查是否包含国漫关键词
        guoman_keywords = ["国潮", "赛璐璐", "平涂", "墨线"]
        has_guoman = any(kw in " ".join(styles) for kw in guoman_keywords)
        
        return {
            "check": "style_consistency",
            "passed": has_guoman,
            "styles": styles[:3],  # 只返回前3个
            "status": "error" if not has_guoman else "info"
        }
```

## 3. 四宫格验证器

```python
class SequenceValidator:
    """四宫格数据验证器"""
    
    def __init__(self, file_path):
        self.file_path = file_path
        self.content = ""
        self.load_content()
    
    def load_content(self):
        """加载文件内容"""
        with open(self.file_path, 'r') as f:
            self.content = f.read()
    
    def validate_all(self) -> dict:
        """执行所有验证"""
        checks = {
            "sequence_count": self.validate_sequence_count(),
            "total_frames": self.validate_total_frames(),
            "style_distribution": self.validate_style_distribution(),
            "coherence": self.validate_coherence(),
            "continuity": self.validate_continuity()
        }
        
        return self._generate_report(checks)
    
    def validate_sequence_count(self) -> dict:
        """验证序列数量"""
        sequences = re.findall(r'^##\s*序列\s*\d+', self.content, re.MULTILINE)
        
        return {
            "check": "sequence_count",
            "passed": len(sequences) == 9,
            "actual": len(sequences),
            "expected": 9,
            "status": "error" if len(sequences) != 9 else "info"
        }
    
    def validate_total_frames(self) -> dict:
        """验证总画面数"""
        # 每个序列有4个画面
        sequences = re.findall(r'^##\s*序列\s*\d+', self.content, re.MULTILINE)
        expected_frames = len(sequences) * 4
        
        # 统计画面标记
        frames = re.findall(r'^###\s*\d+\.\d+\s', self.content, re.MULTILINE)
        actual_frames = len(frames)
        
        return {
            "check": "total_frames",
            "passed": actual_frames == expected_frames,
            "actual": actual_frames,
            "expected": expected_frames,
            "status": "error" if actual_frames != expected_frames else "info"
        }
    
    def validate_style_distribution(self) -> dict:
        """验证风格分布"""
        # 统计国漫和MCU的出现次数
        guoman_count = len(re.findall(r'国漫|国潮', self.content))
        mcu_count = len(re.findall(r'MCU|电影史诗感', self.content))
        
        return {
            "check": "style_distribution",
            "passed": guoman_count > 0 and mcu_count > 0,
            "data": {
                "国漫风格": guoman_count,
                "MCU风格": mcu_count
            },
            "status": "error" if guoman_count == 0 or mcu_count == 0 else "info"
        }
    
    def validate_coherence(self) -> dict:
        """验证连贯性"""
        checks = [
            ("角色一致性", r"鲁达|镇关西|包子猪"),
            ("镜头连贯", r"镜头|画面"),
            ("动作连贯", r"动作|运动")
        ]
        
        results = {}
        all_passed = True
        
        for name, pattern in checks:
            count = len(re.findall(pattern, self.content))
            passed = count > 5
            results[name] = {"count": count, "passed": passed}
            if not passed:
                all_passed = False
        
        return {
            "check": "coherence",
            "passed": all_passed,
            "data": results,
            "status": "warn" if not all_passed else "info"
        }
    
    def validate_continuity(self) -> dict:
        """验证连续性"""
        # 检查相邻序列之间是否有衔接描述
       衔接 = len(re.findall(r'衔接|过渡|承接', self.content))
        
        return {
            "check": "continuity",
            "passed": 衔接 >= 3,
            "actual": 衔接,
            "expected": 3,
            "status": "warn" if 衔接 < 3 else "info"
        }
```

## 4. 动态提示词验证器

```python
class MotionPromptValidator:
    """动态提示词数据验证器"""
    
    def __init__(self, file_path):
        self.file_path = file_path
        self.content = ""
        self.load_content()
    
    def load_content(self):
        """加载文件内容"""
        with open(self.file_path, 'r') as f:
            self.content = f.read()
    
    def validate_all(self) -> dict:
        """执行所有验证"""
        checks = {
            "motion_count": self.validate_motion_count(),
            "pass_rate": self.validate_pass_rate(),
            "five_modules": self.validate_five_modules(),
            "physics_compliance": self.validate_physics_compliance()
        }
        
        return self._generate_report(checks)
    
    def validate_motion_count(self) -> dict:
        """验证Motion Prompt数量"""
        sequences = re.findall(r'^##\s*序列\s*\d+', self.content, re.MULTILINE)
        
        return {
            "check": "motion_count",
            "passed": len(sequences) == 9,
            "actual": len(sequences),
            "expected": 9,
            "status": "error" if len(sequences) != 9 else "info"
        }
    
    def validate_pass_rate(self) -> dict:
        """验证物理通过率"""
        passed = len(re.findall(r'✅', self.content))
        warning = len(re.findall(r'⚠️', self.content))
        total = passed + warning
        
        rate = passed / total * 100 if total > 0 else 0
        
        return {
            "check": "pass_rate",
            "passed": rate >= 50,
            "data": {
                "通过": passed,
                "艺术处理": warning,
                "通过率": f"{rate:.1f}%"
            },
            "status": "error" if rate < 50 else "warn" if rate < 70 else "info"
        }
    
    def validate_five_modules(self) -> dict:
        """验证五模块覆盖率"""
        modules = {
            "镜头运动": len(re.findall(r'镜头|推|拉|摇|移|跟', self.content)),
            "主体动作": len(re.findall(r'动作|跑|走|跳|手势', self.content)),
            "环境动态": len(re.findall(r'环境|光影|气流|粒子', self.content)),
            "节奏控制": len(re.findall(r'节奏|速度|快慢', self.content)),
            "氛围强化": len(re.findall(r'氛围|特效|光晕', self.content))
        }
        
        # 每个模块至少出现10次
        all_passed = all(count >= 10 for count in modules.values())
        
        return {
            "check": "five_modules",
            "passed": all_passed,
            "data": modules,
            "status": "error" if not all_passed else "info"
        }
    
    def validate_physics_compliance(self) -> dict:
        """验证物理合规性"""
        # 检查是否有明显的物理错误
        physics_errors = len(re.findall(r'违反物理|不合理', self.content))
        
        return {
            "check": "physics_compliance",
            "passed": physics_errors == 0,
            "errors": physics_errors,
            "status": "error" if physics_errors > 0 else "info"
        }
```

## 验证报告生成

```python
def _generate_report(self, checks: dict) -> dict:
    """生成验证报告"""
    passed = sum(1 for c in checks.values() if c["passed"])
    total = len(checks)
    
    report = {
        "validator": self.__class__.__name__,
        "file_path": self.file_path,
        "timestamp": get_timestamp(),
        "total_checks": total,
        "passed_checks": passed,
        "failed_checks": total - passed,
        "pass_rate": passed / total * 100,
        "overall_status": "PASS" if passed == total else ("WARN" if passed > 0 else "FAIL"),
        "checks": checks
    }
    
    return report
```

## 使用方式

```python
# 节拍拆解验证
validator = BeatBreakdownValidator("outputs/beat-breakdown-ep01.md")
report = validator.validate_all()

# 九宫格验证
validator = BeatboardValidator("outputs/beat-board-prompt-ep01.md")
report = validator.validate_all()

# 四宫格验证
validator = SequenceValidator("outputs/sequence-board-prompt-ep01.md")
report = validator.validate_all()

# 动态提示词验证
validator = MotionPromptValidator("outputs/motion-prompt-ep01.md")
report = validator.validate_all()

# 检查结果
if report["overall_status"] == "FAIL":
    print("验证失败，需要修复")
    for check in report["checks"].values():
        if not check["passed"]:
            print(f"  - {check['check']}: {check.get('message', '未知错误')}")
elif report["overall_status"] == "WARN":
    print("验证通过，但有警告")
else:
    print("验证全部通过")
```

## 验证结果处理

| 状态 | 说明 | 处理方式 |
|------|------|----------|
| **PASS** | 全部通过 | 继续流程 |
| **WARN** | 部分通过 | 记录警告，继续流程 |
| **FAIL** | 全部失败 | 阻断流程，需修复 |

## 相关文件

| 文件 | 说明 |
|------|------|
| `common/flow-control-hook.md` | 流程控制钩子 |
| `common/self-check-validator.md` | 数据验证器 |
| `agents/producer-self-check.md` | 制片人自查生成器 |
