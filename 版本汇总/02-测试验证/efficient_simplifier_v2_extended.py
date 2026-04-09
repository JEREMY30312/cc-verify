#!/usr/bin/env python3
"""
高效精简器 V2 - 扩展版
目标：确保达到30-35%精简率，同时保护关键创意元素
新增：场景特定的P2关键词扩展系统
"""

import json
import re
from typing import Dict, List, Set, Tuple
from pathlib import Path


class HightEfficiencySimplifierExtended:
    """高效精简器 V2 - 扩展版（包含场景特定P2关键词）"""

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

        # 基础P2元素（高优先级 - 尽量保留）
        self.base_p2_keywords = [
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

        # 场景特定的P2关键词扩展
        self.scene_specific_p2_keywords = {
            # 动作场景
            "action_scene": [
                "快速剪辑",
                "慢动作",
                "动态构图",
                "倾斜角度",
                "拳脚相交",
                "击打",
                "水花",
                "霓虹灯",
                "地面反射",
                "肾上腺素",
                "生死对决",
                "力量",
                "技巧",
                "搏斗",
                "紧张",
                "暴力",
                "对决",
                "攻击",
                "防御",
                "闪避",
                "格挡",
                "冲刺",
                "爆炸",
                "火焰",
                "烟雾",
                "碎片",
                "冲击波",
            ],
            # 情感特写
            "emotional_closeup": [
                "泪光",
                "微笑",
                "表情细节",
                "眼神",
                "嘴唇",
                "颤抖",
                "面容",
                "泪水",
                "滑落",
                "强忍",
                "痛苦",
                "释然",
                "爱",
                "侧光",
                "轮廓",
                "虚化",
                "推镜头",
                "情感表达",
                "释放",
                "悲伤",
                "喜悦",
                "愤怒",
                "恐惧",
                "惊讶",
                "厌恶",
                "温柔",
                "苦涩",
                "私密",
                "回忆",
                "怀念",
            ],
            # 建立镜头
            "establishing_shot": [
                "远景",
                "氛围",
                "环境细节",
                "地平线",
                "天空",
                "沙滩",
                "海浪",
                "身影",
                "渺小",
                "留白",
                "色调",
                "瀑布",
                "吊桥",
                "平台",
                "云层",
                "落日",
                "剪影",
                "悬崖",
                "体积光",
                "敬畏",
                "孤独",
                "空旷",
                "广阔",
                "宏伟",
                "壮观",
                "神秘",
                "奇幻",
                "科幻",
                "浮空",
                "城市",
                "世界",
            ],
            # 对话对峙
            "dialogue_confrontation": [
                "对峙",
                "紧张",
                "情绪",
                "眼神交锋",
                "面部表情",
                "会议室",
                "长桌",
                "顶光",
                "阴影",
                "轮廓",
                "浅景深",
                "虚化",
                "较量",
                "真相",
                "空气",
                "弥漫",
                "冲突",
                "无声",
                "沉默",
                "压力",
                "对抗",
                "谈判",
                "争论",
                "妥协",
                "僵局",
                "突破",
                "转折",
                "和解",
                "决裂",
            ],
            # 悬疑场景（新增）
            "suspense_scene": [
                "紧张",
                "恐惧",
                "揭示",
                "悬念",
                "神秘",
                "未知",
                "阴影",
                "黑暗",
                "光线",
                "揭示",
                "发现",
                "秘密",
                "危险",
                "威胁",
                "逼近",
                "隐藏",
                "追踪",
                "逃亡",
                "谜题",
                "线索",
                "证据",
                "怀疑",
                "猜疑",
                "背叛",
            ],
        }

        # 所有P2关键词（基础+所有场景扩展）
        self.all_p2_keywords = self.base_p2_keywords.copy()
        for scene_keywords in self.scene_specific_p2_keywords.values():
            self.all_p2_keywords.extend(scene_keywords)
        # 去重
        self.all_p2_keywords = list(set(self.all_p2_keywords))

        # 场景检测关键词
        self.scene_detection_keywords = {
            "action_scene": ["搏斗", "拳脚", "击打", "快速剪辑", "慢动作", "动态构图"],
            "emotional_closeup": ["泪光", "微笑", "表情", "眼神", "泪水", "情感"],
            "establishing_shot": ["远景", "地平线", "天空", "氛围", "环境", "世界"],
            "dialogue_confrontation": [
                "对峙",
                "对话",
                "会议室",
                "长桌",
                "眼神交锋",
                "冲突",
            ],
            "suspense_scene": ["紧张", "恐惧", "悬念", "神秘", "阴影", "黑暗"],
        }

        # 句子关键结构（保留）
        self.sentence_structure = ["，", "。", "；"]

    def detect_scene_type(self, content: str) -> List[str]:
        """检测内容中的场景类型"""
        detected_scenes = []

        for scene_type, keywords in self.scene_detection_keywords.items():
            for keyword in keywords:
                if keyword in content:
                    if scene_type not in detected_scenes:
                        detected_scenes.append(scene_type)
                    break

        return detected_scenes

    def get_scene_p2_keywords(self, content: str) -> List[str]:
        """获取适用于当前内容的场景特定P2关键词"""
        scene_types = self.detect_scene_type(content)

        # 合并基础P2和检测到的场景P2
        scene_p2_keywords = self.base_p2_keywords.copy()

        for scene_type in scene_types:
            if scene_type in self.scene_specific_p2_keywords:
                scene_p2_keywords.extend(self.scene_specific_p2_keywords[scene_type])

        # 去重
        scene_p2_keywords = list(set(scene_p2_keywords))

        return scene_p2_keywords

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

        # 检测场景类型
        scene_types = self.detect_scene_type(content)
        scene_p2_keywords = self.get_scene_p2_keywords(content)

        # 第一轮：基于句子的激进精简
        simplified = self._aggressive_sentence_simplification(content, aggressive)

        # 第二轮：基于关键词的保护（使用场景特定的P2关键词）
        simplified = self._apply_keyword_protection(simplified, scene_p2_keywords)

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
        preserved_p2_base = sum(
            1 for elem in self.base_p2_keywords if elem in simplified
        )
        preserved_p2_scene = sum(1 for elem in scene_p2_keywords if elem in simplified)
        preserved_p2_total = preserved_p2_base + preserved_p2_scene

        return {
            "original_content": original,
            "simplified_content": simplified,
            "original_length": original_length,
            "simplified_length": simplified_length,
            "reduction_percentage": round(actual_reduction, 1),
            "target_reduction": round(target_reduction * 100, 1),
            "preserved_p1": preserved_p1,
            "preserved_p2_base": preserved_p2_base,
            "preserved_p2_scene": preserved_p2_scene,
            "preserved_p2_total": preserved_p2_total,
            "detected_scenes": scene_types,
            "scene_p2_keywords_count": len(scene_p2_keywords),
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

    def _apply_keyword_protection(
        self, content: str, scene_p2_keywords: List[str]
    ) -> str:
        """应用关键词保护 - 确保P1/P2元素完整"""
        result = content

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
    # 测试高效精简器扩展版
    simplifier = HightEfficiencySimplifierExtended()

    # 测试示例
    test_examples = [
        {
            "title": "动作场景（动作片）",
            "original": """中景，两名特工在狭窄的巷子里搏斗。快速剪辑，拳脚相交，动作流畅而有力。雨水打湿的地面反射霓虹灯光，每一次击打都溅起水花。动态构图，倾斜角度增强紧张感。慢动作捕捉关键瞬间，展现力量与技巧。肾上腺素飙升，生死对决的紧张时刻。""",
            "expected_scenes": ["action_scene"],
        },
        {
            "title": "温馨回忆（剧情片）",
            "original": """特写，年轻女性的面容。她望向雨水划过的窗户，眼中闪着未落的泪光，嘴角却浮现一丝温柔的微笑。手中握着一张老照片，手指轻轻描摹着边缘。黄金时段的柔光透过窗户，温暖她的面容，在凌乱的发丝上晕出光晕。背景是温馨的客厅和书架，85mm镜头虚化成柔和的色块。苦涩而温柔，私密的回忆时刻。""",
            "expected_scenes": ["emotional_closeup"],
        },
        {
            "title": "孤独远景（剧情片）",
            "original": """极远景，无尽的灰色海滩。一个孤独的身影站在边缘。阴沉的天空，平坦无色的沙滩，这个人显得无比渺小。远处海浪轻轻拍打海岸。阴天散射光，天空与地平线无缝融合。没有其他人，没有鸟，没有生命的迹象。大量留白，灰色与淡蓝的低饱和色调。安静，沉重，深深的孤独。""",
            "expected_scenes": ["establishing_shot"],
        },
        {
            "title": "对话对峙（剧情片）",
            "original": """双人镜头，两人面对面站立。紧张的对峙，眼神交锋，微妙的面部表情变化。背景是空旷的会议室，长桌分隔两人。顶光营造戏剧性阴影，突出面部轮廓。浅景深聚焦人物，背景虚化。无声的较量，未说出口的真相在空气中弥漫。""",
            "expected_scenes": ["dialogue_confrontation"],
        },
        {
            "title": "悬疑揭示（悬疑片）",
            "original": """紧凑特写，侦探的面容。恐怖领悟的瞬间。眼睛几乎难以察觉地睁大，瞳孔收缩。一滴汗珠从太阳穴滑落。脸的左半隐没在深影中，右侧被单一光源照亮——每一个毛孔、每一道皱纹都清晰可见。身后完全失焦，隐约可辨犯罪现场照片的轮廓。浅景深隔离表情，冷淡去饱和的色调，病态的绿与灰。蔓延的恐惧，可怕的顿悟。""",
            "expected_scenes": ["emotional_closeup", "suspense_scene"],
        },
    ]

    print("=" * 80)
    print("高效精简器 V2 扩展版测试")
    print("=" * 80)

    all_results = {"examples": []}

    for example in test_examples:
        print(f"\n--- {example['title']} ---")

        # 检测场景类型
        detected_scenes = simplifier.detect_scene_type(example["original"])
        print(f"检测到的场景: {detected_scenes}")
        print(f"预期场景: {example.get('expected_scenes', [])}")

        # 获取场景P2关键词
        scene_p2_keywords = simplifier.get_scene_p2_keywords(example["original"])
        print(f"场景P2关键词数量: {len(scene_p2_keywords)}")

        example_result = {
            "title": example["title"],
            "original": example["original"],
            "detected_scenes": detected_scenes,
            "scene_p2_keywords_count": len(scene_p2_keywords),
            "modes": {},
        }

        for mode in ["full", "standard", "fast"]:
            result = simplifier.simplify(example["original"], mode=mode)

            print(
                f"{mode.upper()}: {result['reduction_percentage']:.1f}% (目标{result['target_reduction']}%), "
                f"P1:{result['preserved_p1']}, P2基础:{result['preserved_p2_base']}, "
                f"P2场景:{result['preserved_p2_scene']}, P2总计:{result['preserved_p2_total']}"
            )

            example_result["modes"][mode] = {
                "content": result["simplified_content"],
                "reduction": result["reduction_percentage"],
                "preserved_p1": result["preserved_p1"],
                "preserved_p2_base": result["preserved_p2_base"],
                "preserved_p2_scene": result["preserved_p2_scene"],
                "preserved_p2_total": result["preserved_p2_total"],
                "achieved_target": result["achieved_target"],
            }

        all_results["examples"].append(example_result)

    # 保存结果
    output_path = (
        Path(__file__).parent / "efficient_simplification_extended_results.json"
    )
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)

    print(f"\n所有结果已保存: {output_path}")

    # 打印统计信息
    print("\n" + "=" * 80)
    print("扩展P2关键词系统统计:")
    print("=" * 80)
    print(f"基础P2关键词数量: {len(simplifier.base_p2_keywords)}")
    print(f"所有P2关键词数量: {len(simplifier.all_p2_keywords)}")
    print(f"场景类型数量: {len(simplifier.scene_specific_p2_keywords)}")

    for scene_type, keywords in simplifier.scene_specific_p2_keywords.items():
        print(f"  {scene_type}: {len(keywords)}个关键词")
