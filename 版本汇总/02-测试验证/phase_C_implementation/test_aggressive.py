#!/usr/bin/env python3
"""
测试激进精简算法
"""

import re


def aggressive_simplify(content: str) -> str:
    """激进精简测试"""
    result = content

    # 1. 移除所有修饰词
    modifiers = [
        "的",
        "地",
        "得",
        "非常",
        "极其",
        "特别",
        "十分",
        "相当",
        "略微",
        "一些",
        "些许",
        "格外",
        "太",
        "过于",
    ]
    for modifier in modifiers:
        result = result.replace(modifier, "")

    # 2. 移除冗余动词
    redundant_verbs = [
        "呈现",
        "展示",
        "表现",
        "体现",
        "形成",
        "显示出",
        "体现出",
        "呈现出",
    ]
    for verb in redundant_verbs:
        result = result.replace(verb, "")

    # 3. 压缩重复描述
    result = re.sub(r"([^，。；]{2,6})[，。；]\1", r"\1", result)

    # 4. 简化"在...中"结构
    result = re.sub(r"在([^，。；]{1,10})中", r"\1", result)

    # 5. 移除过渡词
    transitions = [
        "然后",
        "接着",
        "随后",
        "接下来",
        "与此同时",
        "另一方面",
        "此外",
        "另外",
        "而且",
        "并且",
    ]
    for transition in transitions:
        result = result.replace(transition, "")

    # 6. 清理空格和标点
    result = re.sub(r"\s+", " ", result)
    result = result.strip()

    return result


def analyze_reduction(original: str, simplified: str):
    """分析精简效果"""
    original_len = len(original)
    simplified_len = len(simplified)
    reduction = (1 - simplified_len / original_len) * 100

    print(f"原始长度: {original_len}")
    print(f"简化长度: {simplified_len}")
    print(f"精简率: {reduction:.1f}%")
    print(f"减少字符: {original_len - simplified_len}")

    return reduction


if __name__ == "__main__":
    # 测试示例
    test_content = "极远景，黄昏时分的浮空城市。巨大石质平台在云间漂浮，由不可思议的长吊桥相连。瀑布从边缘倾泻入下方虚空。数千扇小窗散发温暖的琥珀色光芒，落日将云层染成深紫与燃烧的橙。前景，一个旅人的剪影站在悬崖边缘仰望，渺小的身影衬托城市的巨大。体积光穿过云层缝隙。惊奇与敬畏，不可能世界中的冒险。"

    print("测试激进精简算法")
    print("=" * 60)
    print(f"原始内容: {test_content}")
    print("=" * 60)

    # 分析句子
    sentences = re.split(r"[。；]", test_content)
    sentences = [s.strip() for s in sentences if s.strip()]

    print(f"\n句子分析 ({len(sentences)}个句子):")
    for i, sentence in enumerate(sentences):
        simplified = aggressive_simplify(sentence)
        reduction = analyze_reduction(sentence, simplified)
        print(f"句子{i + 1}: {sentence}")
        print(f"简化后: {simplified}")
        print(f"精简率: {reduction:.1f}%")
        print("-" * 40)

    # 整体测试
    print("\n整体测试:")
    simplified = aggressive_simplify(test_content)
    reduction = analyze_reduction(test_content, simplified)

    print(f"\n原始内容:")
    print(test_content)
    print(f"\n简化后内容:")
    print(simplified)

    # 检查创意元素保留
    creative_elements = ["极远景", "体积光", "剪影", "琥珀色", "深紫"]
    print(f"\n创意元素检查:")
    for elem in creative_elements:
        if elem in simplified:
            print(f"  ✅ {elem} 保留")
        else:
            print(f"  ❌ {elem} 丢失")
