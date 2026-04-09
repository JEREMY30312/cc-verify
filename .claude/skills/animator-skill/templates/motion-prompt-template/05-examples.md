# 完整示例

## 示例1：标准提示词

1-0: Slow dolly in, subject turns head toward camera, hair flowing gently in breeze with dust particles floating in sunlight, gradual acceleration over 2 seconds then hold, cinematic 24fps with subtle motion blur
物理检查：✅ 通过 - 运动连贯，环境动态合理

## 示例2：动作场景

2-0: Quick zoom out while panning left, character jumps backward, clothing flaps vigorously and debris flies upward, sudden burst of speed then rapid decay, dynamic action shot with motion blur
物理检查：⚠️ 艺术处理 - 跳跃高度增加30%增强表现力，为动作风格

## 示例3：占位格建议

PH-1-5: Slow push in to close-up, subject reveals hidden object, based on: previous frame shows searching, next frame shows reaction, building tension before reveal, mysterious low-key lighting
（待用户确认后填充完整）

## 与相关文件的引用关系

- **引用 motion-prompt-methodology/**：五模块结构，环境动态词汇库
- **引用 physics-verification-rules.md**：物理检查规则和标注格式
- **被 animator-skill/SKILL.md 调用**：生成动态提示词步骤使用本模板
- **兼容 storyboard-methodology-playbook/**：保持与分镜方法论的一致性

## 使用注意事项

1. **模块完整性**：确保每个Motion Prompt包含5个模块
2. **物理合理性**：所有提示词必须通过物理检查
3. **占位格处理**：占位格必须明确标注，等待用户确认
4. **一致性检查**：确保与分镜的视觉风格和叙事节奏一致
5. **创意与规则平衡**：在遵循物理规则的同时保持艺术表现力
