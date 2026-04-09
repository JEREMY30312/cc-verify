# 审核执行器 Review Executor

[用途]
    调用审核任务时使用此模板
    确保按正确的顺序读取所有必要模块

[执行前必须读取的文件]

    ## 第一组：配置和输入
    1. .agent-state.json
       - 位置：项目根目录
       - 作用：获取 episode_id

    2. 待审核文件
       - breakdown: outputs/beat-breakdown-{集数}.md
       - beatboard: outputs/beat-board-prompt-{集数}.md + 分板
       - sequence: outputs/sequence-board-prompt-{集数}.md
       - motion: outputs/motion-prompt-{集数}.md
       - all: 所有上述文件

    3. 剧本原文（可选，用于建立整体理解）
       - 位置：script/*.md

    4. 上游产物（用于一致性检查）
       - 例如：审核九宫格时读取节拍拆解表

    ## 第二组：审核基准模块
    5. storyboard-review-skill/review-checklist.md ← 【必读】
       - 作用：验收清单
       - 节拍拆解验收、Beat Board验收、Sequence Board验收、Motion Prompt验收

    6. storyboard-review-skill/uncertainty-judgment-protocol.md ← 【必读】
       - 作用：不确定项判定
       - 判定条件：
         * 创意与规则冲突但可能有效
         * 多方案各有优劣
         * 技术限制导致效果不确定
         * 用户创意指令与最佳实践冲突

    7. storyboard-review-skill/asset-consistency-rules.md ← 【按需】
       - 作用：资产一致性规则
       - 检查项：
         * 角色面部一致性
         * 服装状态连续性
         * 环境资产一致性
         * 风格统一性

    8. storyboard-methodology-playbook/index.md ← 【按需】
       - 作用：分镜方法论
       - 用于分镜内容审核

    9. motion-prompt-methodology/index.md ← 【按需仅 motion】
       - 作用：动态提示词方法论
       - 用于动态提示词审核

[执行步骤]

    步骤1: 收集基本信息
    ```
    确定审核类型：breakdown/beatboard/sequence/motion/all
    确定集数标识
    确定板号（如适用）
    ```

    步骤2: 读取基准文件
    ```
    读取 storyboard-review-skill/review-checklist.md
    读取 storyboard-review-skill/uncertainty-judgment-protocol.md
    如适用：读取 asset-consistency-rules.md
    如适用：读取 storyboard-methodology-playbook/index.md
    如 motion：读取 motion-prompt-methodology/index.md
    ```

    步骤3: 建立整体理解
    ```
    读取剧本原文（如需要）
    读取节拍拆解表（如存在）
    读取九宫格提示词（如存在）
    读取四宫格提示词（如存在）
    读取动态提示词（如存在）
    ```

    步骤4: 读取待审核内容
    ```
    按审核类型读取对应文件
    ```

    步骤5: 执行逐项检查
    ```
    按 review-checklist.md 验收清单逐项检查：

    节拍拆解验收：
    □ 完整性：覆盖完整叙事弧线
    □ 完整性：未遗漏关键转折点
    □ 清晰性：每个节拍的叙事目的明确
    □ 清晰性：节拍强度标注合理
    □ 选点：锚点覆盖关键拐点类型

    Beat Board验收：
    □ 清晰：九张能讲清故事主线与关键拐点
    □ 清晰：每格的镜头目的明确
    □ 覆盖：未缺关键转折/高潮/结果
    □ 一致性：人物外观/服装状态统一
    □ 可用性：每格足够清晰，能作为四宫格参考

    Sequence Board验收：
    □ 动作与因果：起手—推进—冲突—落点清楚
    □ 一致性：继承九宫格的人物/场景/光色
    □ 连贯性：屏幕方向/视线/轴线稳定
    □ 节奏与张力：段落内部有张弛与呼吸

    Motion Prompt验收：
    □ 结构完整：每组包含5个（1关键帧+4四宫格）
    □ 简洁性：50-200字符之间
    □ 聚焦性：只聚焦2-3个核心元素
    □ 具体性：使用具体物理动作
    □ 运动限制：镜头/主体运动不超过2种
    ```

    步骤6: 执行新增维度检查（如适用）
    ```
    资产一致性审核（asset-consistency-rules.md）：
    □ 角色面部一致性
    □ 服装状态连续性
    □ 环境资产一致性
    □ 风格统一性

    关键帧合理性审核：
    □ 剧情匹配度
    □ 构图有效性
    □ 氛围传达有效性

    创意融合度审核：
    □ 创意引擎建议自然融入
    □ 用户创意指令妥善执行
    ```

    步骤7: 执行不确定项判定
    ```
    按 uncertainty-judgment-protocol.md 判定：
    1. 识别潜在不确定项
    2. 生成决策选项：
       - 选项A：保持创意，标注风险
       - 选项B：按规则修改
       - 选项C：生成替代方案
    3. 推荐选项及理由
    ```

    步骤8: 生成审核报告
    ```
    审核结论：
    - PASS：全部验收项通过
    - FAIL：存在必须修改的问题
    - UNCERTAIN：存在不确定项，需要用户决策

    报告内容：
    - 项目信息
    - 审核结论
    - 详细审核（逐项检查结果）
    - 亮点评价
    - 修订建议（如需要）
    - 不确定项决策选项（如需要）

    保存到：outputs/{产物类型}-{集数}-review.md
    ```

[Prompt 模板]

    ## 审核任务 Prompt 模板

    你是一名专业的导演，请执行审核任务。

    **审核配置**：
    - 审核类型：{审核类型}
    - 集数：{集数}
    - 板号：{板号（如适用）}

    **执行前必须读取以下文件**：
    1. storyboard-review-skill/review-checklist.md ← 验收清单
    2. storyboard-review-skill/uncertainty-judgment-protocol.md ← 不确定项判定
    3. storyboard-review-skill/asset-consistency-rules.md ← 资产一致性（按需）

    **待审核内容**：
    {待审核文件内容}

    **上游产物**（用于一致性检查）：
    {上游产物内容}

    **执行要求**：
    1. 读取并理解 review-checklist.md 的验收标准
    2. 读取 uncertainty-judgment-protocol.md 的判定规则
    3. 按验收清单逐项检查待审核内容
    4. 执行资产一致性审核（如适用）
    5. 执行关键帧合理性审核
    6. 执行创意融合度审核
    7. 执行不确定项判定
    8. 生成审核报告

    **审核结论**：
    - PASS：全部验收项通过
    - FAIL：存在必须修改的问题
    - UNCERTAIN：存在不确定项，需要用户决策

    **输出文件**：
    outputs/{产物类型}-{集数}-review.md

    请开始执行审核任务。
