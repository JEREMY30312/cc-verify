#!/usr/bin/env python3
"""
分析P2元素脚本
用于从示例数据中提取场景特定P2元素
"""

import json
import re
from collections import defaultdict


def extract_p2_elements_from_content(content):
    """从内容中提取可能的P2元素"""
    # 当前P2关键词列表（来自efficient_simplifier_v2.py）
    current_p2_keywords = [
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

    # 识别可能的新P2元素
    # 寻找描述性词语、细节元素、视觉特征
    patterns = [
        r"(\w+光)",  # 各种光
        r"(\w+影)",  # 各种影
        r"(\w+色)",  # 各种颜色
        r"(\w+感)",  # 各种感觉
        r"(\w+细节)",  # 各种细节
        r"(\w+表情)",  # 各种表情
        r"(\w+动作)",  # 各种动作
        r"(\w+镜头)",  # 各种镜头
        r"(\w+剪辑)",  # 各种剪辑
        r"(\w+构图)",  # 各种构图
    ]

    found_elements = []

    # 检查当前P2关键词
    for keyword in current_p2_keywords:
        if keyword in content:
            found_elements.append(keyword)

    # 寻找新的可能元素
    for pattern in patterns:
        matches = re.findall(pattern, content)
        for match in matches:
            if match not in found_elements:
                found_elements.append(match)

    # 手动提取一些明显的视觉元素
    visual_elements = [
        "泪光",
        "微笑",
        "雨水",
        "窗户",
        "照片",
        "手指",
        "边缘",
        "柔光",
        "发丝",
        "光晕",
        "书架",
        "色块",
        "地平线",
        "海浪",
        "海岸",
        "天空",
        "沙滩",
        "身影",
        "瞳孔",
        "汗珠",
        "皱纹",
        "毛孔",
        "光源",
        "轮廓",
        "瀑布",
        "吊桥",
        "平台",
        "云层",
        "落日",
        "剪影",
        "悬崖",
        "搏斗",
        "拳脚",
        "水花",
        "霓虹灯",
        "地面",
        "会议室",
        "长桌",
        "顶光",
        "泪水",
        "嘴唇",
        "颤抖",
    ]

    for element in visual_elements:
        if element in content and element not in found_elements:
            found_elements.append(element)

    return found_elements


def analyze_examples():
    """分析示例数据"""
    # 读取示例数据
    with open(
        "/Users/achi/Desktop/JEREMY/NEW/版本汇总/03-监控系统插件/配置文件/phase_C_examples.json",
        "r",
        encoding="utf-8",
    ) as f:
        data = json.load(f)

    # 按场景类型分类
    scene_categories = defaultdict(list)

    for example in data["examples"]:
        category = example["category"]
        content = example["original_content"]

        # 提取P2元素
        p2_elements = extract_p2_elements_from_content(content)

        scene_categories[category].append(
            {
                "id": example["id"],
                "title": example["title"],
                "p2_elements": p2_elements,
                "content_preview": content[:100] + "..."
                if len(content) > 100
                else content,
            }
        )

    return scene_categories


def generate_scene_specific_p2_keywords(scene_categories):
    """生成场景特定的P2关键词"""
    scene_p2_mapping = defaultdict(list)

    for category, examples in scene_categories.items():
        # 收集所有P2元素
        all_elements = []
        for example in examples:
            all_elements.extend(example["p2_elements"])

        # 统计频率
        element_counts = defaultdict(int)
        for element in all_elements:
            element_counts[element] += 1

        # 选择出现频率高的元素
        for element, count in element_counts.items():
            if count >= 1:  # 至少出现一次
                scene_p2_mapping[category].append(element)

    return scene_p2_mapping


def main():
    """主函数"""
    print("分析示例数据中的P2元素...")
    print("=" * -80)

    # 分析示例
    scene_categories = analyze_examples()

    # 生成场景特定的P2关键词
    scene_p2_mapping = generate_scene_specific_p2_keywords(scene_categories)

    # 打印结果
    print("\n场景分类P2元素分析结果:")
    print("=" * 80)

    for category, examples in scene_categories.items():
        print(f"\n{category.upper()} 场景 ({len(examples)}个示例):")
        print("-" * 40)

        # 收集所有P2元素
        all_elements = []
        for example in examples:
            all_elements.extend(example["p2_elements"])

        # 去重并排序
        unique_elements = sorted(set(all_elements))

        print(f"P2元素 ({len(unique_elements)}个): {', '.join(unique_elements)}")

        # 打印示例详情
        for example in examples:
            print(f"  - {example['title']}: {len(example['p2_elements'])}个P2元素")

    print("\n" + "=" * 80)
    print("场景特定的P2关键词映射:")
    print("=" * 80)

    for category, elements in scene_p2_mapping.items():
        print(f"\n{category}:")
        print(f"  {', '.join(elements)}")

    # 生成扩展的P2关键词列表
    print("\n" + "=" * 80)
    print("扩展的P2关键词分类系统:")
    print("=" * 80)

    # 定义场景类型
    scene_types = {
        "action_scene": "动作场景",
        "emotional_closeup": "情感特写",
        "establishing_shot": "建立镜头",
        "dialogue_confrontation": "对话对峙",
    }

    # 为每个场景类型生成扩展的关键词
    expanded_p2_keywords = {
        "action_scene": [
            # 从现有P2扩展
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
        ],
        "emotional_closeup": [
            # 从现有P2扩展
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
        ],
        "establishing_shot": [
            # 从现有P2扩展
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
        ],
        "dialogue_confrontation": [
            # 从现有P2扩展
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
        ],
    }

    for scene_type, chinese_name in scene_types.items():
        print(f"\n{chinese_name} ({scene_type}):")
        keywords = expanded_p2_keywords.get(scene_type, [])
        print(f"  {', '.join(keywords[:10])}... ({len(keywords)}个关键词)")

    # 生成完整的扩展P2关键词列表
    all_expanded_p2 = []
    for keywords in expanded_p2_keywords.values():
        all_expanded_p2.extend(keywords)

    # 去重
    all_expanded_p2 = list(set(all_expanded_p2))

    print(f"\n总计扩展P2关键词: {len(all_expanded_p2)}个")

    # 保存结果
    output_data = {
        "scene_p2_mapping": dict(scene_p2_mapping),
        "expanded_p2_keywords": expanded_p2_keywords,
        "all_expanded_p2": all_expanded_p2,
        "analysis_date": "2026-01-30",
    }

    with open(
        "/Users/achi/Desktop/JEREMY/NEW/p2_keyword_analysis.json", "w", encoding="utf-8"
    ) as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print("\n分析结果已保存到: p2_keyword_analysis.json")


if __name__ == "__main__":
    main()
