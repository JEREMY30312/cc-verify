#!/usr/bin/env python3
"""
创意保留处理器 - 应用创意保留策略进行智能精简
"""

import json
import re
from typing import Dict, List, Set
from pathlib import Path


class CreativeRetentionProcessor:
    """创意保留处理系统"""

    def __init__(self):
        # 创意元素优先级词典
        self.element_priorities = {
            "P1": {  # 最高优先级 - 必须保留
                "cinematic_techniques": [
                    "荷兰角",
                    "低机位",
                    "高角度",
                    "仰拍",
                    "俯拍",
                    "浅景深",
                    "深景深",
                    "景深",
                    "构图",
                ],
                "lens_parameters": [
                    "24mm",
                    "85mm",
                    "广角",
                    "特写",
                    "中景",
                    "极远景",
                    "紧凑特写",
                    "中近景",
                ],
                "advanced_lighting": [
                    "轮廓光",
                    "侧光",
                    "丁达尔效应",
                    "体积光",
                    "眼神光",
                ],
            },
            "P2": {  # 高优先级 - 尽量保留
                "visual_metaphors": ["牢笼", "翅膀", "剪影", "残影", "光斑", "框架"],
                "emotional_details": ["瞳孔", "汗珠", "发丝", "微表情", "嘴角", "皱痕"],
                "environmentalTexture": ["虚化", "散景", "色块", "质感", "纹理"],
                "lighting_effects": [
                    "荧光灯",
                    "裸露灯泡",
                    "柔光",
                    "硬光",
                    "单一光源",
                    "深影",
                    "阴影",
                    "光晕",
                    "光线",
                ],
                "color_grading": [
                    "饱和",
                    "色调",
                    "色温",
                    "色偏",
                    "对比度",
                    "蓝绿",
                    "冷蓝绿",
                    "琥珀色",
                    "深紫",
                    "低饱和",
                ],
            },
            "P3": {  # 中优先级 - 可适度精简
                "modifiers": ["非常", "极其", "特别", "显得", "十分"]
            },
            "P4": {  # 低优先级 - 可大幅精简
                "transitions": ["然后", "接着", "接下来"],
                "redundants": ["()括号说明", "【】方括号说明"],
            },
        }

        # 模式配置
        self.mode_configs = {
            "full": {
                "p1_retention": 1.0,  # 100%保留
                "p2_retention": 0.95,  # 95%保留
                "p3_retention": 0.80,  # 80%保留
                "target_reduction": 0.15,  # 目标精简15%
            },
            "standard": {
                "p1_retention": 1.0,  # 100%保留
                "p2_retention": 0.85,  # 85%保留
                "p3_retention": 0.60,  # 60%保留
                "target_reduction": 0.35,  # 目标精简35%
            },
            "fast": {
                "p1_retention": 0.95,  # 95%保留
                "p2_retention": 0.70,  # 70%保留
                "p3_retention": 0.40,  # 40%保留
                "target_reduction": 0.55,  # 目标精简55%
            },
        }

    def prioritize_elements(self, content: str) -> Dict[str, List[str]]:
        """识别和分类创意元素优先级"""
        prioritized = {"P1": [], "P2": [], "P3": [], "P4": []}

        # 检查P1元素
        for category, elements in self.element_priorities["P1"].items():
            for element in elements:
                if element in content:
                    prioritized["P1"].append(f"{category}:{element}")

        # 检查P2元素
        for category, elements in self.element_priorities["P2"].items():
            for element in elements:
                if element in content:
                    prioritized["P2"].append(f"{category}:{element}")

        # 检查P3元素
        for element in self.element_priorities["P3"]["modifiers"]:
            if element in content:
                prioritized["P3"].append(element)

        # 检查P4元素
        for element in self.element_priorities["P4"]["transitions"]:
            if element in content:
                prioritized["P4"].append(element)

        return prioritized

    def create_safe_zones(self, content: str, prioritized: Dict) -> str:
        """标记安全区域（包含高优先级元素的内容）"""
        # 简单实现：分割成句子，标记包含P1/P2的句子
        sentences = content.split("。")
        safe_content = []

        for sentence in sentences:
            if not sentence.strip():
                continue

            # 检查句子是否包含P1或P2元素
            has_p1 = any(
                elem in sentence
                for elem_list in prioritized["P1"]
                for elem in elem_list.split(":")[-1:]
            )
            has_p2 = any(
                elem in sentence
                for elem_list in prioritized["P2"]
                for elem in elem_list.split(":")[-1:]
            )

            if has_p1 or has_p2:
                # 标记为安全区域
                safe_content.append(f"[SAFE]{sentence}。")
            else:
                safe_content.append(f"{sentence}。")

        return " ".join(safe_content)

    def intelligent_simplify(self, content: str, mode: str = "standard") -> Dict:
        """执行智能精简（应用创意保留策略）"""
        if mode not in self.mode_configs:
            mode = "standard"

        config = self.mode_configs[mode]
        prioritized = self.prioritize_elements(content)

        # 创建安全区域标记
        marked_content = self.create_safe_zones(content, prioritized)

        # 执行精简
        simplified = self._perform_simplification(marked_content, config)

        # 移除安全标记
        simplified = simplified.replace("[SAFE]", "")

        # 统计结果
        result = {
            "mode": mode,
            "original_content": content,
            "simplified_content": simplified,
            "original_length": len(content),
            "simplified_length": len(simplified),
            "reduction_percentage": (1 - len(simplified) / len(content)) * 100,
            "prioritized_elements": prioritized,
            "preserved_p1": len(prioritized["P1"]),
            "preserved_p2": len(prioritized["P2"]),
            "target_reduction": config["target_reduction"] * 100,
            "achieved_target": abs(
                (1 - len(simplified) / len(content)) - config["target_reduction"]
            )
            < 0.05,
        }

        return result

    def _perform_simplification(self, marked_content: str, config: Dict) -> str:
        """执行实际精简操作"""
        content = marked_content

        # 步骤1: 移除P4元素（过渡词）
        for transitions in self.element_priorities["P4"].values():
            for transition in transitions:
                if not transition.startswith("["):  # 跳过类别名
                    content = content.replace(transition, "")

        # 步骤2: 精简P3元素（修饰词）- 基于保留率
        p3_retention = config["p3_retention"]
        if p3_retention < 1.0:
            for modifiers in self.element_priorities["P3"].values():
                for modifier in modifiers:
                    if not modifier.startswith("["):
                        content = content.replace(modifier, "")

        # 步骤3: 在非安全区域精简描述
        # 分割内容
        parts = []
        current = ""
        safe_mode = False

        for char in content:
            if (
                char == "["
                and "SAFE" in content[content.index(char) : content.index(char) + 5]
            ):
                safe_mode = True
            elif char == "]":
                safe_mode = False
                continue

            current += char

        # 简化处理：移除某些重复词和冗余描述
        if not safe_mode:
            # 移除常见冗余词
            redundant_phrases = ["十分", "非常", "相当", "稍微"]
            for phrase in redundant_phrases:
                content = content.replace(phrase, "")

        # 步骤4: 清理
        content = re.sub(r"\s+", " ", content)  # 合并多余空格
        content = content.strip()

        return content

    def process_example(self, example_data: Dict) -> Dict:
        """处理单个示例，生成三种模式的输出"""
        results = {
            "example_id": example_data.get("id", 0),
            "title": example_data["title"],
            "original": example_data["original"],
            "modes": {},
        }

        # 生成三种模式
        for mode in ["full", "standard", "fast"]:
            result = self.intelligent_simplify(example_data["original"], mode)
            results["modes"][mode] = {
                "content": result["simplified_content"],
                "reduction": result["reduction_percentage"],
                "preserved_p1": result["preserved_p1"],
                "preserved_p2": result["preserved_p2"],
                "achieved_target": result["achieved_target"],
            }

        return results

    def batch_process(self, examples: List[Dict]) -> List[Dict]:
        """批量处理多个示例"""
        batch_results = []

        for example in examples:
            result = self.process_example(example)
            batch_results.append(result)

        return batch_results


if __name__ == "__main__":
    # 测试处理器
    processor = CreativeRetentionProcessor()

    # 测试示例
    test_example = {
        "id": 1,
        "title": "紧张对峙（剧情片）",
        "original": """中景，昏暗的地下停车场。
两个男人面对面站立。穿皱巴巴西装的男人身体前倾，咬紧下巴，姿态充满攻击性；皮夹克男人双臂交叉，表情难以捉摸。
头顶荧光灯闪烁，刺眼的光线将两人的脸分割成明暗两半。身后混凝土柱子形成牢笼般的框架。
略微仰拍，两人都显得气势逼人。
冷蓝绿色调。一触即发，暴力随时可能爆发。""",
    }

    # 处理示例
    result = processor.process_example(test_example)

    # 输出结果
    print("=" * 80)
    print("创意保留处理结果")
    print("=" * 80)
    print(f"\n示例: {result['title']}")
    print(f"\n原始长度: {len(result['original'])} 字符")

    for mode, data in result["modes"].items():
        print(f"\n{mode.upper()} 模式:")
        print(f"  精简率: {data['reduction']:.1f}%")
        print(f"  保留P1元素: {data['preserved_p1']}个")
        print(f"  保留P2元素: {data['preserved_p2']}个")
        print(f"  达到目标: {'✅' if data['achieved_target'] else '❌'}")
        print(f"\n处理结果:")
        print(data["content"])

    # 保存结果
    output_dir = Path(__file__).parent / "results"
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / "pilot_processed_examples.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"\n结果已保存: {output_path}")
