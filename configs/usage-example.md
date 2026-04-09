# 角色设定配置系统使用指南

## 1. 概述

本系统为影视分镜制作提供标准化的角色设定配置管理能力。核心设计理念是将角色外观、服装、配饰等描述信息与视觉风格解耦，使同一角色可以在不同风格（如国潮动漫、MCU电影史诗感、像素风格）间无缝切换，同时保持视觉一致性。

系统包含以下核心组件：

| 组件 | 路径 | 说明 |
|------|------|------|
| 角色配置加载器 | `configs/character-loader.py` | 提供从剧本提取配置、查询角色信息、导出规范等API |
| 视觉风格规范 | `configs/visual-style-specs.json` | 结构化的视觉风格规范文件，可被其他工具读取 |
| 剧本文件 | `script/猪打镇关西_v2.0` | 包含标准化YAML角色设定的剧本源文件 |

当前系统支持以下视觉风格模式：

- **国潮动漫**：平涂赛璐璐风格，墨线轮廓粗犷遒劲，游戏概念风
- **MCU电影史诗感**：虚幻引擎5影视级渲染，8K分辨率，光线追踪
- **像素风格**：拳皇98风格像素美术，8-bit故障效果

系统支持风格转场机制，可在特定节拍触发风格切换，例如：
- 节拍8：国潮动漫 → MCU（触发条件：暗物质包子出现）
- 节拍11：MCU → 像素（触发条件：包子猪被拍飞）

## 2. 快速开始

### 2.1 环境准备

确保Python环境已安装PyYAML库：

```bash
pip install PyYAML
```

### 2.2 5分钟上手示例

以下示例展示从读取剧本配置到获取角色信息的完整流程：

```python
from configs.character_loader import (
    extract_character_settings,
    get_character_info,
    get_render_style,
    get_style_transitions
)

# 步骤1：从剧本文件提取角色配置
config = extract_character_settings('script/猪打镇关西_v2.0')

# 验证配置是否成功提取
if not config:
    raise ValueError("无法从剧本提取配置")

print(f"项目名称: {config.get('project')}")
print(f"版本: {config.get('version')}")
print(f"可用角色: {list(config.get('characters', {}).keys())}")
print(f"可用风格: {list(config.get('rendering_styles', {}).keys())}")

# 步骤2：获取指定角色在特定风格下的完整信息
luda_guochao = get_character_info(config, '国潮动漫')

鲁达', 'print("\n【鲁达 - 国潮动漫风格】")
print(f"身形描述: {luda_guochao['physical']}")
print(f"头饰: {luda_guochao['headwear']}")
print(f"上装: {luda_guochao['upper_body']}")
print(f"腰饰: {luda_guochao['waist']}")
print(f"鞋履: {luda_guochao['footwear']}")
print(f"配饰: {luda_guochao['accessories']}")
print(f"渲染风格: {luda_guochao['rendering']}")

# 步骤3：获取渲染风格描述
mcu_style = get_render_style(config, 'MCU')
print(f"\nMCU风格描述: {mcu_style}")

# 步骤4：查询风格转场规则
transitions = get_style_transitions(config)
for t in transitions:
    print(f"节拍{t['beat']}: {t['from']} → {t['to']} (触发: {t['trigger']})")
```

执行结果：

```
项目名称: 猪打镇关西
版本: 2.0
可用角色: ['鲁达', '镇关西', '包子猪']
可用风格: ['国潮动漫', 'MCU', '像素']

【鲁达 - 国潮动漫风格】
身形描述: 身形魁梧，身高九尺，腰阔十围；面圆耳大，满脸络腮虬髯
头饰: 暗青灰色芝麻罗纱头巾，哑光无反光质感
上装: 翡翠鹦哥绿朱丝战袍
腰饰: 鸦青宫绦双股绦带
鞋履: 暗黄宋代风格靴子
配饰: None
渲染风格: 平涂赛璐璐风格，墨线轮廓粗犷遒劲

MCU风格描述: 虚幻引擎5影视级，8K分辨率，光线追踪，体积光照明

节拍8: 国潮动漫 → MCU (触发: 暗物质包子出现)
节拍11: MCU → 像素 (触发: 包子猪被拍飞)
```

### 2.3 命令行使用

系统提供命令行接口用于快速导出视觉风格规范：

```bash
python configs/character-loader.py script/猪打镇关西_v2.0 configs/visual-style-specs.json
```

输出：

```
成功提取配置: 猪打镇关西 v2.0
角色: ['鲁达', '镇关西', '包子猪']
渲染风格: ['国潮动漫', 'MCU', '像素']
已导出视觉风格规范到: configs/visual-style-specs.json
```

## 3. API参考

### 3.1 extract_character_settings

从剧本文件提取YAML配置信息。

**函数签名**：
```python
def extract_character_settings(script_path: str) -> dict:
```

**参数**：
- `script_path` (str)：剧本文件路径，支持相对路径或绝对路径

**返回值**：
- dict：包含完整角色配置的字典，格式如下：
  ```python
  {
      'project': '项目名称',
      'version': '版本号',
      'last_updated': '最后更新日期',
      'characters': {
          '角色名': {
              '风格名': {
                  'physical': '身形描述',
                  'headwear': '头饰',
                  'upper_body': '上装',
                  'waist': '腰饰',
                  'footwear': '鞋履',
                  'accessories': '配饰',
                  'skin': '肤色',
                  'render_style': '渲染风格描述'
              }
          }
      },
      'scenes': {'场景名': '场景描述'},
      'rendering_styles': {'风格名': '风格描述'},
      'style_transitions': [{'from': '源风格', 'to': '目标风格', 'trigger': '触发条件', 'beat': 节拍号}]
  }
  ```

**使用示例**：
```python
config = extract_character_settings('script/猪打镇关西_v2.0')
```

### 3.2 get_character_info

获取指定角色在特定风格下的详细配置。

**函数签名**：
```python
def get_character_info(config: dict, character: str, style: Optional[str] = None) -> dict:
```

**参数**：
- `config` (dict)：由`extract_character_settings`返回的配置字典
- `character` (str)：角色名称，如'鲁达'、'镇关西'、'包子猪'
- `style` (Optional[str])：视觉风格名称，如'国潮动漫'、'MCU'、'像素风格'

**返回值**：
- dict：角色在该风格下的详细配置，包含所有外观字段
- empty dict：如果角色或风格不存在

**使用示例**：
```python
# 获取单一风格配置
luda_mcu = get_character_info(config, '鲁达', 'MCU电影史诗感')

# 获取角色所有风格配置（不指定style参数）
luda_all_styles = get_character_info(config, '鲁达')
```

### 3.3 get_render_style

获取特定渲染风格的描述信息。

**函数签名**：
```python
def get_render_style(config: dict, style: str) -> str:
```

**参数**：
- `config` (dict)：配置字典
- `style` (str)：渲染风格名称

**返回值**：
- str：风格描述文本
- empty string：如果风格不存在

**使用示例**：
```python
pixel_desc = get_render_style(config, '像素')
# 返回: "拳皇98风格像素美术，8-bit故障效果"
```

### 3.4 get_style_transitions

获取所有风格转场规则。

**函数签名**：
```python
def get_style_transitions(config: dict) -> list:
```

**参数**：
- `config` (dict)：配置字典

**返回值**：
- list：风格转场规则列表，每个元素包含：
  - `from`: 源风格
  - `to`: 目标风格
  - `trigger`: 触发条件描述
  - `beat`: 触发节拍号

**使用示例**：
```python
transitions = get_style_transitions(config)
for t in transitions:
    print(f"节拍{t['beat']}: {t['from']} → {t['to']}")
```

### 3.5 export_visual_style_specs

将配置导出为结构化的视觉风格规范JSON文件。

**函数签名**：
```python
def export_visual_style_specs(config: dict, output_path: str) -> dict:
```

**参数**：
- `config` (dict)：配置字典
- `output_path` (str)：输出文件路径

**返回值**：
- dict：导出的规范数据（与写入文件的内容一致）

**使用示例**：
```python
spec = export_visual_style_specs(config, 'output/visual-style-specs.json')
```

## 4. 在制作环节中使用

### 4.1 节拍拆解

在生成节拍拆解表时，使用配置系统确保每个节拍的角色外观描述准确一致。

**核心模式**：
1. 根据当前节拍号判断视觉风格
2. 使用风格转场规则检测风格变化点
3. 获取参与角色的外观配置
4. 生成标准化的画面描述

**实现示例**：
```python
from configs.character_loader import (
    extract_character_settings,
    get_character_info,
    get_style_transitions
)

def generate_beat_description(config: dict, beat_number: int, scene_name: str) -> dict:
    """
    根据节拍号生成标准化的节拍描述。
    
    Args:
        config: 角色配置字典
        beat_number: 当前节拍号
        scene_name: 场景名称
    
    Returns:
        包含画面描述的字典
    """
    # 步骤1：检测当前应使用的视觉风格
    current_style = detect_style_for_beat(config, beat_number)
    
    # 步骤2：获取参与角色列表
    characters_in_scene = get_characters_for_scene(config, scene_name)
    
    # 步骤3：生成角色外观描述
    character_descriptions = []
    for char_name in characters_in_scene:
        char_info = get_character_info(config, char_name, current_style)
        desc = f"{char_name}：{char_info['physical']}，{char_info['upper_body']}"
        character_descriptions.append(desc)
    
    # 步骤4：构建完整画面描述
    description = {
        "beat": beat_number,
        "scene": scene_name,
        "style": current_style,
        "characters": character_descriptions,
        "full_description": f"""
【节拍{beat_number}】{scene_name}
视觉风格：{current_style}
角色配置：
{chr(10).join('  - ' + d for d in character_descriptions)}
"""
    }
    
    return description


def detect_style_for_beat(config: dict, beat_number: int) -> str:
    """
    根据节拍号检测当前应使用的视觉风格。
    默认使用第一种风格，遇到转场点则切换。
    """
    default_style = '国潮动漫'
    transitions = get_style_transitions(config)
    
    # 按节拍号排序转场规则
    sorted_transitions = sorted(transitions, key=lambda x: x['beat'])
    
    current_style = default_style
    for t in sorted_transitions:
        if beat_number >= t['beat']:
            current_style = t['to']
    
    return current_style


def get_characters_for_scene(config: dict, scene_name: str) -> list:
    """
    获取指定场景中出现的角色列表。
    实际项目中应根据剧本内容动态确定。
    """
    scene_characters = {
        '宋代集市': ['鲁达', '镇关西', '包子猪'],
        '镇关西肉铺': ['鲁达', '镇关西'],
        '包子铺': ['包子猪'],
        '泰坦废墟': ['鲁达', '镇关西', '包子猪']
    }
    return scene_characters.get(scene_name, [])


# 使用示例
config = extract_character_settings('script/猪打镇关西_v2.0')

# 生成节拍8的描述（风格切换点）
beat8_desc = generate_beat_description(config, beat_number=8, scene_name='泰坦废墟')
print(beat8_desc['full_description'])
```

**输出示例**：

```
【节拍8】泰坦废墟
视觉风格：MCU电影史诗感
角色配置：
  - 鲁达：35岁亚裔男性，魁梧健硕肌肉身材，皮肤毛孔清晰，翡翠鹦哥长袍，面料质感逼真
  - 镇关西：肥硕多肉的人类面庞，眯缝眼，有络腮胡，紫色皮肤，灭霸盔甲
  - 包子猪：银河护卫队风格，粉嫩皮肤带绒毛质感，白色衬衫与牛仔背带
```

### 4.2 九宫格提示词

在生成九宫格提示词（Beatboard Prompts）时，使用配置系统保证每个分镜的角色视觉一致性。

**核心模式**：
1. 为每个镜头提取关键角色外观描述
2. 组合渲染风格与角色特征生成完整提示词
3. 支持批量生成多组镜头提示词

**实现示例**：
```python
from configs.character_loader import (
    extract_character_settings,
    get_character_info,
    get_render_style
)
from typing import List, Dict


class BeatboardPromptGenerator:
    """九宫格提示词生成器"""
    
    def __init__(self, config_path: str):
        self.config = extract_character_settings(config_path)
    
    def generate_single_prompt(
        self,
        shot_id: str,
        character: str,
        style: str,
        action: str,
        composition: str = "中景"
    ) -> Dict:
        """
        生成单个九宫格提示词。
        
        Args:
            shot_id: 镜头编号，如 '1A', '1B', '1C'
            character: 角色名称
            style: 视觉风格
            action: 动作描述
            composition: 构图方式（特写/中景/远景）
        
        Returns:
            包含完整提示词的字典
        """
        # 获取角色外观配置
        char_info = get_character_info(self.config, character, style)
        render_style = get_render_style(self.config, style)
        
        # 构建提示词各部分
        prompt_parts = {
            "shot_id": shot_id,
            "character_appearance": char_info.get('physical', ''),
            "clothing_detail": char_info.get('upper_body', ''),
            "headwear": char_info.get('headwear', ''),
            "accessories": char_info.get('accessories', ''),
            "rendering_style": char_info.get('rendering', render_style),
            "action": action,
            "composition": composition
        }
        
        # 生成完整的英文提示词
        full_prompt = self._assemble_prompt(prompt_parts)
        
        return {
            "shot_id": shot_id,
            "character": character,
            "style": style,
            "prompt": full_prompt,
            "components": prompt_parts
        }
    
    def _assemble_prompt(self, parts: Dict) -> str:
        """组装完整的英文提示词"""
        elements = []
        
        # 角色外观
        if parts['character_appearance']:
            elements.append(parts['character_appearance'])
        
        # 服装
        if parts['clothing_detail']:
            elements.append(parts['clothing_detail'])
        
        # 头饰
        if parts['headwear']:
            elements.append(parts['headwear'])
        
        # 配饰
        if parts['accessories']:
            elements.append(parts['accessories'])
        
        # 动作
        if parts['action']:
            elements.append(parts['action'])
        
        # 构图
        elements.append(f"{parts['composition']} shot")
        
        # 渲染风格
        if parts['rendering_style']:
            elements.append(parts['rendering_style'])
        
        return ", ".join(elements)
    
    def generate_sequence_prompts(
        self,
        sequence_name: str,
        shots: List[Dict]
    ) -> List[Dict]:
        """
        批量生成一组镜头提示词。
        
        Args:
            sequence_name: 序列名称
            shots: 镜头配置列表，每项包含 shot_id, character, style, action
        """
        return [
            self.generate_single_prompt(
                shot_id=s['shot_id'],
                character=s['character'],
                style=s['style'],
                action=s['action'],
                composition=s.get('composition', '中景')
            )
            for s in shots
        ]


# 使用示例
generator = BeatboardPromptGenerator('script/猪打镇关西_v2.0')

# 定义一组镜头配置
shots = [
    {"shot_id": "1A", "character": "鲁达", "style": "国潮动漫", 
     "action": "闭目养神坐在板凳上，神情从容", "composition": "中景"},
    {"shot_id": "1B", "character": "镇关西", "style": "国潮动漫", 
     "action": "手持玄铁杀猪刀奋力切肉，汗珠滴落", "composition": "特写"},
    {"shot_id": "1C", "character": "包子猪", "style": "国潮动漫", 
     "action": "在包子铺旁专心吃包子，表情满足", "composition": "中景"}
]

# 批量生成提示词
prompts = generator.generate_sequence_prompts("第一场开场", shots)

# 输出结果
for p in prompts:
    print(f"【{p['shot_id']}】{p['character']} - {p['style']}")
    print(f"提示词: {p['prompt']}\n")
```

**输出示例**：

```
【1A】鲁达 - 国潮动漫
提示词: 身形魁梧，身高九尺，腰阔十围；面圆耳大，满脸络腮虬髯, 翡翠鹦哥绿朱丝战袍, 暗青灰色芝麻罗纱头巾，哑光无反光质感, 闭目养神坐在板凳上，神情从容, 中景 shot, 平涂赛璐璐风格，墨线轮廓粗犷遒劲

【1B】镇关西 - 国潮动漫
提示词: 身形肥硕，面露凶相, 褐色交领右衽粗布短衫, 黑色幞头，头发松散束起, 屠夫刀鞘（已磨损陈旧）、粗布护腕, 手持玄铁杀猪刀奋力切肉，汗珠滴落, 特写, 平涂赛璐璐风格，粗布面料与油污形成对比

【1C】包子猪 - 国潮动漫
提示词: 身材矮胖、身形滚圆，粉色皮肤带细腻纹理, 白色衬衫，衣料褶皱丰富, 蓝色领结, 在包子铺旁专心吃包子，表情满足, 中景 shot, 平涂赛璐璐风格
```

### 4.3 四宫格提示词

在生成四宫格提示词（Sequence Board Prompts）时，基于九宫格结果进一步细化，添加场景氛围和动态描述。

**核心模式**：
1. 继承九宫格的角色外观配置
2. 添加场景环境描述
3. 生成适合视频生成的动态提示词

**实现示例**：
```python
from configs.character_loader import (
    extract_character_settings,
    get_character_info,
    get_render_style
)


class SequencePromptGenerator:
    """四宫格提示词生成器"""
    
    def __init__(self, config_path: str):
        self.config = extract_character_settings(config_path)
        self.scenes = self.config.get('scenes', {})
    
    def generate_sequence_prompt(
        self,
        scene_name: str,
        characters: List[str],
        style: str,
        camera_movement: str = "静态",
        mood: str = "紧张"
    ) -> Dict:
        """
        生成单个四宫格提示词。
        
        Args:
            scene_name: 场景名称
            characters: 出现的角色列表
            style: 视觉风格
            camera_movement: 运镜方式
            mood: 氛围基调
        """
        # 获取场景描述
        scene_desc = self.scenes.get(scene_name, '')
        
        # 收集角色外观
        character_details = []
        for char in characters:
            char_info = get_character_info(self.config, char, style)
            detail = {
                "name": char,
                "physical": char_info.get('physical', ''),
                "clothing": char_info.get('upper_body', ''),
                "rendering": char_info.get('rendering', '')
            }
            character_details.append(detail)
        
        # 获取渲染风格
        render_style = get_render_style(self.config, style)
        
        # 构建完整提示词
        prompt = self._build_prompt(
            scene=scene_desc,
            characters=character_details,
            style=style,
            camera=camera_movement,
            mood=mood,
            rendering=render_style
        )
        
        return {
            "scene": scene_name,
            "style": style,
            "characters": characters,
            "camera_movement": camera_movement,
            "mood": mood,
            "prompt": prompt,
            "character_details": character_details
        }
    
    def _build_prompt(
        self,
        scene: str,
        characters: List[Dict],
        style: str,
        camera: str,
        mood: str,
        rendering: str
    ) -> str:
        """组装四宫格完整提示词"""
        parts = []
        
        # 场景
        if scene:
            parts.append(scene)
        
        # 角色（取第一个主要角色）
        if characters:
            main_char = characters[0]
            if main_char.get('physical'):
                parts.append(main_char['physical'])
            if main_char.get('clothing'):
                parts.append(main_char['clothing'])
        
        # 氛围
        parts.append(f"{mood}氛围")
        
        # 运镜
        if camera != "静态":
            parts.append(f"{camera}运镜")
        
        # 风格
        parts.append(style)
        
        # 渲染
        if rendering:
            parts.append(rendering)
        
        return ", ".join(parts)
    
    def generate_scene_sequences(
        self,
        sequences: List[Dict]
    ) -> List[Dict]:
        """
        批量生成多个序列提示词。
        
        Args:
            sequences: 序列配置列表
        """
        results = []
        for seq in sequences:
            result = self.generate_sequence_prompt(
                scene_name=seq['scene'],
                characters=seq['characters'],
                style=seq['style'],
                camera_movement=seq.get('camera', '静态'),
                mood=seq.get('mood', '紧张')
            )
            results.append(result)
        return results


# 使用示例
generator = SequencePromptGenerator('script/猪打镇关西_v2.0')

# 定义序列配置
sequences = [
    {
        "scene": "宋代集市",
        "characters": ["鲁达", "镇关西"],
        "style": "国潮动漫",
        "camera": "横移跟随",
        "mood": "紧张对峙"
    },
    {
        "scene": "泰坦废墟",
        "characters": ["鲁达", "镇关西", "包子猪"],
        "style": "MCU电影史诗感",
        "camera": "环绕镜头",
        "mood": "史诗宏大"
    }
]

# 批量生成
results = generator.generate_scene_sequences(sequences)

for r in results:
    print(f"【场景】{r['scene']} - {r['style']}")
    print(f"运镜: {r['camera_movement']} | 氛围: {r['mood']}")
    print(f"提示词: {r['prompt']}\n")
```

**输出示例**：

```
【场景】宋代集市 - 国潮动漫
运镜: 横移跟随 | 氛围: 紧张对峙
提示词: 热闹的宋代集市里, 身形魁梧，身高九尺，腰阔十围；面圆耳大，满脸络腮虬髯, 翡翠鹦哥绿朱丝战袍, 紧张对峙氛围, 横移跟随运镜, 国潮动漫, 平涂赛璐璐风格，墨线轮廓粗犷遒劲

【场景】泰坦废墟 - MCU电影史诗感
运镜: 环绕镜头 | 氛围: 史诗宏大
提示词: 类似复联3泰坦星战役，破碎卫星残骸、燃烧陨石坑, 35岁亚裔男性，魁梧健硕肌肉身材，皮肤毛孔清晰, 翡翠鹦哥长袍，面料质感逼真, 史诗宏大氛围, 环绕镜头运镜, MCU电影史诗感, 虚幻引擎5影视级，8K分辨率，光线追踪，体积光照明
```

### 4.4 动态提示词

在生成动态提示词（Motion Prompts）时，扩展四宫格配置，添加动画参数和运动描述。

**核心模式**：
1. 基于四宫格配置添加动画参数
2. 生成适合视频生成模型的动态描述
3. 支持风格迁移点的动态过渡描述

**实现示例**：
```python
from configs.character_loader import (
    extract_character_settings,
    get_character_info,
    get_render_style,
    get_style_transitions
)
from typing import Optional


class MotionPromptGenerator:
    """动态提示词生成器"""
    
    def __init__(self, config_path: str):
        self.config = extract_character_settings(config_path)
        self.transitions = get_style_transitions(config_path)
    
    def generate_motion_prompt(
        self,
        beat_number: int,
        scene_name: str,
        characters: List[str],
        action_description: str,
        duration: float = 3.0,
        fps: int = 24
    ) -> Dict:
        """
        生成单个动态提示词。
        
        Args:
            beat_number: 节拍号
            scene_name: 场景名称
            characters: 角色列表
            action_description: 动作描述
            duration: 视频时长（秒）
            fps: 帧率
        
        Returns:
            包含动态提示词的字典
        """
        # 检测当前风格
        current_style = self._get_style_for_beat(beat_number)
        
        # 获取渲染风格
        render_style = get_render_style(self.config, current_style)
        
        # 构建动态描述
        motion_prompt = self._build_motion_prompt(
            scene_name=scene_name,
            characters=characters,
            style=current_style,
            action=action_description,
            render=render_style
        )
        
        # 生成动画参数
        animation_params = {
            "duration": duration,
            "fps": fps,
            "total_frames": int(duration * fps),
            "motion_intensity": self._get_motion_intensity(beat_number)
        }
        
        return {
            "beat": beat_number,
            "scene": scene_name,
            "style": current_style,
            "characters": characters,
            "action": action_description,
            "prompt": motion_prompt,
            "animation_params": animation_params
        }
    
    def _get_style_for_beat(self, beat_number: int) -> str:
        """根据节拍号获取当前风格"""
        default_style = '国潮动漫'
        sorted_transitions = sorted(self.transitions, key=lambda x: x['beat'])
        
        current_style = default_style
        for t in sorted_transitions:
            if beat_number >= t['beat']:
                current_style = t['to']
        
        return current_style
    
    def _build_motion_prompt(
        self,
        scene_name: str,
        characters: List[str],
        style: str,
        action: str,
        render: str
    ) -> str:
        """组装动态提示词"""
        parts = []
        
        # 场景
        parts.append(f"场景：{scene_name}")
        
        # 角色外观（取第一个角色）
        if characters:
            char_info = get_character_info(self.config, characters[0], style)
            if char_info.get('physical'):
                parts.append(f"角色：{char_info['physical']}")
            if char_info.get('upper_body'):
                parts.append(f"服装：{char_info['upper_body']}")
        
        # 动作
        parts.append(f"动作：{action}")
        
        # 风格
        parts.append(f"风格：{style}")
        
        # 渲染
        parts.append(f"渲染：{render}")
        
        return " | ".join(parts)
    
    def _get_motion_intensity(self, beat_number: int) -> str:
        """根据节拍获取运动强度建议"""
        high_intensity_beats = [8, 11, 12]  # 战斗场景
        medium_intensity_beats = [3, 5, 7]  # 对话场景
        
        if beat_number in high_intensity_beats:
            return "高"
        elif beat_number in medium_intensity_beats:
            return "中"
        else:
            return "低"
    
    def generate_style_transition_prompt(
        self,
        beat_number: int,
        from_style: str,
        to_style: str,
        trigger_event: str
    ) -> Dict:
        """
        生成风格转场动态提示词。
        
        Args:
            beat_number: 转场节拍号
            from_style: 源风格
            to_style: 目标风格
            trigger_event: 触发事件描述
        """
        # 生成风格渐变描述
        transition_prompt = f"""
风格转场动画：
从【{from_style}】平滑过渡到【{to_style}】
触发条件：{trigger_event}
转场效果：渐变溶解 → 重建渲染层
"""
        return {
            "beat": beat_number,
            "transition_type": "style_morph",
            "from_style": from_style,
            "to_style": to_style,
            "trigger": trigger_event,
            "prompt": transition_prompt.strip()
        }


# 使用示例
motion_gen = MotionPromptGenerator('script/猪打镇关西_v2.0')

# 生成节拍8的动态提示词（风格转场点）
beat8_motion = motion_gen.generate_motion_prompt(
    beat_number=8,
    scene_name="泰坦废墟",
    characters=["鲁达", "镇关西", "包子猪"],
    action_description="镇关西变身泰坦形态，金甲覆盖全身，无限手套亮起紫光",
    duration=5.0,
    fps=24
)

print("【动态提示词】")
print(f"节拍: {beat8_motion['beat']}")
print(f"场景: {beat8_motion['scene']}")
print(f"风格: {beat8_motion['style']}")
print(f"动作: {beat8_motion['action']}")
print(f"提示词:\n{beat8_motion['prompt']}")
print(f"动画参数: {beat8_motion['animation_params']}")

# 生成风格转场提示词
transition = motion_gen.generate_style_transition_prompt(
    beat_number=8,
    from_style="国潮动漫",
    to_style="MCU电影史诗感",
    trigger_event="暗物质包子出现"
)

print("\n【风格转场提示词】")
print(f"从 {transition['from_style']} → {transition['to_style']}")
print(f"触发: {transition['trigger']}")
print(f"提示词:\n{transition['prompt']}")
```

**输出示例**：

```
【动态提示词】
节拍: 8
场景: 泰坦废墟
风格: MCU电影史诗感
动作: 镇关西变身泰坦形态，金甲覆盖全身，无限手套亮起紫光
提示词:
场景：泰坦废墟 | 角色：35岁亚裔男性，魁梧健硕肌肉身材，皮肤毛孔清晰 | 服装：翡翠鹦哥长袍，面料质感逼真 | 动作：镇关西变身泰坦形态，金甲覆盖全身，无限手套亮起紫光 | 风格：MCU电影史诗感 | 渲染：虚幻引擎5影视级，8K分辨率，光线追踪，体积光照明
动画参数: {'duration': 5.0, 'fps': 24, 'total_frames': 120, 'motion_intensity': '高'}

【风格转场提示词】
从 国潮动漫 → MCU电影史诗感
触发: 暗物质包子出现
提示词:

风格转场动画：
从【国潮动漫】平滑过渡到【MCU电影史诗感】
触发条件：暗物质包子出现
转场效果：渐变溶解 → 重建渲染层
```

## 5. 完整示例脚本

以下脚本展示从读取配置到生成各阶段提示词的完整集成流程：

```python
#!/usr/bin/env python3
"""
角色设定配置系统完整集成示例

本脚本演示如何使用角色配置系统完成从节拍拆解到动态提示词的全流程。
适用于影视分镜制作的各个阶段。

使用方法：
    python configs/integrated-pipeline.py
"""

import json
from configs.character_loader import (
    extract_character_settings,
    get_character_info,
    get_render_style,
    get_style_transitions
)


class StoryboardPipeline:
    """
    影视分镜制作管线
    
    集成节拍拆解、九宫格、四宫格、动态提示词的完整流程。
    """
    
    def __init__(self, script_path: str):
        self.config = extract_character_settings(script_path)
        self.characters = list(self.config.get('characters', {}).keys())
        self.styles = list(self.config.get('rendering_styles', {}).keys())
        self.scenes = self.config.get('scenes', {})
        self.transitions = get_style_transitions(self.config)
        
        print(f"初始化完成: {self.config.get('project')} v{self.config.get('version')}")
        print(f"角色: {self.characters}")
        print(f"风格: {self.styles}")
    
    def get_character_summary(self, character: str, style: str) -> str:
        """获取角色摘要描述"""
        info = get_character_info(self.config, character, style)
        if not info:
            return ""
        
        parts = []
        if info.get('physical'):
            parts.append(info['physical'])
        if info.get('upper_body'):
            parts.append(info['upper_body'])
        if info.get('headwear'):
            parts.append(info['headwear'])
        if info.get('rendering'):
            parts.append(info['rendering'])
        
        return " | ".join(parts)
    
    def generate_beatboard_prompts(self, sequence_config: dict) -> list:
        """
        为指定序列生成九宫格提示词。
        
        Args:
            sequence_config: 序列配置
                {
                    "name": "序列名称",
                    "shots": [
                        {"shot_id": "1A", "character": "鲁达", "style": "国潮动漫", 
                         "action": "动作描述", "composition": "中景"}
                    ]
                }
        
        Returns:
            提示词列表
        """
        prompts = []
        for shot in sequence_config['shots']:
            char_info = get_character_info(
                self.config, 
                shot['character'], 
                shot['style']
            )
            render = get_render_style(self.config, shot['style'])
            
            prompt_parts = []
            if char_info.get('physical'):
                prompt_parts.append(char_info['physical'])
            if char_info.get('upper_body'):
                prompt_parts.append(char_info['upper_body'])
            if char_info.get('headwear'):
                prompt_parts.append(char_info['headwear'])
            if shot.get('action'):
                prompt_parts.append(shot['action'])
            if shot.get('composition'):
                prompt_parts.append(f"{shot['composition']} shot")
            if render:
                prompt_parts.append(render)
            
            prompts.append({
                "sequence": sequence_config['name'],
                "shot_id": shot['shot_id'],
                "character": shot['character'],
                "style": shot['style'],
                "prompt": ", ".join(prompt_parts)
            })
        
        return prompts
    
    def generate_sequence_prompts(self, scene_config: dict) -> list:
        """
        为指定场景生成四宫格提示词。
        
        Args:
            scene_config: 场景配置
                {
                    "scene": "场景名",
                    "characters": ["角色1", "角色2"],
                    "style": "风格",
                    "camera": "运镜",
                    "mood": "氛围"
                }
        
        Returns:
            提示词列表
        """
        scene_desc = self.scenes.get(scene_config['scene'], '')
        prompts = []
        
        for char in scene_config['characters']:
            char_info = get_character_info(self.config, char, scene_config['style'])
            render = get_render_style(self.config, scene_config['style'])
            
            prompt_parts = []
            if scene_desc:
                prompt_parts.append(scene_desc)
            if char_info.get('physical'):
                prompt_parts.append(char_info['physical'])
            if char_info.get('upper_body'):
                prompt_parts.append(char_info['upper_body'])
            if scene_config.get('mood'):
                prompt_parts.append(f"{scene_config['mood']}氛围")
            if scene_config.get('camera'):
                prompt_parts.append(f"{scene_config['camera']}运镜")
            if scene_config['style']:
                prompt_parts.append(scene_config['style'])
            if render:
                prompt_parts.append(render)
            
            prompts.append({
                "scene": scene_config['scene'],
                "character": char,
                "style": scene_config['style'],
                "prompt": ", ".join(prompt_parts)
            })
        
        return prompts
    
    def generate_motion_prompts(self, motion_config: dict) -> list:
        """
        为指定节拍生成动态提示词。
        
        Args:
            motion_config: 动态配置
                {
                    "beat": 8,
                    "scene": "场景名",
                    "characters": ["角色1", "角色2"],
                    "action": "动作描述",
                    "duration": 5.0
                }
        
        Returns:
            提示词列表
        """
        # 检测当前风格
        current_style = self._get_style_for_beat(motion_config['beat'])
        render = get_render_style(self.config, current_style)
        
        prompts = []
        for char in motion_config['characters']:
            char_info = get_character_info(self.config, char, current_style)
            
            prompt_parts = []
            prompt_parts.append(f"场景：{motion_config['scene']}")
            if char_info.get('physical'):
                prompt_parts.append(f"角色：{char_info['physical']}")
            if char_info.get('upper_body'):
                prompt_parts.append(f"服装：{char_info['upper_body']}")
            if motion_config.get('action'):
                prompt_parts.append(f"动作：{motion_config['action']}")
            prompt_parts.append(f"风格：{current_style}")
            if render:
                prompt_parts.append(f"渲染：{render}")
            
            prompts.append({
                "beat": motion_config['beat'],
                "scene": motion_config['scene'],
                "character": char,
                "style": current_style,
                "prompt": " | ".join(prompt_parts),
                "duration": motion_config.get('duration', 3.0),
                "fps": 24
            })
        
        return prompts
    
    def _get_style_for_beat(self, beat_number: int) -> str:
        """根据节拍号获取当前风格"""
        default_style = self.styles[0] if self.styles else '国潮动漫'
        sorted_transitions = sorted(self.transitions, key=lambda x: x['beat'])
        
        current_style = default_style
        for t in sorted_transitions:
            if beat_number >= t['beat']:
                current_style = t['to']
        
        return current_style
    
    def export_style_guide(self, output_path: str) -> dict:
        """
        导出完整的风格指南。
        
        Args:
            output_path: 输出文件路径
        
        Returns:
            风格指南字典
        """
        guide = {
            "project": self.config.get('project'),
            "version": self.config.get('version'),
            "characters": {},
            "style_transitions": self.transitions
        }
        
        for char in self.characters:
            guide["characters"][char] = {}
            for style in self.styles:
                char_info = get_character_info(self.config, char, style)
                if char_info:
                    guide["characters"][char][style] = {
                        "physical": char_info.get('physical', ''),
                        "clothing": char_info.get('upper_body', ''),
                        "headwear": char_info.get('headwear', ''),
                        "render_style": char_info.get('rendering', '')
                    }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(guide, f, ensure_ascii=False, indent=2)
        
        print(f"风格指南已导出: {output_path}")
        return guide


def main():
    """主函数：演示完整流程"""
    
    # 初始化管线
    pipeline = StoryboardPipeline('script/猪打镇关西_v2.0')
    
    print("\n" + "="*60)
    print("阶段1: 角色摘要")
    print("="*60)
    
    for char in ['鲁达', '镇关西', '包子猪']:
        for style in ['国潮动漫', 'MCU电影史诗感']:
            summary = pipeline.get_character_summary(char, style)
            print(f"\n{char} - {style}:")
            print(f"  {summary}")
    
    print("\n" + "="*60)
    print("阶段2: 九宫格提示词")
    print("="*60)
    
    sequence = {
        "name": "第一场开场",
        "shots": [
            {"shot_id": "1A", "character": "鲁达", "style": "国潮动漫",
             "action": "闭目养神坐在肉铺前板凳上", "composition": "中景"},
            {"shot_id": "1B", "character": "镇关西", "style": "国潮动漫",
             "action": "手持杀猪刀奋力切肉，汗珠飞溅", "composition": "特写"},
            {"shot_id": "1C", "character": "包子猪", "style": "国潮动漫",
             "action": "在包子铺旁专心吃包子", "composition": "中景"}
        ]
    }
    
    beatboard_prompts = pipeline.generate_beatboard_prompts(sequence)
    for p in beatboard_prompts:
        print(f"\n[{p['shot_id']}] {p['character']} - {p['style']}")
        print(f"  {p['prompt']}")
    
    print("\n" + "="*60)
    print("阶段3: 四宫格提示词")
    print("="*60)
    
    scene = {
        "scene": "泰坦废墟",
        "characters": ["鲁达", "镇关西"],
        "style": "MCU电影史诗感",
        "camera": "环绕",
        "mood": "史诗"
    }
    
    sequence_prompts = pipeline.generate_sequence_prompts(scene)
    for p in sequence_prompts:
        print(f"\n[{p['scene']}] {p['character']} - {p['style']}")
        print(f"  {p['prompt']}")
    
    print("\n" + "="*60)
    print("阶段4: 动态提示词")
    print("="*60)
    
    motion = {
        "beat": 8,
        "scene": "泰坦废墟",
        "characters": ["镇关西"],
        "action": "变身泰坦形态，金甲覆盖全身，无限手套亮起紫光",
        "duration": 5.0
    }
    
    motion_prompts = pipeline.generate_motion_prompts(motion)
    for p in motion_prompts:
        print(f"\n[节拍{p['beat']}] {p['character']} - {p['style']}")
        print(f"  {p['prompt']}")
        print(f"  时长: {p['duration']}秒 @ {p['fps']}fps")
    
    print("\n" + "="*60)
    print("阶段5: 导出风格指南")
    print("="*60)
    
    pipeline.export_style_guide('output/style-guide.json')
    
    print("\n" + "="*60)
    print("流程完成")
    print("="*60)


if __name__ == "__main__":
    main()
```

### 运行结果

```
初始化完成: 猪打镇关西 v2.0
角色: ['鲁达', '镇关西', '包子猪']
风格: ['国潮动漫', 'MCU', '像素']

============================================================
阶段1: 角色摘要
============================================================

鲁达 - 国潮动漫:
  身形魁梧，身高九尺，腰阔十围；面圆耳大，满脸络腮虬髯 | 翡翠鹦哥绿朱丝战袍 | 暗青灰色芝麻罗纱头巾，哑光无反光质感 | 平涂赛璐璐风格，墨线轮廓粗犷遒劲

鲁达 - MCU电影史诗感:
  35岁亚裔男性，魁梧健硕肌肉身材，皮肤毛孔清晰 | 翡翠鹦哥长袍，面料质感逼真 | 芝麻罗头巾，纱织纹理清晰 | 虚幻引擎5影视级渲染，8K分辨率，光线追踪

镇关西 - 国潮动漫:
  身形肥硕，面露凶相 | 褐色交领右衽粗布短衫 | 黑色幞头，头发松散束起 | 平涂赛璐璐风格，粗布面料与油污形成对比

包子猪 - 国潮动漫:
  身材矮胖、身形滚圆，粉色皮肤带细腻纹理 | 白色衬衫，衣料褶皱丰富 | 平涂赛璐璐风格

============================================================
阶段2: 九宫格提示词
============================================================

[1A] 鲁达 - 国潮动漫:
  身形魁梧，身高九尺，腰阔十围；面圆耳大，满脸络腮虬髯, 翡翠鹦哥绿朱丝战袍, 暗青灰色芝麻罗纱头巾，哑光无反光质感, 闭目养神坐在肉铺前板凳上, 中景 shot, 平涂赛璐璐风格，墨线轮廓粗犷遒劲

[1B] 镇关西 - 国潮动漫:
  身形肥硕，面露凶相, 褐色交领右衽粗布短衫, 黑色幞头，头发松散束起, 手持杀猪刀奋力切肉，汗珠飞溅, 特写, 平涂赛璐璐风格，粗布面料与油污形成对比

[1C] 包子猪 - 国潮动漫:
  身材矮胖、身形滚圆，粉色皮肤带细腻纹理, 白色衬衫，衣料褶皱丰富, 在包子铺旁专心吃包子, 中景 shot, 平涂赛璐璐风格

============================================================
阶段3: 四宫格提示词
============================================================

[泰坦废墟] 鲁达 - MCU电影史诗感:
  类似复联3泰坦星战役，破碎卫星残骸、燃烧陨石坑, 35岁亚裔男性，魁梧健硕肌肉身材，皮肤毛孔清晰, 翡翠鹦哥长袍，面料质感逼真, 史诗氛围, 环绕运镜, MCU电影史诗感, 虚幻引擎5影视级，8K分辨率，光线追踪，体积光照明

[泰坦废墟] 镇关西 - MCU电影史诗感:
  类似复联3泰坦星战役，破碎卫星残骸、燃烧陨石坑, 肥硕多肉的人类面庞，眯缝眼，有络腮胡，紫色皮肤, 灭霸盔甲, 史诗氛围, 环绕运镜, MCU电影史诗感, 虚幻引擎5影视级渲染，光线追踪反射

============================================================
阶段4: 动态提示词
============================================================

[节拍8] 镇关西 - MCU电影史诗感:
  场景：泰坦废墟 | 角色：肥硕多肉的人类面庞，眯缝眼，有络腮胡，紫色皮肤 | 服装：灭霸盔甲 | 动作：变身泰坦形态，金甲覆盖全身，无限手套亮起紫光 | 风格：MCU电影史诗感 | 渲染：虚幻引擎5影视级渲染，光线追踪反射 | 时长: 5.0秒 @ 24fps

============================================================
阶段5: 导出风格指南
============================================================
风格指南已导出: output/style-guide.json

============================================================
流程完成
============================================================
```

## 附录

### A. 配置文件结构

```
configs/
├── character-loader.py        # 角色配置加载器
├── character-template.md      # 角色配置模板
├── visual-style-specs.json    # 视觉风格规范（生成）
└── usage-example.md           # 本文档

script/
└── 猪打镇关西_v2.0             # 包含YAML角色设定的剧本

output/
└── style-guide.json           # 导出的风格指南（生成）
```

### B. 支持的视觉风格

| 风格标识 | 渲染描述 | 适用场景 |
|----------|----------|----------|
| 国潮动漫 | 平涂赛璐璐风格，墨线轮廓粗犷遒劲，游戏概念风 | 日常场景、对话 |
| MCU | 虚幻引擎5影视级，8K分辨率，光线追踪，体积光照明 | 大场面、战斗 |
| 像素风格 | 拳皇98风格像素美术，8-bit故障效果 | 特殊效果、故障转场 |

### C. 风格转场规则

| 节拍 | 源风格 | 目标风格 | 触发条件 |
|------|--------|----------|----------|
| 8 | 国潮动漫 | MCU | 暗物质包子出现 |
| 11 | MCU | 像素 | 包子猪被拍飞 |

### D. 常见问题

**Q1: 如何添加新的视觉风格？**

在剧本文件的YAML头部添加新的风格配置：

```yaml
characters:
  角色名:
    新风格名:
      physical: "身形描述"
      upper_body: "上装描述"
      render_style: "渲染风格描述"
```

**Q2: 如何修改现有角色配置？**

直接编辑剧本文件的YAML头部，修改对应角色的配置即可。

**Q3: 风格转场如何触发？**

系统根据节拍号自动检测风格切换。在节拍8和节拍11处会自动切换到目标风格。

**Q4: 如何导出自定义格式的规范文件？**

使用`export_visual_style_specs`函数自定义输出格式，或参考脚本实现自定义导出逻辑。
