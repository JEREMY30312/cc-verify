# 占位格处理规范

## 占位格识别
- 格式：`PH-{组编号}-{位置编号}`
- 示例：`PH-1-5`（第1组第5个占位格）
- 来源：九宫格中的未确定帧或需要用户确认的帧

## 建议方案格式
[占位格标识]: [建议镜头运动]，[建议主体动作]，[基于上下文的动态建议]，[节奏建议]，[氛围建议]
（待用户确认后填充完整）

## 上下文引用要求
1. **前后帧连贯性**：基于前后帧的动作和节奏
2. **整体叙事节奏**：匹配节拍的情绪曲线
3. **视觉风格统一**：保持一致的视觉风格
4. **不确定性标注**：明确标注不确定部分

## 占位格示例
PH-1-5: Slow push in to close-up, subject reveals hidden object, based on: previous frame shows searching, next frame shows reaction, building tension before reveal, mysterious low-key lighting
（待用户确认后填充完整）

PH-3-2: Whip pan transition, character turns abruptly, based on: need for rapid scene transition, sudden jarring change, disorienting handheld feel
（待用户确认后填充完整）

## 占位格处理流程
1. **识别**：在九宫格中标记占位格位置
2. **分析**：基于上下文推断可能内容
3. **建议**：生成2-3个动态方案选项
4. **标注**：明确标注"待用户确认"
5. **等待**：暂停流程，等待用户输入
6. **填充**：用户确认后生成完整提示词
