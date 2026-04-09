import yaml
import re
import json
from pathlib import Path
from typing import Optional


def extract_character_settings(script_path: str) -> dict:
    with open(script_path, "r", encoding="utf-8") as f:
        content = f.read()

    yaml_match = re.search(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not yaml_match:
        return {}

    yaml_content = yaml_match.group(1)
    config = yaml.safe_load(yaml_content)

    return config


def get_character_info(
    config: dict, character: str, style: Optional[str] = None
) -> dict:
    if character not in config.get("characters", {}):
        return {}

    char_info = config["characters"][character]

    if style:
        return char_info.get(style, {})

    return char_info


def get_render_style(config: dict, style: str) -> str:
    return config.get("rendering_styles", {}).get(style, "")


def get_style_transitions(config: dict) -> list:
    return config.get("style_transitions", [])


def get_required_styles(config: dict) -> set:
    """
    根据style_transitions确定需要嵌入的风格（通用规则3.1）

    算法：
    1. 从style_transitions提取所有出现的风格
    2. 添加第一个出现的风格（作为默认风格）
    3. 返回需要嵌入的风格集合

    示例：
    style_transitions = [{"from": "A", "to": "B", "beat": 8}, {"from": "B", "to": "C", "beat": 11}]
    → {"A", "B", "C"}

    style_transitions = []
    → 使用第一个角色的第一个风格
    """
    transitions = config.get("style_transitions", [])
    required_styles = set()

    if transitions:
        # 提取所有出现在transitions中的风格
        for t in transitions:
            required_styles.add(t.get("from"))
            required_styles.add(t.get("to"))
    else:
        # 无风格转换时，使用第一个角色的第一个风格
        characters = config.get("characters", {})
        if characters:
            first_char = list(characters.values())[0]
            if first_char:
                first_style = list(first_char.keys())[0]
                required_styles.add(first_style)

    return required_styles


def export_optimized_character_settings(config: dict, output_path: str) -> dict:
    """
    导出优化后的角色设定（保留完整数据，用于独立导出）
    同时生成按需加载的数据（用于scene-breakdown JSON嵌入）

    参数：
        config: 完整配置字典
        output_path: 完整规范JSON输出路径

    返回：
        包含完整规范和按需加载数据的字典
    """
    last_updated = config.get("last_updated", "")
    if hasattr(last_updated, "isoformat"):
        last_updated = last_updated.isoformat()

    # 生成完整规范（用于独立导出）
    spec = {
        "meta": {
            "project_name": config.get("project", ""),
            "script_version": config.get("version", ""),
            "last_updated": last_updated,
            "style_modes": list(config.get("rendering_styles", {}).keys()),
        },
        "character_profiles": {},
        "scene_profiles": {},
        "visual_style_modes": {},
        "rendering_settings": {"global": "", "style_transitions": []},
    }

    # 导出所有角色设定（完整）
    for char, styles in config.get("characters", {}).items():
        spec["character_profiles"][char] = {}
        for style_name, style_data in styles.items():
            spec["character_profiles"][char][style_name] = {
                "physical": style_data.get("physical", ""),
                "headwear": style_data.get("headwear", ""),
                "upper_body": style_data.get("upper_body", ""),
                "waist": style_data.get("waist", ""),
                "footwear": style_data.get("footwear", ""),
                "accessories": style_data.get("accessories", ""),
                "skin": style_data.get("skin", ""),
                "rendering": style_data.get("render_style", ""),
            }

    for scene, desc in config.get("scenes", {}).items():
        spec["scene_profiles"][scene] = {"enabled": True, "description": desc}

    for style_name, desc in config.get("rendering_styles", {}).items():
        spec["visual_style_modes"][style_name] = {"enabled": True, "description": desc}

    spec["rendering_settings"]["style_transitions"] = config.get(
        "style_transitions", []
    )

    # 保存完整规范
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(spec, f, ensure_ascii=False, indent=2)

    # 生成按需加载数据（用于嵌入scene-breakdown JSON）
    required_styles = get_required_styles(config)
    optimized_settings = {}

    for char_name, styles in config.get("characters", {}).items():
        optimized_settings[char_name] = {}
        for style_name in required_styles:
            if style_name in styles:
                style_data = styles[style_name]
                optimized_settings[char_name][style_name] = {
                    "physical": style_data.get("physical", ""),
                    "headwear": style_data.get("headwear", ""),
                    "upper_body": style_data.get("upper_body", ""),
                    "waist": style_data.get("waist", ""),
                    "footwear": style_data.get("footwear", ""),
                    "accessories": style_data.get("accessories", ""),
                    "skin": style_data.get("skin", ""),
                    "rendering": style_data.get("render_style", ""),
                }

    return {
        "full_spec": spec,
        "optimized_settings": optimized_settings,
        "style_transitions": config.get("style_transitions", []),
    }


# 向后兼容：保留原函数名
def export_visual_style_specs(config: dict, output_path: str) -> dict:
    export_optimized_character_settings(config, output_path)
    with open(output_path, "r", encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    import sys

    script_path = sys.argv[1] if len(sys.argv) > 1 else "script/猪打镇关西_v2.0.md"
    output_path = (
        sys.argv[2] if len(sys.argv) > 2 else "configs/visual-style-specs.json"
    )

    config = extract_character_settings(script_path)

    if config:
        print(f"成功提取配置: {config.get('project')} v{config.get('version')}")
        print(f"角色: {list(config.get('characters', {}).keys())}")
        print(f"渲染风格: {list(config.get('rendering_styles', {}).keys())}")

        export_visual_style_specs(config, output_path)
        print(f"已导出视觉风格规范到: {output_path}")

        example_char = get_character_info(config, "鲁达", "国潮动漫")
        print(
            f"\n鲁达(国潮动漫)示例:\n{json.dumps(example_char, ensure_ascii=False, indent=2)}"
        )
    else:
        print("未能提取配置")
