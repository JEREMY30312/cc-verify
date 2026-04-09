---
name: animator-skill
description: 动画师技能。用于将静态分镜（Beat Board 九宫格 + Sequence Board 四宫格）转化为图生视频的动态提示词（Motion Prompt）。每组包含 5 个 Motion Prompt（1 关键帧 + 4 四宫格），共 9 组 45 个。
---

# 动画师技能

[技能说明]
    动画师技能，用于将静态分镜转化为图生视频的动态提示词。基于 motion-prompt-methodology/ 中的方法论，为每个关键帧和四宫格展开生成简洁、具体、可执行的 Motion Prompt。每组包含 5 个 Motion Prompt（1 关键帧 + 4 四宫格），共 9 组 45 个。

[文件结构]
     animator-skill/
     ├── SKILL.md                               # 技能包核心配置
     ├── motion-prompt-methodology/              # 动态提示词方法论（已拆分）
     │   └── index.md                           # 入口文件
     ├── film-storyboard-skill/templates/motion-prompt-template/       # 动态提示词模板（已拆分）
     │   └── index.md                           # 入口文件
     ├── physics-verification-rules.md           # 物理验证规则库
     └── montage-engine/                        # 可选：蒙太奇逻辑引擎模块
         ├── montage-analysis.md
         ├── rhythm-curve-generator.md
         └── creative-suggestions.md
<!-- LOG:STEP read=.claude/skills/animator-skill/motion-prompt-methodology/index.md,.claude/skills/animator-skill/physics-verification-rules.md,.claude/skills/animator-skill/montage-engine/index.md,module=analyzer_modules -->


[功能]
    [生成动态提示词]
        [生成动态提示词]
    **第一步：创意引擎调用**
        - 调用蒙太奇逻辑引擎分析动作序列
        - 输入参数：
          - Markdown: outputs/sequence-board-prompt-{集数}-board*.md（四宫格提示词）
          - Markdown: outputs/beat-breakdown-{集数}.md（节拍情绪曲线）
          - Markdown: outputs/beat-board-prompt-{集数}.md（视觉风格参考）
          - ⚠️ [V4.1-CRITICAL] JSON: outputs/sequence-board-data-{集数}.json
            - 读取 boards数组获取所有分镜板
            - 读取 cards数组获取每个镜头的数据
            - 读取 cross_grid_continuity获取跨格连续性评分
            - 用于：动态提示词的继承关系建立、物理验证的上下文检查
            - ⚠️ 如JSON不存在：立即停止，报错要求重新执行 /sequence
        - 输出：创意动作建议，包括：
          - 情绪匹配的运动类型
          - 节奏变化建议
          - 环境互动创意
          - 风格化处理方案

<!-- LOG:STEP read=outputs/sequence-board-prompt-{集数}-board*.md,outputs/beat-breakdown-{集数}.md,outputs/beat-board-prompt-{集数}.md,outputs/sequence-board-data-{集数}.json,engines=montage_logic,algorithm=motion_analysis,output=creative_suggestions -->

    **第二步：五模块构造**
        - 严格按照5个模块构造提示词：
          1. **镜头运动模块**（1-2种运动）
            - 选择与情绪匹配的运动类型
            - 检查运动组合不超过2种
            - 示例：Slow dolly in with subtle tilt up

          2. **主体动作模块**（1-2种动作）
            - 主要动作（必须）
            - 次要动作（可选）
            - 检查动作逻辑链是否连贯
            - 示例：Turns head while reaching out hand

          3. **环境动态模块**（必须包含）
            - 根据场景选择适当的环境动态
            - 检查动态是否服务叙事
            - 避免过度复杂的环境干扰
            - 示例：Dust particles floating in sunbeam

          4. **节奏控制模块**（新增）
            - 设计速度梯度：缓入/匀速/爆发/衰减
            - 分配时间比例：各阶段持续时间
            - 设置节奏点：高潮时刻的强调
            - 示例：Gradual acceleration over 2s, hold for 1s, then rapid deceleration

          5. **氛围强化模块**（新增）
            - 通过运动强化情绪
            - 添加风格化运动效果
            - 设置技术参数
            - 示例：Cinematic 24fps with subtle handheld shake

         - 每个模块必须包含具体参数，避免模糊描述

<!-- LOG:STEP algorithm=five_module_construction,camera_motion,body_motion,environment_dynamic,rhythm_control,atmosphere_enhancement,output=motion_prompts,note=5模块必须包含具体参数 -->

     **第三步：物理合理性检查**
         - 调用 physics-verification-rules.md
         - 逐项检查物理合理性：
           1. 重力影响检查
           2. 惯性表现检查
           3. 材质反应检查
           4. 能量守恒检查
           5. 流体动力学检查
         - 标记物理异常项：
           - ✅ 合理：通过检查
           - ⚠️ 轻微异常：艺术化处理，需标注
           - ❌ 物理错误：必须修正
         - 生成物理检查报告

<!-- LOG:STEP read=.claude/skills/animator-skill/physics-verification-rules.md,algorithm=physics_verification,check_gravity=true,check_inertia=true,check_material=true,check_energy=true,check_fluid=true,output=physics_report,note=5项物理检查 -->

    **第四步：占位格特殊处理**
        - 识别九宫格中的占位格（PH-标记）
        - 对占位格生成"建议动态方案"而非完整提示词
        - 方案格式：
          ```
          [PH-1-5]: [建议镜头运动]，[建议主体动作]，
                    [基于上下文的动态建议]，[节奏建议]，[氛围建议]
          （待用户确认后填充完整）
          ```
        - 明确标注"待用户确认"

    **第五步：输出与标注**
        - Markdown 输出：
          - 保存为 outputs/motion-prompt-{集数}.md
          - 格式：
            ```
            1-0: [镜头运动]，[主体动作]，[环境动态]，[节奏控制]，[氛围强化]
            ```
          - 附加信息：物理检查状态、创意来源说明、异常处理建议
        - ⚠️ [V4.1-CRITICAL] JSON 输出：
          - 保存为 outputs/motion-prompt-data-{集数}.json
          - 包含：boards数组、motion_groups（每组5个）、physics_verification
          - 用途：review阶段必须读取（字段级验证）
          - 生成规则：9组×5个 = 45个 Motion Prompt
          - 验证：物理检查状态必须完整记录，五模块合规性=100%
          - 格式：严格按照 motion-prompt-template.md Schema

    **第六步：质量审核（可选）**
        - 自检清单：
          □ 5个模块是否齐全？
          □ 物理合理性是否通过？
          □ 占位格是否妥善处理？
          □ 与分镜是否匹配？
        - 如发现问题，返回对应步骤修正

    [修改动态提示词]
        第一步：理解修改意见
            - 读取原 motion-prompt.md
            - 读取修改意见
            - 读取 motion-prompt-methodology/index.md

        第二步：执行修改
            - 定位需要修改的格
            - 按修改意见调整，确保符合方法论
            - 更新原文档

[动态提示词原则]
    - **方法论遵循原则**：
        • motion-prompt-methodology/ 全局生效
        • 所有动态提示词必须符合方法论中的规则与验收标准

    - **上下文继承原则**：
        • 动态提示词必须基于分镜的叙事目的与情绪（来自 beat-breakdown.md）
        • 动作设计必须与分镜画面内容匹配

    - **模板遵循原则**：
        • 必须严格遵循 film-storyboard-skill/templates/motion-prompt-template/ 格式
        • 每组 5 个（1 关键帧 + 4 四宫格），共 9 组

[注意事项]
    - motion-prompt-methodology/ 是核心方法论，必须严格遵守
    - templates/ 中的格式是必须遵循的
    - 提示词输出时，直接给可复制的文本块，不要拆成碎片解释


---

## [参考文档]

    animator-skill 依赖以下模块和文件：

    ### 内部模块
    - **motion-prompt-methodology/** - 动态提示词方法论核心
    - **templates/** - 输出格式模板（继承自 film-storyboard-skill）
    - **physics-verification-rules.md** - 物理验证规则库
    - **montage-engine/** - 蒙太奇逻辑引擎模块

    ### 外部依赖
    - **.claude/common/quality-check.md** - 质量检查清单（用于自检）
    - **film-storyboard-skill/templates/** - 动态提示词模板（继承自 film-storyboard-skill）

    ### 输出文件规范
    - 输出文件命名：motion-prompt-{集数}.md
    - 格式规范：见 film-storyboard-skill/templates/motion-prompt-template/
    - 物理验证：见 physics-verification-rules.md
