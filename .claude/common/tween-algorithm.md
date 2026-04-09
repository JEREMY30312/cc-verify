---
name: tween-algorithm
description: ANINEO V2.0 补帧逻辑算法模块。提供五大维度评估体系和高级认知判定，实现镜头层面的智能过渡帧生成。
---

# ANINEO V2.0 补帧逻辑算法模块

[模块说明]
    补帧（Tween）算法模块用于在 Sequence 阶段检测相邻镜头之间的叙事断裂，
    并智能生成过渡镜头以确保叙事连贯性。
    
    核心原则：镜头必须为故事服务，确保信息传递明确，
    严禁在单一镜头内堆叠过载的因果信息。

---

## 一、五大评估维度

### 1.1 维度概览

| 维度 | 字段来源 | 作用 | 触发阈值 |
|------|----------|------|----------|
| **物理轨迹跨度** | `physical_span` | 检测角色姿态或位置的剧烈突变 | gap ≥ 2.0 |
| **情感跨度** | `emotional_level` | 检测情绪状态的突发跳转 | gap ≥ 1.5 |
| **动机一致性** | `motivation` | 检测叙事意图是否断裂 | 不兼容转换 |
| **事件链因果审计** | 脚本语义 | 检查"因果动作"是否被错误压缩 | 缺失因果链 |
| **画面信息承载度** | 认知负荷判定 | 单镜头是否承载过多信息 | 超载熔断 |

---

## 二、物理轨迹跨度判定

### 2.1 物理跨度等级表

| 姿态类型 | physical_span 值 | 示例描述 |
|----------|------------------|----------|
| 静止态 | 1 | 站立、坐着、躺卧（无位移） |
| 缓移动态 | 2 | 慢走、转身、手部动作 |
| 中速动态 | 3 | 正常行走、快跑（非冲刺） |
| 激烈动态 | 4 | 冲刺、跳跃、战斗动作 |
| 极限动态 | 5 | 飞行、瞬移、超高速运动 |

### 2.2 跨度计算算法

```python
def calculate_physical_span_gap(shot_A, shot_B):
    """
    计算两个镜头之间的物理轨迹跨度
    
    Args:
        shot_A: 前一个镜头
        shot_B: 后一个镜头
    
    Returns:
        gap: 物理轨迹跨度 (0-5)
        need_tween: 是否需要补帧
        threshold: 使用的阈值
    """
    
    # 获取物理跨度数据
    span_A = shot_A.get("physical_span", 1)
    span_B = shot_B.get("physical_span", 1)
    
    # 计算跨度差
    gap = abs(span_B - span_A)
    
    # 判定阈值（可配置）
    PHYSICAL_GAP_THRESHOLD = 2.0
    
    # 高密度动作场景阈值放宽
    if shot_A.get("ndi_score", 0) >= 2.5:
        PHYSICAL_GAP_THRESHOLD = 3.0
    
    need_tween = gap >= PHYSICAL_GAP_THRESHOLD
    
    return {
        "gap": gap,
        "need_tween": need_tween,
        "threshold": PHYSICAL_GAP_THRESHOLD,
        "reason": f"物理跨度：{span_A} → {span_B}" if need_tween else None
    }

# 典型触发场景
TWEEN_TRIGGER_SCENARIOS = [
    ("坐着", 1, "站立", 3),      # gap=2，触发
    ("站立", 2, "奔跑", 5),      # gap=3，触发
    ("平静", 1, "暴怒", 4),      # gap=3，触发
    ("走路", 2, "飞行", 5),      # gap=3，触发
]
```

---

## 三、情感跨度判定

### 3.1 情绪权重表

| 情绪 | 权重值 | 说明 |
|------|--------|------|
| 平静 | 0 | 基准状态 |
| 压抑 | 0.5 | 轻微紧张 |
| 惊讶 | 1.0 | 轻度惊讶 |
| 喜悦 | 1.5 | 正面情绪 |
| 悲伤 | 2.0 | 负面情绪 |
| 恐惧 | 2.5 | 高度紧张 |
| 愤怒 | 3.0 | 强烈情绪 |

### 3.2 情感跨度计算算法

```python
# 情绪权重映射表
EMOTION_WEIGHTS = {
    "平静": 0,
    "压抑": 0.5,
    "惊讶": 1.0,
    "喜悦": 1.5,
    "悲伤": 2.0,
    "恐惧": 2.5,
    "愤怒": 3.0,
}

def calculate_emotional_span_gap(shot_A, shot_B):
    """
    计算两个镜头之间的情感跨度
    
    Args:
        shot_A: 前一个镜头
        shot_B: 后一个镜头
    
    Returns:
        gap: 情感跨度 (0-3)
        need_tween: 是否需要补帧
    """
    
    # 提取情绪状态
    mood_A = shot_A.get("mood", "平静")
    mood_B = shot_B.get("mood", "平静")
    
    # 获取权重
    weight_A = EMOTION_WEIGHTS.get(mood_A, 0)
    weight_B = EMOTION_WEIGHTS.get(mood_B, 0)
    
    # 计算跨度
    gap = abs(weight_B - weight_A)
    
    # 判定阈值
    EMOTIONAL_GAP_THRESHOLD = 1.5
    need_tween = gap >= EMOTIONAL_GAP_THRESHOLD
    
    return {
        "gap": gap,
        "need_tween": need_tween,
        "from_mood": mood_A,
        "to_mood": mood_B,
        "reason": f"情绪跨度：{mood_A} → {mood_B}" if need_tween else None
    }
```

---

## 四、动机一致性判定

### 4.1 动机兼容性矩阵

```python
# 动机类型
MOTIVATION_TYPES = [
    "威慑",
    "悬疑",
    "情感受创",
    "冲突升级",
    "氛围渲染",
    "信息传递"
]

# 兼容性矩阵：True=允许平滑转换，False=需要补帧
MOTIVATION_COMPATIBILITY = {
    "威慑": {
        "威慑": True,      # 同一动机延续
        "悬疑": True,      # 威慑→悬疑：张力升级
        "冲突升级": True,  # 威慑→冲突升级：动作升级
        "情感受创": False, # 威慑→情感受创：跨度大，需要补帧
        "氛围渲染": True,  # 威慑→氛围：铺垫
        "信息传递": True,  # 威慑→信息：威胁揭示
    },
    "悬疑": {
        "威慑": True,      # 悬疑→威慑：揭晓威胁
        "悬疑": True,      # 同一动机延续
        "冲突升级": True,  # 悬疑→冲突升级：危机爆发
        "情感受创": True,  # 悬疑→情感受创：可过渡
        "氛围渲染": True,  # 悬疑→氛围：加深悬念
        "信息传递": True,  # 悬疑→信息：线索揭晓
    },
    "情感受创": {
        "威慑": False,     # 情感受创→威慑：跨度大
        "悬疑": True,      # 情感受创→悬疑：悲伤→不安
        "冲突升级": True,  # 情感受创→冲突升级：悲伤→愤怒
        "情感受创": True,  # 同一动机延续
        "氛围渲染": True,  # 情感受创→氛围：情感渲染
        "信息传递": True,  # 情感受创→信息：情感线索
    },
    "冲突升级": {
        "威慑": False,     # 冲突升级→威慑：动作→静态
        "悬疑": False,     # 冲突升级→悬疑：动作→静态
        "冲突升级": True,  # 同一动机延续
        "情感受创": True,  # 冲突升级→情感受创：外部→内心
        "氛围渲染": True,  # 冲突升级→氛围：战后余韵
        "信息传递": True,  # 冲突升级→信息：结果揭示
    },
    "氛围渲染": {
        "威慑": True,      # 氛围→威慑：环境铺垫后威胁出现
        "悬疑": True,      # 氛围→悬疑：环境铺垫后悬念揭晓
        "冲突升级": True,  # 氛围→冲突升级：平静→激烈
        "情感受创": True,  # 氛围→情感受创：环境渲染情绪
        "氛围渲染": True,  # 同一动机延续
        "信息传递": True,  # 氛围→信息：场景信息传递
    },
    "信息传递": {
        "威慑": True,      # 信息→威慑：线索揭示威胁
        "悬疑": True,      # 信息→悬疑：线索加深悬念
        "冲突升级": True,  # 信息→冲突升级：线索引发冲突
        "情感受创": True,  # 信息→情感受创：线索导致情感变化
        "氛围渲染": True,  # 信息→氛围：信息补充氛围
        "信息传递": True,  # 同一动机延续
    },
}
```

### 4.2 动机一致性检查算法

```python
def check_motivation_coherence(shot_A, shot_B):
    """
    检查两个镜头的动机一致性
    
    Args:
        shot_A: 前一个镜头
        shot_B: 后一个镜头
    
    Returns:
        is_coherent: 动机是否一致
        need_tween: 是否需要补帧
    """
    
    motivation_A = shot_A.get("motivation", "信息传递")
    motivation_B = shot_B.get("motivation", "信息传递")
    
    # 检查兼容性
    compatibility_matrix = MOTIVATION_COMPATIBILITY.get(motivation_A, {})
    is_compatible = compatibility_matrix.get(motivation_B, False)
    
    if is_compatible:
        return {
            "is_coherent": True,
            "need_tween": False,
            "from": motivation_A,
            "to": motivation_B,
            "reason": "动机转换平滑"
        }
    else:
        return {
            "is_coherent": False,
            "need_tween": True,
            "from": motivation_A,
            "to": motivation_B,
            "reason": f"动机不兼容：{motivation_A} → {motivation_B}"
        }
```

---

## 五、事件链因果审计

### 5.1 因果动作识别

```python
# 因果动作关键词表
CAUSAL_VERBS = {
    "施力动作": ["打", "砸", "踢", "踹", "推", "轰", "拍", "掐", "砍", "劈"],
    "受力结果": ["飞", "碎", "裂", "倒", "塌", "飞溅", "崩", "毁", "散", "落"],
    "过程动作": ["冲", "奔", "跑", "跳", "跃", "滑", "翻", "转", "闪", "避"]
}

def detect_causal_chain(script_segment):
    """
    检测脚本片段中的因果动作链
    
    Args:
        script_segment: 脚本文本片段
    
    Returns:
        causal_chain: 因果链列表
        missing_causal: 缺失的因果环节
    """
    
    causal_chain = []
    missing_causal = []
    
    # 识别施力动作
    force_actions = []
    for verb in CAUSAL_VERBS["施力动作"]:
        if verb in script_segment:
            force_actions.append(verb)
    
    # 识别受力结果
    result_actions = []
    for verb in CAUSAL_VERBS["受力结果"]:
        if verb in script_segment:
            result_actions.append(verb)
    
    # 识别过程动作
    process_actions = []
    for verb in CAUSAL_VERBS["过程动作"]:
        if verb in script_segment:
            process_actions.append(verb)
    
    # 构建因果链
    if force_actions and result_actions:
        causal_chain.append({
            "type": "force_to_result",
            "force": force_actions,
            "result": result_actions,
            "has_process": len(process_actions) > 0
        })
    
    # 检测缺失环节
    if force_actions and not result_actions:
        missing_causal.append({
            "type": "missing_result",
            "description": "存在施力动作但无受力结果"
        })
    
    if force_actions and result_actions and not process_actions:
        missing_causal.append({
            "type": "missing_process",
            "description": "施力动作与受力结果之间缺少过程动作"
        })
    
    return {
        "causal_chain": causal_chain,
        "missing_causal": missing_causal,
        "is_complete": len(missing_causal) == 0
    }

def check_caudal_audit(shot_A, shot_B):
    """
    事件链因果审计
    
    检查两个镜头之间是否存在被压缩的因果链
    
    Returns:
        need_tween: 是否需要补帧
        reason: 原因说明
    """
    
    script_A = shot_A.get("scene_description", "")
    script_B = shot_B.get("scene_description", "")
    
    # 合并检查（跨镜头因果）
    combined_script = script_A + " " + script_B
    
    causal_check = detect_causal_chain(combined_script)
    
    # 如果因果链不完整，可能需要补帧
    if not causal_check["is_complete"]:
        return {
            "need_tween": True,
            "missing_parts": causal_check["missing_causal"],
            "reason": "因果链不完整，需要补帧展示过程"
        }
    
    return {
        "need_tween": False,
        "reason": "因果链完整"
    }
```

---

## 六、画面信息承载度判定

### 6.1 认知负荷评估

```python
def assess_cognitive_load(shot):
    """
    评估单个镜头的认知负荷
    
    Returns:
        load_level: 负荷等级 (low/medium/high/critical)
        load_score: 负荷分数 (0-10)
        factors: 负荷因素列表
    """
    
    scene_description = shot.get("scene_description", "")
    factors = []
    load_score = 0
    
    # 物理位移计数
    movement_keywords = ["跑", "跳", "飞", "走", "冲", "奔", "滑"]
    movement_count = sum(1 for keyword in movement_keywords if keyword in scene_description)
    if movement_count > 2:
        load_score += movement_count - 2
        factors.append(f"物理位移过多：{movement_count}次")
    
    # 环境破坏描述
    destruction_keywords = ["碎", "裂", "塌", "毁", "崩", "炸"]
    destruction_count = sum(1 for keyword in destruction_keywords if keyword in scene_description)
    if destruction_count > 1:
        load_score += destruction_count
        factors.append(f"环境破坏过多：{destruction_count}处")
    
    # 冲突重心检测
    conflict_keywords = ["打", "踢", "砸", "轰", "掐"]
    conflict_count = sum(1 for keyword in conflict_keywords if keyword in scene_description)
    if conflict_count > 1:
        load_score += conflict_count
        factors.append(f"多重冲突：{conflict_count}个动作重心")
    
    # 角色数量
    character_count = shot.get("character_count", 1)
    if character_count > 3:
        load_score += character_count - 3
        factors.append(f"角色过多：{character_count}人")
    
    # 判定负荷等级
    if load_score >= 8:
        load_level = "critical"
    elif load_score >= 5:
        load_level = "high"
    elif load_score >= 2:
        load_level = "medium"
    else:
        load_level = "low"
    
    return {
        "load_level": load_level,
        "load_score": load_score,
        "factors": factors,
        "need_split": load_level in ["critical", "high"]
    }
```

### 6.2 双重心冲突熔断

```python
def detect_dual_focus_conflict(shot):
    """
    检测双重心冲突（施力者动作 + 受力者反馈同时存在）
    
    Returns:
        has_dual_focus: 是否存在双重心
        need_tween: 是否需要拆分或补帧
    """
    
    scene_description = shot.get("scene_description", "")
    
    # 检测施力动作
    force_present = any(verb in scene_description for verb in CAUSAL_VERBS["施力动作"])
    
    # 检测受力反馈
    result_present = any(verb in scene_description for verb in CAUSAL_VERBS["受力结果"])
    
    if force_present and result_present:
        return {
            "has_dual_focus": True,
            "need_tween": True,
            "reason": "单镜头内同时存在施力动作与受力反馈，视为双重心冲突"
        }
    
    return {
        "has_dual_focus": False,
        "need_tween": False,
        "reason": "无双重心冲突"
    }
```

---

## 七、高级认知判定（导演逻辑）

### 7.1 空间平面跨越判定

```python
def check_depth_plane_transition(shot_A, shot_B):
    """
    空间平面跨越判定
    
    若动作导致角色从一个深度平面位移到另一个平面，
    必须补出位移轨迹镜头。
    
    深度平面定义：
    - 前景层：0-2米
    - 中景层：2-10米
    - 背景层：10-50米
    - 天空层：50米以上
    """
    
    # 提取镜头意图中的景别信息
    lens_A = shot_A.get("lens_intent", "")
    lens_B = shot_B.get("lens_intent", "")
    
    # 景别关键词映射
    SHOT_TYPES = {
        "特写": "前景",
        "近景": "前景",
        "中景": "中景",
        "全景": "中景",
        "远景": "背景",
        "大远景": "背景"
    }
    
    # 识别景别
    plane_A = "中景"  # 默认
    plane_B = "中景"  # 默认
    
    for shot_type, plane in SHOT_TYPES.items():
        if shot_type in lens_A:
            plane_A = plane
        if shot_type in lens_B:
            plane_B = plane
    
    # 判定跨越
    if plane_A != plane_B:
        return {
            "need_tween": True,
            "from_plane": plane_A,
            "to_plane": plane_B,
            "reason": f"空间平面跨越：{plane_A} → {plane_B}，需要补出位移轨迹"
        }
    
    return {
        "need_tween": False,
        "from_plane": plane_A,
        "to_plane": plane_B,
        "reason": "同一平面，无需补帧"
    }
```

### 7.2 主客体逆转审计

```python
def check_subject_object_reversal(shot_A, shot_B):
    """
    主客体逆转审计
    
    当脚本描述从"施力动作"转向"受力结果"时，
    必须生成过渡帧捕捉能量传递过程。
    """
    
    script_A = shot_A.get("scene_description", "")
    script_B = shot_B.get("scene_description", "")
    
    # 检测 A 是否为施力动作
    force_in_A = any(verb in script_A for verb in CAUSAL_VERBS["施力动作"])
    
    # 检测 B 是否为受力结果
    result_in_B = any(verb in script_B for verb in CAUSAL_VERBS["受力结果"])
    
    if force_in_A and result_in_B:
        return {
            "need_tween": True,
            "type": "subject_object_reversal",
            "reason": "施力动作→受力结果，需要补帧捕捉能量传递过程"
        }
    
    return {
        "need_tween": False,
        "reason": "无主客体逆转"
    }
```

---

## 八、综合判定算法

### 8.1 主判定函数

```python
def need_in_between_frame(shot_A, shot_B):
    """
    综合判定是否需要生成补帧镜头
    
    执行五大维度评估 + 高级认知判定
    
    Args:
        shot_A: 前一个镜头
        shot_B: 后一个镜头
    
    Returns:
        result: 综合判定结果
    """
    
    reasons = []
    priority = "low"
    
    # 1. 物理轨迹检查
    physical = calculate_physical_span_gap(shot_A, shot_B)
    if physical["need_tween"]:
        reasons.append({
            "type": "physical_span",
            "detail": physical["reason"],
            "gap": physical["gap"]
        })
    
    # 2. 情感跨度检查
    emotional = calculate_emotional_span_gap(shot_A, shot_B)
    if emotional["need_tween"]:
        reasons.append({
            "type": "emotional_span",
            "detail": emotional["reason"],
            "gap": emotional["gap"]
        })
    
    # 3. 动机一致性检查
    motivation = check_motivation_coherence(shot_A, shot_B)
    if motivation["need_tween"]:
        reasons.append({
            "type": "motivation",
            "detail": motivation["reason"]
        })
    
    # 4. 事件链因果审计
    causal = check_caudal_audit(shot_A, shot_B)
    if causal["need_tween"]:
        reasons.append({
            "type": "causal_chain",
            "detail": causal["reason"],
            "missing": causal.get("missing_parts")
        })
    
    # 5. 画面承载度检查
    load_A = assess_cognitive_load(shot_A)
    load_B = assess_cognitive_load(shot_B)
    
    if load_A["need_split"] or load_B["need_split"]:
        reasons.append({
            "type": "cognitive_load",
            "detail": "画面承载度过高，需要拆分或补帧",
            "load_A": load_A,
            "load_B": load_B
        })
    
    # 双重心冲突检查
    dual_A = detect_dual_focus_conflict(shot_A)
    dual_B = detect_dual_focus_conflict(shot_B)
    
    if dual_A["need_tween"] or dual_B["need_tween"]:
        reasons.append({
            "type": "dual_focus",
            "detail": "双重心冲突，需要补帧"
        })
    
    # 高级认知判定
    depth_transition = check_depth_plane_transition(shot_A, shot_B)
    if depth_transition["need_tween"]:
        reasons.append({
            "type": "depth_plane",
            "detail": depth_transition["reason"]
        })
    
    subject_reversal = check_subject_object_reversal(shot_A, shot_B)
    if subject_reversal["need_tween"]:
        reasons.append({
            "type": "subject_object_reversal",
            "detail": subject_reversal["reason"]
        })
    
    # 综合判定
    need_tween = len(reasons) > 0
    
    # 计算补帧数量
    if not need_tween:
        tween_count = 0
    else:
        max_gap = max([
            r.get("gap", 0) for r in reasons 
            if r.get("gap") is not None
        ] + [1.5])
        
        if max_gap >= 3.0:
            tween_count = 3
        elif max_gap >= 2.0:
            tween_count = 2
        else:
            tween_count = 1
    
    # 确定优先级
    critical_types = ["cognitive_load", "dual_focus", "depth_plane", "subject_object_reversal"]
    if any(r["type"] in critical_types for r in reasons):
        priority = "high"
    elif any(r["type"] == "physical_span" for r in reasons):
        priority = "medium"
    else:
        priority = "low"
    
    return {
        "need_tween": need_tween,
        "reasons": reasons,
        "tween_count": tween_count,
        "priority": priority,
        "shot_A_id": shot_A.get("shot_id"),
        "shot_B_id": shot_B.get("shot_id")
    }
```

---

## 九、补帧生成规范

### 9.1 数量计算公式

```
tween_count = ceil(max(physical_gap, emotional_gap) / 1.5)
```

| max_gap 范围 | 补帧数量 |
|--------------|----------|
| < 1.5 | 0（无需补帧） |
| 1.5 - 2.9 | 1 |
| 3.0 - 4.4 | 2 |
| ≥ 4.5 | 3 |

### 9.2 补帧类型分类

| 补帧类型 | 触发条件 | 典型场景 |
|----------|----------|----------|
| **物理过渡** | 物理跨度大，情感稳定 | 站立 → 奔跑 |
| **情感弧线** | 情绪跨度大，动作较小 | 平静 → 惊恐（微表情演变） |
| **动机桥梁** | 叙事意图不兼容 | 氛围渲染 → 冲突升级 |
| **因果双重建** | 物理与情感双重断裂 | 坐着喝酒 → 暴起杀人 |
| **能量传递** | 主客体逆转 | 拳头轰下 → 撞碎碑石 |
| **平面跨越** | 空间平面变化 | 近景 → 远景 |

---

## 十、补帧数据结构

### 10.1 JSON 结构规范

```json
{
  "tween_shot_id": "S05-T01",
  "parent_shot_A": "S05",
  "parent_shot_B": "S06",
  "tween_type": "physical_emotional",
  "sequence_position": 1,
  "total_tweens": 3,
  "is_ai_generated": true,
  "generation_marker": "[In-between added by AI]",
  "scene_description": "鲁达眼神变化 - 从漫不经心到瞳孔骤缩，右手逐渐握紧拳头，身体重心开始前移",
  "transition_type": "energy_transfer",
  "physical_span": {
    "start": 1,
    "end": 4,
    "interpolation": "ease-in-out"
  },
  "emotional_arc": {
    "start_mood": "平静",
    "end_mood": "愤怒",
    "transition_steps": ["眼神从涣散到聚焦", "呼吸节奏变化", "右手握紧"]
  },
  "relay_point": {
    "exit_vector": "向右出画",
    "visual_anchor": "拳头"
  },
  "confidence": 75
}
```

### 10.2 Markdown 标记规范

```
## 格05 [In-between added by AI]

### 补帧类型：能量传递
- **前序镜头**：S05（鲁达坐着喝酒）
- **后续镜头**：S06（鲁达暴起踹翻案板）
- **触发原因**：主客体逆转（施力→受力）

**画面描述**：[In-between added by AI] 鲁达眼神变化 - 从漫不经心到瞳孔骤缩，右手逐渐握紧拳头，身体重心开始前移
```

---

## 十一、配置参数

### 11.1 可配置阈值

```json
{
  "tween_algorithm": {
    "thresholds": {
      "physical_gap": 2.0,
      "emotional_gap": 1.5,
      "high_density_physical_threshold": 3.0
    },
    "tween_count_rules": {
      "max_tweens": 3,
      "min_tweens": 1
    }
  }
}
```

---

## 十二、子镜头补帧扩展【V2.0 模块 4 新增】

### 12.1 子镜头补帧检测目标

在多镜头节拍的子镜头之间（如：S05-1 → S05-2 → S05-3）执行补帧检测，确保子镜头序列的连贯性。

### 12.2 子镜头补帧触发位置

**检测位置**：同一多镜头节拍的相邻子镜头之间

**示例**：
- S05-1 → S05-2：检测是否需要补帧
- S05-2 → S05-3：检测是否需要补帧
- S05（父镜头）→ S06（下一镜头）：正常检测（不变）

### 12.3 子镜头补帧数据来源

子镜头补帧检测使用 `scene_breakdown.json` 中的 `sub_shots` 数组数据：

| 数据字段 | 来源 | 说明 |
|----------|------|------|
| lens_type | sub_shots[].lens_type | 镜头类型（特写/中景/全景/远景等） |
| scene_description | sub_shots[].scene_description | 子镜头场景描述 |
| visual_anchor | sub_shots[].visual_anchor | 视觉锚点（用于镜头衔接） |
| motion_type | sub_shots[].motion_type | 运动类型（推/拉/摇/移/跟等） |
| transition_type | sub_shots[].transition_type | 转场类型（切/溶/叠化等） |

### 12.4 子镜头补帧判定规则

子镜头补帧判定遵循与常规镜头相同的五大维度评估，但有特殊规则：

#### 规则 1：景别变化优先检测
- 同一多镜头节拍的子镜头通常存在景别变化（如：特写→全景→远景）
- 景别变化越大，补帧需求越高
- 景别跨度≥3（如：特写1→远景5）强制补帧

#### 规则 2：视觉锚点连续性
- 检查相邻子镜头的 visual_anchor 是否形成视觉引导链
- visual_anchor 断裂（如：S05-1 锚点为"眼神"，S05-2 锚点为"脚部"，无过渡）需要补帧

#### 规则 3：运动类型平滑过渡
- 检查 motion_type 的连续性（如：推→拉需要补帧，推→推可直接切）
- motion_type 跳跃（如：跟→移）需要补帧

#### 规则 4：转场类型合理性
- 检查 transition_type 是否符合视觉逻辑（如：切→叠化→切）
- 转场类型不连贯（如：溶→溶→溶）需要补帧

### 12.5 子镜头补帧数量计算

```python
def calculate_sub_shot_tween_count(sub_shot_A, sub_shot_B):
    """
    计算子镜头之间的补帧数量

    子镜头补帧通常比常规镜头更精细（同一场景内的过渡）

    Returns:
        tween_count: 补帧数量 (1-2)
    """

    # 景别跨度
    lens_A = sub_shot_A.get("lens_type", "")
    lens_B = sub_shot_B.get("lens_type", "")

    LENS_ORDER = ["特写", "近景", "中景", "全景", "远景", "大远景"]

    try:
        lens_span_A = LENS_ORDER.index(lens_A)
        lens_span_B = LENS_ORDER.index(lens_B)
    except ValueError:
        lens_span_A = 2  # 默认中景
        lens_span_B = 2

    lens_gap = abs(lens_span_B - lens_span_A)

    # 运动类型跨度
    motion_A = sub_shot_A.get("motion_type", "")
    motion_B = sub_shot_B.get("motion_type", "")

    # 运动类型兼容性（True=无需补帧）
    MOTION_COMPATIBILITY = {
        ("推", "推"): True,
        ("拉", "拉"): True,
        ("摇", "摇"): True,
        ("移", "移"): True,
        ("跟", "跟"): True,
    }

    motion_compatible = MOTION_COMPATIBILITY.get((motion_A, motion_B), False)

    # 视觉锚点连续性
    anchor_A = sub_shot_A.get("visual_anchor", "")
    anchor_B = sub_shot_B.get("visual_anchor", "")

    # 检测锚点是否相关（简单启发式）
    anchor_related = (
        (anchor_A in anchor_B) or
        (anchor_B in anchor_A) or
        (len(set(anchor_A.split()) & set(anchor_B.split())) > 0)
    )

    # 综合判定
    if lens_gap >= 3:
        # 景别跨度大，需要2个补帧
        tween_count = 2
    elif lens_gap >= 2:
        # 景别跨度中等，需要1个补帧
        tween_count = 1
    elif not motion_compatible:
        # 运动类型不兼容，需要1个补帧
        tween_count = 1
    elif not anchor_related:
        # 视觉锚点不相关，需要1个补帧
        tween_count = 1
    else:
        # 无需补帧
        tween_count = 0

    return {
        "tween_count": tween_count,
        "lens_gap": lens_gap,
        "motion_compatible": motion_compatible,
        "anchor_related": anchor_related
    }
```

### 12.6 子镜头补帧ID命名规范

子镜头补帧ID格式：`{子镜头ID}-T{序号}`

**示例**：
- S05-1-T01：S05-1 和 S05-2 之间的补帧
- S05-2-T01：S05-2 和 S05-3 之间的补帧

**JSON 结构示例**：

```json
{
  "tween_shot_id": "S05-1-T01",
  "parent_sub_shot_A": "S05-1",
  "parent_sub_shot_B": "S05-2",
  "parent_shot_id": "S05",
  "tween_type": "lens_transition",
  "sequence_position": 1,
  "total_tweens": 1,
  "is_ai_generated": true,
  "generation_marker": "[In-between added by AI]",
  "scene_description": "从角色面部特写平滑过渡到角色全身，镜头缓慢拉远，保留角色眼神变化",
  "lens_transition": {
    "start": "特写",
    "end": "全景",
    "interpolation": "smooth_pull"
  },
  "visual_anchor": "眼神",
  "relay_point": {
    "exit_vector": "向右出画",
    "visual_anchor": "眼神"
  },
  "confidence": 85
}
```

### 12.7 子镜头补帧与常规补帧对比

| 对比项 | 常规补帧 | 子镜头补帧 |
|--------|----------|------------|
| **检测位置** | S05 → S06（不同镜头） | S05-1 → S05-2（同一父镜头） |
| **数据来源** | scene_breakdown.shots[] | scene_breakdown.shots[].sub_shots[] |
| **补帧数量** | 1-3 个（取决于gap） | 1-2 个（更精细） |
| **ID格式** | S05-T01 | S05-1-T01 |
| **触发阈值** | 五大维度综合评估 | 优先景别变化（lens_gap≥3） |
| **优先级** | 与常规补帧同等 | 优先保证子镜头连贯性 |

### 12.8 子镜头补帧集成到主判定函数

```python
def need_in_between_frame_extended(shot_A, shot_B, sub_shots_mode=False):
    """
    扩展版补帧判定函数

    支持子镜头模式（sub_shots_mode=True）

    Args:
        shot_A: 前一个镜头或子镜头
        shot_B: 后一个镜头或子镜头
        sub_shots_mode: 是否为子镜头模式

    Returns:
        result: 综合判定结果
    """

    if sub_shots_mode:
        # 子镜头模式：使用子镜头专用判定
        return calculate_sub_shot_tween_count(shot_A, shot_B)
    else:
        # 常规模式：使用五大维度判定
        return need_in_between_frame(shot_A, shot_B)

# 使用示例
# 常规补帧
result_regular = need_in_between_frame_extended(S05, S06, sub_shots_mode=False)

# 子镜头补帧
result_sub_shot = need_in_between_frame_extended(S05_1, S05_2, sub_shots_mode=True)
```

---

[使用说明]
    本模块由 film-storyboard-skill/SKILL.md 在 Sequence 阶段调用：

    **常规补帧**：
    1. 读取 scene_breakdown.json 中的全量原子镜头
    2. 对相邻镜头对执行 need_in_between_frame() 判定
    3. 对需要补帧的镜头对生成补帧镜头序列
    4. 将补帧镜头插入到输出中，并添加 [In-between added by AI] 标记
    5. 同步更新 scene-breakdown-tweened.json

    **子镜头补帧**【V2.0 模块 4 新增】：
    1. 读取 scene_breakdown.json 中的 sub_shots 数组
    2. 对同一多镜头节拍的相邻子镜头对执行 calculate_sub_shot_tween_count() 判定
    3. 对需要补帧的子镜头对生成补帧镜头序列
    4. 将补帧镜头插入到子镜头序列中，并添加 [In-between added by AI] 标记
    5. 子镜头补帧ID格式：{子镜头ID}-T{序号}（如：S05-1-T01）
    6. 确保子镜头补帧的 visual_anchor 有效连接前后子镜头

    **集成流程**：
    - 先执行常规补帧检测（镜头级别）
    - 再执行子镜头补帧检测（子镜头级别）
    - 优先级：子镜头补帧 > 常规补帧（确保同一多镜头节拍内部连贯性）
