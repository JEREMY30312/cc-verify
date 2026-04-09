# Gemini 特有参数说明

## 画幅比例（Aspect Ratio）
- 可用比例：1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9
- 16:9：标准宽银幕，适合大多数影视分镜
- 21:9：超宽银幕，适合史诗感建立镜头
- 9:16：竖屏，适合移动端短视频
- 在提示词中可用自然语言描述："Horizontal widescreen format" 或 "Vertical portrait orientation"

## 分辨率（仅 Gemini 3 Pro / Nano Banana Pro）
- 1K（默认）：约 1024px
- 2K：约 2048px
- 4K：约 4096px
- 高分辨率适合需要放大查看细节的场景

## 模型选择建议

**Gemini 2.5 Flash Image（Nano Banana）：**
- 速度快、成本低
- 适合快速迭代、批量生成
- 分辨率最高 1024px

**Gemini 3 Pro Image Preview（Nano Banana Pro）：**
- 质量更高、支持复杂指令
- 内置 Thinking 过程优化构图
- 支持 Google Search 实时信息
- 支持最高 4K 分辨率
- 适合最终成品输出
