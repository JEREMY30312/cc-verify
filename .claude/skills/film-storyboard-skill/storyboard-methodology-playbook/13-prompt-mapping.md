# AI出图提示词映射（影视语言 → Prompt语言）

## 提示词模块化组合原则
- 将提示词分为独立模块，清晰组合：
  - 构图/景别模块：决定取景范围
  - 机位/角度模块：决定视角
  - 镜头效果模块：决定空间感
  - 光影氛围模块：决定情绪基调
  - 主体描述模块：决定画面内容
  - 动作/姿态模块：决定瞬间状态
  - 风格模块：决定美术风格
- 各模块独立描述，便于替换调整
- 模块顺序建议：风格 → 景别 → 角度 → 主体 → 动作 → 光影 → 氛围

## 景别词（Shot Size）
- extreme wide shot / establishing shot / 极远景：环境全貌，人物极小
- wide shot / long shot / 远景：交代环境与人物位置关系
- full shot / 全景：人物全身可见
- medium full shot / 中全景：膝部以上
- medium shot / 中景：腰部以上
- medium close-up / 中近景：胸部以上
- close-up / 近景：肩部以上，聚焦面部表情
- extreme close-up / 极特写：眼睛、嘴唇、手指等细节

## 机位与角度词（Camera Angle）
- eye level / 平视：中性自然
- high angle / 俯拍：弱势、渺小、受压迫
- low angle / 仰拍：强势、威严、高大有力
- bird's eye view / 鸟瞰：正上方俯视
- worm's eye view / 虫视角：极低仰视
- Dutch angle / tilted angle / 荷兰角：倾斜地平线，不安紧张
- POV / subjective shot / first person view / 主观视角：代入角色视角
- over-the-shoulder shot / 过肩镜头：对话常用

## 镜头效果词（Lens Effect）
- wide angle lens / 24mm / 广角镜头：透视夸张，空间纵深强
- telephoto lens / 85mm / 135mm / 长焦镜头：空间压缩，背景拉近
- fisheye lens / 鱼眼镜头：边缘弧形畸变
- tilt-shift / 移轴效果：微缩景观感
- shallow depth of field / bokeh / 浅景深：背景模糊，突出主体
- deep focus / 深焦：前后景都清晰
- motion blur / 运动模糊：暗示速度与动势
- lens flare / 镜头光晕：电影感

## 光影与氛围词（Lighting & Mood）

### 硬光/高反差类
- hard lighting / 硬光
- high contrast / 高反差
- chiaroscuro / 明暗法
- dramatic lighting / 戏剧性光影

### 柔光/暖色类
- soft lighting / 柔光
- diffused light / 漫射光
- warm tone / warm color temperature / 暖色调
- golden hour / magic hour / 黄金时段

### 冷色/压抑类
- cold tone / cool tone / 冷色调
- blue hour / 蓝调时刻
- moonlight / 月光
- overcast / 阴天光

### 光源方向类
- front lighting / 正面光
- side lighting / 侧光
- backlighting / backlit / 逆光
- rim lighting / 轮廓光
- top lighting / 顶光
- under lighting / 底光

### 氛围关键词
- volumetric light / god rays / 体积光
- fog / mist / haze / 雾气
- dust particles / 尘埃颗粒
- rain / 雨
- smoke / 烟雾
- neon light / 霓虹灯
- candlelight / 烛光

## 情绪词（Mood / Emotion）
- tense / suspenseful / 紧张
- melancholic / somber / 忧郁
- serene / peaceful / 宁静
- dramatic / intense / 戏剧性
- ominous / foreboding / 不祥
- hopeful / optimistic / 充满希望
- nostalgic / 怀旧
- eerie / unsettling / 诡异
- romantic / 浪漫
- energetic / dynamic / 充满活力

## 动作与姿态词（Action & Pose）
- dynamic pose / action pose / 动态姿势
- static pose / 静态姿势
- running / walking / jumping / 跑/走/跳
- fighting / combat / 战斗
- falling / 坠落
- frozen moment / peak action / 定格瞬间
- impact moment / 撞击瞬间
- wind-blown hair / clothes / 风吹头发/衣服
- silhouette / 剪影

## 构图词（Composition）
- rule of thirds / 三分法构图
- centered composition / center framing / 居中构图
- diagonal composition / 对角线构图
- frame within frame / 框中取景
- leading lines / 引导线
- negative space / 留白
- symmetrical composition / 对称构图
- asymmetrical composition / 不对称构图
- foreground framing / 前景框架

## 风格词（Visual Style）
- photorealistic / hyperrealistic / 真人写实
- cinematic / film still / 电影感
- anime style / 动漫风格
- illustration / 插画风格
- oil painting / 油画风格
- vintage / retro film / 复古胶片
- noir / 黑色电影
- cyberpunk / 赛博朋克
- fantasy / 奇幻
- minimalist / 极简主义

## 提示词写法说明
- 本附录提供影视术语到英文关键词的对照
- 完整的提示词写法指南和示例请参考 gemini-image-prompt-guide/index.md
- Gemini 图像生成采用叙事描述式（完整段落），而非关键词堆叠式
