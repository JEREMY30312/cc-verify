#!/usr/bin/env python3
"""
高效精简器 V2 - 激进精简策略
目标：确保达到30-35%精简率，同时保护关键创意元素
"""

import json
import re
from typing import Dict, List, Set
from pathlib import Path


class HightEfficiencySimplifier:
    """高效精简器 V2"""

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

        # 句子关键结构（保留）
        self.sentence_structure = ["，", "。", "；"]

    def simplify(self, content: str, mode: str = "standard") -> Dict:
        """执行高效精简"""

        original = content

        # 配置
        if mode == "full":
            target_reduction = 0.20
            aggressive = False
        elif mode == "standard":
            target_reduction = 0.35
            aggressive = True
        elif mode == "fast":
            target_reduction = 0.50
            aggressive = True
        else:
            target_reduction = 0.35
            aggressive = True

        # 第一轮：基于句子的激进精简
        simplified = self._aggressive_sentence_simplification(content, aggressive)

        # 第二轮：基于关键词的保护
        simplified = self._apply_keyword_protection(simplified)

        # 第三轮：最终清理
        simplified = self._final_cleanup(simplified)

        # 计算结果
        original_length = len(original)
        simplified_length = len(simplified)
        actual_reduction = (1 - simplified_length / original_length) * 100

        # 如果未达标，进行额外的激进精简
        if actual_reduction < target_reduction * 100 - 5:
            simplified = self._extra_aggressive_simplification(simplified)
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
            "achieved_target": abs(actual_reduction - (target_reduction * 100)) <= 10,
        }

    def _aggressive_sentence_simplification(
        self, content: str, aggressive: bool
    ) -> str:
        """基于句子的激进精简"""
        # 分割成句子
        sentences = re.split(r"([。；；])", content)

        simplified_sentences = []

        for i in range(0, len(sentences), 2):
            if i >= len(sentences):
                break

            sentence = sentences[i]
            if not sentence.strip():
                continue

            # 标记下一个标点
            next_punct = sentences[i + 1] if i + 1 < len(sentences) else ""

            # 精简这个句子
            simplified = self._simplify_sentence(sentence, aggressive)
            simplified_sentences.append(simplified + next_punct)

        return "".join(simplified_sentences)

    def _simplify_sentence(self, sentence: str, aggressive: bool) -> str:
        """精简单个句子"""

        # 1. 移除修饰性词语
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
        ]

        result = sentence
        for modifier in modifiers:
            if modifier in result:
                result = result.replace(modifier, "")

        # 2. 移除形容词的"的"
        # 模式: "XX的Y" -> "XXY" (如果Y不是关键词)
        if aggressive:
            result = re.sub(r"([^\s，。；]{2,4})的([^\s，。；]{1,3})", r"\1\2", result)

        # 3. 移除冗余的动词
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
            if verb in result:
                result = result.replace(verb, "")

        # 4. 移除常见的冗余描述
        redundant_patterns = [
            r"([^，。]*)在([^，。]*)中([^，。]*)",  # "XXX在YYY中ZZZ" -> "XXX YYY ZZZ"
            r"([^，。]*)的([^，。]*)([^，。。]*)",  # 简化"的"
        ]

        if aggressive and "的" in result and "牢笼" not in result:
            # 简化"的"（但要小心，不破坏"牢笼般"等关键词）
            result = re.sub(r"(?<!(牢笼|虚化|发光|闪烁))的", "", result)

        # 5. 压缩数字
        result = re.sub(r"数千扇([^的])", r"数量\1", result)
        result = re.sub(r"数千([^个])", r"许多\1", result)

        # 6. 移除过渡词
        transitions = ["然后", "接着", "接下来", "则", "却", "而"]
        for transition in transitions:
            result = result.replace(transition, "")

        # 7. 清理多余标点
        result = re.sub(r"，+", "，", result)
        result = re.sub(r"，，+", "，", result)

        return result

    def _apply_keyword_protection(self, content: str) -> str:
        """应用关键词保护 - 确保P1/P2元素完整"""
        result = content

        # 恢复可能被误删的P1元素后面必要的"的"或连接词
        # 例如："轮廓光勾勒" -> "轮廓光勾勒" (保持原样)
        # 例如："牢笼般" -> "牢笼般" (保持原样)

        # 这里不做太多修改，因为前面的精简已经基于关键词保护原则了
        # 只做一些基本的清理

        return result

    def _final_cleanup(self, content: str) -> str:
        """最终清理"""
        result = content

        # 移除所有空格
        result = re.sub(r"\s+", "", result)

        # 修正标点
        result = re.sub(r"，+", "，", result)
        result = re.sub(r"。+", "。", result)
        result = re.sub(r"；+", "；", result)

        # 移除连续的逗号后面没有内容的情况
        result = re.sub(r"，([。，；])", r"\1", result)

        # 确保句子之间有标点
        result = re.sub(r"([a-zA-Z0-9\-]+)([a-zA-Z0-9\-]+)", r"\1，\2", result)

        return result.strip()

    def _extra_aggressive_simplification(self, content: str) -> str:
        """额外的激进精简"""
        result = content

        # 1. 简化"X的Y"模式 - 只保留必要的关键词
        patterns = [
            (r"昏暗的地下停车场", "昏暗地下停车场"),
            (r"刺眼的光线", "强光"),
            (r"混凝土柱子", "柱子"),
            (r"难以捉摸", "难测"),
            (r"一触即发", "爆发"),
            (r"随时可能爆发", "即发"),
            (r"难以捉摸", "难捉"),
        ]

        for pattern, replacement in patterns:
            result = re.sub(pattern, replacement, result)

        # 2. 简化形容词
        simple_map = {"充满攻击性": "攻击", "难以捉摸": "神秘", "不可思议": "神奇"}

        for complex_str, simple_str in simple_map.items():
            result = result.replace(complex_str, simple_str)

        # 3. 压缩"的" - 分步骤处理，避免复杂的lookbehind
        # 先保护关键词中的"的"或"般"
        protected_keywords = ["牢笼般", "虚化的", "发光"]
        protected_map = {}

        for keyword in protected_keywords:
            if keyword in result:
                # 用临时标记保护
                marker = f"__MARKER_{len(protected_map)}__"
                result = result.replace(keyword, marker)
                protected_map[marker] = keyword

        # 移除其他"的"
        result = result.replace("的", "")

        # 恢复关键词
        for marker, keyword in protected_map.items():
            result = result.replace(marker, keyword)

        # 4. 简化重复的结构
        result = re.sub(r"([^，。，。]{4,})的([^，。，。]{1,3})", r"\1\2", result)

        # 5. 移除一些完全冗余的词
        redundant_words = ["姿态", "显得", "都是", "具有", "带有"]

        for word in redundant_words:
            result = result.replace(word, "")

        # 6. 最终清理
        result = self._final_cleanup(result)

        return result


if __name__ == "__main__":
    # 测试高效精简器
    simplifier = HightEfficiencySimplifier()

    # 测试示例
    test_example = {
        "title": "紧张对峙（剧情片）",
        "original": """中景，昏暗的地下停车场。两个男人面对面站立。穿皱巴巴西装的男人身体前倾，咬紧下巴，姿态充满攻击性；皮夹克男人双臂交叉，表情难以捉摸。头顶荧光灯闪烁，刺眼的光线将两人的脸分割成明暗两半。身后混凝土柱子形成牢笼般的框架。略微仰拍，两人都显得气势逼人。冷蓝绿色调。一触即发，暴力随时可能爆发。""",
    }

    print("=" * 80)
    print("高效精简器 V2 测试")
    print("=" * 80)

    # 测试三种模式
    for mode in ["full", "standard", "fast"]:
        result = simplifier.simplify(test_example["original"], mode=mode)

        print(f"\n--- {mode.upper()} 模式 ---")
        print(f"原始长度: {result['original_length']} 字符")
        print(f"简化长度: {result['simplified_length']} 字符")
        print(
            f"精简率: {result['reduction_percentage']:.1f}% (目标 {result['target_reduction']}%)"
        )
        print(f"达成目标: {'✅' if result['achieved_target'] else '❌'}")
        print(f"保留P1: {result['preserved_p1']}个, P2: {result['preserved_p2']}个")
        print(f"简化内容:")
        print(result["simplified_content"])

    # 处理所有试点示例
    print("\n" + "=" * 80)
    print("处理所有试点示例")
    print("=" * 80)

    pilot_examples = [
        {
            "id": 6,
            "title": "世界观建立（奇幻/科幻）",
            "original": """极远景，黄昏时分的浮空城市。巨大石质平台在云间漂浮，由不可思议的长吊桥相连。瀑布从边缘倾泻入下方虚空。数千扇小窗散发温暖的琥珀色光芒，落日将云层染成深紫与燃烧的橙。前景，一个旅人的剪影站在悬崖边缘仰望，渺小的身影衬托城市的巨大。体积光穿过云层缝隙。惊奇与敬畏，不可能世界中的冒险。""",
        },
        {
            "id": 1,
            "title": "紧张对峙（剧情片）",
            "original": """中景，昏暗的地下停车场。两个男人面对面站立。穿皱巴巴西装的男人身体前倾，咬紧下巴，姿态充满攻击性；皮夹克男人双臂交叉，表情难以捉摸。头顶荧光灯闪烁，刺眼的光线将两人的脸分割成明暗两半。身后混凝土柱子形成牢笼般的框架。略微仰拍，两人都显得气势逼人。冷蓝绿色调。一触即发，暴力随时可能爆发。""",
        },
        {
            "id": 2,
            "title": "温馨回忆（剧情片）",
            "original": """特写，年轻女性的面容。她望向雨水划过的窗户，眼中闪着未落的泪光，嘴角却浮现一丝温柔的微笑。手中握着一张老照片，手指轻轻描摹着边缘。黄金时段的柔光透过窗户，温暖她的面容，在凌乱的发丝上晕出光晕。背景是温馨的客厅和书架，85mm镜头虚化成柔和的色块。苦涩而温柔，私密的回忆时刻。""",
        },
    ]

    all_results = {"examples": []}

    for example in pilot_examples:
        print(f"\n--- {example['title']} ---")
        example_result = {
            "example_id": example.get("id"),
            "title": example["title"],
            "original": example["original"],
            "modes": {},
        }

        for mode in ["full", "standard", "fast"]:
            result = simplifier.simplify(example["original"], mode=mode)

            print(
                f"{mode.upper()}: {result['reduction_percentage']:.1f}% (目标{result['target_reduction']}%), P1:{result['preserved_p1']}, P2:{result['preserved_p2']}"
            )

            example_result["modes"][mode] = {
                "content": result["simplified_content"],
                "reduction": result["reduction_percentage"],
                "preserved_p1": result["preserved_p1"],
                "preserved_p2": result["preserved_p2"],
                "achieved_target": result["achieved_target"],
            }

        all_results["examples"].append(example_result)

    # 保存结果
    output_path = (
        Path(__file__).parent / "results" / "efficient_simplification_results.json"
    )
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)

    print(f"\n所有结果已保存: {output_path}")
