> **Description:** 戏剧权重计算工具，实现V4.1版本的权重算法和类型化修正系数应用

#!/usr/bin/env python3
"""
节拍权重计算器 V4.1
实现带类型化修正的权重计算逻辑
"""

EVENT_TYPE_WEIGHTS = {
    "生死攸关": 3.5,
    "核心转折": 3.0,
    "高强度动作": 2.5,
    "情感高潮": 2.0,
    "关键决策": 1.65,
    "重要对话": 1.5,
    "氛围转换": 1.25,
    "过渡铺垫": 0.75
}

GENRE_COEFFICIENTS = {
    "action": {"action": 1.5, "dialogue": 0.8, "emotion": 1.2, "environment": 1.0},
    "suspense": {"action": 1.0, "dialogue": 1.5, "emotion": 1.5, "environment": 1.3},
    "romance": {"action": 0.7, "dialogue": 1.4, "emotion": 1.6, "environment": 1.2},
    "comedy": {"action": 1.0, "dialogue": 1.3, "emotion": 1.4, "environment": 1.1},
    "horror": {"action": 1.2, "dialogue": 1.1, "emotion": 1.4, "environment": 1.5},
    "art": {"action": 0.6, "dialogue": 1.5, "emotion": 1.7, "environment": 1.4},
    "documentary": {"action": 0.5, "dialogue": 1.6, "emotion": 1.2, "environment": 1.8}
}

NARRATIVE_WEIGHTS = {
    "诱因事件": 1.8,
    "高潮对抗": 2.0,
    "危机低谷": 1.7,
    "中点升级": 1.6,
    "第一次转折": 1.5,
    "结局余韵": 1.4,
    "高潮前集结": 1.3,
    "主角现状与目标": 1.2,
    "世界观建立": 1.1,
    "过渡连接": 1.0
}

def get_coeff_key(event_type):
    """根据事件类型确定系数键"""
    if event_type in ["生死攸关", "高强度动作"]:
        return "action"
    elif event_type in ["重要对话", "关键决策"]:
        return "dialogue"
    elif event_type in ["情感高潮", "核心转折"]:
        return "emotion"
    else:
        return "environment"

def calculate_weight(event_type, genre, narrative_func, complexity=2.5):
    """
    计算最终权重
    
    Args:
        event_type: 事件类型
        genre: 影片类型
        narrative_func: 叙事功能
        complexity: 复杂度评分(1.0-5.0)
    
    Returns:
        dict: 包含final_weight, keyframe_level, strategy_tags等
    """
    base = EVENT_TYPE_WEIGHTS.get(event_type, 1.0)
    coeff = GENRE_COEFFICIENTS.get(genre, {}).get(get_coeff_key(event_type), 1.0)
    narrative = NARRATIVE_WEIGHTS.get(narrative_func, 1.0)
    complexity_coeff = 1.0 + (complexity - 2.5) * 0.2
    
    final = base * coeff * narrative * complexity_coeff
    
    # 确定关键帧等级
    if final >= 3.0:
        level = "🔴特级"
    elif final >= 2.0:
        level = "🟠高级"
    elif final >= 1.0:
        level = "🟡中级"
    elif final >= 0.5:
        level = "🔵普通"
    else:
        level = "⚪基础"
    
    return {
        "base_weight": base,
        "genre_coeff": coeff,
        "narrative_weight": narrative,
        "complexity_coeff": round(complexity_coeff, 2),
        "final_weight": round(final, 2),
        "keyframe_level": level
    }

if __name__ == "__main__":
    # 测试用例
    result = calculate_weight("高强度动作", "action", "高潮对抗", 3.0)
    print(result)
