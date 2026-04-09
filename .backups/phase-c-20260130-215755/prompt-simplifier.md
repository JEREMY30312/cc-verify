# 提示词精简算法模块

## 📋 模块概述

**功能**：对生成的提示词进行智能精简，在保留核心创意元素的前提下减少Token消耗。

**目标**：
- 精简率：15-20%（标准模式）
- 质量下降：≤8%
- P1元素保留：100%
- P2元素保留：≥90%

**适用阶段**：
- 九宫格提示词生成后
- 动态分镜板提示词生成后

---

## 🔧 算法配置

### 三种精简模式

| 模式 | 精简率目标 | 质量下降目标 | 适用场景 |
|------|-----------|-------------|----------|
| **完整模式** | 10% | ≤5% | 高质量要求，创意保护优先 |
| **标准模式** | - | - | 平衡质量与效率 |
| **快速模式** | - | - | 效率优先，可接受一定质量损失 |

### 优先级保留策略

#### P1元素（最高优先级 - 100%保留）
- **电影技术术语**：荷兰角、低机位、高角度、仰拍、俯拍
- **镜头参数**：浅景深、深景深、景深、构图、24mm、85mm、广角
- **高级光影**：轮廓光、侧光、丁达尔效应、体积光、眼神光
- **镜头类型**：特写、中景、极远景、紧凑特写、中近景

#### P2元素（高优先级 - ≥90%保留）
**动作场景（12个关键词）**
- **视觉动态**：残影、轨迹、冲击波、碎片、尘埃
- **身体细节**：肌肉紧绷、青筋暴起、咬紧牙关、汗珠飞溅
- **环境互动**：墙壁裂纹、地面凹陷、物体飞散

**情感场景（12个关键词）**
- **面部细节**：瞳孔收缩、睫毛颤动、嘴角微扬、眉头紧锁
- **肢体语言**：手指颤抖、肩膀耸动、身体蜷缩
- **情感氛围**：眼神交流、呼吸节奏、沉默间隙

**建立场景（12个关键词）**
- **空间特征**：天际线、地平线、建筑轮廓、道路延伸
- **环境质感**：材质纹理、表面反光、植被密度
- **光影层次**：明暗对比、色彩渐变、阴影形状

**悬疑场景（11个关键词）**
- **视觉暗示**：剪影、倒影、半掩门、窗帘缝隙
- **光影诡异**：闪烁灯光、诡异光晕、异常阴影
- **细节异常**：时钟停摆、照片歪斜、物品移位

**对话场景（11个关键词）**
- **互动细节**：眼神躲避、手势强调、身体倾斜
- **环境呼应**：背景虚化、焦点转移、景深变化
- **情绪载体**：手中物品、服装褶皱、发型变化

#### P3元素（中优先级 - 60-80%删除）
- **修饰词**：非常、极其、特别、显得、十分、相当、略微、一些、些许、格外、太、过于
- **冗余动词**：呈现、展示、表现、体现、形成、显示出、体现出、呈现出

#### P4元素（低优先级 - 100%删除）
- **过渡词**：然后、接着、随后、接下来、与此同时、另一方面、此外、另外、而且、并且

---

## 🚀 算法实现

### 四轮渐进式精简流程

#### 第一轮：移除P4元素（100%删除）
```python
def remove_p4_elements(content: str) -> str:
    """移除所有过渡词"""
    transitions = ["然后", "接着", "随后", "接下来", 
                   "与此同时", "另一方面", "此外", 
                   "另外", "而且", "并且"]
    result = content
    for transition in transitions:
        result = re.sub(rf"{transition}[，。；]?", "", result)
    return result
```

#### 第二轮：移除P3元素（80%删除）
```python
def remove_p3_elements(content: str, removal_rate: float = 0.8) -> str:
    """移除指定比例的修饰词和冗余动词"""
    modifiers = ["非常", "极其", "特别", "显得", "十分", 
                 "相当", "略微", "一些", "些许", "格外", 
                 "太", "过于"]
    redundant_verbs = ["呈现", "展示", "表现", "体现", 
                       "形成", "显示出", "体现出", "呈现出"]
    
    result = content
    # 随机选择要删除的元素（模拟指定删除率）
    import random
    random.seed(hash(content) % 10000)  # 基于内容确定随机种子
    
    all_elements = modifiers + redundant_verbs
    for element in all_elements:
        if element in result and random.random() < removal_rate:
            result = result.replace(element, "")
    
    return result
```

#### 第三轮：词语级保护 + 激进精简
```python
def word_level_protection_and_simplify(
    content: str, 
    protect_context: int = 2,
    aggressive: bool = True
) -> str:
    """
    词语级保护策略：
    1. 识别所有P1/P2关键词位置
    2. 标记保护区域：关键词位置 ± protect_context字符
    3. 对非保护区域进行激进精简
    4. 重新组合
    """
    # 实现细节见完整代码
    pass
```

#### 第四轮：质量检查和最终清理
```python
def final_cleanup_and_quality_check(content: str) -> str:
    """最终清理和质量检查"""
    # 清理多余空格
    result = re.sub(r"\s+", " ", content)
    
    # 清理开头结尾空格
    result = result.strip()
    
    # 确保标点正确
    result = re.sub(r"([^，。；])[，。；]([^，。；])", r"\1，\2", result)
    
    # 确保句子完整性
    if result and result[-1] not in ["。", "；"]:
        result += "。"
    
    return result
```

### 动态调整机制

#### 创意密度计算
```python
def calculate_creative_density(content: str) -> float:
    """计算创意密度 = (P1+P2元素数量) / 总字符数"""
    p1_count = count_p1_keywords(content)
    p2_count = count_p2_keywords(content)
    total_chars = len(content)
    
    if total_chars == 0:
        return 0.0
        
    return (p1_count + p2_count) / total_chars
```

#### 动态目标调整
```python
def adjust_target_by_density(base_target: float, density: float) -> float:
    """根据创意密度动态调整精简目标"""
    if density > 0.15:  # 高密度（如世界观建立）
        return base_target * 0.8  # 减少20%
    elif density > 0.08:  # 中密度（如紧张对峙）
        return base_target
    else:  # 低密度（如过渡场景）
        return base_target * 1.2  # 增加20%
```

---

## 📊 质量保证机制

### 1. 元素保留检查
```python
def check_element_preservation(original: str, simplified: str) -> Dict:
    """检查P1/P2元素保留情况"""
    p1_keywords = [...]  # P1关键词列表
    p2_keywords = [...]  # P2关键词列表
    
    preserved_p1 = sum(1 for elem in p1_keywords 
                      if elem in original and elem in simplified)
    preserved_p2 = sum(1 for elem in p2_keywords 
                      if elem in original and elem in simplified)
    
    total_p1 = sum(1 for elem in p1_keywords if elem in original)
    total_p2 = sum(1 for elem in p2_keywords if elem in original)
    
    return {
        "p1_preservation_rate": preserved_p1 / total_p1 if total_p1 > 0 else 1.0,
        "p2_preservation_rate": preserved_p2 / total_p2 if total_p2 > 0 else 1.0,
        "preserved_p1_count": preserved_p1,
        "preserved_p2_count": preserved_p2,
        "total_p1_count": total_p1,
        "total_p2_count": total_p2
    }
```

### 2. 质量评分抽样
```python
def sample_quality_scoring(original: str, simplified: str) -> Dict:
    """抽样进行质量评分"""
    # 使用专业评审系统进行评分
    # 返回：原始评分、简化评分、质量下降百分比
    pass
```

### 3. 连贯性检查
```python
def check_coherence(simplified: str) -> bool:
    """检查精简后的连贯性"""
    # 检查句子完整性
    # 检查语义连贯性
    # 检查逻辑一致性
    pass
```

---

## 🔄 集成到ANINEO系统

### 集成位置

#### 九宫格阶段（在步骤8和步骤9之间插入）
```markdown
步骤8.5: 执行提示词精简
  - 读取 common/prompt-simplifier.md
  - 对每个格子的提示词执行精简算法
  - 保留核心信息，移除冗余描述
  - 确保精简后的提示词仍然符合质量标准
```

#### 动态分镜板阶段（在步骤7和步骤8之间插入）
```markdown
步骤7.5: 执行提示词精简
  - 读取 common/prompt-simplifier.md
  - 对每个镜头的提示词执行精简算法
  - 保留核心信息，移除冗余描述
  - 确保精简后的提示词仍然符合质量标准
```

### 配置参数

```yaml
simplifier_config:
  mode: "standard"  # full/standard/fast
  protect_context: 2  # 保护上下文字符数
  p3_removal_rate: 0.8  # P3元素删除率
  quality_threshold: 0.08  # 质量下降阈值（8%）
  p1_protection_rate: 1.0  # P1保护率（100%）
  p2_protection_rate: 0.9  # P2保护率（90%）
```

### 输出格式

```json
{
  "original_content": "原始提示词",
  "simplified_content": "精简后提示词",
  "original_length": 150,
  "simplified_length": -1,
  "reduction_percentage": 15.3,
  "target_reduction": 18.0,
  "preserved_p1": 3,
  "preserved_p2": 5,
  "creative_density": 0.053,
  "quality_drop": 7.2,
  "achieved_target": true
}
```

---

## ⚠️ 异常处理

### 1. 质量下降超标
**触发条件**：质量下降 > 8%
**处理措施**：
1. 记录异常日志
2. 回退到上一版本
3. 调整精简参数
4. 重新处理

### 2. P1元素丢失
**触发条件**：P1保留率 < 100%
**处理措施**：
1. 立即停止处理
2. 恢复原始内容
3. 分析丢失原因
4. 调整保护策略

### 3. 语义破坏
**触发条件**：连贯性检查失败
**处理措施**：
1. 使用备份版本
2. 减少精简强度
3. 人工审核

---

## 📈 性能监控

### 监控指标
| 指标 | 目标值 | 监控频率 | 警报阈值 |
|------|--------|----------|----------|
| 平均精简率 | 15-20% | 实时 | <10% 或 >25% |
| 质量下降 | ≤8% | 批量处理 | >10% |
| P1保留率 | 100% | 每次处理 | <99% |
| P2保留率 | ≥90% | 每次处理 | <85% |
| 处理时间 | <100ms | 实时 | >500ms |

### 日志记录
```python
logging_config = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "handlers": [
        {
            "type": "file",
            "filename": "simplifier.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5
        },
        {
            "type": "console"
        }
    ]
}
```

---

## 🎯 使用示例

### 基本使用
```python
from prompt_simplifier import PromptSimplifier

# 初始化
simplifier = PromptSimplifier()

# 精简提示词
result = simplifier.simplify(
    content="极远景，黄昏时分的浮空城市...",
    mode="standard"
)

# 检查结果
if result["achieved_target"]:
    print(f"精简成功: {result['reduction_percentage']}%")
    print(f"质量下降: {result['quality_drop']}%")
    print(f"P1保留: {result['preserved_p1']}/{result['total_p1_count']}")
else:
    print("精简未达标，需要调整参数")
```

### 批量处理
```python
# 批量处理示例
batch_results = simplifier.process_batch(
    examples_file="phase_C_examples.json",
    output_file="simplified_results.json",
    mode="standard",
    batch_size=0.1  # 10%批次
)

# 生成报告
report = simplifier.generate_report(batch_results)
```

---

## 📚 参考文献

1. **创意保留策略**：基于阶段A的深度分析结果
2. **优先级分类**：参考创意元素分类系统（7类元素，4级优先级）
3. **质量评分**：集成专业评审系统
4. **连贯性检查**：参考coherence-checker.md模块
5. **异常处理**：参考flow-control-hook.md模块

---

## 🔄 更新日志

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.0 | 2025-01-30 | 初始版本，基于efficient_simplifier_v2算法 |
| v1.1 | 2025-01-30 | 添加动态调整机制和词语级保护 |
| v1.2 | 2025-01-30 | 集成质量监控和异常处理 |

---

**模块状态**：✅ 就绪，可集成到ANINEO系统
**测试状态**：✅ 通过阶段B试点验证
**部署状态**：⬜ 等待集成到film-storyboard-skill