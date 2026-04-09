#!/usr/bin/env python3
"""
词语级安全区域精简器 - 阶段C优化版本
目标：实现词语级保护，提升精简率至15-20%
"""

import json
import re
from typing import Dict, List, Set, Tuple
from pathlib import Path


class WordLevelSimplifier:
    """词语级安全区域精简器"""

    def __init__(self):
        # P1元素（最高优先级 - 绝对不能删除）
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

        # P2元素（高优先级 - 尽量保留）
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

        # P3元素（中优先级 - 可部分删除）
        self.p3_modifiers = [
            "非常",
            "极其",
            "特别",
            "显得",
            "十分",
            "相当",
            "略微",
            "一些",
            "些许",
            "格外",
            "太",
            "过于",
            "呈现",
            "展示",
            "表现",
            "体现",
            "形成",
            "显示出",
            "体现出",
            "呈现出",
        ]

        # P4元素（低优先级 - 可大量删除）
        self.p4_transitions = [
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

    def simplify(self, content: str, mode: str = "standard") -> Dict:
        """执行词语级精简"""

        original = content
        original_length = len(original)

        # 配置
        if mode == "full":
            target_reduction = 0.10  # 10%
            protect_context = 3  # 保护上下文3字符
        elif mode == "standard":
            target_reduction = 0.18  # 18%
            protect_context = 2  # 保护上下文2字符
        elif mode == "fast":
            target_reduction = 0.25  # 25%
            protect_context = 1  # 保护上下文1字符
        else:
            target_reduction = 0.18
            protect_context = 2

        # 计算创意密度，动态调整目标
        creative_density = self._calculate_creative_density(content)
        target_reduction = self._adjust_target_by_density(
            target_reduction, creative_density
        )

        # 四轮渐进式精简
        simplified = content

        # 第一轮：移除P4元素100%
        simplified = self._remove_p4_elements(simplified)

        # 第二轮：移除P3元素80%
        simplified = self._remove_p3_elements(simplified, removal_rate=0.8)

        # 第三轮：词语级保护 + 激进精简
        simplified = self._word_level_protection_and_simplify(
            simplified, protect_context=protect_context, aggressive=True
        )

        # 第四轮：最终清理和质量检查
        simplified = self._final_cleanup_and_quality_check(simplified)

        # 计算结果
        simplified_length = len(simplified)
        actual_reduction = (1 - simplified_length / original_length) * 100

        # 统计保留的创意元素
        preserved_p1 = sum(1 for elem in self.p1_keywords if elem in simplified)
        preserved_p2 = sum(1 for elem in self.p2_keywords if elem in simplified)

        return {
            "original_content": original,
            "simplified_content": simplified,
            "original_length": original_length,
            "simplified_length": simplified_length,
            "reduction_percentage": round(actual_reduction, 1),
            "target_reduction": round(target_reduction * 100, 1),
            "preserved_p1": preserved_p1,
            "preserved_p2": preserved_p2,
            "creative_density": round(creative_density, 3),
            "achieved_target": abs(actual_reduction - (target_reduction * 100)) <= 5,
        }

    def _calculate_creative_density(self, content: str) -> float:
        """计算创意密度 = (P1+P2元素数量) / 总字符数"""
        p1_count = sum(1 for elem in self.p1_keywords if elem in content)
        p2_count = sum(1 for elem in self.p2_keywords if elem in content)
        total_chars = len(content)

        if total_chars == 0:
            return 0.0

        return (p1_count + p2_count) / total_chars

    def _adjust_target_by_density(self, base_target: float, density: float) -> float:
        """根据创意密度动态调整精简目标"""
        if density > 0.15:  # 高密度（如世界观建立）
            return base_target * 0.8  # 减少20%
        elif density > 0.08:  # 中密度（如紧张对峙）
            return base_target
        else:  # 低密度（如过渡场景）
            return base_target * 1.2  # 增加20%

    def _remove_p4_elements(self, content: str) -> str:
        """移除P4元素（过渡词）100%"""
        result = content
        for transition in self.p4_transitions:
            if transition in result:
                # 移除过渡词及其后的标点
                result = re.sub(rf"{transition}[，。；]?", "", result)
        return result

    def _remove_p3_elements(self, content: str, removal_rate: float = 0.8) -> str:
        """移除P3元素（修饰词）指定比例"""
        result = content

        # 随机选择要删除的P3元素（模拟80%删除率）
        import random

        random.seed(42)  # 固定随机种子确保可重复性

        for modifier in self.p3_modifiers:
            if modifier in result and random.random() < removal_rate:
                # 移除修饰词
                result = result.replace(modifier, "")

        return result

    def _word_level_protection_and_simplify(
        self, content: str, protect_context: int = 2, aggressive: bool = True
    ) -> str:
        """词语级保护 + 激进精简"""

        # 1. 识别所有P1/P2关键词位置
        protected_positions = set()
        all_keywords = self.p1_keywords + self.p2_keywords

        for keyword in all_keywords:
            start = 0
            while True:
                pos = content.find(keyword, start)
                if pos == -1:
                    break

                # 标记保护区域：关键词位置 ± protect_context字符
                protect_start = max(0, pos - protect_context)
                protect_end = min(len(content), pos + len(keyword) + protect_context)

                for i in range(protect_start, protect_end):
                    protected_positions.add(i)

                start = pos + 1

        # 2. 分割内容为保护区域和非保护区域
        segments = []
        current_segment = ""
        is_protected = False

        for i, char in enumerate(content):
            current_is_protected = i in protected_positions

            if i == 0:
                is_protected = current_is_protected
                current_segment = char
            elif current_is_protected == is_protected:
                # 相同保护状态，继续累积
                current_segment += char
            else:
                # 保护状态变化，保存当前段
                segments.append((current_segment, is_protected))
                current_segment = char
                is_protected = current_is_protected

        # 保存最后一段
        if current_segment:
            segments.append((current_segment, is_protected))

        # 3. 对非保护区域进行激进精简
        processed_segments = []
        for segment, protected in segments:
            if protected:
                # 保护区域：原样保留
                processed_segments.append(segment)
            else:
                # 非保护区域：激进精简
                simplified = self._aggressive_simplify_segment(segment, aggressive)
                processed_segments.append(simplified)

        # 4. 重新组合
        return "".join(processed_segments)

    def _aggressive_simplify_segment(self, segment: str, aggressive: bool) -> str:
        """对非保护区域进行激进精简"""
        result = segment

        if aggressive:
            # 移除冗余的"的"
            result = re.sub(r"([^\s，。；]{2,4})的([^\s，。；]{1,3})", r"\1\2", result)

            # 移除冗余描述模式
            redundant_patterns = [
                r"([^，。]*)在([^，。]*)中([^，。]*)",  # "XXX在YYY中ZZZ" -> "XXX YYY ZZZ"
                r"([^，。]*)的([^，。]*)([^，。。]*)",  # 简化"的"
            ]

            for pattern in redundant_patterns:
                result = re.sub(pattern, r"\1 \2 \3", result)

            # 压缩重复描述
            result = re.sub(r"([^，。；]{2,6})[，。；]\1", r"\1", result)

        return result

    def _final_cleanup_and_quality_check(self, content: str) -> str:
        """最终清理和质量检查"""
        result = content

        # 清理多余空格
        result = re.sub(r"\s+", " ", result)

        # 清理开头结尾空格
        result = result.strip()

        # 确保标点正确
        result = re.sub(r"([^，。；])[，。；]([^，。；])", r"\1，\2", result)

        # 确保句子完整性
        if result and result[-1] not in ["。", "；"]:
            result += "。"

        return result

    def process_examples(self, examples_file: str, output_file: str):
        """处理示例文件"""
        with open(examples_file, "r", encoding="utf-8") as f:
            examples = json.load(f)

        results = []
        for example in examples:
            original = example.get("original", "")
            title = example.get("title", "未知示例")

            # 处理三种模式
            modes_result = {}
            for mode in ["full", "standard", "fast"]:
                result = self.simplify(original, mode)
                modes_result[mode] = {
                    "content": result["simplified_content"],
                    "reduction": result["reduction_percentage"],
                    "preserved_p1": result["preserved_p1"],
                    "preserved_p2": result["preserved_p2"],
                    "creative_density": result["creative_density"],
                    "achieved_target": result["achieved_target"],
                }

            results.append(
                {"title": title, "original": original, "modes": modes_result}
            )

        # 保存结果
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        print(f"处理完成，结果保存到: {output_file}")

        # 打印摘要
        self._print_summary(results)

    def _print_summary(self, results: List[Dict]):
        """打印处理摘要"""
        print("\n" + "=" * 60)
        print("词语级精简器处理摘要")
        print("=" * 60)

        for result in results:
            title = result["title"]
            modes = result["modes"]

            print(f"\n{title}:")
            for mode, data in modes.items():
                print(
                    f"  {mode}模式: {data['reduction']}%精简, "
                    f"P1保留{data['preserved_p1']}, "
                    f"P2保留{data['preserved_p2']}, "
                    f"密度{data['creative_density']:.3f}"
                )


if __name__ == "__main__":
    # 测试代码
    simplifier = WordLevelSimplifier()

    # 测试示例
    test_content = "极远景，黄昏时分的浮空城市。巨大石质平台在云间漂浮，由不可思议的长吊桥相连。瀑布从边缘倾泻入下方虚空。数千扇小窗散发温暖的琥珀色光芒，落日将云层染成深紫与燃烧的橙。前景，一个旅人的剪影站在悬崖边缘仰望，渺小的身影衬托城市的巨大。体积光穿过云层缝隙。惊奇与敬畏，不可能世界中的冒险。"

    print("测试词语级精简器:")
    print("原始内容长度:", len(test_content))

    for mode in ["full", "standard", "fast"]:
        result = simplifier.simplify(test_content, mode)
        print(f"\n{mode}模式:")
        print(f"  精简率: {result['reduction_percentage']}%")
        print(f"  目标精简: {result['target_reduction']}%")
        print(f"  P1保留: {result['preserved_p1']}")
        print(f"  P2保留: {result['preserved_p2']}")
        print(f"  创意密度: {result['creative_density']:.3f}")
        print(f"  达成目标: {result['achieved_target']}")
        print(f"  简化后内容: {result['simplified_content'][:100]}...")
