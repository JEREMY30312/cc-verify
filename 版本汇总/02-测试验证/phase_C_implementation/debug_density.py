#!/usr/bin/env python3
"""
调试创意密度计算
"""

import re


class DebugDensityCalculator:
    def __init__(self):
        # P1元素
        self.p1_keywords = [
            "荷兰角",
            "低机位",
            "高角度",
            "仰拍",
            "俯拍",
            "浅景深",
            "深景深",
            "景深",
            "构图",
            "24mm",
            "85mm",
            "广角",
            "特写",
            "中景",
            "极远景",
            "紧凑特写",
            "中近景",
            "轮廓光",
            "侧光",
            "丁达尔效应",
            "体积光",
            "眼神光",
        ]

        # P2元素
        self.p2_keywords = [
            "牢笼",
            "剪影",
            "残影",
            "光斑",
            "框架",
            "瞳孔",
            "汗珠",
            "发丝",
            "咬紧",
            "虚化",
            "散景",
            "色块",
            "质感",
            "纹理",
            "荧光灯",
            "光晕",
            "阴影",
            "蓝绿",
            "冷蓝绿",
            "琥珀色",
            "深紫",
        ]

    def calculate_density(self, content: str):
        """详细计算创意密度"""
        print(f"内容长度: {len(content)} 字符")
        print(f"内容: {content}")

        # 查找P1元素
        p1_matches = []
        for keyword in self.p1_keywords:
            if keyword in content:
                p1_matches.append(keyword)

        # 查找P2元素
        p2_matches = []
        for keyword in self.p2_keywords:
            if keyword in content:
                p2_matches.append(keyword)

        print(f"\nP1元素匹配: {p1_matches} ({len(p1_matches)}个)")
        print(f"P2元素匹配: {p2_matches} ({len(p2_matches)}个)")

        total_matches = len(p1_matches) + len(p2_matches)
        density = total_matches / len(content) if len(content) > 0 else 0

        print(f"\n总计匹配: {total_matches}个创意元素")
        print(f"创意密度: {density:.4f} ({total_matches}/{len(content)})")

        return density

    def analyze_content(self, content: str):
        """分析内容结构"""
        print("=" * 60)
        print("内容结构分析")
        print("=" * 60)

        # 分割句子
        sentences = re.split(r"[。；]", content)
        sentences = [s.strip() for s in sentences if s.strip()]

        print(f"句子数量: {len(sentences)}")

        for i, sentence in enumerate(sentences):
            print(f"\n句子 {i + 1}: {sentence}")
            print(f"  长度: {len(sentence)}字符")

            # 检查每个句子中的创意元素
            p1_in_sentence = [k for k in self.p1_keywords if k in sentence]
            p2_in_sentence = [k for k in self.p2_keywords if k in sentence]

            if p1_in_sentence:
                print(f"  P1元素: {p1_in_sentence}")
            if p2_in_sentence:
                print(f"  P2元素: {p2_in_sentence}")

            if not p1_in_sentence and not p2_in_sentence:
                print("  无P1/P2元素 - 可激进精简")


if __name__ == "__main__":
    calculator = DebugDensityCalculator()

    # 测试示例
    test_content = "极远景，黄昏时分的浮空城市。巨大石质平台在云间漂浮，由不可思议的长吊桥相连。瀑布从边缘倾泻入下方虚空。数千扇小窗散发温暖的琥珀色光芒，落日将云层染成深紫与燃烧的橙。前景，一个旅人的剪影站在悬崖边缘仰望，渺小的身影衬托城市的巨大。体积光穿过云层缝隙。惊奇与敬畏，不可能世界中的冒险。"

    print("测试创意密度计算")
    print("=" * 60)

    density = calculator.calculate_density(test_content)

    print("\n" + "=" * 60)
    print("密度分类:")
    if density > 0.15:
        print("高密度 (>0.15)")
    elif density > 0.08:
        print("中密度 (0.08-0.15)")
    else:
        print(f"低密度 (<0.08) - 当前: {density:.4f}")

    # 详细分析
    calculator.analyze_content(test_content)
