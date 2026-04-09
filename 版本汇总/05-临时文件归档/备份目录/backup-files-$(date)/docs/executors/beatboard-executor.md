# 九宫格提示词执行器 Beatboard Executor

[用途]
    调用九宫格提示词任务时使用此模板
    确保按正确的顺序读取所有必要模块

[执行前必须读取的文件]

    ## 第一组：配置和输入
    1. .agent-state.json
       - 位置：项目根目录
       - 作用：获取 visual_style, target_medium, aspect_ratio, episode_id

    2. 节拍拆解表
       - 位置：outputs/beat-breakdown-{集数}.md
       - 作用：关键帧选择的基础

    3. 导演决策参数（可选）
       - 位置：common/director-decision.md
       - 作用：获取导演预设参数

    ## 第二组：核心分析模块
    4. common/keyframe-selector.md ← 【必读】
       - 作用：关键帧选择逻辑
       - 关键规则：
         * 基础选点：从节拍拆解中选取9个叙事拐点
         * 动态扩展：每检测到1个氛围转折点 → 增加1个关键帧
         * 动作强化：重大动作节拍可拆分为2-3个关键帧
         * 最大限制：单板不超过16个关键帧

    5. common/layout-calculator.md ← 【必读】
       - 作用：布局计算逻辑
       - 关键规则：
         * 每板固定9格（3×3网格）
         * 关键帧数量 > 9 时自动分板
         * 最后一板不足9格用占位格填充

    6. film-storyboard-skill/templates/beat-board-template.md ← 【必读】
       - 作用：输出格式模板
       - 必须按模板结构生成

    7. common/coherence-checker.md ← 【必读】
       - 作用：连贯性检查
       - 检查项：
         * 角色外观一致性
         * 服装状态连续性
         * 光线/时间连续性
         * 空间关系稳定性

[执行步骤]

    步骤1: 读取项目配置
    ```
    读取 .agent-state.json
    提取：visual_style, target_medium, aspect_ratio, episode_id
    ```

    步骤2: 读取节拍拆解表
    ```
    读取 outputs/beat-breakdown-{集数}.md
    识别：关键节拍列表、综合权重、关键帧等级
    ```

    步骤3: 读取分析模块
    ```
    读取 common/keyframe-selector.md
    理解关键帧选择规则
    读取 common/layout-calculator.md
    理解布局计算规则
    读取 film-storyboard-skill/templates/beat-board-template.md
    理解输出格式要求
    ```

    步骤4: 执行关键帧选择
    ```
    按 keyframe-selector.md 规则：
    - 从节拍拆解中选择关键帧
    - 特级关键帧（🔴）必须入选
    - 高级关键帧（🟠）按需入选
    - 动态扩展：氛围转折点增加关键帧
    - 动作强化：重大动作拆分为多帧
    ```

    步骤5: 计算布局
    ```
    按 layout-calculator.md 规则：
    - 计算每板关键帧数量
    - 确定分板数
    - 选择布局类型（3×3标准网格）
    ```

    步骤6: 生成九宫格提示词
    ```
    按 film-storyboard-skill/templates/beat-board-template.md 格式：
    - 每板9个格子
    - 继承节拍拆解的视觉风格
    - 包含：场景描述、镜头类型、画面要素、情绪基调
    ```

    步骤7: 执行连贯性检查
    ```
    读取 common/coherence-checker.md
    逐项检查：
    □ 角色外观描述是否一致
    □ 服装描述是否一致
    □ 光源位置是否一致
    □ 场景布局是否一致
    ```

    步骤8: 修正并重检（如需要）
    ```
    检查不通过 → 返回步骤6修正 → 重新检查
    ```

    步骤9: 保存输出
    ```
    总览文件：outputs/beat-board-prompt-{集数}.md
    分板文件：outputs/beat-board-prompt-{集数}-board{##}.md
    ```

[Prompt 模板]

    ## 九宫格提示词 Prompt 模板

    你是一名专业的影视分镜师，请执行九宫格提示词生成任务。

    **项目配置**（来自 .agent-state.json）：
    - 视觉风格：{visual_style}
    - 目标媒介：{target_medium}
    - 画幅比例：{aspect_ratio}
    - 集数：{episode_id}

    **执行前必须读取以下文件**：
    1. common/keyframe-selector.md ← 核心选择模块
    2. common/layout-calculator.md ← 布局计算模块
    3. film-storyboard-skill/templates/beat-board-template.md ← 输出格式
    4. common/coherence-checker.md ← 连贯性检查

    **前置产物**（来自节拍拆解表）：
    {节拍拆解表内容}

    **执行要求**：
    1. 读取并理解 keyframe-selector.md 的关键帧选择规则
    2. 读取 layout-calculator.md 的布局计算规则
    3. 从节拍拆解中选择关键帧：
       - 特级关键帧（🔴）必须入选
       - 高级关键帧（🟠）按需入选
       - 氛围转折点增加关键帧
       - 重大动作可拆分为多帧
    4. 计算布局，确定分板数（每板9格）
    5. 按 beat-board-template.md 格式生成九宫格提示词
    6. 执行 coherence-checker.md 连贯性检查
    7. 继承节拍拆解的视觉风格和角色设定

    **输出文件**：
    - outputs/beat-board-prompt-{集数}.md（总览）
    - outputs/beat-board-prompt-{集数}-board{##}.md（分板）

    请开始执行九宫格提示词生成。
