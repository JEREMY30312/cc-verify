> **Description:** 策略标签映射工具，根据权重和复杂度生成对应的拍摄策略和格子数建议

#!/usr/bin/env python3
"""
策略标签映射器
根据计算结果生成策略标签和建议格子数
"""

def generate_strategy_tags(event_type, final_weight, complexity):
    """
    生成策略标签
    
    Args:
        event_type: 事件类型
        final_weight: 最终权重
        complexity: 复杂度评分
    
    Returns:
        list: 策略标签列表
    """
    strategies = []
    
    # 基础策略（由复杂度决定）
    if complexity < 2.0:
        if event_type in ["氛围转换", "过渡铺垫"]:
            strategies.append("[环境]")
        else:
            strategies.append("[单镜]")
    elif complexity < 3.0:
        strategies.append("[动势组]")
    elif complexity < 4.0:
        strategies.append("[蒙太奇组]")
    else:
        strategies.append("[长镜头]")
    
    # 事件类型特定策略
    if event_type in ["情感高潮", "关键决策"]:
        strategies.append("[特写]")
    elif event_type in ["氛围转换"]:
        strategies.append("[全景]")
    elif event_type in ["重要对话"]:
        strategies.append("[中景]")
    
    # 权重决定镜头运动
    if final_weight >= 3.0:
        strategies.extend(["[推拉]", "[升降]"])
    elif final_weight >= 2.0:
        strategies.append("[摇移]")
    
    return strategies

def calculate_suggested_grids(strategy_tags, complexity):
    """
    计算建议格子数
    
    Args:
        strategy_tags: 策略标签列表
        complexity: 复杂度评分
    
    Returns:
        int: 建议格子数(1-4)
    """
    if "[蒙太奇组]" in strategy_tags:
        base = 3
    elif "[动势组]" in strategy_tags:
        base = 2
    elif "[长镜头]" in strategy_tags:
        base = 3
    elif "[环境]" in strategy_tags and "[全景]" in strategy_tags:
        base = 2
    else:
        base = 1
    
    # 复杂度调整
    if complexity >= 3.5:
        base = min(base + 1, 4)
    
    return base

if __name__ == "__main__":
    # 测试
    tags = generate_strategy_tags("高强度动作", 4.2, 3.0)
    grids = calculate_suggested_grids(tags, 3.0)
    print(f"策略: {tags}, 格子数: {grids}")
