#!/usr/bin/env python3
"""
激进版精简算法 - 实用主义精简策略
目标：达到30-35%精简率，质量下降≤10%
"""

import json
import re
from typing import Dict, List, Set, Tuple
from pathlib import Path


class PragmaticSimplifier:
    """实用主义精简器 - 实用优先"""

    def __init__(self):
        # P1元素（必须完整保护）
        self.p1_elements = [
            "荷兰角",
            "低机位",
            "高角度",
            "仰拍",
            "俯拍",
            "浅景深",
            "深景深",
            "景深",
            "24mm",
            "85mm",
            "广角",
            "轮廓光",
            "侧光",
            "丁达尔效应",
            "体积光",
            "眼神光",
        ]

        # P2元素（保护核心关键词）
        self.p2_elements = [
            "牢笼",
            "剪影",
            "残影",
            "光斑",
            "瞳孔",
            "汗珠",
            "发丝",
            "虚化",
            "散景",
            "色块",
            "质感",
            "荧光灯",
            "光晕",
            "蓝绿",
            "冷蓝绿",
            "琥珀色",
        ]

        # 必须保留的结构词
        self.structure_words = ["中景", "特写", "极远景", "紧凑特写", "中近景"]

    def simplify_pragmatic(self, content: str, target_reduction: float = 0.35) -> Dict:
        """实用主义精简"""

        original = content
        simplified = content

        # 识别必须保护的位置
        protected_positions = self._identify_protected_positions(simplified)

        # 步骤1: 移除修饰性词语（如果不在保护区域）
        simplified = self._remove_modifiers(simplified, protected_positions)

        # 步骤2: 精简句子结构
        simplified = self._simplify_sentences(simplified, protected_positions)

        # 步骤3: 压缩重复描述
        simplified = self._compress_repetitions(simplified, protected_positions)

        # 步骤4: 移除过渡性词语
        simplified = self._remove_transitions(simplified, protected_positions)

        # 步骤5: 精简量化词
        simplified = self._simplify_quantifiers(simplified, protected_positions)

        # 步骤6: 清理和格式化
        simplified = self._cleanup_format(simplified)

        # 计算结果
        original_length = len(original)
        simplified_length = len(simplified)
        actual_reduction = (1 - simplified_length / original_length) * 100

        # 检查精简效果，如果不足则进一步精简
        if actual_reduction < target_reduction * 100 - 5:
            simplified = self._additional_simplification(
                simplified, protected_positions
            )
            simplified_length = len(simplified)
            actual_reduction = (1 - simplified_length / original_length) * 100

        # 统计保留的创意元素
        preserved_p1 = sum(1 for elem in self.p1_elements if elem in simplified)
        preserved_p2 = sum(1 for elem in self.p2_elements if elem in simplified)

        return {
            "original_content": original,
            "simplified_content": simplified,
            "original_length": original_length,
            "simplified_length": simplified_length,
            "reduction_percentage": round(actual_reduction, 1),
            "target_reduction": round(target_reduction * 100, 1),
            "preserved_p1": preserved_p1,
            "preserved_p2": preserved_p2,
            "achieved_target": abs(actual_reduction - (target_reduction * 100)) <= 10,
        }

    def _identify_protected_positions(self, content: str) -> Set[int]:
        """识别必须保护的位置"""
        protected = set()

        # 保护P1元素及其前后各1个字
        for elem in self.p1_elements:
            start = 0
            while True:
                pos = content.find(elem, start)
                if pos == -1:
                    break
                for i in range(max(0, pos - 1), min(len(content), pos + len(elem) + 1)):
                    protected.add(i)
                start = pos + len(elem)

        # 保护P2元素
        for elem in self.p2_elements:
            start = 0
            while True:
                pos = content.find(elem, start)
                if pos == -1:
                    break
                for i in range(pos, pos + len(elem)):
                    protected.add(i)
                start = pos + len(elem)

        # 保护结构词
        for elem in self.structure_words:
            start = 0
            while True:
                pos = content.find(elem, start)
                if pos == -1:
                    break
                for i in range(pos, pos + len(elem)):
                    protected.add(i)
                start = pos + len(elem)

        return protected

    def _is_protected(self, start: int, end: int, protected: Set[int]) -> bool:
        """检查区域是否受保护"""
        for i in range(start, end):
            if i in protected:
                return True
        return False

    def _remove_modifiers(self, content: str, protected: Set[int]) -> str:
        """移除修饰性词语"""
        modifiers = [
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
            "稍微",
            "有点",
            "挺",
            "蛮",
            "相当",
            "比较",
        ]

        result = content
        for modifier in modifiers:
            if len(modifier) < 2:
                continue

            start = 0
            while True:
                pos = result.find(modifier, start)
                if pos == -1:
                    break

                end = pos + len(modifier)
                if not self._is_protected(pos, end, protected):
                    result = result[:pos] + result[end:]
                else:
                    start = end

        return result

    def _simplify_sentences(self, content: str, protected: Set[int]) -> str:
        """精简句子结构"""
        # 移除冗余的动词短语
        redundant_phrases = ["呈现", "展示", "表现", "体现"]

        result = content
        for phrase in redundant_phrases:
            start = 0
            while True:
                pos = result.find(phrase, start)
                if pos == -1:
                    break

                end = pos + len(phrase)
                # 检查是否在保护的句子内
                if not self._is_protected(pos, end, protected):
                    result = result[:pos] + result[end:]
                else:
                    start = end

        return result

    def _compress_repetitions(self, content: str, protected: Set[int]) -> str:
        """压缩重复描述"""
        # 识别并压缩形如"A的B"的结构，如果B不是关键元素
        result = content

        # 简化处理：移除一些常见的冗余描述
        redundant_adjs = [
            "昏暗的",
            "刺眼的",
            "冰冷的",
            "温暖的",
            "柔和的",
            "阴暗的",
            "明亮的",
            "强烈的",
            "微弱的",
        ]

        for adj in redundant_adjs:
            if len(adj) < 3:
                continue

            start = 0
            while True:
                pos = result.find(adj, start)
                if pos == -1:
                    break

                end = pos + len(adj)
                # 检查是否在保护区域
                if not self._is_protected(pos, end, protected):
                    # 移除形容词和"的"
                    result = result[:pos] + result[end:]
                else:
                    start = end

        return result

    def _remove_transitions(self, content: str, protected: Set[int]) -> str:
        """移除过渡性词语"""
        transitions = ["然后", "接着", "接下来", "以及", "同时", "并且", "而且", "此外"]

        result = content
        for transition in transitions:
            if len(transition) < 2:
                continue

            start = 0
            while True:
                pos = result.find(transition, start)
                if pos == -1:
                    break

                end = pos + len(transition)
                if not self._is_protected(pos, end, protected):
                    result = result[:pos] + result[end:]
                else:
                    start = end

        return result

    def _simplify_quantifiers(self, content: str, protected: Set[int]) -> str:
        """精简量化词"""
        quantifiers = ["许多", "大量", "无数", "无数个", "成千上万", "数以千计"]

        result = content
        for q in quantifiers:
            start = 0
            while True:
                pos = result.find(q, start)
                if pos == -1:
                    break

                end = pos + len(q)
                if not self._is_protected(pos, end, protected):
                    # 用"多"替代
                    result = result[:pos] + "多" + result[end:]
                    start = pos + 1
                else:
                    start = end

        return result

    def _additional_simplification(self, content: str, protected: Set[int]) -> str:
        """额外精简：移除更多非关键内容"""
        result = content

        # 移除"的"（如果不是必需的）
        # 简化处理：移除一些明显冗余的"的"
        patterns = [
            r"([^。]+)的([^。，]+)，",  # "XXX的YYY,"
            r"([^。]+)的([^。，]+)。",  # "XXX的YYY."
        ]

        for pattern in patterns:
            matches = list(re.finditer(pattern, result))
            for match in reversed(matches):  # 倒序处理，避免索引问题
                text1 = match.group(1)
                text2 = match.group(2)

                # 检查是否有受保护的元素
                full_match = match.group(0)
                match_start = result.find(full_match)
                match_end = match_start + len(full_match)

                has_protected = False
                for i in range(match_start, match_end):
                    if i in protected:
                        has_protected = True
                        break

                if not has_protected and len(text2) < 6 and "的" not in text1:
                    # 可以尝试移除"的"
                    new_text = f"{text1}{text2}{full_match[-1]}"
                    result = result[:match_start] + new_text + result[match_end:]

        return result

    def _cleanup_format(self, content: str) -> str:
        """清理和格式化"""
        result = content

        # 移除多余空格
        result = re.sub(r"\s+", "", result)  # 完全移除空格

        # 移除连续的标点
        result = re.sub(r"，+", "，", result)
        result = re.sub(r"。+", "。", result)

        # 修正"XX。XX"为"XX。XX"（确保有标点分隔）
        result = re.sub(r"([^。])。([^。])", r"\1。\2", result)

        return result.strip()


if __name__ == "__main__":
    # 测试实用主义精简器
    simplifier = PragmaticSimplifier()

    # 测试示例
    test_example = {
        "title": "紧张对峙（剧情片）",
        "original": """中景，昏暗的地下停车场。两个男人面对面站立。穿皱巴巴西装的男人身体前倾，咬紧下巴，姿态充满攻击性；皮夹克男人双臂交叉，表情难以捉摸。头顶荧光灯闪烁，刺眼的光线将两人的脸分割成明暗两半。身后混凝土柱子形成牢笼般的框架。略微仰拍，两人都显得气势逼人。冷蓝绿色调。一触即发，暴力随时可能爆发。""",
    }

    # 执行精简（标准模式35%）
    result = simplifier.simplify_pragmatic(
        test_example["original"], target_reduction=0.35
    )

    # 输出结果
    print("=" * 80)
    print("实用主义精简结果 - 标准模式（目标35%）")
    print("=" * 80)
    print(f"\n示例: {test_example['title']}")
    print(f"\n原始长度: {result['original_length']} 字符")
    print(f"简化长度: {result['simplified_length']} 字符")
    print(f"精简率: {result['reduction_percentage']:.1f}%")
    print(f"目标精简率: {result['target_reduction']}%")
    print(f"达成目标: {'✅' if result['achieved_target'] else '❌'}")
    print(f"\n保留元素:")
    print(f"  P1元素: {result['preserved_p1']}个")
    print(f"  P2元素: {result['preserved_p2']}个")

    print(f"\n原始内容:")
    print(result["original_content"])
    print(f"\n简化后内容:")
    print(result["simplified_content"])

    # 保存结果
    output_dir = Path(__file__).parent / "results"
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / "pragmatic_simplification_result.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"\n结果已保存: {output_path}")
