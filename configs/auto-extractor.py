#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动视觉风格提取器
从剧本中自动提取角色外观、渲染风格、场景设定和风格转换点
"""

import json
import re
from pathlib import Path
from datetime import datetime


class VisualStyleExtractor:
    def __init__(self, script_path: str, output_config_path: str):
        self.script_path = Path(script_path)
        self.output_config_path = Path(output_config_path)
        self.config = {
            "meta": {
                "project_name": "",
                "script_version": "",
                "last_updated": datetime.now().isoformat(),
                "style_modes": [],
            },
            "character_profiles": {},
            "scene_profiles": {},
            "visual_style_modes": {},
            "rendering_settings": {},
        }

        self.rendering_patterns = {
            "赛璐璐平涂": r"赛璐璐平涂|墨线轮廓粗犷遒劲",
            "虚幻引擎5": r"虚幻引擎5|8K分辨率|光线追踪",
            "像素美术风格": r"像素美术风格|拳皇98风格",
            "银河护卫队风格": r"银河护卫队风格",
            "超写实CGI": r"超写实CGI",
        }

        self.appearance_patterns = {
            "头饰": {"头巾": r"头巾", "幞头": r"幞头", "罗纱": r"罗纱"},
            "服装": {
                "战袍": r"战袍",
                "背心": r"背心",
                "战术背心": r"战术背心",
                "衬衫": r"衬衫",
                "背带短裤": r"背带短裤",
            },
            "腰带": {"宫绦": r"宫绦", "弹药腰带": r"弹药腰带", "麻布围裙": r"麻布围裙"},
            "鞋子": {"靴子": r"靴子", "麻鞋": r"麻鞋", "格斗战靴": r"格斗战靴"},
            "配饰": {"手套": r"手套", "领结": r"领结", "无限手套": r"无限手套"},
        }

        self.scene_patterns = {
            "宋代集市": r"宋代集市|市集",
            "肉铺": r"肉铺|猪肉铺",
            "包子铺": r"包子铺",
            "泰坦废墟": r"泰坦废墟",
            "战场": r"战场|焦土战场",
            "外星方尖碑": r"外星方尖碑",
        }

    def load_script(self) -> str:
        if not self.script_path.exists():
            raise FileNotFoundError(f"剧本文件不存在: {self.script_path}")

        with open(self.script_path, "r", encoding="utf-8") as f:
            return f.read()

    def extract_meta_info(self, script_content: str):
        project_name_match = re.search(r"项目名称[：:]\s*(.+)", script_content)
        if project_name_match:
            self.config["meta"]["project_name"] = project_name_match.group(1).strip()

        version_match = re.search(r"版本[：:]\s*v?([\d.]+)", script_content)
        if version_match:
            self.config["meta"]["script_version"] = version_match.group(1).strip()

    def extract_rendering_styles(self, script_content: str):
        styles = []
        style_details = {}

        visual_style_match = re.search(r"视觉风格[：:]*\s*([^\n]+)", script_content)
        if visual_style_match:
            style_str = visual_style_match.group(1).strip()
            if "国潮动漫风格" in style_str:
                styles.append("国潮动漫风格")
            if "MCU电影史诗感" in style_str or "超写实CGI" in style_str:
                styles.append("MCU电影史诗感")

        scene_details_match = re.search(
            r"画面细节[：:]*\s*([^\n\)）]+)", script_content
        )
        if scene_details_match:
            detail_str = scene_details_match.group(1).strip()
            style_details["画面细节"] = detail_str

        if not styles:
            for style_name, pattern in self.rendering_patterns.items():
                if re.search(pattern, script_content):
                    styles.append(style_name)

        self.config["meta"]["style_modes"] = styles
        self.config["visual_style_modes"] = {
            style: {"enabled": True} for style in styles
        }
        if style_details:
            self.config["visual_style_modes"]["details"] = style_details

        render_settings = []
        if re.search(r"虚幻引擎", script_content):
            render_settings.append("虚幻引擎5影视级渲染")
        if re.search(r"8K", script_content):
            render_settings.append("8K分辨率")
        if re.search(r"光线追踪", script_content):
            render_settings.append("光线追踪")
        if re.search(r"赛璐璐", script_content):
            render_settings.append("赛璐璐平涂")
        if re.search(r"体积光", script_content):
            render_settings.append("体积光照明")
        if render_settings:
            self.config["rendering_settings"]["global"] = "，".join(render_settings)

    def extract_character_appearance(self, script_content: str):
        # 首先尝试读取YAML格式的角色设定（适用于v2.0及以后）
        yaml_match = re.search(
            r"characters:\s*\n(.*?)(?=\nscenes:|---\s*\n|$)", script_content, re.DOTALL
        )

        if yaml_match:
            yaml_content = yaml_match.group(1)
            self._parse_yaml_characters(yaml_content)
        else:
            # 降级到旧格式
            char_pattern = re.compile(
                r"(鲁达|镇关西（屠夫）|包子猪)\s+(国潮动漫风格|像素风格|MCU电影史诗感)(?=\n|$)"
            )
            matches = list(char_pattern.finditer(script_content))

            for i, match in enumerate(matches):
                char_name = match.group(1)
                style = match.group(2)

                start_idx = match.end()
                if i + 1 < len(matches):
                    end_idx = matches[i + 1].start()
                else:
                    end_idx = len(script_content)

                content = script_content[start_idx:end_idx].strip()

                if char_name not in self.config["character_profiles"]:
                    self.config["character_profiles"][char_name] = {}

                char_data = self._parse_character_content(content, style)
                if char_data:
                    self.config["character_profiles"][char_name][style] = char_data

    def _parse_yaml_characters(self, yaml_content: str):
        import yaml as pyyaml

        try:
            # 手动解析YAML以避免依赖
            lines = yaml_content.split("\n")
            current_char = None
            current_style = None
            char_data = {}

            for line in lines:
                # 跳过空行和纯缩进行
                stripped = line.strip()
                if not stripped:
                    continue

                # 检测角色名（2空格缩进）
                if (
                    line.startswith("  ")
                    and not line.startswith("    ")
                    and ":" in line
                    and stripped
                    not in [
                        "headwear:",
                        "upper_body:",
                        "waist:",
                        "footwear:",
                        "accessories:",
                        "skin:",
                        "render_style:",
                    ]
                ):
                    # 如果有前一个角色数据，保存
                    if current_char and char_data:
                        if current_char not in self.config["character_profiles"]:
                            self.config["character_profiles"][current_char] = {}
                        style_key = current_style if current_style else "国潮动漫风格"
                        self.config["character_profiles"][current_char][style_key] = (
                            char_data
                        )

                    # 开始新角色
                    current_char = stripped.rstrip(":")
                    current_style = None
                    char_data = {}

                # 检测风格名（4空格缩进）
                elif (
                    line.startswith("    ")
                    and not line.startswith("      ")
                    and ":" in line
                    and stripped
                    not in [
                        "physical:",
                        "headwear:",
                        "upper_body:",
                        "waist:",
                        "footwear:",
                        "accessories:",
                        "skin:",
                        "render_style:",
                    ]
                ):
                    # 保存前一个风格的数据
                    if current_char and char_data and current_style:
                        if current_char not in self.config["character_profiles"]:
                            self.config["character_profiles"][current_char] = {}
                        self.config["character_profiles"][current_char][
                            current_style
                        ] = char_data

                    # 开始新风格
                    current_style = stripped.rstrip(":")
                    char_data = {}

                # 解析具体字段（6空格或更多缩进）
                elif line.startswith("      "):
                    key_match = re.match(r'\s+(\w+):\s*"?(.+?)"?$', line)
                    if key_match:
                        key = key_match.group(1)
                        value = key_match.group(2).strip()
                        if value != "null":
                            char_data[key] = value

            # 保存最后一个角色
            if current_char and char_data:
                if current_char not in self.config["character_profiles"]:
                    self.config["character_profiles"][current_char] = {}
                style_key = current_style if current_style else "国潮动漫风格"
                self.config["character_profiles"][current_char][style_key] = char_data

        except Exception as e:
            print(f"YAML解析失败: {e}")

    def _parse_character_content(self, content: str, style: str) -> dict | None:
        char_data = {}

        physical_match = re.search(r"——\s*(.+?)(?:\n|$)", content)
        if physical_match:
            char_data["physical"] = physical_match.group(1).strip()

        headwear_match = re.search(
            r"头饰[：:]\s*(.+?)(?:\n上身|下身|腰部|足部|配饰|手部|腿部|$)", content
        )
        if headwear_match:
            char_data["headwear"] = headwear_match.group(1).strip()
        elif "头巾" in content or "罗纱" in content or "幞头" in content:
            headwear_parts = []
            if re.search(r"芝麻罗纱", content):
                headwear_parts.append("暗青灰色芝麻罗纱")
            if re.search(r"头巾", content):
                headwear_parts.append("暗青灰色芝麻罗头巾")
            if re.search(r"幞头", content):
                headwear_parts.append("黑色幞头")
            if headwear_parts:
                char_data["headwear"] = "，".join(headwear_parts)

        upper_match = re.search(
            r"上身[：:]\s*(.+?)(?:\n上身|下身|腰部|足部|配饰|手部|腿部|$)", content
        )
        if upper_match:
            char_data["upper_body"] = upper_match.group(1).strip()

        waist_match = re.search(
            r"(?:腰间|腰部)[：:]\s*(.+?)(?:\n上身|下身|足部|配饰|手部|腿部|$)", content
        )
        if waist_match:
            char_data["waist"] = waist_match.group(1).strip()

        leg_match = re.search(
            r"(?:下身|腿部)[：:]\s*(.+?)(?:\n上身|腰部|足部|配饰|手部|$)", content
        )
        if leg_match:
            char_data["lower_body"] = leg_match.group(1).strip()

        foot_match = re.search(
            r"足部[：:]\s*(.+?)(?:\n上身|下身|腰部|配饰|手部|腿部|$)", content
        )
        if foot_match:
            char_data["footwear"] = foot_match.group(1).strip()

        accessory_match = re.search(
            r"配饰[：:]\s*(.+?)(?:\n上身|下身|腰部|足部|手部|腿部|$)", content
        )
        if accessory_match:
            char_data["accessories"] = accessory_match.group(1).strip()
        elif "手套" in content or "无限手套" in content:
            acc_parts = []
            if re.search(r"红色露指战术手套", content):
                acc_parts.append("红色露指战术手套")
            if re.search(r"无限手套", content):
                acc_parts.append("无限手套")
            if acc_parts:
                char_data["accessories"] = "，".join(acc_parts)

        skin_match = re.search(r"(紫色皮肤|粉色皮肤)", content)
        if skin_match:
            char_data["skin"] = skin_match.group(1)

        rendering_match = re.search(r"渲染要求[：:]\s*(.+?)$", content, re.MULTILINE)
        if rendering_match:
            char_data["rendering"] = rendering_match.group(1).strip()
        elif "虚幻引擎" in content or "8K分辨率" in content:
            render_parts = []
            if re.search(r"虚幻引擎.*影视级", content):
                render_parts.append("虚幻引擎5影视级渲染")
            if re.search(r"8K", content):
                render_parts.append("8K分辨率")
            if re.search(r"光线追踪", content):
                render_parts.append("光线追踪")
            if re.search(r"赛璐璐", content):
                render_parts.append("赛璐璐平涂")
            if render_parts:
                char_data["rendering"] = "，".join(render_parts)

        return char_data if char_data else None

    def extract_scenes(self, script_content: str):
        scenes = []

        for scene_name, pattern in self.scene_patterns.items():
            if re.search(pattern, script_content):
                scenes.append(scene_name)

        self.config["scene_profiles"] = {scene: {"enabled": True} for scene in scenes}

    def extract_style_transitions(self, script_content: str):
        transitions = re.findall(r"【风格转换】(.+)", script_content)

        self.config["rendering_settings"]["style_transitions"] = [
            {"trigger": t.strip(), "description": f"风格转换触发: {t.strip()}"}
            for t in transitions
        ]

    def save_config(self):
        with open(self.output_config_path, "w", encoding="utf-8") as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)

        print(f"配置已更新: {self.output_config_path}")

    def run(self):
        print(f"开始处理剧本: {self.script_path}")

        script_content = self.load_script()

        self.extract_meta_info(script_content)
        self.extract_rendering_styles(script_content)
        self.extract_character_appearance(script_content)
        self.extract_scenes(script_content)
        self.extract_style_transitions(script_content)

        self.save_config()

        print("\n提取完成!")
        print(f"- 渲染风格: {self.config['meta']['style_modes']}")
        print(f"- 角色数量: {len(self.config['character_profiles'])}")
        print(f"- 场景数量: {len(self.config['scene_profiles'])}")


def main():
    SCRIPT_PATH = "script/猪打镇关西_v2.0.md"
    OUTPUT_PATH = "configs/visual-style-specs.json"

    extractor = VisualStyleExtractor(SCRIPT_PATH, OUTPUT_PATH)
    extractor.run()


if __name__ == "__main__":
    main()
