# 四宫格提示词执行器 Sequence Executor

[用途]
    调用四宫格提示词任务时使用此模板
    确保按正确的顺序读取所有必要模块

[执行前必须读取的文件]

    ## 第一组：配置和输入
    1. .agent-state.json
       - 位置：项目根目录
       - 作用：获取 visual_style, target_medium, aspect_ratio, episode_id

    2. 九宫格总览
       - 位置：outputs/beat-board-prompt-{集数}.md
       - 作用：整体视觉风格参考

    3. 九宫格分板
       - 位置：outputs/beat-board-prompt-{集数}-board*.md
       - 作用：每个格子的详细描述

    ## 第二组：核心分析模块
    4. common/coherence-checker.md ← 【必读】
       - 作用：连贯性检查
       - 检查项：
         * 与九宫格的一致性继承
         * 屏幕方向/视线/轴线稳定
         * 动作连续性
         * 剪接风险检查

    5. film-storyboard-skill/templates/sequence-board-template.md ← 【必读】
       - 作用：输出格式模板
       - 必须按模板结构生成

[执行步骤]

    步骤1: 读取项目配置
    ```
    读取 .agent-state.json
    提取：visual_style, target_medium, aspect_ratio, episode_id
    ```

    步骤2: 读取九宫格提示词
    ```
    读取 outputs/beat-board-prompt-{集数}.md（总览）
    读取 outputs/beat-board-prompt-{集数}-board*.md（分板）
    继承：视觉风格、角色外观、场景要素、光色基调
    ```

    步骤3: 读取分析模块
    ```
    读取 common/coherence-checker.md
    理解连贯性检查规则
    读取 film-storyboard-skill/templates/sequence-board-template.md
    理解输出格式要求
    ```

    步骤4: 生成四宫格提示词
    ```
    按 sequence-board-template.md 格式：
    - 默认结构：起—承—转—合
    - 动作戏结构：预备→出手→命中/受击→反应/余势
    - 格数可变：2/4/6格按复杂度选择
    - 每格必须继承对应九宫格的：人物/场景/光色描述
    - 发生变化必须显式说明原因（换装、受伤、天气变化等）
    ```

    步骤5: 执行连贯性检查
    ```
    读取 common/coherence-checker.md
    逐项检查：
    □ 是否继承九宫格对应格的人物/场景/光色？
    □ 变化是否有明确原因说明？
    □ 屏幕方向/视线/轴线是否稳定？
    □ 越轴是否有过渡手段？
    □ 是否存在跳接风险？
    □ 动作轨迹是否合理？
    ```

    步骤6: 修正并重检（如需要）
    ```
    检查不通过 → 返回步骤4修正 → 重新检查
    ```

    步骤7: 保存输出
    ```
    输出文件：outputs/sequence-board-prompt-{集数}.md
    ```

[Prompt 模板]

    ## 四宫格提示词 Prompt 模板

    你是一名专业的影视分镜师，请执行四宫格提示词生成任务。

    **项目配置**（来自 .agent-state.json）：
    - 视觉风格：{visual_style}
    - 目标媒介：{target_medium}
    - 画幅比例：{aspect_ratio}
    - 集数：{episode_id}

    **执行前必须读取以下文件**：
    1. common/coherence-checker.md ← 连贯性检查
    2. film-storyboard-skill/templates/sequence-board-template.md ← 输出格式

    **前置产物**（来自九宫格提示词）：
    {九宫格提示词内容}

    **执行要求**：
    1. 读取并理解 coherence-checker.md 的连贯性规则
    2. 读取 sequence-board-template.md 的格式要求
    3. 为每个九宫格格子生成四宫格提示词：
       - 默认结构：起—承—转—合
       - 动作戏结构：预备→出手→命中/受击→反应/余势
       - 格数：2/4/6格按复杂度选择
    4. 继承九宫格对应格的所有要素：
       - 人物外观/服装状态
       - 场景要素/环境设定
       - 光色基调/氛围
    5. 发生变化必须显式说明原因（换装、受伤、天气变化等）
    6. 执行 coherence-checker.md 连贯性检查
    7. 确保屏幕方向、轴线、视线稳定

    **输出文件**：
    outputs/sequence-board-prompt-{集数}.md

    请开始执行四宫格提示词生成。
