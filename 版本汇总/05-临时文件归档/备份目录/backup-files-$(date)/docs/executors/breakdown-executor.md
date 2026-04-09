# 节拍拆解执行器 Breakdown Executor

[用途]
    调用节拍拆解任务时使用此模板
    确保按正确的顺序读取所有必要模块

[执行前必须读取的文件]

    ## 第一组：配置和输入
    1. .agent-state.json
       - 位置：项目根目录
       - 作用：获取 visual_style, target_medium, aspect_ratio, episode_id

    2. script/猪打镇关西_v2.0 ← 【新增】
       - 位置：script/猪打镇关西_v2.0
       - 作用：获取标准化的角色设定和场景信息
       - 读取方式：从文件开头的 YAML 区块提取
       - 关键信息：characters, scenes, rendering_styles, style_transitions

    3. configs/character-loader.py ← 【新增】
       - 作用：从剧本提取角色设定的工具模块
       - 功能：extract_character_settings(), get_character_info()

    4. 剧本文件
       - 位置：script/*-{集数}.md
       - 作用：节拍分析的基础内容

    3. common/director-decision.md (如存在)
       - 作用：获取导演预设参数（可选）

    ## 第二组：核心分析模块
    4. common/beat-analyzer.md ← 【必读】
       - 作用：节拍分析逻辑
       - 关键规则：
         * 三幕结构比例：15-25% / 50-70% / 15-25%
         * 节拍数量：8-12个为宜
         * 关键帧等级：🔴/🟠/🟡/🔵/⚪

    5. film-storyboard-skill/templates/beat-breakdown-template.md ← 【必读】
       - 作用：输出格式模板
       - 必须按模板结构生成

    ## 第三组：质量检查
    6. common/quality-check.md
       - 作用：节拍拆解质量检查清单
       - 生成后必须逐项自检

[执行步骤]

    步骤1: 读取项目配置
    ```
    读取 .agent-state.json
    提取：visual_style, target_medium, aspect_ratio, episode_id
    ```

    步骤2: 读取剧本内容和角色设定
    ```
    读取 script/猪打镇关西_v2.0
    提取 YAML 区块的角色设定（characters, scenes等）
    读取剧本正文（YAML区块之后的内容）
    ```

    步骤3: 使用角色设定生成节拍拆解
    ```
    从角色设定中提取：
    - 角色外观信息（头饰、服装、配饰等）
    - 渲染风格（国潮动漫、MCU、像素）
    - 场景细节（宋代集市、肉铺等）
    - 风格转换点（节拍8、11）
    ```

    步骤4: 在节拍描述中使用角色设定
    ```
    每个节拍生成时：
    - 引用角色外观：{character_info['headwear']}
    - 引用渲染风格：{character_info['render_style']}
    - 引用场景细节：{scene_info['description']}
    ```

    步骤5: 执行节拍分析
    ```
    按 beat-analyzer.md 规则：
    - 识别最小叙事单元
    - 标注节拍类型和权重
    - 计算综合权重和关键帧等级
    - 确保三幕结构完整
    ```

    步骤6: 生成节拍拆解表
    ```
    按 film-storyboard-skill/templates/beat-breakdown-template.md 格式：
    - 填写所有必要字段
    - 包括：场景描述、角色行动、情感表达
    - 包含统计分析和权重曲线
    ```

    步骤7: 质量自检
    ```
    读取 common/quality-check.md
    逐项检查：
    □ 三幕比例符合标准
    □ 节拍数量在 8-12 范围内
    □ 叙事完整性（有开篇、发展、高潮、结局）
    □ 每个节拍有明确的场景描述
    □ 每个节拍有清晰的角色行动
    □ 每个节拍有具体的情感表达
    ```

    步骤8: 修正并重检（如需要）
    ```
    自检不通过 → 返回步骤5修正 → 重新自检
    ```

    步骤9: 保存输出
    ```
    保存到 outputs/beat-breakdown-{集数}.md
    ```

[Prompt 模板]

    ## 节拍拆解 Prompt 模板

    你是一名专业的影视分镜师，请执行节拍拆解任务。

    **角色设定信息**（来自剧本YAML区块）：
    ```json
    {
      "characters": {
        "鲁达": {
          "国潮动漫": {
            "physical": "身形魁梧，身高九尺...",
            "headwear": "暗青灰色芝麻罗纱头巾...",
            "upper_body": "翡翠鹦哥绿朱丝战袍..."
          }
        }
      },
      "scenes": {
        "宋代集市": "热闹非凡的传统市集氛围"
      },
      "rendering_styles": {
        "国潮动漫": "平涂赛璐璐风格..."
      }
    }
    ```

    **项目配置**（来自 .agent-state.json）：
    - 视觉风格：{visual_style}
    - 目标媒介：{target_medium}
    - 画幅比例：{aspect_ratio}
    - 集数：{episode_id}

    **执行前必须读取以下文件**：
    1. common/beat-analyzer.md ← 核心分析模块
    2. film-storyboard-skill/templates/beat-breakdown-template.md ← 输出格式
    3. common/quality-check.md ← 质量检查

    **剧本内容**：
    {剧本内容}

    **执行要求**：
    1. 读取并理解 beat-analyzer.md 的节拍分析规则
    2. 读取 beat-breakdown-template.md 的格式要求
    3. 从剧本中识别关键叙事节拍（8-12个为宜）
    4. 应用三幕结构：15-25% / 50-70% / 15-25%
    5. 每个节拍必须包含：
       - 场景描述：发生了什么
       - 角色行动：具体动作和意图
       - 情感表达：核心情绪
       - 叙事功能：世界观建立/诱因事件/高潮对抗等
    6. 计算综合权重和关键帧等级
    7. 在节拍描述中使用剧本中的角色外观和渲染风格设定
    8. 引用场景细节时使用标准化的场景描述
    9. 执行 quality-check.md 自检
    10. 按模板格式输出节拍拆解表

    **输出文件**：
    outputs/beat-breakdown-{集数}.md

    请开始执行节拍拆解。
