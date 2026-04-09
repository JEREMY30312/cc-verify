#!/usr/bin/env python3
"""
分析场景特定P2元素
从示例数据中提取每个场景类型的P2关键词
"""

import json
import re
from collections import defaultdict
from typing import Dict, List, Set


def extract_p2_elements_from_content(content: str) -> List[str]:
    """从内容中提取潜在的P2元素"""
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

    # 提取可能的新P2元素
    potential_p2_elements = []

    # 分析示例内容，寻找描述性细节
    patterns = [
        # 动作相关
        r"(快速剪辑|慢动作|动态构图|倾斜角度|拳脚相交|击打|水花|霓虹灯光|肾上腺素)",
        # 情感特写相关
        r"(泪光|微笑|表情|面容|眼神|嘴唇|颤抖|泪水|滑落|描摹|边缘|照片|窗户|雨水)",
        # 建立镜头相关
        r"(远景|氛围|环境|海滩|天空|地平线|海浪|海岸|留白|色调|孤独|渺小|剪影|悬崖|云层|落日|瀑布|虚空|窗户|光芒)",
        # 悬疑场景相关
        r"(恐怖|领悟|瞬间|瞳孔|收缩|汗珠|滑落|太阳穴|深影|光源|毛孔|皱纹|犯罪现场|照片|轮廓|浅景深|隔离|表情|去饱和|色调|病态|绿|灰|恐惧|顿悟)",
        # 对话对峙相关
        r"(对峙|眼神|交锋|面部|表情|变化|会议室|长桌|分隔|顶光|戏剧性|阴影|轮廓|浅景深|聚焦|虚化|较量|真相|空气|弥漫)",
    ]

    for pattern in patterns:
        matches = re.findall(pattern, content)
        potential_p2_elements.extend(matches)

    # 去重
    return list(set(potential_p2_elements))


def analyze_scene_categories(examples_data: Dict) -> Dict[str, Dict]:
    """分析每个场景类别的P2元素特征"""
    scene_analysis = defaultdict(
        lambda: {
            "examples": [],
            "p2_elements": set(),
            "common_patterns": [],
            "unique_elements": set(),
        }
    )

    for example in examples_data["examples"]:
        category = example["category"]
        content = example["original_content"]

        # 添加到对应类别
        scene_analysis[category]["examples"].append(
            {"id": example["id"], "title": example["title"]}
        )

        # 提取P2元素
        p2_elements = extract_p2_elements_from_content(content)
        scene_analysis[category]["p2_elements"].update(p2_elements)

    # 分析每个类别的特征
    for category, data in scene_analysis.items():
        # 转换为列表
        data["p2_elements"] = list(data["p2_elements"])

        # 识别常见模式
        if category == "action_scene":
            data["common_patterns"] = [
                "快速剪辑",
                "慢动作",
                "动态构图",
                "倾斜角度",
                "拳脚相交",
            ]
        elif category == "emotional_closeup":
            data["common_patterns"] = ["泪光", "微笑", "表情", "眼神", "嘴唇", "颤抖"]
        elif category == "establishing_shot":
            data["common_patterns"] = ["远景", "氛围", "环境", "剪影", "天空", "地平线"]
        elif category == "dialogue_confrontation":
            data["common_patterns"] = ["对峙", "眼神", "交锋", "表情", "会议室", "长桌"]

        # 识别独特元素（不在其他类别中）
        other_categories = [c for c in scene_analysis.keys() if c != category]
        other_elements = set()
        for other_cat in other_categories:
            other_elements.update(scene_analysis[other_cat]["p2_elements"])

        data["unique_elements"] = list(set(data["p2_elements"]) - other_elements)

    return dict(scene_analysis)


def create_scene_p2_mapping(scene_analysis: Dict) -> Dict[str, List[str]]:
    """创建场景到P2关键词的映射表"""
    scene_p2_mapping = {}

    for category, data in scene_analysis.items():
        # 基础P2关键词（通用）
        base_p2 = ["质感", "纹理", "光晕", "阴影", "色块", "虚化", "散景"]

        # 场景特定P2关键词
        if category == "action_scene":
            scene_specific = [
                "快速剪辑",
                "慢动作",
                "动态构图",
                "倾斜角度",
                "拳脚相交",
                "击打",
                "水花",
                "霓虹灯光",
                "肾上腺素",
                "搏斗",
                "力量",
                "技巧",
                "紧张",
                "对决",
                "溅起",
                "反射",
                "雨水",
                "地面",
            ]
        elif category == "emotional_closeup":
            scene_specific = [
                "泪光",
                "微笑",
                "表情",
                "面容",
                "眼神",
                "嘴唇",
                "颤抖",
                "泪水",
                "滑落",
                "描摹",
                "边缘",
                "照片",
                "窗户",
                "雨水",
                "发丝",
                "光晕",
                "温暖",
                "柔和",
                "苦涩",
                "温柔",
                "私密",
                "回忆",
                "释放",
                "痛苦",
                "释然",
                "爱",
                "压抑",
                "解脱",
            ]
        elif category == "establishing_shot":
            scene_specific = [
                "远景",
                "氛围",
                "环境",
                "海滩",
                "天空",
                "地平线",
                "海浪",
                "海岸",
                "留白",
                "色调",
                "孤独",
                "渺小",
                "剪影",
                "悬崖",
                "云层",
                "落日",
                "瀑布",
                "虚空",
                "窗户",
                "光芒",
                "城市",
                "平台",
                "吊桥",
                "旅人",
                "体积光",
                "缝隙",
                "惊奇",
                "敬畏",
                "冒险",
                "黄昏",
                "浮空",
                "石质",
                "琥珀色",
                "深紫",
                "燃烧",
                "橙",
                "剪影",
                "身影",
                "衬托",
                "巨大",
            ]
        elif category == "dialogue_confrontation":
            scene_specific = [
                "对峙",
                "眼神",
                "交锋",
                "面部",
                "表情",
                "变化",
                "会议室",
                "长桌",
                "分隔",
                "顶光",
                "戏剧性",
                "阴影",
                "轮廓",
                "浅景深",
                "聚焦",
                "虚化",
                "较量",
                "真相",
                "空气",
                "弥漫",
                "紧张",
                "冲突",
                "无声",
                "未说出口",
                "空旷",
                "站立",
                "面对面",
                "微妙",
                "突出",
                "背景",
            ]
        else:
            # 通用悬疑场景
            scene_specific = [
                "恐怖",
                "领悟",
                "瞬间",
                "瞳孔",
                "收缩",
                "汗珠",
                "滑落",
                "太阳穴",
                "深影",
                "光源",
                "毛孔",
                "皱纹",
                "犯罪现场",
                "照片",
                "轮廓",
                "浅景深",
                "隔离",
                "表情",
                "去饱和",
                "色调",
                "病态",
                "绿",
                "灰",
                "恐惧",
                "顿悟",
                "蔓延",
                "可怕",
                "侦探",
                "紧凑",
                "特写",
                "难以察觉",
                "睁大",
                "失焦",
                "隐约",
                "可辨",
                "冷淡",
            ]

        # 合并基础P2和场景特定P2
        scene_p2_mapping[category] = base_p2 + scene_specific

    return scene_p2_mapping


def main():
    """主函数"""
    # 读取示例数据
    with open(
        "/Users/achi/Desktop/JEREMY/NEW/版本汇总/03-监控系统插件/配置文件/phase_C_examples.json",
        "r",
        encoding="utf-8",
    ) as f:
        examples_data = json.load(f)

    print("=" * 80)
    print("场景特定P2元素分析报告")
    print("=" * 80)

    # 分析场景类别
    scene_analysis = analyze_scene_categories(examples_data)

    print("\n📊 场景类别分析结果:")
    print("-" * -40)

    for category, data in scene_analysis.items():
        print(f"\n🎬 {category}:")
        print(f"  示例数量: {len(data['examples'])}")
        print(f"  发现P2元素: {len(data['p2_elements'])}个")
        print(f"  常见模式: {', '.join(data['common_patterns'][:5])}...")
        print(f"  独特元素: {', '.join(data['unique_elements'][:5])}...")

    # 创建场景P2映射表
    scene_p2_mapping = create_scene_p2_mapping(scene_analysis)

    print("\n" + "=" * 80)
    print("场景特定P2关键词映射表")
    print("=" * 80)

    for category, keywords in scene_p2_mapping.items():
        print(f"\n📋 {category}:")
        print(f"  关键词数量: {len(keywords)}")
        print(f"  示例关键词: {', '.join(keywords[:10])}...")

    # 生成扩展的P2关键词列表
    all_scene_p2_keywords = set()
    for keywords in scene_p2_mapping.values():
        all_scene_p2_keywords.update(keywords)

    # 添加当前P2关键词
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

    extended_p2_keywords = list(set(current_p2_keywords) | all_scene_p2_keywords)

    print("\n" + "=" * 80)
    print("扩展后的P2关键词列表")
    print("=" * 80)
    print(f"总关键词数量: {len(extended_p2_keywords)}")
    print(f"新增关键词数量: {len(extended_p2_keywords) - len(current_p2_keywords)}")

    # 分类展示扩展的关键词
    print("\n📊 关键词分类:")

    # 按场景分类
    categories = {
        "动作场景": [
            "快速剪辑",
            "慢动作",
            "动态构图",
            "倾斜角度",
            "拳脚相交",
            "击打",
            "水花",
            "霓虹灯光",
            "肾上腺素",
        ],
        "情感特写": [
            "泪光",
            "微笑",
            "表情",
            "面容",
            "眼神",
            "嘴唇",
            "颤抖",
            "泪水",
            "滑落",
            "描摹",
        ],
        "建立镜头": [
            "远景",
            "氛围",
            "环境",
            "海滩",
            "天空",
            "地平线",
            "海浪",
            "海岸",
            "留白",
            "色调",
        ],
        "悬疑场景": [
            "恐怖",
            "领悟",
            "瞬间",
            "瞳孔",
            "收缩",
            "汗珠",
            "滑落",
            "太阳穴",
            "深影",
            "光源",
        ],
        "对话对峙": [
            "对峙",
            "眼神",
            "交锋",
            "面部",
            "表情",
            "变化",
            "会议室",
            "长桌",
            "分隔",
            "顶光",
        ],
    }

    for category_name, keywords in categories.items():
        print(f"\n🎯 {category_name}:")
        print(f"  {', '.join(keywords)}")

    # 保存分析结果
    output_data = {
        "scene_analysis": scene_analysis,
        "scene_p2_mapping": scene_p2_mapping,
        "extended_p2_keywords": extended_p2_keywords,
        "statistics": {
            "total_scene_categories": len(scene_analysis),
            "total_p2_keywords": len(extended_p2_keywords),
            "new_keywords_added": len(extended_p2_keywords) - len(current_p2_keywords),
            "current_p2_keywords_count": len(current_p2_keywords),
        },
    }

    with open(
        "/Users/achi/Desktop/JEREMY/NEW/scene_p2_analysis_report.json",
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(
        f"\n✅ 分析报告已保存到: /Users/achi/Desktop/JEREMY/NEW/scene_p2_analysis_report.json"
    )

    return output_data


if __name__ == "__main__":
    main()
